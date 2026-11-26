"""EP03 — What If You Only Paid the Minimum on Your Credit Card?  (two timelines)
APR 21.19% = average US credit card APR on accounts assessed interest, Aug 2026 (Fed G.19 via FRED TERMCBCCALLNS);
Aug 2016: 12.51%. Balance $5,000. Minimum = greater of $25 or 1% of balance + interest (a common formula).
Minimum: 229 months, total paid $12,782 (interest $7,782); balance after 12/60/120 months: $4,432 / $2,736 / $1,497.
First minimum $138.29 of which $88.29 interest. Fixed $150: 51 mo, $2,612 interest; $200: 34 mo, $1,655; $300: 20 mo, $974; $500: 12 mo, $550."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
from kit import *  # noqa
import data

APR_S = data.fred("TERMCBCCALLNS")
APR = APR_S["2026-08"]
MA, PA, BA = data.card_payoff(5000, APR)
MB, PB, BB = data.card_payoff(5000, APR, fixed=200)
BB2 = BB + [0.0] * (len(BA) - len(BB))
APR_KEYS = [k for k in sorted(APR_S) if k >= "2006-01"]
APR_VALS = [APR_S[k] for k in APR_KEYS]

SPEED = 1.18
MUSIC_SEED = 3
END_LINE = "PAY MORE THAN THE MINIMUM"

def you(x=960, emo="neutral", size=330, **k):
    return dict(who="you", x=x, y=k.pop("y", 1010), size=size, emo=emo, **k)

BEATS = [
 ("hook", [
   ("What if you bought five thousand dollars of stuff on a credit card, and only ever paid the minimum?", None),
   ("No missed payments. No late fees. You do exactly what the bill asks you to do.", None),
   ("It would take you nineteen years to pay it off.", None),
   ("And that five thousand dollars of stuff would end up costing you almost thirteen thousand.", None),
   ("Today, two versions of you get the same card, the same bill, and make one tiny different choice.", None),
 ], dict(type="stage", loc="void_red", actors=[you(1500, {0: "neutral", 2: "shock", 3: "worried"})],
         props=[dict(kind="card", label="TIMELINE CARD", col=CORAL, x=700, y=420, at=0, scale=1.3, rot=-8), dict(kind="tag", text="19 YEARS", col=CORAL, x=700, y=720, at=2, scale=1.2)],
         counters=[dict(**{"from": 5000, "to": PA}, at=3, dur=2.2, x=700, y=200, col=CORAL, size=140, label="WHAT $5,000 REALLY COSTS")],
         flash={2: CORAL, 3: CORAL}, shake=[2])),
 ("spree", [
   ("It starts on a good day. You just got the card, and Max has ideas.", None),
   ("New phone, because yours has a crack. A sofa, because you're an adult now. A weekend trip, because life is short.", None),
   ("And a few gadgets, because Max said so.", None),
   ("Swipe. Swipe. Swipe. It doesn't even feel like money. It feels like tapping a piece of plastic.", None),
   ("Total: five thousand dollars.", None),
 ], dict(type="stage", loc="store", actors=[you(560, {0: "happy", 3: "money", 4: "worried"}), dict(who="max", x=1400, y=1010, size=320, emo={0: "happy", 2: "smug"}, flip=True, talk=[0, 2])],
         props=[dict(kind="icon", name="iphone", x=800, y=480, at=1, scale=0.8), dict(kind="icon", name="sofa", x=1060, y=500, at=1.3, scale=0.8), dict(kind="tag", text="TRIP $1,500", col=PINK, x=980, y=300, at=1.6, scale=0.9),
                dict(kind="card", label="SWIPE", col=CORAL, x=960, y=600, at=3, scale=0.8, shake_at=3)],
         texts=[dict(text="$5,000", size=170, col=CORAL, y=180, at=4, glow=16)], flash={4: CORAL}, shake=[4])),
 ("bill", [
   ("A month later, the bill arrives.", None),
   ("Balance: five thousand dollars. Minimum payment due: one hundred and thirty eight dollars and twenty nine cents.", None),
   ("You breathe out. That's it? That's easy.", None),
   ("But look closer. Of those one hundred and thirty eight dollars, eighty eight dollars are interest.", None),
   ("Only fifty dollars actually go toward the stuff you bought.", None),
   ("So every month, most of your payment just pays for the privilege of still owing money.", None),
 ], dict(type="stage", loc="kitchen", actors=[you(1500, {0: "neutral", 2: "happy", 3: "shock", 4: "worried"})],
         props=[dict(kind="receipt", lines=[["Balance", "$5,000.00"], ["APR", "21.19%"], ["Minimum due", "$138.29"]], x=760, y=500, at=0, scale=1.3),
                dict(kind="tag", text="INTEREST $88.29", col=CORAL, x=760, y=860, at=3, scale=0.9), dict(kind="tag", text="YOUR STUFF $50.00", col=TEAL, x=760, y=170, at=4, scale=0.9)],
         flash={3: CORAL}, shake=[3])),
 ("apr", [
   ("Where does that interest come from? The annual percentage rate.", None),
   ("In August twenty twenty six, the average credit card rate in America, on accounts that pay interest, was twenty one point one nine percent.", None),
   ("Ten years earlier, in twenty sixteen, it was about twelve and a half.", None),
   ("So the same card balance is now much more expensive to carry than it used to be.", None),
 ], dict(type="chart", reveal=(0, 2), series=[dict(values=APR_VALS, col=CORAL, width=9)], yfmt="{:.0f}%", vmax=26,
         xlabels=[(i, k[:4]) for i, k in enumerate(APR_KEYS) if k.endswith("-02") and int(k[:4]) % 4 == 2],
         side=[dict(label="AVG CARD APR", values=APR_VALS, col=CORAL, fmt="{:.2f}%")],
         footnote="Average APR on credit card accounts assessed interest (Federal Reserve G.19, via FRED TERMCBCCALLNS), quarterly.",
         texts=[dict(text="21.19%", size=150, col=CORAL, x=700, y=170, at=1, glow=16)], actors=[dict(who="you", x=1650, y=1070, size=150, emo={0: "neutral", 1: "shock"})])),
 ("split", [
   ("Now the timeline splits.", None),
   ("Timeline A pays exactly the minimum, every month, forever. Never late. Never more.", None),
   ("Timeline B decides to pay a flat two hundred dollars every month until it's gone.", None),
   ("Neither of them buys anything else on the card. Same balance, same rate.", None),
   ("Just sixty two dollars a month of difference at the start.", None),
 ], dict(type="split", left=dict(title="TIMELINE A", sub="pays the minimum", col=CORAL, who="you", emo="happy", value=dict(**{"from": 0, "to": 138.29}, at=1, dur=1.2, label="first payment")),
         right=dict(title="TIMELINE B", sub="pays $200 every month", col=TEAL, who="you", emo="neutral", at=2, value=dict(**{"from": 0, "to": 200}, at=2, dur=1.2, label="every payment")),
         texts=[dict(text="+$62 / MONTH", size=90, col=AMBER, y=860, at=4, glow=10)])),
 ("year1", [
   ("Timeline A. One year later.", None),
   ("You've made twelve perfect payments. About one thousand six hundred dollars, gone.", None),
   ("You check the balance. Four thousand four hundred and thirty two dollars.", None),
   ("A whole year of paying, and the balance dropped by less than six hundred.", None),
   ("Max says it's normal. Max also still owes you twenty dollars from two thousand nineteen.", None),
 ], dict(type="stage", loc="living", actors=[you(560, {0: "neutral", 2: "shock", 3: "sad"}), dict(who="max", x=1400, y=1010, size=300, emo="smug", flip=True, at=4, talk=[4])],
         props=[dict(kind="phone", text=money(BA[12]), sub="BALANCE · YEAR 1", col=CORAL, x=1000, y=560, at=2, scale=1.0), dict(kind="calendar", top="YEAR", big="1", x=1000, y=300, at=0, until=1.9, scale=0.8)],
         bubbles=[dict(text="Totally normal, bro.", x=1400, y=520, at=4)], flash={2: CORAL})),
 ("year5", [
   ("Year five. The sofa has a stain shaped like Australia.", None),
   ("The phone is so old it's no longer getting updates.", None),
   ("You still owe two thousand seven hundred and thirty six dollars on them.", None),
   ("You're paying for a sofa you would now pay someone to take away.", None),
 ], dict(type="stage", loc="living", actors=[you(560, {0: "worried", 2: "shock", 3: "sad"})],
         props=[dict(kind="icon", name="sofa", x=1300, y=700, at=0, scale=1.2), dict(kind="icon", name="iphone", x=1000, y=380, at=1, scale=0.6), dict(kind="phone", text=money(BA[60]), sub="BALANCE · YEAR 5", col=CORAL, x=1000, y=560, at=2, scale=1.0)],
         texts=[dict(text="STILL PAYING FOR THIS", size=90, col=CORAL, y=170, at=3, glow=10)])),
 ("limit", [
   ("Somewhere around year three, timeline A gets a happy email.", None),
   ("Congratulations! You've been approved for a higher credit limit.", None),
   ("It feels like a reward. Like the bank trusts you.", None),
   ("But think about what the bank sees. A customer who always pays, never pays it all, and keeps a balance month after month.", None),
   ("To a card company, that's not a problem customer. That's the perfect customer.", None),
   ("Max, of course, immediately suggests a bigger TV.", None),
 ], dict(type="stage", loc="living", actors=[you(560, {0: "happy", 3: "worried", 5: "shock"}), dict(who="max", x=1420, y=1010, size=300, emo="happy", flip=True, at=5, talk=[5])],
         props=[dict(kind="phone", text="+$3,000", sub="NEW LIMIT!", col=GREEN, x=1000, y=520, at=1, until=3.9, scale=1.0), dict(kind="tag", text="PERFECT CUSTOMER", col=CORAL, x=1000, y=360, at=4, scale=1.0), dict(kind="icon", name="tv", x=1050, y=640, at=5, scale=0.7)],
         bubbles=[dict(text="Bigger TV?", x=1420, y=520, at=5)], texts=[dict(text="CONGRATULATIONS?", size=110, col=AMBER, y=170, at=1, until=3.9, glow=12)])),
 ("year10", [
   ("Year ten. You've moved apartments twice. The sofa is gone. The phone is in a drawer.", None),
   ("Balance: one thousand four hundred and ninety seven dollars.", None),
   ("You have now paid nine thousand six hundred and eighty nine dollars in total. Almost double the price of everything. And you still owe almost fifteen hundred.", None),
   ("And the payments are getting smaller, so the end keeps moving further away.", None),
 ], dict(type="stage", loc="bedroom", actors=[you(700, {0: "neutral", 1: "sad", 2: "shock"})],
         props=[dict(kind="calendar", top="YEAR", big="10", x=1250, y=320, at=0, scale=0.9), dict(kind="phone", text=money(BA[120]), sub="BALANCE · YEAR 10", col=CORAL, x=1250, y=640, at=1, scale=1.0)],
         flash={2: CORAL})),
 ("end_a", [
   ("Timeline A finally pays it off after two hundred and twenty nine months.", None),
   ("Nineteen years and one month.", None),
   ("Total paid: twelve thousand seven hundred and eighty two dollars. For five thousand dollars of stuff that's long gone.", None),
   ("Seven thousand seven hundred and eighty two dollars of that was pure interest.", None),
   ("You could have bought the whole spree again. And again. With the interest alone.", None),
 ], dict(type="stage", loc="void_red", actors=[you(1520, {0: "neutral", 2: "shock", 4: "sad"})],
         counters=[dict(label="TOTAL PAID", **{"from": 5000, "to": PA}, at=2, dur=2.0, x=700, y=360, col=CORAL, size=150), dict(label="INTEREST ONLY", **{"from": 0, "to": PA - 5000}, at=3, dur=1.8, x=700, y=680, col=AMBER, size=130)],
         texts=[dict(text="19 YEARS, 1 MONTH", size=110, col=CREAM, y=150, at=1, glow=10)], flash={2: CORAL, 3: AMBER}, shake=[2])),
 ("end_b", [
   ("Now timeline B. Two hundred dollars a month, no matter what.", None),
   ("Thirty four months later, the card is at zero. Less than three years.", None),
   ("Total paid: six thousand six hundred and fifty five dollars. Interest: one thousand six hundred and fifty five.", None),
   ("Still not free. But six thousand one hundred dollars cheaper than timeline A.", None),
   ("And for the next sixteen years, that two hundred dollars a month is free to do something else.", None),
 ], dict(type="stage", loc="void_teal", actors=[you(1520, {0: "neutral", 1: "happy", 4: "money"})],
         counters=[dict(label="MONTHS", **{"from": 0, "to": MB}, at=1, dur=1.4, x=700, y=300, col=TEAL, size=140, fmt="int"), dict(label="TOTAL PAID", **{"from": 5000, "to": PB}, at=2, dur=1.6, x=700, y=600, col=TEAL, size=130)],
         texts=[dict(text="SAVED $6,127", size=110, col=GREEN, y=820, at=3, glow=14)], flash={1: TEAL, 3: GREEN})),
 ("freedom", [
   ("And this is where the gap gets really big.", None),
   ("After month thirty four, timeline B still has the habit of paying two hundred dollars a month. It just sends it somewhere else now.", None),
   ("Remember our last video? Two hundred dollars a month invested in an S and P five hundred index fund from twenty ten to twenty twenty six turned forty thousand two hundred dollars into about one hundred and thirty thousand.", None),
   ("Past results, not a promise. But that's the size of what's at stake.", None),
   ("Timeline A spends those same years paying interest on a sofa that's already in a landfill.", None),
 ], dict(type="split", left=dict(title="TIMELINE A", sub="still paying the card", col=CORAL, who="you", emo="sad", props=[dict(kind="icon", name="sofa", x=620, y=640, scale=0.6)]),
         right=dict(title="TIMELINE B", sub="$200/mo, now invested", col=TEAL, who="you", emo="money", at=1, value=dict(**{"from": 40200, "to": 130418}, at=2, dur=2.2, label="$200/mo, 2010 to 2026 (S&P 500, past data)", y=420)),
         flash={2: TEAL})),
 ("curves", [
   ("Here are both balances side by side.", None),
   ("Timeline B drops like a rock and hits zero before year three.", None),
   ("Timeline A slides down so slowly that it almost looks flat.", None),
   ("That long tail is where the bank makes most of its money from you.", None),
 ], dict(type="chart", reveal=(0, 2), series=[dict(values=BA, col=CORAL, width=9), dict(values=BB2, col=TEAL, width=9)],
         xlabels=[(i, f"Y{i // 12}") for i in range(0, len(BA), 36)], side=[dict(label="TIMELINE A OWES", values=BA, col=CORAL), dict(label="TIMELINE B OWES", values=BB2, col=TEAL)],
         footnote="$5,000 at 21.19% APR. A: minimum = greater of $25 or 1% of balance + interest. B: $200 a month. No new purchases.",
         texts=[dict(text="THE LONG TAIL", size=100, col=CORAL, x=900, y=170, at=3, glow=12)])),
 ("stress", [
   ("There's also a cost that doesn't show up on the statement.", None),
   ("Carrying debt for years means every unexpected bill hits harder. A broken laptop, a car repair, a dentist visit.", None),
   ("And when there's no cushion, those surprises often go right back on the same card.", None),
   ("That's how a five thousand dollar balance quietly becomes a lifestyle.", None),
 ], dict(type="stage", loc="kitchen", actors=[you(700, {0: "neutral", 1: "worried", 3: "sad"})],
         props=[dict(kind="tag", text="CAR REPAIR $640", col=CORAL, x=1350, y=320, at=1, scale=0.8), dict(kind="tag", text="DENTIST $280", col=CORAL, x=1350, y=480, at=1.4, scale=0.8), dict(kind="tag", text="LAPTOP $900", col=CORAL, x=1350, y=640, at=1.8, scale=0.8),
                dict(kind="card", label="SAME CARD", col=CORAL, x=1350, y=820, at=2, scale=0.6)],
         texts=[dict(text="DEBT BECOMES A LIFESTYLE", size=96, col=CORAL, y=170, at=3, glow=12)], shake=[2])),
 ("more", [
   ("And look what happens when you pay even more.", None),
   ("One hundred and fifty dollars a month: about four years, two thousand six hundred in interest.", None),
   ("Three hundred a month: twenty months, under one thousand dollars of interest.", None),
   ("Five hundred a month: one year, five hundred and fifty dollars of interest.", None),
   ("Every extra dollar you pay today kills several dollars of future interest.", None),
 ], dict(type="bars", fmt="money", groups=[dict(label="MINIMUM", sub="229 months", vals=[(PA - 5000, CORAL)], at=0), dict(label="$150/mo", sub="51 months", vals=[(2612, AMBER)], at=1),
         dict(label="$200/mo", sub="34 months", vals=[(PB - 5000, TEAL)], at=1.5), dict(label="$300/mo", sub="20 months", vals=[(974, GREEN)], at=2), dict(label="$500/mo", sub="12 months", vals=[(550, GREEN)], at=3)],
         texts=[dict(text="INTEREST YOU PAY", size=90, col=CREAM, y=140, glow=8)])),
 ("why_min", [
   ("So why is the minimum so low?", None),
   ("The minimum is the smallest payment the bank will accept without calling you late. It's not a recommendation.", None),
   ("It's designed to keep your account in good standing. Not to get you out of debt.", None),
   ("In the US, your statement must even show how long paying only the minimum would take. Most people never read that box.", None),
 ], dict(type="stage", loc="bank", actors=[you(560, {0: "neutral", 1: "worried", 3: "shock"}), dict(who="banker", x=1380, y=1010, size=320, emo={0: "happy", 2: "smug"}, flip=True, talk=[1])],
         props=[dict(kind="receipt", lines=[["If you pay only", "the minimum"], ["you will pay off", "in 19 years"]], x=960, y=420, at=3, scale=1.1)],
         texts=[dict(text="MINIMUM IS NOT A PLAN", size=100, col=CORAL, y=170, at=1, glow=12)])),
 ("escape", [
   ("If you're already in timeline A, here's how people usually get out.", None),
   ("One. Stop adding new purchases to the card. You can't bail out a boat that's still taking water.", None),
   ("Two. Pay a fixed amount, above the minimum, and automate it.", None),
   ("Three. If you have several cards, put every extra dollar on the one with the highest rate first.", None),
   ("Four. Call and ask for a lower rate, or look at a balance transfer offer. Read the fees and the end date carefully.", None),
   ("And five. Build even a small emergency fund, so the next surprise doesn't land on the card.", None),
 ], dict(type="list", title="HOW PEOPLE GET OUT", items=[dict(text="Stop adding new purchases", at=1), dict(text="Fixed payment above the minimum, automated", at=2), dict(text="Highest rate first", at=3), dict(text="Ask for a lower rate / balance transfer (read fees)", at=4), dict(text="Small emergency fund", at=5)],
         actors=[you(1690, {0: "worried", 2: "neutral", 4: "happy"}, size=240, y=1040)])),
 ("bnpl", [
   ("And the same idea now hides behind friendlier buttons.", None),
   ("Pay in four. Split it. Only twenty five dollars today.", None),
   ("Some of these plans charge no interest if every payment is on time. Others charge fees, or work like a loan.", None),
   ("The danger isn't one plan. It's ten small plans at once, each looking harmless on its own.", None),
   ("Same rule as the card. Know the total, know the end date, and never let the small number hide the big one.", None),
 ], dict(type="stage", loc="store", actors=[you(1500, {0: "neutral", 3: "worried", 4: "smug"}, size=300)],
         props=[dict(kind="tag", text="PAY IN 4", col=PINK, x=560, y=300, at=1, scale=0.9), dict(kind="tag", text="ONLY $25 TODAY", col=AMBER, x=560, y=460, at=1.4, scale=0.9),
                dict(kind="phone", text="10 PLANS", sub="ACTIVE", col=CORAL, x=1000, y=560, at=3, scale=0.9)],
         texts=[dict(text="KNOW THE TOTAL", size=110, col=GREEN, y=170, at=4, glow=12)])),
 ("cards_ok", [
   ("To be fair, credit cards aren't evil.", None),
   ("If you pay the full statement balance every month, many cards charge you no interest at all.", None),
   ("The card is a tool. The minimum payment is the trap.", None),
 ], dict(type="stage", loc="void", actors=[you(1500, {0: "neutral", 2: "smug"})],
         props=[dict(kind="card", label="FULL BALANCE", col=TEAL, x=700, y=420, at=1, scale=1.2), dict(kind="tag", text="INTEREST $0", col=GREEN, x=700, y=700, at=1.5, scale=1.0)],
         texts=[dict(text="TOOL, NOT TRAP", size=130, col=AMBER, y=170, at=2, glow=14)])),
 ("honest", [
   ("The honest part: this is not financial advice.", None),
   ("Card terms, minimum payment formulas and rates differ by bank and by country. Check your own statement.", None),
   ("If debt feels overwhelming, non-profit credit counselling services can help you make a plan.", None),
 ], dict(type="list", title="NOT FINANCIAL ADVICE", tcol=CORAL, items=[dict(text="Terms differ by bank and country", at=1), dict(text="Check your own statement", at=1.5), dict(text="Non-profit credit counselling exists", at=2)],
         actors=[you(1680, "neutral", size=240, y=1040)])),
 ("outro", [
   ("Same card. Same five thousand dollars. One version of you pays for nineteen years. The other is free in under three.", None),
   ("Have you ever been stuck paying the minimum? Tell me in the comments, no judgement.", None),
   ("And I'll see you in the other timeline.", None),
 ], dict(type="end", q1="MINIMUM OR", q2="MORE?", comment="Ever stuck on the minimum?", comment_at=1, emo={0: "neutral", 1: "happy"})),
]

META = dict(
    file="EP03_Only_Paid_the_Minimum.mp4",
    title="What If You Only Paid the Minimum on Your Credit Card?",
    description="""Two versions of you put $5,000 on a credit card. One pays the minimum, one pays $200 a month. One is free in 34 months. The other pays for 19 years and $12,782.

