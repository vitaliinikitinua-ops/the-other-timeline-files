---
name: finance-timeline-studio
description: Make educational personal-finance "What IF" videos (long 16:9 + 3 Shorts + Ukrainian audio track) for the user's YouTube channel The Other Timeline, fully in code with real market data and a free Piper TTS voice, then publish/schedule via Zapier. Use for any finance / money / investing / saving / debt / inflation video, "фінансове відео", "відео про гроші", or "make the next finance episode".
---

# Finance Timeline Studio

Finance episodes of **The Other Timeline** (@theothertimeline-toti): "What IF You [money habit] Since [year]?"
told as two timelines of the same person (A = the usual habit, B = the other choice), with charts drawn
from real data. Everything is generated in code: no ElevenLabs credits, no image/video AI.
Visual identity, character "You", palette and fonts come from the **other-timeline-studio** skill
(load it too). Shorts caption style comes from **story-shorts-studio**.

Reference implementation (episode 1, "What IF You Saved $5 a Day Since 2010?", published
https://www.youtube.com/watch?v=vOG5hwz-qkc): repo `vitaliinikitinua-ops/the-other-timeline-files`,
branch `claude/awesome-hopper-sx7soy`, folders `finance01/` (test Short) and `finance02/`
(script.py, tts.py, video.py, extras.py, shorts.py, script_uk.py, dub_uk.py, YOUTUBE_PACKAGE.md).
Copy that folder to `financeNN/` and change data, script and scenes; do not rewrite the pipeline.

## Non-negotiable rules (YMYL topic)

- Every number on screen and in narration is computed from a real dataset in code; never estimate,
  never invent. Print the computed values and check them against the script before rendering.
- State the method in the video footnote and the description: amount, frequency, period, price only or
  total return, fees/taxes ignored, data source.
- Always include: "Not financial advice. Past performance does not guarantee future results." spoken in
  an "honest part" beat, as an on-screen card, small text in every Short, and in every description.
- No recommendations of specific products, brokers, coins or stocks to buy. Generic habits only
  (automate, low fees, broad index, emergency fund first, no expensive debt).
- Show the downside honestly: crashes, what panic-selling costs, long flat periods, starting late.
- Before an episode, confirm with the user: topic, voice (Piper / ElevenLabs Christian / own voice),
  length (default ~5 min), language (default English + Ukrainian audio track).

## Data sources (fetch through the proxy; raw.githubusercontent works only for the user's repo,
use cdn.jsdelivr.net/gh/... for other GitHub repos)

- S&P 500 monthly price, dividends, CPI: Robert Shiller dataset,
  `https://raw.githubusercontent.com/datasets/s-and-p-500/main/data/data.csv` (copy saved as
  `finance01/sp500.csv`). Recent months have Dividend=0 and CPI=0: use price only and CPI only up to
  the last non-zero month, and say so. Prices are monthly averages.
- stooq.com resets connections here; do not rely on it.
- For other topics (credit card APR, savings rates, house prices, gold, BTC) find an official or widely
  cited dataset first, save the CSV into the episode folder, cite it in the description.

Episode 1 facts (Jan 2010 - Sep 2026, $152.08 on the 1st of each month): invested $30,569, worth
$99,172 (3.2x, price only); Feb->Mar 2020 -$6,301; Dec 2021->Oct 2022 -$9,283; sold in Apr 2020 and
kept cash = $40,541; start 2015 $21,444 -> $49,841; start 2020 $12,319 -> $20,690; start Jan 2022
$8,669 -> $13,006; $1/day -> $19,834; $10/day -> $198,344; US CPI 2010->2023 +41%.

## Topic bank (what-if + two timelines)

What IF You Started Investing at 18 Instead of 30? / Bought Apple Stock Instead of the First iPhone? /
Only Paid the Minimum on Your Credit Card? / Kept Your Savings in Cash Since 2000? / Rented Instead of
Bought? / Never Sold During a Crash? / Put Your Phone Upgrade Money in the S&P 500?
Pick one simple rule, one everyday prop (coffee cup, phone, credit card, rent bill), one big final number.

## Script structure (~5 min, ~750-800 words, 14-16 beats, one scene per beat)

hook (question + both endings teased) -> rule (the amount per day/month, A spends, B invests) ->
timeline A (prop pile, counter, "left today: $0") -> side effect (inflation / interest) ->
B start (feels pointless, "most people quit here") -> compounding -> first crash -> split again
(panic-sell line vs hold) -> second crash, keep buying -> result (put in vs worth, multiple) ->
starting late (bars) -> amount scale ($1/$5/$10 jars) -> myth/counter-argument -> how in real life
(3 cards) -> honest part (disclaimer checklist) -> outro ("Which timeline are you in?" + comment question).

Write `script.py` as BEATS = [(name, [(subtitle_text, spoken_text_or_None), ...]), ...].
Subtitles use digits ($30,569); spoken text spells numbers and years in words ("twenty ten",
"S and P five hundred") because Piper mis-reads digits. No num2words (it fails to install here).

