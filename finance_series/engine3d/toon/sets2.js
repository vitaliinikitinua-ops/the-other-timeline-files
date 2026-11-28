// Extra toon sets (Karl #02 and later): bedroom, store, office, mall (atrium with stage + giant button).
// Kept separate from toon.js so parallel sessions don't collide. Same look: TOON materials + light outlines.
import * as THREE from "three";
import { TOON, mesh } from "./toon.js";

function box(g, w, h, d, col, x, y, z, o = {}) { const m = mesh(new THREE.BoxGeometry(w, h, d), TOON(col), { outline: o.outline === undefined ? 0x6e6270 : o.outline, w: o.w ?? 0.012, shadow: o.shadow ?? true }); m.position.set(x, y, z); if (o.ry) m.rotation.y = o.ry; g.add(m); return m; }
function plane(g, w, h, col, x, y, z, basic = false) { const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), basic ? new THREE.MeshBasicMaterial({ color: col }) : TOON(col)); m.position.set(x, y, z); m.receiveShadow = true; g.add(m); return m; }
function floor(g, col, w = 40, d = 30) { const f = new THREE.Mesh(new THREE.PlaneGeometry(w, d), TOON(col)); f.rotation.x = -Math.PI / 2; f.receiveShadow = true; g.add(f); return f; }
export function labelTex(lines, w = 512, h = 256, bg = "#ffffff", fg = "#1e1b26") {
  const cv = document.createElement("canvas"); cv.width = w; cv.height = h; const c = cv.getContext("2d");
  c.fillStyle = bg; c.fillRect(0, 0, w, h); c.fillStyle = fg; c.textAlign = "center"; c.textBaseline = "middle";
  lines.forEach(([t, size, col], i) => { let fs = size; do { c.font = `${fs}px Anton, Arial Black, sans-serif`; fs -= 4; } while (c.measureText(t).width > w * 0.9 && fs > 10); c.fillStyle = col || fg; c.fillText(t, w / 2, h / (lines.length + 1) * (i + 1)); });
  const tx = new THREE.CanvasTexture(cv); tx.colorSpace = THREE.SRGBColorSpace; return tx;
}
function sign(g, lines, w, h, x, y, z, bg, fg, ry = 0) { const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: labelTex(lines, 512, Math.round(512 * h / w), bg, fg) })); m.position.set(x, y, z); m.rotation.y = ry; g.add(m); return m; }
const PROD = [0xff6b5b, 0x4a7fc1, 0xf2b84b, 0x3fa874, 0x9a6edc, 0xe86a9a, 0x38c6b4, 0xd9734a];

