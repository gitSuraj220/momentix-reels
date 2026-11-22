// Scenes: street world (neon night + palms + rain), cockpit/x-ray, top-down map, garage.
import * as THREE from 'three';
import {RoundedBoxGeometry} from 'three/addons/geometries/RoundedBoxGeometry.js';
import {supercar, oldCar, policeCar, momo, palm, windowTex, rng, M} from './models.js';

export function neonEnv(renderer) {
  const s = new THREE.Scene(); s.background = new THREE.Color(0x0c0818);
  const add = (c, w, h, x, y, z, ry = 0) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({color: c, side: THREE.DoubleSide})); m.position.set(x, y, z); m.rotation.y = ry; s.add(m); };
  add(0xff3fb4, 14, 1.2, 0, 6, -10); add(0x2ee6ff, 14, 1.0, 0, 4, 10, Math.PI); add(0x7a4dff, 1.2, 10, -10, 5, 0, Math.PI / 2); add(0xffc070, 1.5, 8, 10, 4, 3, -Math.PI / 2);
  add(0x3a2a66, 30, 30, 0, 12, 0); const sky = s.children.at(-1); sky.rotation.x = Math.PI / 2;
  add(0xfff0f8, 6, 0.5, 0, 9, 0); s.children.at(-1).rotation.x = Math.PI / 2;
  const pm = new THREE.PMREMGenerator(renderer); return pm.fromScene(s, 0.02).texture;
}

function skyDome(top = 0x14082e, mid = 0x4a1a6e, low = 0xff5fa8) {
  const g = new THREE.SphereGeometry(400, 32, 16); const m = new THREE.ShaderMaterial({side: THREE.BackSide, depthWrite: false, fog: false,
    uniforms: {a: {value: new THREE.Color(top)}, b: {value: new THREE.Color(mid)}, c: {value: new THREE.Color(low)}},
    vertexShader: 'varying vec3 p; void main(){p=normalize(position); gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',
    fragmentShader: 'uniform vec3 a,b,c; varying vec3 p; void main(){float h=p.y; vec3 col=mix(c,b,smoothstep(-0.02,0.18,h)); col=mix(col,a,smoothstep(0.18,0.6,h)); gl_FragColor=vec4(col,1.);}'});
  return new THREE.Mesh(g, m);
}

function glowTex(c1 = 'rgba(255,255,255,1)') { const c = document.createElement('canvas'); c.width = c.height = 128; const x = c.getContext('2d'); const g = x.createRadialGradient(64, 64, 0, 64, 64, 64); g.addColorStop(0, c1); g.addColorStop(1, 'rgba(0,0,0,0)'); x.fillStyle = g; x.fillRect(0, 0, 128, 128); return new THREE.CanvasTexture(c); }
const GLOW = {}; export function glow(color) { if (!GLOW.t) GLOW.t = glowTex(); return new THREE.MeshBasicMaterial({map: GLOW.t, color, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false}); }

// Rain: line segments in a box; deterministic in t.
export function rain(n = 2600, box = [40, 22, 40], seed = 7, color = 0xbfd0ff) {
  const R = rng(seed); const base = new Float32Array(n * 3); for (let i = 0; i < n; i++) { base[i * 3] = (R() - 0.5) * box[0]; base[i * 3 + 1] = R() * box[1]; base[i * 3 + 2] = (R() - 0.5) * box[2]; }
  const pos = new Float32Array(n * 6); const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  const mat = new THREE.LineBasicMaterial({color, transparent: true, opacity: 0.32, depthWrite: false});
  const obj = new THREE.LineSegments(geo, mat); obj.frustumCulled = false;
  obj.userData.update = (t, cx = 0, cz = 0, len = 0.55) => { for (let i = 0; i < n; i++) { const y = ((base[i * 3 + 1] - t * 16) % box[1] + box[1]) % box[1]; const x = base[i * 3] + cx - t * 1.2, z = base[i * 3 + 2] + cz;
    pos.set([x, y, z, x + 0.04, y + len, z], i * 6); } geo.attributes.position.needsUpdate = true; };
  return obj;
}

