// Rounded 3D cast for The Other Timeline ("clay" style): rigged characters from cast.js, meme faces, poses, props, sets.
import * as THREE from "three";
import { CAST } from "./cast.js";
export { CAST };
const MAT = (c, o = {}) => new THREE.MeshStandardMaterial({ color: c, roughness: 0.62, metalness: 0.0, ...o });
const FLAT = (c, o = {}) => new THREE.MeshStandardMaterial({ color: c, flatShading: true, roughness: 0.75, ...o });
const deg = (a) => a * Math.PI / 180;
const capsule = (r, len, mat, seg = 16) => { const g = new THREE.CapsuleGeometry(r, len, 8, seg); g.translate(0, -len / 2 - r * 0.2, 0); const m = new THREE.Mesh(g, mat); m.castShadow = true; return m; };
const ball = (r, mat, seg = 24) => { const m = new THREE.Mesh(new THREE.SphereGeometry(r, seg, Math.round(seg * 0.7)), mat); m.castShadow = true; return m; };

// ---------------------------------------------------------------- meme faces (canvas painted on a front cap of the head)
const INK = "#1b1630";
export function drawFace(ctx, emo, blink = 1, look = [0, 0], overlays = []) {
  const S = 512; ctx.clearRect(0, 0, S, S);
  const cx = S / 2, ey = S * 0.44, ex = S * 0.17, er = S * 0.085;
  const lashes = overlays.includes("lashes");
  const eye = (x, sx = 1, sy = 1, pupil = 0.5) => {
    ctx.fillStyle = "#fff"; ctx.strokeStyle = INK; ctx.lineWidth = 9;
    ctx.beginPath(); ctx.ellipse(x, ey, er * sx, er * sy * Math.max(0.08, blink), 0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
    if (blink > 0.3) {
      ctx.fillStyle = INK; const pr = er * pupil;
      ctx.beginPath(); ctx.ellipse(x + look[0] * er * 0.35, ey + look[1] * er * 0.35, pr, pr, 0, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = "#fff"; ctx.beginPath(); ctx.arc(x + look[0] * er * 0.35 + pr * 0.35, ey - pr * 0.35, pr * 0.3, 0, Math.PI * 2); ctx.fill();
    }
    if (lashes) { ctx.strokeStyle = INK; ctx.lineWidth = 7; const s = x < cx ? -1 : 1; for (let i = 0; i < 3; i++) { ctx.beginPath(); ctx.moveTo(x + s * er * (0.3 + i * 0.3), ey - er * sy * 0.85); ctx.lineTo(x + s * er * (0.5 + i * 0.4), ey - er * sy * 1.35); ctx.stroke(); } }
  };
  const brow = (x, a, dy = -1.55) => { ctx.strokeStyle = INK; ctx.lineWidth = 14; ctx.lineCap = "round"; ctx.beginPath();
    ctx.moveTo(x - er * 1.1, ey + er * dy + Math.sin(a) * er * 0.6); ctx.lineTo(x + er * 1.1, ey + er * dy - Math.sin(a) * er * 0.6); ctx.stroke(); };
  const cheeks = (a = 0.35) => { ctx.fillStyle = `rgba(255,120,110,${a})`; for (const x of [cx - S * 0.27, cx + S * 0.27]) { ctx.beginPath(); ctx.ellipse(x, S * 0.6, S * 0.06, S * 0.035, 0, 0, Math.PI * 2); ctx.fill(); } };
  const mouthY = S * 0.66, L = cx - ex, R = cx + ex;
  const openMouth = (w, h, teeth = false) => { ctx.fillStyle = "#7a2836"; ctx.beginPath(); ctx.moveTo(cx - w, mouthY - 10); ctx.quadraticCurveTo(cx, mouthY + h, cx + w, mouthY - 10); ctx.closePath(); ctx.fill(); if (teeth) { ctx.fillStyle = "#fff"; ctx.fillRect(cx - w * 0.78, mouthY - 6, w * 1.56, 16); } };
  switch (emo) {
    case "happy": eye(L); eye(R); cheeks(); openMouth(60, 80); break;
    case "shock": eye(L, 1.35, 1.45, 0.28); eye(R, 1.35, 1.45, 0.28); cheeks(0.5); brow(L, 0.5, -2.1); brow(R, -0.5, -2.1);
      ctx.fillStyle = "#7a2836"; ctx.beginPath(); ctx.ellipse(cx, mouthY + 20, 34, 52, 0, 0, Math.PI * 2); ctx.fill(); break;
    case "smug": eye(L, 1, 0.45); eye(R, 1, 0.45); brow(L, -0.25); brow(R, 0.35); cheeks(0.25);
      ctx.strokeStyle = INK; ctx.lineWidth = 12; ctx.beginPath(); ctx.moveTo(cx - 40, mouthY); ctx.quadraticCurveTo(cx + 20, mouthY + 30, cx + 70, mouthY - 25); ctx.stroke(); break;
    case "sad": eye(L, 1, 1, 0.55); eye(R, 1, 1, 0.55); brow(L, 0.5); brow(R, -0.5);
      ctx.strokeStyle = INK; ctx.lineWidth = 12; ctx.beginPath(); ctx.moveTo(cx - 50, mouthY + 30); ctx.quadraticCurveTo(cx, mouthY - 20, cx + 50, mouthY + 30); ctx.stroke();
      ctx.fillStyle = "#8cc8ff"; ctx.beginPath(); ctx.ellipse(R + er * 0.2, ey + er * 1.6, 14, 26, 0, 0, Math.PI * 2); ctx.fill(); break;
    case "panic": eye(L, 1.5, 1.6, 0.18); eye(R, 1.5, 1.6, 0.18); brow(L, 0.7, -2.2); brow(R, -0.7, -2.2);
      ctx.fillStyle = "#7a2836"; ctx.beginPath(); ctx.ellipse(cx, mouthY + 30, 70, 50, 0, 0, Math.PI * 2); ctx.fill(); ctx.fillStyle = "#fff"; ctx.fillRect(cx - 55, mouthY - 5, 110, 18);
      ctx.fillStyle = "#8cc8ff"; for (const [x, y] of [[S * 0.12, S * 0.25], [S * 0.86, S * 0.3]]) { ctx.beginPath(); ctx.ellipse(x, y, 16, 28, 0.3, 0, Math.PI * 2); ctx.fill(); } break;
    case "money": ctx.font = "bold 150px Arial"; ctx.fillStyle = "#3ccf6a"; ctx.strokeStyle = INK; ctx.lineWidth = 8; ctx.textAlign = "center"; ctx.textBaseline = "middle";
      for (const x of [L, R]) { ctx.strokeText("$", x, ey); ctx.fillText("$", x, ey); } cheeks(0.45); openMouth(80, 110, true); break;
    case "laugh": ctx.strokeStyle = INK; ctx.lineWidth = 12; for (const x of [L, R]) { ctx.beginPath(); ctx.moveTo(x - er, ey + 10); ctx.lineTo(x, ey - 20); ctx.lineTo(x + er, ey + 10); ctx.stroke(); }
      cheeks(0.5); openMouth(75, 110);
      ctx.fillStyle = "#8cc8ff"; for (const x of [L - er * 1.2, R + er * 1.2]) { ctx.beginPath(); ctx.ellipse(x, ey + 30, 12, 24, 0, 0, Math.PI * 2); ctx.fill(); } break;
    case "angry": eye(L, 1, 0.8); eye(R, 1, 0.8); brow(L, -0.6, -1.3); brow(R, 0.6, -1.3); cheeks(0.6);
      ctx.strokeStyle = INK; ctx.lineWidth = 14; ctx.beginPath(); ctx.moveTo(cx - 55, mouthY + 20); ctx.lineTo(cx + 55, mouthY + 20); ctx.stroke(); break;
    case "wink": eye(L); ctx.strokeStyle = INK; ctx.lineWidth = 12; ctx.beginPath(); ctx.moveTo(R - er, ey); ctx.quadraticCurveTo(R, ey - 20, R + er, ey); ctx.stroke(); cheeks(0.4); openMouth(55, 60); break;
    default: eye(L); eye(R); cheeks(0.25);
      ctx.strokeStyle = INK; ctx.lineWidth = 11; ctx.beginPath(); ctx.moveTo(cx - 40, mouthY); ctx.quadraticCurveTo(cx, mouthY + 25, cx + 40, mouthY); ctx.stroke();
  }
  if (overlays.includes("freckles")) { ctx.fillStyle = "rgba(160,90,50,0.6)"; for (const [x, y] of [[-0.3, 0.56], [-0.25, 0.6], [-0.33, 0.62], [0.3, 0.56], [0.25, 0.6], [0.33, 0.62]]) { ctx.beginPath(); ctx.arc(cx + x * S, y * S, 5, 0, 7); ctx.fill(); } }
  if (overlays.includes("mustache")) { ctx.fillStyle = "#4a3022"; ctx.beginPath(); ctx.ellipse(cx - 32, mouthY - 22, 38, 15, 0.25, 0, 7); ctx.ellipse(cx + 32, mouthY - 22, 38, 15, -0.25, 0, 7); ctx.fill(); }
  if (overlays.includes("beard")) { ctx.fillStyle = "rgba(90,60,40,0.9)"; ctx.beginPath(); ctx.moveTo(cx - 150, mouthY - 40); ctx.quadraticCurveTo(cx, S * 1.02, cx + 150, mouthY - 40); ctx.quadraticCurveTo(cx, mouthY + 40, cx - 150, mouthY - 40); ctx.fill(); }
  if (overlays.includes("glasses")) { ctx.strokeStyle = "#3c3246"; ctx.lineWidth = 9; for (const x of [L, R]) { ctx.beginPath(); ctx.arc(x, ey, er * 1.45, 0, Math.PI * 2); ctx.stroke(); } ctx.beginPath(); ctx.moveTo(L + er * 1.45, ey); ctx.lineTo(R - er * 1.45, ey); ctx.stroke(); }
  if (overlays.includes("sunglasses")) { ctx.fillStyle = "#15151c"; for (const x of [L, R]) { ctx.beginPath(); ctx.roundRect(x - er * 1.6, ey - er * 1.0, er * 3.2, er * 1.9, 30); ctx.fill(); } ctx.fillRect(L, ey - er * 0.8, R - L, 12);
    ctx.fillStyle = "rgba(255,255,255,0.35)"; for (const x of [L, R]) ctx.fillRect(x - er * 1.1, ey - er * 0.7, er * 0.9, 12); }
  if (overlays.includes("sunglasses_up")) { ctx.fillStyle = "#15151c"; for (const x of [L, R]) { ctx.beginPath(); ctx.roundRect(x - er * 1.4, S * 0.13, er * 2.8, er * 1.3, 24); ctx.fill(); } }
}

// ---------------------------------------------------------------- character builder (rounded)
function hair(head, h, skinMat) {
  const c = MAT(h.color); const st = h.style;
  const cap = (k = 0.45, r = 0.8) => { const m = new THREE.Mesh(new THREE.SphereGeometry(r, 32, 16, 0, Math.PI * 2, 0, Math.PI * k), c); head.add(m); return m; };
  if (st === "short") cap(0.4, 0.8);
  if (st === "side") { for (const s of [-1, 1]) { const b = ball(0.28, c); b.scale.set(0.6, 0.9, 1.1); b.position.set(0.66 * s, 0.05, -0.15); head.add(b); } }
  if (st === "long") { cap(0.47, 0.81); const back = ball(0.7, c); back.scale.set(1.15, 1.3, 0.7); back.position.set(0, -0.35, -0.38); head.add(back); }
  if (st === "ponytail") { cap(0.45, 0.81); const t = capsule(0.18, 0.55, c); t.position.set(0, 0.45, -0.72); t.rotation.x = 0.5; head.add(t); }
  if (st === "bob") { cap(0.5, 0.82); for (const s of [-1, 1]) { const b = ball(0.38, c); b.scale.set(0.7, 1.1, 1.0); b.position.set(0.6 * s, -0.12, -0.05); head.add(b); } }
  if (st === "curly") { for (let i = 0; i < 16; i++) { const a = i / 16 * Math.PI * 2; const b = ball(0.24, c, 14); b.position.set(Math.cos(a) * 0.62, 0.42 + Math.sin(i * 1.7) * 0.08, Math.sin(a) * 0.62 - 0.1); if (b.position.z < 0.35) head.add(b); } cap(0.42, 0.82); }
  if (st === "spiky") { cap(0.42, 0.81); for (let i = 0; i < 7; i++) { const a = -1.1 + i * 0.37; const sp = new THREE.Mesh(new THREE.ConeGeometry(0.17, 0.5, 14), c); sp.position.set(Math.sin(a) * 0.6, 0.6 + Math.cos(a) * 0.1, -0.05); sp.rotation.z = -a * 0.8; head.add(sp); } }
  if (st === "bun") { cap(0.45, 0.81); const b = ball(0.3, c); b.position.set(0, 0.85, -0.2); head.add(b); }
  if (st === "slick") { const m = cap(0.42, 0.82); m.material = MAT(h.color, { roughness: 0.25 }); const q = ball(0.3, m.material); q.scale.set(1.3, 0.6, 0.8); q.position.set(0.15, 0.72, 0.25); head.add(q); }
  if (st === "cap" || st === "capback") { cap(0.42, 0.83); const brim = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.42, 0.05, 24, 1, false, 0, Math.PI), c); brim.position.set(0, 0.35, st === "cap" ? 0.6 : -0.6); brim.rotation.y = st === "cap" ? Math.PI / 2 * 0 : Math.PI; brim.scale.z = 1; head.add(brim);
    brim.rotation.set(0, st === "cap" ? -Math.PI / 2 : Math.PI / 2, 0); brim.position.set(0, 0.38, st === "cap" ? 0.55 : -0.55); }
  if (st === "fedora") { const crown = new THREE.Mesh(new THREE.CylinderGeometry(0.55, 0.62, 0.5, 28), c); crown.position.y = 0.72; head.add(crown); const brim = new THREE.Mesh(new THREE.CylinderGeometry(1.05, 1.05, 0.05, 32), c); brim.position.y = 0.5; head.add(brim);
    const band = new THREE.Mesh(new THREE.CylinderGeometry(0.63, 0.63, 0.1, 28), MAT(0x8a2a2a)); band.position.y = 0.55; head.add(band); }
}
export function makeChar(who) {
  const c = CAST[who]; const H = c.height || 1, belly = c.belly || 0;
  const mTop = MAT(c.top), mAcc = MAT(c.accent || c.top), mSkin = MAT(c.skin), mPants = MAT(c.pants), mShoe = MAT(c.shoes || 0x2a2a33);
  const root = new THREE.Group(); root.name = who;
  const scaler = new THREE.Group(); scaler.scale.setScalar(H); root.add(scaler);
  const hips = new THREE.Group(); hips.position.y = 1.0; scaler.add(hips);
  const torso = new THREE.Group(); hips.add(torso);
  const outfit = c.outfit;
  const coatMat = ["labcoat"].includes(outfit) ? MAT(0xf7f7f7) : mTop;
  const body = ball(0.62, coatMat, 32); body.scale.set(1 + belly * 0.25, 0.95, 0.85 + belly * 0.3); body.position.y = 0.5; torso.add(body);
  const pelvis = ball(0.6, mPants, 24); pelvis.scale.set(1 + belly * 0.15, 0.45, 0.8 + belly * 0.15); pelvis.position.y = 0.06; torso.add(pelvis);
  if (belly > 0) { const b = ball(0.45, coatMat); b.scale.set(1, 0.9, 0.7); b.position.set(0, 0.35, 0.25 + belly * 0.2); torso.add(b); }
  const front = (m, x, y, z, sx, sy, sz) => { const o = ball(0.5, m, 20); o.scale.set(sx, sy, sz); o.position.set(x, y, z); torso.add(o); return o; };
  if (outfit === "suit" || outfit === "blazer") { front(MAT(0xf2f2f6), 0, 0.68, 0.36, 0.38, 0.6, 0.35); for (const s of [-1, 1]) { const lap = front(mTop, 0.17 * s, 0.62, 0.42, 0.22, 0.55, 0.2); lap.rotation.z = 0.25 * s; } }
  if (outfit === "shirt") { front(MAT(0xffffff), 0, 0.98, 0.25, 0.42, 0.14, 0.35); for (let i = 0; i < 3; i++) { const b = ball(0.035, MAT(0xffffff), 10); b.position.set(0, 0.8 - i * 0.2, 0.53); torso.add(b); } }
  if (outfit === "hoodie") { for (const x of [-0.14, 0.14]) { const s = capsule(0.025, 0.3, MAT(0xfff4dc), 8); s.position.set(x, 0.9, 0.5); torso.add(s); } const pocket = front(MAT(c.accent || c.top), 0, 0.28, 0.42, 0.55, 0.22, 0.25); }
  if (outfit === "cardigan") { for (let i = 0; i < 4; i++) { const b = ball(0.045, MAT(0xf0e0c0), 10); b.position.set(0, 0.85 - i * 0.18, 0.54); torso.add(b); } front(MAT(0xf3efe6), 0, 0.82, 0.32, 0.25, 0.35, 0.35); }
  if (outfit === "vest") { front(MAT(0xf3efe6), 0, 0.7, 0.36, 0.3, 0.55, 0.36); }
  if (outfit === "coat") { const skirt = new THREE.Mesh(new THREE.CylinderGeometry(0.6, 0.75, 0.7, 28), mTop); skirt.position.y = -0.25; torso.add(skirt); front(MAT(0x222228), 0, 0.85, 0.36, 0.3, 0.35, 0.3); }
  if (outfit === "apron") { const a = new THREE.Mesh(new THREE.CylinderGeometry(0.57, 0.62, 0.95, 28, 1, true, -0.9, 1.8), MAT(c.accent || 0xd93c3c, { side: THREE.DoubleSide })); a.position.set(0, 0.42, 0.06); torso.add(a); }
  if (outfit === "labcoat") { const skirt = new THREE.Mesh(new THREE.CylinderGeometry(0.62, 0.78, 0.7, 28), MAT(0xf7f7f7)); skirt.position.y = -0.25; torso.add(skirt); front(MAT(c.accent || 0x5ab3e0), 0, 0.72, 0.33, 0.3, 0.5, 0.36); }
  for (const a of c.acc || []) {
    const [k, v] = a.split(":");
    if (k === "tie") { const t = capsule(0.07, 0.45, MAT(parseInt(v)), 10); t.position.set(0, 0.98, 0.55); t.scale.z = 0.5; torso.add(t); }
    if (k === "chain") { const ch = new THREE.Mesh(new THREE.TorusGeometry(0.32, 0.035, 10, 32), MAT(0xffcc33, { metalness: 0.8, roughness: 0.25 })); ch.position.set(0, 0.85, 0.32); ch.rotation.x = 1.15; torso.add(ch); const med = ball(0.09, ch.material); med.position.set(0, 0.6, 0.55); torso.add(med); }
    if (k === "badge" || k === "nametag") { const b = new THREE.Mesh(new THREE.BoxGeometry(0.24, 0.15, 0.03), MAT(0xffffff)); b.position.set(-0.25, 0.75, 0.53); b.rotation.x = -0.25; torso.add(b); }
    if (k === "stethoscope") { const s = new THREE.Mesh(new THREE.TorusGeometry(0.3, 0.03, 10, 32, Math.PI), MAT(0x333340)); s.position.set(0, 0.95, 0.3); s.rotation.set(1.2, 0, Math.PI); torso.add(s); const d = ball(0.08, MAT(0xc0c0c8, { metalness: 0.7 })); d.position.set(0.25, 0.55, 0.55); torso.add(d); }
    if (k === "keys") { const k2 = new THREE.Mesh(new THREE.TorusGeometry(0.08, 0.02, 8, 20), MAT(0xd0d0d8, { metalness: 0.8 })); k2.position.set(0.55, 0.0, 0.3); torso.add(k2); }
  }
  const neck = new THREE.Group(); neck.position.y = 1.02; torso.add(neck);
  const head = new THREE.Group(); head.position.y = 0.7; neck.add(head);
  const skull = ball(0.78, mSkin, 40); head.add(skull);
  for (const s of [-1, 1]) { const ear = ball(0.13, mSkin, 14); ear.scale.set(0.6, 1, 0.8); ear.position.set(0.77 * s, -0.02, -0.02); head.add(ear); }
  if ((c.acc || []).includes("earrings")) for (const s of [-1, 1]) { const e = ball(0.06, MAT(0xffd34d, { metalness: 0.7 })); e.position.set(0.8 * s, -0.17, 0); head.add(e); }
  if ((c.acc || []).includes("headphones")) { const band = new THREE.Mesh(new THREE.TorusGeometry(0.86, 0.05, 10, 40, Math.PI), MAT(0x222230)); band.position.y = 0.0; head.add(band); for (const s of [-1, 1]) { const cup = ball(0.2, MAT(0xff5fa0)); cup.scale.set(0.6, 1, 1); cup.position.set(0.85 * s, -0.02, 0); head.add(cup); } }
  if (c.hair.style === "hood") { const hood = ball(0.93, MAT(c.hair.color), 32); hood.position.set(0, 0.04, -0.17); hood.scale.set(1, 1, 0.85); head.add(hood); }
  else hair(head, c.hair, mSkin);
  const cv = document.createElement("canvas"); cv.width = cv.height = 512; const ctx = cv.getContext("2d");
  const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace;
  const face = new THREE.Mesh(new THREE.SphereGeometry(0.795, 40, 24, Math.PI * 0.05, Math.PI * 0.9, Math.PI * 0.18, Math.PI * 0.64),
    new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false }));
  head.add(face);
  const nose = ball(0.09, mSkin, 16); nose.position.set(0, -0.05, 0.79); head.add(nose);
  const arms = {};
  for (const side of ["L", "R"]) {
    const sx = side === "L" ? -1 : 1;
    const sh = new THREE.Group(); sh.position.set(0.58 * sx * (1 + belly * 0.15), 0.86, 0); torso.add(sh);
    const shoulder = ball(0.17, outfit === "labcoat" ? MAT(0xf7f7f7) : mTop); sh.add(shoulder);
    const sleeve = outfit === "labcoat" ? MAT(0xf7f7f7) : (outfit === "tee" || outfit === "apron" ? mTop : mTop);
    sh.add(capsule(0.13, 0.38, sleeve));
    const el = new THREE.Group(); el.position.y = -0.5; sh.add(el);
    el.add(capsule(0.115, 0.32, outfit === "tee" ? mSkin : sleeve));
    const hand = ball(0.16, mSkin); hand.scale.set(1, 1.05, 0.85); hand.position.y = -0.5; el.add(hand);
    const thumb = capsule(0.05, 0.08, mSkin, 10); thumb.position.set(-0.12 * sx, -0.42, 0.06); thumb.rotation.z = 0.8 * sx; el.add(thumb);
    const grip = new THREE.Group(); grip.position.y = -0.55; el.add(grip);
    arms[side] = { sh, el, hand, thumb, grip, sx };
  }
  if ((c.acc || []).includes("phone")) { const p = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.32, 0.03), MAT(0x15151c)); p.position.set(0, -0.08, 0.12); arms.R.grip.add(p); }
  const legs = {};
  for (const side of ["L", "R"]) {
    const sx = side === "L" ? -1 : 1;
    const hp = new THREE.Group(); hp.position.set(0.26 * sx, 0, 0); hips.add(hp);
    hp.add(capsule(0.16, 0.36, mPants));
    const kn = new THREE.Group(); kn.position.y = -0.5; hp.add(kn);
    kn.add(capsule(0.14, 0.28, mPants));
    const foot = ball(0.17, mShoe); foot.scale.set(1, 0.7, 1.6); foot.position.set(0, -0.44, 0.1); kn.add(foot);
    legs[side] = { hp, kn, sx };
  }
  const ch = { who, root, hips, torso, neck, head, face, ctx, tex, arms, legs, overlays: c.face || [], lastKey: "" };
  setFace(ch, "neutral");
  return ch;
}
export function setFace(ch, emo, blink = 1, look = [0, 0]) {
  const key = emo + (blink > 0.3 ? "o" : "c") + look.map((v) => v.toFixed(1)).join(",");
  if (key === ch.lastKey) return; ch.lastKey = key;
  drawFace(ch.ctx, emo, blink, look, ch.overlays); ch.tex.needsUpdate = true;
}

