// Junk Lot Tycoon - prototype v0.2 (three.js, first person)
import * as THREE from "three";
import { ITEMS, LOTS, UPGRADES, ACHIEVEMENTS, BALANCE, TUTORIAL, rollLot } from "./data.js";

const $ = (id) => document.getElementById(id);
const SAVE_KEY = "junklot_save_v2";
const VERSION = "0.2";

// ---------------------------------------------------------------- state
const S = {
  money: BALANCE.startMoney, xp: 0, lvl: 1, up: {}, ach: {}, tut: 0, quests: [], flags: {}, world: [],
  stats: { earned: 0, sold: 0, trashed: 0, lots: 0, requests: 0, shinies: 0, bestStreak: 0, best: 0 },
};
try {
  const s = JSON.parse(localStorage.getItem(SAVE_KEY) || "null");
  if (s && s.v === 2) { Object.assign(S, s.data); S.stats = Object.assign({ earned: 0, sold: 0, trashed: 0, lots: 0, requests: 0, shinies: 0, bestStreak: 0, best: 0 }, s.data.stats); }
} catch (e) {}
function save() { try { S.world = serializeWorld(); localStorage.setItem(SAVE_KEY, JSON.stringify({ v: 2, data: S })); } catch (e) {} }
setInterval(save, 5000);
addEventListener("beforeunload", save);

// Combined effects of all owned upgrades
function fx() {
  const f = { clean: 1, price: 1, cust: 1, junk: 1, rare: 1, walk: 1, tables: 1, baths: 0, bathSpeed: 1, xp: 1 };
  for (const u of UPGRADES) {
    if (!S.up[u.id]) continue;
    for (const [k, v] of Object.entries(u.fx)) {
      if (k === "tables" || k === "baths") f[k] += v; else if (k === "junk") f.junk = Math.max(f.junk, v); else f[k] *= v;
    }
  }
  return f;
}
let F = fx();

// ---------------------------------------------------------------- audio
let AC = null, noiseGain = null;
function audio() {
  if (AC) return AC;
  try {
    AC = new (window.AudioContext || window.webkitAudioContext)();
    const buf = AC.createBuffer(1, AC.sampleRate, AC.sampleRate), d = buf.getChannelData(0);
    for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
    const src = AC.createBufferSource(); src.buffer = buf; src.loop = true;
    const f = AC.createBiquadFilter(); f.type = "bandpass"; f.frequency.value = 1800; f.Q.value = .7;
    noiseGain = AC.createGain(); noiseGain.gain.value = 0;
    src.connect(f).connect(noiseGain).connect(AC.destination); src.start();
  } catch (e) { AC = null; }
  return AC;
}
function beep(freq, dur = .12, type = "sine", vol = .15, slide = 0) {
  const ac = audio(); if (!ac) return;
  const o = ac.createOscillator(), g = ac.createGain(), t = ac.currentTime;
  o.type = type; o.frequency.setValueAtTime(freq, t); if (slide) o.frequency.exponentialRampToValueAtTime(freq * slide, t + dur);
  g.gain.setValueAtTime(vol, t); g.gain.exponentialRampToValueAtTime(.0001, t + dur);
  o.connect(g).connect(ac.destination); o.start(t); o.stop(t + dur + .02);
}
const sfx = {
  cash() { beep(880, .08, "square", .08); setTimeout(() => beep(1320, .14, "square", .08), 70); },
  pick() { beep(420, .07, "triangle", .12, 1.5); },
  drop() { beep(260, .09, "triangle", .12, .6); },
  shiny() { [988, 1319, 1760].forEach((f, i) => setTimeout(() => beep(f, .2, "sine", .12), i * 80)); },
  ach() { [523, 659, 784, 1047].forEach((f, i) => setTimeout(() => beep(f, .18, "triangle", .12), i * 90)); },
  level() { [392, 523, 659, 784, 1047, 1319].forEach((f, i) => setTimeout(() => beep(f, .22, "square", .07), i * 70)); },
  quest() { [659, 880, 1175].forEach((f, i) => setTimeout(() => beep(f, .16, "triangle", .12), i * 90)); },
  door() { beep(90, 1.6, "sawtooth", .05, 1.4); },
  trash() { beep(160, .2, "square", .07, .5); },
  no() { beep(200, .15, "square", .08, .7); },
};

// ---------------------------------------------------------------- renderer / scene
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.setSize(innerWidth, innerHeight);
document.body.prepend(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x9cc9e8);
scene.fog = new THREE.Fog(0x9cc9e8, 30, 75);
const camera = new THREE.PerspectiveCamera(70, innerWidth / innerHeight, .05, 200);
camera.rotation.order = "YXZ";
camera.position.set(0, 1.7, 3);
scene.add(camera);
addEventListener("resize", () => { camera.aspect = innerWidth / innerHeight; camera.updateProjectionMatrix(); renderer.setSize(innerWidth, innerHeight); });

scene.add(new THREE.HemisphereLight(0xdff1ff, 0x5d7f45, 1.15));
const sun = new THREE.DirectionalLight(0xfff2d8, 1.3); sun.position.set(10, 20, 8); scene.add(sun);

const mat = (c) => new THREE.MeshLambertMaterial({ color: c, flatShading: true });
function box(w, h, d, c, x, y, z, parent = scene) { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat(c)); m.position.set(x, y, z); parent.add(m); return m; }

function labelMesh(text, w, h, bg = "#2b2420", fg = "#ffb02e", size = 64) {
  const cv = document.createElement("canvas"); cv.width = 512; cv.height = Math.round(512 * h / w);
  const g = cv.getContext("2d"); g.fillStyle = bg; g.fillRect(0, 0, cv.width, cv.height);
  g.fillStyle = fg; g.font = `800 ${size}px system-ui, sans-serif`; g.textAlign = "center"; g.textBaseline = "middle";
  const lines = text.split("\n"); lines.forEach((l, i) => g.fillText(l, cv.width / 2, cv.height / 2 + (i - (lines.length - 1) / 2) * size * 1.1));
  const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace;
  return new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: tex }));
}
function priceSprite(text) {
  const cv = document.createElement("canvas"); cv.width = 256; cv.height = 96;
  const g = cv.getContext("2d"); g.fillStyle = "#fff6d8"; g.beginPath(); g.roundRect(6, 6, 244, 84, 18); g.fill();
  g.fillStyle = "#2b2420"; g.font = "800 56px system-ui, sans-serif"; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(text, 128, 50);
  const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace;
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, depthTest: false })); s.scale.set(.5, .19, 1); s.renderOrder = 5; return s;
}

// ---------------------------------------------------------------- world
const colliders = [];
const rect = (minX, maxX, minZ, maxZ) => { const r = { minX, maxX, minZ, maxZ, active: true }; colliders.push(r); return r; };
const targets = [];

const ground = new THREE.Mesh(new THREE.PlaneGeometry(120, 120), mat(0x77a856)); ground.rotation.x = -Math.PI / 2; scene.add(ground);
const road = new THREE.Mesh(new THREE.PlaneGeometry(120, 6), mat(0x55585e)); road.rotation.x = -Math.PI / 2; road.position.set(0, .01, 17); scene.add(road);
for (let x = -50; x < 50; x += 4) { const l = new THREE.Mesh(new THREE.PlaneGeometry(2, .15), mat(0xeeeeee)); l.rotation.x = -Math.PI / 2; l.position.set(x, .02, 17); scene.add(l); }
for (const [x, z] of [[-14, -6], [-12, 8], [-18, 2], [16, -8], [20, -2], [-9, -16], [9, -15], [27, 4], [-16, -12]]) {
  box(.4, 1.4, .4, 0x7a5230, x, .7, z); const c = new THREE.Mesh(new THREE.ConeGeometry(1.4, 3, 7), mat(0x3f8a3a)); c.position.set(x, 2.8, z); scene.add(c);
}

