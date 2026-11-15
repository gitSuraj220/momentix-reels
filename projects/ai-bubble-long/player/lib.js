/* AI Bubble player — shared drawing helpers (window.L). Deterministic: no Math.random. */
(function(){
const W=1920,H=1080;
const L=window.L={IMG:{},W,H,frame:0};
const Y='#ffd23f',RED='#ff3b3b',GRN='#2ee59d',CY='#3fd8ff',INK='#0b0d14';
Object.assign(L,{Y,RED,GRN,CY,INK});
L.clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
L.lerp=(a,b,t)=>a+(b-a)*t;
L.seg=(t,a,b)=>L.clamp((t-a)/(b-a));
L.ease={io:t=>t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2,oc:t=>1-Math.pow(1-t,3),ic:t=>t*t*t,
  ioc:t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2,
  back:t=>{const c=1.70158,c3=c+1;return 1+c3*Math.pow(t-1,3)+c*Math.pow(t-1,2)},
  el:t=>t===0||t===1?t:Math.pow(2,-10*t)*Math.sin((t*10-.75)*2*Math.PI/3)+1};
L.hash=(a,b=0)=>{let h=(a*374761393+b*668265263)|0;h=(h^(h>>>13))*1274126177|0;return((h^(h>>>16))>>>0)/4294967296};
L.noise=(x,s=0)=>{const i=Math.floor(x),f=x-i,u=f*f*(3-2*f);return L.lerp(L.hash(i,s),L.hash(i+1,s),u)*2-1};

/* ---------- number formatting ---------- */
L.fmt=(v,{dec=0,indian=false}={})=>{
  const neg=v<0;v=Math.abs(v);let s=v.toFixed(dec),[a,b]=s.split('.');
  if(indian&&a.length>3){const last=a.slice(-3);let rest=a.slice(0,-3);rest=rest.replace(/\B(?=(\d{2})+(?!\d))/g,',');a=rest+','+last}
  else a=a.replace(/\B(?=(\d{3})+(?!\d))/g,',');
  return(neg?'-':'')+a+(b?'.'+b:'')};

/* ---------- text ---------- */
L.font=(ctx,px,w=800,fam='Poppins')=>{ctx.font=`${w} ${px}px ${fam}`};
L.text=(ctx,s,x,y,{px=80,w=800,fam='Poppins',fill='#fff',align='center',base='middle',stroke=0,sc='#000',glow=0,gc=Y,alpha=1,track=0}={})=>{
  ctx.save();ctx.globalAlpha*=alpha;L.font(ctx,px,w,fam);ctx.textAlign=align;ctx.textBaseline=base;
  if(track)ctx.letterSpacing=track+'px';
  if(glow){ctx.shadowColor=gc;ctx.shadowBlur=glow}
  if(stroke){ctx.lineJoin='round';ctx.lineWidth=stroke;ctx.strokeStyle=sc;ctx.strokeText(s,x,y)}
  ctx.fillStyle=fill;ctx.fillText(s,x,y);ctx.restore()};
L.wrap=(ctx,s,maxW)=>{const words=s.split(/\s+/),out=[];let cur='';
  for(const w of words){const t=cur?cur+' '+w:w;if(ctx.measureText(t).width>maxW&&cur){out.push(cur);cur=w}else cur=t}
  if(cur)out.push(cur);return out};
/* yellow highlight pill behind a word / number */
L.hilite=(ctx,s,x,y,{px=90,w=800,fam='Poppins',p=1,fill='#111',bg=Y,pad=22,align='center'}={})=>{
  ctx.save();L.font(ctx,px,w,fam);const tw=ctx.measureText(s).width;const x0=align==='center'?x-tw/2:x;
  ctx.fillStyle=bg;L.rr(ctx,x0-pad,y-px*.62,(tw+pad*2)*L.ease.oc(p),px*1.24,px*.18);ctx.fill();
  ctx.fillStyle=fill;ctx.textAlign='left';ctx.textBaseline='middle';
  ctx.save();ctx.beginPath();ctx.rect(x0-pad,y-px,(tw+pad*2)*L.ease.oc(p),px*2);ctx.clip();ctx.fillText(s,x0,y+px*.04);ctx.restore();ctx.restore()};
L.rr=(ctx,x,y,w,h,r)=>{r=Math.min(r,Math.abs(w)/2,Math.abs(h)/2);ctx.beginPath();ctx.moveTo(x+r,y);ctx.arcTo(x+w,y,x+w,y+h,r);ctx.arcTo(x+w,y+h,x,y+h,r);ctx.arcTo(x,y+h,x,y,r);ctx.arcTo(x,y,x+w,y,r);ctx.closePath()};
L.pop=(t,a,d=.35)=>L.ease.back(L.seg(t,a,a+d));

/* ---------- backgrounds ---------- */
// code-shot background: deep gradient + soft grid + drifting bokeh + (optional) blurred art plate
L.bg=(ctx,lt,{hue='navy',src=null,grid=true,alpha=.28}={})=>{
  const pal={navy:['#121a33','#05070f'],red:['#3a0d12','#090306'],green:['#0c2a20','#030a07'],gold:['#33240b','#0a0703'],
    purple:['#22123a','#07040d'],teal:['#08303a','#02090c'],grey:['#22252c','#0a0b0e']}[hue]||['#121a33','#05070f'];
  const g=ctx.createRadialGradient(W/2,H*.42,80,W/2,H/2,W*.75);g.addColorStop(0,pal[0]);g.addColorStop(1,pal[1]);
  ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
  if(src&&L.IMG[src]){ctx.save();ctx.globalAlpha=alpha;ctx.filter='blur(14px) saturate(.8)';
    const z=1.15+lt*.01;ctx.drawImage(L.IMG[src],W/2-W*z/2,H/2-H*z/2,W*z,H*z);ctx.restore()}
  if(grid){ctx.save();ctx.strokeStyle='rgba(255,255,255,.045)';ctx.lineWidth=2;const o=(lt*18)%80;
    ctx.beginPath();for(let x=-80+o;x<W+80;x+=80){ctx.moveTo(x,0);ctx.lineTo(x,H)}for(let y=-80+o*.5;y<H+80;y+=80){ctx.moveTo(0,y);ctx.lineTo(W,y)}ctx.stroke();ctx.restore()}
  L.bokeh(ctx,lt,hue)};
L.bokeh=(ctx,lt,hue)=>{ctx.save();ctx.globalCompositeOperation='lighter';
  for(let i=0;i<16;i++){const x=(L.hash(i,7)*W+lt*(10+L.hash(i,8)*30))%(W+200)-100,y=L.hash(i,9)*H+Math.sin(lt*.5+i)*20,r=30+L.hash(i,3)*90;
    const g=ctx.createRadialGradient(x,y,0,x,y,r);const c=hue==='red'?'255,80,80':hue==='green'?'80,255,170':hue==='gold'?'255,200,90':'90,170,255';
    g.addColorStop(0,`rgba(${c},.10)`);g.addColorStop(1,`rgba(${c},0)`);ctx.fillStyle=g;ctx.beginPath();ctx.arc(x,y,r,0,7);ctx.fill()}
  ctx.restore()};
L.city=(ctx,lt,{y=H*.78,col='#0a0e1c',lights=true}={})=>{ctx.save();
  for(let layer=0;layer<2;layer++){ctx.fillStyle=layer?col:'#151b30';const off=-lt*(layer?14:6);
    for(let i=0;i<40;i++){const bw=50+L.hash(i,layer+20)*90,bh=(layer?120:200)+L.hash(i,layer+30)*(layer?260:220),x=((i*110+off)%(W+220)+W+220)%(W+220)-110;
      ctx.fillRect(x,y-bh+(layer?40:0),bw,bh+H);
      if(lights&&layer)for(let k=0;k<10;k++){if(L.hash(i*10+k,4)>.55){ctx.fillStyle=`rgba(255,210,120,${.35+.3*L.hash(i,k)})`;ctx.fillRect(x+8+(k%3)*(bw-16)/3,y-bh+60+Math.floor(k/3)*40,8,12);ctx.fillStyle=col}}}}
  ctx.restore()};
L.dust=(ctx,lt,n=40,a=.5)=>{ctx.save();ctx.globalCompositeOperation='lighter';
  for(let i=0;i<n;i++){const s=L.hash(i,11),x=(L.hash(i,12)*W+lt*(8+s*25)+Math.sin(lt*.7+i)*14)%W,y=(L.hash(i,13)*H-lt*(4+s*10)+H*4)%H,r=1+s*3;
    ctx.fillStyle=`rgba(255,235,200,${a*(.25+.5*L.hash(i,14))*(.6+.4*Math.sin(lt*2+i))})`;ctx.beginPath();ctx.arc(x,y,r,0,7);ctx.fill()}
  ctx.restore()};
L.rays=(ctx,lt,{x=W*.8,y=-80,a=.10}={})=>{ctx.save();ctx.globalCompositeOperation='lighter';
  for(let i=0;i<5;i++){const ang=1.85+i*.13+Math.sin(lt*.3+i)*.03;const g=ctx.createLinearGradient(x,y,x+Math.cos(ang)*1600,y+Math.sin(ang)*1600);
    g.addColorStop(0,`rgba(255,220,160,${a})`);g.addColorStop(1,'rgba(255,220,160,0)');ctx.fillStyle=g;ctx.beginPath();ctx.moveTo(x,y);
    ctx.lineTo(x+Math.cos(ang-.04)*1800,y+Math.sin(ang-.04)*1800);ctx.lineTo(x+Math.cos(ang+.04)*1800,y+Math.sin(ang+.04)*1800);ctx.fill()}
  ctx.restore()};

/* ---------- HF art with Ken Burns (max 1.15x) ---------- */
L.art=(ctx,src,lt,dur,{crop=null,kb='in',flip=false,speed=0,freeze=null,shake=0}={})=>{
  const im=L.IMG[src];if(!im)return false;
  let [cx,cy,cw,ch]=crop||[0,0,1,1];
  const ar=W/H;if(cw*im.width/(ch*im.height)>ar){const nw=ch*im.height*ar/im.width;cx+=(cw-nw)/2;cw=nw}else{const nh=cw*im.width/ar/im.height;cy+=(ch-nh)/2;ch=nh}
  let p=L.clamp(lt/Math.max(dur,.1));if(freeze!=null&&p>freeze)p=freeze;
  const e=L.ease.io(p)*.5+p*.5,amt=speed?.15:.1;
  let z=1,dx=0,dy=0;
  if(kb==='in')z=1+amt*e;else if(kb==='out')z=1+amt*(1-e);
  else if(kb==='l'){z=1+amt;dx=amt*(e-.5)}else if(kb==='r'){z=1+amt;dx=-amt*(e-.5)}else if(kb==='up'){z=1+amt;dy=amt*(.5-e)*.8}
  const sw=cw*im.width/z,sh=ch*im.height/z;let sx=cx*im.width+(cw*im.width-sw)/2+dx*sw*.5,sy=cy*im.height+(ch*im.height-sh)/2+dy*sh*.5;
  sx=L.clamp(sx,0,im.width-sw);sy=L.clamp(sy,0,im.height-sh);
  ctx.save();
  if(shake){const k=L.shakeAmt(lt,dur,shake);ctx.translate(k[0],k[1])}
  if(flip){ctx.translate(W,0);ctx.scale(-1,1)}
  ctx.imageSmoothingQuality='high';ctx.drawImage(im,sx,sy,sw,sh,-12,-12,W+24,H+24);ctx.restore();
  return {sx,sy,sw,sh,im}};
// map 0-1 image coords to screen through the last art() transform
L.map=(r,info)=>{if(!info)return[r[0]*W,r[1]*H,(r[2]||0)*W,(r[3]||0)*H];
  const kx=(W+24)/info.sw,ky=(H+24)/info.sh;return[(r[0]*info.im.width-info.sx)*kx-12,(r[1]*info.im.height-info.sy)*ky-12,(r[2]||0)*info.im.width*kx,(r[3]||0)*info.im.height*ky]};
L.shakeAmt=(lt,dur,amp,at=.12)=>{const d=lt-dur*at;if(d<0)return[0,0];const k=amp*60*Math.exp(-d*7);return[L.noise(lt*40,1)*k,L.noise(lt*40,2)*k]};

/* ---------- post: grade, vignette, grain ---------- */
let GR=[];
L.init=()=>{GR=[];for(let k=0;k<8;k++){const c=document.createElement('canvas');c.width=c.height=384;const g=c.getContext('2d'),d=g.createImageData(384,384);
  for(let i=0;i<d.data.length;i+=4){const v=L.hash(i/4+k*1e6,k)*255;d.data[i]=d.data[i+1]=d.data[i+2]=v;d.data[i+3]=255}g.putImageData(d,0,0);GR.push(c)}};
L.post=(ctx,t,s)=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);
  const v=ctx.createRadialGradient(W/2,H/2,H*.38,W/2,H/2,W*.66);v.addColorStop(0,'rgba(0,0,0,0)');v.addColorStop(1,'rgba(0,0,0,.55)');
  ctx.fillStyle=v;ctx.fillRect(0,0,W,H);
  if(GR.length){ctx.globalCompositeOperation='overlay';ctx.globalAlpha=.10;const g=GR[L.frame%GR.length];
    const ox=-(L.hash(L.frame,5)*384|0),oy=-(L.hash(L.frame,6)*384|0);ctx.fillStyle=ctx.createPattern(g,'repeat');ctx.translate(ox,oy);ctx.fillRect(0,0,W+384,H+384)}
  ctx.restore()};

