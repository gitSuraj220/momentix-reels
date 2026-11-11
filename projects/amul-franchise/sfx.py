"""SFX for HFT video (no music; Suraj adds BGM). Cues mirror reel.html scene times (vo/times.json timeline)."""
import os, sys
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(D, '../../engine'))
from earshot_bank import bank
SR = 48000; END = 28.6; rng = np.random.default_rng(7)
mix = np.zeros((int((END + 1.5) * SR), 2), np.float32)
def norm(x): return (x / (np.abs(x).max() + 1e-9) * .89).astype(np.float32)
def B(k, **kw): return norm(bank(k, **kw))
def add(t, x, g=1.0, pan=0.0):
    i = int(max(0, t) * SR); l, r = np.sqrt(.5 * (1 - pan)), np.sqrt(.5 * (1 + pan)); n = min(len(x), len(mix) - i)
    if n > 0: mix[i:i + n, 0] += x[:n] * g * l; mix[i:i + n, 1] += x[:n] * g * r
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
def register():
    t = np.arange(int(.9 * SR)) / SR
    thunk = bp(rng.standard_normal(len(t)), 120, 900) * np.exp(-t / .03)
    bell = sum(a * np.sin(2 * np.pi * f * t) for f, a in [(2093, 1), (2637, .6), (4186, .3)]) * np.exp(-np.maximum(0, t - .09) / .35) * (t > .09)
    return norm(.7 * thunk + .5 * bell)
def ring():   # old phone bell ring, two short bursts
    t = np.arange(int(1.1 * SR)) / SR; g = ((t % .5) < .32) * (np.sin(2 * np.pi * 22 * t) > 0)
    x = (np.sin(2 * np.pi * 1280 * t) + .6 * np.sin(2 * np.pi * 1660 * t)) * g * np.exp(-t / .9)
    return norm(bp(x, 600, 5000))
def hum(d):   # server-room air + fan hum
    t = np.arange(int(d * SR)) / SR; x = bp(rng.standard_normal(len(t)), 200, 3000) * .5 + .3 * np.sin(2 * np.pi * 120 * t)
    e = np.minimum(1, t / .6) * np.minimum(1, (d - t) / .6); return norm(x * e)
POP = B('pro_pop/boop'); TINK = B('pro_pop/tink'); SW = B('swipe/paper'); WF = B('whoosh_fast/crisp')
PUNCH = B('impact/punch'); _f = int(.6 * SR); PUNCH = PUNCH[:_f] * np.r_[np.ones(_f - int(.25 * SR)), np.linspace(1, 0, int(.25 * SR))].astype(np.float32); SUB = B('cut_hit/sub'); KICK = B('cut_hit/kick'); GL = B('glitch/hit'); STEP = B('ui_pop/step'); DING = B('pro_notify/ding_2045')
# hook
add(.62, PUNCH, .9); add(.62, KICK, .6); add(.62, GL, .35)
add(.7, WF, .55, .4)
add(.82, STEP, .3); add(1.02, POP, .45); add(2.3, POP, .35); add(4.4, register(), .45)
# amul franchise
add(6.35, WF, .5); add(7.0, PUNCH, .4); add(7.6, POP, .4)
add(8.9, STEP, .25); add(9.55, register(), .6); add(9.55, KICK, .35)
add(10.3, SW, .4); add(11.6, PUNCH, .4); add(12.5, POP, .35)
add(14.1, WF, .45); add(14.32, POP, .5, -.3); add(15.26, POP, .5, 0); add(17.1, POP, .5, .3)
add(18.2, register(), .55); add(19.3, PUNCH, .6); add(19.3, KICK, .3)
add(20.9, WF, .45); add(21.0, SW, .3)
for i in range(30): add(21.6 + i * .046, STEP, .06)
add(23.7, TINK, .45); add(23.85, DING, .45)
add(25.6, WF, .4); add(25.7, POP, .45); add(26.2, TINK, .3)
os.makedirs(f'{D}/audio', exist_ok=True); sf.write(f'{D}/audio/sfx_only.wav', mix, SR); print('sfx ok', round(np.abs(mix).max(), 2))
