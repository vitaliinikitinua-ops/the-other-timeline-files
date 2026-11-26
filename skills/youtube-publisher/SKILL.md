---
name: youtube-publisher
description: Publish or schedule finished videos and Shorts to the user's YouTube channel "The Other Timeline" through Zapier - with a publish queue, a scheduled task, upload limits, duplicate checks, first comments and daily stats. Use for "опублікуй", "заплануй", "залий на ютуб", "publish", "schedule the Shorts", "check the stats".
---

# YouTube Publisher (Zapier) v2

Publishing is outward-facing and permanent: publish only what the user asked for, with the privacy they chose.
On 26.11.2026 the user gave standing permission: publish the finance series myself, 1 long video 18:00 +
1 Short 14:00 Warsaw per day, first comment = question, daily stats.

## Connection
- Zapier app `YouTubeV4CLIAPI`; no default connection, always pass `connection_id 02a61b1b-aa32-8b7c-9dde-25c46b2d6c04`.
- Channel "The Other Timeline" (@theothertimeline-toti), id UCfFsm3i2k6o5xpmM7oRZcsw, uploads playlist UUfFsm3i2k6o5xpmM7oRZcsw.
- Upload: write action `upload_video` (tool `youtube_upload_video`): title, video (URL), thumbnail (URL), description,
  tags (list), category_id "27", privacy_status, made_for_kids "false", default_language/default_audio_language "en", license "youtube".
- Read anything else with `youtube_make_api_get_request` (url + querystring + fail_on_errors "false"); write with
  `youtube_make_api_mutating_request` (e.g. first comment: POST commentThreads?part=snippet,
  body {"snippet":{"videoId":"ID","topLevelComment":{"snippet":{"textOriginal":"..."}}}}).
- Files by URL: commit + push, then `https://raw.githubusercontent.com/vitaliinikitinua-ops/the-other-timeline-files/claude/awesome-hopper-sx7soy/<path>`
  (repo is public; files < 100 MB).

## Queue + scheduled task (how the finance series runs)
- `finance_series/QUEUE.json`: items {ep, kind long|short, due_warsaw, status pending|done, title, video, thumbnail,
  description, tags, comment, url}. Add with `python3 finance_series/engine/publish_queue.py epNN <long time> <short time>`.
  Short descriptions contain "(link of the long epNN video)" - replace with the long video's URL at upload time.
- Scheduled task "Finance series: publish queue + daily stats" (trigger trig_01FmjYgwucogcmCG1FL8f6N2, cron
  `CRON_TZ=Europe/Warsaw 2 14,18 * * *`) fires into the session: publishes at most one due item, posts the first comment,
  logs stats to finance_series/STATS.md on the 14:00 run, commits, reports to the user in Ukrainian.

## Limits (learned 25-26.11.2026)
- Zapier free plan: max 5 YouTube uploads per rolling 24 h ("This action has been throttled without retry.").
- YouTube API project quota: "429 Too Many Requests" until the daily reset at midnight Pacific = 09:00 Warsaw;
  uploads worked right after 09:00. Don't hammer retries: one retry per run, then wait for the next slot.
- `publish_at` scheduling is unreliable here; use the queue + scheduled task instead.
- Description must not contain `<` or `>` ("invalid video description").

## Every publish
1. List the uploads playlist (fields=items(snippet(title,publishedAt,resourceId/videoId))) - skip if the title exists.
2. Upload; on any error list the playlist again before retrying (a failed call can still create a video).
3. Long video: post the first comment (question). Shorts: description links the long video.
4. Update QUEUE.json, commit, push; report URL + time (Warsaw/UTC).

## Manual-only steps (tell the user)
Pin a comment, end-screen elements, cards, Shorts "Related video", extra audio tracks, Test & Compare thumbnails,
.srt upload in Studio -> Subtitles.

## Manual fallback for the user (phone)
YouTube app -> + -> Upload video -> file -> title/description from PACKAGE.md -> Schedule -> Related video.
