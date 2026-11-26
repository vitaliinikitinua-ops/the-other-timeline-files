"""EP01 — What If You Got $1 Every Time You Said No?  (superpower story + real math)
Numbers (engine/data.py, S&P 500 Shiller monthly avg price, price only, Jan 2010 - Sep 2026):
$1/day -> invested $6,114, worth $19,834; $5/day -> $30,569 -> $99,172; $10/day -> $61,137 -> $198,344.
$100/month -> $20,100 -> $65,209. US avg hourly earnings Oct 2026: $38.00 (FRED CES0500000003)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
from kit import *  # noqa
import data

SP = data.sp500()
ks, INV, VAL = data.dca(SP, "2010-01", "2026-09", 5 * 365 / 12)
YEARS = [(i, k[:4]) for i, k in enumerate(ks) if k.endswith("-01") and int(k[:4]) % 2 == 0]

SPEED = 1.18
MUSIC_SEED = 1
END_LINE = "WHAT WOULD YOU SAY NO TO?"

def you(x=960, emo="neutral", size=330, **k):
    return dict(who="you", x=x, y=k.pop("y", 1010), size=size, emo=emo, **k)

BEATS = [
 ("hook", [
   ("What if, every time you said one tiny word, a dollar appeared in your pocket?", None),
   ("The word is no.", None),
   ("No to the snooze button. No to the upgrade. No to the thing you didn't even want.", None),
   ("Sounds like the easiest money on Earth.", None),
   ("But by the end of this video, you'll see why that single dollar is worth way more than a dollar.", None),
   ("And why one no almost cost you everything.", None),
 ], dict(type="stage", loc="void", actors=[you(960, {0: "neutral", 1: "shock", 3: "money", 5: "worried"})],
         texts=[dict(text="NO = +$1", size=170, col=GREEN, y=260, at=1, glow=18)],
         rain=[dict(kind="bill", at=3, until=4.5, n=26)],
         props=[dict(kind="coin", x=640, y=520, at=1, scale=1.0), dict(kind="coin", x=1290, y=480, at=2, scale=0.8)],
         flash={1: GREEN}, shake=[1], focus={"default": (960, 560)})),
 ("wake", [
   ("It starts on a Monday. Your alarm goes off at seven.", None),
   ("Your thumb is already on the snooze button, and you mumble the word.", None),
   ("No.", None),
   ("Ding. A crisp one dollar bill drops onto your pillow.", None),
   ("You stare at it. You say it again, just to test. No.", None),
   ("Ding. Another one.", None),
 ], dict(type="stage", loc="bedroom", actors=[you(700, {0: "sad", 2: "neutral", 3: "shock", 5: "money"}, y=1010)],
         props=[dict(kind="bill", amount="1", x=700, y=560, at=3, scale=0.9, rot=-8), dict(kind="bill", amount="1", x=1010, y=600, at=5, scale=0.9, rot=10),
                dict(kind="phone", text="07:00", sub="ALARM", col=CORAL, x=1250, y=640, at=0, until=3, scale=0.9)],
         texts=[dict(text="+$1", size=120, col=GREEN, x=760, y=380, at=3, until=4, glow=12), dict(text="+$1", size=120, col=GREEN, x=1060, y=380, at=5, glow=12)],
         flash={3: GREEN, 5: GREEN}, focus={"default": (760, 560)})),
 ("rule", [
   ("So here are the rules of your new life.", None),
   ("Every time you say no and mean it, you get one dollar. Real money, in your account.", None),
   ("It has to be a real no to something you were about to do or buy.", None),
   ("You can't stand in front of a mirror shouting no all day. You tried. Nothing happened.", None),
   ("And the money only counts if you keep it.", None),
 ], dict(type="list", loc="void", title="THE RULES", items=[
         dict(text="Say no, mean it: +$1", at=1), dict(text="Only real decisions count", at=2), dict(text="No cheating in the mirror", at=3), dict(text="Keep it, or it's gone", at=4)],
         actors=[you(1640, {0: "neutral", 3: "sad"}, size=260, y=1040)])),
 ("cafe", [
   ("First stop, the coffee shop. The barista already knows your order.", None),
   ("The usual? Large caramel latte with an extra shot?", None),
   ("You open your mouth, and out comes a no. Just a regular black coffee, please.", None),
   ("Ding. Plus one dollar. And you saved three more on the drink itself.", None),
   ("The barista looks at you like you just insulted her mother.", None),
 ], dict(type="stage", loc="cafe", actors=[dict(who="barista", x=1320, y=1000, size=330, emo={0: "happy", 4: "angry"}, flip=True, talk=[1]),
                                           you(620, {0: "neutral", 3: "money", 4: "worried"})],
         bubbles=[dict(text="The usual? Large caramel latte + extra shot?", x=1320, y=430, at=1, until=2), dict(text="No. Just black coffee.", x=620, y=430, at=2, until=3)],
         texts=[dict(text="+$1", size=130, col=GREEN, x=620, y=300, at=3, glow=12)],
         props=[dict(kind="tag", text="$7.40", col=CORAL, x=960, y=330, at=1, until=2.9, scale=0.9), dict(kind="tag", text="$3.10", col=GREEN, x=960, y=330, at=3, scale=0.9)],
         flash={3: GREEN}, focus={1: (1320, 560), 2: (620, 560), "default": (960, 560)})),
 ("max", [
   ("Then your phone buzzes. It's Max, your best friend and the worst financial advisor alive.", None),
   ("Bro. Limited drop. Sneakers. Two hundred and twenty dollars. They sell out in ten minutes.", None),
   ("Your heart says yes. Your thumb types no.", None),
   ("Ding. And somewhere, two hundred and twenty dollars stay exactly where they are.", None),
   ("Max sends eleven crying emojis.", None),
 ], dict(type="stage", loc="street", actors=[you(560, {0: "neutral", 2: "worried", 3: "smug"}), dict(who="max", x=1380, y=1010, size=330, emo={0: "happy", 4: "sad"}, talk=[1])],
         props=[dict(kind="tag", text="$220", col=CORAL, x=1380, y=330, at=1, scale=1.2, sub="LIMITED DROP"), dict(kind="phone", text="NO", sub="REPLY", col=CORAL, x=840, y=600, at=2, scale=0.8)],
         bubbles=[dict(text="BRO. Limited drop. 10 minutes!!", x=1380, y=520, at=1, until=2)],
         texts=[dict(text="+$1", size=130, col=GREEN, x=560, y=320, at=3, glow=12), dict(text="CRYING x11", size=70, col=CREAM, x=1380, y=520, at=4)],
         lines=[dict(**{"from": (1380, 480), "to": (620, 420)}, at=3, col=GREEN)], flash={3: GREEN})),
 ("day1", [
   ("By the end of day one, you've said no seven times.", None),
   ("No to the snooze. No to the latte. No to the sneakers. No to a free trial you would have forgotten to cancel.", None),
   ("No to delivery, when there was food in the fridge.", None),
   ("Seven dollars. It doesn't sound like a superpower. It sounds like a coupon.", None),
   ("But you're not looking at the seven dollars. You're looking at what you didn't spend.", None),
   ("Two hundred and sixty dollars, in one day, just because you paused.", "Two hundred and sixty dollars, in one day, just because you paused."),
 ], dict(type="stage", loc="kitchen", actors=[you(1500, {0: "neutral", 3: "sad", 5: "shock"}, size=300)],
         props=[dict(kind="receipt", lines=[["Latte upgrade", "$4"], ["Sneakers", "$220"], ["Free trial", "$15"], ["Delivery", "$21"]], total="$260", x=760, y=560, at=1, scale=1.1)],
         counters=[dict(label="POWER MONEY", **{"from": 0, "to": 7}, x=1480, y=300, at=0, dur=2.0, col=GREEN, size=100)],
         texts=[dict(text="NOT SPENT: $260", size=110, col=AMBER, x=760, y=180, at=5, glow=14)], flash={5: AMBER}, shake=[5])),
 ("week", [
   ("By Friday, you've become a professional.", None),
   ("No to the extra charger. No to the gym you never go to. No to the third streaming service.", None),
   ("You start saying no to things before anyone even offers them.", None),
   ("The cashier asks if you want a bag. No. Ding.", None),
   ("Your bank app starts to look different. For the first time, the number at the end of the week is bigger than the number at the start.", None),
 ], dict(type="stage", loc="store", actors=[you(560, {0: "smug", 3: "happy"}), dict(who="seller", x=1450, y=1010, size=310, emo={0: "happy", 3: "worried"}, flip=True, talk=[3])],
         props=[dict(kind="tag", text="CHARGER $29", col=CORAL, x=980, y=300, at=1, until=2, scale=0.7), dict(kind="tag", text="GYM $49/mo", col=CORAL, x=980, y=420, at=1, until=2, scale=0.7), dict(kind="tag", text="STREAMING $18", col=CORAL, x=980, y=540, at=1, until=2, scale=0.7),
                dict(kind="phone", text="+$412", sub="THIS WEEK", col=GREEN, x=980, y=560, at=4, scale=1.0)],
         bubbles=[dict(text="Need a bag?", x=1450, y=520, at=3, until=4), dict(text="No.", x=560, y=520, at=3, until=4)],
         texts=[dict(text="+$1", size=120, col=GREEN, x=560, y=300, at=3, until=4.5, glow=12)], flash={3: GREEN})),
 ("max_hack", [
   ("Of course, Max finds out.", None),
   ("He shows up at your door with a notebook and a terrible plan.", None),
   ("Okay, I ask you stupid questions all day, you say no, we split the money. Do you want a pet crocodile?", None),
   ("No. Nothing happens. Not a single dollar.", None),
   ("Because the power only pays when the no actually costs you something. When there was a real yes on the table.", None),
   ("Max looks at the notebook, sighs, and asks if you want to get pizza. You almost say yes. Almost.", None),
 ], dict(type="stage", loc="living", actors=[you(620, {0: "neutral", 3: "smug", 5: "worried"}), dict(who="max", x=1350, y=1010, size=320, emo={0: "smug", 3: "shock", 5: "happy"}, flip=True, talk=[2, 5])],
         props=[dict(kind="receipt", lines=[["Q1 crocodile?", "no"], ["Q2 moon trip?", "no"], ["Profit", "$0"]], x=1000, y=520, at=1, until=4, scale=0.9)],
         bubbles=[dict(text="Want a pet crocodile?", x=1350, y=500, at=2, until=3), dict(text="Pizza?", x=1350, y=520, at=5)],
         texts=[dict(text="+$0", size=130, col=CORAL, x=620, y=300, at=3, until=4.6, glow=10), dict(text="ONLY REAL NO'S PAY", size=90, col=AMBER, y=170, at=4, glow=10)],
         flash={3: CORAL})),
 ("month", [
   ("One month in, you check the score.", None),
   ("The magic dollars add up to two hundred and three. Nice, but not life changing.", None),
   ("The money you didn't spend is a different story. Over one thousand dollars, still sitting in your account.", None),
   ("That's the secret nobody puts on a thumbnail. The dollar was the reward. The real money was everything you didn't buy.", None),
   ("And you start to wonder. What happens if this keeps going for years?", None),
 ], dict(type="split", left=dict(title="MAGIC DOLLARS", col=GREEN, who="you", emo="neutral", at=1, value=dict(**{"from": 0, "to": 203}, at=1, dur=1.6, label="one month")),
         right=dict(title="NOT SPENT", col=AMBER, at=2, value=dict(**{"from": 0, "to": 1000}, at=2, dur=1.8, prefix="", suffix="+", label="one month"), props=[dict(kind="jar", fill=0.8, x=1440, y=720)]),
         texts=[dict(text="THE REAL MONEY = WHAT YOU DIDN'T BUY", size=66, col=CREAM, y=840, at=3, glow=8)], flash={2: AMBER})),
 ("problem", [
   ("And that's when things get weird.", None),
   ("Your grandma calls. Sunday dinner, sweetheart? I made your favourite pie.", None),
   ("And before you can think, the word slips out. No.", None),
   ("Ding.", None),
   ("For the first time, the dollar feels heavy.", None),
   ("Because some things you say no to don't come back.", None),
 ], dict(type="stage", loc="living", actors=[dict(who="grandma", x=1400, y=1010, size=320, emo={0: "happy", 2: "sad"}, flip=True, talk=[1]), you(560, {0: "neutral", 2: "shock", 4: "sad"})],
         bubbles=[dict(text="Sunday dinner, sweetheart? I made your favourite pie!", x=1400, y=500, at=1, until=2)],
         texts=[dict(text="+$1", size=120, col=GREY, x=560, y=320, at=3, until=5)],
         props=[dict(kind="icon", name="warning", x=960, y=320, at=5, scale=0.6)], flash={3: GREY}, static=False)),
 ("lesson", [
   ("So you sit in your kitchen and you realise the power was never about the dollar.", None),
   ("The power was the pause. The tiny second between the urge and the purchase.", None),
   ("That second is where your money lives.", None),
   ("And the trick is not to say no to everything. It's to say no to things, so you can say yes to people.", None),
   ("You call Grandma back. Yes. Yes to the pie. No dollar. Totally worth it.", None),
 ], dict(type="stage", loc="kitchen", actors=[you(760, {0: "sad", 1: "neutral", 3: "happy", 4: "love"}), dict(who="grandma", x=1450, y=1010, size=300, emo="happy", at=4, flip=True)],
         texts=[dict(text="THE POWER = THE PAUSE", size=100, col=AMBER, y=200, at=1, glow=12), dict(text="NO TO THINGS. YES TO PEOPLE.", size=86, col=TEAL, y=320, at=3, glow=10)],
         props=[dict(kind="phone", text="CALL", sub="GRANDMA", col=GREEN, x=1150, y=600, at=4, until=4.6, scale=0.8)])),
 ("why_hard", [
   ("And saying no is hard for a reason. The world is designed to get a yes out of you.", None),
   ("Countdown timers. Limited drops. Free trials that quietly turn into monthly payments.", None),
   ("Buy now, pay later buttons that make two hundred dollars look like four small, friendly numbers.", None),
   ("None of that is illegal. It just works best on people who don't pause.", None),
   ("Your new superpower simply gives you one second to notice the trick.", None),
 ], dict(type="stage", loc="store", actors=[you(1500, {0: "neutral", 1: "worried", 4: "smug"}, size=300)],
         props=[dict(kind="tag", text="ENDS IN 09:59", col=CORAL, x=600, y=300, at=1, scale=0.9), dict(kind="tag", text="FREE TRIAL*", col=AMBER, x=600, y=470, at=1.5, scale=0.9),
                dict(kind="tag", text="4 x $50", col=TEAL, x=600, y=640, at=2, scale=0.9, sub="= $200")],
         texts=[dict(text="DESIGNED FOR YES", size=110, col=CORAL, y=150, at=0, glow=12), dict(text="1 SECOND PAUSE", size=90, col=GREEN, x=600, y=820, at=4, glow=10)], shake=[1])),
 ("math_intro", [
   ("Now let's leave the fantasy and do the real math. Because this is where it gets crazy.", None),
   ("Forget the magic dollar. What if you simply moved one dollar a day, every day, into an index fund?", None),
   ("An S and P five hundred index fund owns a small slice of about five hundred of the biggest companies in America.", None),
   ("No stock picking. No genius required. You just keep buying, month after month.", None),
   ("And we're going to use real prices, starting in January twenty ten.", None),
 ], dict(type="stage", loc="void_teal", actors=[you(1560, {0: "neutral", 1: "smug"}, size=300)],
         texts=[dict(text="REAL MATH", size=150, col=TEAL, y=200, glow=16), dict(text="$1 A DAY", size=120, col=GREEN, x=700, y=420, at=1, glow=12)],
         props=[dict(kind="icon", name="chart", x=700, y=650, at=2, scale=1.1), dict(kind="calendar", top="2010", big="JAN", x=1100, y=640, at=4, scale=0.9)])),
 ("snowball", [
   ("Here's why investing changes everything. It's called compounding.", None),
   ("Your dollar earns a little. Then that little bit starts earning too.", None),
   ("It's like a snowball rolling down a hill. Small and slow at the top. Huge at the bottom.", None),
   ("The hill is time. And the longer the hill, the bigger the snowball.", None),
 ], dict(type="stage", loc="void_teal", actors=[you(1560, {0: "neutral", 2: "shock"}, size=280)],
         props=[dict(kind="coin", x=520, y=640, at=0, scale=0.6), dict(kind="coin", x=760, y=600, at=1, scale=0.9), dict(kind="coin", x=1050, y=540, at=2, scale=1.4)],
         texts=[dict(text="COMPOUNDING", size=140, col=TEAL, y=200, glow=16), dict(text="TIME = THE HILL", size=90, col=AMBER, y=860, at=3, glow=10)])),
 ("chart1", [
   ("Here's one dollar a day. About thirty dollars a month. Less than most phone plans.", None),
   ("The first years look like nothing. A few hundred dollars. Boring.", None),
   ("Then the crashes come. Twenty twenty. Twenty twenty two. Your account drops, and you keep buying anyway.", None),
   ("By September twenty twenty six, you've put in six thousand one hundred and fourteen dollars.", None),
   ("And it's worth about nineteen thousand eight hundred.", None),
   ("From one dollar a day.", None),
 ], dict(type="chart", reveal=(0, 3), series=[dict(values=[v / 5 for v in VAL], col=TEAL, fill=True), dict(values=[v / 5 for v in INV], col=AMBER, width=6)],
         xlabels=YEARS, side=[dict(label="PUT IN", values=[v / 5 for v in INV], col=AMBER), dict(label="WORTH", values=[v / 5 for v in VAL], col=TEAL)],
         footnote="S&P 500 monthly avg. price (R. Shiller). $30.42 on the 1st of each month, Jan 2010 - Sep 2026. Price only, no dividends. Not financial advice.",
         texts=[dict(text="$1 = $3.24", size=110, col=GREEN, x=760, y=150, at=5, glow=14)], actors=[dict(who="you", x=1650, y=1070, size=150, emo={0: "neutral", 4: "shock"})])),
 ("scale", [
   ("Now imagine you're an average person who says no five times a day.", None),
   ("Five dollars a day becomes thirty thousand five hundred and sixty nine dollars put in.", None),
   ("And it grows to about ninety nine thousand dollars.", None),
   ("Ten no's a day? Almost two hundred thousand.", None),
   ("Not from a lottery ticket. Not from a crypto tip. From the word no.", None),
 ], dict(type="bars", groups=[dict(label="1 NO / DAY", vals=[(VAL[-1] / 5, GREEN)], at=0), dict(label="5 NO / DAY", vals=[(VAL[-1], TEAL)], at=1), dict(label="10 NO / DAY", vals=[(VAL[-1] * 2, AMBER)], at=3)],
         texts=[dict(text="FROM THE WORD NO", size=90, col=CREAM, y=140, at=4, glow=8)], flash={3: AMBER}, shake=[3])),
 ("late", [
   ("But what if you only discover your power later? Say, in January twenty sixteen?", None),
   ("Five dollars a day from twenty sixteen means about nineteen thousand six hundred put in.", None),
   ("And it's worth roughly forty three thousand today.", None),
   ("Less than the early starter, because the hill was shorter. But still more than double.", None),
   ("The best time to start was years ago. The second best time is your next no.", None),
 ], dict(type="bars", groups=[dict(label="START 2010", vals=[(INV[-1], AMBER), (VAL[-1], TEAL)], at=0), dict(label="START 2016", vals=[(19619, AMBER), (43047, TEAL)], at=1)],
         legend=[("put in", AMBER), ("worth", TEAL)], texts=[dict(text="SECOND BEST TIME = NOW", size=80, col=GREEN, y=140, at=4, glow=10)])),
 ("big_no", [
   ("But here's the part nobody tells you.", None),
   ("The small no's are nice. The big no's change your life.", None),
   ("Saying no to one new phone every two years. No to a car that's nicer than you need. No to a bigger apartment just because your friend got one.", None),
   ("One big no can be worth a thousand small ones.", None),
   ("If you said no to just one hundred dollars of stuff every month since twenty ten, you'd have put in twenty thousand one hundred dollars.", None),
   ("And it would be worth about sixty five thousand two hundred.", None),
 ], dict(type="stage", loc="dealer", actors=[you(560, {0: "neutral", 1: "smug", 5: "shock"}), dict(who="seller", x=1500, y=1010, size=320, emo={0: "happy", 2: "worried"}, flip=True)],
         props=[dict(kind="icon", name="iphone", x=900, y=380, at=2, until=3, scale=0.7), dict(kind="icon", name="car", x=1100, y=420, at=2, until=3, scale=0.9), dict(kind="icon", name="house", x=1300, y=380, at=2, until=3, scale=0.7)],
         counters=[dict(label="$100/MONTH SINCE 2010", **{"from": 20100, "to": 65209}, at=5, dur=2.0, x=1000, y=380, col=TEAL, size=150)],
         texts=[dict(text="1 BIG NO = 1,000 SMALL NO'S", size=86, col=AMBER, y=170, at=3, glow=10)], flash={5: TEAL})),
 ("hours", [
   ("And here's another way to see it.", None),
   ("In the US, the average worker earns about thirty eight dollars an hour.", None),
   ("So those two hundred and twenty dollar sneakers? That's almost six hours of your life.", None),
   ("When you say no, you're not just keeping money. You're keeping hours.", None),
 ], dict(type="stage", loc="office", actors=[you(560, {0: "neutral", 2: "shock", 3: "smug"})],
         props=[dict(kind="tag", text="$38 / HOUR", col=TEAL, x=1300, y=360, at=1, scale=1.0, sub="US AVERAGE, OCT 2026"), dict(kind="tag", text="$220 = 5.8 HOURS", col=CORAL, x=1300, y=600, at=2, scale=1.0)],
         texts=[dict(text="NO = TIME BACK", size=110, col=AMBER, y=180, at=3, glow=12)])),
 ("rule24", [
   ("So how do you get the power without the magic? Three simple tricks.", None),
   ("One. The twenty four hour rule. Anything that isn't food or bills waits one day in your cart. Most of it, you'll forget.", None),
   ("Two. Make the no automatic. Set a small transfer to savings on payday, before you can spend it.", None),
   ("Three. Every month, cancel one thing you pay for but don't use. That's a no that keeps paying, every single month.", None),
   ("None of this feels heroic. That's exactly why it works.", None),
 ], dict(type="list", cards=True, title="THE POWER, WITHOUT MAGIC", items=[dict(text="24-HOUR RULE", sub="the cart waits a day", at=1), dict(text="AUTO-SAVE", sub="on payday, first", at=2), dict(text="CANCEL ONE", sub="every month", at=3)],
         texts=[dict(text="BORING = WORKS", size=80, col=GREEN, y=880, at=4, glow=10)])),
 ("honest", [
   ("Now, the honest part. This is not financial advice.", None),
   ("These are real S and P five hundred prices, but the past doesn't promise the future.", None),
   ("Markets can drop and stay down for years.", None),
   ("Build an emergency fund first, pay off expensive debt, and only invest money you won't need soon.", None),
 ], dict(type="list", title="NOT FINANCIAL ADVICE", tcol=CORAL, items=[dict(text="The past doesn't promise the future", at=1), dict(text="Markets can stay down for years", at=2), dict(text="Emergency fund first", at=3), dict(text="Kill expensive debt first", at=3.4), dict(text="Only money you won't need soon", at=3.8)],
         actors=[you(1680, "neutral", size=240, y=1040)])),
 ("outro", [
   ("So, no magic dollar is coming. But the pause is real, and you already have it.", None),
   ("Next time your thumb hovers over buy now, wait one second and ask: is this a thing, or a person?", None),
   ("What's the one thing you'd say no to this week? Tell me in the comments.", None),
   ("And I'll see you in the other timeline.", None),
 ], dict(type="end", q1="WHAT WOULD YOU", q2="SAY NO TO?", comment="Your one no this week?", comment_at=2, emo={0: "smug", 2: "happy"})),
]

META = dict(
    file="EP01_1_Dollar_Every_No.mp4",
    title="What If You Got $1 Every Time You Said No?",
    description="""Every time you say no, a dollar appears. Easy money... until one no almost costs you everything.
