// 3D TOON look for the Karl series (matches the viral channel: 3D models + cel shading + outlines + glossy black heads).
// Reuses the pose system of ../rig.js (applyPose, POSES, blinkAt, shot). Characters are built here with toon materials.
import * as THREE from "three";
export { applyPose, POSES, blinkAt, shot } from "../rig.js";

const deg = (a) => a * Math.PI / 180;
// 3-tone ramp -> soft cel shading
const ramp = (() => { const d = new Uint8Array([90, 90, 90, 255, 175, 175, 175, 255, 255, 255, 255, 255]); const t = new THREE.DataTexture(d, 3, 1, THREE.RGBAFormat); t.minFilter = t.magFilter = THREE.NearestFilter; t.needsUpdate = true; return t; })();
export const TOON = (c, o = {}) => new THREE.MeshToonMaterial({ color: c, gradientMap: ramp, ...o });
// inverted-hull outline (normal extrusion works for any mesh)
const outlineMats = {};
function outlineMat(color, w) {
  const k = color + ":" + w; if (outlineMats[k]) return outlineMats[k];
  const m = new THREE.MeshBasicMaterial({ color, side: THREE.BackSide });
  m.onBeforeCompile = (s) => { s.vertexShader = s.vertexShader.replace("#include <begin_vertex>", `#include <begin_vertex>\n transformed += normal * ${w.toFixed(4)};`); };
  return (outlineMats[k] = m);
}
export function mesh(geo, mat, { outline = 0x1a1726, w = 0.02, shadow = true } = {}) {
  const g = new THREE.Group(); const m = new THREE.Mesh(geo, mat); m.castShadow = shadow; m.receiveShadow = true; g.add(m);
  if (outline !== null) g.add(new THREE.Mesh(geo, outlineMat(outline, w)));
  return g;
}
const capsuleGeo = (r, len) => { const g = new THREE.CapsuleGeometry(r, len, 8, 16); g.translate(0, -len / 2 - r * 0.2, 0); return g; };

export const CAST = {
  karl:     { name: "Karl", top: 0x2ec4b6, pants: 0x2f3b5c, strings: true },
  karl_red: { name: "Karl (red test)", top: 0xe0413b, pants: 0x2f3b5c, strings: true },
  mom:      { name: "Mom", top: 0x3fa874, pants: 0x2e3a55, hair: "long", hairColor: 0x7a4a2a, lashes: true, cardigan: true },
  dad:      { name: "Dad", top: 0x4a7fc1, pants: 0x8a7650, hair: "short", hairColor: 0x5a3e26, mustache: true, scale: 1.07, collar: true },
  mia:      { name: "Mia", top: 0x9a6edc, pants: 0x2c2c3c, hair: "buns", hairColor: 0x5a3524, scale: 0.74, lashes: true },
  grandma:  { name: "Grandma Rose", top: 0xc45c8a, pants: 0x4a4458, hair: "bun", hairColor: 0xdedce6, glasses: true, scale: 0.93, cardigan: true },
  max:      { name: "Max", top: 0xff6b5b, pants: 0x2f3542, hair: "curly", hairColor: 0x2a1a12, strings: true },
  lena:     { name: "Lena", top: 0xf2a6bf, pants: 0x384a6b, hair: "bob", hairColor: 0xc8843a, lashes: true },
};

