"""Drawing kit for the finance series: characters, locations, props, text. 1920x1080.
Reuses ep2/common.py (channel identity: palette, fonts, You, glow, Encoder)."""
import os, sys, math, random
from functools import lru_cache
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "ep2"))
import common
from common import *  # noqa: W, H, FPS, colours, font, ease*, glow, text_sprite, paste_center, camera, fade, Encoder
from PIL import Image, ImageDraw, ImageFilter

GREEN = (110, 214, 140)
PURPLE = (150, 110, 220)
PINK = (255, 120, 200)
WHITE = (255, 255, 255)
GREY = (120, 130, 150)
MONT = os.path.join(HERE, "..", "..", "ep2", "fonts", "Montserrat.ttf")

# ---------------------------------------------------------------- text
@lru_cache(maxsize=4096)
def T(txt, size, col=CREAM, f="A", glow_r=0):
    fnt = font(ANTON, size) if f == "A" else font(DMS, size, "Bold")
    return text_sprite(txt, fnt, tuple(col) + (255,), glow_r=glow_r, glow_col=tuple(col))

def pop(c, spr, x, y, t, t0, t1=1e9, dur=0.3, anim="pop"):
    if t < t0 or t > t1 + 0.25:
        return
    p = ease_out((t - t0) / dur)
    a = clamp01((t - t0) / 0.15) * clamp01((t1 + 0.25 - t) / 0.25)
    if anim == "pop":
        s = 0.6 + 0.4 * p + 0.08 * math.sin(min(1, (t - t0) / 0.45) * math.pi)
        if abs(s - 1) > 0.01:
            spr = spr.resize((max(1, int(spr.width * s)), max(1, int(spr.height * s))), Image.BICUBIC)
    elif anim == "slide_l":
        x = x - (1 - p) * 400
    elif anim == "slide_r":
        x = x + (1 - p) * 400
    elif anim == "drop":
        y = y - (1 - p) * 300
    paste_center(c, spr, x, y, a)

def money(v, dec=0):
    v = float(v)
    s = f"${abs(v):,.{dec}f}"
    return ("-" if v < 0 else "") + s

# ---------------------------------------------------------------- characters
# name: (skin, outfit, outfit_dark, hair, extra)
CAST = {
    "you":     dict(skin=CREAM, top=AMBER, dark=(214, 140, 40), hood=(226, 150, 50), hair=None, extra="hood"),
    "max":     dict(skin=(240, 205, 170), top=CORAL, dark=(200, 70, 70), hood=None, hair=(60, 40, 30), extra="spiky"),
    "grandma": dict(skin=(245, 222, 200), top=PURPLE, dark=(110, 80, 170), hood=None, hair=(215, 215, 225), extra="bun_glasses"),
    "banker":  dict(skin=(160, 110, 75), top=(40, 55, 90), dark=(25, 35, 60), hood=None, hair=(30, 25, 25), extra="tie"),
    "barista": dict(skin=(225, 180, 140), top=(60, 140, 90), dark=(40, 100, 65), hood=None, hair=(120, 70, 40), extra="cap"),
    "seller":  dict(skin=(235, 195, 160), top=(220, 220, 230), dark=(170, 170, 185), hood=None, hair=(200, 160, 60), extra="tie_red"),
    "stranger":dict(skin=(200, 160, 130), top=(90, 100, 120), dark=(60, 70, 85), hood=None, hair=(40, 40, 40), extra=None),
}

