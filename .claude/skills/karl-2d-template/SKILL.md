---
name: karl-2d-template
description: The MASTER TEMPLATE for new The Other Timeline videos in the viral 2D "What If You...?" style adapted to our hero Karl (decided with the user 28.11.2026) - hero and recurring cast, story formula, money/general topic mix, 2D engine, power effects + "receipt", thumbnails, 6 audio languages, cadence. Use for every new video in this style, together with youtube-skill-1 (style source), new-youtube-video (workflow), youtube-playbook and episode-qa.
---

# Karl 2D template (v1, 28.11.2026) - all answers are user decisions

Source of the style: `youtube-skill-1` (3 viral videos analysed frame by frame). This file says how WE use it.

## 1. Hero: Karl
- Look (same build as the source channel, our own colours): glossy BLACK ball head with a soft top-left sheen,
  two big touching white eyes with black pupils, tiny mouth, blush on happy; thin black stick arms/legs with ball
  hands; ~3 heads tall; white sneakers.
- Identity: **turquoise hoodie (#2EC4B6) + orange cap worn backwards** = default look.
  A/B test: some videos use a **red hoodie** variant (same cap). Log which look each video used in VIDEOS.md and
  compare CTR / retention after 7 days; the winner becomes the default.
- The cap is a story prop (taken away / returned / lost) like the source channel's hat.
- AGE changes per series to fit the topic (user decision): kid 12-14 (allowance, piggy bank, school), student
  18-21 (first card, dorm, side gig), young worker 22-28 (rent, salary, BNPL, dating), 30+ when needed (mortgage,
  kids). Same face and hoodie; age is shown by height, setting and props. Say the age in the first 45 s.

## 2. Recurring cast (international simple names, added gradually)
Phase 1 (draw now): **Mom**, **Dad**, little sister **Mia**, **Grandma Rose**, best friend **Max**, crush **Lena**.
Each = one identity colour + one hair/hat silhouette (no outlines, flat colours, same rig as Karl).
Phase 2+: redraw our existing cast.js roles 1-3 at a time, only when a video needs them (Banker, Cashier, Landlord,
Boss, Car Dealer, Influencer, Scammer...). Keep a sheet per character in `finance_series/engine2d/cast2d/`.

## 3. Topics: 50/50 mix
Alternate money "What If" (power is about money: "$1 every time...", "price tags in hours of your life", "every
debt glows") and general life "What If" (traits, senses, social powers) where money appears as a consequence.
Title pattern: "What If You (Had/Got/Could) + number/power + everyday thing?" (question, no clickbait words).

## 4. Script template (channel formula + honest numbers)
| Time | Beat |
|---|---|
| 0:00-0:40 | COLD OPEN mini-story: an everyday moment where the power acts BEFORE it is named, with a punchline |
| ~0:40 | PREMISE line: "Most people have X. You have Y." / "Every time ..., you get ..." |
| 0:45-2:00 | "At first, it's amazing." 6-8 quick wins with Mom, Mia, Grandma Rose, Max, Lena (plant callbacks) |
| ~2:00 | subscribe pill animation (after the first big laugh) |
| 2:00-3:30 | "Then it gets bigger." escalation ladder to town / country / celebrity level |
| 3:30-6:30 | "But ..." TURN: the cost lands on family and Max; 1-2 REAL facts with numbers and source |
| 6:30-8:30 | lowest point -> public CLIMAX in front of a big crowd where the power is turned around / used for good |
| 8:30-10:00 | MIRROR ending: replay the opening scene, every callback reversed; one honest real-data line |
| last 15 s | "So would you want ...?" + end screen; subscribe pill again |
- 9-11 min, ~190 words/min of narration (1,700-2,000 words). Second person, present tense, deadpan; sentences 4-12
  words; dialogue quoted inside the narration.
- Real numbers follow our YMYL rules (computed from data, one end date, "example" labels, not financial advice).
- 1 long + 1-2 Shorts per video (see new-youtube-video standing rule).

## 5. Visuals: new 2D engine in code (no AI for video frames)
- Flat painted backgrounds with soft gradients, grain, vignette and bloom; muted creamy palette; saturated colour only
  for Karl, key props and effects. Colour grade per act: warm day, blue-purple night, cold/sepia sad, pink climax.
- Shot ladder per scene: wide -> medium -> close-up -> insert (top-down desk/phone close-ups); over-the-shoulder with a
  blurred foreground head; slow push-in + 2.5D parallax on every shot; hard cuts on sentences.
- Average shot 2.2-3 s (faster in the comic first third), holds 6+ s only for emotion.
- Almost no text: diegetic text, thought/speech pills, small UI. Burned-in captions: none (YouTube CC from the SRT).
- POWER EFFECT: each video gets its own effect placed where the power acts (rings + glow + sparkles; colour per power)
  **plus our signature: a small receipt/counter that pops out with the amount or number** (e.g. "+$1", "-3 h",
  "306") - the bridge between the viral style and our honest numbers.

## 6. Thumbnails: channel recipe, rendered in our engine (free)
Karl huge in the foreground (cut by the frame edge) with a shocked/guilty face and a sweat drop; the power drawn as a
glowing line to the person/thing it hits; adult night-time scene with candles/neon; ONE lowercase quote of the most
awkward moment at the top, one word or number in yellow (`"i love you" +$1`). Richer render than the video (gloss,
rim light, bloom). Make A/B/C for Test & Compare.

## 7. Audio languages: English original + 5 dubs
- Languages: **Spanish, Portuguese (BR), German, French, Ukrainian** (expand later if views come).
- Method: translate the script (keep the deadpan short sentences), generate each track with free Piper voices
  (es_ES/es_MX, pt_BR, de_DE, fr_FR, uk_UA), fit each line into the English timing (speed per line, max +-15%), mix
  with the same music/SFX bed -> `epNN/audio/<lang>.m4a`; also translated titles, descriptions and SRT captions.
- Upload: YouTube Studio -> Languages -> Add audio track (the Data API cannot add audio tracks); the user does it.
  If the channel has no multi-language audio access yet, use YouTube's auto-dubbing and keep our captions/titles.

## 8. Narrator
Piper `en_US-ryan-high`, speed ~1.1, almost no pauses, ~190 words/min.

## 9. Cadence
3 long videos per week (9-11 min) + 1-2 Shorts each, 6 audio tracks each.

## 10. Next step (user decision)
Build `finance_series/engine2d/` and show the user a TEST SHEET (Karl turquoise + red, Mom, Dad, Mia, Grandma Rose,
Max, Lena in several emotions, one background) and a 10-second test scene with a power effect + receipt.
Only after approval: the first full video in this style.