/* ---------- shapes ---------- */
L.chip=(ctx,s,x,y,{px=40,bg=Y,fg='#111',p=1,r=null,rot=0}={})=>{ctx.save();ctx.translate(x,y);ctx.rotate(rot);const k=L.ease.back(L.clamp(p));ctx.scale(k,k);
  L.font(ctx,px,800);const tw=ctx.measureText(s).width;ctx.fillStyle=bg;ctx.shadowColor='rgba(0,0,0,.45)';ctx.shadowBlur=24;ctx.shadowOffsetY=8;
  L.rr(ctx,-tw/2-px*.55,-px*.8,tw+px*1.1,px*1.6,r==null?px*.4:r);ctx.fill();ctx.shadowColor='transparent';
  ctx.fillStyle=fg;ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(s,0,px*.05);ctx.restore()};
L.stamp=(ctx,s,x,y,p,{col=RED,px=150,rot=-.18}={})=>{if(p<=0)return;const k=p<1?L.lerp(2.4,1,L.ease.oc(p)):1;
  ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.scale(k,k);ctx.globalAlpha=L.clamp(p*3);
  L.font(ctx,px,400,'Marker');const tw=ctx.measureText(s).width;ctx.strokeStyle=col;ctx.lineWidth=px*.09;
  L.rr(ctx,-tw/2-px*.35,-px*.72,tw+px*.7,px*1.44,px*.12);ctx.stroke();ctx.fillStyle=col;ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(s,0,px*.06);
  ctx.globalCompositeOperation='destination-out';for(let i=0;i<60;i++){ctx.beginPath();ctx.arc((L.hash(i,1)-.5)*(tw+px),(L.hash(i,2)-.5)*px*1.4,2+L.hash(i,3)*6,0,7);ctx.fill()}
  ctx.restore()};
