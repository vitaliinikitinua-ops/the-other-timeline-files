---
name: youtube-skill-1
description: "YouTube Skill №1" - the visual + story style learned frame by frame from viral 2D "What If You Had 500 Charisma?" (IFNation-style channel, ~1.5M views, 9:29). Use when the user asks to make a video "in this style", "як у тих відео на 1.5 млн", "YouTube Skill 1", or when planning the look, pacing, narration, characters, effects or titles of a new The Other Timeline video that should copy this viral format. Analysis only - production uses the studio skills.
---

# YouTube Skill №1 — the viral 2D "What If You Had X?" style (learned 28.11.2026)

Source studied: "What If You Had 500 Charisma?" (9:29, 30 fps, 16:9). Every frame was viewed at 1 fps (569 frames,
contact sheets in `research/yt1/v1/sheets/`), plus 6 fps motion strips (`motion_*.jpg`), cut detection, a colour
palette by k-means and the full narration transcript (`research/yt1/v1/transcript.txt`, Whisper). Numbers below are
measured from the video, not guessed. When more videos from this channel are analysed, add them as v2, v3... and
mark which rules repeat (= channel formula) and which were one-offs.


> **CORRECTION 28.11.2026 (full-res frame check, `research/yt1/close_sheet.jpg`):** the characters are NOT 2D vector
> puppets. They are **3D models rendered with a toon/cel shader**: real perspective cameras, soft 2-tone shading on
> hoodies and limbs, a light-grey inverted-hull OUTLINE around the black sphere heads, glossy specular dots, capsule
> arms/legs with ball hands, depth-of-field blur on foreground heads, 3D crowds of instanced characters. Backgrounds are
> simple 3D sets with flat painted textures. Reproduce with a 3D engine (three.js MeshToonMaterial + outline pass + DOF),
> not with flat 2D canvas drawing. Wherever this file says "2D/flat vector", read "3D toon-shaded".

