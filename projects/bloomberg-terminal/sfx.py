"""SFX for the Bloomberg reel (heavy, paper/pencil/keyboard flavoured). No music."""
import os, sys
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(D, '../../engine'))
from earshot_bank import bank
exec(open(f'{D}/timeline.js').read().split('// subtitles')[0].replace('window.', '').replace('//', '#').replace('{', 'dict(').replace('}', ')').replace(': ', '=').replace(';', ''))  # END, SC, CUE
SR = 48000; rng = np.random.default_rng(5)
mix = np.zeros((int((END + 1.5) * SR), 2), np.float32)
def norm(x): return (x / (np.abs(x).max() + 1e-9) * .89).astype(np.float32)
def B(k, **kw): return norm(bank(k, **kw))
def add(t, x, g=1.0, pan=0.0):
    i = int(max(0, t) * SR); l, r = np.sqrt(.5 * (1 - pan)), np.sqrt(.5 * (1 + pan)); n = min(len(x), len(mix) - i)
    if n > 0: mix[i:i + n, 0] += x[:n] * g * l; mix[i:i + n, 1] += x[:n] * g * r
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
def pencil(d):   # graphite scratch: band noise with stroke envelope
    t = np.arange(int(d * SR)) / SR; e = np.abs(np.sin(np.pi * t / d * max(1, int(d / .22)))) ** .6 * np.minimum(1, (d - t) / .05)
    return norm(bp(rng.standard_normal(len(t)), 2500, 9000) * e)
def crt_hum(d):
    t = np.arange(int(d * SR)) / SR; x = .4 * np.sin(2 * np.pi * 15734 * t) * .1 + bp(rng.standard_normal(len(t)), 60, 400) * .5 + .3 * np.sin(2 * np.pi * 60 * t)
    return norm(x * np.minimum(1, t / .3) * np.minimum(1, (d - t) / .3))
S = dict(SC); Q = CUE
POP = B('pro_pop/boop'); TINK = B('pro_pop/tink'); PAPER = B('swipe/paper'); WF = B('whoosh_fast/crisp'); KICK = B('cut_hit/kick')
PUNCH = B('impact/punch'); _f = int(.6 * SR); PUNCH = PUNCH[:_f] * np.r_[np.ones(_f - int(.25 * SR)), np.linspace(1, 0, int(.25 * SR))].astype(np.float32)
DESK = B('knock/desk'); KEYS = [B('typing_key/clicky', seed=i) for i in range(6)]; KTHOCK = B('fit/key/thock'); DING = B('pro_notify/ding_2045')
STAMP = B('fit/hit/bamboo_tok'); THUP = B('pro_pop/thup'); CELE = B('mallet/celesta'); SHIM = B('pro_shimmer/m1'); GL = B('glitch/dropout'); SUBQ = B('pro_sub_drop/quick')
PIN = B('pro_pop_in/round'); ZDOWN = B('pro_zip/down'); ZUP = B('pro_zip/up'); RISE = B('riser/snatch'); BLOOM = B('logo_sting/soft_bloom'); HT = B('hover_tick/air'); CLG = B('pro_click/glass')
def typing(t0, n, gap=.075, g=.22):
    for i in range(n): add(t0 + i * gap + rng.uniform(-.01, .01), KEYS[i % 6], g, rng.uniform(-.2, .2))
