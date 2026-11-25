"""Finance ep 1: What IF You Saved $5 a Day Since 2010?  16:9 animation synced to build/timing.json.
python3 video.py stills  -> build/contact.png ;  python3 video.py -> build/beat_XX.mp4"""
import sys, os, json, math, random, csv
from functools import lru_cache
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ep2"))
from common import *
from multiprocessing import Pool

TIM = json.load(open(os.path.join(HERE, "build", "timing.json")))
TOTAL = TIM[-1]["end"]

# ---------------- data ----------------
ROWS = [r for r in csv.DictReader(open(os.path.join(HERE, "..", "finance01", "sp500.csv")))
        if "2010-01-01" <= r["Date"] <= "2026-09-01"]
DATES_ = [r["Date"] for r in ROWS]; PX = [float(r["SP500"]) for r in ROWS]
M = 5 * 365 / 12; NM = len(ROWS)
def sim(sell_idx=None):
    sh = cash = inv = 0.0; I = []; V = []
    for i, p in enumerate(PX):
        inv += M
        if sell_idx is not None and i >= sell_idx:
            if sh: cash += sh * p; sh = 0
            cash += M
        else:
            sh += M / p
        I.append(inv); V.append(sh * p + cash)
    return I, V
INV, VAL = sim()
_, SOLD = sim(DATES_.index("2020-04-01"))
IDX = {d: i for i, d in enumerate(DATES_)}
i2012, i2018, iFEB20, iMAR20, iAPR20 = IDX["2012-01-01"], IDX["2018-01-01"], IDX["2020-02-01"], IDX["2020-03-01"], IDX["2020-04-01"]
iDEC21, iOCT22 = IDX["2021-12-01"], IDX["2022-10-01"]
END = NM - 1

BG = gradient_bg(NAVY2, NAVY)
BG_A = gradient_bg((70, 34, 48), NAVY)
BG_B = gradient_bg((18, 60, 70), NAVY)
GREY = (120, 130, 150)

@lru_cache(maxsize=4096)
def T(txt, size, col=CREAM, f="A", glow_r=0):
    fnt = font(ANTON, size) if f == "A" else font(DMS, size, "Bold")
    return text_sprite(txt, fnt, col + (255,), glow_r=glow_r, glow_col=col)

def money(v):
    return f"${int(round(v)):,}"

def pop(c, spr, x, y, t, t0, t1=1e9, dur=0.35):
    if t < t0 or t > t1 + 0.3:
        return
    p = ease_out((t - t0) / dur); a = clamp01((t - t0) / 0.2) * clamp01((t1 + 0.3 - t) / 0.3)
    s = 0.7 + 0.3 * p
    if s < 0.999:
        spr = spr.resize((max(1, int(spr.width * s)), max(1, int(spr.height * s))), Image.BICUBIC)
    paste_center(c, spr, x, y, a)

@lru_cache(maxsize=256)
def you(size, eo=1.0, look=(0, 0)):
    return you_head(size, eo, look)
def blink(t, per=3.3, off=0.0):
    return 0.1 if ((t + off) % per) < 0.12 else 1.0

def particles(c, t, n=40, seed=5, col=AMBER):
    rng = random.Random(seed); d = ImageDraw.Draw(c)
    for i in range(n):
        x = (rng.uniform(0, W) + t * rng.uniform(-12, 12)) % W
        y = (rng.uniform(0, H) - t * rng.uniform(8, 30)) % H
        r = rng.uniform(1.5, 3.5); d.ellipse((x - r, y - r, x + r, y + r), fill=col + (int(70 + 50 * math.sin(t * 2 + i)),))

