#!/usr/bin/env python3
"""Ріже одну суцільну озвучку на репліки сцен (по паузах між словами).

    python3 scripts/split_voiceover.py <voiceover.mp3> <project.json> [<out_dir>]

Бере "line" кожної сцени з project.json (сцени без line пропускає), розпізнає слова у
файлі (faster-whisper), вирівнює їх із текстом і ріже посередині паузи між репліками.
Записує <out_dir>/<scene_id>.wav і проставляє в project.json "audio": "file", "audio_file".
"""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ugc_build import align, duration, run, to_wav, tokens, transcribe_words  # noqa: E402


def main(vo, cfg_path, out_dir=None):
    cfg_path = Path(cfg_path).resolve()
    P = cfg_path.parent
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    out = Path(out_dir) if out_dir else P / "audio" / "vo_lines"
    out.mkdir(parents=True, exist_ok=True)
    full = out / "_full.wav"
    to_wav(vo, full)
    total = duration(full)
    scenes = [s for s in cfg["scenes"] if s.get("line")]
    text = " ".join(s["line"] for s in scenes)
    words = align(text, transcribe_words(full), total)
    # межі реплік за кількістю слів
    idx, bounds = 0, []
    for s in scenes:
        n = len(tokens(s["line"]))
        bounds.append((idx, idx + n - 1)); idx += n
    cuts = [0.0]
    for (a1, b1), (a2, _) in zip(bounds, bounds[1:]):
        cuts.append((words[b1]["e"] + words[a2]["s"]) / 2)
    cuts.append(total)
    for s, st, en in zip(scenes, cuts, cuts[1:]):
        f = out / f"{s['id']}.wav"
        run(["ffmpeg", "-y", "-v", "error", "-i", str(full), "-ss", f"{st:.3f}", "-to", f"{en:.3f}",
             "-af", "silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
                    "silenceremove=start_periods=1:start_threshold=-45dB,areverse",
             "-c:a", "pcm_s16le", str(f)])
        s["audio"] = "file"
        s["audio_file"] = str(f.relative_to(P)) if f.is_relative_to(P) else str(f)
        print(f"  {s['id']}: {st:6.2f}–{en:6.2f}s  {s['line']}")
    cfg_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    main(*sys.argv[1:4])
