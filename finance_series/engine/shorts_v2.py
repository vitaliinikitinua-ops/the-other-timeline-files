"""Shorts v2 - style tests. python3 shorts_v2.py epNN style [variant-name]
Styles:
  full   - no letterbox: blurred full-screen background + zoomed scene, big 2-line hook headline, big captions, progress bar
  number - full + a giant counting number over a dimmed scene for the first ~1.7 s
  quiz   - full + A/B question headline, answer reveal + "comment if you guessed right" in the last 3 s
Hooks/texts per episode live in TESTS below. Output: epNN/tests/EPNN_short_<style>.mp4
"""
import sys, os, json, subprocess, wave, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build as B
from build import *  # noqa  (kit helpers, SC, T, paste_center, AMBER, ...)
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import styles as STY

SW, SH = 1080, 1920
TESTS = {
    "ep01": dict(head=["WHAT IF EVERY \"NO\"", "PAID YOU $1?"], number=dict(text="$198,344", sub="FROM SAYING \"NO\"", col=GREEN),
                 quiz=dict(q="10 \"NO\"s A DAY SINCE 2010 =", a="A) $36K", b="B) $198K", ans="B) ALMOST $200K")),
    "ep02": dict(head=["HE INVESTED 12 YEARS", "AND HAD LESS MONEY"], number=dict(text="-$1,201", sub="AFTER 12 YEARS OF INVESTING", col=CORAL),
                 quiz=dict(q="SAME $200/MONTH. WHO WINS?", a="A) START AT 18", b="B) START AT 30", ans="A) BY ~$190K")),
    "ep03": dict(head=["$5,000 ON A CARD.", "MINIMUM PAYMENTS ONLY."], number=dict(text="$12,782", sub="TO PAY OFF A $5,000 CARD", col=CORAL),
                 quiz=dict(q="MINIMUM PAYMENTS ON $5,000. HOW LONG?", a="A) 3 YEARS", b="B) 19 YEARS", ans="B) 19 YEARS")),
}

def mont(s):
    f = ImageFont.truetype(MONT, s); f.set_variation_by_name("Black"); return f

