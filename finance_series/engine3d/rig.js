// Low-poly 3D cast for The Other Timeline: rigged characters, meme faces, poses, props, sets.
import * as THREE from "three";

export const CAST = {
  you:     { skin: 0xf6ead2, top: 0xffb02e, dark: 0xd98c22, pants: 0x3a4a6b, hood: 0xe8962f, hair: null, extra: "hood" },
  max:     { skin: 0xf0cdaa, top: 0xff6b5b, dark: 0xc84646, pants: 0x2f3542, hood: null, hair: 0x3c281e, extra: "spiky" },
  grandma: { skin: 0xf5dec8, top: 0x9a6edc, dark: 0x6e50aa, pants: 0x5b4a7a, hood: null, hair: 0xe1e1ea, extra: "bun" },
  banker:  { skin: 0xa06e4b, top: 0x28375a, dark: 0x19233c, pants: 0x19233c, hood: null, hair: 0x1e1919, extra: "tie" },
};
const MAT = (c, o = {}) => new THREE.MeshStandardMaterial({ color: c, flatShading: true, roughness: 0.75, metalness: 0.0, ...o });
const deg = (a) => a * Math.PI / 180;

// ---------------------------------------------------------------- meme faces (canvas painted on a front cap of the head)
const INK = "#1b1630";
export function drawFace(ctx, emo, blink = 1, look = [0, 0], extra = null) {
  const S = 512; ctx.clearRect(0, 0, S, S);
  const cx = S / 2, ey = S * 0.44, ex = S * 0.17, er = S * 0.085;
  const eye = (x, sx = 1, sy = 1, pupil = 0.5) => {
    ctx.fillStyle = "#fff"; ctx.strokeStyle = INK; ctx.lineWidth = 9;
    ctx.beginPath(); ctx.ellipse(x, ey, er * sx, er * sy * Math.max(0.08, blink), 0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
    if (blink > 0.3) {
      ctx.fillStyle = INK; const pr = er * pupil;
      ctx.beginPath(); ctx.ellipse(x + look[0] * er * 0.35, ey + look[1] * er * 0.35, pr, pr, 0, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = "#fff"; ctx.beginPath(); ctx.arc(x + look[0] * er * 0.35 + pr * 0.35, ey - pr * 0.35, pr * 0.3, 0, Math.PI * 2); ctx.fill();
    }
  };
  const brow = (x, a, dy = -1.55) => { ctx.strokeStyle = INK; ctx.lineWidth = 14; ctx.lineCap = "round"; ctx.beginPath();
    ctx.moveTo(x - er * 1.1, ey + er * dy + Math.sin(a) * er * 0.6); ctx.lineTo(x + er * 1.1, ey + er * dy - Math.sin(a) * er * 0.6); ctx.stroke(); };
  const mouthPath = (fn) => { ctx.beginPath(); fn(); };
  const cheeks = (a = 0.35) => { ctx.fillStyle = `rgba(255,120,110,${a})`; for (const x of [cx - S * 0.27, cx + S * 0.27]) { ctx.beginPath(); ctx.ellipse(x, S * 0.6, S * 0.06, S * 0.035, 0, 0, Math.PI * 2); ctx.fill(); } };
  const mouthY = S * 0.66;
  const L = cx - ex, R = cx + ex;
  switch (emo) {
    case "happy": eye(L); eye(R); cheeks();
      ctx.fillStyle = "#7a2836"; mouthPath(() => { ctx.moveTo(cx - 60, mouthY - 10); ctx.quadraticCurveTo(cx, mouthY + 80, cx + 60, mouthY - 10); ctx.closePath(); }); ctx.fill(); break;
    case "shock": eye(L, 1.35, 1.45, 0.28); eye(R, 1.35, 1.45, 0.28); cheeks(0.5); brow(L, 0.5, -2.1); brow(R, -0.5, -2.1);
      ctx.fillStyle = "#7a2836"; ctx.beginPath(); ctx.ellipse(cx, mouthY + 20, 34, 52, 0, 0, Math.PI * 2); ctx.fill(); break;
    case "smug": eye(L, 1, 0.45); eye(R, 1, 0.45); brow(L, -0.25); brow(R, 0.35); cheeks(0.25);
      ctx.strokeStyle = INK; ctx.lineWidth = 12; ctx.beginPath(); ctx.moveTo(cx - 40, mouthY); ctx.quadraticCurveTo(cx + 20, mouthY + 30, cx + 70, mouthY - 25); ctx.stroke(); break;
    case "sad": eye(L, 1, 1, 0.55); eye(R, 1, 1, 0.55); brow(L, 0.5); brow(R, -0.5);
      ctx.strokeStyle = INK; ctx.lineWidth = 12; ctx.beginPath(); ctx.moveTo(cx - 50, mouthY + 30); ctx.quadraticCurveTo(cx, mouthY - 20, cx + 50, mouthY + 30); ctx.stroke();
      ctx.fillStyle = "#8cc8ff"; ctx.beginPath(); ctx.ellipse(R + er * 0.2, ey + er * 1.6, 14, 26, 0, 0, Math.PI * 2); ctx.fill(); break;
    case "panic": eye(L, 1.5, 1.6, 0.18); eye(R, 1.5, 1.6, 0.18); brow(L, 0.7, -2.2); brow(R, -0.7, -2.2);
      ctx.fillStyle = "#7a2836"; ctx.beginPath(); ctx.ellipse(cx, mouthY + 30, 70, 50, 0, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = "#fff"; ctx.fillRect(cx - 55, mouthY - 5, 110, 18);
      ctx.fillStyle = "#8cc8ff"; for (const [x, y] of [[S * 0.12, S * 0.25], [S * 0.86, S * 0.3]]) { ctx.beginPath(); ctx.ellipse(x, y, 16, 28, 0.3, 0, Math.PI * 2); ctx.fill(); } break;
    case "money": ctx.font = "bold 150px Arial"; ctx.fillStyle = "#3ccf6a"; ctx.strokeStyle = INK; ctx.lineWidth = 8; ctx.textAlign = "center"; ctx.textBaseline = "middle";
      for (const x of [L, R]) { ctx.strokeText("$", x, ey); ctx.fillText("$", x, ey); } cheeks(0.45);
      ctx.fillStyle = "#7a2836"; mouthPath(() => { ctx.moveTo(cx - 80, mouthY - 10); ctx.quadraticCurveTo(cx, mouthY + 110, cx + 80, mouthY - 10); ctx.closePath(); }); ctx.fill();
      ctx.fillStyle = "#fff"; ctx.fillRect(cx - 62, mouthY - 6, 124, 16); break;
    case "laugh": ctx.strokeStyle = INK; ctx.lineWidth = 12; for (const x of [L, R]) { ctx.beginPath(); ctx.moveTo(x - er, ey + 10); ctx.lineTo(x, ey - 20); ctx.lineTo(x + er, ey + 10); ctx.stroke(); }
      cheeks(0.5); ctx.fillStyle = "#7a2836"; mouthPath(() => { ctx.moveTo(cx - 75, mouthY - 20); ctx.quadraticCurveTo(cx, mouthY + 110, cx + 75, mouthY - 20); ctx.closePath(); }); ctx.fill();
      ctx.fillStyle = "#8cc8ff"; for (const x of [L - er * 1.2, R + er * 1.2]) { ctx.beginPath(); ctx.ellipse(x, ey + 30, 12, 24, 0, 0, Math.PI * 2); ctx.fill(); } break;
    case "angry": eye(L, 1, 0.8); eye(R, 1, 0.8); brow(L, -0.6, -1.3); brow(R, 0.6, -1.3); cheeks(0.6);
      ctx.strokeStyle = INK; ctx.lineWidth = 14; ctx.beginPath(); ctx.moveTo(cx - 55, mouthY + 20); ctx.lineTo(cx + 55, mouthY + 20); ctx.stroke(); break;
    default: eye(L); eye(R); cheeks(0.25);
      ctx.strokeStyle = INK; ctx.lineWidth = 11; ctx.beginPath(); ctx.moveTo(cx - 40, mouthY); ctx.quadraticCurveTo(cx, mouthY + 25, cx + 40, mouthY); ctx.stroke();
  }
  if (extra === "glasses") { ctx.strokeStyle = "#3c3246"; ctx.lineWidth = 9; for (const x of [L, R]) { ctx.beginPath(); ctx.arc(x, ey, er * 1.45, 0, Math.PI * 2); ctx.stroke(); } ctx.beginPath(); ctx.moveTo(L + er * 1.45, ey); ctx.lineTo(R - er * 1.45, ey); ctx.stroke(); }
}

// ---------------------------------------------------------------- character rig
function limb(len, r, mat) {
  const g = new THREE.CylinderGeometry(r, r * 0.9, len, 6); g.translate(0, -len / 2, 0);
  const m = new THREE.Mesh(g, mat); m.castShadow = true; return m;
}
export function makeChar(who) {
  const c = CAST[who];
  const mTop = MAT(c.top), mDark = MAT(c.dark), mSkin = MAT(c.skin), mPants = MAT(c.pants), mShoe = MAT(0x2a2a33);
  const root = new THREE.Group(); root.name = who;
  const hips = new THREE.Group(); hips.position.y = 1.0; root.add(hips);
  const torso = new THREE.Group(); hips.add(torso);
  const body = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.62, 1.0, 7), mTop); body.position.y = 0.5; body.castShadow = true; torso.add(body);
  const belt = new THREE.Mesh(new THREE.CylinderGeometry(0.63, 0.63, 0.14, 7), mPants); belt.position.y = 0.05; torso.add(belt);
  if (c.extra === "tie") {
    const shirt = new THREE.Mesh(new THREE.ConeGeometry(0.2, 0.45, 3), MAT(0xf0f0f5)); shirt.rotation.x = Math.PI; shirt.position.set(0, 0.8, 0.43); shirt.rotation.z = Math.PI; torso.add(shirt);
    const tie = new THREE.Mesh(new THREE.BoxGeometry(0.11, 0.5, 0.05), MAT(0x38c6b4)); tie.position.set(0, 0.6, 0.55); torso.add(tie);
  }
  if (c.extra === "hood") { for (const x of [-0.14, 0.14]) { const s = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.35, 4), MAT(0xfff4dc)); s.position.set(x, 0.72, 0.52); torso.add(s); } }
  const neck = new THREE.Group(); neck.position.y = 1.0; torso.add(neck);
  const head = new THREE.Group(); head.position.y = 0.72; neck.add(head);
  const skull = new THREE.Mesh(new THREE.IcosahedronGeometry(0.78, 1), mSkin); skull.castShadow = true; head.add(skull);
  if (c.extra === "hood") { const hood = new THREE.Mesh(new THREE.IcosahedronGeometry(0.92, 1), MAT(c.hood)); hood.position.set(0, 0.04, -0.16); hood.scale.set(1, 1, 0.85); head.add(hood); }
  if (c.extra === "spiky") { for (let i = 0; i < 7; i++) { const a = -1.1 + i * 0.37; const sp = new THREE.Mesh(new THREE.ConeGeometry(0.17, 0.5, 4), MAT(c.hair)); sp.position.set(Math.sin(a) * 0.6, 0.55 + Math.cos(a) * 0.12, -0.05); sp.rotation.z = -a * 0.8; head.add(sp); }
    const cap = new THREE.Mesh(new THREE.SphereGeometry(0.8, 8, 5, 0, Math.PI * 2, 0, Math.PI * 0.42), MAT(c.hair)); cap.position.y = 0.02; head.add(cap); }
  if (c.extra === "bun") { const cap = new THREE.Mesh(new THREE.SphereGeometry(0.8, 8, 5, 0, Math.PI * 2, 0, Math.PI * 0.45), MAT(c.hair)); head.add(cap);
    const bun = new THREE.Mesh(new THREE.IcosahedronGeometry(0.3, 0), MAT(c.hair)); bun.position.set(0, 0.85, -0.2); head.add(bun); }
  if (c.extra === "tie") { const cap = new THREE.Mesh(new THREE.SphereGeometry(0.8, 8, 5, 0, Math.PI * 2, 0, Math.PI * 0.38), MAT(c.hair)); head.add(cap); }
  // face cap
  const cv = document.createElement("canvas"); cv.width = cv.height = 512; const ctx = cv.getContext("2d");
  const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace;
  const face = new THREE.Mesh(new THREE.SphereGeometry(0.80, 32, 20, Math.PI * 0.05, Math.PI * 0.9, Math.PI * 0.18, Math.PI * 0.64),
    new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false }));
  head.add(face);
  // arms
  const arms = {};
  for (const side of ["L", "R"]) {
    const sx = side === "L" ? -1 : 1;
    const sh = new THREE.Group(); sh.position.set(0.6 * sx, 0.9, 0); torso.add(sh);
    const ball = new THREE.Mesh(new THREE.IcosahedronGeometry(0.17, 0), mTop); sh.add(ball);
    sh.add(limb(0.48, 0.14, mTop));
    const el = new THREE.Group(); el.position.y = -0.48; sh.add(el);
    el.add(limb(0.42, 0.12, mTop));
    const hand = new THREE.Mesh(new THREE.IcosahedronGeometry(0.16, 0), mSkin); hand.position.y = -0.5; hand.castShadow = true; el.add(hand);
    const thumb = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, 0.16, 4), mSkin); thumb.position.set(-0.12 * sx, -0.46, 0.06); thumb.rotation.z = 0.8 * sx; el.add(thumb);
    const grip = new THREE.Group(); grip.position.y = -0.55; el.add(grip);
    arms[side] = { sh, el, hand, thumb, grip, sx };
  }
  const legs = {};
  for (const side of ["L", "R"]) {
    const sx = side === "L" ? -1 : 1;
    const hp = new THREE.Group(); hp.position.set(0.25 * sx, 0, 0); hips.add(hp);
    hp.add(limb(0.5, 0.17, mPants));
    const kn = new THREE.Group(); kn.position.y = -0.5; hp.add(kn);
    kn.add(limb(0.42, 0.15, mPants));
    const foot = new THREE.Mesh(new THREE.BoxGeometry(0.26, 0.14, 0.42), mShoe); foot.position.set(0, -0.44, 0.1); foot.castShadow = true; kn.add(foot);
    legs[side] = { hp, kn, sx };
  }
  const ch = { who, root, hips, torso, neck, head, face, ctx, tex, arms, legs, emo: null, extra: c.extra === "bun" ? "glasses" : null, lastKey: "" };
  setFace(ch, "neutral");
  return ch;
}
export function setFace(ch, emo, blink = 1, look = [0, 0]) {
  const key = emo + (blink > 0.3 ? "o" : "c") + look.map((v) => v.toFixed(1)).join(",");
  if (key === ch.lastKey) return; ch.lastKey = key;
  drawFace(ch.ctx, emo, blink, look, ch.extra); ch.tex.needsUpdate = true;
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
