"""SFX for Short Selling skit (no music; Suraj adds BGM). Cues mirror reel.html / make_base.py cuts."""
import os, sys
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(D, '../../engine'))
from earshot_bank import bank
SR = 48000; END = 49.29; rng = np.random.default_rng(11)
mix = np.zeros((int((END + 1.5) * SR), 2), np.float32)
def norm(x): return (x / (np.abs(x).max() + 1e-9) * .89).astype(np.float32)
def B(k): return norm(bank(k))
def add(t, x, g=1.0, pan=0.0):
    i = int(max(0, t) * SR); l, r = np.sqrt(.5 * (1 - pan)), np.sqrt(.5 * (1 + pan)); n = min(len(x), len(mix) - i)
    if n > 0: mix[i:i + n, 0] += x[:n] * g * l; mix[i:i + n, 1] += x[:n] * g * r
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
def scratch():   # vinyl record scratch: noise through a fast back-and-forth swept band
    d = .55; n = int(d * SR); t = np.arange(n) / SR; out = np.zeros(n)
    f = 900 + 2600 * np.abs(np.sin(2 * np.pi * 3.2 * t)); nz = rng.standard_normal(n)
    for k in range(0, n, 480):
        seg = slice(k, k + 480); out[seg] = bp(nz[seg], f[k] * .6, min(f[k] * 1.6, 20000))
    return norm(out * np.minimum(1, t / .01) * np.minimum(1, (d - t) / .08))
def register():  # cash register "ka-ching": drawer thunk + two bright bell partials
    t = np.arange(int(.9 * SR)) / SR
    thunk = bp(rng.standard_normal(len(t)), 120, 900) * np.exp(-t / .03)
    bell = sum(a * np.sin(2 * np.pi * f * t) for f, a in [(2093, 1), (2637, .6), (4186, .3)]) * np.exp(-np.maximum(0, t - .09) / .35) * (t > .09)
    return norm(.7 * thunk + .5 * bell)
def gulp():
    t = np.arange(int(.22 * SR)) / SR; f = 520 * np.exp(-t * 6)
    return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .07) * np.minimum(1, t / .004))
POP = B('pro_pop/boop'); TINK = B('pro_pop/tink'); SW = B('swipe/paper'); WF = B('whoosh_fast/crisp')
# hook freeze
add(0.08, scratch(), .6); add(.1, B('cut_hit/punch'), .5); add(.15, POP, .45); add(1.0, WF, .4)
# Momo's plan
add(4.6, TINK, .25, .3)                              # idea glint
add(9.0, register(), .45); add(9.0, POP, .35)        # BECHA 80,000
add(9.2, POP, .2)
add(13.0, SW, .4); add(13.0, POP, .35, -.2)          # KHARIDA 60,000
add(15.2, register(), .6); add(15.2, B('cut_hit/kick'), .35)   # +20,000
# 1 saal baad
add(16.5, WF, .6); add(16.9, TINK, .45); add(17.25, B('swipe/paper'), .35)
# return + shock
add(19.2, SW, .3); add(25.5, B('cut_hit/kick'), .45); add(28.5, B('impact/punch'), .55); add(28.55, POP, .3)
add(29.95, gulp(), .5, .3)
# lesson
add(36.1, B('impact/punch'), .55); add(36.12, B('cut_hit/sub'), .4)
add(37.2, POP, .35); add(39.6, B('pro_notify/ding_2045'), .4); add(41.3, B('glitch/hit'), .4)
add(42.8, SW, .3); add(45.8, POP, .4); add(47.6, TINK, .4); add(47.7, B('ui_pop/step'), .3)
os.makedirs(f'{D}/audio', exist_ok=True)
sf.write(f'{D}/audio/sfx_only.wav', mix[:int(END * SR)], SR, subtype='PCM_24'); print('sfx ok', np.abs(mix).max())
