// Dollhouse room built from the 3 sample photos (sizes in feet, estimated from the 7 ft door).
// Used by room.html (interactive tool) and reel.html (scripted demo). API: makeRoom(canvas, {width,height}).
import * as THREE from 'three';
import {RoundedBoxGeometry} from 'three/addons/geometries/RoundedBoxGeometry.js';

export const ROOM = {W: 11, D: 12, H: 10, door: {x0: 7.5, x1: 10.5, hingeX: 10.5, z: 12, r: 3}, window: {z0: 0.8, z1: 4.8, y0: 3, y1: 7}};
export const SIZES = [
  ['Darwaza (door)', '7 ft', 'pakka'], ['Ceiling', '≈ 10 ft', 'guess'], ['Peeche ki deewar', '≈ 11 ft', 'guess'],
  ['Side deewar', '≈ 12 ft', 'guess'], ['Khidki (window)', '≈ 4 ft', 'guess'], ['Bed (queen)', '5 × 6.5 ft', 'pakka']];
export const LAYOUTS = {
  A: {bed: [5.0, 3.35, 0], almirah: [9.4, 0.85, 0], table: [1.0, 2.8, Math.PI / 2], label: 'A · Bed beech mein'},
  B: {bed: [3.35, 7.4, Math.PI / 2], almirah: [9.4, 0.85, 0], table: [1.0, 2.8, Math.PI / 2], label: 'B · Bed deewar se lagao'},
  C: {bed: [8.4, 4.4, 0], almirah: [0.85, 8.2, Math.PI / 2], table: [1.0, 2.8, Math.PI / 2], label: 'C · Bed corner mein'},
};
export const WALLS = {white: 0xefe9dc, sage: 0xb5c7a4, peach: 0xf2c4a2, sky: 0xbfd6e8};

function tileTex() {
  const c = document.createElement('canvas'); c.width = c.height = 1024; const x = c.getContext('2d');
  x.fillStyle = '#d9d9d6'; x.fillRect(0, 0, 1024, 1024);
  for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) { const g = 210 + ((i * 7 + j * 13) % 5) * 4; x.fillStyle = `rgb(${g},${g},${g - 2})`; x.fillRect(i * 256 + 2, j * 256 + 2, 252, 252); }
  x.strokeStyle = '#bdbdb8'; x.lineWidth = 4; for (let k = 0; k <= 4; k++) { x.beginPath(); x.moveTo(k * 256, 0); x.lineTo(k * 256, 1024); x.stroke(); x.beginPath(); x.moveTo(0, k * 256); x.lineTo(1024, k * 256); x.stroke(); }
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(ROOM.W / 8, ROOM.D / 8); t.colorSpace = THREE.SRGBColorSpace; return t;
}
function floralTex() {
  const c = document.createElement('canvas'); c.width = c.height = 512; const x = c.getContext('2d'); x.fillStyle = '#8a2f4d'; x.fillRect(0, 0, 512, 512);
  let s = 3; const r = () => (s = (s * 16807) % 2147483647) / 2147483647;
  for (let i = 0; i < 26; i++) { const cx = r() * 512, cy = r() * 512, rr = 14 + r() * 18; x.fillStyle = 'rgba(240,190,180,.85)'; for (let p = 0; p < 5; p++) { const a = p / 5 * Math.PI * 2; x.beginPath(); x.ellipse(cx + Math.cos(a) * rr * .6, cy + Math.sin(a) * rr * .6, rr * .55, rr * .3, a, 0, 7); x.fill(); } x.fillStyle = '#c56a6a'; x.beginPath(); x.arc(cx, cy, rr * .2, 0, 7); x.fill(); }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; return t;
}
const std = (color, o = {}) => new THREE.MeshStandardMaterial({color, roughness: 0.7, ...o});
const box = (w, h, d, m, r = 0.06) => { const g = r ? new RoundedBoxGeometry(w, h, d, 2, Math.min(r, w / 2, h / 2, d / 2)) : new THREE.BoxGeometry(w, h, d); const o = new THREE.Mesh(g, m); o.castShadow = o.receiveShadow = true; return o; };