// Garage (opening faces +z)
const GZ0 = -13, GZ1 = -7;
box(.15, 3, 6, 0xc8b89a, -2.95, 1.5, -10); box(.15, 3, 6, 0xc8b89a, 2.95, 1.5, -10); box(6, 3, .15, 0xc8b89a, 0, 1.5, -12.95);
box(6.3, .2, 6.3, 0x8f3b2b, 0, 3.1, -10);
const gFloor = new THREE.Mesh(new THREE.PlaneGeometry(5.8, 5.8), mat(0x9a9a92)); gFloor.rotation.x = -Math.PI / 2; gFloor.position.set(0, .015, -10); scene.add(gFloor);
rect(-3.05, -2.85, GZ0, GZ1); rect(2.85, 3.05, GZ0, GZ1); rect(-3, 3, -13.05, -12.85);
const door = box(5.8, 2.9, .08, 0xd9d4c6, 0, 1.45, -7.05); door.userData.kind = "door"; targets.push(door);
for (let i = 0; i < 7; i++) box(5.8, .03, .1, 0xbab4a3, 0, 0, 0, door).position.set(0, -1.15 + i * .4, .01);
const gLight = new THREE.PointLight(0xfff0d0, 18, 12, 1.4); gLight.position.set(0, 2.6, -10); scene.add(gLight);
const doorRect = rect(-3, 3, -7.15, -6.95);
const gLabel = labelMesh("YOUR LOT", 2.2, .5); gLabel.position.set(0, 3.45, -6.85); scene.add(gLabel);
let doorOpen = 1, doorTarget = 1;

// Lots board
box(.12, 2.2, .12, 0x6b4a2a, 3.6, 1.1, -5.5); box(.12, 2.2, .12, 0x6b4a2a, 5.4, 1.1, -5.5);
const board = labelMesh("LOTS FOR SALE\n▶ press E", 1.9, 1.1, "#3b2f26", "#ffd27a", 54); board.position.set(4.5, 1.7, -5.43); scene.add(board);
board.userData.kind = "board"; targets.push(board); rect(3.5, 5.5, -5.6, -5.4);

// Workbench
box(2, .1, 1, 0x9b6b3d, -6, .88, -2); for (const [dx, dz] of [[-.9, -.4], [.9, -.4], [-.9, .4], [.9, .4]]) box(.08, .85, .08, 0x6b4421, -6 + dx, .42, -2 + dz);
box(2, 1.2, .08, 0x6d5642, -6, 1.5, -2.55);
const benchLbl = labelMesh("WORKBENCH", 1.4, .3); benchLbl.position.set(-6, 1.95, -2.5); scene.add(benchLbl);
const benchTop = box(1.9, .02, .9, 0x9b6b3d, -6, .94, -2); benchTop.userData.kind = "bench"; targets.push(benchTop);
rect(-7.05, -4.95, -2.6, -1.45);
const BENCH_POS = new THREE.Vector3(-6, .95, -1.95);
const bench = { pos: BENCH_POS, item: null, active: true, kind: "bench" };

// Ultrasonic baths (hidden until bought)
const baths = [];
for (const [x, z] of [[-9.2, -2], [-9.2, .6]]) {
  const g = new THREE.Group(); scene.add(g);
  box(1.1, .6, .9, 0xe8eef2, x, .3, z, g);
  const water = new THREE.Mesh(new THREE.BoxGeometry(.95, .02, .75), new THREE.MeshLambertMaterial({ color: 0x5ec8ff })); water.position.set(x, .61, z); g.add(water);
  const lbl = labelMesh("ULTRASONIC BATH", 1.1, .22, "#16405a", "#bff0ff", 50); lbl.position.set(x, 1.05, z); lbl.rotation.y = Math.PI / 2; g.add(lbl);
  const b = { pos: new THREE.Vector3(x, .45, z), item: null, active: false, kind: "bath", group: g, r: rect(x - .55, x + .55, z - .45, z + .45) };
  water.userData.kind = "bath"; water.userData.slot = b; targets.push(water); baths.push(b);
}

// Trash container
const bin = new THREE.Mesh(new THREE.CylinderGeometry(.55, .45, 1.05, 12), mat(0x2f6b3f)); bin.position.set(-6, .52, 2.6); scene.add(bin);
bin.userData.kind = "trash"; targets.push(bin); rect(-6.6, -5.4, 2, 3.2);
const binLbl = labelMesh("RECYCLE JUNK", 1, .25, "#1d3d25", "#ffffff", 60); binLbl.position.set(-6, 1.3, 2.6); binLbl.rotation.y = Math.PI / 4; scene.add(binLbl);

// Shop: floor, tables with 4 slots each, computer, delivery crate, sign
const shopFloor = new THREE.Mesh(new THREE.PlaneGeometry(22, 7), mat(0xc79a62)); shopFloor.rotation.x = -Math.PI / 2; shopFloor.position.set(15.5, .012, 6.5); scene.add(shopFloor);
const slots = [];
function makeTable(cx) {
  const g = new THREE.Group(); scene.add(g);
  box(6, .1, 1, 0xa77a48, cx, .86, 8, g); for (const dx of [-2.9, 2.9]) for (const dz of [-.42, .42]) box(.08, .82, .08, 0x6b4421, cx + dx, .41, 8 + dz, g);
  const r = rect(cx - 3, cx + 3, 7.5, 8.5);
  const list = [];
  for (let i = 0; i < 4; i++) {
    const sx = cx - 2.25 + i * 1.5;
    const pad = new THREE.Mesh(new THREE.BoxGeometry(1.2, .02, .8), new THREE.MeshLambertMaterial({ color: 0xfff1d0 }));
    pad.position.set(sx, .92, 8); g.add(pad);
    const slot = { pos: new THREE.Vector3(sx, .93, 8), item: null, reserved: false, active: false, kind: "slot" };
    pad.userData.kind = "slot"; pad.userData.slot = slot; targets.push(pad); slots.push(slot); list.push(slot);
  }
  return { g, r, list };
}
const tables = [makeTable(9), makeTable(15.6), makeTable(22.2)];
box(1.2, .8, .7, 0x5b4636, 4.2, .4, 5); const mon = box(.1, .55, .8, 0x222222, 4.2, 1.1, 5);
const monLbl = labelMesh("COMPUTER\nupgrades · requests", .72, .48, "#10202f", "#7fe0ff", 52); monLbl.position.set(4.14, 1.1, 5); monLbl.rotation.y = -Math.PI / 2; scene.add(monLbl);
monLbl.userData.kind = "terminal"; mon.userData.kind = "terminal"; targets.push(monLbl, mon); rect(3.6, 4.8, 4.65, 5.35);
const crate = box(.9, .7, .9, 0xb07a3a, 2.6, .35, 7.4); crate.userData.kind = "deliver"; targets.push(crate); rect(2.15, 3.05, 6.95, 7.85);
const crateLbl = labelMesh("DELIVERY\nfor requests", .9, .45, "#2b2420", "#ffd27a", 70); crateLbl.position.set(2.6, 1.0, 7.86); crateLbl.rotation.y = Math.PI; scene.add(crateLbl);
const crateLbl2 = crateLbl.clone(); crateLbl2.rotation.y = 0; crateLbl2.position.z = 6.94; scene.add(crateLbl2);
const shopSign = new THREE.Group(); scene.add(shopSign);
box(.15, 3.2, .15, 0x6b4a2a, 6, 1.6, 9.2, shopSign); box(.15, 3.2, .15, 0x6b4a2a, 18.6, 1.6, 9.2, shopSign);
const signLbl = labelMesh("JUNK & WONDERS", 7, .9, "#c23b22", "#fff6d8", 110); signLbl.position.set(12.3, 3, 9.25); signLbl.rotation.y = Math.PI; shopSign.add(signLbl);
const signLbl2 = signLbl.clone(); signLbl2.rotation.y = 0; signLbl2.position.z = 9.15; shopSign.add(signLbl2);
const billboard = new THREE.Group(); scene.add(billboard);
box(.2, 4, .2, 0x555555, -8, 2, 19.5, billboard); box(.2, 4, .2, 0x555555, -2, 2, 19.5, billboard);
const bbLbl = labelMesh("JUNK & WONDERS\nwe buy everything", 6.4, 2.2, "#ffb02e", "#2b2420", 80); bbLbl.position.set(-5, 4.5, 19.4); bbLbl.rotation.y = Math.PI; billboard.add(bbLbl);