Then we do the real math: what $1, $5 and $10 a day would be worth today if you had invested them since 2010, using real S&P 500 prices.

Method: money invested on the 1st of each month (Jan 2010 - Sep 2026) at the S&P 500 monthly average price (Robert Shiller data). Price only, dividends not included. US average hourly earnings: $38.00 (Oct 2026, BLS via FRED).
This video is for education and entertainment only. It is not financial advice. Past performance does not guarantee future results.

#whatif #personalfinance #investing""",
    tags=["what if", "what if you got 1 dollar every time", "saying no", "personal finance", "investing for beginners", "compound interest", "s&p 500", "index fund", "saving money", "money habits", "financial education", "the other timeline", "animated story"],
    comment="What's ONE thing you'd say no to this week? Mine: the third streaming subscription. 👇",
    chapters={"hook": "One word = $1", "rule": "The rules", "cafe": "The coffee shop test", "max": "Max and the $220 sneakers", "day1": "Day one", "week": "One week later",
              "problem": "The no that hurt", "lesson": "The real power", "math_intro": "The real math", "chart1": "$1 a day since 2010", "scale": "$5 and $10 a day",
              "big_no": "The big no's", "hours": "Money = hours", "rule24": "3 tricks", "max_hack": "Max tries to cheat", "month": "One month later", "why_hard": "Why no is hard", "snowball": "The snowball", "late": "Starting late", "honest": "The honest part", "outro": "Your one no"},
)

