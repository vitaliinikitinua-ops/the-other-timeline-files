"""Karl #02 full episode: python3 build_ep.py tts|stills|render|mix|all
tts   -> build/vo/NNN.wav, build/ep_timing.json, captions_en.srt
stills-> build/stills (2 frames per line, contact sheets)
render-> build/video.mp4 (3 parallel chunks)   mix -> music+SFX+VO -> KARL02_Pay_In_4_Real_Price.mp4"""
import os, sys, re, json, subprocess, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); FS = os.path.join(HERE, ".."); ROOT = os.path.join(FS, "..")
sys.path.insert(0, os.path.join(FS, "engine")); TOON = os.path.join(FS, "engine3d", "toon")
B = os.path.join(HERE, "build"); VO = os.path.join(B, "vo"); os.makedirs(VO, exist_ok=True); SR = 44100
VOICE = os.path.join(ROOT, "finance02", "voice", "en_US-ryan-high.onnx")
PAGE = "toon_ep.html?ep=karl02"; FINAL = os.path.join(HERE, "KARL02_Pay_In_4_Real_Price.mp4"); END = 15.0
HOLD = {15: 0.6, 48: 0.4, 68: 0.4, 90: 0.9, 93: 0.5, 101: 0.5, 102: 0.6, 103: 0.5, 110: 0.7, 117: 0.6, 127: 0.9, 134: 0.6, 141: 0.4, 149: 0.8, 157: 0.5, 167: 0.5, 169: 0.9, 171: 0.6}

def lines():
    txt = open(os.path.join(HERE, "script.md")).read().split("---", 1)[1]; out, new_sec = [], False
    for l in txt.splitlines():
        if l.startswith("## "): new_sec = True; continue
        if not l.strip() or l.startswith(("#", "[")): continue
        out.append((l.strip(), new_sec)); new_sec = False
    return out

def speakable(s):
    s = s.replace("11:58", "eleven fifty-eight").replace("11:59", "eleven fifty-nine")
    s = re.sub(r"pay in 4", "pay in four", s, flags=re.I).replace("U.S.", "U.S.").replace("...", ",")
    return s.replace('"', "").replace("—", ",")

def read_wav(p):
    with wave.open(p) as w: a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768; sr = w.getframerate()
    return np.interp(np.arange(0, len(a), sr / SR), np.arange(len(a)), a).astype(np.float32)

def tts(voice, text, path, ls=1.0, extra=()):
    subprocess.run(["piper", "--model", voice, "--output_file", path, "--length_scale", str(ls), *extra], input=text.encode(), check=True, capture_output=True)
    a = read_wav(path); idx = np.where(np.abs(a) > 0.01)[0]
    return a[max(0, idx[0] - 400): idx[-1] + 2000] if len(idx) else a

