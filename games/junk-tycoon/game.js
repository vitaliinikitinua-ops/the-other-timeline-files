// Junk Lot Tycoon - prototype v0.1 (three.js, first person)
import * as THREE from "three";
import { ITEMS, LOTS, UPGRADES, ACHIEVEMENTS, BALANCE, itemPrice, rollLot } from "./data.js";

const $ = (id) => document.getElementById(id);
const SAVE_KEY = "junklot_save_v1";

// ---------------------------------------------------------------- state
const S = { money: BALANCE.startMoney, up: {}, ach: {}, stats: { earned: 0, sold: 0, trashed: 0, lots: 0 } };
try { const s = JSON.parse(localStorage.getItem(SAVE_KEY) || "null"); if (s && s.v === 1) Object.assign(S, s.data); } catch (e) {}
function save() { try { localStorage.setItem(SAVE_KEY, JSON.stringify({ v: 1, data: S })); } catch (e) {} }
setInterval(save, 5000);

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
scene.fog = new THREE.Fog(0x9cc9e8, 30, 70);
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
const colliders = []; // {minX,maxX,minZ,maxZ,active?}
const rect = (minX, maxX, minZ, maxZ) => { const r = { minX, maxX, minZ, maxZ, active: true }; colliders.push(r); return r; };
const targets = []; // meshes the crosshair can hit

const ground = new THREE.Mesh(new THREE.PlaneGeometry(120, 120), mat(0x77a856)); ground.rotation.x = -Math.PI / 2; scene.add(ground);
const road = new THREE.Mesh(new THREE.PlaneGeometry(120, 6), mat(0x55585e)); road.rotation.x = -Math.PI / 2; road.position.set(0, .01, 17); scene.add(road);
for (let x = -50; x < 50; x += 4) { const l = new THREE.Mesh(new THREE.PlaneGeometry(2, .15), mat(0xeeeeee)); l.rotation.x = -Math.PI / 2; l.position.set(x, .02, 17); scene.add(l); }
for (const [x, z] of [[-14, -6], [-12, 8], [-18, 2], [16, -8], [20, -2], [-9, -16], [9, -15], [22, 6]]) {
  box(.4, 1.4, .4, 0x7a5230, x, .7, z); const c = new THREE.Mesh(new THREE.ConeGeometry(1.4, 3, 7), mat(0x3f8a3a)); c.position.set(x, 2.8, z); scene.add(c);
}

// Garage (opening faces +z)
const GZ0 = -13, GZ1 = -7;
box(.15, 3, 6, 0xc8b89a, -2.95, 1.5, -10); box(.15, 3, 6, 0xc8b89a, 2.95, 1.5, -10); box(6, 3, .15, 0xc8b89a, 0, 1.5, -12.95);
box(6.3, .2, 6.3, 0x8f3b2b, 0, 3.1, -10);
const gFloor = new THREE.Mesh(new THREE.PlaneGeometry(5.8, 5.8), mat(0x9a9a92)); gFloor.rotation.x = -Math.PI / 2; gFloor.position.set(0, .015, -10); scene.add(gFloor);
rect(-3.05, -2.85, GZ0, GZ1); rect(2.85, 3.05, GZ0, GZ1); rect(-3, 3, -13.05, -12.85);
const door = box(5.8, 2.9, .08, 0xd9d4c6, 0, 1.45, -7.05); door.userData.kind = "door"; targets.push(door);
for (let i = 0; i < 7; i++) box(5.8, .03, .1, 0xbab4a3, 0, .3 + i * .4, 0, door).position.set(0, -1.15 + i * .4, .01);
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

// Trash container
const bin = new THREE.Mesh(new THREE.CylinderGeometry(.55, .45, 1.05, 12), mat(0x2f6b3f)); bin.position.set(-6, .52, 2.6); scene.add(bin);
bin.userData.kind = "trash"; targets.push(bin); rect(-6.6, -5.4, 2, 3.2);
const binLbl = labelMesh("TRASH  +$1", 1, .25, "#1d3d25", "#ffffff", 70); binLbl.position.set(-6, 1.3, 2.6); binLbl.rotation.y = Math.PI / 4; scene.add(binLbl);