L.phone=(ctx,x,y,w,h,{dark=true}={})=>{ctx.save();ctx.shadowColor='rgba(0,0,0,.6)';ctx.shadowBlur=60;ctx.shadowOffsetY=20;ctx.fillStyle='#111';L.rr(ctx,x,y,w,h,w*.13);ctx.fill();
  ctx.shadowColor='transparent';ctx.fillStyle=dark?'#17181c':'#f5f6f8';L.rr(ctx,x+w*.04,y+w*.04,w*.92,h-w*.08,w*.1);ctx.fill();
  ctx.fillStyle='#000';L.rr(ctx,x+w*.38,y+w*.07,w*.24,w*.06,w*.03);ctx.fill();ctx.restore();return[x+w*.04,y+w*.04,w*.92,h-w*.08]};
L.card=(ctx,x,y,w,h,{fill='#fff',r=28,shadow=true}={})=>{ctx.save();if(shadow){ctx.shadowColor='rgba(0,0,0,.5)';ctx.shadowBlur=50;ctx.shadowOffsetY=18}
  ctx.fillStyle=fill;L.rr(ctx,x,y,w,h,r);ctx.fill();ctx.restore()};
L.burst=(ctx,x,y,r,p,{col=Y,n=14}={})=>{if(p<=0||p>=1)return;ctx.save();ctx.strokeStyle=col;ctx.lineCap='round';ctx.lineWidth=8*(1-p);
  for(let i=0;i<n;i++){const a=i/n*Math.PI*2,r0=r*(.6+p*.7),r1=r*(.8+p*1.1);ctx.beginPath();ctx.moveTo(x+Math.cos(a)*r0,y+Math.sin(a)*r0);ctx.lineTo(x+Math.cos(a)*r1,y+Math.sin(a)*r1);ctx.stroke()}ctx.restore()};
