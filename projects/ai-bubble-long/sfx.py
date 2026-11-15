#!/usr/bin/env python3
"""SFX for AI Bubble (long, 16:9). No music (Suraj adds BGM). Cues come from shots.json + the template timings
in player/tpl.js. Hand-synth (numpy/scipy): the earshot bank could not be installed in the build session.
Writes audio/sfx_only.wav (48 kHz stereo). Run after make_shots.py."""
import os, json
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
D = os.path.dirname(os.path.abspath(__file__))
SH = json.load(open(f'{D}/shots.json')); SHOTS = SH['shots']; END = SH['duration']
SR = 48000; rng = np.random.default_rng(7)
mix = np.zeros((int((END + 2) * SR), 2), np.float32)
T = lambda d: np.arange(int(d * SR)) / SR
def norm(x): return (x / (np.abs(x).max() + 1e-9) * .89).astype(np.float32)
def bp(x, lo, hi): return sosfilt(butter(2, [lo, min(hi, 23000)], 'band', fs=SR, output='sos'), x)
def lp(x, f): return sosfilt(butter(2, f, 'low', fs=SR, output='sos'), x)
def hp(x, f): return sosfilt(butter(2, f, 'high', fs=SR, output='sos'), x)
def fade(x, a=.004, r=.03):
    n = len(x); t = np.arange(n) / SR; return x * np.minimum(1, t / a) * np.minimum(1, (n / SR - t) / r)
def add(t, x, g=1.0, pan=0.0):
    i = int(max(0, t) * SR); l, r = np.sqrt(.5 * (1 - pan)), np.sqrt(.5 * (1 + pan)); n = min(len(x), len(mix) - i)
    if n > 0: mix[i:i + n, 0] += x[:n] * g * l; mix[i:i + n, 1] += x[:n] * g * r
def sweep_noise(d, lo, hi, shape):
    t = T(d); nz = rng.standard_normal(len(t)); out = np.zeros(len(t)); k = 480
    for i in range(0, len(t), k):
        f = lo + (hi - lo) * shape(i / len(t)); out[i:i + k] = bp(nz[i:i + k], f * .6, f * 1.7)[:len(out[i:i + k])]
    return out, t
# ---------------- voices ----------------
def whoosh(d=.36, lo=400, hi=5200):
    out, t = sweep_noise(d, lo, hi, lambda u: np.sin(np.pi * u) ** 2); return norm(fade(out * np.sin(np.pi * t / d) ** 1.5, .02, .05))
def whip(): return whoosh(.22, 900, 7000)
def impact(f=55, d=.8):
    t = T(d); fr = f * (1 + 2.2 * np.exp(-t * 28))
    return norm(np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / .25) + .45 * lp(rng.standard_normal(len(t)), 2500) * np.exp(-t / .035))
def boom():   # bigger cinematic hit: impact + low tail
    t = T(1.6); tail = lp(rng.standard_normal(len(t)), 180) * np.exp(-t / .5)
    x = np.zeros(len(t)); i = impact(45, 1.2); x[:len(i)] += i; return norm(x + .6 * norm(tail))
def punch(): return impact(95, .28)
def thump(): return impact(120, .18)
def pop(f=880):
    t = T(.16); fr = f * np.exp(-t * 16) + f * .45
    return norm(np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / .045) * np.minimum(1, t / .002))
def tink(f=2637):
    t = T(.7); return norm(sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t / dd) for m, a, dd in [(1, 1, .28), (1.5, .45, .2), (2.01, .25, .14)]) * np.minimum(1, t / .002))
def ding(): return norm(np.concatenate([tink(1568)[:int(.09 * SR)], tink(2093)]))
def register():
    t = T(.95); thunk = bp(rng.standard_normal(len(t)), 120, 900) * np.exp(-t / .03)
    bell = sum(a * np.sin(2 * np.pi * f * t) for f, a in [(2093, 1), (2637, .6), (4186, .3)]) * np.exp(-np.maximum(0, t - .09) / .35) * (t > .09)
    return norm(.7 * thunk + .5 * bell)
def glitch(d=.35):
    t = T(d); out = np.zeros(len(t)); i = 0
    while i < len(t):
        n = int(rng.uniform(.012, .05) * SR); f = rng.choice([110, 220, 440, 880, 1760])
        seg = np.sign(np.sin(2 * np.pi * f * t[:n])) * rng.uniform(.3, 1) if rng.random() > .25 else rng.standard_normal(n) * .7
        out[i:i + n] = seg[:len(out[i:i + n])] * (rng.random() > .2); i += n
    return norm(fade(lp(out, 7000), .002, .03))