// Shop: floor, two tables with 4 slots each, terminal, sign
const shopFloor = new THREE.Mesh(new THREE.PlaneGeometry(15, 7), mat(0xc79a62)); shopFloor.rotation.x = -Math.PI / 2; shopFloor.position.set(12, .012, 6.5); scene.add(shopFloor);
const slots = [];
function makeTable(cx, active) {
  const g = new THREE.Group(); scene.add(g);
  box(6, .1, 1, 0xa77a48, cx, .86, 8, g); for (const dx of [-2.9, 2.9]) for (const dz of [-.42, .42]) box(.08, .82, .08, 0x6b4421, cx + dx, .41, 8 + dz, g);
  const r = rect(cx - 3, cx + 3, 7.5, 8.5); r.active = active; g.visible = active;
  const list = [];
  for (let i = 0; i < 4; i++) {
    const sx = cx - 2.25 + i * 1.5;
    const pad = new THREE.Mesh(new THREE.BoxGeometry(1.2, .02, .8), new THREE.MeshLambertMaterial({ color: 0xfff1d0 }));
    pad.position.set(sx, .92, 8); g.add(pad);
    const slot = { pos: new THREE.Vector3(sx, .93, 8), item: null, reserved: false, active, pad };
    pad.userData.kind = "slot"; pad.userData.slot = slot; targets.push(pad); slots.push(slot); list.push(slot);
  }
  return { g, r, list };
}
const tableA = makeTable(9, true);
const tableB = makeTable(15.6, false);
box(1.2, .8, .7, 0x5b4636, 4.2, .4, 5); const mon = box(.1, .55, .8, 0x222222, 4.2, 1.1, 5);
const monLbl = labelMesh("UPGRADES\n▶ press E", .72, .48, "#10202f", "#7fe0ff", 74); monLbl.position.set(4.14, 1.1, 5); monLbl.rotation.y = -Math.PI / 2; scene.add(monLbl);
monLbl.userData.kind = "terminal"; mon.userData.kind = "terminal"; targets.push(monLbl, mon); rect(3.6, 4.8, 4.65, 5.35);
const shopSign = new THREE.Group(); scene.add(shopSign);
box(.15, 3.2, .15, 0x6b4a2a, 6, 1.6, 9.2, shopSign); box(.15, 3.2, .15, 0x6b4a2a, 18.6, 1.6, 9.2, shopSign);
const signLbl = labelMesh("JUNK & WONDERS", 7, .9, "#c23b22", "#fff6d8", 110); signLbl.position.set(12.3, 3, 9.25); signLbl.rotation.y = Math.PI; shopSign.add(signLbl);
const signLbl2 = signLbl.clone(); signLbl2.rotation.y = 0; signLbl2.position.z = 9.15; shopSign.add(signLbl2);

function applyUpgrades() {
  const b = !!S.up.table2; tableB.g.visible = b; tableB.r.active = b; tableB.list.forEach((s) => (s.active = b));
  shopSign.visible = !!S.up.sign;
}
applyUpgrades();

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
  else if (p.s === "tor") { g = new THREE.TorusGeometry(p.sx, p.sz, 6, 16); }
  else g = new THREE.SphereGeometry(1, 10, 8);
  const m = new THREE.Mesh(g, mat(p.c)); m.material.userData.clean = new THREE.Color(p.c);
  if (p.s === "sph") m.scale.set(p.sx, p.sy, p.sz);
  m.position.set(p.x, p.y, p.z); return m;
}

