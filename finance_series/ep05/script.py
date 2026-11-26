"""EP05 — What If You Bought Bitcoin Instead of an iPhone in 2015?  (two timelines, the one crypto episode)
iPhone 6s launch price $649 (16 GB, Sep 25 2015). Bitcoin: Coinbase BTC-USD daily close (FRED CBBTCUSD).
Sep 25 2015: $235.89 -> 2.7513 BTC for $649.
Value: Dec 17 2017 $53,317; Dec 15 2018 $8,757 (-84% from peak); Nov 9 2021 $184,248; Nov 21 2022 $43,349 (-76%);
Oct 5 2025 peak $343,140 (BTC $124,720); Nov 25 2026 $166,849 (BTC $60,644, -51% from peak).
S&P 500 comparison: $649 in Sep 2015 -> $2,560 in Sep 2026 (price only, Shiller)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
from kit import *  # noqa
import data

BD = data.fred("CBBTCUSD", monthly=False)
P0 = BD["2015-09-25"]; COINS = 649 / P0
MONTHS = data.fred("CBBTCUSD")  # first observation of each month
MK = [k for k in sorted(MONTHS) if "2015-10" <= k <= "2026-11"]
VALS = [649.0] + [COINS * MONTHS[k] for k in MK[:-1]] + [COINS * BD["2026-11-25"]]
KEYS = ["2015-09"] + MK
YEARS = [(i, k[:4]) for i, k in enumerate(KEYS) if k.endswith("-01") and int(k[:4]) % 2 == 0]
def at(k): return KEYS.index(k)
i17, i18, i21, i22, i25 = at("2017-12"), at("2018-12"), at("2021-11"), at("2022-11"), at("2025-10")
V = lambda d: COINS * BD[d]
# put the exact key-date closes on the chart so the line hits the numbers that are said
for idx, d in ((i17, "2017-12-17"), (i18, "2018-12-15"), (i21, "2021-11-09"), (i22, "2022-11-21"), (i25, "2025-10-05")):
    VALS[idx] = V(d)

SPEED = 1.18
MUSIC_SEED = 5
END_LINE = "WOULD YOU HAVE HELD?"

def you(x=960, emo="neutral", size=330, **k):
    return dict(who="you", x=x, y=k.pop("y", 1010), size=size, emo=emo, **k)

BEATS = [
 ("hook", [
   ("September twenty fifteen. The new iPhone costs six hundred and forty nine dollars, and you've been saving for months.", None),
   ("What if, instead, you'd spent that money on a strange internet coin called Bitcoin?", None),
   ("Today, that phone would be a museum piece. And the coins would be worth over one hundred and sixty six thousand dollars.", None),
   ("Sounds like the easiest decision in history. But this story has a twist that almost nobody talks about.", None),
   ("To get that money, you would have had to survive three crashes, each one of them brutal.", None),
 ], dict(type="split", left=dict(title="BUY THE IPHONE", col=CORAL, who="you", emo={0: "happy", 2: "sad"}, props=[dict(kind="icon", name="iphone", x=620, y=640, scale=0.8)]),
         right=dict(title="BUY BITCOIN", col=AMBER, who="you", emo={0: "worried", 2: "money"}, at=1, props=[dict(kind="icon", name="btc", x=1580, y=640, scale=0.8)],
                    value=dict(**{"from": 649, "to": V("2026-11-25")}, at=2, dur=2.2, label="Nov 2026", vcol=GREEN)),
         texts=[dict(text="3 CRASHES", size=130, col=CORAL, y=860, at=4, glow=14)], flash={2: GREEN}, shake=[2])),
 ("store", [
   ("Let's go back. You're standing in line at the phone store. Max is next to you, holding his phone like a newborn.", None),
   ("Max: Bro, the camera on this thing. Life changing.", None),
   ("But you've been reading strange forums at three in the morning. Internet money. No banks. Only twenty one million coins will ever exist.", None),
   ("And here the timeline splits.", None),
 ], dict(type="stage", loc="store", actors=[you(560, {0: "neutral", 2: "worried", 3: "smug"}), dict(who="max", x=1380, y=1010, size=320, emo="love", flip=True, talk=[1])],
         props=[dict(kind="icon", name="iphone", x=1100, y=420, at=1, scale=0.7), dict(kind="tag", text="$649", col=CORAL, x=1100, y=640, at=0, scale=1.0), dict(kind="icon", name="btc", x=760, y=360, at=2, scale=0.6)],
         bubbles=[dict(text="The camera. Life changing.", x=1380, y=520, at=1, until=2)], flash={3: AMBER}, shake=[3])),
 ("what_is", [
   ("Quick explanation, in case you skipped those forums.", None),
   ("Bitcoin is digital money that isn't run by a bank or a government. Transactions are recorded on a public ledger that thousands of computers keep in sync.", None),
   ("Its rules say there will never be more than twenty one million coins. That scarcity is a big part of why people buy it.", None),
   ("Its price isn't set by anyone. It's simply whatever the next buyer is willing to pay. And that can change very, very fast.", None),
 ], dict(type="stage", loc="void", actors=[you(1500, {0: "neutral", 2: "smug", 3: "worried"})],
         props=[dict(kind="icon", name="btc", x=650, y=420, at=0, scale=1.1), dict(kind="tag", text="MAX 21,000,000", col=AMBER, x=650, y=700, at=2, scale=1.0), dict(kind="tag", text="PRICE = NEXT BUYER", col=CORAL, x=650, y=860, at=3, scale=0.8)],
         texts=[dict(text="WHAT IS BITCOIN?", size=120, col=AMBER, y=170, glow=14)])),
 ("buy", [
   ("In timeline A, you buy the phone. It's beautiful. You drop it on the first day. It survives. You love it.", None),
   ("In timeline B, you open an exchange account and buy six hundred and forty nine dollars of Bitcoin, at about two hundred and thirty six dollars per coin.", None),
   ("You now own two point seven five bitcoins. And you still have your old cracked phone.", None),
   ("Max thinks you've been scammed. Honestly, so does your bank.", None),
   ("Your bank even calls to double check the payment. Yes, you say. Yes, I really meant to buy internet money.", None),
 ], dict(type="split", left=dict(title="TIMELINE A", sub="iPhone 6s, $649", col=CORAL, who="you", emo="happy", props=[dict(kind="icon", name="iphone", x=620, y=600, scale=0.8)]),
         right=dict(title="TIMELINE B", sub="2.75 BTC at $236", col=AMBER, who="you", emo="worried", at=1, props=[dict(kind="icon", name="btc", x=1580, y=600, scale=0.8)]),
         texts=[dict(text="SCAMMED?", size=110, col=CORAL, x=1440, y=860, at=3, glow=12)])),
 ("boom17", [
   ("For two years, timeline B looks like a genius.", None),
   ("In December twenty seventeen, Bitcoin hits about nineteen thousand dollars. Your six hundred and forty nine dollars are now worth over fifty three thousand.", None),
   ("Taxi drivers are talking about crypto. Your aunt asks you how to buy some. Max is furious.", None),
   ("Timeline A's phone is already slowing down.", None),
 ], dict(type="chart", reveal=(0, 1), series=[dict(values=VALS[:i17 + 1], col=AMBER, width=9, fill=True)],
         xlabels=[(i, k) for i, k in YEARS if i <= i17], side=[dict(label="YOUR $649 OF BTC", values=VALS[:i17 + 1], col=AMBER)],
         footnote="Bitcoin price: Coinbase BTC-USD (FRED CBBTCUSD), first trading day of each month; key dates use daily closes.",
         texts=[dict(text=money(V("2017-12-17")), size=120, col=GREEN, x=760, y=170, at=1, glow=14)], actors=[dict(who="you", x=1650, y=1070, size=150, emo={0: "smug", 1: "money"})], flash={1: GREEN})),
 ("crash18", [
   ("Then, crash number one.", None),
   ("By December twenty eighteen, Bitcoin is around three thousand two hundred dollars. Down about eighty four percent from the top.", None),
   ("Your fifty three thousand dollars are now about eight thousand seven hundred.", None),
   ("You lost forty four thousand dollars of paper money in one year. People online are calling Bitcoin dead.", None),
   ("Every part of you wants to sell what's left and buy a very nice phone.", None),
 ], dict(type="chart", reveal=(0, 2), p0=i17 / i18, series=[dict(values=VALS[:i18 + 1], col=AMBER, width=9, fill=True)],
         xlabels=[(i, k) for i, k in YEARS if i <= i18], side=[dict(label="YOUR $649 OF BTC", values=VALS[:i18 + 1], col=AMBER)],
         notes=[dict(i=i18, text="-84%", col=CORAL, dy=-130, dx=-80, size=90)], actors=[dict(who="you", x=1650, y=1070, size=150, emo={0: "shock", 3: "sad"})], flash={0: CORAL}, shake=[0])),
 ("max_fomo", [
   ("Meanwhile, Max has had enough of hearing about it. In December twenty seventeen, right at the top, he finally buys six hundred and forty nine dollars of Bitcoin too.", None),
   ("At about nineteen thousand dollars a coin, he gets a tiny slice. Three hundredths of a bitcoin.", None),
   ("One year later, his six hundred and forty nine dollars are worth about one hundred and seven dollars.", None),
   ("Max sells, swears at the internet, and goes back to phones.", None),
   ("And the painful part? If Max had simply held that tiny slice until November twenty twenty six, it would be worth about two thousand and thirty dollars. Triple his money.", None),
   ("Same coin. Same amount of money. The only difference was the date, and the nerves.", None),
 ], dict(type="stage", loc="street", actors=[dict(who="max", x=600, y=1010, size=330, emo={0: "money", 2: "shock", 3: "angry"}), you(1380, {0: "neutral", 4: "worried"}, flip=True)],
         props=[dict(kind="tag", text="BOUGHT AT $19,379", col=AMBER, x=1000, y=320, at=0, scale=0.9), dict(kind="phone", text="$107", sub="MAX, DEC 2018", col=CORAL, x=1000, y=600, at=2, scale=0.9)],
         texts=[dict(text="SAME COIN, DIFFERENT DATE", size=90, col=CREAM, y=170, at=4, glow=10)], flash={2: CORAL}, shake=[2])),
 ("boom21", [
   ("You don't sell. Mostly because you forgot your password for a while. That counts.", None),
   ("Then twenty twenty one happens. In November, Bitcoin goes near sixty seven thousand dollars.", None),
   ("Your six hundred and forty nine dollars are now worth about one hundred and eighty four thousand.", None),
   ("You could buy two hundred and eighty iPhones. You don't. You just stare at the screen.", None),
 ], dict(type="chart", reveal=(0, 2), p0=i18 / i21, series=[dict(values=VALS[:i21 + 1], col=AMBER, width=9, fill=True)],
         xlabels=[(i, k) for i, k in YEARS if i <= i21], side=[dict(label="YOUR $649 OF BTC", values=VALS[:i21 + 1], col=AMBER)],
         texts=[dict(text=money(V("2021-11-09")), size=120, col=GREEN, x=760, y=170, at=2, glow=14)], actors=[dict(who="you", x=1650, y=1070, size=150, emo={0: "worried", 2: "money"})], flash={2: GREEN})),
 ("crash22", [
   ("Crash number two.", None),
   ("In twenty twenty two, one of the biggest crypto exchanges in the world, FTX, collapses. Customers can't get their money out.", None),
   ("By November, Bitcoin is under sixteen thousand. Your one hundred and eighty four thousand became forty three thousand.", None),
   ("If your coins had been sitting on the wrong exchange, they might have been stuck or gone, no matter what the price did.", None),
 ], dict(type="chart", reveal=(0, 2), p0=i21 / i22, series=[dict(values=VALS[:i22 + 1], col=AMBER, width=9, fill=True)],
         xlabels=[(i, k) for i, k in YEARS if i <= i22], side=[dict(label="YOUR $649 OF BTC", values=VALS[:i22 + 1], col=AMBER)],
         notes=[dict(i=i22, text="-76%", col=CORAL, dy=-130, dx=-80, size=90)], actors=[dict(who="you", x=1650, y=1070, size=150, emo={0: "shock", 2: "sad"})], flash={0: CORAL}, shake=[0])),
 ("peak25", [
   ("And then, the biggest wave yet.", None),
   ("On October fifth, twenty twenty five, Bitcoin hits about one hundred and twenty four thousand dollars.", None),
   ("Your six hundred and forty nine dollars are now worth three hundred and forty three thousand dollars.", None),
   ("That's a house deposit in many cities. From skipping one phone.", None),
 ], dict(type="chart", reveal=(0, 2), p0=i22 / i25, series=[dict(values=VALS[:i25 + 1], col=AMBER, width=9, fill=True)],
         xlabels=[(i, k) for i, k in YEARS if i <= i25], side=[dict(label="YOUR $649 OF BTC", values=VALS[:i25 + 1], col=AMBER)],
         texts=[dict(text=money(V("2025-10-05")), size=130, col=GREEN, x=760, y=170, at=2, glow=16)], actors=[dict(who="you", x=1650, y=1070, size=150, emo={0: "neutral", 2: "money"})], flash={2: GREEN}, shake=[2])),
 ("crash26", [
   ("And crash number three. Over the following year, Bitcoin falls again.", None),
   ("On November twenty fifth, twenty twenty six, it's around sixty thousand six hundred dollars. About half of the peak.", None),
   ("Your three hundred and forty three thousand dollars are now about one hundred and sixty six thousand.", None),
   ("Still an incredible result. But imagine watching one hundred and seventy six thousand dollars disappear in a year, and doing nothing.", None),
 ], dict(type="chart", reveal=(0, 1), p0=i25 / len(KEYS), series=[dict(values=VALS, col=AMBER, width=9, fill=True)],
         xlabels=YEARS, side=[dict(label="YOUR $649 OF BTC", values=VALS, col=AMBER)],
         notes=[dict(i=len(VALS) - 1, text="-51%", col=CORAL, dy=-130, dx=-80, size=90)], actors=[dict(who="you", x=1650, y=1070, size=150, emo={0: "worried", 3: "shock"})], flash={1: CORAL})),
 ("nerves", [
   ("Why is holding so hard? Because losses hurt more than gains feel good.", None),
   ("Psychologists call it loss aversion. Watching forty four thousand dollars vanish feels far worse than gaining the same amount feels nice.", None),
   ("So most people sell exactly when it hurts the most. Which is usually near the bottom.", None),
   ("Timeline B didn't win because it was smart. It won because it sat still through things that made almost everyone else run.", None),
 ], dict(type="stage", loc="bedroom", actors=[you(700, {0: "worried", 1: "sad", 3: "neutral"})],
         props=[dict(kind="tag", text="LOSSES HURT MORE", col=CORAL, x=1300, y=380, at=1, scale=1.0), dict(kind="phone", text="SELL?", sub="3:00 AM", col=CORAL, x=1300, y=640, at=2, scale=0.8)],
         texts=[dict(text="LOSS AVERSION", size=120, col=AMBER, y=170, at=1, glow=14)])),
 ("phone_side", [
   ("Meanwhile, timeline A. The iPhone six s.", None),
   ("It gave you photos, maps, music, and about four years of a good life. Then a slow battery, then a drawer.", None),
   ("Today, it's worth very little. But to be fair, a phone is not an investment. You use it, and that's the point.", None),
   ("The question isn't phone versus coin. It's what you do with money you don't need for daily life.", None),
   ("If the money is for living, spend it on living. If it's spare money for the long term, that's when the timelines really start to split.", None),
   ("And for most people, the boring long term choice, like a broad index fund, does a lot of the heavy lifting without needing nerves of steel.", None),
 ], dict(type="stage", loc="bedroom", actors=[you(620, {0: "neutral", 1: "happy", 2: "sad", 3: "neutral"})],
         props=[dict(kind="icon", name="iphone", x=1200, y=520, at=0, scale=1.0), dict(kind="tag", text="NOT AN INVESTMENT", col=TEAL, x=1200, y=820, at=2, scale=0.8)],
         texts=[dict(text="A PHONE IS FOR USING", size=96, col=CREAM, y=170, at=2, glow=10)])),
 ("survivor", [
   ("Now the part most crypto videos skip.", None),
   ("Very few people actually held from twenty fifteen to today. Most sold at the first big gain, or the first big crash.", None),
   ("Plenty of other coins from those years lost almost everything. Exchanges failed. People lost passwords and keys forever.", None),
   ("When you hear a Bitcoin success story, you're hearing from the timeline that survived. You don't hear from the ones that didn't.", None),
   ("That's called survivorship bias. And it makes every risky bet look easier than it was.", None),
 ], dict(type="stage", loc="void_red", actors=[you(1500, {0: "neutral", 2: "worried", 4: "shock"})],
         props=[dict(kind="tag", text="SOLD TOO EARLY", col=CORAL, x=650, y=300, at=1, scale=0.9), dict(kind="tag", text="COIN WENT TO ZERO", col=CORAL, x=650, y=450, at=2, scale=0.9), dict(kind="tag", text="EXCHANGE FAILED", col=CORAL, x=650, y=600, at=2.3, scale=0.9), dict(kind="tag", text="LOST THE KEYS", col=CORAL, x=650, y=750, at=2.6, scale=0.9)],
         texts=[dict(text="SURVIVORSHIP BIAS", size=120, col=AMBER, y=170, at=4, glow=14)], flash={4: AMBER})),
 ("compare", [
   ("For comparison, the same six hundred and forty nine dollars in an S and P five hundred index fund in September twenty fifteen would be about two thousand five hundred and sixty dollars, counting price only.", None),
   ("Far less exciting. Also far less terrifying. Its worst drops in these years were nowhere near eighty four percent.", None),
   ("Bitcoin's result is real. So is the risk that came with it.", None),
 ], dict(type="bars", groups=[dict(label="S&P 500", sub="price only, Sep 2026", vals=[(2560, TEAL)], at=0), dict(label="BITCOIN", sub="Nov 25, 2026", vals=[(V("2026-11-25"), AMBER)], at=0.4)],
         texts=[dict(text="REWARD = RISK", size=110, col=CREAM, y=170, at=2, glow=12)])),
 ("now_what", [
   ("So, should you buy Bitcoin today because of this story? This video can't answer that, and nobody honestly can.", None),
   ("The past ten years happened once. The next ten could look completely different, up or down.", None),
   ("What we can learn is about behaviour, not about the coin.", None),
   ("Big rewards almost always come with big drops. If you can't handle the drop, you won't be there for the reward.", None),
   ("And money you need in the next few years has no business riding a rollercoaster.", None),
 ], dict(type="stage", loc="void", actors=[you(1500, {0: "worried", 3: "neutral", 4: "smug"})],
         props=[dict(kind="icon", name="warning", x=650, y=420, at=0, scale=0.9), dict(kind="tag", text="BIG REWARD = BIG DROPS", col=AMBER, x=650, y=720, at=3, scale=0.9)],
         texts=[dict(text="NOBODY KNOWS THE NEXT 10 YEARS", size=80, col=CREAM, y=170, at=1, glow=10)])),
 ("rules", [
   ("So if you're thinking about crypto, here's what the careful people usually say.", None),
   ("Only put in money you could lose completely and still sleep at night.", None),
   ("Keep it a small slice, not your emergency fund, and never borrowed money.", None),
   ("Learn how storage, scams and fees work before you buy anything. Scammers love beginners.", None),
 ], dict(type="list", title="IF YOU TOUCH CRYPTO", tcol=AMBER, items=[dict(text="Only money you can lose 100%", at=1), dict(text="Small slice, never your emergency fund", at=2), dict(text="Never borrowed money", at=2.3), dict(text="Learn storage, scams, fees first", at=3)],
         actors=[you(1690, {0: "neutral", 3: "worried"}, size=240, y=1040)])),
 ("honest", [
   ("And the honest part. This is not financial advice, and definitely not a recommendation to buy Bitcoin.", None),
   ("Crypto prices are extremely volatile, and past returns tell you nothing certain about the future.", None),
   ("Rules and taxes differ by country. Check yours.", None),
 ], dict(type="list", title="NOT FINANCIAL ADVICE", tcol=CORAL, items=[dict(text="Not a recommendation to buy", at=0.5), dict(text="Extremely volatile", at=1), dict(text="Past returns = no promise", at=1.3), dict(text="Rules and taxes differ by country", at=2)],
         actors=[you(1680, "neutral", size=240, y=1040)])),
 ("outro", [
   ("One phone. Two point seven five coins. Three crashes. And a lot of nerves.", None),
   ("Be honest in the comments. Would you have held through all three crashes, or sold in twenty eighteen?", None),
   ("And I'll see you in the other timeline.", None),
 ], dict(type="end", q1="WOULD YOU", q2="HAVE HELD?", comment="Hold or sell in 2018?", comment_at=1, emo={0: "neutral", 1: "smug"})),
]

META = dict(
    file="EP05_Bitcoin_vs_iPhone_2015.mp4",
    title="What If You Bought Bitcoin Instead of an iPhone in 2015?",
    description="""September 2015: the iPhone 6s costs $649. One version of you buys the phone. The other buys 2.75 bitcoins. One ends up with a phone in a drawer, the other with $166,849... after surviving three crashes of 84%, 76% and 51%. Plus the part most crypto videos skip.