// ---------------- STREET WORLD ----------------
export function streetWorld(env) {
  const s = new THREE.Scene(); s.environment = env; s.background = new THREE.Color(0x1a0d33);
  s.fog = new THREE.FogExp2(0x2b1450, 0.022); s.add(skyDome());
  s.add(new THREE.HemisphereLight(0xb39cff, 0x3a1850, 1.35));
  const moonL = new THREE.DirectionalLight(0xb8c4ff, 0.6); moonL.position.set(-10, 20, 8); s.add(moonL);
  // road along X, sidewalks at z=±7
  const road = new THREE.Mesh(new THREE.PlaneGeometry(240, 14), new THREE.MeshStandardMaterial({color: 0x2a2236, roughness: 0.16, metalness: 0.5, envMapIntensity: 1.3}));
  road.rotation.x = -Math.PI / 2; s.add(road);
  const walkM = new THREE.MeshStandardMaterial({color: 0x2a2433, roughness: 0.4, metalness: 0.2});
  for (const z of [-9.5, 9.5]) { const w = new THREE.Mesh(new THREE.BoxGeometry(240, 0.25, 5), walkM); w.position.set(0, 0.12, z); s.add(w); }
  const dashM = new THREE.MeshStandardMaterial({color: 0xdedede, emissive: 0x777777, emissiveIntensity: 0.3});
  for (let x = -110; x < 110; x += 6) { const d = new THREE.Mesh(new THREE.BoxGeometry(2.6, 0.02, 0.18), dashM); d.position.set(x, 0.01, 0); s.add(d); }
  // buildings both sides
  const R = rng(42); const neonCols = [0x2ee6ff, 0xff3fb4, 0xffb347, 0x9b6bff];
  for (const side of [-1, 1]) for (let x = -100; x < 100; x += 9 + R() * 5) {
    const h = 10 + R() * 26, w = 7 + R() * 4, d = 8; const tex = windowTex(Math.floor(R() * 1e6), 5 + Math.floor(R() * 3), Math.floor(h / 1.4)); tex.repeat.set(1, 1);
    const b = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), new THREE.MeshStandardMaterial({color: 0x241a38, roughness: 0.75, emissive: 0xffffff, emissiveMap: tex, emissiveIntensity: 1.1}));
    b.position.set(x, h / 2, side * (13 + d / 2 + R() * 2)); s.add(b);
    if (R() < 0.7) { const c = neonCols[Math.floor(R() * 4)]; const vertical = R() < 0.4;
      const n = new THREE.Mesh(new THREE.BoxGeometry(vertical ? 0.25 : w * 0.8, vertical ? h * 0.5 : 0.25, 0.25), M.emis(c, 4)); n.position.set(x + (vertical ? (R() - 0.5) * w * 0.6 : 0), vertical ? h * 0.45 : 3 + R() * 6, side * 12.9); s.add(n);
      // fake wet-road reflection streak
      const st = new THREE.Mesh(new THREE.PlaneGeometry(vertical ? 0.9 : w * 0.6, 9), glow(c)); st.rotation.x = -Math.PI / 2; st.position.set(n.position.x, 0.02, side * 7.5); st.material.opacity = 0.55; s.add(st); }
  }
  // palms + street lamps along sidewalks
  for (const side of [-1, 1]) for (let x = -60; x < 60; x += 11) { const p = palm(Math.floor(x * 7 + side * 3 + 1000), 6.5 + ((x * 13) % 3)); p.position.set(x + side * 2, 0.25, side * 9.2); p.rotation.y = side * 0.6 + x; s.add(p); }
  const lampM = new THREE.MeshStandardMaterial({color: 0x222230, roughness: 0.5, metalness: 0.6});
  for (const side of [-1, 1]) for (let x = -54; x < 60; x += 22) { const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.1, 6, 8), lampM); pole.position.set(x, 3, side * 7.6); s.add(pole);
    const arm = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.1, 1.4), lampM); arm.position.set(x, 6, side * 7); s.add(arm);
    const head = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.12, 0.3), M.emis(0xffd9a8, 6)); head.position.set(x, 5.92, side * 6.4); s.add(head);
    const pool = new THREE.Mesh(new THREE.CircleGeometry(3.2, 32), glow(0xffc890)); pool.rotation.x = -Math.PI / 2; pool.position.set(x, 0.03, side * 6); pool.material.opacity = 0.55; s.add(pool); }
  // key lights around the hero spot (origin)
  const key = new THREE.SpotLight(0xff7ad0, 60, 45, 0.6, 0.55, 1.6); key.position.set(-6, 9, 6); key.target.position.set(0, 0.5, 0); s.add(key, key.target);
  const rim = new THREE.SpotLight(0x3ee8ff, 55, 45, 0.6, 0.55, 1.6); rim.position.set(7, 7, -6); rim.target.position.set(0, 0.5, 0); s.add(rim, rim.target);
  const fill = new THREE.PointLight(0xffd0a0, 6, 14, 1.5); fill.position.set(2, 4, 5); s.add(fill);
  const W = {scene: s, lights: {key, rim, fill}};
  W.car = supercar(); s.add(W.car);
  W.old = oldCar(); s.add(W.old); W.old.visible = false;
  W.momo = momo(); s.add(W.momo);
  W.rain = rain(); s.add(W.rain);
  // police (distant) for chase
  W.cops = [policeCar(), policeCar()]; W.cops.forEach(c => { s.add(c); c.visible = false; });
  W.copLights = [new THREE.PointLight(0xff1a3d, 0, 18, 1.4), new THREE.PointLight(0x1a6dff, 0, 18, 1.4)]; W.copLights.forEach(l => s.add(l));
  // glass shards (instanced)
  const R2 = rng(9); const n = 70; const sg = new THREE.InstancedMesh(new THREE.TetrahedronGeometry(0.05), new THREE.MeshStandardMaterial({color: 0xcfe6ff, roughness: 0.3, metalness: 0.0, emissive: 0x7fb6ff, emissiveIntensity: 1.2}), n);
  sg.userData.v = Array.from({length: n}, () => [R2() * 1.8 - 0.3, R2() * 2.2 + 0.4, R2() * 2.2 + 0.6, R2() * 6, R2() * 6, 0.6 + R2() * 1.1]); sg.frustumCulled = false; sg.visible = false; s.add(sg); W.shards = sg;
  const flash = new THREE.PointLight(0xbfe0ff, 0, 8, 1.2); s.add(flash); W.flash = flash;
  // outline (inverted hull) for Momo heat-system glow
  W.outline = new THREE.Group(); W.momo.traverse(o => { if (o.isMesh) { const om = new THREE.Mesh(o.geometry, new THREE.MeshBasicMaterial({color: 0x3d8bff, side: THREE.BackSide, transparent: true, opacity: 0})); om.userData.src = o; om.scale.setScalar(1.12); W.outline.add(om); } }); s.add(W.outline);
  W.syncOutline = (op) => { W.momo.updateMatrixWorld(true); W.outline.children.forEach(om => { const src = om.userData.src; src.matrixWorld.decompose(om.position, om.quaternion, om.scale); om.scale.multiplyScalar(1.09); om.material.opacity = op; }); };
  // tracker device on car underside (visible in x-ray)
  const tr = new THREE.Mesh(new RoundedBoxGeometry(0.4, 0.12, 0.28, 2, 0.03), M.emis(0x2f7bff, 2)); tr.position.set(-1.6, 0.36, 0.2); W.car.add(tr); tr.visible = false; W.tracker = tr;
  return W;
}

