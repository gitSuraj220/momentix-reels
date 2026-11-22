"""Code-made SFX for the GTA6 supercar reel -> sfx_lib/*.wav (48 kHz mono)."""
import numpy as np, os, subprocess
from scipy.signal import butter, sosfilt
SR = 48000; R = np.random.default_rng(11); os.makedirs('sfx_lib', exist_ok=True)
t_ = lambda d: np.arange(int(d * SR)) / SR
def bp(x, lo, hi, o=4): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def hp(x, f, o=4): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def lp(x, f, o=4): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def room(x, mix=0.25, d=(0.031, 0.047, 0.061, 0.083), fb=0.45):
    y = x.copy()
    for dl in d:
        n = int(dl * SR); z = np.zeros(len(x) + int(SR * 0.8)); z[:len(x)] += x
        for i in range(n, len(z)): z[i] += fb * z[i - n]
        y = np.pad(y, (0, len(z) - len(y))); y += mix * lp(z, 5000) / len(d)
    return y
def norm(x, pk=0.9): return x / (np.abs(x).max() + 1e-9) * pk
def save(name, x): subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', f'sfx_lib/{name}.wav'], input=norm(x).astype(np.float32).tobytes())

# glass smash
d = 1.4; t = t_(d); x = np.zeros_like(t)
x[:int(.03 * SR)] += lp(R.standard_normal(int(.03 * SR)), 1800) * np.exp(-t[:int(.03 * SR)] * 120) * 1.2
x += np.sin(2 * np.pi * 70 * t) * np.exp(-t * 28) * 0.8
cr = hp(R.standard_normal(len(t)), 2200) * np.exp(-t * 7.5) * (0.6 + 0.4 * (R.random(len(t)) > 0.97)); x += cr * 0.9
for k in range(70):
    s = R.exponential(0.16) + 0.005; f = R.uniform(2600, 9500); dec = R.uniform(18, 60); n = t[t >= s] - s
    x[t >= s] += (np.sin(2 * np.pi * f * n) + 0.5 * np.sin(2 * np.pi * f * 1.47 * n)) * np.exp(-n * dec) * R.uniform(0.08, 0.3) * np.exp(-s * 2)
for k in range(18):
    s = 0.25 + R.random() * 0.9; i = int(s * SR); L = int(0.012 * SR)
    if i + L < len(x): x[i:i + L] += hp(R.standard_normal(L), 3000) * np.exp(-np.arange(L) / SR * 400) * 0.25 * np.exp(-s)
save('glass', room(x, 0.3))

# start fail: relay click + low error buzz x2
t = t_(0.9); x = np.zeros_like(t); L = int(0.006 * SR); x[:L] += hp(R.standard_normal(L), 2500) * 0.8 * np.hanning(L)
for s in (0.08, 0.36):
    n = t[(t >= s) & (t < s + 0.2)] - s; buzz = np.sign(np.sin(2 * np.pi * 110 * n)) * 0.3 + np.sin(2 * np.pi * 220 * n) * 0.4
    x[(t >= s) & (t < s + 0.2)] += lp(buzz, 1800) * np.minimum(1, n * 60) * np.minimum(1, (0.2 - n) * 60) * np.exp(-n * 4)
save('startfail', x)

def engine(f0, dur, grit=0.25, seed=3):
    rr = np.random.default_rng(seed); ph = np.cumsum(2 * np.pi * f0 / SR); n = len(f0)
    x = np.zeros(n)
    for h, a in [(1, 1), (2, .6), (3, .45), (4, .3), (6, .18), (8, .1)]: x += a * np.sin(h * ph + rr.random() * 6)
    fir = (np.sin(ph * 0.5) > 0.6).astype(float); x = x * (0.7 + 0.5 * fir)  # firing pulses
    x += grit * lp(rr.standard_normal(n), 900) * (0.6 + 0.4 * np.sin(ph))
    return np.tanh(x * 1.8)
# engine start: crank -> catch -> rev -> idle
crank = 0.6; d = 2.4; t = t_(d); n = len(t)
f0 = np.where(t < crank, 0, np.interp(t, [crank, crank + .12, crank + .45, crank + .8, crank + 1.2, d], [18, 34, 95, 62, 38, 36]))
eng = engine(np.maximum(f0, 1), d) * (t >= crank) * np.minimum(1, (t - crank).clip(0) * 25)
ck = np.zeros(n); tc = t[t < crank]; ck[:len(tc)] = (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 9 * tc))) * bp(R.standard_normal(len(tc)), 150, 1800) * 0.5 + np.sin(2 * np.pi * 140 * tc + 3 * np.sin(2 * np.pi * 9 * tc)) * 0.25
x = lp(eng, 4000) * 0.9 + ck; save('enginestart', room(x, 0.15))

# rev + drive away (doppler-ish fade)
d = 3.2; t = t_(d); f0 = np.interp(t, [0, .5, .62, 1.3, 1.45, 2.2, d], [40, 120, 80, 135, 95, 120, 110])
x = engine(f0, d, 0.35, 5); x = lp(x, 5000) * np.interp(t, [0, .1, 1.6, d], [0.3, 1, 0.8, 0.12])
x[int(1.6 * SR):] = lp(x[int(1.6 * SR):], 1500); save('revaway', x)
# tyre chirp
t = t_(0.5); x = bp(R.standard_normal(len(t)), 1200, 3800) * np.exp(-t * 6) * (0.6 + 0.4 * np.sin(2 * np.pi * 37 * t)); save('chirp', x)

# siren (two-tone wail), plus distant version
d = 3.0; t = t_(d); f = 760 + 430 * (0.5 + 0.5 * np.sin(2 * np.pi * 0.85 * t - 1.5)); ph = np.cumsum(2 * np.pi * f / SR)
s = np.sin(ph) + 0.35 * np.sin(2 * ph) + 0.15 * np.sign(np.sin(ph)); s = lp(s, 3500)
save('siren', room(s, 0.4)); save('siren_far', room(lp(s, 1400), 0.6))
# radar ping
t = t_(0.7); x = np.sin(2 * np.pi * 1320 * t) * np.exp(-t * 7) + 0.4 * np.sin(2 * np.pi * 2640 * t) * np.exp(-t * 11); save('ping', room(x, 0.5))
# scanner chirps (phone key cloner)
t = t_(0.12); x = np.sin(2 * np.pi * (2200 + 9000 * t) * t) * np.exp(-t * 20); save('scan', x)
# low sub drop / impact for punches
t = t_(1.0); x = np.sin(2 * np.pi * (60 - 25 * t) * t) * np.exp(-t * 4) + lp(R.standard_normal(len(t)), 400) * np.exp(-t * 18) * 0.5; save('sub', x)
# rain hiss (short, used only under the hook)
d = 4.0; t = t_(d); x = bp(R.standard_normal(len(t)), 900, 9000) * 0.35
for k in range(500): i = int(R.random() * (len(t) - 400)); x[i:i + 300] += hp(R.standard_normal(300), 3000) * np.exp(-np.arange(300) / SR * 900) * R.uniform(0.2, 0.7)
save('rain', x)
print('ok', sorted(os.listdir('sfx_lib')))
