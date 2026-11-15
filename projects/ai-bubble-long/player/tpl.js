/* AI Bubble player — shot templates. TPL[name](ctx, p, lt, dur, shot, t)
   lt = seconds into the shot, dur = shot length. Everything deterministic. */
(function(){
const {W,H,Y,RED,GRN,CY}=L,E=L.ease,T=L.text,S=L.seg;
const TPL=window.TPL={};
const hdr=(ctx,s,lt,{y=150,px=64,col='#fff'}={})=>{if(!s)return;const p=E.oc(S(lt,0,.4));T(ctx,s,W/2,y-30*(1-p),{px,alpha:p,fill:col,track:4})};
const prog=(lt,dur,a=.05,b=.7)=>E.oc(S(lt,dur*a,dur*b));
const MS={2:'ChatGPT'};

/* ================= image (HF art + code overlays) ================= */
TPL.image=(ctx,p,lt,dur,s)=>{
  if(p.pending||!L.IMG[p.src])return pending(ctx,p,lt,dur,s);
  let crop=p.crop,kb=p.kb||['in','l','out','r'][s.id%4],slt=lt,sd=dur;
  if(p.cuts){const n=p.cuts.length,i=Math.min(n-1,Math.floor(lt/(dur/n)));crop=p.cuts[i];slt=lt-i*dur/n;sd=dur/n;kb=['in','r','l'][i%3]}
  const info=L.art(ctx,p.src,slt,sd,{crop,kb,flip:p.flip,speed:p.speed,freeze:p.freeze,shake:p.shake});
  if(p.freeze!=null&&lt/dur>p.freeze){ctx.save();ctx.globalCompositeOperation='saturation';ctx.fillStyle=`rgba(0,0,0,${.7*S(lt/dur,p.freeze,p.freeze+.05)})`;ctx.fillRect(0,0,W,H);ctx.restore()}
  L.dust(ctx,lt,36,.45);
  for(const o of p.ov||[])OV[o.k]&&OV[o.k](ctx,o,lt,dur,info,s);
  if(p.kw)L.hilite(ctx,p.kw,W/2,H*.86,{px:84,p:S(lt,.2,.5)});
};
function pending(ctx,p,lt,dur,s){
  L.bg(ctx,lt,{hue:'grey',src:'style_frame',alpha:.35});
  L.card(ctx,W/2-620,H/2-250,1240,500,{fill:'rgba(10,12,18,.82)',r:36});
  T(ctx,`ART PENDING · s${String(s.id).padStart(3,'0')}`,W/2,H/2-170,{px:40,fill:Y,track:6});
  ctx.save();L.font(ctx,40,500);const lines=L.wrap(ctx,s.visual||'',1100).slice(0,6);
  lines.forEach((ln,i)=>T(ctx,ln,W/2,H/2-80+i*58,{px:40,w:500,fill:'#e6e6e6'}));ctx.restore();
  for(const o of p.ov||[])if(['tag','stamp'].includes(o.k))OV[o.k](ctx,o,lt,dur,null,s);
}
/* ---------- overlays on art ---------- */
const OV={
  stamp:(ctx,o,lt,dur,info)=>{const a=(o.at||.5)*dur;L.stamp(ctx,o.text,o.x*W,o.y*H,S(lt,a,a+.22),{px:o.small?110:170})},
  tag:(ctx,o,lt,dur)=>{const a=(o.at||.25)*dur;L.chip(ctx,o.text,o.x*W,o.y*H,{px:54,p:S(lt,a,a+.35),bg:o.red?RED:Y,fg:o.red?'#fff':'#111',rot:-.04})},
  logo:(ctx,o,lt,dur,info)=>{const [x,y,w,h]=L.map(o.rect,info);ctx.save();ctx.globalAlpha=E.oc(S(lt,.15,.6));
    ctx.fillStyle=o.name==='Google'?'rgba(255,255,255,.95)':'rgba(10,20,50,.6)';ctx.shadowColor='rgba(255,255,255,.5)';ctx.shadowBlur=30;L.rr(ctx,x,y,w,h,10);ctx.fill();ctx.restore();
    ctx.save();ctx.globalAlpha=E.oc(S(lt,.3,.8));L.logo(ctx,o.name,x+w/2,y+h/2,h*.55,{light:o.name!=='Google'});ctx.restore()},
  alarm:(ctx,o,lt)=>{ctx.save();ctx.globalCompositeOperation='lighter';const a=.25+.25*Math.sin(lt*14);const g=ctx.createRadialGradient(W*.5,0,10,W*.5,0,W*.7);
    g.addColorStop(0,`rgba(255,40,40,${a})`);g.addColorStop(1,'rgba(255,0,0,0)');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);ctx.restore()},
  phone:(ctx,o,lt,dur)=>{const p=E.back(S(lt,.2,.6));ctx.save();ctx.translate(o.x*W,o.y*H+(1-p)*500);ctx.rotate(-.12);const r=L.phone(ctx,-150,-280,300,560);
    ctx.fillStyle='#212121';ctx.fillRect(...r);L.logo(ctx,'ChatGPT',0,-150,50);for(let i=0;i<4;i++){ctx.fillStyle=i%2?'#2f2f2f':'#10a37f55';L.rr(ctx,-110+(i%2?40:0),-60+i*70,180,50,18);ctx.fill()}ctx.restore()},
  namecards:(ctx,o,lt,dur)=>{o.items.forEach((n,i)=>{const a=dur*(.3+i*.2),p=E.oc(S(lt,a,a+.5));if(p<=0)return;ctx.save();
    ctx.translate(L.lerp(i?W+300:-300,W*(.36+i*.28),p),H*.62-80*Math.sin(p*Math.PI));ctx.rotate((1-p)*(i?2:-2)+(i?.08:-.08));
    L.card(ctx,-210,-80,420,160,{fill:'#f7f3e8',r:12});L.logo(ctx,n,0,0,70,{light:false});ctx.restore()})},
  speedlines:(ctx,o,lt)=>{ctx.save();ctx.strokeStyle='rgba(255,255,255,.55)';ctx.lineCap='round';for(let i=0;i<26;i++){const y=L.hash(i,51)*H,len=200+L.hash(i,52)*500,x=((L.hash(i,53)*W*2-lt*2600)%(W*1.6)+W*1.6)%(W*1.6)-200;
    ctx.lineWidth=2+L.hash(i,54)*5;ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x+len,y);ctx.stroke()}ctx.restore()},
  confetti:(ctx,o,lt)=>L.confetti(ctx,lt,{cheques:o.cheques}),
  plaque:(ctx,o,lt,dur,info)=>{const [x,y,w,h]=L.map(o.rect,info);ctx.save();ctx.globalAlpha=E.oc(S(lt,.1,.5));
    L.font(ctx,h*.42,800);const tw=ctx.measureText(o.text).width;const k=Math.min(1,w*.9/tw);T(ctx,o.text,x+w/2,y+h/2,{px:h*.42*k,fill:'#3b2a10'});ctx.restore();
    if(lt>dur*.4){ctx.save();ctx.globalAlpha=E.oc(S(lt,dur*.4,dur*.6));L.chip(ctx,o.text,W*.5,H*.16,{px:56});ctx.restore()}},
  slide:(ctx,o,lt,dur,info)=>{const [x,y,w,h]=L.map(o.rect,info);ctx.save();ctx.beginPath();ctx.rect(x,y,w,h);ctx.clip();
    ctx.fillStyle='#f4f7fb';ctx.fillRect(x,y,w,h);
    if(o.mode==='dogwalk'){T(ctx,'DogWalk',x+w/2,y+h*.32,{px:h*.2,fill:'#1f6feb'});T(ctx,'AI that walks your dog',x+w/2,y+h*.55,{px:h*.08,w:600,fill:'#334'});
      ctx.save();ctx.translate(x+w/2,y+h*.78);for(let i=0;i<5;i++){ctx.fillStyle='#8a5a2b';ctx.beginPath();ctx.ellipse(-w*.2+i*w*.1,Math.sin(i)*6,10,14,0,0,7);ctx.fill()}ctx.restore()}
    else{ // ML route map
      ctx.strokeStyle='#d5dbe5';ctx.lineWidth=6;for(let i=0;i<7;i++){ctx.beginPath();ctx.moveTo(x,y+i*h/6);ctx.lineTo(x+w,y+i*h/6+30);ctx.stroke();ctx.beginPath();ctx.moveTo(x+i*w/6,y);ctx.lineTo(x+i*w/6-40,y+h);ctx.stroke()}
      const pts=[[.1,.85],[.3,.7],[.28,.45],[.55,.4],[.6,.2],[.9,.15]],p=S(lt,.2,dur*.8);ctx.strokeStyle='#00d3ff';ctx.shadowColor='#00d3ff';ctx.shadowBlur=20;ctx.lineWidth=10;ctx.beginPath();
      pts.forEach((q,i)=>{if(i/(pts.length-1)<=p+.01)(i?ctx.lineTo:ctx.moveTo).call(ctx,x+q[0]*w,y+q[1]*h)});ctx.stroke();ctx.shadowBlur=0;
      L.chip(ctx,'ML',x+w*.55,y+h*.4-40,{px:h*.08,bg:'#00d3ff',p:S(lt,.4,.8)})}
    ctx.restore()},
  drawline:(ctx,o,lt,dur)=>{const p=E.io(S(lt,dur*.15,dur*.6));ctx.save();ctx.strokeStyle='#1d4ed8';ctx.lineWidth=14;ctx.lineCap='round';ctx.shadowColor='rgba(29,78,216,.6)';ctx.shadowBlur=14;
    ctx.beginPath();ctx.moveTo(W*.55,H*.62);ctx.lineTo(W*.55+W*.18*p,H*.62-H*.45*p);ctx.stroke();ctx.restore()},
  spot:(ctx,o,lt)=>{ctx.save();const g=ctx.createRadialGradient(W*.5,H*.45,120,W*.5,H*.45,560);g.addColorStop(0,'rgba(0,0,0,0)');g.addColorStop(1,`rgba(0,0,0,${.75*E.oc(S(lt,0,.5))})`);ctx.fillStyle=g;ctx.fillRect(0,0,W,H);ctx.restore()},
  bubble:(ctx,o,lt,dur)=>{const p=E.back(S(lt,dur*.3,dur*.3+.35));if(p<=0)return;ctx.save();ctx.translate(o.x*W,o.y*H);ctx.scale(p*.6,p*.6);L.card(ctx,-240,-80,480,160,{r:60});
    ctx.fillStyle='#fff';ctx.beginPath();ctx.moveTo(-60,70);ctx.lineTo(-100,140);ctx.lineTo(0,74);ctx.fill();T(ctx,o.text,0,0,{px:64,w:700,fill:'#222'});ctx.restore()},
  mosquito:(ctx,o,lt)=>{const pts=[];for(let k=0;k<40;k++){const tt=lt-k*.04;pts.push([W*.55+Math.cos(tt*2.2)*260+Math.sin(tt*5.3)*60,H*.42+Math.sin(tt*2.9)*150])}
    ctx.save();ctx.setLineDash([6,14]);ctx.strokeStyle='rgba(255,255,255,.6)';ctx.lineWidth=3;ctx.beginPath();pts.forEach((q,i)=>i?ctx.lineTo(...q):ctx.moveTo(...q));ctx.stroke();ctx.setLineDash([]);
    const [x,y]=pts[0];ctx.fillStyle='#111';ctx.beginPath();ctx.ellipse(x,y,14,6,.3,0,7);ctx.fill();ctx.fillStyle='rgba(220,230,255,.7)';
    const f=Math.sin(lt*90)*.5+.5;ctx.beginPath();ctx.ellipse(x-4,y-10*f-4,12,5,-.5,0,7);ctx.ellipse(x+6,y-10*f-4,12,5,.5,0,7);ctx.fill();ctx.restore()},
  logorow:(ctx,o,lt,dur)=>{o.items.forEach((n,i)=>{const a=.2+i*.18,p=E.back(S(lt,a,a+.4));if(p<=0)return;ctx.save();const x=W*(.2+i*.2),y=H*.12;ctx.translate(x,y);ctx.scale(p,p);
    L.card(ctx,-150,-48,300,96,{fill:'rgba(255,255,255,.92)',r:48});L.logo(ctx,n,0,0,46,{light:false});ctx.restore()})},
  spotmove:(ctx,o,lt,dur)=>{const n=o.n||4,k=lt/dur*n,i=Math.min(n-1,Math.floor(k)),f=E.io(L.clamp((k-i)*3));const x=W*(.2+.2*L.lerp(Math.max(0,i-1),i,i?f:1));
    ctx.save();const g=ctx.createRadialGradient(x,H*.45,100,x,H*.45,520);g.addColorStop(0,'rgba(0,0,0,0)');g.addColorStop(1,'rgba(0,0,0,.7)');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);ctx.restore()},
};

