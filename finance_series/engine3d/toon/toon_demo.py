"""10-second 2D style test with Piper VO + simple SFX. python3 demo.py -> engine2d/test/DEMO_TOON_10s.mp4"""
import os, json, subprocess, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..", "..", "..")
VOICE = os.path.join(ROOT, "finance02", "voice", "en_US-ryan-high.onnx"); OUT = os.path.join(HERE, "test"); SR = 44100
os.makedirs(OUT, exist_ok=True)
LINES = ["Max says it's only five dollars a day.", "Then your pocket prints the real price.",
         "One thousand, eight hundred twenty five dollars. A year.", "Max puts the phone down."]

def tts(i, text):
    p = os.path.join(OUT, f"vo{i}.wav")
    subprocess.run(["piper", "--model", VOICE, "--output_file", p, "--length_scale", "0.9"], input=text.encode(), check=True, capture_output=True)
    with wave.open(p) as w: a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768; sr = w.getframerate()
    return np.interp(np.arange(0, len(a), sr / SR), np.arange(len(a)), a).astype(np.float32)

vo = [tts(i, l) for i, l in enumerate(LINES)]
starts, t = [], 0.25
for a in vo: starts.append(round(t, 2)); t += len(a) / SR + 0.25
dur = max(10.0, t + 0.3)
json.dump(starts, open(os.path.join(OUT, "demo_timing.json"), "w"))
mix = np.zeros(int(dur * SR) + SR, np.float32)
def put(t, a): i = int(t * SR); mix[i:i + len(a)] += a[:len(mix) - i]
for s, a in zip(starts, vo): put(s, a)
def tone(f0, f1, d, amp):
    n = int(d * SR); tt = np.arange(n) / SR; return (np.sin(2 * np.pi * np.cumsum(np.linspace(f0, f1, n)) / SR) * amp * np.exp(-tt * 3 / d)).astype(np.float32)
put(starts[1] + 0.15, tone(500, 1400, 0.5, 0.25)); put(starts[1] + 0.5, np.concatenate([tone(1320, 1320, 0.08, 0.15), tone(1760, 1760, 0.25, 0.15)]))
for k in range(8): put(starts[1] + 0.55 + k * 0.12, tone(2400, 2200, 0.03, 0.1))  # receipt printer
put(starts[2] + 0.3, tone(160, 70, 0.4, 0.5))
mix = mix / np.abs(mix).max() * 0.9
with wave.open(os.path.join(OUT, "demo_mix.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
print("timing", starts, "duration", round(dur, 2))
subprocess.run(["node", os.path.join(HERE, "rtoon.js"), "toon_demo.html", "video", os.path.join(OUT, "demo_video.mp4"), str(round(dur, 2))], check=True)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", os.path.join(OUT, "demo_video.mp4"), "-i", os.path.join(OUT, "demo_mix.wav"), "-c:v", "copy", "-c:a", "aac", "-shortest", os.path.join(OUT, "DEMO_TOON_10s.mp4")], check=True)
print("->", os.path.join(OUT, "DEMO_TOON_10s.mp4"))