## Voice (free): Piper TTS

- `pip install piper-tts`; English voice `en_US-ryan-high` from
  `https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/ryan/high/` (.onnx + .onnx.json).
- tts.py: one wav per sentence, `--length-scale 1.12`, trim edges, 0.28 s between sentences, 0.75 s
  between beats, 0.6 s lead-in -> build/vo.wav + build/timing.json (beat and sentence start/end) +
  captions_en.srt. Sentence-level files give exact subtitle timing without transcription.
- If the total is short of the target length, add a beat rather than slowing the voice a lot.
- Ukrainian track: voice `uk_UA-ukrainian_tts-medium` (speaker 1 "mykyta"), `--length-scale 0.78`,
  each sentence placed at the English sentence start (+4 s intro), atempo up to 1.35 if it does not fit,
  same music bed, exact video length -> audio_uk.m4a + captions_uk.srt (dub_uk.py). Ukrainian is ~1.5x
  longer than English, so translate tightly. Check drift (episode 1: max 0.5 s).

## Animation (video.py)

- Reuse `ep2/common.py` (other-timeline-studio drawing code) and fonts in `ep2/fonts/` (Anton, DM Sans,
  Montserrat; download via cdn.jsdelivr.net/gh/google/fonts@main/ofl/...). In common.py the glow colour
  must be `tuple((glow_col or fill)[:3]) + (255,)`.
- Kit already written: `T()` cached text sprites, `pop()` scale-in, `stamp()` rubber stamp, `cup()`,
  `panel()`, `chart_icon()`, `jar()`, `bar()`, `particles()`, live `chart()` (invested amber line,
  value teal line + fill, optional coral "sold" line, auto-rescaling y axis), `counters()` side panel,
  `footnote()` method line, burned 2-line subtitles on a dark band.
- Scene functions get absolute time t and a `B` helper: `b.S(i)` = start of sentence i, so visual events
  land on the words. Render one mp4 per beat with Pool(4) (~5 min for 5 min of video), then concat -c copy.
- Always render `python3 video.py stills` (2 frames per beat contact sheet) and look at it before the
  full render: check text overlapping "You", subtitles covering labels, numbers matching the script.

## Extras (extras.py)

Intro bumper 4 s (amber line branching into teal, You pops, channel name), end screen 15 s (two empty
video slots + subscribe circle), lo-fi music bed in numpy for the full length, 2 thumbnails 1280x720
(A: "$5/DAY -> $99,172" split coral/teal; B: chart + "$99K"), plus 320x180 previews to check readability.
Final mix: voice delayed 4 s, music at 0.32 ducked with sidechaincompress, loudnorm I=-14 TP=-1.5.

## Shorts (shorts.py) - 3 per episode, 30-45 s, 1080x1920

Re-use the narration sentence wavs (no new voice), re-frame the 16:9 scene in the middle band, big
2-line Anton title on top, word-by-word Montserrat Black captions (story-shorts-studio), small
disclaimer + data source, "FULL VIDEO ON THE CHANNEL" at the end. Good cuts: Timeline A habit + result;
the crash and sell-or-hold; the amount comparison / starting late.

## Package (YOUTUBE_PACKAGE.md)

3 title options ("What IF You ... ? (Real S&P 500 Data)"), description with hook, chapters (beat starts
+ 4 s intro, first at 0:00), method, data source, disclaimer, hashtags; 14 tags; pinned comment with a
question + next-topic vote; Shorts titles with #shorts and descriptions linking the full video;
Ukrainian title/description for the audio track.

## Publishing (only after the user says so)

- Zapier YouTube app `YouTubeV4CLIAPI`, action `upload_video`; pass `connection_id` explicitly
  (no default connection is set). Channel id UCfFsm3i2k6o5xpmM7oRZcsw, uploads playlist
  UUfFsm3i2k6o5xpmM7oRZcsw.
- Video and thumbnail are passed as URLs: commit + push, then use
  `https://raw.githubusercontent.com/vitaliinikitinua-ops/the-other-timeline-files/<branch>/<path>`
  (the repo is public; keep the build/ folders and the 120 MB voice models out of git).
- The description must not contain `<` or `>` (YouTube rejects it: write "2010 to 2023", not "->").
- Category 27 (Education), made_for_kids false, language en.
- Zapier can throttle uploads ("throttled without retry"). After any failed upload, list the uploads
  playlist with `youtube_make_api_get_request` before retrying, to avoid duplicates.
- Scheduling: `publish_at` needs a YouTube Partner channel and was throttled; schedule instead with
  `send_later` reminders into this session (the user prefers spacing Shorts by hours, e.g. 2 h apart),
  each reminder containing the full upload parameters.
- Not possible through the API: pinning a comment, end-screen elements, adding the Ukrainian audio track.
  List these as manual steps in YouTube Studio for the user.

## Final report (always)

What was made (files, lengths, LUFS), every number's source, what was published (links) or scheduled
(times in Warsaw and UTC), what the user must still do by hand, and what was not checked.
