"""SFX for the IPO explainer reel. earshot bank first; no continuous bed (Suraj adds music)."""
import numpy as np, json, subprocess, sys
sys.path.insert(0, '/home/claude/momentix-reels/engine')
from audio_common import write_wav
from earshot_bank import bank
SR = 48000
CU = json.load(open('../vo/cues.json')); S = lambda i: CU[i]['s']; E = lambda i: CU[i]['e']
END = E(37) + 1.6
n = int(END * SR) + SR; mix = np.zeros((n, 2)); rng = np.random.default_rng(41)

def add(t, x, g=1.0, pan=0.0):
    i = int(t * SR); x = np.asarray(x)[:max(0, n - i)]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    mix[i:i + len(x), 0] += x * g * l * 1.414; mix[i:i + len(x), 1] += x * g * r * 1.414

def bp(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))

def scratch(d=.45, g=1.0):
    """soft pencil/marker stroke (capped, quiet: Suraj disliked buzz)"""
    d = min(d, .55); N = int(d * SR); t = np.arange(N) / SR
    x = bp(rng.standard_normal(N), 2200, 6000) * (0.4 + 0.6 * np.abs(np.sin(2 * np.pi * 6 * t)) ** 1.5)
    x *= np.minimum(1, t / .03) * np.minimum(1, (d - t) / .07)
    return x / (np.abs(x).max() + 1e-9) * .10 * g

def tape(g=1.0):
    """short tape rip"""
    N = int(.16 * SR); t = np.arange(N) / SR
    x = bp(rng.standard_normal(N), 900, 7000) * (rng.random(N) > .35) * np.exp(-t / .06)
    return x / (np.abs(x).max() + 1e-9) * .13 * g

land = lambda g=1.0: bank('pro_pop_in/airy') * .32 * g
knock = lambda g=1.0: bank('pro_pop_in/knock') * .38 * g
tink = lambda g=1.0: bank('pro_pop/tink') * .30 * g
hit = lambda g=1.0: bank('pro_impact/short') * .42 * g
air = lambda g=1.0: bank('pro_impact/air') * .38 * g
ding = lambda g=1.0: bank('pro_notify/ding_2045') * .32 * g
swoosh = lambda g=1.0: bank('whoosh_fast/crisp') * .20 * g

# scene cuts (same as reel.html W)
cuts = [S(4), S(9), S(13), S(16), S(20), S(24), S(31), S(33)]
for c in cuts: add(c - .15 - .22, swoosh(), 1)
# A: hook + tapri
add(0.05, land(), 1); add(0.55, scratch(.4), 1)
add(S(1) - .15, land(1.1), 1); add(S(1) + .05, tape(), 1, -.3); add(S(1) + .25, swoosh(.6), 1)
add(S(2) + .4, knock(), 1, .3); add(S(2) + .45, tape(.8), 1, .3)
for k in range(3): add(S(2) + .45 + k * .16, tink(.25), 1, .3)
add(S(3) + .5, tink(), 1, .3)
# B: money
add(S(4) + .35, knock(), 1, .3); add(S(5) - .05, land(), 1, .3); add(S(6) + .05, hit(), 1, .25)
add(S(7) + .55, air(), 1); add(S(8) + .02, scratch(.45, 1.2), 1)
# C: DRHP
add(S(9) - .1, tink(.5), 1); add(S(10) + .9, hit(.9), 1, .2); add(S(11) + .05, scratch(.4), 1)
for k in range(3): add(S(12) + k * .5, scratch(.33, .7), 1)
# D: price band
add(S(13) - .1, tink(.5), 1); add(S(14) - .05, land(), 1); add(S(15) - .25, land(.8), 1); add(S(15) + .3, scratch(.55), 1); add(S(15) + .8, scratch(.35), 1)
# E: bidding
add(S(16) - .1, tink(.5), 1)
for i in range(6): add(S(17) + .05 + i * .17, tink(.32 + .08 * (i % 2)), 1, -.4 if i % 2 == 0 else .4)
add(S(18) - .05, land(.8), 1, -.3); add(S(18) + .15, scratch(.45), 1, -.3)
add(S(19) + .25, knock(), 1, .3); add(S(19) + .75, scratch(.4), 1, .3); add(S(19) + 1.05, hit(), 1, .3)
# F: math
add(S(20) + .1, scratch(.35), 1); add(S(20) + .95, scratch(.35), 1); add(S(20) + 1.45, scratch(.3), 1)
add(S(21) + .3, scratch(.4), 1); add(S(21) + .4, land(), 1, -.3); add(S(21) + 1.0, knock(), 1, .3)
add(S(22) - .02, scratch(.3, 1.2), 1); add(S(23) + .55, hit(), 1, .2)
# G: Raju chart
add(S(26) + .55, bank('pro_riser/roll', dur=0.6) * .22, 1)
add(S(26) + 1.15, air(), 1); add(S(26) + 1.55, ding(), 1)
add(S(28), knock(.8), 1, -.3); add(S(29) + .1, hit(.7), 1, -.3); add(S(30) + .1, knock(.9), 1, .3)
# H: newspaper + cheer
add(S(31) - .1, tape(), 1); add(S(31) + .55, land(), 1); add(S(32) + .6, scratch(.45), 1)
# I: Jio chart
add(S(33) + 1.15, bank('pro_riser/roll', dur=0.6) * .22, 1)
add(S(33) + 1.75, air(), 1); add(S(34) + .05, ding(), 1)
add(S(35) + .2, knock(.8), 1, -.3); add(S(36) + .3, knock(.9), 1, .3)
add(E(37) + .1, bank('pro_shimmer/m3') * .22, 1)

sfx = mix[:int(END * SR)]
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', '../vo/vo.wav', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
v = np.frombuffer(raw, dtype=np.float32)[:len(sfx)]
G = 0.42
out = sfx * G; out[:len(v), 0] += v; out[:len(v), 1] += v
np.clip(out, -1, 1, out); write_wav('premix.wav', out, SR); write_wav('sfx_only.wav', sfx * G, SR); print(round(END, 2))
