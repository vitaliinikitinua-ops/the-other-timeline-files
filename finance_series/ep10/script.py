"""EP10 — What If You Invested at the Worst Possible Moment?  (timelines)
S&P 500 monthly average price (Shiller), price only, dividends excluded.
Oct 2007 (pre-crisis top, 1539.66) -> Mar 2009 low 757.13 (-51%) -> back above in Mar 2013 -> Sep 2026: $10,000 -> $49,812.
Bought at the Mar 2009 low: $10,000 -> $101,296. Spread over 12 months from Oct 2007: $56,350.
$100/month from Oct 2007: $22,800 put in -> $84,366.
Aug 2000 top: back above in May 2007; $10,000 -> $51,630 by Sep 2026.
Sep 1929 top 31.30 -> Jun 1932 4.77 (-85%), price back above only in Sep 1954 (dividends excluded)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
from kit import *  # noqa
import data

SP = data.sp500()
KS = [k for k in sorted(SP) if "2007-10" <= k <= "2026-09"]
LUMP = [10000 * SP[k] / SP["2007-10"] for k in KS]
FLAT = [10000.0] * len(KS)
ks2, INV, VAL = data.dca(SP, "2007-10", "2026-09", 100)
iLow = KS.index("2009-03"); iRec = KS.index("2013-03")
BOTTOM = [0.0] * iLow + [10000 * SP[k] / SP["2009-03"] for k in KS[iLow:]]
YEARS = [(i, k[:4]) for i, k in enumerate(KS) if k.endswith("-01") and int(k[:4]) % 3 == 2]
K29 = [k for k in sorted(SP) if "1927-01" <= k <= "1956-12"]
P29 = [SP[k] for k in K29]

SPEED = 1.18
MUSIC_SEED = 10
END_LINE = "TIME IN, NOT TIMING"

def you(x=960, emo="neutral", size=330, **k):
    return dict(who="you", x=x, y=k.pop("y", 1010), size=size, emo=emo, **k)

BEATS = [
 ("hook", [
   ("What if you were the unluckiest investor alive?", None),
   ("You finally invest all your savings, and the very next month, the worst financial crisis in eighty years begins.", None),
   ("Within a year and a half, half your money is gone.", None),
   ("This really happened to millions of people in October two thousand seven. So today, we follow one of them to the end.", None),
   ("And the ending might be the most surprising number in this whole series.", None),
 ], dict(type="stage", loc="void_red", actors=[you(1500, {0: "neutral", 1: "shock", 2: "sad", 4: "worried"})],
         props=[dict(kind="calendar", top="2007", big="OCT", x=650, y=420, at=1, scale=1.1)],
         texts=[dict(text="-51%", size=220, col=CORAL, x=650, y=780, at=2, glow=20)], flash={2: CORAL}, shake=[2])),
 ("inherit", [
   ("October twenty oh seven. Grandma gives you ten thousand dollars. Do something smart with it, sweetheart.", None),
   ("Everyone says the market is doing great. Stocks are at record highs. Your banker smiles a lot.", None),
   ("So you put all ten thousand dollars into an S and P five hundred index fund. In one go.", None),
   ("Without knowing it, you just bought at the top before the global financial crisis.", None),
 ], dict(type="stage", loc="bank", actors=[you(560, {0: "happy", 2: "smug", 3: "neutral"}), dict(who="grandma", x=1000, y=1010, size=280, emo="happy", until=0.95, talk=[0]), dict(who="banker", x=1450, y=1010, size=320, emo="happy", flip=True)],
         props=[dict(kind="bill", amount="10,000", x=1000, y=520, at=0, scale=1.1, rot=-6), dict(kind="tag", text="ALL-TIME HIGH", col=GREEN, x=1000, y=320, at=1, scale=1.0)],
         bubbles=[dict(text="Do something smart with it!", x=1000, y=520, at=0, until=1)], flash={3: CORAL}, shake=[3])),
 ("crash", [
   ("And then it begins. Banks wobble. Then they fall.", None),
   ("Every month, your ten thousand dollars gets smaller. Nine thousand. Seven thousand. Six.", None),
   ("By March two thousand nine, the index's average price is fifty one percent below where you bought.", None),
   ("Your ten thousand dollars is worth about four thousand nine hundred.", None),
   ("Grandma's gift, cut in half, in seventeen months.", None),
 ], dict(type="chart", reveal=(0, 2), series=[dict(values=LUMP[:iLow + 1], col=CORAL, width=9, fill=True), dict(values=FLAT[:iLow + 1], col=CREAM, width=4)], vmax=12000,
         xlabels=[(0, "OCT 2007"), (iLow, "MAR 2009")], side=[dict(label="YOUR $10,000", values=LUMP[:iLow + 1], col=CORAL)],
         footnote="S&P 500 monthly avg. price (R. Shiller). Price only, dividends excluded. Not financial advice.",
         notes=[dict(i=iLow, text="-51%", col=CORAL, dy=-120, dx=-90, size=90)], actors=[dict(who="you", x=1650, y=1070, size=150, emo={0: "worried", 3: "sad"})], flash={2: CORAL}, shake=[2])),
 ("news", [
   ("To understand why selling felt so reasonable, remember what the world looked like in early two thousand nine.", None),
   ("Every news channel showed red arrows. Huge companies were being rescued. People were losing jobs and homes.", None),
   ("Nobody on television was saying, this is a great time to stay calm. It felt like the end.", None),
   ("That's the thing about the bottom. It never looks like the bottom while you're in it. It looks like the beginning of something worse.", None),
 ], dict(type="stage", loc="living", actors=[you(560, {0: "neutral", 1: "worried", 2: "shock", 3: "sad"})],
         props=[dict(kind="icon", name="tv", x=1300, y=500, at=0, scale=1.2), dict(kind="tag", text="MARKETS PLUNGE", col=CORAL, x=1300, y=250, at=1, scale=0.9), dict(kind="icon", name="warning", x=1300, y=760, at=2, scale=0.5)],
         texts=[dict(text="THE BOTTOM NEVER LOOKS LIKE THE BOTTOM", size=72, col=AMBER, y=150, at=3, glow=10)], shake=[2])),
 ("split", [
   ("And here, at the very bottom, the timeline splits.", None),
   ("In timeline A, you can't take it anymore. You sell everything and keep the cash. Four thousand nine hundred dollars, safe forever.", None),
   ("In timeline B, you're scared, but you do nothing. You leave it there and try not to look.", None),
   ("Most people believe they'd be timeline B. In two thousand nine, a lot of real people chose timeline A.", None),
 ], dict(type="split", left=dict(title="TIMELINE A", sub="sells at the bottom", col=CORAL, who="you", emo="shock", value=dict(**{"from": 10000, "to": 4918}, at=1, dur=1.4, label="locked in")),
         right=dict(title="TIMELINE B", sub="does nothing", col=TEAL, who="you", emo="worried", at=2),
         texts=[dict(text="SELL OR SIT?", size=110, col=AMBER, y=800, at=3, glow=12)])),
 ("wait", [
   ("Timeline B waits. Two thousand nine. Twenty ten. Twenty eleven. Still under water.", None),
   ("Friends say you should've put it in a savings account. Max says you should've bought gold. Max says a lot of things.", None),
   ("In March twenty thirteen, five and a half years after you bought, the average price finally climbs back above the October twenty oh seven level.", None),
   ("You're back to ten thousand dollars. Five and a half years to get back to zero.", None),
 ], dict(type="chart", reveal=(0, 2), p0=iLow / iRec, series=[dict(values=LUMP[:iRec + 1], col=TEAL, width=9, fill=True), dict(values=FLAT[:iRec + 1], col=CREAM, width=4)], vmax=13000,
         xlabels=[(0, "2007"), (iLow, "2009"), (iRec, "2013")], side=[dict(label="TIMELINE B", values=LUMP[:iRec + 1], col=TEAL)],
         notes=[dict(i=iRec, text="BACK TO $10K", col=GREEN, dy=-110, dx=-120, size=56)], actors=[dict(who="max", x=1650, y=1070, size=150, emo="smug")])),
 ("climb", [
   ("And then, nobody rings a bell. It just keeps climbing.", None),
   ("Twenty sixteen. Twenty twenty, with a scary drop. Twenty twenty two, another one. Timeline B keeps not looking.", None),
   ("By September twenty twenty six, the unluckiest investment of the decade is worth about forty nine thousand eight hundred dollars.", None),
   ("Price only. Dividends would make it noticeably more.", None),
   ("Bought at the worst possible moment, and still almost five times the money.", None),
 ], dict(type="chart", reveal=(0, 2), p0=iRec / len(KS), series=[dict(values=LUMP, col=TEAL, width=9, fill=True), dict(values=FLAT, col=CREAM, width=4)],
         xlabels=YEARS, side=[dict(label="TIMELINE B", values=LUMP, col=TEAL)], footnote="S&P 500 monthly avg. price (R. Shiller). Price only, dividends excluded. Not financial advice.",
         texts=[dict(text="WORST TIMING: ~5x", size=110, col=GREEN, x=760, y=170, at=4, glow=14)], actors=[dict(who="you", x=1650, y=1070, size=150, emo={0: "neutral", 2: "shock", 4: "money"})], flash={4: GREEN})),
 ("dividends", [
   ("Quick note, because it matters. All the numbers in this series use price only.", None),
   ("But many of the companies inside an index also pay dividends. A small share of their profits, paid to the people who own the shares.", None),
   ("In a typical index fund, those dividends get reinvested automatically and buy even more shares.", None),
   ("We left them out to keep the math simple and conservative. So every real timeline B in this series would likely have ended up with more, not less.", None),
   ("Boring money, quietly paying you to wait.", None),
 ], dict(type="stage", loc="void_teal", actors=[you(1500, {0: "neutral", 3: "smug", 4: "happy"})],
         props=[dict(kind="coin", x=520, y=520, at=1, scale=0.7), dict(kind="coin", x=700, y=460, at=1.4, scale=0.5), dict(kind="tag", text="PRICE ONLY = CONSERVATIVE", col=AMBER, x=650, y=760, at=3, scale=0.9)],
         texts=[dict(text="DIVIDENDS", size=140, col=TEAL, y=170, at=1, glow=16)])),
 ("a_now", [
   ("And timeline A, who sold at the bottom? Still about four thousand nine hundred dollars, plus whatever the bank paid in interest.", None),
   ("The crash didn't destroy timeline A's money. Selling did. The loss only became permanent the day it was locked in.", None),
   ("Same day bought. Same crash. One ends with about forty nine thousand eight hundred, the other with about four thousand nine hundred.", None),
 ], dict(type="bars", groups=[dict(label="A: SOLD IN 2009", vals=[(4918, CORAL)], at=0), dict(label="B: DID NOTHING", vals=[(LUMP[-1], TEAL)], at=2)],
         texts=[dict(text="THE CRASH DIDN'T DO IT. SELLING DID.", size=72, col=AMBER, y=150, at=1, glow=10)], flash={2: TEAL})),
 ("max_timer", [
   ("And then there's Max. Max invested ten thousand dollars on the same day. But Max has a plan.", None),
   ("I'll sell before it gets worse, and buy back in at the bottom. Easy.", None),
   ("In October twenty oh eight, Max sells. His ten thousand dollars is about six thousand three hundred. Then he waits for the perfect moment to get back in.", None),
   ("Prices go up, and he waits for a dip. Prices dip, and he waits for a bigger dip. Years go by.", None),
   ("Max finally buys back in January twenty twenty one. By September twenty twenty six, his ten thousand dollars is worth about twelve thousand seven hundred.", None),
   ("Timeline B, who did absolutely nothing, has almost four times as much.", None),
 ], dict(type="stage", loc="street", actors=[dict(who="max", x=620, y=1010, size=330, emo={0: "smug", 2: "money", 3: "worried", 4: "sad"}, talk=[1]), you(1350, {0: "neutral", 5: "smug"}, flip=True)],
         bubbles=[dict(text="Sell high, buy the bottom. Easy.", x=620, y=500, at=1, until=2)],
         props=[dict(kind="tag", text="SOLD OCT 2008: $6,292", col=CORAL, x=1000, y=300, at=2, scale=0.8), dict(kind="tag", text="BOUGHT BACK JAN 2021", col=AMBER, x=1000, y=450, at=4, scale=0.8), dict(kind="tag", text="MAX: $12,720", col=CORAL, x=1000, y=600, at=4.5, scale=0.9), dict(kind="tag", text="B: $49,812", col=TEAL, x=1000, y=750, at=5, scale=0.9)],
         texts=[dict(text="WAITING FOR THE PERFECT DIP", size=86, col=AMBER, y=150, at=3, glow=10)], flash={5: TEAL})),
 ("lucky", [
   ("Now, for fun, imagine timeline C. A version of you with a time machine, who buys at the exact bottom in March two thousand nine.", None),
   ("That perfect investor turns ten thousand dollars into about one hundred and one thousand.", None),
   ("Impressive. But nobody can do that on purpose. In March two thousand nine, it felt like the end of the world, not like a sale.", None),
   ("The interesting part isn't the perfect investor. It's that the worst investor still did fine, by simply staying.", None),
 ], dict(type="bars", groups=[dict(label="A: SOLD", vals=[(4918, CORAL)], at=0), dict(label="B: WORST DAY", vals=[(LUMP[-1], TEAL)], at=0), dict(label="C: PERFECT DAY", sub="needs a time machine", vals=[(101296, PURPLE)], at=1)],
         texts=[dict(text="NOBODY CAN DO C ON PURPOSE", size=80, col=CREAM, y=150, at=2, glow=10)])),
 ("monthly", [
   ("And there's a fourth timeline, the boring one.", None),
   ("Instead of a lump sum, you invest one hundred dollars every month starting in October twenty oh seven. Through the crash, through everything.", None),
   ("During the crash, every hundred dollars buys more shares, because prices are low. Without trying, you buy cheap.", None),
   ("By September twenty twenty six, you've put in twenty two thousand eight hundred dollars. And it's worth about eighty four thousand.", None),
 ], dict(type="chart", reveal=(1, 3), series=[dict(values=VAL, col=GREEN, width=9, fill=True), dict(values=INV, col=AMBER, width=6)],
         xlabels=YEARS, side=[dict(label="PUT IN", values=INV, col=AMBER), dict(label="WORTH", values=VAL, col=GREEN)],
         footnote="$100 on the 1st of each month from Oct 2007, S&P 500 monthly avg. price (R. Shiller), price only.", actors=[dict(who="you", x=1650, y=1070, size=150, emo={0: "neutral", 3: "happy"})])),
 ("spread", [
   ("One more version. What if, instead of putting all ten thousand in at once, you'd split it into twelve equal parts, one per month, starting in October twenty oh seven?", None),
   ("You'd still be buying right into the crisis. But each month, as prices fall, your money buys a little more.", None),
   ("By September twenty twenty six, that version has about fifty six thousand three hundred dollars. More than the all-at-once version.", None),
   ("It's not always better. When markets rise steadily, investing all at once usually wins. But spreading it out makes bad timing hurt less, and it's much easier on the nerves.", None),
 ], dict(type="bars", groups=[dict(label="ALL AT ONCE", sub="Oct 2007", vals=[(LUMP[-1], TEAL)], at=0), dict(label="SPLIT OVER 12 MONTHS", sub="from Oct 2007", vals=[(56350, GREEN)], at=2)],
         texts=[dict(text="EASIER ON THE NERVES", size=96, col=GREEN, y=150, at=3, glow=12)])),
 ("not_always", [
   ("Now, the uncomfortable truth. It doesn't always go this fast.", None),
   ("If you'd bought at the top in August two thousand, it took until May two thousand seven to get back. And then the next crash hit right away.", None),
   ("And the scariest one: September nineteen twenty nine. The average price fell about eighty five percent by June nineteen thirty two.", None),
   ("Counting price only, it took until nineteen fifty four to get back. Twenty five years. Dividends made the real recovery faster, but it was still brutal.", None),
   ("So staying calm only works if the money can stay for a long time.", None),
 ], dict(type="chart", reveal=(2, 3), series=[dict(values=P29, col=CORAL, width=8, fill=True)], vmax=40, yfmt="{:.0f}",
         xlabels=[(i, k[:4]) for i, k in enumerate(K29) if k.endswith("-01") and int(k[:4]) % 5 == 0], side=[dict(label="S&P (1929 TO 1956)", values=P29, col=CORAL, fmt="{:.2f}")],
         footnote="S&P composite monthly avg. price (R. Shiller), price only. Not financial advice.", texts=[dict(text="-85%", size=150, col=CORAL, x=760, y=170, at=2, glow=16)],
         actors=[dict(who="you", x=1650, y=1070, size=150, emo={0: "worried", 3: "shock"})])),
 ("lessons", [
   ("So what does the unluckiest investor teach us?", None),
   ("One. Timing is mostly luck. Time in the market is what you actually control.", None),
   ("Two. A crash only becomes a permanent loss when you sell. So only invest money that can stay put for many years.", None),
   ("Three. Investing a fixed amount every month takes the guessing out, and buys more when prices are low.", None),
   ("Four. Spread your risk. One country, one sector or one company can have its own nineteen twenty nine.", None),
 ], dict(type="list", title="WHAT THE UNLUCKIEST INVESTOR TEACHES", items=[dict(text="Timing is luck, time is control", at=1), dict(text="Losses lock in when you sell", at=2), dict(text="Fixed monthly amount, no guessing", at=3), dict(text="Spread the risk", at=4)],
         actors=[you(1690, {0: "neutral", 4: "smug"}, size=240, y=1040)])),
 ("grandma", [
   ("In twenty twenty six, you visit Grandma and tell her the whole story.", None),
   ("The crash, the panic, the five years of waiting, and the almost fifty thousand dollars.", None),
   ("She nods and says: I told you to do something smart with it. I never said fast.", None),
 ], dict(type="stage", loc="kitchen", actors=[you(620, {0: "neutral", 1: "happy"}), dict(who="grandma", x=1350, y=1010, size=320, emo={0: "neutral", 2: "smug"}, flip=True, talk=[2])],
         bubbles=[dict(text="I never said FAST.", x=1350, y=500, at=2)])),
 ("honest", [
   ("And the honest part. This is not financial advice.", None),
   ("These are real past prices, but there's no promise the future looks like the past. Some crashes take decades to recover.", None),
   ("Fees, taxes and dividends aren't included. Think about your own time horizon and risk before you invest.", None),
 ], dict(type="list", title="NOT FINANCIAL ADVICE", tcol=CORAL, items=[dict(text="Past prices, no promise", at=1), dict(text="Some recoveries take decades", at=1.4), dict(text="Fees, taxes, dividends not included", at=2)],
         actors=[you(1680, "neutral", size=240, y=1040)])),
 ("outro", [
   ("The worst possible day to invest. And still, almost five times the money, for the one who didn't run.", None),
   ("Tell me in the comments: in March two thousand nine, would you have sold, or held?", None),
   ("And I'll see you in the other timeline.", None),
 ], dict(type="end", q1="SELL OR HOLD", q2="IN 2009?", comment="Sold or held?", comment_at=1, emo={0: "neutral", 1: "smug"})),
]

META = dict(
    file="EP10_Worst_Day_to_Invest.mp4",
    title="What If You Invested at the Worst Possible Moment?",
    description="""October 2007: you invest $10,000 right before the global financial crisis. Half of it disappears in 17 months. One version of you sells at the bottom. The other does nothing. Then the most surprising number of the series, plus the crashes that took far longer to recover.

