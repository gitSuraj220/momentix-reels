// Night-before-exam study room: Momo at a desk, giant floating phone, keycaps, textbook, answer sheet, clock, rainy window -> sunrise.
import * as THREE from 'three';
import {RoundedBoxGeometry} from 'three/addons/geometries/RoundedBoxGeometry.js';
import {momo, rng, M} from './models.js';

export function roomEnv(renderer) {
  const s = new THREE.Scene(); s.background = new THREE.Color(0x0a0c18);
  const add = (c, w, h, x, y, z, ry = 0, rx = 0) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({color: c, side: THREE.DoubleSide})); m.position.set(x, y, z); m.rotation.set(rx, ry, 0); s.add(m); };
  add(0xffc27a, 4, 3, 0, 3, -8); add(0x6fb7ff, 6, 2, 0, 3, 8, Math.PI); add(0x2a3a7a, 2, 8, -8, 3, 0, Math.PI / 2); add(0xfff0dc, 3, 3, 8, 4, 0, -Math.PI / 2);
  add(0x1c2240, 20, 20, 0, 9, 0, 0, Math.PI / 2);
  const pm = new THREE.PMREMGenerator(renderer); return pm.fromScene(s, 0.03).texture;
}

function glowTex() { const c = document.createElement('canvas'); c.width = c.height = 128; const x = c.getContext('2d'); const g = x.createRadialGradient(64, 64, 0, 64, 64, 64); g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(0.35, 'rgba(255,255,255,.35)'); g.addColorStop(1, 'rgba(0,0,0,0)'); x.fillStyle = g; x.fillRect(0, 0, 128, 128); return new THREE.CanvasTexture(c); }
let GT; export function glow(color, op = 1) { GT = GT || glowTex(); return new THREE.MeshBasicMaterial({map: GT, color, transparent: true, opacity: op, blending: THREE.AdditiveBlending, depthWrite: false}); }

// ---- Momo with a face (mouth / brows / sweat) ----
export function faceMomo() {
  const m = momo(); const head = m.userData.head; const ink = new THREE.MeshBasicMaterial({color: 0x120a02});
  const arc = (flip) => { const g = new THREE.TorusGeometry(0.045, 0.009, 8, 20, Math.PI); const o = new THREE.Mesh(g, ink); o.rotation.set(0, Math.PI / 2, flip ? Math.PI : 0); o.position.set(0.292, flip ? 0.345 : 0.305, 0); head.add(o); return o; };
  const smile = arc(true), frown = arc(false);
  const oh = new THREE.Mesh(new THREE.TorusGeometry(0.026, 0.009, 8, 16), ink); oh.rotation.y = Math.PI / 2; oh.position.set(0.292, 0.32, 0); head.add(oh);
  const brows = [-1, 1].map(s => { const b = new THREE.Mesh(new THREE.BoxGeometry(0.012, 0.014, 0.075), ink); b.position.set(0.275, 0.535, s * 0.09); head.add(b); return b; });
  const sweat = new THREE.Mesh(new THREE.SphereGeometry(0.03, 12, 10), new THREE.MeshPhysicalMaterial({color: 0x9fdcff, roughness: 0.05, transmission: 0.2, emissive: 0x4fb4ff, emissiveIntensity: 0.6})); sweat.scale.set(0.8, 1.3, 0.8); head.add(sweat);
  m.userData.face = {smile, frown, oh, brows, sweat};
  return m;
}
// mood: 'stress' | 'worry' | 'neutral' | 'happy' | 'wow' ; k = blend for brow lift
export function setFace(m, mood, t = 0) {
  const f = m.userData.face; f.smile.visible = mood === 'happy'; f.frown.visible = mood === 'stress' || mood === 'worry'; f.oh.visible = mood === 'wow';
  if (mood === 'neutral') { f.frown.visible = false; f.smile.visible = true; f.smile.scale.set(1, 0.45, 1); } else f.smile.scale.set(1, 1, 1);
  const inner = mood === 'stress' || mood === 'worry' ? 0.5 : mood === 'wow' ? -0.0 : mood === 'happy' ? -0.15 : 0;
  f.brows.forEach((b, i) => { const s = i ? 1 : -1; b.rotation.x = s * inner; b.position.y = 0.535 + (mood === 'wow' ? 0.035 : mood === 'happy' ? 0.02 : 0); });
  f.sweat.visible = mood === 'stress'; if (f.sweat.visible) { const u = (t * 0.9) % 1; f.sweat.position.set(0.18, 0.62 - u * 0.22, 0.22); f.sweat.material.opacity = 1; }
}
export function seatMomo(m) { const r = m.userData.rig; for (const L of [r.legR, r.legL]) { L.hip.rotation.z = Math.PI / 2 - 0.05; L.kn.rotation.z = -Math.PI / 2 + 0.05; } }