// ---------------------------------------------------------------- face (painted on a front cap of the black sphere)
function paintFace(ctx, emo, blink, look, c) {
  const W = 512; ctx.clearRect(0, 0, W, W);
  const cx = 256, cy = 250, ex = 70, er = 62, lx = look[0] * 16, ly = look[1] * 12;
  const shocked = emo === "shock" || emo === "panic";
  const eh = blink < 0.5 ? 0.12 : emo === "smug" ? 0.55 : emo === "sleepy" ? 0.35 : shocked ? 1.15 : 1;
  for (const s of [-1, 1]) {
    ctx.save(); ctx.translate(cx + s * ex + lx * 0.5, cy + ly * 0.5); ctx.scale(shocked ? 1.1 : 1, eh);
    ctx.beginPath(); ctx.arc(0, 0, er, 0, 7); ctx.fillStyle = "#fbfaf7"; ctx.fill(); ctx.restore();
    if (eh > 0.3) {
      const pr = shocked ? 15 : 24, py = emo === "dazed" ? -28 : emo === "sad" ? 16 : 0;
      ctx.beginPath(); ctx.arc(cx + s * ex + lx * 1.5, cy + ly * 1.5 + py, pr, 0, 7); ctx.fillStyle = "#141218"; ctx.fill();
      ctx.beginPath(); ctx.arc(cx + s * ex + lx * 1.5 - pr * 0.4, cy + ly * 1.5 + py - pr * 0.4, pr * 0.32, 0, 7); ctx.fillStyle = "#fff"; ctx.fill();
    }
    if (c.lashes && eh > 0.3) { ctx.strokeStyle = "#fbfaf7"; ctx.lineWidth = 7; ctx.lineCap = "round"; for (const k of [-0.5, 0]) { const a = -Math.PI / 2 + s * (0.55 + k); ctx.beginPath(); ctx.moveTo(cx + s * ex + Math.cos(a) * er, cy + Math.sin(a) * er * eh); ctx.lineTo(cx + s * ex + Math.cos(a) * er * 1.28, cy + Math.sin(a) * er * 1.28 * eh); ctx.stroke(); } }
    if (c.glasses) { ctx.strokeStyle = "#cfcadb"; ctx.lineWidth = 7; ctx.beginPath(); ctx.arc(cx + s * ex, cy, er * 1.15, 0, 7); ctx.stroke(); }
  }
  if (["angry", "worried", "sad", "panic"].includes(emo)) { ctx.strokeStyle = "#fbfaf7"; ctx.lineWidth = 12; ctx.lineCap = "round";
    for (const s of [-1, 1]) { const tilt = emo === "angry" ? 18 : -18; ctx.beginPath(); ctx.moveTo(cx + s * ex - 40, cy - 92 + s * tilt); ctx.lineTo(cx + s * ex + 40, cy - 92 - s * tilt); ctx.stroke(); } }
  const my = cy + 120; ctx.lineCap = "round";
  if (["happy", "laugh", "love"].includes(emo)) { ctx.beginPath(); ctx.moveTo(cx - 44, my - 8); ctx.quadraticCurveTo(cx, my + (emo === "laugh" ? 62 : 42), cx + 44, my - 8); ctx.closePath(); ctx.fillStyle = "#e85a6a"; ctx.fill(); }
  else if (["shock", "panic"].includes(emo)) { ctx.beginPath(); ctx.ellipse(cx, my + 10, 20, 28, 0, 0, 7); ctx.fillStyle = "#e85a6a"; ctx.fill(); }
  else if (["sad", "worried"].includes(emo)) { ctx.beginPath(); ctx.arc(cx, my + 34, 26, Math.PI * 1.15, Math.PI * 1.85); ctx.strokeStyle = "#fbfaf7"; ctx.lineWidth = 9; ctx.stroke(); }
  else if (emo === "smug") { ctx.beginPath(); ctx.moveTo(cx - 26, my); ctx.quadraticCurveTo(cx + 10, my + 18, cx + 40, my - 14); ctx.strokeStyle = "#fbfaf7"; ctx.lineWidth = 9; ctx.stroke(); }
  else { ctx.beginPath(); ctx.arc(cx, my - 14, 22, Math.PI * 0.2, Math.PI * 0.8); ctx.strokeStyle = "#fbfaf7"; ctx.lineWidth = 9; ctx.stroke(); }
  if (["happy", "laugh", "love", "dazed", "shy"].includes(emo)) for (const s of [-1, 1]) { ctx.beginPath(); ctx.ellipse(cx + s * 140, cy + 78, 34, 18, 0, 0, 7); ctx.fillStyle = "rgba(255,120,150,0.6)"; ctx.fill(); }
  if (emo === "panic" || emo === "worried") { ctx.beginPath(); ctx.moveTo(cx + 175, cy - 90); ctx.quadraticCurveTo(cx + 205, cy - 30, cx + 175, cy - 15); ctx.quadraticCurveTo(cx + 145, cy - 30, cx + 175, cy - 90); ctx.fillStyle = "#8fd3ff"; ctx.fill(); }
  if (c.mustache) { ctx.fillStyle = "#e9e2d8"; ctx.beginPath(); ctx.ellipse(cx - 30, my - 34, 34, 13, 0.2, 0, 7); ctx.ellipse(cx + 30, my - 34, 34, 13, -0.2, 0, 7); ctx.fill(); }
}
export function setFace(ch, emo, blink = 1, look = [0, 0]) {
  const key = emo + (blink > 0.5 ? "o" : "c") + look.join(","); if (key === ch.lastKey) return; ch.lastKey = key;
  paintFace(ch.ctx, emo, blink, look, ch.spec); ch.tex.needsUpdate = true;
}

