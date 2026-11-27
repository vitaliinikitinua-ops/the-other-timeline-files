#!/usr/bin/env python3
"""UGC_CREATOR — автоматичний монтаж вертикальних UGC-відео (1080x1920, H.264).

Використання:
    python3 scripts/ugc_build.py projects/product_001/project.json

Що робить:
  1. Для кожної сцени готує звук: озвучка Piper (безкоштовно, офлайн), готовий аудіофайл
     (напр. ElevenLabs) або живий звук із кліпу (її власний голос).
  2. Розпізнає слова (faster-whisper) і вирівнює їх з текстом сценарію — субтитри з точним
     таймінгом і правильним написанням.
  3. Рендерить візуал сцени: відео-кліп (обрізка/кадрування 9:16), фото з плавним рухом
     камери або картку продукту з оригінального фото.
  4. Склеює, накладає субтитри + текстові плашки, музику з приглушенням під голос,
     нормалізує гучність (-14 LUFS) і експортує MP4 H.264, мініатюру, SRT і QC-звіт.
"""
import difflib, json, math, os, re, subprocess, sys, wave
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
W, H, FPS = 1080, 1920, 30
FONT_FILE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_NAME = "DejaVu Sans"
PIPER_DEFAULT = ROOT / "models/piper/uk_UA-tetiana-high.onnx"


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(map(str, cmd))}\n{r.stderr[-2000:]}")
    return r.stdout


def duration(path):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                      "-of", "csv=p=0", str(path)]).strip())


# ---------------------------------------------------------------- audio

def tts_piper(text, out_wav, model=PIPER_DEFAULT, length_scale=0.95, speaker=None):
    cmd = [sys.executable, "-m", "piper", "-m", str(model), "-f", str(out_wav),
           "--length-scale", str(length_scale), "--sentence-silence", "0.12"]
    if speaker is not None:
        cmd += ["-s", str(speaker)]
    r = subprocess.run(cmd, input=text, capture_output=True, text=True)
    if r.returncode != 0 or not Path(out_wav).exists():
        raise RuntimeError("Piper TTS failed: " + r.stderr[-1500:])


def to_wav(src, out_wav, start=None, dur=None):
    cmd = ["ffmpeg", "-y", "-v", "error"]
    if start is not None:
        cmd += ["-ss", f"{start:.3f}"]
    cmd += ["-i", str(src)]
    if dur is not None:
        cmd += ["-t", f"{dur:.3f}"]
    cmd += ["-vn", "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le", str(out_wav)]
    run(cmd)


def silence(out_wav, dur):
    run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono",
         "-t", f"{dur:.3f}", "-c:a", "pcm_s16le", str(out_wav)])


def fit_audio(src_wav, out_wav, dur, offset=0.0):
    """Розміщує src з затримкою offset у вікні тривалістю dur."""
    ms = int(offset * 1000)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(src_wav), "-af",
         f"adelay={ms}:all=1,apad,atrim=0:{dur:.3f}", "-ar", "48000", "-ac", "1",
         "-c:a", "pcm_s16le", str(out_wav)])


_whisper = None


def transcribe_words(wav):
    """Слова з таймінгами (faster-whisper, CPU)."""
    global _whisper
    import numpy as np
    from faster_whisper import WhisperModel
    if _whisper is None:
        _whisper = WhisperModel(os.environ.get("UGC_WHISPER", "small"), device="cpu",
                                compute_type="int8")
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(wav), "-f", "s16le", "-ac", "1",
                          "-ar", "16000", "-"], capture_output=True).stdout
    audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    segs, _ = _whisper.transcribe(audio, language="uk", word_timestamps=True)
    words = []
    for s in segs:
        for w in s.words or []:
            if w.word.strip():
                words.append({"w": w.word.strip(), "s": w.start, "e": w.end})
    return words


def norm(w):
    return re.sub(r"[^\wʼ']", "", w.lower()).replace("ʼ", "'")


