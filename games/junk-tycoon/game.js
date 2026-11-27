// Junk Lot Tycoon - v0.3 (three.js, first person, PBR models from Poly Haven - CC0)
import * as THREE from "three";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { RGBELoader } from "three/addons/loaders/RGBELoader.js";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { GTAOPass } from "three/addons/postprocessing/GTAOPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { ITEMS, LOTS, UPGRADES, ACHIEVEMENTS, BALANCE, TUTORIAL, rollLot } from "./data.js";

const $ = (id) => document.getElementById(id);
const SAVE_KEY = "junklot_save_v3";
const VERSION = "0.3";

// ---------------------------------------------------------------- state
const STATS0 = { earned: 0, sold: 0, trashed: 0, lots: 0, requests: 0, shinies: 0, bestStreak: 0, best: 0, online: 0, auctions: 0 };
const S = { money: BALANCE.startMoney, xp: 0, lvl: 1, up: {}, ach: {}, tut: 0, quests: [], flags: {}, world: [], stats: { ...STATS0 } };
try {
  const s = JSON.parse(localStorage.getItem(SAVE_KEY) || "null");
  if (s && s.v === 3) { Object.assign(S, s.data); S.stats = Object.assign({ ...STATS0 }, s.data.stats); }
} catch (e) {}
let worldReady = false;
function save() { if (!worldReady) return; try { S.world = serializeWorld(); localStorage.setItem(SAVE_KEY, JSON.stringify({ v: 3, data: S })); } catch (e) {} }
setInterval(save, 5000);
addEventListener("beforeunload", save);

function fx() {
  const f = { clean: 1, price: 1, cust: 1, junk: 1, rare: 1, walk: 1, tables: 1, baths: 0, bathSpeed: 1, xp: 1, online: 0, onlineSpeed: 1 };
  for (const u of UPGRADES) {
    if (!S.up[u.id]) continue;
    for (const [k, v] of Object.entries(u.fx)) {
      if (k === "tables" || k === "baths" || k === "online") f[k] += v; else if (k === "junk") f.junk = Math.max(f.junk, v); else f[k] *= v;
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
  bid() { beep(700, .06, "square", .07); },
  gavel() { beep(150, .12, "square", .15, .5); setTimeout(() => beep(150, .12, "square", .15, .5), 160); },
};

// ---------------------------------------------------------------- renderer / scene / post
const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
renderer.setPixelRatio(Math.min(devicePixelRatio, 1.5));
renderer.setSize(innerWidth, innerHeight);
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = .95;
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
document.body.prepend(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xa8cbe6);
scene.fog = new THREE.Fog(0xb8d3e8, 35, 95);
const camera = new THREE.PerspectiveCamera(70, innerWidth / innerHeight, .05, 300);
camera.rotation.order = "YXZ";
camera.position.set(0, 1.7, 3);
scene.add(camera);

const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
const gtao = new GTAOPass(scene, camera, innerWidth, innerHeight);
gtao.updateGtaoMaterial({ radius: .35, distanceExponent: 1.4, thickness: 1.2, scale: 1.1 });
gtao.blendIntensity = .9;
composer.addPass(gtao);
composer.addPass(new OutputPass());
let HIGH = S.flags.gfx !== "low";
function setQuality(high) {
  HIGH = high; S.flags.gfx = high ? "high" : "low";
  renderer.shadowMap.enabled = high; scene.traverse((o) => { if (o.material) [].concat(o.material).forEach((m) => (m.needsUpdate = true)); });
  renderer.setPixelRatio(high ? Math.min(devicePixelRatio, 1.5) : 1); renderer.setSize(innerWidth, innerHeight); composer.setSize(innerWidth, innerHeight);
}
addEventListener("resize", () => { camera.aspect = innerWidth / innerHeight; camera.updateProjectionMatrix(); renderer.setSize(innerWidth, innerHeight); composer.setSize(innerWidth, innerHeight); });

scene.add(new THREE.HemisphereLight(0xdff1ff, 0x5d7f45, .35));
const sun = new THREE.DirectionalLight(0xfff0d8, 2.6); sun.position.set(14, 22, 10);
sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048); sun.shadow.bias = -.0004; sun.shadow.normalBias = .03;
Object.assign(sun.shadow.camera, { left: -32, right: 32, top: 26, bottom: -26, near: 1, far: 70 });
sun.target.position.set(4, 0, 0); scene.add(sun, sun.target);

// loading
const manager = new THREE.LoadingManager();
manager.onProgress = (url, done, total) => { const el = $("load-txt"); if (el) el.textContent = `Loading ${done}/${total}...`; };
const texLoader = new THREE.TextureLoader(manager);
const gltfLoader = new GLTFLoader(manager);
manager.itemStart("sky");
fetch("tex/sky.hdr.json").then((r) => r.json()).then((j) => {
  const bin = Uint8Array.from(atob(j.b64), (c) => c.charCodeAt(0));
  const r = new RGBELoader().parse(bin.buffer);
  const t = new THREE.DataTexture(r.data, r.width, r.height, THREE.RGBAFormat, r.type);
  t.colorSpace = THREE.LinearSRGBColorSpace; t.minFilter = t.magFilter = THREE.LinearFilter; t.generateMipmaps = false; t.flipY = true; t.needsUpdate = true;
  t.mapping = THREE.EquirectangularReflectionMapping; scene.environment = t; scene.background = t;
}).catch((e) => console.warn("sky failed", e)).finally(() => manager.itemEnd("sky"));

function tex(name, rep) {
  const d = texLoader.load(`tex/${name}_diff.jpg`), n = texLoader.load(`tex/${name}_nor.jpg`);
  for (const t of [d, n]) { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(rep[0], rep[1]); t.anisotropy = 8; }
  d.colorSpace = THREE.SRGBColorSpace; return { map: d, normalMap: n };
}
const MAT = {
  grass: new THREE.MeshStandardMaterial({ ...tex("grass", [40, 40]), roughness: 1, color: 0xd8e8c0 }),
  asphalt: new THREE.MeshStandardMaterial({ ...tex("asphalt", [30, 1.5]), roughness: .95 }),
  concrete: new THREE.MeshStandardMaterial({ ...tex("concrete", [3, 3]), roughness: .9 }),
  wall: new THREE.MeshStandardMaterial({ ...tex("concrete", [2, 1]), roughness: .95, color: 0xe8dcc8 }),
  wood: new THREE.MeshStandardMaterial({ ...tex("wood", [6, 2]), roughness: .7 }),
  ply: new THREE.MeshStandardMaterial({ ...tex("plywood", [2, 1]), roughness: .75 }),
  plyDark: new THREE.MeshStandardMaterial({ ...tex("plywood", [1, 1]), roughness: .8, color: 0x8a6a4a }),
  roof: new THREE.MeshStandardMaterial({ color: 0x6b2f25, roughness: .6, metalness: .2 }),
  metal: new THREE.MeshStandardMaterial({ color: 0x5a5f66, roughness: .4, metalness: .8 }),
  white: new THREE.MeshStandardMaterial({ color: 0xf2f2f0, roughness: .5 }),
  water: new THREE.MeshStandardMaterial({ color: 0x5ec8ff, roughness: .05, metalness: .1, transparent: true, opacity: .8 }),
  leaf: new THREE.MeshStandardMaterial({ color: 0x4f8a3a, roughness: .9 }),
  bark: new THREE.MeshStandardMaterial({ color: 0x6b4a2e, roughness: 1 }),
};
function shadowy(o, cast = true, receive = true) { o.traverse((c) => { if (c.isMesh) { c.castShadow = cast; c.receiveShadow = receive; } }); return o; }
function rbox(w, h, d, material, x, y, z, parent = scene, r = .03) {
  const m = new THREE.Mesh(new RoundedBoxGeometry(w, h, d, 3, Math.min(r, w / 2.1, h / 2.1, d / 2.1)), material);
  m.position.set(x, y, z); shadowy(m); parent.add(m); return m;
}
function labelMesh(text, w, h, bg = "#2b2420", fg = "#ffb02e", size = 64) {
  const cv = document.createElement("canvas"); cv.width = 512; cv.height = Math.round(512 * h / w);
  const g = cv.getContext("2d"); g.fillStyle = bg; g.fillRect(0, 0, cv.width, cv.height);
  g.fillStyle = fg; g.font = `800 ${size}px system-ui, sans-serif`; g.textAlign = "center"; g.textBaseline = "middle";
  const lines = text.split("\n"); lines.forEach((l, i) => g.fillText(l, cv.width / 2, cv.height / 2 + (i - (lines.length - 1) / 2) * size * 1.1));
  const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
  return new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: t, toneMapped: false }));
}
function priceSprite(text) {
  const cv = document.createElement("canvas"); cv.width = 256; cv.height = 96;
  const g = cv.getContext("2d"); g.fillStyle = "#fff6d8"; g.beginPath(); g.roundRect(6, 6, 244, 84, 18); g.fill();
  g.fillStyle = "#2b2420"; g.font = "800 56px system-ui, sans-serif"; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(text, 128, 50);
  const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace;
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: t, depthTest: false, toneMapped: false })); s.scale.set(.5, .19, 1); s.renderOrder = 5; return s;
}