function applyUpgrades() {
  F = fx();
  tables.forEach((t, i) => { const on = i < F.tables; t.g.visible = on; t.r.active = on; t.list.forEach((s) => (s.active = on)); });
  baths.forEach((b, i) => { const on = i < F.baths; b.group.visible = on; b.r.active = on; b.active = on; });
  shopSign.visible = !!S.up.sign; billboard.visible = !!S.up.billboard;
}

// ---------------------------------------------------------------- items
const items = [];
const DIRT = new THREE.Color(0x5b4a36);
const spotGeo = new THREE.SphereGeometry(1, 6, 4);
const spotMat = new THREE.MeshLambertMaterial({ color: 0x3e2f1f });

function partMesh(p) {
  let g;
  if (p.s === "box") g = new THREE.BoxGeometry(p.sx, p.sy, p.sz);
  else if (p.s === "cyl") g = new THREE.CylinderGeometry(p.sx, p.sx, p.sy, 10);
  else if (p.s === "cone") g = new THREE.ConeGeometry(p.sx, p.sy, 10);
  else if (p.s === "tor") g = new THREE.TorusGeometry(p.sx, p.sz, 6, 16);
  else g = new THREE.SphereGeometry(1, 10, 8);
  const m = new THREE.Mesh(g, mat(p.c)); m.material.userData.clean = new THREE.Color(p.c);
  if (p.s === "sph") m.scale.set(p.sx, p.sy, p.sz);
  m.position.set(p.x, p.y, p.z); return m;
}

function createItem(id, saved) {
  const def = ITEMS[id]; if (!def) return null;
  const group = new THREE.Group();
  const meshes = def.parts.map(partMesh); meshes.forEach((m) => group.add(m));
  const bb = new THREE.Box3().setFromObject(group), size = bb.getSize(new THREE.Vector3());
  const it = { id, def, name: def.name, value: def.value, junk: !!def.junk, mystery: !!def.mystery, group, meshes, size, maxDim: Math.max(size.x, size.y, size.z),
    condition: BALANCE.startCondition[0] + Math.random() * (BALANCE.startCondition[1] - BALANCE.startCondition[0]),
    rare: !!(def.rare && Math.random() < def.rare.chance * F.rare), shinyDone: false, place: "ground", holder: null, tag: null, spots: [] };
  if (saved) Object.assign(it, { condition: saved.c, name: saved.n, value: saved.v, junk: saved.j, mystery: saved.m, rare: saved.r, shinyDone: saved.s });
  for (let i = 0; i < 8; i++) {
    const s = new THREE.Mesh(spotGeo, spotMat); const r = .03 + Math.random() * .05; s.scale.set(r, r * .35, r);
    const face = Math.floor(Math.random() * 3);
    s.position.set(bb.min.x + Math.random() * size.x, face === 0 ? bb.max.y : bb.min.y + Math.random() * size.y, face === 1 ? bb.max.z : bb.min.z + Math.random() * size.z);
    if (face === 2) s.position.x = Math.random() < .5 ? bb.min.x : bb.max.x;
    s.userData.th = .15 + i * .1; group.add(s); it.spots.push(s);
  }
  group.traverse((o) => { o.userData.item = it; if (o.isMesh) targets.push(o); });
  applyCondition(it); scene.add(group); items.push(it); return it;
}
function applyCondition(it) {
  const k = (1 - it.condition) * .72;
  for (const m of it.meshes) m.material.color.copy(m.material.userData.clean).lerp(DIRT, k);
  for (const s of it.spots) s.visible = it.condition < s.userData.th;
}
function removeItem(it) {
  if (it.holder) { it.holder.item = null; it.holder.reserved = false; it.holder = null; }
  if (it.tag) { it.tag.parent && it.tag.parent.remove(it.tag); it.tag = null; }
  it.group.parent && it.group.parent.remove(it.group);
  it.group.traverse((o) => { const i = targets.indexOf(o); if (i >= 0) targets.splice(i, 1); });
  const i = items.indexOf(it); if (i >= 0) items.splice(i, 1);
}
function setScaleFit(it, maxDim) { const s = Math.min(1, maxDim / it.maxDim); it.group.scale.setScalar(s); return s; }
function basePrice(it) { const c = it.condition, v = it.value; return v * (BALANCE.dirtyFloor + (1 - BALANCE.dirtyFloor) * c); }
function priceOf(it) { if (it.junk) return F.junk; return Math.max(1, Math.round(basePrice(it) * F.price * (1 + BALANCE.levelPriceBonus * (S.lvl - 1)))); }

// ---------------------------------------------------------------- particles + marker
const parts = []; const pGeo = new THREE.BoxGeometry(.03, .03, .03);
function burst(pos, color, n = 8, speed = 1.5, life = .6) {
  for (let i = 0; i < n; i++) {
    const m = new THREE.Mesh(pGeo, new THREE.MeshBasicMaterial({ color })); m.position.copy(pos); scene.add(m);
    parts.push({ m, v: new THREE.Vector3((Math.random() - .5) * speed, Math.random() * speed, (Math.random() - .5) * speed), life, max: life });
  }
}
const marker = new THREE.Mesh(new THREE.ConeGeometry(.22, .45, 4), new THREE.MeshBasicMaterial({ color: 0xffd23f, depthTest: false }));
marker.rotation.x = Math.PI; marker.renderOrder = 10; scene.add(marker); marker.visible = false;

