"""SFX for the Nexon fuel reel, cued from vo/timeline.json (same keys as reel.html). No bed — Suraj adds BGM.
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

# ---- scene cuts: short whoosh with its peak on the cut
CUTS = [L[2], L[4], L[5], L[6], L[7], L[8], ct('Agar sirf public'), L[9], ct('ghar pe charging'), ct('Highway pe'), ct('Kam chalana'), VOEND]
for i, c in enumerate(CUTS):
    add(c, bank('whoosh_fast/tight'), .2, (-.3, .3)[i % 2], align_peak=True)
# B1 hook
add(0.0, bank('swish/soft'), .25)
add(0.985, STAMP, .62, align_peak=True); add(0.985, bank('cut_hit/sub'), .3, align_peak=True)
# B2 fuel chips
for key, pan, k in [('petrol loon', -.5, 0), ('diesel loon', 0, 1), ('ya EV', .5, 2)]:
    add(ct(key), pop(k), .42, pan)
# B3 calendar + flips + question mark
add(L[3], bank('pro_pop_in/round'), .4)
for k in range(5): add(L[3] + .2 + (k + 1) * 1.6 / 6, bank('click/soft'), .3, .1)
add(ct('rahegi'), bank('pro_pop/chirp'), .35, .2)
# B4 pen strokes
for t0, d in [(ct('Gaadi har'), .7), (ct('1,500'), .5), (ct('1,500') + .55, .5), (ct('1,500') + 1.0, .45)]:
    add(t0, scratch(d), .5, -.2)
# B5 per-km meters
for key, pan, k in [('Petrol ₹9', -.5, 3), ('Diesel ₹5', 0, 1), ('sirf ₹1', .5, 0)]:
    add(ct(key), pop(k), .5, pan)
add(ct('sirf ₹1') + .05, bank('pro_notify/ding_2045'), .3, .5)
# B6 prices stamped on the showroom tags
add(L[6] + .35, bank('pro_tap/knock'), .4, -.5)
add(ct('diesel lagbhag') + .15, STAMP2, .4, 0, align_peak=True)
add(ct('aur EV ₹2.65') + .1, STAMP, .62, .5, align_peak=True); add(ct('aur EV ₹2.65') + .1, bank('cut_hit/sub'), .35)
add(ct('aur EV ₹2.65') + .4, bank('swish/flick'), .18, .5)   # red circle draws
# B7 coin totals (more clinks for the taller stack)
add(L[7] + .1, bank('pro_pop_in/airy'), .3)
for key, pan, nclk in [('Petrol ₹8.5', -.5, 9), ('Diesel ₹5.8', 0, 6), ('EV sirf ₹3.6', .5, 3)]:
    t0 = ct(key); add(t0, pop(2), .4, pan)
    for k in range(nclk): add(t0 + .04 + k * .07, clink(1800 + rng.random() * 1600, .16), 1, pan + rng.uniform(-.15, .15))
add(ct('EV sirf ₹3.6') + .15, bank('pro_shimmer/m3'), .28, .5)
# B8 twist
r = bank('pro_riser/roll', dur=.7); add(L[8] - len(r) / SR, r, .22)
add(L[8], bank('pro_impact/short'), .45)
add(ct('jab EV ghar') + .1, pop(1), .35)
add(ct('Agar sirf public') + .05, bank('pro_glitch/sparse'), .12)
nb = bank('pro_riser/nblips', dur=.7); add(ct('EV ₹5.7'), nb, .28)
add(ct('EV ₹5.7') + .7, bank('pro_impact/air'), .45); add(ct('EV ₹5.7') + .7, bank('glitch/hit'), .12)
add(ct('lagbhag diesel'), bank('pro_pop_in/knock'), .4)
# B9 odometer ticks slow down, red tag drops, strike
t, gap = L[9] + .35, .07
while t < ct('kam chalate') + .4:
    add(t, bank('hover_tick/detent'), .22, .2); t += gap; gap *= 1.08
add(ct('toh EV ka'), bank('swish/soft'), .25, .3); add(ct('toh EV ka') + .35, bank('pro_impact/short'), .38, .3)
add(ct('hi nahi'), bank('swish/blade'), .3, .2)
# B10 rule
add(L[10], bank('mallet/up4'), .25)
for key, k, pitch in [('ghar pe charging', 0, None), ('Highway pe', 3, None), ('Kam chalana', 1, None)]:
    add(ct(key), pop(k), .48); add(ct(key) + .05, bank('mallet/marimba'), .25)
# ending
add(VOEND, bank('pro_shimmer/m2'), .3)
add(VOEND + .2, pop(0), .35)

pk = np.abs(mix).max()
if pk > .89: mix *= .89 / pk
os.makedirs(f'{D}/audio', exist_ok=True)
sf.write(f'{D}/audio/sfx_only.wav', mix[:int(END * SR)], SR, subtype='PCM_24')
print('sfx ok', round(END, 2), 'peak', round(float(np.abs(mix).max()), 3))