// ---------------------------------------------------------------- poses: arm = [forward deg, outward deg, elbow deg], leg = [forward, knee]
export const POSES = {
  idle:     { L: [5, 10, 10], R: [5, 10, 10], LL: [0, 0], LR: [0, 0], spine: 0, head: [0, 0] },
  cheer:    { L: [0, 160, 10], R: [0, 160, 10], LL: [0, 0], LR: [0, 0], spine: -6, head: [-12, 0] },
  no:       { L: [5, 10, 10], R: [80, 10, 25], LL: [0, 0], LR: [0, 0], spine: -4, head: [0, -8], palm: true },
  point:    { L: [5, 12, 10], R: [88, 5, 0], LL: [0, 0], LR: [0, 0], spine: 0, head: [0, 0] },
  shrug:    { L: [20, 55, 95], R: [20, 55, 95], LL: [0, 0], LR: [0, 0], spine: 0, head: [6, 12] },
  facepalm: { L: [5, 10, 10], R: [60, -15, 130], LL: [0, 0], LR: [0, 0], spine: 8, head: [18, 0] },
  hold:     { L: [55, 18, 55], R: [55, 18, 55], LL: [0, 0], LR: [0, 0], spine: 0, head: [8, 0] },
  thumbsup: { L: [5, 10, 10], R: [35, 25, 100], LL: [0, 0], LR: [0, 0], spine: -4, head: [-4, 6], thumb: true },
  panic:    { L: [40, 140, 115], R: [40, 140, 115], LL: [0, 0], LR: [0, 0], spine: 5, head: [-6, 0] },
  slump:    { L: [-5, 4, 5], R: [-5, 4, 5], LL: [0, 0], LR: [0, 0], spine: 22, head: [28, 0] },
  jump:     { L: [0, 150, 20], R: [0, 150, 20], LL: [30, 50], LR: [-10, 40], spine: -8, head: [-10, 0], lift: 0.45 },
  sit:      { L: [40, 10, 40], R: [40, 10, 40], LL: [90, 90], LR: [90, 90], spine: 0, head: [0, 0], lift: -0.42 },
};
function lerpPose(a, b, k) {
  const out = {};
  for (const key of ["L", "R", "LL", "LR"]) out[key] = a[key].map((v, i) => v + (b[key][i] - v) * k);
  out.spine = a.spine + (b.spine - a.spine) * k; out.head = a.head.map((v, i) => v + (b.head[i] - v) * k);
  out.lift = (a.lift || 0) + ((b.lift || 0) - (a.lift || 0)) * k; out.palm = k > 0.5 ? b.palm : a.palm; out.thumb = k > 0.5 ? b.thumb : a.thumb;
  return out;
}
const ease = (k) => k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2;
// pose spec: string, or {from, to, t0, dur} for a transition; walk: true adds a walk cycle; squash adds bounce
export function applyPose(ch, spec, t, opts = {}) {
  let p;
  if (typeof spec === "string") p = lerpPose(POSES[spec], POSES[spec], 0);
  else { const k = ease(Math.max(0, Math.min(1, (t - spec.t0) / (spec.dur || 0.25)))); p = lerpPose(POSES[spec.from], POSES[spec.to], k); }
  if (opts.walk) {
    const w = t * 7.5, s = Math.sin(w);
    p.LL = [s * 32, Math.max(0, -Math.cos(w)) * 35]; p.LR = [-s * 32, Math.max(0, Math.cos(w)) * 35];
    p.L = [p.L[0] - s * 28, p.L[1], p.L[2] + 15]; p.R = [p.R[0] + s * 28, p.R[1], p.R[2] + 15];
    p.lift += Math.abs(Math.cos(w)) * 0.06;
  }
  for (const side of ["L", "R"]) {
    const a = ch.arms[side], [fw, out, elb] = p[side];
    a.sh.rotation.set(-deg(fw), 0, deg(out) * a.sx);
    a.el.rotation.set(-deg(elb), 0, 0);
    a.thumb.visible = true;
  }
  if (p.palm) ch.arms.R.hand.scale.set(1.25, 1.25, 0.55); else ch.arms.R.hand.scale.set(1, 1, 1);
  for (const side of ["L", "R"]) { const l = ch.legs[side], [fw, kn] = p["L" + side]; l.hp.rotation.set(-deg(fw), 0, 0); l.kn.rotation.set(deg(kn), 0, 0); }
  ch.torso.rotation.x = deg(p.spine); ch.head.rotation.set(deg(p.head[0]), deg(p.head[1]), 0);
  // idle life: breathing + head bob; squash & stretch on beats
  const br = Math.sin(t * 2.4 + (opts.seed || 0)) * 0.02;
  const sq = opts.squash ? Math.exp(-Math.max(0, t - opts.squash) * 7) * Math.sin(Math.max(0, t - opts.squash) * 30) * 0.12 : 0;
  ch.root.scale.set(1 - sq * 0.5, 1 + br + sq, 1 - sq * 0.5);
  ch.hips.position.y = 1.0 + p.lift + (opts.hop ? Math.abs(Math.sin(t * 9)) * 0.25 : 0);
  if (opts.shake) ch.root.position.x = (opts.baseX || 0) + Math.sin(t * 60) * 0.04;
}
export function blinkAt(t, seed = 0) { return ((t + seed) % 3.1) < 0.11 ? 0.1 : 1; }