// ---------------------------------------------------------------- UI helpers
function money(n) { return "$" + Math.round(n).toLocaleString("en-US"); }
function toast(html, cls = "") { const t = document.createElement("div"); t.className = "toast " + cls; t.innerHTML = html; $("toasts").appendChild(t); while ($("toasts").children.length > 5) $("toasts").firstChild.remove(); setTimeout(() => t.remove(), 4200); }
function unlock(id) {
  if (S.ach[id]) return; const a = ACHIEVEMENTS.find((x) => x.id === id); if (!a) return;
  S.ach[id] = Date.now(); sfx.ach(); toast(`🏆 Achievement unlocked: <b>${a.name}</b><small>${a.desc}</small>`, "ach"); save();
  if (ACHIEVEMENTS.every((x) => S.ach[x.id])) setTimeout(finale, 1500);
}
function earn(n) {
  S.money += n; S.stats.earned += n;
  if (S.stats.earned >= 1000) unlock("grand"); if (S.stats.earned >= 10000) unlock("rich");
}
function addXP(n) {
  S.xp += Math.round(n * F.xp);
  let need = BALANCE.xpForLevel(S.lvl);
  while (S.xp >= need) {
    S.xp -= need; S.lvl++; need = BALANCE.xpForLevel(S.lvl);
    sfx.level(); toast(`⭐ <b>Level ${S.lvl}!</b><small>+${Math.round(BALANCE.levelPriceBonus * 100)}% sale prices. New upgrades may be unlocked.</small>`, "ach");
    burst(camera.position.clone().add(new THREE.Vector3(0, .2, 0)).addScaledVector(forward(), 1.5), 0xffd23f, 30, 2.5, 1);
    if (S.lvl >= 5) unlock("lvl5"); if (S.lvl >= 10) unlock("lvl10");
  }
}
function forward() { return new THREE.Vector3(-Math.sin(yaw), 0, -Math.cos(yaw)); }
function updateHUD() {
  $("hud-money").textContent = money(S.money);
  const need = BALANCE.xpForLevel(S.lvl);
  $("hud-lvl").innerHTML = `Lv <b>${S.lvl}</b> <span class="bar"><i style="width:${Math.min(100, S.xp / need * 100)}%"></i></span> ${S.xp}/${need} XP`;
  const got = ACHIEVEMENTS.filter((a) => S.ach[a.id]).length;
  $("hud-ach").textContent = `🏆 ${got}/${ACHIEVEMENTS.length} (Tab)`;
  const st = streak.n > 1 && performance.now() / 1000 - streak.last < BALANCE.streakWindow;
  $("hud-streak").hidden = !st; if (st) $("hud-streak").textContent = `🔥 x${streak.n} streak  +${Math.round((streak.n - 1) * BALANCE.streakBonus * 100)}%`;
  // tutorial or goal
  let html;
  if (S.tut >= 0 && S.tut < TUTORIAL.length) html = `<div class="tut-h">Tutorial ${S.tut + 1}/${TUTORIAL.length}</div>${TUTORIAL[S.tut].text}<div class="tut-skip">T = skip tutorial</div>`;
  else {
    const inGarage = items.filter((i) => i.place === "garage").length;
    if (inGarage) html = `${inGarage} items left in your lot.`;
    else html = `Garage empty: buy another lot at the <b>LOTS</b> board.`;
  }
  if ($("hud-goal").innerHTML !== html) $("hud-goal").innerHTML = html;
  const qh = S.quests.map((q) => `<div class="q ${q.done ? "done" : ""}"><span>${q.text}</span><b>${q.n > 1 ? `${Math.min(q.prog, q.n)}/${q.n}` : ""}</b><em>${money(q.reward)}</em></div>`).join("");
  const qhtml = S.quests.length && S.tut < 0 ? `<div class="qh">📋 Requests</div>${qh}` : "";
  if ($("hud-quests").innerHTML !== qhtml) $("hud-quests").innerHTML = qhtml;
}

// ---------------------------------------------------------------- requests (quests)
function unlockedTiers() { return LOTS.filter((l) => !l.needs || S.up[l.needs]).map((l) => l.tier); }
function pick(arr) { return arr[Math.floor(Math.random() * arr.length)]; }
function newQuest() {
  const tiers = unlockedTiers(), top = Math.max(...tiers);
  const goods = Object.entries(ITEMS).filter(([, d]) => tiers.includes(d.tier) && !d.junk && !d.mystery);
  const types = ["restore", "deliver", "deliver", "sell", "trash", "earn", "lot"].filter((t) => !S.quests.some((q) => q.type === t && t !== "deliver"));
  const type = pick(types); let q;
  if (type === "restore") { const [id, d] = pick(goods); q = { type, item: id, n: 1, text: `Restore to 100%: ${d.name}`, reward: Math.round(d.value * .8 + 20), xp: 40 }; }
  else if (type === "deliver") { const [id, d] = pick(goods); q = { type, item: id, n: 1, text: `Deliver (80%+ clean): ${d.name}`, reward: Math.round(d.value * 2.2 + 15), xp: 60 }; }
  else if (type === "sell") { const n = 3 + Math.floor(Math.random() * 5); q = { type, n, text: `Sell ${n} items in your shop`, reward: Math.round(12 * n * top * top), xp: 40 }; }
  else if (type === "trash") { const n = 3 + Math.floor(Math.random() * 4); q = { type, n, text: `Recycle ${n} junk items`, reward: 10 * n * top, xp: 25 }; }
  else if (type === "earn") { const amt = 150 * top * top * (1 + Math.floor(Math.random() * 3)); q = { type, n: amt, text: `Earn ${money(amt)} from sales`, reward: Math.round(amt * .25), xp: 50 }; }
  else { const lot = LOTS.filter((l) => tiers.includes(l.tier)).pop(); q = { type: "lot", lot: lot.id, n: 1, text: `Buy a lot: ${lot.name}`, reward: Math.round(lot.price * .35 + 10), xp: 35 }; }
  q.prog = 0; q.done = false; q.id = Math.random().toString(36).slice(2);
  return q;
}
function fillQuests() { while (S.quests.length < 3) S.quests.push(newQuest()); }
function questEvent(type, data = {}) {
  for (const q of S.quests) {
    if (q.done || q.type !== type) continue;
    if (type === "restore" && data.id !== q.item) continue;
    if (type === "lot" && data.lot !== q.lot) continue;
    q.prog += data.amount || 1;
    if (q.prog >= q.n) completeQuest(q);
  }
}
function completeQuest(q) {
  q.done = true; earn(q.reward); addXP(q.xp); S.stats.requests++; sfx.quest();
  toast(`📋 Request complete: <b>${q.text}</b><small>+${money(q.reward)} · +${q.xp} XP</small>`, "ach");
  unlock("request1"); if (S.stats.requests >= 10) unlock("request10");
  setTimeout(() => { S.quests = S.quests.filter((x) => x !== q); fillQuests(); save(); }, 2500);
}

