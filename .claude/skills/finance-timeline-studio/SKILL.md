---
name: finance-timeline-studio
description: Make educational personal-finance "What IF" videos (8-10 min 16:9 + one Short each) for the user's YouTube channel The Other Timeline, fully in code with real market data and a free Piper TTS voice, then queue them for publishing. Use for any finance / money / investing / saving / debt / inflation / housing / crypto video, "фінансове відео", "відео про гроші", "зроби серію відео", "make the next finance episode".
---

# Finance Timeline Studio (v3, 27.11.2026)

Finance episodes of **The Other Timeline** (@theothertimeline-toti): "What IF You ...?" told as two or
three timelines of the same person ("You"), or as a superpower story ("every NO pays $1"), always ending
with real numbers. Everything is code: no ElevenLabs credits (user decision 27.11: Piper only), no image AI.
Cadence (27.11): one NEW 8-10 min episode per day for the user to publish at 18:00 + 2-4 Shorts cut from it in the
current winning style (shorts_v2.py) for the automatic Shorts queue. Old EP04-EP10 longs are not published. Load with it:
**other-timeline-studio** (look), **story-shorts-studio** (Short captions), **youtube-publisher** (upload),
**episode-qa** (self-check before publishing), **youtube-playbook** (hooks, layout, titles, tests - read first).

## Where everything is
Repo `vitaliinikitinua-ops/the-other-timeline-files`, branch `claude/awesome-hopper-sx7soy`, folder `finance_series/`:
- `engine/kit.py` characters (`person(who, size, emo)`: you, max, grandma, banker, barista, seller, stranger;
  emos neutral happy smug shock sad angry worried love money), locations (kitchen cafe store bank office street
  bedroom dealer living void void_red void_teal), props (card phone bill tag coin receipt calendar jar icon:
  car house iphone btc gold mattress piggy tv shield warning chart sofa burger box), bubbles, glow_line.
- `engine/scenes.py` declarative scene types: `stage`, `split`, `chart`, `bars`, `list` (or `cards=True`), `end`.
  Items appear on sentence index `at` (floats allowed, 1.5 = halfway through sentence 1), `until`;
  `flash={k: colour}`, `shake=[k]`; camera changes framing on every sentence automatically.
- `engine/data.py` loaders: `sp500()` (Shiller monthly avg, price only), `fred(code, monthly=True)`, `gold()`,
  `dca(prices, start, end, monthly)`, `card_payoff(balance, apr, fixed=None)`.
- `engine/build.py epNN [tts|stills|render|mix|short|thumbs|package|all]`, `engine/publish_queue.py epNN <long> <short>`.
- `epNN/script.py`: BEATS = [(name, [(subtitle, spoken or None), ...], scene_dict), ...], META, THUMBS, SHORT, SPEED, MUSIC_SEED.
  Copy an existing episode (ep01 superpower, ep02/ep04 timelines with charts, ep07 housing) and change it.
- Data in `finance_series/data/`: sp500.csv, gold.csv, fred_*.csv. More FRED series:
  `curl https://fred.stlouisfed.org/graph/fredgraph.csv?id=CODE` (works through the proxy). Used so far: CPIAUCSL,
  CP0000EZ19M086NEST (euro HICP), TERMCBCCALLNS (card APR), MORTGAGE30US, CSUSHPINSA (Case-Shiller), CBBTCUSD,
  CES0500000003 (hourly pay), PSAVERT (saving rate), MSPUS, NASDAQCOM, CUSR0000SETA01/02 (new/used car CPI).
- Piper voice model: `finance02/voice/en_US-ryan-high.onnx` (not in git; re-download from
  huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/ryan/high/ if the container is fresh; `pip install piper-tts`).

## Episodes made (series 1) and what's queued
EP01 $1 every no · EP02 invest at 18 vs 30 · EP03 minimum payment · EP04 mattress vs gold vs S&P since 2000 ·
EP05 Bitcoin vs iPhone 2015 · EP06 price tags in hours · EP07 house 2006 vs 2012 · EP08 salary doubled still broke ·
EP09 everything went wrong in one month · EP10 invested at the worst moment. Queue: `finance_series/QUEUE.json`
(1 long 18:00 + its Short next day 14:00 Warsaw). Don't repeat these topics; build on them (cross-reference numbers).
Ideas next: start at 25 vs 35 in Europe, rent vs buy with rent index, car new vs used (needs sourced prices),
"what if you got $1 every time you saved", subscriptions audit, retirement at 40, kids' account from birth.

## Rules (YMYL)
- Every number on screen and in narration is computed in code from data/. Print and check them before rendering.
  Pick ONE end date per episode and use it for every number (EP04 bug: gold at Oct, chart at Sep).
- Example values (salary, prices, bills) must be labelled "example" on screen and in narration. Never draw a bar
  or tag with an invented number (EP05: an iPhone resale "$60" bar was removed).
- Disclaimer beat ("the honest part") + `not financial advice` in every description. No product/broker/coin picks.
- Show downsides: crashes, recovery times, survivorship bias, local differences (US vs Europe).

## Script recipe (target 8-10 min)
- Piper at SPEED 1.18 speaks ~2.95 words/s incl. pauses: **8 min needs ~1,350-1,450 words**, 13-20 beats.
  First drafts always came out 5.5-6.5 min; plan 18 beats of 5-6 sentences from the start.
