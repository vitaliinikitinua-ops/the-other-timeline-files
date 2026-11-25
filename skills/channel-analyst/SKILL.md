---
name: channel-analyst
description: Analyse any YouTube channel from a link (the user's own "The Other Timeline" or a competitor) and review its videos like an expert - stats, outliers, packaging, hooks, structure, comments - then turn it into concrete next-video decisions saved to the repo. Use for "проаналізуй канал", "подивись це відео як експерт", a pasted youtube.com/@handle or watch URL, "what works in my niche", "why didn't this video work".
---

# Channel Analyst

Works with the other-timeline-studio, finance-timeline-studio and story-shorts-studio skills: this skill
decides WHAT to make next, those skills make it. Save every report to the repo
`vitaliinikitinua-ops/the-other-timeline-files`, folder `research/`, so the next session builds on it.

## What works from this cloud container (tested 2026-11-25)

- YouTube Data API through Zapier: app `YouTubeV4CLIAPI`, read action `youtube_make_api_get_request`
  (tool `execute_zapier_read_action`, action `_zap_raw_request`), always pass
  `connection_id 02a61b1b-aa32-8b7c-9dde-25c46b2d6c04` (no default connection is set) and
  `fail_on_errors false`. Use `fields=` to keep responses small. Works for ANY public channel.
- Thumbnails: `https://i.ytimg.com/vi/<id>/maxresdefault.jpg` (fallback hqdefault.jpg) download fine.
- Channel and watch pages (youtube.com) load over HTTP.
- NOT working: downloading video/audio or auto-captions with yt-dlp ("Sign in to confirm you're not a
  bot"). captions.download in the API works only for the owner's own videos. So for a real "watch":
  ask the user to send the video file or a phone screen recording (the watch-video skill then extracts
  frames + Whisper transcript), or use the transcript the user pastes. Never pretend to have watched
  a video you only saw metadata for; say what the review is based on.
- The user's own channel: id UCfFsm3i2k6o5xpmM7oRZcsw, uploads playlist UUfFsm3i2k6o5xpmM7oRZcsw.
  For own-channel analytics try Zapier read action `get_report` (YouTube Analytics); if it fails, ask
  for YouTube Studio screenshots or CSV exports (Overview, Reach: CTR/impressions, Engagement:
  retention graph) and use the yt-retention skill on them.

## API recipes (endpoint -> params)

1. Resolve a link: `@handle` -> `/youtube/v3/channels?part=snippet,statistics,contentDetails&forHandle=@handle`;
   `/channel/UC...` -> `id=UC...`; a watch URL -> `/youtube/v3/videos?part=snippet&id=<id>` then its channelId.
2. Uploads list: `/youtube/v3/playlistItems?part=contentDetails&playlistId=UU<rest of channel id>&maxResults=50`
   (page with pageToken; 50-200 latest videos is enough).
3. Stats in batches of 50 ids: `/youtube/v3/videos?part=snippet,statistics,contentDetails&id=a,b,c`
   with `fields=items(id,snippet(title,publishedAt,description,tags),statistics,contentDetails/duration)`.
4. Comments: `/youtube/v3/commentThreads?part=snippet&videoId=<id>&order=relevance&maxResults=50`.
5. Niche search (costs 100 quota units per call, use sparingly):
   `/youtube/v3/search?part=snippet&type=video&q=<query>&order=viewCount&publishedAfter=<ISO>&maxResults=25`.
   Uploads via Zapier share the same daily quota, so never run many searches on a publishing day.

Save raw JSON to `research/<channel>/raw/` and compute with Python (no guessing from memory).

## Analysis (always in this order)

1. **Snapshot**: subscribers, total views, video count, upload frequency (videos/week over last 90 days),
   long vs Shorts split (Shorts = duration <= 60 s or #shorts), median views for each.
2. **Outliers**: for each video, ratio = views / median views of that channel's same format
   (long or Short) from the surrounding 20 videos. Ratio >= 3 = outlier, >= 10 = breakout. Also views per day
   since publish so new videos are not punished. List the top 10 and the bottom 5.
3. **Formula**: what the outliers share - topic, title pattern ("What IF You...", number, "Why..."),
   title length, emotional promise, thumbnail (main object, face/character, text words, colours: open
   the thumbnails and look), length, time of publish. Name the formula in one sentence.
4. **Packaging check** for the target video(s): title under ~60 chars and truncation at ~45 on mobile,
   curiosity gap, number or contrast, thumbnail readable at 320x180 (resize and look), title and
   thumbnail do not repeat each other.
5. **Expert video review** (only with real frames/transcript):
   - Hook 0-15 s: is the promise clear in the first sentence, is there a visual change by 3 s?
   - Structure: setup -> escalation -> complication -> payoff; where is the first "reason to stay"?
   - Pacing: shot length, dead air, repeated information, jargon, how often the screen changes.
   - Retention risks: list timestamps where viewers likely leave and why; with a real retention graph,
     match drops to the transcript.
   - Audio: voice energy, music level vs voice, loudness (-14 LUFS target).
   - Ending: CTA, end screen, next-video bridge.
   - Score each 1-10 with one sentence of evidence, then the 3 changes with the biggest impact.
6. **Comments**: what people ask, praise, complain about; questions = next video ideas.
7. **For our channel**: 3-5 concrete video ideas in our formats (what-if story, finance timeline,
   story Short), each with title, thumbnail idea and why it should work (which outlier it copies the
   FORMAT of - never copy characters, scenes, names or scripts).

## YMYL / honesty rules

- All numbers come from the API data saved in `raw/`. Say the date of the snapshot.
- Small channels (< 1000 views total) give noise, not signal: say so, rely more on competitor outliers.
- Don't claim causes you can't see (CTR, retention) for channels you don't own; call them hypotheses.

## Output

`research/<channel>/REPORT_<date>.md` (Ukrainian, short headings: Snapshot, Що працює, Формула,
Розбір відео, Коментарі, Що робимо ми, Наступні 3 відео) + `stats.csv` (id, title, date, format,
duration_s, views, likes, comments, ratio). Commit and push to the session branch. If the report is for
other people, also publish it as an Artifact page. Then offer: "Зробити наступне відео за цим планом?"
