# Bean Baron — coffee tycoon (Little Loop Games)

Play/demo: open index.html through any web server (ads are simulated with `?portal=none`, the default).
Balance check: `node sim/simulate.mjs 240` (first Star ~42 min, second run ~1.6x faster, ads help < 2x).

## Builds
- `dist/BeanBaron_GameDistribution.zip` — GameDistribution build. Before uploading, replace
  `REPLACE_WITH_GD_GAME_ID` in index.html with the Game ID from the GD developer dashboard, and check the
  current GD SDK docs for the rewarded-ad call (`gdsdk.showAd("rewarded")` is used here).
- `dist/BeanBaron_CrazyGames.zip` — CrazyGames SDK v3 build (Basic Launch first; ads are paid after Full Launch).
