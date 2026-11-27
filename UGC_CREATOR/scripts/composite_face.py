#!/usr/bin/env python3
"""Накладає ЛИШЕ анімовану ділянку обличчя з AI-кліпу на оригінальне чітке фото.

    python3 scripts/composite_face.py <still.png> <talk.mp4> <out.mp4>

Маска = пікселі, що змінюються між кадрами (губи, очі, голова), розширена й розмита
(м'які краї). Решта кадру — оригінальне фото без артефактів стиснення.
Вихід: 1080x1920, 30 fps, H.264 (crf 14), звук з talk.mp4.
"""
import subprocess, sys
import numpy as np
from PIL import Image, ImageFilter

W, H = 1080, 1920


def read_frames(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"scale={W}:{H}:flags=lanczos,fps=30",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)


def main(still, talk, out):
    base = np.asarray(Image.open(still).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.float32)
    fr = read_frames(talk)
    # рамка обличчя на чистому фото (RetinaFace у venv SadTalker)
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    bb = subprocess.run([str(root / "tools/sadtalker/.venv/bin/python"), str(root / "scripts/face_bbox.py"), still],
                        capture_output=True, text=True, check=True).stdout.split()
    x0, y0, x1, y1 = (int(v) / 4 for v in bb[-4:])  # у координатах 1/4
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 - (y1 - y0) * 0.05
    rx, ry = (x1 - x0) / 2 * 1.18, (y1 - y0) / 2 * 1.22
    yy, xx = np.mgrid[0:H // 4, 0:W // 4]
    ell = (((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2) <= 1.0
    mask = Image.fromarray((ell * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(max(3, rx * 0.18)))
    mask = np.asarray(mask.resize((W, H), Image.BILINEAR)).astype(np.float32)[..., None] / 255
    print(f"face region (full res): x {cx*4-rx*4:.0f}-{cx*4+rx*4:.0f}, y {cy*4-ry*4:.0f}-{cy*4+ry*4:.0f}")
    Image.fromarray((mask[..., 0] * 255).astype(np.uint8)).save(out.replace(".mp4", "_mask.png"))
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", "30", "-i", "-", "-i", talk, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264",
                            "-preset", "medium", "-crf", "14", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", out],
                           stdin=subprocess.PIPE)
    for f in fr:
        o = f.astype(np.float32) * mask + base * (1 - mask)
        enc.stdin.write(np.clip(o, 0, 255).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait()
    print("OK", out, len(fr), "frames")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(__doc__); sys.exit(1)
    main(*sys.argv[1:])
