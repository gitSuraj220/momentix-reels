"""SFX for HFT video (no music; Suraj adds BGM). Cues mirror reel.html scene times (vo/times.json timeline)."""
import os, sys
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(D, '../../engine'))
from earshot_bank import bank
SR = 48000; END = 84.7; rng = np.random.default_rng(7)
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
add(.5, SUB, .45); add(1.3, PUNCH, .55); add(2.1, STEP, .25)
for i in range(10): add(3.3 + i * .12, TINK, .12, (i - 4.5) / 6)
add(4.9, DING, .4); add(5.45, GL, .18)
add(8.84, PUNCH, .7); add(8.84, KICK, .45); add(11.14, POP, .45); add(11.14, TINK, .3)
add(12.05, WF, .45); add(12.1, KICK, .3)
# system montage
for k in range(13): add(13.6 + k * .18, GL if k % 3 == 0 else STEP, .11 if k % 3 == 0 else .08, ((k % 3) - 1) * .4)
add(15.9, WF, .5); add(16.86, SUB, .8); add(16.86, PUNCH, .6)
# pit
add(19.2, SW, .35); add(24.2, ring(), .32, .3); add(25.04, POP, .4, .3)
add(26.55, WF, .4); add(27.2, GL, .5)
r = B('pro_riser/roll', dur=2.2); add(29.95 - len(r) / SR, r, .45)
add(29.95, SUB, .85); add(29.95, PUNCH, .55)
for i in range(22): add(30.6 + i * .038, STEP, .07)
# you vs giants
add(32.4, SW, .35); add(34.34, TINK, .5, -.4); add(35.6, WF, .5, .4); add(36.3, PUNCH, .55); add(38.22, GL, .45, .4)
# co-location + lines
add(40.3, WF, .4); add(43.2, STEP, .35); add(44.9, WF, .45, .5); add(45.6, DING, .35)
add(46.4, WF, .45); add(46.7, TINK, .25)
# nanosecond
add(49.3, GL, .4)
for i in range(9): add(49.5 + i * .09, STEP, .12)
add(50.3, TINK, .4); add(50.56, PUNCH, .65); add(50.56, KICK, .3)
# money
add(52.2, SW, .4); add(53.8, STEP, .25)
add(55.12, register(), .55); add(55.12, KICK, .35); add(56.74, POP, .35)
add(58.8, SUB, .7); add(58.8, GL, .4); add(61.02, PUNCH, .6)
# people
add(62.5, SW, .3)
for t0, p in [(63.6, -.5), (64.7, 0), (65.56, .5)]: add(t0, POP, .45, p)
add(66.3, WF, .45); add(67.7, STEP, .3); add(70.54, PUNCH, .7); add(70.54, SUB, .45)
# closing
add(71.9, WF, .25); add(73.2, TINK, .2); add(79.78, POP, .45); add(81.5, DING, .4)
os.makedirs(f'{D}/audio', exist_ok=True); sf.write(f'{D}/audio/sfx_only.wav', mix, SR); print('sfx ok', round(np.abs(mix).max(), 2))
