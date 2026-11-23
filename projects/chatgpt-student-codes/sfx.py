"""SFX for the ChatGPT student-codes reel, cued from timeline.json + reel shot logic; VO ducking; stems; mux.
Music: Suraj adds it -> deliver final (VO+SFX) + stems. usage: python3 sfx.py"""
import sys, os, json, subprocess, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'engine'))
from earshot_bank import bank
TL = json.load(open('timeline.json')); T = dict(TL['T']); END = T['end']; W = TL['words']
def WT(w, n=1):
    c = 0
    for x in W:
        if x['w'] == w:
            c += 1
            if c == n: return x['s']
T.update(slash1=WT('', 1), slash2=WT('', 2), slash3=WT('', 3), likho=WT('LIKHO,'), daalo2=WT('DAALO,'), paste=WT('PASTE'), tarah=WT('TARAH.'), aur1=WT('AUR', 1), apna=WT('APNA'), kahan=WT('KAHAN'), personal=T['personal'])
SR = 48000; n = int((END + 1) * SR); mix = np.zeros((n, 2))
def L(name): return np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', f'sfx_lib/{name}.wav', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout, np.float32)
def add(t, s, g=1.0, pan=0.0, fade=None):
    i = max(0, int(t * SR)); s = s[:max(0, n - i)].astype(float).copy()
    if fade: s *= np.interp(np.arange(len(s)) / SR, [0, fade[0], fade[1], fade[1] + 0.01], [0, 1, 1, 0])
    l, r = np.cos((pan + 1) * np.pi / 4) * 1.414, np.sin((pan + 1) * np.pi / 4) * 1.414
    mix[i:i + len(s), 0] += s * g * l; mix[i:i + len(s), 1] += s * g * r
# soft "wrong answer" buzz (two low tones, enveloped)
def buzz():
    t = np.arange(int(0.42 * SR)) / SR; x = np.zeros_like(t)
    for s0 in (0, 0.2):
        m = (t >= s0) & (t < s0 + 0.16); u = t[m] - s0; x[m] += (np.sin(2 * np.pi * 196 * u) + 0.4 * np.sin(2 * np.pi * 392 * u) + 0.2 * np.sign(np.sin(2 * np.pi * 98 * u))) * np.minimum(1, u * 80) * np.minimum(1, (0.16 - u) * 80)
    return x * 0.6
sendQ, sendS, sendE = T['likho'] + 0.25, T['daalo2'] + 0.1, T['paste'] + 0.55
cutFix = [T['kat'] + d for d in (0.85, 1.1, 1.35)]; tEnd = cutFix[2] + 0.3
# shot-change whooshes
cuts = [T['chatgpt'], T['teen'] - 0.05, T['padhai'] - 0.1, T['aur1'], T['pehla'], T['chapter'], T['galat'] - 0.12, T['wahin'] - 0.25, T['doosra'], T['textbook'] - 0.08, sendS - 0.15, T['teesra'], T['apna'] - 0.05, T['examiner2'] - 0.3, tEnd]
for i, c in enumerate(cuts): add(c - 0.28, bank('whoosh_fast/crisp'), 0.16, pan=.3 if i % 2 else -.3)
# hook: rain + clock ticks + lamp flicker
add(0, L('rain'), 0.12, fade=(0.05, T['chatgpt'] + 0.6)); add(T['chatgpt'] + 0.6, L('rain'), 0.04, fade=(0.3, 3.0))
for k in range(2): add(0.15 + k * 0.5, bank('fit/tick/domino'), 0.35, pan=.4)
# phone rises + wakes
add(T['chatgpt'] - 0.15, bank('pro_whoosh_big/swell'), 0.28); add(T['chatgpt'] + 0.3, bank('pro_notify/ding_2045'), 0.32)
# intro mystery keycaps
for d in (0, 0.3, 0.52): add(T['teen'] + d - 0.01, bank('knock/plastic'), 0.5, pan=(d - 0.26) * 2)
# clock fast-forward
add(T['padhai'] - 0.1, bank('pro_riser/roll', dur=1.2), 0.18)
for k in range(14): add(T['padhai'] + k * 0.085, bank('fit/tick/domino'), 0.22 * (1 - k / 20))
add(T['half'] - 0.03, bank('cut_hit/punch'), 0.45)
# best: gold shimmer
add(T['last'], bank('reverse_swell/short'), 0.25); add(T['best'] - 0.08, bank('pro_shimmer/m3'), 0.3); add(T['best'] - 0.05, bank('mallet/glock', pitch='E6'), 0.22)
# keycap slams
KT = {'q': [T['slash1']] + [T['quiz'] + i * 0.07 for i in range(4)], 's': [T['slash2']] + [T['snapnotes'] + i * 0.05 for i in range(9)], 'e': [T['slash3']] + [T['examiner'] + i * 0.055 for i in range(8)]}
for w, ts in KT.items():
    for i, t0 in enumerate(ts):
        add(t0 - 0.004, bank('fit/key/thock', seed=i + (7 if w == 'e' else 0)), 0.55 if i else 0.75, pan=np.clip((i - len(ts) / 2) * 0.08, -.5, .5))
    add(ts[0] - 0.01, bank('cut_hit/kick'), 0.4 if w != 'e' else 0.6)
