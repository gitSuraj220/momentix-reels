"""SFX for the five-incomes reel (no music; Suraj adds BGM)."""
import os, sys
import numpy as np, soundfile as sf
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(D, '../../engine'))
from earshot_bank import bank
SR = 48000; END = 15.6; rng = np.random.default_rng(7)
mix = np.zeros((int((END + .5) * SR), 2), np.float32)
def norm(x): return (x / (np.abs(x).max() + 1e-9) * .89).astype(np.float32)
def B(k, **kw): return norm(bank(k, **kw))
def add(t, x, g=1.0, pan=0.0):
    i = int(max(0, t) * SR); l, r = np.sqrt(.5 * (1 - pan)), np.sqrt(.5 * (1 + pan)); n = min(len(x), len(mix) - i)
    if n > 0: mix[i:i + n, 0] += x[:n] * g * l; mix[i:i + n, 1] += x[:n] * g * r
DRIP = [B('drip/bloop', seed=i) for i in range(4)]; TINK = B('pro_pop/tink'); POP = B('pro_pop/boop'); WIDE = B('ui_pop/wide')
CLG = B('pro_click/glass'); KICK = B('cut_hit/kick'); PUNCH = B('impact/punch'); GL = B('glitch/hit'); ZDW = B('pro_zip/down_warm')
CLUNK = B('knock/wood'); DING = B('pro_notify/ding_2167'); CELE = B('mallet/celesta'); SHIM = B('pro_shimmer/m1'); STEP = B('ui_pop/step'); WF = B('whoosh_fast/crisp')
def snip(t):
    for d in (0, .07): add(t + d, CLG, .5, .3); add(t + d, STEP, .35, .3)
# water drips: right fast until 5.4, left steady
for t in np.arange(.55, 5.4, .16): add(t, DRIP[int(t * 7) % 4], .14, .55)
for t in np.arange(.6, 15.0, .27): add(t, DRIP[int(t * 5) % 4], .12, -.55)
# counter ticks
for t in np.arange(.8, 5.4, .5): add(t, TINK, .1, .5)
for t in np.arange(.9, 15.0, .5): add(t, TINK, .08, -.5)
add(0.02, WF, .4); add(.05, POP, .4); add(.2, POP, .3)            # title
add(2.8, WIDE, .4, .3)                                          # EASY MONEY
add(5.05, WF, .35, .6); snip(5.4); add(5.42, PUNCH, .55); add(5.42, GL, .3, .5)   # layoff 1
add(5.65, WIDE, .45, .3)                                        # WHAT?!
add(7.25, WF, .35, -.2); snip(7.6); add(7.62, KICK, .45); add(8.0, POP, .4, -.3) # layoff 2 + still 4 left
add(9.4, ZDW, .4, .3)                                           # man goes grey
add(9.6, WF, .35, -.3); add(10.15, CLUNK, .5, -.3); add(10.2, DING, .35, -.3); add(10.3, SHIM, .3, -.3)  # new skill
add(10.8, CELE, .4, -.4)                                        # crosses 1.45L
add(11.8, POP, .4); add(12.6, POP, .4); add(12.65, CELE, .3); add(13.2, STEP, .3)  # end text
sf.write(f'{D}/audio/sfx_only.wav', mix, SR); print('sfx ok')
