"""EP11 / Video #1 - Black Friday's Most Expensive Button. Built by engine3d/epbuild.py ep11.
Each sentence: S(sub, spoken, **changes). Scene state carries over from the previous sentence; a dict in `chars`
updates that character only (None hides it). Numbers come from ep11_numbers.py (rounded on screen, user rule)."""

META = {
    "title": "Black Friday's Most Expensive Button",
    "file": "EP11_Black_Friday_Button.mp4",
    "speed": 1.0,          # Piper length_scale = 1/speed
    "music_seed": 2,
}
A, B, RED, AMB, TEAL, GRN = "#ff8a3d", "#38c6b4", "#ff4d5e", "#ffc23a", "#38c6b4", "#4fd17a"

def S(sub, spoken=None, **kw):
    d = dict(kw); d["sub"] = sub; d["spoken"] = spoken if spoken is not None else sub; return d

K = lambda **kw: dict(who="you", **kw)       # Karl (timeline A or default)
KB = lambda **kw: dict(who="you", **kw)      # Karl in timeline B (same look)
CASH = lambda **kw: dict(who="cashier", **kw)

BEATS = [
# ---------------------------------------------------------------- 0:00 END FIRST
("end_first", dict(set="home", bg="#3a2440", chars={"karl": K(x=-1.6, z=0.4, ry=0.5, pose="hold", emo="shock")},
                   props=[{"k": "phone", "on": "karl"}], cam=["close", "karl"], ov=[{"k": "calendar", "mode": "drop", "x": 0.70}]), [
    S("This is Karl.", "This is Karl.", sfx=["boom"]),
    S("It's January, and his whole paycheck is already gone.", sfx=["thunk6"]),
    S("Not to rent. Not to food.", chars={"karl": {"emo": "panic", "pose": "panic", "shake": 1}}),
    S("To six tiny payments of $50.", "To six tiny payments of fifty dollars.", ov=[{"k": "calendar", "mode": "full", "x": 0.70}, {"k": "big", "text": "PAYCHECK GONE", "col": RED, "y": 0.16, "x": 0.70, "size": 90}], sfx=["sad"]),
    S("How did it happen? One button.", chars={"karl": {"emo": "sad", "pose": "slump", "shake": 0}}, ov=[{"k": "title", "text": "6 WEEKS EARLIER", "sub": "BLACK FRIDAY", "at": 0.45}], sfx=["rewind@0.4"]),
]),
# ---------------------------------------------------------------- 0:15 GUESS
("guess", dict(set="store", bg="#24183c", chars={"karl": K(x=0, z=0.5, ry=0, pose="idle", emo="happy", walk=0)}, props=[{"k": "signs"}],
               cam=["wide"], ov=[]), [
    S("Black Friday. 40% off everything.", "Black Friday. Forty percent off everything.", chars={"karl": {"pose": "cheer", "emo": "happy", "hop": 1}}, sfx=["cash"]),
    S("And at every checkout, the same friendly button:", chars={"karl": {"pose": "idle", "hop": 0, "emo": "neutral"}}, cam=["two"],
      props=[{"k": "signs"}, {"k": "button", "x": 1.4, "y": 2.4}]),
    S("\"Pay in 4. Zero interest.\"", "Pay in four. Zero interest.", ov=[{"k": "big", "text": "PAY IN 4", "sub": "0% INTEREST", "col": GRN}], sfx=["ding"]),
    S("Here's your question.", cam=["close", "karl"], chars={"karl": {"emo": "smug", "pose": "point"}}),
    S("By the end of this story, how much did Karl really spend?", ov=[{"k": "title", "text": "HOW MUCH DID KARL", "sub": "REALLY SPEND?"}], sfx=["tick"]),
    S("Guess a number now. Write it down. Keep it.", ov=[{"k": "title", "text": "YOUR GUESS: $____", "sub": "WRITE IT DOWN"}, {"k": "tag", "text": "YOUR GUESS: $____"}], sfx=["boom"]),
]),
# ---------------------------------------------------------------- 0:35 SETUP
("setup", dict(set="street", bg="#2e3a5c", chars={"karl": K(x=-0.6, z=0.3, ry=0.3, pose="hold", emo="happy")}, props=[{"k": "phone", "on": "karl"}],
               cam=["two"], ov=[{"k": "tag", "text": "YOUR GUESS: $____"}]), [
    S("Karl is 26. Normal job, normal paycheck,", "Karl is twenty six. Normal job, normal paycheck,",
      ov=[{"k": "tag", "text": "YOUR GUESS: $____"}, {"k": "facts", "items": ["AGE 26", "$38/HOUR (US AVERAGE)", "ONE CREDIT CARD"], "x": 0.70}]),
    S("one credit card he's proud of not using much.", chars={"karl": {"emo": "smug"}}),
    S("He's not reckless. He has a list:", chars={"karl": {"emo": "neutral", "pose": "idle"}}, cam=["close", "karl"],
      ov=[{"k": "tag", "text": "YOUR GUESS: $____"}, {"k": "list", "title": "KARL'S LIST", "items": ["WINTER JACKET", "GIFT FOR MOM"], "total": "~$400", "x": 0.70}]),
    S("a winter jacket and a gift for his mom. About $400.", "a winter jacket and a gift for his mom. About four hundred dollars."),
    S("That's the plan.", chars={"karl": {"pose": "thumbsup", "emo": "happy"}}),
    S("We're going to watch two versions of Karl walk into the same Black Friday.", set="void", bg="#1d1a33",
      chars={"karl": K(x=-1.5, z=0.3, ry=0.25, pose="idle", emo="neutral", walk=0), "kb": KB(x=1.5, z=0.3, ry=-0.25, pose="idle", emo="neutral")}, props=[],
      cam=["wide"], ov=[{"k": "tag", "text": "YOUR GUESS: $____"}, {"k": "split", "a": "A · FOUR EASY PAYMENTS", "b": "B · FULL PRICE OUT LOUD"}], sfx=["whoosh"]),
    S("Timeline A uses the button.", chars={"karl": {"emo": "happy", "pose": "cheer"}}),
    S("Timeline B uses one strange little habit.", chars={"karl": {"pose": "idle"}, "kb": {"emo": "smug", "pose": "point"}}),
    S("Same guy, same money, same sales.", chars={"karl": {"pose": "shrug"}, "kb": {"pose": "shrug"}}),
]),
# ---------------------------------------------------------------- 1:15 TIMELINE A - FIRST CLICK
("a_click", dict(set="store", bg="#24183c", chars={"karl": K(x=-1.2, z=0.6, ry=0.6, pose="idle", emo="neutral"), "cash": CASH(x=1.3, z=-0.6, ry=-0.5, pose="idle", emo="happy")},
                 props=[{"k": "signs"}, {"k": "counter"}, {"k": "tag", "text": "$200", "x": 0.1, "y": 2.9, "z": -0.2}], cam=["two"],
                 ov=[{"k": "label", "side": "A"}, {"k": "tag", "text": "YOUR GUESS: $____"}]), [
    S("Timeline A. The jacket is $200.", "Timeline A. The jacket is two hundred dollars.", sfx=["whoosh"]),
    S("Too much for one day.", chars={"karl": {"emo": "sad", "pose": "shrug"}}),
    S("But the Cashier leans in.", cam=["close", "cash"], chars={"cash": {"emo": "smug", "pose": "point"}}),
    S("\"Or just $50 today!\"", "Or just fifty today!", voice="cashier", chars={"cash": {"emo": "happy", "pose": "cheer"}},
      props=[{"k": "signs"}, {"k": "counter"}, {"k": "tag", "text": "$200", "to": "4 x $50", "at": 0.2, "x": 0.1, "y": 2.9, "z": -0.2}], sfx=["pop@0.2"]),
    S("Fifty. Fifty is nothing. Fifty is a dinner.", cam=["close", "karl"], chars={"karl": {"emo": "smug", "pose": "idle"}},
      props=[{"k": "signs"}, {"k": "counter"}, {"k": "tag", "text": "4 x $50", "x": 0.1, "y": 2.9, "z": -0.2}]),
    S("Click.", chars={"karl": {"emo": "happy", "pose": "thumbsup"}}, ov=[{"k": "label", "side": "A"}, {"k": "tag", "text": "YOUR GUESS: $____"}, {"k": "counter", "text": "PLANS: 1 · $200"}], sfx=["click", "cash"]),
    S("Here's the trick, and it's not Karl being stupid.", set="void", bg="#2a1f4a", chars={"karl": K(x=0, z=0.3, ry=0, pose="idle", emo="neutral"), "cash": None}, props=[], cam=["two"]),
    S("Your brain doesn't feel $200. It feels $50.", "Your brain doesn't feel two hundred dollars. It feels fifty.",
      ov=[{"k": "label", "side": "A"}, {"k": "tag", "text": "YOUR GUESS: $____"}, {"k": "counter", "text": "PLANS: 1 · $200"}, {"k": "vs", "l": "$200", "op": "FEELS LIKE", "r": "$50", "col": AMB}]),
    S("Splitting a price into four makes paying hurt about four times less.", chars={"karl": {"emo": "happy", "pose": "cheer"}}),
    S("That's not a bug. That's the product.", chars={"karl": {"emo": "shock", "pose": "idle"}}, cam=["close", "karl"], sfx=["boom"]),
    S("Stores pay these apps a fee on every sale, because people who split the price buy more.", cam=["wide"], props=[{"k": "rain"}], chars={"karl": {"emo": "money", "pose": "hold"}}),
    S("One study from the U.S. National Bureau of Economic Research found",
      ov=[{"k": "label", "side": "A"}, {"k": "tag", "text": "YOUR GUESS: $____"}, {"k": "stat", "text": "+$60/WEEK", "sub": "MORE SPENDING AFTER FIRST BNPL USE", "src": "NBER WORKING PAPER 30508 (2022)"}], props=[]),
    S("that after people start using buy now, pay later, their spending goes up and stays up, around $60 a week.",
      "that after people start using buy now, pay later, their spending goes up, and stays up. Around sixty dollars a week.", chars={"karl": {"emo": "sad"}}),
]),
# ---------------------------------------------------------------- 2:30 STACKING
("a_stack", dict(set="store", bg="#24183c", chars={"karl": K(x=-0.8, z=0.6, ry=0.35, pose="hold", emo="happy")},
                 props=[{"k": "signs"}, {"k": "boxes", "n": 1, "x": 1.0, "z": 0.4}], cam=["two"],
                 ov=[{"k": "label", "side": "A"}, {"k": "tag", "text": "YOUR GUESS: $____"}, {"k": "counter", "text": "PLANS: 1 · $200"}]), [
    S("Then the headphones. Fifty today.", props=[{"k": "signs"}, {"k": "boxes", "n": 2, "x": 1.0, "z": 0.4}], ov=[{"k": "label", "side": "A"}, {"k": "tag", "text": "YOUR GUESS: $____"}, {"k": "counter", "text": "PLANS: 2 · $400"}], sfx=["pop", "cash"]),
    S("The sneakers. Fifty today.", cam=["close", "karl"], chars={"karl": {"emo": "smug", "hop": 1}}, props=[{"k": "signs"}, {"k": "boxes", "n": 3, "x": 1.0, "z": 0.4}],
      ov=[{"k": "label", "side": "A"}, {"k": "tag", "text": "YOUR GUESS: $____"}, {"k": "counter", "text": "PLANS: 3 · $600"}], sfx=["pop", "cash"]),
    S("A speaker he didn't know he needed. Fifty today.", cam=["wide"], chars={"karl": {"emo": "happy", "hop": 0, "pose": "cheer"}}, props=[{"k": "signs"}, {"k": "boxes", "n": 4, "x": 1.0, "z": 0.4}],
      ov=[{"k": "label", "side": "A"}, {"k": "tag", "text": "YOUR GUESS: $____"}, {"k": "counter", "text": "PLANS: 4 · $800"}], sfx=["pop", "cash"]),
    S("None of these feel big, because none of them are big. Alone.", chars={"karl": {"pose": "shrug", "emo": "smug"}}),
    S("And here's the sneaky part: each app only sees its own fifty dollars.", cam=["close", "karl"], chars={"karl": {"pose": "idle", "emo": "neutral"}}),
    S("Nobody adds them up. Not the store, not the app, and definitely not Karl at midnight.", cam=["two"], chars={"karl": {"emo": "laugh"}}),
    S("By Cyber Monday, Karl has six plans in four different apps.", props=[{"k": "signs"}, {"k": "boxes", "n": 6, "x": 1.0, "z": 0.4}],
      ov=[{"k": "label", "side": "A"}, {"k": "tag", "text": "YOUR GUESS: $____"}, {"k": "counter", "text": "PLANS: 6 · $1,200"}], chars={"karl": {"pose": "hold", "emo": "happy"}}, sfx=["pop", "pop@0.3", "cash"]),
    S("And he's not unusual.", set="void", bg="#2a1f4a", cam=["two"], props=[{"k": "boxes", "n": 6, "x": 1.0, "z": 0.4}], chars={"karl": {"emo": "neutral", "pose": "idle"}}),
    S("The U.S. Consumer Financial Protection Bureau looked at real borrowers:",
      ov=[{"k": "label", "side": "A"}, {"k": "tag", "text": "YOUR GUESS: $____"}, {"k": "stat", "text": "63%", "sub": "HAD SEVERAL BNPL LOANS AT ONCE", "src": "CFPB REPORT, JAN 2025"}]),
    S("63% had several of these loans open at the same time.", "sixty three percent had several of these loans open at the same time.", sfx=["boom"]),
    S("A third used more than one app.", ov=[{"k": "label", "side": "A"}, {"k": "tag", "text": "YOUR GUESS: $____"}, {"k": "stat", "text": "1 IN 3", "sub": "USED MORE THAN ONE BNPL APP", "src": "CFPB REPORT, JAN 2025"}]),
    S("And it peaks exactly now, during the holidays.", chars={"karl": {"emo": "shock"}}),
    S("Last holiday season Americans put about $20 billion on buy now, pay later online.", "Last holiday season, Americans put about twenty billion dollars on buy now, pay later. Online.",
      ov=[{"k": "label", "side": "A"}, {"k": "tag", "text": "YOUR GUESS: $____"}, {"k": "stat", "text": "$20 BILLION", "sub": "BNPL ONLINE, HOLIDAY SEASON 2025", "src": "ADOBE DIGITAL INSIGHTS"}], props=[{"k": "rain"}, {"k": "boxes", "n": 6, "x": 1.0, "z": 0.4}]),
    S("Remember your guess? Here's the first real number.", props=[{"k": "boxes", "n": 6, "x": 1.0, "z": 0.4}], cam=["close", "karl"],
      ov=[{"k": "label", "side": "A"}, {"k": "title", "text": "REMEMBER YOUR GUESS?", "sub": "FIRST REAL NUMBER"}], sfx=["tick"]),
    S("Six plans of $200.", "Six plans of two hundred.", cam=["wide"], ov=[{"k": "label", "side": "A"}, {"k": "big", "text": "6 x $200", "col": AMB}]),
    S("Karl just spent $1,200.", "Karl just spent one thousand two hundred dollars.", chars={"karl": {"emo": "shock", "pose": "panic"}},
      ov=[{"k": "label", "side": "A"}, {"k": "big", "text": "$1,200", "sub": "ACTUALLY SPENT", "col": RED}], sfx=["boom", "cash"]),
    S("Three times his list.", chars={"karl": {"emo": "sad", "pose": "slump"}}, ov=[{"k": "label", "side": "A"}, {"k": "tag", "text": "STILL THINK $____?"}, {"k": "vs", "l": "$1,200", "op": "VS LIST", "r": "$400", "col": RED}]),
]),
# ---------------------------------------------------------------- 3:45 PRESSURE MACHINE
("pressure", dict(set="store", bg="#3a1630", chars={"karl": K(x=-0.6, z=0.6, ry=0.3, pose="idle", emo="neutral"), "cash": CASH(x=1.4, z=-0.4, ry=-0.5, pose="idle", emo="smug")},
                  props=[{"k": "signs"}, {"k": "counter"}], cam=["wide"],
                  ov=[{"k": "label", "side": "A"}, {"k": "tag", "text": "STILL THINK $____?"}, {"k": "timers"}]), [
    S("And look at everything around that button.", sfx=["tick"]),
    S("A timer. \"Only two left.\" A big green \"zero interest\".", "A timer. Only two left. A big green, zero interest.", chars={"karl": {"emo": "shock"}, "cash": {"pose": "point"}}, cam=["two"], sfx=["ding", "ding@0.4"]),
    S("All of it is built to make you decide in seconds, not days.", chars={"karl": {"emo": "panic", "shake": 1}}),
    S("Now the two myths Karl believes.", set="void", bg="#2a1f4a", chars={"karl": {"emo": "neutral", "shake": 0, "x": 0, "ry": 0}, "cash": None}, props=[], cam=["two"],
      ov=[{"k": "label", "side": "A"}, {"k": "tag", "text": "STILL THINK $____?"}]),
    S("Myth one: \"It's interest-free, so it's free.\"", "Myth one. It's interest free, so it's free.", ov=[{"k": "label", "side": "A"}, {"k": "myth", "n": 1, "text": "\"INTEREST-FREE = FREE\""}], chars={"karl": {"emo": "smug", "pose": "thumbsup"}}),
    S("It's free only if every single payment is on time, and only if you would have bought it anyway.", ov=[{"k": "label", "side": "A"}, {"k": "myth", "n": 1, "text": "\"INTEREST-FREE = FREE\"", "busted": 1}], chars={"karl": {"emo": "shock", "pose": "idle"}}, sfx=["buzz"]),
    S("40% off something you didn't plan to buy isn't a saving. It's 60% spent.", "Forty percent off something you didn't plan to buy isn't a saving. It's sixty percent spent.",
      ov=[{"k": "label", "side": "A"}, {"k": "vs", "l": "-40%", "op": "REALLY MEANS", "r": "60% SPENT", "col": RED}]),
    S("Myth two: \"It's not real debt.\"", "Myth two. It's not real debt.", ov=[{"k": "label", "side": "A"}, {"k": "myth", "n": 2, "text": "\"IT'S NOT REAL DEBT\""}], chars={"karl": {"emo": "smug", "pose": "shrug"}}),
    S("It is a loan.", ov=[{"k": "label", "side": "A"}, {"k": "myth", "n": 2, "text": "\"IT'S NOT REAL DEBT\"", "busted": 1}], sfx=["buzz"], chars={"karl": {"emo": "shock", "pose": "idle"}}),
    S("And for years most of these loans didn't even show up on credit reports.", cam=["close", "karl"]),
    S("Which means nobody saw the full stack.", props=[{"k": "boxes", "n": 6, "x": 1.1, "z": 0.4}], cam=["wide"]),
    S("Not the banks, not the apps. Not even Karl.", chars={"karl": {"emo": "sad", "pose": "facepalm"}}, sfx=["thud"]),
]),
# ---------------------------------------------------------------- 4:30 TIMELINE B
("b_store", dict(set="store", bg="#123a3a", chars={"karl": K(x=-1.2, z=0.6, ry=0.6, pose="idle", emo="neutral"), "cash": CASH(x=1.3, z=-0.6, ry=-0.5, pose="cheer", emo="happy")},
                 props=[{"k": "signs"}, {"k": "counter"}, {"k": "tag", "text": "4 x $50", "x": 0.1, "y": 2.9, "z": -0.2}], cam=["two"],
                 ov=[{"k": "label", "side": "B"}, {"k": "tag", "text": "STILL THINK $____?"}]), [
    S("Timeline B. Same jacket, same Cashier, same button.", sfx=["whoosh"]),
    S("\"Or just $50 today!\"", "Or just fifty today!", voice="cashier"),
    S("But this Karl has one rule.", cam=["close", "karl"], chars={"karl": {"emo": "smug", "pose": "point"}}),
    S("Before he pays, he says the full price out loud.", ov=[{"k": "label", "side": "B"}, {"k": "tag", "text": "STILL THINK $____?"}, {"k": "title", "text": "RULE: SAY THE FULL PRICE", "sub": "OUT LOUD", "col": TEAL}]),
    S("\"Two hundred dollars.\"", "Two hundred dollars.", voice="karl", props=[{"k": "signs"}, {"k": "counter"}, {"k": "tag", "text": "4 x $50", "to": "$200", "at": 0.1, "x": 0.1, "y": 2.9, "z": -0.2}],
      chars={"karl": {"emo": "neutral", "pose": "idle"}}, sfx=["pop@0.1"]),
    S("It sounds silly. It works, because now his brain hears the real number.", cam=["two"], chars={"cash": {"emo": "shock", "pose": "idle"}}),
    S("Then a second question: would I pay $200 in cash, today?", "Then a second question. Would I pay two hundred in cash, today?",
      ov=[{"k": "label", "side": "B"}, {"k": "tag", "text": "STILL THINK $____?"}, {"k": "title", "text": "WOULD I PAY $200", "sub": "IN CASH, TODAY?", "col": TEAL}]),
    S("For the jacket, yes. He planned it.", chars={"karl": {"emo": "happy", "pose": "thumbsup"}}),
    S("He pays with his debit card. Done.", sfx=["cash"], props=[{"k": "signs"}, {"k": "counter"}, {"k": "boxes", "n": 1, "x": -2.1, "z": 0.6}]),
    S("For the headphones he says it out loud: \"$199.\"", "For the headphones, he says it out loud. One hundred ninety nine dollars.", cam=["close", "karl"],
      chars={"karl": {"emo": "neutral", "pose": "hold"}}, props=[{"k": "signs"}, {"k": "counter"}, {"k": "phone", "on": "karl"}, {"k": "boxes", "n": 1, "x": -2.1, "z": 0.6}]),
    S("He hears how it sounds.", chars={"karl": {"emo": "shock"}}),
    S("So he leaves them in the cart for 48 hours.", "So he leaves them in the cart for forty eight hours.", chars={"karl": {"emo": "smug", "pose": "no"}},
      ov=[{"k": "label", "side": "B"}, {"k": "tag", "text": "STILL THINK $____?"}, {"k": "title", "text": "48-HOUR CART", "col": TEAL}], sfx=["click"]),
    S("Black Friday prices aren't the last sale of the year. Most of them come back before Christmas.", cam=["wide"]),
    S("Two days later, he doesn't even remember them.", chars={"karl": {"emo": "happy", "pose": "shrug"}}),
    S("Timeline B spends $400. The list. Nothing else.", "Timeline B spends four hundred dollars. The list. Nothing else.", set="void", bg="#1d1a33",
      chars={"karl": K(x=-1.8, z=0.3, ry=0.25, pose="slump", emo="sad"), "kb": KB(x=1.8, z=0.3, ry=-0.25, pose="thumbsup", emo="happy"), "cash": None},
      props=[{"k": "boxes", "n": 6, "x": -0.4, "z": 0.3}, {"k": "boxes", "n": 2, "x": 3.2, "z": 0.3}], cam=["wide"],
      ov=[{"k": "split", "a": "A · $1,200", "b": "B · $400"}, {"k": "tag", "text": "STILL THINK $____?"}], sfx=["whoosh"]),
]),
# ---------------------------------------------------------------- 5:30 HOURS OF LIFE
("hours", dict(set="void", bg="#2a1f4a", chars={"karl": K(x=-2.2, z=0.3, ry=0.4, pose="idle", emo="neutral")}, props=[], cam=["two"],
               ov=[{"k": "tag", "text": "STILL THINK $____?"}]), [
    S("Let's translate this into something money hides: time.", "Let's translate this into something money hides. Time.", sfx=["tick"]),
    S("The average American earns about $38 an hour before tax.", "The average American earns about thirty eight dollars an hour, before tax.",
      ov=[{"k": "tag", "text": "STILL THINK $____?"}, {"k": "stat", "text": "$38/HOUR", "sub": "AVERAGE US HOURLY PAY, BEFORE TAX", "src": "BLS VIA FRED, OCT 2026", "x": 0.62}]),
    S("So Timeline A's $1,200 is about 32 hours of work.", "So Timeline A's twelve hundred dollars is about thirty two hours of work.",
      ov=[{"k": "tag", "text": "STILL THINK $____?"}, {"k": "hours", "hours": 32, "col": RED, "x": 0.62}], chars={"karl": {"emo": "shock"}}, sfx=["tick"]),
    S("Four full days of Karl's life, for things he mostly didn't plan to buy.", chars={"karl": {"emo": "sad", "pose": "slump"}}),
    S("Timeline B's extra, the stuff he didn't buy, is $800.", "Timeline B's extra, the stuff he didn't buy, is eight hundred dollars.",
      chars={"karl": {"emo": "happy", "pose": "thumbsup"}}, ov=[{"k": "label", "side": "B"}, {"k": "tag", "text": "STILL THINK $____?"}, {"k": "hours", "hours": 21, "col": TEAL, "x": 0.62}]),
    S("21 hours he gets to keep.", "Twenty one hours he gets to keep.", sfx=["ding"]),
]),
# ---------------------------------------------------------------- 6:15 TIMELINE A - DECEMBER
("a_december", dict(set="home", bg="#3a2440", chars={"karl": K(x=-1.6, z=0.4, ry=0.5, pose="hold", emo="neutral")}, props=[{"k": "phone", "on": "karl"}, {"k": "boxes", "n": 6, "x": -3.2, "z": -0.8}],
                    cam=["two"], ov=[{"k": "label", "side": "A"}, {"k": "tag", "text": "STILL THINK $____?"}, {"k": "calendar", "mode": "dec", "x": 0.68}]), [
    S("Back to Timeline A.", sfx=["whoosh"]),
    S("Every two weeks, six payments land on the same days. $300.", "Every two weeks, six payments land on the same days. Three hundred dollars.", sfx=["thunk6"]),
    S("On December 11th.", "On December eleventh.", caln=1, chars={"karl": {"emo": "shock"}}),
    S("On Christmas day.", caln=2, chars={"karl": {"emo": "sad"}}),
    S("On January 8th, the same week as rent.", "On January eighth. The same week as rent.", caln=3, chars={"karl": {"emo": "panic", "pose": "panic"}}, sfx=["boom"]),
    S("And Karl is not the only one struggling.", chars={"karl": {"emo": "sad", "pose": "hold"}}),
    S("In a LendingTree survey, 41% of people who use these loans paid late at least once in a year.", "In a LendingTree survey, forty one percent of people who use these loans paid late at least once in a year.",
      ov=[{"k": "label", "side": "A"}, {"k": "tag", "text": "STILL THINK $____?"}, {"k": "stat", "text": "41%", "sub": "OF BNPL USERS PAID LATE IN A YEAR", "src": "LENDINGTREE SURVEY, 2025", "x": 0.66}]),
    S("The latest version says 47.", "The latest version says forty seven.", ov=[{"k": "label", "side": "A"}, {"k": "tag", "text": "STILL THINK $____?"}, {"k": "stat", "text": "47%", "sub": "LATEST UPDATE", "src": "LENDINGTREE, 2026", "x": 0.66}], sfx=["boom"]),
    S("Late fees are up to $7 or $8 a time, and a missed payment can freeze the app.", "Late fees are up to seven or eight dollars a time. And a missed payment can freeze the app.",
      ov=[{"k": "label", "side": "A"}, {"k": "tag", "text": "STILL THINK $____?"}, {"k": "stat", "text": "UP TO $8", "sub": "LATE FEE (KLARNA $7, AFTERPAY $8)", "src": "PROVIDER TERMS, US", "x": 0.66}]),
    S("And some providers have started reporting these loans to credit bureaus, so a late payment can follow you.", chars={"karl": {"emo": "shock", "pose": "idle"}}),
    S("Karl has three hundred dollars due, rent next to it, and a paycheck that doesn't stretch.", chars={"karl": {"emo": "sad", "pose": "slump"}}),
    S("So Karl does what feels smart.", cam=["close", "karl"], chars={"karl": {"emo": "smug", "pose": "point"}}),
]),
# ---------------------------------------------------------------- 7:00 TIMELINE B - JANUARY
("b_january", dict(set="home", bg="#123a3a", chars={"karl": K(x=-1.2, z=0.4, ry=0.4, pose="hold", emo="happy")}, props=[{"k": "cup", "on": "karl"}, {"k": "boxes", "n": 2, "x": -3.0, "z": -0.8}],
                   cam=["two"], ov=[{"k": "label", "side": "B"}, {"k": "calendar", "mode": "rent", "x": 0.68}]), [
    S("Meanwhile, Timeline B. January 8th. Rent. That's it.", "Meanwhile, Timeline B. January eighth. Rent. That's it.", sfx=["whoosh", "ding@0.6"]),
    S("No bubbles, no buzzing apps.", chars={"karl": {"emo": "neutral"}}),
    S("Honestly, it's a boring January.", chars={"karl": {"emo": "smug", "pose": "shrug"}}),
    S("Karl B didn't get the speaker or the gaming chair, and for about two days he felt like he lost Black Friday.", chars={"karl": {"emo": "sad", "pose": "hold"}}),
    S("But his paycheck is his again.", chars={"karl": {"emo": "happy", "pose": "cheer"}}, sfx=["cash"]),
    S("And the $800 he didn't spend is still sitting there, waiting for a decision.", "And the eight hundred dollars he didn't spend is still sitting there, waiting for a decision.",
      props=[{"k": "jar", "x": 0.2, "y": 1.3, "z": 0.6}, {"k": "boxes", "n": 2, "x": -3.0, "z": -0.8}], chars={"karl": {"pose": "idle", "emo": "happy"}}, cam=["two"],
      ov=[{"k": "label", "side": "B"}, {"k": "tag", "text": "YOUR GUESS: still $____?"}, {"k": "big", "text": "$800", "sub": "NOT SPENT", "col": TEAL, "x": 0.70}]),
]),
# ---------------------------------------------------------------- 7:30 TWIST
("twist", dict(set="home", bg="#3a2440", chars={"karl": K(x=-1.6, z=0.4, ry=0.5, pose="hold", emo="smug")}, props=[{"k": "phone", "on": "karl"}, {"k": "card", "on": "karl"}],
               cam=["close", "karl"], ov=[{"k": "label", "side": "A"}, {"k": "tag", "text": "STILL THINK $____?"}, {"k": "paywith", "x": 0.68}]), [
    S("He pays each $50 payment with his credit card.", "He pays each fifty dollar payment, with his credit card.", sfx=["click"]),
    S("No late fees, no freezes. Problem solved, right?", chars={"karl": {"emo": "happy", "pose": "thumbsup"}}, sfx=["ding"]),
    S("Here's the twist.", chars={"karl": {"emo": "neutral", "pose": "idle"}}, ov=[{"k": "label", "side": "A"}, {"k": "title", "text": "THE TWIST", "col": RED}], sfx=["boom", "musicstop"]),
    S("The zero-interest loan just moved onto a card that charges about 21% a year.", "The zero interest loan just moved onto a card that charges about twenty one percent a year.",
      ov=[{"k": "label", "side": "A"}, {"k": "stamp", "text": "21% APR", "col": RED}], chars={"karl": {"emo": "shock", "pose": "panic"}}, sfx=["stamp"]),
    S("That's the U.S. average on cards that pay interest, August 2026.", "That's the U.S. average on cards that pay interest. August, twenty twenty six.",
      ov=[{"k": "label", "side": "A"}, {"k": "stat", "text": "21%", "sub": "AVG APR, ACCOUNTS PAYING INTEREST", "src": "FEDERAL RESERVE VIA FRED, AUG 2026", "x": 0.68}]),
    S("By January, the whole $1,200 is sitting on that card.", "By January, the whole twelve hundred dollars is sitting on that card.",
      ov=[{"k": "label", "side": "A"}, {"k": "big", "text": "$1,200", "sub": "ON THE CREDIT CARD", "col": RED, "x": 0.68}], chars={"karl": {"emo": "sad", "pose": "slump"}}),
    S("And Karl pays the minimum, because the minimum is what the app suggests.", ov=[{"k": "label", "side": "A"}, {"k": "paywith", "mode": "min", "x": 0.68}], chars={"karl": {"emo": "neutral", "pose": "hold"}}),
    S("His first minimum payment is only about $33. Sounds harmless.", "His first minimum payment is only about thirty three dollars. Sounds harmless.", chars={"karl": {"emo": "happy"}}),
    S("But about two thirds of that $33 is just interest. The debt barely moves.", "But about two thirds of those thirty three dollars is just interest. The debt barely moves.",
      ov=[{"k": "label", "side": "A"}, {"k": "vs", "l": "~$21", "op": "OF $33 IS", "r": "INTEREST", "col": RED}], chars={"karl": {"emo": "shock", "pose": "panic"}}, sfx=["buzz"]),
]),
# ---------------------------------------------------------------- 8:05 REVEAL
("reveal", dict(set="void", bg="#2a1630", chars={"karl": K(x=-3.6, z=0.3, ry=0.35, pose="idle", emo="neutral")}, props=[], cam=["two"],
                ov=[{"k": "label", "side": "A"}, {"k": "tag", "text": "YOUR GUESS: $____"}, {"k": "chart", "x": 0.6}]), [
    S("So, your guess. How much did Karl really spend?", ov=[{"k": "label", "side": "A"}, {"k": "tag", "text": "YOUR GUESS: $____"}, {"k": "chart", "x": 0.6, "at": 0.95}, {"k": "title", "text": "YOUR GUESS?", "sub": "HOW MUCH DID KARL REALLY SPEND?"}], sfx=["tick"]),
    S("At the minimum payment, it takes him about 7 years to clear the card.", "At the minimum payment, it takes him about seven years to clear the card.", sfx=["whoosh"]),
    S("Seven years. For a Black Friday.", chars={"karl": {"emo": "shock", "pose": "panic"}}, sfx=["boom"]),
    S("He pays about $1,070 in interest.", "He pays about one thousand and seventy dollars, in interest.", ov=[{"k": "label", "side": "A"}, {"k": "chart", "x": 0.6, "show": "interest"}]),
    S("Total: about $2,270.", "Total. About two thousand, two hundred seventy dollars.", props=[{"k": "receipt", "x": 0.6, "z": -0.6}], set="void", cam=["wide"],
      ov=[{"k": "label", "side": "A"}, {"k": "big", "text": "$2,270", "sub": "WHAT KARL REALLY SPENT", "col": RED}], chars={"karl": {"x": -2.2, "emo": "panic"}}, sfx=["boom", "cash"]),
    S("And remember the full price, before the 40% off? $2,000.", "And remember the full price, before the forty percent off? Two thousand.",
      ov=[{"k": "label", "side": "A"}, {"k": "vs", "l": "$2,270", "op": "IS MORE THAN", "r": "$2,000", "sub": "-40% SALE  vs  FULL PRICE", "col": RED}]),
    S("Karl paid more than full price for a sale.", chars={"karl": {"emo": "sad", "pose": "facepalm"}}, sfx=["thud"]),
    S("And Timeline B?", set="void", bg="#123a3a", props=[{"k": "jar", "x": 0.9, "y": 1.2, "z": 0.4}], chars={"karl": {"x": -0.9, "emo": "happy", "pose": "thumbsup"}}, cam=["two"],
      ov=[{"k": "label", "side": "B"}]),
    S("If he had put those $800 into the S&P 500 ten years ago, they'd be worth about $2,850 today.", "If he had put those eight hundred unspent dollars into the S and P five hundred ten years ago, they'd be worth about two thousand eight hundred fifty today.",
      ov=[{"k": "label", "side": "B"}, {"k": "big", "text": "~$2,850", "sub": "$800 IN S&P 500, SEP 2016 TO SEP 2026", "col": TEAL, "x": 0.66}], props=[{"k": "rain"}, {"k": "jar", "x": 0.9, "y": 1.2, "z": 0.4}], sfx=["cash"]),
    S("That's history, not a promise.", ov=[{"k": "label", "side": "B"}, {"k": "title", "text": "HISTORY, NOT A PROMISE", "col": "#ffffff"}], props=[{"k": "jar", "x": 0.9, "y": 1.2, "z": 0.4}]),
    S("But the gap is real: one Karl has a seven-year receipt, the other has money.", "But the gap is real. One Karl has a seven year receipt. The other has money.",
      chars={"karl": K(x=-1.8, z=0.3, ry=0.25, pose="slump", emo="sad"), "kb": KB(x=1.8, z=0.3, ry=-0.25, pose="cheer", emo="money")},
      props=[{"k": "receipt", "x": -0.4, "z": -0.6}, {"k": "jar", "x": 3.0, "y": 1.2, "z": 0.4}], cam=["wide"], bg="#1d1a33",
      ov=[{"k": "split", "a": "A · ~$2,270 PAID", "b": "B · ~$2,850 GROWN"}]),
]),
# ---------------------------------------------------------------- 8:45 HONEST PART + RULES
("rules", dict(set="void", bg="#123a3a", chars={"karl": K(x=-2.3, z=0.3, ry=0.35, pose="idle", emo="neutral"), "kb": None}, props=[], cam=["two"], ov=[]), [
    S("To be fair: buy now, pay later is not evil.", "To be fair. Buy now, pay later is not evil.", sfx=["whoosh"]),
    S("If you pay every installment on time, from money you already have, for something you'd buy anyway, it really is zero interest.", chars={"karl": {"emo": "happy", "pose": "thumbsup"}}),
    S("Some people use it well. The trap is the stack, and the card behind it.", chars={"karl": {"emo": "neutral", "pose": "shrug"}}),
    S("And the trap is designed for exactly the moment you're tired, it's late, and the timer says nine minutes.", ov=[{"k": "timers"}], chars={"karl": {"emo": "sad", "pose": "slump"}}),
    S("So three rules. Simple enough to remember at the checkout.", ov=[{"k": "cards", "n": 0, "x": 0.62}], chars={"karl": {"emo": "smug", "pose": "point"}}),
    S("Rule one: say the full price out loud. If you wouldn't pay it in cash today, don't split it.", "Rule one. Say the full price out loud. If you wouldn't pay it in cash today, don't split it.",
      ov=[{"k": "cards", "n": 1, "x": 0.62}], sfx=["ding"]),
    S("Rule two: one plan at a time. Never for groceries or bills.", "Rule two. One plan at a time. Never for groceries or bills.", ov=[{"k": "cards", "n": 2, "x": 0.62}], sfx=["ding"]),
    S("If you need a second plan, you can't afford the first.", chars={"karl": {"emo": "shock", "pose": "idle"}}),
    S("Rule three: never pay a buy-now-pay-later loan with a credit card.", "Rule three. Never pay a buy now, pay later loan, with a credit card.", ov=[{"k": "cards", "n": 3, "x": 0.62}], sfx=["ding"], chars={"karl": {"emo": "smug", "pose": "no"}}),
    S("And if you already have a stack, don't panic. Three steps, tonight.", chars={"karl": {"emo": "neutral", "pose": "hold"}}, ov=[{"k": "cards", "n": 3, "x": 0.62}, {"k": "note", "text": "ALREADY STACKED? 3 STEPS"}]),
    S("One: open every app and write every date and amount in one calendar. See the real total.", ov=[{"k": "note", "text": "1. ALL DATES IN ONE CALENDAR"}]),
    S("Two: pay the smallest plan off first, so the number of payments shrinks fast.", ov=[{"k": "note", "text": "2. SMALLEST PLAN FIRST"}]),
    S("Three: no new plans until the list is empty. Delete the apps if you have to.", ov=[{"k": "note", "text": "3. NO NEW PLANS"}], chars={"karl": {"emo": "smug", "pose": "thumbsup"}}),
    S("This is education, not financial advice.", ov=[{"k": "cards", "n": 3, "x": 0.62}, {"k": "note", "text": "EDUCATION, NOT FINANCIAL ADVICE"}]),
]),
# ---------------------------------------------------------------- 9:40 QUESTION
("question", dict(set="home", bg="#123a3a", chars={"karl": K(x=-1.4, z=0.4, ry=0.4, pose="hold", emo="happy")}, props=[{"k": "cup", "on": "karl"}],
                  cam=["two"], ov=[{"k": "calendar", "mode": "rent", "x": 0.68}]), [
    S("So, did you guess right?", sfx=["tick"]),
    S("Was your number closer to $1,200, or to $2,270? Tell me in the comments.", "Was your number closer to twelve hundred, or to twenty two seventy? Tell me in the comments.",
      ov=[{"k": "vs", "l": "$1,200", "op": "OR", "r": "$2,270", "sub": "COMMENT YOUR GUESS", "col": AMB}], chars={"karl": {"emo": "smug", "pose": "point"}}),
    S("And how many of these plans do you have open right now? Be honest.", chars={"karl": {"emo": "wink", "pose": "shrug"}}, ov=[{"k": "title", "text": "HOW MANY PLANS", "sub": "DO YOU HAVE OPEN?"}]),
]),
]