// ---------------------------------------------------------------- panels
let panelOpen = false;
function openPanel(html, bind) {
  panelOpen = true; scrubbing = null; keys.clear();
  if (document.pointerLockElement) document.exitPointerLock();
  $("panel-body").innerHTML = html + `<div style="text-align:right;margin-top:10px"><button class="ghost" id="p-close">Back to game (Esc)</button></div>`;
  $("panel").hidden = false; $("p-close").onclick = closePanel; bind && bind();
}
function closePanel() { $("panel").hidden = true; panelOpen = false; lockPointer(); }
function lotsPanel() {
  const rows = LOTS.map((l) => {
    const need = l.needs && UPGRADES.find((u) => u.id === l.needs), locked = need && !S.up[l.needs];
    return `<div class="row"><div class="t"><b>${l.name} — ${money(l.price)}</b><span>${locked ? "🔒 Needs the " + need.name + " upgrade" : l.hint}</span></div>
      <button data-lot="${l.id}" ${locked || S.money < l.price ? "disabled" : ""}>Buy</button></div>`;
  }).join("");
  openPanel(`<h2>Lots for sale</h2><p class="sub">You have ${money(S.money)}. What's inside? Nobody knows. That's the fun.</p>${rows}`, () => {
    document.querySelectorAll("[data-lot]").forEach((b) => (b.onclick = () => { buyLot(LOTS.find((l) => l.id === b.dataset.lot)); closePanel(); }));
  });
}
function computerPanel(tab = "up") {
  S.flags.sawComputer = 1; if (tab === "req") S.flags.sawRequests = 1;
  const tabs = `<div class="tabs"><button class="${tab === "up" ? "" : "ghost"}" data-tab="up">Upgrades</button><button class="${tab === "req" ? "" : "ghost"}" data-tab="req">Requests</button><button class="${tab === "stats" ? "" : "ghost"}" data-tab="stats">Stats</button></div>`;
  let body = "";
  if (tab === "up") {
    let cat = "";
    for (const u of UPGRADES) {
      if (u.cat !== cat) { cat = u.cat; body += `<div class="cat">${cat}</div>`; }
      const owned = S.up[u.id], needU = u.needs && !S.up[u.needs], needL = S.lvl < u.lvl;
      const why = needU ? "🔒 Needs " + UPGRADES.find((x) => x.id === u.needs).name : needL ? `🔒 Level ${u.lvl}` : u.desc;
      body += `<div class="row"><div class="t"><b>${u.name} — ${money(u.price)}</b><span>${why}</span></div>
        ${owned ? '<span class="owned">Owned ✓</span>' : `<button data-up="${u.id}" ${needU || needL || S.money < u.price ? "disabled" : ""}>Buy</button>`}</div>`;
    }
  } else if (tab === "req") {
    body = `<p class="sub">People online want things. Requests refresh when you complete them.</p>` + S.quests.map((q) =>
      `<div class="row"><div class="t"><b>${q.done ? "✅ " : ""}${q.text}</b><span>Progress ${Math.min(q.prog, q.n)}/${q.n} · reward ${money(q.reward)} + ${q.xp} XP</span></div></div>`).join("");
  } else {
    const st = S.stats;
    body = `<div class="row"><div class="t"><b>Level ${S.lvl}</b><span>Sale price bonus +${Math.round(BALANCE.levelPriceBonus * (S.lvl - 1) * 100)}%</span></div></div>
      <div class="row"><div class="t"><b>Lots bought: ${st.lots} · Items sold: ${st.sold}</b><span>Junk recycled: ${st.trashed} · Requests done: ${st.requests} · Best streak: x${st.bestStreak}</span></div></div>
      <div class="row"><div class="t"><b>Total earned: ${money(st.earned)}</b><span>Most expensive sale: ${money(st.best)}</span></div></div>
      <p class="sub">Version ${VERSION} · Little Loop Games</p>`;
  }
  openPanel(`<h2>Computer</h2><p class="sub">You have ${money(S.money)} · Level ${S.lvl}</p>${tabs}${body}`, () => {
    document.querySelectorAll("[data-tab]").forEach((b) => (b.onclick = () => computerPanel(b.dataset.tab)));
    document.querySelectorAll("[data-up]").forEach((b) => (b.onclick = () => {
      const u = UPGRADES.find((x) => x.id === b.dataset.up); if (S.money < u.price) return;
      S.money -= u.price; S.up[u.id] = 1; applyUpgrades(); sfx.cash(); addXP(20); unlock("tool_up");
      toast(`🔧 <b>${u.name}</b> installed!<small>${u.desc}</small>`);
      if (UPGRADES.every((x) => S.up[x.id])) unlock("allup");
      save(); computerPanel("up");
    }));
  });
}
function achPanel() {
  const rows = ACHIEVEMENTS.map((a) => {
    const got = S.ach[a.id];
    return `<div class="row ${got ? "" : "locked"}"><div class="t"><b>${got ? "🏆" : "🔒"} ${a.secret && !got ? "???" : a.name}</b><span>${a.secret && !got ? "Secret achievement" : a.desc}</span></div></div>`;
  }).join("");
  const got = ACHIEVEMENTS.filter((a) => S.ach[a.id]).length;
  openPanel(`<h2>Achievements ${got}/${ACHIEVEMENTS.length}</h2><p class="sub">Collect them all to finish the game.</p><div class="achlist">${rows}</div>
    <div style="margin-top:8px"><button class="ghost" id="p-reset">Reset progress</button></div>`, () => {
    $("p-reset").onclick = () => { if (confirm("Delete all progress?")) { try { localStorage.removeItem(SAVE_KEY); } catch (e) {} resetting = true; location.reload(); } };
  });
}
let resetting = false;
function finale() {
  openPanel(`<h2>🏆 100% — Junk Lord of the Year!</h2><p class="sub">You collected every achievement.</p>
    <p>Lots bought: <b>${S.stats.lots}</b> · Items sold: <b>${S.stats.sold}</b> · Total earned: <b>${money(S.stats.earned)}</b></p>
    <p>Thanks for playing the prototype! Keep playing as long as you like.</p>`);
  sfx.level(); for (let i = 0; i < 6; i++) setTimeout(() => burst(camera.position.clone().addScaledVector(forward(), 2), 0xffd23f, 30, 3, 1.2), i * 250);
}

// ---------------------------------------------------------------- lots
function buyLot(lot) {
  if (S.money < lot.price) return sfx.no();
  S.money -= lot.price; S.stats.lots++; addXP(15 * lot.tier); unlock("first_lot");
  if (lot.id === "student") unlock("student"); if (lot.id === "pizzeria") unlock("pizza"); if (lot.id === "circus") unlock("circus");
  questEvent("lot", { lot: lot.id });
  const left = items.filter((i) => i.place === "garage"); if (left.length) { left.forEach(removeItem); toast(`Leftovers from the last lot were hauled away.`); }
  const ids = rollLot(lot);
  const cells = []; for (let gx = 0; gx < 3; gx++) for (let gz = 0; gz < 3; gz++) cells.push([-1.8 + gx * 1.8, -11.9 + gz * 1.5]);
  cells.sort(() => Math.random() - .5);
  ids.forEach((id, i) => {
    const it = createItem(id); it.place = "garage";
    const [x, z] = cells[i % cells.length]; it.group.position.set(x + (Math.random() - .5) * .5, 0, z + (Math.random() - .5) * .4);
    it.group.rotation.y = Math.random() * Math.PI * 2;
  });
  doorOpen = 0; doorTarget = 1; sfx.door(); save();
  toast(`You bought <b>${lot.name}</b>. The door is opening...`);
}

// ---------------------------------------------------------------- input
const keys = new Set();
let yaw = 0, pitch = 0, started = false, fallbackLook = false, scrubbing = null, carrying = null, aim = null;
const streak = { n: 0, last: -99 };
function lockPointer() { if (fallbackLook || !started) return; try { const p = renderer.domElement.requestPointerLock(); if (p && p.catch) p.catch(() => (fallbackLook = true)); } catch (e) { fallbackLook = true; } }
document.addEventListener("pointerlockerror", () => { if (!fallbackLook) { fallbackLook = true; toast("Mouse look without pointer lock: just move the mouse."); } });
document.addEventListener("pointerlockchange", () => {
  if (!document.pointerLockElement && started && !panelOpen && !fallbackLook) openPanel(`<h2>Paused</h2><p class="sub">Your junk is waiting.</p>`);
});
$("btn-play").onclick = () => { $("start").hidden = true; started = true; audio(); lockPointer(); };

