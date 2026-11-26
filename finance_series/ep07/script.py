"""EP07 — What If You Bought Your House in 2006 Instead of 2012?  (three timelines)
Example house: $300,000 in Jul 2006. Its value follows the S&P CoreLogic Case-Shiller US National Home Price Index (FRED CSUSHPINSA):
Jul 2006 184.608 (peak) -> Feb 2012 133.987 (trough) -> Sep 2026 335.754; back above the 2006 peak in Jan 2017.
Rates: Freddie Mac 30-year fixed (FRED MORTGAGE30US): Jul 2006 6.79%, Feb 2012 3.87%, Nov 25 2026 7.21%; low 2.65% (Jan 2021).
20% down, 30-year fixed, principal + interest only (no taxes, insurance, maintenance).
A (Jul 2006): $300,000, loan $240,000, $1,563/mo; in Feb 2012 worth $217,738 but owes $223,353 (underwater). Sep 2026: owes $134,288, equity $411,334. Paid $438,246 incl. down payment.
B (Feb 2012): $217,738, loan $174,190, $819/mo; Sep 2026 owes $113,921, equity $431,701; paid $186,873 incl. down payment.
C (Nov 2026): $545,622, loan $436,498, $2,966/mo. 30-year interest: A $322,688, B $120,509, C $631,208."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
from kit import *  # noqa
import data

CS = data.fred("CSUSHPINSA")
KS = [k for k in sorted(CS) if "2006-07" <= k <= "2026-09"]
HOUSE = [300000 * CS[k] / CS["2006-07"] for k in KS]
def pay(L, r, n=360):
    r = r / 1200; return L * r / (1 - (1 + r) ** -n)
def bal_series(L, r, months):
    p = pay(L, r); rr = r / 1200; b = L; out = [b]
    for _ in range(months):
        b = b * (1 + rr) - p; out.append(b)
    return out
OWE_A = bal_series(240000, 6.79, len(KS) - 1)
iB = KS.index("2012-02"); i17 = KS.index("2017-01")
LB = 0.8 * HOUSE[iB]
OWE_B = [0.0] * iB + bal_series(LB, 3.87, len(KS) - 1 - iB)
YEARS = [(i, k[:4]) for i, k in enumerate(KS) if k.endswith("-01") and int(k[:4]) % 4 == 0]
MR = data.fred("MORTGAGE30US")
MK = [k for k in sorted(MR) if k >= "2000-01"]

SPEED = 1.18
MUSIC_SEED = 7
END_LINE = "WHEN WOULD YOU HAVE BOUGHT?"

def you(x=960, emo="neutral", size=330, **k):
    return dict(who="you", x=x, y=k.pop("y", 1010), size=size, emo=emo, **k)

BEATS = [
 ("hook", [
   ("Same house. Same street. Same three bedrooms. Three versions of you buy it at three different moments.", None),
   ("One pays one thousand five hundred and sixty three dollars a month. One pays eight hundred and nineteen. And one pays almost three thousand.", None),
   ("For the exact same house.", None),
   ("One of them spends years owing more than the house is worth. And yet the ending isn't what you'd expect.", None),
 ], dict(type="stage", loc="street", actors=[you(1500, {0: "neutral", 1: "shock", 3: "worried"})],
         props=[dict(kind="icon", name="house", x=650, y=560, at=0, scale=1.5), dict(kind="tag", text="$1,563 / MO", col=AMBER, x=650, y=250, at=1, scale=0.8, sub="2006"),
                dict(kind="tag", text="$819 / MO", col=TEAL, x=1080, y=330, at=1.3, scale=0.8, sub="2012"), dict(kind="tag", text="$2,966 / MO", col=CORAL, x=650, y=860, at=1.6, scale=0.8, sub="2026")],
         texts=[dict(text="SAME HOUSE", size=140, col=CREAM, y=150, at=2, glow=14)], flash={2: CREAM}, shake=[2])),
 ("2006", [
   ("July two thousand six. Everyone you know is buying a house.", None),
   ("Max just bought his second one. He says house prices only go up. The man at the bank agrees with him, enthusiastically.", None),
   ("You find a nice house for three hundred thousand dollars. This is our example house. Remember it.", None),
   ("Here the timeline splits into three.", None),
 ], dict(type="stage", loc="bank", actors=[you(520, {0: "neutral", 2: "happy"}), dict(who="max", x=980, y=1010, size=300, emo="smug", talk=[1]), dict(who="banker", x=1450, y=1010, size=320, emo="happy", flip=True, talk=[1])],
         props=[dict(kind="calendar", top="2006", big="JUL", x=980, y=300, at=0, until=1.9, scale=0.8), dict(kind="tag", text="$300,000", col=AMBER, x=980, y=330, at=2, scale=1.2, sub="example house")],
         bubbles=[dict(text="Prices only go up!", x=980, y=520, at=1, until=2)], flash={3: AMBER}, shake=[3])),
 ("rules", [
   ("Timeline A buys right now, in July two thousand six.", None),
   ("Timeline B rents and waits until February twenty twelve.", None),
   ("Timeline C is a version of you buying the same house today, in November twenty twenty six.", None),
   ("Each puts down twenty percent and takes a thirty year fixed mortgage at the real average rate of that month. The house's value follows a real national home price index.", None),
 ], dict(type="list", cards=True, title="THREE TIMELINES, ONE HOUSE", items=[dict(text="A: JUL 2006", sub="buys at the peak", col=AMBER, at=0), dict(text="B: FEB 2012", sub="rents, then buys", col=TEAL, at=1), dict(text="C: NOV 2026", sub="buys today", col=CORAL, at=2)],
         texts=[dict(text="20% DOWN · 30-YEAR FIXED · REAL RATES · CASE-SHILLER INDEX", size=46, col=CREAM, y=800, at=3)])),
 ("a_buys", [
   ("Timeline A. You pay sixty thousand dollars down and borrow two hundred and forty thousand.", None),
   ("The average thirty year rate that month is six point seven nine percent.", None),
   ("Your payment, principal and interest only: one thousand five hundred and sixty three dollars a month, for thirty years.", None),
   ("You get the keys. You paint the kitchen. You feel like a real adult.", None),
 ], dict(type="stage", loc="kitchen", actors=[you(560, {0: "neutral", 3: "happy"}), dict(who="banker", x=1450, y=1010, size=300, emo="happy", flip=True)],
         props=[dict(kind="receipt", lines=[["House", "$300,000"], ["Down (20%)", "$60,000"], ["Loan", "$240,000"], ["Rate", "6.79%"]], total="$1,563/mo", x=1000, y=520, at=0, scale=1.1)],
         texts=[dict(text="TIMELINE A", size=110, col=AMBER, y=150, glow=12)])),
 ("crash", [
   ("And then the American housing market collapses.", None),
   ("Two thousand seven, two thousand eight. Banks fail. Millions of homes go into foreclosure across the country.", None),
   ("By February twenty twelve, the national home price index is down about twenty seven percent from the peak.", None),
   ("Your three hundred thousand dollar house is now worth about two hundred and eighteen thousand.", None),
   ("And you still owe the bank about two hundred and twenty three thousand.", None),
 ], dict(type="chart", reveal=(0, 3), series=[dict(values=HOUSE[:iB + 1], col=AMBER, width=9, fill=True), dict(values=OWE_A[:iB + 1], col=CORAL, width=7)], vmax=340000,
         xlabels=[(i, k) for i, k in YEARS if i <= iB], side=[dict(label="HOUSE WORTH", values=HOUSE[:iB + 1], col=AMBER), dict(label="YOU OWE", values=OWE_A[:iB + 1], col=CORAL)],
         footnote="House value follows the S&P CoreLogic Case-Shiller US National Home Price Index (FRED CSUSHPINSA). Example house: $300,000 in Jul 2006.",
         notes=[dict(i=iB, text="-27%", col=CORAL, dy=-150, dx=-80, size=80)], actors=[dict(who="you", x=1650, y=1070, size=150, emo={0: "worried", 4: "shock"})], flash={0: CORAL}, shake=[0])),
 ("underwater", [
   ("This is called being underwater. You owe more than the thing is worth.", None),
   ("After five and a half years of payments and a sixty thousand dollar down payment, if you sold the house, you'd still owe the bank money.", None),
   ("Max, the guy with two houses, is in much worse shape. He has to sell one at a big loss.", None),
   ("You can't sell without losing everything you put in. So you do the only thing you can. You keep paying, and you keep living there.", None),
 ], dict(type="stage", loc="living", actors=[you(560, {0: "sad", 3: "neutral"}), dict(who="max", x=1400, y=1010, size=300, emo={0: "shock", 2: "sad"}, flip=True)],
         props=[dict(kind="tag", text="WORTH $217,738", col=AMBER, x=1000, y=330, at=0, scale=0.9), dict(kind="tag", text="OWES $223,353", col=CORAL, x=1000, y=480, at=0.4, scale=0.9), dict(kind="tag", text="FOR SALE", col=CORAL, x=1400, y=420, at=2, scale=0.8)],
         texts=[dict(text="UNDERWATER", size=150, col=CORAL, y=160, at=0, glow=16)], flash={0: CORAL})),
 ("renting", [
   ("While timeline A is underwater, timeline B is getting teased at every family dinner.", None),
   ("Still renting? You're throwing money away! says an uncle who has never once checked his own mortgage statement.", None),
   ("But rent isn't throwing money away. It buys a roof, flexibility, and no repair bills when the boiler dies.", None),
   ("Timeline B pays rent, saves the difference every month, and builds a down payment while prices fall.", None),
   ("For a few years, it looks like doing nothing. It's actually waiting with a plan.", None),
 ], dict(type="stage", loc="living", actors=[you(560, {0: "neutral", 1: "worried", 3: "smug"}), dict(who="stranger", x=1400, y=1010, size=310, emo={0: "smug", 1: "angry"}, flip=True, talk=[1])],
         bubbles=[dict(text="Still renting?! Throwing money away!", x=1400, y=500, at=1, until=2)],
         props=[dict(kind="tag", text="RENT = ROOF + FLEXIBILITY", col=TEAL, x=980, y=330, at=2, scale=0.8), dict(kind="jar", fill=0.7, x=980, y=640, at=3)],
         texts=[dict(text="WAITING WITH A PLAN", size=100, col=TEAL, y=150, at=4, glow=12)])),
 ("b_buys", [
   ("Meanwhile, timeline B has been renting, and saving, and waiting. February twenty twelve.", None),
   ("The same house is now on sale for about two hundred and eighteen thousand. And mortgage rates have dropped to three point eight seven percent.", None),
   ("You put down forty three thousand five hundred and borrow about one hundred and seventy four thousand.", None),
   ("Your monthly payment: eight hundred and nineteen dollars. Almost half of timeline A's payment, for the same house.", None),
 ], dict(type="stage", loc="bank", actors=[you(560, {0: "neutral", 3: "money"}), dict(who="banker", x=1450, y=1010, size=320, emo="worried", flip=True)],
         props=[dict(kind="receipt", lines=[["House", "$217,738"], ["Down (20%)", "$43,548"], ["Loan", "$174,190"], ["Rate", "3.87%"]], total="$819/mo", x=1000, y=520, at=1, scale=1.1)],
         texts=[dict(text="TIMELINE B", size=110, col=TEAL, y=150, glow=12)], flash={3: TEAL})),
 ("rates", [
   ("Why such a difference? Two things changed at once. The price, and the interest rate.", None),
   ("Mortgage rates move a lot. Over six and a half percent in two thousand six. Under four in twenty twelve. A record low around two point six five percent in January twenty twenty one.", None),
   ("Then back up to almost eight percent in late twenty twenty three.", None),
   ("On a thirty year loan, a few percentage points can change the total cost by hundreds of thousands of dollars.", None),
 ], dict(type="chart", reveal=(0, 2), series=[dict(values=[MR[k] for k in MK], col=CORAL, width=8)], yfmt="{:.0f}%", vmax=10,
         xlabels=[(i, k[:4]) for i, k in enumerate(MK) if k.endswith("-01") and int(k[:4]) % 4 == 0], side=[dict(label="30-YEAR FIXED RATE", values=[MR[k] for k in MK], col=CORAL, fmt="{:.2f}%")],
         footnote="Freddie Mac 30-year fixed mortgage average (FRED MORTGAGE30US), first reading of each month.", actors=[dict(who="you", x=1650, y=1070, size=150, emo={0: "neutral", 2: "shock"})])),
 ("recovery", [
   ("Back to timeline A, still underwater, still paying.", None),
   ("Slowly, the market recovers. In January twenty seventeen, the national index finally climbs back above its two thousand six peak.", None),
   ("Ten and a half years after you bought, your house is worth what you paid for it again.", None),
   ("And then it keeps going.", None),
 ], dict(type="chart", reveal=(0, 3), p0=iB / len(KS), series=[dict(values=HOUSE, col=AMBER, width=9, fill=True), dict(values=OWE_A, col=CORAL, width=7)],
         xlabels=YEARS, side=[dict(label="HOUSE WORTH", values=HOUSE, col=AMBER), dict(label="A STILL OWES", values=OWE_A, col=CORAL)],
         notes=[dict(i=i17, text="BACK TO $300K", col=GREEN, dy=-120, size=50)], actors=[dict(who="you", x=1650, y=1070, size=150, emo={0: "sad", 3: "happy"})])),
 ("today", [
   ("September twenty twenty six. The same house is now worth about five hundred and forty five thousand dollars, according to the index.", None),
   ("Timeline A owes about one hundred and thirty four thousand. Its equity, the part of the house it really owns, is about four hundred and eleven thousand.", None),
   ("Timeline B owes about one hundred and fourteen thousand. Its equity is about four hundred and thirty two thousand.", None),
   ("Both did well. But B bought later, paid much less every month, and still ends up ahead.", None),
   ("And remember, timeline A only got here because it never sold. The people who were forced to sell in twenty ten or twenty eleven locked in their losses forever.", None),
 ], dict(type="bars", groups=[dict(label="TIMELINE A", sub="bought Jul 2006", vals=[(OWE_A[-1], CORAL), (HOUSE[-1] - OWE_A[-1], AMBER)], at=1), dict(label="TIMELINE B", sub="bought Feb 2012", vals=[(OWE_B[-1], CORAL), (HOUSE[-1] - OWE_B[-1], TEAL)], at=2)],
         legend=[("still owes", CORAL), ("equity", AMBER)], texts=[dict(text="HOUSE: ~$545,600", size=90, col=CREAM, y=150, glow=10)])),
 ("paid", [
   ("Now count what each one actually paid out of pocket, including the down payment.", None),
   ("Timeline A: about four hundred and thirty eight thousand dollars so far.", None),
   ("Timeline B: about one hundred and eighty seven thousand.", None),
   ("To be fair, timeline B also paid rent for those five and a half years. But even with that, the gap is enormous.", None),
   ("Same house. The only difference was when they bought, and the rate they got.", None),
 ], dict(type="bars", groups=[dict(label="TIMELINE A", vals=[(438246, AMBER)], at=1), dict(label="TIMELINE B", sub="+ 5.5 years of rent", vals=[(186873, TEAL)], at=2)],
         texts=[dict(text="PAID SO FAR", size=100, col=CREAM, y=150, glow=10)], flash={2: TEAL})),
 ("c_buys", [
   ("And now, timeline C. You, today, in November twenty twenty six, looking at the same house.", None),
   ("The price is about five hundred and forty six thousand. The average thirty year rate is seven point two one percent.", None),
   ("Twenty percent down is over one hundred and nine thousand dollars. The loan is about four hundred and thirty six thousand.", None),
   ("The monthly payment: two thousand nine hundred and sixty six dollars. More than three and a half times timeline B, for the same three bedrooms.", None),
   ("And over thirty years, the interest alone would be about six hundred and thirty one thousand dollars.", None),
 ], dict(type="stage", loc="bank", actors=[you(560, {0: "neutral", 3: "shock", 4: "worried"}), dict(who="banker", x=1450, y=1010, size=320, emo="smug", flip=True)],
         props=[dict(kind="receipt", lines=[["House", "$545,622"], ["Down (20%)", "$109,124"], ["Loan", "$436,498"], ["Rate", "7.21%"]], total="$2,966/mo", x=1000, y=520, at=1, scale=1.1)],
         texts=[dict(text="TIMELINE C", size=110, col=CORAL, y=150, glow=12)], flash={3: CORAL}, shake=[3])),
 ("monthly", [
   ("Here are all three payments side by side.", None),
   ("Eight hundred and nineteen. One thousand five hundred and sixty three. Two thousand nine hundred and sixty six.", None),
   ("Same house. Three completely different lives.", None),
 ], dict(type="bars", groups=[dict(label="B: 2012", sub="3.87%", vals=[(819, TEAL)], at=1), dict(label="A: 2006", sub="6.79%", vals=[(1563, AMBER)], at=1.3), dict(label="C: 2026", sub="7.21%", vals=[(2966, CORAL)], at=1.6)],
         texts=[dict(text="MONTHLY PAYMENT", size=100, col=CREAM, y=150, glow=10)], flash={2: CREAM})),
 ("europe", [
   ("A quick note for everyone outside the US.", None),
   ("Thirty year fixed rates are very American. In many European countries, mortgages are fixed for only a few years, or move with interest rates.", None),
   ("That means your payment can change while you live in the house. When rates jumped in twenty twenty two and twenty twenty three, many families saw their monthly cost rise sharply.", None),
   ("So wherever you live, ask one question before you sign. What happens to my payment if rates go up two points?", None),
 ], dict(type="stage", loc="void", actors=[you(1500, {0: "neutral", 2: "worried", 3: "smug"})],
         props=[dict(kind="tag", text="FIXED 30 YEARS", col=TEAL, x=650, y=360, at=1, scale=1.0, sub="common in the US"), dict(kind="tag", text="VARIABLE / SHORT FIX", col=CORAL, x=650, y=560, at=1.3, scale=1.0, sub="common in much of Europe")],
         texts=[dict(text="WHAT IF RATES +2%?", size=110, col=AMBER, y=160, at=3, glow=14)])),
 ("afford", [
   ("And one more trap. The bank will often approve you for more than you should borrow.", None),
   ("Lenders look at whether you can make the payment. Not whether you can still save, travel, or survive losing your job.", None),
   ("Timeline A felt rich on approval day. Five years later, the payment was eating the budget alive.", None),
   ("A good test: if your income dropped for six months, could you still pay? If the answer is no, the house is too big for now.", None),
 ], dict(type="stage", loc="bank", actors=[you(560, {0: "happy", 2: "worried", 3: "neutral"}), dict(who="banker", x=1450, y=1010, size=320, emo="happy", flip=True, talk=[0])],
         props=[dict(kind="tag", text="APPROVED: MORE!", col=GREEN, x=1000, y=330, at=0, until=1.9, scale=1.0), dict(kind="tag", text="6-MONTH TEST", col=AMBER, x=1000, y=500, at=3, scale=1.1)],
         texts=[dict(text="APPROVED IS NOT AFFORDABLE", size=96, col=CORAL, y=160, at=1, glow=12)])),
 ("lesson", [
   ("So what can you actually learn, if nobody can time the market?", None),
   ("One. The monthly payment matters more than the price tag. Rates can change it by thousands a year.", None),
   ("Two. Timeline A survived because it didn't have to sell. Buy only if you can stay put through a bad few years.", None),
   ("Three. Max lost because he stretched for a second house with borrowed money. Leverage cuts both ways.", None),
   ("And four. A house is first a place to live. If the numbers only work when prices keep rising, the numbers don't work.", None),
 ], dict(type="list", title="WHAT THE THREE TIMELINES TEACH", items=[dict(text="The payment matters more than the price", at=1), dict(text="Only buy if you can stay through bad years", at=2), dict(text="Borrowed money cuts both ways", at=3), dict(text="A home is first a place to live", at=4)],
         actors=[you(1690, {0: "neutral", 4: "smug"}, size=240, y=1040)])),
 ("honest", [
   ("The honest part. This is not financial advice.", None),
   ("This is one example house following a national average index. Local markets can be very different, in the US and in Europe.", None),
   ("Taxes, insurance, maintenance and fees aren't included, and they can add a lot to the cost of owning.", None),
 ], dict(type="list", title="NOT FINANCIAL ADVICE", tcol=CORAL, items=[dict(text="Example house, national average", at=1), dict(text="Local markets differ a lot", at=1.4), dict(text="Taxes, insurance, repairs not included", at=2)],
         actors=[you(1680, "neutral", size=240, y=1040)])),
 ("outro", [
   ("Same house. Three timelines. Eight hundred dollars a month, or three thousand.", None),
   ("Tell me in the comments: when did you buy, or are you still waiting for the right moment?", None),
   ("And I'll see you in the other timeline.", None),
 ], dict(type="end", q1="WHEN WOULD YOU", q2="HAVE BOUGHT?", comment="Bought, or still waiting?", comment_at=1, emo={0: "neutral", 1: "smug"})),
]

META = dict(
    file="EP07_House_2006_vs_2012.mp4",
    title="What If You Bought Your House in 2006 Instead of 2012?",
    description="""Same house, three versions of you. One buys at the 2006 peak and ends up underwater. One waits until 2012 and pays almost half per month. One buys the same house today and pays almost $3,000 a month. Real home price index and real mortgage rates.

