"""devi1 (hook, female) @0.8 s + amrut2 (narration) @6.4 s -> vo/vo48.wav with phone-speaker chain."""
import subprocess, numpy as np, soundfile as sf, os
D = os.path.dirname(os.path.abspath(__file__)); SR = 48000; END = 28.6
CH = 'highpass=f=80,equalizer=f=250:t=q:w=1:g=-2.5,equalizer=f=3000:t=q:w=1.2:g=4,highshelf=f=7000:g=2,acompressor=threshold=-24dB:ratio=4:attack=4:release=70:makeup=3'
def load(f):
    subprocess.run(['ffmpeg','-v','error','-y','-i',f'{D}/vo/{f}.mp3','-ac','1','-ar',str(SR),'-af',CH,f'{D}/vo/{f}_c.wav'],check=True)
    return sf.read(f'{D}/vo/{f}_c.wav')[0]
y = np.zeros(int(END*SR)); 
for f, t, g in [('devi1', 0.8, 1.0), ('amrut2', 6.4, 1.0)]:
    x = load(f) * g; i = int(t*SR); y[i:i+len(x)] += x[:len(y)-i]
sf.write(f'{D}/vo/vo48.wav', y.astype(np.float32), SR); print('ok', END)
