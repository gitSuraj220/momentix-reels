"""SFX for the Buy vs Rent reel (no music bed; Suraj adds BGM). Cues mirror reel.html timing.
Sources: earshot bank, Motion Array stamp/pop/cheer WAVs (sfx_src/), small synths (clock tick, sizzle, siren, error beep)."""
import json, os, sys, glob
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, resample_poly
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(D, '../../engine'))
from earshot_bank import bank
SR = 48000; END = 43.8
TL = json.load(open(f'{D}/vo/timeline.json'))
LN = {int(k): v for k, v in TL['lines'].items()}
L = {k: LN[k][0] for k in LN}
mix = np.zeros((int((END + 1.5) * SR), 2), np.float32); rng = np.random.default_rng(7)
def load(name):
    x, sr = sf.read(f'{D}/sfx_src/{name}', dtype='float32')
    if x.ndim > 1: x = x.mean(1)
    if sr != SR: x = resample_poly(x, SR, sr).astype(np.float32)
    return x / (np.abs(x).max() + 1e-9) * .89
def add(t, x, g=1.0, pan=0.0, align_peak=False):
    if align_peak: t -= int(np.argmax(np.abs(x))) / SR
    i = int(max(0, t) * SR); x = x * g; l, r = np.sqrt(.5 * (1 - pan)), np.sqrt(.5 * (1 + pan))
    n = min(len(x), len(mix) - i)
    if n > 0: mix[i:i + n, 0] += x[:n] * l; mix[i:i + n, 1] += x[:n] * r
def B(k): x = bank(k); return x / (np.abs(x).max() + 1e-9) * .89
def env(n, a=.005, r=.05):
    t = np.arange(n) / SR; d = n / SR
    return np.minimum(1, t / a) * np.minimum(1, np.maximum(0, (d - t) / r))
def tick():
    n = int(.04 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 2400 * t) * np.exp(-t / .006) * .6).astype(np.float32)
def beep(f=880, d=.12):
    n = int(d * SR); t = np.arange(n) / SR
    return (np.sign(np.sin(2 * np.pi * f * t)) * .25 * env(n, .003, .02)).astype(np.float32)
def sizzle(d=1.8):
    n = int(d * SR); x = sosfilt(butter(2, 3000, 'high', fs=SR, output='sos'), rng.standard_normal(n))
    crack = (rng.random(n) > .9993) * rng.uniform(-3, 3, n)
    x = (x * .25 + sosfilt(butter(2, 1500, 'high', fs=SR, output='sos'), crack)) * np.linspace(.2, 1, n) * env(n, .2, .3)
    return (x / np.abs(x).max() * .7).astype(np.float32)
def siren(d=1.6, lo=650, hi=1150, rate=2.2):
    n = int(d * SR); t = np.arange(n) / SR
    f = lo + (hi - lo) * (.5 + .5 * np.sin(2 * np.pi * rate * t)); ph = np.cumsum(f) / SR
    x = sosfilt(butter(2, 3500, 'low', fs=SR, output='sos'), np.sign(np.sin(2 * np.pi * ph)))
    return (x * .35 * env(n, .05, .2)).astype(np.float32)
STAMP = load('MA_Tuttkile_PowerfulApprovalStampHit_1.wav')
POPS = [load(os.path.basename(f)) for f in sorted(glob.glob(f'{D}/sfx_src/MA_CineTransitions_BigCasualPop_*.wav'))]
CHEER = load('MA_Tuttkile_PeopleCheering_1.wav')
def F(s):
    lines = {int(k): v for k, v in TL['lines'].items()}
    fr = []
    by = {}
    for f in TL['frags']: by.setdefault(f['line'], []).append(f)
    for k, fs in by.items():
        a, b = lines[int(k)]; tot = sum(len(f['text']) for f in fs); t = a
        for f in fs: d = (b - a) * len(f['text']) / tot; fr.append((t, f['text'])); t += d
    for t, txt in fr:
        if s.lower() in txt.lower(): return t
    raise KeyError(s)
def clink(f, g=.3):
    t = np.arange(int(.4 * SR)) / SR
    return (sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t / d) for m, a, d in [(1, 1, .1), (1.48, .6, .07), (2.3, .35, .05)]) * g).astype(np.float32)
def keys():
    x = np.zeros(int(.6 * SR), np.float32)
    for i in range(7):
        c = clink(rng.uniform(2800, 5200), .25); o = int(rng.uniform(0, .35) * SR); x[o:o + len(c)] += c[:len(x) - o]
    return x
def gurgle(d):
    n = int(d * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for k in range(int(d * 9)):
        c = int(rng.uniform(0, d - .15) * SR); m = int(.08 * SR); tt = np.arange(m) / SR; f = rng.uniform(300, 700)
        x[c:c + m] += np.sin(2 * np.pi * (f + 2500 * tt) * tt) * np.exp(-tt / .03)
    return (x / (np.abs(x).max() + 1e-9) * .6).astype(np.float32)
# L1
add(.1, POPS[0], .3); add(.3, keys(), .5, -.3); add(1.1, keys(), .4, -.3)
# L2
add(L[2] + .1, POPS[1], .3); add(F('jisme') , B('pro_pop/boop'), .25); add(F('upar se'), B('pro_pop/boop'), .25)
add(F('So total'), B('pro_notify/ding_2296'), .3); add(F('So total') + .05, clink(2600, .35), 1); add(F('So total') + .15, clink(3300, .3), 1)
# L3: whoosh, drain gurgle + coin drips, interest hit
add(L[3] - .05, B('whoosh_fast/whip'), .4, align_peak=True)
add(L[3] + .3, gurgle(L[4] - L[3] - .4), .18, .5)
for i in range(10): add(L[3] + .5 + i * .5, clink(2100 + 200 * (i % 3), .2), 1, .6)
add(F('Matlab ₹64'), B('cut_hit/kick'), .4); add(F('Matlab ₹64') + .02, STAMP, .3)
# L4: rent chip, coins into SIP pot
add(L[4] - .05, B('whoosh_fast/crisp'), .35, align_peak=True); add(L[4] + .1, POPS[2], .3)
for i in range(8): add(F('aur bacha') + i * .55, clink(3000 + 150 * (i % 4), .22), 1, .3)
# L5: race
add(L[5] - .05, B('riser/build'), .25)
for i in range(20): add(L[5] + .2 + 3.8 * ((i / 20) ** .5) * 0 + i * .19, B('pro_pop/boop'), .12 + .006 * i, -.4 + .04 * i)
add(L[5] + 4.0, B('pro_logo_sting/sweep_hit'), .35); add(L[5] + 4.05, CHEER, .22)
# L6: streak ticks, discipline stamp
for i in range(24): add(L[6] + .2 + i * .19, B('ui_pop/step'), .12, .3)
add(F('Market upar'), B('whoosh_fast/whistle'), .2)
add(F('isliye SIP') - .1, STAMP, .4)
# L7: verdict
add(L[7] - .05, B('cut_hit/rumble'), .3); add(L[7] + .1, POPS[0], .3); add(F('agar discipline'), B('pro_notify/ding_2045'), .25)
os.makedirs(f'{D}/audio', exist_ok=True)
sf.write(f'{D}/audio/sfx_only.wav', mix, SR, subtype='PCM_24'); print('sfx ok, peak', float(np.abs(mix).max()))