/* ================= windows (hook: world vs India) ================= */
TPL.windows=(ctx,p,lt,dur)=>{L.bg(ctx,lt,{hue:'navy'});const n=p.srcs.length,ww=560,hh=380,z=1+.08*S(lt,dur*.7,dur);
  ctx.save();ctx.translate(W/2,H/2);ctx.scale(z,z);ctx.translate(-W/2,-H/2);
  p.srcs.forEach((src,i)=>{const a=i*dur*.22,q=E.back(S(lt,a,a+.35));if(q<=0)return;const x=W/2+(i-1)*620,y=H/2+(i===1?-20:20);
    ctx.save();ctx.translate(x,y);ctx.scale(q,q);ctx.rotate((i-1)*.03);
    L.card(ctx,-ww/2-10,-hh/2-52,ww+20,hh+62,{fill:'#e9edf3',r:16});['#ff5f57','#febc2e','#28c840'].forEach((c,k)=>{ctx.fillStyle=c;ctx.beginPath();ctx.arc(-ww/2+18+k*28,-hh/2-26,9,0,7);ctx.fill()});
    T(ctx,p.labels[i],ww/2-80,-hh/2-26,{px:24,fill:'#445'});
    ctx.beginPath();ctx.rect(-ww/2,-hh/2,ww,hh);ctx.clip();const im=L.IMG[src];
    if(im){const k=1.06+.06*S(lt,a,dur);ctx.drawImage(im,-ww*k/2,-hh*k/2,ww*k,hh*k)}ctx.restore()});
  ctx.restore();L.dust(ctx,lt,20,.4)};

/* ================= title ================= */
TPL.title=(ctx,p,lt,dur)=>{const st=p.style||'neon';
  if(st==='black'||st==='tv'){ctx.fillStyle='#000';ctx.fillRect(0,0,W,H)}else L.bg(ctx,lt,{hue:st==='neon'||st==='sparkle'?'purple':st==='crack'?'grey':'red'});
  const pin=E.back(S(lt,.05,.5));
  if(st==='neon'){const fl=lt<.6?(L.hash(Math.floor(lt*20),3)>.4?1:.3):1;
    if(p.sub)T(ctx,p.sub,W/2,H/2-150,{px:54,fill:'#fff',alpha:E.oc(S(lt,0,.3)),track:12});
    T(ctx,p.text,W/2,H/2+30,{px:260,fam:'Anton',w:400,fill:'#ffe9ff',glow:60*fl,gc:'#ff3df2',stroke:6,sc:'#ff3df2',alpha:fl*S(lt,0,.15)});
    L.dust(ctx,lt,40,.6)}
  else if(st==='black'){const n=Math.floor(p.text.length*S(lt,.1,Math.min(dur*.6,1.6)));T(ctx,p.text.slice(0,n),W/2,H/2,{px:96,w:700});
    if(Math.floor(lt*2)%2&&n<p.text.length+1){ctx.save();L.font(ctx,96,700);const tw=ctx.measureText(p.text.slice(0,n)).width;ctx.fillStyle='#fff';ctx.fillRect(W/2+tw/2+10,H/2-50,8,100);ctx.restore()}}
  else if(st==='shake'){const k=L.shakeAmt(lt,dur,.6,.05);ctx.save();ctx.translate(...k);ctx.translate(W/2,H/2);ctx.scale(pin,pin);L.hilite(ctx,p.text,0,0,{px:170,fam:'Anton',w:400});ctx.restore()}
  else if(st==='tilt'){ctx.save();ctx.translate(W/2,H/2);ctx.rotate(-.12*E.oc(S(lt,0,.4)));const z=1+.25*E.ic(S(lt,0,dur));ctx.scale(z,z);T(ctx,p.text,0,0,{px:180,fam:'Anton',w:400,fill:'#fff',glow:40,gc:RED});ctx.restore()}
  else if(st==='curtain'){T(ctx,p.text,W/2,H/2,{px:200,fam:'Anton',w:400,fill:Y,glow:50});const o=E.io(S(lt,.1,dur*.6));
    for(const sd of[-1,1]){ctx.save();const x=sd<0?-o*W*.5:W/2+o*W*.5;const g=ctx.createLinearGradient(x,0,x+W/2,0);for(let i=0;i<=8;i++)g.addColorStop(i/8,i%2?'#7a0d16':'#a5121f');ctx.fillStyle=g;ctx.fillRect(x,0,W/2,H);ctx.restore()}}
  else if(st==='crack'){T(ctx,p.text,W/2,H/2,{px:190,fam:'Anton',w:400,fill:'#fff',alpha:E.oc(S(lt,.3,.8))});const q=S(lt,0,dur*.5);
    ctx.save();ctx.strokeStyle='rgba(230,240,255,.85)';ctx.lineWidth=3;for(let c=0;c<14;c++){const a=L.hash(c,61)*7;let x=W*.46,y=H*.44;ctx.beginPath();ctx.moveTo(x,y);
      for(let k=0;k<12*q;k++){x+=Math.cos(a+L.noise(k,c)*.6)*90;y+=Math.sin(a+L.noise(k,c)*.6)*90;ctx.lineTo(x,y)}ctx.stroke()}
    for(let r=1;r<4;r++){ctx.beginPath();for(let c=0;c<=14;c++){const a=c/14*7;ctx.lineTo(W*.46+Math.cos(a)*r*90*q*1.6,H*.44+Math.sin(a)*r*90*q*1.6)}ctx.stroke()}ctx.restore()}
  else if(st==='sparkle'){ctx.save();ctx.translate(W/2,H/2);ctx.scale(pin,pin);T(ctx,p.text,0,0,{px:520,fam:'Anton',w:400,fill:'#fff',glow:80,gc:Y,stroke:10,sc:Y});ctx.restore();
    for(let i=0;i<22;i++){const a=L.hash(i,81)*7,r=300+L.hash(i,82)*350,tw=Math.max(0,Math.sin(lt*6+i*1.7));star(ctx,W/2+Math.cos(a)*r,H/2+Math.sin(a)*r*.6,(16+L.hash(i,83)*30)*tw)}}
  else if(st==='tv'){const off=lt>dur*.82;if(off){const q=S(lt,dur*.82,dur*.88);ctx.fillStyle='#fff';ctx.fillRect(0,H/2-H*(1-q)*.3,W,H*(1-q)*.6+2*(1-q));return}
    L.card(ctx,W/2-640,H/2-380,1280,720,{fill:'#1a1a1a',r:40});ctx.fillStyle='#0d1f2d';ctx.fillRect(W/2-590,H/2-330,1180,620);
    T(ctx,'NEXT:',W/2,H/2-90,{px:70,fill:'#9fd',w:700,track:10});T(ctx,'SEASON FINALE',W/2,H/2+30,{px:150,fam:'Anton',w:400,fill:'#fff',glow:30,gc:'#9fd'});
    ctx.fillStyle='rgba(255,255,255,.05)';for(let y=H/2-330;y<H/2+290;y+=6)ctx.fillRect(W/2-590,y,1180,2)}
};
function star(ctx,x,y,r,col=Y){if(r<=0)return;ctx.save();ctx.fillStyle=col;ctx.shadowColor=col;ctx.shadowBlur=20;ctx.beginPath();ctx.moveTo(x,y-r);ctx.quadraticCurveTo(x,y,x+r,y);ctx.quadraticCurveTo(x,y,x,y+r);ctx.quadraticCurveTo(x,y,x-r,y);ctx.quadraticCurveTo(x,y,x,y-r);ctx.fill();ctx.restore()}

/* ================= map (world pins / timeline) ================= */
TPL.map=(ctx,p,lt,dur)=>{L.bg(ctx,lt,{hue:'navy'});
  if(p.mode==='timeline'){const y=H*.6,x0=W*.12,x1=W*.88,yrs=[2022,2023,2024,2025,2026];ctx.strokeStyle='#fff';ctx.lineWidth=8;ctx.beginPath();ctx.moveTo(x0,y);ctx.lineTo(x0+(x1-x0)*E.oc(S(lt,0,.6)),y);ctx.stroke();
    yrs.forEach((yr,i)=>{const x=L.lerp(x0,x1,i/4),q=S(lt,.1+i*.1,.3+i*.1);ctx.fillStyle='#fff';ctx.globalAlpha=q;ctx.beginPath();ctx.arc(x,y,14,0,7);ctx.fill();T(ctx,''+yr,x,y+80,{px:44,w:700,fill:i===4?Y:'#fff'});ctx.globalAlpha=1});
    const q=E.el(S(lt,.9,1.7)),px=L.lerp(x0,x1,.97),py=y-14-(1-q)*600;ctx.save();ctx.translate(px,py);ctx.fillStyle=RED;ctx.beginPath();ctx.arc(0,-70,48,Math.PI,0);ctx.lineTo(0,0);ctx.closePath();ctx.fill();
    ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(0,-72,18,0,7);ctx.fill();ctx.restore();L.chip(ctx,'YOU ARE HERE',px-140,y-230,{px:46,p:S(lt,1.3,1.7)});return}
  // stylised globe
  const cx=W/2,cy=H*.54,R=380,rot=lt*.25;const g=ctx.createRadialGradient(cx-120,cy-140,40,cx,cy,R);g.addColorStop(0,'#1d4f8f');g.addColorStop(1,'#071a35');
  ctx.fillStyle=g;ctx.beginPath();ctx.arc(cx,cy,R,0,7);ctx.fill();ctx.save();ctx.beginPath();ctx.arc(cx,cy,R,0,7);ctx.clip();
  ctx.strokeStyle='rgba(120,190,255,.25)';ctx.lineWidth=2;for(let i=-3;i<=3;i++){ctx.beginPath();ctx.ellipse(cx,cy+i*R/4,R*Math.cos(Math.asin(i/4)),6,0,0,7);ctx.stroke()}
  for(let i=0;i<8;i++){const a=(i/8*Math.PI+rot)%Math.PI;ctx.beginPath();ctx.ellipse(cx,cy,Math.abs(Math.cos(a))*R,R,0,0,7);ctx.stroke()}
  // landmasses as dotted blobs
  ctx.fillStyle='rgba(120,220,160,.55)';for(let i=0;i<700;i++){const lon=L.hash(i,91)*Math.PI*2,lat=(L.hash(i,92)-.5)*2.4;const c=Math.sin(lon*3+1)*Math.cos(lat*2)+Math.sin(lon*5)*.4;if(c<.2)continue;
    const x=Math.sin(lon+rot)*Math.cos(lat/1.5),z=Math.cos(lon+rot);if(z<0)continue;ctx.beginPath();ctx.arc(cx+x*R,cy+Math.sin(lat/1.5)*R,4,0,7);ctx.fill()}
  ctx.restore();ctx.strokeStyle='#9cc8ff';ctx.lineWidth=4;ctx.beginPath();ctx.arc(cx,cy,R,0,7);ctx.stroke();
  const fz=p.freeze?0:1;for(let i=0;i<26;i++){const lon=L.hash(i,95)*Math.PI*2,lat=(L.hash(i,96)-.5)*1.8,x=Math.sin(lon+rot*fz)*Math.cos(lat/1.5),z=Math.cos(lon+rot*fz);if(z<.05)continue;
    const a=p.freeze?0:i*.07,q=E.back(S(lt,a,a+.3));if(q<=0)continue;const px=cx+x*R,py=cy+Math.sin(lat/1.5)*R;ctx.save();ctx.translate(px,py);ctx.scale(q,q);
    ctx.fillStyle='#10a37f';ctx.beginPath();ctx.arc(0,-34,22,Math.PI,0);ctx.lineTo(0,0);ctx.closePath();ctx.fill();ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(0,-36,8,0,7);ctx.fill();ctx.restore()}
  L.logo(ctx,'ChatGPT',W/2,H*.1,64);
  if(p.freeze){ctx.save();ctx.globalCompositeOperation='saturation';ctx.fillStyle='rgba(0,0,0,.8)';ctx.fillRect(0,0,W,H);ctx.restore();L.stamp(ctx,p.stamp,W/2,H*.55,S(lt,dur*.35,dur*.35+.22),{px:220})}
};