function bed() {
  const g = new THREE.Group(), wood = std(0x7a4a26, {roughness: 0.55});
  const frame = box(5.2, 1.2, 6.7, wood); frame.position.y = 0.6; g.add(frame);
  const mat = box(5, 0.7, 6.4, std(0xffffff, {map: floralTex(), roughness: 0.9}), 0.25); mat.position.set(0, 1.5, 0.12); g.add(mat);
  const head = box(5.2, 3.2, 0.35, wood); head.position.set(0, 1.6, -3.25); g.add(head);
  for (const sx of [-1.25, 1.25]) { const p = box(1.9, 0.45, 1.1, std(0x93324f, {roughness: 0.9}), 0.2); p.position.set(sx, 2.05, -2.45); g.add(p); }
  g.userData = {w: 5.2, d: 6.7, name: 'bed'}; return g;
}
function almirah() {
  const g = new THREE.Group(), m = std(0x8b9196, {metalness: 0.45, roughness: 0.4});
  const b = box(3, 6.5, 1.6, m, 0.04); b.position.y = 3.35; g.add(b);
  const line = box(0.03, 6.2, 0.02, std(0x555b60), 0); line.position.set(0, 3.35, 0.81); g.add(line);
  const h = box(0.35, 0.06, 0.08, std(0xdddddd, {metalness: 0.9, roughness: 0.2}), 0); h.position.set(0.25, 3.6, 0.85); g.add(h);
  const bag = box(1.6, 0.45, 1.0, std(0x8e3c6a), 0.1); bag.position.set(-0.4, 6.85, 0); g.add(bag);
  g.userData = {w: 3, d: 1.6, name: 'almirah'}; return g;
}
function table() {
  const g = new THREE.Group(), wood = std(0x6e4424, {roughness: 0.6});
  const top = box(3.5, 0.15, 2, wood, 0.03); top.position.y = 2.5; g.add(top);
  for (const [x, z] of [[-1.6, -0.85], [1.6, -0.85], [-1.6, 0.85], [1.6, 0.85]]) { const l = box(0.15, 2.45, 0.15, wood, 0); l.position.set(x, 1.22, z); g.add(l); }
  const dr = box(1.4, 0.4, 1.8, wood, 0.03); dr.position.set(-0.8, 2.2, 0); g.add(dr);
  const cols = [0x2f6dd9, 0xc73e3e, 0xe0a83a, 0x1d6b48]; cols.forEach((c, i) => { const bk = box(0.22, 0.9, 0.7, std(c), 0.02); bk.position.set(-1.4 + i * 0.25, 3.03, -0.4); g.add(bk); });
  const lap = box(1.1, 0.06, 0.8, std(0x222222, {metalness: 0.5}), 0.02); lap.position.set(0.7, 2.62, 0.2); g.add(lap);
  const chair = new THREE.Group(); const seat = box(1.4, 0.15, 1.4, wood, 0.03); seat.position.y = 1.5; chair.add(seat);
  const back = box(1.4, 1.8, 0.12, wood, 0.03); back.position.set(0, 2.4, 0.65); chair.add(back);
  for (const [x, z] of [[-.6, -.6], [.6, -.6], [-.6, .6], [.6, .6]]) { const l = box(0.12, 1.5, 0.12, wood, 0); l.position.set(x, 0.75, z); chair.add(l); }
  chair.position.set(0, 0, 1.55); g.add(chair);
  g.userData = {w: 3.5, d: 2, name: 'table'}; return g;
}
function sofa() {
  const g = new THREE.Group(), fab = std(0x5f7d9e, {roughness: 0.95});
  const base = box(7, 1.4, 3, fab, 0.25); base.position.y = 0.95; g.add(base);
  const back = box(7, 1.6, 0.7, fab, 0.3); back.position.set(0, 2.2, 1.15); g.add(back);
  for (const x of [-3.2, 3.2]) { const a = box(0.6, 1.0, 3, fab, 0.25); a.position.set(x, 1.9, 0); g.add(a); }
  for (const x of [-1.75, 1.75]) { const c = box(3.2, 0.45, 2.2, std(0x6f8db0, {roughness: 0.95}), 0.2); c.position.set(x, 1.85, -0.2); g.add(c); }
  for (const x of [-3.2, 3.2]) for (const z of [-1.2, 1.2]) { const l = box(0.2, 0.25, 0.2, std(0x3a2a1a), 0); l.position.set(x, 0.12, z); g.add(l); }
  g.userData = {w: 7, d: 3, name: 'sofa'}; return g;
}

