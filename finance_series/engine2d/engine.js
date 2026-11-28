// 2D engine for the Karl "What If You...?" style (karl-2d-template). Pure canvas 2D, no libraries.
// Characters: flat puppets with a glossy black ball head; backgrounds: painted flat sets; FX: rings, glow, sparkles,
// receipt; post: grade, vignette, grain. All units in pixels of a 1920x1080 frame.

export const CAST = {
  karl:    { name: "Karl", hoodie: "#2ec4b6", hoodieDark: "#22a093", pants: "#2f3b5c", hat: "cap", hatColor: "#ff8a3d", strings: true },
  karl_red:{ name: "Karl (red test)", hoodie: "#e0413b", hoodieDark: "#b8302c", pants: "#2f3b5c", hat: "cap", hatColor: "#ff8a3d", strings: true },
  mom:     { name: "Mom", hoodie: "#3fa874", hoodieDark: "#2f8a5e", pants: "#2e3a55", top: "cardigan", hair: "long", hairColor: "#7a4a2a", lashes: true },
  dad:     { name: "Dad", hoodie: "#4a7fc1", hoodieDark: "#3a679f", pants: "#8a7650", top: "shirt", hair: "short", hairColor: "#5a3e26", mustache: true, scale: 1.08 },
  mia:     { name: "Mia", hoodie: "#9a6edc", hoodieDark: "#7d55bd", pants: "#2c2c3c", hair: "buns", hairColor: "#5a3524", scale: 0.78 },
  grandma: { name: "Grandma Rose", hoodie: "#c45c8a", hoodieDark: "#a3466f", pants: "#4a4458", top: "cardigan", hair: "bun", hairColor: "#dedce6", glasses: true, scale: 0.95 },
  max:     { name: "Max", hoodie: "#ff6b5b", hoodieDark: "#d9544a", pants: "#2f3542", hair: "curly", hairColor: "#2a1a12", strings: true },
  lena:    { name: "Lena", hoodie: "#f2b6c8", hoodieDark: "#d98fa6", pants: "#384a6b", hair: "bob", hairColor: "#c8843a", lashes: true, band: "#ffffff" },
};

const INK = "#141218";
const lerp = (a, b, k) => a + (b - a) * k;
export const ease = (k) => (k = Math.max(0, Math.min(1, k)), k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2);
export const easeOut = (k) => 1 - Math.pow(1 - Math.max(0, Math.min(1, k)), 3);
export const pop = (k) => { k = Math.max(0, Math.min(1, k)); return easeOut(k * 1.4) + Math.sin(k * Math.PI) * 0.15 * (1 - k); };

// ------------------------------------------------------------------ poses (deg): arm [shoulder, elbow], leg [hip, knee]
export const POSES = {
  idle:   { L: [12, -8], R: [-12, 8], LL: [3, 0], LR: [-3, 0], lean: 0 },
  wave:   { L: [12, -8], R: [-150, -40], LL: [3, 0], LR: [-3, 0], lean: -2 },
  cheer:  { L: [150, 20], R: [-150, -20], LL: [6, 0], LR: [-6, 0], lean: 0 },
  shrug:  { L: [60, 90], R: [-60, -90], LL: [3, 0], LR: [-3, 0], lean: 0 },
  point:  { L: [12, -8], R: [-95, 0], LL: [3, 0], LR: [-3, 0], lean: 2 },
  hold:   { L: [25, -95], R: [-25, 95], LL: [3, 0], LR: [-3, 0], lean: 0 },
  facepalm:{ L: [12, -8], R: [-40, -140], LL: [3, 0], LR: [-3, 0], lean: 6 },
  shock:  { L: [70, 100], R: [-70, -100], LL: [8, 0], LR: [-8, 0], lean: -4 },
  slump:  { L: [4, 0], R: [-4, 0], LL: [2, 0], LR: [-2, 0], lean: 10 },
  walk:   { L: [12, -8], R: [-12, 8], LL: [3, 0], LR: [-3, 0], lean: 2 },
};
export function blendPose(a, b, k) {
  const A = POSES[a] || a, B = POSES[b] || b, o = {};
  for (const key of ["L", "R", "LL", "LR"]) o[key] = A[key].map((v, i) => lerp(v, B[key][i], k));
  o.lean = lerp(A.lean, B.lean, k); return o;
}

