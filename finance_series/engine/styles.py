"""Visual style filters for Shorts (inspired by '10 animation styles' trend). Each takes a PIL RGB scene frame
(1920x1080, flat-vector render from scenes.py) and returns a restyled RGB frame of the same size.
Styles: glow, comic, chalk, lego, pixel, minimal, explainer3d, flat, ps2, cgi."""
import math, random
import numpy as np
from PIL import Image, ImageFilter, ImageOps, ImageEnhance, ImageDraw, ImageChops

_cache = {}

def _edges(img, thick=1, thr=24):
    g = img.convert("L").filter(ImageFilter.FIND_EDGES)
    g = g.point(lambda v: 255 if v > thr else 0)
    if thick > 1:
        g = g.filter(ImageFilter.MaxFilter(thick if thick % 2 else thick + 1))
    return g

def glow(img, t=0):
    e = _edges(img, 3)
    col = ImageEnhance.Color(img).enhance(1.8)
    col = ImageEnhance.Brightness(col).enhance(1.6)
    lines = Image.composite(col, Image.new("RGB", img.size, 0), e)
    # warm ink fallback for dark lines
    bloom = lines.filter(ImageFilter.GaussianBlur(14))
    bloom2 = lines.filter(ImageFilter.GaussianBlur(4))
    out = ImageChops.add(ImageChops.add(lines, bloom2), ImageEnhance.Brightness(bloom).enhance(1.6))
    return out