export function makeSet2(scene, name) {
  const g = new THREE.Group(); g.name = name; scene.add(g);
  if (name === "bedroom") {          // night: bed, desk with headphone box, window with moon, poster
    floor(g, 0x6b5a7a); plane(g, 40, 14, 0x8c86b0, 0, 7, -4);
    const win = plane(g, 2.4, 2.0, 0x23305a, -2.6, 3.6, -3.98, true);
    for (const [w2, h2, x, y] of [[2.6, 0.1, -2.6, 4.6], [2.6, 0.1, -2.6, 2.6], [0.1, 2.1, -3.85, 3.6], [0.1, 2.1, -1.35, 3.6], [0.08, 2.0, -2.6, 3.6]]) box(g, w2, h2, 0.08, 0xd9d4ea, x, y, -3.95, { outline: null });
    const moon = new THREE.Mesh(new THREE.CircleGeometry(0.28, 24), new THREE.MeshBasicMaterial({ color: 0xfff3c4 })); moon.position.set(-3.1, 4.1, -3.97); g.add(moon);
    sign(g, [["LEVEL UP", 120, "#ffc23a"]], 1.4, 1.9, 1.6, 4.0, -3.97, "#3a2f5e", "#fff");
    // bed (right), headboard against wall
    box(g, 3.2, 0.5, 2.2, 0x5b4a3a, 2.4, 0.25, -2.6); box(g, 3.1, 0.35, 2.1, 0xeeeaf6, 2.4, 0.65, -2.6, { outline: 0x8a84a0 });
    box(g, 2.0, 0.3, 2.12, 0x2ec4b6, 2.95, 0.9, -2.6, { outline: 0x1d7d74 }); box(g, 0.9, 0.25, 0.6, 0xffffff, 1.3, 0.95, -3.2, { outline: 0x8a84a0 });
    box(g, 3.2, 1.6, 0.2, 0x5b4a3a, 2.4, 1.0, -3.75);
    // desk (left) + lamp + headphones box
    box(g, 2.2, 0.1, 1.0, 0xb98a63, -2.6, 1.3, -3.3); for (const x of [-3.6, -1.6]) box(g, 0.1, 1.3, 0.9, 0x8a6446, x, 0.65, -3.3);
    box(g, 0.7, 0.45, 0.45, 0x1e1b26, -2.2, 1.58, -3.3, { outline: 0x4a4656 }); box(g, 0.72, 0.06, 0.47, 0xffc23a, -2.2, 1.82, -3.3, { outline: null });
    const lamp = mesh(new THREE.ConeGeometry(0.25, 0.35, 16, 1, true), TOON(0xf2b84b)); lamp.position.set(-3.3, 2.0, -3.4); g.add(lamp);
    const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.09, 10, 8), new THREE.MeshBasicMaterial({ color: 0xfff1c4 })); bulb.position.set(-3.3, 1.88, -3.4); g.add(bulb);
    box(g, 0.9, 0.06, 0.6, 0xc9b9e8, 0.2, 0.03, -1.2, { outline: null, shadow: false });
  }
  if (name === "store") {            // shop with shelves, price tags, sale banner, checkout counter + card terminal
    floor(g, 0xe6e0d4); plane(g, 40, 14, 0xf3ece0, 0, 7, -5);
    box(g, 40, 0.8, 0.1, 0xff5a6a, 0, 4.9, -4.94, { outline: null });
    sign(g, [["-40% TODAY ONLY", 110, "#ffffff"]], 4.4, 0.75, 0, 4.9, -4.88, "#e0344a", "#fff");
    for (const x of [-6, -2.2, 3.8]) { box(g, 3.2, 3.4, 0.9, 0xdcd3c3, x, 1.7, -4.3); for (let r = 0; r < 3; r++) { box(g, 3.1, 0.08, 0.85, 0xc8bba6, x, 0.8 + r * 1.0, -4.2, { outline: null });
      for (let k = 0; k < 4; k++) { const c = PROD[(r * 4 + k + Math.round(x)) & 7]; box(g, 0.55, 0.6, 0.5, c, x - 1.15 + k * 0.76, 1.15 + r * 1.0, -4.2, { w: 0.01 }); } } }
    box(g, 3.4, 1.1, 1.0, 0x5a8ac9, 0.6, 0.55, -1.6); box(g, 3.6, 0.1, 1.15, 0xece5d8, 0.6, 1.15, -1.6);
    box(g, 0.3, 0.45, 0.2, 0x2a2630, 1.6, 1.42, -1.5, { outline: 0x4a4656 });
  }
  if (name === "office") {           // open office: desks with monitors, printer, coffee cart, windows
    floor(g, 0xb8c0c8); plane(g, 40, 14, 0xe7e4dc, 0, 7, -5);
    for (let i = 0; i < 4; i++) { plane(g, 2.4, 2.2, 0xbfe3f5, -6 + i * 4, 3.6, -4.97, true); box(g, 2.6, 0.12, 0.1, 0xffffff, -6 + i * 4, 2.45, -4.92, { outline: null }); }
    for (const [x, z] of [[-3.2, -2.6], [0.4, -2.6], [4.0, -2.6]]) { box(g, 2.4, 0.1, 1.2, 0xf2eee6, x, 1.25, z); for (const dx of [-1.1, 1.1]) box(g, 0.08, 1.25, 1.1, 0x9aa3ad, x + dx, 0.62, z);
      box(g, 0.9, 0.6, 0.06, 0x2a2630, x, 1.75, z - 0.35, { outline: 0x4a4656 }); plane(g, 0.82, 0.52, 0x8fd3ff, x, 1.75, z - 0.31, true); box(g, 0.08, 0.2, 0.08, 0x2a2630, x, 1.4, z - 0.35, { outline: null }); }
    box(g, 1.2, 1.0, 0.8, 0xdcdcdc, 6.6, 0.5, -3.6); box(g, 1.0, 0.25, 0.7, 0xc0c0c0, 6.6, 1.12, -3.6);     // printer
    box(g, 1.8, 1.1, 0.9, 0x8a5a3c, -6.8, 0.55, -2.4); box(g, 1.9, 0.08, 1.0, 0xece5d8, -6.8, 1.14, -2.4);   // coffee cart
    sign(g, [["COFFEE $6", 90, "#ffd27a"]], 1.6, 0.6, -6.8, 2.6, -2.85, "#2b2420", "#ffd27a");
  }
  if (name === "mall") {             // atrium: big floor, balconies, banners, stage with giant red PAY IN 4 button
    floor(g, 0xd8d0c4, 80, 60); plane(g, 80, 30, 0xeee4d4, 0, 15, -20);
    for (let lvl = 0; lvl < 2; lvl++) { box(g, 60, 0.4, 3, 0xcfc4b3, 0, 6 + lvl * 5, -18.5, { outline: 0x8a7e70 }); box(g, 60, 0.9, 0.1, 0xbfe3f5, 0, 6.65 + lvl * 5, -17.0, { outline: null });
      for (let i = 0; i < 8; i++) { plane(g, 5, 3.4, PROD[(i + lvl * 3) & 7], -26 + i * 7.4, 8.2 + lvl * 5 - 5, -19.9, true); } }
    for (let i = 0; i < 6; i++) sign(g, [[["MEGA SALE", "-70%", "PAY IN 4", "MIDNIGHT", "DEALS", "-50%"][i], 140, "#ffffff"]], 2.4, 4.2, -15 + i * 6, 12.5, -16.5, ["#e0344a", "#ff8a3a", "#2ec4b6", "#9a6edc", "#e0344a", "#ff8a3a"][i], "#fff");
    box(g, 12, 1.2, 5, 0x3a3060, 0, 0.6, -10, { outline: 0x221c3c });                                       // stage
    box(g, 12.4, 0.12, 5.4, 0xffc23a, 0, 1.22, -10, { outline: null });
    const ped = mesh(new THREE.CylinderGeometry(0.7, 0.8, 1.1, 32), TOON(0x2a2630), { outline: 0x4a4656 }); ped.position.set(2.5, 1.8, -10); g.add(ped);
    const btn = mesh(new THREE.CylinderGeometry(0.62, 0.62, 0.3, 32), TOON(0xe0344a), { outline: 0x7a1020 }); btn.position.set(2.5, 2.5, -10); btn.name = "bigButton"; g.add(btn);
    sign(g, [["PAY IN 4", 120, "#ffffff"]], 2.2, 0.55, 2.5, 1.65, -9.18, "#e0344a", "#fff");
    const scr = sign(g, [["MIDNIGHT MEGA SALE", 64, "#ffc23a"], ["LIVE", 90, "#ff5a6a"]], 8, 4, 0, 6.2, -12.4, "#1e1b30", "#fff"); scr.name = "screen";
  }
  if (name === "street") {           // sidewalk, shop fronts, lamp posts
    floor(g, 0x8a8f99, 80, 40); box(g, 80, 0.15, 4, 0xcfc9bf, 0, 0.07, -1.5, { outline: null });
    const fr = [0xe8b4a0, 0xb8d4e3, 0xf2d08a, 0xc9b6e4, 0xa8d8b9, 0xf0a8b8];
    for (let i = 0; i < 8; i++) { const x = -21 + i * 6; box(g, 5.8, 8 + (i % 3), 2, fr[i % 6], x, (8 + (i % 3)) / 2, -5, { outline: 0x7a7066 });
      plane(g, 3.6, 2.2, 0xbfe3f5, x, 1.9, -3.98, true); box(g, 4.2, 0.4, 0.8, [0xe0344a, 0x2ec4b6, 0xffc23a][i % 3], x, 3.4, -3.6, { outline: null }); }
    for (const x of [-12, 0, 12]) { const pole = mesh(new THREE.CylinderGeometry(0.06, 0.06, 4.5), TOON(0x3a3a44)); pole.position.set(x, 2.25, 0.4); g.add(pole); const l = mesh(new THREE.SphereGeometry(0.25, 12, 10), TOON(0xfff1c4)); l.position.set(x, 4.6, 0.4); g.add(l); }
  }
  if (name === "studio") {           // TV news desk with big screen
    floor(g, 0x2a3350); plane(g, 40, 14, 0x1e2a48, 0, 7, -5);
    const scr = sign(g, [["LIVE", 120, "#ff5a6a"], ["THE REAL PRICE GUY", 60, "#ffc23a"]], 6, 3.2, 0, 3.6, -4.9, "#14182c", "#fff"); scr.name = "screen";
    box(g, 4.4, 1.1, 1.2, 0x4a7fc1, 0, 0.55, -1.6, { outline: 0x22305a }); box(g, 4.6, 0.1, 1.4, 0xe8e6f0, 0, 1.15, -1.6);
    for (const x of [-6, 6]) box(g, 0.3, 6, 0.3, 0x5a6a9a, x, 3, -4.5);
  }
  if (name === "restaurant") {       // night, candles, window with city lights
    floor(g, 0x6b4630); plane(g, 40, 14, 0x7a3e4a, 0, 7, -4);
    for (let i = 0; i < 3; i++) { plane(g, 2.4, 2.2, 0x1e2448, -4 + i * 4, 3.4, -3.97, true); for (let k = 0; k < 6; k++) { const d = new THREE.Mesh(new THREE.CircleGeometry(0.05, 8), new THREE.MeshBasicMaterial({ color: 0xffe08a })); d.position.set(-4.9 + i * 4 + (k * 0.37) % 1.8, 2.6 + (k * 0.53) % 1.5, -3.96); g.add(d); } }
    box(g, 2.2, 0.1, 1.3, 0xf3efe6, 0, 1.2, -0.8); const leg = mesh(new THREE.CylinderGeometry(0.08, 0.1, 1.2), TOON(0x3a2a20)); leg.position.set(0, 0.6, -0.8); g.add(leg);
    const c = mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.3, 10), TOON(0xfff6e0)); c.position.set(0, 1.4, -0.8); g.add(c);
    const fl = new THREE.Mesh(new THREE.SphereGeometry(0.06, 8, 6), new THREE.MeshBasicMaterial({ color: 0xffc23a })); fl.position.set(0, 1.6, -0.8); fl.scale.y = 1.6; g.add(fl);
  }
  if (name === "lot") {              // car dealership lot with a shiny truck and flags
    floor(g, 0x7a808a, 80, 40); plane(g, 80, 20, 0xbfe3f5, 0, 10, -12, true);
    box(g, 14, 4, 4, 0xf2eee6, -6, 2, -9, { outline: 0x8a8070 }); sign(g, [["ONLY $499 / MONTH", 90, "#ffffff"]], 6, 1, -6, 3.4, -6.9, "#e0344a", "#fff");
    const tr = new THREE.Group(); tr.name = "truck"; g.add(tr);
    box(tr, 3.6, 1.0, 1.8, 0x4a7fc1, 0, 0.9, 0, { outline: 0x22305a }); box(tr, 1.7, 0.9, 1.7, 0x4a7fc1, -0.7, 1.8, 0, { outline: 0x22305a }); box(tr, 1.4, 0.6, 1.72, 0xbfe3f5, -0.7, 1.9, 0, { outline: null });
    for (const [x, z] of [[-1.2, 0.95], [1.2, 0.95], [-1.2, -0.95], [1.2, -0.95]]) { const w = mesh(new THREE.CylinderGeometry(0.42, 0.42, 0.3, 18), TOON(0x1e1b26)); w.rotation.x = Math.PI / 2; w.position.set(x, 0.42, z); tr.add(w); }
    tr.position.set(2.5, 0, -3);
    for (let i = 0; i < 8; i++) { const f = new THREE.Mesh(new THREE.ConeGeometry(0.3, 0.6, 3), new THREE.MeshBasicMaterial({ color: [0xe0344a, 0xffc23a, 0x2ec4b6][i % 3] })); f.rotation.z = Math.PI / 2; f.position.set(-12 + i * 3.4, 5.5, -7); g.add(f); }
  }
  return g;
}
