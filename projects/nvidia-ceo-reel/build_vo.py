"""Cut Momo (momo_2) and Papa (papa_2) takes into lines, interleave as dialogue -> vo/vo48.wav,
write timeline.js (TL line spans, CUE word times, ENV mouth envelopes per speaker)."""
import json, os, subprocess
import numpy as np, soundfile as sf
D = os.path.dirname(os.path.abspath(__file__)); SR = 48000; FPS = 30
CH = ('highpass=f=80,equalizer=f=250:t=q:w=1:g=-2.5,equalizer=f=3000:t=q:w=1.2:g=4,highshelf=f=7000:g=2,'
      'acompressor=threshold=-24dB:ratio=4:attack=4:release=70:makeup=3')
TAKE = {'M': 'momo_2', 'P': 'papa_2'}
# line -> (speaker, start word time in take, start of next line in take or None = end)
LINES = [('M1', 'M', 0.0, 4.72), ('P1', 'P', 0.0, 1.08), ('M2', 'M', 4.72, 10.1), ('P2', 'P', 1.08, 3.94),
         ('M3', 'M', 10.1, 20.45), ('P3', 'P', 3.94, 7.08), ('M4', 'M', 20.45, 24.87), ('P4', 'P', 7.08, None),
         ('M5', 'M', 24.87, None)]
GAP = {'M1': .25, 'P1': .2, 'M2': .3, 'P2': .25, 'M3': .3, 'P3': .25, 'M4': .3, 'P4': .3, 'M5': 1.4}
# cue -> (line, time in take)
CUES = {'crash': ('M1', 3.3), 'affair': ('M2', 7.24), 'down': ('M2', 9.16), 'fayda': ('P2', 3.58),
        'biz': ('M3', 15.02), 'profit': ('M3', 16.96), 'senti': ('M3', 18.7), 'mauka': ('P3', 6.62),
        'risk': ('M4', 21.71), 'samjho': ('M4', 22.71), 'faisla': ('M4', 24.03), 'kaise': ('P4', 9.82), 'cta': ('M5', 31.27)}
CAP = {'M1': [0.0, 1.58, 2.52], 'P1': [0.0], 'M2': [4.72, 7.0, 8.18], 'P2': [1.08, 2.3],
       'M3': [10.1, 10.8, 12.2, 13.16, 15.02, 16.66, 17.3, 18.7], 'P3': [3.94, 5.98], 'M4': [20.45, 21.51, 22.59, 23.79],
       'P4': [7.08, 9.26], 'M5': [24.87, 25.87, 27.61, 29.63, 31.27, 32.17]}

def load(take):
    out = f'{D}/vo/{take}_c.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{D}/vo/{take}.mp3', '-ac', '1', '-ar', str(SR), '-af', CH, out], check=True)
    return sf.read(out)[0]
X = {s: load(t) for s, t in TAKE.items()}; WD = {s: json.load(open(f'{D}/vo/words_{t}.json')) for s, t in TAKE.items()}

def cut_at(spk, t):  # midpoint of the silence before the word that starts at t (0 stays 0)
    if t <= 0: return 0.0
    prev = max([w[1] for w in WD[spk] if w[1] <= t + .01] or [t - .1]); return (prev + t) / 2

pieces, t, TL, OFF, spans = [np.zeros(int(.35 * SR))], .35, {}, {}, {}
for k, spk, a, b in LINES:
    x = X[spk]; ca = cut_at(spk, a); cb = len(x) / SR if b is None else cut_at(spk, b)
    seg = x[int(ca * SR):int(cb * SR)].copy()
    # trim trailing silence (keep 80 ms)
    env = np.abs(seg); thr = 0.01; nz = np.where(env > thr)[0]
    if len(nz): seg = seg[:min(len(seg), nz[-1] + int(.08 * SR))]
    fade = int(.01 * SR); seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
    TL[k] = [round(t, 3), round(t + len(seg) / SR, 3)]; OFF[k] = t - ca; spans[k] = spk
    pieces += [seg, np.zeros(int(GAP[k] * SR))]; t += len(seg) / SR + GAP[k]
y = np.concatenate(pieces); END = round(len(y) / SR + .3, 3)
sf.write(f'{D}/vo/vo48.wav', y.astype(np.float32), SR)
CUE = {c: round(tt + OFF[ln], 3) for c, (ln, tt) in CUES.items()}
for ln, ts in CAP.items():
    for i, tt in enumerate(ts): CUE[f'cap_{ln}_{i}'] = round(max(TL[ln][0], tt + OFF[ln]) - .05, 3)
# mouth envelopes per speaker at 30 fps
N = int(END * FPS) + 1; ENV = {'M': [0] * N, 'P': [0] * N}
for k, (s0, s1) in TL.items():
    for f in range(int(s0 * FPS), min(N, int(s1 * FPS) + 1)):
        i = int(f / FPS * SR); w = y[i:i + SR // FPS]
        if len(w): ENV[spans[k]][f] = round(float(min(1, np.sqrt(np.mean(w ** 2)) * 9)), 2)
open(f'{D}/timeline.js', 'w').write(f'window.TL={json.dumps(TL)};\nwindow.CUE={json.dumps(CUE)};\nwindow.END={END};\nwindow.ENV={json.dumps(ENV)};\n')
json.dump({'TL': TL, 'CUE': CUE, 'END': END}, open(f'{D}/timeline.json', 'w'), indent=1)
print('END', END); print(TL)