Data: Bitcoin price, Coinbase BTC-USD daily close (FRED CBBTCUSD), Sep 25 2015 to Nov 25 2026. S&P 500 comparison: Robert Shiller monthly data, price only. iPhone 6s 16 GB launch price $649. No fees or taxes.
This video is for education and entertainment only. It is not financial advice and not a recommendation to buy crypto.

#whatif #bitcoin #personalfinance""",
    tags=["what if", "bitcoin 2015", "bitcoin instead of iphone", "bitcoin price history", "crypto crash", "survivorship bias", "personal finance", "financial education", "investing", "the other timeline", "animated story"],
    comment="Be honest: would you have held through all 3 crashes, or sold in 2018? 👇",
    chapters={"hook": "$649: phone or coin?", "store": "The phone store", "what_is": "What is Bitcoin?", "max_fomo": "Max buys the top", "nerves": "Why holding is so hard", "buy": "Two timelines", "boom17": "2017: genius", "crash18": "Crash #1 (-84%)", "boom21": "2021", "crash22": "Crash #2 (-76%)",
              "peak25": "The 2025 peak", "crash26": "Crash #3 (-51%)", "phone_side": "Meanwhile, the phone", "survivor": "What nobody tells you", "compare": "Compared to an index fund",
              "now_what": "Should you buy now?", "rules": "If you touch crypto", "honest": "The honest part", "outro": "Would you have held?"},
)