L.confetti=(ctx,lt,{n=90,cols=[Y,RED,CY,GRN,'#ff7ad9'],cheques=false}={})=>{ctx.save();
  for(let i=0;i<n;i++){const s=L.hash(i,40),x=L.hash(i,41)*W+Math.sin(lt*2+i)*40,y=((L.hash(i,42)*H*1.4+lt*(160+s*220))%(H+200))-100,a=lt*(3+s*5)+i;
    ctx.save();ctx.translate(x,y);ctx.rotate(a);ctx.scale(1,Math.cos(a*1.3));
    if(cheques&&i%3==0){ctx.fillStyle='#e9f3e6';ctx.fillRect(-46,-22,92,44);ctx.strokeStyle='#5a8a5a';ctx.lineWidth=2;ctx.strokeRect(-40,-16,80,32);ctx.fillStyle='#5a8a5a';ctx.fillRect(-30,-4,40,4)}
    else{ctx.fillStyle=cols[i%cols.length];ctx.fillRect(-9,-5,18,10)}ctx.restore()}ctx.restore()};
L.money=(ctx,x,y,s,rot)=>{ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.scale(s,s);ctx.fillStyle='#8fd18b';L.rr(ctx,-60,-30,120,60,6);ctx.fill();
  ctx.strokeStyle='#3d7a3a';ctx.lineWidth=3;ctx.strokeRect(-52,-22,104,44);ctx.fillStyle='#3d7a3a';ctx.beginPath();ctx.arc(0,0,14,0,7);ctx.fill();
  ctx.fillStyle='#8fd18b';L.font(ctx,20,800);ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('$',0,1);ctx.restore()};
