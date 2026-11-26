"""Build one episode: python3 build.py epNN [tts|stills|render|mix|short|thumbs|all]
Episode module finance_series/epNN/script.py defines BEATS, META, THUMBS, SHORT."""
import sys, os, json, subprocess, wave, importlib.util, math, random
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
from kit import *  # noqa
import scenes as SC
from PIL import ImageFont

VOICE = os.path.join(ROOT, "..", "finance02", "voice", "en_US-ryan-high.onnx")
SR = 22050
GAP_S, GAP_B, LEAD, TAIL = 0.32, 0.8, 0.25, 0.6
END_S = 15.0

def load_ep(ep):
    p = os.path.join(ROOT, ep, "script.py")
    spec = importlib.util.spec_from_file_location(ep + "_script", p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m

def bdir(ep):
    d = os.path.join(ROOT, ep, "build"); os.makedirs(d, exist_ok=True); return d

# ------------------------------------------------------------------ TTS
def tts(ep, m):
    bd = bdir(ep); os.makedirs(os.path.join(bd, "tts"), exist_ok=True)
    jobs = []
    for bi, (name, sents, sc) in enumerate(m.BEATS):
        for si, s in enumerate(sents):
            show, say = (s, None) if isinstance(s, str) else s
            p = os.path.join(bd, "tts", f"{bi:02d}_{si:02d}.wav")
            if not os.path.exists(p):
                jobs.append((say or show, p))
    from concurrent.futures import ThreadPoolExecutor
    def run(j):
        subprocess.run(["python3", "-m", "piper", "-m", VOICE, "-f", j[1], "--length-scale", str(getattr(m, "SPEED", 1.15)),
                        "--noise-scale", "0.62", "--noise-w-scale", "0.75"], input=j[0].encode(), check=True, capture_output=True)
    with ThreadPoolExecutor(3) as ex:
        list(ex.map(run, jobs))
    audio = [np.zeros(int(LEAD * SR), np.int16)]; t = LEAD; timing = []
    for bi, (name, sents, sc) in enumerate(m.BEATS):
        b0 = t; sl = []
        for si, s in enumerate(sents):
            show = s if isinstance(s, str) else s[0]
            with wave.open(os.path.join(bd, "tts", f"{bi:02d}_{si:02d}.wav")) as w:
                a = np.frombuffer(w.readframes(w.getnframes()), np.int16)
            nz = np.where(np.abs(a) > 300)[0]; a = a[max(0, nz[0] - 300): nz[-1] + 700]
            d = len(a) / SR
            sl.append({"text": show, "start": round(t, 3), "end": round(t + d, 3)})
            audio.append(a); t += d
            g = GAP_S if si < len(sents) - 1 else GAP_B
            audio.append(np.zeros(int(g * SR), np.int16)); t += g
        timing.append({"name": name, "start": round(b0, 3), "end": round(t, 3), "sents": sl})
    audio.append(np.zeros(int(TAIL * SR), np.int16)); t += TAIL; timing[-1]["end"] = round(t, 3)
    pcm = np.concatenate(audio)
    with wave.open(os.path.join(bd, "vo.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    json.dump(timing, open(os.path.join(bd, "timing.json"), "w"), indent=1)
    write_srt(os.path.join(ROOT, ep, "captions_en.srt"), timing)
    words = sum(len((s if isinstance(s, str) else s[0]).split()) for _, ss, _ in m.BEATS for s in ss)
    print(f"{ep}: narration {t:.1f}s ({t/60:.2f} min) + end {END_S}s, {words} words")
    return timing

def write_srt(path, timing, off=0.0):
    def ts(x):
        h, r = divmod(x, 3600); mm, s = divmod(r, 60)
        return f"{int(h):02d}:{int(mm):02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}"
    with open(path, "w") as f:
        n = 1
        for bk in timing:
            for s in bk["sents"]:
                f.write(f"{n}\n{ts(s['start'] + off)} --> {ts(s['end'] + off)}\n{s['text']}\n\n"); n += 1

# ------------------------------------------------------------------ frame
BAND = Image.new("RGBA", (W, 190), (0, 0, 0, 0))
for _y in range(190):
    ImageDraw.Draw(BAND).line([(0, _y), (W, _y)], fill=(5, 8, 16, int(215 * (_y / 190) ** 0.8)))
WM = None

@lru_cache(maxsize=2048)
def sub_lines(txt):
    f = font(DMS, 46, "Bold"); words = txt.split(); lines = [""]
    for w_ in words:
        tst = (lines[-1] + " " + w_).strip()
        if f.getlength(tst) > 1500 and lines[-1]:
            lines.append(w_)
        else:
            lines[-1] = tst
    out = []
    for l in lines:  # numbers in amber
        img = Image.new("RGBA", (int(f.getlength(l)) + 40, 80), (0, 0, 0, 0)); d = ImageDraw.Draw(img); x = 20
        for w_ in l.split(" "):
            col = AMBER if any(ch.isdigit() for ch in w_) else CREAM
            d.text((x + 3, 14), w_, font=f, fill=(0, 0, 0, 160)); d.text((x, 10), w_, font=f, fill=col + (255,)); x += f.getlength(w_ + " ")
        out.append(img)
    return out

def subtitles(c, t, timing):
    for bk in timing:
        if bk["start"] - 0.5 <= t <= bk["end"] + 0.5:
            for s in bk["sents"]:
                if s["start"] - 0.05 <= t <= s["end"] + 0.2:
                    c.alpha_composite(BAND, (0, H - BAND.height))
                    ls = sub_lines(s["text"]); y = H - 68 - (len(ls) - 1) * 56
                    for i, l in enumerate(ls):
                        paste_center(c, l, W / 2, y + i * 56)
                    return

def watermark(c):
    global WM
    if WM is None:
        WM = T("THE OTHER TIMELINE", 30, TEAL, "A")
    paste_center(c, WM, W - WM.width / 2 - 20, 40, 0.55)

def frame(m, timing, bi, t):
    b = SC.B(timing[bi])
    c = SC.render(t, b, m.BEATS[bi][2])
    if 0 <= t - b.t0 < 0.12 and bi > 0:
        c = fade(c, 0.5 * (1 - (t - b.t0) / 0.12), (255, 255, 255))
    subtitles(c, t, timing); watermark(c)
    return c

def render_beat(args):
    ep, bi = args
    m = load_ep(ep); timing = json.load(open(os.path.join(bdir(ep), "timing.json")))
    a = 0.0 if bi == 0 else timing[bi]["start"]; e = timing[bi]["end"]
    enc = Encoder(os.path.join(bdir(ep), f"beat_{bi:02d}.mp4"))
    for n in range(int(round(a * FPS)), int(round(e * FPS))):
        enc.write(frame(m, timing, bi, n / FPS))
    enc.close()
    return bi

def end_screen(ep, m):
    p = os.path.join(bdir(ep), "end.mp4")
    enc = Encoder(p)
    for n in range(int(END_S * FPS)):
        t = n / FPS; c = location("void").copy(); particles(c, t, 50, 91)
        pop(c, T(getattr(m, "END_LINE", "WATCH THE OTHER TIMELINE"), 70, AMBER, "A", 10), W / 2, 110, t, 0.1)
        for x in (560, 1360):
            pop(c, SC.panel_img(680, 383, CREAM), x, 440, t, 0.3)
        pop(c, SC.panel_img(260, 260, TEAL), W / 2, 830, t, 0.5)
        draw_actor(c, "you", W / 2, 925, 150, t, "happy")
        pop(c, T("SUBSCRIBE", 40, TEAL, "D"), W / 2, 995, t, 0.8)
        enc.write(fade(c, clamp01((t - (END_S - 0.6)) / 0.6)))
    enc.close()

def stills(ep, m, timing, name="contact.png"):
    ims = []
    for bi, x in enumerate(timing):
        for q in (0.3, 0.85):
            ims.append(frame(m, timing, bi, lerp(x["start"], x["end"], q)).convert("RGB").resize((384, 216)))
    sheet = Image.new("RGB", (384 * 6, 216 * ((len(ims) + 5) // 6)))
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 6) * 384, (i // 6) * 216))
    sheet.save(os.path.join(bdir(ep), name))

# ------------------------------------------------------------------ audio
def music(total, path, seed=1, bpm=88):
    """Lo-fi bed. Each note is synthesized only over its own short window (fast)."""
    SRm = 44100; N = int(SRm * total)
    out = np.zeros(N + SRm * 5, np.float32); rng = np.random.default_rng(seed)
    noise = rng.normal(0, 1, SRm * 2).astype(np.float32); hp = np.diff(noise, prepend=0).astype(np.float32)
    def add(t0, L, sig_fn, a, dcy, gain):
        i0 = int(t0 * SRm); n = int(L * SRm); x = np.arange(n, dtype=np.float32) / SRm
        e = np.minimum(1, x / max(a, 1e-3)) * np.exp(-x / dcy)
        out[i0:i0 + n] += (sig_fn(x) * e * gain).astype(np.float32)[: max(0, len(out) - i0)]
    beat = 60 / bpm
    progs = [[[220.0, 261.6, 329.6, 392.0], [174.6, 220.0, 261.6, 329.6], [130.8, 196.0, 261.6, 329.6], [196.0, 246.9, 293.7, 392.0]],
             [[146.8, 220.0, 293.7, 349.2], [116.5, 174.6, 233.1, 293.7], [174.6, 220.0, 261.6, 349.2], [130.8, 196.0, 261.6, 329.6]],
             [[164.8, 196.0, 246.9, 329.6], [130.8, 164.8, 196.0, 261.6], [146.8, 174.6, 220.0, 293.7], [123.5, 155.6, 196.0, 246.9]]]
    prog = progs[seed % 3]
    bars = int(total / (4 * beat)) + 1
    for b_ in range(bars):
        ch = prog[b_ % 4]; t0 = b_ * 4 * beat
        add(t0, 4 * beat + 1, lambda x, ch=ch: sum(np.sin(2 * np.pi * f * x) for f in ch), 0.6, 3.0, 0.022)
        for s in range(8):
            f = ch[[0, 2, 1, 3, 2, 1, 3, 2][s]] * 2
            add(t0 + s * beat / 2, 0.8, lambda x, f=f: np.sin(2 * np.pi * f * x), 0.004, 0.22, 0.03)
        add(t0, 4 * beat, lambda x, f=ch[0] / 2: np.sin(2 * np.pi * f * x), 0.02, 0.8, 0.11)
        for k in range(4):
            tk = t0 + k * beat
            if k in (0, 2):
                add(tk, 0.4, lambda x: np.sin(2 * np.pi * np.cumsum(48 + 60 * np.exp(-x * 22)) / SRm), 0.002, 0.14, 0.26)
            else:
                add(tk, 0.25, lambda x: noise[: len(x)], 0.001, 0.07, 0.045)
            add(tk + beat / 2, 0.08, lambda x: hp[: len(x)], 0.001, 0.02, 0.022)
    out = out[:N]
    tt = np.arange(N, dtype=np.float32) / SRm
    out *= np.clip(tt / 1.0, 0, 1) * np.clip((total - tt) / 2.0, 0, 1)
    out /= np.max(np.abs(out)) * 1.1
    pcm = (out * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SRm); w.writeframes(np.stack([pcm, pcm], 1).tobytes())

def mix(ep, m, timing):
    bd = bdir(ep)
    with open(os.path.join(bd, "list.txt"), "w") as f:
        for bi in range(len(timing)):
            f.write(f"file 'beat_{bi:02d}.mp4'\n")
        f.write("file 'end.mp4'\n")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(bd, "list.txt"), "-c", "copy", os.path.join(bd, "video.mp4")], check=True)
    total = timing[-1]["end"] + END_S
    music(total, os.path.join(bd, "music.wav"), seed=getattr(m, "MUSIC_SEED", 1))
    out = os.path.join(ROOT, ep, m.META["file"])
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", os.path.join(bd, "video.mp4"), "-i", os.path.join(bd, "vo.wav"), "-i", os.path.join(bd, "music.wav"),
                    "-filter_complex", "[1:a]aresample=44100,pan=stereo|c0=c0|c1=c0,apad,asplit=2[vo][sc];[2:a]volume=0.30[bed];[bed][sc]sidechaincompress=threshold=0.04:ratio=5:attack=30:release=400[duck];[duck][vo]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", out], check=True)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out], capture_output=True, text=True).stdout)
    print(f"{ep}: final {dur/60:.2f} min -> {out}")
    return out