// ---- canvas-textured screen ----
export function phone() {
  const g = new THREE.Group(); const W = 0.92, H = 1.96;
  const body = new THREE.Mesh(new RoundedBoxGeometry(W + 0.06, H + 0.06, 0.07, 4, 0.06), new THREE.MeshPhysicalMaterial({color: 0x15161c, roughness: 0.25, metalness: 0.85, clearcoat: 1, envMapIntensity: 1.4}));
  g.add(body);
  const rim = new THREE.Mesh(new RoundedBoxGeometry(W + 0.075, H + 0.075, 0.05, 4, 0.065), new THREE.MeshStandardMaterial({color: 0x8a8fa0, roughness: 0.2, metalness: 1, envMapIntensity: 1.6})); rim.position.z = -0.005; g.add(rim);
  const cv = document.createElement('canvas'); cv.width = 900; cv.height = 1918; const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
  const scr = new THREE.Mesh(new THREE.PlaneGeometry(W, H), new THREE.MeshBasicMaterial({map: tex, toneMapped: false})); scr.position.z = 0.037; g.add(scr);
  const cam = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 0.02, 20), new THREE.MeshStandardMaterial({color: 0x050507, roughness: 0.1, metalness: 0.5})); cam.rotation.x = Math.PI / 2; cam.position.set(-0.28, 0.82, -0.045); g.add(cam);
  const halo = new THREE.Mesh(new THREE.PlaneGeometry(W * 2.4, H * 1.7), glow(0x8fb4ff, 0.35)); halo.position.z = -0.08; g.add(halo);
  g.userData = {cv, ctx: cv.getContext('2d'), tex, scr, halo, W, H};
  return g;
}

