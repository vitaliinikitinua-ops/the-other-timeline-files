"""Finance ep 1 script: What IF You Saved $5 a Day Since 2010?
Each beat = one scene. Each sentence = (subtitle text, spoken text or None if identical).
All numbers come from data.py (S&P 500 monthly avg. price, R. Shiller dataset; CPI from same dataset)."""

BEATS = [
 ("hook", [
  ("What if you saved $5 a day, starting in January 2010?", "What if you saved five dollars a day, starting in January twenty ten?"),
  ("Not a fortune. Just the price of one coffee.", None),
  ("Today I'll show you two timelines of the same life.", None),
  ("Same person. Same $5.", "Same person. Same five dollars."),
  ("And by the end, one of them is sitting on almost $100,000.", "And by the end, one of them is sitting on almost one hundred thousand dollars."),
 ]),
 ("rule", [
  ("Here's the rule. Every day, $5.", "Here's the rule. Every day, five dollars."),
  ("That's about $152 a month.", "That's about one hundred and fifty two dollars a month."),
  ("In timeline A, you spend it.", "In timeline A, you spend it."),
  ("In timeline B, on the first of every month, you put it into an S&P 500 index fund.", "In timeline B, on the first of every month, you put it into an S and P five hundred index fund."),
  ("It simply owns a small piece of about 500 of the largest US companies.", "It simply owns a small piece of about five hundred of the largest US companies."),
  ("Nothing fancy. No stock picking.", None),
 ]),
 ("timeline_a", [
  ("Timeline A first. It's 2010.", "Timeline A first. It's twenty ten."),
  ("You grab a coffee on the way to work. It tastes great.", None),
  ("You do it again tomorrow. And the day after.", None),
  ("By September 2026, that's about 6,100 coffees.", "By September twenty twenty six, that's about six thousand one hundred coffees."),
  ("$30,569, spent.", "Thirty thousand, five hundred and sixty nine dollars. Spent."),
  ("And what's left of it today? Some good mornings. And zero dollars.", None),
 ]),
 ("inflation", [
  ("And even if you'd kept that cash under a mattress, it would be shrinking.", None),
  ("Between 2010 and 2023 alone, US consumer prices rose about 41%.", "Between twenty ten and twenty twenty three alone, US consumer prices rose about forty one percent."),
  ("The same banknote buys less every single year.", None),
 ]),
 ("b_start", [
  ("Now, timeline B. Same coffee money, but invested.", None),
  ("The first years feel pointless.", None),
  ("After two years you've put in about $3,800, and it's worth about $4,100.", "After two years you've put in about three thousand eight hundred dollars, and it's worth about four thousand one hundred."),
  ("A few hundred dollars of growth. Most people quit right here.", None),
 ]),
 ("compound", [
  ("But something quietly starts happening.", None),
  ("Your money earns returns, and then those returns earn returns of their own.", None),
  ("That's compounding.", None),
  ("By January 2018, you've put in about $14,800, and it's worth $25,000.", "By January twenty eighteen, you've put in about fourteen thousand eight hundred dollars, and it's worth twenty five thousand."),
 ]),
 ("covid", [
  ("Then, 2020. A pandemic shuts down the world.", "Then, twenty twenty. A pandemic shuts down the world."),
  ("In a single month, your account falls from about $33,800 to $27,500.", "In a single month, your account falls from about thirty three thousand eight hundred dollars, to twenty seven and a half thousand."),
  ("More than $6,000, gone on paper.", "More than six thousand dollars, gone on paper."),
  ("Your stomach drops too.", None),
 ]),
 ("panic", [
  ("This is the moment that splits the timeline again.", None),
  ("In one version, you panic, sell everything in April 2020, and keep saving in cash.", "In one version, you panic, sell everything in April twenty twenty, and keep saving in cash."),
  ("By 2026 you'd have about $40,500. Not bad.", "By twenty twenty six you'd have about forty thousand five hundred dollars. Not bad."),
  ("But compare it to the version of you that did nothing at all.", None),
 ]),
 ("kept", [
  ("That version kept buying. $5 a day, every day.", "That version kept buying. Five dollars a day, every day."),
  ("And it got tested again in 2022, when the account fell from about $52,500 to $43,200.", "And it got tested again in twenty twenty two, when the account fell from about fifty two and a half thousand dollars, to forty three thousand."),
  ("Again, you kept buying.", None),
  ("Every drop meant your $5 bought more shares, on sale.", "Every drop meant your five dollars bought more shares, on sale."),
 ]),
 ("result", [
  ("So. September 2026.", "So. September twenty twenty six."),
  ("Total money you put in: $30,569.", "Total money you put in: thirty thousand, five hundred and sixty nine dollars."),
  ("What it's worth: about $99,000.", "What it's worth: about ninety nine thousand dollars."),
  ("Same coffee money. More than three times bigger.", None),
  ("And that's price growth only, without counting dividends.", None),
 ]),
 ("late", [
  ("Okay, but what if you're starting late?", None),
  ("Start in 2015: about $21,400 in, almost $50,000 now.", "If you'd started in twenty fifteen, you'd have put in about twenty one thousand, and have almost fifty thousand dollars."),
  ("Start in 2020: about $12,300 in, $20,700 now.", "Started in twenty twenty? About twelve thousand in. Twenty thousand seven hundred now."),
  ("Even starting in January 2022, right before a drop: $8,700 became $13,000.", "Even starting in January twenty twenty two, right before a drop, your eight thousand seven hundred would be worth thirteen thousand."),
 ]),
 ("scale", [
  ("And the amount matters less than you think.", None),
  ("Just $1 a day since 2010 would be worth almost $20,000.", "Just one dollar a day since twenty ten would be worth almost twenty thousand dollars."),
  ("$10 a day? Almost $200,000.", "Ten dollars a day? Almost two hundred thousand."),
 ]),
 ("myth", [
  ("Some people call this the latte factor, and they argue it's a myth.", None),
  ("And they have a point. Cutting coffee won't make anyone rich if rent eats half their paycheck.", None),
  ("The coffee was never the point. The point is the habit:", None),
  ("a small, boring amount, moving every month, for a very long time.", None),
 ]),
 ("how", [
  ("So how would timeline B actually work in real life?", None),
  ("First, make it automatic. A transfer on payday, so you never have to decide.", None),
  ("Second, keep it simple and cheap. Broad index funds usually have very low fees.", None),
  ("And third, don't check it every day. The people who did best in this story were the ones who did nothing.", None),
 ]),
 ("honest", [
  ("Now, the honest part. This is not financial advice.", None),
  ("These are real S&P 500 prices, but the past doesn't promise the future.", "These are real S and P five hundred prices, but the past doesn't promise the future."),
  ("There have been long stretches when the market went nowhere.", None),
  ("Invest only money you won't need soon, after an emergency fund, and with no expensive debt.", None),
 ]),
 ("outro", [
  ("So this isn't really about coffee. Enjoy your coffee.", None),
  ("It's about the two timelines every small habit quietly creates.", None),
  ("Which timeline are you in? Tell me in the comments what you'd do with $5 a day.", "Which timeline are you in? Tell me in the comments what you'd do with five dollars a day."),
  ("See you in the other timeline.", None),
 ]),
]
