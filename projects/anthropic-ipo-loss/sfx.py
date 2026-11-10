"""SFX for the Anthropic IPO reel (no music; Suraj adds BGM). Cues mirror the cut/text times in reel.html.
Hand-synth (numpy/scipy) because the earshot bank could not be installed in the build session."""
import os
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
D = os.path.dirname(os.path.abspath(__file__))
SR = 48000; END = 58.6; rng = np.random.default_rng(11)
mix = np.zeros((int((END + 2) * SR), 2), np.float32)
T = lambda d: np.arange(int(d * SR)) / SR
def norm(x): return (x / (np.abs(x).max() + 1e-9) * .89).astype(np.float32)
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
def lp(x, f): return sosfilt(butter(2, f, 'low', fs=SR, output='sos'), x)
def fade(x, a=.004, r=.03):
    n = len(x); t = np.arange(n) / SR; return x * np.minimum(1, t / a) * np.minimum(1, (n / SR - t) / r)
def add(t, x, g=1.0, pan=0.0):
    i = int(max(0, t) * SR); l, r = np.sqrt(.5 * (1 - pan)), np.sqrt(.5 * (1 + pan)); n = min(len(x), len(mix) - i)
    if n > 0: mix[i:i + n, 0] += x[:n] * g * l; mix[i:i + n, 1] += x[:n] * g * r
def whoosh(d=.38, lo=500, hi=5000):          # swept band-passed noise, peak in the middle
    t = T(d); nz = rng.standard_normal(len(t)); out = np.zeros(len(t)); k = 480
    for i in range(0, len(t), k):
        f = lo + (hi - lo) * np.sin(np.pi * i / len(t)) ** 2
        out[i:i + k] = bp(nz[i:i + k + 0], f * .6, min(f * 1.7, 20000))[:len(out[i:i + k])]
    return norm(fade(out * np.sin(np.pi * t / d) ** 1.5, .02, .05))
def impact(f=58, d=.7):                      # sub drop + short noise crack
    t = T(d); fr = f * (1 + 2.2 * np.exp(-t * 28))
    return norm(np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / .22) + .5 * lp(rng.standard_normal(len(t)), 2500) * np.exp(-t / .035))
def punch(): return impact(95, .28)
def pop(f=880):
    t = T(.16); fr = f * np.exp(-t * 16) + f * .45
    return norm(np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / .045) * np.minimum(1, t / .002))
def tink(f=2637):
    t = T(.7); return norm(sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t / dd) for m, a, dd in [(1, 1, .28), (1.5, .45, .2), (2.01, .25, .14)]) * np.minimum(1, t / .002))
def ding(): return norm(np.concatenate([tink(1568)[:int(.09 * SR)], tink(2093)]))
def register():                              # cash register "ka-ching"
    t = T(.95); thunk = bp(rng.standard_normal(len(t)), 120, 900) * np.exp(-t / .03)
    bell = sum(a * np.sin(2 * np.pi * f * t) for f, a in [(2093, 1), (2637, .6), (4186, .3)]) * np.exp(-np.maximum(0, t - .09) / .35) * (t > .09)
    return norm(.7 * thunk + .5 * bell)
def glitch(d=.4):
    t = T(d); out = np.zeros(len(t)); i = 0
    while i < len(t):
        n = int(rng.uniform(.012, .05) * SR); f = rng.choice([110, 220, 440, 880, 1760, 3520])
        seg = np.sign(np.sin(2 * np.pi * f * t[:n])) * rng.uniform(.3, 1) if rng.random() > .25 else rng.standard_normal(n) * .7
        out[i:i + n] = seg[:len(out[i:i + n])] * (rng.random() > .2); i += n
    return norm(fade(lp(out, 7000), .002, .03))
def stamp():
    t = T(.3); return norm(np.sin(2 * np.pi * np.cumsum(140 * np.exp(-t * 30) + 60) / SR) * np.exp(-t / .07) + .7 * bp(rng.standard_normal(len(t)), 300, 3000) * np.exp(-t / .02))
def paper(d=.5):                             # paper flutter: amplitude-modulated bright noise
    t = T(d); return norm(fade(bp(rng.standard_normal(len(t)), 1800, 9000) * (.5 + .5 * np.sin(2 * np.pi * 17 * t + rng.uniform(0, 6))) ** 2 * np.sin(np.pi * t / d), .01, .05))
def ticks(d, f0=1200, f1=2400, n=9):         # counting-up ticks
    out = np.zeros(int(d * SR) + int(.1 * SR))
    for k in range(n):
        tk = T(.05); x = np.sin(2 * np.pi * (f0 + (f1 - f0) * k / n) * tk) * np.exp(-tk / .012); i = int(d * (k / n) ** .8 * SR); out[i:i + len(x)] += x
    return norm(out)
