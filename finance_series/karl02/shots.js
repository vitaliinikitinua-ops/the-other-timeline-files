// Karl #02 shot list for engine3d/toon/toon_ep.html?ep=karl02. Line numbers = build/lines.txt (VO lines of script.md).
export const SETS = ["bedroom", "store", "office", "kitchen", "mall", "street", "studio", "restaurant", "lot"];
export const CAST = ["karl", "max", "mom", "dad", "mia", "grandma", "lena"];
export const EXTRAS = 40;
export const CROWD = { n: 900, box: { x0: -24, x1: 24, z0: 3, z1: 16 } };
const NIGHT = { bg: 0x1c1a33, sun: 0.7, grade: "rgba(60,80,200,0.35)" };
const T = (at, top, bot, t = 0.3, o = {}) => ({ type: "tag", at, top, bot, t, ...o });
const PL = (at, text, t = 0.1, o = {}) => ({ type: "pill", at, text, t, dy: -30, ...o });
const R = (at, lines, t = 0.4, o = {}) => ({ type: "receipt", at, lines, t, dur: 1.2, ...o });
const CARD = (lines, t = 0.15, o = {}) => ({ type: "card", x: 960, y: o.y ?? 300, w: o.w ?? 900, h: o.h ?? (lines.length * 110 + 60), lines, t, ...o });
const TX = (text, size = 110, col = "#ffb828", t = 0.1, o = {}) => ({ type: "text", x: 960, y: o.y ?? 250, text, size, col, t, ...o });
const PH = (o, flip, extra = {}) => ({ type: "phone", o, flip, ...extra });
const HP = { clock: "11:58", old: "$240", price: "$120", sub: "-50%  ENDS IN 00:01:59" };
const ex = (n, x0, dx, z, ry = 0, rows = 1, dz = 1.6) => Array.from({ length: n }, (_, j) => [x0 + (j % Math.ceil(n / rows)) * dx + (Math.floor(j / Math.ceil(n / rows)) % 2) * dx / 2, z + Math.floor(j / Math.ceil(n / rows)) * dz, ry]);
const BED = { karl: [1.6, -2.2, -0.35, 0.5] };
const notebook = (lines) => ({ type: "draw", x: 1400, y: 560, fn: (g, x, y, k) => { if (k <= 0) return; g.save(); g.translate(x, y); g.rotate(-0.06); g.globalAlpha = Math.min(1, k * 2);
  g.fillStyle = "#fffdf4"; g.fillRect(-230, -170, 460, 340); g.strokeStyle = "#9ec3e6"; g.lineWidth = 2; for (let i = 0; i < 7; i++) { g.beginPath(); g.moveTo(-230, -120 + i * 44); g.lineTo(230, -120 + i * 44); g.stroke(); }
  g.fillStyle = "#2a2630"; g.font = "40px Mont"; g.textAlign = "left"; lines.forEach((l, i) => g.fillText(l, -200, -88 + i * 60)); g.restore(); } });
const envelope = (gold) => ({ type: "draw", x: 960, y: 560, fn: (g, x, y, k) => { if (k <= 0) return; const s = Math.min(1, k * 1.5); g.save(); g.translate(x, y); g.scale(s, s); g.rotate(-0.05);
  g.fillStyle = gold ? "#f2c14e" : "#f6efe2"; g.fillRect(-300, -180, 600, 360); g.strokeStyle = gold ? "#b8862a" : "#c9bfa8"; g.lineWidth = 6; g.strokeRect(-300, -180, 600, 360);
  g.beginPath(); g.moveTo(-300, -180); g.lineTo(0, 30); g.lineTo(300, -180); g.stroke(); g.fillStyle = "#e0344a"; g.beginPath(); g.arc(0, 30, 34, 0, 7); g.fill();
  g.font = "44px Anton"; g.fillStyle = "#3a2a10"; g.textAlign = "center"; g.fillText(gold ? "VIP INVITATION" : "FOR THE JAR", 0, 130); g.restore(); } });
const calendar = { type: "draw", x: 960, y: 560, fn: (g, x, y, k, lt) => { if (k <= 0) return; g.save(); g.translate(x, y); g.globalAlpha = Math.min(1, k * 2);
  g.fillStyle = "#fffdf4"; g.beginPath(); g.roundRect(-460, -300, 920, 600, 30); g.fill(); g.fillStyle = "#e0344a"; g.fillRect(-460, -300, 920, 90); g.font = "56px Anton"; g.fillStyle = "#fff"; g.textAlign = "center"; g.fillText("JANUARY", 0, -238);
  for (let d = 0; d < 28; d++) { const cx = -390 + (d % 7) * 130, cy = -150 + Math.floor(d / 7) * 110; g.fillStyle = "#2a2630"; g.font = "28px Mont"; g.fillText(String(d + 1), cx, cy); }
  const due = [[1, 0], [2, 0], [4, 1], [5, 1], [6, 1], [1, 1]]; due.forEach(([c, r], j) => { const kk = Math.min(1, Math.max(0, (lt - 0.3 - j * 0.25) / 0.25)); if (kk <= 0) return; g.fillStyle = "#ff5fa2"; g.beginPath(); g.arc(-390 + c * 130, -110 + r * 110 + 14, 38 * kk, 0, 7); g.fill(); g.fillStyle = "#fff"; g.font = "30px Anton"; g.fillText("$50", -390 + c * 130, -100 + r * 110 + 14); });
  if (lt > 2.0) { g.fillStyle = "#e0344a"; g.beginPath(); g.roundRect(-450 + 3 * 130, -110 + 110 - 26, 140, 70, 14); g.fill(); g.fillStyle = "#fff"; g.font = "38px Anton"; g.fillText("RENT", -390 + 3 * 130, -110 + 110 + 20); } g.restore(); } };
const views = { type: "draw", x: 960, y: 520, fn: (g, x, y, k, lt) => { if (k <= 0) return; const n = Math.floor(Math.min(1, lt / 2.2) ** 2 * 2000000); g.save(); g.translate(x, y);
  g.fillStyle = "#16141c"; g.beginPath(); g.roundRect(-300, -380, 600, 760, 50); g.fill(); g.fillStyle = "#2a2640"; g.fillRect(-270, -330, 540, 420); g.font = "54px Anton"; g.fillStyle = "#ffb828"; g.textAlign = "center"; g.fillText("REAL PRICE GUY", 0, -130);
  g.fillStyle = "#fff"; g.font = "70px Anton"; g.fillText(n.toLocaleString("en-US"), 0, 190); g.font = "34px Mont"; g.fillText("VIEWS", 0, 250); g.restore(); } };
const subscribe = (g, x, y, k) => { const a = Math.min(1, k * 3) * Math.min(1, (5 - k * 5) * 2); };

