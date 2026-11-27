"""Друкує рамку обличчя x0 y0 x1 y1 (RetinaFace, facexlib). Запускати venv SadTalker."""
import sys, cv2
from pathlib import Path
from facexlib.detection import init_detection_model
W = Path(__file__).resolve().parents[1] / "tools/sadtalker/gfpgan/weights"
det = init_detection_model("retinaface_resnet50", half=False, device="cpu", model_rootpath=str(W))
img = cv2.imread(sys.argv[1])
import torch
with torch.no_grad():
    faces = det.detect_faces(img, 0.9)
if len(faces) == 0:
    sys.exit("no face")
f = max(faces, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]))
print(*[int(v) for v in f[:4]])