// ---------------- COCKPIT / X-RAY ----------------
export function cockpit(env) {
  const s = new THREE.Scene(); s.environment = env; s.background = new THREE.Color(0x07060c); s.fog = new THREE.Fog(0x07060c, 6, 16);
  s.add(new THREE.HemisphereLight(0x9a8cff, 0x241030, 1.3));
  const ck = new THREE.SpotLight(0xff8ad8, 30, 14, 0.7, 0.6, 1.4); ck.position.set(-2, 3.2, 3.5); ck.target.position.set(0.4, 0.2, 0.6); s.add(ck, ck.target);
  const ck2 = new THREE.SpotLight(0x4ee8ff, 22, 14, 0.7, 0.6, 1.4); ck2.position.set(3.5, 2.5, 2.5); ck2.target.position.set(0, 0.3, 0.6); s.add(ck2, ck2.target);
  const dashM = new THREE.MeshStandardMaterial({color: 0x2a2236, roughness: 0.5, metalness: 0.35});
  const dash = new THREE.Mesh(new RoundedBoxGeometry(5, 0.9, 1.6, 4, 0.25), dashM); dash.position.set(0, 0, 0); s.add(dash);
  const top = new THREE.Mesh(new RoundedBoxGeometry(5, 0.2, 2.2, 4, 0.1), new THREE.MeshStandardMaterial({color: 0x241a2c, roughness: 0.8})); top.position.set(0, 0.55, -0.4); s.add(top);
  const stitch = new THREE.Mesh(new THREE.BoxGeometry(5, 0.015, 0.02), M.emis(0xff3fb4, 2)); stitch.position.set(0, 0.46, 0.79); s.add(stitch);
  // steering wheel
  const sw = new THREE.Group(); const rimM = new THREE.MeshStandardMaterial({color: 0x101014, roughness: 0.4});
  const rimT = new THREE.Mesh(new THREE.TorusGeometry(0.62, 0.07, 14, 48), rimM); sw.add(rimT);
  for (const a of [0, 2.3, -2.3]) { const sp = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.6, 0.06), rimM); sp.position.set(Math.sin(a) * 0.3, -Math.cos(a) * 0.3, 0); sp.rotation.z = a; sw.add(sp); }
  sw.add(new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, 0.1, 20).rotateX(Math.PI / 2), rimM));
  sw.position.set(-1.1, 0.75, 1.3); sw.rotation.x = -0.35; s.add(sw);
  // start button with ring
  const btn = new THREE.Group(); btn.position.set(0.55, 0.2, 0.82);
  const cap = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 0.08, 40).rotateX(Math.PI / 2), new THREE.MeshStandardMaterial({color: 0xd9b27a, roughness: 0.3, metalness: 0.8})); btn.add(cap);
  const ringM = M.emis(0xffb347, 1.5); const ring = new THREE.Mesh(new THREE.TorusGeometry(0.29, 0.035, 12, 64), ringM); btn.add(ring);
  const sym = new THREE.Mesh(new THREE.TorusGeometry(0.08, 0.014, 8, 32, Math.PI * 1.6), M.emis(0xffffff, 1)); sym.rotation.z = Math.PI * 0.7; sym.position.z = 0.05; btn.add(sym);
  const symL = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.09, 0.01), M.emis(0xffffff, 1)); symL.position.set(0, 0.06, 0.05); btn.add(symL);
  s.add(btn);
  const btnLight = new THREE.PointLight(0xffb347, 2, 3, 1.5); btnLight.position.set(0.55, 0.3, 1.2); s.add(btnLight);
  // small screen
  const scrC = document.createElement('canvas'); scrC.width = 512; scrC.height = 200; const scrT = new THREE.CanvasTexture(scrC); scrT.colorSpace = THREE.SRGBColorSpace;
  const scr = new THREE.Mesh(new THREE.PlaneGeometry(1.1, 0.43), new THREE.MeshBasicMaterial({map: scrT})); scr.position.set(1.55, 0.3, 0.81); s.add(scr);
  const drawScr = (txt, col) => { const x = scrC.getContext('2d'); x.fillStyle = '#05050a'; x.fillRect(0, 0, 512, 200); x.fillStyle = col; x.font = '700 54px Poppins'; x.textAlign = 'center'; x.fillText(txt, 256, 120); scrT.needsUpdate = true; };
  // x-ray components (behind dash, revealed)
  const X = new THREE.Group(); X.visible = false; s.add(X);
  const grid = new THREE.GridHelper(12, 24, 0x5b4a8a, 0x2a2244); grid.position.y = -2.65; X.add(grid);
  const box = (w, h, d, c) => { const g = new THREE.Group(); const b = new THREE.Mesh(new RoundedBoxGeometry(w, h, d, 2, 0.05), new THREE.MeshStandardMaterial({color: 0x2c2c36, roughness: 0.45, metalness: 0.6})); g.add(b);
    for (let k = 0; k < 6; k++) { const f = new THREE.Mesh(new THREE.BoxGeometry(w * 0.85, 0.02, 0.04), new THREE.MeshStandardMaterial({color: 0x1a1a22})); f.position.set(0, h / 2, -d / 2 + 0.1 + k * (d - 0.2) / 5); g.add(f); }
    const led = new THREE.Mesh(new THREE.SphereGeometry(0.035, 10, 8), M.emis(c, 3)); led.position.set(w / 2 - 0.08, 0, d / 2 + 0.01); g.add(led); g.userData.led = led; return g; };
  const immo = box(0.7, 0.22, 0.5, 0xffb347); immo.position.set(0.95, -0.45, 0.45); X.add(immo);
  const ecu = box(0.9, 0.26, 0.6, 0xffb347); ecu.position.set(0.35, -1.2, 0.2); X.add(ecu);
  const eng = new THREE.Group(); const blk = new THREE.Mesh(new RoundedBoxGeometry(1.2, 0.7, 0.8, 3, 0.08), new THREE.MeshStandardMaterial({color: 0x3a3a44, roughness: 0.5, metalness: 0.7})); eng.add(blk);
  for (let k = 0; k < 4; k++) { const cyl = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, 0.25, 12), new THREE.MeshStandardMaterial({color: 0x55555f, metalness: 0.8, roughness: 0.3})); cyl.position.set(-0.4 + k * 0.27, 0.45, 0); eng.add(cyl); }
  eng.position.set(0.95, -2.2, -0.2); X.add(eng);
  const sparks = []; for (let k = 0; k < 4; k++) { const sp = new THREE.Mesh(new THREE.SphereGeometry(0.05, 8, 6), M.emis(0xffd54a, 0)); sp.position.set(-0.4 + k * 0.27, 0.6, 0); eng.add(sp); sparks.push(sp); }
  const wireM = new THREE.MeshStandardMaterial({color: 0x3a2f5c, roughness: 0.5, emissive: 0x2a1f55, emissiveIntensity: 0.8});
  const mkWire = (a, b, lift = 0.4) => { const c = new THREE.CatmullRomCurve3([a, a.clone().lerp(b, 0.5).add(new THREE.Vector3(0, lift, 0.2)), b]); X.add(new THREE.Mesh(new THREE.TubeGeometry(c, 40, 0.025, 8), wireM)); return c; };
  const wpos = v => { const p = new THREE.Vector3(); v.getWorldPosition(p); return p; };
  s.updateMatrixWorld(true);
  const w1 = mkWire(new THREE.Vector3(0.55, 0.2, 0.7), immo.position.clone(), 0.3), w2 = mkWire(immo.position.clone(), ecu.position.clone(), 0.2), w3 = mkWire(ecu.position.clone(), eng.position.clone().add(new THREE.Vector3(0, 0.3, 0)), 0.5);
  const pulses = [w1, w2, w3].map(c => { const m = new THREE.Mesh(new THREE.SphereGeometry(0.06, 10, 8), M.emis(0xffd54a, 4)); m.userData.c = c; X.add(m); return m; });
  // key fob
  const fob = new THREE.Group(); const fb = new THREE.Mesh(new RoundedBoxGeometry(0.45, 0.7, 0.12, 3, 0.08), new THREE.MeshStandardMaterial({color: 0xd8d8de, roughness: 0.35, metalness: 0.3})); fob.add(fb);
  const chip = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.14, 0.02), M.emis(0xffd54a, 1.5)); chip.position.set(0, -0.12, 0.07); fob.add(chip); fob.position.set(-0.4, 0.9, 1.4); fob.visible = false; s.add(fob);
  // Momo glove for pressing
  const glove = new THREE.Group(); const gm = new THREE.MeshStandardMaterial({color: 0x2f3f94, roughness: 0.8});
  const palmM = new THREE.Mesh(new THREE.SphereGeometry(0.17, 16, 12), gm); palmM.scale.set(1, 0.8, 1.2); glove.add(palmM);
  const fing = new THREE.Mesh(new THREE.CapsuleGeometry(0.05, 0.16, 4, 8), gm); fing.rotation.x = Math.PI / 2; fing.position.set(0, 0.02, -0.2); glove.add(fing);
  const sleeve = new THREE.Mesh(new THREE.CylinderGeometry(0.17, 0.2, 1.4, 16), gm); sleeve.rotation.x = Math.PI / 2; sleeve.position.set(0, 0, 0.8); glove.add(sleeve);
  s.add(glove);
  // phone (key cloner) for close-up
  const phone = new THREE.Group(); const ph = new THREE.Mesh(new RoundedBoxGeometry(0.5, 0.95, 0.06, 3, 0.06), new THREE.MeshStandardMaterial({color: 0x0c0c12, roughness: 0.3, metalness: 0.7})); phone.add(ph);
  const phC = document.createElement('canvas'); phC.width = 256; phC.height = 480; const phT = new THREE.CanvasTexture(phC); phT.colorSpace = THREE.SRGBColorSpace;
  const phS = new THREE.Mesh(new THREE.PlaneGeometry(0.44, 0.86), new THREE.MeshBasicMaterial({map: phT})); phS.position.z = 0.035; phone.add(phS); phone.visible = false; s.add(phone);
  const drawPhone = (k, ok) => { const x = phC.getContext('2d'); x.fillStyle = '#06060c'; x.fillRect(0, 0, 256, 480); x.strokeStyle = ok ? '#3dffb0' : '#ffb347'; x.lineWidth = 6;
    for (let r = 0; r < 3; r++) { x.globalAlpha = 0.3 + 0.7 * ((k * 3 + r) % 3 === 0 ? 1 : 0.4); x.beginPath(); x.arc(128, 200, 40 + r * 32, -Math.PI * 0.8, -Math.PI * 0.2); x.stroke(); }
    x.globalAlpha = 1; x.fillStyle = ok ? '#3dffb0' : '#ffb347'; x.font = '700 30px Poppins'; x.textAlign = 'center'; x.fillText(ok ? 'KEY CLONED' : 'SCANNING…', 128, 340);
    x.fillStyle = '#26263a'; x.fillRect(38, 380, 180, 14); x.fillStyle = ok ? '#3dffb0' : '#ffb347'; x.fillRect(38, 380, 180 * Math.min(1, k), 14); phT.needsUpdate = true; };
  return {scene: s, btn, ring, ringM, btnLight, drawScr, X, immo, ecu, eng, sparks, pulses, fob, chip, glove, phone, drawPhone, sw, dash};
}

