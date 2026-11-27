"""Compose the 3D demo Short: overlays (hook number, rewind card, captions, quiz), Piper VO, synthesized SFX, music bed.
python3 compose_demo.py <frames_dir> <out.mp4>"""
import sys, os, subprocess, wave, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..", "..")
ANTON = os.path.join(ROOT, "ep2", "fonts", "Anton-Regular.ttf"); MONT = os.path.join(ROOT, "ep2", "fonts", "Montserrat.ttf")
VOICE = os.path.join(ROOT, "finance02", "voice", "en_US-ryan-high.onnx")
FPS, W, H, SR = 30, 1080, 1920, 44100
frames_dir, out = sys.argv[1], sys.argv[2]
work = os.path.join(frames_dir, "..", "work"); os.makedirs(work, exist_ok=True)

LINES = [  # (start s, spoken, caption)
    (0.15, "Sixteen years later... I'm rich.", "16 YEARS LATER... I'M RICH"),
    (2.65, "Let's rewind.", "LET'S REWIND"),
    (3.45, "Every time I said no...", "EVERY TIME I SAID \"NO\"..."),
    (5.25, "I got one dollar.", "I GOT $1"),
    (7.7, "No to sneakers.", "NO TO SNEAKERS"),
    (8.7, "Grandma approves.", "GRANDMA APPROVES"),
    (9.7, "Max... does not.", "MAX... DOES NOT"),
    (10.75, "So how much did it grow? A, or B?", "HOW MUCH DID IT GROW?"),
    (13.35, "Guess before the next video.", "GUESS: A OR B?"),
]

def f(path, size, var=None):
    fo = ImageFont.truetype(path, size)
    if var: fo.set_variation_by_name(var)
    return fo

def text(d, txt, size, y, col=(255, 255, 255), font=ANTON, stroke=10, maxw=980, var=None):
    fo = f(font, size, var)
    while d.textbbox((0, 0), txt, font=fo, stroke_width=stroke)[2] > maxw and size > 30:
        size -= 4; fo = f(font, size, var)
    bb = d.textbbox((0, 0), txt, font=fo, stroke_width=stroke)
    d.text(((W - (bb[2] - bb[0])) / 2 - bb[0], y - (bb[3] - bb[1]) / 2 - bb[1]), txt, font=fo, fill=col, stroke_width=stroke, stroke_fill=(0, 0, 0))

# ---- voice (Piper) and timing
vo = np.zeros(int(15 * SR), np.float32); spans = []
for i, (st, spoken, cap) in enumerate(LINES):
    wp = os.path.join(work, f"l{i}.wav")
    if not os.path.exists(wp):
        subprocess.run(["piper", "--model", VOICE, "--output_file", wp, "--length_scale", "0.85"], input=spoken.encode(), check=True, capture_output=True)
    with wave.open(wp) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768; sr = w.getframerate()
    a = np.interp(np.arange(0, len(a), sr / SR), np.arange(len(a)), a)
    i0 = int(st * SR); a = a[:len(vo) - i0]; vo[i0:i0 + len(a)] += a; spans.append((st, st + len(a) / SR, cap))

# ---- SFX
sfx = np.zeros_like(vo); rng = np.random.RandomState(4)
def add(t, sig): i0 = int(t * SR); sfx[i0:i0 + len(sig)] += sig[:len(sfx) - i0]
def tone(f0, f1, dur, amp=0.3, kind="sin"):
    n = int(dur * SR); tt = np.arange(n) / SR; fr = np.linspace(f0, f1, n); ph = 2 * np.pi * np.cumsum(fr) / SR
    s = np.sin(ph) if kind == "sin" else np.sign(np.sin(ph)) * 0.5
    return s * amp * np.exp(-tt * (3 / dur))
def whoosh(dur=0.5, amp=0.35):
    n = int(dur * SR); s = rng.randn(n); k = np.convolve(s, np.ones(40) / 40, "same")
    env = np.sin(np.linspace(0, np.pi, n)) ** 2; return k * env * amp * 3