// ---- keycaps ----
function capTex(ch, gold, w = 1) {
  const c = document.createElement('canvas'); c.width = Math.round(256 * w); c.height = 256; const x = c.getContext('2d');
  const gr = x.createLinearGradient(0, 0, 0, 256); gr.addColorStop(0, gold ? '#ffe7a3' : '#f4f5fa'); gr.addColorStop(1, gold ? '#f0b53a' : '#d9dbe6'); x.fillStyle = gr; x.fillRect(0, 0, c.width, 256);
  x.fillStyle = gold ? '#3a2200' : '#15161f'; x.font = `800 ${ch.length > 1 ? 130 : 170}px P`; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(ch, c.width / 2, 140);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
}
export function keycap(ch, gold = false, w = 1) {
  const g = new THREE.Group(); const S = 0.16;
  const capM = new THREE.MeshPhysicalMaterial({color: gold ? 0xf3c04a : 0xeef0f6, roughness: gold ? 0.25 : 0.38, metalness: gold ? 0.55 : 0.0, clearcoat: 0.6, envMapIntensity: 1.2, emissive: gold ? 0x5a3500 : 0x000000, emissiveIntensity: 0.4});
  const base = new THREE.Mesh(new RoundedBoxGeometry(S, 0.07, S * w, 3, 0.02), capM); base.position.y = 0.035; g.add(base);
  const top = new THREE.Mesh(new RoundedBoxGeometry(S * 0.8, 0.05, S * w * 0.82, 3, 0.02), capM); top.position.y = 0.085; g.add(top);
  const lab = new THREE.Mesh(new THREE.PlaneGeometry(S * w * 0.74, S * 0.72), new THREE.MeshStandardMaterial({map: capTex(ch, gold, w), roughness: 0.4, envMapIntensity: 0.6, emissive: 0xffffff, emissiveMap: capTex(ch, gold, w), emissiveIntensity: gold ? 0.25 : 0.12}));
  lab.rotation.set(-Math.PI / 2, 0, -Math.PI / 2); lab.position.y = 0.111; g.add(lab);
  const under = new THREE.Mesh(new THREE.PlaneGeometry(S * 1.6, S * w * 1.6), glow(gold ? 0xffb020 : 0x7fb0ff, 0)); under.rotation.x = -Math.PI / 2; under.position.y = 0.004; g.add(under);
  g.userData = {capM, under}; return g;
}
// a word of keycaps laid along +Z (reads left->right for a camera looking +X)
export function keyWord(rows, gold) { const g = new THREE.Group(); const keys = []; rows.forEach((txt, r) => [...txt].forEach((ch, i) => { const k = keycap(ch, gold); k.position.set((rows.length - 1) / 2 * 0.19 - r * 0.19, 0, (i - (txt.length - 1) / 2) * 0.175); g.add(k); keys.push(k); })); g.userData.keys = keys; return g; }

