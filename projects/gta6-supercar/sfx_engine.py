import numpy as np, subprocess
from scipy.signal import butter, sosfilt, lfilter
SR = 48000; R = np.random.default_rng(4)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def lp(x, f, o=4): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def reson(x, f, q):  # 2-pole resonator
    r = np.exp(-np.pi * f / q / SR); th = 2 * np.pi * f / SR; return lfilter([1 - r], [1, -2 * r * np.cos(th), r * r], x)
def engine(rpm, cyl=8, seed=1):
    rr = np.random.default_rng(seed); n = len(rpm); fire = rpm / 60 * cyl / 2  # firing freq
    ph = np.cumsum(fire / SR); idx = np.where(np.diff(np.floor(ph)) > 0)[0]; x = np.zeros(n)
    for j, i in enumerate(idx):  # combustion pulse: short decaying noise+click, slight per-cylinder variation
        L = min(int(SR / max(fire[i], 1) * 0.9), n - i, 2400); k = np.arange(L) / SR
        amp = 1 + 0.25 * np.sin(j * 2.1) + 0.15 * rr.standard_normal()
        x[i:i + L] += amp * (np.exp(-k * 900) * (1 + 0.5 * rr.standard_normal(L)) )
    y = 0.9 * reson(x, 95, 3) + 0.6 * reson(x, 210, 4) + 0.45 * reson(x, 480, 5) + 0.25 * reson(x, 1100, 6) + 0.08 * bp(x, 1500, 5000)
    y = np.tanh(y * 3.0 / (np.abs(y).max() + 1e-9))
    y += 0.06 * bp(rr.standard_normal(n), 2000, 7000) * (rpm / rpm.max())  # intake hiss
    return lp(y, 7000)
def save(name, x): x = x / np.abs(x).max() * 0.9; subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', f'sfx_lib/{name}.wav'], input=x.astype(np.float32).tobytes())
# start: starter crank 0.55 s then catch, blip to 5500 rpm, settle idle 1100
d = 2.6; t = np.arange(int(d * SR)) / SR; cr = 0.55
rpm = np.interp(t, [0, cr, cr + .1, cr + .4, cr + .75, cr + 1.2, d], [250, 300, 1400, 5600, 2600, 1150, 1100])
e = engine(rpm) * np.clip((t - cr) * 20, 0, 1)
crank = np.zeros_like(t); tc = t < cr; m = (0.5 + 0.5 * np.sin(2 * np.pi * 7.5 * t[tc]))
crank[tc] = bp(R.standard_normal(tc.sum()), 200, 2500) * m * 0.35 + np.sin(2 * np.pi * (180 + 20 * np.sin(2 * np.pi * 7.5 * t[tc])) * t[tc]) * m * 0.2
save('enginestart', e + crank)
d = 3.2; t = np.arange(int(d * SR)) / SR
rpm = np.interp(t, [0, .45, .55, 1.25, 1.35, 2.2, d], [1200, 6500, 4200, 7000, 4800, 6800, 6500])
x = engine(rpm, seed=2) * np.interp(t, [0, .08, 1.7, d], [0.35, 1, 0.85, 0.1]); x[int(1.7 * SR):] = lp(x[int(1.7 * SR):], 1800); save('revaway', x)
print('ok')
