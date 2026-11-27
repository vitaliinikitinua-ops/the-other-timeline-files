"""Cut vertical Shorts from a finished 3D long video.
python3 shorts3d.py epNN   (uses SHORTS in epNN/ep.py: name, head, segs=[(first sub prefix, last sub prefix), ...])
Layout: blurred full-frame background, the 16:9 scene zoomed to 1350 px wide in the middle (burned captions stay readable),
2-line hook headline from frame 1, "FULL VIDEO ON THE CHANNEL" in the last 2.5 s."""
import sys, os, json, subprocess
from epbuild import load, bdir, FS, ROOT
FONT = os.path.join(ROOT, "ep2", "fonts", "Anton-Regular.ttf")

def find(S, prefix, start=0):
    for i in range(start, len(S)):
        if S[i]["sub"].startswith(prefix): return i
    raise SystemExit(f"sentence not found: {prefix}")

def esc(s): return s.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace("%", "\\%")

def make(ep, m, sh):
    bd = bdir(ep); S = json.load(open(os.path.join(bd, "timeline.json")))["sents"]; src = os.path.join(FS, ep, m.META["file"])
    parts = []
    for a, b in sh["segs"]:
        i = find(S, a); j = find(S, b, i); parts.append((S[i]["t0"], S[j]["t1"]))
    dur = sum(e - s for s, e in parts)
    sel = "+".join(f"between(t,{s:.2f},{e:.2f})" for s, e in parts)
    l1, l2 = sh["head"]
    vf = (f"[0:v]select='{sel}',setpts=N/FRAME_RATE/TB,split[a][b];"
          f"[a]scale=-2:1920,crop=1080:1920,boxblur=24:2,eq=brightness=-0.12[bg];"
          f"[b]scale=1350:-2,crop=1080:ih[fg];[bg][fg]overlay=0:(H-h)/2+40,"
          f"drawtext=fontfile={FONT}:text='{esc(l1)}':fontsize=96:fontcolor=white:borderw=8:bordercolor=black:x=(w-tw)/2:y=250,"
          f"drawtext=fontfile={FONT}:text='{esc(l2)}':fontsize=110:fontcolor=0xffc23a:borderw=9:bordercolor=black:x=(w-tw)/2:y=370,"
          f"drawtext=fontfile={FONT}:text='FULL VIDEO ON THE CHANNEL':fontsize=64:fontcolor=white:borderw=6:bordercolor=black:x=(w-tw)/2:y=1560:enable='gte(t,{dur - 2.5:.2f})'[v]")
    af = f"[0:a]aselect='{sel}',asetpts=N/SR/TB[a]"
    out = os.path.join(FS, ep, f"{m.META['file'][:4]}_short_{sh['name']}.mp4")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", src, "-filter_complex", vf + ";" + af, "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out], check=True)
    print(f"{sh['name']}: {dur:.1f} s -> {out}")

if __name__ == "__main__":
    ep = sys.argv[1]; m = load(ep)
    for sh in m.SHORTS: make(ep, m, sh)