# ------------------------------------------------------------------ thumbnails (top-channel style)
def thumbnail(spec, path):
    c = location(spec.get("loc", "street")).copy()
    ov = Image.new("RGBA", c.size, (20, 10, 50, 110)); c = Image.alpha_composite(c, ov)
    particles(c, 1.0, 60, 3, tuple(spec.get("pcol", PINK)), 160)
    for a in spec.get("actors", []):
        draw_actor(c, a["who"], a["x"], a.get("y", 1080), a.get("size", 520), 0.5, a.get("emo", "shock"), tuple(a.get("look", (0, 0))), bob=False, flip=a.get("flip", False))
    for pr in spec.get("props", []):
        spr = SC.PROP[pr["kind"]](pr)
        if pr.get("rot"):
            spr = spr.rotate(pr["rot"], expand=True, resample=Image.BICUBIC)
        g, pad = glow(spr, 18, 0.9); paste_center(c, g, pr["x"], pr["y"])
    if spec.get("line"):
        glow_line(c, *spec["line"], 0.3, tuple(spec.get("lcol", PINK)), 14)
    if spec.get("big"):
        bt = spec["big"]; spr = text_sprite(bt["text"], font(ANTON, bt.get("size", 230)), tuple(bt.get("col", AMBER)) + (255,), stroke=10, stroke_fill=(0, 0, 0), glow_r=24, glow_col=tuple(bt.get("col", AMBER)))
        paste_center(c, spr.rotate(bt.get("rot", 0), expand=True, resample=Image.BICUBIC), bt["x"], bt["y"])
    q = spec.get("quote")
    if q:
        f = ImageFont.truetype(MONT, 120); f.set_variation_by_name("Black")
        words = q.split(" "); hl = spec.get("hl", [])
        widths = [f.getlength(w_ + " ") for w_ in words]; x = W / 2 - sum(widths) / 2; d = ImageDraw.Draw(c)
        for w_, wd in zip(words, widths):
            col = (255, 214, 0) if w_.strip('".,?!') in [h.strip('".,?!') for h in hl] else (255, 255, 255)
            d.text((x, 40), w_, font=f, fill=col, stroke_width=12, stroke_fill=(0, 0, 0)); x += wd
    img = c.convert("RGB").resize((1280, 720), Image.LANCZOS)
    img.save(path, quality=90)
    img.resize((320, 180), Image.LANCZOS).save(path.replace(".jpg", "_320.png"))

