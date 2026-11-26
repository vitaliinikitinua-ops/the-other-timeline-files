"""EP09 — What If Everything Went Wrong in the Same Month?  (two timelines, emergency fund)
Example bad month: $3,500 total (car $1,400, vet $650, laptop $900, dentist $550 — example prices).
Card APR 21.19% (avg on accounts assessed interest, Aug 2026, Fed G.19 via FRED TERMCBCCALLNS).
$3,500 on the card: minimum payments (greater of $25 or 1% + interest): 193 months, $5,133 interest;
$100/mo: 55 months, $1,998 interest; $150/mo: 31 months, $1,051; $200/mo: 22 months, $724.
Emergency fund: $50 a week = $2,600 a year; $3,500 takes 70 weeks."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
from kit import *  # noqa
import data

APR = data.fred("TERMCBCCALLNS")["2026-08"]
MM, PM, BM = data.card_payoff(3500, APR)
M1, P1, B1 = data.card_payoff(3500, APR, fixed=150)
B1p = B1 + [0.0] * (len(BM) - len(B1))

SPEED = 1.18
MUSIC_SEED = 9
END_LINE = "IS YOUR CUSHION READY?"

def you(x=960, emo="neutral", size=330, **k):
    return dict(who="you", x=x, y=k.pop("y", 1010), size=size, emo=emo, **k)

BEATS = [
 ("hook", [
   ("What if everything went wrong in the same month?", None),
   ("The car breaks. The dog gets sick. Your laptop dies. And then a tooth starts hurting.", None),
   ("Three and a half thousand dollars, in thirty days. And none of it was your fault.", None),
   ("Two versions of you live through the exact same terrible month. One of them is still paying for it years later. The other is fine by Friday.", None),
 ], dict(type="stage", loc="void_red", actors=[you(1500, {0: "neutral", 1: "shock", 3: "worried"})],
         props=[dict(kind="icon", name="car", x=500, y=360, at=1, scale=0.7), dict(kind="icon", name="warning", x=800, y=360, at=1.2, scale=0.5), dict(kind="icon", name="tv", x=500, y=640, at=1.4, scale=0.6), dict(kind="tag", text="TOOTH", col=CORAL, x=820, y=640, at=1.6, scale=0.8)],
         counters=[dict(**{"from": 0, "to": 3500}, at=2, dur=1.6, x=660, y=790, col=CORAL, size=130, label="IN ONE MONTH")],
         flash={2: CORAL}, shake=[1, 2])),
 ("normal", [
   ("It's an ordinary month. You've got a job, a car, a dog named Biscuit, and a budget that works if nothing weird happens.", None),
   ("Rent, food, bills, a bit of fun. At the end of the month, there's usually a little left over.", None),
   ("And that little bit is where the two timelines split.", None),
   ("Timeline A spends the leftover. A dinner here, a gadget there. It's not much, so it doesn't feel like it matters.", None),
   ("Timeline B moves fifty dollars every week into a separate savings account and calls it the bad day fund.", None),
 ], dict(type="split", left=dict(title="TIMELINE A", sub="spends the leftover", col=CORAL, who="you", emo="happy", at=3, props=[dict(kind="icon", name="burger", x=640, y=560, scale=0.6)]),
         right=dict(title="TIMELINE B", sub="$50 a week to a bad day fund", col=TEAL, who="you", emo="neutral", at=4, props=[dict(kind="jar", fill=0.35, x=1600, y=600)]),
         texts=[dict(text="THE SPLIT", size=110, col=AMBER, y=420, at=2, until=2.9, glow=12)])),
 ("fund", [
   ("Fifty dollars a week doesn't sound like much. But it's two thousand six hundred dollars a year.", None),
   ("After seventy weeks, about a year and four months, timeline B has three and a half thousand dollars sitting there, doing nothing exciting.", None),
   ("Max thinks this is the most boring thing he's ever heard. You should invest it! Or at least buy a jet ski!", None),
   ("But this money has one job. To be there on the worst day.", None),
 ], dict(type="stage", loc="kitchen", actors=[you(560, {0: "neutral", 1: "smug"}), dict(who="max", x=1400, y=1010, size=300, emo={0: "neutral", 2: "money"}, flip=True, talk=[2])],
         props=[dict(kind="jar", fill=0.9, x=980, y=560, at=1), dict(kind="tag", text="$50 x 70 WEEKS", col=TEAL, x=980, y=280, at=1, scale=0.9)],
         bubbles=[dict(text="Buy a jet ski!", x=1400, y=520, at=2, until=3)], counters=[dict(**{"from": 0, "to": 2600}, at=0, dur=1.4, x=560, y=300, col=TEAL, size=90, label="PER YEAR", until=0.95)],
         texts=[dict(text="ONE JOB: THE WORST DAY", size=96, col=AMBER, y=150, at=3, glow=12)])),
 ("day1", [
   ("And then the worst month arrives.", None),
   ("Monday. The car makes a noise like a shopping trolley falling down stairs. Fourteen hundred dollars to fix it, in this example.", None),
   ("Wednesday. Biscuit eats something he shouldn't. Six hundred and fifty at the vet.", None),
   ("Saturday. Your laptop, the one you need for work, refuses to turn on. Nine hundred for a replacement.", None),
   ("And the following week, a tooth. Five hundred and fifty at the dentist.", None),
 ], dict(type="stage", loc="street", actors=[you(560, {0: "neutral", 1: "shock", 2: "worried", 3: "shock", 4: "sad"})],
         props=[dict(kind="tag", text="CAR $1,400", col=CORAL, x=1250, y=260, at=1, scale=0.9), dict(kind="tag", text="VET $650", col=CORAL, x=1250, y=400, at=2, scale=0.9),
                dict(kind="tag", text="LAPTOP $900", col=CORAL, x=1250, y=540, at=3, scale=0.9), dict(kind="tag", text="DENTIST $550", col=CORAL, x=1250, y=680, at=4, scale=0.9)],
         flash={1: CORAL, 2: CORAL, 3: CORAL, 4: CORAL}, shake=[1, 3])),
 ("bill", [
   ("Total damage: three thousand five hundred dollars. Example prices, but very real life.", None),
   ("Same bills, both timelines. Now watch what happens next.", None),
 ], dict(type="stage", loc="void_red", actors=[you(1500, {0: "worried", 1: "neutral"})],
         props=[dict(kind="receipt", lines=[["Car repair", "$1,400"], ["Vet", "$650"], ["Laptop", "$900"], ["Dentist", "$550"]], total="$3,500", x=700, y=520, at=0, scale=1.3)],
         flash={0: CORAL})),
 ("a_card", [
   ("Timeline A has no cushion. So everything goes on the credit card.", None),
   ("The average card rate on balances that pay interest in the US was twenty one point one nine percent in August twenty twenty six.", None),
   ("If timeline A pays only the minimum, the card company's formula stretches it out for over sixteen years. And adds about five thousand one hundred dollars in interest.", None),
   ("Three and a half thousand dollars of bad luck becomes about eight thousand six hundred.", None),
 ], dict(type="stage", loc="bank", actors=[you(560, {0: "worried", 2: "shock", 3: "sad"}), dict(who="banker", x=1450, y=1010, size=310, emo="smug", flip=True)],
         props=[dict(kind="card", label="TIMELINE A", col=CORAL, x=1000, y=320, at=0, scale=0.9), dict(kind="tag", text="21.19% APR", col=CORAL, x=1000, y=520, at=1, scale=1.0), dict(kind="tag", text="16+ YEARS, $5,133 INTEREST", col=CORAL, x=1000, y=680, at=2, scale=0.8, sub="minimum payments")],
         counters=[dict(**{"from": 3500, "to": PM}, at=3, dur=1.6, x=1000, y=170, col=CORAL, size=110)], flash={3: CORAL}, shake=[3])),
 ("a_fixed", [
   ("Okay, let's be kinder to timeline A. Say you pay a fixed one hundred and fifty dollars a month instead of the minimum.", None),
   ("Then it takes thirty one months, more than two and a half years, to pay off one bad month.", None),
   ("And you pay about one thousand and fifty dollars in interest. Just for the bad luck of not having a cushion.", None),
   ("And here's the cruel part. During those thirty one months, what are the chances nothing else goes wrong?", None),
 ], dict(type="chart", reveal=(0, 2), series=[dict(values=BM, col=CORAL, width=8), dict(values=B1p, col=AMBER, width=8)],
         xlabels=[(i, f"Y{i // 12}") for i in range(0, len(BM), 36)], side=[dict(label="MINIMUM ONLY", values=BM, col=CORAL), dict(label="$150 / MONTH", values=B1p, col=AMBER)],
         footnote="$3,500 at 21.19% APR. Minimum = greater of $25 or 1% of balance + interest. No new purchases.",
         texts=[dict(text="31 MONTHS FOR 1 BAD MONTH", size=80, col=AMBER, x=760, y=170, at=1, glow=10)], actors=[dict(who="you", x=1650, y=1070, size=150, emo={0: "neutral", 3: "worried"})])),
 ("spiral", [
   ("Because life doesn't send one bad month and then politely wait.", None),
   ("Six months later, the washing machine floods. It goes on the same card. Then a friend's wedding. Then a parking fine.", None),
   ("The balance never quite reaches zero. And slowly, the debt stops being an emergency and becomes a permanent roommate.", None),
   ("Timeline A isn't irresponsible. It's just unprotected.", None),
   ("And every month of interest is money that can't go into a cushion, which makes the next surprise even more likely to land on the card.", None),
 ], dict(type="stage", loc="kitchen", actors=[you(560, {0: "neutral", 1: "shock", 2: "sad", 3: "neutral"})],
         props=[dict(kind="tag", text="WASHING MACHINE", col=CORAL, x=1250, y=300, at=1, scale=0.8), dict(kind="tag", text="WEDDING", col=CORAL, x=1250, y=440, at=1.3, scale=0.8), dict(kind="tag", text="PARKING FINE", col=CORAL, x=1250, y=580, at=1.6, scale=0.8),
                dict(kind="card", label="SAME CARD", col=CORAL, x=1250, y=790, at=2, scale=0.6)],
         texts=[dict(text="UNPROTECTED, NOT IRRESPONSIBLE", size=80, col=CREAM, y=150, at=3, glow=10)], shake=[1])),
 ("b_pays", [
   ("Timeline B. Same broken car. Same sick dog. Same dead laptop. Same tooth.", None),
   ("B opens the bad day fund and pays all four bills. Three and a half thousand dollars, gone.", None),
   ("It hurts. B doesn't enjoy it. But the total cost of this awful month is exactly three thousand five hundred dollars. Not a cent of interest.", None),
   ("And the next week, the fifty dollar transfer simply starts refilling the jar.", None),
 ], dict(type="stage", loc="kitchen", actors=[you(560, {0: "worried", 1: "neutral", 2: "sad", 3: "smug"})],
         props=[dict(kind="jar", fill=0.9, x=1100, y=560, at=0, until=1.9), dict(kind="jar", fill=0.05, x=1100, y=560, at=2, until=2.9), dict(kind="jar", fill=0.15, x=1100, y=560, at=3), dict(kind="tag", text="INTEREST: $0", col=GREEN, x=1100, y=260, at=2, scale=1.1)],
         texts=[dict(text="TIMELINE B", size=110, col=TEAL, y=150, glow=12)], flash={2: TEAL})),
 ("compare", [
   ("Side by side, the same month costs very different amounts.", None),
   ("Timeline B: three thousand five hundred.", None),
   ("Timeline A with fixed payments: about four thousand five hundred and fifty. Paying only the minimum: about eight thousand six hundred.", None),
   ("The emergency fund didn't make B richer on paper. It made bad luck cheaper.", None),
 ], dict(type="bars", groups=[dict(label="B: CASH", sub="emergency fund", vals=[(3500, TEAL)], at=1), dict(label="A: $150/MO", sub="31 months", vals=[(P1, AMBER)], at=2), dict(label="A: MINIMUM", sub="193 months", vals=[(PM, CORAL)], at=2.4)],
         texts=[dict(text="BAD LUCK, CHEAPER", size=110, col=GREEN, y=150, at=3, glow=14)], flash={3: GREEN})),
 ("feelings", [
   ("And there's something the numbers can't show.", None),
   ("Timeline A spends the next years with a quiet stress in the background. Every new email from the bank makes the stomach drop.", None),
   ("Timeline B had a terrible month. Then it was over. Sleep is normal again by Friday.", None),
   ("An emergency fund isn't really about money. It's about turning a disaster into an inconvenience.", None),
 ], dict(type="split", left=dict(title="TIMELINE A", sub="months later", col=CORAL, who="you", emo="worried", props=[dict(kind="phone", text="!", sub="NEW STATEMENT", col=CORAL, x=640, y=560, scale=0.7)]),
         right=dict(title="TIMELINE B", sub="by Friday", col=TEAL, who="you", emo="happy", at=2, props=[dict(kind="icon", name="shield", x=1600, y=560, scale=0.6)])
         )),
 ("job", [
   ("And the scariest emergency isn't a broken car. It's losing your income.", None),
   ("Imagine both timelines lose their job in the same month, and it takes three months to find a new one.", None),
   ("Timeline A has nothing to fall back on. Rent goes on the card, then groceries, then the phone bill. Three months can leave a debt that takes years to clear.", None),
   ("Timeline B's fund won't cover three months of everything. But it covers the gap while B cuts back, looks for work, and doesn't have to panic and take the first terrible offer.", None),
   ("That's why the bigger goal is months of expenses, not just one bad bill.", None),
 ], dict(type="split", left=dict(title="TIMELINE A", sub="3 months, no income", col=CORAL, who="you", emo="shock", props=[dict(kind="card", label="RENT", col=CORAL, x=640, y=560, scale=0.7)]),
         right=dict(title="TIMELINE B", sub="3 months, no income", col=TEAL, who="you", emo="worried", at=3, props=[dict(kind="jar", fill=0.6, x=1600, y=600)]),
         texts=[dict(text="MONTHS, NOT JUST BILLS", size=96, col=AMBER, y=800, at=4, glow=12)], flash={0: CORAL}, shake=[0])),
 ("why_not_invest", [
   ("Max still isn't convinced. Why keep three thousand dollars doing nothing? Invest it!", None),
   ("Here's the problem. Emergencies love to arrive when markets are falling. They often have the same cause.", None),
   ("In March twenty twenty, when lots of people lost hours or jobs, the S and P five hundred's average price was about nineteen percent lower than the month before.", None),
   ("If your emergency money had been in stocks, you'd have had to sell at a discount, exactly when you needed it most.", None),
   ("Emergency money is not for growing. It's for being there. Investing is what you do with the money after the cushion is full.", None),
 ], dict(type="stage", loc="living", actors=[you(560, {0: "neutral", 2: "worried", 4: "smug"}), dict(who="max", x=1400, y=1010, size=300, emo={0: "money", 3: "shock"}, flip=True, talk=[0])],
         bubbles=[dict(text="Invest it, bro!", x=1400, y=520, at=0, until=1)],
         props=[dict(kind="tag", text="MARCH 2020: -19%", col=CORAL, x=980, y=360, at=2, scale=1.0, sub="S&P 500 monthly avg vs Feb"), dict(kind="tag", text="CUSHION FIRST, THEN INVEST", col=TEAL, x=980, y=560, at=4, scale=0.9)],
         flash={2: CORAL})),
 ("how_much", [
   ("So how big should a bad day fund be?", None),
   ("Many financial planners suggest working towards three to six months of essential expenses. Rent, food, bills, transport.", None),
   ("That sounds enormous, so don't start there. Start with one bad month. Even five hundred or a thousand dollars changes everything.", None),
   ("Keep it somewhere separate, safe and easy to reach. Not invested in things that can drop fifty percent the week you need it.", None),
 ], dict(type="list", title="HOW BIG?", items=[dict(text="Goal: 3 to 6 months of essentials", at=1), dict(text="Start: one bad month ($500 to $1,000)", at=2), dict(text="Separate, safe, easy to reach", at=3), dict(text="Not in things that can crash", at=3.4)],
         actors=[you(1690, {0: "neutral", 2: "happy"}, size=240, y=1040)])),
 ("build", [
   ("And how do you build it, if there's barely anything left at the end of the month?", None),
   ("One. Automate it on payday, even if it's just ten or twenty dollars a week. It grows while you're not looking.", None),
   ("Two. Throw windfalls at it. Tax refunds, bonuses, birthday money, the money from selling stuff you don't use.", None),
   ("Three. Give it a name. People are much less likely to raid a fund called Biscuit's vet money than an account called savings.", None),
 ], dict(type="list", cards=True, title="BUILD YOUR CUSHION", items=[dict(text="AUTOMATE", sub="even $10 a week", at=1), dict(text="WINDFALLS", sub="refunds, bonuses, gifts", at=2), dict(text="NAME IT", sub="harder to raid", at=3)])),
 ("insurance", [
   ("Some disasters are too big for any jar. That's what insurance is for.", None),
   ("Health, car, home or renters insurance, depending on where you live. The emergency fund covers the deductible. The insurance covers the catastrophe.", None),
   ("Once a year, check what you're actually covered for. Many people find out what their policy doesn't include on the worst day of their life.", None),
   ("Fund for the small disasters. Insurance for the big ones.", None),
 ], dict(type="stage", loc="office", actors=[you(560, {0: "neutral", 2: "worried", 3: "smug"})],
         props=[dict(kind="icon", name="shield", x=1150, y=420, at=1, scale=0.9), dict(kind="tag", text="FUND: SMALL DISASTERS", col=TEAL, x=1150, y=680, at=3, scale=0.8), dict(kind="tag", text="INSURANCE: BIG ONES", col=AMBER, x=1150, y=820, at=3.3, scale=0.8)],
         texts=[dict(text="KNOW YOUR COVERAGE", size=100, col=AMBER, y=150, at=2, glow=12)])),
 ("after", [
   ("And what does timeline B do once the cushion is full again?", None),
   ("The fifty dollars a week keeps going, but now it flows into long term investing instead.", None),
   ("That's the order that works for most people. First, a cushion. Then, expensive debt gone. Then, the money starts growing.", None),
   ("Timeline A wants to skip to step three. Timeline B knows step one is what makes step three possible.", None),
 ], dict(type="list", cards=True, title="THE ORDER THAT WORKS", items=[dict(text="CUSHION", sub="one bad month, then more", at=2), dict(text="DEBT", sub="expensive debt gone", at=2.3), dict(text="GROW", sub="long-term investing", at=2.6)],
         texts=[dict(text="STEP 1 MAKES STEP 3 POSSIBLE", size=70, col=GREEN, y=850, at=3, glow=10)])),
 ("max", [
   ("Max, of course, hears all of this, nods seriously, and opens a savings account.", None),
   ("He names it jet ski fund.", None),
   ("You point out that a jet ski is not an emergency. Max says it will be, if he doesn't get one soon.", None),
   ("It's a start.", None),
   ("And honestly, a fund with a silly name that actually exists beats a perfect plan that never starts.", None),
 ], dict(type="stage", loc="street", actors=[dict(who="max", x=700, y=1010, size=330, emo={0: "neutral", 1: "money", 2: "happy"}), you(1350, {0: "neutral", 2: "smug"}, flip=True)],
         props=[dict(kind="phone", text="JET SKI FUND", sub="NEW ACCOUNT", col=TEAL, x=1030, y=520, at=1, scale=0.9)])),
 ("honest", [
   ("The honest part. This is not financial advice.", None),
   ("The bills in this story are example prices, card terms differ, and your own emergency fund size depends on your life, your job and your family.", None),
   ("If you're already deep in debt, speaking with a non-profit credit counsellor can help you build a plan.", None),
 ], dict(type="list", title="NOT FINANCIAL ADVICE", tcol=CORAL, items=[dict(text="Example prices, your life differs", at=1), dict(text="Card terms differ", at=1.4), dict(text="Non-profit credit counselling exists", at=2)],
         actors=[you(1680, "neutral", size=240, y=1040)])),
 ("outro", [
   ("Same bad month. One timeline pays for years. The other has a terrible week, and then moves on.", None),
   ("Tell me in the comments: what's the worst month your wallet ever survived?", None),
   ("And I'll see you in the other timeline.", None),
 ], dict(type="end", q1="IS YOUR CUSHION", q2="READY?", comment="Worst month your wallet survived?", comment_at=1, emo={0: "neutral", 1: "smug"})),
]

META = dict(
    file="EP09_Everything_Went_Wrong.mp4",
    title="What If Everything Went Wrong in the Same Month?",
    description="""Car, vet, laptop and dentist: $3,500 of bad luck in one month. One version of you puts it on a credit card and pays for years. The other has a bad day fund and is fine by Friday. What an emergency fund really does, with real credit card rates.