/* ================= balloon ================= */
TPL.balloon=(ctx,p,lt,dur)=>{const m=p.mode;
  const sky=ctx.createLinearGradient(0,0,0,H);sky.addColorStop(0,'#0b1020');sky.addColorStop(.7,m==='tighten'?'#3a1420':'#1a2448');sky.addColorStop(1,'#2b1a2a');ctx.fillStyle=sky;ctx.fillRect(0,0,W,H);
  L.city(ctx,lt,{y:H*.95});
  let r=300,st=0,cr=0,wob=0,x=W/2,y=H*.46,lab='AI';
  if(m==='inflate'){const q=E.io(S(lt,.1,dur*.75));r=L.lerp(40,290,q);st=S(lt,dur*.75,dur);wob=st;y=H*.5;
    if(q<.08){L.card(ctx,W/2-90,y-60,180,120,{r:40});T(ctx,'...',W/2,y-10,{px:70,fill:'#333'})}}
  if(m==='crack'){cr=p.thin?.45*S(lt,.2,dur*.8):S(lt,.1,dur*.7);st=.3;wob=.2}
  if(m==='notch'){const k=Math.floor(S(lt,0,dur)*2.2);r=300+k*28+E.el(L.clamp((lt-k*dur/2.2)*2))*0;st=.3+k*.25;wob=.4}
  if(m==='hold'){st=.4;y+=Math.sin(lt*1.5)*10;if(p.megaphones)wob=.6+.4*Math.sin(lt*6);if(p.browser)x=W*.62}
  if(m==='tighten'){const q=S(lt,0,dur);r=320+40*q;st=.6+q*.8;wob=.15+.2*Math.sin(lt*4)*q;cr=.25}
  const pulse=m==='tighten'?1+.015*Math.sin(lt*7):1;
  if(m!=='inflate'||lt>.1)L.balloon(ctx,x,y,r*pulse,{lt,stretch:st,cracks:cr,label:lab,wob});
  if(m==='inflate'&&p.counter){const q=E.io(S(lt,.1,dur*.75));const v=Math.round(q*7)*1e12*(q<1?q:1);
    const s='$'+L.fmt(Math.floor(p.counter.to*E.ic(q)/1e9)*1e9);T(ctx,s,W/2,H*.88,{px:110,fam:'Anton',w:400,fill:'#fff',stroke:10,sc:'#000',glow:30});
    if(lt>dur*.75)L.hilite(ctx,'7 TRILLION DOLLAR KA GAMBLE',W/2,H*.1,{px:60,p:S(lt,dur*.75,dur*.85)})}
  if(m==='crack'&&!p.thin){for(let i=0;i<30;i++){const k=(lt*1.6+L.hash(i,3))%1,a=-.6+L.hash(i,4)*.5;ctx.fillStyle=`rgba(255,255,255,${.5*(1-k)})`;ctx.beginPath();ctx.arc(x+r*.75+k*300*Math.cos(a),y-r*.3+k*300*Math.sin(a),4+k*14,0,7);ctx.fill()}
    L.chip(ctx,'2024',W*.14,H*.14,{px:52,p:S(lt,.1,.4)})}
  if(m==='notch')['HAAN.','HAAN.'].forEach((s,i)=>L.chip(ctx,s,W*(.22+i*.56),H*.22,{px:60,p:S(lt,i*dur/2.2,i*dur/2.2+.3)}));
  if(p.needle){const nx=x-r-120+Math.sin(lt*2)*30,ny=y+40;ctx.save();ctx.translate(nx,ny);ctx.rotate(.15);ctx.fillStyle='#ccd';ctx.fillRect(-220,-5,220,10);ctx.beginPath();ctx.moveTo(0,-5);ctx.lineTo(40,0);ctx.lineTo(0,5);ctx.fill();ctx.fillStyle=RED;ctx.beginPath();ctx.arc(-220,0,16,0,7);ctx.fill();ctx.restore()}
  if(p.megaphones)for(const sd of[-1,1]){ctx.save();ctx.translate(W/2+sd*720,H*.55);ctx.scale(-sd,1);ctx.fillStyle='#e8e8e8';ctx.beginPath();ctx.moveTo(-60,-30);ctx.lineTo(60,-90);ctx.lineTo(60,90);ctx.lineTo(-60,30);ctx.closePath();ctx.fill();
    ctx.strokeStyle=Y;ctx.lineWidth=6;for(let k=0;k<3;k++){const ph=(lt*2+k/3)%1;ctx.globalAlpha=1-ph;ctx.beginPath();ctx.arc(60,0,40+ph*200,-.6,.6);ctx.stroke()}ctx.restore()}
  if(p.browser){const q=S(lt,dur*.25,dur*.5);ctx.save();ctx.translate(W*.24,H*.48);ctx.rotate(-.05);
    if(q<1){L.card(ctx,-280,-200,560,400,{fill:'#c0c0c0',r:4});ctx.fillStyle='#000080';ctx.fillRect(-276,-196,552,40);T(ctx,'Netscape 1999',-150,-176,{px:26,fill:'#fff'});ctx.fillStyle='#fff';ctx.fillRect(-266,-146,532,330);T(ctx,'dot-com',0,0,{px:70,fill:'#000080',fam:'Courier Prime',w:700})}
    if(q>0)for(let i=0;i<24;i++){const a=L.hash(i,5)*7,d=q*500*L.hash(i,6);ctx.save();ctx.translate(Math.cos(a)*d,Math.sin(a)*d+q*q*300);ctx.rotate(a+q*4);ctx.globalAlpha=1-q;ctx.fillStyle='#c0c0c0';ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(60,10);ctx.lineTo(20,60);ctx.fill();ctx.restore()}
    ctx.restore();if(p.kw)L.hilite(ctx,p.kw,W/2,H*.12,{px:96,p:S(lt,dur*.55,dur*.7)})}
  if(m==='tighten'){const v=ctx.createRadialGradient(x,y,r*1.2,x,y,W*.7);v.addColorStop(0,'rgba(0,0,0,0)');v.addColorStop(1,`rgba(0,0,0,${.3+.4*S(lt,0,dur)})`);ctx.fillStyle=v;ctx.fillRect(0,0,W,H)}
  L.dust(ctx,lt,30,.4)};

/* ================= calendar ================= */
TPL.calendar=(ctx,p,lt,dur)=>{L.bg(ctx,lt,{hue:'navy'});
  if(p.mode==='app'){const r=L.phone(ctx,W/2-260,90,520,920,{dark:false});ctx.fillStyle='#fff';ctx.fillRect(...r);T(ctx,'Today',r[0]+40,r[1]+90,{px:48,align:'left',fill:'#111'});
    for(let h=0;h<7;h++){const yy=r[1]+170+h*100;ctx.fillStyle='#e5e7eb';ctx.fillRect(r[0]+110,yy,r[2]-130,2);T(ctx,`${h+1}:00 AM`,r[0]+20,yy,{px:22,align:'left',fill:'#888',w:500})}
    const q=E.back(S(lt,.4,.8));ctx.save();ctx.translate(r[0]+r[2]/2+40,r[1]+170+2*100+50);ctx.scale(q,q);L.card(ctx,-180,-48,360,96,{fill:'#7c3aed',r:16});T(ctx,'Team meeting · 3:00 AM',0,0,{px:28,fill:'#fff',w:700});ctx.restore();
    if(q>0){L.chip(ctx,'✦ AI suggests',W/2+300,H*.3,{px:44,bg:'#7c3aed',fg:'#fff',p:S(lt,.6,1)});star(ctx,W/2+460,H*.22,30*Math.abs(Math.sin(lt*4)))}return}
  const pages=p.mode==='fast'?p.years.map(y=>({m:'DEC',d:31,y})):[{m:p.month,d:p.day,y:p.year,wd:p.wd}];
  const n=pages.length,per=dur/n;const i=Math.min(n-1,Math.floor(lt/per)),pl=lt-i*per,spd=p.mode==='fast'?1+i:1;
  const page=(pg,x,y,rot,sc=1)=>{ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.scale(sc,sc);L.card(ctx,-300,-340,600,680,{fill:'#fbfaf6',r:22});
    ctx.fillStyle=RED;L.rr(ctx,-300,-340,600,170,22);ctx.fill();ctx.fillRect(-300,-200,600,30);T(ctx,pg.m+' '+pg.y,0,-260,{px:74,fill:'#fff',w:800,track:4});
    for(let k=0;k<6;k++){ctx.fillStyle='#2a2a2a';ctx.beginPath();ctx.arc(-220+k*88,-340,12,0,7);ctx.fill()}
    if(pg.d!=null)T(ctx,''+pg.d,0,40,{px:300,fam:'Anton',w:400,fill:'#1a1a1a'});else T(ctx,pg.m,0,40,{px:190,fam:'Anton',w:400,fill:'#1a1a1a'});
    if(pg.wd)T(ctx,pg.wd,0,250,{px:60,w:800,fill:RED,track:8});ctx.restore()};
  // flipping pages behind
  const fl=E.io(S(pl,0,Math.min(.5,per*.4)/spd));
  page(pages[i],W/2,H/2+20,0);
  if(fl<1){const prev={m:'—',d:p.mode==='fast'?null:(p.day?p.day-1:null),y:pages[i].y-(p.mode==='fast'?1:0)};ctx.save();ctx.translate(W/2,H/2-320);ctx.scale(1,Math.cos(fl*Math.PI/2));ctx.translate(-W/2,-(H/2-320));
    page({m:p.mode==='fast'?'DEC':'NOV',d:p.mode==='fast'?31:(p.day?p.day-1:15),y:prev.y},W/2,H/2+20,0);ctx.restore()}
  if(p.mode==='fast'){for(let k=0;k<12;k++){const ph=(lt*1.5*(1+i)+k/12)%1;ctx.save();ctx.translate(W/2+(L.hash(k,1)-.5)*900*ph,H/2-200-ph*500);ctx.rotate(ph*6+k);ctx.globalAlpha=1-ph;
    ctx.fillStyle='#fbfaf6';ctx.fillRect(-60,-70,120,140);ctx.fillStyle=RED;ctx.fillRect(-60,-70,120,34);ctx.restore()}
    L.chip(ctx,['2029?','2030?','2031?'][i],W*.8,H*.2,{px:64,p:S(pl,0,.3)})}
};

/* ================= launch / tweet / notif ================= */
TPL.launch=(ctx,p,lt,dur)=>{ctx.fillStyle='#0a0a0a';ctx.fillRect(0,0,W,H);const gl=E.oc(S(lt,0,.6));
  const g=ctx.createRadialGradient(W/2,H/2,50,W/2,H/2,900);g.addColorStop(0,`rgba(16,163,127,${.35*gl})`);g.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
  ctx.save();ctx.globalAlpha=gl;L.logo(ctx,'OpenAI',W/2,H*.2,70);ctx.restore();
  const q=E.back(S(lt,.25,.7));ctx.save();ctx.translate(W/2,H*.45-(1-q)*200);ctx.globalAlpha=L.clamp(q);T(ctx,'ChatGPT',0,0,{px:220,w:800,fill:'#fff',glow:50,gc:'#10a37f'});ctx.restore();
  const s=p.type,n=Math.floor(s.length*S(lt,.7,Math.max(1.2,dur*.85)));T(ctx,s.slice(0,n)+(Math.floor(lt*3)%2?'|':''),W/2,H*.68,{px:52,fam:'Courier Prime',w:700,fill:'#d1fae5'});
  T(ctx,p.time,W/2,H*.78,{px:36,fill:'#7dd3c0',alpha:S(lt,1,1.4),fam:'Courier Prime'})};