// ------------------------------------------------------------------ face
function drawFace(g, R, emo, look, blink, c) {
  const ex = R * 0.26, ey = -R * 0.02, er = R * 0.3, lx = look[0] * R * 0.08, ly = look[1] * R * 0.06;
  // eyes (touching white circles)
  const eyeH = emo === "smug" ? 0.55 : emo === "sleepy" ? 0.35 : blink < 0.5 ? 0.1 : emo === "shock" || emo === "panic" ? 1.15 : 1;
  for (const s of [-1, 1]) {
    g.save(); g.translate(s * ex + lx * 0.6, ey + ly * 0.6);
    g.scale(emo === "shock" || emo === "panic" ? 1.12 : 1, eyeH);
    g.beginPath(); g.arc(0, 0, er, 0, 7); g.fillStyle = "#fbfaf6"; g.fill(); g.lineWidth = R * 0.035 / eyeH; g.strokeStyle = INK; g.stroke();
    g.restore();
    if (eyeH > 0.3) {
      const pr = emo === "shock" || emo === "panic" ? er * 0.28 : er * 0.42;
      const py = emo === "dazed" ? -er * 0.45 : emo === "sad" ? er * 0.25 : 0;
      g.beginPath(); g.arc(s * ex + lx * 1.6 + (emo === "smug" ? s * 0 : 0), ey + ly * 1.6 + py, pr * Math.min(1, eyeH + 0.2), 0, 7); g.fillStyle = INK; g.fill();
      g.beginPath(); g.arc(s * ex + lx * 1.6 - pr * 0.35, ey + ly * 1.6 + py - pr * 0.35, pr * 0.28, 0, 7); g.fillStyle = "rgba(255,255,255,0.9)"; g.fill();
    }
    if (c.lashes && eyeH > 0.3) { g.strokeStyle = INK; g.lineWidth = R * 0.03; for (let k = -1; k <= 1; k++) { g.beginPath(); const a = -Math.PI / 2 + k * 0.45 + s * 0.5; g.moveTo(s * ex + Math.cos(a) * er, ey + Math.sin(a) * er * eyeH); g.lineTo(s * ex + Math.cos(a) * er * 1.25, ey + Math.sin(a) * er * 1.25 * eyeH); g.stroke(); } }
  }
  // brows for strong emotions
  if (["angry", "worried", "sad", "panic"].includes(emo)) {
    g.strokeStyle = "#fbfaf6"; g.lineWidth = R * 0.05; g.lineCap = "round";
    for (const s of [-1, 1]) { const tilt = emo === "angry" ? 0.28 : -0.28; g.beginPath(); g.moveTo(s * ex - er * 0.6, ey - er * 1.35 + s * tilt * er); g.lineTo(s * ex + er * 0.6, ey - er * 1.35 - s * tilt * er); g.stroke(); }
  }
  if (c.glasses) { g.strokeStyle = "#c9c4d6"; g.lineWidth = R * 0.03; for (const s of [-1, 1]) { g.beginPath(); g.arc(s * ex, ey, er * 1.12, 0, 7); g.stroke(); } }
  // mouth
  const my = R * 0.45; g.lineCap = "round";
  if (emo === "happy" || emo === "laugh" || emo === "love") {
    g.beginPath(); g.moveTo(-R * 0.16, my - R * 0.03); g.quadraticCurveTo(0, my + R * (emo === "laugh" ? 0.22 : 0.14), R * 0.16, my - R * 0.03); g.closePath(); g.fillStyle = "#e85a6a"; g.fill();
  } else if (emo === "shock" || emo === "panic") {
    g.beginPath(); g.ellipse(0, my + R * 0.04, R * 0.08, R * 0.11, 0, 0, 7); g.fillStyle = "#e85a6a"; g.fill();
  } else if (emo === "sad" || emo === "worried") {
    g.beginPath(); g.arc(0, my + R * 0.12, R * 0.1, Math.PI * 1.15, Math.PI * 1.85); g.strokeStyle = "#fbfaf6"; g.lineWidth = R * 0.04; g.stroke();
  } else if (emo === "smug") {
    g.beginPath(); g.moveTo(-R * 0.1, my); g.quadraticCurveTo(R * 0.05, my + R * 0.07, R * 0.15, my - R * 0.05); g.strokeStyle = "#fbfaf6"; g.lineWidth = R * 0.04; g.stroke();
  } else {
    g.beginPath(); g.arc(0, my - R * 0.06, R * 0.09, Math.PI * 0.2, Math.PI * 0.8); g.strokeStyle = "#fbfaf6"; g.lineWidth = R * 0.04; g.stroke();
  }
  if (["happy", "laugh", "love", "dazed", "shy"].includes(emo)) for (const s of [-1, 1]) { g.beginPath(); g.ellipse(s * R * 0.55, R * 0.28, R * 0.13, R * 0.07, 0, 0, 7); g.fillStyle = "rgba(255,120,150,0.55)"; g.fill(); }
  if (emo === "panic" || emo === "worried") { g.beginPath(); g.moveTo(R * 0.72, -R * 0.35); g.quadraticCurveTo(R * 0.86, -R * 0.12, R * 0.72, -R * 0.05); g.quadraticCurveTo(R * 0.6, -R * 0.12, R * 0.72, -R * 0.35); g.fillStyle = "#8fd3ff"; g.fill(); }
  if (c.mustache) { g.fillStyle = "#e9e2d8"; g.beginPath(); g.ellipse(-R * 0.12, my - R * 0.13, R * 0.13, R * 0.05, 0.2, 0, 7); g.ellipse(R * 0.12, my - R * 0.13, R * 0.13, R * 0.05, -0.2, 0, 7); g.fill(); }
}

