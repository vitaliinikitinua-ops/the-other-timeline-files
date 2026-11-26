"""EP08 — What If Your Salary Doubled and You Stayed Broke?  (two timelines, lifestyle inflation)
Example salary path: $40,000 in 2012, +$4,000 a year, $80,000 from 2022 (example, before tax).
Timeline B saves half of every raise (before tax): invested monthly in S&P 500 (Shiller, price only) Jan 2012 - Sep 2026:
$185,000 put in -> $392,441. US personal saving rate (BEA via FRED PSAVERT): Oct 2026 4.1%, Jan 2006 3.0%, Apr 2020 peak 31.8%.
US avg hourly earnings Mar 2006 $20.04 -> Oct 2026 $38.00 (FRED CES0500000003)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
from kit import *  # noqa
import data

SP = data.sp500()
KS = [k for k in sorted(SP) if "2012-01" <= k <= "2026-09"]
def salary(y): return min(80000, 40000 + 4000 * (y - 2012))
INV, VAL = [], []
_sh = _inv = 0.0
for k in KS:
    m = 0.5 * (salary(int(k[:4])) - 40000) / 12
    _sh += m / SP[k]; _inv += m; INV.append(_inv); VAL.append(_sh * SP[k])
SAL = [salary(int(k[:4])) for k in KS]
YEARS = [(i, k[:4]) for i, k in enumerate(KS) if k.endswith("-01") and int(k[:4]) % 2 == 0]
PS = data.fred("PSAVERT"); PK = [k for k in sorted(PS) if k >= "2000-01"]

SPEED = 1.18
MUSIC_SEED = 8
END_LINE = "WHERE DID YOUR RAISE GO?"

def you(x=960, emo="neutral", size=330, **k):
    return dict(who="you", x=x, y=k.pop("y", 1010), size=size, emo=emo, **k)

BEATS = [
 ("hook", [
   ("What if your salary doubled, and ten years later you were exactly as broke as before?", None),
   ("Same stress at the end of the month. Same empty savings account. Just a nicer car parked outside.", None),
   ("It happens to millions of people, and it has a name. Lifestyle inflation.", None),
   ("Today, two versions of you get the exact same raises. One of them ends up with almost four hundred thousand dollars. The other one ends up with a very nice sofa.", None),
 ], dict(type="split", left=dict(title="TIMELINE A", sub="spends every raise", col=CORAL, who="you", emo={0: "happy", 1: "worried"}, props=[dict(kind="icon", name="sofa", x=620, y=640, scale=0.7)]),
         right=dict(title="TIMELINE B", sub="saves half of every raise", col=TEAL, who="you", emo={0: "neutral", 3: "money"}, at=3, value=dict(**{"from": 0, "to": VAL[-1]}, at=3, dur=2.2, label="by Sep 2026", vcol=GREEN)),
         texts=[dict(text="SALARY x2 = STILL BROKE?", size=90, col=AMBER, y=800, at=2, glow=12)], flash={3: GREEN}, shake=[3])),
 ("start", [
   ("It's twenty twelve. You're twenty five, with your first real job. Forty thousand dollars a year, in this example.", None),
   ("You share a small apartment with Max. Your sofa came from the street. Dinner is noodles, and you're honestly kind of happy.", None),
   ("Every year, you get a raise of four thousand dollars. By twenty twenty two, you're making eighty thousand. Double.", None),
   ("And here's where your life splits into two timelines.", None),
 ], dict(type="stage", loc="living", actors=[you(560, {0: "happy", 3: "neutral"}), dict(who="max", x=1400, y=1010, size=300, emo="happy", flip=True)],
         props=[dict(kind="tag", text="$40,000 / YEAR", col=AMBER, x=980, y=320, at=0, scale=1.0, sub="2012, example salary"), dict(kind="tag", text="$80,000 BY 2022", col=GREEN, x=980, y=500, at=2, scale=1.0, sub="+$4,000 a year")],
         flash={3: AMBER}, shake=[3])),
 ("raise1", [
   ("Timeline A. First raise. Four thousand dollars more a year.", None),
   ("That's about three hundred and thirty a month, before tax. You deserve something. You move out from Max's place into your own apartment.", None),
   ("The new rent eats most of the raise. But hey, no more roommate stealing your yoghurt.", None),
   ("Next year, another raise. Time for a car payment. The year after that, a better gym, a few subscriptions, and dinners out instead of noodles.", None),
 ], dict(type="stage", loc="street", actors=[you(560, {0: "happy", 2: "smug", 3: "money"})],
         props=[dict(kind="icon", name="house", x=1200, y=420, at=1, until=2.9, scale=0.8), dict(kind="icon", name="car", x=1200, y=420, at=3, scale=0.9), dict(kind="tag", text="+$4,000 RAISE", col=GREEN, x=1200, y=200, at=0, scale=0.9)],
         texts=[dict(text="TIMELINE A", size=100, col=CORAL, x=560, y=150, glow=10)])),
 ("creep", [
   ("Each upgrade feels small and reasonable on its own. That's what makes it dangerous.", None),
   ("A bigger apartment. A car with heated seats. Takeaway three times a week because you're tired. Holidays that need another holiday to recover from.", None),
   ("None of these are bad things. The problem is that every single raise gets eaten before it ever reaches a savings account.", None),
   ("By twenty twenty two, timeline A earns twice as much. And at the end of every month, the bank balance looks exactly like it did when you ate noodles.", None),
 ], dict(type="stage", loc="living", actors=[you(560, {0: "neutral", 1: "happy", 3: "worried"})],
         props=[dict(kind="receipt", lines=[["Rent upgrade", "more"], ["Car payment", "more"], ["Takeaway", "more"], ["Subscriptions", "more"], ["Holidays", "more"]], total="$0 LEFT", x=1250, y=520, at=1, scale=1.1)],
         texts=[dict(text="LIFESTYLE CREEP", size=120, col=CORAL, y=150, at=0, glow=14)], flash={3: CORAL})),
 ("tax", [
   ("Quick reality check about raises. A four thousand dollar raise is not four thousand dollars in your pocket.", None),
   ("After income tax and other deductions, depending on where you live, a good chunk of it never reaches your account.", None),
   ("That's why a raise often feels smaller than it sounded in the meeting. And why it disappears so easily into a slightly nicer life.", None),
   ("Timeline B's half and half split is easier when it's set up before the first bigger paycheck ever arrives.", None),
 ], dict(type="stage", loc="office", actors=[you(560, {0: "happy", 1: "shock", 2: "worried", 3: "neutral"}), dict(who="banker", x=1450, y=1010, size=300, emo="neutral", flip=True)],
         props=[dict(kind="tag", text="RAISE: +$4,000", col=GREEN, x=1000, y=330, at=0, scale=1.0), dict(kind="tag", text="IN YOUR POCKET: LESS", col=CORAL, x=1000, y=520, at=1, scale=1.0, sub="taxes + deductions")],
         texts=[dict(text="RAISES SHRINK", size=110, col=AMBER, y=150, at=2, glow=12)])),
 ("b_rule", [
   ("Timeline B gets the exact same raises. But makes one simple rule on day one.", None),
   ("Half of every raise is for life. Half is for the future.", None),
   ("So with the first four thousand dollar raise, two thousand goes to life upgrades. And two thousand a year goes automatically into an index fund. About one hundred and sixty seven dollars a month.", None),
   ("Next raise, the same split. The investing amount keeps growing, but so does the lifestyle. Just slower.", None),
 ], dict(type="stage", loc="office", actors=[you(560, {0: "neutral", 1: "smug", 3: "happy"})],
         props=[dict(kind="tag", text="50% LIFE", col=AMBER, x=1200, y=360, at=1, scale=1.2), dict(kind="tag", text="50% FUTURE", col=TEAL, x=1200, y=540, at=1.3, scale=1.2), dict(kind="tag", text="$167 / MONTH", col=GREEN, x=1200, y=720, at=2, scale=0.9, sub="first year")],
         texts=[dict(text="TIMELINE B", size=100, col=TEAL, x=560, y=150, glow=10)])),
 ("b_life", [
   ("Is timeline B living like a monk? Not at all.", None),
   ("B still moves out from Max's place, a couple of years later. B still gets a car, a used one. B still goes on holidays, just not five star ones.", None),
   ("By twenty twenty two, B's lifestyle runs on about sixty thousand a year. Which is still fifty percent more than the noodle days.", None),
   ("The difference is that twenty thousand dollars a year now flows to the future, automatically, without B ever seeing it.", None),
 ], dict(type="split", left=dict(title="A'S LIFESTYLE", col=CORAL, who="you", emo="happy", value=dict(**{"from": 40000, "to": 80000}, at=2, dur=1.6, label="spent per year by 2022")),
         right=dict(title="B'S LIFESTYLE", col=TEAL, who="you", emo="happy", value=dict(**{"from": 40000, "to": 60000}, at=2, dur=1.6, label="spent per year by 2022")),
         texts=[dict(text="+$20,000 / YEAR TO THE FUTURE", size=70, col=GREEN, y=800, at=3, glow=10)])),
 ("y2020", [
   ("Then twenty twenty arrives, and with it the pandemic.", None),
   ("For a few months, both versions of you have their hours cut at work. Same job, same cut.", None),
   ("Timeline A has a car payment, a big rent and a stack of subscriptions, and no cushion. The credit card starts doing the heavy lifting.", None),
   ("Timeline B has the same cut. But B's fixed costs are lower, and there's a growing pile of savings behind them. B is worried, but not scared.", None),
   ("That's the hidden gift of a smaller lifestyle. It's not just cheaper. It's sturdier.", None),
 ], dict(type="split", left=dict(title="TIMELINE A, 2020", col=CORAL, who="you", emo="shock", props=[dict(kind="card", label="CARD", col=CORAL, x=640, y=560, scale=0.7)]),
         right=dict(title="TIMELINE B, 2020", col=TEAL, who="you", emo="worried", at=3, props=[dict(kind="icon", name="shield", x=1600, y=560, scale=0.6)]),
         texts=[dict(text="SMALLER = STURDIER", size=110, col=AMBER, y=800, at=4, glow=12)], flash={2: CORAL}, shake=[2])),
 ("chart", [
   ("Now let's run timeline B through real market history. Every month, half of the raises go into an S and P five hundred index fund, at real prices, starting in twenty twelve.", None),
   ("The first years are small. A couple of thousand a year.", None),
   ("Then the contributions grow with every raise, and the market does its thing.", None),
   ("By September twenty twenty six, timeline B has put in one hundred and eighty five thousand dollars.", None),
   ("And it's worth about three hundred and ninety two thousand.", None),
 ], dict(type="chart", reveal=(0, 3), series=[dict(values=VAL, col=TEAL, width=9, fill=True), dict(values=INV, col=AMBER, width=6)],
         xlabels=YEARS, side=[dict(label="PUT IN", values=INV, col=AMBER), dict(label="WORTH", values=VAL, col=TEAL)],
         footnote="Half of each raise above $40,000 (example salary, before tax), invested monthly at the S&P 500 monthly avg. price (R. Shiller), price only.",
         actors=[dict(who="you", x=1650, y=1070, size=150, emo={0: "neutral", 4: "money"})], flash={4: TEAL})),
 ("a_now", [
   ("And timeline A in twenty twenty six? Earning the same eighty thousand.", None),
   ("A nicer apartment. A nicer car. A lot of nice dinners.", None),
   ("And roughly zero dollars invested. One surprise bill away from the credit card.", None),
   ("Both timelines earned exactly the same money. One of them simply kept a piece of it.", None),
   ("And timeline B didn't need a single genius stock pick to get there. Just a rule, made once, and followed every year.", None),
 ], dict(type="bars", groups=[dict(label="TIMELINE A", sub="spent every raise", vals=[(0, CORAL)], at=2), dict(label="TIMELINE B", sub="saved half of every raise", vals=[(VAL[-1], TEAL)], at=3)],
         texts=[dict(text="SAME SALARY", size=110, col=CREAM, y=150, glow=12)], flash={3: TEAL})),
 ("repair", [
   ("Twenty twenty three. Both timelines hear the same terrible noise from the car.", None),
   ("Two thousand dollars to fix it.", None),
   ("Timeline A puts it on the credit card. At average card rates of over twenty percent, that repair will cost a lot more than two thousand by the time it's paid off.", None),
   ("Timeline B pays from savings, sighs, and moves on. The repair costs exactly two thousand dollars.", None),
   ("Same car. Same noise. One timeline pays extra for being broke.", None),
 ], dict(type="stage", loc="street", actors=[you(560, {0: "shock", 2: "worried", 3: "neutral"})],
         props=[dict(kind="icon", name="car", x=1200, y=600, at=0, scale=1.2, shake_at=0), dict(kind="tag", text="REPAIR $2,000", col=CORAL, x=1200, y=320, at=1, scale=1.0)],
         texts=[dict(text="BROKE COSTS EXTRA", size=110, col=CORAL, y=150, at=4, glow=12)], shake=[0])),
 ("options", [
   ("But the biggest difference isn't the number. It's what the number lets you do.", None),
   ("When timeline B's boss starts being unbearable, B can look for a new job without panicking about next month's rent.", None),
   ("When an opportunity shows up, like a course, a move, or a small business idea, B can afford to try it.", None),
   ("Money in the bank doesn't just buy things. It buys options. And options feel a lot like freedom.", None),
   ("Timeline A has a nicer car. Timeline B has a way out.", None),
 ], dict(type="stage", loc="office", actors=[you(560, {0: "neutral", 1: "smug", 4: "happy"}), dict(who="stranger", x=1450, y=1010, size=310, emo={0: "angry"}, flip=True, at=1)],
         props=[dict(kind="tag", text="NEW JOB?", col=TEAL, x=1000, y=320, at=1, scale=0.9), dict(kind="tag", text="A COURSE?", col=TEAL, x=1000, y=470, at=2, scale=0.9), dict(kind="tag", text="A MOVE?", col=TEAL, x=1000, y=620, at=2.3, scale=0.9)],
         texts=[dict(text="MONEY = OPTIONS", size=120, col=GREEN, y=150, at=3, glow=14)])),
 ("why", [
   ("Why does this happen to so many people? Because of something called hedonic adaptation.", None),
   ("A new car feels amazing for a few weeks. Then it's just your car. A bigger apartment feels huge, until it's just home.", None),
   ("The happiness fades, but the bill stays. Every month. And it makes the next raise feel necessary instead of extra.", None),
   ("Timeline A isn't greedy or stupid. It just never decided where the raise should go, so the raise decided for itself.", None),
 ], dict(type="stage", loc="void_red", actors=[you(1500, {0: "neutral", 1: "love", 2: "sad"})],
         props=[dict(kind="icon", name="car", x=650, y=500, at=1, scale=1.1), dict(kind="tag", text="WOW: 3 WEEKS", col=GREEN, x=650, y=300, at=1.3, scale=0.8), dict(kind="tag", text="BILL: EVERY MONTH", col=CORAL, x=650, y=720, at=2, scale=0.8)],
         texts=[dict(text="HEDONIC ADAPTATION", size=110, col=AMBER, y=150, at=0, glow=14)])),
 ("national", [
   ("And it's not just you. Look at the whole country.", None),
   ("In the US, the personal saving rate in October twenty twenty six was about four point one percent. Roughly four cents of every dollar people had after taxes.", None),
   ("In twenty twenty, during lockdowns, it briefly shot above thirty percent, because there was nothing to spend money on. Then it fell right back.", None),
   ("Meanwhile, average hourly pay almost doubled since two thousand six. Higher pay hasn't automatically meant more saving.", None),
 ], dict(type="chart", reveal=(0, 2), series=[dict(values=[PS[k] for k in PK], col=TEAL, width=8)], yfmt="{:.0f}%", vmax=35,
         xlabels=[(i, k[:4]) for i, k in enumerate(PK) if k.endswith("-01") and int(k[:4]) % 4 == 0], side=[dict(label="US SAVING RATE", values=[PS[k] for k in PK], col=TEAL, fmt="{:.1f}%")],
         footnote="Personal saving as a percent of disposable personal income (BEA via FRED PSAVERT).", actors=[dict(who="you", x=1650, y=1070, size=150, emo={0: "neutral", 2: "shock"})])),
 ("max", [
   ("Max, by the way, did timeline A on hard mode.", None),
   ("Every raise, he upgraded. Every bonus, he upgraded. When there was no raise, he upgraded on a credit card and called it an investment in himself.", None),
   ("In twenty twenty six, Max earns more than ever, and he asks you for twenty dollars until Friday.", None),
   ("You give it to him. You can afford it now.", None),
 ], dict(type="stage", loc="street", actors=[dict(who="max", x=620, y=1010, size=330, emo={0: "smug", 1: "money", 2: "worried"}, talk=[2]), you(1350, {0: "neutral", 3: "smug"}, flip=True)],
         props=[dict(kind="card", label="MAX'S CARD", col=CORAL, x=1000, y=360, at=1, scale=0.8), dict(kind="bill", amount="20", x=1000, y=620, at=3, scale=1.0)],
         bubbles=[dict(text="Twenty bucks till Friday?", x=620, y=500, at=2, until=3)])),
 ("how", [
   ("So how do you become timeline B? Three simple moves.", None),
   ("One. Decide before the raise arrives. Write down the split, like half and half, or even a quarter for the future. Any split beats no split.", None),
   ("Two. Make it automatic on the day the new salary starts. If the money never lands in your spending account, you won't miss it.", None),
   ("Three. Be careful with upgrades that come with monthly bills. A nice dinner is a one time cost. A bigger lease is a cost for years.", None),
   ("And enjoy the half you keep for life. That's the point. Timeline B is happy too.", None),
 ], dict(type="list", cards=True, title="HOW TO BE TIMELINE B", items=[dict(text="SPLIT FIRST", sub="decide before the raise", at=1), dict(text="AUTOMATE", sub="on day one of the raise", at=2), dict(text="WATCH MONTHLY BILLS", sub="leases, loans, subscriptions", at=3)])),
 ("honest", [
   ("And the honest part. This is not financial advice.", None),
   ("The salary here is an example, taxes are ignored to keep it simple, and the investing numbers use real past prices that don't promise the future.", None),
   ("Your split depends on your life. If you have expensive debt, paying that off first is often the best upgrade of all.", None),
 ], dict(type="list", title="NOT FINANCIAL ADVICE", tcol=CORAL, items=[dict(text="Example salary, taxes ignored", at=1), dict(text="Past returns, no promise", at=1.4), dict(text="Expensive debt first", at=2)],
         actors=[you(1680, "neutral", size=240, y=1040)])),
 ("outro", [
   ("Same raises. Same job. One timeline has a nicer car. The other has a choice.", None),
   ("Tell me in the comments: where did your last raise go?", None),
   ("And I'll see you in the other timeline.", None),
 ], dict(type="end", q1="WHERE DID YOUR", q2="LAST RAISE GO?", comment="Your last raise went to...?", comment_at=1, emo={0: "neutral", 1: "smug"})),
]

META = dict(
    file="EP08_Salary_Doubled_Still_Broke.mp4",
    title="What If Your Salary Doubled and You Stayed Broke?",
    description="""Two versions of you get the same raises, from $40,000 to $80,000. One upgrades everything and is still living paycheck to paycheck. The other saves half of every raise and ends up with about $392,000. Lifestyle inflation, explained with real market data.

