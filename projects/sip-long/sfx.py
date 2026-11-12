"""SFX for SIP long video (medium density, no music; Suraj adds BGM). Times from timeline.json."""
import os, sys
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(D, '../../engine'))
from earshot_bank import bank
import json
TJ = json.load(open(os.path.join(D, 'timeline.json'))); TL, CU = TJ['TL'], TJ['CUE']
SR = 48000; END = TJ['END']; rng = np.random.default_rng(7)
mix = np.zeros((int((END + 1.5) * SR), 2), np.float32)
def norm(x): return (x / (np.abs(x).max() + 1e-9) * .89).astype(np.float32)
def B(k, **kw): return norm(bank(k, **kw))
def add(t, x, g=1.0, pan=0.0):
    i = int(max(0, t) * SR); l, r = np.sqrt(.5 * (1 - pan)), np.sqrt(.5 * (1 + pan)); n = min(len(x), len(mix) - i)
    if n > 0: mix[i:i + n, 0] += x[:n] * g * l; mix[i:i + n, 1] += x[:n] * g * r
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
def register():
    t = np.arange(int(.9 * SR)) / SR
    thunk = bp(rng.standard_normal(len(t)), 120, 900) * np.exp(-t / .03)
    bell = sum(a * np.sin(2 * np.pi * f * t) for f, a in [(2093, 1), (2637, .6), (4186, .3)]) * np.exp(-np.maximum(0, t - .09) / .35) * (t > .09)
    return norm(.7 * thunk + .5 * bell)
def ring():   # old phone bell ring, two short bursts
    t = np.arange(int(1.1 * SR)) / SR; g = ((t % .5) < .32) * (np.sin(2 * np.pi * 22 * t) > 0)
    x = (np.sin(2 * np.pi * 1280 * t) + .6 * np.sin(2 * np.pi * 1660 * t)) * g * np.exp(-t / .9)
    return norm(bp(x, 600, 5000))
def hum(d):   # server-room air + fan hum
    t = np.arange(int(d * SR)) / SR; x = bp(rng.standard_normal(len(t)), 200, 3000) * .5 + .3 * np.sin(2 * np.pi * 120 * t)
    e = np.minimum(1, t / .6) * np.minimum(1, (d - t) / .6); return norm(x * e)
POP = B('pro_pop/boop'); TINK = B('pro_pop/tink'); SW = B('swipe/paper'); WF = B('whoosh_fast/crisp')
PUNCH = B('impact/punch'); _f = int(.6 * SR); PUNCH = PUNCH[:_f] * np.r_[np.ones(_f - int(.25 * SR)), np.linspace(1, 0, int(.25 * SR))].astype(np.float32); SUB = B('cut_hit/sub'); KICK = B('cut_hit/kick'); GL = B('glitch/hit'); STEP = B('ui_pop/step'); DING = B('pro_notify/ding_2045')
def S(k): return TL[k][0]
def Q(sc, k): return TL[sc][0] + CU[k]
# scene transitions: whoosh on every scene start (not on app sub-steps)
for k in TL:
    if k in ('hook',): continue
    if k in ('st2', 'st3', 'st4', 'st5', 'st6'): add(S(k) + .02, SW, .35, .3); continue
    add(S(k) - .12, WF, .45)
