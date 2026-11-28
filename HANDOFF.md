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
  (street, store, bank, office, bedroom), lip/face changes per line.
- **Full-episode builder (karl01 session):** `engine3d/toon/epbuild_toon.py` + `episode.html` + `world.js` (extra sets:
  street, mall, hallway, classroom, dealer, hall, behindgym, tv, bus; props; talking mouths via setFace(..., talk)) +
  `rep.js` (range/stills renderer). Episode = `finance_series/<ep>/ep.py` with META + LINES (declarative state per line:
  set/chars/crowd/bars/cam/rc/pill/card/fx, carried line to line) + SHORTS. Commands:
  `python3 epbuild_toon.py <ep> stills|all|dub <lang>|short <n> [stills]`; `bash qs.sh <line idx...>` = quick contact sheet.
  Dubs: `<ep>/lang/<lang>.json` (one string per EN line) -> `<ep>/audio/<lang>.m4a` + captions. Render ~7 fps on 4 cores
  (9 min episode ~ 40-60 min). Thumbnails: `renderThumb` A/B/C in episode.html.
- karl02 session made a parallel player (`toon_ep.html` + `karl02/shots.js`, `sets2.js`, `fx2.js`, `crowd2.js`, `props2.js`).
  Pick one pipeline for future videos (TODO: merge the best parts).
- `finance_series/engine2d/` = flat 2D test (rejected look; keep its FX/overlay helpers: rings, glow, sparkles, receipt, pill, post).
- `finance_series/engine3d/` (epbuild.py, episode.html) = older 3D episode pipeline used for ep11.

## Videos
- **ep11 / Video #1** "Black Friday's Most Expensive Button" (old 3D look): final mp4 + package done (`finance_series/ep11/`).
  Superseded by karl02 (same topic in the new format). Old TODO: cut its 2 Shorts (`engine3d/shorts3d.py ep11`, SHORTS in ep11/ep.py), add to SHORTS_QUEUE.json, finish episode-qa.
- **karl01** "What If You Could See Everyone's Bank Account?" (toon style, Karl 15-16, no cap, turquoise hoodie): script approved
  (v1 + small rhythm edits in `karl01/ep.py`), full video `karl01/KARL01_See_Everyones_Bank_Account.mp4` (~9.2 min),
  thumbs A/B/C, `audio/{es,pt-BR,de,fr,uk}.m4a`, captions x6, 2 Shorts (`KARL01_short_312.mp4`, `KARL01_short_400.mp4`,
  queued), `PACKAGE.md` (title, description, chapters, sources, QA). NEXT: user uploads at 18:00 Warsaw + audio tracks.
- ep11 Shorts: skipped by user decision (Black Friday is remade in the new style as karl02 in another session).
- 10 topic ideas offered (#3 chosen): it's only..., price tags in hours, see bank accounts, money ages like you, hear what
  ads mean, never feel FOMO, every lie costs $1, pause time, remember every dollar, paid to say no.

- **karl02** "What If Every 'Pay in 4' Button Showed the Real Price?" (remake of ep11 in the new format, Karl 23): DONE 28.11 -
  `finance_series/karl02/`: script.md, karl02_numbers.py, shots.js (shot list), build_ep.py (tts|stills|render|final), dub.py (5 tracks ->
  audio/*.m4a), shorts.py (2 Shorts), package.py -> PACKAGE.md (incl. QA), thumb_A/B/C, TRAILER_karl02.mp4. Shorts are in SHORTS_QUEUE.json.
  NEXT: user uploads the long + audio tracks; then publish the Shorts.
- New toon pieces (engine3d/toon): `toon_ep.html?ep=<folder>` = generic full-episode player driven by `<folder>/shots.js` + build/ep_timing.json;
  `sets2.js` (bedroom, store, office, mall+stage, street, studio, restaurant, lot), `props2.js`, `crowd2.js` (instanced crowd, phone prop),
  `fx2.js` (phone checkout UI, amber real-price tag, $ bubbles), `rchunk.js` (render a time range / stills / SFX events), `rstill.js`.
  Full render = 3 parallel chunks, ~50 min for 9.5 min. Encode finals with hqdn3d + CRF 28 (grain otherwise makes files 400+ MB).

## Research
`research/yt1/` = frame-by-frame analysis of 3 IFNation videos + 3 thumbnails (contact sheets, transcripts, close-ups).
Skills: `youtube-skill-1`, `karl-2d-template`, `new-youtube-video`, `finance-timeline-studio`, `youtube-playbook`, `episode-qa`, `youtube-publisher`.

## Environment notes
- Piper voice is not in git: download en_US-ryan-high.onnx(+.json) to `finance02/voice/` from huggingface rhasspy/piper-voices; `pip install piper-tts`.
- Do not start background http servers (blocked); render with rtoon.js / render2d.js (Playwright routing).
- faster-whisper works for transcripts (pass a numpy array, not a path). Downloaded viral videos were dubbed (he/pt).