// ---------------------------------------------------------------- props
function labelTex(text, w, h, bg, fg, font) {
  const cv = document.createElement("canvas"); cv.width = w; cv.height = h; const g = cv.getContext("2d");
  g.fillStyle = bg; g.fillRect(0, 0, w, h); g.fillStyle = fg; g.font = font; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(text, w / 2, h / 2);
  const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; return t;
}
export function bill(amount = "1") {
  const t = labelTex("$" + amount, 256, 128, "#5fcf86", "#1e5a35", "bold 80px Arial");
  const m = new THREE.Mesh(new THREE.BoxGeometry(0.62, 0.3, 0.015), [MAT(0x4fae6e), MAT(0x4fae6e), MAT(0x4fae6e), MAT(0x4fae6e), new THREE.MeshStandardMaterial({ map: t }), new THREE.MeshStandardMaterial({ map: t })]);
  m.castShadow = true; return m;
}
export function coin() { const m = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.22, 0.06, 9), MAT(0xffc83a, { metalness: 0.5, roughness: 0.35 })); m.castShadow = true; return m; }
export function cup() { const g = new THREE.Group(); const c = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.12, 0.34, 7), MAT(0xf5f0e6)); const lid = new THREE.Mesh(new THREE.CylinderGeometry(0.17, 0.17, 0.05, 7), MAT(0x6b4630)); lid.position.y = 0.18; g.add(c, lid); return g; }
export function shoebox() { const g = new THREE.Group(); const b = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.3, 0.38), MAT(0xff6b5b)); const l = new THREE.Mesh(new THREE.BoxGeometry(0.64, 0.08, 0.42), MAT(0xffffff)); l.position.y = 0.17; g.add(b, l); return g; }
export function jar() { const g = new THREE.Group(); const glass = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.3, 0.6, 8), new THREE.MeshStandardMaterial({ color: 0xbfe6ff, transparent: true, opacity: 0.45, flatShading: true }));
  const coins = new THREE.Mesh(new THREE.CylinderGeometry(0.27, 0.27, 0.32, 8), MAT(0xffc83a, { metalness: 0.4 })); coins.position.y = -0.13; g.add(coins, glass); return g; }

