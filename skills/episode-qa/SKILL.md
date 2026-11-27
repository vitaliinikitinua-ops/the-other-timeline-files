---
name: episode-qa
description: Self-check every finished video of The Other Timeline before it is queued or published - facts, numbers, visuals, audio, length, file size, thumbnails and the Short - and fix what fails. Use after rendering any episode or Short, or when the user says "перевір себе", "check the video", "is it ready".
---

# Episode QA (run after every video, before queueing)

Work through the list, fix, re-render only what changed, then note the result in the episode's PACKAGE.md.

## 1. Numbers and facts
- Every number in narration and on screen exists in the script's docstring with its source and date; re-run the
  computation in Python and compare. One end date per episode.
- Example values are labelled "example". No invented bars/tags. Claims about the world (laws, events) are well known
  and phrased carefully ("a common formula", "many planners suggest").
- Disclaimer beat present; description has method + sources + "not financial advice"; no `<` or `>` in description.

## 2. Contact sheet (`build.py epNN stills` -> build/contact.png, 2 frames per beat)
Look at every frame and check:
- Text not covering faces; nothing important below y=820 (subtitle band) - bubbles, counters, big texts.
- Glyphs: no "=" where "≠" was meant, no boxes from "→" or emoji in Anton/DM Sans.
- Chart side panel / labels match what is said at that moment (key-date values injected).
- Props visible (not hidden behind shelves), characters' emotions fit the line.
- Scene variety: no 3 identical frames in a row.

## 3. Final file
- `ffprobe` duration: long video 8-10 min (8.0 min minimum incl. 15 s end screen). Short 25-45 s.
- Loudness `ffmpeg -af ebur128` integrated about -14 LUFS.
- Size < 100 MB (GitHub raw upload limit); mix uses CRF 23.
- Spot frames at 0 s, 25%, 50%, 90% (`select=eq(n,...)` tile) to confirm render + subtitles.

## 4. Thumbnails
- View thumb_A/B at full size and the 320x180 preview: quote readable, highlighted word yellow, one big number,
  faces visible, no number covering a face.

## 5. Short
- Frame 1 already shows the hook number (no fade-in); captions inside the safe area; title lines short;
  "FULL VIDEO ON THE CHANNEL" at the end; segments chosen by beat name and they make sense in order.

## 5b. Shorts v2 / style Shorts
- Extract frames at 1 s, 3 s, 9 s, 18 s and the last 2 s; tile them and look: headline fully inside y 200-460, caption
  readable, scene visible (not an empty part of a split-screen or a dark chart lost in a style filter), progress bar moves.
- Quiz: the answer matches the real number in the script. Number cold-open: the final number equals the script's number.
- Style check: if the scene is unreadable in the chosen style, switch the style (charts -> glow/chalk/minimal).

## 6. Report
In the final report say what was checked, what was fixed, and what could not be checked (e.g. listening to the
whole voice track). Never claim the video was watched end to end if only frames were inspected.