def cash(): return tone(1320, 1320, 0.12, 0.25, "sq") + np.concatenate([np.zeros(int(0.07 * SR)), tone(1760, 1760, 0.25, 0.25, "sq")])[:int(0.12 * SR)]
add(0.0, tone(80, 40, 0.6, 0.6))                    # boom on frame 1
for t in (0.3, 0.9, 1.5, 2.1): add(t, cash())        # money rain dings
add(2.55, whoosh(0.8, 0.5)); add(2.6, tone(900, 200, 0.7, 0.25))   # rewind
add(4.25, whoosh(0.3)); add(5.2, cash()); add(5.25, tone(600, 1200, 0.15, 0.2))
add(7.6, whoosh(0.25)); add(7.75, cash()); add(8.6, whoosh(0.25)); add(8.75, tone(700, 1400, 0.2, 0.2))
add(9.6, whoosh(0.25)); add(9.8, tone(160, 90, 0.35, 0.5))   # facepalm thud
add(10.6, whoosh(0.3)); add(13.2, tone(120, 60, 0.5, 0.5)); add(13.25, whoosh(0.4, 0.5))
for k in range(8): add(10.7 + k * 0.32, tone(440 + k * 30, 440 + k * 30, 0.08, 0.08))   # ticking tension

# ---- music bed (reuse EP01 lo-fi), mix
mpath = os.path.join(ROOT, "finance_series", "ep01", "build", "music.wav")
with wave.open(mpath) as w:
    m = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768; msr = w.getframerate(); ch = w.getnchannels()
if ch == 2: m = m.reshape(-1, 2).mean(1)
m = np.interp(np.arange(0, 15 * msr, msr / SR), np.arange(len(m)), m)[:len(vo)]
duck = np.convolve((np.abs(vo) > 0.02).astype(np.float32), np.ones(int(0.25 * SR)) / int(0.25 * SR), "same")
mix = vo * 1.0 + sfx * 0.8 + m * 0.18 * (1 - 0.6 * np.clip(duck, 0, 1))
mix = mix / max(1e-6, np.abs(mix).max()) * 0.9
apath = os.path.join(work, "mix.wav")
with wave.open(apath, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())

# ---- overlays
files = sorted(fn for fn in os.listdir(frames_dir) if fn.endswith(".jpg"))
p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", apath,
                      "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", out], stdin=subprocess.PIPE)
for n, fn in enumerate(files):
    t = n / FPS; im = Image.open(os.path.join(frames_dir, fn)).convert("RGB"); d = ImageDraw.Draw(im)
    if t < 2.6:   # hook number counting
        v = int(198344 * min(1, t / 1.2)); pulse = 1 + 0.04 * math.sin(t * 14)
        text(d, f"${v:,}", int(190 * pulse), 300, (110, 230, 140), stroke=14)
        text(d, "BECAUSE I SAID \"NO\"", 64, 450, (255, 214, 0), font=MONT, stroke=8, var="Black")
    elif t < 3.35:  # rewind card
        k = (t - 2.6) / 0.75
        for y in range(0, H, 9): d.line((0, y, W, y), fill=(0, 0, 0), width=3)
        text(d, "2010: 16 YEARS EARLIER", 120, H * 0.42, (255, 255, 255), stroke=12)
        text(d, "<< REWIND", 60, H * 0.42 + 140, (255, 90, 90), font=MONT, stroke=8, var="Black")
    elif t < 10.6:
        cnt = 0 + (1 if t > 5.25 else 0) + (1 if t > 7.75 else 0)
        text(d, f"NO COUNTER: {cnt}   SAVED: ${cnt}", 54, 210, (255, 214, 0), font=MONT, stroke=7, var="Black")
        if 5.25 < t < 6.6:
            k = min(1, (t - 5.25) / 0.15); text(d, "+$1", int(220 * (0.6 + 0.4 * k)), 700, (110, 230, 140), stroke=14)
    elif t < 13.2:
        text(d, "10 \"NO\"s A DAY SINCE 2010, INVESTED =", 56, 230, (255, 255, 255), font=MONT, stroke=8, var="Black")
        text(d, "A)  $61,137", 96, 380, (255, 214, 0), stroke=10); text(d, "B)  $198,344", 96, 510, (255, 214, 0), stroke=10)
    else:
        text(d, "A OR B?", 200, 360, (255, 214, 0), stroke=16)
    cap = [c for (s, e, c) in spans if s <= t < e + 0.15]
    if cap:
        text(d, cap[0], 92, 1520, (255, 255, 255), font=MONT, stroke=9, var="Black")
    text(d, "Example story · real S&P 500 math in the full video · not financial advice", 24, 1860, (230, 230, 230), font=MONT, stroke=3, var="Bold")
    d.rectangle((0, H - 10, int(W * t / 15), H), fill=(255, 176, 46))
    p.stdin.write(im.tobytes())
p.stdin.close(); p.wait(); print("ok", out)
