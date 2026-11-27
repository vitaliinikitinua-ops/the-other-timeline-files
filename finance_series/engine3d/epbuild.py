"""3D episode builder (16:9 long videos).
python3 epbuild.py epNN [tts|timeline|stills|render|audio|mux|all]  (stills: contact sheet; render: 4 parallel workers)
Episode file: finance_series/epNN/ep.py with META, BEATS=[(name, base_state, [S(...), ...]), ...], END, optional CAL/CHART.
State (set/bg/chars/props/cam/ov/caln) carries from sentence to sentence; chars merge per id (None hides)."""
import sys, os, json, copy, hashlib, subprocess, wave, importlib.util
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); FS = os.path.join(HERE, ".."); ROOT = os.path.join(FS, "..")
VOICE = os.path.join(ROOT, "finance02", "voice", "en_US-ryan-high.onnx")
SR, FPS, W, H = 44100, 30, 1920, 1080
LEAD, GAP, GAP_BEAT = 0.35, 0.34, 0.9
sys.path.insert(0, os.path.join(FS, "engine"))

def load(ep):
    spec = importlib.util.spec_from_file_location(ep + "_ep", os.path.join(FS, ep, "ep.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def bdir(ep):
    d = os.path.join(FS, ep, "build3d"); os.makedirs(os.path.join(d, "tts"), exist_ok=True); return d

def read_wav(p):
    with wave.open(p) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768; sr = w.getframerate(); ch = w.getnchannels()
    if ch == 2: a = a.reshape(-1, 2).mean(1)
    if sr != SR: a = np.interp(np.arange(0, len(a), sr / SR), np.arange(len(a)), a).astype(np.float32)
    return a

def write_wav(p, a):
    a = np.clip(a, -1, 1)
    with wave.open(p, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((a * 32767).astype(np.int16).tobytes())

# ------------------------------------------------------------------ sentences with resolved state
def sentences(m):
    out = []; state = {"set": "void", "bg": "#222244", "chars": {}, "props": [], "cam": ["wide"], "ov": [], "caln": 0}
    for bi, (name, base, sents) in enumerate(m.BEATS):
        state["caln"] = 0
        for key, v in base.items():
            if key == "chars": state["chars"] = {k: copy.deepcopy(c) for k, c in v.items() if c is not None}
            else: state[key] = copy.deepcopy(v)
        for si, s in enumerate(sents):
            for key, v in s.items():
                if key in ("sub", "spoken", "sfx", "voice"): continue
                if key == "chars":
                    for cid, c in v.items():
                        if c is None: state["chars"].pop(cid, None)
                        elif "who" in c: state["chars"][cid] = copy.deepcopy(c)
                        else: state["chars"].setdefault(cid, {}).update(c)
                else: state[key] = copy.deepcopy(v)
            d = copy.deepcopy(state); d.update(beat=name, bi=bi, si=si, sub=s["sub"], spoken=s["spoken"], sfx=s.get("sfx", []), voice=s.get("voice", "narrator"))
            out.append(d)
            state["ov"] = [o for o in state["ov"] if o["k"] not in ("title", "stamp") or o.get("hold")]   # one-sentence overlays
    return out

# ------------------------------------------------------------------ TTS
def tts(ep, m):
    bd = bdir(ep); ls = 1 / m.META.get("speed", 1.15); res = []
    for i, s in enumerate(sentences(m)):
        key = hashlib.md5((s["spoken"] + s["voice"] + f"{ls:.3f}").encode()).hexdigest()[:12]
        p = os.path.join(bd, "tts", key + ".wav")
        if not os.path.exists(p):
            raw = p + ".raw.wav"
            subprocess.run(["piper", "--model", VOICE, "--output_file", raw, "--length_scale", f"{ls:.3f}", "--sentence_silence", "0.05"],
                           input=s["spoken"].encode(), check=True, capture_output=True)
            if s["voice"] == "cashier":   # brighter, quicker voice for the Cashier
                subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", raw, "-af", "asetrate=22050*1.22,aresample=22050,atempo=0.9", p], check=True)
            elif s["voice"] == "karl":
                subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", raw, "-af", "asetrate=22050*1.07,aresample=22050,atempo=0.95", p], check=True)
            else: os.replace(raw, p)
            if os.path.exists(raw): os.remove(raw)
        res.append(p)
    return res

# ------------------------------------------------------------------ numbers for widgets (computed, not typed)
def card_curve(balance=1200, apr=None):
    if apr is None:
        import csv
        for r in csv.reader(open(os.path.join(FS, "data", "fred_TERMCBCCALLNS.csv"))):
            if r[0] == "2026-08-01": apr = float(r[1]) / 100
    bal, paid, pts = balance, 0.0, [(0, balance, 0.0)]; first = None
    while bal > 0.005:
        i = bal * apr / 12; p = min(max(25, bal * 0.01 + i), bal + i); first = first or p
        bal += i - p; paid += p; pts.append((len(pts), max(0, bal), paid))
    return {"apr": apr, "pts": pts, "first_min": first, "months": len(pts) - 1, "paid": paid, "interest": paid - balance}

# ------------------------------------------------------------------ timeline
def ovkey(o):
    if o["k"] in ("calendar", "chart", "paywith", "cards", "label", "tag", "counter", "split"): return o["k"] + o.get("side", "")
    return json.dumps(o, sort_keys=True)

def timeline(ep, m):
    bd = bdir(ep); files = tts(ep, m); S = sentences(m); t = LEAD; prev = None; ons = {}
    for i, (s, f) in enumerate(zip(S, files)):
        if prev is not None and s["bi"] != prev["bi"]: t += GAP_BEAT
        d = len(read_wav(f)) / SR
        s["t0"], s["sp0"], s["sp1"] = t, t + 0.08, t + 0.08 + d
        t = s["sp1"] + GAP; s["t1"] = t
        s["wav"] = os.path.relpath(f, bd)
        keys = {}
        for o in s["ov"]:
            k = ovkey(o)
            o["on"] = ons.get(k, s["t0"] + o.get("at", 0) * (s["t1"] - s["t0"]))
            keys[k] = o["on"]
        ons = keys
        for cid, c in s["chars"].items():   # pose transition from previous sentence
            pc = prev["chars"].get(cid) if prev else None
            c["from"] = pc.get("pose", "idle") if pc and pc.get("who") == c.get("who") else c.get("pose", "idle")
        for p in s["props"]:
            if p["k"] == "boxes":
                pp = [q for q in (prev["props"] if prev else []) if q["k"] == "boxes" and abs(q.get("x", 0) - p.get("x", 0)) < 0.01]
                p["prev"] = pp[0]["n"] if pp else p["n"]
        prev = s
    end = getattr(m, "END", {"seconds": 15}); total = t + 0.4 + end["seconds"]
    cc = card_curve()
    tl = {"fps": FPS, "w": W, "h": H, "total": total, "end_t0": t + 0.4, "end": end, "sents": S,
          "chart": {"pts": [[p[0], round(p[1], 2), round(p[2], 2)] for p in cc["pts"]], "apr": cc["apr"], "first_min": cc["first_min"]}}
    json.dump(tl, open(os.path.join(bd, "timeline.json"), "w"), indent=1)
    srt = []
    for i, s in enumerate(S, 1):
        f = lambda x: f"{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(x % 1 * 1000):03d}"
        srt.append(f"{i}\n{f(s['sp0'])} --> {f(s['sp1'])}\n{s['sub']}\n")
    open(os.path.join(FS, ep, "captions_en.srt"), "w").write("\n".join(srt))
    words = sum(len(s["spoken"].split()) for s in S)
    print(f"{ep}: {len(S)} sentences, {words} words, {total/60:.2f} min (incl. {end['seconds']} s end screen); "
          f"card: {cc['months']} months, interest ${cc['interest']:,.0f}, paid ${cc['paid']:,.0f}, first min ${cc['first_min']:.2f}")
    return tl

# ------------------------------------------------------------------ audio: VO + SFX + music
def synth(kind, rng):
    def tone(f0, f1, dur, amp=0.3, sq=False):
        n = int(dur * SR); tt = np.arange(n) / SR; ph = 2 * np.pi * np.cumsum(np.linspace(f0, f1, n)) / SR
        s = np.sign(np.sin(ph)) * 0.5 if sq else np.sin(ph); return (s * amp * np.exp(-tt * (3 / dur))).astype(np.float32)
    def noise(dur, amp, smooth=40):
        n = int(dur * SR); s = np.convolve(rng.randn(n), np.ones(smooth) / smooth, "same"); return (s * np.sin(np.linspace(0, np.pi, n)) ** 2 * amp * 3).astype(np.float32)
    cat = lambda *a: np.concatenate(a)
    if kind == "boom": return tone(90, 38, 0.7, 0.7)
    if kind == "thud": return tone(150, 70, 0.35, 0.55)
    if kind == "whoosh": return noise(0.45, 0.35)
    if kind == "rewind": return noise(0.9, 0.4, 20) + tone(1100, 180, 0.9, 0.2)
    if kind == "pop": return tone(500, 1300, 0.12, 0.3)
    if kind == "click": return tone(2500, 2000, 0.03, 0.35, True)
    if kind == "ding": return tone(1568, 1568, 0.5, 0.18) + tone(2093, 2093, 0.5, 0.08)
    if kind == "cash": return cat(tone(1320, 1320, 0.09, 0.2, True), tone(1760, 1760, 0.3, 0.2, True))
    if kind == "tick": return cat(*[cat(tone(900, 900, 0.03, 0.2, True), np.zeros(int(0.22 * SR), np.float32)) for _ in range(6)])
    if kind == "sad": return cat(tone(392, 392, 0.3, 0.15, True), tone(370, 370, 0.3, 0.15, True), tone(349, 349, 0.7, 0.15, True))
    if kind == "buzz": return tone(140, 140, 0.45, 0.25, True)
    if kind == "stamp": a = tone(70, 40, 0.4, 0.8); b = noise(0.12, 0.5, 5); a[:len(b)] += b; return a
    if kind == "thunk6": return cat(*[cat(tone(220, 110, 0.18, 0.45), np.zeros(int(0.17 * SR), np.float32)) for _ in range(6)])
    return np.zeros(1, np.float32)

def audio(ep, m):
    from build import music
    bd = bdir(ep); tl = json.load(open(os.path.join(bd, "timeline.json"))); N = int(tl["total"] * SR) + SR
    vo = np.zeros(N, np.float32); sfx = np.zeros(N, np.float32); stops = []; rng = np.random.RandomState(7)
    def put(buf, t, a): i0 = int(t * SR); buf[i0:i0 + len(a)] += a[:max(0, len(buf) - i0)]
    for s in tl["sents"]:
        put(vo, s["sp0"], read_wav(os.path.join(bd, s["wav"])))
        for tok in s["sfx"]:
            kind, _, at = tok.partition("@"); t = s["t0"] + (float(at) if at else 0) * (s["t1"] - s["t0"])
            if kind == "musicstop": stops.append(t); continue
            put(sfx, t, synth(kind, rng))
    mp = os.path.join(bd, "music.wav")
    if not os.path.exists(mp): music(tl["total"], mp, seed=m.META.get("music_seed", 1))
    mu = read_wav(mp)[:N]; mu = np.pad(mu, (0, N - len(mu)))
    env = np.ones(N, np.float32)
    for t in stops:   # music drops out for the twist, then fades back in
        i0 = int(t * SR); env[i0:i0 + int(2.5 * SR)] = 0.05; env[i0 + int(2.5 * SR):i0 + int(5 * SR)] = np.linspace(0.05, 1, int(2.5 * SR))
    act = np.convolve((np.abs(vo) > 0.015).astype(np.float32), np.ones(int(0.3 * SR)) / int(0.3 * SR), "same")
    mix = vo + sfx * 0.55 + mu * 0.16 * env * (1 - 0.55 * np.clip(act, 0, 1))
    mix = mix / max(1e-6, np.abs(mix).max()) * 0.92
    write_wav(os.path.join(bd, "mix.wav"), mix); print("audio ->", os.path.join(bd, "mix.wav"))

# ------------------------------------------------------------------ render / stills / mux
def server():
    import socket
    s = socket.socket()
    if s.connect_ex(("127.0.0.1", 8790)) != 0:
        subprocess.Popen(["python3", "-m", "http.server", "8790"], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        import time; time.sleep(1.5)

def render(ep, workers=4):
    server(); bd = bdir(ep)
    procs = [subprocess.Popen(["node", os.path.join(HERE, "render_ep.js"), ep, str(i), str(workers)]) for i in range(workers)]
    if any(p.wait() for p in procs): raise SystemExit("render failed")
    with open(os.path.join(bd, "chunks.txt"), "w") as f:
        for i in range(workers): f.write(f"file 'chunk_{i}.mp4'\n")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(bd, "chunks.txt"), "-c", "copy", os.path.join(bd, "video.mp4")], check=True)

def stills(ep, times=None):
    server(); bd = bdir(ep); tl = json.load(open(os.path.join(bd, "timeline.json")))
    if times is None: times = [round((s["t0"] + s["t1"]) / 2, 2) for s in tl["sents"]][::2] + [tl["end_t0"] + 3]
    subprocess.run(["node", os.path.join(HERE, "render_ep.js"), ep, "stills", ",".join(map(str, times))], check=True)
    from PIL import Image
    ims = [Image.open(os.path.join(bd, "stills", f"s_{i:03d}.jpg")).resize((480, 270)) for i in range(len(times))]
    sheet = Image.new("RGB", (480 * 6, 270 * ((len(ims) + 5) // 6)))
    for i, im in enumerate(ims): sheet.paste(im, ((i % 6) * 480, (i // 6) * 270))
    sheet.save(os.path.join(bd, "contact.jpg"), quality=85); print("contact sheet ->", os.path.join(bd, "contact.jpg"))

def mux(ep, m):
    bd = bdir(ep); out = os.path.join(FS, ep, m.META["file"])
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", os.path.join(bd, "video.mp4"), "-i", os.path.join(bd, "mix.wav"),
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", out], check=True)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out], capture_output=True, text=True).stdout)
    print(f"{ep}: {dur/60:.2f} min, {os.path.getsize(out)/1e6:.0f} MB -> {out}")

if __name__ == "__main__":
    ep, step = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "all"); m = load(ep)
    if step in ("tts", "timeline", "all"): timeline(ep, m)
    if step == "stills": stills(ep, [float(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else None)
    if step in ("audio", "all"): audio(ep, m)
    if step in ("render", "all"): render(ep)
    if step in ("mux", "all"): mux(ep, m)
