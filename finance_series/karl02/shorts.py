"""Karl #02 Shorts (1080x1920) cut from the final long video: python3 shorts.py -> short1_*.mp4, short2_*.mp4
Layout (youtube-playbook): headline y 200-460, scene 1.4x zoom in the middle, 1-3 word captions y ~1450, progress bar, end card."""
import os, re, json, subprocess
from build_ep import lines, B, FINAL
HERE = os.path.dirname(os.path.abspath(__file__)); FONTS = os.path.join(HERE, "..", "..", "ep2", "fonts")
SHORTS = [dict(name="short1_button_told_the_truth", ranges=[(0, 17)], head=("THE BUTTON SAID", "\"6 HOURS OF YOUR LIFE\"")),
          dict(name="short2_minus40_cost_more", ranges=[(77, 79), (98, 103)], head=("\"-40% OFF\" COST HIM", "MORE THAN FULL PRICE"))]
END = 2.0
def ts(t): return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"
def colorize(w): return r"{\c&H3AD2FF&}" + w + r"{\c&HFFFFFF&}" if re.search(r"\b(?:\d|\$|percent|dollars?|hours?|years?|hundred|thousand|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|thirty|forty|fifty|sixty|seventy|ninety)\b|\d|\$", w, re.I) else w
def build(sh):
    TM = json.load(open(os.path.join(B, "ep_timing.json"))); L = TM["lines"]; TXT = [l for l, _ in lines()]
    segs, caps, t0 = [], [], 0.0
    for a, b in sh["ranges"]:
        s, e = L[a][0] - 0.1, L[b + 1][0] - 0.05; segs.append((s, e))
        for i in range(a, b + 1):
            words = TXT[i].replace('"', "").split(); st, en = L[i][0] - s + t0, L[i][1] - s + t0; n = max(1, (len(words) + 2) // 3)
            for k in range(n):
                chunk = words[k * 3:(k + 1) * 3]
                if chunk: caps.append((st + (en - st) * k / n, st + (en - st) * (k + 1) / n, " ".join(colorize(w) for w in chunk)))
        t0 += e - s
    dur = t0 + END
    ass = os.path.join(B, sh["name"] + ".ass")
    with open(ass, "w") as f:
        f.write("[Script Info]\nPlayResX: 1080\nPlayResY: 1920\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")
        f.write("Style: H,Anton,92,&H00FFFFFF,&H00FFFFFF,&H00140E0E,&H64000000,0,0,0,0,100,100,0,0,1,7,2,8,40,40,230,1\n")
        f.write("Style: C,Anton,104,&H00FFFFFF,&H00FFFFFF,&H00140E0E,&H64000000,0,0,0,0,100,100,0,0,1,8,3,2,60,60,420,1\n")
        f.write("Style: E,Anton,96,&H003AD2FF,&H00FFFFFF,&H00140E0E,&H64000000,0,0,0,0,100,100,0,0,1,8,3,2,60,60,380,1\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
        f.write(f"Dialogue: 0,{ts(0)},{ts(dur - END)},H,,0,0,0,,{sh['head'][0]}\\N{{\\c&H3AD2FF&}}{sh['head'][1]}\n")
        for a, b, t in caps: f.write(f"Dialogue: 0,{ts(a)},{ts(b)},C,,0,0,0,,{{\\fad(60,0)}}{t}\n")
        f.write(f"Dialogue: 0,{ts(dur - END)},{ts(dur)},E,,0,0,0,,FULL VIDEO\\NON THE CHANNEL\n")
        f.write(f"Dialogue: 0,{ts(dur - 6)},{ts(dur - END)},H,,0,0,0,,{{\\fs40\\pos(540,1830)}}Example numbers · not financial advice\n")
    sel = "+".join(f"between(t,{s:.3f},{e:.3f})" for s, e in segs)
    fc = (f"[0:v]select='{sel}',setpts=N/FRAME_RATE/TB,tpad=stop_mode=clone:stop_duration={END},split[a][b];"
          f"[a]scale=-2:1920,crop=1080:1920,boxblur=30:5,eq=brightness=-0.25[bg];[b]scale=1512:-2,crop=1080:850[fg];"
          f"[bg][fg]overlay=0:560,drawbox=x=0:y=1906:w=1080*t/{dur:.2f}:h=14:color=0xffb828:t=fill,ass={ass}:fontsdir={FONTS}[v];"
          f"[0:a]aselect='{sel}',asetpts=N/SR/TB,apad=pad_dur={END}[au]")
    out = os.path.join(HERE, sh["name"] + ".mp4")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", FINAL, "-filter_complex", fc, "-map", "[v]", "-map", "[au]", "-t", f"{dur:.2f}",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "24", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out], check=True)
    print("->", out, round(dur, 1), "s")
if __name__ == "__main__":
    for sh in SHORTS: build(sh)