// ---------------- TOP-DOWN MAP ----------------
export function mapWorld() {
  const s = new THREE.Scene(); s.background = new THREE.Color(0x0b0a1c);
  s.add(new THREE.HemisphereLight(0x8a7cff, 0x0a0818, 1.0));
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(200, 200), new THREE.MeshStandardMaterial({color: 0x15132a, roughness: 0.9})); ground.rotation.x = -Math.PI / 2; s.add(ground);
  const R = rng(77); const roadM = new THREE.MeshStandardMaterial({color: 0x24213d, roughness: 0.8});
  for (let k = -5; k <= 5; k++) { const a = new THREE.Mesh(new THREE.PlaneGeometry(200, 2.2), roadM); a.rotation.x = -Math.PI / 2; a.position.set(0, 0.01, k * 14); s.add(a);
    const b = new THREE.Mesh(new THREE.PlaneGeometry(2.2, 200), roadM); b.rotation.x = -Math.PI / 2; b.position.set(k * 14, 0.011, 0); s.add(b); }
  for (let i = -5; i < 5; i++) for (let j = -5; j < 5; j++) { const h = 1 + R() * 6; const tex = windowTex(i * 31 + j * 7 + 500, 4, 6, 0.4);
    const b = new THREE.Mesh(new THREE.BoxGeometry(10.5, h, 10.5), new THREE.MeshStandardMaterial({color: 0x2a2346, roughness: 0.7, emissive: 0xffffff, emissiveMap: tex, emissiveIntensity: 0.5})); b.position.set(i * 14 + 7, h / 2, j * 14 + 7); s.add(b); }
  const car = new THREE.Group(); const cb = new THREE.Mesh(new RoundedBoxGeometry(1.8, 0.5, 0.9, 2, 0.15), new THREE.MeshStandardMaterial({color: 0xf6f2f7, roughness: 0.3, emissive: 0x332a3a})); car.add(cb);
  const tl = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.1, 0.7), M.emis(0xff1744, 4)); tl.position.set(-0.92, 0.1, 0); car.add(tl); s.add(car);
  const rings = [0, 1, 2].map(() => { const r = new THREE.Mesh(new THREE.RingGeometry(0.9, 1.05, 48), new THREE.MeshBasicMaterial({color: 0x3d8bff, transparent: true, side: THREE.DoubleSide})); r.rotation.x = -Math.PI / 2; s.add(r); return r; });
  const cops = [0, 1, 2].map(i => { const d = new THREE.Mesh(new THREE.SphereGeometry(0.45, 12, 10), M.emis(i % 2 ? 0x1a6dff : 0xff1a3d, 3)); s.add(d); return d; });
  return {scene: s, car, rings, cops};
}

