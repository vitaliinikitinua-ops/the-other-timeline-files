---
name: web-game-monetization
description: Make money from an HTML5/web game on portals (CrazyGames, Poki, GameDistribution, itch.io) - SDK integration, gameplay events, midgame and rewarded ads that pass review, ad-blocker handling, builds per portal, revenue expectations. Use for "заробіток на грі", "реклама в грі", "CrazyGames", "Poki", "GameDistribution", "rewarded ad", "monetize my game".
---

# Web Game Monetization (portals)

Portals host the game and run the ads; the developer gets a revenue share. Requirements change often:
**before integrating, open the portal's current official docs and re-check every rule below**
(CrazyGames: developer.crazygames.com · Poki: developers.poki.com/guide/requirements-quality and /guide/sdk-html5 ·
GameDistribution: developer agreement + SDK docs on gamedistribution.com). Rules below were collected on
26.11.2026 from official Poki pages and from secondary sources for CrazyGames/GameDistribution.

## Architecture (do this once, reuse for every portal)
- One `ads.js` adapter with the same API for every build: `init()`, `loadingStart/Stop()`, `gameplayStart/Stop()`,
  `midgame()` -> Promise, `rewarded()` -> Promise<boolean>, `happytime()` (optional). Implementations:
  `crazygames`, `poki`, `gamedistribution`, `none` (itch.io / own site / dev). Pick by build flag, never by guessing.
- The game never talks to a portal SDK directly; it only calls the adapter. The `none` adapter resolves immediately
  (rewarded returns true only in dev).
- During any ad: pause the game loop, mute all audio, ignore input; resume after the Promise settles.
- Never fire SDK events while an ad is playing. De-duplicate: no `gameplayStart` after `gameplayStart`, no `stop` after `stop`.
- If the SDK fails to load (ad blocker), the game must still be fully playable; rewarded returns false without breaking UI.

## Gameplay events
- `loadingStart` at boot, `loadingStop` when the first playable screen is ready.
- `gameplayStart` when the player is actually playing (Poki: on the player's first input, not on load).
- `gameplayStop` on pause, menus, level end, shop screens, cutscenes, and before ads.

## Midgame (interstitial) ads
- Only at natural breaks: after a level / between runs / when returning to play from a menu.
- Poki: call `commercialBreak()` right before resuming play (on the way back into gameplay), not when leaving it.
- CrazyGames: request `midgame` at each natural break; the SDK enforces frequency (reported ~1 per 3 min) and
  ignores early calls, so it's safe to request. Don't chain ads.
- Never on first launch before the player has played; never interrupting active play.

## Rewarded ads (the main income in simulators)
- Always optional, clearly labelled ("Watch an ad: x2 offline earnings"), never required to progress (fails review).
- Grant the reward only when the SDK reports the ad finished. If unavailable/blocked: no reward, friendly message.
- Good placements for sims: double offline earnings, 2x income for 5-10 min, free upgrade when the player is
  stuck, revive/continue, extra daily-reward spin. Cap boosts so `sim-economy-design` balance still holds.
- Show the button only when an ad is plausibly available; cool down after use.

## Portal notes (verify!)
- **CrazyGames:** SDK v3 loaded from their CDN, `await SDK.init()` first. Basic Launch: SDK optional, no monetization;
  Full Launch: full integration (gameplay events, ads via SDK, data/user modules where applicable).
  Secondary sources report a 50% ad revenue share and size limits measured up to the first `gameplayStart`.
- **Poki:** curated (they choose games); strict quality + SDK event rules (above); test with the Poki Inspector.
- **GameDistribution:** SDK mandatory; developer agreement states 33% revenue share, payout after a EUR 100 threshold.
  Method names differ between docs versions (`showAd('rewarded')` vs others) - read the current SDK reference.
- **itch.io:** no ad SDK; earn via "pay what you want"/donations; publish with `itch-publish`.
- Exclusivity: some portals want exclusive or first release - read terms before uploading the same build elsewhere.

## Build checklist per portal
Correct adapter flag · SDK script tag as the portal requires · no other ad network code · no external links/ads
that break portal rules · loads fast (small first payload) · works offline of the SDK · mobile + desktop input ·
audio muted during ads · events verified in the portal's test tool · version number visible in settings.

## What to tell the user (honest expectations)
Revenue depends on plays x ad views; small games often earn little at first. Grow by shipping several small games,
watching portal analytics (plays, average playtime, D1 retention) and improving the best one. Accounts, tax and
payout details are the user's to set up on each portal.
