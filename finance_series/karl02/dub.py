"""Karl #02 dubbed audio tracks: python3 dub.py [es pt-BR de fr uk] -> audio/<lang>.m4a (same length as the video).
Each translated line is voiced by Piper, placed at the English line start and sped up (atempo, max x1.3) to fit
before the next English line; if still longer it pushes the next line slightly (drift is re-absorbed by later gaps)."""
import os, sys, json, subprocess, numpy as np
from build_ep import B, SR, ROOT, read_wav, do_mix
VOICES = {"es": ("es_ES-davefx-medium", []), "pt-BR": ("pt_BR-faber-medium", []), "de": ("de_DE-thorsten-high", []),
          "fr": ("fr_FR-tom-medium", []), "uk": ("uk_UA-ukrainian_tts-medium", ["--speaker", "1"])}
HERE = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(HERE, "audio"), exist_ok=True)
def trim(a): idx = np.where(np.abs(a) > 0.01)[0]; return a[max(0, idx[0] - 300): idx[-1] + 1500] if len(idx) else a
def build(lang):
    TM = json.load(open(os.path.join(B, "ep_timing.json"))); L = TM["lines"]
    lines = open(os.path.join(HERE, "dub", f"{lang}.txt"), encoding="utf-8").read().strip().split("\n"); assert len(lines) == len(L), (lang, len(lines))
    model, extra = VOICES[lang]; out = os.path.join(B, "dub", lang); os.makedirs(out, exist_ok=True)
    starts, cursor, stats = [], 0.0, []
    for i, txt in enumerate(lines):
        cache = os.path.join(out, f"{i:03d}.npy"); tfile = os.path.join(out, f"{i:03d}.txt")
        if os.path.exists(cache) and os.path.exists(tfile) and open(tfile, encoding="utf-8").read() == txt:
            a = np.load(cache); start = max(L[i][0], cursor + 0.06); starts.append(start); cursor = start + len(a) / SR; stats.append(1.0); continue
        raw = os.path.join(out, "raw.wav"); txt = txt.replace("«", "").replace("»", "").replace("„", "").replace("“", "").replace('"', "")
        subprocess.run(["piper", "--model", os.path.join(ROOT, "finance02", "voice", model + ".onnx"), "--output_file", raw, "--length_scale", "0.75" if lang == "uk" else "0.92", *extra], input=txt.encode(), check=True, capture_output=True)
        a = trim(read_wav(raw)); start = max(L[i][0], cursor + 0.06); nxt = L[i + 1][0] if i + 1 < len(L) else TM["endStart"]
        avail = max(0.5, nxt - start - 0.06); d = len(a) / SR; tempo = min(1.45 if lang == "uk" else 1.3, d / avail) if d > avail else 1.0
        if tempo > 1.0:
            tmp = os.path.join(out, "t.wav"); import wave
            with wave.open(raw, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((a * 32767).astype(np.int16).tobytes())
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", raw, "-af", f"atempo={tempo:.3f}", tmp], check=True); a = read_wav(tmp)
        np.save(cache, a); open(tfile, "w", encoding="utf-8").write(txt); starts.append(start); cursor = start + len(a) / SR; stats.append(tempo)
    json.dump(starts, open(os.path.join(out, "starts.json"), "w"))
    print(lang, "max tempo", max(stats), "lines sped up", sum(t > 1.0 for t in stats), "max drift", round(max(s - l[0] for s, l in zip(starts, L)), 2))
    wp = do_mix(lang, starts=starts)
    m4a = os.path.join(HERE, "audio", f"{lang}.m4a")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wp, "-af", "loudnorm=I=-14:TP=-1.5", "-c:a", "aac", "-b:a", "128k", m4a], check=True); print("->", m4a)
if __name__ == "__main__":
    for lang in (sys.argv[1:] or VOICES): build(lang)