# ------------------------------------------------------------------ short (9:16, hook on frame 1)
SW, SH = 1080, 1920
def make_short(ep, m, timing):
    sp = m.SHORT; bd = bdir(ep)
    clips = []; t = 0.0
    names = [b_[0] for b_ in m.BEATS]
    for bi, sis in sp["segs"]:
        bi = names.index(bi) if isinstance(bi, str) else bi
        for si in sis:
            with wave.open(os.path.join(bd, "tts", f"{bi:02d}_{si:02d}.wav")) as w:
                a = np.frombuffer(w.readframes(w.getnframes()), np.int16)
            nz = np.where(np.abs(a) > 300)[0]; a = a[max(0, nz[0] - 300): nz[-1] + 700]
            d = len(a) / SR; clips.append((bi, si, t, d, a)); t += d + 0.16
    total = t + 1.0
    words = []
    for bi, si, st, d, _ in clips:
        ws = timing[bi]["sents"][si]["text"].split(); chunks = []; i = 0
        while i < len(ws):
            if i + 1 < len(ws) and len(ws[i]) + len(ws[i + 1]) <= 9:
                chunks.append(ws[i] + " " + ws[i + 1]); i += 2
            else:
                chunks.append(ws[i]); i += 1
        L = sum(len(c_) + 2 for c_ in chunks); x = st
        for c_ in chunks:
            cd = d * (len(c_) + 2) / L; words.append((c_.upper(), x, x + cd)); x += cd
    oW, oH = common.W, common.H; common.W, common.H = SW, SH
    bg = gradient_bg(NAVY2, NAVY); common.W, common.H = oW, oH
    mf = {}
    def cap(c, t):
        cur = [w_ for w_ in words if w_[1] <= t < w_[2]]
        if not cur:
            return
        txt, st, en = cur[0]; k = min(1.0, (t - st) / 0.12); s = int(96 * (0.82 + 0.18 * (1 - (1 - k) ** 3)))
        f = mf.get(s) or ImageFont.truetype(MONT, s); f.set_variation_by_name("Black"); mf[s] = f
        d = ImageDraw.Draw(c); sw = max(6, s // 11)
        while d.textbbox((0, 0), txt, font=f, stroke_width=sw)[2] > 860 and s > 50:
            s -= 6; f = ImageFont.truetype(MONT, s); f.set_variation_by_name("Black")
        bb = d.textbbox((0, 0), txt, font=f, stroke_width=sw)
        col = (255, 214, 0) if any(ch.isdigit() for ch in txt) else (255, 255, 255)
        d.text(((SW - (bb[2] - bb[0])) / 2 - bb[0], SH * 0.665 - (bb[3] - bb[1]) / 2 - bb[1]), txt, font=f, fill=col, stroke_width=sw, stroke_fill=(0, 0, 0))
    vpath = os.path.join(bd, "short_v.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{SW}x{SH}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", vpath], stdin=subprocess.PIPE)
    hook = sp.get("hook")  # big number shown from frame 1
    for n in range(int(total * FPS)):
        t = n / FPS; c = bg.copy()
        cl = clips[0]
        for x in clips:
            if t >= x[2] - 0.16:
                cl = x
        bi, si, st, d, _ = cl
        tb = timing[bi]["sents"][si]
        ot = tb["start"] + clamp01((t - st) / max(d, 0.01)) * (tb["end"] - tb["start"])
        sc = SC.render(ot, SC.B(timing[bi]), m.BEATS[bi][2]).convert("RGB").resize((SW, int(SW * 9 / 16)), Image.LANCZOS)
        y0 = 560; c.paste(sc, (0, y0))
        dd = ImageDraw.Draw(c); dd.rectangle((0, y0 - 6, SW, y0), fill=AMBER + (255,)); dd.rectangle((0, y0 + sc.height, SW, y0 + sc.height + 6), fill=AMBER + (255,))
        for i, line in enumerate(sp["title"]):
            paste_center(c, T(line, 100, AMBER if i else CREAM, "A", 10 if i else 0), SW / 2, 215 + i * 120)
        if hook and t < hook.get("dur", 2.2):
            k = 1 + 0.06 * math.sin(t * 9)
            spr = T(hook["text"], 150, tuple(hook.get("col", GREEN)), "A", 16)
            spr = spr.resize((int(spr.width * k), int(spr.height * k)), Image.BICUBIC)
            paste_center(c, spr, SW / 2, y0 + sc.height / 2, clamp01((hook.get("dur", 2.2) - t) / 0.3))
        cap(c, t)
        paste_center(c, T("Not financial advice · real data", 26, CREAM, "D"), SW / 2, 1560, 0.55)
        paste_center(c, T("FULL VIDEO ON THE CHANNEL", 40, TEAL, "D"), SW / 2, 1490, clamp01((t - (total - 4)) / 0.3))
        p.stdin.write(c.convert("RGB").tobytes())
    p.stdin.close(); p.wait()
    vo = np.zeros(int(total * SR), np.int16)
    for _, _, st, d, a in clips:
        i0 = int(st * SR); vo[i0:i0 + len(a)] = a[:len(vo) - i0]
    with wave.open(os.path.join(bd, "short_vo.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(vo.tobytes())
    out = os.path.join(ROOT, ep, m.META["file"].replace(".mp4", "_SHORT.mp4"))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", vpath, "-i", os.path.join(bd, "short_vo.wav"), "-i", os.path.join(bd, "music.wav"), "-filter_complex",
                    f"[1:a]aresample=44100,pan=stereo|c0=c0|c1=c0,apad,asplit=2[vo][sc];[2:a]atrim=30:{30 + total},asetpts=PTS-STARTPTS,volume=0.35[bed];[bed][sc]sidechaincompress=threshold=0.04:ratio=5:attack=30:release=400[duck];[duck][vo]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{total:.2f}", out], check=True)
    print(f"{ep}: short {total:.1f}s -> {out}")