function hairBack(g, R, c) {
  g.fillStyle = c.hairColor;
  if (c.hair === "long") { g.beginPath(); g.ellipse(0, R * 0.35, R * 1.12, R * 1.25, 0, 0, 7); g.fill(); }
  if (c.hair === "bob") { g.beginPath(); g.ellipse(0, R * 0.1, R * 1.13, R * 1.05, 0, 0, 7); g.fill(); }
  if (c.hair === "buns") for (const s of [-1, 1]) { g.beginPath(); g.arc(s * R * 0.72, -R * 0.72, R * 0.32, 0, 7); g.fill(); }
  if (c.hair === "bun") { g.beginPath(); g.arc(0, -R * 1.18, R * 0.34, 0, 7); g.fill(); }
}
function hairFront(g, R, c) {
  g.fillStyle = c.hairColor;
  if (c.hair === "long" || c.hair === "bob") { g.beginPath(); g.arc(0, -R * 0.05, R * 1.02, Math.PI * 1.08, Math.PI * 1.92); g.quadraticCurveTo(R * 0.25, -R * 0.62, -R * 0.1, -R * 0.78); g.quadraticCurveTo(-R * 0.45, -R * 0.55, -R * 0.98, -R * 0.35); g.fill(); }
  if (c.band) { g.strokeStyle = c.band; g.lineWidth = R * 0.09; g.beginPath(); g.arc(0, R * 0.05, R * 1.0, Math.PI * 1.25, Math.PI * 1.75); g.stroke(); }
  if (c.hair === "short") { g.beginPath(); g.arc(0, -R * 0.1, R * 1.01, Math.PI * 1.12, Math.PI * 1.88); g.quadraticCurveTo(0, -R * 0.82, Math.cos(Math.PI * 1.12) * R * 1.01, -R * 0.1 + Math.sin(Math.PI * 1.12) * R * 1.01); g.fill(); }
  if (c.hair === "curly") for (let i = 0; i < 9; i++) { const a = Math.PI * (1.02 + i * 0.12); g.beginPath(); g.arc(Math.cos(a) * R * 0.92, Math.sin(a) * R * 0.92, R * 0.24, 0, 7); g.fill(); }
  if (c.hair === "bun" || c.hair === "buns") { g.beginPath(); g.arc(0, -R * 0.12, R * 1.0, Math.PI * 1.12, Math.PI * 1.88); g.quadraticCurveTo(0, -R * 0.62, Math.cos(Math.PI * 1.12) * R, -R * 0.12 + Math.sin(Math.PI * 1.12) * R); g.fill(); }
  if (c.hat === "cap") { // backwards cap: dome + short brim at the back
    g.fillStyle = c.hatColor; g.beginPath(); g.arc(0, -R * 0.2, R * 1.03, Math.PI * 1.08, Math.PI * 1.92); g.quadraticCurveTo(0, -R * 0.55, -R * 0.97, -R * 0.47); g.fill();
    g.beginPath(); g.ellipse(-R * 0.98, -R * 0.42, R * 0.42, R * 0.12, -0.25, 0, 7); g.fill();
    g.fillStyle = "rgba(255,255,255,0.25)"; g.beginPath(); g.ellipse(-R * 0.25, -R * 0.95, R * 0.35, R * 0.12, -0.2, 0, 7); g.fill();
    g.fillStyle = "#ffffff"; g.beginPath(); g.arc(0, -R * 1.2, R * 0.07, 0, 7); g.fill();
  }
}