- Structure (v3, user decisions 27.11): END-FIRST hook (final scene + number, then rewind) -> GUESS question on screen
  (A or B?) -> ... -> reveal of the guess at ~85% -> honest part. Tone: irony + drama. Older structure:
  hook (both endings teased, big number) -> setup with recurring cast (Max = bad influence, Grandma = wise,
  Banker) -> rules/timelines -> timeline A story with drama -> timeline B -> chart race -> result bars -> twist
  (stopper, different start date, Max's timing) -> why it works -> how-to cards -> honest part -> outro question.
- Spoken text spells numbers ("twenty ten", "S and P five hundred", "four thousand nine hundred"); subtitle text uses digits.
- Hook in the first sentence; scene changes every sentence; numbers in subtitles are amber automatically.

## 3D cast & engine (approved direction 28.11.2026: rounded "clay" 3D + viral-Shorts meme energy)
- `finance_series/engine3d/`: `cast.js` = CHARACTER BIBLE (19 characters: you, max, grandma, banker + dad, mom, boss,
  coworker, landlord, realtor, car_dealer, crypto_bro, scammer, kid, teen, grandpa, cashier, doctor, influencer), each with
  role, colours, outfit, hair, face overlays, accessories, height, belly. ALWAYS reuse these; add new ones to cast.js.
- `rig.js`: makeChar(who) rounded rig (capsule limbs, sphere hands, elbows/knees), meme faces `setFace(ch, emo)`
  (neutral happy shock smug sad panic money laugh angry wink), poses `applyPose(ch, pose|{from,to,t0,dur}, t, {walk, hop, squash, shake})`
  (idle cheer no point shrug facepalm hold thumbsup panic slump jump sit), props (bill coin cup shoebox jar), sets
  (cafe rich street void), `shot()` camera with punch-in + shake.
- Render: an HTML page exposing `window.renderX(t)` -> dataURL, driven by Playwright (`render_demo.js`, ~0.2 s/frame on
  SwiftShader, 1080x1920); overlays + Piper VO + synth SFX + music in Python (`compose_demo.py`). Serve the repo root
  with `python3 -m http.server 8790`.
- Brand: `finance_series/brand/avatar_800.png`, `banner_2560x1440.png` (text inside the 1546x423 mobile safe area).
  YouTube API can't set the avatar and Zapier can't upload binaries -> the user uploads them in Studio.

## Character upgrade TODO (user decision 27.11) - DONE 28.11 in 3D (see above)
Keep the cast, make them more alive in `engine/kit.py`: arms + hands with gesture poses (point, shrug, facepalm, hold
money, thumbs up), more emotions (panic, smug-rich, crying-laughing), simple body motion (walk cycle, jump, slump,
shake), eye blinks. Do this before the next new episode and show the user a test sheet first.

## Visual gotchas (learned)
- Anton/DM Sans have no "≠", "→", emoji: they render as "=" or boxes. Use words ("IS NOT", "BECOMES", "TO").
- Keep on-screen texts above y=820; subtitles occupy y>890. Bars baseline 770.
- Chart lines must hit the numbers you say: inject key-date values into monthly arrays (EP05).
- FRED CPI has no Oct 2025 value (shutdown): interpolate for charts.
- Always render `build.py epNN stills` and look at the contact sheet before the full render (see episode-qa).

## Build pipeline facts
- `build.py epNN all` = tts, stills, render (Pool 4, ~20 min per 8-min episode), mix (re-encode CRF 23 so files stay
  < 100 MB for raw.githubusercontent uploads), thumbs (A/B), package, short.
- Several episodes in a row: chain them with `while kill -0 PID` waiters (not `pgrep -f`, which matches itself).
- Never name a module `queue.py` (shadows stdlib, breaks multiprocessing) -> it's `publish_queue.py`.
- Don't `git add` while ffmpeg is still writing an mp4 (git error "unstable object source").
- Shorts: SHORT["segs"] uses beat NAMES (not indexes), hook text on frame 1 (80% of viewers swipe in second 1),
  word-by-word captions, 30-45 s.

## Shorts v2 (use these, not build.py short)
`engine/shorts_v2.py epNN <style>` -> `epNN/tests/EPNN_short_<style>.mp4` (reuses build/tts + timing.json + music.wav).
- `full`: no letterbox; blurred full-screen bg + 1.42x zoomed scene + push-in, 2-line hook headline (TESTS[ep]["head"] or
  SHORT["title"]), big 1-2-word captions, progress bar, 0.07 s gaps.
- `number`: + counting giant number on the first 1.8 s (TESTS[ep]["number"] = text/sub/col).
- `quiz`: + A/B question headline and answer reveal + "Comment A or B" in the last 3 s (TESTS[ep]["quiz"]).
- `fx-<style>`: full layout with a look from `engine/styles.py` (glow comic chalk lego pixel minimal explainer3d flat ps2 cgi).
  Match style to scenes: charts -> glow/chalk/minimal; bright character scenes -> lego/pixel/comic. Check frames at 3 s,
  9 s, 18 s before sending (EP04 lego on dark charts was unreadable and had to be redone as glow).
- Render ~5-8 min per Short on 4 CPUs; run 3 in parallel with `xargs -P 3`, then wait with a background until-loop.
- Thumbnail C variants (huge number + one big face): `engine/thumbs_test.py` -> `epNN/tests/thumb_C.jpg`.

## Standing user decisions (28.11.2026)
- MAIN HERO of every video = **Karl** (cast.js key `you`, name "Karl"). Narration and on-screen text call him Karl; the story is still told so the viewer sees themselves in him.
- ROUND all money on screen and in the voice-over so it looks clean ($1,200, ~$390, ~$2,850, ~32 hours). Exact values stay in BRIEF.md / the description's method section.