def package(ep, m, timing):
    md = m.META; lines = [f"# {md['title']}", "", f"File: `{md['file']}` · Short: `{md['file'].replace('.mp4', '_SHORT.mp4')}`", "", "## Description", md["description"].strip(), "", "Chapters:"]
    for bi, bk in enumerate(timing):
        if bk["name"] in md.get("chapters", {}):
            tt = 0 if bi == 0 else bk["start"]; lines.append(f"{int(tt // 60)}:{int(tt % 60):02d} {md['chapters'][bk['name']]}")
    lines += ["", "## Tags", ", ".join(md["tags"]), "", "## First comment", md["comment"], "", "## Short", f"Title: {m.SHORT['yt_title']}", "", m.SHORT["yt_desc"]]
    open(os.path.join(ROOT, ep, "PACKAGE.md"), "w").write("\n".join(lines) + "\n")

def chapters_text(m, timing):
    out = []
    for bi, bk in enumerate(timing):
        if bk["name"] in m.META.get("chapters", {}):
            tt = 0 if bi == 0 else bk["start"]; out.append(f"{int(tt // 60)}:{int(tt % 60):02d} {m.META['chapters'][bk['name']]}")
    return "\n".join(out)

if __name__ == "__main__":
    ep = sys.argv[1]; what = sys.argv[2] if len(sys.argv) > 2 else "all"
    m = load_ep(ep)
    if what in ("tts", "all"):
        timing = tts(ep, m)
    timing = json.load(open(os.path.join(bdir(ep), "timing.json")))
    if what in ("stills", "all"):
        stills(ep, m, timing)
    if what in ("render", "all"):
        from multiprocessing import Pool
        with Pool(4) as pl:
            pl.map(render_beat, [(ep, i) for i in range(len(timing))])
        end_screen(ep, m)
    if what in ("mix", "all"):
        mix(ep, m, timing)
    if what in ("short", "all"):
        if not os.path.exists(os.path.join(bdir(ep), "music.wav")):
            music(timing[-1]["end"] + END_S, os.path.join(bdir(ep), "music.wav"), seed=getattr(m, "MUSIC_SEED", 1))
        make_short(ep, m, timing)
    if what in ("thumbs", "all"):
        for k, spec in m.THUMBS.items():
            thumbnail(spec, os.path.join(ROOT, ep, f"thumb_{k}.jpg"))
    if what in ("package", "all"):
        package(ep, m, timing)
