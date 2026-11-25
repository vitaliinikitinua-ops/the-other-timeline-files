"""Ep 2 trailer: What IF You Could Delete Any Memory?  (render: python3 trailer.py)"""
import sys, math, random
from multiprocessing import Pool
from common import *

DUR = 30.0
# narration segments (from silencedetect on trailer_vo.mp3)
SUBS = [
    (0.0, 2.0, "What if you could delete any memory..."),
    (2.4, 3.3, "with one tap?"),
    (3.8, 5.5, "That embarrassing moment in class?"),
    (5.9, 6.3, "Gone."),
    (6.7, 7.3, "The breakup?"),
    (7.7, 8.1, "Gone."),
    (8.45, 10.1, "Four million memories..."),
    (10.4, 12.6, "and every single one has a delete button."),
    (13.25, 14.8, "But every time you delete one..."),
    (15.15, 17.0, "something else disappears with it."),
    (17.4, 20.5, "And one morning, a stranger knocks on your door and says:"),
    (20.8, 22.7, "\"You promised you'd never forget me.\""),
    (23.35, 25.1, "What if you could delete any memory?"),
    (25.65, 26.6, "Would you press it?"),
]
SCENES = [(0.0, 3.8), (3.8, 8.4), (8.4, 13.2), (13.2, 17.4), (17.4, 23.3), (23.3, DUR)]

BG = gradient_bg(NAVY2, NAVY)
BG_RED = gradient_bg((60, 30, 50), NAVY)
YOU = {}
def you(size, eo=1.0, look=(0, 0)):
    k = (size, round(eo, 2), look)
    if k not in YOU:
        YOU[k] = you_head(size, eo, look)
    return YOU[k]

def blink(t, period=3.1, off=0.0):
    p = (t + off) % period
    return 0.1 if p < 0.12 else 1.0

CARDS = {}
def card(label, scale=1.0, tint=AMBER):
    k = (label, scale, tint)
    if k not in CARDS:
        CARDS[k] = memory_card(label, scale, tint)
    return CARDS[k]

def shatter(canvas, cx, cy, t, w=220, h=130, col=AMBER, seed=1):
    """card dissolving into particles; t in 0..1"""
    rng = random.Random(seed)
    d = ImageDraw.Draw(canvas)
    for i in range(90):
        x0 = cx + rng.uniform(-w / 2, w / 2); y0 = cy + rng.uniform(-h / 2, h / 2)
        ang = rng.uniform(0, 6.28); sp = rng.uniform(80, 420)
        x = x0 + math.cos(ang) * sp * t; y = y0 + math.sin(ang) * sp * t - 120 * t
        a = int(255 * (1 - t)); r = rng.uniform(3, 9) * (1 - 0.6 * t)
        d.rectangle((x - r, y - r, x + r, y + r), fill=col + (a,))

def kinetic(canvas, txt, t, t0, size=170, col=CORAL, y=H / 2, dur=0.9, x=W / 2):
    if t < t0 or t > t0 + dur:
        return
    p = (t - t0) / dur
    s = 1.0 + 0.35 * (1 - ease_out(p * 3))
    spr = text_sprite(txt, font(ANTON, int(size * s)), col + (255,), glow_r=18)
    paste_center(canvas, spr, x, y, alpha=clamp01((1 - p) * 4))

def title_top(canvas, t, a=1.0):
    f = font(ANTON, 78)
    spr = text_sprite("WHAT IF YOU COULD DELETE ANY MEMORY?", f, AMBER + (255,), glow_r=10)
    paste_center(canvas, spr, W / 2, 110, alpha=a)