def align(script_text, heard, total_dur, offset=0.0):
    """Ставить слова СЦЕНАРІЮ на таймінги РОЗПІЗНАНИХ слів (правильний правопис + точний час)."""
    sw = script_text.split()
    if not sw:
        return []
    if not heard:  # рівномірний розподіл
        step = total_dur / len(sw)
        return [{"w": w, "s": offset + i * step, "e": offset + (i + 1) * step} for i, w in enumerate(sw)]
    a = [norm(w) for w in sw]
    b = [norm(w["w"]) for w in heard]
    times = [None] * len(sw)
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal" or (tag == "replace"):
            n, m = i2 - i1, j2 - j1
            if m == 0:
                continue
            for k in range(n):
                jk = j1 + min(m - 1, int(k * m / n))
                times[i1 + k] = (heard[jk]["s"], heard[jk]["e"])
    # інтерполяція пропусків
    first_s = heard[0]["s"]
    last_e = heard[-1]["e"]
    i = 0
    while i < len(sw):
        if times[i] is None:
            j = i
            while j < len(sw) and times[j] is None:
                j += 1
            t0 = times[i - 1][1] if i > 0 else first_s
            t1 = times[j][0] if j < len(sw) else last_e
            step = max(0.05, (t1 - t0) / (j - i))
            for k in range(i, j):
                times[k] = (t0 + (k - i) * step, t0 + (k - i + 1) * step)
            i = j
        else:
            i += 1
    return [{"w": w, "s": offset + t[0], "e": offset + t[1]} for w, t in zip(sw, times)]


# ---------------------------------------------------------------- visuals

def cover(img, w=W, h=H, focus_y=0.4):
    img = ImageOps.exif_transpose(img).convert("RGB")
    sc = max(w / img.width, h / img.height)
    img = img.resize((math.ceil(img.width * sc), math.ceil(img.height * sc)), Image.LANCZOS)
    x = (img.width - w) // 2
    y = int(max(0, min(img.height - h, (img.height - h) * focus_y)))
    return img.crop((x, y, x + w, y + h))


def product_card(src, out_png, bg=(247, 214, 222)):
    """Картка продукту з ОРИГІНАЛЬНОГО фото: етикетка не змінюється."""
    prod = Image.open(src).convert("RGB")
    # прибрати білий фон -> альфа
    import numpy as np
    arr = np.array(prod.convert("RGBA"))
    white = (arr[..., :3] > 238).all(axis=-1)
    arr[..., 3] = np.where(white, 0, 255)
    px = Image.fromarray(arr, "RGBA")
    bbox = px.getbbox()
    px = px.crop(bbox)
    canvas = Image.new("RGB", (W, H), bg)
    # м'який градієнт
    grad = Image.linear_gradient("L").resize((W, H))
    canvas = Image.composite(Image.new("RGB", (W, H), (255, 240, 244)), canvas, grad)
    target_h = int(H * 0.45)
    sc = target_h / px.height
    px = px.resize((int(px.width * sc), target_h), Image.LANCZOS)
    x, y = (W - px.width) // 2, int(H * 0.22)
    shadow = Image.new("RGBA", (px.width + 80, px.height + 80), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse((40, px.height + 10, px.width + 40, px.height + 70), fill=(120, 40, 60, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(22))
    canvas.paste(shadow, (x - 40, y - 40), shadow)
    canvas.paste(px, (x, y), px)
    canvas.save(out_png)


def photo_card(src, out_png, focus_y=0.35):
    cover(Image.open(src), focus_y=focus_y).save(out_png)


def render_still(png, out_mp4, dur, move="in"):
    frames = max(1, round(dur * FPS))
    z = {"in": "1+0.10*on/{n}", "out": "1.10-0.10*on/{n}"}.get(move, "1+0.10*on/{n}").format(n=frames)
    # зум на збільшеному зображенні = плавно, без тремтіння
    vf = (f"scale={W*2}:{H*2},zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
          f":d={frames}:s={W}x{H}:fps={FPS},format=yuv420p,setsar=1")
    run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(png), "-vf", vf, "-frames:v",
         str(frames), "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-an", str(out_mp4)])


def render_clip(src, out_mp4, start, dur, focus="center", speed=1.0):
    loop = ["-stream_loop", "-1"] if duration(src) - start < dur * speed - 0.05 else []
    y = {"top": "0", "center": "(ih-oh)/2", "bottom": "ih-oh"}.get(focus, "(ih-oh)/2")
    vf = (f"setpts=PTS/{speed},scale={W}:{H}:force_original_aspect_ratio=increase,"
          f"crop={W}:{H}:(iw-ow)/2:{y},fps={FPS},format=yuv420p,setsar=1")
    run(["ffmpeg", "-y", "-v", "error", *loop, "-ss", f"{start:.3f}", "-i", str(src), "-t",
         f"{dur:.3f}", "-vf", vf, "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-an",
         str(out_mp4)])


