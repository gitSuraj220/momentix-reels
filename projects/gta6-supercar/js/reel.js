import * as THREE from 'three';
import {EffectComposer} from 'three/addons/postprocessing/EffectComposer.js';
import {RenderPass} from 'three/addons/postprocessing/RenderPass.js';
import {UnrealBloomPass} from 'three/addons/postprocessing/UnrealBloomPass.js';
import {OutputPass} from 'three/addons/postprocessing/OutputPass.js';
import {neonEnv, streetWorld, cockpit, mapWorld, garage, glow} from './world.js';
import {poseMomo, rng} from './models.js';

const W = 1080, H = 1920;
const TL = window.__T__ || await (await fetch('timeline.json?' + Date.now())).json();
const T = TL.T;
await document.fonts.load('84px A2'); await document.fonts.load('700 30px P'); await document.fonts.load('700 50px CP'); await document.fonts.load('500 22px P');

const canvas = document.getElementById('c');
const renderer = new THREE.WebGLRenderer({canvas, antialias: true, preserveDrawingBuffer: true});
renderer.setSize(W, H, false); renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 0.95; renderer.outputColorSpace = THREE.SRGBColorSpace;
const env = neonEnv(renderer);
const S = streetWorld(env), C = cockpit(env), MP = mapWorld(), G = garage(env);
const cam = new THREE.PerspectiveCamera(42, W / H, 0.05, 900);
const comp = new EffectComposer(renderer); const rp = new RenderPass(S.scene, cam); comp.addPass(rp);
const bloom = new UnrealBloomPass(new THREE.Vector2(W / 2, H / 2), 0.55, 0.45, 0.88); comp.addPass(bloom); comp.addPass(new OutputPass());