Data: S&P CoreLogic Case-Shiller US National Home Price Index (FRED CSUSHPINSA), Freddie Mac 30-year fixed mortgage rate (FRED MORTGAGE30US). Example house $300,000 in Jul 2006, 20% down, 30-year fixed, principal and interest only. Taxes, insurance and maintenance not included; local markets differ.
This video is for education and entertainment only. It is not financial advice.

#whatif #housing #personalfinance""",
    tags=["what if", "housing market", "buy a house", "mortgage rates", "2008 housing crash", "underwater mortgage", "case shiller", "rent vs buy", "personal finance", "financial education", "the other timeline", "animated story"],
    comment="Did you buy a home already, or are you still waiting for the right moment? 👇",
    chapters={"hook": "Same house, 3 payments", "2006": "July 2006", "rules": "Three timelines", "a_buys": "Timeline A buys", "crash": "The crash", "underwater": "Underwater",
              "renting": "Still renting?", "b_buys": "Timeline B buys in 2012", "europe": "Outside the US", "afford": "Approved is not affordable", "rates": "Why rates matter", "recovery": "The recovery", "today": "Equity in 2026", "paid": "What each one paid",
              "c_buys": "Timeline C: buying today", "monthly": "Three payments", "lesson": "What to learn", "honest": "The honest part", "outro": "When would you have bought?"},
)