TPL.tweet=(ctx,p,lt,dur)=>{L.bg(ctx,lt,{hue:p.meter?'red':'navy'});const cw=1100,ch=470,x=W/2-cw/2-(p.meter?220:0),y=H/2-ch/2,q=E.back(S(lt,0,.4));
  ctx.save();ctx.translate(x+cw/2,y+ch/2+(1-q)*120);ctx.scale(.9+.1*q,.9+.1*q);ctx.translate(-cw/2,-ch/2);ctx.globalAlpha=L.clamp(q*2);
  L.card(ctx,0,0,cw,ch,{fill:'#fff',r:32});ctx.fillStyle='#6b7280';ctx.beginPath();ctx.arc(80,80,44,0,7);ctx.fill();T(ctx,'SA',80,82,{px:34,fill:'#fff'});
  T(ctx,p.name,145,62,{px:38,fill:'#0f1419',align:'left'});ctx.fillStyle='#1d9bf0';ctx.beginPath();ctx.arc(160+ctx.measureText?370:0,62,0,0,7);
  T(ctx,p.handle+(p.time?' · '+p.time:''),145,104,{px:28,w:500,fill:'#536471',align:'left'});
  L.font(ctx,46,500);const lines=L.wrap(ctx,p.text,cw-120);const words=p.text.split(' ').length;let wi=0;const hk=p.hl?S(lt,.4,dur*.85)*words:0;
  lines.forEach((ln,i)=>{let xx=60;ln.split(' ').forEach(w=>{L.font(ctx,46,500);const ww=ctx.measureText(w+' ').width;if(wi<hk){ctx.fillStyle=Y;ctx.fillRect(xx-4,190+i*64-30,ww,58)}
    T(ctx,w,xx,190+i*64,{px:46,w:500,fill:'#0f1419',align:'left'});xx+=ww;wi++})});
  T(ctx,'💬 1.2K   🔁 8.4K   ♥ 52K',60,ch-50,{px:28,w:500,fill:'#536471',align:'left'});ctx.restore();
  if(p.meter){const mx=W*.8,my=H*.6,a=E.el(S(lt,dur*.3,dur*.75));ctx.save();ctx.translate(mx,my);L.card(ctx,-220,-230,440,330,{fill:'#f1f1f1',r:30});
    const segs=[[GRN,-Math.PI,-Math.PI*.66],[Y,-Math.PI*.66,-Math.PI*.33],[RED,-Math.PI*.33,0]];segs.forEach(([c,a0,a1])=>{ctx.strokeStyle=c;ctx.lineWidth=40;ctx.beginPath();ctx.arc(0,30,150,a0,a1);ctx.stroke()});
    const ang=-Math.PI+Math.PI*(.15+.8*a)+Math.sin(lt*30)*.03*a;ctx.strokeStyle='#111';ctx.lineWidth=10;ctx.beginPath();ctx.moveTo(0,30);ctx.lineTo(Math.cos(ang)*140,30+Math.sin(ang)*140);ctx.stroke();
    ctx.fillStyle='#111';ctx.beginPath();ctx.arc(0,30,18,0,7);ctx.fill();T(ctx,'INVESTOR BP',0,-190,{px:34,fill:'#111'});ctx.restore()}};
TPL.notif=(ctx,p,lt,dur)=>{L.bg(ctx,lt,{hue:'teal'});const r=L.phone(ctx,W*.55-230,70,460,940);ctx.save();ctx.beginPath();ctx.rect(...r);ctx.clip();
  const n=Math.floor(lt*7);for(let i=0;i<n;i++){const age=lt-i/7,yy=r[1]+r[3]-140-(n-1-i)*112+(1-E.oc(L.clamp(age*5)))*-60;if(yy<r[1]-120)continue;
    ctx.save();ctx.globalAlpha=L.clamp(age*5);L.card(ctx,r[0]+16,yy,r[2]-32,100,{fill:'rgba(245,245,245,.95)',r:22,shadow:false});ctx.fillStyle='#10a37f';L.rr(ctx,r[0]+32,yy+20,60,60,14);ctx.fill();
    T(ctx,'ChatGPT',r[0]+110,yy+36,{px:24,fill:'#111',align:'left'});T(ctx,['Your answer is ready','New chat','Write my email…','Fix my code…','Breakup message?'][i%5],r[0]+110,yy+70,{px:22,w:500,fill:'#444',align:'left'});ctx.restore()}
  ctx.restore();ctx.save();ctx.translate(W*.24,H*.5);ctx.strokeStyle='#fff';ctx.lineWidth=14;ctx.beginPath();ctx.arc(0,0,200,0,7);ctx.stroke();
  const a=lt*8;ctx.lineWidth=12;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(Math.cos(a)*150,Math.sin(a)*150);ctx.moveTo(0,0);ctx.lineTo(Math.cos(a/12)*100,Math.sin(a/12)*100);ctx.stroke();ctx.restore();
  L.hilite(ctx,p.clock,W*.24,H*.84,{px:80,p:S(lt,.2,.6),fam:'Anton',w:400})};

/* ================= chat ================= */
TPL.chat=(ctx,p,lt,dur)=>{const th={ChatGPT:['#212121','#2f2f2f','#ececec'],Gemini:['#131314','#1e1f20','#e3e3e3'],Search:['#ffffff','#f1f3f4','#202124'],Forum:['#0b1416','#1a282d','#d7dadc']}[p.app];
  L.bg(ctx,lt,{hue:p.app==='Gemini'?'purple':'grey'});const x=W/2-560,y=80,w=1120,h=920;L.card(ctx,x,y,w,h,{fill:th[0],r:30});
  ctx.save();ctx.beginPath();L.rr(ctx,x,y,w,h,30);ctx.clip();ctx.fillStyle=th[1];ctx.fillRect(x,y,w,100);
  if(p.app==='Search'){L.logo(ctx,'Google',x+150,y+50,50,{light:false});ctx.fillStyle='#fff';L.rr(ctx,x+290,y+22,760,56,28);ctx.fill();ctx.strokeStyle='#dfe1e5';ctx.lineWidth=2;ctx.stroke();T(ctx,p.msgs[0][1],x+320,y+50,{px:28,w:500,fill:'#202124',align:'left'})}
  else if(p.app==='Forum'){ctx.fillStyle='#ff4500';ctx.beginPath();ctx.arc(x+60,y+50,26,0,7);ctx.fill();T(ctx,'r/Pizza',x+100,y+50,{px:32,fill:'#fff',align:'left'})}
  else L.logo(ctx,p.app,x+w/2,y+50,44,{light:true});
  let yy=y+170;const sd=p.type?.25:0;
  if(p.type){const n=Math.floor(p.type.length*S(lt,.2,dur*.55));const sent=lt>dur*.6;
    if(!sent){ctx.fillStyle=th[1];L.rr(ctx,x+60,y+h-150,w-120,100,30);ctx.fill();L.font(ctx,42,500);const ls=L.wrap(ctx,p.type.slice(0,n),w-200);T(ctx,ls[ls.length-1]+(Math.floor(lt*3)%2?'|':''),x+100,y+h-100,{px:42,w:500,fill:th[2],align:'left'})}
    else{bubble(ctx,p.type,x+w-60,yy,'me',th,E.back(S(lt,dur*.6,dur*.6+.3)));if(p.think){const k=Math.floor(lt*4)%4;for(let i=0;i<3;i++){ctx.fillStyle=i<k?th[2]:th[1];ctx.beginPath();ctx.arc(x+90+i*40,y+560,12,0,7);ctx.fill()}}}}
  const msgs=p.msgs||[];msgs.forEach((m,i)=>{const a=p.old&&i<msgs.length-1?-1:(i*dur*.4+.2);const q=a<0?1:E.back(S(lt,a,a+.35));if(q<=0)return;
    if(p.app==='Search'&&m[0]==='me')return;
    if(p.app==='Search'){L.card(ctx,x+80,yy-20,w-160,220,{fill:'#f8fafd',r:20,shadow:false});T(ctx,'✦ AI Overview',x+120,yy+20,{px:28,fill:'#1a73e8',align:'left'});
      L.font(ctx,40,500);L.wrap(ctx,m[1],w-260).forEach((ln,k)=>T(ctx,ln,x+120,yy+90+k*56,{px:40,w:500,fill:'#202124',align:'left'}));
      L.hilite(ctx,'GLUE',x+w-210,yy+340,{px:70,p:S(lt,dur*.5,dur*.7),bg:RED,fill:'#fff'});yy+=260;return}
    if(p.app==='Forum'){L.card(ctx,x+80,yy,w-160,240,{fill:'#1a282d',r:16,shadow:false});T(ctx,'u/pizza_lord · 11y',x+130,yy+50,{px:26,w:500,fill:'#818384',align:'left'});
      T(ctx,m[1],x+130,yy+120,{px:52,w:600,fill:'#d7dadc',align:'left'});const up=Math.floor(8+E.oc(S(lt,.4,dur*.8))*4200);
      ctx.fillStyle='#ff4500';ctx.beginPath();ctx.moveTo(x+130,yy+205);ctx.lineTo(x+150,yy+180);ctx.lineTo(x+170,yy+205);ctx.fill();T(ctx,L.fmt(up),x+185,yy+195,{px:30,fill:'#ff4500',align:'left'});yy+=280;return}
    yy=bubble(ctx,m[1],m[0]==='me'?x+w-60:x+60,yy,m[0],th,q)+40});
  if(p.blank){const q=E.back(S(lt,dur*.65,dur*.65+.4));if(q>0){ctx.save();ctx.translate(x+w-150,y+h-170);ctx.scale(q,q);ctx.fillStyle='#ffd8a8';ctx.beginPath();ctx.arc(0,0,80,0,7);ctx.fill();
    ctx.fillStyle='#111';ctx.beginPath();ctx.arc(-26,-14,8,0,7);ctx.arc(26,-14,8,0,7);ctx.fill();ctx.fillRect(-28,28,56,7);ctx.restore()}}
  ctx.restore()};
function bubble(ctx,s,x,y,who,th,q){L.font(ctx,48,500);const ls=L.wrap(ctx,s,720);const bw=Math.max(...ls.map(l=>ctx.measureText(l).width))+80,bh=ls.length*64+50;
  ctx.save();ctx.globalAlpha=L.clamp(q*2);const bx=who==='me'?x-bw:x;ctx.translate(bx+bw/2,y+bh/2);ctx.scale(.85+.15*q,.85+.15*q);ctx.translate(-bw/2,-bh/2);
  ctx.fillStyle=who==='me'?(th[0]==='#ffffff'?'#e8f0fe':'#303030'):'transparent';L.rr(ctx,0,0,bw,bh,26);ctx.fill();
  if(who!=='me'){ctx.fillStyle='#4796E3';star(ctx,-6,26,18,'#8ab4f8')}
  ls.forEach((l,i)=>T(ctx,l,40,57+i*64,{px:48,w:who==='me'?500:600,fill:th[2],align:'left'}));ctx.restore();return y+bh}