def stamp(t, g=.5): add(t, STAMP, g); add(t, KICK, g * .7); add(t + .01, THUP, g * .5)
# page turns at every scene change
for k, s in SC[1:]: add(s - .12, PAPER, .32, rng.uniform(-.3, .3)); add(s - .02, HT, .12)
# hook
add(0, crt_hum(6.8), .12); add(.05, pencil(.9), .3); typing(.6, 22, .08, .18); add(Q['price'] - .15, WF, .35); add(Q['price'] + .1, PUNCH, .55); add(Q['price'] + .1, TINK, .3, .4)
add(Q['users'], POP, .45); add(Q['users'] + .05, CELE, .25)
# keys
for k in ['kaala', 'orange']: add(Q[k], TINK, .3)
for i, k in enumerate(['yellow', 'green', 'red']): add(Q[k], KTHOCK, .5, (i - 1) * .4); add(Q[k] + .02, POP, .25)
typing(S['keys'] + .3, 10, .1, .14)
# prices
for i, k in enumerate(['shares', 'bonds', 'currency', 'oil']): add(Q[k] - .15, PIN, .45, (i % 2 - .5) * .6); typing(Q[k], 5, .05, .1)
add(Q['sabkuch'], ZUP, .35); typing(Q['sabkuch'] + .2, 14, .06, .14)
# reveal
add(S['reveal'], SHIM, .3); add(Q['title'] - .25, RISE, .3); add(Q['title'] - .2, PUNCH, .5); add(Q['title'] - .18, DING, .3)
# 1981 / merrill
add(S['y1981'] + .1, PAPER, .3); add(Q['y1981'] - .3, pencil(.9), .35); add(Q['y1981'], DESK, .45); add(Q['mb'], pencil(.6), .25); stamp(Q['crore'])
add(S['merrill'] + .1, DESK, .4)
for i in range(20): add(Q['bees'] - .5 + i * .06, CLG if i % 2 else TINK, .18, ((i % 5) - 2) * .2)
# rivals
add(S['rivals'] + .25, POP, .4); stamp(Q['sasta']); stamp(Q['free'], .45); add(Q['lseg'] - .1, PIN, .45, -.4); add(Q['factset'] - .1, PIN, .45, .4)
# why
add(S['why'] + .2, PUNCH, .45); add(Q['asli'], typing.__defaults__ and KTHOCK, .4); add(Q['asli'] + .6, pencil(.4), .45); add(Q['kaun'] - .1, ZUP, .35)
for i in range(9): add(Q['kaun'] + i * .05, POP, .14, (i - 4) * .1)
# chat
add(S['chat'] + .1, pencil(.7), .3)
for i in range(4): add(Q['chatc'] + i * .45, DING if i == 3 else POP, .35, (-.4, .4)[i % 2])
add(Q['lakh3'], RISE, .25); [add(Q['lakh3'] + i * .05, HT, .06, rng.uniform(-.8, .8)) for i in range(28)]; add(Q['lakh3'] + 1.25, TINK, .35); add(Q['banks'], CELE, .3)
# lanes
add(Q['exch'] - .3, pencil(.7), .3); add(Q['exch'] + .4, DESK, .4)
for i in range(3): add(Q['insaan'] + i * .25, POP, .35, (-.3, .3)[i % 2])
# sia
add(S['sia'] + .1, SHIM, .2); add(Q['bond'], ZUP, .3); typing(Q['bond'] + .05, 12, .05, .12)
for i in range(3): add(Q['dealers'] + i * .2, PIN, .35, (i - 1) * .4); add(Q['msg'] + i * .1, CLG, .3)
for i in range(3): add(Q['prices3'] + i * .3, DING if i == 1 else TINK, .3, (i - 1) * .4)
add(Q['best'], CELE, .35); typing(Q['done'] - .6, 4, .12, .3); add(Q['done'], KTHOCK, .55); stamp(Q['done'] + .15, .45)
# room
add(S['room'] + .05, DESK, .35); add(S['room'] + .6, SUBQ, .25)
# outage
add(S['outage'], crt_hum(Q['band'] - S['outage']), .12)
for i in range(16): add(Q['band'] - .4 + rng.uniform(0, 1.2), GL if i % 4 == 0 else THUP, .14 if i % 4 else .2, rng.uniform(-.6, .6))
add(Q['band'], SUBQ, .4); add(Q['britain'], PIN, .45); add(Q['postpone'] - .2, WF, .3); stamp(Q['postpone'], .6)
# revenue
stamp(Q['andaaze'] - .3, .35); add(Q['b14'], ZUP, .35); typing(Q['b14'], 10, .08, .12); add(Q['b14'] + .9, DING, .35); add(Q['isi'], CELE, .3)
# free
add(S['free'] + .1, pencil(.7), .3); stamp(Q['tools'], .45); add(Q['tools'] + .1, TINK, .3)
# final
add(Q['datanahi'] + .2, pencil(.4), .5); add(Q['kaunhai'] - .6, PUNCH, .45); add(Q['kaunhai'], pencil(.6), .35)
# end
add(S['end'], ZUP, .3); typing(S['end'] + .1, 8, .07, .14); add(S['end'] + .5, BLOOM, .35)
for k, v in [(k, v) for k, v in CUE.items()]: pass
sf.write(f'{D}/audio/sfx_only.wav', mix, SR); print('sfx ok', round(len(mix) / SR, 1))
