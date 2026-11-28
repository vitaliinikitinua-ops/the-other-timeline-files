// Big cheap crowds (InstancedMesh: hoodie body + glossy black head) and a phone prop for hands.
import * as THREE from "three";
import { TOON, mesh } from "./toon.js";
const TOPS = [0xff6b5b, 0x4a7fc1, 0x3fa874, 0x9a6edc, 0xf2b84b, 0x38c6b4, 0xe86a9a, 0x7a8a9a, 0xd9734a, 0x5ab0e0];
export function crowd(scene, n, { x0, x1, z0, z1 }, seed = 7) {
  const g = new THREE.Group(); const r = (i, k) => (Math.sin(i * 127.1 + k * 311.7 + seed) * 43758.5453) % 1;
  const R = (i, k) => Math.abs(r(i, k));
  const bodyGeo = new THREE.CapsuleGeometry(0.42, 0.5, 6, 12); const headGeo = new THREE.SphereGeometry(0.62, 18, 12);
  const bodies = new THREE.InstancedMesh(bodyGeo, TOON(0xffffff), n), heads = new THREE.InstancedMesh(headGeo, TOON(0x1d1b23), n);
  const pos = []; const m = new THREE.Matrix4(), c = new THREE.Color();
  for (let i = 0; i < n; i++) { const x = x0 + R(i, 1) * (x1 - x0), z = z0 + R(i, 2) * (z1 - z0), s = 0.9 + R(i, 3) * 0.2; pos.push([x, z, s, R(i, 4) * 6]); bodies.setColorAt(i, c.setHex(TOPS[Math.floor(R(i, 5) * TOPS.length)])); }
  bodies.instanceColor.needsUpdate = true; g.add(bodies, heads);
  g.userData.update = (t) => { pos.forEach(([x, z, s, ph], i) => { const b = Math.abs(Math.sin(t * 4 + ph)) * 0.12;
    m.makeScale(s * 1.1, s, s * 0.75).setPosition(x, (0.95 + b) * s, z); bodies.setMatrixAt(i, m);
    m.makeScale(s, s, s).setPosition(x, (2.05 + b) * s, z); heads.setMatrixAt(i, m); });
    bodies.instanceMatrix.needsUpdate = heads.instanceMatrix.needsUpdate = true; };
  g.userData.update(0); return g;
}
export function phoneProp(ch) {
  const p = new THREE.Group(); const body = mesh(new THREE.BoxGeometry(0.2, 0.38, 0.04), TOON(0x1e1b26), { outline: 0x4a4656, w: 0.008 }); p.add(body);
  const scr = new THREE.Mesh(new THREE.PlaneGeometry(0.17, 0.33), new THREE.MeshBasicMaterial({ color: 0xbfe8ff })); scr.position.z = 0.022; p.add(scr);
  p.position.set(0, -0.05, 0.12); p.rotation.x = -0.3; ch.arms.R.grip.add(p); p.visible = false; return p;
}
