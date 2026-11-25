"""3 vertical Shorts cut from the long video (same narration clips, scenes re-framed for 9:16,
word-by-word captions per story-shorts-studio). python3 shorts.py [stills]"""
import sys, os, wave, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import video as V
from video import *  # noqa
from PIL import Image, ImageDraw, ImageFont

SW, SH = 1080, 1920
MONT = os.path.join(HERE, "..", "ep2", "fonts", "Montserrat.ttf")
SR = 22050; GAP = 0.18

SHORTS = [
    ("short1_coffee", ["$5 COFFEE EVERY DAY", "SINCE 2010"],
     [(0, [0]), (2, [3, 4, 5]), (4, [0]), (9, [1, 2, 3]), (15, [2])]),
    ("short2_crash", ["THE 2020 CRASH:", "SELL OR HOLD?"],
     [(6, [0, 1, 2]), (7, [1, 2, 3]), (8, [0, 1, 3]), (9, [2])]),
    ("short3_amount", ["$1 vs $5 vs $10", "A DAY SINCE 2010"],
     [(0, [0]), (11, [1, 2]), (9, [1, 2]), (10, [0, 2, 3])]),
]

def build_timeline(segs):
    """-> list of clips: (bi, si, short_start, dur, orig_start, wav array)"""
    clips = []; t = 0.35
    for bi, sis in segs:
        for si in sis:
            p = os.path.join(HERE, "build", "tts", f"{bi:02d}_{si:02d}.wav")
            with wave.open(p) as w:
                a = np.frombuffer(w.readframes(w.getnframes()), np.int16)
            nz = np.where(np.abs(a) > 300)[0]; a = a[max(0, nz[0] - 400): nz[-1] + 800]
            d = len(a) / SR
            clips.append((bi, si, t, d, V.TIM[bi]["sents"][si]["start"], a))
            t += d + GAP
    return clips, t + 1.2

def words_of(clips):
    out = []
    for bi, si, st, d, _, _ in clips:
        txt = V.TIM[bi]["sents"][si]["text"]
        ws = txt.split(); chunks = []
        i = 0
        while i < len(ws):  # 1-2 words per chunk, short words paired
            if i + 1 < len(ws) and len(ws[i]) + len(ws[i + 1]) <= 9:
                chunks.append(ws[i] + " " + ws[i + 1]); i += 2
            else:
                chunks.append(ws[i]); i += 1
        L = sum(len(c) + 2 for c in chunks); x = st
        for c in chunks:
            cd = d * (len(c) + 2) / L
            out.append((c.upper(), x, x + cd)); x += cd
    return out

