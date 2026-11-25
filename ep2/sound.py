"""Synth music bed + SFX for the trailer -> build/bed.wav"""
import numpy as np, wave
SR = 44100; DUR = 30.0
N = int(SR * DUR); t = np.arange(N) / SR
rng = np.random.default_rng(7)
out = np.zeros(N)

def env(t0, a, d, length):
    e = np.zeros(N); i0 = int(t0 * SR); n = int(length * SR)
    x = np.arange(n) / SR
    seg = np.minimum(1, x / max(a, 1e-3)) * np.exp(-x / d)
    e[i0:i0 + n] = seg[:max(0, min(n, N - i0))]
    return e

# warm pad: Am - F - C - G, slow
chords = [[220, 261.6, 329.6], [174.6, 220, 261.6], [196, 261.6, 329.6], [196, 246.9, 293.7]]
pad = np.zeros(N)
for k in range(8):
    seg0 = k * 3.75
    for f in chords[k % 4]:
        e = np.clip((t - seg0) / 1.2, 0, 1) * np.clip((seg0 + 4.6 - t) / 1.2, 0, 1)
        pad += e * (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * f * 2.003 * t)) * 0.05
# tension section 13-23: darker, lower
tension = ((t > 13) & (t < 23.3)).astype(float)
pad *= 1 - 0.5 * tension
pad += tension * 0.07 * np.sin(2 * np.pi * 55 * t) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.5 * t))
# soft pulse
for b in np.arange(0, 23, 0.75):
    pad += env(b, 0.005, 0.12, 0.5) * np.sin(2 * np.pi * 60 * t) * 0.12
out += pad

noise = rng.normal(0, 1, N)
def whoosh(t0, length=0.7, gain=0.25):
    global out
    e = env(t0, length * 0.6, length * 0.4, length * 1.5)
    hp = np.diff(noise, prepend=0)
    out += e * hp * gain * 0.5
def shatter(t0, gain=0.3):
    global out
    for i in range(14):
        tt = t0 + rng.uniform(0, 0.35); f = rng.uniform(2000, 5000)
        out += env(tt, 0.002, 0.05, 0.3) * np.sin(2 * np.pi * f * t) * gain * 0.5
    whoosh(t0 - 0.1, 0.5, 0.2)
def knock(t0):
    global out
    out += env(t0, 0.001, 0.05, 0.3) * (np.sin(2 * np.pi * 90 * t) + 0.5 * noise * 0.3) * 0.7
def boom(t0, gain=0.6):
    global out
    f = 45 + 30 * np.exp(-(t - t0).clip(0) * 4)
    out += env(t0, 0.005, 0.8, 2.5) * np.sin(2 * np.pi * np.cumsum(f) / SR) * gain

for s in (2.75, 5.9, 7.7, 13.9, 15.3, 15.9, 16.5):
    shatter(s)
whoosh(0.0, 1.2, 0.15); whoosh(8.2, 0.6); whoosh(23.0, 0.7)
for k in (18.3, 18.65, 19.0):
    knock(k)
boom(20.8, 0.5); boom(23.3, 0.7)
# fade out
out *= np.clip((DUR - t) / 1.2, 0, 1)
out /= np.max(np.abs(out)) * 1.15
pcm = (out * 32767).astype(np.int16)
st = np.stack([pcm, pcm], 1)
with wave.open("build/bed.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