# ---------------------------------------------------------------- subtitles

def ass_time(t):
    t = max(0, t)
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def srt_time(t):
    ms = int(round(t * 1000))
    return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"


def chunk_words(words, max_words=3, max_chars=18):
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        text = " ".join(x["w"] for x in cur)
        if len(cur) >= max_words or len(text) >= max_chars or re.search(r"[.!?,:;—]$", w["w"]):
            chunks.append(cur); cur = []
    if cur:
        chunks.append(cur)
    return chunks


def esc(t):
    return t.replace("\\", "\\\\").replace("{", "(").replace("}", ")")


def build_ass(words, overlays, out_ass, style):
    hl = style.get("highlight", "&H0000E5FF")  # жовтий (ASS = BGR)
    size = style.get("size", 74)
    margin = style.get("margin_v", 600)
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,{FONT_NAME},{size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,7,2,2,90,90,{margin},1
Style: Top,{FONT_NAME},66,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,6,2,8,80,80,190,1
Style: Badge,{FONT_NAME},60,&H00FFFFFF,&H00FFFFFF,&H006A2BD6,&H006A2BD6,1,0,0,0,100,100,0,0,3,18,0,8,80,80,330,1
Style: Cta,{FONT_NAME},64,&H00FFFFFF,&H00FFFFFF,&H006A2BD6,&H006A2BD6,1,0,0,0,100,100,0,0,3,20,0,2,80,80,260,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    for ch in chunk_words(words):
        for i, w in enumerate(ch):
            st = w["s"]
            en = ch[i + 1]["s"] if i + 1 < len(ch) else max(w["e"], w["s"] + 0.25)
            parts = []
            for j, x in enumerate(ch):
                t = esc(x["w"])
                parts.append(f"{{\\c{hl}}}{t}{{\\c&H00FFFFFF&}}" if j == i else t)
            pop = "{\\fscx88\\fscy88\\t(0,90,\\fscx100\\fscy100)}" if i == 0 else ""
            lines.append(f"Dialogue: 1,{ass_time(st)},{ass_time(en)},Sub,,0,0,0,,{pop}{' '.join(parts)}")
    for o in overlays:
        st_name = {"top": "Top", "badge": "Badge", "cta": "Cta"}.get(o.get("style", "top"), "Top")
        txt = esc(o["text"]).replace("\n", "\\N")
        fx = "{\\fad(120,120)\\fscx92\\fscy92\\t(0,120,\\fscx100\\fscy100)}"
        lines.append(f"Dialogue: 2,{ass_time(o['start'])},{ass_time(o['end'])},{st_name},,0,0,0,,{fx}{txt}")
    Path(out_ass).write_text(head + "\n".join(lines) + "\n", encoding="utf-8")


def build_srt(words, out_srt):
    out = []
    for n, ch in enumerate(chunk_words(words, 6, 40), 1):
        out.append(f"{n}\n{srt_time(ch[0]['s'])} --> {srt_time(ch[-1]['e'])}\n{' '.join(w['w'] for w in ch)}\n")
    Path(out_srt).write_text("\n".join(out), encoding="utf-8")


# ---------------------------------------------------------------- thumbnail

def thumbnail(frame_png, text, out_jpg):
    img = Image.open(frame_png).convert("RGB")
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_FILE, 96)
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if d.textlength(test, font=font) > W - 160:
            lines.append(cur); cur = w
        else:
            cur = test
    lines.append(cur)
    y = 260
    for ln in lines:
        tw = d.textlength(ln, font=font)
        x = (W - tw) / 2
        d.rounded_rectangle((x - 30, y - 14, x + tw + 30, y + 112), 24, fill=(214, 43, 106))
        d.text((x, y), ln, font=font, fill="white")
        y += 140
    img.save(out_jpg, quality=92)


# ---------------------------------------------------------------- QC