Method: $5,000 balance at 21.19% APR (average US rate on credit card accounts assessed interest, Aug 2026, Federal Reserve G.19 via FRED). Minimum payment = greater of $25 or 1% of the balance plus interest (a common formula; your card may differ). No new purchases, no fees.
This video is for education and entertainment only. It is not financial advice.

#whatif #creditcard #personalfinance""",
    tags=["what if", "credit card minimum payment", "credit card debt", "minimum payment trap", "apr", "interest", "debt payoff", "personal finance", "financial education", "money tips", "the other timeline", "animated story"],
    comment="Have you ever been stuck paying only the minimum? No judgement, tell me below 👇",
    chapters={"hook": "19 years for $5,000", "spree": "The spree", "bill": "The first bill", "apr": "Why rates matter now", "split": "Two timelines", "year1": "Year 1", "year5": "Year 5", "year10": "Year 10",
              "end_a": "Timeline A: the final bill", "end_b": "Timeline B: 34 months", "limit": "The higher limit", "freedom": "What B does next", "stress": "The hidden cost", "curves": "The long tail", "more": "Pay a bit more", "why_min": "Why the minimum is so low",
              "escape": "How people get out", "bnpl": "Buy now, pay later", "cards_ok": "Cards aren't evil", "honest": "The honest part", "outro": "Minimum or more?"},
)

