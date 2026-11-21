// Verma family — flat 2D characters drawn as SVG strings.
// fam(who, {mood, blink, arm, bob, t}) -> SVG <g> markup in a 400x700 box (feet at y=700, centre x=200).
// mood: neutral | happy | shock | sad | worried | smug ; arm: down | point | head | phone | cheer | cash | laptop
(function(){
const P = {
  rajesh: {skin:'#B97C55', skinD:'#9C6443', hair:'#1E1A18', top:'#5B8DB8', topD:'#47739A', pants:'#3A3F4A', h:1.0, w:1.12, beard:'mustache', hairStyle:'short', badge:true},
  sunita: {skin:'#C88A62', skinD:'#A96F4C', hair:'#231B17', top:'#9E2A3A', topD:'#7E1F2D', pants:'#9E2A3A', h:0.95, w:1.0, hairStyle:'bun', bindi:true, saree:'#E0A93B'},
  priya:  {skin:'#C99068', skinD:'#AA744F', hair:'#2A1E19', top:'#1F8A8A', topD:'#176C6C', pants:'#2E3340', h:0.97, w:0.92, hairStyle:'pony', glasses:true, lanyard:true},
  chhotu: {skin:'#BF8560', skinD:'#A06A47', hair:'#1C1816', top:'#E3A72F', topD:'#C48A1E', pants:'#2F4A6B', h:0.86, w:0.9, hairStyle:'messy', hood:true},
};
const r = (n)=>Math.round(n*10)/10;
function eyes(c, mood, blink){
  const y=0, open = blink ? 0.12 : 1;
  const ey = mood==='shock' ? 1.35 : mood==='happy' ? 0.8 : 1;
  let s='';
  for (const x of [-22, 22]) {
    if (mood==='happy' && !blink) s+=`<path d="M${x-9} ${y+2} Q${x} ${y-9} ${x+9} ${y+2}" fill="none" stroke="#1b1512" stroke-width="5" stroke-linecap="round"/>`;
    else s+=`<ellipse cx="${x}" cy="${y}" rx="${7*ey}" ry="${r(9*ey*open)}" fill="#fff"/><ellipse cx="${x+1}" cy="${y+1}" rx="${4.5*ey}" ry="${r(5.5*ey*open)}" fill="#1b1512"/>`;
  }
  const bl = {neutral:[0,0], happy:[-2,-2], shock:[-10,-10], sad:[6,-6], worried:[6,-8], smug:[-4,3]}[mood]||[0,0];
  s+=`<path d="M-33 ${-17+bl[1]*0.3} L-12 ${-19-bl[0]*0.6}" stroke="${c.hair}" stroke-width="6" stroke-linecap="round"/>`;
  s+=`<path d="M12 ${-19-bl[0]*0.6} L33 ${-17+bl[1]*0.3}" stroke="${c.hair}" stroke-width="6" stroke-linecap="round"/>`;
  if (c.glasses) s+=`<g fill="none" stroke="#2b2b33" stroke-width="4"><rect x="-36" y="-13" width="28" height="24" rx="8"/><rect x="8" y="-13" width="28" height="24" rx="8"/><path d="M-8 -3 L8 -3"/></g>`;
  return s;
}
function mouth(c, mood){
  switch(mood){
    case 'happy': return `<path d="M-20 34 Q0 58 20 34 Z" fill="#6b1f1f"/><path d="M-14 36 Q0 42 14 36" fill="#fff"/>`;
    case 'shock': return `<ellipse cx="0" cy="42" rx="12" ry="16" fill="#4a1414"/>`;
    case 'sad': return `<path d="M-16 46 Q0 32 16 46" fill="none" stroke="#4a1414" stroke-width="5" stroke-linecap="round"/>`;
    case 'worried': return `<path d="M-14 42 Q-5 36 0 42 T14 42" fill="none" stroke="#4a1414" stroke-width="5" stroke-linecap="round"/>`;
    case 'smug': return `<path d="M-14 40 Q6 48 18 34" fill="none" stroke="#4a1414" stroke-width="5" stroke-linecap="round"/>`;
    default: return `<path d="M-12 40 Q0 46 12 40" fill="none" stroke="#4a1414" stroke-width="5" stroke-linecap="round"/>`;
  }
}
function hairBack(c){
  if (c.hairStyle==='pony') return `<path d="M40 -30 Q78 10 58 90 Q48 60 36 20 Z" fill="${c.hair}"/>`;
  if (c.hairStyle==='bun') return `<circle cx="0" cy="-74" r="26" fill="${c.hair}"/>`;
  return '';
}
function hairFront(c){
  switch(c.hairStyle){
    case 'short': return `<path d="M-60 -10 Q-64 -78 0 -80 Q62 -78 60 -10 Q52 -46 20 -52 Q-20 -40 -52 -46 Z" fill="${c.hair}"/>`;
    case 'bun': return `<path d="M-60 0 Q-62 -76 0 -76 Q62 -76 60 0 Q50 -40 0 -50 Q-50 -40 -60 0 Z" fill="${c.hair}"/><path d="M-2 -76 L-2 -48" stroke="#3a2d26" stroke-width="3"/>`;
    case 'pony': return `<path d="M-60 6 Q-66 -78 0 -78 Q64 -78 60 6 Q56 -36 14 -50 Q-24 -36 -60 6 Z" fill="${c.hair}"/>`;
    case 'messy': return `<path d="M-62 -6 L-66 -50 L-44 -72 L-30 -88 L-8 -78 L10 -94 L30 -80 L52 -84 L58 -56 L64 -6 Q50 -40 20 -46 Q-16 -36 -62 -6 Z" fill="${c.hair}"/>`;
  }
  return '';
}
function arm(c, side, kind, t){
  // side: -1 left, +1 right; shoulder at (±62*w, 0) relative to torso top
  const sx = side*58*c.w, sy = 20;
  let ex, ey, hx, hy;
  const wave = Math.sin(t*6)*8;
  switch(kind){
    case 'point': if (side>0){ex=sx+60; ey=sy-20; hx=sx+128; hy=sy-56+wave*0.3;} else {ex=sx-8; ey=sy+90; hx=sx-4; hy=sy+170;} break;
    case 'head': ex=sx+side*60; ey=sy-50; hx=sx-side*10; hy=sy-150; break;
    case 'cheer': ex=sx+side*50; ey=sy-70; hx=sx+side*70; hy=sy-150+wave; break;
    case 'phone': if (side>0){ex=sx+30; ey=sy+80; hx=sx-20; hy=sy+40;} else {ex=sx-8; ey=sy+90; hx=sx-4; hy=sy+170;} break;
    case 'cash': ex=sx+side*40; ey=sy+70; hx=sx+side*20; hy=sy+120; break;
    case 'laptop': ex=sx+side*20; ey=sy+80; hx=sx-side*20; hy=sy+120; break;
    default: ex=sx+side*12; ey=sy+90; hx=sx+side*14; hy=sy+172;
  }
  let s=`<path d="M${r(sx)} ${sy} L${r(ex)} ${r(ey)} L${r(hx)} ${r(hy)}" fill="none" stroke="${c.top}" stroke-width="34" stroke-linecap="round" stroke-linejoin="round"/>`;
  s+=`<circle cx="${r(hx)}" cy="${r(hy)}" r="17" fill="${c.skin}"/>`;
  if (kind==='point' && side>0) s+=`<path d="M${r(hx)} ${r(hy)} l26 -12" stroke="${c.skin}" stroke-width="11" stroke-linecap="round"/>`;
  if (kind==='phone' && side>0) s+=`<rect x="${r(hx-16)}" y="${r(hy-44)}" width="32" height="58" rx="7" fill="#1b1f27" stroke="#555" stroke-width="2"/><rect x="${r(hx-12)}" y="${r(hy-38)}" width="24" height="44" rx="4" fill="#7fd3ff"/>`;
  if (kind==='cash') s+=`<rect x="${r(hx-30)}" y="${r(hy-18)}" width="60" height="32" rx="4" fill="#7DBE6A" stroke="#3F7A34" stroke-width="3"/>`;
  return s;
}
window.fam = function(who, o={}){
  const c=P[who]; const mood=o.mood||'neutral', t=o.t||0, a=o.arm||'down';
  const blink = o.blink!=null ? o.blink : ((t*1.0 + who.length*0.37)%3.2 < 0.12);
  const bob = (o.bob!==false) ? Math.sin(t*2.4 + who.length)*4 : 0;
  const H=c.h, W=c.w;
  const legH=170*H, torsoH=210*H, headY = 700 - legH - torsoH - 70;
  let s=`<g transform="translate(200 0)">`;
  s+=`<ellipse cx="0" cy="700" rx="${110*W}" ry="16" fill="rgba(0,0,0,.18)"/>`;
  // legs
  if (c.saree) s+=`<path d="M${-62*W} ${700-legH-10} L${-78*W} 692 L${78*W} 692 L${62*W} ${700-legH-10} Z" fill="${c.pants}"/><path d="M${-78*W} 680 L${78*W} 680" stroke="${c.saree}" stroke-width="12"/>`;
  else s+=`<rect x="${-52*W}" y="${700-legH}" width="${44*W}" height="${legH-8}" rx="16" fill="${c.pants}"/><rect x="${8*W}" y="${700-legH}" width="${44*W}" height="${legH-8}" rx="16" fill="${c.pants}"/><rect x="${-60*W}" y="684" width="${56*W}" height="18" rx="9" fill="#222"/><rect x="${4*W}" y="684" width="${56*W}" height="18" rx="9" fill="#222"/>`;
  s+=`<g transform="translate(0 ${r(bob)})">`;
  const ty=700-legH-torsoH;
  s+=`<g transform="translate(0 ${r(ty)})">`;
  s+=arm(c,-1,a==='point'?'down':a,t);
  s+=`<path d="M${-66*W} 26 Q${-70*W} 0 ${-40*W} -6 L${40*W} -6 Q${70*W} 0 ${66*W} 26 L${60*W} ${torsoH+10} L${-60*W} ${torsoH+10} Z" fill="${c.top}"/>`;
  if (c.saree) s+=`<path d="M${40*W} -6 L${-58*W} ${torsoH} L${-30*W} ${torsoH+10} L${62*W} 20 Z" fill="${c.saree}" opacity=".95"/>`;
  if (c.hood) s+=`<path d="M-44 -6 Q0 40 44 -6" fill="none" stroke="${c.topD}" stroke-width="14"/><path d="M-12 30 L-14 90 M12 30 L14 90" stroke="#fff" stroke-width="5" stroke-linecap="round"/><rect x="-40" y="${torsoH-70}" width="80" height="44" rx="10" fill="${c.topD}"/>`;
  if (c.badge) s+=`<rect x="${20*W}" y="40" width="40" height="26" rx="4" fill="#fff"/><rect x="${24*W}" y="46" width="30" height="5" fill="#5B8DB8"/><path d="M-6 0 L0 120 L6 0" fill="${c.topD}"/>`;
  if (c.lanyard) s+=`<path d="M-34 -4 L0 96 L34 -4" fill="none" stroke="#E5533D" stroke-width="7"/><rect x="-18" y="92" width="36" height="46" rx="5" fill="#fff"/><rect x="-12" y="100" width="24" height="12" rx="2" fill="#1F8A8A"/>`;
  s+=arm(c,1,a,t);
  s+=`</g>`;
  // head
  const hy=ty-62;
  s+=`<g transform="translate(0 ${r(hy)})">`;
  s+=`<rect x="-16" y="40" width="32" height="34" fill="${c.skinD}"/>`;
  s+=hairBack(c);
  s+=`<ellipse cx="-62" cy="6" rx="11" ry="16" fill="${c.skinD}"/><ellipse cx="62" cy="6" rx="11" ry="16" fill="${c.skinD}"/>`;
  s+=`<ellipse cx="0" cy="0" rx="62" ry="70" fill="${c.skin}"/>`;
  s+=hairFront(c);
  if (c.bindi) s+=`<circle cx="0" cy="-30" r="5" fill="#C41E3A"/>`;
  s+=eyes(c,mood,blink);
  s+=`<path d="M-4 6 Q0 22 8 20" fill="none" stroke="${c.skinD}" stroke-width="4" stroke-linecap="round"/>`;
  if (c.beard==='mustache') s+=`<path d="M-30 30 Q-14 18 0 26 Q14 18 30 30 Q14 32 0 30 Q-14 32 -30 30 Z" fill="${c.hair}"/>`;
  s+=mouth(c,mood);
  if (mood==='shock' || mood==='worried') s+=`<path d="M52 -40 q6 10 0 16 q-6 -6 0 -16" fill="#8fd3ff"/>`;
  s+=`</g></g></g>`;
  return s;
};
})();