// ---------- helpers ----------
const cl = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const seg = (t, a, b) => cl((t - a) / (b - a));
const eio = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
const eo = x => 1 - Math.pow(1 - x, 3);
const back = x => { const c = 1.7; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const V = (x, y, z) => new THREE.Vector3(x, y, z);
const lerpV = (a, b, k) => a.clone().lerp(b, k);
function camAt(p, look, fov = 42, shake = 0, t = 0) { cam.fov = fov; cam.updateProjectionMatrix(); cam.position.copy(p); if (shake) cam.position.add(V(Math.sin(t * 91) * shake, Math.cos(t * 77) * shake, Math.sin(t * 63) * shake)); cam.lookAt(look); }
const $ = id => document.getElementById(id);
const nz = (t, s = 1) => Math.sin(t * 1.3 * s) * 0.5 + Math.sin(t * 2.7 * s + 1) * 0.3;

// shot boundaries (all from VO anchors)
const tSmash = T.glass + 0.32;
const B = {
  smash: [0, tSmash + 0.75], press: [tSmash + 0.75, T.aur], hero: [T.aur, T.purane], retro: [T.purane, T.wajah],
  xray: [T.wajah, T.isliye], two: [T.isliye, T.cloner - 0.45], clone: [T.cloner - 0.45, T.engine], run: [T.engine, T.police],
  chase: [T.police, T.main], pass: [T.main, T.kyunki], track: [T.kyunki, T.matlab], map: [T.matlab, T.heat], heat: [T.heat, T.basically], garage: [T.basically, T.end + 1]
};
const inS = (t, k) => t >= B[k][0] && t < B[k][1];

// ---------- overlay: labels with leader lines ----------
const LABS = [];
function label(id, scene, getP, t0, t1, title, sub, color = '#ffffff', off = [-260, -160]) { LABS.push({id, scene, getP, t0, t1, title, sub, color, off}); }
const labsEl = $('labs'), linesEl = $('lines');
function drawLabels(t, scene) {
  let html = '', svg = '';
  for (const L of LABS) { if (L.scene !== scene || t < L.t0 || t > L.t1) continue;
    const a = eo(seg(t, L.t0, L.t0 + 0.35)) * (1 - seg(t, L.t1 - 0.2, L.t1)); if (a <= 0) continue;
    const p = L.getP(t).project(cam); const x = (p.x + 1) / 2 * W, y = (1 - p.y) / 2 * H;
    const off = typeof L.off === 'function' ? L.off(t) : L.off; let lx = cl(x + off[0], 40, 760), ly = cl(y + off[1], 340, 1120);
    const col = typeof L.color === 'function' ? L.color(t) : L.color; const sub = typeof L.sub === 'function' ? L.sub(t) : L.sub;
    const ex = lx + 20, ey = ly + 48; const k = eo(seg(t, L.t0, L.t0 + 0.45));
    svg += `<line x1="${ex}" y1="${ey}" x2="${ex + (x - ex) * k}" y2="${ey + (y - ey) * k}" stroke="${col}" stroke-width="2.5" stroke-dasharray="${L.dash || ''}" opacity="${a}"/>` +
      `<circle cx="${x}" cy="${y}" r="${9 * k}" fill="none" stroke="${col}" stroke-width="3" opacity="${a}"/><circle cx="${x}" cy="${y}" r="3.5" fill="${col}" opacity="${a * k}"/>`;
    html += `<div class="lab" style="left:${lx}px;top:${ly}px;opacity:${a};border-color:${col}55;transform:translateY(${(1 - eo(seg(t, L.t0, L.t0 + .35))) * 16}px)"><div class="t" style="color:${col}">${L.title}</div>${sub ? `<div class="s">${sub}</div>` : ''}</div>`;
  }
  labsEl.innerHTML = html; linesEl.innerHTML = svg;
}

// ---------- captions ----------
const HOT = new Set(['GLASS', 'START', 'NEXT', 'LEVEL', 'BUTTON,', 'IMMOBILIZER.', 'COMPUTER', 'CODED', 'GALAT?', 'BAND.', 'OVER.', 'HOTWIRE', 'EASY.', 'KEYLESS', 'CLONER.', 'ON.', 'MAIN', 'CHARACTER', 'TRACKER', 'POLICE', 'HEAT', 'SCARY.', 'FAST', 'BEKAAR', 'CAP.']);
function drawCap(t) {
  const c = TL.caps.find(c => t >= c.s - 0.08 && t < (TL.caps[TL.caps.indexOf(c) + 1]?.s ?? 1e9) - 0.08);
  if (!c || t > T.end - 0.3) { $('cap').innerHTML = ''; return; }
  const k = eo(seg(t, c.s - 0.08, c.s + 0.12));
  $('cap').innerHTML = c.i.map(i => { const w = TL.words[i]; const on = t >= w.s - 0.04; const hot = on && HOT.has(w.w); return `<span class="${on ? 'on' : ''} ${hot ? 'hot' : ''}">${w.w.replace(/…/, '…')}</span>`; }).join('');
  $('cap').style.transform = `translateY(${(1 - k) * 22}px) scale(${0.96 + 0.04 * k})`; $('cap').style.opacity = k;
}

// ---------- punch words ----------
const PUNCH = [
  {t0: T.nahi - 0.05, t1: T.aur - 0.05, k: 'KEY NOT RECOGNISED', w: "WON'T START.", c: '#ffb347'},
  {t0: T.game - 0.05, t1: T.isliye - 0.05, k: 'CODE GALAT', w: 'GAME OVER.', c: '#ff2a4d'},
  {t0: T.engine, t1: T.police - 0.1, k: 'KEY ACCEPTED', w: 'RUNNING.', c: '#3dffb0'},
  {t0: T.bekaar + 0.15, t1: T.end + 2, k: 'TRACKED · REMEMBERED', w: 'WORST CAR?', c: '#5b9dff'},
];
function drawPunch(t) {
  const p = PUNCH.find(p => t >= p.t0 && t < p.t1); const el = $('punch');
  if (!p) { el.style.opacity = 0; return; }
  const k = seg(t, p.t0, p.t0 + 0.28), out = seg(t, p.t1 - 0.18, p.t1);
  $('pk').textContent = '— ' + p.k; $('pk').style.color = p.c; $('pw').textContent = p.w;
  $('pw').style.clipPath = `inset(0 ${100 - eo(k) * 100}% 0 0)`; el.style.opacity = 1 - out; el.style.transform = `translateX(${(1 - eo(k)) * -40}px) scale(${1 + 0.06 * (1 - eo(seg(t, p.t0, p.t0 + 0.5)))})`;
}

// ---------- chip ----------
function drawChip(t) {
  let txt = 'NO KEY', col = '#ffb347';
  if (t >= T.engine) { txt = 'RUNNING'; col = '#3dffb0'; } if (t >= T.tracker - 0.1) { txt = 'TRACKED'; col = '#5b9dff'; }
  const c = $('chip'); c.style.color = col; c.style.borderColor = col; $('chipt').textContent = txt;
  const pulse = [T.engine, T.tracker - 0.1].map(x => seg(t, x, x + 0.5)).find(v => v > 0 && v < 1) || 0;
  c.style.transform = `scale(${1 + Math.sin(pulse * Math.PI) * 0.12})`; c.style.boxShadow = `0 0 ${30 * Math.sin(pulse * Math.PI)}px ${col}`;
  $('wm').style.opacity = 1 - seg(t, tSmash + 0.4, tSmash + 0.75); $('wm').style.transform = `translateY(${-seg(t, tSmash + .4, tSmash + .75) * 20}px)`;
}

// ---------- SHOTS ----------
function resetStreet(t) {
  const {car, old, momo, cops, copLights, shards, flash, tracker} = S;
  car.visible = true; car.position.set(0, 0, 0); car.rotation.set(0, 0, 0); car.userData.win.visible = true;
  car.userData.headMat.emissiveIntensity = 0.4; car.userData.tailMat.emissiveIntensity = 2.5; car.userData.wheels.forEach(w => w.rotation.z = 0);
  car.traverse(o => { if (o.isMesh && o.material.userData.ghost) { o.material.opacity = 1; o.material.transparent = false; o.material.userData.ghost = false; } });
  old.visible = false; momo.visible = false; momo.position.set(0, 0, 0); momo.rotation.set(0, 0, 0); poseMomo(momo, {});
  cops.forEach(c => c.visible = false); copLights.forEach(l => l.intensity = 0); shards.visible = false; flash.intensity = 0; tracker.visible = false; S.syncOutline(0);
  S.rain.visible = true; S.rain.userData.update(t, cam.position.x, cam.position.z);
  if (S.phone) S.phone.visible = false;
}

const SHOT = {
  smash(t) {
    resetStreet(t); const m = S.momo; m.visible = true; m.position.set(-0.45, 0.02, 1.62); m.rotation.y = Math.PI / 2;
    const wind = eio(seg(t, 0, tSmash - 0.22)), swing = eo(seg(t, tSmash - 0.22, tSmash)), rec = seg(t, tSmash, tSmash + 0.5);
    poseMomo(m, {rz: 0.1 - 1.9 * wind + 3.2 * swing - 0.6 * rec, re: 0.2 + 1.2 * wind - 1.3 * swing, rx: 0.25, lz: 0.5 * wind - 0.5 * swing, lx: -0.25, turn: -0.15 + 0.2 * swing});
    m.rotation.z = 0.06 * wind - 0.1 * swing;
    const hit = t >= tSmash; S.car.userData.win.visible = !hit;
    if (hit) { const dt = t - tSmash, sg = S.shards, d = new THREE.Object3D(); sg.visible = true;
      sg.userData.v.forEach((v, i) => { d.position.set(-0.35 + (v[0] - 0.6) * 0.5 + v[0] * 0.25 * dt, 1.1 + (v[1] - 1.2) * 0.25 + v[1] * dt - 4.9 * dt * dt, 0.78 + v[2] * dt);
        if (d.position.y < 0.02) d.position.y = 0.02; d.rotation.set(v[3] + dt * 9, v[4] + dt * 7, 0); d.scale.setScalar(v[5]); d.updateMatrix(); sg.setMatrixAt(i, d.matrix); }); sg.instanceMatrix.needsUpdate = true;
      S.flash.position.set(-0.4, 1.3, 2.2); S.flash.intensity = 18 * Math.exp(-dt * 9); }
    const k = eio(seg(t, 0, B.smash[1]));
    camAt(lerpV(V(5.6, 2.0, 8.2), V(3.9, 1.6, 6.0), k), lerpV(V(-0.5, 0.75, 0.6), V(-0.4, 0.85, 0.8), k), 42, hit ? 0.06 * Math.exp(-(t - tSmash) * 6) : 0, t);
    return S.scene;
  },
  press(t) {
    C.X.visible = false; C.fob.visible = false; C.phone.visible = false; C.sw.visible = true; C.dash.material.transparent = false; C.dash.material.opacity = 1;
    const tp = T.phir + 0.25; const reach = eio(seg(t, B.press[0], tp)), back = eio(seg(t, tp + 0.25, tp + 0.9));
    C.glove.visible = true; C.glove.scale.setScalar(0.75); C.glove.position.copy(lerpV(lerpV(V(1.9, -0.4, 3.0), V(0.6, 0.24, 1.08), reach), V(1.5, -0.2, 2.6), back)); C.glove.rotation.set(-0.3, 0.5, 0);
    if (t > tp && t < tp + 0.15) C.glove.position.z -= 0.06;
    const fail = t > tp; const blink = fail ? (Math.floor((t - tp) * 7) % 2 === 0 ? 1 : 0.25) : 1;
    C.ringM.color.set(fail ? 0xff2a4d : 0xffb347); C.ringM.emissive.set(fail ? 0xff2a4d : 0xffb347); C.ringM.emissiveIntensity = (fail ? 2.6 : 1.5) * blink; C.btnLight.color.set(fail ? 0xff2a4d : 0xffb347); C.btnLight.intensity = 3 * blink;
    C.drawScr(fail ? 'KEY NOT FOUND' : 'PRESS START', fail ? '#ff2a4d' : '#ffb347');
    const k = eio(seg(t, B.press[0], B.press[1]));
    camAt(lerpV(V(-1.0, 1.55, 3.9), V(-0.45, 1.25, 3.1), k), V(0.45, 0.3, 0.75), 40, fail ? 0.012 * Math.exp(-(t - tp) * 3) : 0, t);
    return C.scene;
  },
  hero(t) {
    resetStreet(t); const k = eio(seg(t, B.hero[0], B.hero[1]));
    const on = seg(t, T.next - 0.1, T.next + 0.15); S.car.userData.headMat.emissiveIntensity = 0.4 + 3.5 * on;
    const a = 0.75 - 1.1 * k; camAt(V(Math.cos(a) * 8.2, 1.05 + 0.35 * k, Math.sin(a) * 8.2), V(0.1, 0.55, 0), 36, 0, t);
    S.lights.key.position.set(-6 + 12 * seg(t, T.next - 0.4, T.next + 1.2), 9, 6); S.lights.key.intensity = 60 + 60 * Math.sin(seg(t, T.next - .4, T.next + 1.2) * Math.PI);
    return S.scene;
  },
  retro(t) {
    resetStreet(t); const modern = t >= T.gta2; S.lights.key.position.set(-6, 9, 6); S.lights.key.intensity = 60;
    S.car.visible = modern; S.old.visible = !modern; S.old.position.set(0, 0, 0); S.old.userData.headMat.emissiveIntensity = t > T.tumhari ? 6 : 0.3;
    const m = S.momo; m.visible = true; m.position.set(modern ? -0.6 : -0.7, 0.02, 1.7); m.rotation.y = modern ? Math.PI / 2 + 0.6 : Math.PI / 2;
    const press = seg(t, T.button + 0.15, T.button + 0.45); poseMomo(m, modern ? {rz: 0.5, re: -1.2, lz: -0.5, le: 1.2, tilt: 0.25 * seg(t, T.gta2, T.gta2 + .4)} : {rz: 1.2 * Math.sin(press * Math.PI), re: -0.4});
    const k = eio(seg(t, B.retro[0], B.retro[1]));
    camAt(V(1.2 - 1.4 * k, 1.9, 8.6 - 1.2 * k), V(0, 0.8, 0), 40, 0, t);
    return S.scene;
  },
  xray(t) {
    C.X.visible = true; C.glove.visible = false; C.phone.visible = false; const reveal = eio(seg(t, B.xray[0], B.xray[0] + 0.9));
    C.dash.material.transparent = true; C.dash.material.opacity = 1 - 0.85 * reveal; C.sw.visible = reveal < 0.5;
    const bad = t >= T.code, red = 0xff2a4d, amb = 0xffd54a;
    C.ringM.color.set(bad ? red : 0xffb347); C.ringM.emissive.set(bad ? red : 0xffb347); C.ringM.emissiveIntensity = bad ? 2.4 : 1.4; C.btnLight.color.set(bad ? red : 0xffb347);
    [C.immo, C.ecu].forEach((b, i) => { const L = b.userData.led.material; const on = t > [T.immobilizer, T.computer][i]; L.color.set(bad ? red : amb); L.emissive.set(bad ? red : amb); L.emissiveIntensity = on ? (bad ? 4 : 3) * (0.6 + 0.4 * Math.sin(t * 12)) : 0.3; });
    const pw = [[T.andar2, T.computer], [T.computer, T.chaabi], [T.chaabi, T.code]];
    C.pulses.forEach((p, i) => { const a = pw[i]; const u = ((t - a[0]) * 0.9) % 1; p.visible = t > a[0] && !bad; if (p.visible) p.position.copy(p.userData.c.getPoint(u)); p.material.emissive.set(amb); });
    C.fob.visible = t > T.chaabi - 0.2; C.fob.position.set(-0.35, 0.75 + 0.06 * Math.sin(t * 3), 1.5); C.fob.rotation.set(0.2, 0.4 + t * 0.4, 0.1);
    C.chip.material.emissive.set(bad ? red : amb); C.chip.material.emissiveIntensity = bad ? 4 : 1.5;
    C.sparks.forEach((s, i) => { s.material.emissive.set(t > T.fuel ? red : amb); s.material.emissiveIntensity = t > T.fuel ? 0.4 : (Math.sin(t * 30 + i * 2) > 0.6 ? 6 : 0); });
    C.drawScr(bad ? 'CODE INVALID' : 'CHECKING KEY…', bad ? '#ff2a4d' : '#ffd54a');
    const k = eio(seg(t, B.xray[0], B.xray[0] + 1.4)), k2 = eio(seg(t, T.chaabi - 0.4, T.chaabi + 0.5)), k3 = eio(seg(t, T.fuel - 0.4, T.fuel + 0.6));
    let p = lerpV(V(-0.45, 1.25, 3.1), V(3.4, -0.2, 5.6), k), l = lerpV(V(0.45, 0.3, 0.75), V(0.6, -0.85, 0.3), k);
    p = lerpV(p, V(1.6, 0.9, 4.6), k2 * (1 - k3)); l = lerpV(l, V(0.2, 0.1, 0.9), k2 * (1 - k3));
    p = lerpV(p, V(3.0, -1.0, 4.4), k3); l = lerpV(l, V(0.8, -1.6, 0.0), k3); p.x += 0.25 * Math.sin(t * 0.6);
    camAt(p, l, 42, bad ? 0.02 * Math.exp(-(t - T.code) * 4) : 0, t);
    return C.scene;
  },
  two(t) {
    resetStreet(t); S.old.visible = true; S.old.position.set(0, 0, -3.1); S.car.position.set(0, 0, 3.1);
    const easy = t > T.easy - 0.1; S.old.userData.headMat.emissiveIntensity = easy ? 6 : 0.3;
    const k = eio(seg(t, B.two[0], T.purani)), k2 = eio(seg(t, T.mehengi - 0.3, T.mehengi + 0.7));
    let p = lerpV(V(10.5, 4.5, 0.5), V(6.2, 2.0, -5.6), k), l = lerpV(V(0, 0.6, 0), V(0, 0.8, -3.1), k);
    p = lerpV(p, V(6.0, 1.6, 7.0), k2); l = lerpV(l, V(0, 0.8, 3.1), k2);
    camAt(p, l, 40, 0, t); return S.scene;
  },
  clone(t) {
    resetStreet(t); const m = S.momo; m.visible = true; m.position.set(-0.95, 0.02, 1.85); m.rotation.y = Math.PI / 2 - 0.5; poseMomo(m, {rz: 1.2, re: -0.4, lz: -0.3, turn: 0.35});
    if (!S.phone) { S.phone = C.phone; }
    S.scene.add(C.phone); C.phone.visible = true; C.phone.position.set(-0.3, 1.08, 1.3); C.phone.rotation.set(0, 0.55, 0.1); C.phone.scale.setScalar(1.0);
    const ok = t > T.engine - 0.35; C.drawPhone(ok ? 1 : seg(t, B.clone[0], T.engine - 0.35), ok);
    const k = eio(seg(t, B.clone[0], B.clone[1]));
    camAt(lerpV(V(2.0, 1.35, 3.6), V(1.35, 1.2, 2.9), k), V(-0.4, 1.02, 1.2), 38, 0, t); return S.scene;
  },
  run(t) {
    C.scene.add(C.phone); C.phone.visible = false; C.X.visible = false; C.sw.visible = true; C.fob.visible = false; C.dash.material.transparent = false; C.dash.material.opacity = 1;
    C.glove.visible = true; const tp = T.engine - 0.05; C.glove.position.copy(lerpV(V(0.6, 0.24, 1.08), V(1.5, -0.2, 2.6), eio(seg(t, tp + 0.15, tp + 0.7)))); C.glove.rotation.set(-0.3, 0.5, 0);
    const g = 0x3dffb0; C.ringM.color.set(g); C.ringM.emissive.set(g); C.ringM.emissiveIntensity = 1.8 + 1.5 * Math.exp(-(t - tp) * 3); C.btnLight.color.set(g); C.btnLight.intensity = 4;
    C.drawScr('KEY ACCEPTED', '#3dffb0');
    camAt(lerpV(V(-0.45, 1.25, 3.1), V(-0.1, 1.0, 2.5), eio(seg(t, B.run[0], B.run[1]))), V(0.45, 0.3, 0.75), 40, 0.02 * Math.exp(-(t - tp) * 4), t); return C.scene;
  },
  chase(t) {
    resetStreet(t); const dt = t - B.chase[0]; const x = 4 * dt * dt + 6 * dt; S.car.position.x = x; S.car.userData.tailMat.emissiveIntensity = 7; S.car.userData.headMat.emissiveIntensity = 8;
    S.car.userData.wheels.forEach(w => w.rotation.z = -x / 0.36);
    S.cops.forEach((c, i) => { c.visible = true; c.position.set(x - 26 - i * 7 - dt * 6, 0, i ? -2.2 : 2.0); const ph = Math.floor(t * 8 + i) % 2; c.userData.bar.red.emissiveIntensity = ph ? 7 : 0.2; c.userData.bar.blue.emissiveIntensity = ph ? 0.2 : 7; });
    S.copLights[0].position.set(x - 26, 2.5, 1); S.copLights[1].position.set(x - 30, 2.5, -1); const ph = Math.floor(t * 8) % 2; S.copLights[0].intensity = ph ? 30 : 0; S.copLights[1].intensity = ph ? 0 : 30;
    S.lights.key.target.position.set(x, 0.5, 0); S.lights.rim.target.position.set(x, 0.5, 0);
    camAt(V(x - 6.5 + 1.5 * eio(seg(t, B.chase[0], B.chase[1])), 1.3, 1.6), V(x + 2, 0.8, 0), 44, 0.025, t);
    return S.scene;
  },
  pass(t) {
    resetStreet(t); const u = seg(t, B.pass[0], B.pass[1]); const slow = t < T.dikkat ? 1 : 0.35;
    const x = 14 + 19 * eio(seg(t, B.pass[0], T.dikkat)) + 1.2 * seg(t, T.dikkat, B.pass[1]); S.car.position.x = x; S.car.userData.tailMat.emissiveIntensity = 7; S.car.userData.headMat.emissiveIntensity = 8;
    S.car.userData.wheels.forEach(w => w.rotation.z = -x / 0.36 * slow);
    S.lights.key.target.position.set(x, 0.5, 0); S.lights.rim.target.position.set(x, 0.5, 0); S.lights.key.position.set(x - 5, 9, 6); S.lights.rim.position.set(x + 6, 7, -6);
    camAt(V(42, 0.45, 4.2), V(x, 0.75, 0.2), 38, 0, t); S.rain.userData.update(t * (t > T.dikkat ? 0.4 : 1), 38, 0);
    return S.scene;
  },
  track(t) {
    resetStreet(t); S.lights.key.position.set(-6, 9, 6); S.lights.rim.position.set(7, 7, -6); S.lights.key.target.position.set(0, .5, 0); S.lights.rim.target.position.set(0, .5, 0);
    const g = seg(t, B.track[0], B.track[0] + 0.6);
    S.car.traverse(o => { if (o.isMesh && o !== S.tracker && o.material.emissive && o.material.emissive.getHex() === 0) { o.material.transparent = true; o.material.opacity = 1 - 0.82 * g; o.material.userData.ghost = true; } });
    S.car.userData.body.material.transparent = true; S.car.userData.body.material.opacity = 1 - 0.8 * g; S.car.userData.body.material.userData.ghost = true;
    S.tracker.visible = true; S.tracker.material.emissiveIntensity = t > T.tracker ? 1 + 5 * (Math.sin(t * 10) > 0 ? 1 : 0.2) : 0.5;
    const k = eio(seg(t, B.track[0], B.track[1])); camAt(lerpV(V(-7.0, 1.8, 6.2), V(-5.2, 1.1, 4.4), k), V(-1.2, 0.45, 0.2), 40, 0, t);
    return S.scene;
  },
  map(t) {
    const u = t - B.map[0]; const px = -21 + u * 5.5; MP.car.position.set(px, 0.4, 0); MP.car.rotation.y = 0;
    MP.rings.forEach((r, i) => { const ph = ((u * 1.1 + i / 3) % 1); r.position.set(px, 0.3, 0); r.scale.setScalar(0.5 + ph * 7); r.material.opacity = (1 - ph) * 0.9; });
    MP.cops.forEach((c, i) => { const a = i * 2.1 + 0.5; const d = 20 - u * 4.2; c.position.set(px + Math.cos(a) * Math.max(3, d), 0.8, Math.sin(a) * Math.max(3, d) * 0.7); c.material.emissiveIntensity = 2 + 3 * (Math.floor(t * 6 + i) % 2); });
    camAt(V(px + 3, 58 - 10 * eio(seg(t, B.map[0], B.map[1])), 16), V(px, 0, 0), 40, 0, t);
    return MP.scene;
  },
  heat(t) {
    resetStreet(t); const m = S.momo; m.visible = true; m.position.set(1.2, 0.02, 2.0); m.rotation.y = -0.25; poseMomo(m, {rz: 0.25, lz: -0.25, turn: 0.35 * Math.sin(seg(t, T.lowkey - 0.2, T.lowkey + 0.6) * Math.PI)});
    S.syncOutline(0.85 * eo(seg(t, B.heat[0] + 0.15, B.heat[0] + 0.6)));
    const k = eio(seg(t, B.heat[0], B.heat[1])); camAt(lerpV(V(6.5, 1.5, 6.8), V(4.2, 1.25, 4.6), k), V(0.4, 0.85, 1.2), 40, 0, t);
    return S.scene;
  },
  garage(t) {
    const car = G.car; car.position.set(0, 0, 0); car.rotation.y = -0.25;
    car.userData.headMat.emissiveIntensity = t > T.fast - 0.1 ? 3 : 0.4; car.userData.tailMat.emissiveIntensity = 3;
    const cin = eo(seg(t, T.bekaar - 0.4, T.bekaar + 1.0));
    G.cops.forEach((c, i) => { c.position.set(-16 + 9 * cin - i * 1.5, 0, i ? -2.4 : 2.4); c.rotation.y = 0; const ph = Math.floor(t * 8 + i) % 2; c.userData.bar.red.emissiveIntensity = cin > 0 ? (ph ? 8 : 0.2) : 0; c.userData.bar.blue.emissiveIntensity = cin > 0 ? (ph ? 0.2 : 8) : 0; });
    const ph = Math.floor(t * 8) % 2; G.red.intensity = cin > 0 ? (ph ? 70 : 8) : 0; G.blue.intensity = cin > 0 ? (ph ? 8 : 70) : 0; G.red.position.x = G.blue.position.x = -16 + 9 * cin + 1;
    G.rain.userData.update(t, 0, 0);
    const k = eio(seg(t, B.garage[0], T.end)); camAt(lerpV(V(6.4, 1.15, 6.6), V(4.6, 0.95, 5.0), k), V(-0.6, 0.6, 0), 40, cin > 0 && cin < 1 ? 0.01 : 0, t);
    return G.scene;
  },
};

// labels (3D-anchored)
const wp = (o, off = V(0, 0, 0)) => () => { o.updateMatrixWorld(true); return o.localToWorld(off.clone()); };
label('ant', C.scene, wp(C.btn, V(0.25, 0.2, 0)), T.wajah + 0.25, T.isliye, 'KEY ANTENNA', 'start button', '#ffd54a', [-420, -150]);
label('immo', C.scene, wp(C.immo), T.immobilizer - 0.1, T.isliye, 'IMMOBILIZER', 'checks the key code', '#ffd54a', [140, -120]);
label('ecu', C.scene, wp(C.ecu), T.computer - 0.1, T.isliye, 'ENGINE COMPUTER', 'fuel + spark control', '#ffd54a', [-520, -40]);
label('fob', C.scene, wp(C.fob, V(0, 0.2, 0.1)), T.chaabi - 0.1, T.code + 0.5, 'CODED KEY?', 'chip inside the fob', '#ffd54a', [60, -230]);
label('fuel', C.scene, wp(C.eng, V(0, 0.6, 0)), T.fuel - 0.1, T.isliye, 'FUEL + SPARK', () => 'BAND', '#ff2a4d', [100, -60]);
label('hot', S.scene, () => V(1.0, 1.7, -3.1), T.purani - 0.05, T.mehengi + 0.2, 'HOTWIRE', () => 'purani gaadi · ' + (0 ? '' : 'easy'), '#3dffb0', [-300, -260]);
label('kl', S.scene, () => V(0.6, 1.4, 3.1), T.mehengi, B.two[1], 'KEYLESS SUPERCAR', 'needs a coded key', '#ffb347', [-320, -260]);
label('kc', S.scene, wp(C.phone, V(0, 0.4, 0)), B.clone[0] + 0.1, B.clone[1], 'KEY CLONER', 'in-game phone tool', '#ffb347', [-420, -300]);
label('trk', S.scene, wp(S.tracker), T.tracker - 0.15, B.track[1], 'TRACKER', 'hidden under the car', '#5b9dff', [-150, -380]);
label('loc', MP.scene, () => MP.car.position.clone(), T.dhoondh - 0.3, B.map[1], 'POLICE KO LOCATION', 'ping every second', '#5b9dff', [-300, -300]);
label('hcar', S.scene, () => V(-0.6, 1.2, 0), T.heat + 0.3, B.heat[1], 'CAR', 'remembered', '#5b9dff', [-340, -40]);
label('hkap', S.scene, wp(S.momo, V(0, 0.62, 0)), T.kapde - 0.1, B.heat[1], 'KAPDE', 'navy hoodie', '#5b9dff', [120, -60]);
label('hlook', S.scene, wp(S.momo, V(0, 1.45, 0)), T.look - 0.1, B.heat[1], 'LOOK', 'bulb head, lol', '#5b9dff', [100, -260]);

// ---------- frame ----------
let lastPR = 1;
window.renderAt = (t) => {
  const key = Object.keys(B).find(k => inS(t, k)) || 'garage';
  const scene = SHOT[key](t);
  const retro = key === 'retro' && t < T.gta2;
  const pr = retro ? 1 / 7 : 1; if (pr !== lastPR) { renderer.setPixelRatio(pr); comp.setPixelRatio(pr); lastPR = pr; }
  canvas.style.imageRendering = retro ? 'pixelated' : 'auto'; canvas.style.width = '1080px'; canvas.style.height = '1920px';
  canvas.style.filter = retro ? 'saturate(.75) contrast(1.15) sepia(.18)' : 'none';
  if (window.NOFLASH) S.flash.intensity = 0; if (window.NOSHARD) S.shards.visible = false; if (window.NOBLOOM) bloom.enabled = false;
  rp.scene = scene; rp.camera = cam; bloom.strength = key === 'map' ? 0.35 : 0.55;
  comp.render();
  // overlays
  $('retro').style.display = key === 'retro' ? 'block' : 'none';
  if (key === 'retro') {
    $('rt').textContent = t < T.gta2 ? 'PURANE GTA' : 'GTA 6'; $('rt').style.font = t < T.gta2 ? '700 58px CP' : '120px A2'; $('rt').style.color = t < T.gta2 ? '#ffe9a8' : '#ff6fbf'; $('rt').style.textShadow = t < T.gta2 ? '4px 4px 0 #7a3b00' : '0 8px 30px rgba(0,0,0,.6)';
    $('retro').querySelector('.scan').style.opacity = t < T.gta2 ? 1 : 0;
    const pa = seg(t, T.button - 0.15, T.button + 0.1); const pressed = t > T.button + 0.2 && t < T.button + 0.45;
    $('prompt').style.opacity = t < T.khatam ? pa : 0; $('prompt').style.transform = `translateX(-50%) scale(${pressed ? 0.93 : 1})`; $('prompt').style.background = pressed ? 'rgba(255,255,255,.3)' : 'rgba(0,0,0,.72)';
    $('prompt').style.filter = t >= T.gta2 ? `blur(${2 * seg(t, T.gta2, T.khatam)}px)` : 'none'; $('prompt').style.top = (t >= T.gta2 ? 760 : 860) + 'px';
    $('yours').style.opacity = t > T.tumhari - 0.1 && t < T.gta2 ? 1 : 0;
    const st = seg(t, T.khatam - 0.05, T.khatam + 0.18); $('stamp').style.opacity = st > 0 ? 1 : 0; $('stamp').style.transform = `translate(-50%,-50%) rotate(-8deg) scale(${1.6 - 0.6 * back(st)})`;
  }
  const g = seg(t, T.gta2 - 0.05, T.gta2 + 0.3); const gl = g > 0 && g < 1;
  $('glitch').style.opacity = gl ? 0.85 : 0; if (gl) { const R = rng(Math.floor(t * 60)); let h = ''; for (let i = 0; i < 9; i++) h += `<div style="position:absolute;left:0;right:0;top:${R() * 1920}px;height:${10 + R() * 90}px;background:${R() > .5 ? '#ff2a7a' : '#2ee6ff'};opacity:.5;transform:translateX(${(R() - .5) * 200}px)"></div>`; $('glitch').innerHTML = h; }
  // tints
  const redT = key === 'xray' ? 0.28 * seg(t, T.game - 0.1, T.game + 0.3) : key === 'pass' ? 0.25 * seg(t, T.dikkat, T.dikkat + 0.6) : 0;
  $('tint').style.background = key === 'pass' ? 'rgba(10,10,30,1)' : '#5a0010'; $('tint').style.opacity = redT;
  const fl = Math.max(0.55 * seg(t, tSmash, tSmash + 0.02) * (1 - seg(t, tSmash + .02, tSmash + .14)), 0.6 * (1 - seg(t, T.engine, T.engine + .25)) * (t >= T.engine ? 1 : 0));
  $('flashw').style.opacity = fl * 0.55;
  const sc = seg(t, T.lowkey - 0.05, T.lowkey + 0.25) * (1 - seg(t, T.basically - 0.2, T.basically)); $('scary').style.opacity = sc; $('scary').style.transform = `translateX(${Math.sin(t * 50) * 6 * (1 - seg(t, T.lowkey, T.lowkey + .4))}px)`;
  const pa = PUNCH.some(p => t >= p.t0 - 0.1 && t < p.t1); labsEl.style.opacity = linesEl.style.opacity = pa ? 0 : 1;
  drawLabels(t, scene); drawCap(t); drawPunch(t); drawChip(t);
  $('tag').style.opacity = ['xray', 'map', 'track'].includes(key) ? 0.9 : 0.6; $('tag').textContent = ['xray', 'track'].includes(key) ? 'SIMPLIFIED SCHEMATIC' : 'ILLUSTRATIVE RECREATION';
};
window.SHOTS = B; window.DBG = {S, C, G, MP}; window.READY = true;
