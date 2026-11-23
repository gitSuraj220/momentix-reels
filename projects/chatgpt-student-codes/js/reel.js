import * as THREE from 'three';
import {EffectComposer} from 'three/addons/postprocessing/EffectComposer.js';
import {RenderPass} from 'three/addons/postprocessing/RenderPass.js';
import {UnrealBloomPass} from 'three/addons/postprocessing/UnrealBloomPass.js';
import {OutputPass} from 'three/addons/postprocessing/OutputPass.js';
import {roomEnv, room, setFace} from './world.js';
import {poseMomo} from './models.js';

const W = 1080, H = 1920;
const TL = window.__T__ || await (await fetch('timeline.json?' + Date.now())).json();
const T = {...TL.T};
await document.fonts.load('84px A2'); await document.fonts.load('700 30px P'); await document.fonts.load('800 30px P'); await document.fonts.load('500 22px P');
// extra word times
const WT = (w, n = 1) => { let c = 0; for (const x of TL.words) if (x.w === w && ++c === n) return x.s; throw new Error('word ' + w); };
Object.assign(T, {slash1: WT('', 1), slash2: WT('', 2), slash3: WT('', 3), likho: WT('LIKHO,'), daalo2: WT('DAALO,'), paste: WT('PASTE'), tarah: WT('TARAH.'), short: WT('SHORT'), notes: WT('NOTES,'), yaad: WT('YAAD'), kahan: WT('KAHAN'), aur1: WT('AUR', 1), apna: WT('APNA'), hain: WT('HAIN.')});
const {makeChats, drawChat} = await import('./chat.js');
const CH = makeChats(T);

const canvas = document.getElementById('c');
const renderer = new THREE.WebGLRenderer({canvas, antialias: true, preserveDrawingBuffer: true});
renderer.setSize(W, H, false); renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.0; renderer.outputColorSpace = THREE.SRGBColorSpace;
const R = room(roomEnv(renderer));
const cam = new THREE.PerspectiveCamera(42, W / H, 0.03, 60);
const comp = new EffectComposer(renderer); comp.addPass(new RenderPass(R.scene, cam));
const bloom = new UnrealBloomPass(new THREE.Vector2(W / 2, H / 2), 0.4, 0.45, 0.92); comp.addPass(bloom); comp.addPass(new OutputPass());