addEventListener("keydown", (e) => {
  if (!started) return;
  if (e.code === "Tab") { e.preventDefault(); panelOpen ? closePanel() : achPanel(); return; }
  if (e.code === "Escape" && panelOpen) { closePanel(); return; }
  if (panelOpen) return;
  keys.add(e.code);
  if (e.code === "KeyE") interact();
  if (e.code === "KeyT" && S.tut >= 0) { S.tut = -1; fillQuests(); toast("Tutorial skipped. Requests are on the computer."); save(); }
});
addEventListener("keyup", (e) => keys.delete(e.code));
addEventListener("blur", () => keys.clear());
renderer.domElement.addEventListener("mousedown", (e) => {
  if (!started || panelOpen) return;
  if (!document.pointerLockElement && !fallbackLook) { lockPointer(); return; }
  if (e.button !== 0) return;
  if (!carrying && aim && aim.item && aim.item.place === "bench" && aim.item.condition < 1) { scrubbing = aim.item; return; }
  interact();
});
addEventListener("mouseup", () => { scrubbing = null; if (noiseGain) noiseGain.gain.value = 0; });
addEventListener("mousemove", (e) => {
  if (!started || panelOpen) return;
  if (!document.pointerLockElement && !fallbackLook) return;
  const dx = e.movementX || 0, dy = e.movementY || 0;
  if (scrubbing) { scrub(scrubbing, Math.hypot(dx, dy)); return; }
  yaw -= dx * .0024; pitch = Math.max(-1.45, Math.min(1.45, pitch - dy * .0024));
});

let lastScrubFx = 0;
function scrub(it, px) {
  if (it.condition >= 1) return;
  it.condition = Math.min(1, it.condition + px * BALANCE.scrubPerPixel * F.clean);
  applyCondition(it);
  if (noiseGain) noiseGain.gain.value = Math.min(.12, px * .004);
  const now = performance.now();
  if (now - lastScrubFx > 60) { lastScrubFx = now; burst(BENCH_POS.clone().add(new THREE.Vector3((Math.random() - .5) * .4, .15 + Math.random() * .2, .2)), 0x6b5236, 3, 1.2, .4); }
  if (it.condition >= 1) { if (noiseGain) noiseGain.gain.value = 0; scrubbing = null; onCleaned(it, BENCH_POS); }
}
function onCleaned(it, pos, auto = false) {
  if (it.shinyDone) return; it.shinyDone = true;
  sfx.shiny(); burst(pos.clone().add(new THREE.Vector3(0, .3, 0)), 0xfff3a0, 24, 2.2, .9);
  S.stats.shinies++; unlock("shiny"); if (auto) unlock("automation");
  addXP(it.junk ? 2 : 8 + Math.round(it.value / 20));
  if (it.mystery) {
    unlock("mystery"); const r = Math.random(), tier = it.def.tier;
    if (r < .12) { it.name = "Golden Pocket Watch"; it.value = 700 * tier; it.junk = false; toast(`📦 The box held a <b>${it.name}</b>! Worth ${money(priceOf(it))}!`, "ach"); unlock("jackpot"); }
    else if (r < .6) { it.name = "Box of Old Coins"; it.value = Math.round((60 + Math.random() * 180) * tier); it.junk = false; toast(`📦 The box held <b>old coins</b>. Worth ${money(priceOf(it))}.`); }
    else { it.name = "A Smaller Box (Empty)"; it.value = 0; it.junk = true; toast(`📦 Inside the box... a smaller box. It's empty. Recycle it.`); }
    return;
  }
  if (it.rare) { it.name = it.def.rare.name; it.value = it.def.rare.value; unlock("jackpot"); toast(`💎 <b>${it.name}</b><small>It's worth ${money(priceOf(it))}!</small>`, "ach"); }
  else if (!it.junk) toast(`✨ <b>${it.name}</b> is like new! Worth ${money(priceOf(it))}.`);
  questEvent("restore", { id: it.id });
}

// ---------------------------------------------------------------- interaction
const ray = new THREE.Raycaster(); const center = new THREE.Vector2(0, 0);
function findAim() {
  ray.setFromCamera(center, camera); ray.far = 4.2;
  const hits = ray.intersectObjects(targets, false);
  for (const h of hits) {
    const o = h.object;
    let vis = true; o.traverseAncestors((a) => { if (a.visible === false) vis = false; }); if (!vis || !o.visible) continue;
    if (o.userData.item) { if (o.userData.item === carrying) continue; if (h.distance > 3.4) return null; return { item: o.userData.item, point: h.point }; }
    const k = o.userData.kind; if (!k) continue;
    if ((k === "slot" || k === "bath") && !o.userData.slot.active) continue;
    return { kind: k, slot: o.userData.slot, point: h.point, dist: h.distance };
  }
  return null;
}
function pickUp(it) {
  if (it.holder && it.holder.reserved) return sfx.no();
  if (it.holder) { it.holder.item = null; it.holder = null; }
  if (it.tag) { it.tag.parent.remove(it.tag); it.tag = null; }
  scene.remove(it.group); camera.add(it.group);
  it.group.position.set(.42, -.42, -.95); it.group.rotation.set(.15, -.5, 0); setScaleFit(it, .5);
  it.place = "carry"; carrying = it; sfx.pick();
  if (it.junk && !S.flags.junkTip) { S.flags.junkTip = 1; toast("This is <b>junk</b>. Recycle it in the green bin for a little cash."); }
}
function putDown(it, pos, place, fit = 9, holder = null) {
  camera.remove(it.group); scene.add(it.group);
  setScaleFit(it, fit); it.group.position.copy(pos); it.group.rotation.set(0, place === "slot" ? 0 : yaw, 0);
  it.place = place; carrying = null; sfx.drop();
  if (holder) { it.holder = holder; holder.item = it; }
}
function placeOnSlot(it, slot) {
  putDown(it, slot.pos, "slot", 1.0, slot);
  it.tag = priceSprite(money(priceOf(it))); it.tag.position.set(slot.pos.x, slot.pos.y + Math.min(1.2, it.size.y * it.group.scale.x) + .25, slot.pos.z - .3); scene.add(it.tag);
  if (slots.filter((s) => s.active).every((s) => s.item)) unlock("full_shop");
}
function interact() {
  const a = aim;
  if (carrying) {
    const it = carrying;
    if (a && a.kind === "bench") { if (bench.item) return toast("The workbench is busy. Take that item off first."); return putDown(it, BENCH_POS, "bench", 1.1, bench); }
    if (a && a.kind === "bath") { if (a.slot.item) return toast("This bath is busy."); if (it.condition >= 1) return toast("It's already spotless!"); return putDown(it, a.slot.pos, "bath", .8, a.slot); }
    if (a && a.kind === "slot") { if (a.slot.item) return toast("That spot is taken."); return placeOnSlot(it, a.slot); }
    if (a && a.kind === "deliver") return deliver(it);
    if (a && a.kind === "trash") {
      camera.remove(it.group); removeItem(it); carrying = null; sfx.trash(); burst(bin.position.clone().add(new THREE.Vector3(0, .6, 0)), 0x555555, 10);
      if (it.junk) { earn(F.junk); addXP(2); S.stats.trashed++; if (S.stats.trashed >= 10) unlock("trash10"); questEvent("trash"); toast(`Junk recycled: +${money(F.junk)}`); }
      else toast(`You threw away ${it.name}. It was worth ${money(priceOf(it))}... bold.`);
      save(); return;
    }
    const f = forward();
    return putDown(it, new THREE.Vector3(camera.position.x + f.x * 1.3, 0, camera.position.z + f.z * 1.3), "ground");
  }
  if (!a) return;
  if (a.item) return pickUp(a.item);
  if (a.kind === "board") return lotsPanel();
  if (a.kind === "terminal") return computerPanel(S.tut === 6 ? "req" : "up");
  if (a.kind === "door") return toast("Buy a lot at the LOTS board to open the garage.");
  if (a.kind === "deliver") return toast("Bring an item that someone requested. See Requests on the computer.");
}
function deliver(it) {
  const q = S.quests.find((x) => !x.done && x.type === "deliver" && x.item === it.id);
  if (!q) return toast("Nobody requested this item. Check the Requests tab on the computer.");
  if (it.condition < .8) return toast(`They want it in 80%+ condition. This one is ${Math.round(it.condition * 100)}%. Clean it first!`);
  camera.remove(it.group); removeItem(it); carrying = null; burst(crate.position.clone().add(new THREE.Vector3(0, .6, 0)), 0xffd27a, 16, 2);
  completeQuest(q); save();
}
function hintFor(a) {
  if (carrying) {
    const n = `<b>${carrying.name}</b>`;
    if (a && a.kind === "bench") return `<b>E</b> place ${n} on the workbench`;
    if (a && a.kind === "bath") return a.slot.item ? "Bath busy" : `<b>E</b> put ${n} in the bath (cleans by itself)`;
    if (a && a.kind === "slot") return a.slot.item ? "Spot taken" : `<b>E</b> sell ${n} for <b>${money(priceOf(carrying))}</b>`;
    if (a && a.kind === "trash") return carrying.junk ? `<b>E</b> recycle junk (+${money(F.junk)})` : `<b>E</b> throw away?! (worth ${money(priceOf(carrying))})`;
    if (a && a.kind === "deliver") return `<b>E</b> deliver ${n} for a request`;
    return `<b>E</b> drop ${n}`;
  }
  if (!a) return "";
  if (a.item) {
    const it = a.item, c = Math.round(it.condition * 100);
    const info = it.junk ? "junk: recycle it" : it.mystery && !it.shinyDone ? `${c}% · clean it to open!` : `${c}% · ${money(priceOf(it))}`;
    if (it.place === "bench") return it.condition >= 1 ? `<b>${it.name}</b> is spotless · <b>E</b> pick up` : `<b>Hold click + move mouse</b> to scrub · <b>E</b> pick up · ${info}`;
    if (it.place === "bath") return `<b>${it.name}</b> bubbling... ${c}% · <b>E</b> take out`;
    if (it.place === "slot") return `<b>${it.name}</b> on sale for ${money(priceOf(it))} · <b>E</b> take back`;
    return `<b>E</b> pick up <b>${it.name}</b> · ${info}`;
  }
  return { board: "<b>E</b> browse lots", terminal: "<b>E</b> computer: upgrades & requests", door: "Your garage. Buy a lot to open it.", bench: "Workbench: bring an item here", slot: "Shop table: bring an item to sell", trash: "Recycle junk here", deliver: "Delivery crate: bring requested items here", bath: "Ultrasonic bath: drop a dirty item in" }[a.kind] || "";
}