function createItem(id) {
  const def = ITEMS[id], group = new THREE.Group();
  const meshes = def.parts.map(partMesh); meshes.forEach((m) => group.add(m));
  const bb = new THREE.Box3().setFromObject(group), size = bb.getSize(new THREE.Vector3());
  const it = { id, def, name: def.name, value: def.value, junk: !!def.junk, group, meshes, size, maxDim: Math.max(size.x, size.y, size.z),
    condition: BALANCE.startCondition[0] + Math.random() * (BALANCE.startCondition[1] - BALANCE.startCondition[0]),
    rare: !!(def.rare && Math.random() < def.rare.chance), shinyDone: false, place: "ground", slot: null, tag: null, spots: [] };
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
  if (it.slot) { it.slot.item = null; it.slot.reserved = false; it.slot = null; }
  if (it.tag) { it.tag.parent && it.tag.parent.remove(it.tag); it.tag = null; }
  it.group.parent && it.group.parent.remove(it.group);
  it.group.traverse((o) => { const i = targets.indexOf(o); if (i >= 0) targets.splice(i, 1); });
  items.splice(items.indexOf(it), 1);
}
function setScaleFit(it, maxDim) { const s = Math.min(1, maxDim / it.maxDim); it.group.scale.setScalar(s); return s; }

// ---------------------------------------------------------------- particles
const parts = []; const pGeo = new THREE.BoxGeometry(.03, .03, .03);
function burst(pos, color, n = 8, speed = 1.5, life = .6) {
  for (let i = 0; i < n; i++) {
    const m = new THREE.Mesh(pGeo, new THREE.MeshBasicMaterial({ color })); m.position.copy(pos); scene.add(m);
    parts.push({ m, v: new THREE.Vector3((Math.random() - .5) * speed, Math.random() * speed, (Math.random() - .5) * speed), life, max: life });
  }
}

// ---------------------------------------------------------------- UI helpers
function money(n) { return "$" + Math.round(n).toLocaleString("en-US"); }
function toast(html, cls = "") { const t = document.createElement("div"); t.className = "toast " + cls; t.innerHTML = html; $("toasts").appendChild(t); setTimeout(() => t.remove(), 3800); }
function unlock(id) {
  if (S.ach[id]) return; const a = ACHIEVEMENTS.find((x) => x.id === id); if (!a) return;
  S.ach[id] = Date.now(); sfx.ach(); toast(`🏆 Achievement unlocked: <b>${a.name}</b><small>${a.desc}</small>`, "ach"); save();
}
function earn(n) { S.money += n; S.stats.earned += n; if (S.stats.earned >= 1000) unlock("grand"); }
function updateHUD() {
  $("hud-money").textContent = money(S.money);
  const got = ACHIEVEMENTS.filter((a) => S.ach[a.id]).length;
  $("hud-ach").textContent = `🏆 ${got}/${ACHIEVEMENTS.length} (Tab)`;
  let goal;
  const inGarage = items.filter((i) => i.place === "garage").length;
  if (!S.stats.lots) goal = "Goal: buy your first lot at the LOTS board (right of the garage).";
  else if (inGarage) goal = `${inGarage} items in your lot. Carry them to the workbench, scrub them, put them on the shop tables.`;
  else { const next = UPGRADES.find((u) => !S.up[u.id] && (!u.needs || S.up[u.needs])); goal = next ? `Next upgrade: ${next.name} (${money(next.price)}) at the UPGRADES computer.` : "Buy more lots and collect every achievement!"; }
  $("hud-goal").textContent = goal;
}

