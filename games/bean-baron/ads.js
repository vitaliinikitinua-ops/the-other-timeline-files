// One ad adapter for every portal. Pick with ?portal=gd|cg|none or window.BB_PORTAL.
// GameDistribution needs the real GAME_ID from the GD dashboard (set window.BB_GD_ID before loading).
const portal = (new URLSearchParams(location.search).get("portal") || window.BB_PORTAL || "none").toLowerCase();
let ready = false, playing = false, busy = false, sdk = null;
const listeners = { pause: [], resume: [] };
export const Ads = {
  portal,
  on(ev, fn) { listeners[ev].push(fn); },
  async init() {
    try {
      if (portal === "cg") {
        await loadScript("https://sdk.crazygames.com/crazygames-sdk-v3.js");
        sdk = window.CrazyGames.SDK; await sdk.init(); ready = true;
      } else if (portal === "gd") {
        window.GD_OPTIONS = { gameId: window.BB_GD_ID || "REPLACE_WITH_GD_GAME_ID", onEvent: e => {
          if (e.name === "SDK_GAME_PAUSE") fire("pause");
          if (e.name === "SDK_GAME_START") fire("resume");
        } };
        await loadScript("https://html5.api.gamedistribution.com/main.min.js"); ready = !!window.gdsdk;
      }
    } catch (e) { ready = false; }   // ad blocker or offline: game still works
  },
  loadingStart() { if (portal === "cg" && ready) try { sdk.game.loadingStart(); } catch (e) {} },
  loadingStop() { if (portal === "cg" && ready) try { sdk.game.loadingStop(); } catch (e) {} },
  gameplayStart() { if (busy || playing) return; playing = true; if (portal === "cg" && ready) try { sdk.game.gameplayStart(); } catch (e) {} },
  gameplayStop() { if (busy || !playing) return; playing = false; if (portal === "cg" && ready) try { sdk.game.gameplayStop(); } catch (e) {} },
  // natural break only (after opening a new café). Resolves when the game may continue.
  async midgame() {
    if (!ready || busy) return;
    busy = true; fire("pause");
    try {
      if (portal === "cg") await new Promise(res => sdk.ad.requestAd("midgame", { adFinished: res, adError: res, adStarted: () => {} }));
      else if (portal === "gd" && window.gdsdk) await window.gdsdk.showAd();
    } catch (e) {}
    busy = false; fire("resume");
  },
  // returns true only if the player watched the whole rewarded ad
  async rewarded() {
    if (portal === "none") return devReward();
    if (!ready || busy) return false;
    busy = true; fire("pause"); let ok = false;
    try {
      if (portal === "cg") ok = await new Promise(res => sdk.ad.requestAd("rewarded", { adFinished: () => res(true), adError: () => res(false), adStarted: () => {} }));
      else if (portal === "gd" && window.gdsdk) { await window.gdsdk.showAd("rewarded"); ok = true; }
    } catch (e) { ok = false; }
    busy = false; fire("resume"); return ok;
  },
  available() { return portal === "none" || ready; },
};
function fire(ev) { listeners[ev].forEach(f => { try { f(); } catch (e) {} }); }
function loadScript(src) { return new Promise((res, rej) => { const s = document.createElement("script"); s.src = src; s.async = true; s.onload = res; s.onerror = rej; document.head.appendChild(s); }); }
async function devReward() { fire("pause"); await new Promise(r => setTimeout(r, 900)); fire("resume"); return true; } // demo build: fake 1 s "ad"
