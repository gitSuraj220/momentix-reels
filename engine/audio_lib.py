import json, numpy as np, subprocess
SR=48000
tl=json.load(open('timeline.json')); F=tl['frags']; Ln={int(k):v for k,v in tl['lines'].items()}; OFF=tl['off']; END=tl['end']
T=lambda k:Ln[k][0]
n=int(END*SR)+SR; mix=np.zeros((n,2))
rng=np.random.default_rng(7)
def env(N,a=.005,d=.3):
    t=np.arange(N)/SR; return np.minimum(1,t/a)*np.exp(-t/d)
def add(t,x,g=1.0,pan=0.0):
    i=int(t*SR); x=x[:max(0,n-i)]
    l,r=np.cos((pan+1)*np.pi/4),np.sin((pan+1)*np.pi/4)
    mix[i:i+len(x),0]+=x*g*l*1.414; mix[i:i+len(x),1]+=x*g*r*1.414
def ting():
    N=int(1.6*SR); t=np.arange(N)/SR
    x=sum(a*np.sin(2*np.pi*f*t)*np.exp(-t/d) for f,a,d in [(1568,1,.55),(2093,.6,.45),(3136,.3,.3),(4186,.15,.2)])
    x2=np.zeros(N); k=int(.09*SR); t2=t[:N-k]
    x2[k:]=sum(a*np.sin(2*np.pi*f*t2)*np.exp(-t2/d) for f,a,d in [(2093,1,.6),(2637,.5,.45),(4186,.2,.25)])
    return (x+x2)*np.minimum(1,t/.002)*.35
def tap():
    N=int(.08*SR); return rng.standard_normal(N)*env(N,.001,.012)*.5 + np.sin(2*np.pi*180*np.arange(N)/SR)*env(N,.001,.02)*.4
def pop(f=900):
    N=int(.18*SR); t=np.arange(N)/SR; fr=f*np.exp(-t*18)+f*.4
    return np.sin(2*np.pi*np.cumsum(fr)/SR)*env(N,.002,.05)*.5
def whoosh(d=.6,up=True,g=.35):
    N=int(d*SR); x=rng.standard_normal(N); t=np.arange(N)/SR
    # moving bandpass via one-pole smoothing with varying coeff
    fc=np.linspace(400,3500,N) if up else np.linspace(3500,400,N); a=np.exp(-2*np.pi*fc/SR)
    y=np.zeros(N); z=0
    for i in range(N): z=(1-a[i])*x[i]+a[i]*z; y[i]=z
    y=y-np.convolve(y,np.ones(30)/30,'same')
    e=np.sin(np.pi*t/d)**2
    return y/np.abs(y).max()*e*g
def thud():
    N=int(.4*SR); t=np.arange(N)/SR; return np.sin(2*np.pi*(70+60*np.exp(-t*30))*t)*env(N,.002,.12)*.8
def tick():
    N=int(.05*SR); t=np.arange(N)/SR; return np.sin(2*np.pi*2400*t)*env(N,.0005,.01)*.25
def click():
    N=int(.12*SR); t=np.arange(N)/SR; return (np.sin(2*np.pi*1200*t)*env(N,.0005,.015)+np.sin(2*np.pi*600*t)*env(N,.0005,.03))*.35
def rise(d=1.0):
    N=int(d*SR); t=np.arange(N)/SR; f=300+900*(t/d)**2
    return np.sin(2*np.pi*np.cumsum(f)/SR)*(t/d)**2*np.exp(-np.maximum(0,t-d+.05)*80)*.12

def glitch(d=.45,g=.5):
    N=int(d*SR); x=np.zeros(N); i=0
    while i<N:
        L=int(SR*rng.uniform(.01,.05)); f=rng.uniform(200,3000); t=np.arange(min(L,N-i))/SR
        sq=np.sign(np.sin(2*np.pi*f*t))*rng.uniform(.3,1); x[i:i+len(t)]=sq*(rng.random()<.75); i+=L
    x=np.round(x*4)/4
    return x*np.minimum(1,np.arange(N)/(.003*SR))*np.exp(-np.arange(N)/SR/(d*.7))*g
def ringtone(d=.9):
    N=int(d*SR); t=np.arange(N)/SR; on=((t%0.45)<0.3).astype(float)
    return (np.sin(2*np.pi*440*t)+np.sin(2*np.pi*480*t))*on*.12