def qc(final_mp4, cfg, words, out_json, out_md):
    info = json.loads(run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json",
                           str(final_mp4)]))
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    dur = float(info["format"]["duration"])
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(final_mp4), "-af", "ebur128=peak=true",
                        "-f", "null", "-"], capture_output=True, text=True).stderr
    lufs = re.findall(r"I:\s+(-?[\d.]+) LUFS", r)
    peak = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)
    tmin, tmax = cfg.get("target_duration", [30, 40])
    checks = {
        "Роздільна здатність 1080x1920": (v["width"], v["height"]) == (W, H),
        "Кодек H.264": v["codec_name"] == "h264",
        "Піксельний формат yuv420p": v.get("pix_fmt") == "yuv420p",
        "30 fps": v.get("r_frame_rate") in ("30/1", "30000/1000"),
        "Аудіо AAC": bool(a) and a["codec_name"] == "aac",
        f"Тривалість {tmin}–{tmax} с": tmin <= dur <= tmax + 0.5,
        "Гучність -16…-12 LUFS": bool(lufs) and -16 <= float(lufs[-1]) <= -12,
        "Пік ≤ -1 dBFS": bool(peak) and float(peak[-1]) <= -0.9,
        "Субтитри є": len(words) > 0,
    }
    res = {"file": str(final_mp4), "duration": round(dur, 2),
           "lufs": float(lufs[-1]) if lufs else None, "true_peak": float(peak[-1]) if peak else None,
           "checks": checks, "manual_checks": [
               "Обличчя/руки природні (реальна зйомка — так)",
               "Продукт і етикетка точні (картка з оригінального фото)",
               "Немає заборонених тверджень (див. research/product_facts.md)",
               "Субтитри: правопис звірено зі сценарієм"]}
    Path(out_json).write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    md = [f"# QC-звіт: {Path(final_mp4).name}", "", f"- Тривалість: {dur:.2f} с",
          f"- Гучність: {res['lufs']} LUFS, пік {res['true_peak']} dBFS", ""]
    md += [f"- {'✅' if ok else '❌'} {k}" for k, ok in checks.items()]
    md += ["", "## Ручна перевірка", *[f"- [ ] {m}" for m in res["manual_checks"]]]
    Path(out_md).write_text("\n".join(md) + "\n", encoding="utf-8")
    return res


# ---------------------------------------------------------------- main