@lru_cache(maxsize=1024)
def person(who="you", size=300, emo="neutral", look=(0, 0), blink=1.0, body=True):
    """Round-headed channel-style character. emo: neutral happy smug shock sad angry worried love money."""
    cfg = CAST[who]
    S = 2
    w = size * S; h = int(size * (1.45 if body else 1.0)) * S
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    hx, hy, hr = w / 2, w * 0.40, w * 0.36
    if body:
        top, dark = cfg["top"], cfg["dark"]
        d.rounded_rectangle((w * 0.12, w * 0.70, w * 0.88, h + w * 0.3), int(w * 0.25), fill=top + (255,), outline=dark + (255,), width=4 * S)
        if cfg["extra"] in ("tie", "tie_red"):
            d.polygon([(w * 0.38, w * 0.74), (w * 0.62, w * 0.74), (w * 0.5, w * 0.86)], fill=(240, 240, 245, 255))
            tc = TEAL if cfg["extra"] == "tie" else CORAL
            d.polygon([(w * 0.47, w * 0.78), (w * 0.53, w * 0.78), (w * 0.56, w * 1.05), (w * 0.5, w * 1.12), (w * 0.44, w * 1.05)], fill=tc + (255,))
        elif cfg["extra"] == "hood" or who == "you":
            for x in (0.42, 0.58):
                d.line((w * x, w * 0.76, w * x, w * 0.98), fill=CREAM + (255,), width=5 * S)
        elif who == "barista":
            d.rounded_rectangle((w * 0.3, w * 0.8, w * 0.7, h), 20 * S, fill=(40, 100, 65, 255))
    # hood / hair back
    if cfg["hood"]:
        d.ellipse((hx - hr * 1.22, hy - hr * 1.18, hx + hr * 1.22, hy + hr * 1.22), fill=cfg["hood"] + (255,))
    if cfg["extra"] == "bun_glasses":
        d.ellipse((hx - hr * 0.45, hy - hr * 1.55, hx + hr * 0.45, hy - hr * 0.7), fill=cfg["hair"] + (255,))
    skin = cfg["skin"]
    if emo == "angry":
        skin = (min(255, skin[0] + 15), int(skin[1] * 0.7), int(skin[2] * 0.65))
    d.ellipse((hx - hr, hy - hr, hx + hr, hy + hr), fill=skin + (255,))
    if cfg["hair"] and cfg["extra"] != "bun_glasses":
        hc = cfg["hair"] + (255,)
        if cfg["extra"] == "spiky":
            pts = [(hx - hr * 0.95, hy - hr * 0.2)]
            for i in range(7):
                a = math.pi * (1.05 + i * 0.15)
                r = hr * (1.28 if i % 2 == 0 else 1.02)
                pts.append((hx + math.cos(a) * r, hy + math.sin(a) * r))
            pts.append((hx + hr * 0.95, hy - hr * 0.2))
            d.polygon(pts, fill=hc)
        elif cfg["extra"] == "cap":
            d.chord((hx - hr * 1.02, hy - hr * 1.05, hx + hr * 1.02, hy + hr * 0.6), 180, 360, fill=(60, 140, 90, 255))
            d.rounded_rectangle((hx - hr * 0.2, hy - hr * 0.35, hx + hr * 1.35, hy - hr * 0.18), 10 * S, fill=(40, 100, 65, 255))
        else:
            d.chord((hx - hr * 1.02, hy - hr * 1.05, hx + hr * 1.02, hy + hr * 0.5), 185, 355, fill=hc)
    elif cfg["extra"] == "bun_glasses":
        d.chord((hx - hr * 1.02, hy - hr * 1.05, hx + hr * 1.02, hy + hr * 0.4), 185, 355, fill=cfg["hair"] + (255,))
    # cheeks
    ch = (255, 120, 110, 150) if emo in ("angry", "love", "shock") else (255, 170, 150, 110)
    for cx in (hx - hr * 0.62, hx + hr * 0.62):
        d.ellipse((cx - hr * 0.16, hy + hr * 0.18, cx + hr * 0.16, hy + hr * 0.36), fill=ch)
    # eyes
    er = hr * 0.26
    eyes_y = hy - hr * 0.12
    for ex in (hx - hr * 0.36, hx + hr * 0.36):
        ry = er * (1.15 if emo == "shock" else 1.0) * max(0.08, blink)
        if emo == "smug":
            ry *= 0.55
        if emo == "money" and blink > 0.3:
            f = font(ANTON, int(er * 2.0)); d.text((ex - er * 0.45, eyes_y - er * 1.15), "$", font=f, fill=GREEN + (255,))
            continue
        if emo == "love" and blink > 0.3:
            r = er * 0.7
            d.ellipse((ex - r, eyes_y - r, ex, eyes_y), fill=CORAL + (255,)); d.ellipse((ex, eyes_y - r, ex + r, eyes_y), fill=CORAL + (255,))
            d.polygon([(ex - r, eyes_y - r * 0.4), (ex + r, eyes_y - r * 0.4), (ex, eyes_y + r)], fill=CORAL + (255,))
            continue
        d.ellipse((ex - er, eyes_y - ry, ex + er, eyes_y + ry), fill=WHITE + (255,), outline=INK + (255,), width=3 * S)
        if blink > 0.3:
            pr = er * (0.32 if emo == "shock" else 0.5)
            px = ex + look[0] * er * 0.4; py = eyes_y + look[1] * ry * 0.4
            d.ellipse((px - pr, py - pr * min(1, ry / er + 0.2), px + pr, py + pr * min(1, ry / er + 0.2)), fill=INK + (255,))
            d.ellipse((px + pr * 0.1, py - pr * 0.6, px + pr * 0.55, py - pr * 0.15), fill=WHITE + (255,))
        if emo == "angry":
            sgn = -1 if ex < hx else 1
            d.line((ex - er * 1.1, eyes_y - er * (1.5 if sgn < 0 else 0.9), ex + er * 1.1, eyes_y - er * (0.9 if sgn < 0 else 1.5)), fill=INK + (255,), width=5 * S)
        if emo in ("sad", "worried"):
            sgn = -1 if ex < hx else 1
            d.line((ex - er, eyes_y - er * (1.0 if sgn < 0 else 1.6), ex + er, eyes_y - er * (1.6 if sgn < 0 else 1.0)), fill=INK + (255,), width=4 * S)
    if cfg["extra"] == "bun_glasses":
        for ex in (hx - hr * 0.36, hx + hr * 0.36):
            d.ellipse((ex - er * 1.35, eyes_y - er * 1.3, ex + er * 1.35, eyes_y + er * 1.3), outline=(60, 50, 70, 255), width=4 * S)
        d.line((hx - hr * 0.36 + er * 1.35, eyes_y, hx + hr * 0.36 - er * 1.35, eyes_y), fill=(60, 50, 70, 255), width=4 * S)
    # mouth
    my = hy + hr * 0.42; mw = hr * 0.22
    if emo in ("happy", "love", "money"):
        d.chord((hx - mw * 1.4, my - mw * 0.9, hx + mw * 1.4, my + mw * 1.3), 0, 180, fill=(120, 40, 50, 255))
    elif emo == "shock":
        d.ellipse((hx - mw * 0.7, my - mw * 0.5, hx + mw * 0.7, my + mw * 1.1), fill=(120, 40, 50, 255))
    elif emo == "smug":
        d.arc((hx - mw * 0.4, my - mw * 1.2, hx + mw * 1.8, my + mw * 0.6), 20, 150, fill=INK + (255,), width=4 * S)
    elif emo in ("sad", "worried"):
        d.arc((hx - mw, my, hx + mw, my + mw * 1.4), 200, 340, fill=INK + (255,), width=4 * S)
    elif emo == "angry":
        d.line((hx - mw, my + mw * 0.3, hx + mw, my + mw * 0.3), fill=INK + (255,), width=5 * S)
    else:
        d.arc((hx - mw * 0.8, my - mw * 0.6, hx + mw * 0.8, my + mw * 0.6), 20, 160, fill=INK + (255,), width=4 * S)
    if emo in ("worried", "shock"):
        sx, sy = hx + hr * 0.85, hy - hr * 0.55
        d.polygon([(sx, sy - hr * 0.22), (sx - hr * 0.1, sy), (sx + hr * 0.1, sy)], fill=(140, 200, 255, 255))
        d.ellipse((sx - hr * 0.1, sy - hr * 0.05, sx + hr * 0.1, sy + hr * 0.15), fill=(140, 200, 255, 255))
    if emo == "angry":
        vx, vy = hx + hr * 0.55, hy - hr * 0.75
        for a in range(4):
            ang = a * math.pi / 2 + 0.6
            d.line((vx, vy, vx + math.cos(ang) * hr * 0.18, vy + math.sin(ang) * hr * 0.18), fill=CORAL + (255,), width=5 * S)
    return img.resize((size, int(size * (1.45 if body else 1.0))), Image.LANCZOS)

