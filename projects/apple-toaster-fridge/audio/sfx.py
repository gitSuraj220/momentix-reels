import numpy as np, json, subprocess, sys
sys.path.insert(0,'/home/claude/momentix-reels/engine')
from audio_common import write_wav
SR=48000
CU=json.load(open('../vo/cues.json')); S=lambda i:[c for c in CU if c['id']==i][0]['s']; E=lambda i:[c for c in CU if c['id']==i][0]['e']
END=E('m15')+0.9
src=open('/home/claude/momentix-reels/engine/audio_lib.py').read()
src=src.split("def env(",1)[1]; src="def env("+src.split("def finish")[0]
src="\n".join(l for l in src.split("\n") if not l.startswith("gl=lambda"))
n=int(END*SR)+SR; mix=np.zeros((n,2)); rng=np.random.default_rng(8)
exec(src)
def sm(x,k): return np.convolve(x,np.ones(k)/k,'same')
def rewind(d=1.0):
    N=int(d*SR); t=np.arange(N)/SR; f=2200*np.exp(-t*2.5)+300
    x=np.sin(2*np.pi*np.cumsum(f)/SR)*0.3+sm(rng.standard_normal(N),4)*0.25*(0.5+0.5*np.sin(2*np.pi*35*t))
    return x*np.minimum(1,t/.03)*np.minimum(1,(d-t)/.1)*0.6
def boing():
    N=int(.6*SR); t=np.arange(N)/SR; f=180+120*np.sin(2*np.pi*9*t)*np.exp(-t*4)+260*np.exp(-t*6)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t/.25)*.5
def ice():
    N=int(.9*SR); x=np.zeros(N)
    for _ in range(40):
        st=int(rng.uniform(0,.6)*SR); L=N-st; tt=np.arange(L)/SR; f=rng.uniform(4000,9000)
        x[st:]+=np.sin(2*np.pi*f*tt)*np.exp(-tt/rng.uniform(.01,.05))*rng.uniform(.05,.2)
    return x*.6
def sad():
    out=np.zeros(int(2.0*SR))
    for i,(f,d) in enumerate([(392,.32),(370,.32),(349,.32),(330,.7)]):
        st=int(sum([.34]*i)*SR); N=int(d*SR); t=np.arange(N)/SR
        v=np.sign(np.sin(2*np.pi*f*t*(1+0.01*np.sin(2*np.pi*6*t))))*0.2+np.sin(2*np.pi*f*t)*0.3
        out[st:st+N]+=sm(v,30)*np.minimum(1,t/.02)*np.minimum(1,(d-t)/.05)
    return out*.5
def chaching():
    a=ting(); b=np.concatenate([np.zeros(int(.09*SR)),ting()]); m=max(len(a),len(b)); x=np.zeros(m); x[:len(a)]+=a; x[:len(b)]+=b*.8; return x
def rimshot():
    N=int(.9*SR); x=np.zeros(N); t=np.arange(N)/SR
    for st in (0,.16):
        i=int(st*SR); tt=t[:N-i]; x[i:]+=np.sin(2*np.pi*140*tt)*np.exp(-tt/.08)*.5
    i=int(.34*SR); tt=t[:N-i]; x[i:]+=rng.standard_normal(N-i)*np.exp(-tt/.25)*.35
    return x
def hum(d):
    N=int(d*SR); t=np.arange(N)/SR; x=np.sin(2*np.pi*65*t)*.5+np.sin(2*np.pi*97.5*t+1)*.3+sm(rng.standard_normal(N),300)*2
    return x*.05*np.minimum(1,t/1)*np.minimum(1,(d-t)/.8)
add(0,hum(END),1.0)
W2=S('m1')-0.1; W3=S('m3')-0.1; W4=S('m8')-0.15; W5=S('m10')-0.1; W6=S('b2')-0.15
add(0.0,whoosh(.6,True,.3)); add(0.65,tap(),.9); add(0.95,tap(),.9); add(0.7,ting(),.4)
add(W2,rewind(1.1),1.0); add(W2+0.25,stampfx(),.9)
add(W3-0.2,whoosh(.5,True,.3)); add(S('m3')+0.4,pop(900),.6)
add(W3+1.2,ting(),.7); add(W3+1.25,boing(),.9); add(W3+1.3,ice(),1.0)
add(S('m5')+0.9,pop(1100),.6)
add(W4-0.2,whoosh(.5,False,.28)); add(S('m9')+1.1,sad(),.8)
add(S('m10')-0.05,riser(1.4,.22)); add(S('m11')+1.55,boom(.9)); add(S('m11')+1.55,whoosh(.4,True,.3))
add(S('m12'),pop(1000),.5); add(S('m13'),boom(1.0)); add(S('m13')+0.05,chaching(),.8)
add(W6,whoosh(.4,True,.25)); add(S('b2')+0.6,boing(),.5); add(S('m15')+0.1,rimshot(),.9)
sfx=mix[:int(END*SR)]
raw=subprocess.run(['ffmpeg','-v','error','-i','../vo/vo.wav','-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout
v=np.frombuffer(raw,dtype=np.float32)[:len(sfx)]
out=sfx*0.16; out[:len(v),0]+=v; out[:len(v),1]+=v
np.clip(out,-1,1,out); write_wav('premix.wav',out,SR); write_wav('sfx_only.wav',sfx*0.16,SR); print(round(END,2))
