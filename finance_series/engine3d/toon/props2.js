// Simple toon props for episode scenes. makeProp(name) -> THREE.Group (feet at y=0 unless noted).
import * as THREE from "three";
import { TOON, mesh } from "./toon.js";
const B = (g, w, h, d, c, x, y, z, o = {}) => { const m = mesh(new THREE.BoxGeometry(w, h, d), TOON(c), { outline: o.outline === undefined ? 0x4a4656 : o.outline, w: o.w ?? 0.01 }); m.position.set(x, y, z); g.add(m); return m; };
const C = (g, rt, rb, h, c, x, y, z, seg = 20) => { const m = mesh(new THREE.CylinderGeometry(rt, rb, h, seg), TOON(c), { outline: 0x4a4656, w: 0.01 }); m.position.set(x, y, z); g.add(m); return m; };
export function makeProp(name) {
  const g = new THREE.Group(); g.name = name;
  if (name === "chair") { B(g, 0.9, 0.15, 0.9, 0x1e1b26, 0, 0.75, 0); B(g, 0.9, 1.3, 0.15, 0xe0344a, 0, 1.5, -0.4); B(g, 0.5, 0.5, 0.17, 0x1e1b26, 0, 1.6, -0.39); C(g, 0.06, 0.06, 0.6, 0x3a3a44, 0, 0.4, 0); C(g, 0.4, 0.4, 0.06, 0x3a3a44, 0, 0.08, 0); }
  if (name === "cake") { C(g, 0.45, 0.45, 0.35, 0xf2a6bf, 0, 0.18, 0, 24); C(g, 0.47, 0.47, 0.06, 0xffffff, 0, 0.37, 0, 24); for (let i = 0; i < 4; i++) { C(g, 0.025, 0.025, 0.2, 0xffc23a, -0.2 + i * 0.13, 0.5, 0, 6); } }
  if (name === "cup") { C(g, 0.1, 0.08, 0.24, 0xf5f0e6, 0, 0.12, 0, 12); C(g, 0.105, 0.105, 0.04, 0x6b4630, 0, 0.26, 0, 12); }
  if (name === "tv") { B(g, 2.4, 1.4, 0.12, 0x1e1b26, 0, 1.6, 0); const s = new THREE.Mesh(new THREE.PlaneGeometry(2.2, 1.22), new THREE.MeshBasicMaterial({ color: 0x5ab0e0 })); s.position.set(0, 1.6, 0.065); g.add(s); B(g, 0.6, 0.06, 0.3, 0x1e1b26, 0, 0.85, 0); C(g, 0.04, 0.04, 0.8, 0x1e1b26, 0, 0.45, 0, 8); }
  if (name === "blender") { C(g, 0.18, 0.2, 0.2, 0xe0344a, 0, 0.1, 0); const j = new THREE.Mesh(new THREE.CylinderGeometry(0.17, 0.12, 0.45, 16), new THREE.MeshBasicMaterial({ color: 0xbfe6ff, transparent: true, opacity: 0.6 })); j.position.y = 0.42; g.add(j); C(g, 0.18, 0.18, 0.05, 0x1e1b26, 0, 0.66, 0); }
  if (name === "box") { B(g, 0.7, 0.45, 0.45, 0x1e1b26, 0, 0.23, 0); B(g, 0.72, 0.06, 0.47, 0xffc23a, 0, 0.47, 0, { outline: null }); }
  if (name === "bags") { for (const [x, c] of [[-0.3, 0xe0344a], [0.05, 0xffc23a], [0.38, 0x9a6edc]]) { B(g, 0.32, 0.42, 0.16, c, x, 0.21, 0); } }
  if (name === "mic") { C(g, 0.03, 0.03, 0.3, 0x2a2630, 0, 0, 0, 8); const h = mesh(new THREE.SphereGeometry(0.07, 12, 10), TOON(0x8a8496)); h.position.y = 0.18; g.add(h); }
  if (name === "table") { B(g, 2.4, 0.1, 1.2, 0xd9a66f, 0, 1.2, 0); for (const [x, z] of [[-1.1, -0.5], [1.1, -0.5], [-1.1, 0.5], [1.1, 0.5]]) B(g, 0.08, 1.2, 0.08, 0xb9884f, x, 0.6, z); }
  if (name === "stairs") { for (let i = 0; i < 6; i++) B(g, 2.2, 0.35, 0.6, 0xb98a63, 0, 0.17 + i * 0.35, -i * 0.6, { outline: 0x6e5a4a }); }
  if (name === "fridge") { B(g, 1.3, 2.6, 0.9, 0xf2eee6, 0, 1.3, 0); B(g, 0.06, 0.6, 0.05, 0xc8c1b4, 0.5, 1.9, 0.47, { outline: null }); }
  return g;
}