def blink_at(t, seed=0.0, per=3.4):
    return 0.1 if ((t + seed) % per) < 0.12 else 1.0

def draw_actor(c, who, x, y, size, t, emo="neutral", look=(0, 0), bob=True, seed=0.0, alpha=1.0, flip=False, talk=False):
    b = blink_at(t, seed)
    spr = person(who, size, emo, (round(look[0], 1), round(look[1], 1)), b)
    if flip:
        spr = spr.transpose(Image.FLIP_LEFT_RIGHT)
    dy = math.sin(t * 2.2 + seed * 3) * size * 0.012 if bob else 0
    if talk:
        dy += abs(math.sin(t * 11 + seed)) * size * 0.015
    paste_center(c, spr, x, y - spr.height / 2 + dy, alpha)

# ---------------------------------------------------------------- props
@lru_cache(maxsize=256)
def card(label="VISA", col=TEAL, scale=1.0, number="4417"):
    w, h = int(340 * scale), int(214 * scale)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w - 1, h - 1), int(22 * scale), fill=col + (255,))
    d.rounded_rectangle((int(28 * scale), int(70 * scale), int(88 * scale), int(116 * scale)), int(8 * scale), fill=(240, 200, 90, 255))
    d.text((int(28 * scale), int(140 * scale)), f"**** **** **** {number}", font=font(DMS, int(24 * scale), "Bold"), fill=WHITE + (230,))
    d.text((int(28 * scale), int(20 * scale)), label, font=font(ANTON, int(34 * scale)), fill=WHITE + (255,))
    return img

@lru_cache(maxsize=256)
def phone(text="$4.17", sub="BALANCE", col=GREEN, scale=1.0):
    w, h = int(240 * scale), int(440 * scale)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w - 1, h - 1), int(36 * scale), fill=(20, 22, 30, 255))
    d.rounded_rectangle((int(12 * scale), int(14 * scale), w - int(12 * scale), h - int(14 * scale)), int(28 * scale), fill=(245, 246, 250, 255))
    f = font(DMS, int(22 * scale), "Bold"); d.text((w / 2 - f.getlength(sub) / 2, int(120 * scale)), sub, font=f, fill=(110, 115, 130, 255))
    fs = int(64 * scale)
    f2 = font(ANTON, fs)
    while f2.getlength(text) > w - 40 * scale and fs > 20:
        fs -= 4; f2 = font(ANTON, fs)
    d.text((w / 2 - f2.getlength(text) / 2, int(160 * scale)), text, font=f2, fill=col + (255,))
    d.rounded_rectangle((int(40 * scale), int(300 * scale), w - int(40 * scale), int(350 * scale)), int(20 * scale), fill=col + (255,))
    return img

