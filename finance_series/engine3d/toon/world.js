// Extra sets and props for the toon engine (Karl series). Same look as toon.js: MeshToon + inverted-hull outlines.
import * as THREE from "three";
import { TOON, mesh } from "./toon.js";

function box(g, w, h, d, col, x, y, z, o = {}) { const m = mesh(new THREE.BoxGeometry(w, h, d), TOON(col), { outline: o.outline === undefined ? 0x6e6270 : o.outline, w: o.w ?? 0.012, shadow: o.shadow ?? true }); m.position.set(x, y, z); if (o.ry) m.rotation.y = o.ry; g.add(m); return m; }
function plane(g, w, h, col, x, y, z, basic = false) { const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), basic ? new THREE.MeshBasicMaterial({ color: col }) : TOON(col)); m.position.set(x, y, z); m.receiveShadow = true; g.add(m); return m; }
function floor(g, col, w = 60, d = 40) { const f = new THREE.Mesh(new THREE.PlaneGeometry(w, d), TOON(col)); f.rotation.x = -Math.PI / 2; f.receiveShadow = true; g.add(f); return f; }
export function labelTex(lines, w = 512, h = 256, bg = "#ffffff", fg = "#1e1b26", font = "Anton") {
  const cv = document.createElement("canvas"); cv.width = w; cv.height = h; const g = cv.getContext("2d");
  g.fillStyle = bg; g.fillRect(0, 0, w, h); g.fillStyle = fg; g.textAlign = "center"; g.textBaseline = "middle";
  const L = Array.isArray(lines) ? lines : [lines]; L.forEach((l, i) => { g.font = `${Math.floor(h / (L.length + 0.6))}px ${font}`; g.fillText(l, w / 2, h * (i + 0.8) / (L.length + 0.6)); });
  const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; return t;
}
function sign(g, text, w, h, x, y, z, bg, fg) { const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: labelTex(text, 512, Math.round(512 * h / w), bg, fg) })); m.position.set(x, y, z); g.add(m); return m; }

