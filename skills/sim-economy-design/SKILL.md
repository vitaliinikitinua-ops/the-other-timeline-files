---
name: sim-economy-design
description: Design and balance the economy of a simulator / idle / tycoon / life-sim web game - core loop, currencies, upgrade cost curves, income growth, offline earnings, prestige, daily rewards - and verify the balance by simulating thousands of players in code before shipping. Use for "симулятор", "idle game", "tycoon", "balance the economy", "progression is too fast/slow", "why do players quit".
---

# Sim Economy Design

Engine-neutral. Pairs with `phaser-core` (engine), `save-systems` (offline time, persistence), `game-ui-ux`
(numbers on screen), `game-feel` (reward feedback), `web-game-monetization` (rewarded ads as boosts).

## 1. Write the loop before any code
One sentence each, in a `DESIGN.md` next to the game:
- **Core loop (10 s):** act -> earn -> see the number go up. (tap / assign / sell)
- **Session loop (5-15 min):** earn -> buy an upgrade or unlock -> earn faster -> new goal appears.
- **Meta loop (days):** prestige / new area / new era -> permanent multiplier -> come back tomorrow.
- **Fantasy:** what the player *becomes* (owner of a coffee chain, a millionaire timeline, a city).
Every system must feed one of these loops or it is cut.

## 2. Keep the economy in plain data + pure functions
- `economy.js` with no engine imports: `state`, `tick(state, dt)`, `buy(state, id)`, `offline(state, seconds)`,
  `prestige(state)`. All numbers in one `BALANCE` object (costs, rates, multipliers). Scenes only read state.
- Same module runs in the browser and in `node` for the simulator (step 5). Seeded RNG for anything random.
- Big numbers: plain JS numbers are fine up to ~1e15 with care; beyond that use a mantissa/exponent pair or
  `break_infinity.js`/`break_eternity.js` (load a pinned version). Format with suffixes (K, M, B, T, then aa, ab).

## 3. Standard formulas (start here, then tune)
- Upgrade cost: `cost(n) = base * r^n`, r = 1.07-1.15 (idle classic ~1.07 for producers, 1.15+ for one-off boosts).
- Producer income: linear in count `income = rate * count * multipliers`; milestone x2 multipliers at 25/50/100/...
  so growth feels like steps, not a flat slope.
- Next-unlock pacing: each new producer costs ~8-12x the previous and earns ~4-8x -> the newest is always the best buy.
- Offline earnings: `offline = income_per_sec * min(seconds, cap) * efficiency`, cap 2-8 h, efficiency 0.5-1.0;
  show a "welcome back" screen; doubling it is the most accepted rewarded-ad placement.
- Prestige: reset currency for a permanent bonus `bonus = k * sqrt(lifetime_earnings / threshold)`; first prestige
  should be reachable in ~30-60 min of play and make the next run visibly faster (aim: 2x speed).
- Daily reward: streak ladder (day 1..7), missing a day steps back one, never wipes everything.

## 4. Targets to balance against (write them down first)
- First upgrade within 10-20 s; something new unlocks every 30-90 s for the first 10 minutes.
- Time between "can afford next meaningful thing" stays roughly flat (30 s -> 3 min -> 10 min) - not exploding.
- No dead ends: from any state the player can always afford *something* within 2 minutes (or there is a boost).
- A full session of 5-10 min ends with a visible goal for next time.

## 5. Prove it with a simulated player (always, before release)
Write `sim/simulate.mjs` that imports `economy.js` and plays automatically:
- Strategies: `greedy` (buy cheapest useful), `best_roi` (buy best income per cost), `idle` (returns every 4 h),
  `ad_watcher` (takes every rewarded boost). Run each for simulated 0-7 days, 1,000 seeds where randomness exists.
- Log per minute: currency, income/s, owned items, time-to-next-purchase. Write CSV + a quick chart (matplotlib or
  plain SVG) and look at it.
- Fail the build if: any time-to-next-purchase > 3x the target, prestige reached < 15 min or > 3 h,
  ad_watcher is more than ~2x faster than greedy (ads should help, not be mandatory), or numbers overflow/NaN.
- Re-run after every balance change; keep the CSVs in `sim/out/` to compare versions.

## 6. Real-data themes (optional, educational sims)
If the game uses real history (prices, inflation, rates), load the dataset as JSON, cite the source in the credits
screen, label invented values "example", and keep the fantasy fun: real data shapes events, the player still wins
through choices. Never give financial advice in the game.

## 7. Checklist before shipping
DESIGN.md loops written · BALANCE in one place · simulator passes · offline earnings capped and shown ·
save/load versioned (`save-systems`) · no progress gated behind ads · numbers readable on a phone.
