// ===================== Jammer explainer — premium dark look =====================
const T = k => TL.lines[k][0], TE = k => TL.lines[k][1];
const F = i => TL.frags[i];
const D = {sky0:'#060915', sky1:'#0C1330', sky2:'#1B1240', ink:'#E8ECF6', mute:'#8C96B5', panel:'#121A33', panel2:'#18223F',
  line:'#26304F', cyan:'#22D3EE', cyan2:'#67E8F9', yellow:'#FFD43B', red:'#F43F5E', red2:'#FB7185', green:'#22C55E', green2:'#4ADE80',
  orange:'#FB923C', brick:'#B4532A', brick2:'#6B2A12'};
const hh=(i,j=0)=>hash(i*13.37+j*71.11);
function T2(x,y,s,o={}){ // text with optional halo
  const halo=o.halo?`stroke="${o.halo}" stroke-width="${o.hw||10}" paint-order="stroke" stroke-linejoin="round"`:'';
  return `<text x="${x}" y="${y}" font-size="${o.size||40}" font-weight="${o.w||700}" fill="${o.fill||D.ink}" text-anchor="${o.anchor||'middle'}" opacity="${o.op??1}" ${o.ls?`letter-spacing="${o.ls}"`:''} ${halo}>${esc(s)}</text>`}
