"""SFX for the Trump midterm / Sensex reel, cued from vo/timeline.json (same cue logic as reel.html).
No music bed (Suraj adds BGM). Sources: earshot bank, Motion Array stamp/pop/crowd/cheer WAVs from Suraj's
library (sfx_src/), plus small synths (car horn, record scratch, coin clink). Writes audio/sfx_only.wav."""
import json, os, sys, glob
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, resample_poly
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(D, '../../engine'))
from earshot_bank import bank
SR = 48000
TL = json.load(open(f'{D}/vo/timeline.json'))
LN = {int(k): v for k, v in TL['lines'].items()}
END = 25.2
def F(s):
    for f in TL['frags']:
        if s.lower() in f['text'].lower(): return f['s']
    raise KeyError(s)
T1 = LN[3][0] - .05; T2 = T1 + .36; T3 = LN[4][0] - .08; T4 = LN[5][0] - .08; T5 = LN[6][0] - .1
mix = np.zeros((int((END + 1.5) * SR), 2), np.float32)
rng = np.random.default_rng(11)

def load(name):
    x, sr = sf.read(f'{D}/sfx_src/{name}', dtype='float32')
    if x.ndim > 1: x = x.mean(1)
    if sr != SR: x = resample_poly(x, SR, sr).astype(np.float32)
    return x / (np.abs(x).max() + 1e-9) * .89
def add(t, x, g=1.0, pan=0.0, align_peak=False):
    if align_peak: t -= int(np.argmax(np.abs(x))) / SR
    i = int(max(0, t) * SR); x = x * g
    l, r = np.sqrt(.5 * (1 - pan)), np.sqrt(.5 * (1 + pan))
    n = min(len(x), len(mix) - i)
    if n > 0: mix[i:i + n, 0] += x[:n] * l; mix[i:i + n, 1] += x[:n] * r
def B(k): x = bank(k); return x / (np.abs(x).max() + 1e-9) * .89
def clink(f, g=.3):
    t = np.arange(int(.45 * SR)) / SR
    return (sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t / d) for m, a, d in
                [(1, 1, .11), (1.48, .6, .08), (2.3, .35, .05), (3.1, .2, .035)]) * np.minimum(1, t / .001) * g).astype(np.float32)
def horn(dur=.32, f=(392, 494)):
    t = np.arange(int(dur * SR)) / SR
    x = sum(np.sign(np.sin(2 * np.pi * fr * t)) for fr in f) / len(f)
    x = sosfilt(butter(4, 2200, 'low', fs=SR, output='sos'), x)
    env = np.minimum(1, t / .01) * np.minimum(1, (dur - t) / .03)
    return (x * env * .5).astype(np.float32)
def scratch(dur=.34):
    """vinyl record scratch: band-passed noise + tone with a fast back-and-forth pitch sweep"""
    n = int(dur * SR); t = np.arange(n) / SR
    sweep = np.abs(np.sin(2 * np.pi * (1 / dur) * 1.5 * t))
    ph = np.cumsum(220 + 900 * sweep) / SR
    tone = np.sin(2 * np.pi * ph) * .5
    nz = sosfilt(butter(2, [700, 5000], 'bandpass', fs=SR, output='sos'), rng.standard_normal(n)) * .6
    x = (tone + nz) * (.3 + .7 * sweep) * np.minimum(1, t / .005) * np.minimum(1, (dur - t) / .02)
    return (x / np.abs(x).max() * .8).astype(np.float32)
def crunch(dur=.25, g=.5):
    """popcorn crunch: a burst of tiny filtered clicks"""
    n = int(dur * SR); x = np.zeros(n, np.float32)
    for _ in range(18):
        i = rng.integers(0, n - 600); k = rng.standard_normal(500) * np.exp(-np.arange(500) / 60)
        x[i:i + 500] += k * rng.uniform(.3, 1)
    x = sosfilt(butter(2, [900, 7000], 'bandpass', fs=SR, output='sos'), x)
    return (x / (np.abs(x).max() + 1e-9) * g).astype(np.float32)

STAMP, STAMP2 = load('MA_Tuttkile_PowerfulApprovalStampHit_1.wav'), load('MA_Tuttkile_PowerfulApprovalStampHit_3.wav')
POPS = [load(os.path.basename(f)) for f in sorted(glob.glob(f'{D}/sfx_src/MA_CineTransitions_BigCasualPop_*.wav'))]
OHNO, GASP, WOW = (load(f'MA_PeopleSFX_AstonishedCrowdReaction_{k}.wav') for k in ('OhNo', 'Gasp', 'Wow'))
CHEER = load('MA_Tuttkile_PeopleCheering_1.wav')