// ---------------------------------------------------------------- models
const modelCache = new Map();
function loadModel(name) {
  if (!modelCache.has(name)) modelCache.set(name, new Promise((res, rej) => gltfLoader.load(`models/${name}/${name}.json`, (g) => res(g.scene), undefined, rej)));
  return modelCache.get(name);
}
// Normalise a model: optional sub-object filter, rotation, scale; centred on x/z, standing on y = 0.
function shapeModel(src, o = {}) {
  const root = src.clone(true);
  if (o.keepX) {
    root.updateMatrixWorld(true);
    for (const c of [...root.children]) { const b = new THREE.Box3().setFromObject(c); const cx = (b.min.x + b.max.x) / 2; if (cx < o.keepX[0] || cx > o.keepX[1]) root.remove(c); }
  }
  if (o.rot) root.rotation.set(o.rot[0], o.rot[1], o.rot[2]);
  if (o.scale) root.scale.multiplyScalar(o.scale);
  const wrap = new THREE.Group(); wrap.add(root); wrap.updateMatrixWorld(true);
  let bb = new THREE.Box3().setFromObject(root), size = bb.getSize(new THREE.Vector3());
  const md = Math.max(size.x, size.y, size.z);
  if (o.minSize && md < o.minSize) { root.scale.multiplyScalar(o.minSize / md); wrap.updateMatrixWorld(true); bb = new THREE.Box3().setFromObject(root); size = bb.getSize(new THREE.Vector3()); }
  root.position.x -= (bb.min.x + bb.max.x) / 2; root.position.z -= (bb.min.z + bb.max.z) / 2; root.position.y -= bb.min.y;
  return { obj: wrap, size };
}
async function prop(name, x, y, z, ry = 0, o = {}) {
  const src = await loadModel(name); const { obj, size } = shapeModel(src, o);
  obj.position.set(x, y, z); obj.rotation.y = ry; shadowy(obj); scene.add(obj);
  if (o.collide) { const hx = (Math.abs(Math.cos(ry)) * size.x + Math.abs(Math.sin(ry)) * size.z) / 2, hz = (Math.abs(Math.sin(ry)) * size.x + Math.abs(Math.cos(ry)) * size.z) / 2; rect(x - hx, x + hx, z - hz, z + hz); }
  if (o.kind) obj.traverse((c) => { if (c.isMesh) { c.userData.kind = o.kind; targets.push(c); } });
  return obj;
}

// ---------------------------------------------------------------- world
const colliders = [];
const rect = (minX, maxX, minZ, maxZ) => { const r = { minX, maxX, minZ, maxZ, active: true }; colliders.push(r); return r; };
const targets = [];

const ground = new THREE.Mesh(new THREE.PlaneGeometry(160, 160), MAT.grass); ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; scene.add(ground);
const road = new THREE.Mesh(new THREE.PlaneGeometry(160, 6), MAT.asphalt); road.rotation.x = -Math.PI / 2; road.position.set(0, .01, 17); road.receiveShadow = true; scene.add(road);
const lineMat = new THREE.MeshStandardMaterial({ color: 0xf0f0e8, roughness: .6 });
for (let x = -70; x < 70; x += 4) { const l = new THREE.Mesh(new THREE.PlaneGeometry(2, .15), lineMat); l.rotation.x = -Math.PI / 2; l.position.set(x, .02, 17); scene.add(l); }
const pathM = new THREE.Mesh(new THREE.PlaneGeometry(28, 2.4), MAT.concrete); pathM.rotation.x = -Math.PI / 2; pathM.position.set(5, .011, 2); pathM.receiveShadow = true; scene.add(pathM);
// trees: smooth stylised
function tree(x, z, s = 1) {
  const g = new THREE.Group(); g.position.set(x, 0, z); g.scale.setScalar(s);
  const trunk = new THREE.Mesh(new THREE.CylinderGeometry(.16, .24, 2.2, 10), MAT.bark); trunk.position.y = 1.1; g.add(trunk);
  for (let i = 0; i < 5; i++) {
    const r = .9 + Math.random() * .6, b = new THREE.Mesh(new THREE.IcosahedronGeometry(r, 2), MAT.leaf);
    b.position.set((Math.random() - .5) * 1.4, 2.6 + Math.random() * 1.3, (Math.random() - .5) * 1.4); b.scale.y = .85; g.add(b);
  }
  shadowy(g); scene.add(g); rect(x - .3, x + .3, z - .3, z + .3);
}
for (const [x, z, s] of [[-14, -6, 1.1], [-12, 8, 1], [-18, 2, 1.3], [16, -8, 1.2], [21, -3, 1], [-9, -17, 1.4], [9, -16, 1.2], [29, 3, 1.1], [-17, -12, 1], [-22, -4, 1.2], [24, -12, 1.3]]) tree(x, z, s);

// Garage (opening faces +z)
const GZ0 = -13, GZ1 = -7;
rbox(.2, 3, 6, MAT.wall, -2.95, 1.5, -10); rbox(.2, 3, 6, MAT.wall, 2.95, 1.5, -10); rbox(6, 3, .2, MAT.wall, 0, 1.5, -12.95);
rbox(6.5, .22, 6.6, MAT.roof, 0, 3.1, -10.05);
rbox(6.3, .5, .25, MAT.wall, 0, 2.75, -7.05);
const gFloor = new THREE.Mesh(new THREE.PlaneGeometry(5.8, 5.8), MAT.concrete); gFloor.rotation.x = -Math.PI / 2; gFloor.position.set(0, .015, -10); gFloor.receiveShadow = true; scene.add(gFloor);
rect(-3.05, -2.85, GZ0, GZ1); rect(2.85, 3.05, GZ0, GZ1); rect(-3, 3, -13.05, -12.85);
const door = new THREE.Group(); door.position.set(0, 0, -7.0); scene.add(door);
const doorRect = rect(-3, 3, -7.15, -6.85);
const gLight = new THREE.PointLight(0xfff0d0, 14, 10, 1.6); gLight.position.set(0, 2.6, -10); scene.add(gLight);
const gLabel = labelMesh("YOUR LOT", 2.2, .45); gLabel.position.set(0, 3.0, -6.91); scene.add(gLabel);
let doorOpen = 1, doorTarget = 1;