// ---------------------------------------------------------------- sets
export function makeSet(scene, name) {
  const g = new THREE.Group(); scene.add(g);
  const floorCol = { cafe: 0x8a5a3c, rich: 0x3a2a5a, street: 0x56606e, void: 0x2a2450 }[name] || 0x444444;
  const floor = new THREE.Mesh(new THREE.CircleGeometry(30, 24), MAT(floorCol)); floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true; g.add(floor);
  if (name === "cafe") {
    const wall = new THREE.Mesh(new THREE.BoxGeometry(20, 8, 0.3), MAT(0xf0d9b5)); wall.position.set(0, 4, -4); wall.receiveShadow = true; g.add(wall);
    const counter = new THREE.Mesh(new THREE.BoxGeometry(5, 1.2, 1.0), MAT(0x6b4026)); counter.position.set(-1.5, 0.6, -2.6); counter.castShadow = counter.receiveShadow = true; g.add(counter);
    const top = new THREE.Mesh(new THREE.BoxGeometry(5.2, 0.1, 1.2), MAT(0xe8e2d8)); top.position.set(-1.5, 1.25, -2.6); g.add(top);
    const menu = new THREE.Mesh(new THREE.PlaneGeometry(2.6, 1.4), new THREE.MeshStandardMaterial({ map: labelTex("LATTE $5", 512, 280, "#2b2420", "#ffd27a", "bold 90px Arial") })); menu.position.set(-1.5, 3.2, -3.84); g.add(menu);
    for (let i = 0; i < 4; i++) { const l = new THREE.Mesh(new THREE.ConeGeometry(0.4, 0.4, 6, 1, true), MAT(0x2b2b33, { side: THREE.DoubleSide })); l.position.set(-3 + i * 2, 5.2, -1.5); g.add(l);
      const b = new THREE.Mesh(new THREE.IcosahedronGeometry(0.14, 0), new THREE.MeshBasicMaterial({ color: 0xfff1c4 })); b.position.set(-3 + i * 2, 4.95, -1.5); g.add(b); }
  }
  if (name === "rich") {
    for (let i = 0; i < 160; i++) { const c = coin(); const r = Math.random() * 2.2, a = Math.random() * 6.28; c.position.set(Math.cos(a) * r, Math.max(0, 0.9 - r * 0.38) + Math.random() * 0.12, Math.sin(a) * r * 0.8 - 0.6); c.rotation.set(Math.random(), Math.random() * 3, Math.random()); g.add(c); }
    const back = new THREE.Mesh(new THREE.BoxGeometry(30, 14, 0.3), MAT(0x2a1d48)); back.position.set(0, 7, -6); g.add(back);
  }
  if (name === "street") {
    for (let i = 0; i < 9; i++) { const h = 3 + (i * 7 % 5) * 1.3; const b = new THREE.Mesh(new THREE.BoxGeometry(2.2, h, 2), MAT([0x3a4566, 0x46385e, 0x2e5266][i % 3])); b.position.set(-9 + i * 2.4, h / 2, -6); b.castShadow = true; g.add(b);
      for (let y = 1; y < h - 0.5; y += 0.9) for (const x of [-0.5, 0.5]) { const wnd = new THREE.Mesh(new THREE.PlaneGeometry(0.4, 0.5), new THREE.MeshBasicMaterial({ color: (i + y) % 3 < 1 ? 0xffd27a : 0x6d7fa8 })); wnd.position.set(-9 + i * 2.4 + x, y, -4.99); g.add(wnd); } }
  }
  return g;
}