THUMBS = {
    "A": dict(loc="living", quote="i only paid the minimum..", hl=["minimum.."], actors=[dict(who="you", x=520, size=560, emo="shock"), dict(who="banker", x=1460, size=540, emo="smug", flip=True)],
              props=[dict(kind="card", label="CARD", col=CORAL, x=960, y=600, scale=1.3, rot=-10)], big=dict(text="19 YEARS", x=990, y=380, col=CORAL, size=190, rot=-4), line=(1380, 560, 640, 620), lcol=CORAL),
    "B": dict(loc="void_red", quote="$5,000 became..", hl=["$5,000"], actors=[dict(who="you", x=480, size=580, emo="worried")],
              props=[dict(kind="card", label="MINIMUM", col=CORAL, x=1380, y=640, scale=1.2, rot=8)], big=dict(text="$12,782", x=1200, y=360, col=CORAL, size=200)),
}

SHORT = dict(segs=[("bill", [1, 3, 4]), ("end_a", [1, 2, 3])], title=["ONLY PAYING THE MINIMUM?", "WATCH THIS"], hook=dict(text="19 YEARS", col=CORAL, dur=1.8),
             yt_title="Only Paying the Minimum = 19 Years 😳 #shorts",
             yt_desc="$5,000 at 21.19% APR, minimum payments only. Real average US card rate (Fed G.19). Full video on the channel. Not financial advice. #creditcard #debt #money")