THUMBS = {
    "A": dict(loc="store", quote="i skipped the iPhone..", hl=["iPhone.."], actors=[dict(who="you", x=480, size=560, emo="money"), dict(who="max", x=1480, size=520, emo="shock", flip=True)],
              props=[dict(kind="icon", name="btc", x=980, y=600, scale=1.2)], big=dict(text="$343,140", x=980, y=350, col=GREEN, size=170, rot=-4), line=(620, 600, 1380, 640), lcol=AMBER),
    "B": dict(loc="void_red", quote="-84% then THIS", hl=["-84%", "THIS"], actors=[dict(who="you", x=460, size=580, emo="shock")],
              props=[dict(kind="icon", name="iphone", x=1100, y=640, scale=1.0), dict(kind="icon", name="btc", x=1550, y=640, scale=1.0)], big=dict(text="$649 = ???", x=1320, y=380, col=AMBER, size=170)),
}

SHORT = dict(segs=[("hook", [0, 1, 2]), ("crash18", [1, 2, 3]), ("survivor", [3])], title=["BITCOIN INSTEAD OF", "AN IPHONE IN 2015?"], hook=dict(text="$166,849", col=GREEN, dur=1.8),
             yt_title="I Skipped the iPhone and Bought Bitcoin in 2015 #shorts",
             yt_desc="$649 of Bitcoin on Sep 25 2015, real Coinbase prices (FRED), three crashes included. Full video on the channel. Not financial advice. #bitcoin #whatif #money")