def comic(img, t=0):
    p = ImageOps.posterize(ImageEnhance.Color(img).enhance(1.5), 3)
    # halftone dots on midtones
    key = ("halftone", img.size)
    if key not in _cache:
        w, h = img.size; dots = Image.new("L", img.size, 255); d = ImageDraw.Draw(dots)
        for y in range(0, h, 12):
            for x in range((y // 12 % 2) * 6, w, 12):
                d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=170)
        _cache[key] = dots
    lum = p.convert("L").point(lambda v: 255 if 70 < v < 190 else 0)
    shade = Image.composite(_cache[key], Image.new("L", img.size, 255), lum)
    p = ImageChops.multiply(p, Image.merge("RGB", [shade] * 3))
    ink = _edges(img, 5)
    p.paste((10, 10, 10), mask=ink)
    return p

def chalk(img, t=0):
    key = ("board", img.size)
    if key not in _cache:
        w, h = img.size
        n = (np.random.RandomState(3).rand(h // 4, w // 4) * 40).astype(np.uint8)
        nz = Image.fromarray(n).resize((w, h), Image.BILINEAR).filter(ImageFilter.GaussianBlur(2))
        base = Image.new("RGB", (w, h), (30, 64, 44))
        board = ImageChops.add(base, Image.merge("RGB", [nz, nz, nz]), scale=1.6)
        _cache[key] = board
        grain = (np.random.RandomState(5).rand(h, w) > 0.35).astype(np.uint8) * 255
        _cache[("grain", img.size)] = Image.fromarray(grain)
    e = _edges(img, 3)
    e = ImageChops.multiply(e, _cache[("grain", img.size)]).filter(ImageFilter.GaussianBlur(0.8))
    out = _cache[key].copy()
    out.paste((236, 240, 228), mask=e)
    # tinted chalk for coloured elements (numbers, money)
    sat = np.array(img.convert("HSV"))[:, :, 1]
    colmask = Image.fromarray(((sat > 140).astype(np.uint8) * 255)).filter(ImageFilter.MinFilter(3))
    colmask = ImageChops.multiply(colmask, e)
    out.paste(ImageEnhance.Brightness(img).enhance(1.4), mask=colmask)
    return out

def lego(img, t=0, cell=40):
    w, h = img.size
    small = img.resize((w // cell, h // cell), Image.BILINEAR)
    small = ImageEnhance.Color(small).enhance(1.4).quantize(colors=16, method=Image.Quantize.MEDIANCUT).convert("RGB")
    big = small.resize((w, h), Image.NEAREST)
    key = ("studs", img.size, cell)
    if key not in _cache:
        hi = Image.new("L", img.size, 0); sh = Image.new("L", img.size, 0)
        dh, ds = ImageDraw.Draw(hi), ImageDraw.Draw(sh)
        r = cell * 0.32
        for y in range(0, h, cell):
            for x in range(0, w, cell):
                dh.line((x, y, x + cell - 1, y), fill=55, width=2); dh.line((x, y, x, y + cell - 1), fill=55, width=2)
                ds.line((x, y + cell - 1, x + cell - 1, y + cell - 1), fill=90, width=2); ds.line((x + cell - 1, y, x + cell - 1, y + cell - 1), fill=90, width=2)
                cx, cy = x + cell / 2, y + cell / 2
                ds.ellipse((cx - r + 3, cy - r + 3, cx + r + 3, cy + r + 3), fill=85)
                dh.ellipse((cx - r, cy - r, cx + r - 2, cy + r - 2), fill=45)
        _cache[key] = (hi.filter(ImageFilter.GaussianBlur(0.7)), sh.filter(ImageFilter.GaussianBlur(0.7)))
    hi, sh = _cache[key]
    out = ImageChops.subtract(big, Image.merge("RGB", [sh] * 3))
    out = ImageChops.add(out, Image.merge("RGB", [hi] * 3))
    return ImageEnhance.Color(out).enhance(1.3)

def pixel(img, t=0, px=14):
    w, h = img.size
    s = img.resize((w // px, h // px), Image.BOX).quantize(colors=16, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert("RGB")
    return ImageEnhance.Color(s.resize((w, h), Image.NEAREST)).enhance(1.25)

def minimal(img, t=0):
    e = _edges(img, 3)
    out = Image.new("RGB", img.size, (246, 242, 234))
    out.paste((28, 28, 32), mask=e)
    hsv = np.array(img.convert("HSV")); acc = ((hsv[:, :, 1] > 150) & (hsv[:, :, 2] > 150)).astype(np.uint8) * 255
    accm = Image.fromarray(acc).filter(ImageFilter.MinFilter(5))
    out.paste((238, 90, 60), mask=ImageChops.multiply(accm, e.filter(ImageFilter.MaxFilter(3))))
    return out

def flat(img, t=0):
    out = ImageEnhance.Color(img).enhance(1.25)
    out = ImageEnhance.Contrast(out).enhance(1.08)
    ink = _edges(img, 3, thr=40)
    out.paste((22, 18, 40), mask=ink)
    return out

def ps2(img, t=0):
    w, h = img.size
    s = img.resize((424, 240), Image.BILINEAR)
    s = ImageOps.posterize(s, 5)
    s = s.convert("P", palette=Image.Palette.ADAPTIVE, colors=64).convert("RGB")
    # vertex-wobble style jitter
    j = int(round(math.sin(t * 7.3) * 1.2)); s = ImageChops.offset(s, j, 0)
    big = s.resize((w, h), Image.NEAREST).filter(ImageFilter.GaussianBlur(0.6))
    fog = Image.new("RGB", (w, h), (120, 130, 160))
    grad = Image.linear_gradient("L").resize((w, h)).point(lambda v: int(v * 0.18))
    big = Image.composite(big, fog, ImageOps.invert(grad).point(lambda v: min(255, v + 20)))
    big = ImageEnhance.Contrast(ImageEnhance.Color(big).enhance(0.95)).enhance(1.2)
    # CRT scanlines
    key = ("scan", img.size)
    if key not in _cache:
        sc = Image.new("L", (w, h), 255); d = ImageDraw.Draw(sc)
        for y in range(0, h, 4):
            d.line((0, y, w, y), fill=205)
        _cache[key] = Image.merge("RGB", [sc] * 3)
    return ImageChops.multiply(big, _cache[key])

def cgi(img, t=0):
    w, h = img.size
    soft = img.filter(ImageFilter.GaussianBlur(0.8))
    lum = np.asarray(soft.convert("L"), dtype=np.float32)
    height = np.asarray(Image.fromarray(lum.astype(np.uint8)).filter(ImageFilter.GaussianBlur(9)), dtype=np.float32)
    gy, gx = np.gradient(height)
    light = np.clip(0.95 + (-gx * 0.7 - gy * 1.0) / 7.0, 0.55, 1.45)
    base = np.asarray(ImageEnhance.Color(soft).enhance(1.15), dtype=np.float32)
    shaded = np.clip(base * light[:, :, None], 0, 255).astype(np.uint8)
    out = Image.fromarray(shaded)
    bloom = ImageEnhance.Brightness(out.filter(ImageFilter.GaussianBlur(18))).enhance(0.5)
    out = ImageChops.screen(out, bloom)
    # depth of field: blur the top band
    key = ("dof", img.size)
    if key not in _cache:
        m = Image.linear_gradient("L").resize((w, h)).point(lambda v: 160 if v < 25 else max(0, int(160 - (v - 25) * 4)))
        _cache[key] = m
    out = Image.composite(out.filter(ImageFilter.GaussianBlur(5)), out, _cache[key])
    vign = Image.radial_gradient("L").resize((w, h)).point(lambda v: int(255 - v * 0.35))
    return ImageChops.multiply(out, Image.merge("RGB", [vign] * 3))

def explainer3d(img, t=0):
    """Scene on a floating 3D card: perspective tilt that slowly sways, thickness, soft shadow, studio background."""
    w, h = img.size
    face = ImageEnhance.Color(img).enhance(1.15)
    ang = math.sin(t * 0.8) * 0.06
    sx, sy = 0.78, 0.78
    # target quad (tl, tr, br, bl) in output space
    cx, cy = w / 2, h / 2 - 20
    hw, hh = w * sx / 2, h * sy / 2
    dz = 0.10 + ang
    tl = (cx - hw * (1 - dz), cy - hh * 0.92); tr = (cx + hw * (1 + dz), cy - hh * 1.0)
    br = (cx + hw * (1 + dz) * 1.02, cy + hh * 1.0); bl = (cx - hw * (1 - dz) * 1.02, cy + hh * 0.92)
    def coeffs(src, dst):
        A = []; B = []
        for (x, y), (u, v) in zip(dst, src):
            A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]; B += [u, v]
        return np.linalg.solve(np.array(A, float), np.array(B, float)).tolist()
    src = [(0, 0), (w, 0), (w, h), (0, h)]; dst = [tl, tr, br, bl]
    key = ("studio", img.size)
    if key not in _cache:
        bg = Image.radial_gradient("L").resize((w, h)).point(lambda v: int(250 - v * 0.55))
        _cache[key] = Image.merge("RGB", [bg, bg.point(lambda v: int(v * 0.97)), bg.point(lambda v: int(v * 1.0))])
    out = _cache[key].copy()
    # shadow
    shadow = Image.new("L", (w, h), 0); ImageDraw.Draw(shadow).polygon([(p[0] + 30, p[1] + 60) for p in dst], fill=140)
    out = Image.composite(Image.new("RGB", (w, h), (40, 40, 60)), out, shadow.filter(ImageFilter.GaussianBlur(40)))
    # thickness (edge slab)
    slab = [(bl[0], bl[1]), (br[0], br[1]), (br[0], br[1] + 22), (bl[0], bl[1] + 22)]
    ImageDraw.Draw(out).polygon(slab, fill=(70, 60, 110))
    warped = face.transform((w, h), Image.PERSPECTIVE, coeffs(src, dst), Image.BICUBIC)
    mask = Image.new("L", (w, h), 0); ImageDraw.Draw(mask).polygon(dst, fill=255)
    out.paste(warped, mask=mask)
    # glossy highlight
    gl = Image.new("L", (w, h), 0); ImageDraw.Draw(gl).polygon([tl, (tl[0] + (tr[0] - tl[0]) * 0.45, tl[1]), (bl[0] + (br[0] - bl[0]) * 0.2, bl[1]), bl], fill=26)
    out = Image.composite(Image.new("RGB", (w, h), (255, 255, 255)), out, ImageChops.multiply(gl, mask))
    return out

STYLES = {"glow": glow, "comic": comic, "chalk": chalk, "lego": lego, "pixel": pixel, "minimal": minimal,
          "explainer3d": explainer3d, "flat": flat, "ps2": ps2, "cgi": cgi}
NAMES = {"glow": "Glow Sketch", "comic": "Comic Art", "chalk": "Chalkboard", "lego": "Lego Style", "pixel": "Pixel Art",
         "minimal": "Minimal Line", "explainer3d": "Explainer 3D", "flat": "Flat Vector", "ps2": "PS2 Style", "cgi": "CGI Motion"}