/* ================= counter ================= */
TPL.counter=(ctx,p,lt,dur,s)=>{const st=p.style||'big';L.bg(ctx,lt,{hue:st==='bill'||p.fire?'red':p.city?'teal':'navy',src:p.src});
  if(p.city){L.city(ctx,lt,{y:H*1.02,col:'#06141c'});ctx.save();ctx.globalCompositeOperation='lighter';const g=ctx.createLinearGradient(0,H*.5,0,H);g.addColorStop(0,'rgba(0,0,0,0)');g.addColorStop(1,'rgba(40,200,255,.25)');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);ctx.restore()}
  if(p.fire)for(let i=0;i<26;i++){const ph=(lt*1.4+L.hash(i,2))%1,x=W/2+(L.hash(i,3)-.5)*900,y=H*.98-ph*300;ctx.save();ctx.globalAlpha=(1-ph)*.9;L.icon(ctx,'fire',x,y,50+60*(1-ph));ctx.restore();
    if(i<8)L.money(ctx,x,y-60,.8,ph*4+i)}
  const q=E.oc(S(lt,.15,Math.min(dur*.7,2.6))),fr=p.from||0,v=fr+(p.to-fr)*q;
  const txt=(p.prefix||'')+L.fmt(p.dec?v:Math.round(v),{dec:p.dec||0,indian:p.indian})+(p.suffix||'');
  const landed=q>=.999,land=S(lt,Math.min(dur*.7,2.6),Math.min(dur*.7,2.6)+.3);
  ctx.save();if(p.slam&&landed){const k=L.shakeAmt(lt-Math.min(dur*.7,2.6),1,.4,0);ctx.translate(...k)}
  if(st==='bill'){const bx=W/2-430,by=170;ctx.save();ctx.shadowColor='rgba(0,0,0,.5)';ctx.shadowBlur=40;ctx.fillStyle='#fbfaf3';ctx.beginPath();ctx.moveTo(bx,by);ctx.lineTo(bx+860,by);ctx.lineTo(bx+860,by+760);
    for(let i=0;i<=20;i++)ctx.lineTo(bx+860-i*43,by+760+(i%2?-18:0));ctx.closePath();ctx.fill();ctx.restore();
    T(ctx,'GPU RENT · INVOICE',W/2,by+70,{px:40,fam:'Courier Prime',w:700,fill:'#222',track:4});ctx.setLineDash([10,10]);ctx.strokeStyle='#999';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(bx+40,by+120);ctx.lineTo(bx+820,by+120);ctx.stroke();ctx.setLineDash([]);
    const rows=[['1 x H100','$3 / hr'],['x 500 chips','$1,500 / hr'],['x 24 hrs','$36,000 / day'],['x 30 days','$11,00,000+']];const nr=s.id-57;
    rows.slice(0,nr).forEach((r,i)=>{T(ctx,r[0],bx+60,by+180+i*64,{px:36,fam:'Courier Prime',fill:'#444',align:'left'});T(ctx,r[1],bx+800,by+180+i*64,{px:36,fam:'Courier Prime',fill:'#444',align:'right'})});
    T(ctx,'TOTAL',W/2,by+480,{px:36,fam:'Courier Prime',w:700,fill:'#888',track:8});T(ctx,txt,W/2,by+590,{px:Math.min(130,1500/txt.length),fam:'Anton',w:400,fill:RED})}
  else if(st==='token'){L.card(ctx,W/2-460,H/2-300,920,600,{fill:'#2a2d34',r:40});ctx.fillStyle='#0b0b0b';L.rr(ctx,W/2-380,H/2-150,760,280,20);ctx.fill();
    T(ctx,p.tag,W/2,H/2-220,{px:54,fill:'#fff',track:8});T(ctx,txt,W/2,H/2-10,{px:150,fam:'Anton',w:400,fill:'#ff3434',glow:40,gc:'#ff0000'});
    for(let k=0;k<10;k++){const ph=(lt*.8+k/10)%1;ctx.save();ctx.translate(W*(.15+.7*L.hash(k,9)),-80+ph*(H+160));ctx.rotate(ph*5+k);ctx.fillStyle='#fbfaf6';ctx.fillRect(-50,-60,100,120);ctx.fillStyle=RED;ctx.fillRect(-50,-60,100,28);ctx.restore()}}
  else if(st==='price'){ctx.save();ctx.translate(W/2,H/2-40);ctx.rotate(-.05+Math.sin(lt*2)*.02);ctx.fillStyle=Y;ctx.beginPath();ctx.moveTo(-520,-170);ctx.lineTo(360,-170);ctx.lineTo(520,0);ctx.lineTo(360,170);ctx.lineTo(-520,170);ctx.closePath();
    ctx.shadowColor='rgba(0,0,0,.5)';ctx.shadowBlur=40;ctx.fill();ctx.shadowBlur=0;ctx.fillStyle='#111';ctx.beginPath();ctx.arc(380,0,26,0,7);ctx.fill();T(ctx,txt,-60,10,{px:170,fam:'Anton',w:400,fill:'#111'});ctx.restore();
    L.chip(ctx,p.tag,W/2,H*.16,{px:50,bg:'#fff',p:S(lt,0,.3)});
    if(p.sub){const a=S(lt,dur*.5,dur*.6);ctx.save();ctx.globalAlpha=a;ctx.strokeStyle=RED;ctx.fillStyle=RED;ctx.lineWidth=18;ctx.beginPath();ctx.moveTo(W/2-200,H*.72);ctx.lineTo(W/2+150,H*.72+60*a);ctx.stroke();
      ctx.beginPath();ctx.moveTo(W/2+150,H*.72+60*a-30);ctx.lineTo(W/2+210,H*.72+60*a+10);ctx.lineTo(W/2+130,H*.72+60*a+40);ctx.fill();ctx.restore();T(ctx,p.sub,W/2,H*.88,{px:60,fill:RED,alpha:a})}}
  else{T(ctx,txt,W/2,H/2+20,{px:txt.length>14?140:txt.length>10?180:220,fam:'Anton',w:400,fill:'#fff',stroke:10,sc:'#000',glow:landed?50:20,gc:Y});
    if(p.tag)L.chip(ctx,p.tag,W/2,H*.22,{px:56,p:S(lt,.05,.4)});if(p.label)L.hilite(ctx,p.label,W/2,H*.8,{px:60,p:land})}
  ctx.restore();
  if(landed)L.burst(ctx,W/2,H/2,420,land,{});
  L.dust(ctx,lt,24,.4)};

/* ================= race ================= */
TPL.race=(ctx,p,lt,dur)=>{L.bg(ctx,lt,{hue:'navy'});hdr(ctx,p.title,lt);const n=p.items.length,maxV=54,clock=E.io(S(lt,.3,dur*.85))*maxV;
  const x0=W*.24,x1=W*.9,top=H*.3,lh=Math.min(200,H*.55/n);
  T(ctx,`${(clock/12).toFixed(1)} YRS`,W*.88,H*.9,{px:56,fam:'Anton',w:400,fill:'#9ab',align:'right'});
  p.items.forEach(([name,v,disp],i)=>{const y=top+i*lh+lh/2,q=L.clamp(clock/v),fin=clock>=v;
    ctx.fillStyle='rgba(255,255,255,.07)';L.rr(ctx,x0,y-lh*.32,x1-x0,lh*.64,lh*.32);ctx.fill();
    const g=ctx.createLinearGradient(x0,0,x1,0);g.addColorStop(0,name==='ChatGPT'?'#10a37f':name==='Instagram'?'#D62976':'#1877F2');g.addColorStop(1,'#fff');
    ctx.fillStyle=g;L.rr(ctx,x0,y-lh*.32,Math.max(lh*.64,(x1-x0)*q),lh*.64,lh*.32);ctx.fill();
    L.logo(ctx,name,x0-30,y,lh*.42,{align:'right'});
    if(name==='ChatGPT'){const rx=x0+(x1-x0)*q;for(let k=0;k<12;k++){ctx.fillStyle=`rgba(255,${150+k*8},60,${.6-k*.05})`;ctx.beginPath();ctx.arc(rx-30-k*22,y+Math.sin(lt*30+k)*6,14-k,0,7);ctx.fill()}}
    if(fin)L.chip(ctx,disp,Math.min(x1-120,x0+(x1-x0)*q-100),y,{px:40,p:S(clock,v,v+3),bg:'#fff'})});
  ctx.strokeStyle='#fff';ctx.setLineDash([16,12]);ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(x1,top-30);ctx.lineTo(x1,top+n*lh);ctx.stroke();ctx.setLineDash([]);
  if(p.win){const q=E.back(S(lt,dur*.45,dur*.45+.5));if(q>0){ctx.save();ctx.translate(W*.5,H*.86);ctx.scale(q,q);L.hilite(ctx,'🏆 '+p.win,0,0,{px:76,fam:'Anton',w:400});ctx.restore()}}};

/* ================= cards ================= */
TPL.cards=(ctx,p,lt,dur)=>{const st=p.style;L.bg(ctx,lt,{hue:st==='fan'||st==='flip'?'red':'navy'});const n=p.items.length;
  if(st==='bubbles'){p.items.forEach(([ic,lab],i)=>{const a=dur*(.1+i*.25),q=E.back(S(lt,a,a+.4));if(q<=0)return;const x=W*(.22+i*.28),y=H*.45+Math.sin(lt*2+i)*14;
    ctx.save();ctx.translate(x,y);ctx.scale(q,q);ctx.fillStyle='#fff';ctx.beginPath();for(let k=0;k<10;k++){const aa=k/10*7;ctx.moveTo(0,0);ctx.arc(Math.cos(aa)*150,Math.sin(aa)*110,70,0,7)}ctx.fill();
    ctx.beginPath();ctx.arc(-40,190,26,0,7);ctx.arc(-70,240,14,0,7);ctx.fill();L.icon(ctx,ic,0,-20,120);T(ctx,lab,0,90,{px:46,fill:'#111'});ctx.restore()});return}
  if(st==='icons'){p.items.forEach(([ic,lab],i)=>{const a=dur*(i/n)*.8,q=E.back(S(lt,a,a+.35));if(q<=0)return;const x=W*(.2+i*.3);ctx.save();ctx.translate(x,H*.48);ctx.scale(q,q);
    L.card(ctx,-220,-220,440,440,{fill:'rgba(255,255,255,.08)',r:40});L.icon(ctx,ic,0,-50,190,{p:1});
    if(ic==='bag'){const sm=S(lt,a+.6,a+1.2);if(sm>0){ctx.globalAlpha=sm;for(let k=0;k<8;k++){ctx.fillStyle='rgba(180,180,180,.6)';ctx.beginPath();ctx.arc((L.hash(k,1)-.5)*160,-50-sm*120*L.hash(k,2),40,0,7);ctx.fill()}}}
    ctx.globalAlpha=1;T(ctx,lab,0,140,{px:38,fill:'#fff'});ctx.restore()});return}
  if(st==='morph'){const per=dur/n,i=Math.min(n-1,Math.floor(lt/per)),pl=lt-i*per,[ic,lab]=p.items[i],q=E.back(S(pl,0,.35));
    ctx.save();ctx.translate(W/2,H*.45);ctx.scale(q,q);ctx.rotate((1-q)*.5);L.icon(ctx,ic,0,0,360);ctx.restore();L.hilite(ctx,lab,W/2,H*.82,{px:76,p:S(pl,.1,.4)});
    for(let k=0;k<n;k++){ctx.fillStyle=k===i?Y:'rgba(255,255,255,.3)';ctx.beginPath();ctx.arc(W/2+(k-1)*40,H*.94,10,0,7);ctx.fill()}return}
  // fan / flip: numbered trigger cards
  p.items.forEach(([num,lab],i)=>{const fan=E.back(S(lt,i*.15,i*.15+.5)),x=W/2+(i-1)*480*fan,rot=(i-1)*.08*fan;
    let flip=0;if(st==='flip'&&p.flip===i)flip=E.io(S(lt,.2,.8));const big=st==='flip'&&p.flip===i?1+.15*flip:st==='flip'?.9:1;
    ctx.save();ctx.translate(x,H*.52+(st==='flip'&&p.flip!==i?40:0));ctx.rotate(rot);ctx.scale(Math.abs(Math.cos(flip*Math.PI))*big||.01,big);
    if(st==='flip'&&p.flip!==i)ctx.globalAlpha=.45;const face=flip>.5;
    L.card(ctx,-190,-270,380,540,{fill:face?'#fff':'#1d2433',r:30});ctx.strokeStyle=face?RED:Y;ctx.lineWidth=8;L.rr(ctx,-170,-250,340,500,22);ctx.stroke();
    if(!face){T(ctx,num,0,-40,{px:260,fam:'Anton',w:400,fill:Y});if(num==='3')monster(ctx,lt);}
    else{T(ctx,num,0,-150,{px:90,fam:'Anton',w:400,fill:RED});ctx.save();ctx.scale(-1,1);ctx.scale(-1,1);L.font(ctx,64,800);L.wrap(ctx,lab,300).forEach((ln,k)=>T(ctx,ln,0,10+k*80,{px:64,fill:'#111'}));ctx.restore()}
    ctx.restore()})};
