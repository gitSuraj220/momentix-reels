// Procedural low-poly models for the GTA 6 supercar reel (all original designs, no brands).
import * as THREE from 'three';
import {RoundedBoxGeometry} from 'three/addons/geometries/RoundedBoxGeometry.js';

export function rng(seed) { let a = seed >>> 0; return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }

const M = {
  pearl: () => new THREE.MeshPhysicalMaterial({color: 0xf6f2f7, roughness: 0.26, metalness: 0.15, clearcoat: 1, clearcoatRoughness: 0.05, iridescence: 0.45, iridescenceIOR: 1.5, sheen: 0.4, sheenColor: new THREE.Color(0xffc6f0), envMapIntensity: 1.3}),
  glass: () => new THREE.MeshPhysicalMaterial({color: 0x07070d, roughness: 0.04, metalness: 0.9, clearcoat: 1, envMapIntensity: 1.6}),
  black: () => new THREE.MeshStandardMaterial({color: 0x0b0b10, roughness: 0.5, metalness: 0.3}),
  rubber: () => new THREE.MeshStandardMaterial({color: 0x101014, roughness: 0.85}),
  rim: () => new THREE.MeshStandardMaterial({color: 0x2a2a33, roughness: 0.25, metalness: 0.95, envMapIntensity: 1.4}),
  emis: (c, i = 3) => new THREE.MeshStandardMaterial({color: c, emissive: c, emissiveIntensity: i, roughness: 0.4}),
};
export {M};

function extrudeProfile(pts, width, bevel = 0.06) {
  const sh = new THREE.Shape(); sh.moveTo(pts[0][0], pts[0][1]); for (const p of pts.slice(1)) sh.lineTo(p[0], p[1]); sh.closePath();
  const g = new THREE.ExtrudeGeometry(sh, {depth: width, bevelEnabled: true, bevelThickness: bevel, bevelSize: bevel, bevelSegments: 3, curveSegments: 6});
  g.translate(0, 0, -width / 2); return g;
}

function wheel(r = 0.36, w = 0.3, caliper = 0xff2d6a) {
  const g = new THREE.Group();
  const tire = new THREE.Mesh(new THREE.CylinderGeometry(r, r, w, 28), M.rubber()); tire.rotation.x = Math.PI / 2; g.add(tire);
  const rimM = M.rim();
  const disc = new THREE.Mesh(new THREE.CylinderGeometry(r * 0.72, r * 0.72, w + 0.02, 28), new THREE.MeshStandardMaterial({color: 0x07070a, roughness: 0.6})); disc.rotation.x = Math.PI / 2; g.add(disc);
  for (let k = 0; k < 5; k++) { const s = new THREE.Mesh(new THREE.BoxGeometry(0.07, r * 1.35, 0.04), rimM); s.rotation.z = k * Math.PI * 2 / 5; s.position.z = w / 2 + 0.01; g.add(s); const s2 = s.clone(); s2.position.z = -w / 2 - 0.01; g.add(s2); }
  const hub = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, w + 0.06, 12), rimM); hub.rotation.x = Math.PI / 2; g.add(hub);
  const cal = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.2, 0.05), M.emis(caliper, 1.2)); cal.position.set(0.16, 0.1, w / 2 - 0.02); g.add(cal);
  g.userData.spin = g; return g;
}