THUMBS = {
    "A": dict(loc="cafe", quote="I just said no..", hl=["no.."], actors=[dict(who="you", x=520, size=560, emo="smug"), dict(who="barista", x=1450, size=520, emo="shock", flip=True)],
              props=[dict(kind="bill", amount="1", x=960, y=520, scale=1.3, rot=-12)], line=(620, 560, 1350, 600), lcol=GREEN, big=dict(text="+$1", x=960, y=330, col=GREEN, size=200)),
    "B": dict(loc="street", quote="every NO = +$1", hl=["NO", "+$1"], actors=[dict(who="you", x=600, size=600, emo="money"), dict(who="max", x=1450, size=520, emo="shock", flip=True)],
              big=dict(text="$198,344", x=1340, y=870, col=GREEN, size=170, rot=-4), pcol=GREEN),
}

SHORT = dict(segs=[("day1", [3, 4, 5]), ("scale", [0, 1, 2, 3])], title=["$1 EVERY TIME", "YOU SAY NO"], hook=dict(text="+$1", col=GREEN, dur=1.6),
             yt_title="What If Every NO Paid You $1? #shorts",
             yt_desc="One day of saying no saved $260. Then the real math with S&P 500 prices since 2010.\nFull video on the channel. Not financial advice. #whatif #personalfinance #money")