function monster(ctx,lt){ctx.save();ctx.translate(0,150);ctx.fillStyle='#2a7a3a';ctx.beginPath();ctx.ellipse(0,0,90,60,0,0,7);ctx.fill();ctx.beginPath();ctx.ellipse(70,-50,40,30,.3,0,7);ctx.fill();
  ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(82,-58,8,0,7);ctx.fill();ctx.fillStyle='#2a7a3a';for(let k=0;k<5;k++){ctx.beginPath();ctx.moveTo(-60+k*25,-50);ctx.lineTo(-48+k*25,-80);ctx.lineTo(-36+k*25,-50);ctx.fill()}ctx.restore()}

/* ================= money (truck / vault) ================= */
TPL.money=(ctx,p,lt,dur)=>{L.bg(ctx,lt,{hue:'green'});ctx.fillStyle='#1b2a22';ctx.fillRect(0,H*.78,W,H*.22);
  // destination building
  ctx.save();ctx.translate(W*.8,H*.78);ctx.fillStyle='#dfe6ee';ctx.fillRect(-200,-480,400,480);ctx.fillStyle='#9fb3c8';for(let i=0;i<5;i++)for(let j=0;j<4;j++)ctx.fillRect(-170+j*90,-450+i*80,60,50);
  ctx.fillStyle='#333';ctx.fillRect(-60,-130,120,130);ctx.fillStyle='#fff';L.rr(ctx,-180,-560,360,80,20);ctx.fill();L.logo(ctx,p.to,0,-520,46,{light:false});ctx.restore();
  if(p.mode==='vault'){const q=E.io(S(lt,.2,dur*.6));ctx.strokeStyle='#888';ctx.lineWidth=8;ctx.beginPath();ctx.moveTo(W*.42,0);ctx.lineTo(W*.42,H*.2+q*H*.32);ctx.stroke();
    ctx.save();ctx.translate(W*.42,H*.32+q*H*.32);ctx.rotate(Math.sin(lt*2)*.03*(1-q));L.card(ctx,-220,-140,440,280,{fill:'#7b8794',r:16});ctx.strokeStyle='#4b5563';ctx.lineWidth=10;ctx.beginPath();ctx.arc(110,0,60,0,7);ctx.stroke();
    T(ctx,p.bags[0],-50,0,{px:50,fill:'#fff',fam:'Anton',w:400});ctx.restore();ctx.fillStyle='#f59e0b';ctx.fillRect(W*.36,0,W*.12,30);
    L.logo(ctx,p.from,W*.42,H*.1,60);return}
  // truck drives in, dumps bags
  const drive=E.oc(S(lt,0,dur*.35)),tx=L.lerp(-500,W*.48,drive);ctx.save();ctx.translate(tx,H*.78);
  const tilt=-.35*E.io(S(lt,dur*.38,dur*.5));ctx.fillStyle='#e9eef5';L.rr(ctx,-420,-300,460,240,12);ctx.fill();L.logo(ctx,p.from,-190,-180,56,{light:false});
  ctx.fillStyle='#4f8cc9';L.rr(ctx,50,-230,180,170,16);ctx.fill();ctx.fillStyle='#bfe0ff';ctx.fillRect(120,-210,90,70);
  ctx.fillStyle='#111';[-320,-150,150].forEach(x=>{ctx.beginPath();ctx.arc(x,-50,50,0,7);ctx.fill();ctx.fillStyle='#777';ctx.beginPath();ctx.arc(x,-50,20,0,7);ctx.fill();ctx.fillStyle='#111'});ctx.restore();
  const dump=S(lt,dur*.45,dur*.75);if(dump>0){const bx=W*.62;for(let k=0;k<6;k++){const q=L.clamp(dump*1.6-k*.12);if(q<=0)continue;ctx.save();ctx.translate(L.lerp(tx+100,bx-60+k*30,q),L.lerp(H*.5,H*.7-(k%2)*70,E.oc(q)));L.icon(ctx,'bag',0,0,130);ctx.restore()}
    L.chip(ctx,p.bags[0],bx,H*.48,{px:70,p:S(lt,dur*.55,dur*.65)})}
  if(p.bags[1]){const q=E.back(S(lt,dur*.72,dur*.82));if(q>0){ctx.save();ctx.translate(W*.32,H*.68);ctx.scale(q,q);L.icon(ctx,'bag',0,0,110);ctx.restore();L.chip(ctx,p.bags[1]+' READY',W*.32,H*.5,{px:46,bg:'#fff',p:q})}}};

/* ================= reveal (briefcase) ================= */
TPL.reveal=(ctx,p,lt,dur)=>{L.bg(ctx,lt,{hue:'gold'});const o=E.back(S(lt,.15,.6));
  if(o>.3)L.rays(ctx,lt,{x:W/2,y:H*.55,a:.12*o});
  ctx.save();ctx.translate(W/2,H*.62);ctx.fillStyle='#3b2412';L.rr(ctx,-380,-40,760,300,24);ctx.fill();ctx.fillStyle='#d4a017';ctx.fillRect(-80,-60,160,30);
  ctx.save();ctx.translate(0,-40);ctx.scale(1,Math.cos(o*Math.PI*.55));ctx.fillStyle='#4a2e18';L.rr(ctx,-380,-260,760,260,24);ctx.fill();ctx.restore();
  if(o>.2){ctx.save();ctx.globalAlpha=L.clamp(o);for(let k=0;k<7;k++)L.money(ctx,-300+k*100,10,1.4,0);ctx.restore()}ctx.restore();
  if(o>.4){ctx.save();ctx.translate(W/2,H*.3);ctx.scale(o,o);T(ctx,p.text,0,0,{px:240,fam:'Anton',w:400,fill:'#fff',glow:60,gc:Y,stroke:10,sc:'#000'});ctx.restore()}};

/* ================= podium ================= */
TPL.podium=(ctx,p,lt,dur)=>{L.bg(ctx,lt,{hue:'green'});L.rays(ctx,lt,{x:W/2,y:-50,a:.12});
  [[W/2-380,240,'2'],[W/2,360,'1'],[W/2+380,180,'3']].forEach(([x,h,n])=>{ctx.fillStyle=n==='1'?'#e8e8e8':'#b9c0c9';ctx.fillRect(x-170,H-h,340,h);T(ctx,n,x,H-h+90,{px:110,fam:'Anton',w:400,fill:'#2b2f36'})});
  const q=E.io(S(lt,.2,dur*.55)),x=W/2,y=L.lerp(H+150,H-360-90,q)-Math.sin(q*Math.PI)*120;
  ctx.save();ctx.translate(x,y);L.card(ctx,-260,-80,520,160,{fill:'#111',r:20});L.logo(ctx,p.logo,0,0,70);ctx.restore();
  const c=E.el(S(lt,dur*.6,dur*.6+.8));if(c>0){ctx.save();ctx.translate(x,L.lerp(-200,y-160,c));ctx.fillStyle=Y;ctx.beginPath();ctx.moveTo(-90,40);ctx.lineTo(-100,-40);ctx.lineTo(-45,0);ctx.lineTo(0,-60);ctx.lineTo(45,0);ctx.lineTo(100,-40);ctx.lineTo(90,40);ctx.closePath();
    ctx.shadowColor=Y;ctx.shadowBlur=40;ctx.fill();ctx.restore();L.burst(ctx,x,y-160,200,S(lt,dur*.6+.6,dur*.6+1.1))}
  L.confetti(ctx,Math.max(0,lt-dur*.65),{n:lt>dur*.65?60:0})};

/* ================= gpu grid ================= */
TPL.gpu=(ctx,p,lt,dur)=>{L.bg(ctx,lt,{hue:'green'});const n0=p.n0||p.n,n=Math.round(L.lerp(n0,p.n,E.io(S(lt,.1,dur*.8))));
  if(n<=1){const w=p.wiggle?Math.sin(lt*10)*.06:0;ctx.save();ctx.translate(W/2,H*.48);ctx.scale(1+.04*Math.sin(lt*2),1);L.icon(ctx,'gpu',0,0,620);ctx.restore();
    ctx.save();ctx.translate(W/2+330,H*.28);ctx.rotate(w-.1);L.chip(ctx,p.tag,0,0,{px:70,p:S(lt,.2,.6)});ctx.restore();if(p.kw)L.hilite(ctx,p.kw,W/2,H*.86,{px:80,p:S(lt,.4,.8)});return}
  const cols=Math.ceil(Math.sqrt(n*16/9)),rows=Math.ceil(n/cols),cw=W*.92/cols,ch=Math.min(cw*.7,H*.78/rows),s=Math.min(cw,ch/.62)*.92;
  for(let i=0;i<n;i++){const c=i%cols,r=Math.floor(i/cols);L.icon(ctx,'gpu',W*.04+cw*(c+.5),H*.15+ch*(r+.5),s,{p:1})}
  if(p.tag){const q=E.back(S(lt,dur*.7,dur*.7+.4));if(q>0){ctx.save();ctx.translate(W/2,H/2);ctx.scale(q,q);T(ctx,p.tag,0,0,{px:300,fam:'Anton',w:400,fill:Y,stroke:16,sc:'#000',glow:40});ctx.restore()}}};

/* ================= stickers ================= */
TPL.stickers=(ctx,p,lt,dur)=>{L.bg(ctx,lt,{hue:'purple'});T(ctx,p.year,W/2,H*.18,{px:150,fam:'Anton',w:400,fill:'#fff',alpha:E.oc(S(lt,0,.3))});
  const objs=['toaster','fridge','brush','shoe','lamp'];objs.forEach((o,i)=>{const x=W*(.14+i*.18),y=H*.6;obj(ctx,o,x,y);const a=.4+i*dur*.13,q=S(lt,a,a+.18);
    if(q>0)L.stamp(ctx,p.text,x,y-20,q,{col:'#00e5ff',px:44,rot:(L.hash(i,1)-.5)*.5})})};
function obj(ctx,k,x,y){ctx.save();ctx.translate(x,y);ctx.fillStyle='#cfd6e2';ctx.strokeStyle='#0b0d14';ctx.lineWidth=6;
  if(k==='toaster'){L.rr(ctx,-110,-70,220,140,30);ctx.fill();ctx.stroke();ctx.fillStyle='#333';ctx.fillRect(-60,-80,40,14);ctx.fillRect(20,-80,40,14)}
  else if(k==='fridge'){L.rr(ctx,-80,-170,160,340,16);ctx.fill();ctx.stroke();ctx.beginPath();ctx.moveTo(-80,-50);ctx.lineTo(80,-50);ctx.stroke()}
  else if(k==='brush'){ctx.rotate(-.5);L.rr(ctx,-20,-160,40,280,16);ctx.fill();ctx.stroke();ctx.fillStyle='#7dd3fc';ctx.fillRect(-20,-200,40,50)}
  else if(k==='shoe'){ctx.beginPath();ctx.moveTo(-120,40);ctx.lineTo(-110,-50);ctx.lineTo(-20,-40);ctx.quadraticCurveTo(60,0,120,10);ctx.lineTo(120,40);ctx.closePath();ctx.fill();ctx.stroke()}
  else{ctx.beginPath();ctx.moveTo(-80,-60);ctx.lineTo(80,-60);ctx.lineTo(50,-150);ctx.lineTo(-50,-150);ctx.closePath();ctx.fillStyle=Y;ctx.fill();ctx.stroke();ctx.fillStyle='#cfd6e2';ctx.fillRect(-8,-60,16,160);ctx.fillRect(-60,100,120,20)}
  ctx.restore()}