// ---- textbook page (NEET Bio, Living World) ----
function pageTex() {
  const c = document.createElement('canvas'); c.width = 700; c.height = 900; const x = c.getContext('2d');
  x.fillStyle = '#f6f1e3'; x.fillRect(0, 0, 700, 900); x.fillStyle = '#1d6b48'; x.fillRect(0, 0, 700, 70); x.fillStyle = '#fff'; x.font = '700 34px P'; x.fillText('1.3  TAXONOMIC CATEGORIES', 30, 47);
  x.fillStyle = '#333'; x.font = '500 20px P'; const R = rng(5);
  for (let i = 0; i < 9; i++) { const w = 560 + R() * 80; x.fillRect(30, 100 + i * 30, w, 8); }
  const lv = ['KINGDOM', 'PHYLUM', 'CLASS', 'ORDER', 'FAMILY', 'GENUS', 'SPECIES']; x.textAlign = 'center';
  lv.forEach((l, i) => { const w = 560 - i * 64; x.fillStyle = `hsl(${150 - i * 12},45%,${40 + i * 4}%)`; x.fillRect(350 - w / 2, 390 + i * 50, w, 42); x.fillStyle = '#fff'; x.font = '700 22px P'; x.fillText(l, 350, 418 + i * 50); });
  x.textAlign = 'left'; x.fillStyle = '#333'; for (let i = 0; i < 4; i++) x.fillRect(30, 760 + i * 30, 520 + R() * 100, 8);
  x.fillStyle = '#777'; x.font = '500 18px P'; x.fillText('Fig 1.1  Taxonomic hierarchy', 30, 890);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
}
export function textbook() {
  const g = new THREE.Group(); const cover = new THREE.MeshStandardMaterial({color: 0x1d6b48, roughness: 0.6});
  const L = new THREE.Mesh(new THREE.BoxGeometry(0.46, 0.04, 0.6), cover); L.position.set(0, 0.02, -0.235); L.rotation.x = 0.04; g.add(L);
  const pg = new THREE.Mesh(new THREE.PlaneGeometry(0.42, 0.54), new THREE.MeshStandardMaterial({map: pageTex(), roughness: 0.8}));
  pg.rotation.set(-Math.PI / 2, 0, -Math.PI / 2); pg.position.set(0, 0.046, 0.235); g.add(pg);
  const R2 = new THREE.Mesh(new THREE.BoxGeometry(0.46, 0.04, 0.5), cover); R2.position.set(0, 0.02, 0.235); g.add(R2);
  const lp = new THREE.Mesh(new THREE.PlaneGeometry(0.42, 0.54), new THREE.MeshStandardMaterial({color: 0xf3eedf, roughness: 0.85})); lp.rotation.set(-Math.PI / 2, 0, -Math.PI / 2); lp.position.set(0, 0.046, -0.235); g.add(lp);
  const scan = new THREE.Mesh(new THREE.PlaneGeometry(0.03, 0.56), new THREE.MeshBasicMaterial({color: 0x6fe3ff, transparent: true, opacity: 0.9, blending: THREE.AdditiveBlending, depthWrite: false})); scan.rotation.set(-Math.PI / 2, 0, -Math.PI / 2); scan.position.set(0, 0.05, 0.235); g.add(scan);
  const sg = new THREE.Mesh(new THREE.PlaneGeometry(0.2, 0.7), glow(0x6fe3ff, 0.6)); sg.rotation.set(-Math.PI / 2, 0, -Math.PI / 2); sg.position.copy(scan.position); g.add(sg);
  g.userData = {page: pg, scan, sg}; return g;
}
// UPSC answer sheet (handwriting lines)
export function answerSheet() {
  const c = document.createElement('canvas'); c.width = 600; c.height = 800; const x = c.getContext('2d'); x.fillStyle = '#fbfbf6'; x.fillRect(0, 0, 600, 800);
  x.strokeStyle = '#b9cbe8'; x.lineWidth = 2; for (let y = 90; y < 800; y += 34) { x.beginPath(); x.moveTo(0, y); x.lineTo(600, y); x.stroke(); }
  x.strokeStyle = '#e98a8a'; x.beginPath(); x.moveTo(70, 0); x.lineTo(70, 800); x.stroke();
  x.fillStyle = '#1b2a6b'; x.font = '700 30px P'; x.fillText('Q.  Renewable energy &', 84, 60); const R = rng(9);
  for (let i = 0; i < 18; i++) { let px = 84; const y = 118 + i * 34; while (px < 540 - (i === 17 ? 200 : 0)) { const w = 20 + R() * 60; x.fillRect(px, y - 6, w, 4); px += w + 10; } }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  const m = new THREE.Mesh(new THREE.PlaneGeometry(0.4, 0.53), new THREE.MeshStandardMaterial({map: t, roughness: 0.85, side: THREE.DoubleSide})); return m;
}

// ---- clock ----
function clock() {
  const g = new THREE.Group(); const face = new THREE.Mesh(new THREE.CylinderGeometry(0.32, 0.32, 0.04, 48), new THREE.MeshStandardMaterial({color: 0xf3efe6, roughness: 0.5, emissive: 0x30281a, emissiveIntensity: 0.5}));
  face.rotation.x = Math.PI / 2; g.add(face);
  const ring = new THREE.Mesh(new THREE.TorusGeometry(0.33, 0.03, 10, 48), new THREE.MeshStandardMaterial({color: 0xe24a4a, roughness: 0.35, metalness: 0.2})); g.add(ring);
  const ink = new THREE.MeshBasicMaterial({color: 0x15161f});
  for (let i = 0; i < 12; i++) { const a = i / 12 * Math.PI * 2; const tk = new THREE.Mesh(new THREE.BoxGeometry(i % 3 ? 0.012 : 0.022, 0.05, 0.01), ink); tk.position.set(Math.sin(a) * 0.26, Math.cos(a) * 0.26, 0.025); tk.rotation.z = -a; g.add(tk); }
  const hand = (l, w) => { const p = new THREE.Group(); const b = new THREE.Mesh(new THREE.BoxGeometry(w, l, 0.01), ink); b.position.y = l / 2 - 0.02; p.add(b); p.position.z = 0.035; g.add(p); return p; };
  g.userData = {hr: hand(0.15, 0.03), mn: hand(0.23, 0.02)}; g.userData.set = (hours) => { g.userData.hr.rotation.z = -hours / 12 * Math.PI * 2; g.userData.mn.rotation.z = -hours * Math.PI * 2; };
  return g;
}