export function makeRoom(canvas, opt = {}) {
  const W = opt.width || canvas.width, H = opt.height || canvas.height;
  const renderer = new THREE.WebGLRenderer({canvas, antialias: true, alpha: true, preserveDrawingBuffer: true});
  renderer.setSize(W, H, false); renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.outputColorSpace = THREE.SRGBColorSpace; renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
  const scene = new THREE.Scene();
  const aspect = W / H, vs = opt.viewSize || 19;
  const cam = new THREE.OrthographicCamera(-vs * aspect / 2, vs * aspect / 2, vs / 2, -vs / 2, -100, 200);
  const target = new THREE.Vector3(ROOM.W / 2, 2.6, ROOM.D / 2);
  let az = Math.PI / 4, el = 0.62; const setCam = () => { const r = 60; cam.position.set(target.x + r * Math.cos(el) * Math.sin(az), target.y + r * Math.sin(el), target.z + r * Math.cos(el) * Math.cos(az)); cam.lookAt(target); cam.updateProjectionMatrix(); }; setCam();
  scene.add(new THREE.HemisphereLight(0xfff6ea, 0x9a8f80, 1.3));
  const sun = new THREE.DirectionalLight(0xfff1dc, 2.2); sun.position.set(24, 30, 18); sun.target.position.copy(target); sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048); Object.assign(sun.shadow.camera, {left: -14, right: 14, top: 14, bottom: -14, near: 1, far: 90}); sun.shadow.bias = -0.0004; sun.shadow.radius = 4; scene.add(sun, sun.target);
  const winLight = new THREE.PointLight(0xfff3d6, 18, 14, 1.6); winLight.position.set(1.2, 5.5, 2.8); scene.add(winLight);
  // base + floor
  const base = box(ROOM.W + 0.8, 0.6, ROOM.D + 0.8, std(0x2b2f2e, {roughness: 0.9}), 0.1); base.position.set(ROOM.W / 2, -0.3, ROOM.D / 2); scene.add(base);
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(ROOM.W, ROOM.D), std(0xffffff, {map: tileTex(), roughness: 0.25, metalness: 0.05})); floor.rotation.x = -Math.PI / 2; floor.position.set(ROOM.W / 2, 0.01, ROOM.D / 2); floor.receiveShadow = true; scene.add(floor);
  // walls
  const wallM = std(WALLS.white, {roughness: 0.92}); const T = 0.4;
  const north = box(ROOM.W + T, ROOM.H, T, wallM, 0); north.position.set(ROOM.W / 2 - T / 2, ROOM.H / 2, -T / 2); scene.add(north);
  const wz = ROOM.window, west = new THREE.Group(); scene.add(west);
  const wseg = (z0, z1, y0, y1) => { const s = box(T, y1 - y0, z1 - z0, wallM, 0); s.position.set(-T / 2, (y0 + y1) / 2, (z0 + z1) / 2); west.add(s); };
  wseg(-T, wz.z0, 0, ROOM.H); wseg(wz.z1, ROOM.D, 0, ROOM.H); wseg(wz.z0, wz.z1, 0, wz.y0); wseg(wz.z0, wz.z1, wz.y1, ROOM.H);
  const glass = new THREE.Mesh(new THREE.PlaneGeometry(wz.z1 - wz.z0, wz.y1 - wz.y0), new THREE.MeshBasicMaterial({color: 0xcfe8c4})); glass.rotation.y = Math.PI / 2; glass.position.set(-T + 0.02, (wz.y0 + wz.y1) / 2, (wz.z0 + wz.z1) / 2); scene.add(glass);
  for (let k = 1; k < 6; k++) { const bar = box(0.05, wz.y1 - wz.y0, 0.05, std(0x9a9a9a, {metalness: 0.6}), 0); bar.position.set(-0.05, (wz.y0 + wz.y1) / 2, wz.z0 + (wz.z1 - wz.z0) * k / 6); scene.add(bar); }
  const frameM = std(0xf4f4f0); for (const [w, h, y, z] of [[0.12, 4.3, 5, wz.z0], [0.12, 4.3, 5, wz.z1], [0.12, 0.12, wz.y0, (wz.z0 + wz.z1) / 2], [0.12, 0.12, wz.y1, (wz.z0 + wz.z1) / 2]]) { const f = box(0.12, h === 0.12 ? 0.12 : h, h === 0.12 ? wz.z1 - wz.z0 : 0.12, frameM, 0); f.position.set(0.02, y, z); scene.add(f); }
  for (const z of [wz.z0 - 0.35, wz.z1 + 0.35]) { const c = box(0.15, 4.8, 1.1, std(0xf0a05e, {roughness: 0.95}), 0.05); c.position.set(0.25, 4.95, z); scene.add(c); }
  const rod = box(0.06, 0.06, wz.z1 - wz.z0 + 2.4, std(0xaaaaaa, {metalness: 0.8}), 0); rod.position.set(0.25, 7.45, (wz.z0 + wz.z1) / 2); scene.add(rod);
  // tube light + calendar on north wall, curbs on open sides
  const tube = box(4, 0.18, 0.18, new THREE.MeshStandardMaterial({color: 0xffffff, emissive: 0xffffff, emissiveIntensity: 1.2}), 0.06); tube.position.set(5.2, 8.2, 0.15); scene.add(tube);
  const cal = new THREE.Mesh(new THREE.PlaneGeometry(1.1, 1.6), std(0xf6f2ea)); cal.position.set(8.9, 5.6, 0.02); scene.add(cal);
  const calTop = new THREE.Mesh(new THREE.PlaneGeometry(1.1, 0.6), std(0x3f8fd0)); calTop.position.set(8.9, 6.1, 0.03); scene.add(calTop);
  const curbM = std(0xe4ddcf, {roughness: 0.9});
  const cs = box(ROOM.door.x0 + T, 0.5, T, curbM, 0); cs.position.set((ROOM.door.x0 - T) / 2, 0.25, ROOM.D + T / 2); scene.add(cs);
  const cs2 = box(ROOM.W - ROOM.door.x1, 0.5, T, curbM, 0); cs2.position.set((ROOM.W + ROOM.door.x1) / 2, 0.25, ROOM.D + T / 2); scene.add(cs2);
  const ce = box(T, 0.5, ROOM.D + T, curbM, 0); ce.position.set(ROOM.W + T / 2, 0.25, ROOM.D / 2); scene.add(ce);
  // door swing (floor arc) + door leaf (thin, open)
  const arcG = new THREE.RingGeometry(ROOM.door.r - 0.06, ROOM.door.r, 48, 1, Math.PI / 2, Math.PI / 2);
  const arcM = new THREE.MeshBasicMaterial({color: 0x8a6a4a, transparent: true, opacity: 0.6, side: THREE.DoubleSide}); const arc = new THREE.Mesh(arcG, arcM);
  arc.rotation.x = -Math.PI / 2; arc.position.set(ROOM.door.hingeX, 0.03, ROOM.door.z); scene.add(arc);
  const sweep = new THREE.Mesh(new THREE.CircleGeometry(ROOM.door.r, 48, Math.PI / 2, Math.PI / 2), new THREE.MeshBasicMaterial({color: 0xff4d5e, transparent: true, opacity: 0, side: THREE.DoubleSide, depthWrite: false}));
  sweep.rotation.x = -Math.PI / 2; sweep.position.set(ROOM.door.hingeX, 0.025, ROOM.door.z); scene.add(sweep);
  const leaf = box(0.15, 1.0, ROOM.door.r, std(0x9a5a2e), 0.02); leaf.position.set(ROOM.door.hingeX - 0.1, 0.5, ROOM.D - ROOM.door.r / 2); scene.add(leaf);
  // furniture
  const items = {bed: bed(), almirah: almirah(), table: table(), sofa: sofa()};
  for (const k in items) scene.add(items[k]);
  items.sofa.visible = false;
  const ring = new THREE.Mesh(new THREE.RingGeometry(0.97, 1.0, 64), new THREE.MeshBasicMaterial({color: 0x3d8bff, transparent: true, opacity: 0.9, side: THREE.DoubleSide})); ring.rotation.x = -Math.PI / 2; ring.position.y = 0.04; ring.visible = false; scene.add(ring);
  const outline = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(1, 1, 1)), new THREE.LineBasicMaterial({color: 0x3ddc84})); outline.visible = false; scene.add(outline);
  const place = (k, x, z, rot) => { const o = items[k]; o.position.set(x, 0, z); o.rotation.y = rot; };
  const setLayout = (L) => { for (const k of ['bed', 'almirah', 'table']) place(k, ...LAYOUTS[L][k]); };
  setLayout('A'); place('sofa', 5.0, 10.4, 0);
  // footprint rect (axis aligned, rotations are multiples of 90°)
  const rect = (k) => { const o = items[k], u = o.userData; const q = Math.abs(Math.round(o.rotation.y / (Math.PI / 2))) % 2; const w = q ? u.d : u.w, d = q ? u.w : u.d; return {x0: o.position.x - w / 2, x1: o.position.x + w / 2, z0: o.position.z - d / 2, z1: o.position.z + d / 2}; };
  function fitCheck(k = 'sofa') {
    const r = rect(k); const walls = r.x0 >= -0.01 && r.x1 <= ROOM.W + 0.01 && r.z0 >= -0.01 && r.z1 <= ROOM.D + 0.01;
    const D = ROOM.door; const cx = Math.max(r.x0, Math.min(D.hingeX, r.x1)), cz = Math.max(r.z0, Math.min(D.z, r.z1)); const inQuad = (x, z) => x <= D.hingeX && z <= D.z && Math.hypot(x - D.hingeX, z - D.z) < D.r;
    const door = !(inQuad(cx, cz) || (r.x1 > D.x0 && r.x0 < D.hingeX && r.z1 > D.z - D.r));
    let gap = 99; for (const o of ['bed', 'almirah', 'table']) { const q = rect(o); const dx = Math.max(0, q.x0 - r.x1, r.x0 - q.x1), dz = Math.max(0, q.z0 - r.z1, r.z0 - q.z1); gap = Math.min(gap, Math.max(dx, dz)); }
    return {walls, door, space: gap >= 2, gap};
  }
  const v = new THREE.Vector3();
  const project = (x, y, z) => { v.set(x, y, z).project(cam); return {x: (v.x + 1) / 2 * W, y: (1 - v.y) / 2 * H}; };
  const api = {
    renderer, scene, cam, items, place, setLayout, fitCheck, rect, project, ROOM,
    setWall(hex) { wallM.color.setHex(hex); },
    setWallMix(a, b, k) { wallM.color.setHex(a).lerp(new THREE.Color(b), k); },
    select(k, on = true) { if (!on || !k) { ring.visible = false; return; } const r = rect(k); ring.visible = true; ring.position.x = (r.x0 + r.x1) / 2; ring.position.z = (r.z0 + r.z1) / 2; const s = Math.max(r.x1 - r.x0, r.z1 - r.z0) * 0.62; ring.scale.set(s, s, 1); },
    outlineOn(k, color, on = true) { if (!on) { outline.visible = false; return; } const r = rect(k); outline.visible = true; outline.material.color.setHex(color); outline.position.set((r.x0 + r.x1) / 2, 1.6, (r.z0 + r.z1) / 2); outline.scale.set(r.x1 - r.x0 + 0.1, 3.2, r.z1 - r.z0 + 0.1); },
    doorWarn(k) { sweep.material.opacity = 0.45 * k; arcM.color.setHex(k > 0.1 ? 0xff4d5e : 0x8a6a4a); },
    orbit(a, e) { az = a; if (e !== undefined) el = e; setCam(); },
    zoom(s, tx, tz) { cam.zoom = s; if (tx !== undefined) { target.x = tx; target.z = tz; } setCam(); },
    render() { renderer.render(scene, cam); },
  };
  // interactive drag / rotate (room.html)
  if (opt.interactive) {
    const rc = new THREE.Raycaster(), m = new THREE.Vector2(), plane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0), hit = new THREE.Vector3(); let sel = null, drag = false, off = new THREE.Vector3();
    const pick = (e) => { const b = canvas.getBoundingClientRect(); m.set((e.clientX - b.left) / b.width * 2 - 1, -((e.clientY - b.top) / b.height) * 2 + 1); rc.setFromCamera(m, cam); };
    canvas.addEventListener('pointerdown', (e) => { pick(e); const hits = rc.intersectObjects(Object.values(items).filter(o => o.visible), true); if (!hits.length) { sel = null; api.select(null, false); api.render(); return; }
      let o = hits[0].object; while (o.parent && !o.userData.name) o = o.parent; sel = o.userData.name; drag = true; rc.ray.intersectPlane(plane, hit); off.copy(items[sel].position).sub(hit); api.select(sel); api.render(); opt.onSelect && opt.onSelect(sel); });
    canvas.addEventListener('pointermove', (e) => { if (!drag || !sel) return; pick(e); rc.ray.intersectPlane(plane, hit); const p = hit.add(off); const o = items[sel]; o.position.x = Math.round(Math.max(0, Math.min(ROOM.W, p.x)) * 4) / 4; o.position.z = Math.round(Math.max(0, Math.min(ROOM.D, p.z)) * 4) / 4; api.select(sel); api.render(); opt.onMove && opt.onMove(sel); });
    window.addEventListener('pointerup', () => { drag = false; });
    api.rotateSelected = () => { if (!sel) return; items[sel].rotation.y += Math.PI / 2; api.select(sel); api.render(); opt.onMove && opt.onMove(sel); };
    window.addEventListener('keydown', (e) => { if (e.key === 'r' || e.key === 'R') api.rotateSelected(); });
  }
  return api;
}