export const BLOCKS = [
  { from: 0, to: 15, set: "bedroom", ...NIGHT, cast: BED, pose: { karl: "sit" }, sit: { karl: 0.18 }, phone: { karl: 1 }, emo: { karl: "sleepy" }, look: { karl: [-0.6, 0.6] }, cams: ["wide", "ms", "cu"], props: [["box", -2.2, 1.35, -3.3]] },
  { from: 16, to: 21, set: "street", cast: { karl: [0, 1.2, 0] }, extras: ex(8, -7, 2, -1.2, 0.2), cams: ["wide", "cu", "wide"] },
  { from: 22, to: 29, set: "store", cast: { karl: [-1.4, 1.2, 0.4], max: [1.6, 0.4, -0.4] }, props: [["chair", 2.7, 0, 0.0, -0.5]], extras: [[4.2, 0.2, -0.6]], cams: ["wide", "two", "cu:karl", "ms:max"] },
  { from: 30, to: 36, set: "kitchen", cast: { karl: [1.8, 0.6, -0.4], mom: [-1.6, -1.6, 0.4] }, props: [["blender", -2.4, 1.72, -3.3]], cams: ["wide", "ms:mom", "two", "cu:karl"] },
  { from: 37, to: 39, set: "lot", cast: { karl: [-3.2, 1.6, 0.5], dad: [-1.4, 0.8, 0.3] }, extras: [[0.6, 0.6, -0.5]], cams: ["wide", "ms:dad", "two"] },
  { from: 40, to: 43, set: "store", cast: { karl: [-1.0, 1.2, 0.3], grandma: [0.9, -0.4, -0.2] }, cams: ["ms:grandma", "two", "cu:grandma", "cu:grandma"] },
  { from: 44, to: 48, set: "office", cast: { karl: [-5.4, -0.6, 0.6], lena: [-3.6, -0.8, -0.5] }, props: [["cup", -6.4, 1.18, -2.2], ["cup", -6.0, 1.18, -2.2]], cams: ["wide", "ms:lena", "two", "cu:lena", "cu:karl"] },
  { from: 49, to: 53, set: "store", cast: { karl: [0, 1.0, 0.1], max: [3.2, 2.4, -0.9] }, phone: { max: 1 }, props: [["tv", -2.6, 0, -2.6, 0.3]], cams: ["wide", "ots:max:karl", "ms:karl", "wide", "cu:karl"] },
  { from: 54, to: 57, set: "street", cast: { karl: [0, 1.0, 0] }, extras: ex(10, -6, 1.3, -0.6, 0.15, 2, -1.4), exPose: ["point", "cheer", "point"], cams: ["wide", "two", "wide", "cu:karl"] },
  { from: 58, to: 59, set: "studio", cast: { karl: [-1.0, -1.0, 0.25] }, extras: [[1.2, -1.0, -0.25]], cams: ["wide", "two"] },
  { from: 60, to: 62, set: "street", cast: { karl: [0, 1.0, 0] }, extras: ex(14, -9, 1.4, -1.0, 0, 2, -1.6), cams: ["wide", "wide", "wide"] },
  { from: 63, to: 68, set: "bedroom", cast: { karl: [0.2, -0.6, 0.1] }, cams: ["ms:karl", "wide", "cu:karl"] },
  { from: 69, to: 74, set: "restaurant", bg: 0x2a1a2a, sun: 1.0, grade: "rgba(255,120,60,0.18)", cast: { karl: [-1.3, -0.6, 1.2], lena: [1.3, -0.6, -1.2] }, cams: ["two", "ots:karl:lena", "cu:karl", "ots:lena:karl"] },
  { from: 75, to: 86, set: "store", cast: { max: [0.6, 0.4, -0.2], karl: [-2.0, 1.4, 0.5] }, props: [["bags", 1.9, 0, 0.3]], phone: { max: 1 }, emo: { max: "happy", karl: "worried" }, cams: ["wide", "ms:max", "two", "cu:max", "ms:karl"] },
  { from: 87, to: 93, set: "kitchen", grade: "rgba(255,140,80,0.15)", cast: { max: [1.2, 0.2, -0.2], karl: [-1.6, 0.8, 0.5], mia: [3.4, -0.4, -0.6] }, props: [["cake", 1.2, 1.31, -1.2]], extras: [[-3.4, -1.0, 0.4], [4.8, 0.6, -0.8], [-0.2, -2.2, 0]], cams: ["wide", "cu:karl", "two", "cu:max"] },
  { from: 94, to: 103, set: "kitchen", ...NIGHT, grade: "rgba(90,70,160,0.35)", cast: { max: [0.6, 0.4, 0] }, phone: { max: 1 }, emo: { max: "worried" }, cams: ["wide", "cu:max", "ms:max"] },
  { from: 104, to: 110, set: "kitchen", ...NIGHT, cast: { mom: [0.4, -1.8, 0.1], dad: [2.2, -1.6, -0.4] }, emo: { mom: "sad", dad: "worried" }, cams: ["wide", "ms:mom", "ms:dad"] },
  { from: 111, to: 122, set: "bedroom", ...NIGHT, grade: "rgba(255,150,40,0.25)", cast: { karl: [0.8, -0.4, 0.2] }, emo: { karl: "sad" }, pose: { karl: "slump" }, cams: ["wide", "cu:karl", "ms:karl"], props: [["box", -2.2, 1.35, -3.3]] },
  { from: 123, to: 149, set: "mall", crowd: true, bg: 0x2a2440, grade: "rgba(140,60,200,0.2)", cast: { karl: [-0.5, -10, 0, 1.28] },
    extras: [[-3.2, -10.2, 0.3, 1.28], ...ex(30, -9, 2, -5.6, Math.PI, 3)], exPose: ["cheer", "idle", "point", "cheer"], props: [["mic", -0.2, 2.5, -9.6]], cams: ["crowdwide", "stage", "cu:karl"] },
  { from: 150, to: 157, set: "bedroom", ...NIGHT, cast: BED, pose: { karl: "sit" }, sit: { karl: 0.18 }, phone: { karl: 1 }, emo: { karl: "neutral" }, look: { karl: [-0.6, 0.6] }, cams: ["wide", "ms", "cu"], props: [["box", -2.2, 1.35, -3.3]] },
  { from: 158, to: 158, set: "kitchen", cast: { max: [0.8, 0.4, -0.2] }, props: [["fridge", 5.6, 0, -2.9]], emo: { max: "happy" }, cams: ["ms:max"] },
  { from: 159, to: 159, set: "kitchen", cast: { mom: [-0.6, -0.4, 0.3], dad: [1.4, -0.4, -0.3] }, emo: { mom: "happy", dad: "laugh" }, props: [["cup", 1.1, 1.31, -1.2]], cams: ["two"] },
  { from: 160, to: 160, set: "lot", cast: { dad: [0.2, 0.6, 0.4] }, emo: { dad: "happy" }, pose: { dad: "thumbsup" }, cams: ["wide"] },
  { from: 161, to: 161, set: "kitchen", cast: { mia: [0.6, 0.2, 0], karl: [-1.4, 0.6, 0.4] }, emo: { mia: "happy", karl: "happy" }, cams: ["two"] },
  { from: 162, to: 162, set: "kitchen", cast: { grandma: [0.4, 0.0, 0], karl: [-1.4, 0.6, 0.4] }, emo: { grandma: "happy", karl: "love" }, cams: ["two"] },
  { from: 163, to: 167, set: "office", cast: { karl: [-5.4, -0.6, 0.6], lena: [-3.6, -0.8, -0.5] }, props: [["cup", -6.4, 1.18, -2.2], ["cup", -6.0, 1.18, -2.2]], emo: { karl: "happy", lena: "smug" }, cams: ["two", "cu:lena", "cu:karl"] },
  { from: 168, to: 171, set: "office", cast: { karl: [0, 0.6, 0] }, emo: { karl: "smug" }, cams: ["ms:karl", "ms:karl", "cu:karl", "cu:karl"] },
];
const bedPhone = (o, flip) => ({ cam: "ms:karl", emo: { karl: "neutral" }, fx: [PH(o, flip)] });
export const LINES = {
  0: { fx: [{ type: "draw", x: 360, y: 170, fn: (g, x, y, k) => { g.save(); g.globalAlpha = Math.min(1, k * 3); g.font = "70px Anton"; g.fillStyle = "#ff5a6a"; g.textAlign = "center"; g.fillText("11:58", x, y); g.font = "30px Mont"; g.fillStyle = "#e8e4ff"; g.fillText("BLACK FRIDAY", x, y + 48); g.restore(); } }] },
  2: bedPhone(HP), 3: bedPhone(HP), 4: { cam: "cu:karl", emo: { karl: "smug" }, fx: [PL("head:karl", "That's a pizza.", 0.6)] },
  5: bedPhone(HP), 6: bedPhone(HP, 0.3), 7: { ...bedPhone(HP, -1), sfx: [["ping", 0.1]] },
  8: { cam: "cu:karl", emo: { karl: ["shock", 0.6, "dazed"] }, punch: 1 },
  9: bedPhone({ ...HP, real: ["YOU ALREADY", "OWN THESE"] }, 0.3), 10: bedPhone({ ...HP, real: ["YOU ALREADY", "OWN THESE"] }, -1),
  11: { cam: "wide", emo: { karl: "shock" }, look: { karl: [-1, 0.2] } },
  12: { cam: [[-2.6, 2.4, -0.4], [-2.5, 2.3, -0.9], [-2.2, 1.6, -3.3]], fx: [T("prop:0", "LAST BLACK FRIDAY", "STILL IN THE BOX", 0.4, { size: 46 })] },
  13: { cam: [[-2.5, 2.3, -0.9], [-2.45, 2.2, -1.3], [-2.2, 1.6, -3.3]], fx: [R("prop:0:0.4", ["HEADPHONES", { l: "PAYMENT 3 OF 4", size: 38, font: "Anton", col: "#e0344a" }], 0.2, { dx: 280, dy: 300 })], sfx: [] },
  14: { cam: "ms:karl", phone: { karl: 0 }, emo: { karl: "neutral" }, fx: [{ type: "draw", x: 360, y: 170, fn: (g, x, y, k) => { g.save(); g.globalAlpha = Math.min(1, k * 3); g.font = "70px Anton"; g.fillStyle = "#4fe08a"; g.textAlign = "center"; g.fillText("11:59", x, y); g.restore(); } }] },
  15: { cam: "cu:karl", phone: { karl: 0 }, emo: { karl: "happy" } },
  16: { fx: [0, 2, 4, 6].map((j, n) => T("head:" + j, "PAY IN 4", "JUST $30", 0.2 + n * 0.2, { ring: false, size: 36, sub: 20 })) },
  17: { emo: { karl: "smug" }, fx: [{ type: "rings", at: "head:karl", t: 0.1, n: 4, r: 400 }, { type: "glow", at: "face:karl", t: 0.1, r: 420, a: 0.3 }] },
  18: { cam: "wide", fx: [0, 1, 3, 5, 7].map((j, n) => T("head:" + j, ["$80", "$120", "$300", "$45", "$600"][n], ["4 H", "6 H", "15 H", "2 H", "30 H"][n], 0.2 + n * 0.25, { size: 40, sub: 20 })) },
  19: { cam: "cu:karl", fx: [R([1350, 820], ["THE REAL PRICE:", { l: "1. THE WHOLE NUMBER", size: 30, font: "Anton" }, { l: "2. HOURS OF YOUR LIFE", size: 30, font: "Anton" }, { l: "3. IF ONE PAYMENT SLIPS", size: 30, font: "Anton", col: "#e0344a" }], 0.3, { w: 440, dur: 2.0 })] },
  20: { set: "office", cast: { karl: [0.4, -1.4, 0] }, extras: [], pose: { karl: "thumbsup" }, emo: { karl: "happy" }, cam: "ms:karl", fx: [CARD([["KARL, 23", 70, "#ffb828"], ["FIRST JOB · ~$20/HOUR AFTER TAX", 40], ["EXAMPLE", 26, "#bbb"]], 0.2, { y: 220, w: 860 })] },
  21: { cam: "wide", fx: [0, 2, 4, 6].map((j, n) => T("head:" + j, ["$120", "$400", "$90", "$240"][n], "REAL PRICE", 0.2 + n * 0.2, { size: 40, sub: 20 })) },
  22: { walk: { karl: 0.3 }, emo: { karl: "happy" }, cam: "wide", cast: { max: null }, props: [], extras: [] },
  23: { cam: [[0, 3.2, 6], [0, 3.6, 5.2], [0, 4.9, -4.9]], fx: [] },
  24: { cam: [[0, 3.6, 5.2], [0, 3.8, 4.6], [0, 4.6, -4.9]], fx: [T([0, 4.0, -4.8], "ALSO TODAY ONLY", "LAST TUESDAY", 0.4, { size: 46 })] },
  25: { cam: "two", cast: { max: null }, emo: { karl: "laugh" }, pose: { karl: "cheer" }, props: [], extras: [[2.4, 0.4, -0.6]], exEmo: ["worried"] },
  26: { emo: { max: "happy", karl: "neutral" } },
  27: { cam: "ms:max", emo: { max: "laugh" }, pose: { max: "thumbsup" }, fx: [PL("head:max", "Just $100 today, bro.")] },
  28: { cam: "two", emo: { karl: "worried" }, fx: [T("prop:0:2.4", "$400", "20 HOURS · PLAN #4 THIS MONTH", 0.3)] },
  29: { cam: "two", emo: { karl: "neutral", max: "happy" } },
  30: { cam: "ms:mom", phone: { mom: 1 }, emo: { mom: "happy" }, fx: [PL("head:mom", "Only $22.50, four times!")] },
  31: { cam: "two", phone: { mom: 1 }, emo: { mom: "neutral", karl: "smug" }, fx: [T("phone:mom", "$90", "YOU HAVE A BLENDER", 0.3, { dy: -120 })] },
  32: { cam: "ms:mom", emo: { mom: "laugh" }, pose: { mom: ["idle", "sit", 0.8, 0.4] }, fx: [{ type: "rings", at: "prop:0:0.8", t: 0.1, col: "255,255,255" }] },
  33: { cam: "cu:karl", emo: { karl: "happy" }, fx: [T("head:karl", "SAVED: $90", "PAID IN LASAGNA", 0.5, { size: 44 })] },
  34: { cast: { mom: null, mia: [-0.6, 0.0, 0.5] }, phone: { mia: 1 }, cam: "ms:mia", emo: { mia: "happy" }, props: [], fx: [PL("head:mia", "Pay in 4. Basically free.")] },
  35: { cast: { mom: null, mia: [-0.6, 0.0, 0.5] }, cam: "two", props: [], emo: { mia: "shock", karl: "smug" }, fx: [T("head:mia:1.7", "$240", "30 HOURS OF BABYSITTING", 0.3)] },
  36: { cast: { mom: null, mia: [-0.6, 0.0, 0.5] }, cam: "ms:mia", props: [], emo: { mia: ["angry", 1.5, "neutral"] }, fx: [notebook(["$240 = 30 H", "ONE PAIR ✓"].map(s => s.replace("✓", "OK")))] },
  37: { cam: "ms:0", emo: { dad: "happy" }, exEmo: ["smug"], exPose: ["thumbsup"], fx: [PL("head:0", "Only $499 a month!")] },
  38: { cam: "two", emo: { dad: "shock" }, fx: [T("head:0:1.6", "72 PAYMENTS", "~$36,000", 0.3, { size: 58, sub: 34 })] },
  39: { cam: "wide", extras: [], emo: { dad: "smug" }, pose: { dad: "thumbsup" }, fx: [CARD([["MEET \"THIRTY-SIX THOUSAND\"", 54, "#ffb828"]], 0.4, { y: 200, w: 960, h: 140 })] },
  40: { emo: { grandma: "happy" }, pose: { grandma: "hold" }, fx: [{ type: "draw", at: "hand:grandma", fn: (g, x, y, k) => { if (k <= 0) return; g.save(); g.translate(x, y - 40); g.rotate(-0.15); for (let i = 0; i < 3; i++) { g.fillStyle = ["#f6efe2", "#efe4cf", "#f6efe2"][i]; g.fillRect(-70 + i * 14, -45 - i * 10, 140, 90); g.strokeStyle = "#c9bfa8"; g.lineWidth = 3; g.strokeRect(-70 + i * 14, -45 - i * 10, 140, 90); } g.restore(); } }] },
  41: { emo: { grandma: "smug" }, fx: [T("head:grandma", "$24", "= $24", 0.3)] },
  42: { emo: { grandma: "smug" } },
  43: { emo: { grandma: "laugh" }, fx: [PL("head:grandma", "I'm old, not new.", 0.8)] },
  45: { cast: { karl: [-5.4, -0.6, 0.6], lena: [5.6, -2.6, -0.6] }, emo: { lena: "smug" }, pose: { lena: "point" }, fx: [{ type: "spark", at: [6.6, 1.4, -3.6], t: 0.6 }] },
  46: { emo: { karl: "happy", lena: "happy" }, fx: [T("prop:0:0.4", "$6", null, 0.6, { ring: false, size: 40 })] },
  47: { emo: { lena: "happy" }, fx: [T("head:lena", "$6", "WORTH IT", 0.3, { size: 60, sub: 30 })] },
  48: { emo: { karl: "love" }, fx: [{ type: "spark", at: "head:karl", t: 0.2, n: 6 }] },
  49: { emo: { karl: "smug" }, fx: [TX("THEN IT GETS BIGGER", 100, "#ffffff", 0.05, { y: 200 })] },
  50: { emo: { karl: "neutral", max: "laugh" } },
  51: { pose: { karl: "point" }, fx: [T("prop:0:2.4", "$600", "30 HOURS · 18 MONTHS", 0.3)] },
  52: { cam: "wide", fx: [views] },
  53: { emo: { karl: "shock" }, fx: [CARD([["\"THE REAL PRICE GUY\"", 72, "#ffb828"]], 0.3, { y: 200, h: 150 })] },
  54: { emo: { karl: "worried" } },
  55: { fx: [PL("head:3", "What does mine say?", 0.1)] },
  56: { cast: { karl: [-1.0, 1.0, 0.3] }, extras: [[1.4, 0.6, -0.4]], exEmo: ["angry"], exPose: ["no"], cam: "two", fx: [{ type: "card", at: "head:0:0.5", dy: -60, w: 560, h: 180, lines: [["NO REAL PRICES", 44, "#ffffff"], ["PAST THIS POINT", 44, "#ff5a6a"]], t: 0.3 }] },
  57: { set: "kitchen", cast: { karl: [0.6, 0.8, -0.2] }, extras: [], props: [["cake", 1.2, 1.31, -1.2]], emo: { karl: "dazed" }, cam: [[1.6, 2.8, 2.2], [1.5, 2.7, 1.6], [1.2, 1.5, -1.2]], fx: [{ type: "text", at: "prop:0:0.8", text: "PAY IN 4", size: 70, col: "#ff5fa2", t: 1.4 }] },
  58: { fx: [T([-3.5, 3.5, -4], "GOLD WATCH", "$1,200 · 60 H", 0.6, { size: 36, sub: 20 }), T([0, 3.0, -4], "SOFA", "$900 · 45 H", 1.2, { size: 36, sub: 20 }), T([3.5, 3.5, -4], "WEDDING DRESS", "$2,000 · 100 H", 1.8, { size: 36, sub: 20 })] },
  59: { exEmo: ["shock"], exPose: ["shrug"], emo: { karl: "smug" } },
  60: { fx: [0, 2, 4, 6, 8, 10, 12].map((j, n) => T("head:" + j, ["$50", "$30", "$100", "$25", "$75", "$40", "$60"][n], "x4", 0.1 + n * 0.12, { size: 34, sub: 18 })) },
  61: { fx: [R([1400, 860], [{ l: "HOLIDAY SEASON 2025", size: 28 }, { l: "BUY NOW, PAY LATER", size: 30, font: "Anton" }, { l: "~$20 BILLION", size: 56, font: "Anton", col: "#e0344a" }, { l: "SOURCE: ADOBE", size: 22, col: "#8a8496" }], 0.4, { w: 420 })] },
  62: { fx: [TX("$20,000,000,000", 120, "#ffb828", 0.1, { y: 260 }), TX("4 EASY PAYMENTS AT A TIME", 50, "#ffffff", 0.6, { y: 380 })] },
  63: { emo: { karl: "shock" }, pose: { karl: "hold" }, fx: [envelope(true)] },
  64: { set: "mall", crowd: true, bg: 0x2a2440, cast: {}, cam: "crowdwide", fx: [] },
  65: { set: "mall", crowd: true, bg: 0x2a2440, cast: {}, cam: [[0, 9, 20], [0, 8, 17], [0, 3, -9]], fx: [CARD([["10,000 PEOPLE", 70, "#ffffff"], ["MIDNIGHT · LIVE ON TV", 46, "#ff5a6a"]], 0.2, { y: 200 })] },
  66: { set: "mall", bg: 0x2a2440, cast: {}, cam: [[4, 3.6, -3], [3.6, 3.4, -4], [2.5, 2.4, -10]], fx: [{ type: "rings", at: [2.5, 2.7, -10], col: "255,90,106", t: 0.3 }, { type: "glow", at: [2.5, 2.7, -10], col: "255,90,106", r: 220, a: 0.35 }] },
  67: { emo: { karl: "shock" }, fx: [TX("$5,000", 160, "#4fe08a", 0.2, { y: 280 })] },
  68: { emo: { karl: "smug" }, pose: { karl: "thumbsup" } },
  69: { cam: "cu:karl", emo: { karl: "worried" }, fx: [{ type: "glow", at: "face:karl", r: 380, a: 0.3, t: 0.1 }] },
  70: { emo: { lena: "happy" }, fx: [{ type: "glow", at: [0, 1.4, -0.8], r: 300, a: 0.4, t: 0.3 }] },
  71: { cam: "two", fx: [T([-0.5, 2.0, -0.8], "PASTA $18", "~1 HOUR", 0.2, { size: 40, sub: 22 }), T([0.6, 2.4, -0.8], "DESSERT", "40 MINUTES", 1.6, { size: 40, sub: 22 })] },
  72: { emo: { karl: "sad" } },
  73: { emo: { lena: "worried" }, fx: [PL("head:lena", "Reading the menu like a contract?")] },
  74: { cam: "two", emo: { karl: "smug", lena: "sad" }, fx: [PL("head:karl", "It kind of is.")] },
  77: { fx: [R([1400, 850], [{ l: "MAX'S CART", size: 26 }, { l: "$2,000", size: 36, font: "Anton" }, { l: "-40%", size: 36, font: "Anton", col: "#e0344a" }, { l: "$1,200", size: 50, font: "Anton" }, { l: "EXAMPLE", size: 22, col: "#8a8496" }], 0.2, { w: 340 })] },
  78: { fx: [{ type: "bubbles", at: "head:max:1.4", n: 6, t: 0.2 }, TX("6 PLANS · 24 × $50", 64, "#ffffff", 0.8, { y: 960 })] },
  79: { cam: "two", fx: [{ type: "bubbles", at: "head:max:1.4", n: 6, t: 0, merge: 1.4, top: "$1,200", bot: "60 HOURS · EXAMPLE" }] },
  80: { emo: { max: "happy" }, pose: { max: "thumbsup" } },
  81: { cam: "ms:karl", fx: [R([1380, 860], [{ l: "MORE THAN ONE", size: 30, font: "Anton" }, { l: "BNPL LOAN AT ONCE", size: 30, font: "Anton" }, { l: "~6 IN 10", size: 60, font: "Anton", col: "#e0344a" }, { l: "SOURCE: CFPB, 2025", size: 22, col: "#8a8496" }], 0.6, { w: 400 })] },
  82: { cam: "cu:max", fx: [] },
  83: { cam: "two", fx: [{ type: "bubbles", at: "head:max:1.4", n: 1, t: 0.1 }, T("head:max:3.0", "$1,200", "WHAT IT REALLY IS", 1.2, { dx: 360 })] },
  84: { cast: { karl: null }, cam: "ms:max", fx: [TX("$200  →  4 × $50", 90, "#ffffff", 0.1, { y: 230 }), TX("HURTS LESS", 70, "#ff5fa2", 0.9, { y: 340 })] },
  85: { cam: "cu:karl", emo: { karl: "smug" }, fx: [CARD([["NOT A BUG.", 70, "#ffffff"], ["THE PRODUCT.", 70, "#ffb828"]], 0.6, { y: 230 })] },
  86: { cam: "wide", fx: [R([1400, 860], [{ l: "STORE PAYS THE APP", size: 28, font: "Anton" }, { l: "A FEE ON EVERY SALE", size: 28, font: "Anton" }, { l: "SPLIT PRICE", size: 34 }, { l: "= BUY MORE", size: 46, font: "Anton", col: "#e0344a" }], 0.4, { w: 400 })] },
  87: { cam: "ms:max", emo: { max: "laugh" }, pose: { max: "shrug" }, fx: [PL("head:max", "Only $50 here, $50 there!")] },
  88: { emo: { karl: "worried" } },
  89: { cam: "two", emo: { karl: "angry", max: ["happy", 1.2, "shock"] }, pose: { karl: "point" }, fx: [PL("head:karl", "It's $1,200, Max. 60 hours."), T("head:max:1.6", "$1,200", "60 HOURS", 1.0)] },
  90: { exEmo: ["shock"], exPose: ["idle"], emo: { karl: "worried", max: "shock", mia: "shock" } },
  91: { emo: { max: "sad" }, pose: { max: "slump" } },
  92: { cam: "two", emo: { max: "angry", karl: "sad" }, fx: [PL("head:max", "Must be nice. Smarter than everybody.")] },
  93: { set: "bedroom", ...NIGHT, cast: { karl: [0.8, -0.4, 0.2] }, props: [], extras: [], pose: { karl: "slump" }, phone: { karl: 1 }, emo: { karl: "sad" }, cam: "ms:karl", fx: [{ type: "draw", x: 1380, y: 400, fn: (g, x, y, k) => { if (k <= 0) return; g.save(); g.globalAlpha = Math.min(1, k * 2); for (let i = 0; i < 3; i++) { g.fillStyle = "#2ec4b6"; g.beginPath(); g.roundRect(x - 220, y - 120 + i * 100, 440, 74, 30); g.fill(); g.fillStyle = "#fff"; g.font = "34px Mont"; g.textAlign = "center"; g.fillText(["Sorry man", "Max?", "you ok?"][i], x, y - 74 + i * 100); g.font = "20px Mont"; g.fillStyle = "#cfcadb"; g.fillText("Seen", x + 190, y - 30 + i * 100); } g.restore(); } }] },
  94: { cam: "wide", fx: [calendar] },
  95: { emo: { max: "panic" }, pose: { max: "panic" }, fx: [TX("MISSED: 1", 80, "#ff5a6a", 0.1, { y: 230 }), TX("MISSED: 2", 80, "#ff5a6a", 1.0, { y: 340 })] },
  96: { cam: "ms:max", fx: [R([1400, 860], [{ l: "PAID LATE", size: 30, font: "Anton" }, { l: "IN THE PAST YEAR", size: 28 }, { l: "~4 IN 10", size: 60, font: "Anton", col: "#e0344a" }, { l: "SOURCE: LENDINGTREE 2025", size: 20, col: "#8a8496" }], 0.4, { w: 420 })] },
  97: { fx: [TX("2026: ALMOST HALF", 96, "#ff5a6a", 0.1, { y: 250 })] },
  98: { cam: "cu:max", fx: [{ type: "draw", at: "hand:max", fn: (g, x, y, k) => { if (k <= 0) return; g.save(); g.translate(x + 60, y - 60); g.rotate(-0.2); const s = Math.min(1, k * 2); g.scale(s, s); g.fillStyle = "#4a7fc1"; g.beginPath(); g.roundRect(-120, -75, 240, 150, 16); g.fill(); g.fillStyle = "#ffc23a"; g.fillRect(-90, -30, 50, 36); g.fillStyle = "#fff"; g.font = "26px Mont"; g.fillText("•••• 1200", -90, 50); g.restore(); } }] },
  99: { fx: [T("head:max", "~21%", "INTEREST A YEAR", 0.3)] },
  100: { cam: "wide", fx: [R([1300, 950], [{ l: "EXAMPLE", size: 22, col: "#8a8496" }, { l: "$1,200 ON A CARD", size: 34, font: "Anton" }, { l: "~21% A YEAR", size: 30 }, { l: "MINIMUM PAYMENTS", size: 30 }, { l: "MONTH 1 ... 12 ... 36 ...", size: 28 }, { l: "... 60 ... 87", size: 28 }], 0.3, { w: 440, dur: 3.0 })] },
  101: { cam: "cu:max", emo: { max: "shock" }, punch: 1, fx: [TX("~7 YEARS", 180, "#ff5a6a", 0.05, { y: 260 })] },
  102: { cam: "cu:max", emo: { max: "panic" }, fx: [TX("~$2,270", 180, "#ff5a6a", 0.05, { y: 260 })] },
  103: { cam: "ms:max", emo: { max: "sad" }, pose: { max: "slump" }, fx: [CARD([["FULL PRICE  $2,000", 54, "#ffffff"], ["\"-40%\" ON A CARD  ~$2,270", 54, "#ff5a6a"]], 0.2, { y: 240, w: 1000 })] },
  104: { cast: { karl: [-2.4, 1.2, 0.5] }, emo: { karl: "worried" }, cam: "wide" },
  105: { cam: [[1.6, 3.0, 1.4], [1.4, 2.9, 1.0], [1.2, 1.3, -1.2]], cast: {}, fx: [PH({ clock: "21:14", title: "3 ACTIVE PLANS", old: null, price: null, sub: "CHRISTMAS GIFTS", btn: ["PAY IN 4", "NEXT: $40 ON FRIDAY"], draw: (g, x, y) => { g.fillStyle = "#ff5fa2"; for (let i = 0; i < 3; i++) { g.beginPath(); g.arc(x - 110 + i * 110, y, 44, 0, 7); g.fill(); } g.fillStyle = "#fff"; g.font = "30px Anton"; g.textAlign = "center"; for (let i = 0; i < 3; i++) g.fillText("$40", x - 110 + i * 110, y + 10); } })] },
  106: { cam: [[1.4, 2.9, 1.0], [1.3, 2.8, 0.7], [1.2, 1.3, -1.2]], cast: {}, fx: [PH({ clock: "21:14", title: "3 ACTIVE PLANS", sub: "1 GIFT FOR: KARL", btn: ["PAY IN 4", "3 × $160"], draw: (g, x, y) => { g.fillStyle = "#2ec4b6"; g.fillRect(x - 70, y - 60, 140, 120); g.fillStyle = "#e0344a"; g.fillRect(x - 12, y - 60, 24, 120); g.fillRect(x - 70, y - 12, 140, 24); } }, 1.2)] },
  107: { cast: { karl: [-0.6, 0.6, 0.2] }, cam: "cu:karl", emo: { karl: "sad" }, fx: [T("head:karl", "$160", "2 WEEKS OF GROCERY MONEY", 0.3)] },
  108: { cast: { karl: [-4.2, 1.6, 0.6, 0.7] }, props: [["stairs", -4.2, 0, 2.6, Math.PI]], pose: { karl: "sit" }, emo: { karl: "sad", mom: "sad", dad: "worried" }, cam: [[-6.8, 2.6, 4.6], [-6.4, 2.5, 4.2], [0.6, 2.2, -1.6]] },
  109: { cam: "ms:dad", fx: [PL("head:dad", "We can't keep doing this every December.")] },
  110: { cam: "ms:mom", emo: { mom: "sad" }, fx: [PL("head:mom", "I just wanted a normal Christmas.")] },
  111: { cam: "wide", fx: [T([2.4, 1.4, -2.6], "BED", "$400 · 20 H", 0.2, { size: 36, sub: 20 }), T([-3.3, 2.5, -3.4], "LAMP", "$35", 0.7, { size: 36, sub: 20 }), T([-2.2, 2.1, -3.3], "HEADPHONES", "$120 · STILL IN BOX", 1.2, { size: 36, sub: 20 })] },
  113: { set: "street", grade: "rgba(90,110,160,0.3)", cast: { karl: [0, 1.0, 0] }, props: [], walk: { karl: 0.4 }, pose: { karl: "idle" }, cam: "wide" },
  114: { set: "kitchen", grade: null, cast: { mia: [0.8, -0.2, -0.3], karl: [-1.6, 0.8, 0.5] }, props: [], pose: { karl: "idle", mia: "hold" }, emo: { mia: "angry", karl: "sad" }, cam: "two" },
  115: { set: "office", grade: "rgba(90,110,160,0.25)", cast: { karl: [-5.4, -0.6, 0.6] }, props: [], pose: { karl: "idle" }, cam: "ms:karl", fx: [T("head:karl", "$6", "18 MINUTES", 0.5)] },
  116: { set: "street", grade: "rgba(90,110,160,0.3)", cast: { karl: [-6, 1.0, 1.4] }, props: [], walk: { karl: 0.9 }, pose: { karl: "idle" }, cam: "wide" },
  117: { cam: "wide", pose: { karl: "slump" }, fx: [{ type: "glow", x: 960, y: 540, r: 900, a: 0.25, t: 0.2 }, ...[[2.4, 1.4, -2.6], [-3.3, 2.5, -3.4], [-2.2, 2.1, -3.3], [1.6, 4.0, -3.9]].map((p, j) => ({ type: "rings", at: p, t: 0.2 + j * 0.3, n: 2 }))] },
  119: { fx: [CARD([["SEEING THE REAL PRICE", 56, "#ffffff"], ["WAS NEVER THE HARD PART", 56, "#ffffff"]], 0.2, { y: 230, w: 1000 })] },
  120: { emo: { karl: "neutral" }, pose: { karl: "idle" }, fx: [CARD([["SAYING IT SO PEOPLE", 56, "#ffb828"], ["CAN HEAR IT IS", 56, "#ffb828"]], 0.2, { y: 230, w: 1000 })] },
  121: { emo: { karl: "worried" }, pose: { karl: "idle" }, fx: [envelope(true), TX("3 DAYS", 90, "#ff5a6a", 0.6, { y: 200 })] },
  122: { emo: { karl: "worried" }, pose: { karl: "idle" } },
  123: { fx: [] },
  124: { cam: [[4, 3.6, -3], [3.6, 3.4, -4], [2.5, 2.4, -10]], fx: [{ type: "rings", at: [2.5, 2.7, -10], col: "255,90,106", t: 0.3 }, { type: "glow", at: [2.5, 2.7, -10], col: "255,90,106", r: 220, a: 0.35, t: 0.1 }] },
  125: { cam: "ms:0", fx: [PL("head:0", "Real Price Guy! Press it!")], exPose: ["point"] },
  126: { cam: [[-0.5, 3.2, -8.4], [-0.5, 3.4, -7.6], [0, 2.4, 6]], fx: [0, 2, 4, 6, 8, 10, 12, 14].map((j, n) => T("head:" + (j + 1), ["$120", "$400", "$90", "$1,200", "$60", "$240", "$800", "$35"][n], null, 0.2 + n * 0.12, { size: 34, ring: false })) },
  127: { cam: "cu:karl", emo: { karl: "neutral" }, pose: { karl: "no" } },
  128: { cam: "stage", fx: [PL("head:karl", "I'm not here to tell you what to buy.")] },
  129: { cam: "ms:karl", pose: { karl: "shrug" }, fx: [PL("head:karl", "Some of you need that fridge.")] },
  130: { cam: "cu:karl", emo: { karl: "smug" }, fx: [PL("head:karl", "Here's what the button doesn't say.")] },
  131: { cam: "stage", pose: { karl: "point" }, fx: [CARD([["SAY THE FULL PRICE", 64, "#ffffff"], ["OUT LOUD", 64, "#ffb828"]], 0.3, { y: 220 })] },
  132: { cam: "ms:karl", fx: [TX("NOT $50.", 90, "#ff5fa2", 0.1, { y: 200 }), TX("THE WHOLE THING.", 90, "#ffb828", 0.8, { y: 310 })] },
  133: { cam: "crowdwide", fx: [CARD([["CASH TODAY? → PRESS IT", 52, "#4fe08a"], ["NOT IN CASH? → IT'S A LOAN", 52, "#ff5a6a"]], 0.3, { y: 220, w: 1100 })] },
  134: { cam: "ms:0", exEmo: ["shock"], exPose: ["shrug"] },
  135: { cam: "crowdwide", fx: [{ type: "rings", x: 1500, y: 900, t: 0.6, col: "255,255,255" }] },
  136: { cast: { karl: [-0.5, -10, 0, 1.28], max: [6, 2.0, Math.PI * 0.85] }, phone: { max: 1 }, emo: { max: "worried" }, cam: [[3.4, 3.0, -2.4], [3.6, 3.0, -1.8], [6, 2.6, 2.0]], fx: [PL("head:max", "Twelve hundred dollars!")] },
  137: { cast: { karl: [-0.5, -10, 0, 1.28], max: [6, 2.0, Math.PI * 0.85] }, phone: { max: 1 }, emo: { max: "neutral" }, cam: [[3.6, 3.0, -1.8], [3.8, 2.9, -1.2], [6, 2.6, 2.0]], fx: [T("phone:max", "$1,200", "PAYING IT OFF", 0.3)] },
  138: { cast: { karl: [-0.5, -10, 0, 1.28], max: [6, 2.0, Math.PI * 0.85] }, emo: { max: "happy" }, pose: { max: "cheer" }, cam: [[3.8, 2.9, -1.2], [4.0, 2.9, -0.8], [6, 2.6, 2.0]], fx: [PL("head:max", "And I'm paying it off!")] },
  139: { cam: [[0, 4, -4], [0, 4.2, -3.2], [0, 2.4, 6]], exPose: ["cheer"], fx: [PL("head:7", "$340!", 0.8)] },
  140: { cast: { karl: [-0.5, -10, 0, 1.28], dad: [-5, 1.6, Math.PI * 1.1] }, emo: { dad: "laugh" }, pose: { dad: "cheer" }, cam: [[-3, 3.0, -2.2], [-3.2, 3.0, -1.6], [-5, 2.6, 1.6]], fx: [PL("head:dad", "$36,000! And I said no!")] },
  141: { cast: { karl: [-0.5, -10, 0, 1.28], mom: [-1.5, 3.0, Math.PI], grandma: [0.2, 3.0, Math.PI] }, emo: { mom: "happy", grandma: "smug" }, pose: { mom: "cheer", grandma: "cheer" }, cam: [[-0.6, 3.0, -0.6], [-0.6, 3.0, 0.0], [-0.6, 2.4, 3.0]], fx: [PL("head:mom", "$480!", 0.1), PL("head:grandma", "Zero!", 1.8)] },
  142: { cam: "cu:karl", emo: { karl: "dazed" }, fx: [{ type: "rings", at: "head:karl", n: 4, r: 600, t: 0.3 }, { type: "glow", at: "face:karl", r: 500, a: 0.35, t: 0.2 }] },
  143: { cam: "crowdwide", fx: [{ type: "rings", x: 960, y: 520, n: 5, r: 1100, t: 0.1 }, ...[0, 3, 6, 9, 12, 15, 18, 21].map((j, n) => T("head:" + (j + 1), ["$120", "$400", "$90", "$1,200", "$60", "$240", "$800", "$35"][n], null, 0.6 + n * 0.1, { size: 30, ring: false }))] },
  144: { cam: [[-0.5, 3.2, -8.4], [-0.5, 3.4, -7.6], [0, 2.4, 6]], emo: { karl: "happy" }, fx: [...[1, 3, 5, 7, 9, 11, 13, 15, 17, 19].map((j, n) => T("head:" + j, ["$120", "$400", "$90", "$1,200", "$60", "$240", "$800", "$35", "$300", "$75"][n], "REAL PRICE", 0.1 + n * 0.1, { size: 30, sub: 16, ring: false }))] },
  145: { cam: [[0, 4, -4], [0, 4.2, -3.2], [0, 2.4, 6]], exPose: ["hold", "point", "shrug"], exEmo: ["happy", "neutral", "smug"] },
  146: { cam: "crowdwide", fx: [R([1450, 880], [{ l: "SAID OUT LOUD", size: 30, font: "Anton" }, { l: "10,000", size: 50, font: "Anton", col: "#2ec4b6" }, { l: "PUT BACK: A LOT", size: 30 }, { l: "PAID ON PURPOSE: THE REST", size: 26 }], 0.3, { w: 460, dur: 1.6 })] },
  147: { cam: "ms:0", exEmo: ["sad"], exPose: ["slump"] },
  148: { cam: "cu:karl", emo: { karl: "smug" }, fx: [TX("$5,000", 160, "#8a8496", 0.1, { y: 260 }), { type: "draw", x: 960, y: 260, t: 0.8, fn: (g, x, y, k) => { if (k <= 0) return; g.save(); g.strokeStyle = "#ff5a6a"; g.lineWidth = 18; g.lineCap = "round"; g.beginPath(); g.moveTo(x - 300, y + 40); g.lineTo(x - 300 + 600 * Math.min(1, k * 2), y + 40 - 80 * Math.min(1, k * 2)); g.stroke(); g.restore(); } }] },
  149: { cam: "stage", emo: { karl: "happy" }, pose: { karl: "cheer" }, fx: [{ type: "spark", at: "head:karl", n: 6, t: 0.2 }] },
  150: { fx: [{ type: "draw", x: 360, y: 170, fn: (g, x, y, k) => { g.save(); g.globalAlpha = Math.min(1, k * 3); g.font = "70px Anton"; g.fillStyle = "#ff5a6a"; g.textAlign = "center"; g.fillText("11:58", x, y); g.font = "30px Mont"; g.fillStyle = "#e8e4ff"; g.fillText("ONE YEAR LATER", x, y + 48); g.restore(); } }] },
  152: bedPhone(HP), 153: bedPhone(HP), 154: { cam: "cu:karl", emo: { karl: "smug" } },
  155: { cam: "cu:karl", emo: { karl: "neutral" }, fx: [PL("head:karl", "$120. Six hours.", 0.3)] },
  156: { cam: "ms:karl", emo: { karl: "neutral" }, fx: [CARD([["PAY IT IN CASH TODAY?", 60, "#ffffff"], ["NO.", 80, "#ff5a6a"]], 0.2, { y: 230 })] },
  157: { cam: "cu:karl", phone: { karl: 0 }, emo: { karl: "happy" }, fx: [{ type: "draw", x: 360, y: 170, fn: (g, x, y, k) => { g.save(); g.globalAlpha = Math.min(1, k * 3); g.font = "70px Anton"; g.fillStyle = "#4fe08a"; g.textAlign = "center"; g.fillText("11:59", x, y); g.restore(); } }] },
  158: { fx: [notebook(["PLAN 6 OF 6", "DUE: FRI 14", "THEN: FREE"])] },
  159: { fx: [T("prop:0:0.6", "HANDMADE", "PRICELESS (~$4)", 0.6, { size: 40 })] },
  160: { fx: [{ type: "spark", at: [2.5, 2.2, -3], t: 0.4, n: 5 }] },
  161: { fx: [R([1350, 850], [{ l: "SNEAKERS", size: 32, font: "Anton" }, { l: "PAID: CASH", size: 34 }, { l: "BABYSITTING MONEY", size: 26 }, { l: "PAID IN FULL", size: 40, font: "Anton", col: "#2ec4b6" }], 0.3, { w: 400 })] },
  162: { fx: [envelope(false)] },
  164: { cam: "two", fx: [PL("head:karl", "Six dollars. Worth it.")] },
  165: { fx: [PL("head:lena", "Did you just price me?")] },
  166: { emo: { karl: "love" }, fx: [PL("head:karl", "Yeah. Worth it."), T("head:lena", "$6", "WORTH IT", 0.6, { dx: 300 })] },
  167: { cam: "two", emo: { lena: "laugh", karl: "love" }, fx: [{ type: "spark", at: "head:lena", n: 5, t: 0.3 }] },
  168: { fx: [] },
  169: { fx: [CARD([["BEFORE ANY \"PAY IN 4\":", 54, "#ffffff"], ["SAY THE FULL PRICE OUT LOUD", 54, "#ffb828"], ["NOT IN CASH TODAY? IT'S A LOAN.", 44, "#ff5a6a"]], 0.2, { y: 260, w: 1200 })] },
  170: { fx: [{ type: "rings", at: "head:karl", n: 3, r: 500, t: 0.2 }, TX("WOULD YOU WANT IT?", 96, "#ffb828", 0.4, { y: 200 })] },
  171: { emo: { karl: "happy" }, fx: [PL("head:karl", "Tell me in the comments.", 0.6)] },
};
// subscribe pill at the start of "Then it gets bigger" (line 49) for 5 s, top centre
export function GLOBAL(g, t, TM, h) {
  const s = TM.lines[49]?.[0]; if (s === undefined || t < s || t > s + 5) return; const k = (t - s) / 5, a = h.pop(Math.min(1, k * 6)) * Math.min(1, (1 - k) * 8);
  g.save(); g.translate(960, 110); g.scale(a, a); g.fillStyle = "#ffffff"; g.beginPath(); g.roundRect(-260, -48, 520, 96, 48); g.fill();
  g.fillStyle = "#2ec4b6"; g.beginPath(); g.arc(-200, 0, 34, 0, 7); g.fill(); g.fillStyle = "#1d1b23"; g.beginPath(); g.arc(-200, 2, 22, 0, 7); g.fill();
  const done = k > 0.45; g.fillStyle = done ? "#8a8496" : "#e0344a"; g.beginPath(); g.roundRect(-140, -32, 300, 64, 32); g.fill();
  g.fillStyle = "#fff"; g.font = "34px Anton"; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(done ? "SUBSCRIBED" : "SUBSCRIBE", 10, 2);
  g.fillStyle = "#1d1b23"; g.font = "40px Anton"; g.fillText(done ? "🔔" : "", 210, 2);
  const cx = 60 + (1 - Math.min(1, k * 2.4)) * 300, cy = 40 + (1 - Math.min(1, k * 2.4)) * 200; g.fillStyle = "#fff"; g.strokeStyle = "#1d1b23"; g.lineWidth = 4;
  g.beginPath(); g.moveTo(cx, cy); g.lineTo(cx + 28, cy + 70); g.lineTo(cx + 38, cy + 40); g.lineTo(cx + 66, cy + 30); g.closePath(); g.fill(); g.stroke(); g.restore();
}
