import numpy as np, json, subprocess, sys
sys.path.insert(0, '/home/claude/momentix-reels/engine')
from audio_common import write_wav
SR = 48000
CU = json.load(open('../vo/cues.json')); S = lambda i: [c for c in CU if c['id'] == i][0]['s']; E = lambda i: [c for c in CU if c['id'] == i][0]['e']
END = E('c31') + 1.6
src = open('/home/claude/momentix-reels/engine/audio_lib.py').read()
src = src.split("def env(", 1)[1]; src = "def env(" + src.split("def finish")[0]
src = "\n".join(l for l in src.split("\n") if not l.startswith("gl=lambda"))
n = int(END * SR) + SR; mix = np.zeros((n, 2)); rng = np.random.default_rng(21)
exec(src)

def bp(x, lo, hi):  # crude band-pass via FFT
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))

def pencil(d=0.7, g=1.0):
    """graphite scratch: band-passed noise, stroke rhythm ~7 Hz"""
    N = int(d * SR); t = np.arange(N) / SR
    x = bp(rng.standard_normal(N), 1800, 7500)
    strokes = 0.35 + 0.65 * np.abs(np.sin(2 * np.pi * rng.uniform(5.5, 8) * t + rng.uniform(0, 3))) ** 1.5
    e = np.minimum(1, t / .04) * np.minimum(1, (d - t) / .08)
    x = x * strokes * e
    return x / (np.abs(x).max() + 1e-9) * .22 * g

def flip(g=1.0):
    """page turn: soft swoosh + paper crinkle"""
    N = int(.55 * SR); t = np.arange(N) / SR
    sw = bp(rng.standard_normal(N), 400, 5000) * np.sin(np.pi * np.clip(t / .45, 0, 1)) ** 2
    cr = np.zeros(N)
    for _ in range(14):
        i = int(rng.uniform(.05, .4) * SR); L = int(.015 * SR); cr[i:i + L] += bp(rng.standard_normal(L), 2500, 9000)[:N - i] * rng.uniform(.3, 1)
    x = sw / (np.abs(sw).max() + 1e-9) * .5 + cr * .35
    return x * .3 * g

def soft_pop(f=700, g=1.0):
    return pop(f) * .6 * g

def counter(d=1.2, g=1.0):
    out = np.zeros(int(d * SR)); k = 0; t = 0.0
    while t < d - .05:
        i = int(t * SR); x = tick(); out[i:i + len(x)] += x[:len(out) - i] * .35; k += 1; t += .05 + .06 * (t / d) ** 2
    return out * g

def paper_thud():
    N = int(.35 * SR); t = np.arange(N) / SR
    return (np.sin(2 * np.pi * 85 * t) * np.exp(-t / .07) * .7 + bp(rng.standard_normal(N), 200, 2000) * np.exp(-t / .04) * .4) * .7

def bed(d):
    """very soft room tone + slow pad so silences aren't dead (Suraj adds music later)"""
    N = int(d * SR); t = np.arange(N) / SR
    pad = sum(np.sin(2 * np.pi * f * t + p) * a for f, a, p in [(110, .5, 0), (164.8, .3, 1), (220, .25, 2), (277.2, .12, .5)])
    pad *= (0.75 + 0.25 * np.sin(2 * np.pi * .07 * t))
    room = bp(rng.standard_normal(N), 100, 1200) * .15
    return (pad * .035 + room * .06) * np.minimum(1, t / 1.5) * np.minimum(1, (d - t) / 1.5)

add(0, bed(END), 1.0)
# scene starts (page flips)
W = {'s2': S('c1') - .12, 's3': S('c4') - .18, 's4': S('c7') - .18, 's5': S('c9') - .18, 's6': S('c11') - .18, 's7': S('c15') - .18,
     's8': S('c19') - .18, 's9': S('c21') - .12, 's10': S('c22') - .18, 's11': S('c29') - .18}
for k, v in W.items(): add(v - .15, flip(), 1.0, pan=rng.uniform(-.3, .3))
# S1
add(0.1, pencil(.7), 1, -.2); add(S('c0') + 1.6, pencil(.7, 1.1), 1, .2); add(S('c0') + 2.2, pencil(.5, .8), 1)
# S2
add(S('c1') - .05, soft_pop(600), 1); add(S('c2') - .1, pencil(.6), 1); add(S('c2'), soft_pop(500), .8)
add(S('c3') - .1, whoosh(.4, False, .18)); add(S('c3') + .15, ting(), .35); add(S('c3') + .25, paper_thud(), .7)
# S3
add(S('c4') + .3, pencil(1.0), 1); add(S('c5') - .1, pencil(1.3, 1.1), 1); add(S('c5') - .1, counter(1.3), .8); add(S('c6'), soft_pop(900), 1); add(S('c6') + .05, ting(), .3)
# S4
add(W['s4'] + .15, pencil(.6), 1); add(S('c8') - .2, whoosh(.5, True, .2)); add(S('c8'), pencil(.6), 1)
# S5
add(S('c9') + .4, pencil(1.2), 1); add(S('c10') + .3, pencil(1.1), 1); add(S('c9') + 1.8, soft_pop(1000), 1)
# S6
add(S('c11') - .05, pencil(.5), 1); add(S('c12'), pencil(.6), 1); add(S('c12') + .1, pencil(1.6, 1.2), 1, .1)
add(S('c13') + .3, soft_pop(1200), 1); add(S('c14') + .1, paper_thud(), .8); add(S('c14') + .1, soft_pop(450), .8)
# S7
add(S('c15') - .05, pencil(.6), 1); add(S('c16'), pencil(1.2, .9), 1); add(S('c17') + .3, pencil(1.2, .9), 1); add(S('c18'), soft_pop(800), 1); add(S('c18') + .05, ting(), .3)
# S8 / S9
add(S('c19') + .1, pencil(.8), 1); add(S('c19') + .8, pencil(.4, .7), 1); add(S('c20') - .15, pencil(.6), 1); add(S('c20') + .2, soft_pop(1000), 1)
add(S('c21'), paper_thud(), .7); add(S('c21') + .05, whoosh(.5, False, .14))
# S10
add(S('c22') - .05, pencil(.6), 1); add(S('c23') - .05, stampfx(), .9); add(S('c23') + .1, pencil(.45, 1.1), 1)
add(S('c24'), pencil(.6), 1)
for i in range(32): add(S('c24') + .3 + i * .04, soft_pop(600 + 25 * (i % 8), .45), .7, pan=-.4 + .8 * (i % 8) / 7)
add(S('c26') - .1, soft_pop(500), 1); add(S('c26') + .2, pencil(.5), 1)
add(S('c27') - .05, pencil(.55, 1.1), 1); add(S('c27') + .45, pencil(.3, .8), 1); add(S('c28') - .05, pencil(.55, 1.1), 1); add(S('c28') + .3, ting(), .3)
# S11
add(S('c29') - .05, pencil(.7), 1); add(S('c30'), pencil(.9, 1.0), 1); add(E('c31') + .2, ting(), .25)
sfx = mix[:int(END * SR)]
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', '../vo/vo.wav', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
v = np.frombuffer(raw, dtype=np.float32)[:len(sfx)]
G = 0.5
out = sfx * G; out[:len(v), 0] += v; out[:len(v), 1] += v
np.clip(out, -1, 1, out); write_wav('premix.wav', out, SR); write_wav('sfx_only.wav', sfx * G, SR); print(round(END, 2))