// Lots board (chalkboard)
const board = labelMesh("LOTS & AUCTIONS\n▶ press E", .8, .62, "#1e2a22", "#f4f1e0", 56); board.position.set(4.5, 1.05, -5.3); scene.add(board);
board.userData.kind = "board"; targets.push(board); rect(3.9, 5.1, -5.9, -5.0);

// Workbench
const benchTop = rbox(2, .08, 1, MAT.ply, -6, .9, -2, scene, .02); benchTop.userData.kind = "bench"; targets.push(benchTop);
for (const [dx, dz] of [[-.92, -.42], [.92, -.42], [-.92, .42], [.92, .42]]) rbox(.07, .86, .07, MAT.metal, -6 + dx, .43, -2 + dz, scene, .01);
rbox(1.9, .04, .8, MAT.metal, -6, .25, -2, scene, .01);
rbox(2, 1.1, .05, MAT.plyDark, -6, 1.5, -2.52, scene, .01);
const benchLbl = labelMesh("WORKBENCH", 1.1, .22); benchLbl.position.set(-6, 1.92, -2.49); scene.add(benchLbl);
const benchLight = new THREE.PointLight(0xfff2dd, 4, 4, 1.8); benchLight.position.set(-6, 2.0, -1.6); scene.add(benchLight);
rect(-7.05, -4.95, -2.6, -1.45);
const BENCH_POS = new THREE.Vector3(-6, .945, -1.95);
const bench = { pos: BENCH_POS, item: null, active: true, kind: "bench" };

// Ultrasonic baths (hidden until bought)
const baths = [];
for (const [x, z] of [[-9.2, -2], [-9.2, .6]]) {
  const g = new THREE.Group(); scene.add(g);
  rbox(1.1, .62, .9, MAT.white, x, .31, z, g, .06);
  const water = new THREE.Mesh(new THREE.BoxGeometry(.95, .02, .75), MAT.water); water.position.set(x, .62, z); g.add(water);
  const lbl = labelMesh("ULTRASONIC BATH", 1.0, .2, "#16405a", "#bff0ff", 50); lbl.position.set(x + .56, .45, z); lbl.rotation.y = Math.PI / 2; g.add(lbl);
  const b = { pos: new THREE.Vector3(x, .45, z), item: null, active: false, kind: "bath", group: g, r: rect(x - .55, x + .55, z - .45, z + .45) };
  water.userData.kind = "bath"; water.userData.slot = b; targets.push(water); baths.push(b);
}

// Shop: floor, tables, computer desk, online photo tables, delivery crate, sign, billboard
const shopFloor = new THREE.Mesh(new THREE.PlaneGeometry(22, 7), MAT.wood); shopFloor.rotation.x = -Math.PI / 2; shopFloor.position.set(15.5, .012, 6.5); shopFloor.receiveShadow = true; scene.add(shopFloor);
const slots = [];
function makeTable(cx) {
  const g = new THREE.Group(); scene.add(g);
  rbox(6, .08, 1, MAT.ply, cx, .88, 8, g, .02); for (const dx of [-2.85, 2.85]) for (const dz of [-.4, .4]) rbox(.07, .84, .07, MAT.metal, cx + dx, .42, 8 + dz, g, .01);
  const r = rect(cx - 3, cx + 3, 7.5, 8.5);
  const list = [];
  for (let i = 0; i < 4; i++) {
    const sx = cx - 2.25 + i * 1.5;
    const pad = new THREE.Mesh(new THREE.BoxGeometry(1.25, .01, .85), new THREE.MeshStandardMaterial({ color: 0xc23b22, roughness: .9, transparent: true, opacity: .25 }));
    pad.position.set(sx, .925, 8); g.add(pad);
    const slot = { pos: new THREE.Vector3(sx, .925, 8), item: null, reserved: false, active: false, kind: "slot" };
    pad.userData.kind = "slot"; pad.userData.slot = slot; targets.push(pad); slots.push(slot); list.push(slot);
  }
  return { g, r, list };
}
const tables = [makeTable(9), makeTable(15.6), makeTable(22.2)];
const termLbl = labelMesh("COMPUTER\nupgrades · requests", .7, .3, "#10202f", "#7fe0ff", 46); termLbl.position.set(4.2, 1.55, 5.2); termLbl.rotation.y = -Math.PI / 2; scene.add(termLbl);
termLbl.userData.kind = "terminal"; targets.push(termLbl); rect(3.75, 4.65, 4.2, 6.2);
const onlineSpots = [];
for (const [x, z] of [[1.0, 4.4], [1.0, 2.4]]) {
  const g = new THREE.Group(); scene.add(g);
  rbox(1.0, .8, .8, MAT.white, x, .4, z, g, .05);
  const top = new THREE.Mesh(new THREE.BoxGeometry(.95, .01, .75), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .3 })); top.position.set(x, .805, z); g.add(top);
  const bd = labelMesh("JUNKBAY PHOTO\n+30% online", .9, .5, "#2a1a4a", "#ffd2ff", 60); bd.position.set(x, 1.65, z - .45); g.add(bd);
  rbox(.04, 1.6, .04, MAT.metal, x - .45, .8, z - .45, g, .01); rbox(.04, 1.6, .04, MAT.metal, x + .45, .8, z - .45, g, .01);
  const lamp = new THREE.PointLight(0xffffff, 3, 2.5, 2); lamp.position.set(x, 1.6, z + .3); g.add(lamp);
  const spot = { pos: new THREE.Vector3(x, .81, z), item: null, active: false, kind: "online", group: g, r: rect(x - .5, x + .5, z - .4, z + .4), timer: 0 };
  top.userData.kind = "online"; top.userData.slot = spot; targets.push(top); onlineSpots.push(spot);
}
const crateLbl = labelMesh("DELIVERY\nfor requests", .9, .42, "#2b2420", "#ffd27a", 70); crateLbl.position.set(2.6, 1.15, 6.88); scene.add(crateLbl);
crateLbl.userData.kind = "deliver"; targets.push(crateLbl);
const shopSign = new THREE.Group(); scene.add(shopSign);
rbox(.15, 3.4, .15, MAT.metal, 6, 1.7, 9.3, shopSign); rbox(.15, 3.4, .15, MAT.metal, 18.6, 1.7, 9.3, shopSign);
const signLbl = labelMesh("JUNK & WONDERS", 7, .9, "#c23b22", "#fff6d8", 110); signLbl.position.set(12.3, 3.1, 9.35); signLbl.rotation.y = Math.PI; shopSign.add(signLbl);
const signLbl2 = signLbl.clone(); signLbl2.rotation.y = 0; signLbl2.position.z = 9.25; shopSign.add(signLbl2);
const billboard = new THREE.Group(); scene.add(billboard);
rbox(.25, 4.2, .25, MAT.metal, -8, 2.1, 20.5, billboard); rbox(.25, 4.2, .25, MAT.metal, -2, 2.1, 20.5, billboard);
const bbLbl = labelMesh("JUNK & WONDERS\nwe buy everything", 6.4, 2.2, "#ffb02e", "#2b2420", 80); bbLbl.position.set(-5, 4.6, 20.4); bbLbl.rotation.y = Math.PI; billboard.add(bbLbl);

