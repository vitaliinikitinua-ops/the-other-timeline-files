"""EP06 — What If Every Price Tag Showed Hours of Your Life?  (superpower story)
US average hourly earnings, all private employees, Oct 2026: $38.00 (BLS CES via FRED CES0500000003); Mar 2006: $20.04.
Mar 2006 -> Oct 2026: wages x1.90, prices (CPI-U) x1.69 -> real hourly pay +12%.
Prices in the story are example prices, labelled as such. Hours = price / $38 (before tax).
1 hour of pay per week ($164.67/month) into S&P 500 from Jan 2010 to Sep 2026: $33,098 in -> $107,378 (Shiller, price only)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
from kit import *  # noqa
import data

WAGE = data.fred("CES0500000003")
W0 = WAGE["2026-10"]
SP = data.sp500()
ks, INV, VAL = data.dca(SP, "2010-01", "2026-09", W0 * 52 / 12)
WK = [k for k in sorted(WAGE) if k >= "2006-03"]
def h(price): return price / W0
def hs(price):
    x = h(price)
    return f"{x * 60:.0f} MIN" if x < 1 else (f"{x:.1f} HOURS" if x < 100 else f"{x:,.0f} HOURS")

SPEED = 1.18
MUSIC_SEED = 6
END_LINE = "IS IT WORTH THE HOURS?"

def you(x=960, emo="neutral", size=330, **k):
    return dict(who="you", x=x, y=k.pop("y", 1010), size=size, emo=emo, **k)

BEATS = [
 ("hook", [
   ("What if you woke up tomorrow, and every price tag in the world showed a new number?", None),
   ("Not dollars. Not euros. Hours. Hours of your life it takes to pay for that thing.", None),
   ("A coffee: nine minutes. A new phone: almost thirty two hours. A new car: over a thousand hours of your life.", None),
   ("Today you get that superpower. And by the end, you'll never look at a shopping cart the same way.", None),
 ], dict(type="stage", loc="store", actors=[you(1480, {0: "neutral", 1: "shock", 3: "smug"})],
         props=[dict(kind="tag", text=hs(6), col=AMBER, x=620, y=300, at=2, scale=0.9, sub="coffee, $6 example"), dict(kind="tag", text=hs(1199), col=CORAL, x=620, y=470, at=2.3, scale=0.9, sub="phone, $1,199 example"),
                dict(kind="tag", text=hs(40000), col=CORAL, x=620, y=640, at=2.6, scale=0.9, sub="car, $40,000 example")],
         texts=[dict(text="PRICES IN HOURS", size=140, col=AMBER, y=150, at=1, glow=16)], flash={1: AMBER}, shake=[1])),
 ("rate", [
   ("First, how many hours is a dollar? We need your hourly pay.", None),
   ("In October twenty twenty six, the average private sector worker in the US earned about thirty eight dollars an hour, before tax.", None),
   ("Your number might be higher or lower. And after tax, it's lower for almost everyone. But let's use thirty eight to keep it simple.", None),
   ("So every thirty eight dollars costs you one hour of your life. That's the exchange rate of your new superpower.", None),
   ("In Europe the numbers are different, but the idea is exactly the same. Take your pay after tax, divide by your hours, and that's your price of one hour.", None),
 ], dict(type="stage", loc="office", actors=[you(560, {0: "neutral", 3: "smug"})],
         props=[dict(kind="tag", text="$38.00 / HOUR", col=TEAL, x=1250, y=420, at=1, scale=1.3, sub="US avg, Oct 2026, before tax"), dict(kind="tag", text="$38 = 1 HOUR", col=AMBER, x=1250, y=660, at=3, scale=1.2)],
         texts=[dict(text="YOUR EXCHANGE RATE", size=110, col=CREAM, y=160, glow=10)])),
 ("cafe", [
   ("Monday morning. The coffee shop.", None),
   ("The barista smiles. A large oat latte with caramel? Your eyes see the tag: nine minutes.", None),
   ("Nine minutes doesn't sound like much. But you buy one every workday.", None),
   ("That's about three and a half hours a month. Almost half a working day, every month, for coffee.", None),
   ("You still buy it. But now you actually taste it.", None),
   ("Because something you pay for with your life should at least be enjoyed, not swallowed on the way to the bus.", None),
 ], dict(type="stage", loc="cafe", actors=[dict(who="barista", x=1350, y=1010, size=320, emo="happy", flip=True, talk=[1]), you(600, {0: "neutral", 1: "shock", 4: "happy"})],
         props=[dict(kind="tag", text="9 MIN", col=AMBER, x=980, y=330, at=1, scale=1.1), dict(kind="tag", text="3.5 HOURS / MONTH", col=CORAL, x=980, y=520, at=3, scale=0.9, sub="22 workdays x $6")],
         bubbles=[dict(text="Large oat latte with caramel?", x=1350, y=500, at=1, until=2)])),
 ("grocery", [
   ("Tuesday. The supermarket. This is where the superpower gets loud.", None),
   ("Every snack shouts its hours at you. The fancy brand cereal: eighteen minutes. The store brand next to it: ten.", None),
   ("Pre-cut fruit, bottled water, ready meals. Each one only a few minutes. But a weekly shop is made of fifty little decisions.", None),
   ("You don't buy the cheapest thing every time. You just stop paying for convenience you don't even want.", None),
   ("At the checkout, the total is about an hour less than last week. Nobody else even notices. You do.", None),
 ], dict(type="stage", loc="store", actors=[you(1500, {0: "neutral", 1: "shock", 4: "happy"})],
         props=[dict(kind="tag", text="18 MIN", col=CORAL, x=600, y=320, at=1, scale=1.0, sub="brand cereal, $11.40 example"), dict(kind="tag", text="10 MIN", col=GREEN, x=600, y=520, at=1.4, scale=1.0, sub="store brand, $6.30 example"),
                dict(kind="tag", text="-1 HOUR / WEEK", col=GREEN, x=600, y=740, at=4, scale=1.0)],
         texts=[dict(text="50 LITTLE DECISIONS", size=100, col=AMBER, y=150, at=2, glow=12)])),
 ("max_car", [
   ("At lunch, Max shows you pictures of a new car. Forty thousand dollars. He's already picked the colour.", None),
   ("Above the car, your superpower shows the real price. One thousand and fifty three hours.", None),
   ("That's about twenty six full work weeks. Half a year of Mondays, just for the car. Before insurance, fuel or repairs.", None),
   ("Max looks at the number for a long time. Then he asks if the red one is more expensive.", None),
 ], dict(type="stage", loc="dealer", actors=[dict(who="max", x=600, y=1010, size=330, emo={0: "love", 2: "shock", 3: "worried"}, talk=[0, 3]), dict(who="seller", x=1450, y=1010, size=310, emo="happy", flip=True)],
         props=[dict(kind="icon", name="car", x=1020, y=600, at=0, scale=1.3), dict(kind="tag", text=hs(40000), col=CORAL, x=1020, y=330, at=1, scale=1.2, sub="$40,000 example car")],
         texts=[dict(text="26 WORK WEEKS", size=120, col=CORAL, y=160, at=2, glow=14)], flash={1: CORAL}, shake=[1])),
 ("commute", [
   ("Wednesday, the superpower shows you something sneakier. Your hourly pay is probably lower than you think.", None),
   ("Say you work forty hours a week, but you also spend an hour every day getting to and from work. Unpaid.", None),
   ("That's forty five hours of your life for forty hours of pay. Your thirty eight dollars an hour quietly becomes about thirty four.", None),
   ("Add work clothes, lunches out and the after work takeaway because you're too tired to cook, and it drops even more.", None),
   ("So when you translate prices into hours, use your real hours, not the ones on the contract.", None),
 ], dict(type="stage", loc="street", actors=[you(560, {0: "neutral", 2: "shock", 4: "smug"})],
         props=[dict(kind="tag", text="40 PAID + 5 COMMUTE", col=AMBER, x=1250, y=320, at=1, scale=0.9, sub="example week"), dict(kind="tag", text="$38 BECOMES ~$34 / HOUR", col=CORAL, x=1250, y=520, at=2, scale=0.9), dict(kind="icon", name="car", x=1250, y=740, at=1, scale=0.7)],
         texts=[dict(text="YOUR REAL HOURLY PAY", size=96, col=CORAL, y=150, at=0, glow=12)])),
 ("subs", [
   ("Evening. You open your phone and the superpower lights up your subscriptions.", None),
   ("Streaming, music, cloud storage, an app you forgot, a gym you visit twice a year.", None),
   ("Ninety dollars a month in this example. That's two hours and twenty minutes a month. Over twenty eight hours a year.", None),
   ("Three and a half work days a year, paid automatically, for things you barely notice.", None),
   ("You cancel two of them before bed. That's a few hours of your year, back.", None),
 ], dict(type="stage", loc="bedroom", actors=[you(700, {0: "neutral", 2: "shock", 4: "smug"})],
         props=[dict(kind="receipt", lines=[["Streaming", "$18"], ["Music", "$11"], ["Cloud", "$10"], ["Forgotten app", "$9"], ["Gym", "$42"]], total="$90/mo", x=1300, y=520, at=1, scale=1.0),
                dict(kind="tag", text="28 HOURS / YEAR", col=CORAL, x=1300, y=170, at=2, scale=1.0)])),
 ("rent", [
   ("And then the big one. Rent.", None),
   ("In this example, eighteen hundred dollars a month. Forty seven hours. More than a full work week, every month, just for the roof.", None),
   ("You can't stop paying rent. But now you understand why housing is the biggest decision in most people's money.", None),
   ("A slightly cheaper place, or a roommate, can be worth more hours than a lifetime of skipped coffees.", None),
 ], dict(type="stage", loc="living", actors=[you(560, {0: "neutral", 1: "shock", 3: "smug"})],
         props=[dict(kind="icon", name="house", x=1250, y=520, at=0, scale=1.2), dict(kind="tag", text=hs(1800), col=CORAL, x=1250, y=260, at=1, scale=1.1, sub="$1,800 example rent")],
         texts=[dict(text="BIG THINGS > SMALL THINGS", size=96, col=AMBER, y=150, at=3, glow=12)])),
 ("phone", [
   ("Then your phone does the most dangerous thing a phone can do. It shows you an ad for a newer phone.", None),
   ("Eleven hundred and ninety nine dollars in this example. Thirty one and a half hours.", None),
   ("And here's the trick. If you upgrade every two years instead of every four, you pay those thirty one hours twice as often.", None),
   ("Over twenty years, that's the difference between about one hundred and sixty hours and over three hundred. Four extra work weeks, for a slightly better camera.", None),
   ("Your current phone suddenly looks fantastic.", None),
   ("You put it in a new case, clean the screen, and it feels almost new. Zero hours spent.", None),
 ], dict(type="stage", loc="bedroom", actors=[you(620, {0: "love", 2: "shock", 4: "happy"})],
         props=[dict(kind="icon", name="iphone", x=1050, y=520, at=0, scale=1.0), dict(kind="tag", text="31.6 HOURS", col=CORAL, x=1450, y=330, at=1, scale=1.0, sub="$1,199 example phone"),
                dict(kind="tag", text="EVERY 2 YEARS: 316 H", col=CORAL, x=1450, y=560, at=3, scale=0.8, sub="over 20 years"), dict(kind="tag", text="EVERY 4 YEARS: 158 H", col=GREEN, x=1450, y=700, at=3.3, scale=0.8)],
         texts=[dict(text="+4 WORK WEEKS", size=110, col=CORAL, y=150, at=3, glow=12)])),
 ("max_debt", [
   ("Thursday. Max asks you to look at his credit card statement with your superpower. Big mistake.", None),
   ("He owes five thousand dollars and pays the minimum. The superpower doesn't show the balance. It shows the interest.", None),
   ("At today's average card rates, paying the minimum on that balance could cost him over seven thousand dollars in interest. That's over two hundred hours. Just interest.", None),
   ("Five full work weeks, for the privilege of having bought things earlier.", None),
   ("Max closes the app, opens it again, and sets up a fixed payment. Character development.", None),
 ], dict(type="stage", loc="living", actors=[dict(who="max", x=600, y=1010, size=330, emo={0: "happy", 2: "shock", 4: "neutral"}), you(1380, {0: "neutral", 2: "worried", 4: "happy"}, flip=True)],
         props=[dict(kind="card", label="MAX'S CARD", col=CORAL, x=1000, y=340, at=1, scale=0.9), dict(kind="tag", text="205 HOURS OF INTEREST", col=CORAL, x=1000, y=600, at=2, scale=1.0, sub="$7,782 at 21.19% APR, minimum payments")],
         texts=[dict(text="5 WORK WEEKS", size=110, col=CORAL, y=160, at=3, glow=12)], flash={2: CORAL}, shake=[2])),
 ("date", [
   ("By Friday, the superpower is changing how you live.", None),
   ("A concert ticket: two and a half hours. Totally worth it. You go.", None),
   ("A random gadget at two in the morning: four hours. Not worth it. Cart deleted.", None),
   ("You're not spending less on everything. You're spending more on the things that matter, and nothing on the things that don't.", None),
   ("That's the real superpower. Not being cheap. Being clear.", None),
 ], dict(type="split", left=dict(title="WORTH IT", col=GREEN, who="you", emo="happy", props=[dict(kind="tag", text="CONCERT 2.5 H", col=GREEN, x=640, y=560, scale=0.8)], at=1),
         right=dict(title="NOT WORTH IT", col=CORAL, who="you", emo="smug", at=2, props=[dict(kind="tag", text="GADGET 4 H", col=CORAL, x=1600, y=560, scale=0.8)]),
         texts=[dict(text="NOT CHEAP. CLEAR.", size=110, col=AMBER, y=800, at=4, glow=12)])),
 ("grandma", [
   ("On Saturday, you visit Grandma. She asks why you keep squinting at the price of her biscuits.", None),
   ("You explain the superpower. She laughs, and says she's been doing this her whole life. She just never called it a superpower.", None),
   ("When I was young, she says, we asked one question before we bought anything. How long did I work for this?", None),
   ("Then she hands you a biscuit. Zero hours. Free. The best price in the world.", None),
 ], dict(type="stage", loc="kitchen", actors=[you(600, {0: "neutral", 1: "shock", 3: "love"}), dict(who="grandma", x=1350, y=1010, size=320, emo={0: "neutral", 1: "happy"}, flip=True, talk=[1, 2])],
         bubbles=[dict(text="How long did I work for this?", x=1350, y=500, at=2, until=3)],
         props=[dict(kind="tag", text="0 HOURS", col=GREEN, x=980, y=360, at=3, scale=1.2, sub="grandma's biscuit")])),
 ("wage_history", [
   ("Now here's an uncomfortable twist. Is your hour worth more than it used to be?", None),
   ("In March two thousand six, the average US hourly pay was about twenty dollars. Today it's thirty eight. Almost double.", None),
   ("But prices rose too. The consumer price index went up about sixty nine percent over the same years.", None),
   ("So, after inflation, an hour of work buys only about twelve percent more than it did in two thousand six.", None),
   ("Twenty years of work history, and your hour got about twelve percent stronger. That's why every hour you spend matters.", None),
 ], dict(type="chart", reveal=(0, 2), series=[dict(values=[WAGE[k] for k in WK], col=TEAL, width=9, fill=True)], vmax=45,
         yfmt="${:,.0f}", xlabels=[(i, k[:4]) for i, k in enumerate(WK) if k.endswith("-01") and int(k[:4]) % 4 == 2],
         side=[dict(label="AVG HOURLY PAY", values=[WAGE[k] for k in WK], col=TEAL, fmt="${:,.2f}")],
         footnote="Average hourly earnings of all private employees (BLS CES via FRED CES0500000003). Real change uses CPI-U.",
         texts=[dict(text="REAL: +12%", size=120, col=AMBER, x=760, y=170, at=3, glow=14)], actors=[dict(who="you", x=1650, y=1070, size=150, emo={0: "neutral", 3: "shock"})])),
 ("buy_back", [
   ("So what if you could use the superpower in reverse? Not to spend hours, but to buy them back?", None),
   ("Here's the idea. Take just one hour of pay per week, thirty eight dollars, and invest it instead of spending it.", None),
   ("That's about one hundred and sixty five dollars a month. Let's put it in an S and P five hundred index fund, starting in January twenty ten, at real prices.", None),
   ("By September twenty twenty six, you've put in about thirty three thousand dollars.", None),
   ("And it's worth about one hundred and seven thousand.", None),
 ], dict(type="chart", reveal=(2, 4), series=[dict(values=VAL, col=GREEN, width=9, fill=True), dict(values=INV, col=AMBER, width=6)],
         xlabels=[(i, k[:4]) for i, k in enumerate(ks) if k.endswith("-01") and int(k[:4]) % 2 == 0],
         side=[dict(label="PUT IN", values=INV, col=AMBER), dict(label="WORTH", values=VAL, col=GREEN)],
         footnote="$164.67 (one hour of $38 pay per week) on the 1st of each month, S&P 500 monthly avg. price (R. Shiller), price only. Not financial advice.",
         actors=[dict(who="you", x=1650, y=1070, size=150, emo={0: "neutral", 4: "money"})])),
 ("freedom_hours", [
   ("Now turn that back into hours. One hundred and seven thousand dollars, at thirty eight dollars an hour, is over two thousand eight hundred hours.", None),
   ("That is about one year and four months of full time work. Bought back with one hour a week.", None),
   ("That money could be a career break, a safety net, a house deposit, or simply the freedom to say no to a job you hate.", None),
   ("That's what money really is. Stored time. You decide whether it's stored for someone else, or for you.", None),
 ], dict(type="stage", loc="void_teal", actors=[you(1500, {0: "neutral", 1: "shock", 3: "happy"})],
         counters=[dict(label="HOURS BOUGHT BACK", **{"from": 0, "to": VAL[-1] / W0}, at=0, dur=2.2, x=650, y=400, col=GREEN, size=160, fmt="int")],
         texts=[dict(text="MONEY = STORED TIME", size=110, col=AMBER, y=170, at=3, glow=14), dict(text="~1.4 YEARS OF WORK", size=80, col=CREAM, x=650, y=620, at=1, glow=8)], flash={1: GREEN})),
 ("how", [
   ("You don't need a superpower to do this. Three simple habits.", None),
   ("One. Before any purchase over fifty dollars, divide the price by your take home hourly pay. Say the hours out loud.", None),
   ("Two. Look at the big three first: housing, transport and food. That's where most of your hours go.", None),
   ("Three. Pay yourself first. Move one hour of pay a week to savings or investing on payday, automatically.", None),
   ("And one bonus habit. Once a year, add up your recurring payments and convert them into hours. It's the most honest number you'll see all year.", None),
 ], dict(type="list", cards=True, title="THE SUPERPOWER, WITHOUT MAGIC", items=[dict(text="PRICE / HOURLY PAY", sub="say the hours out loud", at=1), dict(text="BIG THREE FIRST", sub="housing, transport, food", at=2), dict(text="1 HOUR A WEEK", sub="pay yourself first", at=3)])),
 ("honest", [
   ("The honest part. This is not financial advice.", None),
   ("The prices in this story are examples, your hourly pay is your own, and taxes change everything.", None),
   ("And the investing numbers use real past prices, which don't promise the future.", None),
 ], dict(type="list", title="NOT FINANCIAL ADVICE", tcol=CORAL, items=[dict(text="Prices here are examples", at=1), dict(text="Use your own after-tax pay", at=1.4), dict(text="Past returns, no promise", at=2)],
         actors=[you(1680, "neutral", size=240, y=1040)])),
 ("outro", [
   ("Every price is a question. How many hours of my life is this worth?", None),
   ("So tell me in the comments: what's one thing you buy that suddenly feels too expensive when you count it in hours?", None),
   ("And I'll see you in the other timeline.", None),
 ], dict(type="end", q1="IS IT WORTH", q2="THE HOURS?", comment="Too many hours for...?", comment_at=1, emo={0: "neutral", 1: "smug"})),
]

META = dict(
    file="EP06_Price_Tags_in_Hours.mp4",
    title="What If Every Price Tag Showed Hours of Your Life?",
    description="""You wake up with a strange superpower: every price tag shows how many hours of your life it costs. A coffee is 9 minutes. A car is over 1,000 hours. Then we use the power in reverse and buy hours back.