// ---- window sky (night -> sunrise) ----
function skyMat() {
  return new THREE.ShaderMaterial({uniforms: {k: {value: 0}, t: {value: 0}}, toneMapped: false,
    vertexShader: 'varying vec2 v; void main(){v=uv; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',
    fragmentShader: `uniform float k,t; varying vec2 v;
      float h(vec2 p){return fract(sin(dot(p,vec2(12.9898,78.233)))*43758.5453);}
      void main(){ vec3 n1=vec3(.02,.03,.09), n2=vec3(.07,.1,.24); vec3 d1=vec3(.98,.55,.25), d2=vec3(.45,.6,.95);
        vec3 night=mix(n2,n1,v.y); vec3 dawn=mix(d1,d2,smoothstep(.0,.9,v.y)); vec3 c=mix(night,dawn,k);
        vec2 sp=vec2(.62,.12+.25*k); float s=length((v-sp)*vec2(1.,1.4)); c+=k*(vec3(1.,.8,.45)*smoothstep(.16,.0,s)*1.6+vec3(1.,.55,.25)*smoothstep(.6,.0,s)*.5);
        // city silhouette
        float x=floor(v.x*18.); float bh=.12+.18*h(vec2(x,3.)); if(v.y<bh){ c=mix(vec3(.01,.012,.03),vec3(.12,.08,.1),k); vec2 w=fract(v*vec2(90.,60.)); if(h(floor(v*vec2(90.,60.)))>.78 && w.x<.5 && w.y<.5) c+=vec3(1.,.8,.4)*.6*(1.-k);}
        // rain streaks on glass
        vec2 q=v*vec2(60.,8.); q.y+=t*3.*(1.+h(vec2(floor(q.x),1.))); float r=step(.93,h(floor(q)))*step(.5,fract(q.x))*(1.-k); c+=r*.12;
        gl_FragColor=vec4(c,1.); }`});
}

