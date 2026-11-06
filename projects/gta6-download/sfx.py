"""Game-style SFX for the GTA 6 download reel (no music bed; Suraj adds BGM). Cues mirror reel.html timing.
Sources: earshot bank, Motion Array stamp/pop/cheer WAVs (sfx_src/), small synths (clock tick, sizzle, siren, error beep)."""
import json, os, sys, glob
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, resample_poly
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(D, '../../engine'))
from earshot_bank import bank
SR = 48000; END = 32.3
TL = json.load(open(f'{D}/vo/timeline.json'))
LN = {int(k): v for k, v in TL['lines'].items()}
L = {k: LN[k][0] - .08 for k in LN}; L[8] = LN[8][0] - .1; L[2] = LN[2][0] - .1
T_CUT = 4.25
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

# S1: clock ticks to midnight, bell, data streams build, tower sizzles + alarm
for i in range(2): add(i * .45, tick(), .5)
add(.9, B('mallet/glock'), .35); add(.9, B('pro_logo_sting/sweep_hit'), .3)
add(.4, B('riser/build'), .25)
add(2.2, sizzle(2.1), .35); add(3.0, siren(1.2), .14)
add(3.1, B('cut_hit/rumble'), .35)
# cut to Momo: impact + glitch + error beeps
add(T_CUT, B('impact/punch'), .45); add(T_CUT, B('glitch/burst'), .3)
for k in range(3): add(T_CUT + .25 + k * .38, beep(440 if k % 2 else 330, .14), .45, .3)
# data scenes: whip in each, pops, counters
for k in (2, 3, 4, 5, 6): add(L[k], B('whoosh_fast/whip'), .4, align_peak=True)
add(L[2] + .05, POPS[0], .32)
for i in range(14): add(L[2] + .25 + i * .11, tick(), .25)
add(L[2] + .35, B('pro_zip/up'), .25)
add(L[3] + .1, B('pro_zip/up'), .3)
for i in range(10): add(LN[3][0] + 2.0 + i * .16, tick(), .22)
add(LN[3][0] + 3.6, B('pro_notify/ding_2045'), .25)
add(L[4] + .05, POPS[1], .3)
for i in range(9): add(LN[4][0] + 1.6 + i * .1, B('pro_pop/boop'), .14, -.3 + i * .07)
add(LN[4][0] + 2.5, B('cut_hit/kick'), .35)
add(L[5] + .1, siren(3.3, 500, 900, 1.6), .16); add(L[5] + .3, B('cut_hit/rumble'), .35)
for k in range(4): add(L[5] + .6 + k * .9, B('glitch/mid'), .2, (-1) ** k * .4)
add(L[6] + .25, POPS[2], .3, -.4); add(LN[6][0] + 2.6, POPS[0], .3, .4)
add(LN[6][0] + .4, B('pro_notify/ding_2296'), .22)
# preload filling: soft beeps, done ding
add(L[7], B('whoosh_fast/crisp'), .35, align_peak=True)
for i in range(5): add(L[7] + .4 + i * .45, beep(1200, .05), .18)
add(L[7] + 2.65, B('pro_notify/ding_2167'), .3)
# unlock: key whoosh, chunk, burst, sting, cheer
add(L[8] + .3, B('whoosh_fast/whistle'), .3)
add(L[8] + 2.3, STAMP, .35); add(L[8] + 2.45, B('pro_logo_sting/sweep_hit'), .45); add(L[8] + 2.45, B('impact/punch'), .35)
add(L[8] + 2.9, CHEER, .25)
os.makedirs(f'{D}/audio', exist_ok=True)
sf.write(f'{D}/audio/sfx_only.wav', mix, SR, subtype='PCM_24'); print('sfx ok, peak', float(np.abs(mix).max()))