Data: S&P 500 / S&P composite monthly average price (Robert Shiller data), price only, dividends excluded, no fees or taxes.
This video is for education and entertainment only. It is not financial advice. Past performance does not guarantee future results.

#whatif #investing #personalfinance""",
    tags=["what if", "worst time to invest", "market timing", "2008 financial crisis", "stock market crash", "time in the market", "dollar cost averaging", "1929 crash", "s&p 500", "personal finance", "the other timeline", "animated story"],
    comment="March 2009, your $10,000 is now $4,900. Be honest: sell or hold? 👇",
    chapters={"hook": "The unluckiest investor", "inherit": "October 2007", "crash": "The crash", "news": "Why selling felt right", "split": "Sell or sit?", "wait": "5.5 years to get back", "climb": "The climb",
              "dividends": "The part we left out", "a_now": "The one who sold", "max_timer": "Max times the market", "lucky": "The perfect investor", "monthly": "The boring timeline", "spread": "Split it over 12 months", "not_always": "It's not always this fast", "lessons": "4 lessons",
              "grandma": "Grandma's verdict", "honest": "The honest part", "outro": "Sell or hold?"},
)

THUMBS = {
    "A": dict(loc="void_red", quote="i invested at the WORST time..", hl=["WORST"], actors=[dict(who="you", x=480, size=560, emo="shock"), dict(who="grandma", x=1480, size=500, emo="smug", flip=True)],
              big=dict(text="-51%", x=980, y=430, col=CORAL, size=240)),
    "B": dict(loc="void_teal", quote="worst timing ever.. then", hl=["then"], actors=[dict(who="you", x=480, size=560, emo="money")],
              props=[dict(kind="icon", name="chart", x=1350, y=680, scale=1.2)], big=dict(text="$49,812", x=1300, y=360, col=GREEN, size=180)),
}

SHORT = dict(segs=[("crash", [2, 3]), ("split", [1, 2]), ("climb", [2, 4]), ("a_now", [1])], title=["HE INVESTED AT", "THE WORST MOMENT"], hook=dict(text="-51%", col=CORAL, dur=1.6),
             yt_title="He Invested Right Before the 2008 Crash #shorts",
             yt_desc="$10,000 in the S&P 500 in October 2007, real Shiller prices. Sell at the bottom or hold? Full video on the channel. Not financial advice. #investing #whatif")
