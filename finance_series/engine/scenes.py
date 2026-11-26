"""Declarative scene renderer. A beat = (name, sentences, scene). Scene items appear on sentence
indexes (`at`), so visuals land on the words. Camera changes shot on every sentence (max motion)."""
import math, random
from kit import *  # noqa

class B:
    """Timing helper for one beat: absolute t0/t1 and sentence starts."""
    def __init__(self, tb):
        self.t0, self.t1 = tb["start"], tb["end"]
        self.s = [x["start"] for x in tb["sents"]]
        self.e = [x["end"] for x in tb["sents"]]
    def S(self, i):
        if i is None:
            return self.t0
        if isinstance(i, float) and not float(i).is_integer():
            k = int(i); return self.s[min(k, len(self.s) - 1)] + (i - k) * (self.e[min(k, len(self.e) - 1)] - self.s[min(k, len(self.s) - 1)])
        return self.s[min(int(i), len(self.s) - 1)] if i >= 0 else self.t0
    def E(self, i):
        return self.e[min(int(i), len(self.e) - 1)]
    def sent(self, t):
        k = 0
        for i, s in enumerate(self.s):
            if t >= s - 0.05:
                k = i
        return k

def at(b, item, key="at", default=0):
    v = item.get(key, default)
    return b.t0 if v is None else b.S(v)

def until(b, item):
    v = item.get("until")
    return 1e9 if v is None else b.S(v)

def emo_at(spec, k):
    if isinstance(spec, str):
        return spec
    cur = "neutral"
    for i in sorted(spec):
        if k >= i:
            cur = spec[i]
    return cur

PROP = {
    "card": lambda a: card(a.get("label", "VISA"), tuple(a.get("col", TEAL)), a.get("scale", 1.0), a.get("number", "4417")),
    "phone": lambda a: phone(a.get("text", "$0"), a.get("sub", "BALANCE"), tuple(a.get("col", GREEN)), a.get("scale", 1.0)),
    "bill": lambda a: bill(a.get("amount", "100"), a.get("scale", 1.0)),
    "tag": lambda a: tag(a["text"], tuple(a.get("col", AMBER)), a.get("scale", 1.0), a.get("sub")),
    "icon": lambda a: icon(a["name"], a.get("scale", 1.0)),
    "receipt": lambda a: receipt(tuple(tuple(x) for x in a["lines"]), a.get("total"), a.get("scale", 1.0)),
    "calendar": lambda a: calendar(a.get("top", "2010"), a.get("big", "JAN"), a.get("scale", 1.0), tuple(a.get("col", CORAL))),
    "coin": lambda a: coin(a.get("scale", 1.0), a.get("sym", "$")),
    "jar": lambda a: jar(round(a.get("fill", 0.5), 2)),
}

def draw_common_overlays(c, t, b, sc):
    """texts, bubbles, counters, lines, rains shared by most scene types."""
    k = b.sent(t)
    for ln in sc.get("lines", []):
        t0 = at(b, ln)
        if t0 <= t <= until(b, ln):
            p = ease_out(clamp01((t - t0) / 0.6))
            glow_line(c, *ln["from"], *ln["to"], t, tuple(ln.get("col", PINK)), ln.get("width", 10), p)
    for rn in sc.get("rain", []):
        t0 = at(b, rn)
        if t0 <= t <= until(b, rn):
            rng = random.Random(rn.get("seed", 3))
            for i in range(rn.get("n", 24)):
                x = rng.uniform(80, W - 80); sp = rng.uniform(250, 520); ph = rng.uniform(0, 2)
                y = ((t - t0) * sp + ph * 300) % (H + 200) - 120
                spr = bill("1", 0.45) if rn.get("kind", "bill") == "bill" else coin(0.45)
                paste_center(c, spr.rotate(rng.uniform(-30, 30) + t * 40 * (1 if i % 2 else -1), expand=True), x, y, 0.95)
    for pr in sc.get("props", []):
        t0 = at(b, pr)
        if t < t0 or t > until(b, pr) + 0.25:
            continue
        spr = PROP[pr["kind"]](pr)
        if pr.get("rot"):
            spr = spr.rotate(pr["rot"], expand=True, resample=Image.BICUBIC)
        y = pr["y"] + (math.sin(t * 2.4 + pr["x"] * 0.01) * 10 if pr.get("float", True) else 0)
        if pr.get("shake_at") is not None and 0 <= t - b.S(pr["shake_at"]) < 0.5:
            y += math.sin(t * 60) * 8
        pop(c, spr, pr["x"], y, t, t0, until(b, pr), anim=pr.get("anim", "pop"))
    for bu in sc.get("bubbles", []):
        t0 = at(b, bu)
        if t0 <= t <= until(b, bu):
            bubble(c, bu["text"], bu["x"], bu["y"], clamp01((t - t0) / 0.3), bu.get("tail", "down"), bu.get("size", 40), tuple(bu.get("tint", CREAM)))
    for tx in sc.get("texts", []):
        t0 = at(b, tx)
        spr = T(tx["text"], tx.get("size", 90), tuple(tx.get("col", CREAM)), tx.get("f", "A"), tx.get("glow", 0))
        pop(c, spr, tx.get("x", W / 2), tx.get("y", 160), t, t0, until(b, tx), anim=tx.get("anim", "pop"))
    for cn in sc.get("counters", []):
        t0 = at(b, cn)
        if t < t0 or t > until(b, cn) + 0.25:
            continue
        t1 = b.S(cn["to_at"]) if "to_at" in cn else t0 + cn.get("dur", 1.6)
        v = lerp(cn["from"], cn["to"], ease_out(clamp01((t - t0) / max(0.1, t1 - t0))))
        txt = cn.get("prefix", "") + (money(v) if cn.get("fmt", "money") == "money" else f"{int(round(v)):,}") + cn.get("suffix", "")
        if cn.get("label"):
            pop(c, T(cn["label"], cn.get("lsize", 38), tuple(cn.get("lcol", CREAM)), "D"), cn["x"], cn["y"] - cn.get("size", 110) * 0.75, t, t0, until(b, cn))
        pop(c, T(txt, cn.get("size", 110), tuple(cn.get("col", AMBER)), "A", 0), cn["x"], cn["y"], t, t0, until(b, cn))

