"""EP11 thumbnails A/B/C (1280x720) from clean 3D frames (build3d/clean/s_00N.jpg). Run: python3 thumbs.py"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
HERE = os.path.dirname(os.path.abspath(__file__)); CL = os.path.join(HERE, "build3d", "clean")
ANTON = os.path.join(HERE, "..", "..", "ep2", "fonts", "Anton-Regular.ttf")
W, H = 1280, 720

def base(i, crop, darken_right=True):
    im = Image.open(os.path.join(CL, f"s_{i:03d}.jpg")).crop(crop).resize((W, H), Image.LANCZOS)
    im = ImageEnhance.Color(im).enhance(1.35); im = ImageEnhance.Contrast(im).enhance(1.12)
    if darken_right:
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        for x in range(W // 2, W): d.line([(x, 0), (x, H)], fill=(10, 6, 24, int(200 * (x - W // 2) / (W // 2))))
        im = Image.alpha_composite(im.convert("RGBA"), ov)
    return im.convert("RGBA")

def text(d, s, cx, cy, size, fill, stroke=12, maxw=600, angle=0, im=None):
    f = ImageFont.truetype(ANTON, size)
    while d.textlength(s, font=f) > maxw and size > 30: size -= 4; f = ImageFont.truetype(ANTON, size)
    d.text((cx, cy), s, font=f, fill=fill, anchor="mm", stroke_width=stroke, stroke_fill=(12, 8, 26))
    return d.textbbox((cx, cy), s, font=f, anchor="mm", stroke_width=stroke)

def strike(d, bb, col=(255, 60, 80)):
    d.line([(bb[0] + 10, bb[3] - 25), (bb[2] - 10, bb[1] + 25)], fill=col, width=22)

def make_A():
    im = base(0, (0, 0, 1920, 1080)); d = ImageDraw.Draw(im)
    text(d, "\"ONLY", 960, 95, 90, "white", maxw=520)
    bb = text(d, "$50\"", 960, 215, 150, "white", maxw=520); strike(d, bb)
    text(d, "$1,200", 1000, 470, 250, (255, 194, 58), stroke=16, maxw=500)
    text(d, "REALLY SPENT", 960, 640, 80, "white", maxw=560)
    return im

def make_B():
    im = base(1, (80, 60, 1360, 780)); d = ImageDraw.Draw(im)
    bb = text(d, "-40%", 960, 110, 150, (255, 194, 58), maxw=500); strike(d, bb)
    text(d, "$2,270", 960, 360, 250, (255, 77, 94), stroke=16, maxw=600)
    text(d, "MORE THAN", 960, 540, 90, "white", maxw=560); text(d, "FULL PRICE", 960, 640, 90, "white", maxw=560)
    return im

def make_C():
    im = base(2, (600, 100, 1920, 842)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([780, 50, 1140, 160], 50, fill=(47, 213, 106)); text(d, "PAY IN 4", 960, 105, 70, "white", stroke=0, maxw=320)
    text(d, "7 YEARS", 960, 360, 230, (255, 77, 94), stroke=16, maxw=600)
    text(d, "OF PAYMENTS", 960, 540, 90, "white", maxw=560); text(d, "FOR ONE SALE", 960, 640, 90, (255, 194, 58), maxw=560)
    return im

for n, fn in (("A", make_A), ("B", make_B), ("C", make_C)):
    im = fn().convert("RGB"); im.save(os.path.join(HERE, f"thumb_{n}.jpg"), quality=92)
    im.resize((320, 180), Image.LANCZOS).save(os.path.join(HERE, f"thumb_{n}_320.png"))
sheet = Image.new("RGB", (1920, 360))
for i, n in enumerate("ABC"): sheet.paste(Image.open(os.path.join(HERE, f"thumb_{n}.jpg")).resize((640, 360)), (i * 640, 0)) if i < 3 else None
sheet.save(os.path.join(HERE, "build3d", "thumbs_sheet.jpg")); print("thumbs A/B/C ->", HERE)
