---
name: youtube-playbook
description: The rulebook for making The Other Timeline videos and Shorts interesting and well packaged - what each second should look like, where hooks, text, numbers, CTAs and end screens go, title/thumbnail rules, styles, publishing rhythm and how to A/B test - built from our own channel data (Nov 2026), competitor breakdowns and viral Reels. Use before writing any script, Short, title or thumbnail, and for "як зробити цікавіше", "хук", "превю", "що поставити", "коли публікувати", "чому не дивляться", "make it more engaging".
---

# YouTube Playbook (v2, 27.11.2026)

Load together with: `finance-timeline-studio` (production), `episode-qa` (check), `youtube-publisher` (upload),
`channel-analyst` (data). This file says WHAT to make and WHERE things go; the others say HOW.
Mark every rule as **[data]** (seen in our numbers), **[competitor]** (seen in outliers we analysed) or
**[practice]** (common creator practice, not yet proven for us). Update the rule labels when tests finish.

## 00. Channel decisions by the user (27.11.2026) - these override any recommendation below
| Topic | Decision |
|---|---|
| Long videos | 8-10 min, a NEW episode every day, published by the USER manually at 18:00 Warsaw (I prepare the package) |
| Shorts | Published by ME automatically, up to 5 per day (Zapier limit), slots ~13:00, 15:00, 17:00, 19:00, 21:00 Warsaw |
| Voice | Piper only (free). No ElevenLabs. |
| Platforms | YouTube only (no TikTok/Reels for now) |
| CTA | NO keyword CTA, no "comment X to get Y". A plain question in the first comment is fine. |
| Style of long videos | Decided after the Shorts style test (winner style becomes the long-video style) |
| Old long EP04-EP10 | Not published. New episodes are made from scratch. |
| Old hourly queue task | Disabled 27.11 (trig_01FmjYgwucogcmCG1FL8f6N2) |
| Hook (first 3 s) | **END FIRST** (flash-forward): open on the final outcome - rich/broke/shocked character + the final number - then "how did this happen?" and rewind to the start |
| Tone | Irony + drama: funny recurring cast (You, Max, Grandma, Banker), serious real numbers |
| Characters | 3D rounded "clay" low-poly cast with meme faces + fast viral-Shorts editing (punch-ins, shake, SFX). Cast bible: `finance_series/engine3d/cast.js` (19 characters) - reuse them, add new ones there |
| Retention device (long videos) | **Viewer guesses**: an open question on screen in the first 30 s ("Who ends up richer? Guess now"), reminders mid-video, answer revealed near the end |
Package for every long video (user uploads in Studio): mp4, 3 thumbnails A/B/C for Test & Compare, title (<= 55 chars),
description with chapters + method + sources + not financial advice, tags, first comment (question), suggested end screen.

## 0. What our data says so far (snapshot 27.11.2026, channel 3 days old)
- 13 videos, 473 views, 0 subscribers. Shorts: 100-160 views each, then stop. Long videos: 0-6 views. **[data]**
- Meaning: Shorts get YouTube's small test pool and are not pushed further -> viewers swipe early;
  long videos get no browse traffic until the channel has an audience. **Shorts first, longs later.** **[data]**
- Mixed topics (memory series + finance) confuse who to show us to. One niche: money "what if" with real numbers. **[practice]**
- Robotic Piper voice + static letterboxed layout are likely swipe reasons. The user keeps Piper (free): compensate with faster pacing (SPEED, tight gaps), stronger hooks and visual styles.

## 1. The first 3 seconds (decides everything)
- Frame 1 is never empty, never a logo, never a fade-in. It already shows the conflict: a giant number, a question
  headline, or a character reacting. **[practice]**
- Say the payoff-promise in the first sentence: "$5,000 on a card, minimum payments only - it takes 19 years." **[competitor]**
- Headline on screen = the question the video answers, max 2 lines x 22 characters, white line + yellow line. **[practice]**
- DEFAULT HOOK (user choice): **end first**. Frame 1 = the ending (character's reaction + final number, e.g. "$198,344"
  or "19 YEARS"), line 1 = the outcome ("This is me, 20 years later, with $198,344. Because I said NO."), line 2 = the
  rewind ("Let's go back to day one."), visual rewind effect (fast reverse + "20 YEARS EARLIER" card).
- Other hook types (use only for tests):
  1. **Big number** cold-open (number counts up in 1 s, sub-line explains). 2. **Question + A/B quiz** (answer at the end).
  3. **Contrast** ("same $200/month, 18 vs 30"). 4. **Impossible premise** ("every NO pays you $1").
  5. **Mistake** ("he invested at the worst moment").
- Something must move or change by 0.5 s and again by 3 s. **[practice]**

## 2. Shorts layout (1080x1920) - where everything goes
```
y 0-180     safe top (app UI) - nothing important
y 200-460   HOOK HEADLINE (2 lines, 84-100 px, white + yellow, black stroke)
y 560-1380  SCENE full width, zoomed 1.4x, slow push-in per sentence (no letterbox bars!)
y 1380-1620 CAPTION: 1-2 words at a time, 110-120 px, numbers/$ in yellow, pop-in 0.1 s
y 1700-1800 safe bottom (likes/description overlay) - only the tiny "Not financial advice · real data"
y 1906-1920 progress bar (amber), grows with time
```
- Background = same frame blurred + darkened, never a flat colour. **[practice]**
- Captions: max 8 characters per chunk, no full sentences on screen. **[practice]**
- Length 25-45 s. Cut silences (gap 0.07 s between sentences). Faster than the long video. **[practice]**
- End: the last frame connects to the first (loop) or reveals the quiz answer + "Comment A or B". **[practice]**
- Old format (static title block + 16:9 scene in a letterbox strip) = 100-160 views ceiling. Don't use it. **[data]**

