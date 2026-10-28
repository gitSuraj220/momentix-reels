import numpy as np, json, subprocess, sys
sys.path.insert(0,'/home/claude/momentix-reels/engine')
from audio_common import write_wav
SR=48000
CU=json.load(open('../vo/cues.json')); S=lambda i:[c for c in CU if c['id']==i][0]['s']; E=lambda i:[c for c in CU if c['id']==i][0]['e']
END=E('b1')+1.1
src=open('/home/claude/momentix-reels/engine/audio_lib.py').read()
src=src.split("def env(",1)[1]; src="def env("+src.split("def finish")[0]
src="\n".join(l for l in src.split("\n") if not l.startswith("gl=lambda"))
n=int(END*SR)+SR; mix=np.zeros((n,2)); rng=np.random.default_rng(5)
exec(src)
def sm(x,k): return np.convolve(x,np.ones(k)/k,'same')
def sizzle(d,g=1):
    N=int(d*SR); t=np.arange(N)/SR; x=rng.standard_normal(N); x=x-sm(x,6)
    crack=(rng.random(N)<0.0009)*rng.standard_normal(N)*4; x+=np.convolve(crack,np.exp(-np.arange(200)/30),'same')
    return x*0.06*g*np.minimum(1,t/.3)*np.minimum(1,(d-t)/.3)
def drone(d,f=55):
    N=int(d*SR); t=np.arange(N)/SR
    x=np.sin(2*np.pi*f*t)+.5*np.sin(2*np.pi*f*1.5*t+1)+.25*np.sin(2*np.pi*f*2.01*t)
    return x*.12*np.minimum(1,t/1.2)*np.minimum(1,(d-t)/.8)
def drain(d=1.6):
    N=int(d*SR); t=np.arange(N)/SR; f=600*np.exp(-t*1.4)+90
    return np.sin(2*np.pi*np.cumsum(f)/SR)*.25*np.minimum(1,t/.05)*np.exp(-t/1.2)
def tension(d):
    N=int(d*SR); t=np.arange(N)/SR; x=sm(rng.standard_normal(N),80); x/=np.abs(x).max()
    return (x*.25+np.sin(2*np.pi*70*t)*.15)*(0.6+0.4*np.sin(2*np.pi*1.5*t))*np.minimum(1,t/.3)*np.minimum(1,(d-t)/.3)
W1=S('p1'); 
# beds
add(0,sizzle(S('p2')),0.9); add(S('w1')-0.15,sizzle(S('s1')-S('w1')),1.2); add(S('b1')-0.2,sizzle(END-S('b1')+0.2),0.8)
add(0,drone(S('s1')+7,49),1.0)
# hook
add(0.0,boom(.8)); add(0.05,riser(2.4,.18))
add(S('h2')-0.05,whoosh(.35,True,.3)); add(S('h2'),boom(.9)); add(S('h2'),ting(),.6)
# cuts
for c in ['p1','p2','t1','w1','s1','b1']: add(S(c)-0.25,whoosh(.45,True,.28),1,0)
add(S('p1')+0.3,pop(1000),.5)
# calendar ticks + crosses
for i in range(10): add(S('p2')+0.1+1.4*((i/10)**0.6),tick(),.7)
for k in range(4): add(S('p3')+0.15+k*0.32,thud(),.9); add(S('p3')+0.15+k*0.32,slash(),.35)
# power drain + inflation slam
add(S('t2')+0.2,drain(),1.0); add(S('t3')+0.75,riser(.3,.25)); add(S('t3')+0.9,boom(1.0)); add(S('t3')+0.9,stampfx(),.8)
# tags
for k,dt in enumerate([0.25,0.75,1.25,1.9]): add(S('w1')+dt,pop(900+120*k),.7)
# tug of war
add(S('s1')-0.1,tension(S('s4')-S('s1')+0.6),1.0); add(S('s2'),thud(),.6); add(S('s3')-0.05,boom(.8)); add(S('s3')-0.05,failtone(),.4)
# ending
add(S('b1')+0.6,failtone(),.35); add(END-0.6,boom(.5))
sfx=mix[:int(END*SR)]
raw=subprocess.run(['ffmpeg','-v','error','-i','../vo/vo.wav','-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout
v=np.frombuffer(raw,dtype=np.float32)[:len(sfx)]
out=sfx*0.16; out[:len(v),0]+=v; out[:len(v),1]+=v
np.clip(out,-1,1,out); write_wav('premix.wav',out,SR); write_wav('sfx_only.wav',sfx*0.16,SR)
print(round(END,2))