def stamp():
    t = T(.3); return norm(np.sin(2 * np.pi * np.cumsum(140 * np.exp(-t * 30) + 60) / SR) * np.exp(-t / .07) + .7 * bp(rng.standard_normal(len(t)), 300, 3000) * np.exp(-t / .02))
def paper(d=.45):
    t = T(d); return norm(fade(bp(rng.standard_normal(len(t)), 1800, 9000) * (.5 + .5 * np.sin(2 * np.pi * 17 * t + rng.uniform(0, 6))) ** 2 * np.sin(np.pi * t / d), .01, .05))
def ticks(d, n=14, f0=1400, f1=2600):
    out = np.zeros(int(d * SR) + int(.1 * SR))
    for k in range(n):
        tk = T(.04); x = np.sin(2 * np.pi * (f0 + (f1 - f0) * k / n) * tk) * np.exp(-tk / .01); i = int(d * (k / n) ** .7 * SR); out[i:i + len(x)] += x
    return norm(out)
def riser(d=1.0):
    t = T(d); f = 180 * (5 ** (t / d)); return norm(fade((np.sin(2 * np.pi * np.cumsum(f) / SR) * .45 + bp(rng.standard_normal(len(t)), 700, 7000) * .55) * (t / d) ** 2.2, .02, .01))
def shimmer(d=1.4):
    t = T(d); return norm(fade(sum(np.sin(2 * np.pi * f * t + rng.uniform(0, 6)) * np.exp(-t / .5) for f in [1568, 2093, 2637, 3136, 4186]), .05, .4))
def key():
    t = T(.06); return norm(bp(rng.standard_normal(len(t)), 1500, 7000) * np.exp(-t / .008) + .4 * np.sin(2 * np.pi * 180 * t) * np.exp(-t / .01))
def typing(d, rate=11):
    out = np.zeros(int((d + .1) * SR)); k = key(); tt = 0
    while tt < d:
        i = int(tt * SR); out[i:i + len(k)] += k * rng.uniform(.5, 1); tt += 1 / rate * rng.uniform(.6, 1.4)
    return norm(out)
def scratch():   # record scratch: fast pitch-wobbled noise + tone
    t = T(.55); f = 600 + 900 * np.sin(2 * np.pi * 7 * t) * np.exp(-t * 2)
    x = bp(rng.standard_normal(len(t)), 500, 5000) * (.5 + .5 * np.sin(2 * np.pi * np.cumsum(f) / SR * .05)) + .4 * np.sin(2 * np.pi * np.cumsum(f) / SR)
    return norm(fade(x * np.exp(-t / .3), .002, .06))
def crack():   # wood snap: two broadband clicks + creak
    t = T(.5); x = hp(rng.standard_normal(len(t)), 900) * (np.exp(-t / .006) + .8 * np.exp(-np.maximum(0, t - .035) / .01) * (t > .035))
    return norm(x + .3 * bp(rng.standard_normal(len(t)), 200, 1200) * np.exp(-t / .12))
def buzz(d=3.0):   # mosquito: 600 Hz saw with wobble, panned by caller
    t = T(d); f = 620 + 40 * np.sin(2 * np.pi * 3.1 * t) + 25 * np.sin(2 * np.pi * 11 * t)
    ph = np.cumsum(f) / SR; x = 2 * (ph % 1) - 1; return norm(fade(bp(x, 400, 6000) * (.6 + .4 * np.sin(2 * np.pi * .7 * t)), .3, .3))
def gavel():
    t = T(.5); return norm(bp(rng.standard_normal(len(t)), 150, 2500) * np.exp(-t / .02) + .8 * np.sin(2 * np.pi * 320 * t) * np.exp(-t / .06) + .5 * np.sin(2 * np.pi * 95 * t) * np.exp(-t / .12))
def dundun():
    t = T(1.6); f = np.where(t < .55, 98, 92.5); env = np.exp(-np.mod(t, .55) / .3) * (t < 1.6)
    x = (np.sign(np.sin(2 * np.pi * f * t)) * .3 + np.sin(2 * np.pi * f * t) + .5 * np.sin(np.pi * f * t)) * env; return norm(lp(x, 1800))
