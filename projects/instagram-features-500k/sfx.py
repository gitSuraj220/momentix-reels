"""News-style SFX for the Instagram Features reel (no music; Suraj adds BGM). Cues mirror reel.html.
Sources: earshot bank + Motion Array stamp hit (../buy-vs-rent/sfx_src) + small synths (record scratch, coin clink, cash register)."""
import os, sys
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, resample_poly
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(D, '../../engine'))
from earshot_bank import bank
SR = 48000; END = 25.7; rng = np.random.default_rng(5)
mix = np.zeros((int((END + 1.5) * SR), 2), np.float32)
def norm(x): return (x / (np.abs(x).max() + 1e-9) * .89).astype(np.float32)
def B(k): return norm(bank(k))
def load(p):
    x, sr = sf.read(p, dtype='float32'); x = x.mean(1) if x.ndim > 1 else x
    return norm(resample_poly(x, SR, sr) if sr != SR else x)
def add(t, x, g=1.0, pan=0.0, peak=False):
    if peak: t -= int(np.argmax(np.abs(x))) / SR
    i = int(max(0, t) * SR); l, r = np.sqrt(.5 * (1 - pan)), np.sqrt(.5 * (1 + pan)); n = min(len(x), len(mix) - i)
    if n > 0: mix[i:i + n, 0] += x[:n] * g * l; mix[i:i + n, 1] += x[:n] * g * r
def clink(f, g=1):
    t = np.arange(int(.45 * SR)) / SR
    return norm(sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t / d) for m, a, d in [(1, 1, .11), (1.48, .6, .08), (2.3, .35, .05), (3.1, .2, .035)]) * np.minimum(1, t / .001)) * g
def scratch(dur=.36):
    n = int(dur * SR); t = np.arange(n) / SR; sw = np.abs(np.sin(2 * np.pi * (1 / dur) * 1.5 * t))
    tone = np.sin(2 * np.pi * np.cumsum(220 + 900 * sw) / SR) * .5
    nz = sosfilt(butter(2, [700, 5000], 'bandpass', fs=SR, output='sos'), rng.standard_normal(n)) * .6
    return norm((tone + nz) * (.3 + .7 * sw) * np.minimum(1, t / .005) * np.minimum(1, (dur - t) / .02))
def register():  # "cha-ching": drawer thunk + bell
    t = np.arange(int(.9 * SR)) / SR
    thunk = sosfilt(butter(2, 900, 'low', fs=SR, output='sos'), rng.standard_normal(len(t))) * np.exp(-t / .03)
    bell = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-np.maximum(0, t - .12) / .35) * (t > .12) for f, a in [(2637, 1), (3951, .5), (5274, .25)])
    return norm(thunk * .8 + bell * .7)
STAMP = load(f'{D}/../buy-vs-rent/sfx_src/MA_Tuttkile_PowerfulApprovalStampHit_1.wav')
WH = B('whoosh_big/thump') if True else None
# hook: bag slam + coins
add(.05, B('impact/punch'), .55); add(.35, register(), .5, .2)
for i in range(6): add(.4 + i * .07, clink(rng.uniform(2200, 3000), .35), .45, rng.uniform(-.5, .5))
add(.1, B('pro_pop/boop'), .35); add(2.7, B('pro_pop/boop'), .35)
# section whooshes
for t0 in (4.02, 10.63, 15.06): add(t0, B('swipe/paper'), .55, 0, peak=True)
# $ counter ticks + ₹4 crore hit
for t0 in np.arange(4.05, 4.9, .06): add(t0, clink(4200, .2), .18, .3)
add(4.9, B('cut_hit/punch'), .7); add(4.95, register(), .45)
add(6.14, STAMP, .85, 0, peak=True)                             # BAS SHART EK
add(7.7, B('ui_pop/step'), .4, -.4); add(8.1, B('ui_pop/step'), .4, .4)
add(8.25, B('whoosh_fast/crisp'), .4); add(8.85, B('pro_pop/tink'), .35, .4)   # same video slides over
add(11.0, B('pro_pop/boop'), .35)
for t0 in np.arange(12.69, 14.7, .1): add(t0, clink(5200, .15), .1, .2)       # timer ticking to 90:00
add(14.7, B('pro_notify/ding_2045'), .4)
add(15.4, B('cut_hit/kick'), .6)                                 # VS
add(16.8, B('impact/punch'), .8); add(16.85, B('glitch/hit'), .3)  # takkar boom
add(18.99, scratch(), .6); add(19.0, B('cut_hit/sub'), .5)       # PAR RUKO
add(19.6, B('ui_pop/step'), .35); add(19.82, B('pro_pop/tink'), .3); add(22.45, B('pro_pop/tink'), .3)
os.makedirs(f'{D}/audio', exist_ok=True)
sf.write(f'{D}/audio/sfx_only.wav', mix[:int(END * SR)], SR, subtype='PCM_24'); print('sfx ok', np.abs(mix).max())