function chipD(x,y,label,o={}){
  const sz=o.size||30, w=o.w||label.length*sz*.6+56, h=sz*1.85;
  return `<g opacity="${o.op??1}" transform="translate(${x} ${y}) scale(${o.sc??1})"><rect x="${-w/2}" y="${-h/2}" width="${w}" height="${h}" rx="${h/2}" fill="${o.bg||'rgba(18,26,51,.92)'}" stroke="${o.stroke||'rgba(103,232,249,.35)'}" stroke-width="2.5"/>`+
    T2(0,sz*.36,label,{size:sz,w:o.fw||800,fill:o.fill||D.ink,ls:o.ls})+'</g>';
}
function shake(t,t0,a=14,d=.35){ if(t<t0||t>t0+d) return [0,0]; const k=Math.exp(-(t-t0)*10); return [a*k*Math.sin((t-t0)*95), a*.7*k*Math.cos((t-t0)*77)]; }
// ----------------------------------------------------------------- icons
function bars(x,y,s,level,col=D.ink,dim='rgba(255,255,255,.18)'){ // bottom-left at x,y
  let g=''; for(let i=0;i<4;i++){const h=(8+i*7)*s, on=clamp(level-i); g+=`<rect x="${x+i*9*s}" y="${y-h}" width="${6*s}" height="${h}" rx="${1.5*s}" fill="${dim}"/>`;
    if(on>0) g+=`<rect x="${x+i*9*s}" y="${y-h}" width="${6*s}" height="${h}" rx="${1.5*s}" fill="${col}" opacity="${on}"/>`;}
  return g;
}
function phoneD(cx,cy,w,st={},op=1){
  const h=w*2.05, x=cx-w/2, y=cy-h/2, r=w*.15, s=w/400, sx=x+12*s, sy=y+12*s, sw=w-24*s, sh=h-24*s;
  let g=`<g opacity="${op}"><rect x="${x+10*s}" y="${y+24*s}" width="${w}" height="${h}" rx="${r}" fill="#000" opacity=".45"/>`+
    `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="url(#rim)"/>`+
    `<rect x="${sx}" y="${sy}" width="${sw}" height="${sh}" rx="${r*.82}" fill="${st.screen||'#0B1124'}"/>`;
  const clip=`phc${Math.round(cx)}${Math.round(cy)}`;
  g+=`<clipPath id="${clip}"><rect x="${sx}" y="${sy}" width="${sw}" height="${sh}" rx="${r*.82}"/></clipPath><g clip-path="url(#${clip})">`;
  const md=st.mode||'map';
  if(md==='map'){
    g+=`<rect x="${sx}" y="${sy}" width="${sw}" height="${sh}" fill="#0E1730"/>`;
    for(let i=0;i<9;i++){const yy=sy+60*s+i*86*s+((i*37)%23)*s; g+=`<line x1="${sx}" y1="${yy}" x2="${sx+sw}" y2="${yy+(hh(i)-.5)*60*s}" stroke="#1C2A4C" stroke-width="${(i%3?6:12)*s}"/>`;}
    for(let i=0;i<5;i++){const xx=sx+40*s+i*80*s; g+=`<line x1="${xx}" y1="${sy}" x2="${xx+(hh(i,3)-.5)*80*s}" y2="${sy+sh}" stroke="#1C2A4C" stroke-width="${(i%2?6:12)*s}"/>`;}
    g+=`<rect x="${sx+210*s}" y="${sy+250*s}" width="${120*s}" height="${90*s}" rx="${12*s}" fill="#173322" opacity=".9"/>`;
    const route=[[sx+90*s,sy+sh-90*s],[sx+90*s,sy+520*s],[sx+260*s,sy+470*s],[sx+260*s,sy+300*s]];
    g+=`<polyline points="${route.map(p=>p.join(',')).join(' ')}" fill="none" stroke="${st.offline?'#46506B':D.cyan}" stroke-width="${9*s}" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="${2*s} ${16*s}" opacity=".95"/>`;
    const pin=route[3]; g+=`<g transform="translate(${pin[0]} ${pin[1]-30*s})"><path d="M0 ${30*s} C ${-30*s} ${-2*s}, ${-24*s} ${-34*s}, 0 ${-34*s} C ${24*s} ${-34*s}, ${30*s} ${-2*s}, 0 ${30*s} Z" fill="${D.red}"/><circle cx="0" cy="${-12*s}" r="${9*s}" fill="#fff"/></g>`;
    g+=`<rect x="${pin[0]-118*s}" y="${pin[1]-122*s}" width="${236*s}" height="${44*s}" rx="${22*s}" fill="#fff"/>`+T2(pin[0],pin[1]-92*s,'Jantar Mantar',{size:24*s,w:800,fill:'#111'});
    const p=along(route,st.walk??0); g+=`<circle cx="${p[0]}" cy="${p[1]}" r="${26*s}" fill="${D.cyan}" opacity=".25"/><circle cx="${p[0]}" cy="${p[1]}" r="${13*s}" fill="${st.offline?'#9AA3B8':D.cyan}" stroke="#fff" stroke-width="${4*s}"/>`;
    // search bar
    g+=`<rect x="${sx+24*s}" y="${sy+92*s}" width="${sw-48*s}" height="${60*s}" rx="${30*s}" fill="#1A2546"/>`+T2(sx+60*s,sy+131*s,'Jantar Mantar, New Delhi',{size:22*s,w:500,fill:'#AEB7D0',anchor:'start'});
    if(st.offline>0){ g+=`<rect x="${sx}" y="${sy}" width="${sw}" height="${sh}" fill="#060915" opacity="${.55*st.offline}"/>`;
      g+=`<g opacity="${st.offline}"><rect x="${sx+30*s}" y="${sy+sh-190*s}" width="${sw-60*s}" height="${84*s}" rx="${18*s}" fill="#2A1320" stroke="${D.red}" stroke-width="${3*s}"/>`+
        T2(cx,sy+sh-140*s,'No internet connection',{size:26*s,w:800,fill:D.red2})+'</g>';}
    if(st.dataX>0){ g+=`<g opacity="${st.dataX}" transform="translate(${cx} ${cy-40*s}) scale(${.6+.4*back(st.dataX)})"><rect x="${-150*s}" y="${-70*s}" width="${300*s}" height="${140*s}" rx="${26*s}" fill="#1B0E18" stroke="${D.red}" stroke-width="${4*s}"/>`+
        T2(0,-12*s,'Mobile Data',{size:30*s,w:800})+T2(0,40*s,'✕  Not working',{size:28*s,w:800,fill:D.red2})+'</g>';}
  }
  if(md==='call'){
    g+=`<rect x="${sx}" y="${sy}" width="${sw}" height="${sh}" fill="url(#callbg)"/>`;
    g+=`<circle cx="${cx}" cy="${sy+300*s}" r="${86*s}" fill="#2B3561"/>`+T2(cx,sy+332*s,'M',{size:88*s,w:800,fill:'#C7D2FE'});
    g+=T2(cx,sy+450*s,'Mummy',{size:46*s,w:800});
    const failed=st.failed||0;
    g+=T2(cx,sy+505*s,'Calling…',{size:28*s,w:500,fill:'#AEB7D0',op:1-failed})+T2(cx,sy+505*s,'Call failed',{size:30*s,w:800,fill:D.red2,op:failed});
    if(!failed){const k=(st.tt||0)%1.2/1.2; g+=`<circle cx="${cx}" cy="${sy+300*s}" r="${(90+70*k)*s}" fill="none" stroke="${D.green2}" stroke-width="${3*s}" opacity="${.6*(1-k)}"/>`;}
    g+=`<circle cx="${cx}" cy="${sy+sh-150*s}" r="${48*s}" fill="${D.red}"/><path d="M${cx-22*s} ${sy+sh-146*s} q ${22*s} ${-16*s} ${44*s} 0" stroke="#fff" stroke-width="${8*s}" fill="none" stroke-linecap="round"/>`;
  }
  if(md==='ring'){ // call working, internet off (shutdown)
    g+=`<rect x="${sx}" y="${sy}" width="${sw}" height="${sh}" fill="url(#callbg)"/>`;
    g+=`<circle cx="${cx}" cy="${sy+280*s}" r="${80*s}" fill="#1F4D3A"/>`+T2(cx,sy+308*s,'M',{size:80*s,w:800,fill:'#BBF7D0'});
    g+=T2(cx,sy+420*s,'Mummy',{size:44*s,w:800})+T2(cx,sy+470*s,'00:'+String(Math.floor((st.tt||0)%60)).padStart(2,'0'),{size:30*s,w:700,fill:D.green2});
    const k=(st.tt||0)%1/1; g+=`<circle cx="${cx}" cy="${sy+280*s}" r="${(84+60*k)*s}" fill="none" stroke="${D.green2}" stroke-width="${3*s}" opacity="${.6*(1-k)}"/>`;
    g+=`<rect x="${sx+30*s}" y="${sy+sh-260*s}" width="${sw-60*s}" height="${70*s}" rx="${16*s}" fill="#2A1320" stroke="${D.red}" stroke-width="${3*s}"/>`+T2(cx,sy+sh-215*s,'Internet ✕',{size:28*s,w:800,fill:D.red2});
  }
  if(md==='noise'){ // jammer: can't hear
    g+=`<rect x="${sx}" y="${sy}" width="${sw}" height="${sh}" fill="#0B1124"/>`;
    g+=T2(cx,sy+260*s,'No Service',{size:36*s,w:800,fill:D.red2});
    g+=T2(cx,sy+330*s,'Call ✕  SMS ✕',{size:26*s,w:700,fill:'#AEB7D0'})+T2(cx,sy+372*s,'Internet ✕',{size:26*s,w:700,fill:'#AEB7D0'});
  }
  // static
  if(st.static>0){ const fr=Math.floor((st.tt||0)*30); for(let i=0;i<70;i++){const a=hh(fr,i),b=hh(fr+7,i),c=hh(fr+3,i); g+=`<rect x="${sx+a*sw}" y="${sy+b*sh}" width="${(6+c*40)*s}" height="${3*s}" fill="${c>.5?'#fff':'#9AA3B8'}" opacity="${st.static*(.25+.5*c)}"/>`;} }
  // glitch slices
  if(st.glitch>0){ const fr=Math.floor((st.tt||0)*30); for(let i=0;i<7;i++){const yy=sy+hh(fr,i)*sh, hgt=(8+hh(fr,i+9)*40)*s, dx=(hh(fr,i+3)-.5)*60*s*st.glitch;
      g+=`<rect x="${sx+dx}" y="${yy}" width="${sw}" height="${hgt}" fill="${i%2?D.cyan:D.red}" opacity="${.28*st.glitch}"/>`;} }
  g+='</g>';
  // status bar
  const by=sy+46*s;
  g+=T2(sx+46*s,by,'7:42',{size:22*s,w:800,anchor:'start'});
  g+=`<rect x="${cx-62*s}" y="${sy+18*s}" width="${124*s}" height="${36*s}" rx="${18*s}" fill="#000"/>`;
  const lv=st.bars??4; g+=bars(sx+sw-150*s,by+2*s,1.15*s,lv,lv<1?D.red2:'#fff');
  if(lv>=3.5) g+=T2(sx+sw-96*s,by,'5G',{size:20*s,w:800,anchor:'start'}); else if(lv<.5) g+=T2(sx+sw-96*s,by,'SOS',{size:17*s,w:800,anchor:'start',fill:D.red2});
  g+=`<rect x="${sx+sw-62*s}" y="${by-15*s}" width="${36*s}" height="${17*s}" rx="${4*s}" fill="none" stroke="#fff" stroke-width="${2*s}"/><rect x="${sx+sw-59*s}" y="${by-12*s}" width="${22*s}" height="${11*s}" rx="${2*s}" fill="#fff"/>`;
  return g+'</g>';
}
function tower(x,base,h,o={}){
  const top=base-h, w=h*.28, op=o.op??1, col=o.col||'#9FB0D6'; let g=`<g opacity="${op}">`;
  g+=`<path d="M${x-w/2} ${base} L${x-6} ${top+40} M${x+w/2} ${base} L${x+6} ${top+40}" stroke="${col}" stroke-width="7" stroke-linecap="round"/>`;
  const n=7; for(let i=0;i<n;i++){const y1=lerp(base,top+40,i/n), y2=lerp(base,top+40,(i+1)/n), a=lerp(w/2,6,i/n), b=lerp(w/2,6,(i+1)/n);
    g+=`<path d="M${x-a} ${y1} L${x+b} ${y2} M${x+a} ${y1} L${x-b} ${y2} M${x-b} ${y2} L${x+b} ${y2}" stroke="${col}" stroke-width="3" opacity=".75"/>`;}
  g+=`<line x1="${x}" y1="${top+40}" x2="${x}" y2="${top-10}" stroke="${col}" stroke-width="6"/>`;
  for(const d of [-1,1]) g+=`<rect x="${x+d*22-7}" y="${top+20}" width="14" height="70" rx="4" fill="#DCE5FA"/>`;
  g+=`<rect x="${x-7}" y="${top+5}" width="14" height="70" rx="4" fill="#DCE5FA"/>`;
  const blink=o.t!==undefined?(Math.floor(o.t*1.6)%2?1:.25):1;
  g+=`<circle cx="${x}" cy="${top-14}" r="20" fill="${D.red}" opacity="${.25*blink}"/><circle cx="${x}" cy="${top-14}" r="8" fill="${D.red2}" opacity="${blink}"/>`;
  if(o.label) g+=T2(x,base+52,o.label,{size:30,w:800,fill:D.mute,halo:D.sky0});
  return g+'</g>';
}
function waves(x,y,t,col,dir=1,n=3,op=1,sz=1){ // arcs radiating
  let g=''; for(let i=0;i<n;i++){const k=((t*.9+i/n)%1); const r=(30+120*k)*sz; const a=dir>0?-35:145, b=dir>0?35:215;
    const p1=[x+r*Math.cos(a*Math.PI/180),y+r*Math.sin(a*Math.PI/180)], p2=[x+r*Math.cos(b*Math.PI/180),y+r*Math.sin(b*Math.PI/180)];
    g+=`<path d="M${p1[0]} ${p1[1]} A ${r} ${r} 0 0 1 ${p2[0]} ${p2[1]}" fill="none" stroke="${col}" stroke-width="${6*sz}" stroke-linecap="round" opacity="${op*(1-k)}"/>`;}
  return g;
}
function bubble(x,y,text,o={}){
  const sz=o.size||32, w=text.length*sz*.56+60, h=sz*2.1, op=o.op??1, sc=o.sc??1, col=o.col||D.cyan, tail=o.tail||'left';
  const tx=tail==='left'?-w/2+40:w/2-40;
  return `<g opacity="${op}" transform="translate(${x} ${y}) scale(${sc})"><rect x="${-w/2}" y="${-h/2}" width="${w}" height="${h}" rx="${h/2}" fill="${o.bg||'#F8FAFF'}" stroke="${col}" stroke-width="4"/>`+
    `<path d="M${tx-14} ${h/2-2} L${tx+(tail==='left'?-10:10)} ${h/2+28} L${tx+14} ${h/2-2} Z" fill="${o.bg||'#F8FAFF'}" stroke="${col}" stroke-width="4" stroke-linejoin="round"/><rect x="${tx-16}" y="${h/2-8}" width="32" height="8" fill="${o.bg||'#F8FAFF'}"/>`+
    T2(0,sz*.36,text,{size:sz,w:800,fill:o.fill||'#0B1124'})+'</g>';
}
function doc(x,y,s,stamp,op=1){
  let g=`<g opacity="${op}" transform="translate(${x} ${y}) scale(${s})"><rect x="-70" y="-90" width="140" height="180" rx="12" fill="#EEF2FF"/><path d="M40 -90 L70 -60 L40 -60 Z" fill="#C7D2FE"/>`;
  for(let i=0;i<6;i++) g+=`<rect x="-48" y="${-56+i*22}" width="${i==0?70:96-(i%2)*24}" height="8" rx="4" fill="#A5B4FC" opacity=".8"/>`;
  if(stamp>0) g+=`<g transform="translate(6 46) rotate(-14) scale(${lerp(1.8,1,out(stamp))})" opacity="${clamp(stamp*3)}"><rect x="-58" y="-22" width="116" height="44" rx="8" fill="none" stroke="${D.red}" stroke-width="6"/>`+T2(0,13,'ORDER',{size:30,w:800,fill:D.red})+'</g>';
  return g+'</g>';
}
function building(x,y,s,op=1,lit=1){
  let g=`<g opacity="${op}" transform="translate(${x} ${y}) scale(${s})"><rect x="-80" y="-110" width="160" height="220" rx="10" fill="#1E2A4D" stroke="#3B4A78" stroke-width="4"/>`;
  for(let r=0;r<5;r++)for(let c=0;c<3;c++) g+=`<rect x="${-58+c*44}" y="${-88+r*36}" width="28" height="20" rx="3" fill="${D.yellow}" opacity="${(hh(r,c)>.35?.85:.2)*lit}"/>`;
  g+=`<rect x="-20" y="72" width="40" height="38" fill="#0B1124"/>`;
  return g+'</g>';
}
function toggle(x,y,label,on,o={}){ // on 0..1
  const w=150,h=76, kx=lerp(-w/2+h/2,w/2-h/2,on), col=on>.5?D.green:'#4B556F';
  return `<g transform="translate(${x} ${y})" opacity="${o.op??1}">`+T2(0,-70,label,{size:36,w:800,fill:D.ink})+
    `<rect x="${-w/2}" y="${-h/2}" width="${w}" height="${h}" rx="${h/2}" fill="${col}"/><circle cx="${kx}" cy="0" r="${h/2-7}" fill="#fff"/>`+
    T2(0,h/2+50,on>.5?'ON':'OFF',{size:34,w:800,fill:on>.5?D.green2:D.red2})+'</g>';
}
function jammer(x,y,s,op=1,on=0,t=0){
  let g=`<g opacity="${op}" transform="translate(${x} ${y}) scale(${s})">`;
  if(on>0) g+=`<circle cx="0" cy="0" r="170" fill="url(#redglow)" opacity="${on}"/>`;
  for(const ax of [-75,-25,25,75]) g+=`<line x1="${ax}" y1="-60" x2="${ax*1.15}" y2="-175" stroke="#C9D2EA" stroke-width="9" stroke-linecap="round"/><circle cx="${ax*1.15}" cy="-178" r="9" fill="#C9D2EA"/>`;
  g+=`<rect x="-120" y="-70" width="240" height="140" rx="22" fill="#2A2F45" stroke="#4A5274" stroke-width="5"/><rect x="-96" y="-44" width="192" height="40" rx="10" fill="#151A2C"/>`;
  g+=T2(0,-14,'JAMMER',{size:28,w:800,fill:D.red2,ls:3});
  for(let i=0;i<4;i++) g+=`<circle cx="${-60+i*40}" cy="34" r="9" fill="${on>0&&(Math.floor(t*6+i)%2)?D.red2:'#545C7A'}"/>`;
  return g+'</g>';
}
function noiseField(cx,cy,R,t,amt){ // deterministic static ring/field
  if(amt<=0) return ''; const fr=Math.floor(t*30); let g='';
  for(let i=0;i<120;i++){const a=hh(fr,i)*Math.PI*2, r=Math.sqrt(hh(fr+11,i))*R, x=cx+r*Math.cos(a), y=cy+r*Math.sin(a)*.8, w=6+hh(fr+5,i)*26;
    g+=`<rect x="${x}" y="${y}" width="${w}" height="3" fill="${i%3?D.red2:'#fff'}" opacity="${amt*(.25+.6*hh(fr+2,i))}"/>`;}
  for(let i=0;i<3;i++){const k=((t*1.3+i/3)%1); g+=`<circle cx="${cx}" cy="${cy}" r="${40+R*k}" fill="none" stroke="${D.red}" stroke-width="5" stroke-dasharray="6 10" opacity="${amt*.7*(1-k)}"/>`;}
  return g;
}
function resultChip(x,y,label,ok,k,o={}){
  if(k<=0) return ''; const w=o.w||250, col=ok?D.green:D.red;
  return `<g opacity="${clamp(k*2)}" transform="translate(${x} ${y}) scale(${.6+.4*back(k)})"><rect x="${-w/2}" y="-42" width="${w}" height="84" rx="42" fill="${ok?'#0F2A1C':'#2A0F18'}" stroke="${col}" stroke-width="4"/>`+
    `<circle cx="${-w/2+42}" cy="0" r="24" fill="${col}"/>`+T2(-w/2+42,11,ok?'✓':'✕',{size:32,w:800,fill:'#fff'})+T2(22,12,label,{size:34,w:800,fill:'#fff'})+'</g>';
}
function bigWord(lines,x,y,t,t0,o={}){ // kinetic glitch headline
  const dur=o.dur||1.4; if(t<t0-.05||t>t0+dur) return '';
  const k=prog(t,t0,.22), fo=1-prog(t,t0+dur-.3,.3), sc=lerp(1.5,1,out(k)), sz=o.size||130, col=o.col||D.red, gl=Math.max(0,1-prog(t,t0,.5));
  let g=`<g opacity="${clamp(k*3)*fo}" transform="translate(${x} ${y}) scale(${sc}) rotate(${o.rot??-3})">`;
  g+=`<ellipse cx="0" cy="${-sz*.35*(lines.length-1)}" rx="${520}" ry="${sz*.9*lines.length}" fill="url(#scrim)"/>`;
  lines.forEach((s,i)=>{const yy=(i-(lines.length-1)/2)*sz*1.02+sz*.35;
    if(gl>0){g+=T2(-10*gl,yy,s,{size:sz,w:800,fill:D.cyan,op:.7*gl})+T2(10*gl,yy+4*gl,s,{size:sz,w:800,fill:D.red,op:.7*gl});}
    g+=T2(0,yy,s,{size:sz,w:800,fill:i===lines.length-1?col:'#fff',halo:'#05070F',hw:16});});
  return g+'</g>';
}
// ----------------------------------------------------------------- backgrounds
function nightBg(t,op){
  if(op<=0) return ''; let g=`<g opacity="${op}"><rect width="1080" height="1920" fill="url(#night)"/>`;
  for(let i=0;i<70;i++){const x=hh(i)*1080, y=hh(i,1)*900, tw=.4+.6*Math.abs(Math.sin(t*1.5+i)); g+=`<circle cx="${x}" cy="${y}" r="${1+hh(i,2)*1.8}" fill="#fff" opacity="${.5*tw}"/>`;}
  g+=`<circle cx="880" cy="420" r="170" fill="url(#moonglow)"/><circle cx="880" cy="420" r="46" fill="#F4EFD9"/><circle cx="895" cy="411" r="42" fill="#0C1330" opacity=".18"/>`;
  return g+'</g>';
}
function labBg(t,op){
  if(op<=0) return ''; let g=`<g opacity="${op}"><rect width="1080" height="1920" fill="url(#lab)"/>`;
  for(let x=0;x<=1080;x+=60) g+=`<line x1="${x}" y1="0" x2="${x}" y2="1920" stroke="#7DD3FC" stroke-width="1" opacity=".05"/>`;
  for(let y=0;y<=1920;y+=60) g+=`<line x1="0" y1="${y}" x2="1080" y2="${y}" stroke="#7DD3FC" stroke-width="1" opacity=".05"/>`;
  g+=`<circle cx="540" cy="760" r="620" fill="url(#centerglow)"/>`;
  return g+'</g>';
}
function yantra(op,dy=0,dx=0){ // stylised Jantar Mantar (Samrat Yantra) silhouette
  if(op<=0) return ''; let g=`<g opacity="${op}" transform="translate(${dx} ${dy})">`;
  g+=`<path d="M60 1180 A 300 300 0 0 1 360 880 L360 1180 Z" fill="url(#brick)" opacity=".85"/><path d="M1020 1180 A 300 300 0 0 0 720 880 L720 1180 Z" fill="url(#brick)" opacity=".85"/>`;
  g+=`<path d="M100 1180 A 260 260 0 0 1 360 920" fill="none" stroke="#E7A07A" stroke-width="3" opacity=".35"/><path d="M980 1180 A 260 260 0 0 0 720 920" fill="none" stroke="#E7A07A" stroke-width="3" opacity=".35"/>`;
  g+=`<path d="M300 1180 L560 560 L640 560 L640 1180 Z" fill="url(#brick)"/>`;
  for(let i=0;i<20;i++){const k=i/20, x=lerp(300,560,k), y=lerp(1180,560,k); g+=`<rect x="${x}" y="${y-6}" width="22" height="6" fill="#E7A07A" opacity=".35"/>`;}
  g+=`<rect x="556" y="548" width="88" height="16" fill="#8A3A1A"/><path d="M560 560 L640 560" stroke="#F6C29E" stroke-width="3" opacity=".6"/>`;
  for(const ax of [160,920]) g+=`<path d="M${ax-34} 1180 L${ax-34} 1100 A 34 34 0 0 1 ${ax+34} 1100 L${ax+34} 1180 Z" fill="#0A0E1C" opacity=".55"/>`;
  g+=`<rect x="${-dx-20}" y="1176" width="1200" height="760" fill="#070A16"/>`;
  return g+'</g>';
}
function crowd(t,op){
  if(op<=0) return ''; let g=`<g opacity="${op}">`;
  for(let i=0;i<16;i++){const x=20+i*68+hh(i)*20, y=1215+hh(i,2)*30, bob=Math.sin(t*2+i)*4;
    if(hh(i,4)>.55){const px=x+10, py=y-170+bob; g+=`<line x1="${px}" y1="${py+60}" x2="${px}" y2="${y-20}" stroke="#2A2F45" stroke-width="5"/><rect x="${px-48}" y="${py}" width="96" height="62" rx="6" fill="#222842" stroke="#3A4266" stroke-width="3"/>`;
      if(hh(i,6)>.5) g+=T2(px,py+46,'?',{size:42,w:800,fill:'#5D688F'});}
    g+=`<circle cx="${x}" cy="${y-50+bob}" r="26" fill="#0B0F1F"/><path d="M${x-48} ${y+60} Q ${x-46} ${y-20+bob} ${x} ${y-22+bob} Q ${x+46} ${y-20+bob} ${x+48} ${y+60} Z" fill="#0B0F1F"/>`;}
  return g+'</g>';
}
