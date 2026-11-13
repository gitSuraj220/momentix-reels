"""SFX for the Nvidia CEO reel (no music; Suraj adds BGM). Cue times come from timeline.json (real VO)."""
import json, os, sys
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(D, '../../engine'))
from earshot_bank import bank
J = json.load(open(f'{D}/timeline.json')); TL, CUE, END = J['TL'], J['CUE'], J['END']
SR = 48000; rng = np.random.default_rng(11)
mix = np.zeros((int((END + 1.5) * SR), 2), np.float32)
def norm(x): return (x / (np.abs(x).max() + 1e-9) * .89).astype(np.float32)
def B(k, **kw): return norm(bank(k, **kw))
def add(t, x, g=1.0, pan=0.0):
    i = int(max(0, t) * SR); l, r = np.sqrt(.5 * (1 - pan)), np.sqrt(.5 * (1 + pan)); n = min(len(x), len(mix) - i)
    if n > 0: mix[i:i + n, 0] += x[:n] * g * l; mix[i:i + n, 1] += x[:n] * g * r
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
def room(d):   # quiet dinner-room tone: low air + faint clock tick
    t = np.arange(int(d * SR)) / SR; x = bp(rng.standard_normal(len(t)), 120, 1200) * .25
    tick = np.zeros(len(t));
    for s in np.arange(.3, d, 1.0): i = int(s * SR); k = np.arange(min(400, len(t) - i)); tick[i:i + len(k)] += np.exp(-k / 60) * np.sin(2 * np.pi * 2500 * k / SR)
    e = np.minimum(1, t / .4) * np.minimum(1, (d - t) / .4); return norm((x + .5 * tick) * e)
def news_sting():   # TV "breaking news" two-note synth stab
    t = np.arange(int(.9 * SR)) / SR; f = np.where(t < .18, 880, 659)
    x = np.sign(np.sin(2 * np.pi * f * t)) * .3 + np.sin(2 * np.pi * f / 2 * t)
    return norm(bp(x, 200, 5000) * np.exp(-np.maximum(0, t - .18) / .25))
def needle(d=.8):   # gauge swing: rising-falling creak
    t = np.arange(int(d * SR)) / SR; f = 300 + 500 * t / d
    return norm(bp(np.sin(2 * np.pi * np.cumsum(f) / SR) * (np.sin(2 * np.pi * 30 * t) > 0), 200, 3000) * np.exp(-t / .5))
POP = B('pro_pop/boop'); TINK = B('pro_pop/tink'); SW = B('swipe/paper'); WF = B('whoosh_fast/crisp')
PUNCH = B('impact/punch'); _f = int(.6 * SR); PUNCH = PUNCH[:_f] * np.r_[np.ones(_f - int(.25 * SR)), np.linspace(1, 0, int(.25 * SR))].astype(np.float32)
KICK = B('cut_hit/kick'); GL = B('glitch/hit'); STEP = B('ui_pop/step'); DING = B('pro_notify/ding_2045')
S = lambda k: TL[k][0]
# dinner room tone under the table scenes
for k in ['M1', 'P1', 'P2', 'P3']: add(S(k) - .1, room(TL[k][1] - S(k) + .4), .18)
# hook
add(0.05, news_sting(), .5); add(1.5, WF, .45); add(CUE['crash'], PUNCH, .75); add(CUE['crash'], KICK, .5); add(CUE['crash'] + .03, GL, .3)
# kaise
add(S('P1') - .1, SW, .35); [add(S('P1') + .15 + i * .12, TINK, .3, (i - 1) * .4) for i in range(3)]
# affair: spotlight thunk, heart crack, cards, arrow down
add(S('M2') - .12, WF, .45); add(S('M2') + .05, KICK, .35)
add(CUE['affair'] - .3, POP, .4); add(CUE['affair'] + .3, GL, .45); add(CUE['affair'] + .32, KICK, .3)
for c in [CUE['affair'] - .2, CUE['affair'] + .25]: add(c, SW, .35, .3)
add(CUE['down'], WF, .4); add(CUE['down'] + .45, PUNCH, .5)
# fayda
add(S('P2') - .1, SW, .35); add(CUE['fayda'], POP, .45)
# news pile -> boxes -> gauge
add(S('M3') - .12, WF, .4)
for i in range(7): add(S('M3') + .15 + i * .22, SW, .22, (i % 3 - 1) * .4)
add(CUE['biz'], POP, .45, -.3); add(CUE['biz'] + .2, DING, .3, -.3); add(CUE['profit'], POP, .45, .3); add(CUE['profit'] + .2, DING, .3, .3)
add(CUE['senti'] - .1, STEP, .35); add(CUE['senti'], needle(), .4); add(CUE['senti'] + .6, KICK, .3)
# mauka tag
add(S('P3') - .1, SW, .3); add(CUE['mauka'] - .3, POP, .45); add(CUE['mauka'] + .1, TINK, .3)
# seesaw + magnifier
add(S('M4') - .12, WF, .4); add(S('M4') + .1, POP, .35, -.4); add(CUE['risk'] - .05, POP, .45, .4); add(CUE['risk'] + .1, KICK, .3)
add(CUE['samjho'], WF, .35); add(CUE['samjho'] + .05, TINK, .3); add(CUE['faisla'], STEP, .3)
# globe
add(S('P4') - .12, WF, .4); add(S('P4') + .3, SW, .3); add(CUE['kaise'], TINK, .3); add(CUE['kaise'] + .1, TINK, .25, .3)
# app
s0 = S('M5'); add(s0 - .05, WF, .5, .4)
for i in range(4): add(s0 + .7 + i * .15, STEP, .2)
add(s0 + 2.0, POP, .4); add(s0 + 2.8, STEP, .45); add(s0 + 3.1, DING, .45)
# CTA: typing STOCK, send, DM
c = CUE['cta']; add(c - .1, WF, .45); add(c, POP, .4)
for i in range(5): add(c + .3 + i * .09, STEP, .18)
add(c + .9, SW, .35); add(c + 1.05, DING, .45)
sf.write(f'{D}/audio/sfx_only.wav', mix, SR); print('sfx ok', len(mix) / SR)