// ---------- helpers ----------
const cl = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const seg = (t, a, b) => cl((t - a) / (b - a));
const eio = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
const eo = x => 1 - Math.pow(1 - x, 3);
const back = x => { const c = 1.7; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const V = (x, y, z) => new THREE.Vector3(x, y, z);
const lerpV = (a, b, k) => a.clone().lerp(b, k);
const $ = id => document.getElementById(id);
let shake = 0;
function camAt(p, look, fov = 42, sh = 0, t = 0) { cam.fov = fov; cam.updateProjectionMatrix(); cam.position.copy(p); if (sh) cam.position.add(V(Math.sin(t * 91) * sh, Math.cos(t * 77) * sh, Math.sin(t * 63) * sh)); cam.lookAt(look); }

// ---------- shot boundaries ----------
const sendS = T.daalo2 + 0.1, cut3 = CH.exam.cutFix[2];
const B = {
  hook: [0, T.chatgpt], rise: [T.chatgpt, T.teen - 0.05], intro: [T.teen - 0.05, T.padhai - 0.1], clock: [T.padhai - 0.1, T.aur1], best: [T.aur1, T.pehla],
  code1: [T.pehla, T.chapter], quiz: [T.chapter, T.galat - 0.12], react: [T.galat - 0.12, T.wahin - 0.25], quiz2: [T.wahin - 0.25, T.doosra],
  code2: [T.doosra, T.textbook - 0.08], photo: [T.textbook - 0.08, sendS - 0.15], notes: [sendS - 0.15, T.teesra],
  code3: [T.teesra, T.apna - 0.05], paste: [T.apna - 0.05, T.examiner2 - 0.3], score: [T.examiner2 - 0.3, cut3 + 0.3], end: [cut3 + 0.3, T.end + 2],
};
const shotOf = t => Object.keys(B).find(k => t >= B[k][0] && t < B[k][1]) || 'end';

// ---------- phone placement ----------
const PH = R.phone, qFloat = new THREE.Quaternion().setFromEuler(new THREE.Euler(0, -Math.PI / 2, 0)), qFlat = new THREE.Quaternion().setFromEuler(new THREE.Euler(-Math.PI / 2, -Math.PI / 2, 0, 'YXZ'));
const qDown = new THREE.Quaternion().setFromEuler(new THREE.Euler(-Math.PI / 2, -Math.PI / 2, 0, 'YXZ')), qEnd = new THREE.Quaternion().setFromEuler(new THREE.Euler(0, -0.35, 0));
const pFloat = V(1.7, 1.72, 0), pDesk = V(0.72, 0.672, 0.5), pScan = V(0.83, 1.05, 0.235);
function placePhone(t, key) {
  let p = pFloat.clone(), q = qFloat.clone(), s = 1;
  if (t < T.chatgpt + 0.7) { const k = eio(seg(t, T.chatgpt - 0.05, T.chatgpt + 0.7)); p = lerpV(pDesk, pFloat, k); p.y += Math.sin(k * Math.PI) * 0.25; q = qFlat.clone().slerp(qFloat, k); s = 0.09 + 0.91 * back(k); }
  if (key === 'photo' || (t > B.photo[0] - 0.4 && t < B.photo[1] + 0.5)) { const k = eio(seg(t, B.photo[0] - 0.35, B.photo[0] + 0.35)) * (1 - eio(seg(t, B.photo[1] - 0.1, B.photo[1] + 0.5)));
    p = lerpV(pFloat, pScan, k); q = qFloat.clone().slerp(qDown, k); s = 1 - 0.62 * k; p.y += 0.015 * Math.sin(t * 5) * k; }
  if (t > B.end[0] - 0.1) { const k = eio(seg(t, B.end[0] - 0.1, B.end[0] + 0.6)); q = qFloat.clone().slerp(qEnd, k); p = lerpV(pFloat, V(1.25, 1.7, 0.75), k); }
  p.y += 0.02 * Math.sin(t * 1.4); PH.position.copy(p); PH.quaternion.copy(q); PH.scale.setScalar(s);
  return s;
}
// canvas y on screen -> world point (phone in float pose)
const scrW = cy => PH.localToWorld(V(0, 0.98 - cy / 1918 * 1.96, 0.04));

// ---------- keycaps ----------
const KW = R.words; const keyTimes = {
  quiz: [T.slash1, ...[0, 1, 2, 3].map(i => T.quiz + i * 0.07)],
  snap: [T.slash2, ...[...Array(9)].map((_, i) => T.snapnotes + i * 0.05)],
  exam: [T.slash3, ...[...Array(8)].map((_, i) => T.examiner + i * 0.055)],
};
function placeKeys(t, which) {
  for (const k of ['quiz', 'snap', 'exam']) { const g = KW[k]; g.visible = k === which; if (!g.visible) continue;
    g.userData.keys.forEach((key, i) => { const ts = keyTimes[k][i]; const fall = seg(t, ts - 0.14, ts); const land = t - ts;
      key.visible = t > ts - 0.14; key.position.y = (1 - fall * fall) * 0.9 + (land > 0 ? Math.abs(Math.sin(land * 22)) * 0.03 * Math.exp(-land * 9) : 0);
      key.rotation.y = (1 - fall) * 0.6 * (i % 2 ? 1 : -1); key.scale.setScalar(land > 0 ? 1 + 0.12 * Math.exp(-land * 14) : 1);
      key.userData.under.material.opacity = land > 0 ? 0.9 * Math.exp(-land * 3) + 0.25 : 0; }); }
}
function lastSlam(t, which) { if (!which) return -9; let l = -9; for (const ts of keyTimes[which]) if (t >= ts) l = ts; return l; }

// ---------- Momo ----------
const MO = R.momo;
function momoAt(t, key) {
  MO.visible = !['code1', 'code2', 'code3', 'quiz', 'quiz2', 'notes', 'score', 'photo'].includes(key); const bm = MO.userData.bulbM;
  let pose = {rz: 1.15, re: 0.35, lz: 1.15, le: 0.35, rx: -0.1, lx: 0.1}, mood = 'neutral', tilt = 0, turn = 0, bulb = 0.6;
  if (t < T.chatgpt) { pose = {rz: 2.55, re: 1.95, rx: -0.75, lz: 2.55, le: 1.95, lx: 0.75}; mood = 'stress'; bulb = 0.22 + 0.15 * (Math.sin(t * 37) > 0.3 ? 1 : 0); tilt = -0.12 + 0.05 * Math.sin(t * 9); }
  else if (t < T.teen) { const k = eo(seg(t, T.chatgpt, T.chatgpt + 0.5)); pose = {rz: 2.55 - 2.3 * k, re: 1.95 - 1.7 * k, rx: -0.75 + 0.65 * k, lz: 2.55 - 2.3 * k, le: 1.95 - 1.7 * k, lx: 0.75 - 0.65 * k}; mood = 'wow'; tilt = 0.28 * k; }
  else if (key === 'intro' || key === 'best' || key === 'clock') { mood = t > T.best - 0.2 ? 'wow' : 'neutral'; tilt = 0.25; pose = {rz: 0.3, lz: 0.3}; }
  else if (key === 'react') { mood = 'worry'; tilt = 0.12; pose = {rz: 1.0, re: 0.6, lz: 1.0, le: 0.6, rx: -0.1, lx: 0.1}; turn = -0.1 * Math.sin(seg(t, B.react[0], B.react[1]) * Math.PI * 3); }
  else if (key === 'quiz2' && t > T.personal) { mood = 'happy'; tilt = 0.2; }
  else if (key === 'notes' || key === 'photo') { mood = t > T.seconds ? 'happy' : 'neutral'; tilt = 0.2; }
  else if (key === 'score') { mood = t > T.kat - 0.1 && t < CH.exam.cutFix[0] ? 'worry' : t >= CH.exam.cutFix[0] ? 'happy' : 'neutral'; tilt = 0.2; }
  else if (key === 'end') { const k = eo(seg(t, B.end[0], B.end[0] + 0.35)); const w = Math.sin((t - B.end[0]) * 14) * 0.15 * k; pose = {rz: 1.15 + 1.75 * k + w, re: 0.35 - 0.3 * k, rx: -0.1 - 0.5 * k, lz: 1.15 + 1.75 * k - w, le: 0.35 - 0.3 * k, lx: 0.1 + 0.5 * k}; mood = 'happy'; tilt = 0.15; bulb = 0.6 + 1.2 * k; }
  else tilt = 0.22;
  if (['quiz', 'quiz2', 'notes', 'score', 'paste'].includes(key)) { const ty = Math.sin(t * 26) * 0.08; pose.rz += ty; pose.lz -= ty; }
  poseMomo(MO, pose); MO.userData.head.rotation.z = tilt; MO.userData.head.rotation.y = turn; setFace(MO, mood, t);
  bm.emissiveIntensity = bulb; MO.position.y = key === 'end' ? 0.05 * Math.abs(Math.sin((t - B.end[0]) * 9)) * seg(t, B.end[0], B.end[0] + 0.3) : 0;
}

// ---------- screen camera: track newest content ----------
function screenCam(t, focus, z = 0.25, d = 2.25) {
  const f = cl(focus, 640, 1640); const pw = scrW(f); const dy = 0.2;
  const sway = 0.04 * Math.sin(t * 0.7);
  camAt(V(pw.x - d, pw.y + 0.02, z + sway), V(pw.x, pw.y - dy, 0), 40, 0, t);
}

// ---------- overlays ----------
const HOT = new Set(['CHATGPT', '3', 'HALF', 'BEST', '/QUIZ.', 'MCQ', 'GALAT', 'PERSONAL', 'TUTOR', '/SNAPNOTES.', 'PHOTO', 'SECONDS', 'TRICK.', 'OP:', '/EXAMINER.', 'ANSWER', 'MARKS', 'KAT']);
function drawCap(t) {
  const i = TL.caps.findIndex((c, j) => t >= c.s - 0.08 && t < (TL.caps[j + 1]?.s ?? 1e9) - 0.08); const c = TL.caps[i];
  if (!c || t > T.hain + 0.9) { $('cap').innerHTML = ''; return; }
  const k = eo(seg(t, c.s - 0.08, c.s + 0.12));
  $('cap').innerHTML = c.i.map(i => { const w = TL.words[i]; const on = t >= w.s - 0.04; const hot = on && HOT.has(w.w); return `<span class="${on ? 'on' : ''} ${hot ? 'hot' : ''}">${w.w}</span>`; }).join('');
  $('cap').style.transform = `translateY(${(1 - k) * 22}px) scale(${0.96 + 0.04 * k})`; $('cap').style.opacity = k;
}
const PUNCH = [
  {t0: T.half - 0.05, t1: T.aur1 - 0.05, k: 'POORI PADHAI', w: 'HALF TIME.', c: '#7dd3ff'},
  {t0: T.op - 0.05, t1: T.slash3 - 0.05, k: 'TEESRA CODE', w: 'SABSE OP.', c: '#ffc93c'},
  {t0: B.end[0] + 0.1, t1: T.end + 2, k: 'EXAMINER SCORE', w: '6 → 9/10', c: '#2fd17a'},
];
function drawPunch(t) {
  const p = PUNCH.find(p => t >= p.t0 && t < p.t1); const el = $('punch');
  if (!p) { el.style.opacity = 0; return; }
  const k = seg(t, p.t0, p.t0 + 0.28), out = seg(t, p.t1 - 0.18, p.t1);
  $('pk').textContent = '— ' + p.k; $('pk').style.color = p.c; $('pw').textContent = p.w; $('pw').style.color = p.c === '#ffc93c' ? '#ffe7a3' : '#f4f6ff';
  $('pw').style.clipPath = `inset(0 ${100 - eo(k) * 100}% 0 0)`; el.style.opacity = 1 - out; el.style.transform = `translateX(${(1 - eo(k)) * -40}px) scale(${1 + 0.06 * (1 - eo(seg(t, p.t0, p.t0 + 0.5)))})`;
}
const CODES = {code1: ['CODE 01', '#7dd3ff', 'QUIZ MODE'], code2: ['CODE 02', '#7dd3ff', 'PHOTO → NOTES'], code3: ['CODE 03', '#ffc93c', 'EXAMINER MODE']};
function drawCodeNo(t, key) {
  const c = CODES[key], el = $('codeno'); if (!c || PUNCH.some(p => t >= p.t0 - 0.1 && t < p.t1)) { el.style.opacity = 0; return; }
  const k = eo(seg(t, B[key][0] + 0.05, B[key][0] + 0.4)), out = seg(t, B[key][1] - 0.2, B[key][1]);
  el.style.opacity = k * (1 - out); el.style.color = c[1]; el.querySelector('.n').textContent = c[0]; el.querySelector('.s').textContent = c[2];
  el.style.transform = `translateY(${(1 - k) * 30}px)`;
}
function drawChip(t) {
  let txt = '2:00 AM · KAL EXAM', col = '#ff6b78';
  if (t >= T.pehla) { txt = 'CODE 1 / 3'; col = '#7dd3ff'; } if (t >= T.doosra) txt = 'CODE 2 / 3'; if (t >= T.teesra) { txt = 'CODE 3 / 3'; col = '#ffc93c'; } if (t >= B.end[0]) { txt = '6:00 AM · READY'; col = '#2fd17a'; }
  const c = $('chip'); c.style.color = col; c.style.borderColor = col; $('chipt').textContent = txt;
  const pulse = [T.pehla, T.doosra, T.teesra, B.end[0]].map(x => seg(t, x, x + 0.5)).find(v => v > 0 && v < 1) || 0;
  c.style.transform = `scale(${1 + Math.sin(pulse * Math.PI) * 0.12})`; c.style.boxShadow = `0 0 ${30 * Math.sin(pulse * Math.PI)}px ${col}`;
  const wa = 1 - seg(t, T.teen - 0.3, T.teen); $('wm').style.opacity = wa * eo(seg(t, 0.05, 0.35)); $('wm').style.transform = `translateY(${(1 - eo(seg(t, 0.05, 0.4))) * 30}px)`;
}
function drawSticker(t) { const el = $('sticker'); const on = t >= T.personal - 0.05 && t < T.doosra - 0.1; const k = back(seg(t, T.personal - 0.05, T.personal + 0.3));
  el.style.opacity = on ? cl(k * 2) : 0; el.style.transform = `rotate(-4deg) scale(${0.5 + 0.5 * k})`; }

// ---------- frame ----------
window.renderAt = (t) => {
  const key = shotOf(t); shake = 0;
  // world states
  R.sky.uniforms.t.value = t; const sun = eio(seg(t, B.end[0] - 0.6, B.end[0] + 1.0)); R.sky.uniforms.k.value = sun;
  R.sunL.intensity = 4.5 * sun; R.hemi.color.setHex(0x5a6cc8).lerp(new THREE.Color(0xffc89a), sun); R.hemi.intensity = 0.55 + 0.6 * sun; R.winLight.color.setHex(0x6f8cff).lerp(new THREE.Color(0xffa860), sun); R.winLight.intensity = 6 + 10 * sun;
  const flick = t < T.chatgpt ? (Math.sin(t * 43) > 0.85 ? 0.55 : 1) : 1; R.lamp.intensity = 6 * flick; R.lampFill.intensity = 1.6 * flick; R.bulbG.material.emissiveIntensity = 4 * flick;
  const hrs = t < T.padhai ? 2 + t * 0.002 : t < T.aur1 + 0.3 ? 2 + 3 * eio(seg(t, T.padhai, T.aur1 + 0.3)) : t < B.end[0] - 0.5 ? 5 + 0.002 * t : 5 + eio(seg(t, B.end[0] - 0.5, B.end[0] + 0.8)); R.clock.userData.set(hrs);
  const s = placePhone(t, key); momoAt(t, key);
  // intro keycaps
  const intro = KW.intro; intro.forEach((k, i) => { const ts = T.teen + [0, 0.3, 0.52][i]; const vis = t > ts - 0.2 && t < T.pehla; k.visible = vis; if (!vis) return;
    const a = eo(seg(t, ts - 0.2, ts + 0.15)); let p = V(1.12, 1.9 + (1 - a) * 0.9, (i - 1) * 0.5); const best = seg(t, T.last, T.best + 0.1);
    if (i === 2) { p = lerpV(p, V(1.0, 1.95, 0.3), eio(best)); } else p.y -= 0.15 * eio(best);
    k.position.copy(p); k.rotation.set(0.15 * Math.sin(t * 2 + i), 0, Math.PI / 2 + (i === 2 ? 0.25 * eio(best) * Math.sin(t * 3) : 0)); k.scale.setScalar((i === 2 ? 1 + 0.15 * eio(best) : 1) * (0.6 + 0.4 * back(a)));
    k.userData.capM.emissiveIntensity = i === 2 ? 0.4 + 2.2 * best * (0.8 + 0.2 * Math.sin(t * 12)) : 0.0; k.userData.capM.color.setHex(i === 2 ? 0xf3c04a : 0xeef0f6).multiplyScalar(i < 2 ? 1 - 0.55 * best : 1);
    k.userData.under.material.opacity = i === 2 ? 0.8 * best : 0; });
  const kwhich = {code1: 'quiz', quiz: t < T.chapter + 0.3 ? 'quiz' : null, code2: 'snap', code3: 'exam'}[key] || null; placeKeys(t, kwhich);
  // book + sheet
  R.book.visible = key === 'photo' || key === 'code2' && t > B.code2[1] - 0.3; const scanK = seg(t, T.photo - 0.35, T.photo + 0.25);
  R.book.userData.scan.visible = R.book.userData.sg.visible = scanK > 0 && scanK < 1; R.book.userData.scan.position.x = R.book.userData.sg.position.x = 0.2 - 0.4 * scanK;
  R.sheet.visible = key === 'paste'; if (key === 'paste') { const k = eio(seg(t, T.answer - 0.05, T.paste + 0.45)); const start = V(0.78, 0.665, -0.35), end = scrW(1300);
    const p = lerpV(start, end, k); p.y += Math.sin(k * Math.PI) * 0.45; R.sheet.position.copy(p); R.sheet.rotation.set(-Math.PI / 2 * (1 - k), -Math.PI / 2 * k, -Math.PI / 2 * (1 - k)); R.sheet.scale.setScalar(1.6 - 0.9 * k); R.sheet.visible = k < 0.98; }
  // phone screen
  let chat = null; if (t >= CH.exam.t0) chat = CH.exam; else if (t >= CH.snap.t0) chat = CH.snap; else if (t >= CH.quiz.t0) chat = CH.quiz;
  const flash = key === 'photo' ? 0.6 * Math.exp(-Math.max(0, t - T.photo) * 12) * (t >= T.photo ? 1 : 0) : 0;
  const vf = key === 'photo' && t < sendS - 0.2 ? seg(t, B.photo[0], T.photo + 0.3) * 0.999 + 0.0005 : 0;
  const clockS = t >= B.end[0] - 0.5 ? '6:02' : t > T.aur1 ? '5:10' : '2:07';
  const focus = drawChat(PH, t < T.chatgpt - 0.05 ? null : chat, t, {wake: T.chatgpt + 0.25, clock: clockS, flash, viewfinder: vf});
  const scrOn = t < T.chatgpt + 0.1 ? 0.15 * seg(t, T.chatgpt - 0.1, T.chatgpt + 0.1) + (Math.sin(t * 6) > 0.97 ? 0.3 : 0) : 1;
  PH.userData.scr.material.color.setScalar(t < T.chatgpt - 0.1 ? 0.04 + (Math.floor(t * 2) % 3 === 0 ? 0.25 : 0) : cl(scrOn * 1.0, 0.04, 1));
  PH.userData.halo.material.opacity = 0.32 * cl(s * 1.4 - 0.2);
  // phone light colour by moment
  let pc = new THREE.Color(0x9fc0ff), pi = 5 * cl(s * 1.2 - 0.1);
  if (t > T.galat && t < T.wahin) { pc = new THREE.Color(0xff3d55); pi = 9; } else if (key === 'notes' && t > T.trick) pc = new THREE.Color(0xffd27a); else if (key === 'score' && t > T.marks && t < CH.exam.cutFix[0]) pc = new THREE.Color(0xff7a5a); else if (t >= CH.exam.cutFix[0]) pc = new THREE.Color(0x7dffb0);
  if (['code1', 'code2', 'code3'].includes(key)) { const l = lastSlam(t, kwhich); pi += 2.5 * Math.exp(-(t - l) * 6); if (key === 'code3') pc = new THREE.Color(0xffc93c); }
  R.phLight.color.copy(pc); R.phLight.intensity = pi; R.phLight.position.copy(PH.position).add(V(-0.35, -0.1, 0));
  // ---- cameras ----
  const u = k => eio(seg(t, B[k][0], B[k][1]));
  if (key === 'hook') camAt(lerpV(V(2.5, 1.75, 2.7), V(2.05, 1.62, 2.2), u('hook')), V(0.45, 1.2, -0.3), 42, 0, t);
  else if (key === 'rise') camAt(lerpV(V(-0.95, 1.4, 1.05), V(-0.85, 1.72, 0.55), u('rise')), lerpV(V(0.9, 1.0, 0.3), V(1.5, 1.8, 0), eo(seg(t, B.rise[0], B.rise[0] + 0.8))), 44, 0, t);
  else if (key === 'intro') camAt(lerpV(V(-0.85, 1.72, 0.55), V(-0.55, 1.78, 0.35), u('intro')), V(1.3, 1.82, 0), 44, 0.012 * Math.exp(-Math.max(0, t - T.teen - 0.52) * 8) * (t > T.teen ? 1 : 0), t);
  else if (key === 'clock') camAt(lerpV(V(1.6, 2.2, -1.0), V(1.8, 2.35, -1.45), u('clock')), V(2.0, 2.4, -2.55), 40, 0, t);
  else if (key === 'best') camAt(lerpV(V(-0.55, 1.78, 0.35), V(-0.1, 1.85, 0.4), u('best')), lerpV(V(1.3, 1.82, 0), V(0.95, 1.9, 0.3), eio(seg(t, T.last, T.best + 0.2))), 42, 0, t);
  else if (key === 'code1' || key === 'code2' || key === 'code3') { const l = lastSlam(t, kwhich); const sh = (key === 'code3' ? 0.022 : 0.012) * Math.exp(-(t - l) * 10) * (l > 0 ? 1 : 0);
    camAt(lerpV(V(-0.62, 2.02, 0.06), V(-0.45, 1.9, 0), u(key)), V(0.8, 0.72, 0), 52, sh, t); }
  else if (key === 'quiz' || key === 'quiz2' || key === 'notes' || key === 'score') screenCam(t, focus - (key === 'score' ? 220 : 60));
  else if (key === 'react') camAt(lerpV(V(1.75, 1.45, 0.65), V(1.6, 1.42, 0.55), u('react')), V(0.05, 1.25, 0), 38, 0.008 * Math.exp(-(t - T.galat) * 5) * (t > T.galat ? 1 : 0), t);
  else if (key === 'photo') camAt(lerpV(V(0.1, 1.85, 0.3), V(0.25, 1.75, 0.26), u('photo')), V(0.86, 0.95, 0.235), 46, 0.006 * Math.exp(-Math.max(0, t - T.photo) * 6) * (t > T.photo ? 1 : 0), t);
  else if (key === 'paste') camAt(lerpV(V(-0.9, 1.6, 0.75), V(-0.75, 1.7, 0.55), u('paste')), V(1.3, 1.45, 0), 46, 0, t);
  else camAt(lerpV(V(1.9, 1.62, 3.0), V(1.6, 1.55, 2.6), eio(seg(t, B.end[0], T.end))), V(0.25, 1.3, -0.2), 46, 0, t);
  bloom.strength = 0.4;
  comp.render();
  // ---- overlays ----
  drawCap(t); drawPunch(t); drawChip(t); drawCodeNo(t, key); drawSticker(t);
  $('flashw').style.opacity = 0.35 * flash * (key === 'photo' ? 1 : 0) + 0.35 * Math.exp(-Math.max(0, t - T.slash3) * 8) * (key === 'code3' && t > T.slash3 ? 1 : 0);
  $('tint').style.opacity = t > T.galat && t < T.wahin - 0.25 ? 0.22 * (1 - seg(t, T.wahin - 0.6, T.wahin - 0.25)) : 0;
  if (window.COVER) $('ov').style.display = 'none';
};
window.SHOTS = B; window.TT = T; window.DBG = {R}; window.READY = true;
