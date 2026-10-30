"""SFX for the Dhanteras gold reel. No continuous bed (Suraj adds music)."""
import numpy as np, json, subprocess, sys
sys.path.insert(0, '/home/claude/momentix-reels/engine')
from audio_common import write_wav
SR = 48000
CU = json.load(open('../vo/cues.json')); S = lambda i: CU[i]['s']; E = lambda i: CU[i]['e']
END = E(27) + 1.6
src = open('/home/claude/momentix-reels/engine/audio_lib.py').read()
src = src.split("def env(", 1)[1]; src = "def env(" + src.split("def finish")[0]
src = "\n".join(l for l in src.split("\n") if not l.startswith("gl=lambda"))
n = int(END * SR) + SR; mix = np.zeros((n, 2)); rng = np.random.default_rng(31)
exec(src)

def bp(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))

def coin(g=1.0, f0=3100):
    """metallic coin clink"""
    N = int(.7 * SR); t = np.arange(N) / SR
    x = sum(a * np.sin(2 * np.pi * f0 * m * t) * np.exp(-t / d) for m, a, d in [(1, 1, .25), (1.51, .6, .18), (2.33, .4, .12), (3.1, .25, .08)])
    return x * np.minimum(1, t / .001) * .28 * g

def card_in(g=1.0):
    """paper slide: short soft swoosh + tap"""
    N = int(.32 * SR); t = np.arange(N) / SR
    sw = bp(rng.standard_normal(N), 600, 5000) * np.sin(np.pi * np.clip(t / .28, 0, 1)) ** 2
    return (sw / (np.abs(sw).max() + 1e-9) * .22 + np.concatenate([np.zeros(int(.25 * SR)), tap()])[:N] * .5) * g

def scratch(d=.5, g=1.0):
    d = min(d, .5); N = int(d * SR); t = np.arange(N) / SR
    x = bp(rng.standard_normal(N), 2200, 6000) * (0.4 + 0.6 * np.abs(np.sin(2 * np.pi * 7 * t)) ** 1.5)
    x *= np.minimum(1, t / .03) * np.minimum(1, (d - t) / .06)
    return x / (np.abs(x).max() + 1e-9) * .09 * g

def sizzle(d=1.4):
    N = int(d * SR); t = np.arange(N) / SR
    x = bp(rng.standard_normal(N), 1500, 9000) * (0.6 + 0.4 * rng.random(N) ** 6)
    return x / (np.abs(x).max() + 1e-9) * .14 * np.minimum(1, t / .15) * np.minimum(1, (d - t) / .3)

def splash():
    N = int(.8 * SR); t = np.arange(N) / SR
    x = bp(rng.standard_normal(N), 300, 4000) * np.exp(-t / .18)
    for _ in range(10):
        i = int(rng.uniform(.05, .5) * SR); L = int(.04 * SR); tt = np.arange(L) / SR
        x[i:i + L] += np.sin(2 * np.pi * rng.uniform(600, 1400) * tt * (1 + 3 * tt)) * np.exp(-tt / .02) * .3
    return x * .4

def ding(g=1.0):
    return ting() * .5 * g

# W starts (scene cuts)
W = [S(3) - .15, S(9) - .15, S(12) - .15, S(16) - .15, S(19) - .15, S(25) - .15]
add(0.0, coin(.8), 1, -.2); add(0.12, coin(.6, 3600), 1, .2)
for w in W: add(w - .2, whoosh(.45, True, .2), 1)
# S1
add(S(1) + .2, card_in(), 1); add(S(1) + .5, scratch(.6), 1); add(S(2) + .25, thud(), .7); add(S(2) + .3, coin(.7, 2400), 1); add(S(2) + .6, pop(700), .5)
# S2 melt
add(S(3) + .2, sizzle(2.0), 1); add(S(4) - .2, card_in(), 1); add(S(4), scratch(.6), 1); add(S(5), pop(1100), .5)
add(S(6) + .2, scratch(.5), 1); add(S(7) + .2, scratch(.35), 1); add(S(8) + .05, stampfx(), .8); add(S(8) + .1, coin(.5, 2000), 1)
# S3 scale
add(S(9) - .1, card_in(), 1); add(S(10) + .3, pop(600), .5); add(S(11) + .1, stampfx(), .9); add(S(11) + .15, failtone(), .35)
# S4 phone
add(S(12) - .1, splash(), 1); add(S(12) + .1, card_in(), 1); add(S(12) + .5, scratch(.6), 1); add(S(13), pop(900), .5); add(S(14), pop(800), .5)
add(S(15), coin(.6, 2600), 1)
# S5 ETF
add(S(16) + .1, card_in(), 1); add(S(17), pop(1000), .5); add(S(18), ding(1.0), 1); add(S(18) + .05, coin(.6, 3400), 1)
# S6 hero
add(S(19) - .05, scratch(.5), 1); add(S(20) - .05, rise(.8) * .5, 1); add(S(22) - .3, rise(.8) * .5, 1); add(S(24) - .3, rise(.8) * .5, 1)
add(S(20) + .75, pop(700), .5); add(S(22) + .5, pop(850), .5); add(S(24) + .5, ding(.9), 1)
# S7 ending
add(S(25) - .05, card_in(), 1); add(S(25) + .1, scratch(.5), 1); add(S(26) + .1, scratch(.5), 1); add(E(27) + .1, coin(.7), 1); add(E(27) + .25, coin(.5, 3700), 1)
sfx = mix[:int(END * SR)]
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', '../vo/vo.wav', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
v = np.frombuffer(raw, dtype=np.float32)[:len(sfx)]
G = 0.5
out = sfx * G; out[:len(v), 0] += v; out[:len(v), 1] += v
np.clip(out, -1, 1, out); write_wav('premix.wav', out, SR); write_wav('sfx_only.wav', sfx * G, SR); print(round(END, 2))
