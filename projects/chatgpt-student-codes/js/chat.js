// Dark-mode ChatGPT-style chat drawn on the phone's canvas, fully deterministic in t.
const SW = 900, SH = 1918, CTOP = 225, CBOT = 1700;
const LOGO = new Path2D(await (await fetch('assets/logo_path.txt')).text());
const cl = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x)); const seg = (t, a, b) => cl((t - a) / (b - a)); const eo = x => 1 - Math.pow(1 - x, 3);
const back = x => { const c = 1.9; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };

function rr(x, X, Y, w, h, r) { x.beginPath(); x.moveTo(X + r, Y); x.arcTo(X + w, Y, X + w, Y + h, r); x.arcTo(X + w, Y + h, X, Y + h, r); x.arcTo(X, Y + h, X, Y, r); x.arcTo(X, Y, X + w, Y, r); x.closePath(); }
function logo(x, cx, cy, s, col = '#fff') { x.save(); x.translate(cx - 12 * s, cy - 12 * s); x.scale(s, s); x.fillStyle = col; x.fill(LOGO); x.restore(); }
function wrap(x, text, maxW) { const out = []; for (const para of text.split('\n')) { let line = ''; for (const w of para.split(' ')) { const tryL = line ? line + ' ' + w : w; if (x.measureText(tryL).width > maxW && line) { out.push(line); line = w; } else line = tryL; } out.push(line); } return out; }

