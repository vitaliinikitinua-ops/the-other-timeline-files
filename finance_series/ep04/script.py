"""EP04 — What If You Hid $10,000 Under Your Mattress in 2000?  (three timelines: cash / gold / S&P 500)
Data: US CPI-U (FRED CPIAUCSL), euro area HICP (FRED CP0000EZ19M086NEST), monthly gold price (github.com/datasets/gold-prices),
S&P 500 monthly avg price (Shiller; price only, dividends excluded). Start Jan 2000.
All values at Sep 2026. Cash: $10,000 buys like $5,034 of Jan-2000 goods (prices x1.99). Euro: like EUR 5,577.
Gold: $10,000 -> $152,077 ($4,319/oz); peak Sep 2011 $1,772/oz -> Dec 2015 $1,076 (-39%).
S&P 500: $10,000 -> $53,798 (Sep 2026, price only); Mar 2009 $5,311; Jan 2013 $10,384.
Start Jan 2010 instead: gold -> $36,717, S&P -> $68,259, cash power -> $6,445.
Real (2000 dollars): gold ~$72,500, S&P ~$27,000 (price only)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
from kit import *  # noqa
import data

CPI = data.fred("CPIAUCSL"); G = data.gold(); SP = data.sp500()
if "2025-10" not in CPI:  # BLS published no October 2025 CPI (government shutdown); interpolate for the chart only
    CPI["2025-10"] = (CPI["2025-09"] + CPI["2025-11"]) / 2
KS = [k for k in sorted(SP) if "2000-01" <= k <= "2026-09"]
CASH_REAL = [10000 * CPI["2000-01"] / CPI[k] for k in KS]
GOLD = [10000 * G[k] / G["2000-01"] for k in KS]
STOCK = [10000 * SP[k] / SP["2000-01"] for k in KS]
FLAT = [10000.0] * len(KS)
YEARS = [(i, k[:4]) for i, k in enumerate(KS) if k.endswith("-01") and int(k[:4]) % 4 == 0]
i09 = KS.index("2009-03"); i11 = KS.index("2011-09"); i15 = KS.index("2015-12")

SPEED = 1.18
MUSIC_SEED = 4
END_LINE = "WHERE WOULD YOU HIDE IT?"

def you(x=960, emo="neutral", size=330, **k):
    return dict(who="you", x=x, y=k.pop("y", 1010), size=size, emo=emo, **k)

BEATS = [
 ("hook", [
   ("What if you hid ten thousand dollars under your mattress in the year two thousand, and didn't touch it for twenty six years?", None),
   ("Nobody steals it. Nobody spends it. Every single bill is still there.", None),
   ("You count it in twenty twenty six, and it's exactly ten thousand dollars. To the cent.", None),
   ("And yet, it would have lost half of its value.", None),
   ("Today, three versions of you hide the same ten thousand dollars in three different places.", None),
   ("One of them ends up with more than fifteen times the money. And it's not the one you'd guess.", None),
 ], dict(type="stage", loc="bedroom", actors=[you(1450, {0: "neutral", 3: "shock", 5: "smug"})],
         props=[dict(kind="icon", name="mattress", x=650, y=700, at=0, scale=1.6), dict(kind="bill", amount="10,000", x=650, y=560, at=0, scale=1.1, rot=-6)],
         texts=[dict(text="-50%", size=200, col=CORAL, x=650, y=280, at=3, glow=20), dict(text="15x?", size=170, col=GREEN, x=1450, y=280, at=5, glow=18)],
         flash={3: CORAL}, shake=[3])),
 ("win", [
   ("It's January two thousand. The world didn't end at midnight, and you just won ten thousand dollars in a radio contest.", None),
   ("Everyone has an opinion about what to do with it.", None),
   ("Grandma says: cash. Under the mattress. Banks can fail. Cash is cash.", None),
   ("Max's uncle says: gold. Gold is real money. It's been around for thousands of years.", None),
   ("And the man at the bank says: an index fund that tracks the S and P five hundred.", None),
 ], dict(type="stage", loc="living", actors=[you(420, {0: "happy", 1: "worried"}), dict(who="grandma", x=900, y=1010, size=280, emo="neutral", at=2, talk=[2]),
                                              dict(who="max", x=1250, y=1010, size=280, emo="smug", at=3, talk=[3]), dict(who="banker", x=1600, y=1010, size=280, emo="happy", at=4, flip=True, talk=[4])],
         props=[dict(kind="calendar", top="2000", big="JAN", x=420, y=300, at=0, until=1.9, scale=0.8), dict(kind="icon", name="mattress", x=900, y=380, at=2, scale=0.6), dict(kind="icon", name="gold", x=1250, y=380, at=3, scale=0.6), dict(kind="icon", name="chart", x=1600, y=380, at=4, scale=0.6)],
         texts=[dict(text="$10,000", size=130, col=GREEN, x=420, y=180, at=0, until=1.9, glow=14)])),
 ("rules", [
   ("So the timeline splits into three.", None),
   ("Timeline A keeps the cash. Timeline B buys gold. Timeline C buys the index fund.", None),
   ("Nobody adds a cent. Nobody sells. We just open the box in twenty twenty six.", None),
   ("And we'll use real historical prices for all three. Including the parts that hurt.", None),
 ], dict(type="list", cards=True, title="THREE TIMELINES", items=[dict(text="A: CASH", sub="under the mattress", col=CREAM, at=1), dict(text="B: GOLD", sub="real metal", col=AMBER, at=1.3), dict(text="C: S&P 500", sub="index fund, price only", col=TEAL, at=1.6)],
         texts=[dict(text="2000 TO 2026 · NO TOUCHING", size=60, col=CREAM, y=880, at=2)])),
 ("inflation", [
   ("First, a quick reality check. Why would cash lose value if nobody touches it?", None),
   ("Because prices go up. It's called inflation.", None),
   ("In the US, the consumer price index measures the average price of a basket of things people buy. Food, rent, fuel, haircuts.", None),
   ("From January two thousand to September twenty twenty six, that basket became almost exactly twice as expensive.", None),
   ("So the same bill buys about half as much.", None),
 ], dict(type="stage", loc="store", actors=[you(1500, {0: "neutral", 3: "shock", 4: "sad"}, size=300)],
         props=[dict(kind="receipt", lines=[["Bread", "2000"], ["Fuel", "2000"], ["Rent", "2000"]], total="x1", x=520, y=520, at=2, until=2.9, scale=1.0),
                dict(kind="receipt", lines=[["Bread", "2026"], ["Fuel", "2026"], ["Rent", "2026"]], total="x1.99", x=900, y=520, at=3, scale=1.0)],
         texts=[dict(text="INFLATION", size=150, col=CORAL, y=170, at=1, glow=16), dict(text="PRICES x1.99", size=100, col=CORAL, x=900, y=860, at=3, glow=10)], flash={3: CORAL})),
 ("cash", [
   ("Timeline A. The mattress.", None),
   ("In twenty ten, you peek under it. Still ten thousand dollars. But it now buys what about seven thousand eight hundred bought in two thousand.", None),
   ("In twenty twenty, it buys like six thousand five hundred.", None),
   ("And by September twenty twenty six, your ten thousand dollars buys what about five thousand and thirty four dollars bought when you hid it.", None),
   ("You didn't lose a single bill. You lost half the money.", None),
 ], dict(type="chart", reveal=(0, 3), vmax=12000, series=[dict(values=FLAT, col=CREAM, width=5), dict(values=CASH_REAL, col=CORAL, width=9, fill=True)],
         xlabels=YEARS, side=[dict(label="BILLS IN THE BOX", values=FLAT, col=CREAM), dict(label="BUYS LIKE (2000 $)", values=CASH_REAL, col=CORAL)],
         footnote="Purchasing power of $10,000 in January-2000 dollars, US CPI-U (BLS via FRED CPIAUCSL).",
         texts=[dict(text="-50% WITHOUT SPENDING", size=90, col=CORAL, x=760, y=160, at=4, glow=12)], actors=[dict(who="you", x=1650, y=1070, size=150, emo={0: "neutral", 3: "sad"})])),
 ("euro", [
   ("And before anyone in Europe feels safe. The euro did the same thing, just a bit slower.", None),
   ("Ten thousand euros hidden in January two thousand would buy roughly what five and a half thousand euros bought back then.", None),
   ("And in many countries with higher inflation, cash melted much faster than that.", None),
   ("Cash is great for emergencies and next month's bills. As a twenty year plan, it slowly melts.", None),
 ], dict(type="stage", loc="void", actors=[you(1500, {0: "neutral", 1: "worried"})],
         props=[dict(kind="tag", text="EUR 10,000", col=TEAL, x=650, y=380, at=0, scale=1.1), dict(kind="tag", text="BUYS LIKE EUR 5,577", col=CORAL, x=650, y=600, at=1, scale=1.1, sub="euro area HICP, Jan 2000 to Sep 2026")],
         texts=[dict(text="CASH MELTS", size=140, col=CORAL, y=170, at=2, glow=16)])),
 ("gold_up", [
   ("Timeline B. Max's uncle and the gold.", None),
   ("In January two thousand, gold costs about two hundred and eighty four dollars an ounce. You buy a small, heavy pile.", None),
   ("And for ten years, the uncle looks like a genius. By twenty ten, your ten thousand dollars of gold is worth about thirty nine thousand.", None),
   ("By September twenty eleven, gold is over seventeen hundred dollars an ounce. Max's uncle buys a boat.", None),
 ], dict(type="chart", reveal=(0, 3), p0=0.0, series=[dict(values=GOLD[:i11 + 1], col=AMBER, width=9, fill=True)],
         xlabels=[(i, k) for i, k in YEARS if i <= i11], side=[dict(label="GOLD (TIMELINE B)", values=GOLD[:i11 + 1], col=AMBER)],
         footnote="Monthly gold price in USD (github.com/datasets/gold-prices). No storage costs or fees included.",
         actors=[dict(who="max", x=1650, y=1070, size=150, emo={0: "smug", 3: "money"})])),
 ("gold_down", [
   ("And then gold does something people forget it can do. It falls.", None),
   ("From September twenty eleven to December twenty fifteen, gold drops about thirty nine percent.", None),
   ("Four years of watching your pile shrink. The boat is for sale.", None),
   ("Gold doesn't pay interest or dividends. It just sits there and waits for someone to pay more for it.", None),
 ], dict(type="chart", reveal=(0, 1), p0=i11 / i15, series=[dict(values=GOLD[:i15 + 1], col=AMBER, width=9, fill=True)],
         xlabels=[(i, k) for i, k in YEARS if i <= i15], side=[dict(label="GOLD (TIMELINE B)", values=GOLD[:i15 + 1], col=AMBER)],
         notes=[dict(i=i15, text="-39%", col=CORAL, dy=-120, dx=-120, size=80)], actors=[dict(who="max", x=1650, y=1070, size=150, emo={0: "worried", 2: "sad"})],
         flash={1: CORAL}, shake=[1])),
 ("uncle_sells", [
   ("And here's a side story inside timeline B.", None),
   ("In December twenty fifteen, after four years of falling prices, Max's uncle gives up. He sells all his gold at about one thousand and seventy six dollars an ounce.", None),
   ("His ten thousand dollars from two thousand is now about thirty seven thousand nine hundred. Still a great result. He feels smart for getting out.", None),
   ("Then, over the next ten years, gold climbs to over four thousand three hundred dollars an ounce. Four times the price he sold at.", None),
   ("The hardest part of any investment isn't buying. It's sitting still when it hurts.", None),
 ], dict(type="stage", loc="street", actors=[dict(who="max", x=600, y=1010, size=320, emo={0: "neutral", 1: "worried", 2: "smug", 3: "shock"}), you(1350, {0: "neutral", 4: "smug"}, flip=True)],
         props=[dict(kind="tag", text="SOLD AT $1,076", col=CORAL, x=980, y=330, at=1, scale=1.0), dict(kind="tag", text="NOW $4,319 / oz", col=AMBER, x=980, y=520, at=3, scale=1.0, sub="Sep 2026")],
         texts=[dict(text="SIT STILL WHEN IT HURTS", size=90, col=AMBER, y=170, at=4, glow=12)], flash={3: AMBER}, shake=[3])),
 ("stock_crash", [
   ("Timeline C. The index fund. And this one starts with pain.", None),
   ("January two thousand turns out to be almost the worst possible month to buy American stocks. Right at the top of the internet bubble.", None),
   ("Then the dot-com crash. Then two thousand eight.", None),
   ("By March two thousand nine, your ten thousand dollars is worth five thousand three hundred. Less than the mattress, in plain dollars.", None),
   ("Grandma is not saying anything. But she's thinking it very loudly.", None),
 ], dict(type="chart", reveal=(0, 3), vmax=14000, series=[dict(values=STOCK[:i09 + 1], col=TEAL, width=9, fill=True), dict(values=FLAT[:i09 + 1], col=CREAM, width=4)],
         xlabels=[(i, k) for i, k in YEARS if i <= i09], side=[dict(label="S&P 500 (TIMELINE C)", values=STOCK[:i09 + 1], col=TEAL), dict(label="MATTRESS", values=FLAT[:i09 + 1], col=CREAM)],
         notes=[dict(i=i09, text="-47%", col=CORAL, dy=-120, dx=-100, size=80)], footnote="S&P 500 monthly avg. price (R. Shiller). Price only, dividends excluded.",
         actors=[dict(who="grandma", x=1650, y=1070, size=150, emo={0: "neutral", 4: "smug"})], flash={3: CORAL}, shake=[3])),
 ("stock_up", [
   ("It takes until twenty thirteen just to get back above ten thousand dollars. Thirteen years.", None),
   ("But then the long climb begins.", None),
   ("By September twenty twenty six, timeline C's ten thousand dollars is worth about fifty three thousand eight hundred. And that's price growth only.", None),
   ("The dividends companies paid along the way aren't even counted here. With them reinvested, the number would be noticeably higher.", None),
 ], dict(type="chart", reveal=(0, 2), p0=i09 / len(KS), series=[dict(values=STOCK, col=TEAL, width=9, fill=True), dict(values=FLAT, col=CREAM, width=4)],
         xlabels=YEARS, side=[dict(label="S&P 500 (TIMELINE C)", values=STOCK, col=TEAL), dict(label="MATTRESS", values=FLAT, col=CREAM)],
         footnote="S&P 500 monthly avg. price (R. Shiller). Price only, dividends excluded.", actors=[dict(who="banker", x=1650, y=1070, size=150, emo={0: "neutral", 2: "happy"})])),
 ("race", [
   ("Now let's put all three timelines on one chart.", None),
   ("The flat line is the mattress. The amber one is gold. The teal one is the index fund.", None),
   ("For most of these twenty six years, gold and stocks take turns being the hero.", None),
   ("And the mattress never wins a single year against inflation.", None),
   ("Notice something else. Both winners had long stretches where holding them felt terrible. Gold for four years. Stocks for thirteen.", None),
   ("The people who got the big numbers at the end were simply the ones who didn't quit in the middle.", None),
 ], dict(type="chart", reveal=(0, 2), series=[dict(values=GOLD, col=AMBER, width=8), dict(values=STOCK, col=TEAL, width=8), dict(values=FLAT, col=CREAM, width=5)],
         xlabels=YEARS, side=[dict(label="GOLD", values=GOLD, col=AMBER), dict(label="S&P 500", values=STOCK, col=TEAL), dict(label="CASH", values=FLAT, col=CREAM)])),
 ("result", [
   ("So, September twenty twenty six. Open the boxes.", None),
   ("Timeline A, the mattress: ten thousand dollars that buy like five thousand.", None),
   ("Timeline C, the index fund: about fifty three thousand eight hundred.", None),
   ("And timeline B, gold: about one hundred and fifty two thousand dollars. Over fifteen times the money.", None),
   ("Max's uncle buys a second boat.", None),
 ], dict(type="bars", groups=[dict(label="A: CASH", sub="buys like $5,034", vals=[(10000, CREAM)], at=1), dict(label="C: S&P 500", sub="price only", vals=[(STOCK[-1], TEAL)], at=2), dict(label="B: GOLD", sub="Sep 2026", vals=[(GOLD[-1], AMBER)], at=3)],
         texts=[dict(text="15.2x", size=150, col=AMBER, y=170, at=3, glow=18)], flash={3: AMBER}, shake=[3])),
 ("twist", [
   ("So gold is the answer? Not so fast.", None),
   ("Watch what happens if the radio contest happens ten years later, in January twenty ten.", None),
   ("Same ten thousand dollars. Gold ends at about thirty eight thousand six hundred.", None),
   ("The index fund ends at about sixty eight thousand three hundred. Almost double gold.", None),
   ("Same three choices. Different start date. Completely different winner.", None),
   ("Anyone who tells you they know which one will win the next twenty years is guessing. Some of them are just guessing very confidently.", None),
 ], dict(type="bars", groups=[dict(label="START 2000", vals=[(STOCK[-1], TEAL), (GOLD[-1], AMBER)], at=0), dict(label="START 2010", vals=[(68259, TEAL), (38631, AMBER)], at=2)],
         legend=[("S&P 500", TEAL), ("gold", AMBER)], texts=[dict(text="THE WINNER CHANGES", size=100, col=CREAM, y=170, at=4, glow=12)], flash={4: CREAM})),
 ("lesson", [
   ("And that's the real lesson of the three timelines.", None),
   ("Cash is not a bad thing. It's the right tool for emergencies and short term plans. It's just a bad place for twenty year money.", None),
   ("Gold and stocks both beat inflation over this long period, but both had painful years where they lost a third or half of their value.", None),
   ("Nobody knows which one wins the next twenty years. That's why many people spread long term money instead of betting on one box.", None),
 ], dict(type="list", cards=True, title="WHAT THE TIMELINES TEACH", items=[dict(text="CASH", sub="emergencies, short-term", col=CREAM, at=1), dict(text="GOLD + STOCKS", sub="beat inflation, painful drops", col=AMBER, at=2), dict(text="SPREAD IT", sub="nobody knows the winner", col=TEAL, at=3)])),
 ("cash_role", [
   ("So should you never hold cash? Of course not.", None),
   ("Cash is what saves you when the car breaks down or the job disappears. Many planners suggest keeping a few months of expenses somewhere safe and easy to reach.", None),
   ("The trick is to give every euro or dollar a job. Short term money stays safe. Long term money needs a chance to grow faster than prices.", None),
   ("And if your cash is going to sit for a while, at least shop around for an account that pays interest, so inflation bites a little less.", None),
   ("Grandma's mattress kept the money safe from thieves. It just didn't keep it safe from prices.", None),
 ], dict(type="stage", loc="kitchen", actors=[you(620, {0: "neutral", 2: "smug"}), dict(who="grandma", x=1380, y=1010, size=300, emo={0: "neutral", 4: "worried"}, flip=True)],
         props=[dict(kind="icon", name="shield", x=980, y=360, at=1, scale=0.6), dict(kind="tag", text="SHORT-TERM: SAFE", col=TEAL, x=980, y=560, at=2, scale=0.8), dict(kind="tag", text="LONG-TERM: GROW", col=AMBER, x=980, y=700, at=2.4, scale=0.8)],
         texts=[dict(text="GIVE EVERY DOLLAR A JOB", size=100, col=GREEN, y=170, at=2, glow=12)])),
 ("real", [
   ("One more thing. Remember, all of these numbers are in today's inflated dollars.", None),
   ("In two thousand money, the gold timeline is worth about seventy six thousand. The index fund about twenty seven thousand.", None),
   ("Still way ahead of the mattress. But inflation takes a bite out of every timeline, not just the cash.", None),
 ], dict(type="bars", groups=[dict(label="CASH", vals=[(5034, CREAM)], at=1), dict(label="S&P 500", vals=[(27083, TEAL)], at=1.3), dict(label="GOLD", vals=[(76559, AMBER)], at=1.6)],
         texts=[dict(text="IN YEAR-2000 DOLLARS", size=90, col=CREAM, y=170, glow=10)])),
 ("honest", [
   ("The honest part: this is not financial advice.", None),
   ("Past returns don't predict future ones. Gold has no dividends and can fall for years. Stocks can crash by half.", None),
   ("Fees, taxes and storage costs aren't included here, and they matter.", None),
 ], dict(type="list", title="NOT FINANCIAL ADVICE", tcol=CORAL, items=[dict(text="Past returns don't predict the future", at=1), dict(text="Gold and stocks can both drop for years", at=1.4), dict(text="Fees, taxes, storage not included", at=2)],
         actors=[you(1680, "neutral", size=240, y=1040)])),
 ("outro", [
   ("Same ten thousand dollars. Three places to hide it. Twenty six years.", None),
   ("If you had ten thousand dollars in two thousand, where would you have put it? Cash, gold or stocks? Tell me in the comments.", None),
   ("And I'll see you in the other timeline.", None),
 ], dict(type="end", q1="CASH, GOLD", q2="OR STOCKS?", comment="Where would you hide it?", comment_at=1, emo={0: "neutral", 1: "happy"})),
]

META = dict(
    file="EP04_Mattress_Gold_Stocks_2000.mp4",
    title="What If You Hid $10,000 Under Your Mattress in 2000?",
    description="""Three versions of you hide the same $10,000 in January 2000: under the mattress, in gold, and in an S&P 500 index fund. Nobody touches it for 26 years. One loses half its value without losing a single bill. One grows over 15x. And then we change the start date...

