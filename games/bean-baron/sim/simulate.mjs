// Simulated players for Bean Baron. node sim/simulate.mjs [minutes]
import * as E from "../economy.js";
import fs from "fs";
const MIN = +(process.argv[2] || 180);
function deltaIncome(st, act) {
  const c = structuredClone(st); c.coins = 1e300;
  const before = E.incomePerSec(c);
  if (act.type === "s") E.buyStation(c, act.id); else E.buyUpgrade(c, act.id);
  return E.incomePerSec(c) - before;
}
function options(st) {
  const o = [];
  E.BALANCE.stations.forEach((s, i) => { if (E.unlocked(st, i)) o.push({ type: "s", id: s.id, cost: E.stationCost(s, st.owned[s.id]), name: s.name }); });
  for (const u of E.availableUpgrades(st)) o.push({ type: "u", id: u.id, cost: u.cost, name: u.name });
  return o;
}
function run(strategy, taps = 3, label = strategy, startStars = 0) {
  const st = E.newState(); st.stars = startStars; const log = []; const buys = [];
  let lastBuy = 0, maxGap = 0, firstStar = null, tenStars = null;
  for (let t = 0; t < MIN * 60; t++) {
    E.tick(st, 1);
    const active = t < 20 * 60 || (t % 3600) < 600;        // plays actively first 20 min, then 10 min per hour
    if (active) for (let k = 0; k < taps; k++) E.tap(st);
    if (strategy === "ad_watcher" && active) E.startBoost(st);
    if (active) {
      for (let guard = 0; guard < 20; guard++) {
        const opts = options(st).filter(o => o.cost <= st.coins);
        if (!opts.length) break;
        let pick;
        if (strategy === "greedy") pick = opts.sort((a, b) => a.cost - b.cost)[0];
        else pick = opts.map(o => ({ ...o, roi: deltaIncome(st, o) / o.cost })).sort((a, b) => b.roi - a.roi)[0];
        const ok = pick.type === "s" ? E.buyStation(st, pick.id) : E.buyUpgrade(st, pick.id);
        if (!ok) break;
        buys.push([t, pick.name]); if (t < 20 * 60 && t - lastBuy > maxGap) maxGap = t - lastBuy; lastBuy = t;
      }
    }
    if (firstStar === null && E.pendingStars(st) >= 1) firstStar = t;
    if (tenStars === null && E.pendingStars(st) >= 4) tenStars = t;
    if (t % 60 === 0) log.push([t / 60, st.coins, E.incomePerSec(st), Object.values(st.owned).reduce((a, b) => a + b, 0)]);
    if (!isFinite(st.coins) || isNaN(st.coins)) throw new Error("NaN/overflow");
  }
  fs.mkdirSync("sim/out", { recursive: true });
  fs.writeFileSync(`sim/out/${label}.csv`, "min,coins,ips,owned\n" + log.map(r => r.join(",")).join("\n"));
  const firstBuy = buys[0]?.[0]; const unlocks = E.BALANCE.stations.map(s => { const b = buys.find(x => x[1] === s.name); return b ? +(b[0] / 60).toFixed(1) : null; });
  // purchase gaps in first 10 minutes
  const early = buys.filter(b => b[0] < 600).map(b => b[0]); let eg = 0; for (let i = 1; i < early.length; i++) eg = Math.max(eg, early[i] - early[i - 1]);
  return { label, firstBuy, maxGapEarly10min: eg, maxGapActive: maxGap, firstStarMin: firstStar && +(firstStar / 60).toFixed(1), tenStarsMin: tenStars && +(tenStars / 60).toFixed(1),
           unlockMin: unlocks, ipsAt: [10, 30, 60, 120].map(m => E.fmt(log[Math.min(m, log.length - 1)][2])) };
}
const res = [run("greedy"), run("best_roi"), run("ad_watcher"), run("best_roi", 3, "run2_with_4_stars", 4)];
console.table(res.map(r => ({ ...r, unlockMin: r.unlockMin.join(" "), ipsAt: r.ipsAt.join(" ") })));