@lru_cache(maxsize=256)
def bill(amount="100", scale=1.0, col=(120, 200, 140)):
    w, h = int(300 * scale), int(140 * scale)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w - 1, h - 1), int(10 * scale), fill=col + (255,), outline=(40, 90, 50, 255), width=max(2, int(4 * scale)))
    d.ellipse((w / 2 - h * 0.3, h * 0.2, w / 2 + h * 0.3, h * 0.8), outline=(40, 90, 50, 255), width=max(2, int(3 * scale)))
    f = font(ANTON, int(46 * scale)); d.text((int(14 * scale), int(6 * scale)), "$" + amount, font=f, fill=(30, 70, 40, 255))
    return img

@lru_cache(maxsize=256)
def tag(text, col=AMBER, scale=1.0, sub=None):
    f = font(ANTON, int(56 * scale)); tw = f.getlength(text)
    w, h = int(tw + 90 * scale), int((120 if sub else 96) * scale)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.polygon([(0, h / 2), (int(36 * scale), 0), (w - 1, 0), (w - 1, h - 1), (int(36 * scale), h - 1)], fill=col + (255,))
    d.ellipse((int(18 * scale), h / 2 - 8 * scale, int(34 * scale), h / 2 + 8 * scale), fill=INK + (255,))
    d.text((int(56 * scale), int(10 * scale)), text, font=f, fill=INK + (255,))
    if sub:
        f2 = font(DMS, int(22 * scale), "Bold"); d.text((int(58 * scale), int(80 * scale)), sub, font=f2, fill=INK + (255,))
    return img

@lru_cache(maxsize=64)
def coin(scale=1.0, sym="$", col=AMBER):
    r = int(60 * scale)
    img = Image.new("RGBA", (2 * r, 2 * r), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.ellipse((0, 0, 2 * r - 1, 2 * r - 1), fill=col + (255,), outline=(200, 130, 30, 255), width=max(2, int(6 * scale)))
    f = font(ANTON, int(70 * scale)); d.text((r - f.getlength(sym) / 2, r * 0.28), sym, font=f, fill=(150, 90, 20, 255))
    return img

@lru_cache(maxsize=64)
def receipt(lines=(("Coffee", "$5"),), total=None, scale=1.0):
    w = int(320 * scale); lh = int(44 * scale); h = int((len(lines) + (2 if total else 1)) * lh + 70 * scale)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    pts = [(0, 0), (w, 0), (w, h - 12)] + [(w - i * 24 * scale, h - (0 if i % 2 else 12)) for i in range(int(w / (24 * scale)) + 1)] + [(0, h - 12)]
    d.polygon(pts, fill=(250, 248, 240, 255))
    f = font(DMS, int(26 * scale), "Bold")
    y = int(30 * scale)
    for a, b in lines:
        d.text((int(24 * scale), y), a, font=f, fill=(60, 60, 70, 255)); d.text((w - int(24 * scale) - f.getlength(b), y), b, font=f, fill=(60, 60, 70, 255)); y += lh
    if total:
        d.line((int(20 * scale), y + 4, w - int(20 * scale), y + 4), fill=(60, 60, 70, 255), width=2)
        f2 = font(ANTON, int(34 * scale)); d.text((int(24 * scale), y + 10), "TOTAL", font=f2, fill=CORAL + (255,)); d.text((w - int(24 * scale) - f2.getlength(total), y + 10), total, font=f2, fill=CORAL + (255,))
    return img

@lru_cache(maxsize=32)
def calendar(top="2010", big="JAN", scale=1.0, col=CORAL):
    w, h = int(260 * scale), int(280 * scale)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w - 1, h - 1), int(22 * scale), fill=(250, 246, 236, 255))
    d.rounded_rectangle((0, 0, w - 1, int(80 * scale)), int(22 * scale), fill=col + (255,)); d.rectangle((0, int(50 * scale), w - 1, int(80 * scale)), fill=col + (255,))
    f = font(ANTON, int(52 * scale)); d.text((w / 2 - f.getlength(top) / 2, int(8 * scale)), top, font=f, fill=WHITE + (255,))
    f2 = font(ANTON, int(110 * scale)); d.text((w / 2 - f2.getlength(big) / 2, int(100 * scale)), big, font=f2, fill=INK + (255,))
    return img