async function buildProps() {
  const P = [];
  for (let i = 0; i < 5; i++) P.push(prop("rollershutter_door", -2.4 + i * 1.2, 0, 0, 0, { keepX: [-1, 1] }).then((o) => { o.position.z = 0; door.add(o); o.scale.x = 1.12; o.traverse((c) => { if (c.isMesh) { c.userData.kind = "door"; targets.push(c); } }); }));
  P.push(prop("standing_chalkboard_01", 4.5, 0, -5.45, 0, { kind: "board" }));
  P.push(prop("steel_frame_shelves_01", -2.4, 0, -11.8, Math.PI / 2, { scale: .1 }));
  P.push(prop("steel_frame_shelves_01", 2.4, 0, -11.8, -Math.PI / 2, { scale: .1 }));
  P.push(prop("bench_vice_01", -6.75, .94, -2.2, 0));
  P.push(prop("metal_tool_chest", -7.6, 0, -2.6, 0, { collide: true }));
  P.push(prop("metal_trash_can", -6, 0, 2.6, Math.PI / 6, { keepX: [-2, 0], scale: 1.2, kind: "trash", collide: true }));
  P.push(prop("metal_office_desk", 4.2, 0, 5.2, Math.PI / 2));
  P.push(prop("classic_laptop", 4.25, .79, 5.2, -Math.PI / 2, { kind: "terminal" }));
  P.push(prop("wooden_crate_01", 2.6, 0, 7.3, 0, { scale: 1.3, kind: "deliver", collide: true }));
  P.push(prop("wooden_crate_01", 2.6, .45, 7.3, .2, { scale: 1.1, kind: "deliver" }));
  P.push(prop("CashRegister_01", 5.6, 0, 8.4, Math.PI, {}).then((o) => { o.position.y = 0; }));
  P.push(prop("covered_car", -8.5, 0, -10, .15, { collide: true }));
  P.push(prop("Barrel_01", 3.7, 0, -12.2, 0, { collide: true })); P.push(prop("Barrel_01", 3.7, 0, -11.5, 1, { collide: true }));
  P.push(prop("hand_truck", 3.6, 0, -8.6, -.6));
  P.push(prop("propane_tank", -10.3, 0, -3.2, 0, { collide: true }));
  P.push(prop("plastic_crate_01", -7.1, 0, 3.1, .3)); P.push(prop("plastic_crate_01", -7.1, .27, 3.1, .5));
  P.push(prop("potted_plant_01", 6.2, 0, 10.1, 0)); P.push(prop("potted_plant_01", 25.6, 0, 10.1, 1));
  P.push(prop("fire_hydrant", -3.2, 0, 13.6, 0, { keepX: [-1, 0] }));
  for (const x of [-22, -6, 10, 26]) P.push(prop("street_lamp_01", x, 0, 13.9, Math.PI, { collide: true }));
  P.push(prop("wooden_display_shelves_01", 25.8, 0, 6, -Math.PI / 2, { collide: true }));
  await Promise.all(P.map((p) => p.catch((e) => console.warn("prop failed", e))));
}

function applyUpgrades() {
  F = fx();
  tables.forEach((t, i) => { const on = i < F.tables; t.g.visible = on; t.r.active = on; t.list.forEach((s) => (s.active = on)); });
  baths.forEach((b, i) => { const on = i < F.baths; b.group.visible = on; b.r.active = on; b.active = on; });
  onlineSpots.forEach((b, i) => { const on = i < F.online; b.group.visible = on; b.r.active = on; b.active = on; });
  shopSign.visible = !!S.up.sign; billboard.visible = !!S.up.billboard;
}

// ---------------------------------------------------------------- items (PBR models + procedural grime shader)
const items = [];
const DIRT_GLSL = `
varying vec3 vDirtPos; uniform float uDirt; uniform float uDirtScale;
float dh(vec3 p){ return fract(sin(dot(p, vec3(12.9898,78.233,45.164)))*43758.5453); }
float dn(vec3 p){ vec3 i=floor(p), f=fract(p); f=f*f*(3.-2.*f);
  return mix(mix(mix(dh(i),dh(i+vec3(1,0,0)),f.x),mix(dh(i+vec3(0,1,0)),dh(i+vec3(1,1,0)),f.x),f.y),
             mix(mix(dh(i+vec3(0,0,1)),dh(i+vec3(1,0,1)),f.x),mix(dh(i+vec3(0,1,1)),dh(i+vec3(1,1,1)),f.x),f.y),f.z); }
float dfbm(vec3 p){ return dn(p)*.5 + dn(p*2.07)*.3 + dn(p*4.3)*.2; }`;
function dirtify(m, uni) {
  m.onBeforeCompile = (sh) => {
    sh.uniforms.uDirt = uni.uDirt; sh.uniforms.uDirtScale = uni.uDirtScale;
    sh.vertexShader = sh.vertexShader.replace("#include <common>", "#include <common>\nvarying vec3 vDirtPos;").replace("#include <begin_vertex>", "#include <begin_vertex>\nvDirtPos = (modelMatrix * vec4(position, 1.0)).xyz - (modelMatrix * vec4(0.,0.,0.,1.)).xyz;");
    sh.fragmentShader = sh.fragmentShader.replace("#include <common>", "#include <common>\n" + DIRT_GLSL)
      .replace("#include <map_fragment>", `#include <map_fragment>
        float dN = dfbm(vDirtPos * uDirtScale);
        float dG = dn(vDirtPos * uDirtScale * 7.0);
        float dMask = smoothstep(1.0 - uDirt - 0.05, 1.0 - uDirt + 0.05, dN * 0.85 + dG * 0.15) * step(0.002, uDirt);
        vec3 dCol = mix(vec3(0.085,0.065,0.04), vec3(0.24,0.18,0.115), dG);
        diffuseColor.rgb *= 1.0 - uDirt * 0.3;
        diffuseColor.rgb = mix(diffuseColor.rgb, dCol, dMask * 0.95);`)
      .replace("#include <roughnessmap_fragment>", "#include <roughnessmap_fragment>\nroughnessFactor = mix(roughnessFactor, 1.0, dMask);")
      .replace("#include <metalnessmap_fragment>", "#include <metalnessmap_fragment>\nmetalnessFactor = mix(metalnessFactor, 0.0, dMask);");
  };
  m.customProgramCacheKey = () => "dirt1";
}
async function createItem(id, saved) {
  const def = ITEMS[id]; if (!def) return null;
  const src = await loadModel(def.model);
  const { obj: group, size } = shapeModel(src, { keepX: def.keepX, rot: def.rot, scale: def.scale, minSize: .28 });
  const uni = { uDirt: { value: .7 }, uDirtScale: { value: 11 } };
  group.traverse((c) => { if (c.isMesh) { c.material = Array.isArray(c.material) ? c.material.map((m) => m.clone()) : c.material.clone(); [].concat(c.material).forEach((m) => dirtify(m, uni)); c.castShadow = c.receiveShadow = true; } });
  const it = { id, def, name: def.name, value: def.value, junk: !!def.junk, mystery: !!def.mystery, group, uni, size, maxDim: Math.max(size.x, size.y, size.z),
    condition: BALANCE.startCondition[0] + Math.random() * (BALANCE.startCondition[1] - BALANCE.startCondition[0]),
    rare: !!(def.rare && Math.random() < def.rare.chance * F.rare), shinyDone: false, place: "ground", holder: null, tag: null };
  if (saved) Object.assign(it, { condition: saved.c, name: saved.n, value: saved.v, junk: saved.j, mystery: saved.m, rare: saved.r, shinyDone: saved.s });
  group.traverse((o) => { o.userData.item = it; if (o.isMesh) targets.push(o); });
  applyCondition(it); scene.add(group); items.push(it); return it;
}
function applyCondition(it) { it.uni.uDirt.value = Math.max(0, (1 - it.condition) * .88); }
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
const parts = []; const pGeo = new THREE.SphereGeometry(.018, 6, 4);
function burst(pos, color, n = 8, speed = 1.5, life = .6) {
  for (let i = 0; i < n; i++) {
    const m = new THREE.Mesh(pGeo, new THREE.MeshBasicMaterial({ color, toneMapped: false })); m.position.copy(pos); scene.add(m);
    parts.push({ m, v: new THREE.Vector3((Math.random() - .5) * speed, Math.random() * speed, (Math.random() - .5) * speed), life, max: life });
  }
}
const marker = new THREE.Mesh(new THREE.ConeGeometry(.2, .42, 24), new THREE.MeshBasicMaterial({ color: 0xffd23f, depthTest: false, toneMapped: false }));
marker.rotation.x = Math.PI; marker.renderOrder = 10; scene.add(marker); marker.visible = false;