L.coin=(ctx,x,y,r,spin=0)=>{ctx.save();ctx.translate(x,y);ctx.scale(Math.cos(spin)||.05,1);const g=ctx.createRadialGradient(-r*.3,-r*.3,r*.1,0,0,r);
  g.addColorStop(0,'#fff3a6');g.addColorStop(1,'#d39a12');ctx.fillStyle=g;ctx.beginPath();ctx.arc(0,0,r,0,7);ctx.fill();ctx.strokeStyle='#9a6a00';ctx.lineWidth=r*.1;ctx.stroke();
  ctx.fillStyle='#9a6a00';L.font(ctx,r*1.1,800);ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('$',0,r*.05);ctx.restore()};

/* ---------- balloon (the AI bubble) ---------- */
L.balloon=(ctx,x,y,r,{lt=0,stretch=0,cracks=0,label='AI',hue=195,wob=0}={})=>{
  ctx.save();ctx.translate(x,y);const sx=1+stretch*.06+Math.sin(lt*9)*wob*.03,sy=1+stretch*.1-Math.sin(lt*9)*wob*.03;ctx.scale(sx,sy);
  // string
  ctx.strokeStyle='rgba(255,255,255,.55)';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(0,r*1.02);
  for(let k=1;k<=10;k++)ctx.lineTo(Math.sin(lt*2+k*.8)*12*k/10,r*1.02+k*r*.09);ctx.stroke();
  ctx.fillStyle=`hsl(${hue},70%,38%)`;ctx.beginPath();ctx.moveTo(-r*.08,r*.98);ctx.lineTo(r*.08,r*.98);ctx.lineTo(0,r*1.08);ctx.fill();
  ctx.shadowColor=`hsla(${hue},90%,60%,.55)`;ctx.shadowBlur=r*.5;
  const g=ctx.createRadialGradient(-r*.35,-r*.4,r*.05,0,0,r*1.05);g.addColorStop(0,`hsl(${hue},95%,${78-stretch*5}%)`);g.addColorStop(.55,`hsl(${hue},80%,50%)`);g.addColorStop(1,`hsl(${hue+20},80%,${26-stretch*4}%)`);
  ctx.fillStyle=g;ctx.beginPath();ctx.ellipse(0,0,r*.92,r,0,0,7);ctx.fill();ctx.shadowColor='transparent';
  ctx.strokeStyle='#081018';ctx.lineWidth=Math.max(4,r*.025);ctx.stroke();
  // highlight
  ctx.fillStyle='rgba(255,255,255,.55)';ctx.beginPath();ctx.ellipse(-r*.42,-r*.48,r*.13,r*.24,-.6,0,7);ctx.fill();
  // stretch marks
  if(stretch>0){ctx.strokeStyle=`rgba(255,255,255,${.25*stretch})`;ctx.lineWidth=3;for(let i=0;i<9;i++){const a=-1.2+i*.3;ctx.beginPath();ctx.arc(0,0,r*(.75+.04*Math.sin(i)),a,a+.12);ctx.stroke()}}
  if(label){L.text(ctx,label,0,r*.05,{px:r*.48,fam:'Anton',w:400,fill:'rgba(255,255,255,.92)',stroke:r*.03,sc:'rgba(0,20,40,.6)'})}
  if(cracks>0){ctx.strokeStyle='rgba(10,10,20,.9)';ctx.lineWidth=Math.max(2,r*.012);ctx.lineCap='round';
    for(let c=0;c<5;c++){let px=(L.hash(c,71)-.5)*r*.9,py=(L.hash(c,72)-.5)*r*.9;const n=Math.floor(8*cracks);ctx.beginPath();ctx.moveTo(px,py);
      for(let k=0;k<n;k++){px+=(L.hash(c*20+k,73)-.5)*r*.18;py+=(L.hash(c*20+k,74)-.5)*r*.18;ctx.lineTo(px,py)}ctx.stroke()}}
  ctx.restore()};