# ---------- S1 hook: news sting, satire tag, popcorn, toss, thud, crowd, bull walk-in
add(0.0, B('pro_logo_sting/sweep_hit'), .35)
add(0.08, POPS[0], .38)                                   # SATIRE tag
add(0.55, crunch(.3), .5, .2); add(1.35, crunch(.25), .45, -.2)
add(2.62, B('whoosh_big/cape'), .45, align_peak=True)    # toss
add(3.05, B('impact/punch'), .55); add(3.07, B('cut_hit/kick'), .35)
add(3.12, OHNO, .32)
bt = F('bull run chalu')
for i in range(4): add(bt - .1 + i * .32, B('ui_pop/step'), .22, -.6)
# ---------- record scratch + rewind
add(T1, scratch(.36), .55); add(T1 + .02, B('downlifter/tape'), .3)
add(T2, B('whoosh_fast/crisp'), .35, align_peak=True); add(T2, B('shutter/snap'), .25)
# ---------- S2 Oval: TV on, stamp, bars
add(T2 + .1, B('pro_pop_in/knock'), .35, -.4)
add(F('Dekho') + .45, STAMP, .5, .3)
for k, dt in ((0, -.1), (1, .35)):
    add(F('bas unki') + dt, B('pro_zip/up'), .25, -.4)
    add(F('bas unki') + dt + .55, B('pro_notify/ding_2045'), .25, -.4)
# ---------- S3 Capitol: whip, horns on BEEP/HONK, sweat, PENDING stamp
add(T3, B('whoosh_fast/whip'), .45, align_peak=True)
ts = np.arange(T3, T4, 1 / 30)
for prev, cur in zip(ts[:-1], ts[1:]):
    if np.sin(cur * 5) > .6 >= np.sin(prev * 5): add(cur, horn(.3), .22, -.5)
    if np.sin(cur * 4 + 2) > .7 >= np.sin(prev * 4 + 2): add(cur, horn(.24, (330, 415)), .2, .5)
add(T3 + .5, B('drip/bloop'), .15, -.4); add(T3 + 1.3, B('drip/bloop'), .12, -.4)
add(F('aasaani se') + .25, STAMP2, .55)
# ---------- S4 studio graphics
f1, f2, f3, f4 = F('Tariff ka darr'), F('crude 8%'), F('aur foreign'), F('Sensex 5')
add(T4, B('whoosh_fast/whip'), .45, align_peak=True)
add(f1, B('pro_pop_in/round'), .3); add(f1 + .2, B('pro_zip/down'), .3)
add(f2, B('pro_pop_in/round'), .3); add(f2 + .15, B('downlifter/air_fall'), .32)
add(f3, B('pro_pop_in/round'), .3); add(f3 + .1, B('whoosh_big/jet'), .3, -.3)
add(f3 + .7, B('pro_notify/ding_2296'), .3); add(f3 + .75, clink(2600, .3), 1, .3); add(f3 + .85, clink(3200, .25), 1, -.3)
add(f4, B('pro_pop_in/round'), .3)
for i in range(5): add(f4 + .1 + i * .32, B('pro_pop/boop'), .22 + i * .02, -.5 + i * .25)
add(F('4,000'), CHEER, .3); add(F('4,000') + .05, B('pro_notify/ding_2167'), .3)
# ---------- S5 bull slip
add(T5, B('whoosh_fast/whip'), .45, align_peak=True)
add(F('Toh kya'), POPS[2], .3)
add(T5 + 1.2, B('whoosh_fast/whistle'), .4)              # slide
add(T5 + 1.65, B('impact/punch'), .6); add(T5 + 1.67, B('cut_hit/rumble'), .35)
add(T5 + 1.72, GASP, .35)
add(F('profit booking') - .05, POPS[1], .38); add(F('profit booking'), B('glitch/burst'), .2)
add(F('aur crude kabhi'), B('pro_pop_in/round'), .3); add(F('aur crude kabhi') + .2, B('riser/tension'), .22)
add(LN[6][1] - .05, B('mallet/glock'), .2)
os.makedirs(f'{D}/audio', exist_ok=True)
sf.write(f'{D}/audio/sfx_only.wav', mix, SR, subtype='PCM_24'); print('sfx ok, peak', float(np.abs(mix).max()))
