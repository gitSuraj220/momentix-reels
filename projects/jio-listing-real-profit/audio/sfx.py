# SFX cued from the same voice cues the film uses; mix with voice to -16 LUFS (Suraj adds music later).
import numpy as np, json, subprocess, sys
sys.path.insert(0,'/home/claude/momentix-reels/engine')
SR=48000
CU=json.load(open('../vo/cues.json')); S=lambda i:[c for c in CU if c['id']==i][0]['s']; E=lambda i:[c for c in CU if c['id']==i][0]['e']
END=E('b6')+1.6
T=dict(grow0=S('b2')+.4,grow1=E('b2')-.2,plus=S('b3'),freeze=S('ruko'),laser=S('m1'),tax=S('m2')+.3,slice=S('m3')-.1,fee=S('m5'),real=S('m6'),shatter=S('m7'),slam=S('m8'),cal=S('m9'),ltcg=S('m10')+.5,shield=S('m11'),open=S('m13')+.4,zero=S('m14'),plinth=S('b4')+.2,tip=S('b6')+.3)
src=open('/home/claude/momentix-reels/engine/audio_lib.py').read()
src=src.split("def env(",1)[1]; src="def env("+src.split("def finish")[0]
src="\n".join(l for l in src.split("\n") if not l.startswith("gl=lambda"))
n=int(END*SR)+SR; mix=np.zeros((n,2)); rng=np.random.default_rng(11)
exec(src)
def sm(x,k): return np.convolve(x,np.ones(k)/k,'same')
def clink(f=None):
    f=f or rng.uniform(2600,4200); N=int(.35*SR); t=np.arange(N)/SR
    x=sum(a*np.sin(2*np.pi*f*m*t)*np.exp(-t/d) for m,a,d in [(1,1,.09),(1.47,.6,.06),(2.31,.35,.04)])
    return (x+rng.standard_normal(N)*np.exp(-t/.004)*.6)*.32
def hum(d):
    N=int(d*SR); t=np.arange(N)/SR; x=np.sign(np.sin(2*np.pi*110*t))*.3+np.sin(2*np.pi*220*t)*.3
    x=sm(x,8)*(0.5+0.5*np.sin(2*np.pi*13*t)); return x*np.minimum(1,t/.15)*np.minimum(1,(d-t)/.1)*.18
def zap():
    N=int(.35*SR); t=np.arange(N)/SR; f=2400*np.exp(-t*9)+200
    return (np.sin(2*np.pi*np.cumsum(f)/SR)+rng.standard_normal(N)*.3)*np.exp(-t/.09)*.45
def glass():
    N=int(.9*SR); t=np.arange(N)/SR; x=np.zeros(N)
    for _ in range(26):
        st=int(rng.uniform(0,.35)*SR); f=rng.uniform(3000,8000); L=N-st; tt=np.arange(L)/SR
        x[st:]+=np.sin(2*np.pi*f*tt)*np.exp(-tt/rng.uniform(.03,.12))*rng.uniform(.1,.3)
    x+=rng.standard_normal(N)*np.exp(-t/.05)*.5; return x*.45
def roll(d):
    N=int(d*SR); t=np.arange(N)/SR; x=sm(rng.standard_normal(N),30); x/=np.abs(x).max()
    return x*(0.6+0.4*np.sin(2*np.pi*9*t))*.22*np.minimum(1,t/.1)*np.minimum(1,(d-t)/.15)
def creak():
    N=int(.9*SR); t=np.arange(N)/SR; f=90+30*np.sin(2*np.pi*3*t)
    return np.sign(np.sin(2*np.pi*np.cumsum(f)/SR))*sm(rng.standard_normal(N),50)*0+np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t/.5)*.25
def drone():
    N=int(END*SR); t=np.arange(N)/SR
    x=np.sin(2*np.pi*55*t)*.5+np.sin(2*np.pi*82.5*t+1)*.3+sm(rng.standard_normal(N),400)*3
    return x*.05*np.minimum(1,t/1.5)*np.minimum(1,(END-t)/1.0)
add(0,drone(),1.0)
# hook
add(0.0,boom(.7)); add(0.05,whoosh(.8,False,.3))
k=0.25
while k<S('b1'): add(k,blip(900),.35,-.2); k+=0.85
# grow: coins land
for i in range(12):
    td=T['grow0']+(T['grow1']-T['grow0'])*i/12+0.32; add(td,clink(),.9,rng.uniform(-.3,.3))
add(T['plus'],ting(),.7); add(T['plus'],pop(1200),.6)
# freeze
add(T['freeze'],glitch(.3,.35)); add(T['freeze']+.05,whoosh(.5,False,.25))
# vault slides in, laser hum + zap
add(T['laser']-.2,whoosh(.7,True,.3),1,.5); add(T['laser']+.65,thud(),1.0,.4)
add(T['laser'],hum(T['slice']+.6-T['laser']),1.0)
add(T['slice'],zap(),1.0); add(T['slice']+.05,slash(),.7)
for j in range(3):
    add(T['slice']+j*.09,whoosh(.5,True,.18),1,.3); add(T['slice']+j*.09+.75,clink(1800),1.0,.5)
add(T['slice']+.6,stampfx(),.8)
# fee
add(T['fee']+.25,tick(),.9,-.4); add(T['fee']+.25,whoosh(.4,True,.15),1,-.5); add(T['fee']+.2,pop(700),.5)
# real profit counter ticks
k=T['real']+.4
while k<T['real']+1.6: add(k,tick(),.45); k+=.07
add(T['shatter']+.35,glass(),1.0); add(T['slam'],boom(.9)); add(T['slam'],thud(),.8)
# calendar flips
for i in range(12):
    tt=T['cal']+.15+1.1*((i/12)**0.5); add(tt,tick(),.6,.1); add(tt,whoosh(.12,True,.06),1,.1)
add(T['ltcg']+.4,slash(),.7); add(T['ltcg']+.6,pop(1100),.6)
add(T['shield']-.8,riser(.9,.2)); add(T['shield'],ting(),.6); add(T['shield']+.15,ting(),.35)
add(T['open'],thud(),.9,.4); add(T['open']+.05,creak(),1.0,.4); add(T['zero']-.05,ting(),.8); add(T['zero']-.05,pop(1300),.6)
# plinth
add(T['plinth'],thud(),.7,-.3); add(T['plinth']+.05,whoosh(.9,False,.25),1,-.3)
add(T['plinth']+.6,roll(1.6),1.0,-.2)
add(S('b5')+.5,pop(1000),.5); add(S('b6')-.1,stampfx(),.9)
for j,dt in enumerate([0,.12,.2,.26,.3]): add(T['tip']+.55+dt,clink(2200+j*150),.7*(1-j*.15),-.2)
np.save('sfx.npy',mix[:int(END*SR)])
# voice
raw=subprocess.run(['ffmpeg','-v','error','-i','../vo/vo.wav','-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout
v=np.frombuffer(raw,dtype=np.float32)[:int(END*SR)]
L=int(END*SR); out=mix[:L].copy()*0.14
out[:len(v),0]+=v*1.0; out[:len(v),1]+=v*1.0
np.clip(out,-1,1,out)
from audio_common import write_wav
write_wav('premix.wav',out,SR)
print('END',round(END,2))
