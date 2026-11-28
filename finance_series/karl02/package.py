"""Writes PACKAGE.md for Karl #02 with chapter times taken from build/ep_timing.json. python3 package.py"""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__)); TM = json.load(open(os.path.join(HERE, "build", "ep_timing.json"))); L = TM["lines"]
CH = [(0, "11:58 on Black Friday"), (16, "The power: you see the real price"), (22, "At first, it's amazing"), (49, "Then it gets bigger (Real Price Guy)"),
      (69, "But you can't turn it off"), (75, "Max and the six plans"), (94, "January: $1,200 becomes ~7 years"), (104, "Mom's three plans"),
      (111, "Everything has a price tag"), (123, "10,000 people, one giant button"), (150, "One year later"), (168, "The one rule + your question")]
def mmss(t): return f"{int(t // 60)}:{int(t % 60):02d}"
chap = "\n".join(f"{mmss(0 if i == 0 else L[i][0])} {name}" for i, name in CH)
DESC = f"""Every "Pay in 4" button now shows you the REAL price: the whole number, the hours of your life it costs, and what it turns into if one payment slips. At first it's amazing. Then your best friend Max splits a $1,200 Black Friday cart into 24 "tiny" payments...

How would you use it? And what's the first thing you'd look at? 👇

Chapters
{chap}

Method (example story, real data; numbers on screen and in the voice-over are rounded)
- Karl's take-home pay is an EXAMPLE: $20 an hour. $120 = 6 hours, $400 = 20 hours, $1,200 = 60 hours.
- Max's cart is an EXAMPLE: $2,000 full price, 40% off = $1,200 = 6 plans x $200 = 24 payments of $50.
- Card: $1,200 at 21.19% APR (FRED TERMCBCCALLNS, Aug 2026, accounts assessed interest), minimum payment = 1% of balance + interest, at least $25: 87 months (~7 years), $1,072 interest, $2,272 total (shown as ~$2,270), more than the $2,000 full price.
- Dad's truck: $499 x 72 months = $35,928 (~$36,000), example.
- Facts: CFPB (Jan 2025) found 63% of BNPL borrowers had more than one loan at the same time ("about 6 in 10"). LendingTree survey: 41% of BNPL users paid late in the past year (2025); 47% in the 2026 update ("almost half"). Adobe: about $20 billion spent with BNPL in the 2025 holiday season.

Sources
- CFPB, "Consumer Use of Buy Now, Pay Later and Other Unsecured Debt" (Jan 2025)
- LendingTree BNPL survey (2025) and 2026 update
- Adobe Digital Insights, 2025 holiday season recap (Jan 2026)
- FRED: TERMCBCCALLNS (Federal Reserve G.19)

This is a fictional story for education, not financial advice. No product, app or provider recommendations."""
LANG = {
 "es": ("¿Y si cada botón de «Paga en 4» te mostrara el precio real?", "Cada botón de «Paga en 4» te muestra el precio real: el total, las horas de tu vida y lo que pasa si se retrasa un pago. Historia de ficción con datos reales (CFPB, LendingTree, Adobe, FRED). No es asesoramiento financiero."),
 "pt-BR": ("E se todo botão de \"Pague em 4\" mostrasse o preço real?", "Todo botão de \"Pague em 4\" mostra o preço real: o total, as horas da sua vida e o que acontece se uma parcela atrasar. História fictícia com dados reais (CFPB, LendingTree, Adobe, FRED). Não é recomendação financeira."),
 "de": ("Was wäre, wenn jeder Ratenkauf-Knopf den echten Preis zeigt?", "Jeder „In 4 Raten zahlen\"-Knopf zeigt dir den echten Preis: die ganze Summe, Stunden deines Lebens und was passiert, wenn eine Rate ausfällt. Fiktive Geschichte mit echten Daten (CFPB, LendingTree, Adobe, FRED). Keine Finanzberatung."),
 "fr": ("Et si chaque bouton « Payez en 4 fois » montrait le vrai prix ?", "Chaque bouton « Payez en 4 fois » te montre le vrai prix : le total, les heures de ta vie et ce que ça devient si un paiement glisse. Histoire fictive, données réelles (CFPB, LendingTree, Adobe, FRED). Pas un conseil financier."),
 "uk": ("Що, якби кожна кнопка «Оплата частинами» показувала справжню ціну?", "Кожна кнопка «Оплата частинами» показує справжню ціну: усю суму, години твого життя і що буде, якщо один платіж зірветься. Вигадана історія з реальними даними (CFPB, LendingTree, Adobe, FRED). Не фінансова порада."),
}
md = f"""# Karl #02 — publishing package (remake of ep11 in the new "What If You...?" format; user publishes the long at 18:00 Warsaw)

**File:** `finance_series/karl02/KARL02_Pay_In_4_Real_Price.mp4` (16:9, {TM['dur']/60:.1f} min incl. 15 s end screen) · look: turquoise hoodie, no cap (log in VIDEOS.md)
**Thumbnails (Test & Compare):** `thumb_A.jpg` ("only $50" = $1,200) · `thumb_B.jpg` (-40% cost me more.. ~$2,270) · `thumb_C.jpg` (i didn't press it..)
**Captions:** `captions_en.srt` · **Audio tracks (Studio -> Languages -> Add audio track):** `audio/es.m4a`, `audio/pt-BR.m4a`, `audio/de.m4a`, `audio/fr.m4a`, `audio/uk.m4a`
**Trailer:** `TRAILER_karl02.mp4` (28 s, for Community/Shorts teaser)

## Title (47 chars)
What If Every "Pay in 4" Button Showed the Real Price?

A/B title variants: `What If You Could See the Real Price of Everything?` · `What If "Pay in 4" Told You the Truth?`

## Description
{DESC}

## Tags
what if, what if you, buy now pay later, BNPL, pay in 4, black friday, cyber monday, real price, credit card debt, minimum payment, credit card interest, personal finance, money, budgeting, animation, story, the other timeline, karl

## First comment (pin it)
If every "Pay in 4" button showed you the real price... what's the FIRST thing you'd look at? 👇

## End screen (last 15 s, set in Studio)
Left: "What If You Could See Everyone's Bank Account?" (Karl #01) when published, else the best recent video. Right: best for viewer. Subscribe in the centre.

## Translated titles and descriptions (Studio -> Languages -> Add translation)
""" + "\n".join(f"- **{k}**: {t}\n  {d}" for k, (t, d) in LANG.items()) + """

## Shorts (2; topic is broad with two strong hooks; each links to the full video)
- `short1_button_told_the_truth.mp4` — cold open: "Pay in 4: just $30" flips to "$120 · 6 hours of your life". Title: `The "Pay in 4" Button Told Him the Truth #shorts`
- `short2_minus40_cost_more.mp4` — Max: $1,200 in 24 payments -> card at ~21% -> ~7 years, ~$2,270. Title: `"-40% Off" Cost Him MORE Than Full Price #shorts`

## QA
See the QA section below (episode-qa).
"""
open(os.path.join(HERE, "PACKAGE.md"), "w").write(md); print(chap)
