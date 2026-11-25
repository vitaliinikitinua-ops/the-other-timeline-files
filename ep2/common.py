import math, random, subprocess, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1920, 1080, 30
NAVY = (15, 26, 46)
NAVY2 = (28, 44, 74)
AMBER = (255, 181, 71)
CORAL = (255, 107, 107)
TEAL = (62, 199, 194)
CREAM = (244, 234, 213)
INK = (10, 14, 24)

ANTON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "Anton-Regular.ttf")
DMS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "DMSans.ttf")

_fcache = {}
def font(path, size, var=None):
    k = (path, size, var)
    if k not in _fcache:
        f = ImageFont.truetype(path, size)
        if var:
            try:
                f.set_variation_by_name(var)
            except Exception:
                pass
        _fcache[k] = f
    return _fcache[k]

def ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)

def ease_out(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3

def ease_in(t):
    t = max(0.0, min(1.0, t))
    return t ** 3

def lerp(a, b, t):
    return a + (b - a) * t

def clamp01(x):
    return max(0.0, min(1.0, x))

def gradient_bg(top, bottom, vignette=0.55):
    y = np.linspace(0, 1, H)[:, None, None]
    top = np.array(top, float)[None, None, :]
    bottom = np.array(bottom, float)[None, None, :]
    img = top * (1 - y) + bottom * y
    img = np.repeat(img, W, axis=1)
    xx, yy = np.meshgrid(np.linspace(-1, 1, W), np.linspace(-1, 1, H))
    d = np.sqrt(xx ** 2 * 0.8 + yy ** 2)
    v = 1 - vignette * np.clip(d - 0.35, 0, 1) ** 1.5
    img = img * v[:, :, None]
    rng = np.random.default_rng(3)
    img += rng.normal(0, 2.0, img.shape)
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB").convert("RGBA")

def glow(img, radius, strength=1.0):
    pad = radius * 3
    big = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad), (0, 0, 0, 0))
    big.paste(img, (pad, pad), img)
    halo = big.filter(ImageFilter.GaussianBlur(radius))
    if strength != 1.0:
        a = np.array(halo).astype(float)
        a[:, :, 3] = np.clip(a[:, :, 3] * strength, 0, 255)
        halo = Image.fromarray(a.astype(np.uint8), "RGBA")
    out = Image.alpha_composite(halo, big)
    return out, pad

def with_alpha(img, a):
    if a >= 0.999:
        return img
    arr = np.array(img)
    arr[:, :, 3] = (arr[:, :, 3].astype(np.float32) * max(0.0, a)).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")

def paste_center(canvas, sprite, cx, cy, alpha=1.0):
    if alpha <= 0.002:
        return
    x = int(round(cx - sprite.width / 2)); y = int(round(cy - sprite.height / 2))
    if x >= canvas.width or y >= canvas.height or x + sprite.width <= 0 or y + sprite.height <= 0:
        return
    if x < 0 or y < 0:
        sprite = sprite.crop((max(-x, 0), max(-y, 0), sprite.width, sprite.height))
        x, y = max(x, 0), max(y, 0)
    if x + sprite.width > canvas.width or y + sprite.height > canvas.height:
        sprite = sprite.crop((0, 0, min(sprite.width, canvas.width - x), min(sprite.height, canvas.height - y)))
    s = with_alpha(sprite, alpha)
    canvas.alpha_composite(s, (x, y))

def camera(frame, zoom=1.0, cx=W / 2, cy=H / 2, shake=0.0, t=0.0):
    if shake:
        cx += shake * (math.sin(t * 37.1) + 0.6 * math.sin(t * 23.7)) * 6
        cy += shake * (math.cos(t * 31.3) + 0.6 * math.sin(t * 19.1)) * 6
    if zoom <= 1.0001 and not shake:
        return frame
    w = W / zoom; h = H / zoom
    x0 = min(max(cx - w / 2, 0), W - w); y0 = min(max(cy - h / 2, 0), H - h)
    return frame.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + w, y0 + h))

def fade(frame, a, color=(0, 0, 0)):
    if a <= 0:
        return frame
    ov = Image.new("RGBA", frame.size, color + (int(255 * clamp01(a)),))
    return Image.alpha_composite(frame, ov)

