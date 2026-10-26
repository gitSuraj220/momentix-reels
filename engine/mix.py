import numpy as np, subprocess, json, sys
sys.path.insert(0,__import__('os').path.dirname(__file__))
import audio_common as Cm
SR=48000
tl=json.load(open('timeline.json'))
sfx=np.load('sfx.npy'); mus=np.load('music.npy'); n=len(sfx)
vo=Cm.decode('vo.mp3',SR,stereo=True)
V=np.zeros((n,2),np.float32); i=int(tl['off']*SR); V[i:i+len(vo)]=vo[:n-i]
def lufs(x): return Cm.lufs_integrated(x,SR)
V*=10**((-16-lufs(V))/20)
# music: target -29 LUFS, duck 5 dB while voice active
M=np.stack([mus,mus],1)
M*=10**((-27-lufs(M))/20)
e=np.abs(V).mean(1); w=int(.05*SR); env=np.convolve(e,np.ones(w)/w,'same'); act=(env>10**(-38/20)).astype(float)
k=int(.25*SR); act=np.convolve(act,np.ones(k)/k,'same')
M*=(10**(-5/20)*act+(1-act))[:,None]
S=sfx*10**((-26-lufs(sfx))/20)
mix=V+M+S
mix*=10**((-14-lufs(mix))/20)


print('LUFS',round(lufs(mix),1),'peak dB',round(20*np.log10(np.abs(mix).max()),2),'music LUFS',round(lufs(M),1))
Cm.write_wav('mix.wav',mix.astype(np.float32),SR)

subprocess.run(['ffmpeg','-v','error','-y','-i','mix.wav','-af','loudnorm=I=-14:TP=-1.5:LRA=11','-ar','48000','mix_norm.wav'],check=True)
print('wrote mix_norm.wav')
