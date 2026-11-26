"""EP02 — What If You Started Investing at 18 Instead of 30?  (two timelines)
S&P 500 monthly avg price (Shiller), $200 on the 1st of each month, price only.
A: Jan 1998 - Sep 2026: put in $69,000 -> $321,043. 2000-08: $6,400 -> $7,638; 2002-10: $11,600 -> $8,323;
2007-10: $23,600 -> $30,777; 2009-03: $27,000 -> $17,435; 2009-12: $28,800 -> $27,599.
A-stopper (Jan 1998 - Dec 2009 then hold): $28,800 -> $190,625.  B: Jan 2010 - Sep 2026: $40,200 -> $130,418.
B needs ~$492/month to reach A's $321k."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
from kit import *  # noqa
import data

SP = data.sp500()
KA, IA, VA = data.dca(SP, "1998-01", "2026-09", 200)
# B aligned on A's month axis (zero before 2010)
KB, IB, VB = data.dca(SP, "2010-01", "2026-09", 200)
off = KA.index("2010-01")
IB2 = [0.0] * off + IB; VB2 = [0.0] * off + VB
YEARS = [(i, k[:4]) for i, k in enumerate(KA) if k.endswith("-01") and int(k[:4]) % 4 == 2]
i00, i02, i09 = KA.index("2000-08"), KA.index("2002-10"), KA.index("2009-03")

SPEED = 1.18
MUSIC_SEED = 2
END_LINE = "WHEN DID YOU START?"

def you(x=960, emo="neutral", size=330, **k):
    return dict(who="you", x=x, y=k.pop("y", 1010), size=size, emo=emo, **k)

BEATS = [
 ("hook", [
   ("Two versions of you. Same job. Same salary. Same two hundred dollars a month.", None),
   ("One starts investing at eighteen. The other waits until thirty.", None),
   ("Twelve years. That's the only difference.", None),
   ("By the end of this video, one of them has almost two hundred thousand dollars more than the other.", None),
   ("And the twist is, for the first twelve years, the early starter looks like a complete idiot.", None),
 ], dict(type="split", left=dict(title="START AT 18", col=TEAL, who="you", emo={0: "happy", 4: "worried"}),
         right=dict(title="START AT 30", col=CORAL, who="you", emo={0: "smug", 4: "happy"}, at=1),
         texts=[dict(text="12 YEARS", size=170, col=AMBER, y=470, at=2, glow=18), dict(text="+$190,000?", size=130, col=GREEN, y=640, at=3, glow=14)],
         flash={2: AMBER}, shake=[3])),
 ("setup", [
   ("It's January nineteen ninety eight. You're eighteen.", None),
   ("You have a part time job, a terrible haircut, and a grandma with opinions.", None),
   ("Sweetheart, put a little away every month. Don't touch it. Just let it grow.", None),
   ("Two hundred dollars a month. That's a lot of pizza at eighteen.", None),
   ("And here the timeline splits.", None),
 ], dict(type="stage", loc="living", actors=[you(600, {0: "neutral", 1: "smug", 3: "worried"}), dict(who="grandma", x=1350, y=1010, size=320, emo="happy", flip=True, talk=[2])],
         props=[dict(kind="calendar", top="1998", big="JAN", x=960, y=330, at=0, scale=0.9)],
         bubbles=[dict(text="Put a little away every month. Don't touch it.", x=1350, y=500, at=2, until=3)],
         texts=[dict(text="$200 / MONTH", size=110, col=AMBER, y=200, at=3, glow=12)], flash={4: AMBER}, shake=[4])),
 ("rules", [
   ("In timeline A, you listen to grandma. Two hundred dollars a month into an S and P five hundred index fund, starting right now, at eighteen.", None),
   ("In timeline B, you think, I'm young. I'll start later. And you do. At thirty, in January twenty ten.", None),
   ("Same fund. Same two hundred a month. Both keep going until September twenty twenty six.", None),
   ("We'll use real historical prices. Every crash included.", None),
 ], dict(type="split", left=dict(title="TIMELINE A", sub="starts Jan 1998 (age 18)", col=TEAL, who="you", emo="happy", props=[dict(kind="calendar", top="1998", big="18", x=620, y=600, scale=0.8, col=TEAL)]),
         right=dict(title="TIMELINE B", sub="starts Jan 2010 (age 30)", col=CORAL, who="you", emo="smug", at=1, props=[dict(kind="calendar", top="2010", big="30", x=1580, y=600, scale=0.8)]),
         texts=[dict(text="$200/MONTH · S&P 500 · UNTIL SEP 2026", size=56, col=CREAM, y=860, at=2)])),
 ("dotcom_up", [
   ("Timeline A. The first two years feel amazing.", None),
   ("It's the late nineties. Everyone is talking about the internet. Your neighbour quit his job to trade stocks.", None),
   ("By August two thousand, you've put in six thousand four hundred dollars, and it's worth over seven thousand six hundred.", None),
   ("You feel like a genius. You tell everyone at parties.", None),
 ], dict(type="chart", reveal=(0, 2), p0=0.0, vmax=12000, series=[dict(values=VA[:i00 + 1], col=TEAL, fill=True), dict(values=IA[:i00 + 1], col=AMBER, width=6)],
         xlabels=[(0, "1998"), (12, "1999"), (24, "2000")], side=[dict(label="PUT IN", values=IA[:i00 + 1], col=AMBER), dict(label="WORTH", values=VA[:i00 + 1], col=TEAL)],
         actors=[dict(who="you", x=1650, y=1070, size=150, emo={0: "happy", 3: "smug"})], texts=[dict(text="GENIUS?", size=100, col=GREEN, x=700, y=150, at=3, glow=12)],
         footnote="S&P 500 monthly avg. price (R. Shiller), $200 on the 1st of each month. Price only. Not financial advice.")),
 ("dotcom_crash", [
   ("Then the internet bubble pops.", None),
   ("By October two thousand two, you've put in eleven thousand six hundred dollars.", None),
   ("And it's worth eight thousand three hundred.", None),
   ("You've lost money. Real money. Pizza money.", None),
   ("Every month, you're buying more of something that keeps going down.", None),
 ], dict(type="chart", reveal=(0, 2), p0=i00 / i02, vmax=12000, series=[dict(values=VA[:i02 + 1], col=TEAL, fill=True), dict(values=IA[:i02 + 1], col=AMBER, width=6)],
         xlabels=[(0, "1998"), (24, "2000"), (48, "2002")], side=[dict(label="PUT IN", values=IA[:i02 + 1], col=AMBER), dict(label="WORTH", values=VA[:i02 + 1], col=TEAL)],
         notes=[dict(i=i02, text="-$3,277", col=CORAL, dy=-120, dx=-120, size=60)],
         actors=[dict(who="you", x=1650, y=1070, size=150, emo={0: "shock", 3: "sad"})], flash={0: CORAL}, shake=[0])),
 ("b_life", [
   ("Meanwhile, in timeline B, you're having the time of your life.", None),
   ("No investing. Just road trips with Max. Concert tickets. A used car with a sound system louder than its engine.", None),
   ("Max raises a glass. To never checking a stock price, ever.", None),
   ("Honestly? Timeline B looks smarter right now.", None),
 ], dict(type="stage", loc="street", actors=[you(620, {0: "happy", 3: "smug"}), dict(who="max", x=1300, y=1010, size=320, emo="happy", flip=True, talk=[2])],
         props=[dict(kind="icon", name="car", x=960, y=640, at=1, scale=1.0), dict(kind="tag", text="CONCERT $120", col=PINK, x=960, y=300, at=1, scale=0.7)],
         bubbles=[dict(text="To never checking a stock price!", x=1300, y=520, at=2, until=3)],
         texts=[dict(text="TIMELINE B: WINNING?", size=96, col=CORAL, y=160, at=3, glow=10)])),
 ("crisis", [
   ("Back in timeline A, things get worse. Two thousand eight. The global financial crisis.", None),
   ("Banks collapse on the news. People lose their homes.", None),
   ("By March two thousand nine, you've put in twenty seven thousand dollars over eleven years.", None),
   ("And it's worth seventeen thousand four hundred.", None),
   ("Eleven years of discipline, and you're almost ten thousand dollars down.", None),
   ("Every voice in your head says sell. Stop. You were wrong.", None),
 ], dict(type="chart", reveal=(0, 3), p0=0.45, vmax=36000, series=[dict(values=VA[:i09 + 1], col=TEAL, fill=True), dict(values=IA[:i09 + 1], col=AMBER, width=6)],
         xlabels=[(0, "1998"), (48, "2002"), (96, "2006"), (132, "2009")], side=[dict(label="PUT IN", values=IA[:i09 + 1], col=AMBER), dict(label="WORTH", values=VA[:i09 + 1], col=TEAL)],
         notes=[dict(i=i09, text="-$9,565", col=CORAL, dy=-130, dx=-160, size=64)],
         actors=[dict(who="you", x=1650, y=1070, size=150, emo={0: "worried", 4: "sad", 5: "shock"})], flash={3: CORAL}, shake=[3])),
 ("panic", [
   ("And here, the timeline could split one more time.", None),
   ("Imagine a version of you who can't take it anymore. In March two thousand nine, at the very bottom, you sell everything.", None),
   ("Seventeen thousand four hundred dollars. You put it in a savings account, swear you'll never touch stocks again, and you keep that promise.", None),
   ("That version of you locks in the loss forever. Hold on to that number. Seventeen thousand four hundred. We'll come back to it.", None),
   ("But in our timeline A, you do the hardest thing in investing. Absolutely nothing. You keep buying.", None),
 ], dict(type="stage", loc="bank", actors=[you(560, {0: "worried", 1: "shock", 3: "sad", 4: "neutral"}), dict(who="banker", x=1380, y=1010, size=320, emo={0: "neutral", 1: "worried"}, flip=True)],
         props=[dict(kind="phone", text="SELL ALL", sub="MARCH 2009", col=CORAL, x=960, y=560, at=1, until=2.9, scale=0.9), dict(kind="tag", text="$17,435", col=CORAL, x=960, y=420, at=2, until=3.9, scale=1.2, sub="locked in forever")],
         texts=[dict(text="DO NOTHING", size=130, col=TEAL, y=180, at=4, glow=14)], flash={1: CORAL}, shake=[1])),
 ("lost_decade", [
   ("Then you turn thirty. December two thousand nine.", None),
   ("Twelve years of investing. Twenty eight thousand eight hundred dollars put in.", None),
   ("Your account says twenty seven thousand six hundred.", None),
   ("Less than you put in. After twelve years.", None),
   ("Timeline B has zero dollars invested, but a lot of good memories. Max is laughing at you. Openly.", None),
   ("This is the exact moment most people quit forever.", None),
 ], dict(type="split", left=dict(title="TIMELINE A · AGE 30", col=TEAL, who="you", emo={0: "neutral", 3: "sad"}, value=dict(**{"from": 0, "to": 27599}, at=1, to_at=2.5, label="worth (put in $28,800)")),
         right=dict(title="TIMELINE B · AGE 30", col=CORAL, who="max", emo="happy", at=4, value=dict(**{"from": 0, "to": 0}, at=4, dur=0.5, label="invested so far")),
         texts=[dict(text="MOST PEOPLE QUIT HERE", size=90, col=CORAL, y=860, at=5, glow=12)], flash={3: CORAL})),
 ("b_starts", [
   ("And now timeline B wakes up. You're thirty. You've got a better job. You read one article about compound interest.", None),
   ("January twenty ten. You start the same two hundred dollars a month.", None),
   ("And here's the thing. Your timing is incredible. You start right after the crash, when prices are low.", None),
   ("Timeline A has to keep going. Timeline B gets a fresh start at a discount.", None),
 ], dict(type="stage", loc="office", actors=[you(620, {0: "neutral", 2: "smug"}), dict(who="banker", x=1350, y=1010, size=320, emo="happy", flip=True)],
         props=[dict(kind="calendar", top="2010", big="JAN", x=980, y=340, at=1, scale=0.9), dict(kind="tag", text="PRICES ON SALE", col=GREEN, x=980, y=600, at=2, scale=0.9)],
         texts=[dict(text="TIMELINE B STARTS", size=100, col=CORAL, y=160, glow=10)])),
 ("race", [
   ("So now both timelines invest the same two hundred dollars every month.", None),
   ("Watch the two lines.", None),
   ("Timeline A has twelve extra years of shares. And now, finally, those twelve years start to pay.", None),
   ("Every rise in the market lifts a much bigger pile.", None),
   ("Twenty twenty. Twenty twenty two. Both drop. Both keep buying. And the gap keeps getting wider.", None),
 ], dict(type="chart", reveal=(0, 4), p0=0.42, series=[dict(values=VA, col=TEAL, fill=True), dict(values=VB2, col=CORAL, width=8)],
         xlabels=YEARS, side=[dict(label="TIMELINE A", values=VA, col=TEAL), dict(label="TIMELINE B", values=VB2, col=CORAL)],
         footnote="S&P 500 monthly avg. price (R. Shiller), $200 on the 1st of each month, to Sep 2026. Price only. Not financial advice.",
         actors=[dict(who="you", x=1650, y=1070, size=150, emo={0: "neutral", 2: "shock"})])),
 ("result", [
   ("September twenty twenty six. Final numbers.", None),
   ("Timeline B, starting at thirty: forty thousand two hundred dollars put in. Worth about one hundred and thirty thousand.", None),
   ("Not bad at all.", None),
   ("Timeline A, starting at eighteen: sixty nine thousand put in.", None),
   ("Worth about three hundred and twenty one thousand dollars.", None),
   ("A difference of about one hundred and ninety thousand dollars. From starting twelve years earlier.", None),
 ], dict(type="bars", groups=[dict(label="START AT 30", vals=[(IB[-1], AMBER), (VB[-1], CORAL)], at=1), dict(label="START AT 18", vals=[(IA[-1], AMBER), (VA[-1], TEAL)], at=3)],
         legend=[("put in", AMBER), ("worth", TEAL)], texts=[dict(text="+$190,625", size=130, col=GREEN, y=170, at=5, glow=16)], flash={4: TEAL}, shake=[4])),
 ("max_2026", [
   ("Max hears these numbers at a barbecue in twenty twenty six.", None),
   ("Wait. You're telling me the boring one is the rich one?", None),
   ("Yes, Max. And remember the version who sold everything in two thousand nine? Still seventeen thousand four hundred dollars. Plus a little bank interest.", None),
   ("Timeline A, who did nothing, has over eighteen times more.", None),
   ("Max quietly opens an investing app under the table.", None),
 ], dict(type="stage", loc="street", actors=[you(560, {0: "smug", 3: "happy"}), dict(who="max", x=1380, y=1010, size=320, emo={0: "neutral", 1: "shock", 4: "worried"}, flip=True, talk=[1])],
         bubbles=[dict(text="The BORING one is the rich one?!", x=1380, y=500, at=1, until=2)],
         props=[dict(kind="tag", text="SOLD 2009: $17,435", col=CORAL, x=960, y=330, at=2, scale=0.8), dict(kind="tag", text="HELD: $321,043", col=TEAL, x=960, y=500, at=3, scale=0.8), dict(kind="phone", text="OPEN", sub="INVEST APP", col=GREEN, x=1100, y=640, at=4, scale=0.7)],
         texts=[dict(text="18x MORE", size=120, col=GREEN, y=170, at=3, glow=14)], flash={3: GREEN})),
 ("twist", [
   ("But here's the craziest part.", None),
   ("Imagine a third timeline. You start at eighteen, and at thirty, you stop. Completely. You never add another dollar.", None),
   ("You put in twenty eight thousand eight hundred dollars. Less than timeline B.", None),
   ("And by twenty twenty six, it's worth about one hundred and ninety thousand.", None),
   ("The person who stopped at thirty beats the person who started at thirty. By sixty thousand dollars.", None),
   ("And look closely at that number. It's exactly the gap between timelines A and B. That's not a coincidence. That gap is simply what those first twelve years grew into.", None),
 ], dict(type="bars", groups=[dict(label="START AT 30", sub="kept going", vals=[(IB[-1], AMBER), (VB[-1], CORAL)], at=0), dict(label="18 TO 30 ONLY", sub="then stopped", vals=[(28800, AMBER), (190625, PURPLE)], at=1)],
         legend=[("put in", AMBER), ("worth", PURPLE)], texts=[dict(text="STOPPED AT 30 > STARTED AT 30", size=74, col=PURPLE, y=170, at=4, glow=12)], flash={3: PURPLE}, shake=[3])),
 ("catch_up", [
   ("So what would timeline B need to catch up?", None),
   ("Starting at thirty, you'd need to invest about four hundred and ninety two dollars every month, not two hundred, to end up with the same three hundred and twenty one thousand.", None),
   ("Almost two and a half times more money, every month, for sixteen years.", None),
   ("That's the price of waiting.", None),
 ], dict(type="stage", loc="void_red", actors=[you(1560, {0: "neutral", 2: "shock"}, size=300)],
         props=[dict(kind="tag", text="$200 / MONTH", col=TEAL, x=650, y=360, at=0, scale=1.1, sub="start at 18"), dict(kind="tag", text="$492 / MONTH", col=CORAL, x=650, y=600, at=1, scale=1.1, sub="start at 30, same result")],
         texts=[dict(text="THE PRICE OF WAITING", size=110, col=CORAL, y=170, at=3, glow=14)], flash={3: CORAL})),
 ("why", [
   ("Why does this happen? Because compounding loves time more than it loves money.", None),
   ("The money from your first years has the longest hill to roll down. It grows, and then its growth grows.", None),
   ("Those first twelve years looked like a total waste. Two crashes. No profit. But they were planting seeds.", None),
   ("The hard part was never the math. It was staying calm while it looked like you were losing.", None),
 ], dict(type="stage", loc="void_teal", actors=[you(1560, {0: "neutral", 3: "smug"}, size=280)],
         props=[dict(kind="coin", x=480, y=700, at=1, scale=0.5), dict(kind="coin", x=700, y=640, at=1.5, scale=0.8), dict(kind="coin", x=1000, y=560, at=2, scale=1.3)],
         texts=[dict(text="TIME > MONEY", size=150, col=TEAL, y=200, glow=16), dict(text="THE HARD PART = STAYING CALM", size=76, col=AMBER, y=860, at=3, glow=10)])),
 ("not_18", [
   ("Now, maybe you're not eighteen. Maybe you're thirty, or forty, or fifty. So is this video useless?", None),
   ("No. Because there's always a version of you who is ten years older and wishes you'd started today.", None),
   ("Timeline B still turned forty thousand dollars into about one hundred and thirty thousand. That's real money.", None),
   ("And this works far beyond America. In Europe and most of the world, you can buy broad, low cost index funds that track thousands of companies.", None),
   ("Even small amounts count. Twenty five dollars a month that actually happens beats five hundred dollars a month that you keep postponing.", None),
   ("The best day to start was years ago. The second best is today.", None),
 ], dict(type="stage", loc="kitchen", actors=[you(640, {0: "worried", 1: "neutral", 4: "happy"}), dict(who="grandma", x=1380, y=1010, size=300, emo="happy", flip=True, at=4)],
         texts=[dict(text="START TODAY", size=140, col=GREEN, y=190, at=5, glow=16), dict(text="$25 THAT HAPPENS > $500 SOMEDAY", size=70, col=AMBER, y=330, at=4, until=4.9, glow=8)],
         props=[dict(kind="phone", text="$130,418", sub="TIMELINE B", col=CORAL, x=1050, y=560, at=2, until=3.9, scale=0.9), dict(kind="icon", name="chart", x=1050, y=560, at=3, until=3.9, scale=0.8)])),
 ("tips", [
   ("If you want to start, three boring rules.", None),
   ("One. Automate it. The money leaves your account the day you get paid, so you never have to decide.", None),
   ("Two. Keep it cheap and broad. A low fee index fund beats picking the next hot stock for most people.", None),
   ("Three. When the market crashes, don't look away from the plan. Look away from the news.", None),
   ("And a bonus rule. Every time your income goes up, raise the monthly amount a little, before your lifestyle eats the raise.", None),
   ("That's it. No secret stock. No guru. Just time, and a plan you don't break.", None),
 ], dict(type="list", cards=True, title="3 BORING RULES", items=[dict(text="AUTOMATE", sub="on payday", at=1), dict(text="CHEAP + BROAD", sub="low-fee index", at=2), dict(text="IGNORE CRASHES", sub="keep the plan", at=3)])),
 ("honest", [
   ("And the honest part. This is not financial advice.", None),
   ("These are real past prices, and the past doesn't promise the future. Some decades are much worse than others.", None),
   ("Have an emergency fund, deal with expensive debt first, and only invest money you won't need for years.", None),
 ], dict(type="list", title="NOT FINANCIAL ADVICE", tcol=CORAL, items=[dict(text="The past doesn't promise the future", at=1), dict(text="Some decades are bad", at=1.5), dict(text="Emergency fund first", at=2), dict(text="Expensive debt first", at=2.3), dict(text="Long-term money only", at=2.6)],
         actors=[you(1680, "neutral", size=240, y=1040)])),
 ("outro", [
   ("Twelve years. Two crashes. One grandma who was right.", None),
   ("So tell me in the comments. How old were you when you started investing, or are you starting today?", None),
   ("And I'll see you in the other timeline.", None),
 ], dict(type="end", q1="HOW OLD WERE YOU", q2="WHEN YOU STARTED?", comment="How old were you?", comment_at=1, emo={0: "smug", 1: "happy"})),
]

META = dict(
    file="EP02_Invest_at_18_vs_30.mp4",
    title="What If You Started Investing at 18 Instead of 30?",
    description="""Two versions of you invest the same $200 a month. One starts at 18 (1998), one at 30 (2010). For 12 years the early starter looks like a fool... then the gap explodes. Real S&P 500 prices, every crash included.

