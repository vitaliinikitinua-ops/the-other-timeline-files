#!/usr/bin/env python3
"""«Цифровий двійник»: перемальовує губи на її СПРАВЖНЬОМУ відео під новий голос (Wav2Lip, CPU, $0).

    python3 scripts/lipdub.py <her_talking_video.mp4> <new_voice.wav|mp3> <out.mp4>

- Якщо аудіо довше за відео, кадри відео повторюються (краще брати базовий кліп ≥ довжини репліки).
- Швидкість на CPU: ~2 хв на 1 с відео 1080x1920 (найдовше — пошук обличчя).
- Пам'ять: face_det_batch_size=2 (16 → OOM на 15 ГБ RAM).
Встановлення: tools/wav2lip (github.com/Rudrabha/Wav2Lip) + checkpoints/wav2lip_gan.pth,
face_detection/detection/sfd/s3fd.pth (huggingface.co/camenduru/Wav2Lip); Python — venv SadTalker;
патч audio.py: librosa.filters.mel(sr=..., n_fft=...).
"""
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
W2L = ROOT / "tools/wav2lip"
PY = ROOT / "tools/sadtalker/.venv/bin/python"


def main(video, audio, out):
    video, audio, out = (Path(p).resolve() for p in (video, audio, out))
    out.parent.mkdir(parents=True, exist_ok=True)
    (W2L / "temp").mkdir(exist_ok=True)
    tmp = out.with_name(out.stem + "_w2l.mp4")
    subprocess.run([str(PY), "inference.py", "--checkpoint_path", "checkpoints/wav2lip_gan.pth",
                    "--face", str(video), "--audio", str(audio), "--outfile", str(tmp),
                    "--pads", "0", "15", "0", "0", "--face_det_batch_size", "2",
                    "--wav2lip_batch_size", "32", "--nosmooth"], cwd=W2L, check=True)
    # якісне перекодування (Wav2Lip пише з низьким бітрейтом)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(tmp), "-c:v", "libx264", "-crf", "15",
                    "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", str(out)],
                   check=True)
    tmp.unlink(missing_ok=True)
    print("OK", out)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(__doc__); sys.exit(1)
    main(*sys.argv[1:])
