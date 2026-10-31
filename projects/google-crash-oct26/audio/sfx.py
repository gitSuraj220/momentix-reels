"""Heavy cinematic SFX for the Google crash reel (Suraj: dramatic thriller). earshot bank; no continuous bed."""
import numpy as np, json, subprocess, sys
sys.path.insert(0, '/home/claude/momentix-reels/engine')
from audio_common import write_wav
from earshot_bank import bank
SR = 48000
CU = json.load(open('../vo/cues.json')); S = lambda i: CU[i]['s']; E = lambda i: CU[i]['e']
END = E(31) + 1.6
n = int(END * SR) + SR; mix = np.zeros((n, 2)); rng = np.random.default_rng(51)

def add(t, x, g=1.0, pan=0.0):
    i = max(0, int(t * SR)); x = np.asarray(x)[:max(0, n - i)]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    mix[i:i + len(x), 0] += x * g * l * 1.414; mix[i:i + len(x), 1] += x * g * r * 1.414

def trim(x, d, fade=.25):
    x = x[:int(d * SR)].copy(); F = int(fade * SR); x[-F:] *= np.linspace(1, 0, F); return x

def bp(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))

def scratch(d=.4, g=1.0):
    d = min(d, .5); N = int(d * SR); t = np.arange(N) / SR
    x = bp(rng.standard_normal(N), 2200, 6000) * (0.4 + 0.6 * np.abs(np.sin(2 * np.pi * 6 * t)) ** 1.5)
    x *= np.minimum(1, t / .03) * np.minimum(1, (d - t) / .07)
    return x / (np.abs(x).max() + 1e-9) * .09 * g

BOOM = lambda g=1.0: trim(bank('impact/deep'), 2.6, .9) * .55 * g
HIT = lambda g=1.0: bank('pro_impact/deep') * .45 * g
PUNCH = lambda g=1.0: bank('pro_impact/short') * .42 * g
SUB = lambda g=1.0: bank('cut_hit/sub') * .5 * g
KICK = lambda g=1.0: bank('cut_hit/kick') * .45 * g
GL = lambda g=1.0: bank('glitch/hit') * .18 * g
WH = lambda g=1.0: bank('whoosh_fast/crisp') * .22 * g
SINK = lambda d=1.2, g=1.0: bank('downlifter/sub_sink', dur=d) * .32 * g
FALL = lambda d=1.0, g=1.0: bank('downlifter/air_fall', dur=d) * .22 * g
RISE = lambda d=.8, g=1.0: bank('pro_riser/roll', dur=d) * .24 * g
POPK = lambda g=1.0: bank('pro_pop_in/knock') * .35 * g
TINK = lambda g=1.0: bank('pro_pop/tink') * .25 * g

cuts = [S(5), S(7), S(13), S(14), S(17), S(20), S(24), S(28), S(30)]
for c in cuts: add(c - .1 - .22, WH(), 1)

# A: hook — cliff + heartbeat under the 2008/Covid lines
add(0.30, FALL(0.7, 1.2), 1); add(0.95, BOOM(), 1); add(0.95, GL(), 1)
for k, tt in enumerate(np.arange(S(0) + .3, S(3) - .1, 0.82)):
    add(tt, KICK(.7), 1); add(tt + .16, KICK(.45), 1)
add(S(0) + .25, PUNCH(.8), 1, -.3); add(S(1), PUNCH(.8), 1, .3)
add(S(2) + .7, scratch(.3, 1.3), 1, -.3); add(S(2) + .95, scratch(.3, 1.3), 1, .3)
add(S(4) - .7, RISE(.7), 1); add(S(4) + .05, BOOM(1.1), 1); add(S(4) + .05, SUB(), 1)
# B: traders + money
add(S(5) + .35, HIT(), 1); add(S(5) + .35, SUB(.8), 1); add(S(6) + .55, PUNCH(), 1, .3)
# C: everything fell
for i in range(11): add(S(7) + .15 + i * .12, TINK(.35 + .03 * i), 1, -.5 + i * .1)
add(S(7) + .15, GL(1.2), 1); add(S(7) + .15, HIT(.8), 1)
add(S(9) - .05, FALL(1.0), 1); add(S(9) + .1, HIT(.85), 1); add(S(9) + .1, GL(), 1)
add(S(11) + .1, HIT(.85), 1); add(S(11) + .1, GL(), 1); add(S(12) + .4, SINK(1.2, .8), 1)
# D: AI bubble
add(S(13) - .5, RISE(.6), 1); add(S(13) + .25, BOOM(1.1), 1); add(S(13) + .7, scratch(.45), 1)
# E: report card
add(S(14), POPK(.8), 1); add(S(15) + .5, scratch(.35), 1); add(S(16) + .25, scratch(.4), 1)
add(S(16) + .95, HIT(.9), 1); add(S(16) + .95, SUB(.7), 1)
# F: reason 1
add(S(17) + .05, POPK(.7), 1); add(S(18) - .1, TINK(.6), 1); add(S(19) - .1, POPK(.8), 1)
add(S(19) + 1.4, RISE(.3), 1); add(S(19) + 1.7, PUNCH(), 1, .3)
# G: cash flow
add(S(20) - .1, TINK(.6), 1); add(S(21) - .05, scratch(.3), 1); add(S(21) + .6, scratch(.3), 1)
add(S(22) - .1, scratch(.3), 1); add(S(22) + .3, HIT(), 1); add(S(22) + .3, SUB(.7), 1); add(S(23) + .35, PUNCH(), 1, .2)
# H: search
add(S(24) - .1, TINK(.6), 1); add(S(26) - .05, POPK(.7), 1, -.3); add(S(27) - .2, POPK(.7), 1, .3)
for i in range(3): add(S(27) + .1 + i * .45, TINK(.5), 1, .3)
add(S(27) + 1.3, scratch(.4), 1, .3); add(S(27) + 1.3, SINK(1.0, .7), 1)
# I: sell everything
for i in range(4): add(S(28) + .1 + i * .18, PUNCH(.45), 1, -.4)
for i in range(4): add(S(29) + .1 + i * .12, WH(.5), 1, .2)
add(S(29) + .7, HIT(.9), 1, .3)
# J: ending
add(S(30) + .05, SUB(.7), 1); add(S(31) + 1.5, RISE(.4), 1); add(S(31) + 1.9, BOOM(1.2), 1); add(S(31) + 1.9, GL(), 1)

sfx = mix[:int(END * SR)]
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', '../vo/vo.wav', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
v = np.frombuffer(raw, dtype=np.float32)[:len(sfx)]
G = 0.45
out = sfx * G; out[:len(v), 0] += v; out[:len(v), 1] += v
np.clip(out, -1, 1, out); write_wav('premix.wav', out, SR); write_wav('sfx_only.wav', sfx * G, SR); print(round(END, 2))