// ---------------------------------------------------------------- character
export function makeChar(who) {
  const c = typeof who === "string" ? CAST[who] : who; const S = c.scale || 1;
  const mTop = TOON(c.top), mPants = TOON(c.pants), mInk = TOON(0x1c1a22), mShoe = TOON(0xf4f2ee);
  const root = new THREE.Group(); const scaler = new THREE.Group(); scaler.scale.setScalar(S); root.add(scaler);
  const hips = new THREE.Group(); hips.position.y = 1.0; scaler.add(hips);
  const torso = new THREE.Group(); hips.add(torso);
  // hoodie body: soft rounded block
  const bodyGeo = new THREE.CapsuleGeometry(0.46, 0.42, 10, 24); const body = mesh(bodyGeo, mTop); body.scale.set(1.1, 1, 0.72); body.position.y = 0.52; torso.add(body);
  const hem = mesh(new THREE.CylinderGeometry(0.5, 0.5, 0.12, 24), TOON(new THREE.Color(c.top).multiplyScalar(0.82))); hem.scale.set(1.0, 1, 0.68); hem.position.y = 0.08; torso.add(hem);
  if (!c.cardigan && !c.collar) {
    const pocket = mesh(new THREE.CapsuleGeometry(0.12, 0.42, 6, 12), TOON(new THREE.Color(c.top).multiplyScalar(0.85)), { w: 0.012 }); pocket.rotation.z = Math.PI / 2; pocket.scale.set(1, 1, 0.4); pocket.position.set(0, 0.3, 0.33); torso.add(pocket);
    const hood = mesh(new THREE.TorusGeometry(0.3, 0.1, 10, 24), TOON(new THREE.Color(c.top).multiplyScalar(0.88))); hood.rotation.x = Math.PI / 2 - 0.25; hood.position.set(0, 1.0, -0.05); torso.add(hood);
    if (c.strings) for (const s of [-1, 1]) { const st = mesh(new THREE.CylinderGeometry(0.018, 0.018, 0.32), TOON(0xffffff), { w: 0.008 }); st.position.set(s * 0.11, 0.8, 0.37); st.rotation.x = -0.2; torso.add(st);
      const tip = mesh(new THREE.SphereGeometry(0.035, 10, 8), TOON(0xffffff), { w: 0.008 }); tip.position.set(s * 0.11, 0.63, 0.4); torso.add(tip); }
  }
  if (c.cardigan) { const band = mesh(new THREE.BoxGeometry(0.16, 0.85, 0.05), TOON(0xf3efe6), { w: 0.01 }); band.position.set(0, 0.52, 0.34); torso.add(band); for (let i = 0; i < 3; i++) { const b = mesh(new THREE.SphereGeometry(0.035, 8, 6), TOON(0xffffff), { w: 0.006 }); b.position.set(0.12, 0.78 - i * 0.2, 0.36); torso.add(b); } }
  if (c.collar) { const col = mesh(new THREE.ConeGeometry(0.2, 0.2, 3), TOON(0xffffff), { w: 0.01 }); col.rotation.x = Math.PI; col.position.set(0, 0.92, 0.3); torso.add(col); }
  // head: glossy black sphere + light outline + specular dots + face cap
  const neck = new THREE.Group(); neck.position.y = 1.0; torso.add(neck);
  const head = new THREE.Group(); head.position.y = 0.68; neck.add(head);
  const skull = mesh(new THREE.SphereGeometry(0.78, 48, 32), TOON(0x1d1b23), { outline: 0xb7b2c4, w: 0.022 }); head.add(skull);
  for (const [x, y, r] of [[-0.34, 0.5, 0.07], [-0.2, 0.6, 0.035], [-0.44, 0.36, 0.03]]) { const sp = new THREE.Mesh(new THREE.SphereGeometry(r, 12, 8), new THREE.MeshBasicMaterial({ color: 0xe8e6f0 })); const z = Math.sqrt(Math.max(0, 0.78 * 0.78 - x * x - y * y)); sp.position.set(x, y, z - 0.01); sp.scale.z = 0.3; head.add(sp); }
  const cv = document.createElement("canvas"); cv.width = cv.height = 512; const ctx = cv.getContext("2d");
  const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace;
  const face = new THREE.Mesh(new THREE.SphereGeometry(0.785, 48, 32, Math.PI * 0.05, Math.PI * 0.9, Math.PI * 0.18, Math.PI * 0.64), new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false }));
  head.add(face);
  // hair / cap
  const hcol = TOON(c.hairColor || 0x333333);
  if (c.hat === "cap") {
    const dome = mesh(new THREE.SphereGeometry(0.805, 40, 20, 0, Math.PI * 2, 0, Math.PI * 0.4), TOON(c.hatColor)); dome.rotation.x = -0.2; head.add(dome);
    const brim = mesh(new THREE.CylinderGeometry(0.42, 0.42, 0.05, 24, 1, false, Math.PI * 0.6, Math.PI * 0.8), TOON(c.hatColor)); brim.scale.set(1, 1, 1.25); brim.position.set(0, 0.2, -0.72); brim.rotation.x = -0.55; head.add(brim);
    const btn = mesh(new THREE.SphereGeometry(0.06, 10, 8), TOON(0xffffff), { w: 0.008 }); btn.position.set(0, 0.76, -0.25); head.add(btn);
  }
  if (c.hair === "long" || c.hair === "bob") { const back = mesh(new THREE.SphereGeometry(0.87, 32, 24, Math.PI * 0.82, Math.PI * 1.36, 0, c.hair === "long" ? Math.PI * 0.85 : Math.PI * 0.65), hcol, { w: 0.015 }); back.position.set(0, 0.02, -0.04); back.scale.set(1.05, c.hair === "long" ? 1.18 : 1.02, 1); head.add(back);
    const top = mesh(new THREE.SphereGeometry(0.815, 32, 16, 0, Math.PI * 2, 0, Math.PI * 0.27), hcol); top.rotation.x = 0.15; head.add(top);
    const side = mesh(new THREE.SphereGeometry(0.3, 16, 12), hcol); side.scale.set(1.3, 0.55, 0.8); side.position.set(-0.42, 0.56, 0.42); side.rotation.z = 0.5; head.add(side); }
  if (c.hair === "short") { const top = mesh(new THREE.SphereGeometry(0.81, 32, 16, 0, Math.PI * 2, 0, Math.PI * 0.3), hcol); top.rotation.x = -0.1; head.add(top); }
  if (c.hair === "curly") for (let i = 0; i < 14; i++) { const a = i / 14 * Math.PI * 2, b = mesh(new THREE.SphereGeometry(0.2, 12, 10), hcol, { w: 0.015 }); b.position.set(Math.cos(a) * 0.55, 0.62 + Math.sin(i * 1.7) * 0.05, Math.sin(a) * 0.55 - 0.05); head.add(b); }
  if (c.hair === "buns") { const top = mesh(new THREE.SphereGeometry(0.81, 32, 16, 0, Math.PI * 2, 0, Math.PI * 0.3), hcol); head.add(top); for (const s of [-1, 1]) { const b = mesh(new THREE.SphereGeometry(0.24, 16, 12), hcol); b.position.set(s * 0.55, 0.62, -0.1); head.add(b); } }
  if (c.hair === "bun") { const top = mesh(new THREE.SphereGeometry(0.81, 32, 16, 0, Math.PI * 2, 0, Math.PI * 0.32), hcol); head.add(top); const b = mesh(new THREE.SphereGeometry(0.28, 16, 12), hcol); b.position.set(0, 0.88, -0.15); head.add(b); }
  // arms: sleeve capsules + black ball hands (thin, long)
  const arms = {};
  for (const side of ["L", "R"]) {
    const sx = side === "L" ? -1 : 1;
    const sh = new THREE.Group(); sh.position.set(0.5 * sx, 0.82, 0); torso.add(sh);
    sh.add(mesh(capsuleGeo(0.1, 0.36), mTop, { w: 0.014 }));
    const el = new THREE.Group(); el.position.y = -0.48; sh.add(el);
    el.add(mesh(capsuleGeo(0.075, 0.32), mInk, { w: 0.01 }));
    const hand = mesh(new THREE.SphereGeometry(0.13, 16, 12), mInk, { outline: 0x4a4656, w: 0.012 }); hand.position.y = -0.48; el.add(hand);
    const thumb = new THREE.Group(); el.add(thumb);
    const grip = new THREE.Group(); grip.position.y = -0.5; el.add(grip);
    arms[side] = { sh, el, hand, thumb, grip, sx };
  }
  const legs = {};
  for (const side of ["L", "R"]) {
    const sx = side === "L" ? -1 : 1;
    const hp = new THREE.Group(); hp.position.set(0.2 * sx, 0.05, 0); hips.add(hp);
    hp.add(mesh(capsuleGeo(0.1, 0.38), mPants, { w: 0.012 }));
    const kn = new THREE.Group(); kn.position.y = -0.5; hp.add(kn);
    kn.add(mesh(capsuleGeo(0.09, 0.3), mPants, { w: 0.012 }));
    const foot = mesh(new THREE.SphereGeometry(0.15, 16, 12), mShoe, { w: 0.012 }); foot.scale.set(1, 0.65, 1.6); foot.position.set(0, -0.47, 0.08); kn.add(foot);
    legs[side] = { hp, kn, sx };
  }
  const ch = { who: typeof who === "string" ? who : "extra", spec: c, root, hips, torso, neck, head, face, ctx, tex, arms, legs, lastKey: "" };
  setFace(ch, "neutral"); return ch;
}
export function worldPos(obj) { return obj.getWorldPosition(new THREE.Vector3()); }