export function makeSet2(scene, name) {
  const g = new THREE.Group(); scene.add(g);
  if (name === "street") {   // corner store + sidewalk + parked loud car
    floor(g, 0x8d8f99); box(g, 60, 0.18, 6, 0xcfc8bb, 0, 0.09, -2, { outline: null });
    plane(g, 60, 16, 0xc9a27e, 0, 8, -5);
    box(g, 9, 5.6, 0.3, 0xe07a5f, -1, 2.8, -4.85);
    const win = plane(g, 3.4, 2.4, 0xa8dbf2, -3.2, 2.2, -4.65, true); const win2 = plane(g, 3.4, 2.4, 0xa8dbf2, 2.4, 2.2, -4.65, true);
    box(g, 1.4, 3.0, 0.1, 0x5a3e2e, -0.4, 1.5, -4.65);
    sign(g, "CORNER STORE", 6, 1.0, -0.6, 4.8, -4.6, "#f2b84b", "#2a1a12");
    for (let i = 0; i < 3; i++) box(g, 1.1, 0.12, 0.12, 0xf6f1e7, -3.2, 1.2 + i * 0.6, -4.55, { outline: null });
    // loud car
    const car = makeCar(0xffc23a); car.position.set(5.2, 0, 0.6); car.rotation.y = -0.15; g.add(car);
    for (const x of [-9, 9]) { const p = mesh(new THREE.CylinderGeometry(0.08, 0.08, 5), TOON(0x3a3a44)); p.position.set(x, 2.5, -1.2); g.add(p); }
  }
  if (name === "mall") {
    floor(g, 0xe9e4dc); plane(g, 60, 16, 0xf3ede4, 0, 8, -6);
    const cols = [0xff6b5b, 0x9a6edc, 0x38c6b4, 0xf2b84b, 0x4a7fc1];
    const names = ["LUXE", "SNKRZ", "GLAM", "TECH+", "BRANDO"];
    for (let i = 0; i < 5; i++) { const x = -12 + i * 6; box(g, 5.4, 4.6, 0.3, cols[i], x, 2.3, -5.8);
      plane(g, 4.2, 2.8, 0xbfe6f7, x, 2.0, -5.62, true); sign(g, names[i], 3.6, 0.8, x, 4.1, -5.6, "#ffffff", "#1e1b26");
      for (let k = 0; k < 3; k++) { const hg = mesh(new THREE.ConeGeometry(0.3, 0.6, 4), TOON(cols[(i + k + 1) % 5]), { w: 0.01 }); hg.position.set(x - 1.2 + k * 1.2, 1.4, -5.4); g.add(hg); } }
    box(g, 60, 0.4, 3, 0xdcd3c6, 0, 6.2, -4.5, { outline: null });
    for (const x of [-7, 7]) { const pot = box(g, 0.9, 0.8, 0.9, 0xd9734a, x, 0.4, -1.5); const tree = mesh(new THREE.SphereGeometry(0.8, 14, 10), TOON(0x5aa06a)); tree.position.set(x, 1.6, -1.5); g.add(tree); }
  }
  if (name === "hallway") {  // school hallway with lockers
    floor(g, 0xcfd6d6); plane(g, 60, 16, 0xf0e6d2, 0, 8, -3.2);
    for (let i = 0; i < 18; i++) { const x = -13.5 + i * 1.5; box(g, 1.4, 3.4, 0.6, i % 6 === 3 ? 0xff6b5b : 0x4a7fc1, x, 1.7, -2.9, { w: 0.01 });
      for (let k = 0; k < 3; k++) box(g, 0.8, 0.05, 0.05, 0x2e4f7a, x, 2.9 - k * 0.12, -2.58, { outline: null }); }
    box(g, 60, 0.6, 0.1, 0x9aa3ad, 0, 4.0, -3.1, { outline: null });
  }
  if (name === "classroom") {
    floor(g, 0xc6a77e); plane(g, 60, 16, 0xe9e2cf, 0, 8, -5); plane(g, 16, 16, 0xe2dac6, 8, 8, 0).rotation.y = -Math.PI / 2;
    box(g, 6, 2.6, 0.1, 0x2f5a46, -1.5, 3.2, -4.92, { outline: 0x3a3030 });
    const chalk = sign(g, ["x² + 2x = 3"], 3.6, 0.9, -1.5, 3.4, -4.85, "#2f5a46", "#f6f1e7"); chalk.scale.set(1, 1, 1);
    for (let i = 0; i < 2; i++) { plane(g, 2.6, 2.4, 0x9fd3ef, 7.95, 3.0, -2.5 + i * 3.6, true).rotation.y = -Math.PI / 2; }
    for (let r = 0; r < 3; r++) for (let c = 0; c < 4; c++) { const x = -4.5 + c * 2.6, z = -2.2 + r * 2.2; box(g, 1.5, 0.1, 1.0, 0xd9a66f, x, 1.15, z); box(g, 0.1, 1.1, 0.8, 0x9aa3ad, x, 0.55, z); }
  }
  if (name === "dealer") {   // car showroom
    floor(g, 0xf2f0ec); plane(g, 60, 16, 0xe8eef3, 0, 8, -6);
    plane(g, 30, 5, 0xbfe0f2, 0, 3.4, -5.95, true);
    sign(g, "ONLY $400/MO*", 5.2, 1.0, 0, 6.6, -5.9, "#e0344a", "#ffffff");
    const car = makeCar(0xe0413b, true); car.position.set(0.2, 0, -1.6); car.rotation.y = 0.35; g.add(car);
    const c2 = makeCar(0x2f3b5c, true); c2.position.set(-7.5, 0, -3); c2.rotation.y = 0.9; g.add(c2);
    for (const x of [-4, 4]) { const lamp = mesh(new THREE.CylinderGeometry(0.6, 0.6, 0.08, 20), TOON(0xffffff)); lamp.position.set(x, 7, -2); g.add(lamp); }
  }
  if (name === "hall") {     // home hallway at night: stairs + kitchen door glowing
    floor(g, 0x7a5a44); plane(g, 60, 16, 0x5a5878, 0, 8, -4);
    for (let i = 0; i < 9; i++) box(g, 2.4, 0.32, 0.8, 0x9a7454, -3.2, 0.16 + i * 0.32, 1.6 - i * 0.62, { w: 0.01 });
    box(g, 0.12, 3.4, 6, 0xd9c3a4, -1.95, 2.6, -0.8, { outline: 0x3a2a20 });
    const door = plane(g, 2.0, 3.4, 0xffd99a, 3.2, 1.7, -3.95, true);
    box(g, 2.3, 0.15, 0.15, 0x3a2a20, 3.2, 3.5, -3.9, { outline: null });
    for (const x of [2.05, 4.35]) box(g, 0.15, 3.6, 0.15, 0x3a2a20, x, 1.8, -3.9, { outline: null });
    const pl = new THREE.PointLight(0xffc27a, 6, 9); pl.position.set(3.2, 2.2, -3.2); g.add(pl);
  }
  if (name === "behindgym") {
    floor(g, 0x9a9488); const wall = plane(g, 60, 16, 0xa9583f, 0, 8, -3);
    for (let r = 0; r < 14; r++) box(g, 60, 0.04, 0.04, 0x8a4430, 0, 0.5 + r * 0.6, -2.97, { outline: null });
    box(g, 1.4, 1.2, 1.0, 0x5a7a5a, 4.5, 0.6, -2.2); box(g, 1.4, 1.2, 1.0, 0x5a7a5a, 6.0, 0.6, -2.2);
  }
  if (name === "tv") {       // TV studio of "the Millionaire Mindset"
    floor(g, 0x26213a); plane(g, 60, 16, 0x3a2f6a, 0, 8, -5);
    for (let i = 0; i < 9; i++) { const s = mesh(new THREE.SphereGeometry(0.18, 10, 8), new THREE.MeshBasicMaterial({ color: 0xffd36a }), { outline: null }); s.position.set(-8 + i * 2, 6.4, -4.8); g.add(s); }
    sign(g, ["MILLIONAIRE MINDSET"], 7, 1.1, 0, 5.2, -4.9, "#ffc23a", "#2a1a12");
    const car = makeCar(0xff8a1e, true); car.position.set(3.2, 0, -2.2); car.rotation.y = -0.5; g.add(car);
  }
  if (name === "bus") {      // school bus parking lot (trip) - simple
    floor(g, 0x8d8f99); plane(g, 60, 16, 0x9fd3ef, 0, 8, -10, true);
    const bus = new THREE.Group(); box(bus, 9, 2.6, 2.4, 0xf2b84b, 0, 1.7, 0); for (let i = 0; i < 6; i++) plane(bus, 1.0, 0.8, 0xbfe6f7, -3.4 + i * 1.35, 2.2, 1.22, true);
    for (const x of [-3, 3]) for (const z of [-1.2, 1.2]) { const w = mesh(new THREE.CylinderGeometry(0.5, 0.5, 0.3, 16), TOON(0x222222)); w.rotation.x = Math.PI / 2; w.position.set(x, 0.5, z); bus.add(w); }
    bus.position.set(0, 0, -4); g.add(bus);
  }
  return g;
}