// ----- blocks: measure(x) -> h ; draw(x, y, t) -----
const F = (w, s) => `${w} ${s}px P`;
function P(text, o = {}) { // streamed paragraph
  return {t0: o.t0 ?? 0, rate: o.rate ?? 0.016, side: o.side || 'ai', h(x) { x.font = F(o.w || 500, o.s || 42); this.L = wrap(x, text, o.maxW || 780); return this.L.length * (o.lh || 60) + (o.mb ?? 16); },
    draw(x, y, t) { x.font = F(o.w || 500, o.s || 42); let n = Math.floor((t - this.t0) / this.rate); x.fillStyle = o.c || '#ececec'; x.textBaseline = 'top';
      this.L.forEach((l, i) => { if (n <= 0) return; const s = l.slice(0, n); n -= l.length + 1; drawRich(x, s, 60, y + i * (o.lh || 60), o); }); }};
}
function drawRich(x, s, X, Y, o) { // **gold** segments
  if (!o.hl) { x.fillText(s, X, Y); return; } let px = X; for (const part of s.split(/(\*[^*]*\*?)/)) { if (!part) continue; const hot = part.startsWith('*'); const txt = part.replace(/\*/g, ''); x.fillStyle = hot ? o.hl : (o.c || '#ececec'); x.font = F(hot ? 800 : (o.w || 500), o.s || 42); x.fillText(txt, px, Y); px += x.measureText(txt).width; }
}
function AIHead(t0) { return {t0, h: () => 84, draw(x, y) { x.fillStyle = '#ffffff'; x.beginPath(); x.arc(88, y + 30, 28, 0, 7); x.fill(); logo(x, 88, y + 30, 1.85, '#0d0d0d'); x.fillStyle = '#9b9b9b'; x.font = F(600, 32); x.textBaseline = 'middle'; x.fillText('ChatGPT', 132, y + 30); }}; }
function Opt(L, text, t0, st) { // st(t) -> 'none' | 'picked' | 'wrong' | 'right'
  return {t0, opt: true, h: () => 112, draw(x, y, t) { const s = st(t); const col = {none: '#3a3a3a', picked: '#5b8cff', wrong: '#ff4d5e', right: '#2fd17a'}[s];
    const a = eo(seg(t, t0, t0 + 0.25)); x.globalAlpha *= a; rr(x, 60 + (1 - a) * 40, y, 780, 94, 26); x.fillStyle = s === 'none' ? '#2a2a2a' : col + '33'; x.fill(); x.lineWidth = s === 'none' ? 2 : 5; x.strokeStyle = col; x.stroke();
    x.fillStyle = s === 'none' ? '#444' : col; x.beginPath(); x.arc(118, y + 47, 28, 0, 7); x.fill(); x.fillStyle = '#fff'; x.font = F(700, 34); x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(s === 'wrong' ? '✕' : s === 'right' ? '✓' : L, 118, y + 48); x.textAlign = 'left';
    x.font = F(600, 40); x.fillStyle = '#f2f2f2'; x.fillText(text, 170, y + 48); x.globalAlpha = 1; }};
}
function Trick(t0, title, line) {
  return {t0, h: () => 250, draw(x, y, t) { const a = eo(seg(t, t0, t0 + 0.35)), p = back(seg(t, t0, t0 + 0.45)); x.save(); x.globalAlpha = a; x.translate(450, y + 115); x.scale(0.9 + 0.1 * p, 0.9 + 0.1 * p); x.translate(-450, -(y + 115));
    rr(x, 50, y, 800, 230, 30); const g = x.createLinearGradient(0, y, 0, y + 230); g.addColorStop(0, '#3b2a05'); g.addColorStop(1, '#271b02'); x.fillStyle = g; x.fill(); x.lineWidth = 4; x.strokeStyle = '#ffc93c'; x.stroke();
    x.fillStyle = '#ffc93c'; x.font = F(800, 34); x.textBaseline = 'top'; x.fillText('★  ' + title.toUpperCase(), 84, y + 30);
    x.font = F(700, 44); let px = 84, py = y + 92; for (const w of line.split(' ')) { const ww = x.measureText(w + ' ').width; if (px + ww > 830) { px = 84; py += 62; } x.fillStyle = '#ffc93c'; x.fillText(w[0], px, py); x.fillStyle = '#fff4d6'; x.fillText(w.slice(1), px + x.measureText(w[0]).width, py); px += ww; }
    x.restore(); }};
}
function Score(t0, val) { // val(t) -> number 0..10
  return {t0, h: () => 300, draw(x, y, t) { const v = val(t), p = back(seg(t, t0, t0 + 0.4)); const col = v >= 9 ? '#2fd17a' : v >= 7 ? '#ffc93c' : '#ff4d5e';
    x.save(); x.globalAlpha = cl(p * 2); x.translate(210, y + 140); x.scale(0.4 + 0.6 * p, 0.4 + 0.6 * p);
    x.lineWidth = 26; x.strokeStyle = '#333'; x.beginPath(); x.arc(0, 0, 112, 0, 7); x.stroke(); x.strokeStyle = col; x.lineCap = 'round'; x.beginPath(); x.arc(0, 0, 112, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * v / 10); x.stroke();
    x.fillStyle = '#fff'; x.font = F(800, 92); x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(Math.round(v), -14, 2); x.font = F(700, 40); x.fillStyle = '#aaa'; x.fillText('/10', 58, 26); x.restore();
    x.globalAlpha = cl(p * 2); x.textAlign = 'left'; x.textBaseline = 'top'; x.fillStyle = col; x.font = F(800, 40); x.fillText(v >= 9 ? 'EXCELLENT' : v >= 7 ? 'IMPROVING' : 'AVERAGE', 380, y + 82); x.fillStyle = '#bdbdbd'; x.font = F(500, 34); x.fillText('Examiner score', 380, y + 138); x.fillText('GS-3 · 10 marks', 380, y + 184); x.globalAlpha = 1; }};
}
function Cut(t0, text, fixAt) {
  return {t0, h: () => 98, draw(x, y, t) { const a = eo(seg(t, t0, t0 + 0.22)), f = t >= fixAt; x.globalAlpha = a; const col = f ? '#2fd17a' : '#ff4d5e';
    rr(x, 60 + (1 - a) * 50, y, 780, 82, 22); x.fillStyle = col + '22'; x.fill(); x.lineWidth = 3; x.strokeStyle = col + 'aa'; x.stroke();
    rr(x, 80, y + 15, 92, 52, 16); x.fillStyle = col; x.fill(); x.fillStyle = '#fff'; x.font = F(800, 34); x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(f ? '+1' : '−1', 126, y + 42); x.textAlign = 'left';
    x.fillStyle = f ? '#c9f5dc' : '#ffd9dd'; x.font = F(600, 38); x.fillText(text, 196, y + 42);
    if (f) { const k = seg(t, fixAt, fixAt + 0.2); x.fillStyle = '#2fd17a'; x.font = F(800, 40); x.fillText('✓', 790, y + 42); x.globalAlpha = 1 - k; rr(x, 60, y, 780, 82, 22); x.fillStyle = '#ffffff'; x.fill(); }
    x.globalAlpha = 1; }};
}
function pageThumb(x, X, Y, w, h) { x.save(); rr(x, X, Y, w, h, 18); x.clip(); x.fillStyle = '#f6f1e3'; x.fillRect(X, Y, w, h); x.fillStyle = '#1d6b48'; x.fillRect(X, Y, w, h * 0.09); x.fillStyle = '#fff'; x.font = F(700, w * 0.05); x.textBaseline = 'middle'; x.fillText('1.3 TAXONOMIC CATEGORIES', X + w * 0.05, Y + h * 0.045);
  x.fillStyle = '#555'; for (let i = 0; i < 7; i++) x.fillRect(X + w * 0.05, Y + h * (0.13 + i * 0.035), w * (0.8 + 0.1 * Math.sin(i * 3)), h * 0.01);
  for (let i = 0; i < 7; i++) { const ww = w * (0.8 - i * 0.09); x.fillStyle = `hsl(${150 - i * 12},45%,${40 + i * 4}%)`; x.fillRect(X + (w - ww) / 2, Y + h * (0.43 + i * 0.056), ww, h * 0.046); }
  x.restore(); }