Method: $200 invested on the 1st of each month at the S&P 500 monthly average price (Robert Shiller data), until Sep 2026. Price only, dividends not included, no fees or taxes.
This video is for education and entertainment only. It is not financial advice. Past performance does not guarantee future results.

#whatif #investing #personalfinance""",
    tags=["what if", "investing at 18", "start investing early", "compound interest", "s&p 500", "index fund", "dollar cost averaging", "personal finance", "financial education", "dot com crash", "2008 crisis", "the other timeline", "animated story"],
    comment="How old were you when you started investing? (Or is today day one?) 👇",
    chapters={"hook": "Two versions of you", "setup": "1998: grandma's advice", "rules": "The rules", "dotcom_up": "The internet boom", "dotcom_crash": "The dot-com crash", "b_life": "Meanwhile in timeline B",
              "crisis": "2008", "panic": "The panic seller", "max_2026": "Max finds out", "lost_decade": "12 years, no profit", "b_starts": "Timeline B starts", "race": "The race", "result": "Final numbers", "twist": "The stopper twist",
              "catch_up": "The price of waiting", "why": "Why it happens", "not_18": "Not 18 anymore?", "tips": "3 boring rules", "honest": "The honest part", "outro": "When did you start?"},
)

THUMBS = {
    "A": dict(loc="street", quote="i started at 18..", hl=["18.."], actors=[dict(who="you", x=520, size=560, emo="smug"), dict(who="max", x=1450, size=540, emo="shock", flip=True)],
              big=dict(text="$321,043", x=1000, y=420, col=GREEN, size=180, rot=-4), line=(620, 600, 1380, 640), lcol=GREEN),
    "B": dict(loc="void_red", quote="18 vs 30", hl=["18", "30"], actors=[dict(who="you", x=480, size=560, emo="money"), dict(who="you", x=1440, size=560, emo="sad", flip=True)],
              big=dict(text="+$190K", x=960, y=430, col=AMBER, size=220)),
}

SHORT = dict(segs=[("lost_decade", [1, 2, 3, 5]), ("result", [3, 4, 5])], title=["12 YEARS, NO PROFIT...", "THEN THIS"], hook=dict(text="-$1,201", col=CORAL, dur=1.8),
             yt_title="He Invested for 12 Years and Had LESS Money #shorts",
             yt_desc="Start at 18 vs start at 30, same $200 a month, real S&P 500 prices. Full video on the channel. Not financial advice. #investing #whatif #money")
