"""Thumbnail C variants for YouTube Test & Compare: huge number, one big face, 2-4 words."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from build import thumbnail, ROOT, GREEN, CORAL, AMBER
C = {
    "ep01": dict(loc="void_red", quote="just say NO", hl=["NO"], actors=[dict(who="you", x=1430, y=1100, size=600, emo="money", flip=True)],
                 big=dict(text="$198,344", x=640, y=560, col=GREEN, size=230, rot=-6), pcol=GREEN),
    "ep02": dict(loc="void_red", quote="18 or 30?", hl=["18", "30?"], actors=[dict(who="you", x=1450, y=1100, size=600, emo="shock", flip=True)],
                 big=dict(text="+$190K", x=640, y=560, col=GREEN, size=270, rot=-6), pcol=GREEN),
    "ep03": dict(loc="void_red", quote="the minimum trap", hl=["minimum"], actors=[dict(who="you", x=1450, y=1100, size=600, emo="shock", flip=True)],
                 big=dict(text="19 YEARS", x=640, y=560, col=CORAL, size=240, rot=-6), pcol=CORAL),
}
for ep, spec in C.items():
    d = os.path.join(ROOT, ep, "tests"); os.makedirs(d, exist_ok=True)
    thumbnail(spec, os.path.join(d, "thumb_C.jpg")); print("ok", ep)