function limb(g, x0, y0, a1, l1, a2, l2, w, col) { // angles in deg from straight down
  const r1 = a1 * Math.PI / 180, r2 = (a1 + a2) * Math.PI / 180;
  const x1 = x0 + Math.sin(r1) * l1, y1 = y0 + Math.cos(r1) * l1, x2 = x1 + Math.sin(r2) * l2, y2 = y1 + Math.cos(r2) * l2;
  g.strokeStyle = col; g.lineWidth = w; g.lineCap = "round"; g.lineJoin = "round";
  g.beginPath(); g.moveTo(x0, y0); g.lineTo(x1, y1); g.lineTo(x2, y2); g.stroke(); return [x2, y2];
}

// Draw a character standing with feet at (x, y). H = total height in px. opts: {pose, pose2, k, emo, look, blink, t, flip, walk, bob}
export function drawChar(g, who, x, y, H, o = {}) {
  const c = CAST[who]; H *= c.scale || 1; const R = H * 0.2, t = o.t || 0;
  const p = o.pose2 ? blendPose(o.pose || "idle", o.pose2, ease(o.k ?? 1)) : blendPose(o.pose || "idle", o.pose || "idle", 0);
  if (o.walk) { const w = Math.sin(t * 8); p.LL = [w * 22, 0]; p.LR = [-w * 22, 0]; p.L = [12 - w * 18, -8]; p.R = [-12 + w * 18, 8]; }
  const bob = (o.walk ? Math.abs(Math.cos(t * 8)) * H * 0.02 : Math.sin(t * 2.4 + x) * H * 0.006) + (o.hop ? Math.abs(Math.sin(t * 9)) * H * 0.06 : 0);
  g.save(); g.translate(x, y - bob); if (o.flip) g.scale(-1, 1);
  // shadow
  g.save(); g.scale(1, 0.22); g.beginPath(); g.arc(0, bob / 0.22, R * 0.9, 0, 7); g.fillStyle = "rgba(20,15,30,0.18)"; g.fill(); g.restore();
  const legL = H * 0.2, hipY = -H * 0.4, shY = hipY - H * 0.27, bw = R * 1.05;
  g.rotate(p.lean * Math.PI / 180 * 0.3);
  // legs + sneakers
  for (const [s, a] of [[-1, p.LL], [1, p.LR]]) {
    const [fx, fy] = limb(g, s * R * 0.32, hipY, a[0], legL, a[1], legL * 0.95, R * 0.24, c.pants);
    g.fillStyle = "#f4f2ee"; g.beginPath(); g.ellipse(fx + s * R * 0.08, fy + R * 0.02, R * 0.24, R * 0.12, 0, 0, 7); g.fill(); g.fillStyle = "#d9d5cf"; g.fillRect(fx - R * 0.16 + s * R * 0.08, fy + R * 0.06, R * 0.32, R * 0.05);
  }
  // back arm
  const arm = (side, a) => { const [hx, hy] = limb(g, side * bw * 0.86, shY + R * 0.22, -a[0], H * 0.15, -a[1], H * 0.14, R * 0.13, INK); g.beginPath(); g.arc(hx, hy, R * 0.15, 0, 7); g.fillStyle = INK; g.fill(); return [hx, hy]; };
  // torso (hoodie / cardigan / shirt): rounded trapezoid
  g.fillStyle = c.hoodie; g.beginPath();
  g.moveTo(-bw * 0.85, shY); g.quadraticCurveTo(-bw * 1.05, shY + R * 0.1, -bw * 1.02, shY + R * 0.5);
  g.lineTo(-bw * 0.98, hipY + R * 0.12); g.quadraticCurveTo(0, hipY + R * 0.28, bw * 0.98, hipY + R * 0.12);
  g.lineTo(bw * 1.02, shY + R * 0.5); g.quadraticCurveTo(bw * 1.05, shY + R * 0.1, bw * 0.85, shY); g.closePath(); g.fill();
  g.fillStyle = c.hoodieDark; g.fillRect(-bw * 0.98, hipY - R * 0.02, bw * 1.96, R * 0.14);
  if (c.top === "cardigan") { g.fillStyle = "#f3efe6"; g.beginPath(); g.moveTo(-R * 0.2, shY); g.lineTo(R * 0.2, shY); g.lineTo(R * 0.05, hipY); g.lineTo(-R * 0.05, hipY); g.fill(); g.fillStyle = "#ffffff"; for (let i = 0; i < 3; i++) { g.beginPath(); g.arc(R * 0.18, shY + R * (0.35 + i * 0.32), R * 0.05, 0, 7); g.fill(); } }
  else if (c.top === "shirt") { g.fillStyle = "#ffffff"; g.beginPath(); g.moveTo(-R * 0.28, shY); g.lineTo(0, shY + R * 0.3); g.lineTo(R * 0.28, shY); g.fill(); }
  else { g.fillStyle = c.hoodieDark; g.beginPath(); g.ellipse(0, hipY - R * 0.32, bw * 0.55, R * 0.22, 0, 0, 7); g.fill(); // pocket
    if (c.strings) { g.strokeStyle = "#ffffff"; g.lineWidth = R * 0.05; for (const s of [-1, 1]) { g.beginPath(); g.moveTo(s * R * 0.16, shY + R * 0.05); g.lineTo(s * R * 0.18, shY + R * 0.55); g.stroke(); g.beginPath(); g.arc(s * R * 0.18, shY + R * 0.58, R * 0.04, 0, 7); g.fillStyle = "#fff"; g.fill(); } }
    g.fillStyle = c.hoodieDark; g.beginPath(); g.ellipse(0, shY - R * 0.05, R * 0.75, R * 0.22, 0, 0, Math.PI); g.fill(); } // hood rim
  const hands = { L: arm(-1, p.L), R: arm(1, p.R) };
  // head
  const hy = shY - R * 0.88;
  g.save(); g.translate(0, hy); g.rotate((o.tilt || 0) * Math.PI / 180);
  hairBack(g, R, c);
  const gr = g.createRadialGradient(-R * 0.35, -R * 0.45, R * 0.1, 0, 0, R * 1.05);
  gr.addColorStop(0, "#4a4652"); gr.addColorStop(0.45, "#25222b"); gr.addColorStop(1, "#141218");
  g.beginPath(); g.arc(0, 0, R, 0, 7); g.fillStyle = gr; g.fill();
  g.beginPath(); g.ellipse(-R * 0.42, -R * 0.55, R * 0.22, R * 0.12, -0.6, 0, 7); g.fillStyle = "rgba(255,255,255,0.22)"; g.fill();
  drawFace(g, R, o.emo || "neutral", o.look || [0, 0], o.blink ?? 1, c);
  hairFront(g, R, c);
  g.restore();
  g.restore();
  const s = o.flip ? -1 : 1;
  return { head: [x, y - bob + hy], R, hands: { L: [x + s * hands.L[0], y - bob + hands.L[1]], R: [x + s * hands.R[0], y - bob + hands.R[1]] }, pocket: [x, y - bob + hipY - R * 0.32] };
}
export const blinkAt = (t, seed = 0) => ((t + seed * 1.3) % 3.4) < 0.1 ? 0 : 1;

