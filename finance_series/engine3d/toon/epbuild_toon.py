"""Toon episode builder (Karl series).
python3 epbuild_toon.py <ep> tts|timeline|stills|render|audio|mux|srt|all
python3 epbuild_toon.py <ep> dub <lang>          (lang file: <ep>/lang/<lang>.json = list of strings, one per EN line)
python3 epbuild_toon.py <ep> short <n>           (SHORTS in <ep>/ep.py)
Episode file: finance_series/<ep>/ep.py with META, LINES (see karl01/ep.py)."""
import sys, os, json, copy, hashlib, subprocess, wave, importlib.util, re
from concurrent.futures import ThreadPoolExecutor
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); FS = os.path.join(HERE, "..", ".."); ROOT = os.path.abspath(os.path.join(FS, ".."))
VDIR = os.path.join(ROOT, "finance02", "voice")
SR, FPS = 44100, 30
GAP, GAP_BEAT, LEAD = 0.24, 0.65, 0.35
sys.path.insert(0, os.path.join(FS, "engine"))

# voice: (model, speaker, pitch factor, extra length factor)
VOICES = {
    "en": {"n": ("en_US-ryan-high", None, 1.0, 1.0), "karl": ("en_US-ryan-high", None, 1.12, 0.97), "max": ("en_US-ryan-high", None, 1.2, 0.95),
           "dad": ("en_US-ryan-high", None, 0.9, 1.0), "sales": ("en_US-ryan-high", None, 0.96, 0.9), "guru": ("en_US-ryan-high", None, 1.04, 0.9),
           "ortiz": ("en_US-ryan-high", None, 0.88, 1.05), "principal": ("en_US-amy-medium", None, 0.92, 1.0), "kid": ("en_US-ryan-high", None, 1.25, 0.95),
           "mom": ("en_US-amy-medium", None, 1.0, 1.0), "lena": ("en_US-amy-medium", None, 1.08, 1.0), "mia": ("en_US-amy-medium", None, 1.22, 0.95),
           "grandma": ("en_US-amy-medium", None, 0.9, 1.1)},
    "es": {"n": ("es_ES-davefx-medium", None, 1.0, 1.0), "_f": ("es_MX-claude-high", None, 1.0, 1.0)},
    "pt-BR": {"n": ("pt_BR-faber-medium", None, 1.0, 1.0), "_f": ("pt_BR-faber-medium", None, 1.22, 1.0)},
    "de": {"n": ("de_DE-thorsten-high", None, 1.0, 1.0), "_f": ("de_DE-kerstin-low", None, 1.0, 1.0)},
    "fr": {"n": ("fr_FR-tom-medium", None, 1.0, 1.0), "_f": ("fr_FR-siwis-medium", None, 1.0, 1.0)},
    "uk": {"n": ("uk_UA-ukrainian_tts-medium", 1, 1.0, 1.0), "_f": ("uk_UA-ukrainian_tts-medium", 0, 1.0, 1.0)},
}
FEMALE = {"mom", "lena", "mia", "grandma", "principal"}
PITCH = {"karl": 1.1, "max": 1.17, "dad": 0.9, "ortiz": 0.88, "kid": 1.22, "mia": 1.15, "grandma": 0.92, "lena": 1.04}

def voice_for(lang, v):
    tab = VOICES[lang]
    if v in tab: return tab[v]
    base = tab["_f"] if v in FEMALE else tab["n"]
    return (base[0], base[1], base[2] * PITCH.get(v, 1.0), base[3])

