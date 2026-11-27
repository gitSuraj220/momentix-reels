"""SFX for the Maths Dangal ad (chalkboard). Cued from timeline.json + reel.html element times. VO ducking, stems, mux.
Music: Suraj adds it -> final (VO+SFX) + stems."""
import sys, os, json, subprocess, numpy as np
from scipy.signal import butter, sosfilt
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'engine'))
from earshot_bank import bank
TL = json.load(open('timeline.json')); T = TL['T']; END = T['end']
SR = 48000; n = int((END + 1) * SR); mix = np.zeros((n, 2)); R = np.random.default_rng(5)
def add(t, s, g=1.0, pan=0.0):
    i = max(0, int(t * SR)); s = np.asarray(s, float)[:max(0, n - i)]
    l, r = np.cos((pan + 1) * np.pi / 4) * 1.414, np.sin((pan + 1) * np.pi / 4) * 1.414
    mix[i:i + len(s), 0] += s * g * l; mix[i:i + len(s), 1] += s * g * r
bp = lambda x, lo, hi: sosfilt(butter(4, [lo, hi], 'band', fs=SR, output='sos'), x)
lp = lambda x, f: sosfilt(butter(4, f, 'low', fs=SR, output='sos'), x)
def chalk(d):  # chalk on slate: gritty band noise in short strokes + squeak-free taps
    m = int(d * SR); t = np.arange(m) / SR; x = bp(R.standard_normal(m), 1800, 7000)
    grit = (R.random(m) > 0.85) * R.random(m); x = x * (0.55 + 0.9 * grit)
    env = np.zeros(m); pos = 0
    while pos < m:
        L = int(R.uniform(0.06, 0.16) * SR); a = np.sin(np.linspace(0, np.pi, min(L, m - pos))) ** 0.6; env[pos:pos + len(a)] = a * R.uniform(0.6, 1); pos += L + int(R.uniform(0.0, 0.04) * SR)
    x = x * env; x[:int(0.01 * SR)] += bp(R.standard_normal(int(0.01 * SR)), 800, 4000) * np.hanning(int(0.01 * SR)) * 2
    return x / (np.abs(x).max() + 1e-9) * np.minimum(1, t * 40) * np.minimum(1, (d - t) * 25)
def rub(d):  # felt eraser rub
    m = int(d * SR); t = np.arange(m) / SR; x = lp(R.standard_normal(m), 1400) * (0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 6 * t)))
    return x / (np.abs(x).max() + 1e-9) * np.sin(np.pi * t / d) ** 0.5
def buzzer():
    m = int(0.55 * SR); t = np.arange(m) / SR; x = (np.sign(np.sin(2 * np.pi * 220 * t)) * 0.4 + np.sin(2 * np.pi * 440 * t) * 0.5); x = lp(x, 2500)
    return x * np.minimum(1, t * 80) * np.minimum(1, (0.55 - t) * 30) * 0.7
def wt(w, after=0):
    for o in TL['words']:
        if o['s'] >= after and ''.join(c for c in o['w'].lower() if c.isalnum()) == w: return o['s']
    return after
# hook: wall of 27 formulas scribbled fast
for i in range(27): add(0.1 + i * 0.095, chalk(0.11), 0.16, pan=((i % 3) - 1) * 0.4)
add(T['n27'] - 0.05, bank('cut_hit/punch'), 0.5); add(T['n27'] - 0.03, bank('knock/desk'), 0.3)
# wipes
WIPES = [(T['hexagon'] - 1.0, T['hexagon'] - 0.15), (T['rule1'] - 0.35, T['rule1'] - 0.02), (T['rule2'] - 0.35, T['rule2'] - 0.02), (T['rule3'] - 0.35, T['rule3'] - 0.02),
         (T['rule4'] - 0.35, T['rule4'] - 0.02), (T['literally'] - 0.05, T['literally'] + 0.2), (T['poori'] - 0.3, T['poori'] + 0.15)]
