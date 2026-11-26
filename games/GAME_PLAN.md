# Game plan: a "100% achievements" simulator (Little Loop Games)

## 1. Market analysis (YouTube data, 26.11.2026)

### Reference channel: СТОДНЕВКА (UCZLpgWja6zOqI4Mod9jSDqg)
282K subscribers, 46.7M views, 94 videos. Format: "Я прошел <game> на 100%", 50 min - 3 h, one game per video.

Last 50 videos. Top results:

| Views | Game | Video length |
|---|---|---|
| 1.75M + 1.08M | Find The Needle (two videos) | 1:16 / 2:28 |
| 1.04M | "Мне нужно вернуть 1 миллиард долларов" | 1:53 |
| 1.00M | One Million Coins | 1:16 |
| 944K | How to Fish | 1:36 |
| 892K | Potato Please | 2:31 |
| 772K | Project P.I.T.T. | 1:55 |
| 611K / 609K | Scratch the Ticket / Chop Chop Inc. | 1:21 / 4:30 |
| 606K | "Построил атомную бомбу на заднем дворе" | 1:28 |
| 587K / 584K / 569K | Supermarket Chaos / KOTAMON / Moon Sweepers | |
| 481K / 499K / 501K | Hammer These Nails / CRACK / Carpet Cleaning Simulator | |

Weakest:
- Pacific Drive, 39K. A big, serious game.
- Multi-part series (Cat Mail Co. #1/#2, 26-55K).
- Very fresh videos (still growing).

### Similar channels (same format, RU and EN)
- RU: СТОПРОЦЕНТЫЧ, СОТОЧКА, NiFRiN, Эвот, СКУМА, MOBIK, Hishi, Alimusin, Санвэй, Лимит, СТОПУДОВКА, шагон.
- EN: Let's Get Miserable ("I Played 100% of..."), Cheru, BlueKai, GamerGar.

These channels pick up new small games every week. That is the free marketing channel for our game.

### What the games that win have in common
1. **One absurd goal, readable in the title:** find the needle, drink the ocean, a million coins, hammer the nails, punch the walls, a billion dollars. The title of the video *is* the game's premise.
2. **A huge counter toward that goal:** 1,000,000 / 100% / a billion. Viewers watch the number grow.
3. **An incremental/upgrade loop.** You start weak and absurd, become absurdly strong, and the visible change is big (spoon -> pump -> black hole).
4. **Satisfying physics and feedback:** things break, pile up and fly, with sounds.
5. **Short to 100%: 1-3 hours.** 20-40 Steam achievements, some of them funny or secret. That is exactly the length of the video.
6. **Cheap:** 0-5 USD on Steam, a solo or small developer, often "A Game About X" / incremental.
7. **Stages / zones** that change the picture every 10-20 minutes, so the video doesn't get boring.
8. **Secrets and an ending:** a final event, a secret achievement, a funny twist ("и вот что произошло").

What doesn't work: big serious games, long games that need several videos, and slow starts.

## 2. Conclusion for us
- The game should be made **for YouTubers to film it**: a 1-3 h run to 100%, a clear absurd goal, a counter, zones, achievements, an ending.
- Money:
  - **Steam** (sales of 2-5 USD; needs the Steamworks fee of 100 USD, tax forms and a bank account on the user's side);
  - a **free web demo** (itch.io / CrazyGames / GameDistribution with ads) as the traffic funnel;
  - **keys sent to the channels above** (free marketing).
- Tech: JavaScript (Phaser 2D or three.js 3D low-poly), packaged for Steam with Electron (many incremental games on Steam are built this way). The same code runs as the web demo.
- Bean Baron (idle coffee shop) can stay as a web-portal game or be reworked into this format.

## 3. Production plan
1. **Questions -> concept** (title, goal, 3-5 zones, upgrades, ending, achievements). Done in chat.
2. **Prototype (1 session):** core action + counter + 5 upgrades + first zone; playable link.
3. **Feedback round with the user** -> fixes.
4. **Full content:** all zones, 25-40 achievements, secrets, ending, sounds, settings, saves.
5. **Balance by simulation:** a 100% run lasts 1.5-3 h; no dead spots longer than 2 min.
6. **Builds:** web demo (first zone) + full desktop build (Electron) + Steam page assets (capsule art, screenshots, trailer made with our video engine).
7. **Launch:** Steam page with wishlists -> demo on portals -> keys to the YouTubers on the list -> release.
8. **After release:** patches, a sequel or a new small game every 1-2 months.

## 4. Open questions (asked in chat)
See the conversation: platform, visual style, concept, languages, user accounts (Steam / portals).

## 5. Decisions (user, 26.11.2026)
- Platform: Steam (full game, 2-5 USD) + free web demo on portals.
- Visual style: 3D low-poly (three.js).
- Concept: **Dig to the Core**: dig a hole from your backyard to the Earth's core.
- Languages: English + Ukrainian + more Steam languages (machine translation, then review).
- Camera: first person (shovel or drill in hand, the pit deepening under your feet).
- Gameplay (user's words): "not only digging but everything else; the point is to improve, sell and so on".
  So: digging is the spine, plus side sim activities that all feed improve -> sell -> upgrade.
- Tone: absurd humour (funny finds, a neighbour, a strange ending at the core).
- Length: 1.5-2.5 h to 100%; price 2.99 USD.
- Round 3: the user rejected the digging theme -> choose a new theme (still: improve -> sell -> upgrade, first person, 3D low-poly, absurd humour).
- No characters (no neighbour or radio): humour comes from items, upgrades, achievement names and the escalation.
- Next deliverable: a full design document for approval, before any code.
- Theme chosen: **junk buying -> mystery selling** (storage lots / garages / containers).
- Buying: fixed-price lots + auctions for rare lots. Restoration: manual at first, then upgrades and machines automate it.
- Selling: own shop (faceless customer figures) + an online marketplace on the shop computer.
- Ending: collect all achievements (100%). Design doc: games/junk-tycoon/DESIGN_DOC.md