def load(ep):
    spec = importlib.util.spec_from_file_location(ep + "_ep", os.path.join(FS, ep, "ep.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def bdir(ep, *sub):
    d = os.path.join(FS, ep, "build", *sub); os.makedirs(d, exist_ok=True); return d

def read_wav(p):
    with wave.open(p) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768; sr = w.getframerate(); ch = w.getnchannels()
    if ch == 2: a = a.reshape(-1, 2).mean(1)
    if sr != SR: a = np.interp(np.arange(0, len(a) * SR / sr) * sr / SR, np.arange(len(a)), a).astype(np.float32)
    return a

def write_wav(p, a):
    a = np.clip(a, -1, 1)
    with wave.open(p, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((a * 32767).astype(np.int16).tobytes())

def trim(a, thr=0.01):
    idx = np.where(np.abs(a) > thr)[0]
    if not len(idx): return a
    return a[max(0, idx[0] - int(0.03 * SR)): idx[-1] + int(0.06 * SR)]

# ------------------------------------------------------------------ TTS
UK_NUM = {}
def prep_text(lang, text):
    if lang == "uk":
        text = text.replace("«", "").replace("»", "").replace("“", "").replace("”", "").replace('"', "").lower()
        text = re.sub(r"[^а-яіїєґ'’ ,.!?:;\-—́]", " ", text)
    return text

def synth(lang, text, v, speed, cache):
    model, spk, pitch, lf = voice_for(lang, v)
    key = hashlib.md5(f"{lang}|{text}|{v}|{speed}|{model}|{spk}|{pitch}|{lf}".encode()).hexdigest()[:14]
    p = os.path.join(cache, key + ".wav")
    if not os.path.exists(p):
        raw = p + ".raw.wav"; ls = lf / speed
        cmd = ["piper", "--model", os.path.join(VDIR, model + ".onnx"), "--output_file", raw, "--length_scale", f"{ls:.3f}", "--sentence_silence", "0.12"]
        if spk is not None: cmd += ["--speaker", str(spk)]
        subprocess.run(cmd, input=prep_text(lang, text).encode(), check=True, capture_output=True)
        if pitch != 1.0:
            with wave.open(raw) as w: sr = w.getframerate()
            af = f"asetrate={int(sr * pitch)},aresample={sr},atempo={1 / pitch:.4f}"
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", raw, "-af", af, p], check=True); os.remove(raw)
        else: os.replace(raw, p)
    return trim(read_wav(p))

def tts(ep, m, lang="en", texts=None):
    cache = bdir(ep, "tts"); speed = m.META.get("speed", 1.1)
    texts = texts or [l["t"] for l in m.LINES]
    jobs = [(lang, t, l["v"], speed, cache) for t, l in zip(texts, m.LINES)]
    with ThreadPoolExecutor(4) as ex: return list(ex.map(lambda j: synth(*j), jobs))

# ------------------------------------------------------------------ timeline
CARRY = ("set", "grade", "chars", "crowd", "crowdbars", "crowdpose", "props", "bars", "cam")
def char_dict(c, prev=None):
    if isinstance(c, dict):
        d = dict(prev or {}); d.update(c)
        if "walk" in c:
            d["from"] = c.get("from") or [d.get("x", 0), d.get("z", 0)]
            d["x"], d["z"] = c["walk"]
        return d
    x, z, ry, pose, emo = c[:5]; look = list(c[5]) if len(c) > 5 else [0, 0]
    return {"x": x, "z": z, "ry": ry, "pose": pose, "emo": emo, "look": look}

def resolve(m):
    state = {"set": "void", "grade": None, "chars": {}, "crowd": None, "crowdbars": False, "crowdpose": None, "props": [], "bars": {}, "cam": "wide"}
    out = []
    for i, l in enumerate(m.LINES):
        prev_bars = dict(state["bars"])
        if "set" in l and l["set"] != state["set"]:   # new location: only the people/props/bars this line names
            state["chars"] = {}; state["bars"] = {}; state["props"] = []
            if "crowd" not in l: state["crowd"] = None
            if "crowdbars" not in l: state["crowdbars"] = False
        for k, v in l.items():
            if k in ("t", "v", "beat"): continue
            if k == "chars":
                for cid, c in v.items():
                    if c is None: state["chars"].pop(cid, None)
                    else:
                        d = char_dict(c, state["chars"].get(cid))
                        state["chars"][cid] = d
            elif k == "bars":
                if v == {}: state["bars"] = {}
                else:
                    for bid, b in v.items():
                        if b is None: state["bars"].pop(bid, None)
                        else: state["bars"][bid] = b
            elif k in CARRY: state[k] = copy.deepcopy(v)
        s = copy.deepcopy(state)
        for k in ("rc", "pill", "card", "fx", "tvframe", "locker", "empty", "shadows", "phone"):
            if k in l: s[k] = l[k]
        # chars that walked: next line starts where they ended
        out.append({"t": l["t"], "v": l["v"], "beat": l.get("beat"), "s": s, "prevBars": prev_bars})
        for cid, c in state["chars"].items():
            if "walk" in c: c.pop("walk", None); c.pop("from", None); c["pose"] = c.get("pose", "idle")
    return out

def timeline(ep, m, vo):
    res = resolve(m); t = LEAD; lines = []
    for i, (r, a) in enumerate(zip(res, vo)):
        if i and r["beat"]: t += GAP_BEAT - GAP
        d = len(a) / SR
        s = r["s"]; hold = 0.0
        if s.get("card"): hold = max(hold, 3.2 - d if s["card"]["k"] not in ("sub",) else 2.6 - d)
        if s.get("rc"): hold = max(hold, 2.4 - d)
        if "punch" in s.get("fx", []) or "silence" in s.get("fx", []): hold = max(hold, 0.5)
        hold = max(hold, 1.5 - d, 0)
        lines.append({"start": round(t, 3), "vo": round(t + 0.04, 3), "len": round(d, 3), "end": round(t + d + hold + GAP, 3), **r})
        t += d + hold + GAP
    speech_end = round(t + 0.6, 3); dur = round(speech_end + m.META.get("end_screen", 15), 3)
    lines[-1]["end"] = speech_end
    tl = {"lines": lines, "speech_end": speech_end, "dur": dur}
    json.dump(tl, open(os.path.join(bdir(ep), "timeline.json"), "w"))
    return tl

# ------------------------------------------------------------------ audio
def tone(f0, f1, d, amp, decay=3.0):
    n = int(d * SR); tt = np.arange(n) / SR
    return (np.sin(2 * np.pi * np.cumsum(np.linspace(f0, f1, n)) / SR) * amp * np.exp(-tt * decay / d)).astype(np.float32)
def noise(d, amp, decay=4.0, seed=0):
    n = int(d * SR); r = np.random.default_rng(seed).normal(0, 1, n).astype(np.float32); tt = np.arange(n) / SR
    return np.convolve(r, np.ones(8) / 8, "same").astype(np.float32) * amp * np.exp(-tt * decay / d)

def sfx_track(tl):
    N = int((tl["dur"] + 2) * SR); out = np.zeros(N, np.float32)
    def put(t, a): i = int(t * SR); out[i:i + len(a)] += a[:max(0, N - i)]
    prev_set = None
    for ln in tl["lines"]:
        s, t0 = ln["s"], ln["start"]
        if s["set"] != prev_set and prev_set is not None: put(t0, noise(0.35, 0.05, 6, 7))   # scene whoosh
        prev_set = s["set"]
        for f in s.get("fx", []):
            k = f.split(":")[0]
            if k == "ping": put(t0 + 0.1, tone(700, 1500, 0.35, 0.22)); put(t0 + 0.12, tone(1500, 1500, 0.25, 0.08))
            if k == "pingall":
                for j in range(9): put(t0 + 0.15 + j * 0.07, tone(1100 + j * 70, 1300 + j * 70, 0.12, 0.08))
            if k == "punch": put(t0, noise(0.25, 0.12, 5, 3)); put(t0, tone(120, 50, 0.3, 0.35))
            if k == "thud": put(t0 + 0.45, tone(90, 40, 0.5, 0.6))
            if k == "buzz": put(t0 + 0.2, tone(140, 110, 0.45, 0.25, 1.5))
            if k in ("coin", "gold"):
                put(t0 + 0.4, tone(1320, 1320, 0.1, 0.15)); put(t0 + 0.5, tone(1760, 1760, 0.35, 0.15))
            if k in ("sparkle", "hearts", "glow"):
                for j in range(4): put(t0 + 0.3 + j * 0.09, tone(2000 + j * 300, 2100 + j * 300, 0.2, 0.05))
            if k == "sting": put(t0, tone(220, 180, 1.2, 0.3, 1.2)); put(t0, tone(233, 190, 1.2, 0.2, 1.2))
            if k == "whisper": put(t0, noise(1.4, 0.06, 1.5, 11))
            if k == "laugh":
                for j in range(14): put(t0 + 0.1 + j * 0.11, tone(300 + (j % 4) * 60, 260, 0.1, 0.05))
        if s.get("rc"):
            for j in range(10 if s["rc"].get("long") else 6): put(t0 + 0.5 + j * 0.1, tone(2400, 2200, 0.03, 0.08))
        if s.get("card") and s["card"]["k"] == "sub": put(t0 + 1.6, tone(900, 900, 0.06, 0.2)); put(t0 + 1.68, tone(1300, 1300, 0.15, 0.15))
    return out

def mix_track(ep, m, tl, vo_parts, lang="en"):
    """vo_parts: list of (time, samples)."""
    N = int((tl["dur"] + 2) * SR); vo = np.zeros(N, np.float32)
    for t, a in vo_parts: i = int(t * SR); vo[i:i + len(a)] += a[:max(0, N - i)]
    vo = vo / max(1e-6, np.abs(vo).max()) * 0.9
    from build import music
    mp = os.path.join(bdir(ep), "music.wav")
    if not os.path.exists(mp): music(tl["dur"] + 1, mp, seed=m.META.get("music_seed", 4))
    mu = read_wav(mp); mu = np.pad(mu, (0, max(0, N - len(mu))))[:N]
    act = np.convolve((np.abs(vo) > 0.02).astype(np.float32), np.ones(int(0.4 * SR)) / int(0.4 * SR), "same")
    gain = 0.20 * (1 - 0.55 * np.clip(act, 0, 1))
    for ln in tl["lines"]:   # dip the music on "silence" lines
        if "silence" in ln["s"].get("fx", []): i0, i1 = int(ln["start"] * SR), int(ln["end"] * SR); gain[i0:i1] *= 0.15
    se = int(tl["speech_end"] * SR); gain[se:] = 0.32
    out = vo + sfx_track(tl)[:N] * 0.55 + mu * gain
    fade = int(2.5 * SR); end = int(tl["dur"] * SR); out[end - fade:end] *= np.linspace(1, 0, fade); out[end:] = 0
    out = out / np.abs(out).max() * 0.92
    p = os.path.join(bdir(ep), f"mix_{lang}.wav"); write_wav(p, out[:end]); return p

# ------------------------------------------------------------------ render
def render(ep, tl, workers=4):
    d = bdir(ep, "chunks"); dur = tl["dur"]; n = workers * 3; step = dur / n
    q = f"episode.html?tl=finance_series/{ep}/build/timeline.json"
    jobs = [(i, round(i * step, 3), round(min(dur, (i + 1) * step), 3)) for i in range(n)]
    def run(j):
        i, a, b = j; out = os.path.join(d, f"c{i:02d}.mp4")
        if os.path.exists(out) and os.path.getsize(out) > 1000: return out
        tmp = out + ".tmp.mp4"
        subprocess.run(["node", os.path.join(HERE, "rep.js"), q, "video", tmp, str(a), str(b)], check=True); os.replace(tmp, out); return out
    with ThreadPoolExecutor(workers) as ex: outs = list(ex.map(run, jobs))
    lst = os.path.join(d, "list.txt"); open(lst, "w").write("".join(f"file '{o}'\n" for o in outs))
    vid = os.path.join(bdir(ep), "video.mp4")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", vid], check=True)
    return vid

def stills(ep, tl, every=1):
    ts = [round((l["start"] + l["end"]) / 2, 2) for l in tl["lines"][::every]]
    d = bdir(ep, "stills"); q = f"episode.html?tl=finance_series/{ep}/build/timeline.json"
    chunks = [ts[i::4] for i in range(4)]
    def run(c): subprocess.run(["node", os.path.join(HERE, "rep.js"), q, "stills", d, ",".join(map(str, c))], check=True)
    with ThreadPoolExecutor(4) as ex: list(ex.map(run, chunks))
    return d

def srt_time(t): h = int(t // 3600); m_ = int(t % 3600 // 60); s = t % 60; return f"{h:02d}:{m_:02d}:{int(s):02d},{int((s % 1) * 1000):03d}"
def srt(ep, tl, texts=None, lang="en"):
    out = []
    for i, ln in enumerate(tl["lines"]):
        txt = (texts or [l["t"] for l in tl["lines"]])[i]
        out.append(f"{i + 1}\n{srt_time(ln['vo'])} --> {srt_time(ln['vo'] + max(1.0, ln['len']))}\n{txt}\n")
    p = os.path.join(FS, ep, f"captions_{lang}.srt"); open(p, "w").write("\n".join(out)); return p

def mux(ep, m, tl, wav, out):
    vid = os.path.join(bdir(ep), "video.mp4")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", vid, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "23",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out], check=True)

def fit_dub(tl, parts):
    """Place each dubbed line at the EN line start; speed it up (max 1.35x) if it would run into the next line."""
    out = []
    for i, (ln, a) in enumerate(zip(tl["lines"], parts)):
        nxt = tl["lines"][i + 1]["vo"] if i + 1 < len(tl["lines"]) else tl["speech_end"]
        room = nxt - ln["vo"] - 0.08; d = len(a) / SR
        if d > room:
            r = min(1.35, d / room)
            a = tempo(a, r)
        out.append((ln["vo"], a))
    return out

def tempo(a, r):
    import tempfile; d = tempfile.mkdtemp(); p = os.path.join(d, "i.wav"); q = os.path.join(d, "o.wav")
    write_wav(p, a); subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", p, "-af", f"atempo={r:.4f}", q], check=True); return read_wav(q)

if __name__ == "__main__":
    ep, cmd = sys.argv[1], sys.argv[2]; m = load(ep)
    if cmd in ("tts", "timeline", "all", "audio", "srt", "stills", "render", "mux"):
        vo = tts(ep, m); tl = timeline(ep, m, vo)
        print("lines", len(tl["lines"]), "speech", tl["speech_end"], "dur", tl["dur"], "min", round(tl["dur"] / 60, 2))
    if cmd in ("stills",): print(stills(ep, tl, int(sys.argv[3]) if len(sys.argv) > 3 else 1))
    if cmd in ("audio", "all", "mux"): wav = mix_track(ep, m, tl, [(l["vo"], a) for l, a in zip(tl["lines"], vo)]); print(wav)
    if cmd in ("srt", "all"): print(srt(ep, tl))
    if cmd in ("render", "all"): print(render(ep, tl))
    if cmd in ("mux", "all"): out = os.path.join(FS, ep, m.META["file"]); mux(ep, m, tl, wav, out); print(out)
    if cmd == "short":
        sh = m.SHORTS[int(sys.argv[3])]; tl = json.load(open(os.path.join(bdir(ep), "timeline.json")))
        t0 = max(0, tl["lines"][sh["a"]]["start"] - 0.2); t1 = tl["lines"][sh["b"]]["end"]
        env = dict(os.environ, SHORT=json.dumps({"title": sh["title"], "t0": t0, "t1": t1}))
        q = f"episode.html?tl=finance_series/{ep}/build/timeline.json&w=1080&h=1920"; vid = os.path.join(bdir(ep), sh["name"] + "_v.mp4")
        if len(sys.argv) > 4 and sys.argv[4] == "stills":
            subprocess.run(["node", os.path.join(HERE, "rep.js"), q, "stills", bdir(ep, "short_stills"), ",".join(str(round(t0 + f * (t1 - t0), 2)) for f in (0.02, 0.3, 0.6, 0.97)), "renderShort"], check=True, env=env); sys.exit()
        subprocess.run(["node", os.path.join(HERE, "rep.js"), q, "video", vid, str(t0), str(t1), "renderShort"], check=True, env=env)
        out = os.path.join(FS, ep, sh["name"] + ".mp4"); wav = os.path.join(bdir(ep), "mix_en.wav")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", vid, "-ss", str(t0), "-t", str(t1 - t0), "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "23", "-preset", "medium",
                        "-af", f"afade=t=out:st={t1 - t0 - 0.8:.2f}:d=0.8,loudnorm=I=-14:TP=-1.5", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out], check=True)
        print(out)
    if cmd == "dub":
        lang = sys.argv[3]; texts = json.load(open(os.path.join(FS, ep, "lang", lang + ".json")))
        assert len(texts) == len(m.LINES), (len(texts), len(m.LINES))
        tl = json.load(open(os.path.join(bdir(ep), "timeline.json")))
        parts = tts(ep, m, lang, texts); wav = mix_track(ep, m, tl, fit_dub(tl, parts), lang)
        d = os.path.join(FS, ep, "audio"); os.makedirs(d, exist_ok=True); out = os.path.join(d, f"{lang}.m4a")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wav, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "160k", out], check=True)
        print(out, srt(ep, tl, texts, lang))
