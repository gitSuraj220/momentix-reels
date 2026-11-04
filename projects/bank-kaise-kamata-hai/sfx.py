"""SFX for the bank kamai reel, cued from vo/timeline.json (same keys as reel.html). No bed — Suraj adds BGM.
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
def R(i):
    x = np.sin(i * 127.1 + 311.7) * 43758.5453
    return float(x - np.floor(x))

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

# ---- whip cuts
for i, c in enumerate([L[2], L[4], L[5], L[6], ct('aur ye sirf'), L[7], L[8]]):
    add(c, bank('whoosh_fast/tight'), .26, (-.3, .3)[i % 2], align_peak=True)
# 1 exterior
add(0.05, clink(2400, .25), 1, -.3); add(0.2, clink(3100, .2), 1, .3)
add(ct('Kabhi socha'), pop(0), .35, -.5); add(ct('HDFC'), pop(2), .35, .5)
add(.25, bank('pro_pop_in/round'), .3)
add(ct('paise kaise'), bank('pro_pop_in/knock'), .4)
# 2 counter
for k in range(4): add(L[2] + .05 + k * .22, bank('fit/land.light/finger_wood'), .22, -.4)   # footsteps
g = ct('Aapne bank') + .75; add(g, bank('pro_click/soft'), .35, -.1); add(g + .35, bank('mallet/pluck', pitch=None), .3)  # pen yank boing
add(L[2] + 1.55, bank('glitch/mid'), .12, .3)                      # SERVER DOWN flicker
d = ct('₹1 lakh deposit') + .55; add(d, bank('knock/desk'), .5); add(d + .05, pop(1), .3)
# 3 savings
add(L[3] + .05, bank('click/thock'), .35); add(L[3] + .2, bank('swish/flick'), .2)
for k in range(10): add(L[3] + .5 + k * .12, bank('click/soft'), .12, -.3)     # calendar flips
t0 = ct('yaani sirf')
for k in range(5): add(t0 + k * .24, clink(1700 + k * 90, .14), 1, -.4)
add(t0 + .7, bank('swish/soft'), .2, .3)                                       # banner unroll
add(t0 + .95, bank('pro_pop/boop'), .3, -.3)                                   # itna hi?
# 4 loan
add(L[4] + .2, bank('whoosh_big/thump_airy'), .25, .3)
add(ct('lagbhag 8') - .05, bank('click/thock'), .35)
add(L[4] + 1.3, bank('whoosh_fast/whistle'), .18, .4)                          # form unrolls
g0 = ct('aur kamaata')
for k in range(9): add(g0 + k * .11, clink(2000 + R(k) * 1400, .17), 1, -.2)
# 5 maths
add(L[5], pop(3), .4, -.4); add(ct('₹2,500 aapko'), pop(0), .35, .4)
add(ct('bache'), bank('pro_notify/ding_2045'), .45); add(ct('bache') + .05, bank('pro_shimmer/m3'), .25)
# 6 crore
add(L[6] + .6, bank('pro_pop_in/airy'), .3, .4)                                 # gold mug
for k in range(14): add(ct('Ab crore') + k * .065, bank('hover_tick/detent'), .2, .3)   # token racing
for k in range(12): add(ct('aur ye sirf') + k * .25, clink(1500 + R(k + 3) * 2000, .12), 1, R(k) - .5)
add(ct('ka paisa socho'), bank('pro_impact/short'), .35); add(ct('ka paisa socho') + .05, pop(2), .35)
# 7 card
add(L[7] + .1, bank('whoosh_fast/crisp'), .3); add(L[7] + .5, bank('pro_click/glass'), .35)
add(ct('aur bill time') + .1, bank('swish/soft'), .25)
add(ct('pe nahi bhara') + .4, bank('pro_notify/ding_1930'), .3, -.4)
add(ct('45% saal') - .15, bank('click/thock'), .4)
add(ct('₹45,000') - .05, bank('pro_impact/deep'), .55); add(ct('₹45,000') - .05, bank('cut_hit/sub'), .45)
# 8 end
add(ct('poora bharo'), bank('knock/double'), .5); add(ct('poora bharo') + .02, bank('cut_hit/punch'), .3)
cg = ct('ki sabse moti'); add(cg - .1, bank('pro_pop_in/round'), .35, -.3); add(cg + .15, bank('pro_glitch/sparse'), .1, -.3)
add(cg + 1.0, bank('downlifter/tape', dur=.6), .2, -.2)
add(END - .65, bank('swish/soft'), .2)
pk = np.abs(mix).max()
if pk > .89: mix *= .89 / pk
os.makedirs(f'{D}/audio', exist_ok=True)
sf.write(f'{D}/audio/sfx_only.wav', mix[:int(END * SR)], SR, subtype='PCM_24')
print('sfx ok', round(END, 2), 'peak', round(float(np.abs(mix).max()), 3))
