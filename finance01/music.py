"""Upbeat synth bed for finance short -> build/bed.wav (31 s)"""
import numpy as np, wave
SR = 44100; DUR = 31.0; N = int(SR * DUR); t = np.arange(N) / SR
out = np.zeros(N); rng = np.random.default_rng(3); noise = rng.normal(0, 1, N)
BPM = 112; beat = 60 / BPM
def env(t0, a, d, L):
    e = np.zeros(N); i0 = int(t0 * SR); n = int(L * SR); x = np.arange(n) / SR
    s = np.minimum(1, x / max(a, 1e-3)) * np.exp(-x / d); m = max(0, min(n, N - i0)); e[i0:i0 + m] = s[:m]; return e
prog = [[261.6, 329.6, 392.0], [220.0, 261.6, 329.6], [174.6, 220.0, 261.6], [196.0, 246.9, 293.7]]
bars = int(DUR / (4 * beat)) + 1
for b in range(bars):
    ch = prog[b % 4]; t0 = b * 4 * beat
    for s in range(8):  # plucky eighths
        f = ch[s % 3] * (2 if s % 4 == 3 else 1)
        out += env(t0 + s * beat / 2, 0.005, 0.18, 0.6) * np.sin(2 * np.pi * f * t) * 0.10
    out += env(t0, 0.3, 2.0, 4 * beat) * sum(np.sin(2 * np.pi * f / 2 * t) for f in ch) * 0.04
    out += env(t0, 0.01, 0.4, 4 * beat) * np.sin(2 * np.pi * ch[0] / 4 * t) * 0.25
# drums from 4 s (timeline A), quieter in hook
for k in range(int(DUR / beat)):
    tk = k * beat; g = 0.5 if tk < 4 else 1.0
    f = 50 + 70 * np.exp(-np.clip(t - tk, 0, None) * 25)
    out += g * env(tk, 0.002, 0.15, 0.4) * np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.45
    out += g * env(tk + beat / 2, 0.001, 0.03, 0.1) * np.diff(noise, prepend=0) * 0.06
    if k % 2 == 1:
        out += g * env(tk, 0.001, 0.08, 0.3) * noise * 0.12
# risers / hits at scene cuts
for c in (4, 9.5, 12, 23, 27.5):
    out += env(c - 0.8, 0.75, 0.05, 0.9) * np.diff(noise, prepend=0) * 0.12
    out += env(c, 0.003, 0.5, 1.5) * np.sin(2 * np.pi * 55 * t) * 0.4
# cash ding on the reveal
for c in (24.5, 25.9):
    out += env(c, 0.002, 0.35, 1.2) * (np.sin(2 * np.pi * 1568 * t) + 0.6 * np.sin(2 * np.pi * 2093 * t)) * 0.15
out *= np.clip((DUR - t) / 1.0, 0, 1)
out /= np.max(np.abs(out)) * 1.1
pcm = (out * 32767).astype(np.int16)
with wave.open("build/bed.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.stack([pcm, pcm], 1).tobytes())
