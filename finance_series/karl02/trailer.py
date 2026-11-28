"""Karl #02 trailer (~30 s): Piper VO + music bed + SFX, rendered with engine3d/toon/karl02_trailer.html.
python3 trailer.py [stills] -> karl02/TRAILER_karl02.mp4"""
import os, sys, json, subprocess, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); FS = os.path.join(HERE, ".."); ROOT = os.path.join(FS, "..")
sys.path.insert(0, os.path.join(FS, "engine"))
VOICE = os.path.join(ROOT, "finance02", "voice", "en_US-ryan-high.onnx"); OUT = os.path.join(HERE, "build"); SR = 44100
TOON = os.path.join(FS, "engine3d", "toon"); os.makedirs(OUT, exist_ok=True)
LINES = [("It's eleven fifty-eight on Black Friday night.", "n"), ("Pay in four. Just thirty dollars today.", "ad"),
         ("Then the button flickers.", "n"), ("One hundred twenty dollars. Six hours of your life.", "n"),
         ("Most people see pay in four. You see the real price.", "n"), ("Max's only fifty dollars? Twelve hundred.", "n"),
         ("Seven years. About two thousand two hundred seventy dollars.", "n"), ("Ten thousand people. One giant button.", "n"),
         ("What if every pay in four button showed you the real price?", "n")]

def tts(i, text, voice):
    raw, p = os.path.join(OUT, f"tr{i}_raw.wav"), os.path.join(OUT, f"tr{i}.wav")
    subprocess.run(["piper", "--model", VOICE, "--output_file", raw, "--length_scale", "0.88"], input=text.encode(), check=True, capture_output=True)
    af = "asetrate=22050*1.12,aresample=22050,atempo=1.0,aecho=0.6:0.4:30:0.25" if voice == "ad" else "anull"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", raw, "-af", af, p], check=True); os.remove(raw)
    with wave.open(p) as w: a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768; sr = w.getframerate()
    os.remove(p); return np.interp(np.arange(0, len(a), sr / SR), np.arange(len(a)), a).astype(np.float32)

vo = [tts(i, l, v) for i, (l, v) in enumerate(LINES)]
spans, t = [], 0.3
for j, a in enumerate(vo):
    d = len(a) / SR; hold = {3: 0.9, 5: 1.0, 6: 1.1, 7: 0.8}.get(j, 0.3)
    spans.append([round(t, 2), round(t + d + hold, 2)]); t += d + hold
spans[-1][1] = round(spans[-1][1] + 2.4, 2); dur = spans[-1][1] + 0.2
json.dump(spans, open(os.path.join(OUT, "trailer_timing.json"), "w"))
print("spans", spans, "dur", round(dur, 1))
if len(sys.argv) > 1 and sys.argv[1] == "stills":
    ts = ",".join(str(round((a + b) / 2, 2)) for a, b in spans) + "," + str(round(spans[2][0] + 1.0, 2))
    subprocess.run(["node", os.path.join(TOON, "rstill.js"), "karl02_trailer.html", os.path.join(OUT, "stills"), ts], check=True); sys.exit()
N = int(dur * SR) + SR; mix = np.zeros(N, np.float32)
def put(buf, t, a): i = int(t * SR); buf[i:i + len(a)] += a[:N - i]
for (s, _), a in zip(spans, vo): put(mix, s + 0.05, a)
def tone(f0, f1, d, amp):
    n = int(d * SR); tt = np.arange(n) / SR; return (np.sin(2 * np.pi * np.cumsum(np.linspace(f0, f1, n)) / SR) * amp * np.exp(-tt * 3 / d)).astype(np.float32)
sfx = np.zeros(N, np.float32)
put(sfx, spans[1][0] + 0.1, tone(900, 1300, 0.15, 0.25))                     # app blip
put(sfx, spans[2][0] + 0.35, tone(300, 1800, 0.45, 0.35))                    # flip whoosh
for k in range(5): put(sfx, spans[2][0] + 0.6 + k * 0.09, tone(1500 + k * 120, 1700 + k * 120, 0.1, 0.12))
for j in (4,):
    for k in range(7): put(sfx, spans[j][0] + 0.3 + k * 0.22, tone(1100 + k * 50, 1500, 0.12, 0.14))
for k in range(6): put(sfx, spans[5][0] + 0.1 + k * 0.15, tone(700, 760, 0.08, 0.18))   # $50 pops
put(sfx, spans[5][0] + 1.6, tone(200, 900, 0.5, 0.35))
for k in range(12): put(sfx, spans[6][0] + k * 0.12, tone(2400, 2200, 0.03, 0.1))      # receipt printing
put(sfx, spans[7][0] + 0.2, tone(80, 35, 0.9, 0.8)); put(sfx, spans[8][0] + 0.2, tone(400, 1600, 0.8, 0.3))
from build import music
mp = os.path.join(OUT, "trailer_music.wav"); music(dur, mp, seed=5)
with wave.open(mp) as w: m = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768; ch = w.getnchannels()
if ch == 2: m = m.reshape(-1, 2).mean(1)
m = np.pad(m, (0, max(0, N - len(m))))[:N]; os.remove(mp)
act = np.convolve((np.abs(mix) > 0.02).astype(np.float32), np.ones(int(0.3 * SR)) / int(0.3 * SR), "same")
out = mix + sfx * 0.6 + m * 0.22 * (1 - 0.5 * np.clip(act, 0, 1)); out = out / np.abs(out).max() * 0.92
wp = os.path.join(OUT, "trailer_mix.wav")
with wave.open(wp, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes())
vid = os.path.join(OUT, "trailer_video.mp4")
subprocess.run(["node", os.path.join(TOON, "rtoon.js"), "karl02_trailer.html", "video", vid, str(round(dur, 2))], check=True)
final = os.path.join(HERE, "TRAILER_karl02.mp4")
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", vid, "-i", wp, "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", final], check=True)
os.remove(vid); print("->", final)
