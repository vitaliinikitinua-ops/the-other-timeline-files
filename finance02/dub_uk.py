"""Ukrainian audio track (Piper, voice mykyta) aligned to the English sentence timings.
-> audio_uk.m4a (exact video length) + captions_uk.srt"""
import json, os, subprocess, wave, numpy as np
from script import BEATS
from script_uk import UK
TIM = json.load(open("build/timing.json"))
assert [len(s) for _, s in BEATS] == [len(x) for x in UK]
OFF = 4.0; SR = 22050; TOTAL = 286.733
os.makedirs("build/uk", exist_ok=True)
def synth(text, path, ls=1.0):
    subprocess.run(["python3", "-m", "piper", "-m", "voice/uk_UA-ukrainian_tts-medium.onnx", "-s", "1", "-f", path,
                    "--length-scale", str(ls)], input=text.encode(), check=True, capture_output=True)
def load(p):
    with wave.open(p) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)
        sr = w.getframerate()
    nz = np.where(np.abs(a) > 300)[0]
    return a[max(0, nz[0] - 300): nz[-1] + 600], sr
flat = []
for bi, b in enumerate(TIM):
    for si, s in enumerate(b["sents"]):
        flat.append((bi, si, s["start"] + OFF))
starts = [x[2] for x in flat] + [TIM[-1]["end"] + OFF]
out = np.zeros(int(TOTAL * SR) + SR, np.float32); cursor = 0.0; subs = []
for k, (bi, si, st) in enumerate(flat):
    show, say = UK[bi][si]
    p = f"build/uk/{bi:02d}_{si:02d}.wav"
    if not os.path.exists(p):
        synth(say or show, p, 0.78)
    a, sr = load(p); assert sr == SR
    t0 = max(st, cursor)
    slot = starts[k + 1] - t0 - 0.15
    d = len(a) / SR
    if d > slot and slot > 0.5:
        tempo = min(1.35, d / slot)
        q = p.replace(".wav", "_fast.wav")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", p, "-filter:a", f"atempo={tempo:.3f}", q], check=True)
        a, _ = load(q); d = len(a) / SR
    i0 = int(t0 * SR); out[i0:i0 + len(a)] += a[:len(out) - i0]
    cursor = t0 + d + 0.12
    subs.append((t0, t0 + d, show))
drift = max(0, cursor - TOTAL)
print("last end", round(cursor, 2), "overflow", round(drift, 2))
pcm = np.clip(out[:int(TOTAL * SR)], -32767, 32767).astype(np.int16)
with wave.open("build/vo_uk.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
def ts(x):
    h, r = divmod(x, 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}"
open("captions_uk.srt", "w").write("\n".join(f"{i+1}\n{ts(a)} --> {ts(b)}\n{t}\n" for i, (a, b, t) in enumerate(subs)))
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", "build/vo_uk.wav", "-i", "build/music.wav", "-filter_complex",
    "[0:a]aresample=44100,pan=stereo|c0=c0|c1=c0,apad,asplit=2[vo][sc];[1:a]volume=0.32[bed];[bed][sc]sidechaincompress=threshold=0.04:ratio=5:attack=30:release=400[duck];[duck][vo]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]",
    "-map", "[a]", "-t", str(TOTAL), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "audio_uk.m4a"], check=True)