const TOPS = [0xff6b5b, 0x4a7fc1, 0x3fa874, 0x9a6edc, 0xf2b84b, 0x38c6b4, 0xe86a9a, 0x7a8a9a, 0xd9734a, 0x5ab0e0];
const HAIRS = [null, "short", "curly", "bob", "long", "buns", null, "short"];
export function extraSpec(i) { const r = (k) => ((i * 9301 + k * 49297) % 233280) / 233280;
  return { name: "extra", top: TOPS[Math.floor(r(1) * TOPS.length)], pants: [0x2f3b5c, 0x2c2c3c, 0x4a4458, 0x384a6b][Math.floor(r(2) * 4)], hair: HAIRS[Math.floor(r(3) * HAIRS.length)], hairColor: [0x2a1a12, 0x5a3524, 0xc8843a, 0x7a4a2a][Math.floor(r(4) * 4)], strings: r(5) > 0.5, lashes: r(6) > 0.6, scale: 0.92 + r(7) * 0.12 }; }

// ---------------------------------------------------------------- stage + sets
export function makeStage(w = 1920, h = 1080) {
  const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
  renderer.setSize(w, h); renderer.setPixelRatio(1); renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  const scene = new THREE.Scene(); scene.background = new THREE.Color(0xe9dcc9);
  scene.add(new THREE.HemisphereLight(0xfff6ea, 0x9a8a9e, 1.6));
  const sun = new THREE.DirectionalLight(0xffffff, 2.0); sun.position.set(3, 8, 6); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, { left: -9, right: 9, top: 9, bottom: -9 }); sun.shadow.radius = 6; scene.add(sun);
  const camera = new THREE.PerspectiveCamera(32, w / h, 0.1, 200);
  return { renderer, scene, camera, sun };
}
function box(g, w, h, d, col, x, y, z, o = {}) { const m = mesh(new THREE.BoxGeometry(w, h, d), TOON(col), { outline: o.outline ?? 0x6e6270, w: o.w ?? 0.012, shadow: o.shadow ?? true }); m.position.set(x, y, z); g.add(m); return m; }
export function makeSet(scene, name) {
  const g = new THREE.Group(); scene.add(g);
  if (name === "kitchen") {
    const fl = new THREE.Mesh(new THREE.PlaneGeometry(40, 30), TOON(0xb98a63)); fl.rotation.x = -Math.PI / 2; fl.receiveShadow = true; g.add(fl);
    const wall = new THREE.Mesh(new THREE.PlaneGeometry(40, 14), TOON(0xe9dcc9)); wall.position.set(0, 7, -4); wall.receiveShadow = true; g.add(wall);
    for (let i = 0; i < 5; i++) { box(g, 1.15, 1.6, 0.9, 0x7fbab1, -6.2 + i * 1.22, 0.8, -3.5); box(g, 1.1, 1.1, 0.5, 0x8fcbc2, -6.2 + i * 1.22, 4.4, -3.7);
      box(g, 0.25, 0.06, 0.06, 0xe8e2d6, -6.2 + i * 1.22, 1.35, -3.03, { outline: null }); }
    box(g, 6.2, 0.12, 1.0, 0xece5d8, -3.75, 1.66, -3.5);
    const win = new THREE.Mesh(new THREE.PlaneGeometry(2.8, 2.0), new THREE.MeshBasicMaterial({ color: 0xa8dbf2 })); win.position.set(2.2, 3.5, -3.98); g.add(win);
    for (const [w2, h2, x, y] of [[3.0, 0.12, 2.2, 4.5], [3.0, 0.12, 2.2, 2.5], [0.12, 2.1, 0.7, 3.5], [0.12, 2.1, 3.7, 3.5], [0.1, 2.0, 2.2, 3.5]]) box(g, w2, h2, 0.1, 0xf6f1e7, x, y, -3.95, { outline: null });
    for (let i = 0; i < 4; i++) { const b = new THREE.Mesh(new THREE.CircleGeometry(0.5, 16, 0, Math.PI), new THREE.MeshBasicMaterial({ color: 0x86b872 })); b.position.set(1.0 + i * 0.75, 2.56, -3.96); g.add(b); }
    box(g, 1.6, 3.6, 1.1, 0xf2eee6, 5.6, 1.8, -3.3); box(g, 0.08, 0.7, 0.05, 0xc8c1b4, 5.0, 2.6, -2.72, { outline: null });
    box(g, 2.8, 0.12, 1.4, 0xd9a66f, 1.2, 1.25, -1.2); for (const [x, z] of [[-0.1, -1.7], [2.5, -1.7], [-0.1, -0.7], [2.5, -0.7]]) box(g, 0.1, 1.2, 0.1, 0xb9884f, x, 0.6, z);
  }
  if (name === "cafeteria") {
    const fl = new THREE.Mesh(new THREE.PlaneGeometry(40, 30), TOON(0xd8d2c4)); fl.rotation.x = -Math.PI / 2; fl.receiveShadow = true; g.add(fl);
    const wall = new THREE.Mesh(new THREE.PlaneGeometry(40, 14), TOON(0xf0e6d2)); wall.position.set(0, 7, -5); g.add(wall);
    box(g, 40, 1.2, 0.1, 0x5a8ac9, 0, 0.6, -4.95, { outline: null });
    for (let i = 0; i < 4; i++) { const w = new THREE.Mesh(new THREE.PlaneGeometry(2.2, 1.8), new THREE.MeshBasicMaterial({ color: 0xa8dbf2 })); w.position.set(-6 + i * 4, 3.6, -4.94); g.add(w); box(g, 2.4, 0.12, 0.1, 0xffffff, -6 + i * 4, 2.65, -4.9, { outline: null }); }
    box(g, 3.2, 0.6, 0.05, 0x3f6e52, 0, 5.5, -4.93, { outline: null });
    for (const z of [-1.2, 2.2]) { box(g, 7, 0.12, 1.3, 0xece5d8, 0, 1.05, z); for (const x of [-3.2, 3.2]) box(g, 0.12, 1.0, 0.9, 0x9aa3ad, x, 0.5, z);
      for (const dz of [-1.05, 1.05]) box(g, 7, 0.1, 0.4, 0x5a8ac9, 0, 0.6, z + dz); }
  }
  if (name === "gym") {
    const fl = new THREE.Mesh(new THREE.PlaneGeometry(60, 40), TOON(0xd9a96a)); fl.rotation.x = -Math.PI / 2; fl.receiveShadow = true; g.add(fl);
    const wall = new THREE.Mesh(new THREE.PlaneGeometry(60, 20), TOON(0xe8dfcf)); wall.position.set(0, 10, -14); g.add(wall);
    for (let r = 0; r < 4; r++) box(g, 36, 0.5, 1.4, 0x8a6a4a, 0, 0.25 + r * 0.5, -6 - r * 1.4, { outline: 0x5a4532 });
    box(g, 4, 0.5, 2, 0x3a4a6a, 0, 0.25, 5.5); const pole = mesh(new THREE.CylinderGeometry(0.03, 0.03, 1.6), TOON(0x222222)); pole.position.set(0.9, 1.3, 5.6); g.add(pole);
    const banner = new THREE.Mesh(new THREE.PlaneGeometry(8, 1.4), new THREE.MeshBasicMaterial({ color: 0x2ec4b6 })); banner.position.set(0, 7.5, -13.9); g.add(banner);
  }
  if (name === "void") { const fl = new THREE.Mesh(new THREE.CircleGeometry(30, 32), TOON(0x3a3060)); fl.rotation.x = -Math.PI / 2; fl.receiveShadow = true; g.add(fl); }
  return g;
}