@lru_cache(maxsize=8)
def cup(scale=1.0):
    w, h = int(150 * scale), int(190 * scale)
    img = Image.new("RGBA", (w + 10, h + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.polygon([(0, 30 * scale), (w, 30 * scale), (w * 0.85, h), (w * 0.15, h)], fill=CREAM + (255,), outline=INK + (255,))
    d.rounded_rectangle((0, 0, w, 38 * scale), max(2, int(10 * scale)), fill=(120, 80, 50, 255))
    d.rectangle((w * 0.12, 80 * scale, w * 0.88, 140 * scale), fill=AMBER + (255,))
    f = font(ANTON, max(8, int(46 * scale))); bb = f.getbbox("$5")
    d.text((w / 2 - (bb[2] - bb[0]) / 2 - bb[0], 110 * scale - (bb[3] - bb[1]) / 2 - bb[1]), "$5", font=f, fill=INK + (255,))
    return img

def panel(w, h, col=TEAL, fill=(14, 22, 40, 240), r=30, width=5):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=fill, outline=col + (255,), width=width)
    return img

@lru_cache(maxsize=4)
def chart_icon(s=1.0):
    w, h = int(220 * s), int(200 * s)
    ic = Image.new("RGBA", (w, h), (0, 0, 0, 0)); di = ImageDraw.Draw(ic)
    di.rounded_rectangle((0, 0, w - 1, h - 1), int(24 * s), fill=(14, 22, 40, 255), outline=TEAL + (255,), width=max(2, int(5 * s)))
    pts = [(25, 160), (70, 130), (100, 145), (140, 90), (165, 100), (195, 40)]
    di.line([(x * s, y * s) for x, y in pts], fill=TEAL + (255,), width=max(3, int(10 * s)))
    return ic

def stamp(c, txt, x, y, t, t0, col=CORAL, size=90, rot=-8):
    if t < t0:
        return
    p = ease_out((t - t0) / 0.25)
    spr = T(txt, size, col, "A", 0)
    box = Image.new("RGBA", (spr.width + 40, spr.height + 20), (0, 0, 0, 0))
    ImageDraw.Draw(box).rounded_rectangle((4, 4, box.width - 5, box.height - 5), 16, outline=col + (255,), width=8)
    box.alpha_composite(spr, (20, 10))
    box = box.rotate(rot, expand=True, resample=Image.BICUBIC)
    s = 1.6 - 0.6 * p
    box = box.resize((int(box.width * s), int(box.height * s)), Image.BICUBIC)
    paste_center(c, box, x, y, clamp01(p * 2))

# ---------------- chart ----------------
CX0, CY0, CX1, CY1 = 150, 190, 1380, 840
def chart(c, t, k, sold_k=None, highlight=None, dim_main=False, vmax_override=None):
    """k: float index of last month drawn on main line."""
    k = max(0.0, min(END, k)); ki = int(k)
    vis = VAL[:ki + 1] + ([SOLD[j] for j in range(iAPR20, int(sold_k) + 1)] if sold_k else [])
    vmax = vmax_override or max(6000, max(vis) * 1.25)
    d = ImageDraw.Draw(c)
    def X(i): return CX0 + (CX1 - CX0) * i / END
    def Y(v): return CY1 - (CY1 - CY0) * v / vmax
    step = [1000, 2000, 5000, 10000, 20000, 25000, 50000][[1000, 2000, 5000, 10000, 20000, 25000, 50000].index(next(s for s in [1000, 2000, 5000, 10000, 20000, 25000, 50000] if vmax / s <= 6))]
    fs = font(DMS, 26, "Bold")
    v = 0
    while v <= vmax:
        y = Y(v); d.line((CX0, y, CX1, y), fill=(255, 255, 255, 25), width=2)
        d.text((CX0 - 10 - fs.getlength(f"${v // 1000}K" if v else "$0"), y - 16), f"${v // 1000}K" if v else "$0", font=fs, fill=CREAM + (140,))
        v += step
    for yr in range(2010, 2027, 2):
        i = min((yr - 2010) * 12, END)
        d.text((X(i) - 30, CY1 + 14), str(yr), font=fs, fill=CREAM + (150,))
    pv = [(X(i), Y(VAL[i])) for i in range(ki + 1)]
    frac = k - ki
    if ki < END and frac > 0:
        pv.append((X(k), Y(lerp(VAL[ki], VAL[ki + 1], frac))))
    pi = [(X(i), Y(INV[i])) for i in range(ki + 1)]
    if len(pv) > 1:
        ov = Image.new("RGBA", c.size, (0, 0, 0, 0))
        ImageDraw.Draw(ov).polygon(pv + [(pv[-1][0], CY1), (CX0, CY1)], fill=TEAL + (30 if dim_main else 45,))
        c.alpha_composite(ov)
        d = ImageDraw.Draw(c)
        d.line(pi, fill=AMBER + (255,), width=6)
        d.line(pv, fill=(TEAL if not dim_main else GREY) + (255,), width=8, joint="curve")
        x, y = pv[-1]
        d.ellipse((x - 13, y - 13, x + 13, y + 13), fill=TEAL + (255,), outline=CREAM + (255,), width=4)
    if sold_k:
        ps = [(X(i), Y(SOLD[i])) for i in range(iAPR20, int(sold_k) + 1)]
        if len(ps) > 1:
            d.line(ps, fill=CORAL + (255,), width=7)
            x, y = ps[-1]; d.ellipse((x - 11, y - 11, x + 11, y + 11), fill=CORAL + (255,))
    return X, Y

def counters(c, k, label="TIMELINE B", sold=None):
    ki = int(max(0, min(END, k)))
    x = 1650
    paste_center(c, T(label, 64, TEAL, "A", 8), x, 230)
    paste_center(c, T("PUT IN", 34, AMBER, "D"), x, 330)
    paste_center(c, T(money(INV[ki]), 66, AMBER), x, 390)
    paste_center(c, T("WORTH", 34, TEAL, "D"), x, 480)
    paste_center(c, T(money(VAL[ki]), 76, TEAL), x, 545)
    d = ImageDraw.Draw(c)
    yr = DATES_[ki][:7].replace("-", " / ")
    paste_center(c, T(yr, 34, CREAM, "D"), x, 625)
    if sold is not None:
        paste_center(c, T("IF YOU SOLD", 30, CORAL, "D"), x, 690)
        paste_center(c, T(money(sold), 56, CORAL), x, 745)

def footnote(c):
    d = ImageDraw.Draw(c)
    d.text((CX0, 900), "S&P 500 monthly avg. price (R. Shiller data). $152.08 invested on the 1st of each month. Price only, no dividends.",
           font=font(DMS, 22, "Bold"), fill=CREAM + (95,))

# ---------------- helpers for timing ----------------
class B:
    def __init__(self, i):
        self.b = TIM[i]; self.s = [x["start"] for x in self.b["sents"]]
        self.t0, self.t1 = self.b["start"], self.b["end"]
    def S(self, i):
        return self.s[min(i, len(self.s) - 1)]
    def p(self, t, a=None, b=None):
        a = self.t0 if a is None else a; b = self.t1 if b is None else b
        return clamp01((t - a) / max(0.01, b - a))

# ---------------- scenes ----------------
def sc_hook(t, b):
    c = BG.copy(); particles(c, t)
    if t < b.S(2):
        pop(c, T("WHAT IF YOU SAVED", 100, CREAM), W / 2, 170, t, b.t0 + 0.1)
        pop(c, T("$5 A DAY SINCE 2010?", 120, AMBER, "A", 14), W / 2, 300, t, b.t0 + 0.4)
        paste_center(c, you(400, blink(t), (0.7, 0.2)), W / 2 - 140, 700)
        sc = 1.0 + 0.35 * ease_out(b.p(t, b.S(1), b.S(1) + 0.5))
        cp = cup(1.0); cp = cp.resize((int(cp.width * sc), int(cp.height * sc)), Image.BICUBIC)
        paste_center(c, cp, W / 2 + 200, 660 + 10 * math.sin(t * 3), clamp01((t - b.t0 - 0.8) / 0.3))
    else:
        c = BG.copy()
        d = ImageDraw.Draw(c)
        ov = Image.new("RGBA", c.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        od.rectangle((0, 0, W / 2, H), fill=CORAL + (28,)); od.rectangle((W / 2, 0, W, H), fill=TEAL + (28,))
        c.alpha_composite(ov); d = ImageDraw.Draw(c)
        g = ease(b.p(t, b.S(2), b.S(2) + 1.0))
        d.line([(W / 2, H), (W / 2, 900)], fill=AMBER + (255,), width=10)
        d.line([(W / 2, 900), (lerp(W / 2, W / 4, g), lerp(900, 760, g))], fill=CORAL + (255,), width=10)
        d.line([(W / 2, 900), (lerp(W / 2, 3 * W / 4, g), lerp(900, 760, g))], fill=TEAL + (255,), width=10)
        pop(c, T("TIMELINE A", 80, CORAL, "A", 8), W / 4, 150, t, b.S(2) + 0.3)
        pop(c, T("TIMELINE B", 80, TEAL, "A", 8), 3 * W / 4, 150, t, b.S(2) + 0.5)
        paste_center(c, you(260, blink(t), (0.5, 0)), W / 4 - 60, 500, clamp01((t - b.S(2) - 0.6) / 0.3))
        paste_center(c, cup(0.7), W / 4 + 110, 470, clamp01((t - b.S(2) - 0.6) / 0.3))
        paste_center(c, you(260, blink(t, 3.1, 1), (-0.5, 0)), 3 * W / 4 + 60, 500, clamp01((t - b.S(2) - 0.8) / 0.3))
        paste_center(c, chart_icon(0.7), 3 * W / 4 - 110, 470, clamp01((t - b.S(2) - 0.8) / 0.3))
        pop(c, T("SAME $5", 70, AMBER), W / 2, 330, t, b.S(3), b.S(4) - 0.2)
        if t > b.S(4):
            pop(c, T("$0", 110, CORAL, "A", 10), W / 4, 730, t, b.S(4) + 0.4)
            v = lerp(0, 99172, ease_out(b.p(t, b.S(4) + 0.6, b.S(4) + 2.6)))
            pop(c, T("≈ " + money(v), 100, TEAL), 3 * W / 4, 730, t, b.S(4) + 0.6)
    return c

def sc_rule(t, b):
    c = BG.copy(); particles(c, t, 30, 7)
    # calendar
    a1 = 1 - clamp01((t - b.S(2) + 0.2) / 0.3)
    if a1 > 0:
        cal = panel(360, 380, CORAL, (244, 234, 213, 255), 28, 0)
        dd = ImageDraw.Draw(cal); dd.rounded_rectangle((0, 0, 359, 90), 28, fill=CORAL + (255,)); dd.rectangle((0, 50, 359, 90), fill=CORAL + (255,))
        f = font(ANTON, 54); dd.text((180 - f.getlength("EVERY DAY") / 2, 12), "EVERY DAY", font=f, fill=CREAM + (255,))
        f2 = font(ANTON, 190); dd.text((180 - f2.getlength("$5") / 2, 110), "$5", font=f2, fill=INK + (255,))
        paste_center(c, cal, W / 2 - 330, 480, a1 * clamp01((t - b.t0) / 0.3))
        pop(c, T("$5 × 365 ÷ 12", 70, CREAM), W / 2 + 280, 400, t, b.S(1), b.S(2) - 0.5)
        pop(c, T("≈ $152 / MONTH", 100, AMBER, "A", 12), W / 2 + 280, 540, t, b.S(1) + 0.5, b.S(2) - 0.5)
    if t > b.S(2) - 0.2:
        d = ImageDraw.Draw(c)
        g = ease(b.p(t, b.S(2) - 0.2, b.S(2) + 0.6))
        d.line([(W / 2, 1000), (W / 2, 820)], fill=AMBER + (255,), width=10)
        d.line([(W / 2, 820), (lerp(W / 2, 480, g), lerp(820, 600, g))], fill=CORAL + (255,), width=10)
        g2 = ease(b.p(t, b.S(3) - 0.2, b.S(3) + 0.6))
        d.line([(W / 2, 820), (lerp(W / 2, 1440, g2), lerp(820, 600, g2))], fill=TEAL + (255,), width=10)
        paste_center(c, you(180, blink(t), (0, -0.5)), W / 2, 920)
        pop(c, T("A: SPEND", 80, CORAL, "A", 8), 480, 230, t, b.S(2))
        pop(c, cup(1.0), 480, 450, t, b.S(2) + 0.2)
        pop(c, T("B: INVEST", 80, TEAL, "A", 8), 1440, 230, t, b.S(3))
        if t > b.S(3):
            pn = panel(560, 300, TEAL)
            dd = ImageDraw.Draw(pn)
            f = font(ANTON, 54); dd.text((280 - f.getlength("S&P 500 INDEX FUND") / 2, 20), "S&P 500 INDEX FUND", font=f, fill=CREAM + (255,))
            n = int(500 * ease(b.p(t, b.S(4), b.S(4) + 2.0)))
            for i in range(n):
                cx = 30 + (i % 50) * 10; cy = 110 + (i // 50) * 17
                dd.rectangle((cx, cy, cx + 6, cy + 12), fill=(AMBER if i % 7 else TEAL) + (255,))
            paste_center(c, pn, 1440, 450, clamp01((t - b.S(3)) / 0.3))
            pop(c, T("~500 BIG US COMPANIES", 40, AMBER, "D"), 1440, 640, t, b.S(4))
        stamp(c, "NO STOCK PICKING", W / 2, 330, t, b.S(5), CORAL, 60)
    return c

def sc_timeline_a(t, b):
    c = BG_A.copy()
    d = ImageDraw.Draw(c)
    d.rectangle((0, 780, W, H), fill=(60, 40, 40, 255))
    d.rectangle((0, 640, 900, 790), fill=(120, 80, 50, 255)); d.rectangle((0, 630, 900, 650), fill=(150, 100, 60, 255))
    d.rounded_rectangle((120, 120, 760, 460), 20, fill=(30, 40, 60, 255), outline=(150, 100, 60, 255), width=12)
    f = font(DMS, 40, "Bold"); d.text((170, 160), "MENU", font=f, fill=CREAM + (220,))
    for i, (n, p) in enumerate([("Latte", "$5"), ("Cappuccino", "$5"), ("Flat white", "$5")]):
        d.text((170, 230 + i * 60), n, font=f, fill=CREAM + (200,)); d.text((640, 230 + i * 60), p, font=f, fill=AMBER + (255,))
    paste_center(c, T("TIMELINE A", 70, CORAL, "A", 8), 1500, 120)
    # year counter
    yp = ease(b.p(t, b.S(2), b.S(3) + 1.0))
    yr = int(lerp(2010, 2026, yp))
    paste_center(c, T(str(yr), 120, CREAM), 1500, 260)
    paste_center(c, you(300, blink(t), (-0.4, 0.1)), 520, 560)
    paste_center(c, cup(0.8), 700, 600 + 6 * math.sin(t * 2.5))
    # pile of cups
    n = int(70 * yp); rng = random.Random(4)
    for i in range(n):
        x = rng.uniform(1000, 1900); y = 1030 - (i // 14) * 60 + rng.uniform(-8, 8)
        paste_center(c, cup(0.4).rotate(rng.uniform(-15, 15), expand=True), x, y)
    coffees = int(round(INV[-1] / 5) * yp)
    if t > b.S(3):
        pop(c, T(f"{coffees:,} COFFEES", 76, AMBER), 1500, 400, t, b.S(3))
    pop(c, T(money(INV[-1]) + " SPENT", 80, CREAM), 1500, 510, t, b.S(4))
    if t > b.S(5) + 1.3:
        stamp(c, "LEFT TODAY: $0", 1500, 640, t, b.S(5) + 1.3, CORAL, 80)
    return c

def sc_inflation(t, b):
    c = BG_A.copy(); particles(c, t, 25, 3, CORAL)
    d = ImageDraw.Draw(c)
    # mattress
    d.rounded_rectangle((200, 700, 900, 840), 40, fill=(200, 205, 225, 255), outline=INK + (255,), width=5)
    for x in range(260, 880, 80):
        d.line((x, 715, x, 825), fill=(160, 165, 190, 255), width=3)
    shrink = 1 - 0.29 * ease(b.p(t, b.S(1) + 0.5, b.S(2) + 1.5))
    bw, bh = int(420 * shrink), int(200 * shrink)
    note = Image.new("RGBA", (bw, bh), (0, 0, 0, 0)); nd = ImageDraw.Draw(note)
    nd.rounded_rectangle((0, 0, bw - 1, bh - 1), 14, fill=(120, 200, 140, 255), outline=(40, 90, 50, 255), width=5)
    nd.ellipse((bw / 2 - bh * 0.32, bh * 0.18, bw / 2 + bh * 0.32, bh * 0.82), outline=(40, 90, 50, 255), width=4)
    f = font(ANTON, max(10, int(70 * shrink))); nd.text((18, 10), "$100", font=f, fill=(30, 70, 40, 255))
    paste_center(c, note, 550, 600)
    paste_center(c, you(220, blink(t), (-0.6, 0.3)), 1000, 680)
    pop(c, T("+41% PRICES", 110, CORAL, "A", 12), 1440, 330, t, b.S(1))
    pop(c, T("US CPI, 2010 → 2023", 40, CREAM, "D"), 1440, 450, t, b.S(1) + 0.4)
    if t > b.S(2):
        bp = ease(b.p(t, b.S(2), b.S(2) + 1.5))
        val = lerp(100, 71, bp)
        d = ImageDraw.Draw(c)
        d.rounded_rectangle((1160, 560, 1720, 620), 20, outline=CREAM + (200,), width=4)
        d.rounded_rectangle((1166, 566, 1166 + 548 * val / 100, 614), 16, fill=(120, 200, 140, 255))
        pop(c, T(f"$100 NOW BUYS ≈ ${int(val)} OF 2010 STUFF", 40, CREAM, "D"), 1440, 680, t, b.S(2))
    return c

def chart_scene(t, b, k0, k1, label_events=(), sold=False, bg=BG):
    c = bg.copy()
    k = lerp(k0, k1, ease(b.p(t, b.t0 + 0.3, b.t1 - 0.6)))
    chart(c, t, k)
    counters(c, k)
    footnote(c)
    paste_center(c, you(140, blink(t), (-0.6, -0.4)), 1650, 905)
    return c, k

def sc_b_start(t, b):
    c, k = chart_scene(t, b, 0, i2012, bg=BG_B)
    pop(c, T("Same coffee money. Invested.", 46, CREAM, "D"), 760, 120, t, b.t0 + 0.2)
    if t > b.S(3):
        stamp(c, "MOST PEOPLE QUIT HERE", 760, 470, t, b.S(3), CORAL, 70)
    return c

def sc_compound(t, b):
    c, k = chart_scene(t, b, i2012, i2018, bg=BG_B)
    pop(c, T("RETURNS EARN RETURNS", 54, AMBER, "A", 8), 760, 95, t, b.S(1))
    pop(c, T("= COMPOUNDING", 50, TEAL, "A", 8), 760, 160, t, b.S(2))
    return c

def sc_covid(t, b):
    c = BG.copy()
    k = lerp(i2018, iMAR20, ease(b.p(t, b.t0 + 0.2, b.S(1) + 1.2)))
    X, Y = chart(c, t, k, vmax_override=45000)
    counters(c, k); footnote(c)
    pop(c, T("2020: PANDEMIC", 70, CORAL, "A", 8), 700, 140, t, b.t0 + 0.2)
    if k >= iMAR20 - 0.01:
        pop(c, T("−" + money(VAL[iFEB20] - VAL[iMAR20]), 90, CORAL, "A", 12), X(iMAR20) - 160, Y(VAL[iMAR20]) + 120, t, b.S(1) + 1.2)
        pop(c, T("ON PAPER", 40, CREAM, "D"), X(iMAR20) - 160, Y(VAL[iMAR20]) + 200, t, b.S(2))
    fl = clamp01(1 - (t - b.S(1) - 1.2) / 0.25) if t > b.S(1) + 1.2 else 0
    c = fade(c, fl * 0.35, CORAL)
    eo = 1.0 if t < b.S(3) else 1.0
    paste_center(c, you(140, blink(t), (0, 0.6) if t > b.S(3) else (-0.6, -0.4)), 1650, 905)
    z = 1.0 + 0.25 * ease(b.p(t, b.S(1) + 1.0, b.S(1) + 2.5)) - 0.25 * ease(b.p(t, b.t1 - 1.0, b.t1))
    return camera(c, z, 1050, 450)

def sc_panic(t, b):
    c = BG.copy()
    sk = lerp(iAPR20, END, ease(b.p(t, b.S(1) + 0.5, b.S(2) + 2.0))) if t > b.S(1) + 0.5 else None
    chart(c, t, iMAR20, sold_k=sk, dim_main=False, vmax_override=60000 if not sk else max(60000, SOLD[int(sk)] * 1.3))
    counters(c, iMAR20, sold=SOLD[int(sk)] if sk else None); footnote(c)
    pop(c, T("THE TIMELINE SPLITS AGAIN", 60, AMBER, "A", 8), 760, 130, t, b.t0 + 0.2)
    if t > b.S(1):
        pop(c, T("SELL EVERYTHING!", 60, CORAL, "A", 8), 900, 260, t, b.S(1), b.S(2) + 2)
    if t > b.S(3):
        pop(c, T("...or do nothing?", 56, TEAL, "D"), 760, 360, t, b.S(3))
    paste_center(c, you(140, blink(t), (0, 0.5)), 1650, 905)
    return c

def sc_kept(t, b):
    c = BG_B.copy()
    k = lerp(iMAR20, END, ease(b.p(t, b.t0 + 0.2, b.t1 - 0.5)))
    X, Y = chart(c, t, k, sold_k=END)
    counters(c, k, sold=SOLD[END]); footnote(c)
    pop(c, T("KEPT BUYING", 70, TEAL, "A", 10), 600, 140, t, b.t0 + 0.3)
    if k >= iOCT22:
        pop(c, T("−" + money(VAL[iDEC21] - VAL[iOCT22]), 70, CORAL, "A", 8), X(iOCT22) - 40, Y(VAL[iOCT22]) + 110, t, b.S(1) + 1.0)
    if t > b.S(3):
        stamp(c, "SHARES ON SALE", 600, 330, t, b.S(3), AMBER, 60)
    paste_center(c, you(140, blink(t), (-0.6, -0.4)), 1650, 905)
    return c

def bar(c, x, y, w, h, col, a=1.0):
    if h < 2:
        return
    ov = Image.new("RGBA", (w, int(h)), col + (255,))
    paste_center(c, ov, x, y - h / 2, a)

def sc_result(t, b):
    c = BG.copy(); particles(c, t, 50, 21, TEAL)
    pop(c, T("SEPTEMBER 2026", 70, CREAM), W / 2, 110, t, b.t0)
    base = 820; scale = 560 / VAL[-1]
    hp = ease_out(b.p(t, b.S(1), b.S(1) + 1.2)); hv = ease_out(b.p(t, b.S(2), b.S(2) + 1.6))
    bar(c, 720, base, 260, INV[-1] * scale * hp, AMBER)
    bar(c, 1200, base, 260, VAL[-1] * scale * hv, TEAL)
    if t > b.S(1):
        pop(c, T("YOU PUT IN", 44, AMBER, "D"), 720, base + 50, t, b.S(1))
        pop(c, T(money(INV[-1] * hp), 72, AMBER), 720, base - INV[-1] * scale * hp - 60, t, b.S(1))
    if t > b.S(2):
        pop(c, T("IT'S WORTH", 44, TEAL, "D"), 1200, base + 50, t, b.S(2))
        pop(c, T("≈ " + money(round(VAL[-1] * hv, -1)), 72, TEAL), 1200, base - VAL[-1] * scale * hv - 60, t, b.S(2))
    pop(c, T(f"{VAL[-1] / INV[-1]:.1f}×", 150, TEAL, "A", 16), 1620, 500, t, b.S(3))
    pop(c, T("price only · no dividends", 34, CREAM, "D"), 1620, 620, t, b.S(4))
    paste_center(c, you(220, blink(t), (0.5, -0.5)), 260, 780)
    return c

LATE = [("2010", 0), ("2015", IDX["2015-01-01"]), ("2020", IDX["2020-01-01"]), ("2022", IDX["2022-01-01"])]
def late_vals(si):
    inv = (NM - si) * M; sh = sum(M / PX[i] for i in range(si, NM)); return inv, sh * PX[-1]
def sc_late(t, b):
    c = BG.copy(); particles(c, t, 30, 31)
    pop(c, T("STARTING LATE?", 80, AMBER, "A", 10), W / 2, 110, t, b.t0)
    base = 800; scale = 520 / VAL[-1]
    for j, (lab, si) in enumerate(LATE):
        t0 = b.t0 + 0.3 if j == 0 else b.S(j)
        if t < t0:
            continue
        inv, val = late_vals(si)
        x = 330 + j * 430; p = ease_out(clamp01((t - t0) / 1.0))
        bar(c, x - 75, base, 120, inv * scale * p, AMBER)
        bar(c, x + 75, base, 120, val * scale * p, TEAL)
        pop(c, T("START " + lab, 44, CREAM), x, base + 50, t, t0)
        pop(c, T(money(round(inv, -2)), 36, AMBER, "D"), x - 75, base - inv * scale * p - 30, t, t0 + 0.6)
        pop(c, T(money(round(val, -2)), 40, TEAL, "D"), x + 75, base - val * scale * p - 30, t, t0 + 0.6)
    d = ImageDraw.Draw(c)
    d.rectangle((1500, 180, 1530, 210), fill=AMBER + (255,)); d.text((1545, 178), "put in", font=font(DMS, 30, "Bold"), fill=CREAM + (220,))
    d.rectangle((1680, 180, 1710, 210), fill=TEAL + (255,)); d.text((1725, 178), "worth", font=font(DMS, 30, "Bold"), fill=CREAM + (220,))
    return c

def jar(fill_p, w=300, h=380):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle((20, 40, w - 20, h - 5), 40, fill=(40, 60, 90, 200), outline=CREAM + (230,), width=6)
    d.rounded_rectangle((50, 10, w - 50, 50), 10, fill=(120, 130, 150, 255))
    fh = (h - 60) * fill_p
    if fh > 4:
        d.rounded_rectangle((30, h - 15 - fh, w - 30, h - 15), 32, fill=AMBER + (255,))
        for i in range(int(fh / 26)):
            y = h - 30 - i * 26
            d.line((40, y, w - 40, y), fill=(214, 140, 40, 255), width=3)
    return img

def sc_scale(t, b):
    c = BG.copy(); particles(c, t, 40, 41)
    pop(c, T("HOW MUCH PER DAY?", 80, AMBER, "A", 10), W / 2, 110, t, b.t0)
    items = [("$1 / DAY", 0.1, VAL[-1] / 5, b.S(1)), ("$5 / DAY", 0.5, VAL[-1], b.t0 + 0.3), ("$10 / DAY", 1.0, VAL[-1] * 2, b.S(2))]
    for j, (lab, fp, v, t0) in enumerate(items):
        if t < t0:
            continue
        x = 420 + j * 540; p = ease_out(clamp01((t - t0) / 1.2))
        paste_center(c, jar(fp * p), x, 560)
        pop(c, T(lab, 56, CREAM), x, 820, t, t0)
        pop(c, T("≈ " + money(round(v * p, -2)), 64, TEAL), x, 300, t, t0 + 0.3)
    return c

def sc_myth(t, b):
    c = BG.copy(); particles(c, t, 25, 51)
    paste_center(c, cup(1.6), 430, 520)
    pop(c, T("THE LATTE FACTOR", 80, AMBER, "A", 10), 430, 180, t, b.t0)
    stamp(c, "MYTH?", 430, 520, t, b.t0 + 2.5, CORAL, 100)
    if t > b.S(1):
        x0 = 900; d = ImageDraw.Draw(c)
        pop(c, T("PAYCHECK", 44, CREAM, "D"), 1400, 300, t, b.S(1))
        d.rounded_rectangle((x0, 350, 1880, 450), 20, outline=CREAM + (200,), width=4)
        rp = ease(b.p(t, b.S(1) + 0.3, b.S(1) + 1.5))
        d.rounded_rectangle((x0 + 6, 356, x0 + 6 + 962 * 0.5 * rp, 444), 16, fill=CORAL + (255,))
        if rp > 0.5:
            d.text((x0 + 30, 375), "RENT", font=font(ANTON, 50), fill=CREAM + (255,))
        d.rounded_rectangle((x0 + 6 + 481, 356, x0 + 6 + 481 + 30, 444), 6, fill=AMBER + (int(255 * rp),))
        pop(c, T("coffee", 30, AMBER, "D"), x0 + 500, 480, t, b.S(1) + 1.5)
    if t > b.S(2):
        pop(c, T("THE HABIT IS THE POINT", 64, TEAL, "A", 10), 1390, 640, t, b.S(2))
        d = ImageDraw.Draw(c)
        n = int(12 * ease(b.p(t, b.S(3), b.S(3) + 2.5)))
        for i in range(n):
            x = 960 + i * 75
            d.rounded_rectangle((x, 760, x + 60, 820), 10, fill=TEAL + (255,))
            d.text((x + 8, 772), "$152", font=font(DMS, 20, "Bold"), fill=INK + (255,))
    return c

def sc_how(t, b):
    c = BG_B.copy(); particles(c, t, 30, 61, TEAL)
    pop(c, T("HOW TIMELINE B WORKS IN REAL LIFE", 70, CREAM), W / 2, 120, t, b.t0)
    cards = [("1", "AUTOMATIC", "a transfer on payday", b.S(1)), ("2", "SIMPLE & CHEAP", "broad index, low fees", b.S(2)), ("3", "DON'T CHECK DAILY", "do nothing, keep going", b.S(3))]
    for j, (n, h1, h2, t0) in enumerate(cards):
        if t < t0:
            continue
        x = 360 + j * 600
        pn = panel(520, 560, [AMBER, TEAL, CORAL][j])
        pop(c, pn, x, 560, t, t0)
        pop(c, T(n, 140, [AMBER, TEAL, CORAL][j], "A", 10), x, 400, t, t0 + 0.1)
        pop(c, T(h1, 54, CREAM), x, 600, t, t0 + 0.2)
        pop(c, T(h2, 34, CREAM, "D"), x, 690, t, t0 + 0.3)
    return c

def sc_honest(t, b):
    c = BG.copy()
    pop(c, T("NOT FINANCIAL ADVICE", 110, CORAL, "A", 12), W / 2, 150, t, b.t0)
    items = [("The past doesn't promise the future", b.S(1)), ("Markets can go nowhere for years", b.S(2)),
             ("Emergency fund first", b.S(3)), ("No expensive debt", b.S(3) + 1.2), ("Only money you won't need soon", b.S(3) + 2.4)]
    for j, (txt, t0) in enumerate(items):
        if t < t0:
            continue
        y = 320 + j * 110
        d = ImageDraw.Draw(c)
        a = clamp01((t - t0) / 0.3)
        d.rounded_rectangle((460, y - 30, 520, y + 30), 12, outline=TEAL + (int(255 * a),), width=6)
        if t > t0 + 0.3:
            d.line([(472, y), (488, y + 18), (512, y - 18)], fill=TEAL + (255,), width=8)
        paste_center(c, T(txt, 52, CREAM, "D"), 560 + T(txt, 52, CREAM, "D").width / 2, y, a)
    paste_center(c, you(220, blink(t), (-0.5, -0.3)), 1680, 820)
    return c

def sc_outro(t, b):
    c = BG.copy(); particles(c, t, 50, 71)
    d = ImageDraw.Draw(c)
    d.line([(W / 2, H), (W / 2, 820)], fill=AMBER + (255,), width=10)
    d.line([(W / 2, 820), (480, 640)], fill=CORAL + (255,), width=10)
    d.line([(W / 2, 820), (1440, 640)], fill=TEAL + (255,), width=10)
    paste_center(c, you(240, blink(t), (0.6, 0)), 430, 480); paste_center(c, cup(0.7), 600, 460)
    paste_center(c, you(240, blink(t, 3.0, 1), (-0.6, 0)), 1490, 480); paste_center(c, chart_icon(0.7), 1320, 460)
    pop(c, T("Enjoy your coffee.", 56, CREAM, "D"), W / 2, 170, t, b.t0 + 1.5, b.S(2) - 0.3)
    pop(c, T("WHICH TIMELINE", 100, CREAM), W / 2, 130, t, b.S(2))
    pop(c, T("ARE YOU IN?", 120, AMBER, "A", 14), W / 2, 260, t, b.S(2) + 0.3)
    if t > b.S(2) + 2:
        pop(c, panel(620, 110, CREAM, (244, 234, 213, 255), 30, 0), W / 2, 960, t, b.S(2) + 2)
        pop(c, T("What would YOU do with $5 a day?", 36, INK, "D"), W / 2, 960, t, b.S(2) + 2.1)
    pop(c, T("THE OTHER TIMELINE", 70, TEAL, "A", 10), W / 2, 660, t, b.S(3))
    return fade(c, clamp01((t - (b.t1 - 0.6)) / 0.6))

SCENES = {"hook": sc_hook, "rule": sc_rule, "timeline_a": sc_timeline_a, "inflation": sc_inflation,
          "b_start": sc_b_start, "compound": sc_compound, "covid": sc_covid, "panic": sc_panic, "kept": sc_kept,
          "result": sc_result, "late": sc_late, "scale": sc_scale, "myth": sc_myth, "how": sc_how,
          "honest": sc_honest, "outro": sc_outro}

# ---------------- subtitles ----------------
BAND = Image.new("RGBA", (W, 190), (0, 0, 0, 0))
for _y in range(190):
    ImageDraw.Draw(BAND).line([(0, _y), (W, _y)], fill=(5, 8, 16, int(210 * (_y / 190) ** 0.8)))

@lru_cache(maxsize=512)
def sub_lines(txt):
    f = font(DMS, 44, "Bold"); words = txt.split(); lines = [""]
    for w in words:
        test = (lines[-1] + " " + w).strip()
        if f.getlength(test) > 1500 and lines[-1]:
            lines.append(w)
        else:
            lines[-1] = test
    return [T(l, 44, CREAM, "D") for l in lines]

def subtitles(c, t):
    for bb in TIM:
        if bb["start"] - 0.5 <= t <= bb["end"] + 0.5:
            for s in bb["sents"]:
                if s["start"] - 0.05 <= t <= s["end"] + 0.25:
                    c.alpha_composite(BAND, (0, H - BAND.height))
                    ls = sub_lines(s["text"])
                    y = H - 70 - (len(ls) - 1) * 56
                    for i, l in enumerate(ls):
                        paste_center(c, l, W / 2, y + i * 56)
                    return

def frame(t, bi=None):
    if bi is None:
        bi = next((i for i, x in enumerate(TIM) if x["start"] <= t < x["end"]), len(TIM) - 1)
        if t < TIM[0]["start"]:
            bi = 0
    b = B(bi)
    c = SCENES[TIM[bi]["name"]](t, b)
    if 0 <= t - b.t0 < 0.25 and bi > 0:
        c = fade(c, 1 - (t - b.t0) / 0.25, NAVY)
    subtitles(c, t)
    return c

def render(bi):
    a = 0.0 if bi == 0 else TIM[bi]["start"]; e = TIM[bi]["end"]
    enc = Encoder(os.path.join(HERE, "build", f"beat_{bi:02d}.mp4"))
    for n in range(int(round(a * FPS)), int(round(e * FPS))):
        enc.write(frame(n / FPS, bi))
    enc.close()
    return bi

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        ims = []
        for bi, x in enumerate(TIM):
            for q in (0.35, 0.92):
                ims.append(frame(lerp(x["start"], x["end"], q), bi).convert("RGB").resize((384, 216)))
        sheet = Image.new("RGB", (384 * 6, 216 * ((len(ims) + 5) // 6)))
        for i, im in enumerate(ims):
            sheet.paste(im, ((i % 6) * 384, (i // 6) * 216))
        sheet.save(os.path.join(HERE, "build", "contact.png")); sys.exit()
    only = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else range(len(TIM))
    with Pool(4) as p:
        print(p.map(render, only))
