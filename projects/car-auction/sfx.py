"""SFX for car auction reel (no music; Suraj adds BGM). Cues mirror reel.html scene times (vo/times.json timeline)."""
import os, sys
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(D, '../../engine'))
from earshot_bank import bank
SR = 48000; END = 51.3; rng = np.random.default_rng(7)
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
# hook: each car whooshes in, price stamp slams
for t0, ts in [(0.25, 1.7), (2.6, 3.8), (4.9, 5.86)]:
    add(t0 - .05, WF, .55, .4); add(t0 + .1, STEP, .25)
    add(ts, PUNCH, .7); add(ts, KICK, .45); add(ts + .02, TINK, .25)
add(2.35, SW, .3, -.4); add(4.65, SW, .3, -.4)
# chori nahi -> official auction
add(6.95, WF, .45); add(7.15, POP, .4); add(7.95, GL, .35); add(7.95, KICK, .3)
add(8.7, POP, .4); add(9.3, POP, .45); add(9.84, PUNCH, .75); add(9.84, KICK, .45)
# EMI rows
add(11.0, WF, .45); add(12.25, POP, .45, -.2); add(14.4, POP, .45, .2); add(14.6, STEP, .3); add(16.4, POP, .45, -.2); add(17.75, register(), .45)
# 40-50%
add(19.05, SW, .4); add(20.0, STEP, .25); add(20.6, STEP, .25)
for i in range(12): add(21.7 + i * .05, STEP, .07)
add(22.35, PUNCH, .5); add(23.2, POP, .45)
# sites
add(24.45, WF, .45); add(24.6, POP, .4); add(24.9, POP, .35)
for k, t in enumerate([26.3, 26.6, 26.9]): add(t, TINK, .35, (k - 1) * .4)
add(27.5, DING, .4)
# 3 steps
add(29.45, WF, .45); add(29.5, PUNCH, .4); add(30.2, POP, .4)
for i in range(3): add(30.3 + i * .2, STEP, .35, (i - 1) * .4)
# step 1 form
add(31.45, SW, .4); add(31.6, POP, .35)
for i in range(28): add(31.9 + i * .043, STEP, .05)
add(33.9, register(), .5)
# step 2 inspection
add(34.55, WF, .45); add(35.3, POP, .4)
for i in range(4): add(36.5 + i * .35, TINK, .3)
add(37.95, POP, .45)
# step 3 bid
add(39.8, WF, .45); add(40.45, POP, .4); add(41.5, PUNCH, .5); add(41.55, DING, .35)
# ghar le aao
add(42.35, SW, .4); add(42.9, register(), .55); add(42.95, TINK, .35)
# CTA
add(43.85, WF, .4); add(45.5, POP, .45); add(46.6, PUNCH, .5)
for i in range(3): add(46.75 + i * .15, STEP, .2)
add(47.5, TINK, .4); add(47.75, WF, .4, .4); add(48.85, DING, .5)
os.makedirs(f'{D}/audio', exist_ok=True); sf.write(f'{D}/audio/sfx_only.wav', mix, SR); print('sfx ok', round(np.abs(mix).max(), 2))
