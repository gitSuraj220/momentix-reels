"""Paper-collage SFX for the FD-se-zyada video (no music; Suraj adds BGM). Cue times mirror reel.html.
Sources: earshot bank, Motion Array stamp hit (../buy-vs-rent/sfx_src), small synths (pen scribble, tape rip, coin clink)."""
import os, sys
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, resample_poly
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(D, '../../engine'))
from earshot_bank import bank
SR = 48000; END = 40.0
mix = np.zeros((int((END + 1.5) * SR), 2), np.float32); rng = np.random.default_rng(11)
def norm(x): return (x / (np.abs(x).max() + 1e-9) * .89).astype(np.float32)
def B(k, **kw): return norm(bank(k, **kw))
def load(p):
    x, sr = sf.read(p, dtype='float32'); x = x.mean(1) if x.ndim > 1 else x
    return norm(resample_poly(x, SR, sr) if sr != SR else x)
def add(t, x, g=1.0, pan=0.0, peak=False):
    if peak: t -= int(np.argmax(np.abs(x))) / SR
    i = int(max(0, t) * SR); l, r = np.sqrt(.5 * (1 - pan)), np.sqrt(.5 * (1 + pan)); n = min(len(x), len(mix) - i)
    if n > 0: mix[i:i + n, 0] += x[:n] * g * l; mix[i:i + n, 1] += x[:n] * g * r
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
def scribble(d):
    n = int(d * SR); t = np.arange(n) / SR
    rate = 7 + rng.uniform(-1, 2); m = np.abs(np.sin(2 * np.pi * rate * t + rng.uniform(0, 3))) ** 1.5
    x = bp(rng.standard_normal(n), 1800, 6500) * (.35 + .65 * m)
    e = np.minimum(1, t / .03) * np.minimum(1, (d - t) / .05)
    return norm(x * e)
def tape(d=.32):
    n = int(d * SR); t = np.arange(n) / SR
    crack = (rng.random(n) > .985) * rng.uniform(-1, 1, n)
    x = bp(rng.standard_normal(n) * .4 + crack * 3, 900, 9000) * np.minimum(1, t / .02) * np.exp(-np.maximum(0, t - d * .8) / .02)
    return norm(x)
def clink(f0=None, g=1.0):
    n = int(.35 * SR); t = np.arange(n) / SR; f0 = f0 or rng.uniform(1900, 2600)
    x = sum(a * np.sin(2 * np.pi * f0 * k * t) * np.exp(-t / dcy) for k, a, dcy in [(1, 1, .09), (1.63, .6, .06), (2.71, .45, .04), (3.9, .25, .03)])
    return norm(x * np.minimum(1, t / .001)) * g
def slapfx():
    n = int(.12 * SR); t = np.arange(n) / SR
    body = sosfilt(butter(2, 1400, 'low', fs=SR, output='sos'), rng.standard_normal(n)) * np.exp(-t / .018)
    k = B('pro_pop_in/knock'); out = np.zeros(max(n, len(k)), np.float32); out[:n] += norm(body); out[:len(k)] += k * .6
    return norm(out)
STAMP = load(f'{D}/../buy-vs-rent/sfx_src/MA_Tuttkile_PowerfulApprovalStampHit_1.wav')
SWIPE = B('swipe/paper'); POP = B('pro_pop/boop'); DING = B('pro_notify/ding_2045'); BUB = B('drip/bubble'); STEP = B('ui_pop/step')

# landings (paper slaps)
for t0, pan in [(.15, -.4), (.45, -.6), (1.75, .1), (2.05, .2), (2.35, .3), (4.85, -.5), (5.6, 0), (10.45, -.1), (12.55, .2), (14.5, -.5),
                (15.3, 0), (21.6, 0), (23.8, .2), (25.95, -.5), (27.3, -.1), (28.7, .3), (34.05, -.4), (38.55, -.5), (38.75, 0), (38.95, .4)]:
    add(t0, slapfx(), .75, pan)
# pen / marker writing
for t0, d in [(.05, .75), (.85, .35), (6.7, .55), (7.35, .45), (8.2, .6), (17.9, .55), (18.55, .4), (19.55, .4), (22.55, .6),
              (28.0, .6), (30.1, .55), (30.75, .35), (35.9, .7), (2.75, .6)]:
    add(t0, scribble(d), .38, -.1)
for t0 in (2.7, 37.35): add(t0, scribble(.45), .3, .1)          # highlighter swipe
for t0 in (5.05, 14.7, 26.15): add(t0, tape(), .45, -.3)        # tape strips
for t0 in (11.35, 13.25, 16.25, 22.2): add(t0, STAMP, .9, 0, peak=True)
add(13.4, DING, .35, .2)
for t0 in (9.5, 19.3, 32.6): add(t0, POP, .5)
for t0 in (4.67, 14.33, 25.75, 38.4): add(t0, SWIPE, .6, 0, peak=True)
for i, t0 in enumerate(np.arange(.9, 1.5, .09)): add(t0, clink(1500 + i * 70, .5), .5, -.3)   # chained lock rattle
for i in range(5): add(5.65 + i * .05, clink(), .35, .1)                                     # coins in glass
for t0 in np.arange(6.1, 14.2, .9): add(t0 + rng.uniform(0, .3), BUB, .12, .15)
for i in range(5):                                                                            # rent coins land in wallet
    for k in range(8):
        ta = 28.7 + i * .22 + .95 * 1.6 + k * 1.6
        if ta < 38.4: add(ta, clink(rng.uniform(2200, 2900)), .18, .4)
for t0 in np.arange(27.6, 29.0, .12): add(t0, clink(4200, .3), .05, -.1)                    # windows lighting
add(32.3, STEP, .5); add(24.2, B('whoosh_fast/crisp'), .35, .3, peak=False)
for t0 in (1.7, 4.8, 13.2, 14.5, 23.8, 25.9, 35.8): add(t0, B('pro_pop/tink'), .22, .6)       # Momo pose pops
add(39.2, DING, .3)
os.makedirs(f'{D}/audio', exist_ok=True)
sf.write(f'{D}/audio/sfx_only.wav', mix[:int(END * SR)], SR, subtype='PCM_24'); print('sfx ok', np.abs(mix).max())
