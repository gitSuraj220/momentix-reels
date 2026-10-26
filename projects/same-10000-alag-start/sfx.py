import json,subprocess,numpy as np,sys
SR=48000;END=15.0
cu=json.load(open('cues.json'));T0,T1,T35=cu['T0'],cu['T1'],cu['T35']
src=open('/home/claude/out/momentix-reels/scripts/audio_lib.py').read()
src=src.split("def env(",1)[1]; src="def env("+src.split("def finish")[0]
src="\n".join(l for l in src.split("\n") if not l.startswith("gl=lambda"))
n=int(END*SR)+SR//2; mix=np.zeros((n,2)); rng=np.random.default_rng(5)
exec(src)
def lp(x,a):  # one-pole lowpass
    y=np.zeros_like(x);acc=0.0
    for i in range(len(x)): acc+=a*(x[i]-acc); y[i]=acc
    return y
def clink(f=2600,g=.4):
    N=int(.5*SR);t=np.arange(N)/SR
    return sum(a*np.sin(2*np.pi*f*m*t)*np.exp(-t/d) for m,a,d in [(1,1,.12),(1.48,.6,.09),(2.3,.35,.06),(3.1,.2,.04)])*np.minimum(1,t/.001)*g
# intro
add(0.0,whoosh(.7,True,.3)); add(0.25,boom(.35))
# rolling rumble per panel (pan up=slightly left, bottom=slightly right)
def rumble(t0,t1,pan,vfn):
    N=int((t1-t0)*SR);t=np.arange(N)/SR
    noise=rng.standard_normal(N)
    # cheap lowpass via cumulative moving average
    k=int(SR/180);x=np.convolve(noise,np.ones(k)/k,'same');x/=np.abs(x).max()+1e-9
    size=vfn(t0+t)
    bump=1+0.35*np.sin(2*np.pi*(1.2+0.8*size)*t)
    amp=(0.12+0.5*size)*bump*np.minimum(1,t/.25)*np.minimum(1,(t1-t0-t)/.15)
    add(t0,x*amp,1.0,pan)
def ageAt(t):
    u=min(1,max(0,(t-T0)/(T1-T0)));return 25+35*(0.55*u+0.45*u*u*(3-2*u))
def fv(m): i=.01; return 0 if m<=0 else 10000*((1+i)**m-1)/i
VM=fv(420)
sz=lambda off: (lambda tt: np.sqrt(np.array([fv(max(0,(ageAt(x)-off)*12)) for x in tt[::480]]).repeat(480)[:len(tt)]/VM))
rumble(T0,T1+.15,-.25,sz(25)); rumble(T35,T1+.15,.25,sz(35))
add(T0,thud(),.7); add(T0+.02,whoosh(.35,True,.25))
# yearly ticks + coin clink every 5 years
for k,t in enumerate(cu['years']):
    a=26+k
    add(t,tick(),.45)
    if a%5==0: add(t,clink(2400+a*12,.35),1.0,-.2)
# Bunty phone taps before 35
for t in (1.3,2.1,2.9,3.6): add(t,tap(),.45,.3); add(t+.03,blip(2100),.25,.3)
# Bunty starts at 35
add(T35-.15,whoosh(.4,True,.35)); add(T35,ting(),.6,.25); add(T35+.02,pop(900),.5,.25)
# finish at 60
add(T1-.9,riser(.9,.3)); add(T1,boom(.9)); add(T1,thud(),.8)
for i in range(14): add(T1+.05+i*.07,clink(1900+rng.random()*1800,.28),1.0,rng.uniform(-.6,.6))
# headline
add(T1+.5,whoosh(.45,False,.35)); add(T1+.62,pop(700),.6); add(T1+.85,ting(),.45)
out=mix.astype(np.float32)
sys.path.insert(0,'/home/claude/out/momentix-reels/scripts'); import audio_common as Cm
out*=10**((-16-Cm.lufs_integrated(out,SR))/20)
pk=np.abs(out).max()
if pk>0.9: out*=0.9/pk
Cm.write_wav('sfx.wav',out,SR)
print('ok',Cm.lufs_integrated(out,SR))