def bubble(canvas, txt, cx, cy, p, tail_x=None, size=44, tint=CREAM):
    if p <= 0:
        return
    f = font(DMS, size, "Bold")
    bb = f.getbbox(txt)
    bw, bh = bb[2] - bb[0] + 70, bb[3] - bb[1] + 50
    s = ease_out(p)
    img = Image.new("RGBA", (bw + 40, bh + 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((20, 10, 20 + bw, 10 + bh), 30, fill=tint + (255,), outline=INK + (255,), width=5)
    tx = (tail_x if tail_x is not None else bw // 2) + 20
    d.polygon([(tx - 22, 10 + bh - 4), (tx + 22, 10 + bh - 4), (tx - 10, 10 + bh + 40)], fill=tint + (255,))
    d.line([(tx - 22, 10 + bh - 1), (tx - 10, 10 + bh + 40), (tx + 22, 10 + bh - 1)], fill=INK + (255,), width=5)
    d.text((20 + 35 - bb[0], 10 + 25 - bb[1]), txt, font=f, fill=INK + (255,))
    img = img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))), Image.LANCZOS)
    paste_center(canvas, img, cx, cy, alpha=clamp01(p * 3))

def delete_btn(w=150, h=46, pressed=False):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 12, fill=(CORAL if not pressed else (200, 70, 70)) + (255,))
    f = font(DMS, 26, "Bold"); bb = f.getbbox("DELETE")
    d.text(((w - (bb[2] - bb[0])) / 2 - bb[0], (h - (bb[3] - bb[1])) / 2 - bb[1]), "DELETE", font=f, fill=CREAM + (255,))
    return img

