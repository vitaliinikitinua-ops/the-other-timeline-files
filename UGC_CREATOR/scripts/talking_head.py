#!/usr/bin/env python3
"""Оживлення фото під аудіо (SadTalker, CPU, безкоштовно, офлайн).

Запуск — інтерпретатором ізольованого середовища SadTalker:
    tools/sadtalker/.venv/bin/python scripts/talking_head.py <image.png> <audio.wav> <out.mp4> [--size 256] [--no-enhance]

Режим: preprocess=full + still → анімується лише обличчя (губи, очі, легкі рухи голови),
тіло й фон лишаються з оригінального фото, тож обличчя — справжнє обличчя моделі.
Результат має ту саму роздільність, що й вхідне фото (готуйте 1080x1920).
"""
import argparse, os, shutil, sys, tempfile
from pathlib import Path

ST = Path(__file__).resolve().parents[1] / "tools" / "sadtalker"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image"); ap.add_argument("audio"); ap.add_argument("out")
    ap.add_argument("--size", type=int, default=256)
    ap.add_argument("--no-enhance", action="store_true")
    ap.add_argument("--exp-scale", type=float, default=1.0)
    ap.add_argument("--pose-style", type=int, default=0)
    a = ap.parse_args()
    img, aud, out = (Path(p).resolve() for p in (a.image, a.audio, a.out))
    os.chdir(ST)
    sys.path.insert(0, str(ST))
    from src.gradio_demo import SadTalker
    tmp = Path(tempfile.mkdtemp(prefix="st_"))
    si, sa = tmp / img.name, tmp / aud.name
    shutil.copy(img, si); shutil.copy(aud, sa)  # SadTalker переміщує вхідні файли
    st = SadTalker(checkpoint_path="checkpoints", config_path="src/config", lazy_load=True)
    res = st.test(str(si), str(sa), preprocess="full", still_mode=True,
                  use_enhancer=not a.no_enhance, batch_size=1, size=a.size,
                  pose_style=a.pose_style, exp_scale=a.exp_scale, result_dir=str(tmp / "res"))
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(res, out)
    print("OK", out)


if __name__ == "__main__":
    main()