def srt_time(t): h, m = int(t // 3600), int(t % 3600 // 60); s = t % 60; return f"{h:02d}:{m:02d}:{int(s):02d},{int((s % 1) * 1000):03d}"

def do_tts():
    L = lines(); spans, t = [], 0.4
    for i, (l, sec) in enumerate(L):
        if sec and i: t += 0.45
        a = tts(VOICE, speakable(l), os.path.join(VO, f"{i:03d}.wav"), 1.0); np.save(os.path.join(VO, f"{i:03d}.npy"), a)
        d = len(a) / SR; spans.append([round(t, 3), round(t + d, 3)]); t += d + 0.16 + HOLD.get(i, 0)
    end_start = t + 0.6; dur = end_start + END
    json.dump({"lines": spans, "endStart": round(end_start, 2), "dur": round(dur, 2)}, open(os.path.join(B, "ep_timing.json"), "w"))
    with open(os.path.join(HERE, "captions_en.srt"), "w") as f:
        for i, ((l, _), (a, b)) in enumerate(zip(L, spans)): f.write(f"{i+1}\n{srt_time(a)} --> {srt_time(b + 0.1)}\n{l}\n\n")
    words = sum(len(l.split()) for l, _ in L); print(f"{len(L)} lines, {words} words, VO end {t/60:.2f} min, total {dur/60:.2f} min, {words/(sum(b-a for a,b in spans)/60):.0f} wpm")

def do_stills():
    TM = json.load(open(os.path.join(B, "ep_timing.json"))); ts = []
    for a, b in TM["lines"]: ts += [a + 0.15, (a + b) / 2 + 0.3]
    ts += [TM["endStart"] + 2]
    sd = os.path.join(B, "stills"); subprocess.run(["rm", "-rf", sd])
    subprocess.run(["node", os.path.join(TOON, "rchunk.js"), PAGE, "stills", sd, ",".join(f"{t:.2f}" for t in ts)], check=True)
    from PIL import Image, ImageDraw
    fs = sorted(os.listdir(sd), key=lambda f: float(f[2:-4])); per = 24
    for s in range(0, len(fs), per):
        sheet = Image.new("RGB", (6 * 400, 4 * 225))
        for j, f in enumerate(fs[s:s + per]):
            im = Image.open(os.path.join(sd, f)).resize((400, 225)); ImageDraw.Draw(im).text((6, 4), f"{s//2 + j//2} {f[2:-4]}", fill=(255, 255, 0)); sheet.paste(im, ((j % 6) * 400, (j // 6) * 225))
        sheet.save(os.path.join(B, f"contact_{s // per:02d}.jpg"))
    print("sheets", (len(fs) + per - 1) // per)

def do_render(n=3):
    TM = json.load(open(os.path.join(B, "ep_timing.json"))); dur = TM["dur"]; cuts = [round(dur * k / n * 30) / 30 for k in range(n + 1)]
    ps = [subprocess.Popen(["node", os.path.join(TOON, "rchunk.js"), PAGE, os.path.join(B, f"chunk{k}.mp4"), str(cuts[k]), str(cuts[k + 1])]) for k in range(n)]
    for p in ps: p.wait()
    with open(os.path.join(B, "chunks.txt"), "w") as f: f.writelines(f"file 'chunk{k}.mp4'\n" for k in range(n))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(B, "chunks.txt"), "-c", "copy", os.path.join(B, "video.mp4")], check=True)

def tone(f0, f1, d, amp):
    n = int(d * SR); tt = np.arange(n) / SR; return (np.sin(2 * np.pi * np.cumsum(np.linspace(f0, f1, n)) / SR) * amp * np.exp(-tt * 3 / d)).astype(np.float32)
def noise(d, amp, lp=0.2):
    n = int(d * SR); x = np.random.default_rng(1).standard_normal(n).astype(np.float32); x = np.convolve(x, np.ones(5) / 5, "same"); return x * amp * np.linspace(1, 0, n)
SFX = {"ping": lambda: tone(900, 1500, 0.3, 0.25), "print": lambda: np.concatenate([tone(2400, 2200, 0.03, 0.12) for _ in range(10)] + [np.zeros(1)]),
       "pops": lambda: np.concatenate([np.pad(tone(700, 800, 0.08, 0.2), (0, int(0.07 * SR))) for _ in range(6)]), "merge": lambda: tone(200, 900, 0.5, 0.3),
       "flip": lambda: tone(300, 1800, 0.45, 0.3), "blip": lambda: tone(900, 1300, 0.12, 0.15), "pop": lambda: tone(500, 700, 0.1, 0.15), "whoosh": lambda: noise(0.4, 0.25)}

def mix_track(TM, vo_dir, ext=".npy", starts=None):
    dur = TM["dur"]; N = int(dur * SR) + SR; vo = np.zeros(N, np.float32)
    for i, (a, _) in enumerate(TM["lines"]):
        if starts: a = starts[i]
        p = os.path.join(vo_dir, f"{i:03d}{ext}")
        if os.path.exists(p):
            x = np.load(p); j = int(a * SR)
            if j < N: x = x[:N - j]; vo[j:j + len(x)] += x
    return vo, N

def do_mix(lang="en", starts=None):
    TM = json.load(open(os.path.join(B, "ep_timing.json"))); dur = TM["dur"]
    vo, N = mix_track(TM, VO if lang == "en" else os.path.join(B, "dub", lang), starts=starts)
    sfx = np.zeros(N, np.float32); evp = os.path.join(B, "events.json")
    if not os.path.exists(evp): subprocess.run(["node", os.path.join(TOON, "rchunk.js"), PAGE, "events", evp], check=True)
    for e in json.load(open(evp)):
        x = SFX[e["type"]](); j = int(e["t"] * SR); sfx[j:j + len(x)] += x[:max(0, N - j)]
    from build import music
    mp = os.path.join(B, "music.wav")
    if not os.path.exists(mp): music(dur, mp, seed=11)
    with wave.open(mp) as w: m = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768; ch = w.getnchannels()
    if ch == 2: m = m.reshape(-1, 2).mean(1)
    m = np.pad(m, (0, max(0, N - len(m))))[:N]
    x = (np.abs(vo) > 0.02).astype(np.float64); K = int(0.3 * SR); c = np.concatenate([[0], np.cumsum(x)]); act = np.zeros_like(x); idx = np.arange(len(x)); lo = np.clip(idx - K // 2, 0, len(x)); hi = np.clip(idx + K // 2, 0, len(x)); act = ((c[hi] - c[lo]) / K).astype(np.float32)
    out = vo + sfx * 0.5 + m * 0.2 * (1 - 0.55 * np.clip(act, 0, 1)); out = out / np.abs(out).max() * 0.9
    wp = os.path.join(B, f"mix_{lang}.wav")
    with wave.open(wp, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes())
    return wp

def do_final():
    wp = do_mix("en")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", os.path.join(B, "video.mp4"), "-i", wp, "-vf", "hqdn3d=4:3:5:5", "-c:v", "libx264", "-preset", "medium", "-crf", "28",
                    "-af", "loudnorm=I=-14:TP=-1.5", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", FINAL], check=True)
    print("->", FINAL)

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd in ("tts", "all"): do_tts()
    if cmd == "stills": do_stills()
    if cmd in ("render", "all"): do_render()
    if cmd in ("final", "all"): do_final()