_mf = {}
def word_caption(canvas, words, t, y=SH * 0.66, size=92, pop=0.12):
    cur = [w for w in words if w[1] <= t < w[2]]
    if not cur:
        return
    txt, st, en = cur[0]
    k = min(1.0, (t - st) / pop)
    s = int(size * (0.82 + 0.18 * (1 - (1 - k) ** 3)))
    if s not in _mf:
        f = ImageFont.truetype(MONT, s); f.set_variation_by_name("Black"); _mf[s] = f
    f = _mf[s]
    d = ImageDraw.Draw(canvas); sw = max(6, s // 11)
    while d.textbbox((0, 0), txt, font=f, stroke_width=sw)[2] > 860 and s > 50:
        s -= 6; f = ImageFont.truetype(MONT, s); f.set_variation_by_name("Black")
    bb = d.textbbox((0, 0), txt, font=f, stroke_width=sw)
    col = (255, 255, 255)
    if "$" in txt:
        col = TEAL if any(c.isdigit() for c in txt) and t > 0 else AMBER
    d.text(((SW - (bb[2] - bb[0])) / 2 - bb[0], y - (bb[3] - bb[1]) / 2 - bb[1]), txt, font=f,
           fill=col, stroke_width=sw, stroke_fill=(0, 0, 0))

BGV = None
def vframe(t, clips, title, words, total):
    global BGV
    if BGV is None:
        import common
        oW, oH = common.W, common.H
        common.W, common.H = SW, SH
        BGV = common.gradient_bg(NAVY2, NAVY)
        common.W, common.H = oW, oH
    c = BGV.copy()
    # which clip?
    cl = clips[0]
    for x in clips:
        if t >= x[2] - GAP:
            cl = x
    bi, si, st, d, ost, _ = cl
    ot = ost + clamp01((t - st) / max(d, 0.01)) * (V.TIM[bi]["sents"][si]["end"] - ost) if t >= st else ost
    sc = V.SCENES[V.TIM[bi]["name"]](ot, V.B(bi)).convert("RGB")
    sc = sc.resize((SW, int(SW * 1080 / 1920)), Image.LANCZOS)
    y0 = 560
    c.paste(sc, (0, y0))
    d_ = ImageDraw.Draw(c)
    d_.rectangle((0, y0 - 6, SW, y0), fill=AMBER + (255,)); d_.rectangle((0, y0 + sc.height, SW, y0 + sc.height + 6), fill=AMBER + (255,))
    for i, line in enumerate(title):
        spr = V.T(line, 104, AMBER if i else CREAM, "A", 10 if i else 0)
        paste_center(c, spr, SW / 2, 250 + i * 125)
    word_caption(c, words, t)
    paste_center(c, V.T("Not financial advice · S&P 500 data: R. Shiller", 26, CREAM, "D"), SW / 2, 1560, 0.55)
    paste_center(c, V.T("FULL VIDEO ON THE CHANNEL", 40, TEAL, "D"), SW / 2, 1490, clamp01((t - (total - 4)) / 0.3))
    if t < 0.2:
        c = fade(c, 1 - t / 0.2, NAVY)
    return fade(c, clamp01((t - (total - 0.4)) / 0.4), NAVY)

def render_short(idx):
    name, title, segs = SHORTS[idx]
    clips, total = build_timeline(segs)
    words = words_of(clips)
    out = os.path.join(HERE, "build", name)
    # audio
    vo = np.zeros(int(total * SR), np.int16)
    for _, _, st, d, _, a in clips:
        i0 = int(st * SR); vo[i0:i0 + len(a)] = a[:len(vo) - i0]
    with wave.open(out + "_vo.wav", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(vo.tobytes())
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{SW}x{SH}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                          "-pix_fmt", "yuv420p", out + "_v.mp4"], stdin=subprocess.PIPE)
    for n in range(int(total * FPS)):
        p.stdin.write(vframe(n / FPS, clips, title, words, total).convert("RGB").tobytes())
    p.stdin.close(); p.wait()
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", out + "_v.mp4", "-i", out + "_vo.wav", "-i",
                    os.path.join(HERE, "build", "music.wav"), "-filter_complex",
                    f"[1:a]aresample=44100,pan=stereo|c0=c0|c1=c0,apad,asplit=2[vo][sc];[2:a]atrim=60:{60 + total},asetpts=PTS-STARTPTS,volume=0.35[bed];[bed][sc]sidechaincompress=threshold=0.04:ratio=5:attack=30:release=400[duck];[duck][vo]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{total:.2f}",
                    os.path.join(HERE, f"Short_{idx + 1}_{name.split('_')[1]}.mp4")], check=True)
    return name, round(total, 1)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ims = []
        for i, (name, title, segs) in enumerate(SHORTS):
            clips, total = build_timeline(segs); words = words_of(clips)
            print(name, round(total, 1))
            for q in (0.05, 0.5, 0.97):
                ims.append(vframe(total * q, clips, title, words, total).convert("RGB").resize((270, 480)))
        sh = Image.new("RGB", (270 * 9, 480))
        for i, im in enumerate(ims):
            sh.paste(im, (i * 270, 0))
        sh.save(os.path.join(HERE, "build", "shorts_contact.png")); sys.exit()
    from multiprocessing import Pool
    with Pool(3) as pl:
        print(pl.map(render_short, range(3)))