function User(t0, text, o = {}) {
  return {t0, h(x) { x.font = F(500, 42); this.L = wrap(x, text, 560); this.ph = o.paste ? (x.font = F(500, 32), this.PL = wrap(x, o.paste, 560).slice(0, 4)).length * 44 + 30 : 0; return (o.img ? 400 : 0) + this.L.length * 58 + 52 + this.ph + 30; },
    draw(x, y, t) { const a = eo(seg(t, t0, t0 + 0.25)); x.globalAlpha = a; const dy = (1 - a) * 40; y += dy;
      if (o.img) { pageThumb(x, 840 - 300, y, 300, 380); y += 400; }
      x.font = F(500, 42); const w = Math.max(...this.L.map(l => x.measureText(l).width), o.paste ? 560 : 0) + 64; const h = this.L.length * 58 + 52 + this.ph;
      rr(x, 840 - w, y, w, h, 40); x.fillStyle = '#303030'; x.fill(); x.fillStyle = '#fff'; x.textBaseline = 'top'; this.L.forEach((l, i) => x.fillText(l, 840 - w + 32, y + 26 + i * 58));
      if (o.paste) { const py = y + 26 + this.L.length * 58 + 10; x.fillStyle = '#5b8cff'; x.fillRect(840 - w + 32, py, 5, this.ph - 26); x.font = F(500, 32); x.fillStyle = '#b8b8b8'; this.PL.forEach((l, i) => x.fillText(i === 3 ? l.slice(0, 26) + '…' : l, 840 - w + 54, py + i * 44)); }
      x.globalAlpha = 1; }};
}

// ----- the three chats -----
export function makeChats(T) {
  const kq = T.quiz, ks = T.snapnotes, ke = T.examiner;
  const tapA = 12.15, galat = T.galat;
  const quizSt = (L) => t => L === 'A' ? (t >= galat ? 'wrong' : t >= tapA ? 'picked' : 'none') : L === 'B' ? (t >= galat + 0.3 ? 'right' : 'none') : 'none';
  const sendQ = T.likho + 0.25, sendS = T.daalo2 + 0.1, sendE = T.paste + 0.55;
  const cutFix = [0.95, 1.3, 1.65].map(d => T.kat + d);
  const scoreVal = t => 6 + cutFix.filter(f => t >= f + 0.05).length;
  return {
    quiz: {t0: kq - 0.6, typed: [['/', T.slash1], ...[...'quiz'].map((c, i) => [c, kq + i * 0.07]), ...[...' JEE Physics: Rotational Motion'].map((c, i) => [c, T.chapter + 0.05 + i * 0.026])], send: sendQ,
      blocks: [User(sendQ, '/quiz JEE Physics: Rotational Motion'), AIHead(sendQ + 0.3), P('Q1. A ring and a disc (same mass, same radius) roll down the same slope. Which reaches the bottom first?', {t0: sendQ + 0.4, w: 700, rate: 0.012}),
        Opt('A', 'Ring', T.mcq - 0.05, quizSt('A')), Opt('B', 'Disc', T.mcq + 0.07, quizSt('B')), Opt('C', 'Both together', T.mcq + 0.19, quizSt('C')), Opt('D', 'Depends on mass', T.mcq + 0.31, quizSt('D')),
        P('*Galat!* Sahi answer: *B) Disc.*', {t0: T.wahin - 0.15, w: 700, hl: '#ff6b78', rate: 0.02}),
        P('Disc ka I = MR²/2, ring ka MR². Kam inertia = zyada speed, isliye disc pehle pahunchti hai.', {t0: T.wahin + 0.35, rate: 0.014}),
        P('Ready for Q2? →', {t0: T.tarah + 0.1, c: '#9b9b9b', rate: 0.02})], tap: [tapA, 'A']},
    snap: {t0: ks - 0.6, typed: [['/', T.slash2], ...[...'snapnotes'].map((c, i) => [c, ks + i * 0.05])], attach: T.photo + 0.25, send: sendS,
      blocks: [User(sendS, '/snapnotes', {img: true}), AIHead(sendS + 0.25), P('Short Notes: Taxonomic Categories', {t0: sendS + 0.3, w: 800, s: 44, rate: 0.012}),
        P('• Taxonomy = organisms ko naam dena + groups mein rakhna', {t0: T.seconds + 0.05, rate: 0.01}), P('• Basic unit: Species', {t0: T.short, rate: 0.012}),
        P('• Kingdom → Phylum → Class → Order → Family → Genus → Species', {t0: T.notes + 0.1, rate: 0.008}), P('• Binomial name: Genus + species (Mangifera indica = aam)', {t0: T.yaad, rate: 0.01}),
        Trick(T.trick - 0.05, 'Yaad rakhne ki trick', 'King Philip Came Over For Good Soup')]},
    exam: {t0: ke - 0.6, typed: [['/', T.slash3], ...[...'examiner'].map((c, i) => [c, ke + i * 0.055])], paste: T.answer + 0.2, send: sendE,
      blocks: [User(sendE, '/examiner', {paste: "Q. Discuss the role of renewable energy in India's energy security. (GS-3, 10 marks)  Ans: Renewable energy like solar and wind reduces India's dependence on imported coal and oil. India gets good sunlight for most of the year, so solar parks can"}),
        AIHead(T.examiner2 - 0.2), Score(T.marks - 0.05, scoreVal),
        P('Marks yahan kat rahe hain:', {t0: T.batayega - 0.1, w: 700, rate: 0.016}), Cut(T.batayega + 0.3, 'No data / facts', cutFix[0]), Cut(T.kahan + 0.25, 'No diagram or map', cutFix[1]), Cut(T.kat + 0.05, 'Weak conclusion', cutFix[2])], cutFix},
  };
}