// ---------------------------------------------------------------- customers
const customers = []; let custTimer = 3;
const bodyGeo = new THREE.CylinderGeometry(.22, .26, 1.1, 8), headGeo = new THREE.SphereGeometry(.2, 10, 8);
const custColors = [0x8fa3b8, 0xb89f8f, 0x9fb88f, 0xb88fae, 0xa8a8a8];
function spawnCustomer() {
  const free = slots.filter((s) => s.active && s.item && !s.reserved); if (!free.length) return;
  const slot = free[Math.floor(Math.random() * free.length)]; slot.reserved = true;
  const g = new THREE.Group(), c = custColors[Math.floor(Math.random() * custColors.length)];
  const b = new THREE.Mesh(bodyGeo, mat(c)); b.position.y = .55; g.add(b);
  const h = new THREE.Mesh(headGeo, mat(0xe6d6c4)); h.position.y = 1.32; g.add(h);
  g.position.set(slot.pos.x + (Math.random() - .5) * 8, 0, 20); scene.add(g);
  customers.push({ g, slot, state: "in", t: 0, target: new THREE.Vector3(slot.pos.x, 0, 8.95) });
}
function sell(it) {
  const now = performance.now() / 1000;
  streak.n = now - streak.last < BALANCE.streakWindow ? Math.min(5, streak.n + 1) : 1; streak.last = now;
  S.stats.bestStreak = Math.max(S.stats.bestStreak, streak.n); if (streak.n >= 5) unlock("streak5");
  const p = Math.round(priceOf(it) * (1 + (streak.n - 1) * BALANCE.streakBonus));
  earn(p); addXP(5 + Math.round(p / 15)); S.stats.sold++; S.stats.best = Math.max(S.stats.best, p);
  unlock("first_sale"); if (S.stats.sold >= 50) unlock("sold50"); if (p >= 1000) unlock("whale");
  questEvent("sell"); questEvent("earn", { amount: p });
  sfx.cash(); burst(it.group.position.clone().add(new THREE.Vector3(0, .5, 0)), 0x5fd38d, 10, 1.6);
  toast(`Sold <b>${it.name}</b> for <b>${money(p)}</b>${streak.n > 1 ? ` · 🔥x${streak.n}` : ""}`);
  removeItem(it); save();
}
function updateCustomers(dt) {
  custTimer -= dt;
  if (custTimer <= 0) { custTimer = BALANCE.customerEvery / F.cust * (.7 + Math.random() * .6); spawnCustomer(); }
  for (let i = customers.length - 1; i >= 0; i--) {
    const c = customers[i]; c.t += dt;
    if (c.state === "in" || c.state === "out") {
      const d = c.target.clone().sub(c.g.position); d.y = 0; const L = d.length();
      if (L < .05) {
        if (c.state === "in") { c.state = "browse"; c.t = 0; }
        else { scene.remove(c.g); customers.splice(i, 1); continue; }
      } else { d.multiplyScalar(Math.min(1, 1.9 * dt / L)); c.g.position.add(d); c.g.rotation.y = Math.atan2(d.x, d.z); }
      c.g.position.y = Math.abs(Math.sin(c.t * 9)) * .05;
    } else if (c.state === "browse") {
      c.g.rotation.y = Math.PI; c.g.children[1].position.y = 1.32 + Math.sin(c.t * 4) * .03;
      if (c.t > 1.4) {
        if (c.slot.item) sell(c.slot.item);
        c.slot.reserved = false; c.state = "out"; c.target = new THREE.Vector3(c.g.position.x + (Math.random() - .5) * 6, 0, 21);
      }
    }
  }
}

// ---------------------------------------------------------------- tutorial
function tutorialDone(i) {
  switch (i) {
    case 0: return S.stats.lots >= 1;
    case 1: return !!carrying || items.some((x) => x.place === "bench" || x.place === "slot");
    case 2: return !!bench.item || S.stats.shinies > 0;
    case 3: return S.stats.shinies > 0;
    case 4: return slots.some((s) => s.item) || S.stats.sold > 0;
    case 5: return S.stats.sold > 0;
    case 6: return !!S.flags.sawRequests;
    case 7: return Object.keys(S.up).length > 0;
  }
  return false;
}
function updateTutorial() {
  if (S.tut < 0 || S.tut >= TUTORIAL.length) return;
  if (S.tut === 6 && !S.quests.length) fillQuests();
  if (tutorialDone(S.tut)) {
    const st = TUTORIAL[S.tut]; if (st.reward) { earn(st.reward); toast(`✔ Step done! +${money(st.reward)}`); }
    addXP(10); S.tut++;
    if (S.tut >= TUTORIAL.length) { S.tut = -1; unlock("tutorial"); fillQuests(); toast("🎓 Tutorial complete! Now: requests, upgrades, bigger lots. Get every achievement!", "ach"); }
    save();
  }
}
function markerTarget() {
  if (S.tut < 0 || panelOpen) return null;
  const t = TUTORIAL[S.tut].target;
  if (t === "board") return new THREE.Vector3(4.5, 2.9, -5.4);
  if (t === "garage") { const g = items.find((i) => i.place === "garage"); return g ? g.group.position.clone().add(new THREE.Vector3(0, 1.4, 0)) : new THREE.Vector3(0, 2.5, -9); }
  if (t === "bench") return carrying || bench.item ? new THREE.Vector3(-6, 2.0, -1.95) : null;
  if (t === "table") { const s = slots.find((x) => x.active && !x.item) || slots[0]; return new THREE.Vector3(s.pos.x, 2.0, s.pos.z); }
  if (t === "computer") return new THREE.Vector3(4.2, 2.1, 5);
  return null;
}