// ---------------------------------------------------------------- panels
let panelOpen = false;
function openPanel(html, bind) {
  panelOpen = true; scrubbing = null; keys.clear();
  if (document.pointerLockElement) document.exitPointerLock();
  $("panel-body").innerHTML = html + `<div style="text-align:right;margin-top:10px"><button class="ghost" id="p-close">Back to game</button></div>`;
  $("panel").hidden = false; $("p-close").onclick = closePanel; bind && bind();
}
function closePanel() { $("panel").hidden = true; panelOpen = false; lockPointer(); }
function lotsPanel() {
  const rows = LOTS.map((l) => {
    const locked = l.needs && !S.up[l.needs];
    return `<div class="row"><div class="t"><b>${l.name} — ${money(l.price)}</b><span>${locked ? "🔒 Needs: " + UPGRADES.find((u) => u.id === l.needs).name : l.hint}</span></div>
      <button data-lot="${l.id}" ${locked || S.money < l.price ? "disabled" : ""}>Buy</button></div>`;
  }).join("");
  openPanel(`<h2>Lots for sale</h2><p class="sub">You have ${money(S.money)}. What's inside? Nobody knows. That's the fun.</p>${rows}`, () => {
    document.querySelectorAll("[data-lot]").forEach((b) => (b.onclick = () => { buyLot(LOTS.find((l) => l.id === b.dataset.lot)); closePanel(); }));
  });
}
function upgradesPanel() {
  const rows = UPGRADES.map((u) => {
    const owned = S.up[u.id], locked = u.needs && !S.up[u.needs];
    return `<div class="row"><div class="t"><b>${u.name} — ${money(u.price)}</b><span>${locked ? "🔒 Needs " + UPGRADES.find((x) => x.id === u.needs).name : u.desc}</span></div>
      ${owned ? '<span class="owned">Owned ✓</span>' : `<button data-up="${u.id}" ${locked || S.money < u.price ? "disabled" : ""}>Buy</button>`}</div>`;
  }).join("");
  openPanel(`<h2>Upgrades</h2><p class="sub">You have ${money(S.money)}.</p>${rows}`, () => {
    document.querySelectorAll("[data-up]").forEach((b) => (b.onclick = () => {
      const u = UPGRADES.find((x) => x.id === b.dataset.up); if (S.money < u.price) return;
      S.money -= u.price; S.up[u.id] = 1; applyUpgrades(); sfx.cash(); unlock("tool_up"); save(); upgradesPanel();
    }));
  });
}
function achPanel() {
  const rows = ACHIEVEMENTS.map((a) => {
    const got = S.ach[a.id];
    return `<div class="row ${got ? "" : "locked"}"><div class="t"><b>${got ? "🏆" : "🔒"} ${a.secret && !got ? "???" : a.name}</b><span>${a.secret && !got ? "Secret achievement" : a.desc}</span></div></div>`;
  }).join("");
  const st = S.stats;
  openPanel(`<h2>Achievements</h2><p class="sub">Lots bought ${st.lots} · items sold ${st.sold} · total earned ${money(st.earned)}</p><div class="achlist">${rows}</div>
    <div style="margin-top:8px"><button class="ghost" id="p-reset">Reset progress</button></div>`, () => {
    $("p-reset").onclick = () => { if (confirm("Delete all progress?")) { try { localStorage.removeItem(SAVE_KEY); } catch (e) {} location.reload(); } };
  });
}

