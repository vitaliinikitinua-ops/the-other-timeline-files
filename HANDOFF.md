# HANDOFF — state of The Other Timeline work (28.11.2026)
Read this first in a new session, then the skills it names. Branch: `claude/awesome-hopper-sx7soy`. Answer the user in Ukrainian.

## Standing user decisions (all also written into the skills)
- Hero = **Karl** (cast key `you` in engine3d/cast.js; in the new style Karl = turquoise hoodie #2EC4B6, NO cap (removed by the user 28.11);
  some videos use a RED hoodie as an A/B test -> log which in VIDEOS.md, compare CTR/retention after 7 days).
- Round all money on screen and in VO; exact values stay in BRIEF/description method.
- 1 long video + **1-2 Shorts** (2 only if the topic is broad with many hooks), short, always link to the full video.
- New format = viral "What If You...?" style learned from channel IFNation (skill `youtube-skill-1`), adapted in
  `karl-2d-template` (name is historical: the look is **3D toon**, see below). Topics 50/50 money / general life.
  9-11 min, ~190 wpm deadpan 2nd-person narration (Piper en_US-ryan-high, speed ~1.1), 3 videos/week.
  Cast: Mom, Dad, sister Mia, Grandma Rose, best friend Max, crush Lena; redraw old cast.js roles 1-3 at a time when needed.
  Formula: cold open -> premise by 0:45 -> "At first, it's amazing" -> "Then it gets bigger" -> "But..." turn via family/Max
  -> public climax where the power becomes good -> mirror ending + 1 money rule -> "So would you want ...?". 1-3 real
  facts with sources (YMYL rules: computed numbers, "example" labels, not financial advice).
  Power effect per video + our signature RECEIPT/counter. Thumbnails: channel recipe (Karl foreground shocked, power as a
  glowing line, one lowercase quote with one yellow word), rendered in our engine, A/B/C.
- Languages: English + 5 dubbed audio tracks (es, pt-BR, de, fr, uk) made with Piper, fitted to EN timing; the user
  uploads them in YouTube Studio -> Languages (no API). Fallback: YouTube auto-dubbing.
- User publishes longs at 18:00 Warsaw; Shorts go to SHORTS_QUEUE.json.

## Engines
- `finance_series/engine3d/toon/` = **current look** (three.js MeshToon + outlines + glossy black heads). `toon.js` (cast,
  extras, sets kitchen/cafeteria/gym/void), `toon_sheet.html`, `toon_demo.html`, `trailer.html`, `rtoon.js` (renders via
  Playwright routing, no server), `trailer.py`. Known TODO: depth-of-field, smoother gestures, more sets
  (street, store, bank, office, bedroom), lip/face changes per line, a full-episode builder like engine3d/epbuild.py.
- `finance_series/engine2d/` = flat 2D test (rejected look; keep its FX/overlay helpers: rings, glow, sparkles, receipt, pill, post).
- `finance_series/engine3d/` (epbuild.py, episode.html) = older 3D episode pipeline used for ep11.

## Videos
- **ep11 / Video #1** "Black Friday's Most Expensive Button" (old 3D look): final mp4 + package done (`finance_series/ep11/`).
  Still TODO: cut its 2 Shorts (`engine3d/shorts3d.py ep11`, SHORTS in ep11/ep.py), add to SHORTS_QUEUE.json, finish episode-qa.
- **karl01** "What If You Could See Everyone's Bank Account?" (new toon style, Karl 15-16): `finance_series/karl01/script.md`
  (v1, ~1,600 words, facts: Fed SHED 2025 $400, SCF 2022 mean vs median, Philadelphia Fed lottery-neighbours study) +
  `karl01/TRAILER_karl01.mp4`. NEXT: show the user the trailer + script summary, collect edits, then build the full episode,
  thumbnails, 5 language tracks, 1-2 Shorts.
- 10 topic ideas offered (#3 chosen): it's only..., price tags in hours, see bank accounts, money ages like you, hear what
  ads mean, never feel FOMO, every lie costs $1, pause time, remember every dollar, paid to say no.

## Research
`research/yt1/` = frame-by-frame analysis of 3 IFNation videos + 3 thumbnails (contact sheets, transcripts, close-ups).
Skills: `youtube-skill-1`, `karl-2d-template`, `new-youtube-video`, `finance-timeline-studio`, `youtube-playbook`, `episode-qa`, `youtube-publisher`.

## Environment notes
- Piper voice is not in git: download en_US-ryan-high.onnx(+.json) to `finance02/voice/` from huggingface rhasspy/piper-voices; `pip install piper-tts`.
- Do not start background http servers (blocked); render with rtoon.js / render2d.js (Playwright routing).
- faster-whisper works for transcripts (pass a numpy array, not a path). Downloaded viral videos were dubbed (he/pt).
