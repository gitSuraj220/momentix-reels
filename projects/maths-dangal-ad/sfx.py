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
# board writes (mirror reel.html: id, t0, dur)
W = [(0.22, 0.95), (T['ye'] - 0.05, 0.2), (T['teen'] + 0.45, 0.55), (T['ulta'] - 0.05, 0.5), (T['aadha'] - 0.45, 0.6), (T['nau'] - 0.08, 0.18),
     (T['sau'] - 0.45, 0.55), (T['guna1'] - 0.45, 0.8), (T['guna2'] - 0.55, 0.15), (T['guna2'] - 0.45, 0.8), (T['speed'] - 0.15, 0.45), (T['practice'] - 0.7, 0.75), (T['barah'] - 0.1, 0.5)]
for i, (t0, d) in enumerate(W): add(t0, chalk(d), 0.32, pan=(-0.2 if i % 2 else 0.2))
# wipes (eraser)
for w0, w1 in [(T['dekho'] - 0.05, T['dekho'] + 0.45), (T['kyun'] - 0.2, T['kyun'] + 0.35), (T['par'] - 0.15, T['par'] + 0.38), (T['isliye'] - 0.05, T['isliye'] + 0.3)]:
    add(w0, rub(w1 - w0), 0.28)
# countdown ticks + buzzer
c0 = T['teen'] + 0.02; st = (T['nahi'] - c0) / 3
for k in range(6): add(c0 + k * st / 2, bank('fit/tick/domino'), 0.55 if k % 2 == 0 else 0.3, pan=.25 if k % 2 else -.25)
add(T['nahi'] - 0.01, buzzer(), 0.5); add(T['nahi'], bank('cut_hit/kick'), 0.35)
# trick: arrows swish, swap whoosh, ULTA pop, 9 ding, ho gaya
add(T['bas'] + 0.03, bank('swish/soft'), 0.3); add(T['e18'] + 0.2, bank('whoosh_fast/crisp'), 0.3)
add(T['ulta'] - 0.05, bank('ui_pop/soft'), 0.25); add(T['nau'] + 0.02, bank('mallet/marimba', pitch='G5'), 0.4); add(T['ho'] - 0.02, bank('pro_notify/ding_2045'), 0.3)
# why: SAME stamp
add(T['same'] - 0.08, bank('cut_hit/punch'), 0.5); add(T['same'] - 0.06, bank('knock/desk'), 0.35)
# PDF shots: page whooshes
for t0 in (T['maths'] - 0.32, T['pehle'] - 0.42, T['practice2'] - 0.2): add(t0 - 0.12, bank('whoosh_fast/crisp'), 0.3); add(t0 + 0.05, bank('swish/flick'), 0.18)
add(T['percentage'] - 0.2, bank('whoosh_fast/crisp'), 0.25)
# chips + 12 chapters
for t0 in (T['percentage'] - 0.05, T['percentage'] + 0.45, T['time'] - 0.05): add(t0, bank('ui_pop/soft'), 0.35)
add(T['barah'] + 0.35, bank('pro_impact/short'), 0.35)
# end card
add(T['teen2'] - 0.3, bank('reverse_swell/short'), 0.22); add(T['teen2'] - 0.1, bank('pro_impact/air'), 0.35)
add(T['ninety'] - 0.05, bank('pro_notify/ding_2296'), 0.35); add(T['neeche'] + 0.02, bank('pro_pop_in/round'), 0.3)
os.makedirs('final/stems', exist_ok=True)
sfx = mix[:int(END * SR)]
vo = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', 'vo/vo_full.wav', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout, np.float32)[:len(sfx)]
vo = np.pad(vo, (0, len(sfx) - len(vo)))
e = np.convolve(np.abs(vo), np.ones(2400) / 2400, 'same'); duck = 1 - np.clip(e / (e.max() * .25 + 1e-9), 0, 1) * .35
sfxd = sfx * duck[:, None] * .6; out = sfxd + vo[:, None]; g = .95 / (np.abs(out).max() + 1e-9)
w = lambda arr, ch, f: subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', str(ch), '-i', '-', f], input=arr.astype(np.float32).tobytes())
w(out * g, 2, 'build/mix_raw.wav'); w(vo * g, 1, 'final/stems/vo.wav'); w(sfxd * g, 2, 'final/stems/sfx.wav')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/mix_raw.wav', '-af', 'loudnorm=I=-13.6:TP=-2.2:LRA=11', '-ar', '48000', 'build/mix.wav'])
name = 'final/Maths_Dangal_Ad.mp4'
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/video_only.mp4', '-i', 'build/mix.wav', '-map', '0:v', '-map', '1:a',
                '-c:v', 'libx264', '-preset', 'slow', '-b:v', '10M', '-minrate', '10M', '-maxrate', '10M', '-bufsize', '10M', '-x264-params', 'nal-hrd=cbr', '-pix_fmt', 'yuv420p', '-r', '30',
                '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', name])
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/video_only.mp4', '-c:v', 'copy', '-an', 'final/stems/video_only.mp4'])
print('ok', name)