// ---------------------------------------------------------------- save / load world
function serializeWorld() {
  return items.map((it) => {
    const h = it.holder; const p = it.place === "carry" ? "ground" : it.place;
    let x = it.group.position.x, z = it.group.position.z;
    if (it.place === "carry") { const f = forward(); x = camera.position.x + f.x; z = camera.position.z + f.z; }
    return { id: it.id, c: +it.condition.toFixed(3), n: it.name, v: it.value, j: it.junk, m: it.mystery, r: it.rare, s: it.shinyDone, p,
      h: h ? (h.kind === "slot" ? "s" + slots.indexOf(h) : h.kind === "bath" ? "b" + baths.indexOf(h) : "w") : null, x: +x.toFixed(2), z: +z.toFixed(2), ry: +it.group.rotation.y.toFixed(2) };
  });
}
function loadWorld() {
  for (const w of S.world || []) {
    const it = createItem(w.id, w); if (!it) continue;
    let holder = null;
    if (w.h === "w") holder = bench; else if (w.h && w.h[0] === "s") holder = slots[+w.h.slice(1)]; else if (w.h && w.h[0] === "b") holder = baths[+w.h.slice(1)];
    if (holder && (!holder.active && holder.kind !== "bench" || holder.item)) holder = null;
    if (holder) {
      it.place = holder.kind === "bench" ? "bench" : holder.kind; it.holder = holder; holder.item = it;
      setScaleFit(it, holder.kind === "slot" ? 1.0 : holder.kind === "bath" ? .8 : 1.1); it.group.position.copy(holder.pos);
      if (holder.kind === "slot") { it.tag = priceSprite(money(priceOf(it))); it.tag.position.set(holder.pos.x, holder.pos.y + Math.min(1.2, it.size.y * it.group.scale.x) + .25, holder.pos.z - .3); scene.add(it.tag); }
    } else { it.place = w.p === "garage" ? "garage" : "ground"; it.group.position.set(w.x, 0, w.z); it.group.rotation.y = w.ry || 0; }
  }
}

// ---------------------------------------------------------------- movement + loop
function collide(p) {
  const R = .32;
  for (const r of colliders) {
    if (!r.active) continue;
    if (p.x > r.minX - R && p.x < r.maxX + R && p.z > r.minZ - R && p.z < r.maxZ + R) {
      const dl = p.x - (r.minX - R), dr = r.maxX + R - p.x, dt = p.z - (r.minZ - R), db = r.maxZ + R - p.z, m = Math.min(dl, dr, dt, db);
      if (m === dl) p.x = r.minX - R; else if (m === dr) p.x = r.maxX + R; else if (m === dt) p.z = r.minZ - R; else p.z = r.maxZ + R;
    }
  }
  p.x = Math.max(-28, Math.min(28, p.x)); p.z = Math.max(-28, Math.min(14, p.z));
}
applyUpgrades();
loadWorld();
if (S.tut < 0) fillQuests();
let last = performance.now();
function loop(now) {
  const dt = Math.min(.05, (now - last) / 1000); last = now;
  if (started && !panelOpen) {
    if (keys.has("ArrowLeft")) yaw += 1.8 * dt; if (keys.has("ArrowRight")) yaw -= 1.8 * dt;
    const f = (keys.has("KeyW") || keys.has("ArrowUp") ? 1 : 0) - (keys.has("KeyS") || keys.has("ArrowDown") ? 1 : 0);
    const s = (keys.has("KeyD") ? 1 : 0) - (keys.has("KeyA") ? 1 : 0);
    if (f || s) {
      const sp = (keys.has("ShiftLeft") ? 6.5 : 4.2) * F.walk * dt / Math.hypot(f, s);
      camera.position.x += (-Math.sin(yaw) * f + Math.cos(yaw) * s) * sp;
      camera.position.z += (-Math.cos(yaw) * f - Math.sin(yaw) * s) * sp;
      collide(camera.position);
      camera.position.y = 1.7 + Math.sin(now / 110) * .025;
    }
  }
  camera.rotation.set(pitch, yaw, 0);
  if (doorOpen < doorTarget) doorOpen = Math.min(doorTarget, doorOpen + dt * .45);
  door.position.y = 1.45 + doorOpen * 2.8; door.scale.y = 1 - doorOpen * .92; doorRect.active = doorOpen < .6;
  // baths clean by themselves
  for (const b of baths) {
    const it = b.item; if (!b.active || !it || it.condition >= 1) continue;
    it.condition = Math.min(1, it.condition + BALANCE.bathRate * F.bathSpeed * dt); applyCondition(it);
    it.group.position.y = b.pos.y + Math.sin(now / 200) * .02;
    if (Math.random() < dt * 8) burst(b.pos.clone().add(new THREE.Vector3((Math.random() - .5) * .6, .25, (Math.random() - .5) * .5)), 0xd8f6ff, 1, .6, .7);
    if (it.condition >= 1) onCleaned(it, b.pos, true);
  }
  for (let i = parts.length - 1; i >= 0; i--) {
    const p = parts[i]; p.life -= dt; p.v.y -= 4 * dt; p.m.position.addScaledVector(p.v, dt); p.m.scale.setScalar(Math.max(.01, p.life / p.max));
    if (p.life <= 0) { scene.remove(p.m); p.m.material.dispose(); parts.splice(i, 1); }
  }
  updateCustomers(dt);
  if (started) updateTutorial();
  const mt = started ? markerTarget() : null; marker.visible = !!mt;
  if (mt) { marker.position.copy(mt); marker.position.y += Math.sin(now / 200) * .12; marker.rotation.y += dt * 2; }
  aim = started && !panelOpen ? findAim() : null;
  const h = started && !panelOpen ? hintFor(aim) : ""; const hint = $("hint");
  if (h) { if (hint.innerHTML !== h) hint.innerHTML = h; hint.hidden = false; } else hint.hidden = true;
  const showC = aim && aim.item && (aim.item.place === "bench" || aim.item.place === "bath") && !carrying; $("cond").hidden = !showC;
  if (showC) $("cond").firstChild.style.width = Math.round(aim.item.condition * 100) + "%";
  if (carrying) carrying.group.position.y = -.42 + Math.sin(now / 160) * .01;
  updateHUD();
  renderer.render(scene, camera);
  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);
window.__game = { S, items, slots, baths, bench, buyLot, LOTS, camera, get aim() { return aim; }, get carrying() { return carrying; }, interact, scrub, sell, computerPanel, closePanel,
  setLook(y, p) { yaw = y; pitch = p; }, lookAt(x, y, z) { const c = camera.position, dx = x - c.x, dz = z - c.z; yaw = Math.atan2(-dx, -dz); pitch = Math.atan2(y - c.y, Math.hypot(dx, dz)); }, customers, applyUpgrades, addXP };