def hiss(d=1.8):
    t = T(d); return norm(fade(bp(rng.standard_normal(len(t)), 2500, 11000) * (.6 + .4 * np.sin(2 * np.pi * 5 * t)), .05, .3))
def rumble(d):
    t = T(d); return norm(fade(lp(rng.standard_normal(len(t)), 160) * (1 + .3 * np.sin(2 * np.pi * 9 * t)) + .3 * np.sin(2 * np.pi * 48 * t), .3, .3))
def squeak(d=1.0):   # balloon rubber stretch
    t = T(d); f = 300 + 500 * (t / d) + 60 * np.sin(2 * np.pi * 13 * t); x = np.sin(2 * np.pi * np.cumsum(f) / SR) * (np.sin(2 * np.pi * 23 * t) > -.3)
    return norm(fade(bp(x, 250, 3000) * (t / d), .05, .1))
def static(d=.4):
    t = T(d); return norm(fade(hp(rng.standard_normal(len(t)), 1500), .002, .05))
def heartbeat():
    t = T(.8); b = lambda o: np.sin(2 * np.pi * 50 * (t - o)) * np.exp(-np.maximum(0, t - o) / .07) * (t > o)
    return norm(lp(b(0) + .7 * b(.22), 300))
def room(d, kind='office'):
    t = T(d); lo, hi = {'office': (90, 900), 'night': (60, 500), 'crowd': (200, 2500)}[kind]
    x = bp(rng.standard_normal(len(t)), lo, hi)
    if kind == 'crowd': x *= .6 + .4 * np.abs(np.sin(2 * np.pi * .4 * t))
    return norm(fade(x, .3, .3))
def coins(n=6):
    out = np.zeros(int(.8 * SR))
    for k in range(n):
        x = tink(rng.uniform(3000, 4800))[:int(.3 * SR)] * .6; i = int(rng.uniform(0, .5) * SR); out[i:i + len(x)] += x
    return norm(out)

def failtone():
    t = T(.8); f = 330 * np.exp(-t * 1.1); return norm(fade(np.sin(2 * np.pi * np.cumsum(f) / SR) + .4 * np.sin(2 * np.pi * np.cumsum(f * 1.5) / SR), .01, .15))
def alarm():
    t = T(.2); return norm(fade(np.sign(np.sin(2 * np.pi * 900 * t)) * .5 + np.sin(2 * np.pi * 450 * t) * .5, .004, .05) * np.exp(-t / .1))
FAIL = failtone(); ALARM = alarm()
WH = [whoosh(.34 + .04 * k, 350 + 60 * k, 4800 + 300 * k) for k in range(4)]; WP = [whip() for _ in range(3)]
IMP = impact(); BOOM = boom(); PUNCH = punch(); THUMP = thump(); POPS = [pop(f) for f in (660, 880, 1046, 1318)]
TINK = tink(); DING = ding(); REG = register(); GL = glitch(); STAMP = stamp(); PAPER = paper(); SHIM = shimmer(); KEY = key()

