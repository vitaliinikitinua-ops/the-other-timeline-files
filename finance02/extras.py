"""Intro bumper (4 s), end screen (15 s), music bed for full length, 2 thumbnails.
python3 extras.py  (after tts.py)"""
import sys, os, json, math, random, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from video import *  # noqa  (W, H, helpers, TIM, VAL, INV)

INTRO, OUTRO = 4.0, 15.0

def intro_frame(t):
    c = BG.copy(); particles(c, t, 50, 81)
    d = ImageDraw.Draw(c)
    g = ease(clamp01(t / 1.2))
    d.line([(0, 640), (lerp(0, 900, g), 640)], fill=AMBER + (255,), width=12)
    g2 = ease(clamp01((t - 1.0) / 1.0))
    if g2 > 0:
        d.line([(900, 640), (lerp(900, W, g2), 640)], fill=AMBER + (255,), width=12)
        d.line([(900, 640), (lerp(900, W, g2), lerp(640, 330, g2))], fill=TEAL + (255,), width=12)
    if t > 1.5:
        p = ease_out(clamp01((t - 1.5) / 0.4))
        y = you(int(260 * (0.6 + 0.4 * p)), blink(t), (0.5, -0.3))
        paste_center(c, y, 900, 640 - 40 * p, clamp01((t - 1.5) / 0.2))
    pop(c, T("THE OTHER TIMELINE", 110, TEAL, "A", 14), W / 2, 880, t, 2.0)
    pop(c, T("What if your life went the other way?", 40, CREAM, "D"), W / 2, 980, t, 2.4)
    return fade(c, clamp01((t - (INTRO - 0.35)) / 0.35))

def outro_frame(t):
    c = BG.copy(); particles(c, t, 50, 91)
    pop(c, T("WATCH NEXT", 80, AMBER, "A", 10), W / 2, 120, t, 0.2)
    # two video slots (YouTube end-screen elements go here)
    for x in (560, 1360):
        pop(c, panel(680, 383, CREAM, (20, 30, 52, 230), 24, 4), x, 440, t, 0.3)
    # subscribe circle
    pop(c, panel(260, 260, TEAL, (20, 30, 52, 230), 130, 6), W / 2, 830, t, 0.5)
    paste_center(c, you(150, blink(t), (0, -0.2)), W / 2, 830, clamp01((t - 0.6) / 0.3))
    pop(c, T("SUBSCRIBE", 40, TEAL, "D"), W / 2, 995, t, 0.8)
    return fade(c, clamp01((t - (OUTRO - 0.6)) / 0.6))

def render_clip(fn, dur, path):
    enc = Encoder(path)
    for n in range(int(dur * FPS)):
        enc.write(fn(n / FPS))
    enc.close()

def music(total, path):
    SR = 44100; N = int(SR * total); t = np.arange(N) / SR
    out = np.zeros(N); rng = np.random.default_rng(1); noise = rng.normal(0, 1, N)
    def env(t0, a, dcy, L):
        e = np.zeros(N); i0 = int(t0 * SR); n = int(L * SR); x = np.arange(n) / SR
        s = np.minimum(1, x / max(a, 1e-3)) * np.exp(-x / dcy); m = max(0, min(n, N - i0)); e[i0:i0 + m] = s[:m]; return e
    bpm = 86; beat = 60 / bpm
    prog = [[220.0, 261.6, 329.6, 392.0], [174.6, 220.0, 261.6, 329.6], [130.8, 196.0, 261.6, 329.6], [196.0, 246.9, 293.7, 392.0]]
    bars = int(total / (4 * beat)) + 1
    for b in range(bars):
        ch = prog[b % 4]; t0 = b * 4 * beat
        out += env(t0, 0.6, 3.0, 4 * beat + 1) * sum(np.sin(2 * np.pi * f * t) for f in ch) * 0.025  # pad
        for s in range(8):  # soft keys arpeggio
            f = ch[[0, 2, 1, 3, 2, 1, 3, 2][s]] * 2
            out += env(t0 + s * beat / 2, 0.004, 0.25, 0.9) * np.sin(2 * np.pi * f * t) * 0.035
        out += env(t0, 0.02, 0.8, 4 * beat) * np.sin(2 * np.pi * ch[0] / 2 * t) * 0.12  # bass
        for k in range(4):  # lo-fi kick / hat
            tk = t0 + k * beat
            f = 48 + 60 * np.exp(-np.clip(t - tk, 0, None) * 22)
            if k in (0, 2):
                out += env(tk, 0.002, 0.14, 0.4) * np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.28
            else:
                out += env(tk, 0.001, 0.07, 0.25) * noise * 0.05
            out += env(tk + beat / 2, 0.001, 0.02, 0.08) * np.diff(noise, prepend=0) * 0.025
    out *= np.clip(t / 1.0, 0, 1) * np.clip((total - t) / 2.0, 0, 1)
    out /= np.max(np.abs(out)) * 1.1
    pcm = (out * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.stack([pcm, pcm], 1).tobytes())

def thumb(variant, path):
    c = gradient_bg(NAVY2, NAVY, 0.4)
    d = ImageDraw.Draw(c)
    if variant == "A":
        ov = Image.new("RGBA", c.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        od.rectangle((0, 0, W / 2, H), fill=CORAL + (40,)); od.rectangle((W / 2, 0, W, H), fill=TEAL + (40,))
        c.alpha_composite(ov)
        paste_center(c, cup(2.2), 470, 520)
        paste_center(c, T("$5/DAY", 150, CREAM), 470, 140)
        paste_center(c, T("→", 220, AMBER, "A", 10), W / 2, 520)
        paste_center(c, T("$99,172", 210, TEAL, "A", 20), 1440, 470)
        paste_center(c, you(330, 1.0, (-0.6, -0.2)), 1440, 860)
    else:
        X0, Y0, X1, Y1 = 120, 300, 1300, 980
        pts = [(X0 + (X1 - X0) * i / END, Y1 - (Y1 - Y0) * VAL[i] / 105000) for i in range(END + 1)]
        ov = Image.new("RGBA", c.size, (0, 0, 0, 0))
        ImageDraw.Draw(ov).polygon(pts + [(X1, Y1), (X0, Y1)], fill=TEAL + (60,)); c.alpha_composite(ov)
        d = ImageDraw.Draw(c); d.line(pts, fill=TEAL + (255,), width=16, joint="curve")
        d.line([(X0, Y1), (X1, Y1 - (Y1 - Y0) * INV[-1] / 105000)], fill=AMBER + (255,), width=12)
        paste_center(c, T("COFFEE MONEY", 140, CREAM), W / 2, 130)
        paste_center(c, T("$99K", 260, AMBER, "A", 20), 1560, 420)
        paste_center(c, you(380, 1.0, (-0.7, -0.5)), 1560, 840)
    img = c.convert("RGB").resize((1280, 720), Image.LANCZOS)
    img.save(path, quality=90)
    img.resize((320, 180), Image.LANCZOS).save(path.replace(".jpg", "_320.png"))

if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "build"), exist_ok=True)
    total = INTRO + TIM[-1]["end"] + OUTRO
    music(total, os.path.join(HERE, "build", "music.wav"))
    thumb("A", os.path.join(HERE, "thumbnail_A.jpg")); thumb("B", os.path.join(HERE, "thumbnail_B.jpg"))
    render_clip(intro_frame, INTRO, os.path.join(HERE, "build", "intro.mp4"))
    render_clip(outro_frame, OUTRO, os.path.join(HERE, "build", "outro.mp4"))
    print("ok", round(total, 1))
