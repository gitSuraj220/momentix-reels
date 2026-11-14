"""Tighten Devi take: EQ/comp, shorten pauses (max .24 s, section breaks .42 s), speed up 1.12x -> vo/vo48.wav."""
import os, re, subprocess
import numpy as np, soundfile as sf
D = os.path.dirname(os.path.abspath(__file__)); SR = 48000; TAKE = 'devi_2'; SPEED = 1.18
CH = ('highpass=f=80,equalizer=f=250:t=q:w=1:g=-2.5,equalizer=f=3000:t=q:w=1.2:g=4,highshelf=f=7000:g=2,'
      'acompressor=threshold=-24dB:ratio=4:attack=4:release=70:makeup=3')
src = f'{D}/vo/{TAKE}.mp3'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-ac', '1', '-ar', str(SR), '-af', CH, f'{D}/vo/_c.wav'], check=True)
x = sf.read(f'{D}/vo/_c.wav')[0]
log = subprocess.run(['ffmpeg', '-nostats', '-i', src, '-af', 'silencedetect=n=-38dB:d=0.18', '-f', 'null', '-'],
                     capture_output=True, text=True).stderr
st = [float(v) for v in re.findall(r'silence_start: ([\d.]+)', log)]; en = [float(v) for v in re.findall(r'silence_end: ([\d.]+)', log)]
out, prev = [], 0
for a, b in zip(st, en):
    if a <= 0.05: prev = int(max(0, b - .05) * SR); continue
    keep = .42 if b - a > .7 else .24
    if b - a <= keep: continue
    mid_a = int((a + .06) * SR); out.append(x[prev:mid_a]); out.append(np.zeros(int((keep - .12) * SR))); prev = int((b - .06) * SR)
out.append(x[prev:]); y = np.concatenate(out)
sf.write(f'{D}/vo/_tight.wav', y.astype(np.float32), SR)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{D}/vo/_tight.wav', '-af', f'atempo={SPEED}', '-ar', str(SR), f'{D}/vo/vo48.wav'], check=True)
z = sf.read(f'{D}/vo/vo48.wav')[0]
print('raw', round(len(x) / SR, 1), 'tight', round(len(y) / SR, 1), 'final', round(len(z) / SR, 1))