/* ================= bars ================= */
TPL.bars=(ctx,p,lt,dur)=>{L.bg(ctx,lt,{hue:'navy'});
  if(p.mode==='updown'){const by=H*.55;ctx.strokeStyle='#fff';ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(W*.2,by);ctx.lineTo(W*.8,by);ctx.stroke();
    L.logo(ctx,'OpenAI',W/2-100,H*.1,56);T(ctx,'2024',W/2+180,H*.1,{px:56,fam:'Anton',w:400,fill:Y});
    p.items.forEach(([lab,v,disp],i)=>{const a=.3+i*dur*.35,q=E.oc(S(lt,a,a+.8)),x=W*(.36+i*.28),hh=Math.abs(v)*70*q;ctx.fillStyle=v>0?GRN:RED;
      if(v>0)L.rr(ctx,x-110,by-hh,220,hh,12);else L.rr(ctx,x-110,by,220,hh,12);ctx.fill();
      T(ctx,lab,x,v>0?by+50:by-40,{px:40,fill:'#fff',alpha:q});T(ctx,disp,x,v>0?by-hh-60:by+hh+60,{px:80,fam:'Anton',w:400,fill:v>0?GRN:RED,alpha:q})});return}
  // target bars ($2T needed vs $200B)
  const base=H*.88,maxH=H*.66;p.items.forEach(([lab,v,disp],i)=>{const a=p.old>i?-1:.2,q=a<0?1:E.oc(S(lt,a,a+1.2)),x=W*(.38+i*.26),hh=v/2000*maxH*q;
    const g=ctx.createLinearGradient(0,base-hh,0,base);g.addColorStop(0,i?GRN:RED);g.addColorStop(1,i?'#0f5a3e':'#5a0f17');ctx.fillStyle=g;L.rr(ctx,x-130,base-hh,260,hh,14);ctx.fill();
    T(ctx,disp,x,base-hh-60,{px:90,fam:'Anton',w:400,fill:'#fff',alpha:L.clamp(q*2)});T(ctx,lab,x,base+40,{px:34,fill:'#bcd',alpha:L.clamp(q*2)})});
  if(p.arrow){const q=E.oc(S(lt,.2,dur*.6)),x=W*.51;ctx.strokeStyle=Y;ctx.fillStyle=Y;ctx.lineWidth=16;ctx.beginPath();ctx.moveTo(x,base-80);ctx.lineTo(x,L.lerp(base-80,base-maxH+40,q));ctx.stroke();
    const ty=L.lerp(base-80,base-maxH+40,q);ctx.beginPath();ctx.moveTo(x-40,ty+20);ctx.lineTo(x,ty-40);ctx.lineTo(x+40,ty+20);ctx.fill();L.hilite(ctx,p.arrow,x-230,H*.45,{px:130,fam:'Anton',w:400,p:S(lt,dur*.4,dur*.6)})}};

/* ================= split ================= */
TPL.split=(ctx,p,lt,dur)=>{
  if(p.mode==='block'){L.bg(ctx,lt,{hue:'teal'});const q=p.old?1:E.io(S(lt,.4,1.2)),gap=60*q,tw=1500,x0=W/2-tw/2-gap/2,wa=tw*5.2/6.7,wb=tw*1.5/6.7,y=H*.36,h=360;
    if(q<1)T(ctx,p.total,W/2,H*.2,{px:90,fam:'Anton',w:400,fill:'#fff',alpha:1-q});
    [[p.a,x0,wa,'a'],[p.b,x0+wa+gap,wb,'b']].forEach(([d,x,w,k])=>{const hl=p.hl===k;ctx.save();ctx.globalAlpha=hl||q<1?1:.4;const g=ctx.createLinearGradient(x,y,x,y+h);g.addColorStop(0,k==='a'?'#ffb020':'#3fb6ff');g.addColorStop(1,k==='a'?'#a35c00':'#0d5f99');
      ctx.fillStyle=g;L.rr(ctx,x,y,w,h,24);ctx.fill();T(ctx,d[0],x+w/2,y+h*.38,{px:k==='a'?130:90,fam:'Anton',w:400,fill:'#fff'});T(ctx,d[1],x+w/2,y+h*.72,{px:40,fill:'#fff'});
      if(hl)d[2].forEach((ic,i)=>{const a=1+i*.35,qq=E.back(S(lt,a,a+.35));if(qq>0)L.icon(ctx,ic,x+w/2+(i-(d[2].length-1)/2)*(Math.min(w,1100)/d[2].length),y+h+150,140,{p:qq})});ctx.restore()});return}
  if(p.mode==='lawsuit'){L.bg(ctx,lt,{hue:'grey'});ctx.fillStyle='#5b3a1e';ctx.fillRect(0,H*.7,W,H*.3);p.pairs.forEach(([a,b],i)=>{const t0=i*dur*.48+.1,q=S(lt,t0,t0+.25);if(q<=0)return;
    const x=W*(.3+i*.4),y=L.lerp(-400,H*.48,E.ic(q));ctx.save();ctx.translate(x,y);ctx.rotate((i?.06:-.05));L.card(ctx,-300,-380,600,700,{fill:'#f8f5ec',r:8});
    T(ctx,'LAWSUIT',0,-300,{px:60,fam:'Courier Prime',w:700,fill:'#222',track:8});L.logo(ctx,a,0,-170,i?44:50,{light:false});T(ctx,'v.',0,-80,{px:50,fam:'Caveat',w:700,fill:'#555'});L.logo(ctx,b,0,10,50,{light:false});
    ctx.fillStyle='#aaa';for(let k=0;k<5;k++)ctx.fillRect(-230,100+k*36,k%2?380:460,10);L.stamp(ctx,'COPYRIGHT',60,250,S(lt,t0+.4,t0+.6),{px:54,rot:-.1});ctx.restore();
    if(q>=1)L.burst(ctx,x,H*.48+300,300,S(lt,t0+.25,t0+.6),{col:'#fff'})});return}
  // megaphone vs spreadsheet
  ctx.fillStyle='#1b1030';ctx.fillRect(0,0,W/2,H);ctx.fillStyle='#090a0c';ctx.fillRect(W/2,0,W/2,H);
  ctx.save();ctx.translate(W*.22,H*.5);const sh=Math.sin(lt*30)*4;ctx.translate(sh,0);ctx.fillStyle='#e8e8e8';ctx.beginPath();ctx.moveTo(-140,-50);ctx.lineTo(80,-160);ctx.lineTo(80,160);ctx.lineTo(-140,50);ctx.closePath();ctx.fill();
  ctx.strokeStyle=Y;ctx.lineWidth=10;for(let k=0;k<3;k++){const ph=(lt*2+k/3)%1;ctx.globalAlpha=1-ph;ctx.beginPath();ctx.arc(80,0,60+ph*260,-.7,.7);ctx.stroke()}ctx.globalAlpha=1;
  T(ctx,'AI!',320,-140,{px:150,fam:'Anton',w:400,fill:Y,glow:30});ctx.restore();
  const x0=W*.56,y0=H*.18;for(let r=0;r<10;r++)for(let c=0;c<4;c++){ctx.strokeStyle='#26303a';ctx.strokeRect(x0+c*190,y0+r*70,190,70);const v=L.hash(r*4+c,8);if(r>0&&c>0&&lt>r*.12)T(ctx,(v<.6?'-':'')+'$'+(v*99).toFixed(1)+'B',x0+c*190+95,y0+r*70+36,{px:28,fam:'Courier Prime',w:700,fill:v<.6?RED:'#7a8'})}
  T(ctx,'HYPE',W*.25,H*.9,{px:60,fill:'#fff',track:10});T(ctx,'NUMBERS',W*.75,H*.9,{px:60,fill:RED,track:10})};

/* ================= logos ================= */
TPL.logos=(ctx,p,lt,dur)=>{L.bg(ctx,lt,{hue:p.mode?'green':'navy'});
  if(p.mode==='rain'||p.mode==='coins'){const q=E.back(S(lt,0,.4));ctx.save();ctx.translate(W/2,H*.2);ctx.scale(q,q);L.card(ctx,-330,-80,660,160,{fill:'#fff',r:80});L.logo(ctx,p.items[0],0,0,74,{light:false});ctx.restore();
    if(p.mode==='rain'){L.icon(ctx,'cloud',W/2,H*.42,330);for(let i=0;i<34;i++){const ph=(lt*.9+L.hash(i,4))%1;L.money(ctx,W/2+(L.hash(i,5)-.5)*560,H*.5+ph*H*.55,.9,ph*6+i)}}
    else for(let i=0;i<8;i++){const a=.3+i*.25,q=S(lt,a,a+.6),x=W*(.12+i*.11),y=H*.55+Math.sin(i)*60;if(q<.5){ctx.save();ctx.translate(x,y);ctx.scale(Math.cos(q*Math.PI),1);L.card(ctx,-80,-50,160,100,{fill:'#fff',r:12});T(ctx,'Ad',0,0,{px:40,fill:'#1a73e8'});ctx.restore()}
      else L.coin(ctx,x,y+E.ic((q-.5)*2)*160,60,lt*4+i)}
    L.hilite(ctx,p.sub,W/2,H*.9,{px:60,p:S(lt,.3,.6)});return}
  const n=p.items.length;p.items.forEach((nm,i)=>{const a=-Math.PI*.75+i*Math.PI/2,q=E.back(S(lt,.1+i*.2,.5+i*.2)),x=W/2+Math.cos(a)*560,y=H/2+Math.sin(a)*330;if(q<=0)return;
    ctx.save();ctx.translate(x,y);ctx.scale(q,q);L.card(ctx,-240,-80,480,160,{fill:'#fff',r:30});L.logo(ctx,nm,0,0,62,{light:false});ctx.restore();
    ctx.strokeStyle='rgba(255,210,63,.4)';ctx.setLineDash([12,10]);ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(x*.6+W/2*.4,y*.6+H/2*.4);ctx.lineTo(W/2,H/2);ctx.stroke();ctx.setLineDash([])});
  const q=E.back(S(lt,1,1.5));ctx.save();ctx.translate(W/2,H/2);ctx.scale(q,q);T(ctx,p.center,0,0,{px:170,fam:'Anton',w:400,fill:'#fff',glow:50,gc:Y,stroke:10,sc:'#000'});T(ctx,p.sub,0,110,{px:48,fill:Y});ctx.restore()};

/* ================= hockey stick ================= */
TPL.hockey=(ctx,p,lt,dur)=>{ctx.fillStyle='#3a2a1a';ctx.fillRect(0,0,W,H);L.card(ctx,W*.1,H*.08,W*.8,H*.8,{fill:'#f4f6f5',r:12});ctx.strokeStyle='#c8ccd0';ctx.lineWidth=12;ctx.strokeRect(W*.1,H*.08,W*.8,H*.8);
  const ax=W*.2,ay=H*.78;ctx.strokeStyle='#333';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(ax,H*.15);ctx.lineTo(ax,ay);ctx.lineTo(W*.84,ay);ctx.stroke();
  T(ctx,'REVENUE',ax-20,H*.13,{px:30,fill:'#333',align:'left'});T(ctx,'2025',ax+60,ay+40,{px:32,fill:'#333'});T(ctx,'2029',W*.8,ay+40,{px:32,fill:'#333'});
  T(ctx,'$20B',ax+60,ay-80,{px:40,fam:'Caveat',w:700,fill:'#1d4ed8'});T(ctx,'$100B?',W*.78,H*.2,{px:50,fam:'Caveat',w:700,fill:'#1d4ed8'});
  const m=p.mode==='morph'?E.io(S(lt,.3,dur*.6)):1;const pts=[];for(let i=0;i<=40;i++){const u=i/40;const straight=[ax+60+u*(W*.6),ay-60-u*(H*.55)];
    const hk=u<.7?[ax+60+u*W*.6,ay-60-u*30+Math.sin(u*40)*8]:[ax+60+u*W*.6+((u-.7)/.3)*-40,ay-60-21-((u-.7)/.3)**1.5*H*.52+Math.sin(u*50)*10];pts.push([L.lerp(straight[0],hk[0],m),L.lerp(straight[1],hk[1],m)])}
  const col=m>.5?RED:'#1d4ed8';const snap=p.mode==='snap'?E.oc(S(lt,dur*.45,dur*.6)):0;const cut=29;
  ctx.lineCap='round';ctx.lineJoin='round';ctx.lineWidth=16;ctx.strokeStyle=col;
  ctx.beginPath();pts.slice(0,cut+1).forEach((q,i)=>i?ctx.lineTo(...q):ctx.moveTo(...q));ctx.stroke();
  ctx.save();ctx.translate(...pts[cut]);ctx.rotate(snap*.9);ctx.translate(snap*80,snap*snap*380);ctx.beginPath();pts.slice(cut).forEach((q,i)=>{const r=[q[0]-pts[cut][0],q[1]-pts[cut][1]];i?ctx.lineTo(...r):ctx.moveTo(...r)});ctx.stroke();ctx.restore();
  if(snap>0){L.burst(ctx,...pts[cut],160,snap,{col:'#111'});L.stamp(ctx,'CRACK!',W*.62,H*.42,S(lt,dur*.45,dur*.55),{px:120})}
  if(p.mode==='morph')L.hilite(ctx,'HOCKEY STICK?',W/2,H*.93,{px:56,p:S(lt,dur*.6,dur*.75)})};