def text_sprite(txt, fnt, fill, stroke=0, stroke_fill=(0, 0, 0), shadow=True, glow_r=0, glow_col=None):
    bbox = fnt.getbbox(txt, stroke_width=stroke)
    w = bbox[2] - bbox[0] + 40; h = bbox[3] - bbox[1] + 40
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if shadow:
        sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((20 - bbox[0] + 3, 20 - bbox[1] + 5), txt, font=fnt, fill=(0, 0, 0, 170),
                                stroke_width=stroke, stroke_fill=(0, 0, 0, 170))
        sh = sh.filter(ImageFilter.GaussianBlur(6))
        img.alpha_composite(sh)
    d.text((20 - bbox[0], 20 - bbox[1]), txt, font=fnt, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    if glow_r:
        g = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(g).text((20 - bbox[0], 20 - bbox[1]), txt, font=fnt, fill=tuple((glow_col or fill)[:3]) + (255,))
        g, pad = glow(g, glow_r, 0.9)
        base = Image.new("RGBA", g.size, (0, 0, 0, 0))
        base.alpha_composite(g)
        base.alpha_composite(img, (pad, pad))
        return base
    return img

def subtitle(canvas, txt, t_in, t, t_out, y=H - 120, size=50):
    if t < t_in or t > t_out + 0.4:
        return
    n = int(len(txt) * clamp01((t - t_in) / max(0.6, len(txt) * 0.035)))
    a = clamp01((t_out + 0.4 - t) / 0.4)
    shown = txt[:max(n, 1)]
    f = font(DMS, size, "Bold")
    full = f.getbbox(txt)
    spr = text_sprite(shown, f, CREAM + (255,), shadow=True)
    x = W / 2 - (full[2] - full[0]) / 2 - 20
    canvas.alpha_composite(with_alpha(spr, a), (int(x), int(y - spr.height / 2)))

class Encoder:
    def __init__(self, path):
        self.path = path
        self.tmp = path[:-4] + ".part.mp4"
        self.p = subprocess.Popen([
            "ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-r", str(FPS), self.tmp], stdin=subprocess.PIPE)

    def write(self, frame):
        self.p.stdin.write(frame.convert("RGB").tobytes())

    def close(self):
        self.p.stdin.close()
        if self.p.wait() == 0:
            os.replace(self.tmp, self.path)
        else:
            raise RuntimeError("ffmpeg failed for " + self.path)


def memory_card(label, scale=1.0, tint=AMBER, ss=2):
    """A glowing memory card with a date label."""
    cw, ch = int(220 * scale), int(130 * scale)
    S = ss
    img = Image.new("RGBA", (cw * S, ch * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = int(16 * scale * S)
    d.rounded_rectangle((0, 0, cw * S - 1, ch * S - 1), r, fill=(int(tint[0]*0.35),int(tint[1]*0.3),int(tint[2]*0.25),235), outline=tint + (255,), width=max(2, int(4 * scale * S)))
    pad = int(14 * scale * S)
    d.rounded_rectangle((pad, pad, cw * S - pad, int(ch * S * 0.58)), int(8 * scale * S), fill=tint + (90,))
    d.ellipse((int(cw * S * 0.65), int(pad * 1.6), int(cw * S * 0.65 + 22 * scale * S), int(pad * 1.6 + 22 * scale * S)), fill=CREAM + (200,))
    f = font(DMS, max(10, int(26 * scale * S)), "Bold")
    tb = f.getbbox(label)
    d.text(((cw * S - (tb[2] - tb[0])) / 2 - tb[0], int(ch * S * 0.66) - tb[1]), label, font=f, fill=CREAM + (255,))
    img = img.resize((cw, ch), Image.LANCZOS)
    g, pad2 = glow(img, max(4, int(14 * scale)), 0.8)
    return g

def you_head(size=300, eyes_open=1.0, look=(0, 0), ss=3):
    """Protagonist 'You': round head, big eyes, amber hoodie collar."""
    S = ss
    w = size * S; h = int(size * 1.35) * S
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((int(w * 0.08), int(h * 0.62), int(w * 0.92), h + w // 2), int(w * 0.28), fill=AMBER + (255,))
    d.rounded_rectangle((int(w * 0.08), int(h * 0.62), int(w * 0.92), h + w // 2), int(w * 0.28), outline=(214, 140, 40, 255), width=int(4 * S))
    d.ellipse((int(w * 0.06), int(h * 0.02), int(w * 0.94), int(h * 0.70)), fill=(226, 150, 50, 255))
    d.ellipse((int(w * 0.14), int(h * 0.07), int(w * 0.86), int(h * 0.64)), fill=CREAM + (255,))
    d.ellipse((int(w * 0.22), int(h * 0.42), int(w * 0.32), int(h * 0.49)), fill=(255, 170, 150, 120))
    d.ellipse((int(w * 0.68), int(h * 0.42), int(w * 0.78), int(h * 0.49)), fill=(255, 170, 150, 120))
    ex = [0.37, 0.63]; ey = 0.35
    er = 0.085
    for x in ex:
        cx, cy = w * x, h * ey
        rx, ry = w * er, h * er * 0.82 * max(0.08, eyes_open)
        d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=(255, 255, 255, 255), outline=INK + (255,), width=int(3 * S))
        if eyes_open > 0.25:
            px = cx + look[0] * rx * 0.4; py = cy + look[1] * ry * 0.4
            pr = rx * 0.48
            d.ellipse((px - pr, py - pr * max(0.2, eyes_open), px + pr, py + pr * max(0.2, eyes_open)), fill=INK + (255,))
            d.ellipse((px - pr * 0.15 + pr * 0.35, py - pr * 0.55, px + pr * 0.25 + pr * 0.35, py - pr * 0.15), fill=(255, 255, 255, 255))
    d.arc((int(w * 0.45), int(h * 0.47), int(w * 0.55), int(h * 0.52)), 20, 160, fill=INK + (255,), width=int(3 * S))
    for x in (0.42, 0.58):
        d.line((w * x, h * 0.68, w * x, h * 0.86), fill=CREAM + (255,), width=int(5 * S))
    return img.resize((size, int(size * 1.35)), Image.LANCZOS)

DATES = ["JUN 8 2000", "MAR 3 2019", "SEP 14 2011", "JAN 1 2008", "OCT 31 2016", "MAY 22 2013",
         "DEC 25 2009", "AUG 2 2021", "FEB 29 2012", "JUL 4 2015", "APR 9 2018", "NOV 17 2007",
         "JUN 30 2022", "MAR 11 2010", "SEP 1 2014", "JAN 20 2017"]