THUMBS = {
    "A": dict(loc="street", quote="same house, 3 prices..", hl=["3"], actors=[dict(who="you", x=420, size=520, emo="shock"), dict(who="banker", x=1520, size=500, emo="smug", flip=True)],
              props=[dict(kind="icon", name="house", x=960, y=640, scale=1.6)], big=dict(text="$819 vs $2,966", x=960, y=330, col=AMBER, size=150, rot=-3)),
    "B": dict(loc="void_red", quote="i bought in 2006..", hl=["2006.."], actors=[dict(who="you", x=480, size=560, emo="sad")],
              props=[dict(kind="icon", name="house", x=1350, y=640, scale=1.4)], big=dict(text="UNDERWATER", x=1300, y=330, col=CORAL, size=150, rot=-4)),
}

SHORT = dict(segs=[("hook", [0, 1, 2]), ("c_buys", [1, 3])], title=["SAME HOUSE.", "3 DIFFERENT PRICES"], hook=dict(text="$2,966/MO", col=CORAL, dur=1.8),
             yt_title="Same House: $819 vs $2,966 a Month #shorts",
             yt_desc="Case-Shiller home price index and Freddie Mac mortgage rates, 2006 vs 2012 vs today. Full video on the channel. Not financial advice. #housing #mortgage #money")