END = {"seconds": 15, "text": "WATCH NEXT", "sub": "SUBSCRIBE FOR MORE WHAT-IFS"}

# calendar data (rounded): 6 plans x $50 every 2 weeks; BNPL "pay in 4" = 1 at checkout + 3 (Dec 11, Dec 25, Jan 8)
CAL = {"jan_day": 8, "bubbles": 6, "amount": "$50", "rent": "RENT", "balance": "PAYCHECK GONE"}
CHART = {"months": 87, "total": "~$2,270", "interest": "~$1,070", "years": "~7 YEARS"}

THUMBS = [
    {"name": "A", "big": "$1,200", "small": "$50", "face": "shock", "words": "\"ONLY $50\""},
    {"name": "B", "big": "$2,270", "small": "-40%", "face": "panic", "words": "MORE THAN FULL PRICE"},
    {"name": "C", "big": "7 YEARS", "small": "PAY IN 4", "face": "sad", "words": "FOR A BLACK FRIDAY"},
]

SHORTS = [
    {"name": "twist", "head": ("-40% COST HIM", "MORE THAN FULL PRICE"),
     "segs": [("He pays each $50 payment", "And Karl pays the minimum"), ("At the minimum payment", "Karl paid more than full price")]},
    {"name": "guess", "head": ("\"ONLY $50\"...", "HOW MUCH DID HE SPEND?"),
     "segs": [("Then the headphones", "None of these feel big"), ("Remember your guess?", "Three times his list.")]},
]