def draw_actors(c, t, b, sc):
    k = b.sent(t)
    for i, ac in enumerate(sc.get("actors", [])):
        t0 = at(b, ac, default=None) if "at" in ac else b.t0
        if t < t0 or t > until(b, ac) + 0.2:
            continue
        a = clamp01((t - t0) / 0.25) * clamp01((until(b, ac) + 0.2 - t) / 0.2)
        x = ac["x"]
        if "move" in ac:  # [(sent, x)]
            for (si, nx), nxt in zip(ac["move"], ac["move"][1:] + [None]):
                pass
            for si, nx in ac["move"]:
                if t >= b.S(si):
                    x0 = x; ts = b.S(si); x = lerp(x0, nx, ease(clamp01((t - ts) / 0.8)))
        talk = k in ac.get("talk", [])
        draw_actor(c, ac["who"], x, ac.get("y", 1000), ac.get("size", 300), t, emo_at(ac.get("emo", "neutral"), k),
                   tuple(ac.get("look", (0, 0))), seed=i * 1.7, alpha=a, flip=ac.get("flip", False), talk=talk)

def shot(c, t, b, sc):
    """Auto camera: a new framing on every sentence (wide / push to focus / pan)."""
    if sc.get("static"):
        return c
    k = b.sent(t)
    focus = sc.get("focus", {})
    fx, fy = focus.get(k, focus.get("default", (W / 2, H / 2 - 40))) if isinstance(focus, dict) else focus
    ts = b.S(k); u = ease(clamp01((t - ts) / 0.7))
    mode = k % 3
    if mode == 0:
        z = 1.0 + 0.04 * clamp01((t - ts) / 6)
        cx, cy = W / 2, H / 2
    elif mode == 1:
        z = 1.10 + 0.04 * clamp01((t - ts) / 6)
        cx, cy = lerp(W / 2, fx, 0.85), lerp(H / 2, fy, 0.85)
    else:
        z = 1.06
        cx, cy = W / 2 + (1 if k % 2 else -1) * 60 * (clamp01((t - ts) / 6) - 0.5), H / 2
    if sc.get("type") == "chart":  # keep the side panel and axis labels fully in frame
        z = min(z, 1.035); cx, cy = W / 2, H / 2
    sh = 0
    for s_k in sc.get("shake", []):
        if 0 <= t - b.S(s_k) < 0.45:
            sh = 1.0 - (t - b.S(s_k)) / 0.45
    # quick zoom-in snap on shot change
    z *= 1 + 0.03 * (1 - u)
    return camera(c, z, cx, cy, sh, t)

def flash(c, t, b, sc):
    for s_k, col in sc.get("flash", {}).items():
        dt = t - b.S(s_k)
        if 0 <= dt < 0.3:
            c = fade(c, 0.45 * (1 - dt / 0.3), tuple(col))
    return c

