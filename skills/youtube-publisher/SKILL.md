---
name: youtube-publisher
description: Publish or schedule finished videos and Shorts to the user's YouTube channel "The Other Timeline" through Zapier, respecting the upload limits, avoiding duplicates, and listing the manual Studio steps. Use for "опублікуй", "заплануй", "залий на ютуб", "publish", "schedule the Shorts".
---

# YouTube Publisher (Zapier)

Publishing is outward-facing and permanent: publish only what the user asked to publish, with the
privacy they chose (ask: public / unlisted / private, and title + thumbnail variant if not given).

## Connection

- Zapier app `YouTubeV4CLIAPI`; there is NO default connection, always pass
  `connection_id 02a61b1b-aa32-8b7c-9dde-25c46b2d6c04`.
- Channel "The Other Timeline" (@theothertimeline-toti), id UCfFsm3i2k6o5xpmM7oRZcsw,
  uploads playlist UUfFsm3i2k6o5xpmM7oRZcsw.
- Upload: write action `upload_video` (tool `youtube_upload_video`). Params used: title, video (URL),
  thumbnail (URL), description, tags (list), category_id "27" (Education) or "24" (Entertainment)
  for story episodes, privacy_status, made_for_kids "false", default_language "en",
  default_audio_language "en", license "youtube", notify_subscribers.
- Files must be reachable by URL: commit + push to the session branch, then
  `https://raw.githubusercontent.com/vitaliinikitinua-ops/the-other-timeline-files/<branch>/<path>`
  (repo is public; keep files < 100 MB; keep build/ dirs and voice models out of git).

## Limits (learned 2026-11-25)

- Zapier free plan: max 5 YouTube uploads per rolling 24 h (counts uploads made via Zapier from any
  session). When exceeded, Zapier answers "This action has been throttled without retry." and nothing
  is uploaded. YouTube API itself allows about 6 uploads/day per project.
- So: plan at most 5 uploads per 24 h; before scheduling, list the uploads playlist and count uploads
  in the last 24 h; the next free slot = (5th most recent upload time) + 24 h + 5 min.
- `publish_at` (native YouTube scheduling) needs privacy "private" and may be blocked for this channel;
  prefer scheduling with `send_later` reminders into the session, one per video, spaced by the hours the
  user wants. Each reminder must contain ALL upload params (it runs without this context), the duplicate
  check, and "if throttled, retry once 60 min later and tell the user".
- Description must not contain `<` or `>` (YouTube: "invalid video description"). Write "to" instead of "->".

## Every publish

1. List the uploads playlist (`youtube_make_api_get_request` on `/youtube/v3/playlistItems`,
   `fields=items(snippet(title,publishedAt,resourceId/videoId))`) - skip if the same title exists.
2. Upload. On any error, list the playlist again before retrying (a failed call can still create a video).
3. Report the watch URL, privacy and time (Warsaw and UTC).
4. Shorts: description links the full video; remind the user to set "Related video" in Studio.

## Cannot be done via API (give the user these Studio steps)

Pin a comment (posting is possible, pinning is not), end-screen elements, cards, "Related video" for
Shorts, extra audio tracks (Languages -> Add audio track), Test & Compare thumbnails.
Uploading Ukrainian / other subtitles .srt is done in Studio -> Subtitles.

## Manual fallback for the user (phone)

YouTube app -> + -> Upload video -> pick file -> paste title/description from YOUTUBE_PACKAGE.md ->
Schedule (works without limits in the app) -> Related video = the full episode.
