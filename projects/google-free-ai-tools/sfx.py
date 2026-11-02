"""SFX for the Google free AI tools reel, cued from vo/timeline.json (same keys as reel.html). No bed — Suraj adds BGM.
Sources: earshot bank + Motion Array stamp/pop SFX from Suraj's library (sfx_src/). Writes audio/sfx_only.wav."""
import json, os, sys, glob
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, resample_poly
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(D, '../../engine'))
from earshot_bank import bank
SR = 48000
TL = json.load(open(f'{D}/vo/timeline.json'))
L = {int(k): v[0] for k, v in TL['lines'].items()}
END = TL['end']; VOEND = TL['frags'][-1]['e']
def ct(s):
    for c in TL['chunks']:
        if s.lower() in c['text'].lower(): return c['t']
    raise KeyError(s)
mix = np.zeros((int((END + 1.5) * SR), 2), np.float32)

def load(name):
    x, sr = sf.read(f'{D}/sfx_src/{name}', dtype='float32')
    if x.ndim > 1: x = x.mean(1)
    if sr != SR: x = resample_poly(x, SR, sr).astype(np.float32)
    return x / (np.abs(x).max() + 1e-9) * .89

def add(t, x, g=1.0, pan=0.0, align_peak=False):
    if align_peak: t -= int(np.argmax(np.abs(x))) / SR
    i = int(max(0, t) * SR); x = x * g
    l, r = np.sqrt(0.5 * (1 - pan)), np.sqrt(0.5 * (1 + pan))
    n = min(len(x), len(mix) - i)
    if n > 0: mix[i:i + n, 0] += x[:n] * l; mix[i:i + n, 1] += x[:n] * r

rng = np.random.default_rng(7)
def clink(f, g=.3):
    t = np.arange(int(.45 * SR)) / SR
    return (sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t / d) for m, a, d in
                [(1, 1, .11), (1.48, .6, .08), (2.3, .35, .05), (3.1, .2, .035)]) * np.minimum(1, t / .001) * g).astype(np.float32)
def scratch(dur, g=.25):  # pen on paper: band-passed noise with stroke modulation
    n = int(dur * SR); x = rng.standard_normal(n).astype(np.float32)
    x = sosfilt(butter(2, [1800, 6500], 'bandpass', fs=SR, output='sos'), x)
    t = np.arange(n) / SR; env = (.55 + .45 * np.sin(2 * np.pi * 7.5 * t + rng.random() * 6)) ** 2
    env *= np.minimum(1, t / .03) * np.minimum(1, (dur - t) / .06)
    return (x * env / (np.abs(x).max() + 1e-9) * g).astype(np.float32)

STAMP, STAMP2 = load('MA_Tuttkile_PowerfulApprovalStampHit_1.wav'), load('MA_Tuttkile_PowerfulApprovalStampHit_3.wav')
POPS = [load(os.path.basename(f)) for f in sorted(glob.glob(f'{D}/sfx_src/MA_CineTransitions_BigCasualPop_*.wav'))]
pop = lambda i: POPS[i % len(POPS)]

# ---- cuts (blur-whips): whoosh peak on each scene change
for i, c in enumerate([L[2], L[3], L[4], ct('prompt se poora'), L[5], L[6], L[7]]):
    add(c, bank('whoosh_fast/tight'), .28, (-.3, .3)[i % 2], align_peak=True)
# 1 hook
add(0.05, pop(0), .45, -.4); add(0.35, pop(2), .45, .4)
for k in range(10): add(1.3 + k * .07, bank('ui_pop/blip'), .12, rng.uniform(-.6, .6))
add(ct('par Google'), bank('pro_impact/short'), .55); add(ct('par Google'), bank('cut_hit/sub'), .4)
add(ct('par Google') + .05, bank('swish/soft'), .2)
for k in range(10): add(ct('chupchaap') + k * .1, bank('pro_pop/tink'), .22, -.6 + k * .13)
add(ct('10 free AI'), bank('pro_pop_in/round'), .45)
add(.3, bank('pro_pop_in/airy'), .25, -.6)              # Momo badge
# 2 Antigravity
add(L[2] + .1, bank('pro_shimmer/m3'), .2)
add(ct('Cursor jaisa'), pop(1), .35, .5)
t0 = L[2] + .9; r = bank('pro_typing_run/soft'); add(t0, r, .3); add(t0 + len(r) / SR, bank('pro_typing_run/soft'), .25)
add(ct('poori app'), bank('pro_notify/ding_2045'), .4)
# 3 AI Studio
add(L[3] + .3, bank('pro_typing_run/soft'), .25)
add(ct('seconds mein') - .1, bank('pro_click/soft'), .4); add(ct('seconds mein') + .4, pop(3), .4)
# 4 Stitch
add(L[4] + .1, bank('pro_pop_in/round'), .35)
for k in range(3): add(ct('prompt se poora') + .1 + k * .12, bank('swish/flick'), .22, -.4 + k * .4)
add(ct('code.'), bank('pro_click/mouse'), .5); add(ct('code.') + .08, pop(0), .3)
# 5 Opal
add(L[5] + .1, bank('swish/soft'), .22, -.5); add(L[5] + .2, bank('swish/soft'), .22, .5)
add(ct('ka combo'), bank('pro_logo_sting/zap_bloom'), .35)
for k in range(4): add(ct('ka combo') + .3 + k * .22, bank('pro_pop/tink'), .2)
add(ct('bina code'), pop(2), .4, .3)
# 6 carousel + counter
add(L[6], bank('whoosh_big/jet'), .25)
for k in range(8): add(L[6] + .2 + k * .2, bank('hover_tick/detent'), .3)
add(ct('4 hain'), bank('pro_impact/short'), .4)
# 7 CTA
add(L[7], bank('pro_pop_in/round'), .5); add(L[7] + .05, bank('pro_pop_in/airy'), .3, -.6)
add(ct('Comment karo'), bank('pro_notify/ding_2045'), .4)
for k in range(5): add(ct('Comment karo') + .9 + k * .6, bank('pro_pop/boop'), .12)
pk = np.abs(mix).max()
if pk > .89: mix *= .89 / pk
os.makedirs(f'{D}/audio', exist_ok=True)
sf.write(f'{D}/audio/sfx_only.wav', mix[:int(END * SR)], SR, subtype='PCM_24')
print('sfx ok', round(END, 2), 'peak', round(float(np.abs(mix).max()), 3))