// ---------------------------------------------------------------- UI helpers
function money(n) { return "$" + Math.round(n).toLocaleString("en-US"); }
function toast(html, cls = "") { const t = document.createElement("div"); t.className = "toast " + cls; t.innerHTML = html; $("toasts").appendChild(t); while ($("toasts").children.length > 5) $("toasts").firstChild.remove(); setTimeout(() => t.remove(), 4200); }
function unlock(id) {
  if (S.ach[id]) return; const a = ACHIEVEMENTS.find((x) => x.id === id); if (!a) return;
  S.ach[id] = Date.now(); sfx.ach(); toast(`🏆 Achievement unlocked: <b>${a.name}</b><small>${a.desc}</small>`, "ach"); save();
  if (ACHIEVEMENTS.every((x) => S.ach[x.id])) setTimeout(finale, 1500);
}
function earn(n) { S.money += n; S.stats.earned += n; if (S.stats.earned >= 1000) unlock("grand"); if (S.stats.earned >= 10000) unlock("rich"); }
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
  const lv = `Lv <b>${S.lvl}</b> <span class="bar"><i style="width:${Math.min(100, S.xp / need * 100)}%"></i></span> ${S.xp}/${need} XP`;
  if ($("hud-lvl").innerHTML !== lv) $("hud-lvl").innerHTML = lv;
  const got = ACHIEVEMENTS.filter((a) => S.ach[a.id]).length;
  $("hud-ach").textContent = `🏆 ${got}/${ACHIEVEMENTS.length} (Tab)`;
  const st = streak.n > 1 && performance.now() / 1000 - streak.last < BALANCE.streakWindow;
  $("hud-streak").hidden = !st; if (st) $("hud-streak").textContent = `🔥 x${streak.n} streak  +${Math.round((streak.n - 1) * BALANCE.streakBonus * 100)}%`;
  let html;
  if (S.tut >= 0 && S.tut < TUTORIAL.length) html = `<div class="tut-h">Tutorial ${S.tut + 1}/${TUTORIAL.length}</div>${TUTORIAL[S.tut].text}<div class="tut-skip">T = skip tutorial</div>`;
  else {
    const inGarage = items.filter((i) => i.place === "garage").length;
    const online = onlineSpots.filter((s) => s.item).map((s) => `📸 ${s.item.name}: offer in ${Math.max(0, Math.ceil(s.timer))}s`).join("<br>");
    html = (inGarage ? `${inGarage} items left in your lot.` : `Garage empty: buy another lot at the <b>LOTS</b> board.`) + (online ? `<br>${online}` : "");
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
  else if (type === "sell") { const n = 3 + Math.floor(Math.random() * 5); q = { type, n, text: `Sell ${n} items`, reward: Math.round(12 * n * top * top), xp: 40 }; }
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
let panelOpen = false, auction = null;
function openPanel(html, bind) {
  panelOpen = true; scrubbing = null; keys.clear();
  if (document.pointerLockElement) document.exitPointerLock();
  $("panel-body").innerHTML = html + `<div style="text-align:right;margin-top:10px"><button class="ghost" id="p-close">Back to game (Esc)</button></div>`;
  $("panel").hidden = false; $("p-close").onclick = closePanel; bind && bind();
}
function closePanel() { if (auction && auction.running) return toast("The auction is still running!"); $("panel").hidden = true; panelOpen = false; auction = null; lockPointer(); }
function lotsPanel() {
  const rows = LOTS.map((l) => {
    const need = l.needs && UPGRADES.find((u) => u.id === l.needs), locked = need && !S.up[l.needs];
    return `<div class="row"><div class="t"><b>${l.name} — ${money(l.price)}</b><span>${locked ? "🔒 Needs the " + need.name + " upgrade" : l.hint}</span></div>
      <button data-lot="${l.id}" ${locked || S.money < l.price ? "disabled" : ""}>Buy</button></div>`;
  }).join("");
  const now = Date.now(), ready = !S.flags.auctionAt || now >= S.flags.auctionAt;
  const aucRows = S.up.paddle ? LOTS.filter((l) => !l.needs || S.up[l.needs]).map((l) =>
    `<div class="row"><div class="t"><b>🔨 Sealed ${l.name}</b><span>Bigger lot (+3 items) with a guaranteed rare. Bidding starts at ${money(l.price * .6)}.</span></div>
     <button data-auc="${l.id}" ${!ready || S.money < l.price * .6 ? "disabled" : ""}>${ready ? "Join" : "Soon"}</button></div>`).join("")
    + (ready ? "" : `<p class="sub">Next auction in ${Math.ceil((S.flags.auctionAt - now) / 1000)}s.</p>`)
    : `<p class="sub">🔒 Buy the <b>Auction Paddle</b> upgrade to join storage auctions.</p>`;
  openPanel(`<h2>Lots for sale</h2><p class="sub">You have ${money(S.money)}. What's inside? Nobody knows. That's the fun.</p>${rows}<div class="cat">Auctions</div>${aucRows}`, () => {
    document.querySelectorAll("[data-lot]").forEach((b) => (b.onclick = () => { buyLot(LOTS.find((l) => l.id === b.dataset.lot)); closePanel(); }));
    document.querySelectorAll("[data-auc]").forEach((b) => (b.onclick = () => startAuction(LOTS.find((l) => l.id === b.dataset.auc))));
  });
}
// ---- auctions: bots with hidden max bids, 7-second countdown resets on every bid
const BOTS = ["Gary_Storage_King", "xX_FlipQueen_Xx", "Uncle Bob", "AntiqueAndy", "BargainBarbara"];
function startAuction(lot) {
  const bots = [...BOTS].sort(() => Math.random() - .5).slice(0, 3).map((n) => ({ n, max: lot.price * (1.1 + Math.random() * 1.3) }));
  auction = { lot, bid: Math.round(lot.price * .6), leader: null, t: 7, bots, running: true, step: Math.max(5, Math.round(lot.price * .08)), botWait: 1.2, log: [] };
  renderAuction();
}
function renderAuction() {
  const a = auction; if (!a) return;
  const you = a.leader === "You";
  const html = `<h2>🔨 Auction: Sealed ${a.lot.name}</h2><p class="sub">Highest bid wins when the timer hits 0. You have ${money(S.money)}.</p>
    <div class="auc"><div class="auc-bid">${money(a.bid)}</div><div class="auc-lead">${a.leader ? (you ? "🟢 You are winning!" : "🔴 " + a.leader + " leads") : "No bids yet"}</div>
    <div class="auc-t" id="auc-t">${a.running ? `⏱ ${a.t.toFixed(1)}s` : "SOLD!"}</div></div>
    <div class="auc-log">${a.log.slice(-5).reverse().join("<br>")}</div>
    ${a.running ? `<button id="a-bid" ${you || S.money < a.bid + a.step ? "disabled" : ""}>Bid ${money(a.bid + a.step)}</button> <button class="ghost" id="a-quit">Give up</button>` : ""}`;
  $("panel-body").innerHTML = html + (a.running ? "" : `<div style="text-align:right;margin-top:10px"><button class="ghost" id="p-close">Back to game (Esc)</button></div>`);
  $("panel").hidden = false; panelOpen = true; if (document.pointerLockElement) document.exitPointerLock();
  if ($("a-bid")) $("a-bid").onclick = () => { a.bid += a.step; a.leader = "You"; a.t = Math.max(a.t, 5); a.botWait = .8 + Math.random() * 1.6; a.log.push(`You bid ${money(a.bid)}`); sfx.bid(); renderAuction(); };
  if ($("a-quit")) $("a-quit").onclick = () => { a.running = false; S.flags.auctionAt = Date.now() + 60000; auction = null; closePanel(); };
  if ($("p-close")) $("p-close").onclick = () => { auction = null; closePanel(); };
}
function updateAuction(dt) {
  const a = auction; if (!a || !a.running) return;
  a.t -= dt; a.botWait -= dt;
  if (a.botWait <= 0 && a.leader !== null || (a.leader === null && a.botWait <= 0)) {
    const next = a.bid + a.step, cands = a.bots.filter((b) => b.max >= next && b.n !== a.leader);
    if (cands.length && Math.random() < .85) { const b = pick(cands); a.bid = next; a.leader = b.n; a.t = Math.max(a.t, 4); a.log.push(`${b.n} bids ${money(a.bid)}`); sfx.bid(); a.dirty = true; }
    a.botWait = 1 + Math.random() * 2.2;
  }
  if (a.t <= 0) {
    a.running = false; sfx.gavel(); S.flags.auctionAt = Date.now() + 90000;
    if (a.leader === "You") {
      S.money -= a.bid; S.stats.auctions++; unlock("auction"); addXP(40 * a.lot.tier);
      a.log.push(`🎉 SOLD to you for ${money(a.bid)}!`); buyLot(a.lot, { free: true, extra: 3, rare: true });
    } else a.log.push(a.leader ? `Sold to ${a.leader}. Better luck next time.` : "No bids. Auction closed.");
  }
  if (a.dirty || !a.running) { a.dirty = false; renderAuction(); } else if ($("auc-t")) $("auc-t").textContent = `⏱ ${Math.max(0, a.t).toFixed(1)}s`;
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
      <div class="row"><div class="t"><b>Lots bought: ${st.lots} · Auctions won: ${st.auctions} · Items sold: ${st.sold} (online ${st.online})</b><span>Junk recycled: ${st.trashed} · Requests done: ${st.requests} · Best streak: x${st.bestStreak}</span></div></div>
      <div class="row"><div class="t"><b>Total earned: ${money(st.earned)}</b><span>Most expensive sale: ${money(st.best)}</span></div></div>
      <div class="row"><div class="t"><b>Graphics: ${HIGH ? "High" : "Low"}</b><span>Press G in game to switch (Low = faster on weak PCs)</span></div></div>
      <p class="sub">Version ${VERSION} · Little Loop Games · 3D models & textures: Poly Haven (CC0)</p>`;
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
    $("p-reset").onclick = () => { if (confirm("Delete all progress?")) { worldReady = false; try { localStorage.removeItem(SAVE_KEY); } catch (e) {} location.reload(); } };
  });
}
function finale() {
  openPanel(`<h2>🏆 100% — Junk Lord of the Year!</h2><p class="sub">You collected every achievement.</p>
    <p>Lots bought: <b>${S.stats.lots}</b> · Items sold: <b>${S.stats.sold}</b> · Total earned: <b>${money(S.stats.earned)}</b></p>
    <p>Thanks for playing! Keep going as long as you like.</p>`);
  sfx.level(); for (let i = 0; i < 6; i++) setTimeout(() => burst(camera.position.clone().addScaledVector(forward(), 2), 0xffd23f, 30, 3, 1.2), i * 250);
}

// ---------------------------------------------------------------- lots
async function buyLot(lot, opt = {}) {
  if (!opt.free) { if (S.money < lot.price) return sfx.no(); S.money -= lot.price; }
  S.stats.lots++; addXP(15 * lot.tier); unlock("first_lot");
  if (lot.id === "student") unlock("student"); if (lot.id === "workshop") unlock("workshop"); if (lot.id === "mansion") unlock("mansion");
  questEvent("lot", { lot: lot.id });
  const left = items.filter((i) => i.place === "garage"); if (left.length) { left.forEach(removeItem); toast(`Leftovers from the last lot were hauled away.`); }
  doorOpen = 0; doorTarget = 0; sfx.door();
  toast(`You got <b>${lot.name}</b>. Opening the shutter...`);
  const ids = rollLot(lot, Math.random, opt.extra || 0);
  if (opt.rare) { const r = Object.entries(ITEMS).filter(([, d]) => d.tier === lot.tier && d.rare); if (r.length) ids[0] = pick(r)[0]; }
  await Promise.all(ids.map((id) => loadModel(ITEMS[id].model)));
  const cells = []; for (let gx = 0; gx < 4; gx++) for (let gz = 0; gz < 3; gz++) cells.push([-2.0 + gx * 1.33, -11.6 + gz * 1.35]);
  cells.sort(() => Math.random() - .5);
  for (let i = 0; i < ids.length; i++) {
    const it = await createItem(ids[i]); it.place = "garage";
    if (opt.rare && i === 0) it.rare = true;
    const [x, z] = cells[i % cells.length]; it.group.position.set(x + (Math.random() - .5) * .4, 0, z + (Math.random() - .5) * .3);
    it.group.rotation.y = Math.random() * Math.PI * 2;
  }
  doorTarget = 1; save();
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
$("btn-play").onclick = () => { $("start").hidden = true; started = true; audio(); lockPointer(); preloadAll(); };

addEventListener("keydown", (e) => {
  if (!started) return;
  if (e.code === "Tab") { e.preventDefault(); panelOpen ? closePanel() : achPanel(); return; }
  if (e.code === "Escape" && panelOpen) { if (auction && !auction.running) auction = null; closePanel(); return; }
  if (panelOpen) return;
  keys.add(e.code);
  if (e.code === "KeyE") interact();
  if (e.code === "KeyG") { setQuality(!HIGH); toast(`Graphics: <b>${HIGH ? "High" : "Low"}</b>`); save(); }
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
  if (now - lastScrubFx > 50) { lastScrubFx = now; burst(BENCH_POS.clone().add(new THREE.Vector3((Math.random() - .5) * .4, .1 + Math.random() * it.size.y * it.group.scale.x, .25)), Math.random() < .5 ? 0x6b5236 : 0xe8f4ff, 3, 1.2, .45); }
  if (it.condition >= 1) { if (noiseGain) noiseGain.gain.value = 0; scrubbing = null; onCleaned(it, BENCH_POS); }
}
function onCleaned(it, pos, auto = false) {
  if (it.shinyDone) return; it.shinyDone = true;
  sfx.shiny(); burst(pos.clone().add(new THREE.Vector3(0, .3, 0)), 0xfff3a0, 26, 2.2, .9);
  S.stats.shinies++; unlock("shiny"); if (auto) unlock("automation");
  addXP(it.junk ? 2 : 8 + Math.round(it.value / 20));
  if (it.mystery) {
    unlock("mystery"); const r = Math.random(), tier = it.def.tier;
    if (r < .12) { it.name = "Chest of Gold Coins"; it.value = 700 * tier; it.junk = false; toast(`🧰 The chest was full of <b>gold coins</b>! Worth ${money(priceOf(it))}!`, "ach"); unlock("jackpot"); }
    else if (r < .6) { it.name = "Chest of Old Coins"; it.value = Math.round((60 + Math.random() * 180) * tier); it.junk = false; toast(`🧰 The chest held <b>old coins</b>. Worth ${money(priceOf(it))}.`); }
    else { it.name = "Empty Chest (Nice Chest Though)"; it.value = 40 * tier; it.junk = false; toast(`🧰 The chest is empty... but it's a nice chest. Worth ${money(priceOf(it))}.`); }
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
    let vis = o.visible; o.traverseAncestors((a) => { if (a.visible === false) vis = false; }); if (!vis) continue;
    if (o.userData.item) { if (o.userData.item === carrying) continue; if (h.distance > 3.4) return null; return { item: o.userData.item, point: h.point }; }
    const k = o.userData.kind; if (!k) continue;
    if ((k === "slot" || k === "bath" || k === "online") && !o.userData.slot.active) continue;
    return { kind: k, slot: o.userData.slot, point: h.point, dist: h.distance };
  }
  return null;
}
function pickUp(it) {
  if (it.holder && (it.holder.reserved || it.holder.kind === "online")) return it.holder.kind === "online" ? toast("It's listed on JunkBay. Wait for the offer!") : sfx.no();
  if (it.holder) { it.holder.item = null; it.holder = null; }
  if (it.tag) { it.tag.parent.remove(it.tag); it.tag = null; }
  scene.remove(it.group); camera.add(it.group);
  it.group.position.set(.42, -.42, -.95); it.group.rotation.set(.15, -.5, 0); setScaleFit(it, .5);
  it.place = "carry"; carrying = it; sfx.pick();
  if (it.junk && !S.flags.junkTip) { S.flags.junkTip = 1; toast("This is <b>junk</b>. Recycle it in the rusty bin for a little cash."); }
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
    if (a && a.kind === "online") {
      if (a.slot.item) return toast("Already listing something here.");
      if (it.junk) return toast("Nobody buys junk online. Recycle it!");
      putDown(it, a.slot.pos, "online", .85, a.slot);
      a.slot.timer = (BALANCE.onlineWait[0] + Math.random() * (BALANCE.onlineWait[1] - BALANCE.onlineWait[0])) / F.onlineSpeed;
      burst(a.slot.pos.clone().add(new THREE.Vector3(0, .6, 0)), 0xffffff, 12, 1.5, .3);
      return toast(`📸 Listed <b>${it.name}</b> on JunkBay for ${money(priceOf(it) * BALANCE.onlineBonus)}. Waiting for offers...`);
    }
    if (a && a.kind === "deliver") return deliver(it);
    if (a && a.kind === "trash") {
      camera.remove(it.group); removeItem(it); carrying = null; sfx.trash(); burst(new THREE.Vector3(-6, 1.1, 2.6), 0x555555, 10);
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
  camera.remove(it.group); removeItem(it); carrying = null; burst(new THREE.Vector3(2.6, 1.2, 7.3), 0xffd27a, 16, 2);
  completeQuest(q); save();
}
function hintFor(a) {
  if (carrying) {
    const n = `<b>${carrying.name}</b>`;
    if (a && a.kind === "bench") return `<b>E</b> place ${n} on the workbench`;
    if (a && a.kind === "bath") return a.slot.item ? "Bath busy" : `<b>E</b> put ${n} in the bath (cleans by itself)`;
    if (a && a.kind === "slot") return a.slot.item ? "Spot taken" : `<b>E</b> sell ${n} for <b>${money(priceOf(carrying))}</b>`;
    if (a && a.kind === "online") return a.slot.item ? "Already listing" : `<b>E</b> list ${n} on JunkBay for <b>${money(priceOf(carrying) * BALANCE.onlineBonus)}</b>`;
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
    if (it.place === "online") return `<b>${it.name}</b> listed on JunkBay · offer in ${Math.ceil(it.holder ? it.holder.timer : 0)}s`;
    return `<b>E</b> pick up <b>${it.name}</b> · ${info}`;
  }
  return { board: "<b>E</b> lots & auctions", terminal: "<b>E</b> computer: upgrades & requests", door: "Your garage. Buy a lot to open it.", bench: "Workbench: bring an item here", slot: "Shop table: bring an item to sell", trash: "Recycle junk here", deliver: "Delivery crate: bring requested items here", bath: "Ultrasonic bath: drop a dirty item in", online: "JunkBay photo table: list an item online (+30%)" }[a.kind] || "";
}

// ---------------------------------------------------------------- customers
const customers = []; let custTimer = 3;
const bodyGeo = new THREE.CapsuleGeometry(.24, .8, 6, 16), headGeo = new THREE.SphereGeometry(.17, 24, 16);
const custColors = [0x8fa3b8, 0xb89f8f, 0x9fb88f, 0xb88fae, 0xa8a8a8, 0xd9b26a];
function spawnCustomer() {
  const free = slots.filter((s) => s.active && s.item && !s.reserved); if (!free.length) return;
  const slot = free[Math.floor(Math.random() * free.length)]; slot.reserved = true;
  const g = new THREE.Group(), c = custColors[Math.floor(Math.random() * custColors.length)];
  const b = new THREE.Mesh(bodyGeo, new THREE.MeshStandardMaterial({ color: c, roughness: .6 })); b.position.y = .66; g.add(b);
  const h = new THREE.Mesh(headGeo, new THREE.MeshStandardMaterial({ color: 0xe9e4dc, roughness: .35 })); h.position.y = 1.42; g.add(h);
  shadowy(g, true, false);
  g.position.set(slot.pos.x + (Math.random() - .5) * 8, 0, 20); scene.add(g);
  customers.push({ g, slot, state: "in", t: 0, target: new THREE.Vector3(slot.pos.x, 0, 8.95) });
}
function sell(it, online = false) {
  const now = performance.now() / 1000;
  let p;
  if (online) { p = Math.round(priceOf(it) * BALANCE.onlineBonus); S.stats.online++; unlock("online"); }
  else {
    streak.n = now - streak.last < BALANCE.streakWindow ? Math.min(5, streak.n + 1) : 1; streak.last = now;
    S.stats.bestStreak = Math.max(S.stats.bestStreak, streak.n); if (streak.n >= 5) unlock("streak5");
    p = Math.round(priceOf(it) * (1 + (streak.n - 1) * BALANCE.streakBonus));
  }
  earn(p); addXP(5 + Math.round(p / 15)); S.stats.sold++; S.stats.best = Math.max(S.stats.best, p);
  unlock("first_sale"); if (S.stats.sold >= 50) unlock("sold50"); if (p >= 1000) unlock("whale");
  questEvent("sell"); questEvent("earn", { amount: p });
  sfx.cash(); burst(it.group.position.clone().add(new THREE.Vector3(0, .5, 0)), 0x5fd38d, 12, 1.6);
  toast(online ? `📦 JunkBay: <b>${it.name}</b> sold for <b>${money(p)}</b> and shipped!` : `Sold <b>${it.name}</b> for <b>${money(p)}</b>${streak.n > 1 ? ` · 🔥x${streak.n}` : ""}`);
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
      c.g.position.y = Math.abs(Math.sin(c.t * 9)) * .04; c.g.rotation.z = Math.sin(c.t * 9) * .04;
    } else if (c.state === "browse") {
      c.g.rotation.y = Math.PI; c.g.rotation.z = 0; c.g.children[1].position.y = 1.42 + Math.sin(c.t * 4) * .03;
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
  if (t === "board") return new THREE.Vector3(4.5, 2.1, -5.4);
  if (t === "garage") { const g = items.find((i) => i.place === "garage"); return g ? g.group.position.clone().add(new THREE.Vector3(0, 1.3, 0)) : new THREE.Vector3(0, 2.4, -9); }
  if (t === "bench") return carrying || bench.item ? new THREE.Vector3(-6, 2.0, -1.95) : null;
  if (t === "table") { const s = slots.find((x) => x.active && !x.item) || slots[0]; return new THREE.Vector3(s.pos.x, 2.0, s.pos.z); }
  if (t === "computer") return new THREE.Vector3(4.2, 2.1, 5.2);
  return null;
}

// ---------------------------------------------------------------- save / load world
function holderCode(h) { if (!h) return null; if (h.kind === "slot") return "s" + slots.indexOf(h); if (h.kind === "bath") return "b" + baths.indexOf(h); if (h.kind === "online") return "o" + onlineSpots.indexOf(h); return "w"; }
function serializeWorld() {
  return items.map((it) => {
    let x = it.group.position.x, z = it.group.position.z;
    if (it.place === "carry") { const f = forward(); x = camera.position.x + f.x; z = camera.position.z + f.z; }
    return { id: it.id, c: +it.condition.toFixed(3), n: it.name, v: it.value, j: it.junk, m: it.mystery, r: it.rare, s: it.shinyDone, p: it.place === "carry" ? "ground" : it.place,
      h: holderCode(it.holder), t: it.holder && it.holder.kind === "online" ? Math.round(it.holder.timer) : 0, x: +x.toFixed(2), z: +z.toFixed(2), ry: +it.group.rotation.y.toFixed(2) };
  });
}
async function loadWorld() {
  for (const w of S.world || []) {
    const it = await createItem(w.id, w).catch(() => null); if (!it) continue;
    let holder = null;
    if (w.h === "w") holder = bench; else if (w.h && w.h[0] === "s") holder = slots[+w.h.slice(1)]; else if (w.h && w.h[0] === "b") holder = baths[+w.h.slice(1)]; else if (w.h && w.h[0] === "o") holder = onlineSpots[+w.h.slice(1)];
    if (holder && ((!holder.active && holder.kind !== "bench") || holder.item)) holder = null;
    if (holder) {
      it.place = holder.kind === "bench" ? "bench" : holder.kind; it.holder = holder; holder.item = it;
      setScaleFit(it, { slot: 1.0, bath: .8, online: .85 }[holder.kind] || 1.1); it.group.position.copy(holder.pos);
      if (holder.kind === "online") holder.timer = w.t || 20;
      if (holder.kind === "slot") { it.tag = priceSprite(money(priceOf(it))); it.tag.position.set(holder.pos.x, holder.pos.y + Math.min(1.2, it.size.y * it.group.scale.x) + .25, holder.pos.z - .3); scene.add(it.tag); }
    } else { it.place = w.p === "garage" ? "garage" : "ground"; it.group.position.set(w.x, 0, w.z); it.group.rotation.y = w.ry || 0; }
  }
}
let preloading = false;
async function preloadAll() { if (preloading) return; preloading = true; for (const d of Object.values(ITEMS)) { await loadModel(d.model).catch(() => {}); } }

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
if (!HIGH) setQuality(false);
(async () => {
  const tier1 = Object.values(ITEMS).filter((d) => d.tier === 1).map((d) => loadModel(d.model).catch(() => {}));
  await Promise.all([buildProps(), ...tier1]);
  await loadWorld(); worldReady = true;
  if (S.tut < 0) fillQuests();
  $("load-txt").textContent = "Ready!"; $("btn-play").disabled = false;
})();
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
  door.position.y = doorOpen * 2.35; door.scale.y = 1 - doorOpen * .85; door.visible = doorOpen < .98; doorRect.active = doorOpen < .6;
  for (const b of baths) {
    const it = b.item; if (!b.active || !it || it.condition >= 1) continue;
    it.condition = Math.min(1, it.condition + BALANCE.bathRate * F.bathSpeed * dt); applyCondition(it);
    it.group.position.y = b.pos.y + Math.sin(now / 200) * .02;
    if (Math.random() < dt * 10) burst(b.pos.clone().add(new THREE.Vector3((Math.random() - .5) * .6, .2, (Math.random() - .5) * .5)), 0xd8f6ff, 1, .6, .7);
    if (it.condition >= 1) onCleaned(it, b.pos, true);
  }
  for (const o of onlineSpots) {
    if (!o.active || !o.item) continue;
    o.timer -= dt; o.item.group.rotation.y += dt * .6;
    if (o.timer <= 0) { const it = o.item; sell(it, true); o.item = null; }
  }
  for (let i = parts.length - 1; i >= 0; i--) {
    const p = parts[i]; p.life -= dt; p.v.y -= 4 * dt; p.m.position.addScaledVector(p.v, dt); p.m.scale.setScalar(Math.max(.01, p.life / p.max));
    if (p.life <= 0) { scene.remove(p.m); p.m.material.dispose(); parts.splice(i, 1); }
  }
  updateCustomers(dt); updateAuction(dt);
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
  if (HIGH) composer.render(); else renderer.render(scene, camera);
  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);
window.__game = { S, items, slots, baths, onlineSpots, bench, buyLot, LOTS, camera, get aim() { return aim; }, get carrying() { return carrying; }, interact, scrub, sell, computerPanel, closePanel, lotsPanel, startAuction,
  get auction() { return auction; }, setQuality, setLook(y, p) { yaw = y; pitch = p; }, lookAt(x, y, z) { const c = camera.position, dx = x - c.x, dz = z - c.z; yaw = Math.atan2(-dx, -dz); pitch = Math.atan2(y - c.y, Math.hypot(dx, dz)); }, customers, applyUpgrades, addXP };