# ------------------------------------------------------------ scene types
def sc_stage(t, b, sc):
    c = location(sc.get("loc", "void")).copy()
    if sc.get("particles", sc.get("loc", "void").startswith("void")):
        particles(c, t, 35, 7, tuple(sc.get("pcol", AMBER)))
    draw_actors(c, t, b, sc)
    draw_common_overlays(c, t, b, sc)
    return shot(c, t, b, sc)

def sc_split(t, b, sc):
    c = location("void").copy()
    ov = Image.new("RGBA", c.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    for side, x0 in (("left", 0), ("right", W // 2)):
        s = sc[side]; od.rectangle((x0, 0, x0 + W // 2, H), fill=tuple(s.get("col", CORAL)) + (34,))
    c.alpha_composite(ov)
    d = ImageDraw.Draw(c); d.line((W / 2, 60, W / 2, H - 60), fill=CREAM + (90,), width=4)
    k = b.sent(t)
    for side, cx in (("left", W / 4), ("right", 3 * W / 4)):
        s = sc[side]; t0 = at(b, s)
        if t < t0:
            continue
        pop(c, T(s["title"], 72, tuple(s.get("col", CORAL)), "A", 8), cx, 120, t, t0)
        if s.get("sub"):
            pop(c, T(s["sub"], 36, CREAM, "D"), cx, 200, t, t0 + 0.2)
        if s.get("who"):
            draw_actor(c, s["who"], cx + s.get("dx", -120), 980, s.get("size", 300), t, emo_at(s.get("emo", "neutral"), k), seed=1 if side == "left" else 2)
        for pr in s.get("props", []):
            pr2 = dict(pr); pr2.setdefault("x", cx + 140); pr2.setdefault("y", 700)
            t1 = at(b, pr2, default=s.get("at", 0))
            if t >= t1:
                y = pr2["y"] + math.sin(t * 2.4 + cx) * 8
                pop(c, PROP[pr2["kind"]](pr2), pr2["x"], y, t, t1)
        v = s.get("value")
        if v:
            tv0 = b.S(v.get("at", s.get("at", 0))); tv1 = b.S(v["to_at"]) if "to_at" in v else tv0 + v.get("dur", 2.0)
            if t >= tv0:
                val = lerp(v["from"], v["to"], ease_out(clamp01((t - tv0) / max(0.1, tv1 - tv0))))
                txt = v.get("prefix", "") + (money(val) if v.get("fmt", "money") == "money" else f"{int(round(val)):,}") + v.get("suffix", "")
                pop(c, T(txt, v.get("size", 110), tuple(v.get("vcol", s.get("col", CORAL))), "A", 10), cx, v.get("y", 380), t, tv0)
                if v.get("label"):
                    pop(c, T(v["label"], 34, CREAM, "D"), cx, v.get("y", 380) + 85, t, tv0)
    draw_common_overlays(c, t, b, sc)
    return shot(c, t, b, dict(sc, focus=sc.get("focus", {"default": (W / 2, H / 2)})))

def sc_chart(t, b, sc):
    c = location(sc.get("loc", "void")).copy()
    particles(c, t, 25, 11, TEAL)
    X0, Y0, X1, Y1 = sc.get("box", (150, 210, 1380, 840))
    n = len(sc["series"][0]["values"])
    r0, r1 = sc.get("reveal", (None, None))
    ta = b.S(r0) if r0 is not None else b.t0 + 0.4
    tb_ = b.S(r1) if r1 is not None else b.t1 - 0.8
    p = ease(clamp01((t - ta) / max(0.5, tb_ - ta)))
    p0 = sc.get("p0", 0.0)
    p = p0 + (1 - p0) * p
    kf = max(1.0, p * (n - 1)); ki = int(kf)
    vis = [v for s in sc["series"] for v in s["values"][:ki + 1]]
    vmax = sc.get("vmax") or max(1, max(vis) * 1.22)
    d = ImageDraw.Draw(c)
    fs = font(DMS, 26, "Bold")
    steps = [1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000, 2000, 2500, 5000, 10000, 20000, 25000, 50000, 100000, 200000, 250000, 500000]
    step = next((s for s in steps if vmax / s <= 6), steps[-1])
    def X(i): return X0 + (X1 - X0) * i / max(1, n - 1)
    def Y(v): return Y1 - (Y1 - Y0) * v / vmax
    v = 0
    while v <= vmax:
        y = Y(v); d.line((X0, y, X1, y), fill=(255, 255, 255, 25), width=2)
        lab = sc.get("yfmt", "${:,.0f}").format(v) if step < 1000 else (f"${v / 1000:,.0f}K" if step % 1000 == 0 else f"${v / 1000:,.1f}K")
        if sc.get("yfmt") == "{:.0f}%":
            lab = f"{v:.0f}%"
        d.text((X0 - 12 - fs.getlength(lab), y - 16), lab, font=fs, fill=CREAM + (140,))
        v += step
    for i, lab in sc.get("xlabels", []):
        d.text((X(i) - fs.getlength(lab) / 2, Y1 + 14), lab, font=fs, fill=CREAM + (150,))
    for s in sc["series"]:
        vals = s["values"]
        pts = [(X(i), Y(vals[i])) for i in range(ki + 1)]
        if ki < n - 1 and kf > ki:
            pts.append((X(kf), Y(lerp(vals[ki], vals[ki + 1], kf - ki))))
        if len(pts) < 2:
            continue
        if s.get("fill"):
            ov = Image.new("RGBA", c.size, (0, 0, 0, 0))
            ImageDraw.Draw(ov).polygon(pts + [(pts[-1][0], Y1), (X0, Y1)], fill=tuple(s["col"]) + (45,)); c.alpha_composite(ov); d = ImageDraw.Draw(c)
        d.line(pts, fill=tuple(s["col"]) + (255,), width=s.get("width", 8), joint="curve")
        x, y = pts[-1]; d.ellipse((x - 12, y - 12, x + 12, y + 12), fill=tuple(s["col"]) + (255,), outline=CREAM + (255,), width=4)
        if s.get("label"):
            pop(c, T(s["label"](kf) if callable(s["label"]) else s["label"], 40, tuple(s["col"]), "A"), min(x + 20, X1 + 120), y - 40, t, ta)
    for nt in sc.get("notes", []):
        if kf >= nt["i"]:
            yy = Y(nt.get("v", sc["series"][nt.get("s", 0)]["values"][nt["i"]])) + nt.get("dy", 90)
            pop(c, T(nt["text"], nt.get("size", 44), tuple(nt.get("col", CORAL)), "A", 6), X(nt["i"]) + nt.get("dx", 0), yy, t, ta)
    # side panel
    for j, cn in enumerate(sc.get("side", [])):
        vals = cn["values"]; vv = vals[min(int(kf), len(vals) - 1)]
        y = 300 + j * 160
        lab = T(cn["label"], 34, tuple(cn.get("col", CREAM)), "D")
        if lab.width > 420:
            lab = lab.resize((420, int(lab.height * 420 / lab.width)), Image.LANCZOS)
        paste_center(c, lab, 1650, y)
        txt = money(vv) if cn.get("fmt", "money") == "money" else cn["fmt"].format(vv)
        val = T(txt, 70, tuple(cn.get("col", CREAM)), "A")
        if val.width > 420:
            val = val.resize((420, int(val.height * 420 / val.width)), Image.LANCZOS)
        paste_center(c, val, 1650, y + 62)
    if sc.get("xnow"):
        paste_center(c, T(sc["xnow"](kf), 36, CREAM, "D"), 1650, 300 + len(sc.get("side", [])) * 160 + 20)
    if sc.get("footnote"):
        d = ImageDraw.Draw(c); d.text((X0, 905), sc["footnote"], font=font(DMS, 22, "Bold"), fill=CREAM + (100,))
    for ac in sc.get("actors", []):
        draw_actor(c, ac["who"], ac.get("x", 1650), ac.get("y", 1060), ac.get("size", 170), t, emo_at(ac.get("emo", "neutral"), b.sent(t)), seed=0.5)
    draw_common_overlays(c, t, b, sc)
    return shot(c, t, b, dict(sc, focus=sc.get("focus", {"default": (900, 500)})))

def sc_bars(t, b, sc):
    c = location(sc.get("loc", "void")).copy(); particles(c, t, 30, 13)
    base = sc.get("base", 770); hmax = sc.get("hmax", 480)
    allv = [v for g in sc["groups"] for v, _ in g["vals"]]
    vmax = sc.get("vmax") or max(allv)
    ng = len(sc["groups"]); gw = (W - 300) / ng
    for j, g in enumerate(sc["groups"]):
        t0 = at(b, g)
        if t < t0:
            continue
        p = ease_out(clamp01((t - t0) / 1.0))
        cx = 150 + gw * (j + 0.5); nv = len(g["vals"]); bw = min(150, gw / (nv + 0.6))
        for i, (v, col) in enumerate(g["vals"]):
            x = cx + (i - (nv - 1) / 2) * (bw + 16)
            hgt = hmax * v / vmax * p
            if hgt > 2:
                paste_center(c, Image.new("RGBA", (int(bw), int(hgt)), tuple(col) + (255,)), x, base - hgt / 2)
            lab = money(round(v * p, 0 if v < 10000 else (-1 if v < 100000 else -2))) if sc.get("fmt", "money") == "money" else sc["fmt"].format(v * p)
            pop(c, T(lab, 38 if nv > 1 else 52, tuple(col), "A"), x, base - hgt - 34, t, t0 + 0.2)
        pop(c, T(g["label"], 40, CREAM, "A"), cx, base + 48, t, t0)
        if g.get("sub"):
            pop(c, T(g["sub"], 28, CREAM, "D"), cx, base + 98, t, t0 + 0.2)
    if sc.get("legend"):
        x = 1350
        for lab, col in sc["legend"]:
            d = ImageDraw.Draw(c); d.rectangle((x, 160, x + 30, 190), fill=tuple(col) + (255,)); d.text((x + 42, 158), lab, font=font(DMS, 30, "Bold"), fill=CREAM + (220,)); x += 60 + font(DMS, 30, "Bold").getlength(lab)
    draw_actors(c, t, b, sc)
    draw_common_overlays(c, t, b, sc)
    return shot(c, t, b, dict(sc, focus=sc.get("focus", {"default": (W / 2, 560)})))

def sc_list(t, b, sc):
    c = location(sc.get("loc", "void")).copy(); particles(c, t, 30, 17)
    if sc.get("title"):
        pop(c, T(sc["title"], 84, tuple(sc.get("tcol", AMBER)), "A", 10), W / 2, 130, t, b.t0)
    items = sc["items"]
    if sc.get("cards"):
        n = len(items); cw = min(520, (W - 200) / n - 40)
        for j, it in enumerate(items):
            t0 = b.S(it.get("at", j))
            if t < t0:
                continue
            x = W / 2 + (j - (n - 1) / 2) * (cw + 40); col = tuple(it.get("col", [AMBER, TEAL, CORAL, PURPLE][j % 4]))
            pop(c, panel_img(int(cw), 520, col), x, 560, t, t0)
            pop(c, T(it.get("num", str(j + 1)), 120, col, "A", 8), x, 400, t, t0 + 0.1)
            pop(c, T(it["text"], 46 if len(it["text"]) < 18 else 36, CREAM, "A"), x, 580, t, t0 + 0.2)
            if it.get("sub"):
                pop(c, T(it["sub"], 28, CREAM, "D"), x, 660, t, t0 + 0.3)
    else:
        for j, it in enumerate(items):
            t0 = b.S(it.get("at", j))
            if t < t0:
                continue
            y = 290 + j * 112; a = clamp01((t - t0) / 0.3)
            d = ImageDraw.Draw(c)
            d.rounded_rectangle((300, y - 32, 364, y + 32), 14, outline=TEAL + (int(255 * a),), width=6)
            if t > t0 + 0.3:
                d.line([(314, y), (330, y + 18), (352, y - 18)], fill=TEAL + (255,), width=8)
            spr = T(it["text"], 50, CREAM, "D")
            pop(c, spr, 400 + spr.width / 2, y, t, t0, anim="slide_r")
    draw_actors(c, t, b, sc)
    draw_common_overlays(c, t, b, sc)
    return shot(c, t, b, dict(sc, focus=sc.get("focus", {"default": (W / 2, 520)})))

@lru_cache(maxsize=16)
def panel_img(w, h, col):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle((0, 0, w - 1, h - 1), 30, fill=(14, 22, 40, 235), outline=col + (255,), width=5)
    return img

def sc_end(t, b, sc):
    """Outro question + end-screen safe layout (two video slots + subscribe circle in the last 15 s)."""
    c = location("void").copy(); particles(c, t, 50, 91)
    k = b.sent(t)
    pop(c, T(sc.get("q1", "WHICH TIMELINE"), 100, CREAM), W / 2, 150, t, b.t0)
    pop(c, T(sc.get("q2", "ARE YOU IN?"), 120, AMBER, "A", 14), W / 2, 280, t, b.t0 + 0.3)
    draw_actor(c, "you", W / 2, 960, 320, t, emo_at(sc.get("emo", "happy"), k))
    if sc.get("comment"):
        bubble(c, sc["comment"], W / 2, 520, clamp01((t - b.S(sc.get("comment_at", 1))) / 0.3), size=40)
    draw_common_overlays(c, t, b, sc)
    return c

TYPES = {"stage": sc_stage, "split": sc_split, "chart": sc_chart, "bars": sc_bars, "list": sc_list, "end": sc_end}

def render(t, b, sc):
    c = TYPES[sc.get("type", "stage")](t, b, sc)
    return flash(c, t, b, sc)
