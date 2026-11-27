---
name: new-youtube-video
description: The fixed workflow for every new video of The Other Timeline - triggered ONLY when the user writes "нове відео ютуб" (or "new youtube video"); NOT for "нове відео" alone, which belongs to the Polsha bez stresu channel skill (nove-video). Opens a dedicated chat (session) for the video, asks the user structured questions, analyses the viewer's problem and real solutions with real data, then writes the script with the user and produces the video. Use whenever a new video starts.
---

# New YouTube video - workflow (agreed with the user 28.11.2026)

Goal: every video must be USEFUL to the viewer: a real money problem of a US/EU middle-class person, why it happens,
what it costs (real data), and what actually helps. Format rules: `youtube-playbook` (END-FIRST hook, GUESS question,
irony + drama, 3D rounded cast, fast edit, 8-10 min, Piper voice, no keyword CTA). Production: `finance-timeline-studio`
(3D engine in `finance_series/engine3d`, cast bible `cast.js`). QA: `episode-qa`. Publishing: longs = user, Shorts = me.

## 0. Open a dedicated chat
- If this is the main/channel chat: create a new session (claude-code-remote `create_session`, same repo and branch
  `claude/awesome-hopper-sx7soy`) titled "Відео #N: <working title or 'нова тема'>", with the prompt:
  "РЕЖИМ: сесія відео #N. Запусти скіл new-youtube-video з кроку 1. Відповідай українською." Tell the user the chat is
  open and that the questions are waiting there. N = next number in `finance_series/VIDEOS.md` (create it if missing).
- If the prompt already says "РЕЖИМ: сесія відео": skip step 0 and start at step 1.
- If creating a session is impossible, run the whole workflow in the current chat.

## 1. Questions round 1 - topic & viewer (AskUserQuestion, max 4 questions)
- Offer 3-4 concrete topic ideas (+ "свою тему") based on: STATS.md (what worked), done topics in VIDEOS.md (no repeats),
  current money news, seasonal moments (taxes, holidays, Black Friday, new year resolutions). Each idea = one-line pain.
- Who is the viewer (student / young worker / family with kids / renter / 40+), what pain they feel, what they should
  be able to DO after watching.

## 2. Research: problem -> causes -> cost -> solutions (do this yourself, save `epNN/BRIEF.md`)
- Problem in one sentence in the viewer's words. 3-5 causes (psychology + system: fees, interest, inflation, marketing).
- Cost in real numbers: FRED/BLS/Fed/Eurostat/Shiller data from `finance_series/data` or downloaded; one end date.
- Common myths and mistakes. 3-5 solutions that work for normal people, with honest limits; no product/broker picks.
- Two timelines A/B that dramatise the choice; the END-FIRST scene; the GUESS question with the real answer.
- Sources list. Mark example values as "example". Show the brief to the user in short form.

## 3. Questions round 2 - story (AskUserQuestion)
- Which timeline A/B and characters from cast.js (or a new character -> add it to cast.js), end-first scene choice,
  guess question choice, the twist, tone accents. Optional round 3: title + thumbnail direction (3 variants each).

## 4. Script (epNN/script.md + build data)
- Beat map from youtube-playbook section 4 (end first -> rewind -> guess -> timelines -> twist -> reveal ~85% -> honest
  part -> 3 rules -> question). ~1,350-1,450 spoken words for 8-10 min. Numbers computed in code and printed.
- Show the script to the user, apply edits, get an explicit "так/ок" before production.

## 5. Production -> QA -> package
- 3D render (engine3d), VO (Piper), SFX, music, overlays; 2-4 Shorts cut from it; run episode-qa.
- Package for the user (publishes at 18:00): mp4, 3 thumbnails A/B/C, title, description (chapters, method, sources,
  not financial advice), tags, first comment, end-screen suggestion. Add Shorts to SHORTS_QUEUE.json.
- Log the video in `finance_series/VIDEOS.md` (number, topic, viewer, problem, date, links). Commit + push.

## Standing user decisions (28.11.2026)
- MAIN HERO of every video = **Karl** (cast.js key `you`, name "Karl"). Narration and on-screen text call him Karl; the story is still told so the viewer sees themselves in him.
- ROUND all money on screen and in the voice-over so it looks clean ($1,200, ~$390, ~$2,850, ~32 hours). Exact values stay in BRIEF.md / the description's method section.