def finger(canvas, x, y, a=1.0):
    img = Image.new("RGBA", (90, 150), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((25, 0, 65, 120), 20, fill=CREAM + (255,), outline=INK + (255,), width=4)
    d.rounded_rectangle((32, 6, 58, 30), 8, fill=(255, 220, 210, 255))
    d.rectangle((10, 95, 80, 150), fill=AMBER + (255,))
    paste_center(canvas, img, x + 0, y + 75, alpha=a)

def particles(canvas, t, n=40, seed=5, col=AMBER):
    rng = random.Random(seed); d = ImageDraw.Draw(canvas)
    for i in range(n):
        x = (rng.uniform(0, W) + t * rng.uniform(-15, 15)) % W
        y = (rng.uniform(0, H) - t * rng.uniform(10, 40)) % H
        r = rng.uniform(1.5, 4); a = int(90 + 80 * math.sin(t * 2 + i))
        d.ellipse((x - r, y - r, x + r, y + r), fill=col + (a,))

# ---------------- scenes ----------------
def s1(t):  # 0-3.8 hook: You + orbiting memories, tap delete on one
    c = BG.copy(); particles(c, t)
    for i in range(8):
        ang = i / 8 * 6.283 + t * 0.35
        x = W / 2 + math.cos(ang) * 560; y = 600 + math.sin(ang) * 250
        if i == 2:
            continue
        paste_center(c, card(DATES[i], 0.8), x, y, alpha=0.85)
    paste_center(c, you(330, blink(t), (0.6, -0.2)), W / 2, 640)
    # hero card + delete
    hx, hy = 1350, 470
    if t < 2.75:
        cs = card("SEP 14 2011", 1.3)
        paste_center(c, cs, hx, hy)
        paste_center(c, delete_btn(pressed=t > 2.6), hx, hy + 120)
        fy = lerp(hy + 400, hy + 120, ease_out((t - 1.6) / 0.9)) if t > 1.6 else H + 200
        finger(c, hx + 10, fy, 1.0)
    else:
        shatter(c, hx, hy, clamp01((t - 2.75) / 0.9), 290, 170)
        kinetic(c, "DELETED.", t, 2.75, 120, CORAL, hy, 0.9, hx)
    title_top(c, t, clamp01(t / 0.4))
    return camera(c, 1.0 + 0.04 * t / 3.8)

def classroom(c, t):
    d = ImageDraw.Draw(c)
    d.rectangle((0, 760, W, H), fill=(40, 52, 80, 255))
    d.rounded_rectangle((360, 200, 1560, 560), 16, fill=(30, 70, 60, 255), outline=(120, 90, 60, 255), width=18)
    f = font(DMS, 54, "Bold")
    d.text((440, 260), "PRESENTATION DAY", font=f, fill=(220, 230, 220, 200))
    d.text((440, 340), "2 + 2 = 5 ?", font=f, fill=(220, 230, 220, 160))
    for x in (260, 1660):
        d.rounded_rectangle((x - 130, 820, x + 130, 860), 8, fill=(140, 100, 70, 255))

def s2(t):  # 3.8-8.4 class & breakup, Gone x2
    lt = t - 3.8
    c = BG.copy()
    if t < 6.6:
        classroom(c, t)
        flush = clamp01((lt - 0.4) / 0.6) * (1 - clamp01((t - 5.9) / 0.4))
        yh = you(300, blink(t, 2.2), (0, 0.3))
        paste_center(c, yh, W / 2, 740)
        if flush > 0:
            ov = Image.new("RGBA", c.size, (0, 0, 0, 0))
            ImageDraw.Draw(ov).ellipse((W / 2 - 120, 640, W / 2 + 120, 730), fill=CORAL + (int(110 * flush),))
            c.alpha_composite(ov.filter(ImageFilter.GaussianBlur(20)))
        # laughing classmates bubbles
        bubble(c, "HAHAHA", 380, 640, clamp01((lt - 0.5) / 0.3) * (t < 5.9), size=40)
        bubble(c, "LOL", 1540, 640, clamp01((lt - 0.8) / 0.3) * (t < 5.9), size=40)
        if t < 5.9:
            paste_center(c, card("CLASS 2014", 1.0, CORAL), 1500, 330, clamp01((lt - 0.2) / 0.3))
        else:
            shatter(c, 1500, 330, clamp01((t - 5.9) / 0.7), col=CORAL)
        kinetic(c, "GONE.", t, 5.9, 200, AMBER, 480, 0.8)
    else:
        c = BG_RED.copy(); particles(c, t, 25, 9, CORAL)
        paste_center(c, you(300, blink(t), (-0.7, 0)), 640, 700)
        # broken heart photo
        hx, hy = 1250, 560
        if t < 7.7:
            img = Image.new("RGBA", (360, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
            d.rounded_rectangle((0, 0, 359, 299), 18, fill=CREAM + (255,))
            d.ellipse((60, 60, 180, 180), fill=CORAL + (255,)); d.ellipse((180, 60, 300, 180), fill=CORAL + (255,))
            d.polygon([(64, 140), (296, 140), (180, 270)], fill=CORAL + (255,))
            d.line([(180, 70), (160, 140), (200, 180), (175, 260)], fill=CREAM + (255,), width=12)
            paste_center(c, img.rotate(-6, expand=True, resample=Image.BICUBIC), hx, hy, clamp01((t - 6.6) / 0.25))
            f = font(DMS, 34, "Bold")
            paste_center(c, text_sprite("MAR 3 2019", f, CREAM + (255,)), hx, hy + 200, clamp01((t - 6.6) / 0.25))
        else:
            shatter(c, hx, hy, clamp01((t - 7.7) / 0.7), 360, 300, CORAL, 3)
        kinetic(c, "GONE.", t, 7.7, 200, AMBER, 300, 0.75)
    return c

def s3(t):  # 8.4-13.2 memory menu with counter
    lt = t - 8.4
    c = BG.copy(); particles(c, t, 30, 11, TEAL)
    d = ImageDraw.Draw(c)
    d.rounded_rectangle((180, 120, W - 180, H - 170), 40, fill=(12, 20, 36, 235), outline=TEAL + (255,), width=6)
    f = font(ANTON, 96)
    n = int(lerp(0, 4382117, ease_out(lt / 1.6)))
    spr = text_sprite(f"{n:,}", f, AMBER + (255,), glow_r=14)
    paste_center(c, spr, W / 2 - 150, 230)
    paste_center(c, text_sprite("MEMORIES", font(ANTON, 60), CREAM + (255,)), W / 2 + 300, 240)
    cols, rows = 5, 3
    for r in range(rows):
        for k in range(cols):
            i = r * cols + k
            x = 420 + k * 270; y = 430 + r * 175
            a = clamp01((lt - 0.6 - i * 0.08) / 0.3)
            paste_center(c, card(DATES[i % len(DATES)], 0.85), x, y - 15, a)
            if lt > 2.0:
                paste_center(c, delete_btn(110, 34), x, y + 62, clamp01((lt - 2.0 - i * 0.04) / 0.2))
    paste_center(c, you(200, blink(t), (0, -0.6)), 1690, 870)
    return camera(c, 1.0 + 0.08 * ease(lt / 4.8), W / 2, H / 2 - 40)

def s4(t):  # 13.2-17.4 deleting one pulls another
    lt = t - 13.2
    c = BG.copy(); particles(c, t, 25, 13)
    pts = [(560, 420, "JUL 4 2015", "BEST FRIEND"), (1000, 360, "APR 9 2018", "FIRST BIKE"),
           (1400, 470, "DEC 25 2009", "GRANDMA"), (900, 640, "JUN 8 2000", "HER VOICE")]
    d = ImageDraw.Draw(c)
    gone = [13.9, 15.3, 15.9, 16.5]
    for i in range(len(pts) - 1):
        x0, y0 = pts[i][:2]; x1, y1 = pts[i + 1][:2]
        a = 1 - clamp01((t - gone[i + 1]) / 0.4)
        d.line([(x0, y0), (x1, y1)], fill=AMBER + (int(160 * a),), width=6)
    for i, (x, y, dt, lab) in enumerate(pts):
        if t < gone[i]:
            cs = card(dt, 1.0)
            paste_center(c, cs, x, y)
            paste_center(c, text_sprite(lab, font(DMS, 30, "Bold"), CREAM + (255,)), x, y + 95)
        else:
            shatter(c, x, y, clamp01((t - gone[i]) / 0.8), col=AMBER if i == 0 else CORAL, seed=i + 20)
    if lt < 0.9:
        finger(c, 570, lerp(700, 470, ease_out(lt / 0.6)))
    eo = 1.0 if t < 15.3 else 1.25
    paste_center(c, you(300, blink(t, 2.5) * eo if eo <= 1 else 1.0, (0.3 if t < 15 else -0.5, -0.3)), 1500, 860)
    if t > 15.3:
        bubble(c, "...wait. Who is that?", 1560, 600, clamp01((t - 15.5) / 0.3), size=40)
    return c

def s5(t):  # 17.4-23.3 knock at door, stranger
    lt = t - 17.4
    c = gradient_bg((20, 24, 44), (8, 12, 22)).copy() if False else BG.copy()
    d = ImageDraw.Draw(c)
    d.rectangle((0, 820, W, H), fill=(36, 44, 70, 255))
    # door frame
    dx, dy, dw, dh = 1100, 220, 380, 600
    d.rectangle((dx - 20, dy - 20, dx + dw + 20, dy + dh), fill=(90, 62, 40, 255))
    open_p = ease(clamp01((lt - 2.6) / 0.8))
    d.rectangle((dx, dy, dx + dw, dy + dh), fill=(250, 220, 160, 255) if open_p > 0 else (60, 40, 26, 255))
    if open_p > 0:
        # stranger silhouette in light
        sx = dx + dw / 2; a = int(255 * open_p)
        d.ellipse((sx - 80, dy + 110, sx + 80, dy + 270), fill=(30, 30, 44, a))
        d.rounded_rectangle((sx - 130, dy + 260, sx + 130, dy + dh + 40), 70, fill=(30, 30, 44, a))
    dwid = int(dw * (1 - open_p))
    if dwid > 4:
        d.rectangle((dx, dy, dx + dwid, dy + dh), fill=(120, 80, 50, 255), outline=(70, 45, 28, 255), width=6)
        d.ellipse((dx + dwid - 50, dy + 300, dx + dwid - 26, dy + 324), fill=AMBER + (255,))
    # knocks
    for k, kt in enumerate((0.9, 1.25, 1.6)):
        if kt < lt < kt + 0.35:
            spr = text_sprite("KNOCK", font(ANTON, 70), CREAM + (255,), glow_r=8)
            paste_center(c, spr, dx + dw / 2 + (k - 1) * 150, dy + 120 + k * 40, 1 - (lt - kt) / 0.35)
    shake = 1.2 if any(kt < lt < kt + 0.15 for kt in (0.9, 1.25, 1.6)) else 0
    paste_center(c, you(320, blink(t) if lt < 3.4 else 1.0, (0.8, 0) if lt < 3.4 else (0.9, -0.2)), 620, 760)
    if t > 20.8:
        bubble(c, "You promised you'd never forget me.", 1290, 150, clamp01((t - 20.8) / 0.3), size=40, tail_x=430)
    z = 1.0 + 0.12 * ease(clamp01((lt - 3.3) / 2.5))
    return camera(c, z, 1000, 520, shake, t)

def s6(t):  # 23.3-30 title card + dialog
    lt = t - 23.3
    c = BG.copy(); particles(c, t, 50, 17)
    d = ImageDraw.Draw(c)
    pa = clamp01(lt / 0.35)
    bx0, by0, bx1, by1 = 560, 300, 1360, 700
    pnl = Image.new("RGBA", (bx1 - bx0, by1 - by0), (0, 0, 0, 0)); pd = ImageDraw.Draw(pnl)
    pd.rounded_rectangle((0, 0, pnl.width - 1, pnl.height - 1), 34, fill=(14, 22, 40, 245), outline=AMBER + (255,), width=6)
    f = font(ANTON, 92); bb = f.getbbox("DELETE MEMORY?")
    pd.text(((pnl.width - (bb[2] - bb[0])) / 2 - bb[0], 50 - bb[1]), "DELETE MEMORY?", font=f, fill=CREAM + (255,))
    for i, (lab, col) in enumerate((("YES", CORAL), ("NO", TEAL))):
        x = 110 + i * 330
        pd.rounded_rectangle((x, 230, x + 250, 330), 22, fill=col + (255,))
        fb = font(ANTON, 64); b2 = fb.getbbox(lab)
        pd.text((x + 125 - (b2[2] - b2[0]) / 2 - b2[0], 280 - (b2[3] - b2[1]) / 2 - b2[1]), lab, font=fb, fill=INK + (255,))
    paste_center(c, pnl, W / 2, 470, pa)
    # finger hovering between yes / no
    fx = W / 2 + math.sin(lt * 2.2) * 170
    finger(c, fx, 640 + 10 * math.sin(lt * 5), clamp01((lt - 0.6) / 0.3))
    paste_center(c, you(220, blink(t, 2.7), (math.sin(lt * 2.2) * 0.8, -0.4)), 300, 820, pa)
    if lt > 3.9:
        a = clamp01((lt - 3.9) / 0.4)
        paste_center(c, text_sprite("THE OTHER TIMELINE", font(ANTON, 64), TEAL + (255,), glow_r=10), W / 2, 850, a)
        paste_center(c, text_sprite("NEW EPISODE  ·  COMING SOON", font(DMS, 36, "Bold"), CREAM + (255,)), W / 2, 915, a)
    title_top(c, t, pa)
    return fade(c, clamp01((t - (DUR - 0.6)) / 0.6))

BAND = Image.new("RGBA", (W, 200), (0, 0, 0, 0))
for _y in range(200):
    ImageDraw.Draw(BAND).line([(0, _y), (W, _y)], fill=(5, 8, 16, int(200 * (_y / 200) ** 0.8)))

FUNCS = [s1, s2, s3, s4, s5, s6]

def frame(t):
    for (a, b), fn in zip(SCENES, FUNCS):
        if a <= t < b or fn is s6:
            c = fn(t)
            break
    if t < 0.25:
        c = fade(c, 1 - t / 0.25)
    if any(a - 0.1 <= t <= b + 0.4 for a, b, _ in SUBS):
        c.alpha_composite(BAND, (0, H - BAND.height))
    for a, b, txt in SUBS:
        subtitle(c, txt, a, t, b, y=H - 90, size=46)
    return c

def render_scene(i):
    a, b = SCENES[i]
    enc = Encoder(f"build/scene{i}.mp4")
    n0, n1 = int(round(a * FPS)), int(round(b * FPS))
    for n in range(n0, n1):
        enc.write(frame(n / FPS))
    enc.close()
    return i

if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for t in [1.2, 2.2, 3.2, 4.8, 6.0, 7.2, 8.0, 9.5, 12.0, 14.0, 16.0, 19.0, 21.5, 24.5, 28.0]:
            frame(t).convert("RGB").resize((640, 360)).save(f"build/still_{t:05.1f}.png")
        sys.exit()
    with Pool(4) as p:
        print(p.map(render_scene, range(len(SCENES))))
