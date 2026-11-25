"""Piper TTS per sentence -> build/vo.wav + build/timing.json + captions .srt"""
import json, os, subprocess, wave, numpy as np
from script import BEATS
os.makedirs("build/tts", exist_ok=True)
SR = 22050
GAP_S, GAP_B, LEAD = 0.28, 0.75, 0.6
audio = [np.zeros(int(LEAD * SR), np.int16)]; t = LEAD
timing = []
def run(text, path):
    subprocess.run(["python3", "-m", "piper", "-m", "voice/en_US-ryan-high.onnx", "-f", path,
                    "--length-scale", "1.12", "--noise-scale", "0.6", "--noise-w-scale", "0.7"],
                   input=text.encode(), check=True, capture_output=True)
for bi, (name, sents) in enumerate(BEATS):
    b0 = t; sl = []
    for si, (show, say) in enumerate(sents):
        p = f"build/tts/{bi:02d}_{si:02d}.wav"
        if not os.path.exists(p):
            run(say or show, p)
        with wave.open(p) as w:
            assert w.getframerate() == SR
            a = np.frombuffer(w.readframes(w.getnframes()), np.int16)
        # trim edges
        nz = np.where(np.abs(a) > 300)[0]
        a = a[max(0, nz[0] - 400): nz[-1] + 800]
        d = len(a) / SR
        sl.append({"text": show, "start": round(t, 3), "end": round(t + d, 3)})
        audio.append(a); t += d
        gap = GAP_S if si < len(sents) - 1 else GAP_B
        audio.append(np.zeros(int(gap * SR), np.int16)); t += gap
    timing.append({"name": name, "start": round(b0, 3), "end": round(t, 3), "sents": sl})
audio.append(np.zeros(int(1.5 * SR), np.int16)); t += 1.5
timing[-1]["end"] = round(t, 3)
pcm = np.concatenate(audio)
with wave.open("build/vo.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
json.dump(timing, open("build/timing.json", "w"), indent=1)
def ts(x):
    h, r = divmod(x, 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}"
with open("captions_en.srt", "w") as f:
    n = 1
    for b in timing:
        for s in b["sents"]:
            f.write(f"{n}\n{ts(s['start'])} --> {ts(s['end'])}\n{s['text']}\n\n"); n += 1
print("total", round(t, 1), "s")
for b in timing: print(b["name"], b["start"], b["end"])