def riser(d=.9):
    t = T(d); f = 200 * (4 ** (t / d)); return norm(fade((np.sin(2 * np.pi * np.cumsum(f) / SR) * .5 + bp(rng.standard_normal(len(t)), 800, 6000) * .5) * (t / d) ** 2, .02, .02))
def alarm():
    t = T(.16); return norm(fade(np.sign(np.sin(2 * np.pi * 1320 * t)) * .5 + np.sin(2 * np.pi * 660 * t) * .5, .004, .02))
def failtone():
    t = T(.7); f = 330 * np.exp(-t * 1.1); return norm(fade(np.sin(2 * np.pi * np.cumsum(f) / SR) + .4 * np.sin(2 * np.pi * np.cumsum(f * 1.5) / SR), .01, .15))
def shimmer():
    t = T(1.4); return norm(fade(sum(np.sin(2 * np.pi * f * t + rng.uniform(0, 6)) * np.exp(-t / .5) for f in [1568, 2093, 2637, 3136, 4186]), .05, .4))

W = whoosh; CUTS = [3.75, 8.3, 11.85, 14.6, 18.35, 21.55, 26.55, 28.9, 33.45, 37.3, 41.3, 44.8, 47.1, 52.25]
for i, c in enumerate(CUTS): add(c - .14, W(), .42, (-.3, .3)[i % 2])
for c in [23.6, 30.75, 35.1, 39.85, 51.3, 53.85]: add(c, punch(), .4)
# line 1 — profit, then the $66B slam
add(0.02, impact(), .55); add(.1, pop(), .35); add(1.55, stamp(), .5); add(2.2, register(), .6); add(2.25, tink(), .3, .3)
add(3.75, impact(48, .9), .7); add(3.95, pop(660), .3); add(5.0, riser(.25), .3); add(5.25, glitch(.5), .5); add(5.25, impact(44, 1.0), .75); add(6.75, stamp(), .55)
# line 2 — Anthropic, IPO filing
add(8.45, pop(), .3); add(8.75, stamp(), .45); add(8.95, tink(2093), .3, -.2); add(10.1, pop(1040), .35)
add(12.0, pop(), .3); add(13.05, stamp(), .7); add(13.05, impact(70, .5), .45); add(13.1, ding(), .3, .2)
# line 3 — revenue jump
add(14.8, pop(), .3); add(16.2, ticks(1.05), .4); add(17.3, register(), .6); add(16.2, impact(64, .5), .4)
add(18.5, pop(), .35); add(19.6, pop(700), .35); add(20.3, W(.25, 900, 6000), .3); add(20.55, register(), .6); add(20.95, tink(3136), .35, .3)
# line 4 — $8 on every $100
add(21.75, pop(), .3); add(22.6, tink(2637), .22, .3); add(23.75, register(), .65); add(24.5, ticks(.7, 900, 1500, 8), .3); add(25.8, stamp(), .65); add(25.82, ding(), .35)
# line 5 — the paper loss
add(26.55, impact(46, .9), .7); add(26.7, glitch(.35), .4); add(29.2, pop(), .3); add(29.45, paper(.45), .45); add(29.45, stamp(), .4)
add(30.95, pop(1040), .35); add(31.6, paper(.5), .3, .3); add(33.65, riser(1.3), .35); add(35.25, glitch(.4), .45); add(35.25, impact(46, .9), .65)
# line 6 — non-cash
for k, tt in enumerate(np.arange(37.35, 41.1, .42)): add(tt, paper(.5), .3, (-.5, .5, 0)[k % 3])
add(37.6, ding(), .45); add(39.95, stamp(), .6); add(39.95, impact(60, .5), .45); add(40.3, pop(), .25)
# line 7 — $17B, then the gauge
add(41.6, pop(), .3)
for k in range(5): add(41.9 + k * .26, pop(520 + k * 90), .28, -.3 + k * .15)
add(43.3, ticks(.85), .4); add(44.2, register(), .6)
add(44.8, impact(50, .8), .6)
for tt in np.arange(45.0, 47.0, .35): add(tt, alarm(), .26)
add(46.0, failtone(), .4)
# line 8 — the lesson
add(47.6, paper(.4), .4); add(47.6, stamp(), .45); add(48.6, glitch(.2), .2); add(51.4, impact(52, .8), .65); add(51.4, stamp(), .5)
add(52.45, pop(), .35); add(54.0, stamp(), .55); add(54.05, ding(), .4, -.2); add(55.85, stamp(), .55); add(55.9, ding(), .4, .2); add(57.2, shimmer(), .3)
os.makedirs(f'{D}/audio', exist_ok=True)
sf.write(f'{D}/audio/sfx_only.wav', mix[:int(END * SR)], SR, subtype='PCM_24'); print('sfx ok, peak', float(np.abs(mix).max()))
