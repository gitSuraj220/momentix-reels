"""SFX for GTA6 PS5 stream Short (no music). Cues mirror reel.html."""
import os, sys
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(D, '../../engine'))
from earshot_bank import bank
SR = 48000; END = 47.0; rng = np.random.default_rng(6)
mix = np.zeros((int((END + 1.5) * SR), 2), np.float32)
def norm(x): return (x / (np.abs(x).max() + 1e-9) * .89).astype(np.float32)
def B(k): return norm(bank(k))
def add(t, x, g=1.0, pan=0.0):
    i = int(max(0, t) * SR); l, r = np.sqrt(.5 * (1 - pan)), np.sqrt(.5 * (1 + pan)); n = min(len(x), len(mix) - i)
    if n > 0: mix[i:i + n, 0] += x[:n] * g * l; mix[i:i + n, 1] += x[:n] * g * r
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
def glass(d=1.4):  # shatter: dense random tinkles + noise burst
    n = int(d * SR); t = np.arange(n) / SR; out = bp(rng.standard_normal(n), 2500, 12000) * np.exp(-t / .12) * .8
    for _ in range(70):
        st = int(rng.uniform(0, d * .8) * SR); f = rng.uniform(2500, 7500); L = int(.12 * SR); tt = np.arange(L) / SR
        seg = np.sin(2 * np.pi * f * tt) * np.exp(-tt / rng.uniform(.02, .06)) * rng.uniform(.2, .6) * np.exp(-st / SR / .5)
        out[st:st + L] += seg[:max(0, min(L, n - st))]
    return norm(out)
def blip(f=1200, d=.06):
    t = np.arange(int(d * SR)) / SR; return norm(np.sin(2 * np.pi * f * t) * np.exp(-t / (d / 3)))
def footstep():
    t = np.arange(int(.12 * SR)) / SR; return norm(bp(rng.standard_normal(len(t)), 80, 900) * np.exp(-t / .025))
POP = B('pro_pop/boop'); TINK = B('pro_pop/tink'); WF = B('whoosh_fast/crisp'); CLICK = B('ui_pop/step')
# hook: footsteps, bat whoosh, smash
for k, tt in enumerate([.2, .75, 1.3, 1.85, 2.4]): add(tt, footstep(), .35, -.2 + .1 * k)
add(.15, POP, .4); add(.5, TINK, .3, .4)
add(2.85, WF, .6); add(3.2, B('impact/punch'), .75); add(3.2, glass(), .6); add(3.22, B('cut_hit/sub'), .5)
add(3.3, POP, .4); add(5.65, B('cut_hit/kick'), .45); add(5.7, POP, .35)
add(7.4, B('glitch/hit'), .35); add(7.85, B('glitch/hit'), .3); add(8.8, B('impact/punch'), .55)
# UI sections
for s in [9.25, 14.2, 20.9, 29.2, 35.9, 40.3]: add(s - .12, WF, .4); add(s, POP, .35)
add(11.6, blip(1500), .35); add(11.9, B('pro_notify/ding_2045'), .3)            # live streaming ON
add(14.9, B('cut_hit/kick'), .3)                                               # game on
add(16.6, CLICK, .55); add(16.62, blip(900, .05), .3)                          # create press
for tt in [17.0, 17.5, 17.95]: add(tt, blip(1300 if tt < 17.9 else 1800), .3)   # menu nav
add(19.5, CLICK, .45); add(20.0, B('pro_notify/ding_2045'), .3)                # linked
for tt in [21.0, 22.5, 24.4, 25.6, 26.6]: add(tt, blip(1350), .3)
add(26.7, TINK, .3)
add(30.3, CLICK, .5); add(30.35, blip(1000, .25), .25)                         # mic on beep
add(33.3, blip(800, .08), .3)
add(36.95, CLICK, .6); add(37.2, B('pro_notify/ding_2045'), .45); add(37.25, B('cut_hit/punch'), .4)  # GO LIVE
for k in range(6): add(38.0 + k * .3, POP, .18, .3)                               # chat pops
for k in range(3): add(41.0 + k * .6, TINK, .3)                                # checklist
add(42.9, B('impact/punch'), .4)
# ending callback: bat whoosh + smash to black
add(44.5, WF, .45); add(46.35, WF, .6); add(46.6, B('impact/punch'), .7); add(46.6, glass(.9), .5)
os.makedirs(f'{D}/audio', exist_ok=True)
sf.write(f'{D}/audio/sfx_only.wav', mix[:int(END * SR)], SR, subtype='PCM_24'); print('sfx ok', np.abs(mix).max())