// ---------------------------------------------------------------- stage (renderer, lights, camera with punch & shake)
export function makeStage(w = 1080, h = 1920, bg = 0x30285a) {
  const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
  renderer.setSize(w, h); renderer.setPixelRatio(1); renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.outputColorSpace = THREE.SRGBColorSpace;
  document.body.appendChild(renderer.domElement);
  const scene = new THREE.Scene(); scene.background = new THREE.Color(bg); scene.fog = new THREE.Fog(bg, 14, 30);
  const hemi = new THREE.HemisphereLight(0xfff4e6, 0x8a7ab0, 1.5); scene.add(hemi);
  const fill = new THREE.DirectionalLight(0xfff0e0, 1.3); fill.position.set(0, 3, 10); scene.add(fill);
  const sun = new THREE.DirectionalLight(0xffffff, 2.2); sun.position.set(4, 9, 6); sun.castShadow = true; sun.shadow.mapSize.set(1024, 1024);
  Object.assign(sun.shadow.camera, { left: -8, right: 8, top: 8, bottom: -8 }); scene.add(sun);
  const rim = new THREE.DirectionalLight(0x9fd0ff, 1.2); rim.position.set(-5, 4, -5); scene.add(rim);
  const camera = new THREE.PerspectiveCamera(38, w / h, 0.1, 100);
  return { renderer, scene, camera, sun };
}
export function shot(camera, from, to, look, k, punch = 0, shake = 0, t = 0) {
  const e = ease(Math.max(0, Math.min(1, k)));
  camera.position.set(from[0] + (to[0] - from[0]) * e, from[1] + (to[1] - from[1]) * e, from[2] + (to[2] - from[2]) * e);
  const target = new THREE.Vector3(...look);
  if (punch) camera.position.lerp(target, punch);
  if (shake) { camera.position.x += Math.sin(t * 71) * shake; camera.position.y += Math.cos(t * 53) * shake; }
  camera.lookAt(target);
}
