"""Karl #01 trailer: Piper VO + music bed + SFX, rendered with trailer.html. python3 trailer.py -> karl01/TRAILER_karl01.mp4"""
import os, sys, json, subprocess, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); FS = os.path.join(HERE, "..", ".."); ROOT = os.path.join(FS, "..")
sys.path.insert(0, os.path.join(FS, "engine"))
VOICE = os.path.join(ROOT, "finance02", "voice", "en_US-ryan-high.onnx"); OUT = os.path.join(HERE, "test"); SR = 44100
LINES = [("Max slams a shoebox on the cafeteria table.", "n"), ("Limited edition. Two hundred dollars.", "max"),
         ("You look at Max. Then you look a little higher.", "n"), ("Three dollars and twelve cents.", "n"),
         ("Most people look at faces. You see balances.", "n"), ("Grandma's number doesn't even fit above her head.", "n"),
         ("At dinner, Dad's number is red. And it's flashing.", "n"), ("Eight hundred kids. Eight hundred numbers.", "n"),
         ("What if you could see everyone's bank account?", "n")]

def tts(i, text, voice):
    raw, p = os.path.join(OUT, f"tr{i}_raw.wav"), os.path.join(OUT, f"tr{i}.wav")
    subprocess.run(["piper", "--model", VOICE, "--output_file", raw, "--length_scale", "0.9"], input=text.encode(), check=True, capture_output=True)
    af = "asetrate=22050*1.18,aresample=22050,atempo=0.92" if voice == "max" else "anull"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", raw, "-af", af, p], check=True); os.remove(raw)
    with wave.open(p) as w: a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768; sr = w.getframerate()
    os.remove(p); return np.interp(np.arange(0, len(a), sr / SR), np.arange(len(a)), a).astype(np.float32)

vo = [tts(i, l, v) for i, (l, v) in enumerate(LINES)]
spans, t = [], 0.4
for j, a in enumerate(vo):
    d = len(a) / SR; hold = 1.2 if j in (3, 4, 7) else 0.35
    spans.append([round(t, 2), round(t + d + hold, 2)]); t += d + hold
spans[-1][1] = round(spans[-1][1] + 2.5, 2); dur = spans[-1][1] + 0.3
json.dump(spans, open(os.path.join(OUT, "trailer_timing.json"), "w"))
N = int(dur * SR) + SR; mix = np.zeros(N, np.float32)
def put(t, a): i = int(t * SR); mix[i:i + len(a)] += a[:N - i]
for (s, _), a in zip(spans, vo): put(s + 0.05, a)
def tone(f0, f1, d, amp):
    n = int(d * SR); tt = np.arange(n) / SR; return (np.sin(2 * np.pi * np.cumsum(np.linspace(f0, f1, n)) / SR) * amp * np.exp(-tt * 3 / d)).astype(np.float32)
sfx = np.zeros(N, np.float32)
def sput(t, a): i = int(t * SR); sfx[i:i + len(a)] += a[:N - i]
sput(spans[0][0] + 0.45, tone(90, 40, 0.5, 0.6))                    # shoebox slam
sput(spans[3][0] + 0.1, tone(600, 1500, 0.35, 0.3))                 # ping
for k in range(10): sput(spans[4][0] + 0.3 + k * 0.12, tone(1200 + k * 60, 1400 + k * 60, 0.12, 0.12))
for k in range(6): sput(spans[3][0] + 0.85 + k * 0.1, tone(2400, 2200, 0.03, 0.1))   # receipt
sput(spans[6][0] + 0.2, tone(200, 120, 0.6, 0.4)); sput(spans[8][0] + 0.2, tone(80, 35, 0.9, 0.8))
from build import music
mp = os.path.join(OUT, "trailer_music.wav"); music(dur, mp, seed=3)
with wave.open(mp) as w: m = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768; ch = w.getnchannels()
if ch == 2: m = m.reshape(-1, 2).mean(1)
m = np.pad(m, (0, max(0, N - len(m))))[:N]; os.remove(mp)
act = np.convolve((np.abs(mix) > 0.02).astype(np.float32), np.ones(int(0.3 * SR)) / int(0.3 * SR), "same")
out = mix + sfx * 0.6 + m * 0.22 * (1 - 0.5 * np.clip(act, 0, 1)); out = out / np.abs(out).max() * 0.92
wp = os.path.join(OUT, "trailer_mix.wav")
with wave.open(wp, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes())
print("spans", spans, "dur", round(dur, 1))
vid = os.path.join(OUT, "trailer_video.mp4")
subprocess.run(["node", os.path.join(HERE, "rtoon.js"), "trailer.html", "video", vid, str(round(dur, 2))], check=True)
final = os.path.join(FS, "karl01", "TRAILER_karl01.mp4")
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", vid, "-i", wp, "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", final], check=True)
os.remove(vid); os.remove(wp); print("->", final)