/* ---------- logos (drawn wordmarks; swap for real SVGs in art/logos/ if A adds them) ---------- */
const GC=['#4285F4','#EA4335','#FBBC05','#4285F4','#34A853','#EA4335'];
L.logo=(ctx,name,x,y,h=80,{align='center',light=true,mark=true}={})=>{
  ctx.save();ctx.translate(x,y);const fg=light?'#fff':'#111';ctx.textBaseline='middle';
  const word=(s,px,w=700,fam='Poppins',col=fg,ox=0)=>{L.font(ctx,px,w,fam);ctx.fillStyle=col;ctx.textAlign='left';ctx.fillText(s,ox,px*.04);return ctx.measureText(s).width};
  const measure=(s,px,w=700,fam='Poppins')=>{L.font(ctx,px,w,fam);return ctx.measureText(s).width};
  let mw=0,tw=0,draw;
  const n=name.toLowerCase();
  if(n==='google'||n==='bard'&&false){tw=measure('Google',h,500);draw=o=>{L.font(ctx,h,500);let xx=o;'Google'.split('').forEach((c,i)=>{ctx.fillStyle=GC[i];ctx.fillText(c,xx,h*.04);xx+=ctx.measureText(c).width})}}
  else if(n==='microsoft'){mw=h*.9;tw=measure('Microsoft',h*.62,500);draw=o=>{const s=h*.42;[['#F25022',0,0],['#7FBA00',1,0],['#00A4EF',0,1],['#FFB900',1,1]].forEach(([c,i,j])=>{ctx.fillStyle=c;ctx.fillRect(o+i*(s+h*.05),-h*.45+j*(s+h*.05),s,s)});word('Microsoft',h*.62,500,'Poppins',light?'#e8e8e8':'#5e5e5e',o+mw+h*.2)}}
  else if(n==='amazon'){tw=measure('amazon',h,700);draw=o=>{word('amazon',h,700,'Poppins',fg,o);ctx.strokeStyle='#FF9900';ctx.lineWidth=h*.09;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(o+tw*.1,h*.42);ctx.quadraticCurveTo(o+tw*.5,h*.72,o+tw*.86,h*.38);ctx.stroke();
    ctx.beginPath();ctx.moveTo(o+tw*.78,h*.32);ctx.lineTo(o+tw*.88,h*.36);ctx.lineTo(o+tw*.86,h*.48);ctx.stroke()}}
  else if(n==='meta'){mw=h*1.6;tw=measure('Meta',h*.8,600);draw=o=>{ctx.strokeStyle='#0081FB';ctx.lineWidth=h*.17;ctx.lineCap='round';ctx.beginPath();
    for(let i=0;i<=60;i++){const a=i/60*Math.PI*2,d=1+Math.sin(a)**2;const px=o+mw/2+Math.cos(a)/d*mw*.45,py=Math.sin(a)*Math.cos(a)/d*h*.9;i?ctx.lineTo(px,py):ctx.moveTo(px,py)}ctx.stroke();word('Meta',h*.8,600,'Poppins',fg,o+mw+h*.25)}}
  else if(n==='nvidia'){mw=h*1.1;tw=measure('NVIDIA',h*.8,800);draw=o=>{ctx.fillStyle='#76B900';ctx.fillRect(o,-h*.5,mw,h);ctx.strokeStyle='#fff';ctx.lineWidth=h*.08;ctx.beginPath();ctx.ellipse(o+mw*.55,0,mw*.32,h*.26,0,0,7);ctx.stroke();
    ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(o+mw*.55,0,h*.1,0,7);ctx.fill();word('NVIDIA',h*.8,800,'Poppins',light?'#fff':'#111',o+mw+h*.25)}}
  else if(n==='openai'||n==='chatgpt'){const tx=n==='openai'?'OpenAI':'ChatGPT';mw=h;tw=measure(tx,h*.75,600);draw=o=>{
    if(n==='chatgpt'){ctx.fillStyle='#10a37f';L.rr(ctx,o,-h*.5,h,h,h*.22);ctx.fill()}
    ctx.save();ctx.translate(o+h/2,0);ctx.strokeStyle=n==='chatgpt'?'#fff':fg;ctx.lineWidth=h*.075;for(let i=0;i<6;i++){ctx.rotate(Math.PI/3);ctx.beginPath();ctx.ellipse(0,-h*.17,h*.1,h*.2,0,0,7);ctx.stroke()}ctx.restore();
    word(tx,h*.75,600,'Poppins',fg,o+mw+h*.25)}}
  else if(n==='instagram'){mw=h;tw=measure('Instagram',h*.72,600);draw=o=>{const g=ctx.createLinearGradient(o,h*.5,o+h,-h*.5);g.addColorStop(0,'#FEDA75');g.addColorStop(.35,'#FA7E1E');g.addColorStop(.6,'#D62976');g.addColorStop(1,'#4F5BD5');
    ctx.fillStyle=g;L.rr(ctx,o,-h*.5,h,h,h*.26);ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=h*.08;L.rr(ctx,o+h*.2,-h*.3,h*.6,h*.6,h*.17);ctx.stroke();ctx.beginPath();ctx.arc(o+h/2,0,h*.15,0,7);ctx.stroke();
    ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(o+h*.69,-h*.19,h*.045,0,7);ctx.fill();word('Instagram',h*.72,600,'Poppins',fg,o+mw+h*.25)}}
  else if(n==='facebook'){mw=h;tw=measure('Facebook',h*.72,700);draw=o=>{ctx.fillStyle='#1877F2';ctx.beginPath();ctx.arc(o+h/2,0,h/2,0,7);ctx.fill();
    L.font(ctx,h*.8,800);ctx.fillStyle='#fff';ctx.textAlign='center';ctx.fillText('f',o+h*.55,h*.12);word('Facebook',h*.72,700,'Poppins',fg,o+mw+h*.25)}}
  else if(n==='gemini'||n==='bard'){const tx=n==='gemini'?'Gemini':'Bard';mw=h;tw=measure(tx,h*.75,600);draw=o=>{const g=ctx.createLinearGradient(o,h*.5,o+h,-h*.5);g.addColorStop(0,'#4796E3');g.addColorStop(1,'#C86FD7');
    ctx.fillStyle=g;ctx.beginPath();const c=o+h/2;ctx.moveTo(c,-h*.5);ctx.quadraticCurveTo(c,0,c+h*.5,0);ctx.quadraticCurveTo(c,0,c,h*.5);ctx.quadraticCurveTo(c,0,c-h*.5,0);ctx.quadraticCurveTo(c,0,c,-h*.5);ctx.fill();
    word(tx,h*.75,600,'Poppins',fg,o+mw+h*.25)}}
  else if(n==='anthropic'){tw=measure('ANTHROPIC',h*.7,700);draw=o=>word('ANTHROPIC',h*.7,700,'Poppins',light?'#f0e6d8':'#191919',o)}
  else if(n==='the new york times'){tw=measure('The New York Times',h*.7,700,'Caveat');draw=o=>word('The New York Times',h*.7,700,'Caveat',fg,o)}
  else{tw=measure(name,h*.72,700);draw=o=>word(name,h*.72,700,'Poppins',fg,o)}
  const total=mw+(mw?h*.25:0)+tw;const o=align==='center'?-total/2:align==='right'?-total:0;draw(o);ctx.restore();return total};

