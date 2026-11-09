"""SFX for ChatGPT 5 codes reel (no music; Suraj adds BGM). Cues mirror reel.html."""
import os, sys
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(D, '../../engine'))
from earshot_bank import bank
SR = 48000; END = 35.6; rng = np.random.default_rng(9)
mix = np.zeros((int((END + 1.5) * SR), 2), np.float32)
def norm(x): return (x / (np.abs(x).max() + 1e-9) * .89).astype(np.float32)
def B(k): return norm(bank(k))
def add(t, x, g=1.0, pan=0.0, peak=False):
    if peak: t -= int(np.argmax(np.abs(x))) / SR
    i = int(max(0, t) * SR); l, r = np.sqrt(.5 * (1 - pan)), np.sqrt(.5 * (1 + pan)); n = min(len(x), len(mix) - i)
    if n > 0: mix[i:i + n, 0] += x[:n] * g * l; mix[i:i + n, 1] += x[:n] * g * r
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
def scribble(d):
    n = int(d * SR); t = np.arange(n) / SR; m = np.abs(np.sin(2 * np.pi * 9 * t)) ** 1.5
    return norm(bp(rng.standard_normal(n), 1800, 6500) * (.35 + .65 * m) * np.minimum(1, t / .03) * np.minimum(1, (d - t) / .05))
def gulp():  # comic nervous gulp: quick downward pitch blip
    t = np.arange(int(.22 * SR)) / SR; f = 520 * np.exp(-t * 6)
    return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .07) * np.minimum(1, t / .004))
KEYS = [B('fit/key/thock') if False else None]
def key():
    n = int(.05 * SR); t = np.arange(n) / SR
    return norm(bp(rng.standard_normal(n), 2000, 8000) * np.exp(-t / .008) + .4 * bp(rng.standard_normal(n), 300, 900) * np.exp(-t / .012))
POP = B('pro_pop/boop'); TINK = B('pro_pop/tink'); SW = B('swipe/paper'); WF = B('whoosh_fast/crisp')
# hook: pencil scribble, nervous gulp, comic sting, title pops
add(0.0, scribble(2.2), .35, -.3); add(2.3, scribble(1.6), .25, .3)
add(.15, POP, .5); add(2.54, B('cut_hit/punch'), .55); add(3.0, gulp(), .5, .4); add(4.1, TINK, .35)
add(4.57, WF, .55)                                   # into phone
C = [(4.57, 7.58, 11.36, 5), (11.36, 13.56, 16.79, 7), (16.79, 19.08, 22.84, 8), (22.84, 25.24, 28.35, 11), (28.35, 30.40, 34.37, 9)]
for t0, td, te, nk in C:
    add(t0, B('cut_hit/kick'), .45); add(t0 + .02, POP, .4)
    for j in range(nk): add(t0 + .15 + j * .07, key(), .22, .1)           # typing the code
    add(t0 + .75, TINK, .35)        # message sent
    for j in range(6): add(td + .15 + j * .13, key(), .08, -.1)          # answer streaming ticks
add(34.6, B('pro_notify/ding_2045'), .35)
os.makedirs(f'{D}/audio', exist_ok=True)
sf.write(f'{D}/audio/sfx_only.wav', mix[:int(END * SR)], SR, subtype='PCM_24'); print('sfx ok', np.abs(mix).max())