for w0, w1 in WIPES: add(w0, rub(w1 - w0), 0.26)
# hexagon + spokes + labels
add(T['hexagon'] - 0.05, chalk(0.75), 0.34); add(T['hexagon'] + 0.65, chalk(0.35), 0.2)
for k in ('sin1', 'tan1', 'sec1', 'cos1', 'cot1', 'cosec1'): add(T[k], chalk(0.22), 0.3, pan=(-0.3 if k in ('sin1', 'tan1', 'sec1') else 0.3)); add(T[k] + 0.12, bank('ui_pop/soft'), 0.12)
add(T['beech'] + 0.35, chalk(0.22), 0.3); add(T['beech'] + 0.5, bank('mallet/marimba', pitch='C6'), 0.3)
add(T['right'] + 0.15, chalk(0.35), 0.22); add(T['setup'] - 0.1, chalk(0.4), 0.3); add(T['setup'] + 0.3, bank('pro_notify/ding_2045'), 0.3)
# rule chips
for k in ('rule1', 'rule2', 'rule3', 'rule4'): add(T[k] - 0.05, bank('ui_pop/soft'), 0.35); add(T[k] - 0.02, bank('pro_pop_in/round'), 0.2)
# rule 1: diagonals + formulas
notes = ['E5', 'G5', 'C6']
for i, k in enumerate(('sin2', 'cos2', 'tan2')): add(T[k] - 0.1, bank('swish/soft'), 0.25); add(T[k] - 0.05, chalk(0.48), 0.28); add(T[k] + 0.3, bank('mallet/marimba', pitch=notes[i]), 0.28)
add(T['tan2'] + 0.45, chalk(0.4), 0.2)
# rule 2: arrows + formulas
add(T['tan3'] - 0.35, bank('whoosh_fast/crisp'), 0.22); add(T['tan3'], chalk(0.6), 0.3)
add(T['cot3'] - 0.35, bank('whoosh_fast/tight'), 0.22); add(T['cot3'], chalk(0.6), 0.3)
# rule 3
add(T['padosi'] - 0.2, bank('swish/soft'), 0.25); add(T['padosi'], bank('pro_pop/thup'), 0.2); add(T['padosi'] + 0.1, bank('pro_pop/thup'), 0.2)
add(T['tan4'], chalk(0.6), 0.3); add(T['tan4'] + 0.65, chalk(0.45), 0.2)
# rule 4
for i in range(3): add(T['neeche'] + i * 0.25, bank('ui_pop/step'), 0.22, pan=(i - 1) * 0.4)
for i, dt in enumerate((0, 0.75, 1.35)): add(T['sin5'] + dt, chalk(0.55), 0.3); add(T['sin5'] + dt + 0.5, bank('mallet/marimba', pitch=['C6', 'E6', 'G6'][i]), 0.22)
# cheat code (student)
add(T['literally'] + 0.2, bank('impact/punch'), 0.5); add(T['literally'] + 0.22, bank('cut_hit/sub'), 0.3); add(T['literally'] + 0.55, chalk(0.7), 0.25); add(T['literally'] + 1.25, bank('pro_shimmer/m2'), 0.25)
# CTA
add(T['comment'] - 0.05, chalk(0.3), 0.25); add(T['formula'] - 0.05, bank('pro_impact/short'), 0.4); add(T['formula'] + 0.05, bank('ui_pop/soft'), 0.3)
add(T['dm'] - 0.45, chalk(0.45), 0.25); add(T['dm'] + 0.1, bank('pro_notify/ding_2296'), 0.35)
os.makedirs('final/stems', exist_ok=True)
sfx = mix[:int(END * SR)]
vo = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', 'vo/vo_full.wav', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout, np.float32)[:len(sfx)]
vo = np.pad(vo, (0, len(sfx) - len(vo)))
e = np.convolve(np.abs(vo), np.ones(2400) / 2400, 'same'); duck = 1 - np.clip(e / (e.max() * .25 + 1e-9), 0, 1) * .35
sfxd = sfx * duck[:, None] * .6; out = sfxd + vo[:, None]; g = .95 / (np.abs(out).max() + 1e-9)
w = lambda arr, ch, f: subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', str(ch), '-i', '-', f], input=arr.astype(np.float32).tobytes())
w(out * g, 2, 'build/mix_raw.wav'); w(vo * g, 1, 'final/stems/vo.wav'); w(sfxd * g, 2, 'final/stems/sfx.wav')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/mix_raw.wav', '-af', 'loudnorm=I=-13.6:TP=-2.2:LRA=11', '-ar', '48000', 'build/mix.wav'])
name = 'final/Trig_Hexagon.mp4'
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/video_only.mp4', '-i', 'build/mix.wav', '-map', '0:v', '-map', '1:a',
                '-c:v', 'libx264', '-preset', 'slow', '-b:v', '10M', '-minrate', '10M', '-maxrate', '10M', '-bufsize', '10M', '-x264-params', 'nal-hrd=cbr', '-pix_fmt', 'yuv420p', '-r', '30',
                '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', name])
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/video_only.mp4', '-c:v', 'copy', '-an', 'final/stems/video_only.mp4'])
print('ok', name)
