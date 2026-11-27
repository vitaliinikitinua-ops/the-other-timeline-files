# Finance series — overnight plan (started 26.11.2026)

User's answers (26.11): Piper voice; English only; publish myself gradually (1 long 18:00 + 1 Short 14:00
Warsaw daily); audience US + Europe middle class, "interesting, lots of animation, max watch time,
clickbait thumbnails"; topics: investing/compound, debt/cards, inflation/money, budget/life, 1 crypto;
format mix (two timelines + superpower story); top-style thumbnails (quote + yellow word, You + reaction,
glowing line, neon night); Shorts = best moment of each long; no intro (hook first), 15 s end screen;
max motion; recurring side characters; quality over quantity; daily stats check; first comment = question;
update + add skills; report here in chat.

## Episodes (8-10 min each, every number computed from data/ in code)

| # | Title | Format | Data |
|---|---|---|---|
| 01 | What If You Got $1 Every Time You Said No? | superpower | S&P 500 (Shiller) |
| 02 | What If You Started Investing at 18 Instead of 30? | two timelines | S&P 500 |
| 03 | What If You Only Paid the Minimum on Your Credit Card? | two timelines | FRED TERMCBCCALLNS (APR) |
| 04 | What If You Kept $10,000 Under Your Mattress Since 2000? | two timelines | FRED CPIAUCSL, euro HICP, gold, S&P |
| 05 | What If You Bought Bitcoin Instead of an iPhone in 2015? | two timelines | FRED CBBTCUSD |
| 06 | What If Price Tags Showed Hours of Your Life? | superpower | FRED CES0500000003 (wage) |
| 07 | What If You Never Bought a New Car? | two timelines | FRED new/used car CPI, S&P |
| 08 | What If Your Salary Doubled and You Stayed Broke? | story | FRED PSAVERT |
| 09 | What If Everything Went Wrong in the Same Month? | two timelines | FRED APR |
| 10 | What If You Invested on the Worst Day in History? | two timelines | S&P 500 (Oct 2007 peak) |

## Pipeline
`finance_series/engine/` = shared kit (characters, locations, props, charts, captions, music, thumbnails,
shorts). `finance_series/epNN/script.py` = beats with declarative scenes. `build.py epNN` renders all.
Publish queue: `finance_series/QUEUE.md`, worked by a scheduled task twice a day.

## Status (26.11, 13:00 Warsaw)
- EP01-EP10 written from real data, narrated (Piper), rendered 7.9-8.1 min, each with a Short (30-45 s) and 2 thumbnails.
- EP07 topic changed from "never bought a new car" to "house 2006 vs 2012" (car prices had no reliable dataset; housing has Case-Shiller + Freddie Mac).
- QA done per episode via contact sheets (see skills/episode-qa). Fixes made: chart side panel cropped by camera zoom
  (all chart beats re-rendered), y-axis labels, Anton missing glyphs (≠, →), EP04 single end date, EP05 key-date values.
- Publishing: QUEUE.json + scheduled task (14:02 / 18:02 Warsaw). EP01 long goes out 26.11 18:00.

## Notes 27.11.2026 (from stats)
- Shorts are the only traffic source right now (100-140 views each); long videos 0-4 views.
- Ideas: pin the "Full video" link as first comment on each Short (manual), add an end-screen to longs (manual),
  consider 2-3 extra Shorts per long episode (more entry points) instead of 1, and test a stronger first frame on longs.
