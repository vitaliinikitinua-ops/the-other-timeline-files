// Bean Baron economy - pure functions, no DOM. Runs in browser and node.
export const BALANCE = {
  version: 1,
  growth: 1.15,
  milestones: [25, 50, 100, 200, 300, 400],
  stations: [
    { id: "drip", name: "Drip Coffee", cost: 10, rate: 1 },
    { id: "espresso", name: "Espresso Bar", cost: 150, rate: 7 },
    { id: "pastry", name: "Pastry Case", cost: 2250, rate: 49 },
    { id: "latte", name: "Latte Art Station", cost: 33750, rate: 343 },
    { id: "cold", name: "Cold Brew Tap", cost: 506250, rate: 2401 },
    { id: "drive", name: "Drive-Thru", cost: 7.59375e+06, rate: 16807 },
    { id: "roast", name: "Roastery", cost: 1.13906e+08, rate: 117649 },
    { id: "trucks", name: "Coffee Truck Fleet", cost: 1.70859e+09, rate: 823543 },
  ],
  // one-off upgrades: x3 to one station (or "all") when you own `need` of it
  upgrades: [],
  tapBase: 1, tapShare: 0.05,          // tap gives max(1, 10% of income/s)
  offlineCap: 4 * 3600, offlineEff: 0.5,
  boostMult: 2, boostTime: 180, boostCooldown: 900,
  prestigeMin: 1e8,                     // lifetime coins needed for the first star
  starBonus: 0.25,                      // +25% income per star
};
(function makeUpgrades() {
  const st = BALANCE.stations;
  st.forEach((s, i) => {
    [10, 25, 50].forEach((need, k) => BALANCE.upgrades.push({ id: `${s.id}_${need}`, station: s.id, need,
      cost: s.cost * [60, 600, 8000][k], mult: 3, name: `${s.name} upgrade ${k + 1}` }));
  });
  [2e6, 2e8, 2e10].forEach((c, k) => BALANCE.upgrades.push({ id: `all_${k}`, station: "all", need: 0, cost: c, mult: 2, name: `Better beans ${k + 1}` }));
})();

export function newState(now = 0) {
  return { v: BALANCE.version, coins: 0, lifetime: 0, runEarned: 0, stars: 0, owned: Object.fromEntries(BALANCE.stations.map(s => [s.id, 0])),
           ups: {}, boostUntil: 0, boostReadyAt: 0, lastSeen: now, daily: { day: 0, last: -1 }, time: 0 };
}
const B = BALANCE;
export const stationCost = (s, n) => s.cost * Math.pow(B.growth, n);
export function bulkCost(s, n, k) { const g = B.growth; return s.cost * Math.pow(g, n) * (Math.pow(g, k) - 1) / (g - 1); }
export function milestoneMult(n) { return Math.pow(2, B.milestones.filter(m => n >= m).length); }
export function stationMult(st, id) {
  let m = 1; for (const u of B.upgrades) if (st.ups[u.id] && (u.station === id || u.station === "all")) m *= u.mult;
  return m * milestoneMult(st.owned[id]);
}
export function globalMult(st) { return (1 + B.starBonus * st.stars) * (st.time < st.boostUntil ? B.boostMult : 1); }
export function stationIncome(st, s) { return s.rate * st.owned[s.id] * stationMult(st, s.id) * globalMult(st); }
export function incomePerSec(st) { return B.stations.reduce((a, s) => a + stationIncome(st, s), 0); }
export function tapValue(st) { return Math.max(B.tapBase * (1 + st.stars * B.starBonus), incomePerSec(st) * B.tapShare); }
export function unlocked(st, i) { return i === 0 || st.owned[B.stations[i - 1].id] > 0 || st.lifetime >= B.stations[i].cost * 0.5; }
function earn(st, x) { st.coins += x; st.lifetime += x; st.runEarned += x; }
export function tick(st, dt) { earn(st, incomePerSec(st) * dt); st.time += dt; }
export function tap(st) { const v = tapValue(st); earn(st, v); return v; }
export function buyStation(st, id, k = 1) {
  const s = B.stations.find(x => x.id === id); const c = bulkCost(s, st.owned[id], k);
  if (st.coins < c) return false; st.coins -= c; st.owned[id] += k; return true;
}
export function availableUpgrades(st) { return B.upgrades.filter(u => !st.ups[u.id] && (u.station === "all" ? st.runEarned >= u.cost * 0.3 : st.owned[u.station] >= u.need)); }
export function buyUpgrade(st, id) { const u = B.upgrades.find(x => x.id === id); if (!u || st.ups[id] || st.coins < u.cost) return false; st.coins -= u.cost; st.ups[id] = 1; return true; }
export function offlineEarnings(st, seconds) { return incomePerSec({ ...st, time: Infinity, boostUntil: 0 }) * Math.min(seconds, B.offlineCap) * B.offlineEff; }
export function starsFor(lifetime) { return Math.floor(Math.sqrt(lifetime / B.prestigeMin)); }
export function pendingStars(st) { return Math.max(0, starsFor(st.lifetime) - st.stars); }
export function prestige(st) {
  const add = pendingStars(st); if (add <= 0) return 0;
  const keep = { lifetime: st.lifetime, stars: st.stars + add, daily: st.daily, time: st.time };
  Object.assign(st, newState(), keep); return add;
}
export function startBoost(st) { if (st.time < st.boostReadyAt) return false; st.boostUntil = st.time + B.boostTime; st.boostReadyAt = st.time + B.boostTime + B.boostCooldown; return true; }
export const DAILY = [100, 250, 500, 1000, 2000, 4000, 10000]; // x (1 + income/s * 60 / reward) handled in UI
export function fmt(x) {
  if (!isFinite(x)) return "∞"; if (x < 1000) return x < 10 ? x.toFixed(1).replace(/\.0$/, "") : Math.floor(x).toString();
  const u = ["K", "M", "B", "T", "Qa", "Qi", "Sx", "Sp", "Oc", "No", "Dc"]; let i = -1;
  while (x >= 1000 && i < u.length - 1) { x /= 1000; i++; } return (x < 100 ? x.toFixed(2) : x.toFixed(1)).replace(/\.?0+$/, "") + u[i];
}