## 1. The formula in one paragraph
A second-person story ("You throw the dodgeball...") about ONE ordinary kid who gets ONE exaggerated stat
("500 charisma" when "most people have about 10"). It starts mid-scene with a small everyday disaster, shows the
power solving it in a funny way, ESCALATES through life (home, school, town, mayor, governor, NBA, President), then
the power quietly turns dark (people can't say no, friend gets hurt, nobody likes you by choice), the hero gives the
power away in a public climax, and the ending mirrors the opening with everything back to normal — and better.
Two real psychology facts are slipped in as "breathers". Ends with the question "So would you want 500 charisma?".

## 2. Title and packaging
- Title pattern: **"What If You Had 500 Charisma?"** = "What If You Had" + ABSURD NUMBER + ONE everyday trait/stat.
  Game-stat language (charisma, luck, IQ, strength, speed...) makes it instantly clear and "RPG-like"; the number is
  50x normal (normal is stated in the video: "about 10"). 32 characters, no clickbait words, no emojis, a question.
- For our money channel the equivalent: "What If You Had 500 Luck?", "What If You Had $1,000,000 Credit Score?"-type
  is wrong; keep ONE stat + absurd number + "You": "What If You Never Paid Interest?", "What If You Had 1,000 Patience?".
- Promise of the title is delivered in the first 45 s (the stat line comes at 0:44: "Most people have about 10
  charisma. You have 500.").

## 3. Story structure (timestamps from the source, 9:29 total)
| Time | Beat | What happens | Purpose |
|---|---|---|---|
| 0:00-0:43 | COLD OPEN mini-story | dodgeball through the gym window -> detention -> one question about the principal's goldfish -> no detention + vending-machine keys | proves the power BEFORE naming it; a complete joke with payoff |
| 0:44-0:49 | THE STAT | "Most people have about 10 charisma. You have 500." + game UI bars over heads | title promise |
| 0:50-1:52 | "At first, it's amazing" | rapid list of small wins, 1 per 3-6 s: dog, open-book quiz, bully returns hat (+ carries backpack forever), lunch lady pizza corner, sister's remote, grandma stops pinching cheeks; plants "Priya - you're saving that one" | fun + plants callbacks for the ending |
| 1:53-2:46 | "Then it gets bigger" | science fact (first impression in 1/10 s) -> mom's raise -> mayor -> skate park with your name -> governor's helicopter ("For about four seconds") -> courtside NBA, miss the shot, 19,000 cheer anyway | escalation ladder, each step one sentence |
| 2:47-3:01 | THE HOOK FOR THE ENDING | White House envelope: the President wants to meet you in April | sets the climax date |
| 3:02-4:32 | THE TURN | "But nobody can say no to you. Not even when they want to." Lady gives her ring with wet eyes, grandma sits on her hands, Priya "I don't know why I said yes", best friend laughs at bad jokes, throws his comic away, mom: "I can't say no to him. I don't know what's wrong with me." | the cost, told through the SAME characters from the fun part |
| 4:33-5:29 | TESTING + DISASTER | shoes, bus to the beach (40 kids miss school), psychology fact (pickle study), "Bet you won't jump." -> broken arm -> "Best day ever." | darkest point |
| 5:30-7:04 | WITHDRAWAL | stops asking for anything (walks around the table for salt), news crew -> lunch ladies fired, essays all get A, 200 people at birthday; "you can't name one person who'd still like you if they had a choice" | emotional low, slower edit |
| 7:05-8:07 | CLIMAX | White House, 30,000 people, President: "name it" -> "Don't do anything just because I asked. Ever. And don't like me unless you actually do." -> everyone says yes -> power gone, "Who invited this kid?" -> one clap: the friend slapping his cast | the reversal uses the power to destroy itself |
| 8:08-9:15 | MIRROR ENDING | every early win is reversed one by one (detention slip for the window, Dex takes the hat, Ruby takes the remote, grandma pinches), "The dog stays though", friend draws comic again, "Not funny." Priya: "Maybe Friday." + second psychology fact | callbacks = satisfying closure |
| 9:16-9:28 | QUESTION + CTA | "So would you want 500 charisma?" + sponsor CTA | comments |

Rules taken from this:
- 25-30 distinct mini-scenes. Every planted detail comes back (window, hat, remote, cheeks, pizza, dog, comic, Priya).
- The middle turn is announced by a one-line pivot sentence ("Then it gets bigger." / "But nobody can say no to you.").
- Real-world facts are SHORT (1-3 sentences: "Psychologists found...", "Scientists found...") and never more than
  2-3 per video; they explain the fantasy, they are not the topic.
- Ending reverses the opening scene exactly (same principal, same slip, same desk angle).

## 4. Narration (voice track)
- ONE narrator, second person, PRESENT tense, calm and dry, almost deadpan; the joke is in the facts, not the tone.
- 1,788 words in 9:16 of speech = **~193 words/min** (faster than our Piper 1.0 at ~170). Short sentences, often
  4-8 words. Many one-word or fragment lines: "He lets you." / "For about four seconds." / "Ever." / "No."
- Dialogue is quoted INSIDE the narration in the same voice ("Nobody ever asks about Gerald.", "Who invited this kid?").
- Specific, concrete, funny details beat adjectives: "the corner piece of pizza. The one with the most cheese",
  "a sign with your name on it", "his cast covered in signatures".
- Rule of three + time jumps: "Ten minutes later... Twenty minutes later... By the bell...", "By Friday", "By Monday".
- Pauses: only ~5 silences longer than 0.25 s in 9.5 min -> the voice runs almost continuously; music and SFX sit low.

## 5. Visual style
### Characters (all 2D, flat vector, "puppet" rig)
- HEAD: a perfect circle filled near-black (#1c1a22..#2a2630) with a soft radial sheen/highlight top-left (looks
  slightly 3D, not flat black). Head is big: ~40% of total character height. No outline needed.
- EYES: two white circles with thin dark outline, touching or almost touching, set slightly above head centre and
  offset toward the look direction; black round pupils that move (look up = dazed, sideways = suspicious). Eyelids
  as flat lids for sleepy/smug. Tears = blue teardrops; crying = wavy shut eyes.
- MOUTH: tiny — a short curve smile, small open "o" (shock), red open mouth for laughs; pink BLUSH ovals on cheeks
  for happy/charmed. Brows only on strong emotions.
- BODY: a clothing shape only (hoodie, blazer, cardigan, dress) — rounded trapezoid torso with seams/drawstrings,
  hood behind the neck. ARMS and LEGS are thin dark sticks (~1/12 of head width) ending in small black ball hands;
  legs in dark pants/stick legs with small white sneakers. Whole character is ~3 heads tall.
- IDENTITY = colour of top + hat/hair silhouette. Hero: mustard-yellow hoodie (#e5b52a) with white drawstrings; at
  0:00 bare head, from 1:17 a blue baseball cap (continuity prop: he got the hat back). Girls: brown hair shape
  framing the face (behind the head + side bangs) and pink/teal tops; grandma: grey bun + purple cardigan; adults in
  suits; principal: grey bun, maroon blazer. Crowds = same rig, random tops and hair, at 30-100 per frame.
- Animals and props are flat cartoon objects with soft shading (dog, goldfish, bus, helicopter).

### Backgrounds and colour
- Painted flat illustrations with soft gradients, no outlines, subtle paper/noise texture, gentle vignette, warm
  window light with bloom. Every location is a real-world place a kid knows: gym, principal's office, hallway with
  lockers, classroom, cafeteria, kitchen, living room, bedroom, bus, street, festival, stadium, White House lawn.
- Palette is MUTED and creamy (measured k-means, share of pixels): #d0c5b7 11% · #b8ab9b 10% · #969188 9% ·
  #757a71 8% · #e0ded7 8% · #5b565d 6% · #47373a 6% · #8fa2b9 6% · #a3785a 6% · #221e2b 5% (heads) · #7c5340 5% ·
  #b4c1ce 5% · #5a7fb2 5% (locker blue) · #363c5f 5% · #4c608a 4% · #cea441 2% (hero yellow, the brightest accent).
  Saturated colour is reserved for the hero, props that matter (red fire alarm, yellow bus) and effects (gold glow).
- MOOD GRADING: the whole frame is colour-graded per act — warm sunset orange at the festival (2:12), purple tint at
  the creepy birthday party (6:31-6:53), cold grey-blue desaturation when the power disappears (7:48-8:07), darker
  dusk kitchen in the withdrawal act (5:36-5:48). Normal scenes are neutral warm cream.

### Composition and camera
- 16:9, mostly eye-level side views like a stage; characters stand on a floor line at ~75-85% of frame height.
- Shot ladder for every mini-scene: ESTABLISHING wide (location, tiny characters) -> MEDIUM two-shot -> CLOSE-UP of
  a face reacting -> INSERT of an object. Inserts are drawn as top-down close-ups on a wooden desk or held by a
  black ball-hand: detention slip being written, goldfish photos, test papers with red "A"s, pizza tray, phone video
  call, comic panels, tally marks on a notepad, X-ray of a broken arm, White House envelope.
- OVER-THE-SHOULDER shots with the hero's head huge and BLURRED in the foreground (depth of field) — used for
  conversations (0:24, 4:20).
- Camera is never static: every shot has a slow push-in or lateral drift (Ken Burns, ~3-8% scale over the shot),
  with 2.5D parallax (foreground/background layers move at different speeds; the bus window landscape scrolls).
- Split screen (two panels side by side, 8:53-8:57) to show "the same moment, two people".

### Motion (limited, puppet animation)
- Characters mostly hold poses; motion = 2-4 frame pose swaps, small bobs, head tilts, arm raises, hand-shakes,
  walk-ins from the frame edge, eye/pupil changes every line. Blinks. No lip-sync (mouth changes per line only).
- Group reactions: a crowd raising arms together (4:48), everyone turning heads.

### Signature effect: the "charisma hit" (copy it as the power's visual language)
Measured at 6 fps (0:23-0:27, 2:13-2:17, 4:45):
1. a thin white ring appears around the target's head and EXPANDS outward, fading (~0.4-0.6 s);
2. 2-4 white four-point sparkle stars pop around the head;
3. a warm GOLD glow/halo stays around the head for the rest of the shot (the person is "under the spell");
4. their face switches to dazed: pupils up, soft smile, blush.
Later in the video the glow sits on EVERYONE in a crowd (6:46-7:30) — the same effect, multiplied, turns creepy.
When the power ends the glows disappear and the grade turns cold. For our videos: give every "superpower/rule" one
such simple, repeatable visual signature and let it change meaning as the story turns.

### On-screen text and UI
- Almost NO text on screen and NO burned-in captions. Text appears only as diegetic objects (sign, envelope, paper)
  or as a GAME UI: small dark rounded bars over heads "CHARISMA 10" / the hero's bar counting up to 435 -> 500
  (0:44-0:49, again at 5:04-5:05 "420"). One idea, shown once, recalled once.

## 6. Editing rhythm
- 211 shots in 569 s: **mean shot 2.7 s, median 2.2 s**, 10% under 1.2 s, 90% under 4.5 s.
- Pace by act: 0-60 s 28 cuts/min, 1-3 min 30 cuts/min (the fun montage is the fastest), from 3 min on ~20 cuts/min.
- Long holds are deliberate and rare (6-23 s): the slow push-in on the lonely hero in an empty kitchen (6:54-7:04),
  the White House climax, the final scenes — the slowdown itself signals emotion.
- Transitions: hard cuts on the narration beat (a new sentence = a new shot); no wipes, no zoom transitions.
  Mood changes are done by colour grade, not by transition effects.

## 7. Sound
- Narrator dominant (mean -17.6 dB, peaks -3.9 dB), light background music under it, small cartoon SFX for hits
  (glass break, sparkles on the charisma ring, crowd cheer). No silence gaps; music carries the transitions.

## 8. Retention and monetisation elements seen
- Animated "SUBSCRIBE" pill with a cursor clicking subscribe + bell, top centre, at 2:00-2:06 (after the first big
  laugh, right at "Then it gets bigger") and again at 9:06-9:11.
- Sponsor card (QR + one line) in a corner at 2:48-3:00, 4:50-5:01 and 8:09-8:20 — always during low-motion talk.
- No intro, no logo sting, no "in this video". Last 13 s = sponsor CTA; no classic 20 s end-screen.

## 9. How to reproduce this style for The Other Timeline
- Keep our hero Karl (user decision), but draw him in THIS language: black ball head with the two-white-eye face,
  yellow/orange hoodie as identity colour, one continuity prop (a cap, a wallet) that can be taken and returned.
- Engine options: (a) a 2D canvas/SVG renderer with layered flat backgrounds + puppet characters (closest look);
  (b) our three.js engine with an orthographic camera, unlit flat materials, painted background planes, sphere heads
  with a soft sheen, stick limbs — and a post pass for grain, vignette, bloom and per-act colour grade. Decide with
  the user before building; show a 10-second test first.
- Story template for a money topic: cold-open mini-disaster solved by the "power" -> "Most people have X. You
  have Y." -> 6-8 quick wins (planting callbacks) -> "Then it gets bigger." escalation ladder -> pivot sentence
  "But..." -> the cost through the same people -> darkest moment -> giving it up in public -> mirror ending with
  every callback reversed -> one honest real-data fact -> "So would you want ...?"
- Voice: second person, present tense, ~190 wpm, sentences 4-12 words, quote dialogue inside narration.
- Edit: new shot every 2-3 s (one sentence = one shot), 3-6 s holds only for emotion, colour grade per act.
- Our YMYL rules still apply on top: real numbers from data, "example" labels, honest part, not financial advice.

## 10. Video v2: "What If You Got $1 Every Time Someone Lied to You?" (13:11, analysed 28.11.2026)
All 791 frames viewed at 1 fps (`research/yt1/v2/sheets/`), cuts measured. NOTE: the file the user sent has a HEBREW
dub; the transcript (`research/yt1/v2/transcript.txt`) is a rough Whisper translation, good enough for the plot only.
- Story: cold open at an ice-cream stand (cone is $3, seller says something untrue -> a dollar bill pops out of the
  hoodie pocket) -> premise line at 0:30 "Every time someone lies to you, you get a dollar" -> "At first, it's
  amazing": mom's hidden cookies, little sister Cleo ("I didn't touch your tablet" = $1), best friend Wes, a dentist,
  text messages ("On my way" / "Sorry, just saw this") -> escalation: scam calls ("SCAM LIKELY", "your computer has
  a virus"), a real stat (Americans lost ~$16 BILLION to scams), used-car dealer "Honest Hank's", a political debate,
  physics of cash (1 bill = 1 g, ~450 = 1 lb, a 20 LB duffel bag), the bank won't open an account for a kid -> the
  closet fills with money, popularity is bought (everyone says "We always liked you") -> TURN: a tally notebook per
  person (CLEO, MOM, WES; mom = 306 lies), a psychology fact about everyday lying, he starts to see why people lie ->
  low point: friends exposed, mom crying alone on the stairs over bills, he secretly gives her money and it backfires
  (police, she must explain) -> CLIMAX: a free party for 1,000 kids in the park, on stage he asks "Would you still be
  here if it wasn't free?" -> 1,000 "yes" = 1,000 dollars at once (the money pours out on stage) -> aftermath: real
  friends, Wes's honest answer, scam call ignored, phone face down -> ENDING mirrors the start (bedroom, sister,
  "the best dollar you ever got") -> "So, would you want a dollar every time someone lies to you?"
- The superpower's visual sign: pink glow + expanding ring on the hoodie POCKET, a bill peeks out (same "ring +
  glow" grammar as v1's gold head halo, but placed where the money appears).
- New devices: the TALLY NOTEBOOK (top-down insert, counts per person, a big circled total "306"); phone screens
  full-frame (lock screen 6:40, group chat "what did everybody do this weekend? / Nothing / Stayed home"); white
  speech-bubble pills over heads for short dialogue ("Love the shoes.", "Sick backpack.", "We always liked you.");
  thought clouds; infographic inserts on plain cream background (grid of bills -> two piles -> "5%"; scale "1 g",
  "450 = 1 LB", "20 LB"; balance scale money vs. a kid); aerial crowd of ~1,000 for the climax; TV-in-the-room shots.
- Grades: neutral cream day scenes; night = blue-purple; sad = brown/sepia vignette (kitchen at night, stairs).
- Edit: 220 shots in 791 s, mean 3.6 s, median 3.3 s (10% under 1.9 s); 20 cuts/min in the first minute, 14-18 in
  the middle, 12 at the end. Slower than v1 (2.7 s) because the video is longer and talkier.
- Subscribe pill animation (channel avatar + SUBSCRIBE -> SUBSCRIBED + bell) at 2:20-2:26 and 13:04-13:10.
  No sponsor card in this one.

## 11. Channel formula = confirmed in 2 of 2 videos (treat as rules)
| Rule | v1 Charisma | v2 $1 per lie |
|---|---|---|
| Title "What If You (Had/Got) + number + everyday thing", a question | yes | yes |
| Second person, present tense, deadpan narrator | yes | yes |
| Cold-open mini-story proving the power before naming it, premise line at 0:30-0:45 | 0:44 | 0:30 |
| Same cast language: black ball heads, two white eyes, stick limbs, hero in mustard hoodie | yes | yes |
| Same world: house, kitchen, bedroom with basketball poster, school lockers, cafeteria, town | yes | yes |
| One repeatable "power" effect: ring + glow + sparkles | head, gold | pocket, pink |
| "At first, it's amazing" wins -> escalation up to national level | President | $16B, politicians |
| 1-3 short real facts/stats ("Psychologists found...") | 2 | 2-3 |
| Dark turn through family and best friend; mom crying alone | yes | yes |
| Public climax in front of a huge crowd where the power is used against itself | 30,000 | 1,000 |
| Mirror ending + callbacks, last line = "So would you want ...?" | yes | yes |
| Almost no on-screen text; only diegetic text, UI bars, infographic labels | yes | yes |
| Colour grade per mood (warm day, purple night, cold/sepia sad) | yes | yes |
| Animated subscribe pill around 2:00-2:30 and at the end | yes | yes |
Varies: length (9.5 vs 13 min), cut speed (2.7 vs 3.6 s), sponsor card (v1 only), counting device (UI bar vs notebook).

## 12. Video v3: "What If Everyone Could Hear Your Thoughts?" (11:08, analysed 28.11.2026)
All 668 frames viewed at 1 fps (`research/yt1/v3/sheets/`). The file has a PORTUGUESE dub; transcript is a Whisper
translation (plot only, stops at ~8:00; the rest of the plot is read from the frames).
- Story: cold open in a test - hero gives Nora a pencil, thinks "She's so pretty." and the whole class hears it;
  "Wait. Did I say that out loud?" / "Stop thinking about how pretty she is." / "Okay, floor. Swallow me. Please." ->
  premise at 0:49 ("everyone around you can hear your thoughts") -> "At first, it's amazing": knows Canberra, wins
  the fight with little sister Tess, roasts the bully back, grandpa's lasagna ("best thing I've ever eaten" -> he makes
  it every Sunday) -> "Then it gets bigger": "best taco in the history of the world" -> line around the block, every
  shop wants him, it can't be filmed (videos show just a kid chewing), a toy company flies him in ("Boring." -> line
  cancelled), pop star Skye books him for her 20,000 arena show (tickets 19,945 -> 1,147 -> SOLD OUT on a phone) ->
  science fact (2025 Stanford brain implant decoding inner speech; password lock) -> TURN: "the baby looks exactly like
  a potato", a nervous classmate drops her cards because everyone hears him, choosing Carter over best friend Miles
  in his head, "I hate you" from Tess, grandpa's cookies "like chewing a bug" -> he stops baking them, Tess's hidden D
  ("Don't think about the math test... in the front pocket of her backpack" -> mom finds it), white-bear experiment
  (1987, thought suppression), bathroom/principal "Don't think Carter", kids go silent around him, he hums to drown
  thoughts, alone on the back steps -> Miles's secret (family living in the Starlite motel) he must not think about ->
  TV "MOST TRUSTED KID IN AMERICA" -> CLIMAX: on stage with Skye in front of 20,000, he can't hide anything - so he
  lets the true good thoughts out (what he loves about Nora: tiny stars on her shoes, half her sandwich in 3rd grade,
  "I like her so much it's embarrassing", "Nora laughs like a hiccup") -> crowd cries and cheers, Skye turns it into a
  song (lyrics on a phone) -> repair: Miles on the steps, Tess "I never hated you. Not for one second.", note in the
  lunch bag -> MIRROR ENDING: the same test, pencil to Nora, "She's so pretty." - and this time she smiles back.
- Power visual: concentric lavender/white rings expanding from the head + a white CLOUD-EDGED thought pill with the
  thought typed in word by word (synced to narration: "She's" -> "She's so" -> "She's so pretty."); small doodle
  thought clouds for images (pizza, taco, cookie, a white bear, a sheep, a heart). At the climax the rings turn
  PINK and fill the arena.
- Inserts: answer sheet + pencil (opening and ending), whiteboard grade sheet with a "C+" circled, test with a red
  "D", phone screens (tickets, lyrics, group photos), chalkboard menu with an item crossed out, lunch box with a note.
- Edit: 271 shots in 668 s, mean 2.5 s, median 2.2 s; 26-28 cuts/min in the first 3 min, 21-24 later. Closest to v1.
- Subscribe pill at 2:14-2:19 and 11:01-11:06 (again "after the first escalation" + the very end).

## 13. Thumbnails (3 channel thumbnails supplied, `research/yt1/thumbs/`)
They look DIFFERENT from the video: a glossy, high-detail, saturated illustration (not the flat in-video look).
- Subject: the same yellow-hoodie hero with a black glossy head (white rim light, specular highlight), HUGE white eyes,
  sweat drop, mouth open in shock or a guilty grin; he is cut by the frame edge in the foreground (left or right third),
  the "victims" (date, family, bride) in mid-ground with big expressive eyes, lashes, real hair and clothes.
- The POWER is drawn as a glowing beam/energy line (neon green with a dollar bill, magenta arcs from his head to each
  head at the table, a pink beam from his waving hand to the bride) - the viewer sees cause -> effect in one frame.
- Location = an emotionally loaded adult scene the video only hints at (candle-lit date, Thanksgiving dinner with a
  carving fork, a church wedding), night lighting, warm candles + purple/teal neon, deep vignette.
- Text: ONE short line, a quote of the awkward moment, lowercase, chunky rounded sans (white with black outline and
  drop shadow), last word or the number in YELLOW: `"i love you" +$1`, `your mom's hot..`, `i just said hi..`.
  The text is NOT the title; it is the funniest consequence. Trailing ".." = cringe.
- Composition: text across the top ~22%, hero face 35-45% of the frame height, eye contact lines toward the glow.
- For our videos: same recipe - Karl in the foreground with a shocked face, the "power" as a glowing line toward the
  person/thing it affects, one lowercase quote with one yellow word or number; render with a richer, glossier look
  than the video itself.

## 14. Channel formula update (3 of 3 videos)
Confirmed again in v3: question title, deadpan 2nd person, cold open solving/causing a mini-crisis, premise before
0:50, "At first, it's amazing" -> "Then it gets bigger" -> turn -> family + best friend hurt -> public climax in a huge
crowd (30,000 / 1,000 / 20,000) where the power is turned around -> mirror ending with the same props -> "So would
you want ...?", 1 visual signature for the power (rings + glow), 2-3 real research facts, subscribe pill ~2:00-2:30 and
at the end, mood colour grades, near-zero on-screen text except diegetic/UI/thought pills.
New pattern: the climax uses the power for something GOOD (truth/love/no-asking) instead of fighting it.
Edit speed: 2.5-3.6 s average shot; faster (2.2-2.5 s) when the power is visual and comedic.

## 15. Open questions for the next videos
- Is the subscribe pill always at 2:00-2:30? Do they ever use a sponsor? Typical end length 9-13 min.

## Standing user decisions (28.11.2026)
- NEW STYLE (user decision 28.11.2026): new videos follow `karl-2d-template` (viral 2D "What If You...?" style from `youtube-skill-1`, Karl in turquoise hoodie (no cap) with a red-hoodie A/B test, cast Mom/Dad/Mia/Grandma Rose/Max/Lena, 50/50 money/general topics, 9-11 min, 3 per week, English + 5 audio dubs es/pt-BR/de/fr/uk). The 3D engine stays for older formats.
