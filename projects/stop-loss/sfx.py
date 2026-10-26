import numpy as np,sys
SR=48000;END=14.5
src=open('/home/claude/out/momentix-reels/scripts/audio_lib.py').read()
src=src.split("def env(",1)[1]; src="def env("+src.split("def finish")[0]
src="\n".join(l for l in src.split("\n") if not l.startswith("gl=lambda"))
n=int(END*SR)+SR//2; mix=np.zeros((n,2)); rng=np.random.default_rng(9)
exec(src)
def smooth(x,k):return np.convolve(x,np.ones(k)/k,'same')
def noise(N):return rng.standard_normal(N)
# ocean ambience 0..9.6 : lowpassed noise with slow swells
N=int(9.7*SR);t=np.arange(N)/SR
oc=smooth(noise(N),int(SR/400));oc/=np.abs(oc).max()
sw=0.55+0.45*np.sin(2*np.pi*t/3.2)**2
add(0,oc*sw*0.35*np.minimum(1,t/.6),1.0,-.15)
hiss=smooth(noise(N),6);hiss/=np.abs(hiss).max();add(0,hiss*0.05*sw,1.0,.15)
# rain 7.2..9.6
N2=int(2.5*SR);t2=np.arange(N2)/SR;rain=noise(N2)*0.10*np.minimum(1,t2/.6);add(7.2,rain*(0.6+0.4*rng.random(N2)),1.0,0)
# footsteps & sign drags
MOVES=[(2.55,3.55),(5.35,6.35),(7.85,8.65)]
def step():
    N=int(.12*SR);tt=np.arange(N)/SR;return (smooth(noise(N),20)*np.exp(-tt/.03))*0.9
def drag(d):
    N=int(d*SR);tt=np.arange(N)/SR;x=smooth(noise(N),40);x/=np.abs(x).max();return x*0.35*np.minimum(1,tt/.08)*np.minimum(1,(d-tt)/.1)
def lossTone():
    N=int(.55*SR);tt=np.arange(N)/SR;f=620*np.exp(-tt*2.2)+180
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt/.25)*0.5
for a,b in MOVES:
    add(a,whoosh(.3,True,.2));add(a+.05,drag(b-a-.05),1.0,.1)
    k=a+.08
    while k<b: add(k,step(),.8,.2); k+=.2
    add(b,thud(),.9); add(b-.12,lossTone(),1.0)
# tension heartbeat 4.6..9.4 accelerating
k=4.6;ib=0.85
while k<9.3:
    add(k,boom(.18));add(k+.16,boom(.12));k+=ib;ib=max(.38,ib*0.93)
# wave: riser + roar then crash
add(8.1,riser(1.4,.45))
N3=int(1.6*SR);t3=np.arange(N3)/SR;roar=smooth(noise(N3),int(SR/250));roar/=np.abs(roar).max();add(8.0,roar*np.minimum(1,t3/1.3)**2*0.7,1.0,-.2)
add(9.5,boom(1.0));add(9.52,thud(),1.0)
N4=int(1.2*SR);t4=np.arange(N4)/SR;sp=smooth(noise(N4),3);add(9.5,sp*0.35*np.exp(-t4/.35),1.0,.1)
# underwater: muffled rumble + bubbles
N5=int((END-9.6)*SR);t5=np.arange(N5)/SR;uw=smooth(noise(N5),int(SR/120));uw/=np.abs(uw).max();add(9.6,uw*0.45*np.minimum(1,t5/.3),1.0,0)
def bubble(f):
    N=int(.09*SR);tt=np.arange(N)/SR;fr=f*(1+tt*14);return np.sin(2*np.pi*np.cumsum(fr)/SR)*np.exp(-tt/.03)*0.25
for i in range(30):add(9.7+rng.random()*4.5,bubble(400+rng.random()*700),1.0,rng.uniform(-.7,.7))
add(9.65,lossTone(),1.2)
# typewriter
full=["MOVING YOUR STOP LOSS","ISN'T HOPE.","IT'S DENIAL."];cps=22;c=0
for li,line in enumerate(full):
    for ch in line:
        tt=11.0+c/cps
        if ch!=' ':add(tt,blip(1500+rng.random()*300),.18)
        c+=1
    c+=3
add(11.0+ (len(full[0])+len(full[1])+3*2+5)/cps,thud(),.6)
add(13.0,ting(),.35)
out=mix.astype(np.float32)
sys.path.insert(0,'/home/claude/out/momentix-reels/scripts');import audio_common as Cm
out*=10**((-16-Cm.lufs_integrated(out,SR))/20);pk=np.abs(out).max()
if pk>.92:out*=.92/pk
Cm.write_wav('sfx.wav',out,SR);print('ok',round(Cm.lufs_integrated(out,SR),1))