def build(cfg_path):
    cfg_path = Path(cfg_path).resolve()
    P = cfg_path.parent
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    name = cfg.get("name", "video")
    d_audio, d_scenes, d_sub, d_ren, d_fin, d_img = (P / x for x in
        ("audio", "scenes", "subtitles", "renders", "final", "images"))
    for d in (d_audio, d_scenes, d_sub, d_ren, d_fin, d_img):
        d.mkdir(parents=True, exist_ok=True)
    rp = lambda p: (P / p).resolve() if not Path(p).is_absolute() else Path(p)
    voice = cfg.get("voice", {})

    t = 0.0
    all_words, overlays, scene_mp4s, scene_wavs, starts = [], [], [], [], []
    for sc in cfg["scenes"]:
        sid = sc["id"]
        vis = sc["visual"]
        lead = sc.get("lead", 0.15)
        tail = sc.get("tail", 0.25)
        audio_mode = sc.get("audio", voice.get("mode", "tts"))
        line = sc.get("line", "")
        raw = d_audio / f"{sid}_raw.wav"
        if audio_mode == "tts" and line:
            tts_piper(line, raw, rp(voice.get("model", PIPER_DEFAULT)),
                      voice.get("length_scale", 0.95), voice.get("speaker"))
        elif audio_mode == "file":
            to_wav(rp(sc["audio_file"]), raw)
        elif audio_mode == "clip":
            cs = vis.get("in", 0.0)
            cd = vis.get("dur") or (duration(rp(vis["src"])) - cs)
            to_wav(rp(vis["src"]), raw, cs, cd)
            lead, tail = 0.0, 0.0
        else:
            raw = None
        a_dur = duration(raw) if raw else 0.0
        dur = max(sc.get("min_dur", 1.5), lead + a_dur + tail)
        if sc.get("dur"):
            dur = sc["dur"]
        if audio_mode == "clip" and vis.get("dur"):
            dur = vis["dur"]
        # звук сцени
        wav = d_audio / f"{sid}.wav"
        if raw:
            fit_audio(raw, wav, dur, lead)
        else:
            silence(wav, dur)
        # слова для субтитрів
        if line and raw and sc.get("subtitles", True):
            heard = transcribe_words(raw)
            all_words += align(line, heard, a_dur, t + lead)
        # візуал
        out = d_scenes / f"{sid}.mp4"
        kind = vis["type"]
        if kind == "video":
            render_clip(rp(vis["src"]), out, vis.get("in", 0.0), dur, vis.get("focus", "center"),
                        vis.get("speed", 1.0))
        elif kind in ("photo", "product"):
            png = d_img / f"{sid}.png"
            if kind == "product":
                product_card(rp(vis["src"]), png)
            else:
                photo_card(rp(vis["src"]), png, vis.get("focus_y", 0.35))
            render_still(png, out, dur, vis.get("move", "in"))
        else:
            raise ValueError(f"Невідомий тип візуалу: {kind}")
        for o in sc.get("overlays", []):
            overlays.append({**o, "start": t + o.get("at", 0.0),
                             "end": t + min(dur, o.get("until", dur))})
        starts.append(t)
        scene_mp4s.append(out); scene_wavs.append(wav)
        print(f"  [{sid}] {kind:<7} {dur:5.2f}s  {line[:60]}")
        t += dur

    # склейка відео / голосу
    lst = d_ren / "concat.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in scene_mp4s))
    silent = d_ren / "video_silent.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy",
         str(silent)])
    alst = d_ren / "concat_audio.txt"
    alst.write_text("".join(f"file '{p}'\n" for p in scene_wavs))
    vo = d_ren / "voice.wav"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(alst),
         "-c:a", "pcm_s16le", str(vo)])

    # субтитри
    ass = d_sub / f"{name}.ass"
    build_ass(all_words, overlays, ass, cfg.get("subtitle_style", {}))
    build_srt(all_words, d_sub / f"{name}.srt")
    (d_sub / f"{name}_words.json").write_text(json.dumps(all_words, ensure_ascii=False, indent=1),
                                              encoding="utf-8")

    # звук: голос + музика з дакінгом + нормалізація
    music = cfg.get("music") or {}
    inputs = ["-i", str(silent), "-i", str(vo)]
    if music.get("file"):
        inputs += ["-stream_loop", "-1", "-i", str(rp(music["file"]))]
        vol = music.get("volume_db", -18)
        af = (f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit=2[v1][v2];"
              f"[2:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={vol}dB[m];"
              f"[m][v2]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300[md];"
              f"[v1][md]amix=inputs=2:duration=first:normalize=0,"
              f"loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    else:
        af = "[1:a]aformat=sample_rates=48000:channel_layouts=stereo,loudnorm=I=-14:TP=-1.5:LRA=11[a]"
    fontsdir = str(Path(FONT_FILE).parent)
    vf = f"[0:v]subtitles='{ass}':fontsdir='{fontsdir}'[v]"
    final = d_fin / f"{name}.mp4"
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", f"{vf};{af}",
         "-map", "[v]", "-map", "[a]", "-t", f"{t:.3f}",
         "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-profile:v", "high", "-level", "4.1",
         "-pix_fmt", "yuv420p", "-r", str(FPS), "-g", str(FPS * 2),
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(final)])

    # мініатюра
    th = cfg.get("thumbnail", {})
    ts = th.get("scene")
    tt = (starts[[s["id"] for s in cfg["scenes"]].index(ts)] if ts else 0) + th.get("offset", 0.5)
    fr = d_ren / "thumb_frame.png"
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{tt:.2f}", "-i", str(silent), "-frames:v", "1",
         str(fr)])
    thumbnail(fr, th.get("text", ""), d_fin / f"{name}_thumbnail.jpg")

    res = qc(final, cfg, all_words, d_fin / f"{name}_qc.json", d_fin / f"{name}_qc.md")
    print(f"\nГОТОВО: {final}  ({res['duration']} с, {res['lufs']} LUFS)")
    for k, ok in res["checks"].items():
        print(f"  {'OK ' if ok else 'ERR'} {k}")
    return final


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    build(sys.argv[1])