// Pearl-white wedge supercar. Length along +X (front at +X). Origin on ground, centre.
export function supercar() {
  const car = new THREE.Group(); const L = 4.5, Wd = 1.95;
  const body = new THREE.Mesh(extrudeProfile([[-2.25, 0.28], [2.2, 0.28], [2.32, 0.42], [2.2, 0.62], [1.2, 0.78], [0.6, 0.95], [-0.9, 1.08], [-1.8, 1.0], [-2.3, 0.92], [-2.35, 0.55]], Wd - 0.12), M.pearl());
  body.castShadow = true; car.add(body); car.userData.body = body;
  // cabin glass canopy
  const cab = new THREE.Mesh(extrudeProfile([[0.55, 0.9], [-0.15, 1.28], [-1.15, 1.3], [-1.75, 1.04], [-0.9, 0.98]], 1.42, 0.05), M.glass()); car.add(cab);
  // driver side window (breakable) on +Z side
  const winM = new THREE.MeshPhysicalMaterial({color: 0x15151f, roughness: 0.05, metalness: 0.6, transparent: true, opacity: 0.88, envMapIntensity: 2});
  const win = new THREE.Mesh(new THREE.ShapeGeometry((() => { const s = new THREE.Shape(); s.moveTo(0.45, 0.98); s.lineTo(-0.15, 1.26); s.lineTo(-1.05, 1.27); s.lineTo(-1.2, 1.02); s.closePath(); return s; })()), winM);
  win.position.z = 0.73; car.add(win); car.userData.win = win;
  // side intake + skirt
  const intake = new THREE.Mesh(new THREE.BoxGeometry(0.75, 0.32, 0.05), M.black()); intake.position.set(-1.25, 0.66, Wd / 2 - 0.02); car.add(intake);
  const intake2 = intake.clone(); intake2.position.z = -Wd / 2 + 0.02; car.add(intake2);
  const skirt = new THREE.Mesh(new THREE.BoxGeometry(3.4, 0.07, Wd + 0.02), M.black()); skirt.position.set(-0.05, 0.3, 0); car.add(skirt);
  // rear engine louvres
  for (let k = 0; k < 5; k++) { const l = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.02, 1.0), M.black()); l.position.set(-1.45 - k * 0.14, 1.06 - k * 0.012, 0); car.add(l); }
  // headlights (thin strips) + DRL
  const hl = M.emis(0xffffff, 6); const head = []; for (const z of [-0.62, 0.62]) { const h = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.05, 0.5), hl); h.position.set(2.22, 0.6, z); h.rotation.z = 0.35; car.add(h); head.push(h); }
  car.userData.headMat = hl;
  // tail light bar
  const tl = M.emis(0xff1744, 5); const tail = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.06, Wd - 0.2), tl); tail.position.set(-2.36, 0.8, 0); car.add(tail); car.userData.tailMat = tl;
  const diff = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.18, 1.4), M.black()); diff.position.set(-2.28, 0.36, 0); car.add(diff);
  // spoiler
  const sp = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.04, Wd - 0.1), M.pearl()); sp.position.set(-2.1, 1.12, 0); car.add(sp);
  // wheels
  car.userData.wheels = [];
  for (const [x, z] of [[1.42, Wd / 2 - 0.08], [1.42, -Wd / 2 + 0.08], [-1.45, Wd / 2 - 0.08], [-1.45, -Wd / 2 + 0.08]]) { const w = wheel(x > 0 ? 0.35 : 0.38, 0.3); w.position.set(x, x > 0 ? 0.35 : 0.38, z); if (z < 0) w.rotation.y = Math.PI; car.add(w); car.userData.wheels.push(w); }
  // interior: seat + steering hint seen through glass
  const seat = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.5, 0.5), new THREE.MeshStandardMaterial({color: 0x2a0d1a, roughness: 0.8})); seat.position.set(-0.75, 0.75, 0.35); car.add(seat);
  return car;
}

// Boxy 80s sedan (cream) — the "purani gaadi".
export function oldCar(color = 0xe6bf7e) {
  const car = new THREE.Group(); const paint = new THREE.MeshPhysicalMaterial({color, roughness: 0.45, metalness: 0.1, clearcoat: 0.4, envMapIntensity: 0.9});
  const lower = new THREE.Mesh(new RoundedBoxGeometry(4.6, 0.62, 1.85, 3, 0.08), paint); lower.position.y = 0.66; lower.castShadow = true; car.add(lower);
  const upper = new THREE.Mesh(new RoundedBoxGeometry(2.3, 0.6, 1.62, 3, 0.07), paint); upper.position.set(-0.25, 1.24, 0); car.add(upper);
  const g = M.glass(); for (const z of [0.82, -0.82]) { const w = new THREE.Mesh(new THREE.BoxGeometry(2.0, 0.42, 0.02), g); w.position.set(-0.25, 1.26, z); car.add(w); }
  const ws = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.45, 1.45), g); ws.position.set(0.91, 1.25, 0); ws.rotation.z = -0.35; car.add(ws);
  const chrome = new THREE.MeshStandardMaterial({color: 0xcfd3da, roughness: 0.15, metalness: 1, envMapIntensity: 1.5});
  for (const x of [2.32, -2.32]) { const b = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.16, 1.9), chrome); b.position.set(x, 0.48, 0); car.add(b); }
  const hl = M.emis(0xfff3c4, 5); for (const z of [0.6, -0.6]) { const h = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.13, 0.05, 20), hl); h.rotation.z = Math.PI / 2; h.position.set(2.31, 0.75, z); car.add(h); }
  car.userData.headMat = hl;
  const tl = M.emis(0xff3030, 3); for (const z of [0.65, -0.65]) { const t = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.16, 0.35), tl); t.position.set(-2.31, 0.78, z); car.add(t); }
  car.userData.wheels = [];
  for (const [x, z] of [[1.45, 0.86], [1.45, -0.86], [-1.45, 0.86], [-1.45, -0.86]]) { const w = wheel(0.34, 0.26, 0x333333); w.position.set(x, 0.34, z); if (z < 0) w.rotation.y = Math.PI; car.add(w); car.userData.wheels.push(w); }
  return car;
}