// ------------------------------------------------------------------ sets (painted flat backgrounds), drawn in world space 1920x1080
export function drawSet(g, name, W = 1920, H = 1080) {
  const lg = (y0, y1, a, b) => { const gr = g.createLinearGradient(0, y0, 0, y1); gr.addColorStop(0, a); gr.addColorStop(1, b); return gr; };
  if (name === "kitchen") {
    g.fillStyle = lg(0, 760, "#e9dcc9", "#dccbb3"); g.fillRect(-200, 0, W + 400, 760);
    g.fillStyle = "#8fc9c0"; g.fillRect(-200, 120, 980, 210); // upper cabinets
    for (let i = 0; i < 6; i++) { g.fillStyle = "#7db8af"; g.fillRect(-180 + i * 160, 135, 145, 180); g.fillStyle = "#e8e2d6"; g.fillRect(-120 + i * 160, 290, 24, 8); }
    g.fillStyle = lg(380, 600, "#9fd3f0", "#d8eef7"); g.fillRect(1020, 150, 420, 300); // window
    g.fillStyle = "#7fb36a"; for (let i = 0; i < 5; i++) { g.beginPath(); g.arc(1060 + i * 90, 440, 60, Math.PI, 0); g.fill(); }
    g.strokeStyle = "#f6f1e7"; g.lineWidth = 18; g.strokeRect(1020, 150, 420, 300); g.beginPath(); g.moveTo(1230, 150); g.lineTo(1230, 450); g.stroke();
    g.fillStyle = "#f2eee6"; g.fillRect(1560, 160, 260, 560); g.fillStyle = "#e3ddd2"; g.fillRect(1560, 390, 260, 8); g.fillStyle = "#c8c1b4"; g.fillRect(1580, 250, 10, 90); // fridge
    g.fillStyle = "#c98c5c"; g.fillRect(-200, 470, 1000, 290); g.fillStyle = "#e6ddd0"; g.fillRect(-200, 460, 1010, 26); // counter
    for (let i = 0; i < 6; i++) { g.fillStyle = "#b97c4e"; g.fillRect(-180 + i * 160, 500, 145, 240); }
    g.fillStyle = lg(760, H, "#b98a63", "#9c7150"); g.fillRect(-200, 760, W + 400, H - 760); // floor
    g.strokeStyle = "rgba(0,0,0,0.06)"; g.lineWidth = 3; for (let x = -200; x < W + 200; x += 120) { g.beginPath(); g.moveTo(x, 760); g.lineTo(x - 260, H); g.stroke(); }
    // table
    g.fillStyle = "#d9a66f"; g.fillRect(780, 690, 560, 28); g.fillStyle = "#b9884f"; g.fillRect(810, 718, 26, 200); g.fillRect(1284, 718, 26, 200);
  }
  if (name === "street") {
    g.fillStyle = lg(0, 600, "#a8d8f0", "#e6f2f0"); g.fillRect(-200, 0, W + 400, 640);
    g.fillStyle = "#cfe6c0"; for (let i = 0; i < 4; i++) { g.beginPath(); g.ellipse(200 + i * 520, 610, 420, 90, 0, Math.PI, 0); g.fill(); }
    const houses = [["#f4d7c5", "#c45c5c"], ["#cfe0f0", "#5a6c8a"], ["#f2e6b8", "#8a5a3a"], ["#e0d0f0", "#6a4a8a"]];
    houses.forEach(([wall, roof], i) => { const x = -60 + i * 520; g.fillStyle = wall; g.fillRect(x, 360, 380, 260); g.fillStyle = roof; g.beginPath(); g.moveTo(x - 30, 365); g.lineTo(x + 190, 230); g.lineTo(x + 410, 365); g.fill(); g.fillStyle = "#9fc9e6"; g.fillRect(x + 40, 420, 90, 80); g.fillRect(x + 250, 420, 90, 80); g.fillStyle = "#8a5a3a"; g.fillRect(x + 160, 480, 60, 140); });
    g.fillStyle = "#7fb36a"; for (let i = 0; i < 4; i++) { g.beginPath(); g.arc(360 + i * 520, 470, 95, 0, 7); g.fill(); g.fillStyle = "#6a9e58"; g.beginPath(); g.arc(390 + i * 520, 500, 60, 0, 7); g.fill(); g.fillStyle = "#7fb36a"; }
    g.fillStyle = "#d8d4cc"; g.fillRect(-200, 620, W + 400, 160); g.fillStyle = "#6c6f78"; g.fillRect(-200, 780, W + 400, H - 780);
    g.fillStyle = "#e9e3d6"; for (let x = -200; x < W + 200; x += 180) g.fillRect(x, 890, 100, 14);
  }
}