Data: US CPI-U (BLS via FRED CPIAUCSL), euro area HICP (Eurostat via FRED), monthly gold price (github.com/datasets/gold-prices), S&P 500 monthly average price (Robert Shiller data, price only, dividends excluded). No fees, taxes or storage costs.
This video is for education and entertainment only. It is not financial advice. Past performance does not guarantee future results.

#whatif #inflation #gold""",
    tags=["what if", "inflation", "cash under mattress", "gold vs stocks", "gold price", "s&p 500", "purchasing power", "personal finance", "financial education", "investing", "the other timeline", "animated story"],
    comment="You get $10,000 in the year 2000. Cash, gold or stocks? (No hindsight allowed 😄) 👇",
    chapters={"hook": "$10,000 under the mattress", "win": "January 2000", "rules": "Three timelines", "inflation": "What inflation does", "cash": "Timeline A: cash", "euro": "In euros",
              "gold_up": "Timeline B: gold boom", "gold_down": "Gold falls", "uncle_sells": "The uncle sells", "stock_crash": "Timeline C: the crash", "cash_role": "When cash is right", "stock_up": "The long climb", "race": "All three", "result": "Opening the boxes",
              "twist": "Change the start date", "lesson": "The lesson", "real": "In year-2000 dollars", "honest": "The honest part", "outro": "Where would you hide it?"},
)

