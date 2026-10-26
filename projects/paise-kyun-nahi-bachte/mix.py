import json,subprocess,numpy as np,sys
SR=48000
tl=json.load(open('timeline.json')); END=tl['end']; C=tl['cuts']; W=tl['words']
src=open('/home/claude/out/momentix-reels/scripts/audio_lib.py').read()
src=src.split("def env(",1)[1]; src="def env("+src.split("def finish")[0]
src="\n".join(l for l in src.split("\n") if not l.startswith("gl=lambda"))
n=int(END*SR)+SR; mix=np.zeros((n,2)); rng=np.random.default_rng(11)
exec(src)
def load(f,ch=2): return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f,'-ac',str(ch),'-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout,dtype=np.float32).reshape(-1,ch)
wt=lambda p: next(w['t'] for w in W if w['w'].lower().startswith(p))
# opening tap on phone
add(0.15,tap(),.6); add(0.25,pop(1400),.35)
for c in C[1:]: add(c-.18,whoosh(.45,True,.32))
add(wt('mithai?'),pop(620),.6)
for t in (13.9,14.55,15.25,15.95): add(t,thud(),.75); add(t+.02,pop(900),.3)
add(wt('sale'),ting(),.35)
J=wt('jhatka'); add(J-.9,riser(.9,.35)); add(J,ting(),.7); add(J,boom(.45)); add(J+.02,glitch(.3,.25))
add(wt('pheeka'),failtone(),.25)
AD=wt('auto-debit'); add(AD,click(),.8); add(AD+.08,ting(),.45)
add(wt('card')-.05,whoosh(.4,False,.45))
t=wt('khareedne')
while t<C[8]-.2: add(t,tick(),.55); t+=.5
add(C[8]-1.0,riser(1.0,.3)); add(C[8]+.05,ting(),.6)
for i in range(7): add(C[8]+.25+i*.11,pop(1100+i*120),.35)
add(wt('ped'),ting(),.5)
sfx=mix.astype(np.float32)
mus=load('music.wav'); m0=int(1.2*SR); M=np.zeros((n,2),np.float32); seg=mus[m0:m0+n]; M[:len(seg)]=seg
tt=np.arange(n)/SR; M*=(np.minimum(1,tt/.4)*np.clip((END-tt)/1.8,0,1))[:,None]
V=np.zeros((n,2),np.float32)
B=load('bunty_1.mp3'); Mo=load('momo_1.mp3')
def place(srcarr,a,b,at):
    x=srcarr[int(max(0,a-.04)*SR):int(b*SR)]; i=int((at-.04)*SR); V[i:i+len(x)]+=x[:n-i]
place(B,0,5.40,0.30); place(Mo,0,3.62,5.95); place(B,5.75,8.751,9.85); place(Mo,3.70,28.369,13.20)
sys.path.insert(0,'/home/claude/out/momentix-reels/scripts'); import audio_common as Cm
lu=lambda x: Cm.lufs_integrated(x,SR)
V*=10**((-16-lu(V))/20); M*=10**((-22-lu(M))/20)
e=np.abs(V).mean(1); w=int(.05*SR); env=np.convolve(e,np.ones(w)/w,'same'); act=(env>10**(-38/20)).astype(float); k=int(.25*SR); act=np.convolve(act,np.ones(k)/k,'same')
M*=(10**(-6/20)*act+(1-act))[:,None]
Sx=sfx*10**((-23-lu(sfx))/20)
out=V+M+Sx; out*=10**((-14-lu(out))/20)
Cm.write_wav('mix.wav',out.astype(np.float32),SR)
subprocess.run(['ffmpeg','-v','error','-y','-i','mix.wav','-af','loudnorm=I=-14:TP=-1.5:LRA=11','-ar','48000','mix_norm.wav'],check=True)
print('ok')