# hook
add(.25, SUB, .5); add(.3, POP, .4)
for i in range(8): add(1.4 + i * .1, STEP, .12, (i % 2 - .5))
add(Q('hook', 'h_chalu'), POP, .45, -.4); add(Q('hook', 'h_samajh'), POP, .45, .4); add(Q('hook', 'h_ye'), PUNCH, .5); add(Q('hook', 'h_doubt'), POP, .45); add(Q('hook', 'h_doubt') + .6, DING, .4)
# SIP letters + flow
for i in range(3): add(S('sipdef') + .3 + i * .35, POP, .35, (i - 1) * .3)
add(Q('sipdef', 'd_har') - .3, TINK, .35); add(Q('sipdef', 'd_har') + .8, TINK, .35)
for i in range(6): add(Q('sipdef', 'd_har') + 1.3 + i * .7, STEP, .12)
add(Q('sipdef', 'd_apne'), POP, .4)
# units demo
for i in range(6): add(Q('units', 'u_fayda') + .2 + i * .9, TINK, .3, -.6 + i * .24)
add(Q('units', 'u_neeche'), POP, .4); add(Q('units', 'u_upar'), POP, .4); add(Q('units', 'u_long'), register(), .4)
# devi1 / mf title
add(S('devi1') + .15, GL, .3); add(S('mftitle') + .15, PUNCH, .55); add(S('mftitle') + .45, KICK, .35)
# tokri
for i in range(10): add(Q('tokri', 't_hazaar') + .35 + i * .13, TINK, .12, (i % 2 - .5))
add(Q('tokri', 't_expert'), POP, .4)
for i in range(6): add(Q('tokri', 't_expert') + 1 + i * .25, STEP, .2, (i - 2.5) * .25)
for i in range(6): add(Q('tokri', 't_units') + i * .1, POP, .2, (i - 2.5) * .2)
# cats + rank
for i in range(3): add(Q('cats', f'c_{i}'), PUNCH if i == 2 else POP, .45, (i - 1) * .5)
add(S('rank') + .2, SW, .35)
for k in ('r_100', 'r_101', 'r_251'): add(Q('rank', k), POP, .45)
# cars: each vehicle arrives with a whoosh; bike gets a rev-like punch
for k, g in (('k_suv', .35), ('k_sedan', .4), ('k_bike', .55)): add(Q('cars', k) - .3, WF, g); add(Q('cars', k) - .2, SUB, .35)
add(Q('cars', 'k_bike') - .1, PUNCH, .45)
# fall
add(S('fall') + .5, B('riser/dark') if False else GL, .35); add(S('fall') + 2.2, SUB, .5); add(Q('fall', 'f_ghabra') + .3, GL, .45)
# devi2 + answer slider
add(S('devi2') + .1, POP, .35); add(Q('answer', 'a_kam') + .4, POP, .4, -.5); add(Q('answer', 'a_zyada') + .6, POP, .4, .5)
# app intro + steps
add(S('appintro') + .1, POP, .4); add(Q('appintro', 'ai_6'), PUNCH, .45)
for k in ('st1', 'st2', 'st3', 'st4', 'st5', 'st6'): add(S(k) + .05, TINK, .35)
for i in range(30): add(S('st1') + 1 + i * .095, STEP, .06)
add(Q('st1', 'k1_ek'), DING, .4)
for i in range(3): add(S('st2') + 1.2 + i * .8, STEP, .25)
add(Q('st3', 'k3_sip'), POP, .35)
for i in range(4): add(Q('st3', 'k3_amt') + i * .25, STEP, .25)
add(Q('st4', 'k4_salary'), POP, .4); add(Q('st5', 'k5_upi'), STEP, .3); add(Q('st5', 'k5_approve'), DING, .45)
add(Q('st6', 'k6_confirm'), register(), .5)
# bas
add(S('bas') + .1, PUNCH, .5); add(S('bas') + .15, DING, .45)
# galtiyan
for i in range(4): add(Q('galti', f'g_{i}'), GL, .35); add(Q('galti', f'g_{i}') + .02, KICK, .3)
# recap + like
for i in range(5): add(Q('recap', f'rc_{i}'), POP, .4, (i - 2) * .2)
add(S('like') + .3, POP, .45); add(Q('like', 'l_sub'), DING, .45)
os.makedirs(f'{D}/audio', exist_ok=True); sf.write(f'{D}/audio/sfx_only.wav', mix, SR); print('sfx ok', round(np.abs(mix).max(), 2))