@lru_cache(maxsize=32)
def jar(fill_p=0.5, w=260, h=330, col=AMBER):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle((16, 36, w - 16, h - 4), 36, fill=(40, 60, 90, 200), outline=CREAM + (230,), width=6)
    d.rounded_rectangle((44, 8, w - 44, 44), 10, fill=(120, 130, 150, 255))
    fh = (h - 56) * fill_p
    if fh > 6:
        d.rounded_rectangle((26, h - 14 - fh, w - 26, h - 14), 28, fill=col + (255,))
        for i in range(int(fh / 24)):
            yy = h - 28 - i * 24; d.line((36, yy, w - 36, yy), fill=(214, 140, 40, 255), width=3)
    return img

@lru_cache(maxsize=32)
def icon(kind, scale=1.0):
    """Simple object icons: car, house, iphone, btc, gold, mattress, piggy, tv, shield, chart, warning, sofa, burger."""
    s = scale; w, h = int(320 * s), int(240 * s)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    if kind == "car":
        d.rounded_rectangle((20 * s, 100 * s, 300 * s, 180 * s), int(30 * s), fill=CORAL + (255,))
        d.polygon([(80 * s, 100 * s), (110 * s, 50 * s), (220 * s, 50 * s), (250 * s, 100 * s)], fill=CORAL + (255,))
        d.polygon([(100 * s, 98 * s), (120 * s, 62 * s), (160 * s, 62 * s), (160 * s, 98 * s)], fill=(180, 220, 240, 255))
        d.polygon([(170 * s, 98 * s), (170 * s, 62 * s), (212 * s, 62 * s), (236 * s, 98 * s)], fill=(180, 220, 240, 255))
        for x in (80, 240):
            d.ellipse(((x - 30) * s, 150 * s, (x + 30) * s, 210 * s), fill=(30, 30, 40, 255)); d.ellipse(((x - 12) * s, 168 * s, (x + 12) * s, 192 * s), fill=(180, 180, 190, 255))
    elif kind == "house":
        d.polygon([(40 * s, 110 * s), (160 * s, 20 * s), (280 * s, 110 * s)], fill=CORAL + (255,))
        d.rectangle((60 * s, 110 * s, 260 * s, 230 * s), fill=CREAM + (255,))
        d.rectangle((140 * s, 160 * s, 180 * s, 230 * s), fill=(120, 80, 50, 255))
        d.rectangle((80 * s, 130 * s, 120 * s, 170 * s), fill=(180, 220, 240, 255)); d.rectangle((200 * s, 130 * s, 240 * s, 170 * s), fill=(180, 220, 240, 255))
    elif kind == "iphone":
        d.rounded_rectangle((110 * s, 10 * s, 210 * s, 230 * s), int(20 * s), fill=(200, 200, 210, 255))
        d.rounded_rectangle((118 * s, 22 * s, 202 * s, 218 * s), int(14 * s), fill=(30, 40, 70, 255))
        d.ellipse((150 * s, 196 * s, 170 * s, 214 * s), fill=(160, 160, 170, 255))
    elif kind == "btc":
        d.ellipse((60 * s, 20 * s, 260 * s, 220 * s), fill=(247, 147, 26, 255))
        f = font(ANTON, int(140 * s)); d.text((160 * s - f.getlength("B") / 2, 30 * s), "B", font=f, fill=WHITE + (255,))
        d.line((140 * s, 30 * s, 140 * s, 210 * s), fill=WHITE + (255,), width=int(8 * s)); d.line((175 * s, 30 * s, 175 * s, 210 * s), fill=WHITE + (255,), width=int(8 * s))
    elif kind == "gold":
        for i, (x, y) in enumerate([(60, 140), (180, 140), (120, 80)]):
            d.polygon([((x + 10) * s, y * s), ((x + 110) * s, y * s), ((x + 125) * s, (y + 60) * s), ((x - 5) * s, (y + 60) * s)], fill=(240, 190, 60, 255), outline=(190, 130, 20, 255))
    elif kind == "mattress":
        d.rounded_rectangle((10 * s, 120 * s, 310 * s, 210 * s), int(30 * s), fill=(200, 205, 225, 255), outline=INK + (255,), width=int(4 * s))
        for x in range(50, 300, 60):
            d.line((x * s, 130 * s, x * s, 200 * s), fill=(160, 165, 190, 255), width=int(3 * s))
    elif kind == "piggy":
        d.ellipse((50 * s, 60 * s, 270 * s, 210 * s), fill=PINK + (255,)); d.ellipse((240 * s, 110 * s, 300 * s, 160 * s), fill=(255, 150, 210, 255))
        d.rounded_rectangle((130 * s, 60 * s, 190 * s, 72 * s), 4, fill=INK + (255,)); d.ellipse((200 * s, 100 * s, 214 * s, 114 * s), fill=INK + (255,))
        for x in (90, 200):
            d.rectangle((x * s, 190 * s, (x + 24) * s, 230 * s), fill=PINK + (255,))
    elif kind == "tv":
        d.rounded_rectangle((20 * s, 20 * s, 300 * s, 190 * s), int(14 * s), fill=(30, 32, 44, 255)); d.rectangle((36 * s, 36 * s, 284 * s, 174 * s), fill=(90, 160, 220, 255))
        d.rectangle((140 * s, 190 * s, 180 * s, 220 * s), fill=(30, 32, 44, 255)); d.rectangle((100 * s, 220 * s, 220 * s, 232 * s), fill=(30, 32, 44, 255))
    elif kind == "shield":
        d.polygon([(160 * s, 10 * s), (270 * s, 50 * s), (250 * s, 160 * s), (160 * s, 230 * s), (70 * s, 160 * s), (50 * s, 50 * s)], fill=TEAL + (255,))
        d.line([(110 * s, 120 * s), (150 * s, 160 * s), (220 * s, 80 * s)], fill=WHITE + (255,), width=int(16 * s))
    elif kind == "warning":
        d.polygon([(160 * s, 10 * s), (300 * s, 230 * s), (20 * s, 230 * s)], fill=CORAL + (255,))
        f = font(ANTON, int(150 * s)); d.text((160 * s - f.getlength("!") / 2, 50 * s), "!", font=f, fill=WHITE + (255,))
    elif kind == "chart":
        d.rounded_rectangle((20 * s, 20 * s, 300 * s, 220 * s), int(20 * s), fill=(14, 22, 40, 255), outline=TEAL + (255,), width=int(5 * s))
        d.line([(50 * s, 180 * s), (110 * s, 140 * s), (150 * s, 160 * s), (200 * s, 100 * s), (230 * s, 110 * s), (275 * s, 50 * s)], fill=TEAL + (255,), width=int(10 * s))
    elif kind == "sofa":
        d.rounded_rectangle((20 * s, 90 * s, 300 * s, 200 * s), int(30 * s), fill=TEAL + (255,)); d.rounded_rectangle((50 * s, 60 * s, 270 * s, 130 * s), int(24 * s), fill=(50, 170, 165, 255))
    elif kind == "burger":
        d.chord((60 * s, 40 * s, 260 * s, 180 * s), 180, 360, fill=(230, 160, 70, 255)); d.rectangle((60 * s, 110 * s, 260 * s, 130 * s), fill=(110, 60, 40, 255))
        d.rectangle((55 * s, 130 * s, 265 * s, 140 * s), fill=GREEN + (255,)); d.rounded_rectangle((60 * s, 140 * s, 260 * s, 180 * s), int(16 * s), fill=(230, 160, 70, 255))
    elif kind == "box":
        d.polygon([(60 * s, 80 * s), (160 * s, 40 * s), (260 * s, 80 * s), (160 * s, 120 * s)], fill=(210, 160, 100, 255))
        d.polygon([(60 * s, 80 * s), (160 * s, 120 * s), (160 * s, 230 * s), (60 * s, 190 * s)], fill=(180, 130, 80, 255))
        d.polygon([(260 * s, 80 * s), (160 * s, 120 * s), (160 * s, 230 * s), (260 * s, 190 * s)], fill=(160, 110, 70, 255))
    return img

