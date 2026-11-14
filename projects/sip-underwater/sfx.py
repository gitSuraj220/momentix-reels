"""SFX for the SIP underwater reel (no music; Suraj adds BGM)."""
import os, sys
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(D, '../../engine'))
from earshot_bank import bank
SR = 48000; END = 20.9; rng = np.random.default_rng(3)
mix = np.zeros((int((END + .5) * SR), 2), np.float32)
def norm(x): return (x / (np.abs(x).max() + 1e-9) * .89).astype(np.float32)
def B(k, **kw): return norm(bank(k, **kw))
def add(t, x, g=1.0, pan=0.0):
    i = int(max(0, t) * SR); l, r = np.sqrt(.5 * (1 - pan)), np.sqrt(.5 * (1 + pan)); n = min(len(x), len(mix) - i)
    if n > 0: mix[i:i + n, 0] += x[:n] * g * l; mix[i:i + n, 1] += x[:n] * g * r
def lp(x, f): return sosfilt(butter(2, f, 'low', fs=SR, output='sos'), x)
def bp(x, a, b): return sosfilt(butter(2, [a, b], 'band', fs=SR, output='sos'), x)
def underwater(d):
    t = np.arange(int(d * SR)) / SR; x = lp(rng.standard_normal(len(t)), 300) * (1 + .3 * np.sin(2 * np.pi * .2 * t))
    return norm(x * np.minimum(1, t / 1.0) * np.minimum(1, (d - t) / 1.0))
def bubble(f0=None):
    f0 = f0 or rng.uniform(500, 1400); d = .09; t = np.arange(int(d * SR)) / SR
    return norm(np.sin(2 * np.pi * f0 * (1 + 2.5 * t / d) * t) * np.exp(-t / .03))
def kick():
    d = .35; t = np.arange(int(d * SR)) / SR; return norm(bp(rng.standard_normal(len(t)), 150, 900) * np.sin(np.pi * t / d) ** 2)
def creak(d=1.4):
    t = np.arange(int(d * SR)) / SR; f = 90 + 40 * np.sin(2 * np.pi * 1.3 * t)
    x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * (rng.random(len(t)) > .3); return norm(bp(x, 300, 2500) * np.minimum(1, t / .5) * (1 - t / d))
POP = B('pro_pop/boop'); WIDE = B('ui_pop/wide'); THUD = B('impact/punch'); KICKH = B('cut_hit/kick'); CLG = B('pro_click/glass')
WUP = B('pro_zip/up'); RISE = B('riser/snatch'); WF = B('whoosh_fast/crisp'); SHIM = B('pro_shimmer/m1'); CELE = B('mallet/celesta')
BLOOM = B('logo_sting/soft_bloom'); ZDW = B('pro_zip/down_warm'); GL = B('glitch/hit'); TINK = B('pro_pop/tink'); SUBQ = B('pro_sub_drop/quick')
add(0, underwater(END), .5)
for t in np.arange(.2, END - .5, .19):   # bubble trickle
    if rng.random() < .6: add(t + rng.uniform(0, .1), bubble(), .1, rng.uniform(-.7, .7))
for t in np.arange(.4, 7.0, .45): add(t, kick(), .25, -.5)          # left kicking
for t in np.arange(.6, 14.4, .45): add(t, kick(), .25 if t < 10 else .15, .5)   # right kicking (tiring)
add(.5, TINK, .3); add(.55, GL, .2)                                 # market ticker
for t0, pan in [(1.3, -.4), (4.6, .4), (7.0, -.4), (9.4, -.4), (10.6, .4), (12.4, .4), (16.0, -.4)]: add(t0, WIDE if t0 in (12.4,) else POP, .4, pan)
add(7.3, ZDW, .4, -.4); add(9.35, THUD, .45, -.4); add(9.36, SUBQ, .3, -.4)    # sinks, lands
add(12.6, creak(1.8), .35, .4); add(SNAP := 14.4, CLG, .6, .4); add(14.4, KICKH, .5, .4); add(14.4, GL, .3, .4)
add(14.4 - len(RISE) / SR + .02, RISE, .25, .4); add(14.45, WUP, .5, .4); add(14.5, WF, .45, .4)
for i in range(10): add(14.5 + i * .06, bubble(rng.uniform(600, 1600)), .25, .4)
add(15.2, B('swipe/paper'), .2, .4); add(15.2, THUD, .3, .4); add(15.25, SHIM, .5, .4); add(15.4, CELE, .45, .4); add(15.6, BLOOM, .4, .3)
add(17.0, SHIM, .25, .4); add(18.8, SHIM, .2, .4)
sf.write(f'{D}/audio/sfx_only.wav', mix, SR); print('sfx ok')