Data: US average hourly earnings of all private employees, $38.00 in Oct 2026 (BLS CES via FRED CES0500000003), CPI-U for the real change since 2006. Prices in the story are examples. Investing example: S&P 500 monthly average price (Robert Shiller data), price only.
This video is for education and entertainment only. It is not financial advice.

#whatif #money #personalfinance""",
    tags=["what if", "price in hours", "time is money", "hourly wage", "budgeting", "subscriptions", "lifestyle inflation", "personal finance", "financial education", "saving money", "the other timeline", "animated story"],
    comment="What's one thing that suddenly feels too expensive when you count it in HOURS? 👇",
    chapters={"hook": "Prices in hours", "rate": "Your exchange rate", "cafe": "The 9-minute coffee", "grocery": "The supermarket", "max_car": "Max and the 1,053-hour car", "commute": "Your real hourly pay", "phone": "The phone upgrade", "max_debt": "Max's card in hours", "grandma": "Grandma knew", "subs": "Subscriptions", "rent": "The big one: rent",
              "date": "Worth it or not", "wage_history": "Is your hour worth more?", "buy_back": "Buying hours back", "freedom_hours": "Money = stored time", "how": "3 habits",
              "honest": "The honest part", "outro": "Is it worth the hours?"},
)

THUMBS = {
    "A": dict(loc="dealer", quote="this car costs 1,053 hours..", hl=["1,053", "hours.."], actors=[dict(who="you", x=480, size=560, emo="shock"), dict(who="seller", x=1480, size=520, emo="smug", flip=True)],
              props=[dict(kind="icon", name="car", x=980, y=700, scale=1.3), dict(kind="tag", text="1,053 HOURS", col=CORAL, x=980, y=400, scale=1.3)]),
    "B": dict(loc="cafe", quote="this coffee = 9 minutes", hl=["9", "minutes"], actors=[dict(who="you", x=520, size=560, emo="shock"), dict(who="barista", x=1460, size=520, emo="happy", flip=True)],
              props=[dict(kind="tag", text="9 MIN", col=AMBER, x=980, y=520, scale=1.6)], line=(1380, 560, 640, 600), lcol=AMBER),
}

SHORT = dict(segs=[("hook", [1, 2]), ("max_car", [1, 2, 3]), ("subs", [2])], title=["WHAT IF PRICES", "SHOWED HOURS?"], hook=dict(text="1,053 HOURS", col=CORAL, dur=1.8),
             yt_title="Price Tags in HOURS of Your Life #shorts",
             yt_desc="US average pay $38/hour (BLS, Oct 2026). A $40,000 car = 1,053 hours. Full video on the channel. Not financial advice. #money #whatif")
