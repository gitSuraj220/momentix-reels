"""Cut Bunty (Amrut, take 2) + Momo (Nishant M, take 1) lines, trim silence, place on the timeline -> vo/vo48.wav + timeline.json."""
import json, os, subprocess, numpy as np, soundfile as sf
D = os.path.dirname(os.path.abspath(__file__)); SR = 48000
def load(f):
    subprocess.run(['ffmpeg','-v','error','-y','-i',f'{D}/vo/{f}.mp3','-ar',str(SR),'-ac','1',f'/tmp/claude-0/{f}.wav'],check=True)
    return sf.read(f'/tmp/claude-0/{f}.wav')[0]
A = {'bunty': load('bunty'), 'momo': load('momo')}
# (speaker, rough start, rough end) from per-segment Whisper pass
L = [('B1','bunty',0.00,4.24),('M1','momo',0.00,12.25),('B2','bunty',4.24,6.02),('M2','momo',12.25,19.10),('B3','bunty',6.02,10.30),
     ('M3','momo',19.10,21.06),('B4','bunty',10.30,13.45),('M4','momo',21.06,22.20),('B5','bunty',13.45,20.29),('M5','momo',22.20,24.53),('B6','bunty',20.29,23.80)]
def trim(x):
    e = np.convolve(np.abs(x), np.ones(480)/480, 'same'); th = e.max()*0.04; idx = np.where(e > th)[0]
    a, b = max(0, idx[0]-int(.03*SR)), min(len(x), idx[-1]+int(.08*SR)); return x[a:b]
GAP = {'M1':.25,'B2':.9,'M2':.3,'B3':.3,'M3':.3,'B4':.3,'M4':.25,'B5':.25,'M5':.3,'B6':.3}  # B2 after the 1-SAAL-BAAD card
t = 0.30; out = np.zeros(int(70*SR)); TL = {}
for k, spk, s, e in L:
    t += GAP.get(k, 0)
    x = trim(A[spk][int(s*SR):int(min(e, len(A[spk])/SR)*SR)])
    i = int(t*SR); out[i:i+len(x)] += x; TL[k] = [round(t,3), round(t+len(x)/SR,3)]; t += len(x)/SR
END = round(t + 0.9, 2); TL['END'] = END
sf.write(f'/tmp/claude-0/vo_raw.wav', out[:int(END*SR)], SR)
CH = 'highpass=f=80,equalizer=f=250:t=q:w=1:g=-2.5,equalizer=f=3000:t=q:w=1.2:g=4,highshelf=f=7000:g=2,acompressor=threshold=-24dB:ratio=4:attack=4:release=70:makeup=3'
subprocess.run(['ffmpeg','-v','error','-y','-i','/tmp/claude-0/vo_raw.wav','-af',CH,f'{D}/vo/vo48.wav'],check=True)
json.dump(TL, open(f'{D}/timeline.json','w'), indent=1); print(json.dumps(TL))