export function room(env) {
  const s = new THREE.Scene(); s.environment = env; s.background = new THREE.Color(0x05060c);
  const hemi = new THREE.HemisphereLight(0x5a6cc8, 0x140c10, 0.55); s.add(hemi);
  const wallM = new THREE.MeshStandardMaterial({color: 0x232a4a, roughness: 0.92}), floorM = new THREE.MeshStandardMaterial({color: 0x3a2618, roughness: 0.55, metalness: 0.05});
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(14, 14), floorM); floor.rotation.x = -Math.PI / 2; s.add(floor);
  // planks
  for (let i = -7; i < 7; i += 0.35) { const l = new THREE.Mesh(new THREE.BoxGeometry(14, 0.003, 0.012), new THREE.MeshBasicMaterial({color: 0x1d120a})); l.position.set(0, 0.002, i); s.add(l); }
  const back = new THREE.Mesh(new THREE.PlaneGeometry(14, 5), wallM); back.position.set(0, 2.5, -2.6); s.add(back);
  const front = new THREE.Mesh(new THREE.PlaneGeometry(14, 5), wallM); front.rotation.y = -Math.PI / 2; front.position.set(3.4, 2.5, 0); s.add(front);
  const left = new THREE.Mesh(new THREE.PlaneGeometry(14, 5), wallM); left.rotation.y = Math.PI / 2; left.position.set(-3.0, 2.5, 0); s.add(left);
  // window on back wall (z=-2.6)
  const sky = skyMat(); const win = new THREE.Mesh(new THREE.PlaneGeometry(2.0, 1.5), sky); win.position.set(0.2, 2.05, -2.58); s.add(win);
  const frameM = new THREE.MeshStandardMaterial({color: 0xd8d2c4, roughness: 0.6});
  for (const [w, h, x, y] of [[2.12, 0.07, 0.2, 2.8], [2.12, 0.07, 0.2, 1.3], [0.07, 1.56, -0.83, 2.05], [0.07, 1.56, 1.23, 2.05], [0.05, 1.5, 0.2, 2.05], [2.0, 0.04, 0.2, 2.05]]) { const f = new THREE.Mesh(new THREE.BoxGeometry(w, h, 0.08), frameM); f.position.set(x, y, -2.55); s.add(f); }
  const sill = new THREE.Mesh(new THREE.BoxGeometry(2.3, 0.05, 0.25), frameM); sill.position.set(0.2, 1.26, -2.48); s.add(sill);
  const winLight = new THREE.SpotLight(0x6f8cff, 6, 9, 0.9, 0.7, 1.2); winLight.position.set(0.2, 2.1, -2.3); winLight.target.position.set(0.6, 0.6, 0.5); s.add(winLight, winLight.target);
  const ck = clock(); ck.position.set(2.1, 2.45, -2.55); s.add(ck);
  // poster blocks on back wall
  const R = rng(3); for (const [x, y, c] of [[-1.9, 2.2, 0x2f6dd9], [-1.35, 2.5, 0xe24a7a], [2.75, 1.85, 0xf0b53a]]) { const p = new THREE.Mesh(new THREE.PlaneGeometry(0.45, 0.6), new THREE.MeshStandardMaterial({color: c, roughness: 0.8})); p.position.set(x, y, -2.57); p.rotation.z = (R() - 0.5) * 0.1; s.add(p); }
  // desk (top y 0.66), x 0.35..1.35
  const wood = new THREE.MeshStandardMaterial({color: 0x6b4428, roughness: 0.45, metalness: 0.05, envMapIntensity: 0.8});
  const top = new THREE.Mesh(new RoundedBoxGeometry(1.1, 0.05, 2.4, 2, 0.02), wood); top.position.set(0.85, 0.635, 0); s.add(top);
  for (const [x, z] of [[0.36, -1.1], [0.36, 1.1], [1.34, -1.1], [1.34, 1.1]]) { const l = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.62, 0.05), wood); l.position.set(x, 0.31, z); s.add(l); }
  // chair
  const chairM = new THREE.MeshStandardMaterial({color: 0x2a2a33, roughness: 0.6});
  const seat = new THREE.Mesh(new RoundedBoxGeometry(0.42, 0.05, 0.46, 2, 0.02), chairM); seat.position.set(0.02, 0.34, 0); s.add(seat);
  const backr = new THREE.Mesh(new RoundedBoxGeometry(0.05, 0.5, 0.44, 2, 0.02), chairM); backr.position.set(-0.22, 0.62, 0); s.add(backr);
  const post = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.32, 10), chairM); post.position.set(0.02, 0.16, 0); s.add(post);
  // lamp on desk (z = -0.85)
  const lampM = new THREE.MeshStandardMaterial({color: 0xe8e2d6, roughness: 0.35, metalness: 0.3});
  const lb = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.12, 0.03, 24), lampM); lb.position.set(1.0, 0.675, -0.85); s.add(lb);
  const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 0.55, 8), lampM); arm.position.set(0.95, 0.94, -0.85); arm.rotation.z = 0.25; s.add(arm);
  const shade = new THREE.Mesh(new THREE.ConeGeometry(0.13, 0.16, 24, 1, true), new THREE.MeshStandardMaterial({color: 0xe8e2d6, roughness: 0.4, side: THREE.DoubleSide})); shade.position.set(0.82, 1.2, -0.85); shade.rotation.z = 0.6; s.add(shade);
  const bulbG = new THREE.Mesh(new THREE.SphereGeometry(0.04, 12, 10), M.emis(0xffd59a, 4)); bulbG.position.set(0.78, 1.15, -0.85); s.add(bulbG);
  const lamp = new THREE.SpotLight(0xffc27a, 14, 5, 0.85, 0.55, 1.4); lamp.position.set(0.8, 1.15, -0.85); lamp.target.position.set(0.7, 0.62, -0.1); s.add(lamp, lamp.target);
  const lampFill = new THREE.PointLight(0xffb070, 1.6, 4, 1.5); lampFill.position.set(0.6, 1.3, -0.6); s.add(lampFill);
  // books + mug
  const bc = [0xc73e3e, 0x2f6dd9, 0x1d6b48, 0xe0a83a, 0x7a4fc7, 0x2a9d9d];
  for (let i = 0; i < 6; i++) { const b = new THREE.Mesh(new RoundedBoxGeometry(0.32 - (i % 2) * 0.04, 0.06, 0.24, 2, 0.01), new THREE.MeshStandardMaterial({color: bc[i], roughness: 0.65})); b.position.set(1.05 + (R() - .5) * 0.04, 0.69 + i * 0.062, 0.9 + (R() - .5) * 0.04); b.rotation.y = (R() - 0.5) * 0.3; s.add(b); }
  for (let i = 0; i < 3; i++) { const b = new THREE.Mesh(new RoundedBoxGeometry(0.3, 0.05, 0.22, 2, 0.01), new THREE.MeshStandardMaterial({color: bc[(i + 3) % 6], roughness: 0.65})); b.position.set(1.12, 0.685 + i * 0.052, -0.4); b.rotation.y = 0.4 + i * 0.2; s.add(b); }
  const mug = new THREE.Mesh(new THREE.CylinderGeometry(0.055, 0.05, 0.12, 20), new THREE.MeshStandardMaterial({color: 0xf2f2f2, roughness: 0.3})); mug.position.set(0.6, 0.72, 0.62); s.add(mug);
  const chai = new THREE.Mesh(new THREE.CircleGeometry(0.048, 20), new THREE.MeshStandardMaterial({color: 0x8a5a2b, roughness: 0.2})); chai.rotation.x = -Math.PI / 2; chai.position.set(0.6, 0.775, 0.62); s.add(chai);
  // crumpled papers on floor
  for (let i = 0; i < 6; i++) { const p = new THREE.Mesh(new THREE.IcosahedronGeometry(0.05 + R() * 0.03, 0), new THREE.MeshStandardMaterial({color: 0xf0eee6, roughness: 0.9, flatShading: true})); p.position.set(0.4 + R() * 1.6, 0.04, -1.6 + R() * 3.2); s.add(p); }
  // Momo seated
  const mo = faceMomo(); mo.position.set(0.0, 0.0, 0); seatMomo(mo); s.add(mo);
  // phone
  const ph = phone(); ph.position.set(1.7, 1.72, 0); ph.rotation.y = -Math.PI / 2; s.add(ph);
  const phLight = new THREE.PointLight(0x9fc0ff, 5, 4, 1.6); phLight.position.set(1.35, 1.6, 0); s.add(phLight);
  // keyword sets
  const words = {intro: [0, 1, 2].map(i => keycap('/???', i === 2, 2.4)), quiz: keyWord(['/QUIZ']), snap: keyWord(['/SNAP', 'NOTES']), exam: keyWord(['/EXAM', 'INER'], true)};
  words.intro.forEach(k => s.add(k)); for (const k of ['quiz', 'snap', 'exam']) { words[k].position.set(0.8, 0.66, 0); s.add(words[k]); }
  const book = textbook(); book.position.set(0.82, 0.66, 0.0); s.add(book);
  const sheet = answerSheet(); s.add(sheet);
  const sunL = new THREE.DirectionalLight(0xffb070, 0); sunL.position.set(0.5, 3, -6); sunL.target.position.set(0.6, 0.6, 0.6); s.add(sunL, sunL.target);
  return {scene: s, momo: mo, phone: ph, phLight, lamp, lampFill, bulbG, hemi, winLight, sky, clock: ck, words, book, sheet, sunL, mug};
}