// Generic police cruiser (no real livery): two-tone + light bar.
export function policeCar() {
  const car = oldCar(0x1b2340); const white = new THREE.MeshPhysicalMaterial({color: 0xf2f2f2, roughness: 0.4, clearcoat: 0.5});
  const door = new THREE.Mesh(new THREE.BoxGeometry(1.8, 0.5, 1.88), white); door.position.set(0, 0.7, 0); car.add(door);
  const red = M.emis(0xff1a3d, 0), blue = M.emis(0x1a6dff, 0);
  const r = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.12, 0.6), red); r.position.set(-0.2, 1.6, 0.36); car.add(r);
  const b = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.12, 0.6), blue); b.position.set(-0.2, 1.6, -0.36); car.add(b);
  car.userData.bar = {red, blue}; return car;
}

// Momo: glass bulb head, gold screw neck, navy hoodie. Height ~1.35. Faces +X.
export function momo() {
  const g = new THREE.Group(); const navy = new THREE.MeshStandardMaterial({color: 0x1d2860, roughness: 0.92});
  const navyD = new THREE.MeshStandardMaterial({color: 0x161f4c, roughness: 0.95});
  const prof = []; for (let i = 0; i <= 24; i++) { const a = -Math.PI / 2 + Math.PI * i / 24; prof.push(new THREE.Vector2(Math.max(0.001, Math.cos(a) * 0.3), 0.3 + Math.sin(a) * 0.3)); }
  const lathe = [new THREE.Vector2(0.09, -0.16), new THREE.Vector2(0.11, -0.08), new THREE.Vector2(0.17, 0.02), ...prof.filter(p => p.y > 0.07)];
  const bulbM = new THREE.MeshPhysicalMaterial({color: 0xffd97a, emissive: 0xffb43c, emissiveIntensity: 0.55, roughness: 0.08, clearcoat: 1, clearcoatRoughness: 0.03, transparent: true, opacity: 0.96, envMapIntensity: 1.6});
  const head = new THREE.Group(); head.position.y = 1.0;
  const bulb = new THREE.Mesh(new THREE.LatheGeometry(lathe, 32), bulbM); bulb.position.y = 0.12; head.add(bulb);
  const inner = new THREE.Mesh(new THREE.SphereGeometry(0.17, 20, 16), new THREE.MeshBasicMaterial({color: 0xfff1b8, transparent: true, opacity: 0.55})); inner.position.y = 0.42; head.add(inner);
  const eyeM = new THREE.MeshStandardMaterial({color: 0x050505, roughness: 0.15, metalness: 0.2}); const hiM = new THREE.MeshBasicMaterial({color: 0xffffff});
  for (const z of [-0.09, 0.09]) { const e = new THREE.Mesh(new THREE.SphereGeometry(0.055, 16, 12), eyeM); e.scale.set(0.55, 1.15, 0.9); e.position.set(0.27, 0.44, z); head.add(e); const h = new THREE.Mesh(new THREE.SphereGeometry(0.013, 8, 6), hiM); h.position.set(0.3, 0.47, z + 0.01); head.add(h); }
  const gold = new THREE.MeshStandardMaterial({color: 0xd9a441, roughness: 0.25, metalness: 1, envMapIntensity: 1.5});
  const screwP = []; for (let i = 0; i <= 12; i++) screwP.push(new THREE.Vector2(0.1 + (i % 2 ? 0.012 : 0), -0.02 - i * 0.012));
  const screw = new THREE.Mesh(new THREE.LatheGeometry(screwP, 24), gold); screw.position.y = 0.0; head.add(screw);
  g.add(head); g.userData.head = head; g.userData.bulbM = bulbM;
  const torso = new THREE.Mesh(new THREE.CapsuleGeometry(0.24, 0.26, 6, 16), navy); torso.scale.set(1, 1, 0.8); torso.position.y = 0.66; g.add(torso);
  const hood = new THREE.Mesh(new THREE.TorusGeometry(0.15, 0.06, 10, 20), navyD); hood.rotation.x = Math.PI / 2; hood.position.y = 0.88; g.add(hood);
  const pocket = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.12, 0.3), navyD); pocket.position.set(0.2, 0.56, 0); g.add(pocket);
  const limb = (r, l) => new THREE.Mesh(new THREE.CapsuleGeometry(r, l, 4, 10), navy);
  const mkArm = (z) => { const sh = new THREE.Group(); sh.position.set(0, 0.84, z); const up = limb(0.075, 0.2); up.position.y = -0.14; sh.add(up); const el = new THREE.Group(); el.position.y = -0.28; sh.add(el); const lo = limb(0.07, 0.18); lo.position.y = -0.12; el.add(lo); const hand = new THREE.Mesh(new THREE.SphereGeometry(0.08, 14, 10), navyD); hand.position.y = -0.27; el.add(hand); g.add(sh); return {sh, el, hand}; };
  const armR = mkArm(0.3), armL = mkArm(-0.3);
  const mkLeg = (z) => { const hip = new THREE.Group(); hip.position.set(0, 0.42, z); const th = limb(0.09, 0.14); th.position.y = -0.1; hip.add(th); const kn = new THREE.Group(); kn.position.y = -0.2; hip.add(kn); const sh = limb(0.08, 0.1); sh.position.y = -0.08; kn.add(sh);
    const shoe = new THREE.Mesh(new RoundedBoxGeometry(0.26, 0.1, 0.14, 2, 0.04), new THREE.MeshStandardMaterial({color: 0xf4f4f4, roughness: 0.5})); shoe.position.set(0.05, -0.18, 0); kn.add(shoe);
    const stripe = new THREE.Mesh(new THREE.BoxGeometry(0.15, 0.03, 0.145), navyD); stripe.position.set(0.04, -0.15, 0); kn.add(stripe); g.add(hip); return {hip, kn}; };
  const legR = mkLeg(0.12), legL = mkLeg(-0.12);
  g.userData.rig = {armR, armL, legR, legL, torso};
  g.traverse(o => { if (o.isMesh) o.castShadow = true; });
  return g;
}
// pose: {armR:[shX,shZ,el], armL:[...], legs walk phase}
export function poseMomo(m, p) {
  const r = m.userData.rig; const s = (o, x = 0, z = 0) => { o.rotation.x = x; o.rotation.z = z; };
  s(r.armR.sh, p.rx || 0.15, p.rz || 0); r.armR.el.rotation.z = p.re || 0;
  s(r.armL.sh, p.lx || -0.15, p.lz || 0); r.armL.el.rotation.z = p.le || 0;
  const w = p.walk || 0; r.legR.hip.rotation.z = Math.sin(w) * 0.5; r.legL.hip.rotation.z = -Math.sin(w) * 0.5;
  r.legR.kn.rotation.z = -Math.max(0, Math.sin(w + 1.2)) * 0.6; r.legL.kn.rotation.z = -Math.max(0, -Math.sin(w + 1.2)) * 0.6;
  if (w) { r.armR.sh.rotation.z = -Math.sin(w) * 0.4; r.armL.sh.rotation.z = Math.sin(w) * 0.4; }
  m.userData.head.rotation.z = p.tilt || 0; m.userData.head.rotation.y = p.turn || 0;
}