THUMBS = {
    "A": dict(loc="bedroom", quote="it lost half..", hl=["half.."], actors=[dict(who="you", x=480, size=560, emo="shock"), dict(who="grandma", x=1480, size=520, emo="worried", flip=True)],
              props=[dict(kind="icon", name="mattress", x=960, y=760, scale=1.4), dict(kind="bill", amount="10,000", x=960, y=600, scale=1.2, rot=-8)], big=dict(text="-50%", x=960, y=360, col=CORAL, size=240)),
    "B": dict(loc="void", quote="cash vs gold vs stocks", hl=["gold"], actors=[dict(who="you", x=420, size=520, emo="money")],
              props=[dict(kind="icon", name="gold", x=1000, y=620, scale=1.3), dict(kind="icon", name="mattress", x=1500, y=740, scale=0.9)], big=dict(text="15x", x=1350, y=380, col=AMBER, size=260)),
}

SHORT = dict(segs=[("cash", [1, 3, 4]), ("result", [1, 2, 3])], title=["$10,000 HIDDEN IN 2000", "CASH vs GOLD vs STOCKS"], hook=dict(text="-50%", col=CORAL, dur=1.8),
             yt_title="I Hid $10,000 Under My Mattress in 2000 #shorts",
             yt_desc="Cash vs gold vs S&P 500 from January 2000, real CPI and price data. Full video on the channel. Not financial advice. #inflation #gold #money")