def bubble(c, txt, cx, cy, p, tail="down", size=40, tint=CREAM, maxw=620):
    if p <= 0:
        return
    f = font(DMS, size, "Bold")
    words = txt.split(); lines = [""]
    for w_ in words:
        tst = (lines[-1] + " " + w_).strip()
        if f.getlength(tst) > maxw and lines[-1]:
            lines.append(w_)
        else:
            lines[-1] = tst
    lh = int(size * 1.25)
    bw = int(max(f.getlength(l) for l in lines) + 60); bh = lh * len(lines) + 36
    img = Image.new("RGBA", (bw + 20, bh + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle((10, 6, 10 + bw, 6 + bh), 28, fill=tint + (255,), outline=INK + (255,), width=4)
    tx = 10 + bw * (0.25 if tail == "left" else 0.75 if tail == "right" else 0.5)
    d.polygon([(tx - 18, 6 + bh - 3), (tx + 18, 6 + bh - 3), (tx - 6, 6 + bh + 36)], fill=tint + (255,))
    d.line([(tx - 18, 6 + bh - 1), (tx - 6, 6 + bh + 36), (tx + 18, 6 + bh - 1)], fill=INK + (255,), width=4)
    for i, l in enumerate(lines):
        d.text((10 + bw / 2 - f.getlength(l) / 2, 6 + 18 + i * lh), l, font=f, fill=INK + (255,))
    s = 0.5 + 0.5 * ease_out(p)
    img = img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))), Image.BICUBIC)
    paste_center(c, img, cx, cy - img.height / 2, clamp01(p * 3))

# ---------------------------------------------------------------- locations
def _base(top, bottom):
    return gradient_bg(top, bottom, 0.45)