// ---------------- GARAGE ----------------
export function garage(env) {
  const s = new THREE.Scene(); s.environment = env; s.background = new THREE.Color(0x09080f); s.fog = new THREE.FogExp2(0x0d0b16, 0.03);
  s.add(new THREE.HemisphereLight(0x9aa2d0, 0x1a1428, 0.9));
  const gk = new THREE.SpotLight(0xffffff, 12, 30, 0.7, 0.5, 1.4); gk.position.set(4, 4, 5); gk.target.position.set(0, 0.5, 0); s.add(gk, gk.target);
  const gr = new THREE.SpotLight(0x7fd8ff, 8, 30, 0.6, 0.5, 1.4); gr.position.set(-5, 3.8, -3); gr.target.position.set(0, 0.6, 0); s.add(gr, gr.target);
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(80, 80), new THREE.MeshStandardMaterial({color: 0x34313c, roughness: 0.22, metalness: 0.35})); floor.rotation.x = -Math.PI / 2; s.add(floor);
  const ceil = new THREE.Mesh(new THREE.PlaneGeometry(80, 80), new THREE.MeshStandardMaterial({color: 0x15141b, roughness: 0.9})); ceil.rotation.x = Math.PI / 2; ceil.position.y = 4.2; s.add(ceil);
  const pilM = new THREE.MeshStandardMaterial({color: 0x3a3842, roughness: 0.85});
  for (let x = -24; x <= 24; x += 8) for (const z of [-5, 5]) { const p = new THREE.Mesh(new THREE.BoxGeometry(0.7, 4.2, 0.7), pilM); p.position.set(x, 2.1, z); s.add(p);
    const stripe = new THREE.Mesh(new THREE.BoxGeometry(0.72, 0.35, 0.72), new THREE.MeshStandardMaterial({color: 0xf2c230, roughness: 0.6})); stripe.position.set(x, 0.5, z); s.add(stripe); }
  for (let x = -24; x <= 24; x += 4) { const l = new THREE.Mesh(new THREE.BoxGeometry(1.8, 0.05, 0.18), M.emis(0xe8f0ff, 3)); l.position.set(x, 4.15, 0); s.add(l); }
  for (let x = -24; x <= 24; x += 3.2) for (const z of [-3, 3]) { const m = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.01, 2.2), new THREE.MeshBasicMaterial({color: 0xbfbfbf})); m.position.set(x, 0.01, z); s.add(m); }
  const signC = document.createElement('canvas'); signC.width = signC.height = 128; const sx = signC.getContext('2d'); sx.fillStyle = '#f4f4f4'; sx.fillRect(0, 0, 128, 128); sx.fillStyle = '#111'; sx.font = '900 100px Poppins'; sx.textAlign = 'center'; sx.fillText('P', 64, 104);
  const sign = new THREE.Mesh(new THREE.PlaneGeometry(0.8, 0.8), new THREE.MeshBasicMaterial({map: new THREE.CanvasTexture(signC)})); sign.position.set(-4, 3, -4.6); s.add(sign);
  const car = supercar(); s.add(car);
  const cops = [policeCar(), policeCar()]; cops.forEach(c => s.add(c));
  const red = new THREE.PointLight(0xff1a3d, 0, 30, 1.2), blue = new THREE.PointLight(0x1a6dff, 0, 30, 1.2); red.position.set(-6, 2.5, -1); blue.position.set(-6, 2.5, 1); s.add(red, blue);
  const ov = new THREE.PointLight(0xdfe8ff, 9, 14, 1.4); ov.position.set(0, 3.8, 0); s.add(ov);
  const r2 = rain(900, [30, 12, 6], 3); r2.position.set(0, 0, -9); s.add(r2);
  return {scene: s, car, cops, red, blue, rain: r2};
}