add(T['slash3'] - 0.01, L('sub'), 0.35); add(T['op'] - 0.04, bank('pro_impact/deep'), 0.55); add(T['teesra'] - 0.4, bank('riser/build', dur=1.0), 0.15)
# typing on screen (chars after keycaps)
for i in range(len(' JEE Physics: Rotational Motion')):
    if i % 2 == 0: add(T['chapter'] + 0.05 + i * 0.026, bank('pro_typing_key/soft', seed=i), 0.12)
for s0 in (sendQ, sendS, sendE): add(s0 - 0.02, bank('pro_pop/thup'), 0.32)
# quiz: options pop, tap, wrong buzz, right ding
for d in (-0.05, 0.07, 0.19, 0.31): add(T['mcq'] + d, bank('ui_pop/soft'), 0.22)
add(12.15, bank('tap/glass'), 0.4); add(T['galat'], buzz(), 0.35); add(T['galat'] + 0.3, bank('pro_notify/ding_2296'), 0.3)
add(T['personal'] - 0.05, bank('pro_pop_in/round'), 0.35)
# photo: scan sweep + shutter
add(T['photo'] - 0.4, bank('swish/soft'), 0.25); add(T['photo'] - 0.02, bank('shutter/quick'), 0.6)
add(T['trick'] - 0.08, bank('mallet/celesta', pitch='C6'), 0.3); add(T['trick'] - 0.05, bank('pro_pop_in/double'), 0.25)
# paste: sheet whoosh into phone
add(T['answer'] - 0.05, bank('swish/flick'), 0.3); add(T['paste'] + 0.45, bank('pro_pop_in/airy'), 0.25)
# score stamp + cuts + fixes
add(T['marks'] - 0.05, bank('pro_impact/short'), 0.45); add(T['marks'] - 0.03, bank('knock/desk'), 0.35)
for t0 in (T['batayega'] + 0.3, T['kahan'] + 0.25, T['kat'] + 0.05): add(t0, bank('knock/wood'), 0.35)
for i, f in enumerate(cutFix): add(f, bank('mallet/marimba', pitch=['C5', 'E5', 'G5'][i]), 0.35)
# end: sunrise swell + celebration
add(tEnd - 0.5, bank('reverse_swell/cymbal'), 0.25); add(tEnd + 0.05, bank('pro_impact/air'), 0.4); add(tEnd + 0.1, bank('mallet/flourish'), 0.3)

os.makedirs('final/stems', exist_ok=True); os.makedirs('build', exist_ok=True)
sfx = mix[:int(END * SR)]
vo = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', 'vo/vo_full.wav', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout, np.float32)[:len(sfx)]
vo = np.pad(vo, (0, len(sfx) - len(vo)))
e = np.convolve(np.abs(vo), np.ones(2400) / 2400, 'same'); duck = 1 - np.clip(e / (e.max() * .25 + 1e-9), 0, 1) * .4
sfxd = sfx * duck[:, None] * .6; out = sfxd + vo[:, None]; g = .95 / (np.abs(out).max() + 1e-9)
w = lambda arr, ch, f: subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', str(ch), '-i', '-', f], input=arr.astype(np.float32).tobytes())
w(sfx, 2, 'build/sfx_only.wav'); w(out * g, 2, 'build/mix_raw.wav'); w(vo * g, 1, 'final/stems/vo.wav'); w(sfxd * g, 2, 'final/stems/sfx.wav')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/mix_raw.wav', '-af', 'loudnorm=I=-13.6:TP=-2.2:LRA=11', '-ar', '48000', 'build/mix.wav'])
name = 'final/ChatGPT_Student_Codes.mp4'
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/video_only.mp4', '-i', 'build/mix.wav', '-map', '0:v', '-map', '1:a',
                '-c:v', 'libx264', '-preset', 'slow', '-b:v', '10M', '-minrate', '10M', '-maxrate', '10M', '-bufsize', '10M', '-x264-params', 'nal-hrd=cbr', '-pix_fmt', 'yuv420p',
                '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', name])
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/video_only.mp4', '-c:v', 'copy', '-an', 'final/stems/video_only.mp4'])
print('ok', name)
