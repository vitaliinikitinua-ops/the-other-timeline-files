"""Add an episode (long + Short) to finance_series/QUEUE.json.  python3 queue.py ep01 2026-11-26T18:00 2026-11-27T14:00"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import build
RAW = "https://raw.githubusercontent.com/vitaliinikitinua-ops/the-other-timeline-files/claude/awesome-hopper-sx7soy/finance_series/"
Q = os.path.join(ROOT, "QUEUE.json")

def add(ep, t_long, t_short):
    m = build.load_ep(ep); timing = json.load(open(os.path.join(build.bdir(ep), "timing.json")))
    md = m.META
    desc = md["description"].strip().split("\n\n")
    desc = desc[0] + "\n\n" + build.chapters_text(m, timing) + "\n\n" + "\n\n".join(desc[1:])
    for ch in "<>":
        assert ch not in desc
    q = json.load(open(Q)) if os.path.exists(Q) else []
    q = [x for x in q if x["ep"] != ep]
    q.append(dict(ep=ep, kind="long", due_warsaw=t_long, status="pending", title=md["title"], video=RAW + f"{ep}/{md['file']}", thumbnail=RAW + f"{ep}/thumb_A.jpg",
                  description=desc, tags=md["tags"], comment=md["comment"], url=None))
    q.append(dict(ep=ep, kind="short", due_warsaw=t_short, status="pending", title=m.SHORT["yt_title"], video=RAW + f"{ep}/{md['file'].replace('.mp4', '_SHORT.mp4')}",
                  description=m.SHORT["yt_desc"] + "\nFull video: (link of the long " + ep + " video)", tags=["shorts"] + md["tags"][:8], comment=None, url=None))
    q.sort(key=lambda x: x["due_warsaw"])
    json.dump(q, open(Q, "w"), indent=1, ensure_ascii=False)
    print("queued", ep, t_long, t_short)

if __name__ == "__main__":
    add(sys.argv[1], sys.argv[2], sys.argv[3])