Method: example salary $40,000 in 2012, +$4,000 a year to $80,000 (before tax). Timeline B invests half of every raise monthly at the S&P 500 monthly average price (Robert Shiller data), price only, Jan 2012 to Sep 2026. US personal saving rate: BEA via FRED PSAVERT. Average hourly earnings: BLS via FRED.
This video is for education and entertainment only. It is not financial advice.

#whatif #lifestyleinflation #personalfinance""",
    tags=["what if", "lifestyle inflation", "lifestyle creep", "save your raise", "paycheck to paycheck", "personal saving rate", "investing", "personal finance", "financial education", "money habits", "the other timeline", "animated story"],
    comment="Be honest: where did your last raise go? 👇",
    chapters={"hook": "Salary doubled, still broke", "start": "2012: noodles", "raise1": "Timeline A upgrades", "creep": "Lifestyle creep", "tax": "Why raises shrink", "b_rule": "Timeline B's rule", "b_life": "B is not a monk",
              "y2020": "2020: the stress test", "chart": "Half the raises, invested", "repair": "The $2,000 repair", "options": "Money = options", "a_now": "Same salary, different life", "why": "Why it happens", "national": "The whole country", "max": "Max on hard mode",
              "how": "How to be timeline B", "honest": "The honest part", "outro": "Where did your raise go?"},
)

THUMBS = {
    "A": dict(loc="street", quote="my salary doubled..", hl=["doubled.."], actors=[dict(who="you", x=480, size=560, emo="worried"), dict(who="max", x=1480, size=520, emo="money", flip=True)],
              props=[dict(kind="icon", name="car", x=980, y=700, scale=1.1)], big=dict(text="STILL BROKE", x=980, y=360, col=CORAL, size=170, rot=-4)),
    "B": dict(loc="void_teal", quote="same raise, 2 lives", hl=["2"], actors=[dict(who="you", x=460, size=560, emo="sad"), dict(who="you", x=1460, size=560, emo="money", flip=True)],
              big=dict(text="$0 vs $392K", x=960, y=380, col=GREEN, size=160)),
}

SHORT = dict(segs=[("hook", [0, 1, 2]), ("chart", [3, 4]), ("a_now", [2, 3])], title=["SALARY DOUBLED...", "STILL BROKE?"], hook=dict(text="$392,441", col=GREEN, dur=1.8),
             yt_title="Salary Doubled, Still Broke? #shorts",
             yt_desc="Same raises, two timelines. Saving half of every raise, invested at real S&P 500 prices since 2012 (example salary). Full video on the channel. Not financial advice. #money #whatif")