def text_center(c, txt, size, y, col=(255, 255, 255), maxw=980, stroke=None):
    d = ImageDraw.Draw(c); f = mont(size); sw = stroke or max(6, size // 10)
    while d.textbbox((0, 0), txt, font=f, stroke_width=sw)[2] > maxw and size > 40:
        size -= 4; f = mont(size); sw = stroke or max(6, size // 10)
    bb = d.textbbox((0, 0), txt, font=f, stroke_width=sw)
    d.text(((SW - (bb[2] - bb[0])) / 2 - bb[0], y - (bb[3] - bb[1]) / 2 - bb[1]), txt, font=f, fill=col, stroke_width=sw, stroke_fill=(0, 0, 0))

def make(ep, style):
    m = B.load_ep(ep); sp = m.SHORT; bd = B.bdir(ep)
    fx = None
    if style.startswith("fx-"):
        fx = style[3:]
    cfg = dict(TESTS.get(ep, {})); cfg.setdefault("head", sp["title"]); cfg.setdefault("number", dict(text="", sub="", col=GREEN)); cfg.setdefault("quiz", {})
    timing = json.load(open(os.path.join(bd, "timing.json")))
    clips = []; t = 0.0; names = [b_[0] for b_ in m.BEATS]
    for bi, sis in sp["segs"]:
        bi = names.index(bi) if isinstance(bi, str) else bi
        for si in sis:
            with wave.open(os.path.join(bd, "tts", f"{bi:02d}_{si:02d}.wav")) as w:
                a = np.frombuffer(w.readframes(w.getnframes()), np.int16)
            nz = np.where(np.abs(a) > 300)[0]; a = a[max(0, nz[0] - 200): nz[-1] + 500]
            d = len(a) / B.SR; clips.append((bi, si, t, d, a)); t += d + 0.07   # tighter gaps = faster pace
    total = t + (3.2 if style == "quiz" else 0.8)
    words = []
    for bi, si, st, d, _ in clips:
        ws = timing[bi]["sents"][si]["text"].split(); chunks = []; i = 0
        while i < len(ws):
            if i + 1 < len(ws) and len(ws[i]) + len(ws[i + 1]) <= 8:
                chunks.append(ws[i] + " " + ws[i + 1]); i += 2
            else:
                chunks.append(ws[i]); i += 1
        L = sum(len(c_) + 2 for c_ in chunks); x = st
        for c_ in chunks:
            cd = d * (len(c_) + 2) / L; words.append((c_.upper(), x, x + cd)); x += cd
    out_dir = os.path.join(B.ROOT, ep, "tests"); os.makedirs(out_dir, exist_ok=True)
    vpath = os.path.join(bd, f"short_{style}_v.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{SW}x{SH}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", vpath], stdin=subprocess.PIPE)
    num = cfg["number"]; qz = cfg["quiz"]
    for n in range(int(total * FPS)):
        t = n / FPS
        cl = clips[0]
        for x in clips:
            if t >= x[2] - 0.07:
                cl = x
        bi, si, st, d, _ = cl
        tb = timing[bi]["sents"][si]
        ot = tb["start"] + clamp01((t - st) / max(d, 0.01)) * (tb["end"] - tb["start"])
        sc = SC.render(ot, SC.B(timing[bi]), m.BEATS[bi][2]).convert("RGB")
        if fx:
            sc = STY.STYLES[fx](sc, t)
        # background: the same frame, zoomed to fill, blurred and darkened
        bgs = sc.resize((int(sc.width * SH / sc.height), SH), Image.BILINEAR)
        x0 = (bgs.width - SW) // 2; bg = bgs.crop((x0, 0, x0 + SW, SH)).resize((SW // 8, SH // 8)).filter(ImageFilter.GaussianBlur(3)).resize((SW, SH), Image.BILINEAR)
        c = Image.blend(bg, Image.new("RGB", (SW, SH), (8, 6, 24)), 0.45).convert("RGBA")
        # foreground: zoomed scene with a slow push-in per sentence
        k = (1.0 if fx == "explainer3d" else 1.42) + 0.05 * clamp01((t - st) / max(d, 0.01))
        fw = int(SW * k); fh = int(fw * sc.height / sc.width)
        fg = sc.resize((fw, fh), Image.LANCZOS); cx = (fw - SW) // 2; fg = fg.crop((cx, 0, cx + SW, fh))
        y0 = 560; c.paste(fg, (0, y0))
        dd = ImageDraw.Draw(c); dd.rectangle((0, y0 + fh - 8, SW, y0 + fh), fill=AMBER + (255,))
        # headline (hook) at the top
        if style == "quiz":
            text_center(c, qz["q"], 70, 250, (255, 255, 255))
            text_center(c, qz["a"], 64, 360, (255, 214, 0)); text_center(c, qz["b"], 64, 450, (255, 214, 0))
        else:
            big = 1.0 if t > 2.0 else 1.12
            text_center(c, cfg["head"][0], int(84 * big), 270, (255, 255, 255))
            text_center(c, cfg["head"][1], int(84 * big), 385, (255, 214, 0))
        # captions
        cur = [w_ for w_ in words if w_[1] <= t < w_[2]]
        if cur:
            txt, s0, _ = cur[0]; kk = min(1.0, (t - s0) / 0.1); size = int(118 * (0.85 + 0.15 * (1 - (1 - kk) ** 3)))
            col = (255, 214, 0) if any(ch.isdigit() for ch in txt) or "$" in txt else (255, 255, 255)
            text_center(c, txt, size, y0 + fh + 190, col, 1000)
        # number cold-open
        if style == "number" and t < 1.8:
            a = clamp01((1.8 - t) / 0.3)
            ov = Image.new("RGBA", (SW, SH), (0, 0, 0, int(170 * a))); c = Image.alpha_composite(c, ov)
            digits = "".join(ch for ch in num["text"] if ch.isdigit()); target = int(digits) if digits else 0
            cur_v = int(target * min(1.0, t / 1.0))
            shown = (num["text"][:next(i for i, ch in enumerate(num["text"]) if ch.isdigit())] + f"{cur_v:,}") if digits else num["text"]
            pulse = 1 + 0.05 * math.sin(t * 12)
            spr = T(shown, int(190 * pulse), tuple(num["col"]), "A", 16)
            paste_center(c, spr, SW / 2, SH * 0.45, a)
            spr2 = T(num["sub"], 56, CREAM, "D", 6); paste_center(c, spr2, SW / 2, SH * 0.45 + 170, a)
        # quiz answer reveal
        if style == "quiz" and t > total - 3.0:
            a = clamp01((t - (total - 3.0)) / 0.25)
            ov = Image.new("RGBA", (SW, SH), (0, 0, 0, int(160 * a))); c = Image.alpha_composite(c, ov)
            paste_center(c, T("ANSWER:", 80, CREAM, "A", 8), SW / 2, SH * 0.40, a)
            paste_center(c, T(qz["ans"], 120, GREEN, "A", 12), SW / 2, SH * 0.40 + 150, a)
            paste_center(c, T("DID YOU GUESS RIGHT? COMMENT A OR B", 44, CREAM, "D", 6), SW / 2, SH * 0.40 + 300, a)
        # progress bar + footer
        dd = ImageDraw.Draw(c); dd.rectangle((0, SH - 14, int(SW * t / total), SH), fill=AMBER + (255,))
        paste_center(c, T("Not financial advice · real data", 26, CREAM, "D"), SW / 2, SH - 60, 0.55)
        p.stdin.write(c.convert("RGB").tobytes())
    p.stdin.close(); p.wait()
    vo = np.zeros(int(total * B.SR), np.int16)
    for _, _, st, d, a in clips:
        i0 = int(st * B.SR); vo[i0:i0 + len(a)] = a[:len(vo) - i0]
    vw = os.path.join(bd, f"short_{style}_vo.wav")
    with wave.open(vw, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(B.SR); w.writeframes(vo.tobytes())
    out = os.path.join(out_dir, f"{ep.upper()}_short_{style}.mp4")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", vpath, "-i", vw, "-i", os.path.join(bd, "music.wav"), "-filter_complex",
                    f"[1:a]aresample=44100,pan=stereo|c0=c0|c1=c0,apad,asplit=2[vo][sc];[2:a]atrim=30:{30 + total},asetpts=PTS-STARTPTS,volume=0.4[bed];[bed][sc]sidechaincompress=threshold=0.04:ratio=5:attack=30:release=400[duck];[duck][vo]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{total:.2f}", out], check=True)
    print(f"{ep} {style}: {total:.1f}s -> {out}")

if __name__ == "__main__":
    make(sys.argv[1], sys.argv[2])