// Palm tree
export function palm(seed = 1, h = 7) {
  const R = rng(seed); const g = new THREE.Group(); const bend = (R() - 0.5) * 1.6;
  const pts = []; for (let i = 0; i <= 8; i++) { const k = i / 8; pts.push(new THREE.Vector3(bend * k * k, k * h, 0)); }
  const curve = new THREE.CatmullRomCurve3(pts);
  const trunk = new THREE.Mesh(new THREE.TubeGeometry(curve, 24, 0.16, 8), new THREE.MeshStandardMaterial({color: 0x3a2a2e, roughness: 0.9})); g.add(trunk);
  const top = pts[8]; const leafM = new THREE.MeshStandardMaterial({color: 0x123a2c, roughness: 0.7, side: THREE.DoubleSide, emissive: 0x0b2a22, emissiveIntensity: 0.6});
  for (let k = 0; k < 9; k++) {
    const len = 2.4 + R() * 0.8; const geo = new THREE.PlaneGeometry(len, 0.5, 12, 1); const pos = geo.attributes.position;
    for (let i = 0; i < pos.count; i++) { const x = pos.getX(i) + len / 2; const y = pos.getY(i); pos.setXYZ(i, x, -0.35 * (x / len) ** 2 * len * 0.6 + y * 0.15, y * (1 - x / len) * 1.6); }
    geo.computeVertexNormals(); const leaf = new THREE.Mesh(geo, leafM); leaf.position.copy(top); leaf.rotation.y = k * Math.PI * 2 / 9 + R() * 0.3; leaf.rotation.z = -0.15 + R() * 0.3; g.add(leaf);
  }
  return g;
}

// Window texture for buildings
export function windowTex(seed, cols = 6, rows = 14, warm = 0.55) {
  const R = rng(seed); const c = document.createElement('canvas'); c.width = 256; c.height = 512; const x = c.getContext('2d');
  x.fillStyle = '#000'; x.fillRect(0, 0, 256, 512); const cw = 256 / cols, rh = 512 / rows;
  for (let i = 0; i < cols; i++) for (let j = 0; j < rows; j++) { const v = R(); if (v < 0.42) continue; x.fillStyle = v > 1 - warm * 0.5 ? '#ffcf8a' : v > 0.75 ? '#9fd8ff' : '#5b3b7a'; x.globalAlpha = 0.35 + R() * 0.65; x.fillRect(i * cw + cw * 0.22, j * rh + rh * 0.2, cw * 0.56, rh * 0.55); }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}