// ---------------------------------------------------------------- lots
function buyLot(lot) {
  if (S.money < lot.price) return sfx.no();
  S.money -= lot.price; S.stats.lots++; unlock("first_lot"); if (lot.id === "student") unlock("student");
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
function lockPointer() { if (fallbackLook) return; try { const p = renderer.domElement.requestPointerLock(); if (p && p.catch) p.catch(() => (fallbackLook = true)); } catch (e) { fallbackLook = true; } }
document.addEventListener("pointerlockerror", () => { if (!fallbackLook) { fallbackLook = true; toast("Mouse look without pointer lock: just move the mouse."); } });
document.addEventListener("pointerlockchange", () => {
  if (!document.pointerLockElement && started && !panelOpen && !fallbackLook) openPanel(`<h2>Paused</h2><p class="sub">Your junk is waiting.</p>`);
});
$("btn-play").onclick = () => { $("start").hidden = true; started = true; audio(); lockPointer(); };

addEventListener("keydown", (e) => {
  if (!started) return;
  if (e.code === "Tab") { e.preventDefault(); panelOpen ? closePanel() : achPanel(); return; }
  if (panelOpen) return;
  keys.add(e.code);
  if (e.code === "KeyE") interact();
});
addEventListener("keyup", (e) => keys.delete(e.code));
addEventListener("blur", () => keys.clear());
renderer.domElement.addEventListener("mousedown", (e) => {
  if (!started || panelOpen) return;
  if (!document.pointerLockElement && !fallbackLook) { lockPointer(); return; }
  if (e.button !== 0) return;
  if (!carrying && aim && aim.item && aim.item.place === "bench") { scrubbing = aim.item; return; }
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

function toolMult() { return (S.up.sponge ? 2 : 1) * (S.up.washer ? 4 : 1); }
let lastScrubFx = 0;
function scrub(it, px) {
  if (it.condition >= 1) return;
  it.condition = Math.min(1, it.condition + px * BALANCE.scrubPerPixel * toolMult());
  applyCondition(it);
  if (noiseGain) noiseGain.gain.value = Math.min(.12, px * .004);
  const now = performance.now();
  if (now - lastScrubFx > 60) { lastScrubFx = now; burst(BENCH_POS.clone().add(new THREE.Vector3((Math.random() - .5) * .4, .15 + Math.random() * .2, .2)), 0x6b5236, 3, 1.2, .4); }
  if (it.condition >= 1 && !it.shinyDone) {
    it.shinyDone = true; sfx.shiny(); unlock("shiny"); burst(BENCH_POS.clone().add(new THREE.Vector3(0, .3, 0)), 0xfff3a0, 24, 2.2, .9);
    if (noiseGain) noiseGain.gain.value = 0; scrubbing = null;
    if (it.rare) { it.name = it.def.rare.name; it.value = it.def.rare.value; unlock("jackpot"); toast(`💎 <b>${it.name}</b><small>It's worth ${money(it.value)}!</small>`, "ach"); }
    else toast(`✨ <b>${it.name}</b> is like new! Worth ${money(itemPrice(it))}.`);
  }
}

// ---------------------------------------------------------------- interaction
const ray = new THREE.Raycaster(); const center = new THREE.Vector2(0, 0);
function findAim() {
  ray.setFromCamera(center, camera); ray.far = 4.2;
  const hits = ray.intersectObjects(targets.filter((t) => t.visible !== false), false);
  for (const h of hits) {
    const o = h.object;
    if (o.userData.item) { if (o.userData.item === carrying) continue; if (h.distance > 3.4) return null; return { item: o.userData.item, point: h.point }; }
    const k = o.userData.kind; if (!k) continue;
    if (k === "slot" && !o.userData.slot.active) continue;
    return { kind: k, slot: o.userData.slot, point: h.point, dist: h.distance };
  }
  return null;
}
function pickUp(it) {
  if (it.slot && it.slot.reserved) return sfx.no();
  if (it.slot) { it.slot.item = null; it.slot = null; }
  if (it.tag) { it.tag.parent.remove(it.tag); it.tag = null; }
  scene.remove(it.group); camera.add(it.group);
  it.group.position.set(.42, -.42, -.95); it.group.rotation.set(.15, -.5, 0); setScaleFit(it, .5);
  it.place = "carry"; carrying = it; sfx.pick();
}
function putDown(it, pos, place, fit = 9) {
  camera.remove(it.group); scene.add(it.group);
  setScaleFit(it, fit); it.group.position.copy(pos); it.group.rotation.set(0, yaw, 0);
  it.place = place; carrying = null; sfx.drop();
}
function interact() {
  const a = aim;
  if (carrying) {
    const it = carrying;
    if (a && a.kind === "bench") { if (items.some((i) => i.place === "bench")) return toast("The workbench is busy. Take that item off first."); return putDown(it, BENCH_POS, "bench", 1.1); }
    if (a && a.kind === "slot") {
      if (a.slot.item) return toast("That spot is taken.");
      putDown(it, a.slot.pos, "slot", 1.0); it.slot = a.slot; a.slot.item = it;
      it.tag = priceSprite(money(itemPrice(it))); it.tag.position.set(a.slot.pos.x, a.slot.pos.y + Math.min(1, it.size.y * it.group.scale.x) + .25, a.slot.pos.z - .3); scene.add(it.tag);
      if (slots.filter((s) => s.active).every((s) => s.item)) unlock("full_shop");
      return;
    }
    if (a && a.kind === "trash") {
      const gain = it.junk ? BALANCE.junkScrap : 0;
      camera.remove(it.group); removeItem(it); carrying = null; sfx.trash(); burst(bin.position.clone().add(new THREE.Vector3(0, .6, 0)), 0x555555, 10);
      if (it.junk) { earn(gain); S.stats.trashed++; if (S.stats.trashed >= 10) unlock("trash10"); toast(`Junk recycled: +${money(gain)}`); }
      else toast(`You threw away ${it.name}. It was worth ${money(itemPrice(it))}... bold.`);
      save(); return;
    }
    const f = new THREE.Vector3(-Math.sin(yaw), 0, -Math.cos(yaw));
    return putDown(it, new THREE.Vector3(camera.position.x + f.x * 1.3, 0, camera.position.z + f.z * 1.3), "ground");
  }
  if (!a) return;
  if (a.item) return pickUp(a.item);
  if (a.kind === "board") return lotsPanel();
  if (a.kind === "terminal") return upgradesPanel();
  if (a.kind === "door") return toast("Buy a lot at the LOTS board to open the garage.");
}
function hintFor(a) {
  if (carrying) {
    const n = `<b>${carrying.name}</b>`;
    if (a && a.kind === "bench") return `<b>E</b> place ${n} on the workbench`;
    if (a && a.kind === "slot") return a.slot.item ? "Spot taken" : `<b>E</b> sell ${n} for <b>${money(itemPrice(carrying))}</b>`;
    if (a && a.kind === "trash") return carrying.junk ? `<b>E</b> recycle junk (+$1)` : `<b>E</b> throw away?! (worth ${money(itemPrice(carrying))})`;
    return `<b>E</b> drop ${n}`;
  }
  if (!a) return "";
  if (a.item) {
    const it = a.item, c = Math.round(it.condition * 100);
    const info = it.junk ? "junk, recycle it" : `${c}% · ${money(itemPrice(it))}`;
    if (it.place === "bench") return it.condition >= 1 ? `<b>${it.name}</b> is spotless · <b>E</b> pick up` : `<b>Hold click + move mouse</b> to scrub · <b>E</b> pick up · ${info}`;
    if (it.place === "slot") return `<b>${it.name}</b> on sale for ${money(itemPrice(it))} · <b>E</b> take back`;
    return `<b>E</b> pick up <b>${it.name}</b> · ${info}`;
  }
  return { board: "<b>E</b> browse lots", terminal: "<b>E</b> upgrades", door: "Your garage. Buy a lot to open it.", bench: "Workbench: bring an item here", slot: "Shop table: bring an item to sell", trash: "Trash: recycle junk for $1" }[a.kind] || "";
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
function updateCustomers(dt) {
  custTimer -= dt;
  if (custTimer <= 0) { custTimer = BALANCE.customerEvery * (S.up.sign ? .5 : 1) * (.7 + Math.random() * .6); spawnCustomer(); }
  for (let i = customers.length - 1; i >= 0; i--) {
    const c = customers[i]; c.t += dt;
    if (c.state === "in" || c.state === "out") {
      const d = c.target.clone().sub(c.g.position); d.y = 0; const L = d.length();
      if (L < .05) {
        if (c.state === "in") { c.state = "browse"; c.t = 0; }
        else { scene.remove(c.g); customers.splice(i, 1); continue; }
      } else { d.multiplyScalar(Math.min(1, 1.7 * dt / L)); c.g.position.add(d); c.g.rotation.y = Math.atan2(d.x, d.z); }
      c.g.position.y = Math.abs(Math.sin(c.t * 9)) * .05;
    } else if (c.state === "browse") {
      c.g.rotation.y = Math.PI; c.g.children[1].position.y = 1.32 + Math.sin(c.t * 4) * .03;
      if (c.t > 1.6) {
        const it = c.slot.item;
        if (it) { const p = itemPrice(it); earn(p); S.stats.sold++; unlock("first_sale"); sfx.cash(); burst(it.group.position.clone().add(new THREE.Vector3(0, .5, 0)), 0x5fd38d, 10, 1.6); toast(`Sold <b>${it.name}</b> for <b>${money(p)}</b>`); removeItem(it); save(); }
        c.slot.reserved = false; c.state = "out"; c.target = new THREE.Vector3(c.g.position.x + (Math.random() - .5) * 6, 0, 21);
      }
    }
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
let last = performance.now();
function loop(now) {
  const dt = Math.min(.05, (now - last) / 1000); last = now;
  if (started && !panelOpen) {
    if (keys.has("ArrowLeft")) yaw += 1.8 * dt; if (keys.has("ArrowRight")) yaw -= 1.8 * dt;
    const f = (keys.has("KeyW") || keys.has("ArrowUp") ? 1 : 0) - (keys.has("KeyS") || keys.has("ArrowDown") ? 1 : 0);
    const s = (keys.has("KeyD") ? 1 : 0) - (keys.has("KeyA") ? 1 : 0);
    if (f || s) {
      const sp = (keys.has("ShiftLeft") ? 6.5 : 4.2) * dt / Math.hypot(f, s);
      camera.position.x += (-Math.sin(yaw) * f + Math.cos(yaw) * s) * sp;
      camera.position.z += (-Math.cos(yaw) * f - Math.sin(yaw) * s) * sp;
      collide(camera.position);
      camera.position.y = 1.7 + Math.sin(now / 110) * .025;
    }
  }
  camera.rotation.set(pitch, yaw, 0);
  // door
  if (doorOpen < doorTarget) { doorOpen = Math.min(doorTarget, doorOpen + dt * .45); }
  door.position.y = 1.45 + doorOpen * 2.8; door.scale.y = 1 - doorOpen * .92; doorRect.active = doorOpen < .6;
  // particles
  for (let i = parts.length - 1; i >= 0; i--) {
    const p = parts[i]; p.life -= dt; p.v.y -= 4 * dt; p.m.position.addScaledVector(p.v, dt); p.m.scale.setScalar(Math.max(.01, p.life / p.max));
    if (p.life <= 0) { scene.remove(p.m); p.m.material.dispose(); parts.splice(i, 1); }
  }
  updateCustomers(dt);
  // aim + hint
  aim = started && !panelOpen ? findAim() : null;
  const h = started && !panelOpen ? hintFor(aim) : ""; const hint = $("hint");
  if (h) { if (hint.innerHTML !== h) hint.innerHTML = h; hint.hidden = false; } else hint.hidden = true;
  const showC = aim && aim.item && aim.item.place === "bench" && !carrying; $("cond").hidden = !showC;
  if (showC) $("cond").firstChild.style.width = Math.round(aim.item.condition * 100) + "%";
  if (carrying) carrying.group.position.y = -.42 + Math.sin(now / 160) * .01;
  updateHUD();
  renderer.render(scene, camera);
  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);
window.__game = { S, items, slots, buyLot, LOTS, camera, get aim() { return aim; }, interact, scrub, setLook(y, p) { yaw = y; pitch = p; },
  lookAt(x, y, z) { const c = camera.position, dx = x - c.x, dz = z - c.z; yaw = Math.atan2(-dx, -dz); pitch = Math.atan2(y - c.y, Math.hypot(dx, dz)); }, customers };