/* ---------- icons (simple flat drawings, size s = box) ---------- */
L.icon=(ctx,name,x,y,s,{col='#fff',p=1}={})=>{ctx.save();ctx.translate(x,y);const k=L.ease.back(L.clamp(p));ctx.scale(k*s/100,k*s/100);ctx.lineJoin='round';ctx.lineCap='round';
  ctx.strokeStyle='#0b0d14';ctx.lineWidth=6;const f=(c)=>{ctx.fillStyle=c;ctx.fill();ctx.stroke()};
  switch(name){
  case 'gpu':L.rr(ctx,-48,-28,96,56,6);f('#2b2f3a');ctx.fillStyle='#76B900';ctx.fillRect(-48,-28,96,8);[-22,22].forEach(cx=>{ctx.beginPath();ctx.arc(cx,4,18,0,7);f('#11141b');ctx.strokeStyle='#666';ctx.lineWidth=3;for(let i=0;i<6;i++){ctx.beginPath();ctx.moveTo(cx,4);ctx.lineTo(cx+Math.cos(i)*15,4+Math.sin(i)*15);ctx.stroke()}ctx.strokeStyle='#0b0d14';ctx.lineWidth=6});
    ctx.fillStyle='#d4a017';ctx.fillRect(-36,28,60,8);break;
  case 'chip':L.rr(ctx,-30,-30,60,60,6);f('#2e3440');ctx.fillStyle='#76B900';ctx.fillRect(-16,-16,32,32);ctx.strokeStyle='#c9c9c9';ctx.lineWidth=4;for(let i=-2;i<=2;i++){[[i*12,-30,i*12,-44],[i*12,30,i*12,44],[-30,i*12,-44,i*12],[30,i*12,44,i*12]].forEach(([a,b,c,d])=>{ctx.beginPath();ctx.moveTo(a,b);ctx.lineTo(c,d);ctx.stroke()})}break;
  case 'bolt':ctx.beginPath();ctx.moveTo(8,-48);ctx.lineTo(-26,6);ctx.lineTo(-2,6);ctx.lineTo(-10,48);ctx.lineTo(26,-8);ctx.lineTo(2,-8);ctx.closePath();f(Y);break;
  case 'snow':ctx.strokeStyle=CY;ctx.lineWidth=8;for(let i=0;i<3;i++){ctx.save();ctx.rotate(i*Math.PI/3);ctx.beginPath();ctx.moveTo(0,-44);ctx.lineTo(0,44);ctx.moveTo(-12,-32);ctx.lineTo(0,-22);ctx.lineTo(12,-32);ctx.moveTo(-12,32);ctx.lineTo(0,22);ctx.lineTo(12,32);ctx.stroke();ctx.restore()}break;
  case 'building':ctx.beginPath();ctx.rect(-34,-46,68,92);f('#5b6b8c');ctx.fillStyle=Y;for(let i=0;i<4;i++)for(let j=0;j<3;j++)ctx.fillRect(-24+j*18,-36+i*20,10,10);break;
  case 'cloud':ctx.beginPath();ctx.arc(-20,8,24,Math.PI*.5,Math.PI*1.5);ctx.arc(2,-14,28,Math.PI,0);ctx.arc(26,6,22,-Math.PI*.5,Math.PI*.5);ctx.closePath();f('#dbe9ff');break;
  case 'speech':L.rr(ctx,-44,-36,88,58,18);f('#fff');ctx.beginPath();ctx.moveTo(-14,22);ctx.lineTo(-24,42);ctx.lineTo(4,22);f('#fff');break;
  case 'gavel':ctx.save();ctx.rotate(-.6);L.rr(ctx,-34,-38,68,30,6);f('#8b5a2b');ctx.beginPath();ctx.rect(-6,-8,12,58);f('#a8713a');ctx.restore();ctx.beginPath();ctx.rect(-40,34,60,12);f('#6b4423');break;
  case 'paper':ctx.beginPath();ctx.rect(-36,-46,72,92);f('#f4f1ea');ctx.fillStyle='#333';ctx.fillRect(-26,-36,52,10);ctx.fillStyle='#999';for(let i=0;i<5;i++)ctx.fillRect(-26,-18+i*12,i%2?40:52,5);break;
  case 'phone':L.rr(ctx,-28,-48,56,96,10);f('#1d1f26');ctx.fillStyle='#4aa3ff';ctx.fillRect(-22,-40,44,76);break;
  case 'search':ctx.beginPath();ctx.arc(-8,-8,26,0,7);ctx.lineWidth=10;ctx.strokeStyle='#fff';ctx.stroke();ctx.beginPath();ctx.moveTo(12,12);ctx.lineTo(38,38);ctx.lineWidth=14;ctx.stroke();break;
  case 'rate':ctx.beginPath();ctx.arc(0,0,44,0,7);f(RED);L.text(ctx,'%',0,4,{px:56,fill:'#fff'});break;
  case 'tag':ctx.beginPath();ctx.moveTo(-44,-24);ctx.lineTo(20,-24);ctx.lineTo(44,0);ctx.lineTo(20,24);ctx.lineTo(-44,24);ctx.closePath();f(Y);ctx.fillStyle='#0b0d14';ctx.beginPath();ctx.arc(22,0,6,0,7);ctx.fill();L.text(ctx,'$',-12,2,{px:34,fill:'#111'});break;
  case 'bag':ctx.beginPath();ctx.moveTo(-14,-34);ctx.lineTo(14,-34);ctx.lineTo(6,-22);ctx.quadraticCurveTo(46,0,34,36);ctx.lineTo(-34,36);ctx.quadraticCurveTo(-46,0,-6,-22);ctx.closePath();f('#c8a15a');L.text(ctx,'$',0,8,{px:40,fill:'#5a3d0a'});break;
  case 'fire':ctx.beginPath();ctx.moveTo(0,-48);ctx.quadraticCurveTo(40,-6,26,26);ctx.quadraticCurveTo(14,46,0,46);ctx.quadraticCurveTo(-30,46,-30,16);ctx.quadraticCurveTo(-30,-10,0,-48);f('#ff7a1a');break;
  default:ctx.beginPath();ctx.arc(0,0,40,0,7);f('#fff');}
  ctx.restore()};
})();