// ------------------------------------------------------------------ FX
export function rings(g, x, y, t0, t, col = "255,255,255", n = 3, maxR = 260) {
  for (let i = 0; i < n; i++) { const k = (t - t0 - i * 0.18) / 0.7; if (k < 0 || k > 1) continue;
    g.beginPath(); g.arc(x, y, 40 + easeOut(k) * maxR, 0, 7); g.strokeStyle = `rgba(${col},${(1 - k) * 0.9})`; g.lineWidth = 6 * (1 - k) + 2; g.stroke(); }
}
export function glow(g, x, y, r, col = "255,200,90", a = 0.6) {
  const gr = g.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, `rgba(${col},${a})`); gr.addColorStop(1, `rgba(${col},0)`); g.fillStyle = gr; g.beginPath(); g.arc(x, y, r, 0, 7); g.fill();
}
export function sparkles(g, x, y, t0, t, n = 4, spread = 120) {
  for (let i = 0; i < n; i++) { const k = (t - t0 - i * 0.08) / 0.5; if (k < 0 || k > 1) continue;
    const a = i * 2.4 + 0.6, d = spread * (0.6 + 0.4 * ((i * 37) % 10) / 10), sx = x + Math.cos(a) * d, sy = y + Math.sin(a) * d, s = 22 * Math.sin(k * Math.PI);
    g.fillStyle = "#ffffff"; g.beginPath(); g.moveTo(sx, sy - s); g.quadraticCurveTo(sx, sy, sx + s * 0.35, sy); g.quadraticCurveTo(sx, sy, sx, sy + s); g.quadraticCurveTo(sx, sy, sx - s * 0.35, sy); g.quadraticCurveTo(sx, sy, sx, sy - s); g.fill();
    g.beginPath(); g.moveTo(sx - s, sy); g.quadraticCurveTo(sx, sy, sx, sy + s * 0.35); g.quadraticCurveTo(sx, sy, sx + s, sy); g.quadraticCurveTo(sx, sy, sx, sy - s * 0.35); g.fill(); }
}
// Our signature: a receipt that prints upward out of a point with lines of text; k = 0..1 print progress
export function receipt(g, x, y, lines, k, opts = {}) {
  const w = opts.w || 300, lh = 46, h = 40 + lines.length * lh + 30, shown = h * easeOut(k);
  g.save(); g.translate(x, y); g.rotate((opts.rot ?? -4) * Math.PI / 180);
  g.shadowColor = "rgba(0,0,0,0.25)"; g.shadowBlur = 18; g.shadowOffsetY = 6;
  g.beginPath(); g.rect(-w / 2, -shown, w, shown); g.fillStyle = "#fbfaf4"; g.fill(); g.shadowColor = "transparent";
  g.save(); g.beginPath(); g.rect(-w / 2, -shown, w, shown); g.clip();
  // zigzag top edge
  g.fillStyle = "rgba(0,0,0,0.0)";
  lines.forEach((ln, i) => { const ly = -shown + 40 + i * lh + 12; g.font = `${ln.size || 34}px ${ln.font || "Mont"}`; g.textBaseline = "middle";
    g.fillStyle = ln.col || "#2a2630"; g.textAlign = ln.align || "left"; g.fillText(ln.l || "", -w / 2 + 22, ly); if (ln.r) { g.textAlign = "right"; g.fillText(ln.r, w / 2 - 22, ly); } });
  g.strokeStyle = "rgba(0,0,0,0.15)"; g.setLineDash([6, 6]); g.beginPath(); g.moveTo(-w / 2 + 18, -shown + 40 + lines.length * lh - 4); g.lineTo(w / 2 - 18, -shown + 40 + lines.length * lh - 4); g.stroke(); g.setLineDash([]);
  g.restore();
  g.fillStyle = "#fbfaf4"; for (let i = 0; i < w / 20; i++) { g.beginPath(); g.moveTo(-w / 2 + i * 20, -shown); g.lineTo(-w / 2 + i * 20 + 10, -shown - 10); g.lineTo(-w / 2 + i * 20 + 20, -shown); g.fill(); }
  g.restore();
}
// White cloud-edged speech/thought pill, text typed word by word (k = 0..1)
export function pill(g, x, y, text, k = 1, opts = {}) {
  const words = text.split(" "), n = Math.max(1, Math.ceil(words.length * Math.min(1, k * 1.2))), shown = words.slice(0, n).join(" ");
  g.font = `700 ${opts.size || 34}px Mont`; const w = Math.max(160, g.measureText(text).width + 70), h = (opts.size || 34) * 2.1;
  const a = pop(k * 3); g.save(); g.translate(x, y); g.scale(a, a);
  g.fillStyle = "#ffffff"; g.beginPath(); g.roundRect(-w / 2, -h / 2, w, h, h / 2); g.fill();
  for (let i = 0; i <= w / 34; i++) for (const s of [-1, 1]) { g.beginPath(); g.arc(-w / 2 + h / 3 + i * 34, s * h / 2, 15, 0, 7); g.fill(); }
  if (opts.tail) { g.beginPath(); g.arc(opts.tail[0] * 0.5, h / 2 + 30, 12, 0, 7); g.arc(opts.tail[0], h / 2 + 62, 7, 0, 7); g.fill(); }
  g.fillStyle = "#1e1b26"; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(shown, 0, 2);
  g.restore();
}

