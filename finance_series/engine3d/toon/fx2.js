// 2D overlay FX for the "real price" power (Karl #02): phone checkout UI, amber flip, $ bubbles, big numbers.
import { easeOut, pop } from "../../engine2d/engine.js";
export const AMBER = "255,184,40", AMBER_HEX = "#ffb828";

// Phone held up to camera. o = {title, old, price, btn, real, flipK (0..1), sub, clock}
export function phone(g, x, y, s, o, t) {
  g.save(); g.translate(x, y); g.scale(s, s);
  const W = 420, H = 820;
  g.shadowColor = "rgba(0,0,0,0.35)"; g.shadowBlur = 40; g.fillStyle = "#16141c"; g.beginPath(); g.roundRect(-W / 2 - 18, -H / 2 - 18, W + 36, H + 36, 56); g.fill(); g.shadowColor = "transparent";
  g.fillStyle = "#f7f4ee"; g.beginPath(); g.roundRect(-W / 2, -H / 2, W, H, 40); g.fill();
  g.fillStyle = "#16141c"; g.beginPath(); g.roundRect(-60, -H / 2 + 12, 120, 26, 13); g.fill();
  g.textAlign = "center"; g.textBaseline = "middle";
  if (o.clock) { g.font = "26px Mont"; g.fillStyle = "#2a2630"; g.fillText(o.clock, -W / 2 + 60, -H / 2 + 26); }
  // product card
  g.fillStyle = "#e9e3f5"; g.beginPath(); g.roundRect(-W / 2 + 30, -H / 2 + 70, W - 60, 300, 26); g.fill();
  if (o.draw) o.draw(g, 0, -H / 2 + 220); else headphones(g, 0, -H / 2 + 220, 1);
  g.font = "38px Anton"; g.fillStyle = "#1e1b26"; g.fillText(o.title || "WIRELESS HEADPHONES", 0, -H / 2 + 420);
  if (o.old) { g.font = "34px Mont"; g.fillStyle = "#8a8496"; g.fillText(o.old, -80, -H / 2 + 480); g.strokeStyle = "#e0344a"; g.lineWidth = 4; g.beginPath(); g.moveTo(-140, -H / 2 + 480); g.lineTo(-20, -H / 2 + 480); g.stroke(); }
  if (o.price) { g.font = "52px Anton"; g.fillStyle = "#e0344a"; g.fillText(o.price, 90, -H / 2 + 480); }
  if (o.sub) { g.font = "26px Mont"; g.fillStyle = "#e0344a"; g.fillText(o.sub, 0, -H / 2 + 535); }
  // the button: flips to the REAL price (amber) with a squash
  const fk = o.flipK || 0, by = H / 2 - 170, sq = Math.abs(Math.cos(Math.min(1, fk) * Math.PI));
  const real = fk > 0.5;
  g.save(); g.translate(0, by); g.scale(1, Math.max(0.05, sq));
  g.fillStyle = real ? "#1e1b26" : "#ff5fa2"; g.beginPath(); g.roundRect(-W / 2 + 30, -70, W - 60, 140, 34); g.fill();
  if (real) { g.lineWidth = 6; g.strokeStyle = AMBER_HEX; g.stroke(); }
  const lines = real ? (o.real || ["$120", "6 HOURS OF YOUR LIFE"]) : (o.btn || ["PAY IN 4", "JUST $30 TODAY"]);
  g.fillStyle = real ? AMBER_HEX : "#ffffff"; g.font = (real ? "56px" : "50px") + " Anton"; g.fillText(lines[0], 0, -22);
  g.font = (real ? "26px" : "30px") + " Mont"; g.fillStyle = real ? "#ffe2a0" : "#ffffff"; g.fillText(lines[1] || "", 0, 34);
  g.restore();
  if (real) { const k = (fk - 0.5) * 2; g.globalAlpha = Math.max(0, 1 - k); g.strokeStyle = `rgba(${AMBER},1)`; g.lineWidth = 8; g.beginPath(); g.roundRect(-W / 2 + 30 - k * 60, by - 70 - k * 60, W - 60 + k * 120, 140 + k * 120, 40); g.stroke(); g.globalAlpha = 1; }
  g.restore();
}
export function headphones(g, x, y, s) {
  g.save(); g.translate(x, y); g.scale(s, s); g.lineCap = "round";
  g.strokeStyle = "#2a2630"; g.lineWidth = 22; g.beginPath(); g.arc(0, 10, 95, Math.PI * 1.1, Math.PI * 1.9); g.stroke();
  for (const sx of [-1, 1]) { g.fillStyle = "#2ec4b6"; g.beginPath(); g.roundRect(sx * 92 - 34, -10, 68, 100, 30); g.fill(); g.fillStyle = "#1d7d74"; g.beginPath(); g.roundRect(sx * 92 - 20, 6, 40, 68, 18); g.fill(); }
  g.restore();
}
// amber price tag that pops above a point (screen coords)
export function realTag(g, x, y, top, bottom, k, opts = {}) {
  const a = pop(k); if (a <= 0.01) return; g.save(); g.translate(x, y); g.scale(a, a);
  g.font = `${opts.size || 50}px Anton`; const w1 = g.measureText(top).width; g.font = `${opts.sub || 26}px Mont`; const w2 = bottom ? g.measureText(bottom).width : 0;
  const w = Math.max(w1, w2) + 60, h = bottom ? (opts.size || 50) + 58 : (opts.size || 50) + 28;
  g.fillStyle = "rgba(24,20,32,0.92)"; g.beginPath(); g.roundRect(-w / 2, -h / 2, w, h, 22); g.fill(); g.lineWidth = 5; g.strokeStyle = AMBER_HEX; g.stroke();
  g.beginPath(); g.moveTo(-14, h / 2); g.lineTo(0, h / 2 + 18); g.lineTo(14, h / 2); g.fillStyle = AMBER_HEX; g.fill();
  g.textAlign = "center"; g.textBaseline = "middle"; g.font = `${opts.size || 50}px Anton`; g.fillStyle = AMBER_HEX; g.fillText(top, 0, bottom ? -14 : 2);
  if (bottom) { g.font = `${opts.sub || 26}px Mont`; g.fillStyle = "#ffe9b8"; g.fillText(bottom, 0, 30); }
  g.restore();
}
// pink "$50" payment bubble
export function bubble(g, x, y, text, k, col = "#ff5fa2") {
  const a = pop(k); if (a <= 0.01) return; g.save(); g.translate(x, y); g.scale(a, a);
  g.fillStyle = col; g.beginPath(); g.arc(0, 0, 62, 0, 7); g.fill(); g.lineWidth = 5; g.strokeStyle = "#fff"; g.stroke();
  g.fillStyle = "#fff"; g.font = "44px Anton"; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(text, 0, 3); g.restore();
}
export function bigText(g, x, y, text, size, col, k = 1, stroke = "#141218") {
  const a = easeOut(k); if (a <= 0.01) return; g.save(); g.globalAlpha = a; g.translate(x, y); const s = 0.8 + 0.2 * a; g.scale(s, s);
  g.font = `${size}px Anton`; g.textAlign = "center"; g.textBaseline = "middle"; g.lineJoin = "round"; g.lineWidth = size * 0.16; g.strokeStyle = stroke; g.strokeText(text, 0, 0); g.fillStyle = col; g.fillText(text, 0, 0); g.restore();
}
export function label(g, x, y, text) { g.save(); g.font = "22px Mont"; g.textAlign = "left"; g.fillStyle = "rgba(255,255,255,0.75)"; g.fillText(text, x, y); g.restore(); }