Method: example bills totalling $3,500. Card APR 21.19% (average US rate on accounts assessed interest, Aug 2026, Federal Reserve G.19 via FRED). Minimum payment = greater of $25 or 1% of balance plus interest (a common formula). No new purchases.
This video is for education and entertainment only. It is not financial advice.

#whatif #emergencyfund #personalfinance""",
    tags=["what if", "emergency fund", "unexpected expenses", "credit card debt", "budgeting", "saving money", "financial stress", "personal finance", "financial education", "money tips", "the other timeline", "animated story"],
    comment="What's the worst month your wallet ever survived? 👇",
    chapters={"hook": "Everything goes wrong", "normal": "An ordinary month", "fund": "The bad day fund", "day1": "The worst month", "bill": "The total", "a_card": "Timeline A: the card",
              "a_fixed": "31 months for 1 bad month", "spiral": "When it keeps happening", "b_pays": "Timeline B pays cash", "compare": "Side by side", "feelings": "What numbers can't show",
              "job": "Losing your income", "why_not_invest": "Why not invest it?", "how_much": "How big should it be?", "build": "How to build it", "insurance": "Insurance for the big ones", "after": "The order that works", "max": "Max's new fund", "honest": "The honest part", "outro": "Your worst month?"},
)

THUMBS = {
    "A": dict(loc="street", quote="everything broke at once..", hl=["once.."], actors=[dict(who="you", x=480, size=560, emo="shock")],
              props=[dict(kind="icon", name="car", x=1150, y=700, scale=1.0), dict(kind="tag", text="$3,500", col=CORAL, x=1350, y=420, scale=1.6)]),
    "B": dict(loc="void_red", quote="$3,500 became $8,633", hl=["$8,633"], actors=[dict(who="you", x=460, size=560, emo="worried")],
              props=[dict(kind="card", label="21.19% APR", col=CORAL, x=1350, y=620, scale=1.3, rot=8)], big=dict(text="16 YEARS", x=1300, y=340, col=CORAL, size=170)),
}

SHORT = dict(segs=[("day1", [1, 2, 3, 4]), ("compare", [1, 2, 3])], title=["EVERYTHING WENT WRONG", "IN ONE MONTH"], hook=dict(text="$3,500", col=CORAL, dur=1.6),
             yt_title="Everything Broke in the Same Month #shorts",
             yt_desc="$3,500 of bad luck: credit card vs emergency fund, at the real average US card rate (21.19%). Full video on the channel. Not financial advice. #money #emergencyfund")