// ---------------------------------------------------------------- props
export function makeCar(col, shiny = false) {
  const g = new THREE.Group(); const m = TOON(col);
  const body = mesh(new THREE.BoxGeometry(4.2, 0.8, 1.9), m); body.position.y = 0.75; g.add(body);
  const cab = mesh(new THREE.BoxGeometry(2.2, 0.7, 1.7), m); cab.position.set(-0.2, 1.45, 0); g.add(cab);
  const glass = new THREE.Mesh(new THREE.BoxGeometry(2.25, 0.5, 1.72), new THREE.MeshBasicMaterial({ color: 0x9fd3ef })); glass.position.set(-0.2, 1.48, 0); g.add(glass);
  for (const x of [-1.3, 1.3]) for (const z of [-0.95, 0.95]) { const w = mesh(new THREE.CylinderGeometry(0.4, 0.4, 0.3, 18), TOON(0x222228)); w.rotation.x = Math.PI / 2; w.position.set(x, 0.4, z); g.add(w); }
  if (shiny) { const sp = new THREE.Mesh(new THREE.SphereGeometry(0.12, 8, 6), new THREE.MeshBasicMaterial({ color: 0xffffff })); sp.position.set(0.8, 1.17, 0.96); g.add(sp); }
  return g;
}
export function makeProp(kind, opt = {}) {
  const g = new THREE.Group();
  if (kind === "shoebox") { box(g, 0.75, 0.36, 0.48, 0xff6b5b, 0, 0.18, 0); box(g, 0.8, 0.09, 0.52, 0xffffff, 0, 0.4, 0); }
  if (kind === "sneakers") for (const s of [-1, 1]) { const sh = mesh(new THREE.SphereGeometry(0.2, 14, 10), TOON(opt.col || 0xffc23a)); sh.scale.set(1, 0.6, 1.8); sh.position.set(s * 0.24, 0.12, 0); g.add(sh); const sole = mesh(new THREE.BoxGeometry(0.36, 0.06, 0.7), TOON(0xffffff), { w: 0.008 }); sole.position.set(s * 0.24, 0.03, 0); g.add(sole); }
  if (kind === "phone") { box(g, 0.32, 0.6, 0.04, 0x1e1b26, 0, 0, 0); const sc = new THREE.Mesh(new THREE.PlaneGeometry(0.28, 0.54), new THREE.MeshBasicMaterial({ color: 0x8fd3ff })); sc.position.z = 0.025; g.add(sc); }
  if (kind === "jar") { const gl = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.3, 0.6, 20), new THREE.MeshToonMaterial({ color: 0xbfe6ff, transparent: true, opacity: 0.55 })); gl.position.y = 0.3; g.add(gl);
    box(g, 0.5, 0.08, 0.5, 0xd9a66f, 0, 0.64, 0, { w: 0.008 }); const coins = mesh(new THREE.CylinderGeometry(0.27, 0.27, opt.fill || 0.12, 20), TOON(0xffc23a)); coins.position.y = (opt.fill || 0.12) / 2 + 0.02; g.add(coins);
    if (opt.label) { const l = new THREE.Mesh(new THREE.PlaneGeometry(0.46, 0.2), new THREE.MeshBasicMaterial({ map: labelTex(opt.label, 256, 112, "#fbfaf4", "#1e1b26") })); l.position.set(0, 0.35, 0.31); g.add(l); } }
  if (kind === "donation") { box(g, 1.0, 0.8, 0.7, 0xd9a66f, 0, 0.4, 0); box(g, 0.5, 0.04, 0.08, 0x2a1a12, 0, 0.81, 0, { outline: null });
    const l = new THREE.Mesh(new THREE.PlaneGeometry(0.8, 0.36), new THREE.MeshBasicMaterial({ map: labelTex(["TRIP FUND"], 256, 116, "#fbfaf4", "#1e1b26") })); l.position.set(0, 0.45, 0.36); g.add(l); }
  if (kind === "table") { box(g, 1.6, 0.1, 1.0, 0x9aa3ad, 0, 1.0, 0); box(g, 0.1, 1.0, 0.1, 0x6e7680, 0, 0.5, 0); }
  if (kind === "mic") { const p = mesh(new THREE.CylinderGeometry(0.03, 0.03, 1.6), TOON(0x222222)); p.position.y = 0.8; g.add(p); const h = mesh(new THREE.SphereGeometry(0.1, 10, 8), TOON(0x444444)); h.position.y = 1.65; g.add(h); }
  if (kind === "mop") { const p = mesh(new THREE.CylinderGeometry(0.035, 0.035, 2.0), TOON(0xd9a66f)); p.position.y = 1.0; g.add(p); const h = mesh(new THREE.SphereGeometry(0.25, 10, 8), TOON(0xe9e2d8)); h.scale.set(1.3, 0.5, 1); h.position.y = 0.1; g.add(h); }
  if (kind === "cake") { const c = mesh(new THREE.CylinderGeometry(0.4, 0.4, 0.35, 24), TOON(0xf2a6bf)); c.position.y = 0.18; g.add(c); const t2 = mesh(new THREE.CylinderGeometry(0.42, 0.42, 0.06, 24), TOON(0xffffff)); t2.position.y = 0.37; g.add(t2);
    const cd = mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.2), TOON(0x8fd3ff)); cd.position.y = 0.5; g.add(cd); }
  if (kind === "cereal") { box(g, 0.4, 0.6, 0.14, opt.col || 0xf2b84b, 0, 0.3, 0); }
  if (kind === "hoodie") { const h = mesh(new THREE.BoxGeometry(0.9, 0.7, 0.08), TOON(opt.col || 0x9a6edc)); h.position.y = 0; g.add(h); }
  if (kind === "notebook") { box(g, 0.9, 0.04, 1.2, 0xfbfaf4, 0, 0.02, 0); }
  if (kind === "bags") for (let i = 0; i < 4; i++) { const b = box(g, 0.4, 0.5, 0.18, [0xff6b5b, 0x9a6edc, 0xf2b84b, 0x38c6b4][i], (i - 1.5) * 0.3, 0.25, (i % 2) * 0.15); b.rotation.y = i * 0.3; }
  if (kind === "coffee") { const c = mesh(new THREE.CylinderGeometry(0.1, 0.08, 0.26, 12), TOON(0xf5f0e6)); c.position.y = 0.13; g.add(c); }
  if (kind === "coins") for (let i = 0; i < 6; i++) { const c = mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.02, 12), TOON(0xffc23a), { w: 0.005 }); c.position.set((i % 3) * 0.13, 0.01 + Math.floor(i / 3) * 0.02, Math.floor(i / 3) * 0.05); g.add(c); }
  if (kind === "chair") { box(g, 0.9, 0.12, 0.9, 0x222228, 0, 0.9, 0); box(g, 0.9, 1.1, 0.12, 0xe0344a, 0, 1.5, -0.4); box(g, 0.1, 0.9, 0.1, 0x444444, 0, 0.45, 0); }
  if (kind === "piggy") { const b = mesh(new THREE.SphereGeometry(0.3, 16, 12), TOON(0xf2a6bf)); b.scale.set(1.3, 1, 1); b.position.y = 0.3; g.add(b); const sn = mesh(new THREE.CylinderGeometry(0.1, 0.1, 0.08, 12), TOON(0xe88aa8)); sn.rotation.z = Math.PI / 2; sn.position.set(0.4, 0.32, 0); g.add(sn); }
  return g;
}