// ----- frame -----
function statusBar(x, clock) { x.fillStyle = '#fff'; x.font = F(600, 34); x.textBaseline = 'middle'; x.fillText(clock, 70, 62);
  for (let i = 0; i < 4; i++) x.fillRect(700 + i * 14, 72 - i * 7, 9, 10 + i * 7); rr(x, 770, 48, 62, 30, 9); x.strokeStyle = '#fff'; x.lineWidth = 3; x.stroke(); x.fillRect(775, 53, 44, 20); x.fillRect(835, 57, 5, 12);
  rr(x, 360, 34, 180, 54, 27); x.fillStyle = '#000'; x.fill(); }
function header(x) { x.fillStyle = '#ececec'; for (let i = 0; i < 2; i++) { rr(x, 56, 150 + i * 20, i ? 30 : 44, 6, 3); x.fill(); }
  x.font = F(600, 44); x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText('ChatGPT  ›', 450, 162); x.textAlign = 'left';
  x.lineWidth = 5; x.strokeStyle = '#ececec'; rr(x, 806, 138, 44, 44, 10); x.stroke(); }
function input(x, txt, t, o = {}) {
  const has = !!txt || o.attach; rr(x, 30, 1736, 840, 132, 66); x.fillStyle = '#2f2f2f'; x.fill(); x.lineWidth = 2; x.strokeStyle = '#3d3d3d'; x.stroke();
  x.strokeStyle = '#d0d0d0'; x.lineWidth = 5; x.beginPath(); x.moveTo(98, 1782); x.lineTo(98, 1822); x.moveTo(78, 1802); x.lineTo(118, 1802); x.stroke();
  let tx = 150; if (o.attach) { pageThumb(x, 150, 1758, 70, 88); tx = 240; }
  x.font = F(500, 42); x.textBaseline = 'middle'; x.fillStyle = txt ? '#fff' : '#8e8e8e'; let s = txt || 'Ask anything'; while (x.measureText(s).width > 560 - (tx - 150)) s = '…' + s.slice(2);
  x.fillText(s, tx, 1802); if (txt && Math.floor(t * 3) % 2 === 0) { x.fillRect(tx + x.measureText(s).width + 4, 1780, 3, 46); }
  if (has) { x.fillStyle = '#fff'; x.beginPath(); x.arc(806, 1802, 40, 0, 7); x.fill(); x.strokeStyle = '#000'; x.lineWidth = 7; x.lineCap = 'round'; x.beginPath(); x.moveTo(806, 1822); x.lineTo(806, 1784); x.moveTo(790, 1798); x.lineTo(806, 1782); x.lineTo(822, 1798); x.stroke(); x.lineCap = 'butt'; }
  else { x.fillStyle = '#d0d0d0'; for (let i = 0; i < 4; i++) rr(x, 784 + i * 13, 1802 - [10, 20, 14, 6][i], 7, [10, 20, 14, 6][i] * 2, 3), x.fill(); }
}
function layout(x, chat, t) { let y = CTOP; const out = []; for (const b of chat.blocks) { if (t < b.t0) continue; const h = b.h(x); out.push([b, y]); y += h; } return {out, bottom: y}; }
export function scrollOf(x, chat, t) { const {bottom} = layout(x, chat, t); return Math.max(0, bottom - CBOT); }
// returns focus canvas-y (bottom of newest content, after scroll)
export function drawChat(ph, chat, t, o = {}) {
  const x = ph.userData.ctx; x.globalAlpha = 1; x.fillStyle = '#212121'; x.fillRect(0, 0, SW, SH);
  let focus = 700;
  if (!chat || t < (chat.send ?? 1e9)) { // home screen
    const a = eo(seg(t, o.wake ?? -1, (o.wake ?? -1) + 0.5)); x.globalAlpha = a;
    const p = back(seg(t, o.wake ?? -1, (o.wake ?? -1) + 0.6)); x.save(); x.translate(450, 760); x.scale(p, p); x.fillStyle = '#fff'; x.beginPath(); x.arc(0, 0, 88, 0, 7); x.fill(); logo(x, 0, 0, 5.4, '#0d0d0d'); x.restore();
    x.fillStyle = '#ececec'; x.font = F(600, 54); x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText('What can I help with?', 450, 940); x.textAlign = 'left'; x.globalAlpha = 1;
    focus = 1500;
  } else {
    const avg = [0, 0.08, 0.16, 0.24].reduce((s, d) => s + scrollOf(x, chat, Math.max(chat.send, t - d)), 0) / 4;
    const {out, bottom} = layout(x, chat, t); x.save(); x.beginPath(); x.rect(0, CTOP - 20, SW, CBOT - CTOP + 30); x.clip(); x.translate(0, -avg);
    for (const [b, y] of out) b.draw(x, y, t);
    if (chat.tap && t > chat.tap[0] - 0.15 && t < chat.tap[0] + 0.5) { const ent = out.find(([b]) => b.opt); if (ent) { const k = seg(t, chat.tap[0] - 0.15, chat.tap[0] + 0.5); x.globalAlpha = 1 - k; x.fillStyle = '#ffffff'; x.beginPath(); x.arc(300, ent[1] + 47, 30 + 80 * k, 0, 7); x.fill(); x.globalAlpha = 1; } }
    x.restore(); focus = bottom - avg;
  }
  // header, status, input on top
  x.fillStyle = '#212121'; x.fillRect(0, 0, SW, CTOP - 20); statusBar(x, o.clock || '2:07'); header(x);
  x.fillStyle = '#212121'; x.fillRect(0, 1715, SW, SH - 1715);
  let typed = ''; if (chat && t < chat.send) { for (const [c, tt] of chat.typed) if (t >= tt) typed += c; if (chat.paste && t >= chat.paste) typed += " Q. Discuss the role of renewable energy…"; }
  input(x, typed, t, {attach: chat && chat.attach && t >= chat.attach && t < chat.send});
  rr(x, 330, 1886, 240, 10, 5); x.fillStyle = '#8a8a8a'; x.fill();
  if (o.flash) { x.fillStyle = `rgba(255,255,255,${o.flash})`; x.fillRect(0, 0, SW, SH); }
  if (o.viewfinder) viewfinder(x, o.viewfinder, t);
  ph.userData.tex.needsUpdate = true; return focus;
}
function viewfinder(x, k, t) { x.fillStyle = '#000'; x.fillRect(0, 0, SW, SH); pageThumb(x, 90, 330, 720, 960); x.strokeStyle = '#ffd54a'; x.lineWidth = 8;
  for (const [cx, cy, sx, sy] of [[110, 350, 1, 1], [790, 350, -1, 1], [110, 1270, 1, -1], [790, 1270, -1, -1]]) { x.beginPath(); x.moveTo(cx, cy + sy * 80); x.lineTo(cx, cy); x.lineTo(cx + sx * 80, cy); x.stroke(); }
  x.fillStyle = 'rgba(111,227,255,.8)'; x.fillRect(90, 330 + 960 * (k % 1), 720, 8);
  x.fillStyle = '#fff'; x.font = F(700, 40); x.textAlign = 'center'; x.fillText('SCANNING PAGE…', 450, 1400); x.textAlign = 'left';
  x.beginPath(); x.arc(450, 1650, 80, 0, 7); x.fill(); x.lineWidth = 8; x.strokeStyle = '#000'; x.beginPath(); x.arc(450, 1650, 66, 0, 7); x.stroke(); }
