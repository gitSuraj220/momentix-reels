"""Take 1 -> vo/vo48.wav with dramatic pauses inserted + voice chain; writes vo/times.json (word times on the new timeline)."""
import json, os, subprocess
import numpy as np, soundfile as sf
D = os.path.dirname(os.path.abspath(__file__)); SR = 48000
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{D}/vo/vo1.mp3', '-ac', '1', '-ar', str(SR), '-af',
                'highpass=f=80,equalizer=f=250:t=q:w=1:g=-2.5,equalizer=f=3000:t=q:w=1.2:g=4,highshelf=f=7000:g=2,'
                'acompressor=threshold=-24dB:ratio=4:attack=4:release=70:makeup=3', f'{D}/vo/vo_chain.wav'], check=True)
x, _ = sf.read(f'{D}/vo/vo_chain.wav')
LEAD = 0.6                       # silence before first word (hook card lands first)
# (cut point in original seconds = middle of a natural silence, extra pause seconds)
GAPS = [(12.35, 0.5), (16.80, 1.3), (20.05, 0.9), (22.42, 0.7), (23.71, 2.0),
        (51.59, 1.0), (55.03, 0.7), (63.99, 1.3), (71.68, 0.8)]
parts, prev = [np.zeros(int(LEAD * SR))], 0
for c, g in GAPS:
    i = int(c * SR); parts += [x[prev:i], np.zeros(int(g * SR))]; prev = i
parts.append(x[prev:]); parts.append(np.zeros(int(2.5 * SR)))   # tail for end card
y = np.concatenate(parts); sf.write(f'{D}/vo/vo48.wav', y.astype(np.float32), SR)
def remap(t):
    s = LEAD
    for c, g in GAPS:
        if t > c: s += g
    return round(t + s, 3)
W = json.load(open(f'{D}/vo/words1.json'))
json.dump([[remap(a), remap(b), w] for a, b, w in W], open(f'{D}/vo/times.json', 'w'))
print('vo48 len', round(len(y) / SR, 2), 'gaps at', [remap(c) for c, _ in GAPS])
