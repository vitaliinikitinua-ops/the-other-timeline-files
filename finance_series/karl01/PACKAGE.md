# KARL01 / Video K1: publishing package (the user publishes the long video at 18:00 Warsaw)

**File:** `finance_series/karl01/KARL01_See_Everyones_Bank_Account.mp4` (16:9, ~9.2 min incl. 15 s end screen, 3D toon style, Karl without the cap, turquoise hoodie)
**Thumbnails (Test & Compare):** `thumb_A.jpg` ("nice shoes." $3.12) · `thumb_B.jpg` ("just my little pension" $1,284,900) · `thumb_C.jpg` ("business is great" -$2,300)
**Captions:** `captions_en.srt` (+ `captions_es/pt-BR/de/fr/uk.srt`)
**Audio tracks (YouTube Studio -> Languages -> Add audio track):** `audio/es.m4a`, `audio/pt-BR.m4a`, `audio/de.m4a`, `audio/fr.m4a`, `audio/uk.m4a`
(dubbed with Piper, each line placed on the English timing; same music and SFX bed)
**Hero look (A/B log):** turquoise hoodie, no cap.

## Title
What If You Could See Everyone's Bank Account?

A/B title variants: `I Could See Everyone's Bank Account (It Ruined Everything)` · `What If Everyone's Balance Floated Over Their Head?`

## Description
Your best friend brags about $200 sneakers. Then you see the number floating over his head: $3.12.

What if you could see what everyone really has, today, right now? At first it's amazing. Then you start sorting people, you hurt your best friend, and you finally see your own number.

Would you want this power? Whose number would you look at first? 👇

Chapters
0:00 The $200 sneakers
0:33 The power
0:45 At first, it's amazing
2:25 Then it gets bigger
3:32 The $400 question
4:03 But you can't stop seeing
5:40 The class trip
6:26 800 kids, 800 numbers
7:50 The jar
8:51 Would you want it?

Method (example story, real data; numbers on screen are rounded)
- All characters and their balances are invented for the story.
- Janitor example: $200 a month for 40 years at 6% a year (monthly compounding) = $398,298, shown as "almost $400K". Past returns are not a promise.
- "$400 surprise bill": 63% of adults would cover it with cash or its equivalent, so about 4 in 10 would not (Federal Reserve, Economic Well-Being of U.S. Households in 2025, published May 2026).
- "Average vs middle": mean family net worth $1,063,700, median $192,900 (Federal Reserve, Survey of Consumer Finances 2022).
- Lottery neighbours: a bigger lottery win raises the bankruptcy rate of the winner's close neighbours (Agarwal, Mikhed & Scholnick, "Peers' Income and Financial Distress: Evidence from Lottery Winners and Neighboring Bankruptcies", Review of Financial Studies, 2020; Philadelphia Fed working paper).

Sources
- Federal Reserve Board, Economic Well-Being of U.S. Households in 2025 (SHED)
- Federal Reserve Board, Survey of Consumer Finances 2022
- Agarwal, Mikhed, Scholnick, Review of Financial Studies 33(1), 2020

This video is education and entertainment, not financial advice.

## Tags
what if, what if you could, bank account, see everyone's bank account, money, personal finance, keeping up with the joneses, comparison, social media rich, net worth, average vs median, emergency fund, 400 dollar emergency, saving money, money for teens, animated story, the other timeline, karl

## First comment (pin it)
Be honest: whose number would you check first? Your best friend, your parents, or your crush? 👇

## End screen (last 15 s, set in Studio)
Left box: latest Karl video (or "Black Friday's Most Expensive Button"). Right box: best for viewer. Subscribe button centre-bottom.

## Shorts from this video (2: broad topic, many hooks; each links to the full video)
1. `KARL01_short_312.mp4`: "He bragged about $200 shoes..." (cold open, $3.12 reveal)
2. `KARL01_short_400.mp4`: "Could you pay $400 today?" (4 in 10, average vs middle)
Both are in `../SHORTS_QUEUE.json` (status pending).

## QA (episode-qa, 28.11.2026)
Checked:
- Numbers: janitor example recomputed in `ep.py numbers()` = $398,298 ("almost $400K", labelled EXAMPLE on screen);
  SHED 2025 63% -> "about 4 in 10"; SCF 2022 mean $1,063,700 / median $192,900 -> "~$1.06M" / "~$193K"; lottery study
  phrased as in the paper. All other balances are story numbers. Disclaimer in the description.
- Visuals: contact sheets of all 179 lines before the full render (fixed: cameras inside heads, over-the-shoulder shots,
  classroom orientation, mirror shot, assembly wide shot), then 1 frame every 15 s of the final file: no broken frames.
- File: 9:11 (551 s incl. 15 s end screen), 94.8 MB (grain removed with a denoise pass to stay under 100 MB),
  loudness -15.4 LUFS integrated (target about -14; acceptable).
- Audio tracks: 5 x 551.3 s, same length as the video. Each dubbed line starts with the English line and is sped up
  (max 1.35x) only when it would run into the next one.
- Thumbnails A/B/C viewed at full size; quote readable, one yellow word, number not covering faces.
- Shorts: 42.8 s and 35.3 s, hook headline from frame 1, CTA "FULL VIDEO ON THE CHANNEL" in the last 3 s.
Not checked: nobody listened to the full English or dubbed tracks end to end (only the timing and lengths were checked).
The dubbed voices are free Piper voices; female characters in pt-BR use a pitched male voice (no free pt-BR female voice).
