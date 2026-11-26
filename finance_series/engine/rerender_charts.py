"""Re-render only chart beats of finished episodes after the chart framing fix, then re-mix (+ Short if it uses a chart)."""
import sys, json, os
import build
from multiprocessing import Pool
eps = sys.argv[1:]
jobs = []
for ep in eps:
    m = build.load_ep(ep)
    jobs += [(ep, i) for i, b in enumerate(m.BEATS) if b[2].get("type") == "chart"]
with Pool(4) as p:
    p.map(build.render_beat, jobs)
for ep in eps:
    m = build.load_ep(ep); timing = json.load(open(os.path.join(build.bdir(ep), "timing.json")))
    build.mix(ep, m, timing)
    names = [b[0] for b in m.BEATS]
    if any(m.BEATS[names.index(n)][2].get("type") == "chart" for n, _ in m.SHORT["segs"]):
        build.make_short(ep, m, timing)
print("done", eps)