/* ================= funnel ================= */
TPL.funnel=(ctx,p,lt,dur)=>{L.bg(ctx,lt,{hue:'gold'});const fx=W*.62,fy=H*.62;
  L.chip(ctx,p.from,W*.1,H*.2,{px:60,bg:'#fff'});
  for(let i=0;i<40;i++){const ph=(lt*.45+L.hash(i,6))%1,x=L.lerp(W*.08,fx,ph),y=L.lerp(H*.28,fy-150,ph)+Math.sin(ph*9+i)*40*(1-ph);L.money(ctx,x,y,1-.4*ph,ph*5+i)}
  ctx.fillStyle='#c0c7d1';ctx.beginPath();ctx.moveTo(fx-220,fy-200);ctx.lineTo(fx+220,fy-200);ctx.lineTo(fx+40,fy+40);ctx.lineTo(fx+40,fy+180);ctx.lineTo(fx-40,fy+180);ctx.lineTo(fx-40,fy+40);ctx.closePath();ctx.fill();
  ctx.strokeStyle='#0b0d14';ctx.lineWidth=6;ctx.stroke();T(ctx,p.to,fx,fy-110,{px:90,fam:'Anton',w:400,fill:'#111'});
  if(p.balloons){for(let i=0;i<p.balloons;i++){const a=.3+i*.12,q=E.oc(S(lt,a,a+1.6)),x=W*(.42+i*.055),y=H*.16+(i%2)*90;if(q>0)L.balloon(ctx,x,y-q*30,30+q*45,{lt:lt+i,label:'',hue:180+i*14})}
    L.hilite(ctx,p.label,W*.3,H*.82,{px:90,fam:'Anton',w:400,p:S(lt,dur*.5,dur*.65)})}};

/* ================= paper ================= */
TPL.paper=(ctx,p,lt,dur)=>{L.bg(ctx,lt,{hue:p.mode==='earnings'?'red':'grey'});const x=W/2,y=H/2;
  if(p.mode==='site'){L.card(ctx,x-560,y-380,1120,760,{fill:'#c0c0c0',r:4});ctx.fillStyle='#000080';ctx.fillRect(x-554,y-374,1108,50);T(ctx,'Netscape — '+p.title,x-530,y-349,{px:28,fill:'#fff',align:'left'});
    ctx.fillStyle='#fff';ctx.fillRect(x-540,y-310,1080,670);T(ctx,'Welcome to the FUTURE!!',x,y-220,{px:60,fam:'Courier Prime',w:700,fill:'#000080'});
    ['Online shopping','Email for everyone','Free websites'].forEach((s,i)=>T(ctx,'• '+s,x-400,y-100+i*70,{px:44,fam:'Courier Prime',fill:'#000',align:'left'}));
    const q=E.back(S(lt,dur*.4,dur*.4+.4));if(q>0){ctx.save();ctx.translate(x+340,y+150);ctx.scale(q,q);ctx.strokeStyle=GRN;ctx.lineWidth=40;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(-90,0);ctx.lineTo(-20,70);ctx.lineTo(120,-90);ctx.stroke();ctx.restore()}return}
  if(p.mode==='earnings'){L.card(ctx,x-520,y-400,1040,800,{fill:'#f5f0e1',r:10});T(ctx,p.title,x,y-320,{px:56,fam:'Courier Prime',w:700,fill:'#222'});
    ctx.strokeStyle='#ccc';ctx.lineWidth=2;for(let i=0;i<6;i++){ctx.beginPath();ctx.moveTo(x-440,y-220+i*90);ctx.lineTo(x+440,y-220+i*90);ctx.stroke()}
    const q=S(lt,.3,dur*.8),pts=[[0,.3],[.2,.25],[.4,.2],[.55,.22],[.7,.6],[.85,.85],[1,.95]];ctx.strokeStyle=RED;ctx.lineWidth=14;ctx.lineJoin='round';ctx.beginPath();
    pts.forEach(([u,v],i)=>{if(u<=q+.01)(i?ctx.lineTo:ctx.moveTo).call(ctx,x-440+u*880,y-220+v*450)});ctx.stroke();if(q>.7)L.stamp(ctx,'MISSED',x+200,y-120,S(lt,dur*.65,dur*.75),{px:100});return}
  // dust: fake paper dissolves
  const d=S(lt,dur*.35,dur*.9);ctx.save();ctx.globalAlpha=1-d;ctx.translate(x,y);ctx.rotate(-.03);L.card(ctx,-380,-460,760,920,{fill:'#fbfaf6',r:6});
  T(ctx,p.title,0,-360,{px:56,fam:'Courier Prime',w:700,fill:'#222'});T(ctx,'Journal of Very Real Science',0,-290,{px:30,fam:'Courier Prime',fill:'#666'});
  ctx.fillStyle='#bbb';for(let i=0;i<14;i++)ctx.fillRect(-300,-200+i*44,i%3?560:600,12);ctx.restore();
  for(let i=0;i<220;i++){const sx=x+(L.hash(i,1)-.5)*760,sy=y+(L.hash(i,2)-.5)*920,dd=L.clamp(d*1.6-L.hash(i,3)*.6);if(dd<=0)continue;
    ctx.fillStyle=`rgba(240,236,225,${1-dd})`;ctx.fillRect(sx+dd*400*(L.hash(i,4)+.2),sy-dd*300*L.hash(i,5),6,6)}
  L.chip(ctx,'DOES NOT EXIST',x,H*.9,{px:50,bg:RED,fg:'#fff',p:S(lt,dur*.6,dur*.75)})};

/* ================= meter ================= */
TPL.meter=(ctx,p,lt,dur)=>{L.bg(ctx,lt,{hue:p.mode==='seismo'?'grey':'red'});
  const gauge=(x,y,v,label)=>{ctx.save();ctx.translate(x,y);ctx.lineWidth=46;[[GRN,-Math.PI,-Math.PI*.66],[Y,-Math.PI*.66,-Math.PI*.33],[RED,-Math.PI*.33,0]].forEach(([c,a,b])=>{ctx.strokeStyle=c;ctx.beginPath();ctx.arc(0,0,200,a,b);ctx.stroke()});
    const ang=-Math.PI+Math.PI*v+(v>.95?Math.sin(lt*40)*.03:0);ctx.strokeStyle='#fff';ctx.lineWidth=12;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(Math.cos(ang)*190,Math.sin(ang)*190);ctx.stroke();
    ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(0,0,20,0,7);ctx.fill();T(ctx,label,0,80,{px:48,fill:'#fff',track:6});ctx.restore()};
  if(p.mode==='valuation'){gauge(W*.27,H*.58,E.el(S(lt,.2,1.4)),'LOSS');const q=E.oc(S(lt,dur*.35,dur*.8));ctx.fillStyle='#8b95a5';L.rr(ctx,W*.66,H*.72,220,140,12);ctx.fill();T(ctx,'REALITY',W*.66+110,H*.72+70,{px:38,fill:'#111'});
    ctx.strokeStyle='rgba(255,255,255,.6)';ctx.setLineDash([10,10]);ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(W*.72,H*.72);ctx.lineTo(W*.72,H*.62-q*H*.32);ctx.stroke();ctx.setLineDash([]);
    L.balloon(ctx,W*.72,H*.5-q*H*.32,90+q*30,{lt,label:'',hue:40});L.chip(ctx,'VALUATION',W*.72,H*.5-q*H*.32,{px:36,p:q});return}
  if(p.mode==='profit'){gauge(W/2,H*.6,.02,'PROFIT');const q=S(lt,dur*.4,dur*.6);ctx.strokeStyle=RED;ctx.lineWidth=30;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(W/2-260,H*.32);ctx.lineTo(W/2-260+520*q,H*.32+400*q);ctx.stroke();
    T(ctx,'$0',W/2,H*.85,{px:120,fam:'Anton',w:400,fill:RED});return}
  // seismograph flat + empty SCAM frame
  const y0=H*.42;ctx.fillStyle='#f1efe8';ctx.fillRect(0,y0-220,W,440);ctx.strokeStyle='#d6d2c4';ctx.lineWidth=2;for(let x=-(lt*200)%80;x<W;x+=80){ctx.beginPath();ctx.moveTo(x,y0-220);ctx.lineTo(x,y0+220);ctx.stroke()}
  ctx.strokeStyle='#222';ctx.lineWidth=5;ctx.beginPath();for(let x=0;x<=W*.8;x+=6){const yy=y0+L.noise(x*.05+lt*10,3)*4;x?ctx.lineTo(x,yy):ctx.moveTo(x,yy)}ctx.stroke();ctx.fillStyle='#222';ctx.beginPath();ctx.arc(W*.8,y0,10,0,7);ctx.fill();
  T(ctx,'BHOOCHAAL: 0.0',W*.5,y0-170,{px:44,fam:'Courier Prime',w:700,fill:'#444'});
  const q=E.back(S(lt,dur*.45,dur*.45+.4));if(q>0){ctx.save();ctx.translate(W/2,H*.82);ctx.scale(q,q);ctx.strokeStyle=Y;ctx.lineWidth=10;ctx.setLineDash([24,16]);ctx.strokeRect(-260,-90,520,180);ctx.setLineDash([]);T(ctx,'SCAM?',0,0,{px:80,fam:'Anton',w:400,fill:'rgba(255,255,255,.35)'});ctx.restore()}};

/* ================= grid (office signs going dark) ================= */
TPL.grid=(ctx,p,lt,dur)=>{ctx.fillStyle='#07080c';ctx.fillRect(0,0,W,H);const names=['pets.com','webvan','eToys','Kozmo','boo.com','Flooz','Pixelon','GovWorks','theGlobe','Excite','Iridium','Napster'];
  for(let r=0;r<3;r++)for(let c=0;c<4;c++){const i=r*4+c,x=W*(.14+c*.24),y=H*(.2+r*.3),off=S(lt,.2+i*dur*.065,.3+i*dur*.065);const fl=off>0&&off<1&&L.hash(Math.floor(lt*20),i)>.5;
    ctx.fillStyle='#14161c';ctx.fillRect(x-200,y-110,400,220);const on=off<1&&!fl;ctx.save();if(on){ctx.shadowColor=['#ff3df2','#3fd8ff','#ffd23f'][i%3];ctx.shadowBlur=30}
    T(ctx,names[i],x,y,{px:52,w:800,fill:on?'#fff':'#2a2d35'});ctx.restore()}};

/* ================= end screen (YouTube elements go on top in Studio) ================= */
TPL.endscreen=(ctx,p,lt,dur)=>{L.bg(ctx,lt,{hue:'navy',src:'style_frame',alpha:.25});
  L.balloon(ctx,W*.5,H*.18+Math.sin(lt)*10,90,{lt,label:'AI',stretch:.8});
  [[W*.28,H*.55],[W*.72,H*.55]].forEach(([x,y],i)=>{ctx.save();ctx.strokeStyle='rgba(255,255,255,.35)';ctx.lineWidth=4;ctx.setLineDash([18,12]);ctx.lineDashOffset=-lt*30;L.rr(ctx,x-380,y-214,760,428,20);ctx.stroke();ctx.restore()});
  ctx.save();ctx.strokeStyle='rgba(255,255,255,.35)';ctx.lineWidth=4;ctx.beginPath();ctx.arc(W/2,H*.88,70,0,7);ctx.stroke();ctx.restore();
  T(ctx,'Agla episode dekho 👇',W/2,H*.3,{px:56,fill:'#fff',alpha:E.oc(S(lt,.2,.8))});L.dust(ctx,lt,40,.5)};
})();