## 3. Styles (keep the story, change the look)
`engine/styles.py` has 10 looks applied on top of our scenes: glow (neon sketch), comic, chalk (chalkboard), lego
(brick mosaic), pixel, minimal (line art), explainer3d (floating 3D card), flat, ps2, cgi.
- Best with our scenes: glow (charts!), chalk, minimal, pixel, explainer3d. **[practice: visual check]**
- Lego/pixel need bright scenes with characters; on dark charts they become unreadable -> use glow/chalk for chart episodes.
- ps2/cgi are only approximations (2D filters), don't promise "3D".
- One style per Short; test one style per day (section 8). Winning style becomes the default.

## 4. Long videos (8-10 min) - beat map
| Time | What | Why |
|---|---|---|
| 0:00-0:15 | END FIRST: final scene + final number + reaction, then rewind card | intro drop-off |
| 0:15-0:30 | The GUESS: question on screen "Who ends up richer? A or B - guess now" | open loop |
| 0:20-1:00 | Setup: who (You/Max/Grandma), the rule, the stakes in one sentence | context |
| every ~2 min | Remind the guess ("Still think A?") with a small on-screen tag | retention |
| every 45-60 s | A new scene / twist / number reveal; never the same frame > 6 s | re-hook |
| middle | Chart race or timeline split - the visual payoff | value |
| 60-75% | Twist (stopper, late start, crash) | mid-video dip |
| ~85% | REVEAL the answer to the guess with a big moment | payoff |
| last 90 s | Honest part, 3 practical rules, question for comments ("Did you guess right?") | trust + engagement |
| last 15 s | End screen (next video + subscribe) | session time |
- Our data says longs get 0-6 views without an audience **[data]**, but the user chose daily longs: so every long gets 1-2 Shorts cut from it (new styles), published in the Shorts slots, so viewers have a path to the long.

## 5. Titles and thumbnails
- Title <= 55 characters, the hook in the first 40 (mobile truncation). Pattern: "What If You ...?" / "He ... and Had LESS Money" /
  "$X ... = Y Years". One number, one emotion. Shorts title differs from the long title (no duplicate signals). **[competitor]**
- Thumbnail = ONE big number + ONE big face (character) + max 3-4 words; readable at 320x180; title and thumbnail
  say different things (thumbnail = number, title = question). **[competitor]**
- Always make 3 thumbnails (A: scene + quote, B: two characters + number, C: minimal: huge number + one face) for
  YouTube Studio -> Test & Compare (manual; the user uploads them). **[practice]**

## 6. Engagement mechanics (when to put what)
- Comment keyword CTA ("comment MONEY to get X") worked hugely on a viral Reel **[competitor]**, but the USER DECLINED it
  (27.11): don't use keyword CTAs. Use a plain question or the A/B quiz instead.
- **Quiz** at the start, answer at the end -> loops + comments. **[practice]**
- **Numbered list** visible from the start ("1 of 10 ... 10") -> people wait for the last item. **[competitor]**
- First comment on every long video = a question (automated); pin it (manual). Shorts: pinned comment with the full-video link (manual).
- Never ask for subscribe in the first 30 s. Ask after delivering value, once. **[practice]**

## 7. Niche & competitors learned
- 100%-completion gaming channels (СТОДНЕВКА etc.): one absurd goal in the title, big counter, 1-3 h - shows the
  power of "one clear goal + number" titles. **[competitor]**
- Finance "what if" competitors: real numbers + clear contrast + a character beat purely abstract talk. **[competitor]**
- Keep: real data, honest part, "not financial advice". This is what makes us different and safe (YMYL).

## 8. Testing protocol (one variable at a time)
1. Change ONE thing: style, hook type, voice, title pattern or length. Keep topic quality similar.
2. Publish 1 test Short per day at the same time (Warsaw 14:00-18:00 for US+EU overlap).
3. Read after 48 h in Studio: **Viewed vs swiped away %**, average % viewed, views, subs gained. API only gives views/likes;
   ask the user for Studio screenshots for the rest.
4. Log in `finance_series/STATS.md` (date, video, variable, result). Winner = higher viewed% AND higher avg % viewed.
5. After 3 tests in a row with the same winner, make it the default in this playbook (change the label to **[data]**).

## 9. Publishing rhythm
- Max 5 uploads per rolling 24 h through Zapier (failed runs count). Prefer 2-3 Shorts/day over longs right now.
- Same posting time daily. Shorts of an episode 30-60 min after its long (when longs return).
- YouTube only for now (user decision 27.11).

## Standing user decisions (28.11.2026)
- NEW STYLE (user decision 28.11.2026): new videos follow `karl-2d-template` (viral 2D "What If You...?" style from `youtube-skill-1`, Karl in turquoise hoodie (no cap) with a red-hoodie A/B test, cast Mom/Dad/Mia/Grandma Rose/Max/Lena, 50/50 money/general topics, 9-11 min, 3 per week, English + 5 audio dubs es/pt-BR/de/fr/uk). The 3D engine stays for older formats.
- SHORTS PER VIDEO (user decision 28.11.2026): 1 long video + **1-2 Shorts**, never 3+. 2 Shorts only when the topic is broad and the long video has many strong hooks; otherwise 1. Shorts are SHORT (~20-40 s), one hook each, and always point to the full video (pinned comment/description link + "FULL VIDEO ON THE CHANNEL" end card).
- MAIN HERO of every video = **Karl** (cast.js key `you`, name "Karl"). Narration and on-screen text call him Karl; the story is still told so the viewer sees themselves in him.
- ROUND all money on screen and in the voice-over so it looks clean ($1,200, ~$390, ~$2,850, ~32 hours). Exact values stay in BRIEF.md / the description's method section.