def failtone():
    out=[]
    for f in (950,1400,1800):
        N=int(.28*SR); t=np.arange(N)/SR; out.append(np.sin(2*np.pi*f*t)*np.minimum(1,t/.01)*np.minimum(1,(N/SR-t)/.02)*.18)
    return np.concatenate(out)
def blip(f=1800):
    N=int(.06*SR); t=np.arange(N)/SR; return np.sin(2*np.pi*f*t)*np.exp(-t/.015)*.15
def static_bed(t0,t1,g=.25):
    N=int((t1-t0)*SR); x=rng.standard_normal(N)
    y=np.zeros(N); z=0; a=.35
    for i in range(N): z=(1-a)*x[i]+a*z; y[i]=z
    t=np.arange(N)/SR; ramp=np.minimum(1,t/1.5)*np.minimum(1,(N/SR-t)/.4)
    crackle=(rng.random(N)<.002)*rng.uniform(-1,1,N)*3
    return (y*.5+crackle)*ramp*(.6+.4*np.sin(2*np.pi*7*t)**2)*g
gl=lambda i:F[i]['s']

# ---- extra hook fx
def boom(g=1.0):
    N=int(1.4*SR); t=np.arange(N)/SR
    sub=np.sin(2*np.pi*(38+70*np.exp(-t*9))*t)*np.exp(-t/.55)
    hit=rng.standard_normal(N)*np.exp(-t/.05)*.6
    return (sub*1.1+hit)*g
def riser(d=1.2,g=.25):
    N=int(d*SR); t=np.arange(N)/SR; x=rng.standard_normal(N)
    y=np.zeros(N); z=0
    for i in range(N): a=np.exp(-2*np.pi*(300+3500*(t[i]/d)**2)/SR); z=(1-a)*x[i]+a*z; y[i]=z
    return y/np.abs(y).max()*(t/d)**2*g
def slash():
    N=int(.16*SR); t=np.arange(N)/SR; x=rng.standard_normal(N)
    y=np.zeros(N); z=0
    for i in range(N): a=np.exp(-2*np.pi*(5000-4000*t[i]/.16)/SR); z=(1-a)*x[i]+a*z; y[i]=z
    return y/np.abs(y).max()*np.sin(np.pi*t/.16)*.35
def stampfx():
    return thud()*1.0

gl=lambda i:F[i]['s']

def finish(music_drop=None):
    """Write sfx.npy + music.npy. music_drop: list of (t0,t1,level) to duck/cut the bed (e.g. silence on a 'network gul' hit)."""
    sfx=mix.copy()
    # ---- music bed: soft pad + pluck arpeggio, 96 bpm
    t=np.arange(n)/SR; bpm=88; beat=60/bpm
    chords=[[57,60,64],[53,57,60],[50,53,57],[52,56,59]]  # Am F Dm E
    mus=np.zeros(n)
    hz=lambda m:440*2**((m-69)/12)
    bar=4*beat
    for b in range(int(END/bar)+2):
        ch=chords[b%4]; s0=int(b*bar*SR); N=int(bar*SR)+SR//2
        tt=np.arange(N)/SR
        pad=sum(np.sin(2*np.pi*hz(m)*tt)+.3*np.sin(2*np.pi*hz(m)*2.003*tt) for m in ch)/3*np.minimum(1,tt/.6)*np.minimum(1,np.maximum(0,(N/SR-tt)/.5))*.18
        seg=mus[s0:s0+N]; seg+=pad[:len(seg)]
        for k in range(8):
            m=ch[k%3]+12+(12 if k in(3,7) else 0); s1=int((b*bar+k*beat/2)*SR); M=int(.5*SR)
            tt2=np.arange(M)/SR; pl=(np.sin(2*np.pi*hz(m)*tt2)+.4*np.sin(2*np.pi*hz(m)*2*tt2))*np.exp(-tt2/.18)*np.minimum(1,tt2/.003)*.22
            seg2=mus[s1:s1+M]; seg2+=pl[:len(seg2)]
    fade=np.minimum(1,t/0.05)*np.minimum(1,np.maximum(0,(END-t)/2.0))
    mus*=fade
    drop=np.ones(n); ramp=int(.3*SR)
    for (t0,t1,lv) in (music_drop or []):
        a0,a1=int(t0*SR),int(t1*SR); drop[a0:a1]=lv; drop[a1:a1+ramp]=np.linspace(lv,1,len(drop[a1:a1+ramp]))
    mus*=drop
    np.save('sfx.npy',sfx.astype(np.float32)); np.save('music.npy',mus.astype(np.float32))
    print('ok', n/SR)