# ---------------- per-shot cues ----------------
for k, s in enumerate(SHOTS):
    t0, t1, p, tpl = s['t0'], s['t1'], s['p'], s['tpl']; d = t1 - t0; sid = s['id']; pan = ((sid % 5) - 2) * .15
    # transition into the shot
    if k:
        if s['tr'] == 'whip': add(t0 - .17, WH[sid % 4], .42, pan); add(t0 - .1, WP[sid % 3], .18, -pan)
        elif s['tr'] == 'flash': add(t0 - .02, IMP, .55); add(t0 - .1, WH[sid % 4], .3)
        elif s['tr'] == 'punch': add(t0, THUMP, .35)
    # room tone under art shots
    if tpl == 'image':
        kind = 'crowd' if any(w in s['visual'].lower() for w in ('crowd', 'party', 'audience', 'concert')) else 'night' if 'night' in s['visual'].lower() else 'office'
        add(t0, room(d + .2, kind), .06 if kind != 'crowd' else .09)
        if p.get('shake'): add(t0 + d * .12, PUNCH, .5)
        for o in p.get('ov', []):
            a = t0 + d * o.get('at', .25)
            if o['k'] == 'stamp': add(t0 + d * o.get('at', .5), STAMP, .55)
            elif o['k'] == 'tag': add(a, POPS[sid % 4], .4, .3)
            elif o['k'] == 'logo': add(t0 + .3, TINK, .25)
            elif o['k'] == 'alarm': [add(t0 + i * .45, ALARM, .14) for i in range(int(d / .45))]
            elif o['k'] == 'namecards': [add(t0 + d * (.3 + i * .2), PAPER, .45, (-1) ** i * .5) for i in range(2)]
            elif o['k'] == 'speedlines': add(t0, rumble(d), .25); [add(t0 + i * .5, WP[i % 3], .2, (-1) ** i * .5) for i in range(int(d / .5))]
            elif o['k'] in ('confetti',): add(t0 + .1, coins() if o.get('cheques') else SHIM, .3)
            elif o['k'] == 'phone': add(t0 + d * .2, WH[1], .3); add(t0 + d * .45, POPS[2], .35)
            elif o['k'] == 'slide': add(t0 + .1, KEY, .3); add(t0 + .2, POPS[0], .25)
            elif o['k'] == 'bubble': add(t0 + d * .3, POPS[1], .4)
            elif o['k'] == 'drawline': add(t0 + d * .15, squeak(d * .45), .2)
            elif o['k'] == 'logorow': [add(t0 + .2 + i * .18, POPS[i % 4], .35, (i - 1.5) * .3) for i in range(len(o['items']))]
            elif o['k'] == 'spotmove': [add(t0 + i * d / o.get('n', 4), THUMP, .3) for i in range(o.get('n', 4))]
            elif o['k'] == 'spot': add(t0 + .05, THUMP, .45)
    elif tpl == 'counter':
        cd = min(d * .7, 2.6); add(t0 - .9, riser(.9), .3); add(t0 + .15, ticks(cd - .15, 18), .3); add(t0 + cd, BOOM if p.get('slam') or p.get('to', 0) >= 1e9 else IMP, .6)
        if p.get('style') == 'bill': add(t0 + cd + .1, REG, .4)
        if p.get('fire'): add(t0, hiss(d) * .5, .3); add(t0, rumble(d), .3)
        if p.get('style') == 'token': [add(t0 + i * .25, PAPER, .18, (-1) ** i * .5) for i in range(int(d / .25))]
    elif tpl == 'balloon':
        m = p['mode']
        if m == 'inflate': add(t0 + .1, squeak(d * .65), .35); add(t0 + .1, ticks(d * .65, 24), .25); add(t0 + d * .75, BOOM, .55)
        elif m == 'crack': add(t0 + .1, hiss(d), .35 if not p.get('thin') else .18); [add(t0 + .2 + i * .6, crack() * .6, .25) for i in range(2)]
        elif m == 'notch': [add(t0 + i * d / 2.2, squeak(.5), .4) for i in range(2)]
        elif m == 'tighten': add(t0, rumble(d), .35); [add(t0 + i * .9, heartbeat(), .5) for i in range(int(d / .9))]; add(t0, squeak(d), .12)
        else:
            add(t0, rumble(d), .18)
            if p.get('megaphones'): [add(t0 + i * .5, glitch(.18), .2, (-1) ** i * .7) for i in range(int(d / .5))]
            if p.get('browser'): add(t0 + d * .25, GL, .4); add(t0 + d * .26, crack(), .5)
            if p.get('needle'): add(t0 + .2, TINK, .25)
    elif tpl == 'title':
        st = p.get('style')
        if st == 'neon': add(t0, glitch(.3), .35); add(t0 + .05, SHIM, .3)
        elif st == 'black': add(t0 + .1, typing(min(d * .6, 1.6)), .35)
        elif st == 'shake': add(t0, BOOM, .5)
        elif st == 'curtain': add(t0 + .1, rumble(d * .6), .35); add(t0 + .1, PAPER, .3)
        elif st == 'crack': add(t0, crack(), .6); add(t0 + .05, GL, .25)
        elif st == 'sparkle': add(t0, SHIM, .45); add(t0, IMP, .4)
        elif st == 'tv': add(t0, static(.3), .25); add(t0 + d * .82, static(.15), .4); add(t0 + d * .82, THUMP, .5)
    elif tpl == 'calendar':
        if p.get('mode') == 'app': add(t0 + d * .4, DING, .4)
        elif p.get('mode') == 'fast': [add(t0 + u, PAPER, .3, (-1) ** i * .4) for i, u in enumerate(np.cumsum([.5, .4, .32, .25, .2, .16, .13, .11, .1, .09, .08])) if u < d]
        else: add(t0, PAPER, .5); add(t0 + .45, THUMP, .4)
    elif tpl == 'launch': add(t0, SHIM, .35); add(t0 + .25, IMP, .45); add(t0 + .7, typing(min(1.4, d - .8)), .3)
    elif tpl == 'tweet':
        add(t0, POPS[1], .4); add(t0 + .15, DING, .25)
        if p.get('meter'): add(t0 + d * .3, riser(d * .45), .3); [add(t0 + d * .75 + i * .8, heartbeat(), .55) for i in range(3)]
        if p.get('hl'): [add(t0 + .4 + i * (d * .45) / 10, KEY, .2) for i in range(10)]
    elif tpl == 'notif': [add(t0 + i / 7, POPS[i % 4], .28, (i % 3 - 1) * .4) for i in range(int(d * 7))]; add(t0, ticks(d, int(d * 4), 900, 900), .2)
    elif tpl == 'chat':
        if p.get('type'): add(t0 + .2, typing(d * .35), .4); add(t0 + d * .6, WP[0], .3); add(t0 + d * .62, POPS[2], .35)
        for i, _ in enumerate(p.get('msgs', [])):
            if p.get('old') and i < len(p['msgs']) - 1: continue
            add(t0 + .2 + i * d * .4, POPS[(i + 1) % 4], .4)
        if p.get('app') == 'Search': add(t0 + d * .5, STAMP, .4)
        if p.get('upvote'): add(t0 + .4, ticks(d * .4, 12), .2)
        if p.get('blank'): add(t0 + d * .65, THUMP, .4)
    elif tpl == 'race': add(t0 + .3, rumble(d * .6), .3); add(t0 + .3, WH[2], .3); add(t0 + .3 + d * .5, DING, .3)
    elif tpl == 'windows': [add(t0 + i * d * .22, POPS[i], .45, (i - 1) * .5) for i in range(3)]; add(t0 + d * .7, WH[3], .3)
    elif tpl == 'map':
        if p.get('mode') == 'timeline': add(t0 + .1, WH[0], .3); add(t0 + .9, WP[1], .3); add(t0 + 1.5, IMP, .5)
        elif p.get('freeze'): add(t0, glitch(.25), .3); add(t0 + d * .35, STAMP, .65); add(t0 + d * .35, IMP, .4)
        else: [add(t0 + i * .07, POPS[i % 4], .18, (i - 13) / 20) for i in range(26) if i * .07 < d]
    elif tpl == 'cards':
        st = p.get('style')
        if st in ('fan',): [add(t0 + i * .15, PAPER, .4, (i - 1) * .5) for i in range(3)]
        elif st == 'flip': add(t0 + .2, PAPER, .4); add(t0 + .55, IMP, .45)
        elif st == 'morph': [add(t0 + i * d / 3, WP[i % 3], .3) for i in range(3)]; [add(t0 + i * d / 3 + .05, POPS[i], .35) for i in range(3)]
        else: [add(t0 + d * (.1 + i * .25 if st == 'bubbles' else i / 3 * .8), POPS[i % 4], .45, (i - 1) * .5) for i in range(3)]
        if st == 'icons': add(t0 + d * .53 + .6, hiss(.6), .25)
    elif tpl == 'money':
        if p.get('mode') == 'vault': add(t0 + .2, rumble(d * .5), .3); add(t0 + .2 + d * .4, BOOM, .5)
        else: add(t0, rumble(d * .5), .45); add(t0 + d * .38, PUNCH, .4); [add(t0 + d * .45 + i * .12, THUMP, .4) for i in range(6)]; add(t0 + d * .72, POPS[0], .35)
    elif tpl == 'reveal': add(t0 - .9, riser(.9), .35); add(t0 + .2, PUNCH, .4); add(t0 + .35, SHIM, .45); add(t0 + .4, REG, .35)
    elif tpl == 'podium': add(t0 + .2, riser(d * .4), .35); add(t0 + d * .6, IMP, .4); add(t0 + d * .6 + .6, SHIM, .45); add(t0 + d * .65, coins(10), .3)
    elif tpl == 'gpu':
        if p.get('n0') and p['n'] > p['n0'] or p.get('n', 1) > 1 and p.get('n0'): add(t0 + .1, ticks(d * .7, 30, 900, 2400), .3)
        if p.get('tag'): add(t0 + (d * .7 if p.get('n', 1) > 1 else .2), IMP if p.get('n', 1) > 1 else POPS[1], .5)
        if p.get('wiggle'): add(t0 + .4, POPS[3], .3)
    elif tpl == 'stickers': [add(t0 + .4 + i * d * .13, STAMP, .45, (i - 2) * .3) for i in range(5)]; add(t0, THUMP, .3)
    elif tpl == 'bars':
        if p.get('mode') == 'updown': add(t0 + .3, riser(.8), .25); add(t0 + 1.1, IMP, .4); add(t0 + .3 + d * .35 + .8, BOOM, .5)
        else:
            add(t0 + .2, riser(1.2), .3); add(t0 + 1.4, IMP, .45)
            if p.get('arrow'): add(t0 + .2, squeak(d * .4), .25); add(t0 + d * .5, BOOM, .5)
    elif tpl == 'split':
        m = p.get('mode')
        if m == 'block': add(t0 + .4, crack(), .3); add(t0 + .4, WH[1], .3); [add(t0 + 1 + i * .35, POPS[i % 4], .35, (i - 2) * .3) for i in range(5 if not p.get('old') else 1)]
        elif m == 'lawsuit': [add(t0 + i * d * .48 + .1 + .25, PUNCH, .55) for i in range(2)]; [add(t0 + i * d * .48 + .5, STAMP, .5) for i in range(2)]
        else: [add(t0 + i * .5, glitch(.15), .2, -.6) for i in range(int(d / .5))]; add(t0, rumble(d), .2)
    elif tpl == 'logos':
        if p.get('mode') == 'rain': add(t0, coins(14), .35); add(t0 + .6, coins(14), .3); add(t0, rumble(d), .2)
        elif p.get('mode') == 'coins': [add(t0 + .3 + i * .25 + .3, tink(3500 + i * 150), .2, (i - 4) * .2) for i in range(8)]
        else: [add(t0 + .1 + i * .2, POPS[i % 4], .4, (i - 1.5) * .4) for i in range(len(p['items']))]; add(t0 + 1, IMP, .5)
    elif tpl == 'hockey':
        if p['mode'] == 'morph': add(t0 + .3, squeak(d * .3), .3); add(t0 + d * .6, FAIL, .3)
    elif tpl == 'funnel': add(t0, paper(d) * .6, .3); add(t0, rumble(d), .2)
    elif tpl == 'paper':
        if p['mode'] == 'dust': add(t0 + d * .35, hiss(d * .55), .25); add(t0 + d * .35, SHIM, .2)
        elif p['mode'] == 'site': add(t0 + d * .4, DING, .45)
        else: add(t0 + .3, FAIL, .3); add(t0 + d * .65, STAMP, .5)
    elif tpl == 'meter':
        if p['mode'] == 'valuation': add(t0 + .2, squeak(1.2), .3); add(t0 + d * .35, riser(d * .45), .25)
        elif p['mode'] == 'profit': add(t0 + d * .4, STAMP, .5)
        else: add(t0, static(d) * .3, .1); add(t0 + d * .45, POPS[0], .3)
    elif tpl == 'grid': [add(t0 + .2 + i * d * .065, THUMP, .3, (i % 4 - 1.5) * .3) for i in range(12)]
    elif tpl == 'endscreen': add(t0 + .2, SHIM, .3); add(t0, room(d, 'night'), .05)
    # special cues from the brief
    for c in p.get('sfx', []):
        if c == 'scratch': add(t0 + d * (p.get('freeze') or .35) - .05, scratch(), .7)
        if c == 'crack': add(t0 + d * .45, crack(), .8); add(t0 + d * .45, IMP, .4)
        if c == 'buzz': add(t0 + .2, buzz(d - .3), .3, .35)
        if c == 'gavel': add(t0 + d * .12, gavel(), .8)
        if c == 'dundun': add(t0 + .05, dundun(), .7)
os.makedirs(f'{D}/audio', exist_ok=True)
pk = np.abs(mix).max(); mix *= .89 / pk
sf.write(f'{D}/audio/sfx_only.wav', mix, SR, subtype='PCM_24')
print('sfx_only.wav', round(len(mix) / SR, 2), 's; peak norm from', round(float(pk), 2))