@lru_cache(maxsize=32)
def location(name):
    if name == "void":
        return gradient_bg(NAVY2, NAVY)
    if name == "void_red":
        return gradient_bg((70, 30, 45), NAVY)
    if name == "void_teal":
        return gradient_bg((18, 60, 70), NAVY)
    c = _base((44, 58, 92), (24, 32, 54))
    d = ImageDraw.Draw(c)
    floor = 800
    if name == "kitchen":
        c = _base((70, 80, 110), (40, 46, 70)); d = ImageDraw.Draw(c)
        d.rectangle((0, floor, W, H), fill=(90, 70, 60, 255))
        for x in range(0, W, 120):
            d.rectangle((x, floor, x + 118, H), fill=(100 + (x // 120 % 2) * 12, 78, 64, 255))
        d.rectangle((0, 560, W, floor), fill=(220, 220, 228, 255)); d.rectangle((0, 540, W, 570), fill=(160, 170, 185, 255))
        for x in range(60, W, 300):
            d.rounded_rectangle((x, 140, x + 240, 380), 12, fill=(235, 220, 200, 255), outline=(180, 160, 140, 255), width=4)
            d.ellipse((x + 110, 250, x + 130, 270), fill=(160, 140, 120, 255))
        d.rounded_rectangle((1500, 300, 1760, 800), 16, fill=(210, 215, 225, 255)); d.line((1520, 520, 1740, 520), fill=(150, 155, 170, 255), width=4)
        d.rounded_rectangle((800, 120, 1100, 420), 10, fill=(130, 190, 230, 255), outline=(240, 240, 245, 255), width=14)
    elif name == "cafe":
        c = _base((90, 60, 50), (40, 28, 30)); d = ImageDraw.Draw(c)
        d.rectangle((0, floor, W, H), fill=(70, 45, 35, 255))
        d.rectangle((0, 600, W, floor), fill=(130, 85, 55, 255)); d.rectangle((0, 585, W, 610), fill=(160, 110, 70, 255))
        d.rounded_rectangle((120, 110, 760, 430), 18, fill=(30, 40, 50, 255), outline=(150, 100, 60, 255), width=12)
        f = font(DMS, 40, "Bold"); d.text((170, 140), "MENU", font=f, fill=CREAM + (220,))
        for i, (n, p) in enumerate([("Latte", "$5"), ("Cappuccino", "$5"), ("Cold brew", "$6")]):
            d.text((170, 210 + i * 62), n, font=f, fill=CREAM + (200,)); d.text((640, 210 + i * 62), p, font=f, fill=AMBER + (255,))
        for x in range(1000, 1850, 170):
            d.line((x, 0, x, 120), fill=(60, 50, 40, 255), width=3); d.ellipse((x - 40, 110, x + 40, 170), fill=(255, 210, 120, 255))
        d.rounded_rectangle((1250, 430, 1430, 600), 14, fill=(60, 60, 70, 255))
    elif name == "store":
        c = _base((210, 220, 235), (150, 160, 180)); d = ImageDraw.Draw(c)
        d.rectangle((0, floor, W, H), fill=(190, 195, 205, 255))
        for row in range(3):
            y = 180 + row * 190
            d.rectangle((0, y + 120, W, y + 136), fill=(120, 130, 150, 255))
            for i in range(14):
                x = 40 + i * 135; col = [CORAL, TEAL, AMBER, PURPLE, GREEN][(i + row) % 5]
                d.rounded_rectangle((x, y + 20, x + 100, y + 120), 10, fill=col + (255,))
        d.rounded_rectangle((1300, 620, 1800, 820), 16, fill=(90, 95, 110, 255))
    elif name == "bank":
        c = _base((60, 70, 90), (30, 36, 52)); d = ImageDraw.Draw(c)
        d.rectangle((0, floor, W, H), fill=(180, 170, 150, 255))
        for x in range(120, W, 340):
            d.rectangle((x, 80, x + 70, floor), fill=(220, 210, 190, 255)); d.rectangle((x - 15, 70, x + 85, 100), fill=(235, 225, 205, 255))
        d.rectangle((0, 40, W, 80), fill=(235, 225, 205, 255))
        f = font(ANTON, 70); d.text((W / 2 - f.getlength("FIRST TIMELINE BANK") / 2, -6), "FIRST TIMELINE BANK", font=f, fill=(120, 100, 60, 255))
        d.rectangle((300, 620, 1620, 820), fill=(110, 80, 55, 255)); d.rectangle((300, 600, 1620, 630), fill=(140, 105, 70, 255))
    elif name == "office":
        c = _base((120, 140, 170), (70, 80, 100)); d = ImageDraw.Draw(c)
        d.rectangle((0, floor, W, H), fill=(70, 75, 90, 255))
        for x in range(100, W, 420):
            d.rectangle((x, 120, x + 320, 420), fill=(170, 210, 240, 255)); d.line((x + 160, 120, x + 160, 420), fill=(240, 240, 245, 255), width=8)
        d.rectangle((200, 640, 1720, 680), fill=(200, 170, 130, 255))
        d.rounded_rectangle((760, 440, 1160, 640), 10, fill=(30, 35, 45, 255)); d.rectangle((780, 458, 1140, 622), fill=(60, 120, 200, 255))
    elif name == "street":
        c = _base((40, 50, 90), (25, 30, 55)); d = ImageDraw.Draw(c)
        rng = random.Random(5)
        for i in range(12):
            x = i * 170 - 40; hgt = rng.randint(300, 650)
            d.rectangle((x, floor - hgt, x + 160, floor), fill=(55 + rng.randint(0, 25), 60 + rng.randint(0, 25), 95, 255))
            for yy in range(floor - hgt + 30, floor - 40, 70):
                for xx in range(x + 20, x + 150, 50):
                    if rng.random() < 0.6:
                        d.rectangle((xx, yy, xx + 26, yy + 36), fill=(255, 210, 120, 220))
        d.rectangle((0, floor, W, H), fill=(50, 52, 62, 255)); d.rectangle((0, floor, W, floor + 30), fill=(120, 120, 130, 255))
    elif name == "bedroom":
        c = _base((40, 40, 80), (22, 24, 48)); d = ImageDraw.Draw(c)
        d.rectangle((0, floor, W, H), fill=(60, 50, 70, 255))
        d.rounded_rectangle((1250, 140, 1650, 460), 10, fill=(20, 30, 60, 255), outline=(200, 200, 220, 255), width=12)
        d.ellipse((1500, 190, 1580, 270), fill=(250, 240, 200, 255)); d.ellipse((1525, 180, 1600, 255), fill=(20, 30, 60, 255))
        d.rounded_rectangle((150, 560, 1000, 820), 30, fill=(80, 100, 160, 255)); d.rounded_rectangle((170, 520, 380, 600), 26, fill=(230, 230, 240, 255))
    elif name == "dealer":
        c = _base((220, 225, 235), (160, 170, 190)); d = ImageDraw.Draw(c)
        d.rectangle((0, floor, W, H), fill=(230, 232, 238, 255))
        for x in range(0, W, 240):
            d.rectangle((x, 60, x + 220, 520), fill=(180, 210, 235, 255))
        f = font(ANTON, 80); d.text((60, 560), "NEW CARS", font=f, fill=CORAL + (255,))
    elif name == "living":
        c = _base((90, 80, 110), (50, 44, 66)); d = ImageDraw.Draw(c)
        d.rectangle((0, floor, W, H), fill=(110, 85, 70, 255))
        d.rounded_rectangle((200, 120, 600, 420), 10, fill=(150, 200, 230, 255), outline=(240, 235, 225, 255), width=14)
        d.rounded_rectangle((1200, 520, 1800, 800), 40, fill=(70, 150, 150, 255)); d.rounded_rectangle((1240, 460, 1760, 600), 34, fill=(60, 130, 130, 255))
        d.rectangle((1350, 200, 1650, 380), fill=(30, 32, 44, 255)); d.rectangle((1366, 216, 1634, 364), fill=(80, 140, 200, 255))
    c = c.filter(ImageFilter.GaussianBlur(1.2))
    # vignette & tint so characters pop
    ov = Image.new("RGBA", (W, H), (10, 14, 30, 22))
    return Image.alpha_composite(c, ov)

def particles(c, t, n=30, seed=5, col=AMBER, alpha=80):
    rng = random.Random(seed); d = ImageDraw.Draw(c)
    for i in range(n):
        x = (rng.uniform(0, W) + t * rng.uniform(-12, 12)) % W
        y = (rng.uniform(0, H) - t * rng.uniform(8, 30)) % H
        r = rng.uniform(1.5, 3.5); d.ellipse((x - r, y - r, x + r, y + r), fill=col + (int(alpha + 50 * math.sin(t * 2 + i)),))

def glow_line(c, x0, y0, x1, y1, t, col=PINK, width=10, p=1.0):
    """Magic 'power' line from one point to another (thumbnail style)."""
    ov = Image.new("RGBA", c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    pts = []
    for i in range(41):
        u = i / 40 * p
        x = lerp(x0, x1, u); y = lerp(y0, y1, u) - math.sin(u * math.pi) * 120 + math.sin(u * 20 + t * 8) * 6
        pts.append((x, y))
    if len(pts) > 1:
        d.line(pts, fill=col + (120,), width=width * 3, joint="curve")
        g = ov.filter(ImageFilter.GaussianBlur(10))
        c.alpha_composite(g)
        ImageDraw.Draw(c).line(pts, fill=col + (255,), width=width, joint="curve")
        ImageDraw.Draw(c).line(pts, fill=WHITE + (255,), width=max(2, width // 3), joint="curve")