// ------------------------------------------------------------------ post: grade, vignette, grain
let grainCv = null;
export function post(g, W, H, t, grade = null) {
  if (grade) { g.fillStyle = grade; g.globalCompositeOperation = "soft-light"; g.fillRect(0, 0, W, H); g.globalCompositeOperation = "source-over"; }
  const v = g.createRadialGradient(W / 2, H / 2, H * 0.45, W / 2, H / 2, H * 1.05); v.addColorStop(0, "rgba(30,20,40,0)"); v.addColorStop(1, "rgba(30,20,40,0.45)"); g.fillStyle = v; g.fillRect(0, 0, W, H);
  if (!grainCv) { grainCv = document.createElement("canvas"); grainCv.width = 512; grainCv.height = 512; const gg = grainCv.getContext("2d"), id = gg.createImageData(512, 512);
    for (let i = 0; i < id.data.length; i += 4) { const v = Math.random() * 255; id.data[i] = id.data[i + 1] = id.data[i + 2] = v; id.data[i + 3] = 14; } gg.putImageData(id, 0, 0); }
  const ox = (Math.floor(t * 24) * 97) % 512, oy = (Math.floor(t * 24) * 61) % 512;
  g.save(); g.translate(-ox, -oy); g.fillStyle = g.createPattern(grainCv, "repeat"); g.fillRect(ox, oy, W, H); g.restore();
}
// camera: push-in around a focus point, k = 0..1 over the shot
export function camera(g, W, H, focus, zoom0, zoom1, k, layer = 1) {
  const z = lerp(zoom0, zoom1, ease(k)), zz = 1 + (z - 1) * layer;
  g.translate(W / 2, H / 2); g.scale(zz, zz); g.translate(-lerp(W / 2, focus[0], layer * 0.6), -lerp(H / 2, focus[1], layer * 0.6));
}
export async function loadFonts(base = "../../ep2/fonts/") {
  for (const [n, f] of [["Anton", "Anton-Regular.ttf"], ["Mont", "Montserrat.ttf"]]) { const ff = new FontFace(n, `url(${base}${f})`); await ff.load(); document.fonts.add(ff); }
}
