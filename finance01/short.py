"""Finance Short #1 (no voice): What IF You Saved $5 a Day Since 2010?
Data: S&P 500 monthly average price (Robert Shiller dataset via github.com/datasets/s-and-p-500),
$5/day = $152.08 invested on the 1st of every month, Jan 2010 - Sep 2026, price only (no dividends).
Render: python3 short.py   (needs ../ep2/common.py and ../ep2/fonts)"""
import sys, os, csv, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ep2"))
import common
common.W, common.H = 1080, 1920
from common import *
W, H = 1080, 1920
from multiprocessing import Pool

DUR = 31.0
GREEN = (120, 220, 140)

# ---- data ----
rows = [r for r in csv.DictReader(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sp500.csv")))
        if "2010-01-01" <= r["Date"] <= "2026-09-01"]
MONTHLY = 5 * 365 / 12
inv, val, sh = [], [], 0.0
for i, r in enumerate(rows):
    p = float(r["SP500"]); sh += MONTHLY / p
    inv.append(MONTHLY * (i + 1)); val.append(sh * p)
N = len(rows)
INVESTED, FINAL = inv[-1], val[-1]

BG = gradient_bg(NAVY2, NAVY)

def T(txt, size, col=CREAM, f=ANTON, glow_r=0, var=None):
    return text_sprite(txt, font(f, size, var), col + (255,), glow_r=glow_r, glow_col=col)

def pop(canvas, spr, x, y, t, t0, t1=99):
    if t < t0 or t > t1 + 0.3:
        return
    p = ease_out((t - t0) / 0.35); a = clamp01((t - t0) / 0.2) * clamp01((t1 + 0.3 - t) / 0.3)
    s = 0.6 + 0.4 * p
    if s < 0.999:
        spr = spr.resize((max(1, int(spr.width * s)), max(1, int(spr.height * s))), Image.BICUBIC)
    paste_center(canvas, spr, x, y, a)

YOUC = {}
def you(size, eo=1.0, look=(0, 0)):
    k = (size, eo, look)
    if k not in YOUC:
        YOUC[k] = you_head(size, eo, look)
    return YOUC[k]
def blink(t, per=2.9):
    return 0.1 if (t % per) < 0.12 else 1.0

def cup(scale=1.0):
    w, h = int(150 * scale), int(190 * scale)
    img = Image.new("RGBA", (w + 60, h + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.polygon([(0, 30 * scale), (w, 30 * scale), (w * 0.85, h), (w * 0.15, h)], fill=CREAM + (255,), outline=INK + (255,))
    d.rounded_rectangle((-5, 0, w + 5, 38 * scale), int(10 * scale), fill=(120, 80, 50, 255))
    d.rectangle((w * 0.12, 80 * scale, w * 0.88, 140 * scale), fill=AMBER + (255,))
    f = font(ANTON, int(46 * scale)); bb = f.getbbox("$5")
    d.text((w / 2 - (bb[2] - bb[0]) / 2 - bb[0], 110 * scale - (bb[3] - bb[1]) / 2 - bb[1]), "$5", font=f, fill=INK + (255,))
    return img

CUP = cup(1.0); CUP_S = cup(0.55)

def particles(c, t, n=40, seed=5, col=AMBER):
    rng = random.Random(seed); d = ImageDraw.Draw(c)
    for i in range(n):
        x = (rng.uniform(0, W) + t * rng.uniform(-15, 15)) % W
        y = (rng.uniform(0, H) - t * rng.uniform(10, 40)) % H
        r = rng.uniform(1.5, 4); d.ellipse((x - r, y - r, x + r, y + r), fill=col + (int(80 + 60 * math.sin(t * 2 + i)),))

# ---- scenes ----
def hook(t):  # 0-4
    c = BG.copy(); particles(c, t)
    pop(c, T("WHAT IF YOU", 120, CREAM), W / 2, 330, t, 0.1)
    pop(c, T("SAVED $5 A DAY", 132, AMBER, glow_r=14), W / 2, 480, t, 0.4)
    pop(c, T("SINCE 2010?", 132, AMBER, glow_r=14), W / 2, 630, t, 0.7)
    paste_center(c, you(460, blink(t), (0.7, 0.2)), W / 2 - 120, 1250)
    bob = 12 * math.sin(t * 3)
    paste_center(c, CUP, W / 2 + 230, 1180 + bob, clamp01((t - 1.0) / 0.3))
    return camera(c, 1 + 0.03 * t / 4)

def timeline_a(t):  # 4-9.5 coffee every day
    lt = t - 4
    c = gradient_bg((60, 30, 45), NAVY) if False else BG.copy()
    pop(c, T("TIMELINE A", 90, CORAL, glow_r=10), W / 2, 230, t, 4.0)
    pop(c, T("$5 coffee. Every. Single. Day.", 54, CREAM, DMS, var="Bold"), W / 2, 340, t, 4.3)
    # pile of cups
    n = int(min(60, 60 * ease(lt / 3.5)))
    rng = random.Random(4)
    for i in range(n):
        x = rng.uniform(180, 900); y = 1500 - (i // 8) * 85 + rng.uniform(-10, 10)
        paste_center(c, CUP_S.rotate(rng.uniform(-14, 14), expand=True, resample=Image.BICUBIC), x, y)
    paste_center(c, you(300, blink(t), (0, -0.5)), W / 2, 1720)
    days = int(lerp(0, round(INVESTED / 5), ease(lt / 3.5)))
    pop(c, T(f"{days:,} coffees", 100, AMBER), W / 2, 520, t, 4.6)
    pop(c, T(f"= ${days * 5:,} SPENT", 88, CREAM), W / 2, 650, t, 4.9)
    pop(c, T("LEFT TODAY: $0", 110, CORAL, glow_r=12), W / 2, 800, t, 7.9)
    return c

def timeline_b_intro(t):  # 9.5-12
    c = BG.copy(); particles(c, t, 40, 9, TEAL)
    pop(c, T("TIMELINE B", 90, TEAL, glow_r=10), W / 2, 380, t, 9.5)
    pop(c, T("Same $5 a day.", 64, CREAM, DMS, var="Bold"), W / 2, 520, t, 9.8)
    pop(c, T("Into an S&P 500", 80, AMBER), W / 2, 660, t, 10.3)
    pop(c, T("index fund instead.", 80, AMBER), W / 2, 770, t, 10.5)
    paste_center(c, you(420, blink(t), (0.3, -0.3)), W / 2, 1300)
    return c

CH = (110, 520, 980, 1380)  # chart box x0,y0,x1,y1
VMAX = 110000
def cx_(i): return CH[0] + (CH[2] - CH[0]) * i / (N - 1)
def cy_(v): return CH[3] - (CH[3] - CH[1]) * v / VMAX

def chart(t):  # 12-23
    lt = t - 12
    c = BG.copy()
    d = ImageDraw.Draw(c)
    fs = font(DMS, 30, "Bold")
    for v in (0, 25000, 50000, 75000, 100000):
        y = cy_(v); d.line((CH[0], y, CH[2], y), fill=(255, 255, 255, 28), width=2)
        d.text((CH[0], y - 38), f"${v // 1000}K" if v else "$0", font=fs, fill=CREAM + (150,))
    for yr in (2010, 2014, 2018, 2022, 2026):
        i = (yr - 2010) * 12; x = cx_(min(i, N - 1))
        d.text((x - 36, CH[3] + 16), str(yr), font=fs, fill=CREAM + (170,))
    p = ease(clamp01((lt - 0.5) / 8.0))
    k = max(1, int(p * (N - 1)))
    pts_v = [(cx_(i), cy_(val[i])) for i in range(k + 1)]
    pts_i = [(cx_(i), cy_(inv[i])) for i in range(k + 1)]
    # fill under value
    ov = Image.new("RGBA", c.size, (0, 0, 0, 0))
    ImageDraw.Draw(ov).polygon(pts_v + [(pts_v[-1][0], CH[3]), (CH[0], CH[3])], fill=TEAL + (45,))
    c.alpha_composite(ov)
    d = ImageDraw.Draw(c)
    if len(pts_i) > 1:
        d.line(pts_i, fill=AMBER + (255,), width=7)
        d.line(pts_v, fill=TEAL + (255,), width=9, joint="curve")
    x, y = pts_v[-1]
    d.ellipse((x - 14, y - 14, x + 14, y + 14), fill=TEAL + (255,), outline=CREAM + (255,), width=4)
    # legend + live counters
    paste_center(c, T("TIMELINE B", 80, TEAL, glow_r=8), W / 2, 200)
    paste_center(c, T(f"PUT IN: ${int(inv[k]):,}", 60, AMBER), W / 2, 310)
    paste_center(c, T(f"WORTH: ${int(val[k]):,}", 76, TEAL), W / 2, 410)
    # event labels
    def lab(date, txt, col, t0):
        i = [r["Date"] for r in rows].index(date)
        if k >= i:
            pop(c, T(txt, 40, col, DMS, var="Bold"), cx_(i) - 60, cy_(val[i]) - 120, t, max(t0, 0))
    lab("2020-03-01", "COVID CRASH", CORAL, 0)
    lab("2022-10-01", "2022 DROP", CORAL, 0)
    if k >= (2020 - 2010) * 12 + 2:
        pop(c, T("You kept buying.", 56, CREAM, DMS, var="Bold"), W / 2, 1530, t, 12 + 6.2)
    d.text((CH[0], 1820), "S&P 500 monthly avg. price, $152.08 on the 1st of each month,",
           font=font(DMS, 24, "Bold"), fill=CREAM + (110,))
    d.text((CH[0], 1852), "Jan 2010 - Sep 2026. Dividends not included. Source: R. Shiller data.",
           font=font(DMS, 24, "Bold"), fill=CREAM + (110,))
    paste_center(c, you(170, blink(t), (0.8, -0.6)), 930, 1660)
    return c

def result(t):  # 23-27.5
    c = BG.copy(); particles(c, t, 50, 21, TEAL)
    pop(c, T("YOU PUT IN", 80, CREAM), W / 2, 360, t, 23.0)
    pop(c, T(f"${int(INVESTED):,}", 150, AMBER, glow_r=12), W / 2, 500, t, 23.3)
    pop(c, T("IT'S WORTH ABOUT", 80, CREAM), W / 2, 760, t, 24.2)
    shown = int(lerp(INVESTED, FINAL, ease_out(clamp01((t - 24.5) / 1.4))))
    pop(c, T(f"${shown:,}", 190, TEAL, glow_r=18), W / 2, 930, t, 24.5)
    pop(c, T("Same coffee money.", 60, CREAM, DMS, var="Bold"), W / 2, 1120, t, 26.0)
    paste_center(c, you(380, 1.0 if t > 24.6 else blink(t), (0, -0.4)), W / 2, 1500)
    return c

def outro(t):  # 27.5-31
    c = BG.copy(); particles(c, t, 50, 25)
    pop(c, T("WHICH TIMELINE", 110, CREAM), W / 2, 520, t, 27.5)
    pop(c, T("ARE YOU IN?", 130, AMBER, glow_r=14), W / 2, 670, t, 27.8)
    paste_center(c, CUP, 330, 1050, clamp01((t - 28.1) / 0.3))
    pop(c, T("VS", 90, CREAM), W / 2, 1050, t, 28.3)
    # tiny chart icon
    ic = Image.new("RGBA", (220, 200), (0, 0, 0, 0)); di = ImageDraw.Draw(ic)
    di.rounded_rectangle((0, 0, 219, 199), 24, fill=(14, 22, 40, 255), outline=TEAL + (255,), width=5)
    di.line([(25, 160), (70, 130), (100, 145), (140, 90), (165, 100), (195, 40)], fill=TEAL + (255,), width=10)
    paste_center(c, ic, 750, 1050, clamp01((t - 28.1) / 0.3))
    pop(c, T("THE OTHER TIMELINE", 64, TEAL, glow_r=10), W / 2, 1380, t, 28.8)
    d = ImageDraw.Draw(c)
    msg = "Not financial advice. Past returns don't guarantee future ones."
    f = font(DMS, 28, "Bold"); bb = f.getbbox(msg)
    d.text((W / 2 - (bb[2] - bb[0]) / 2, 1800), msg, font=f, fill=CREAM + (120,))
    return fade(c, clamp01((t - (DUR - 0.5)) / 0.5))

SCENES = [(0, 4, hook), (4, 9.5, timeline_a), (9.5, 12, timeline_b_intro), (12, 23, chart), (23, 27.5, result), (27.5, DUR, outro)]

def frame(t):
    for a, b, fn in SCENES:
        if a <= t < b:
            c = fn(t); break
    else:
        c = SCENES[-1][2](t)
    for a, _, _ in SCENES[1:]:  # quick white flash on cuts
        if 0 <= t - a < 0.08:
            c = fade(c, 0.35, (255, 255, 255))
    return c

def render(i):
    a, b, _ = SCENES[i]
    enc = Encoder(f"build/scene{i}.mp4")
    for n in range(int(round(a * FPS)), int(round(b * FPS))):
        enc.write(frame(n / FPS))
    enc.close()

if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)
    if len(sys.argv) > 1:
        ts = [1.5, 3.5, 6.0, 8.5, 11.0, 15.0, 19.0, 22.5, 24.0, 26.5, 29.5]
        ims = [frame(t).convert("RGB").resize((270, 480)) for t in ts]
        sheet = Image.new("RGB", (270 * 6, 480 * 2))
        for i, im in enumerate(ims):
            sheet.paste(im, ((i % 6) * 270, (i // 6) * 480))
        sheet.save("build/contact.png"); sys.exit()
    print(f"invested {INVESTED:.0f} final {FINAL:.0f}")
    with Pool(4) as p:
        p.map(render, range(len(SCENES)))
