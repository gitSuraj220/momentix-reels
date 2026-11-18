"""SFX for the Dada ji Short (hand-synth, no BGM) + final mix to -14 LUFS.
Run after render.py: python3 sfx.py -> final/Dada_Dividend_Short.mp4"""
import numpy as np, subprocess, json, os
SR = 48000; END = 38.63; n = int((END + 0.5) * SR)
mix = np.zeros((n, 2)); rng = np.random.default_rng(11)

def env(N, a=.005, d=.3):
    t = np.arange(N) / SR; return np.minimum(1, t / a) * np.exp(-t / d)
def add(t, s, g=1.0, pan=0.0):
    i = int(t * SR); s = s[:max(0, n - i)]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    mix[i:i + len(s), 0] += s * g * l * 1.414; mix[i:i + len(s), 1] += s * g * r * 1.414
def lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); z = 0
    for i in range(len(x)): z = (1 - a) * x[i] + a * z; y[i] = z
    return y
def whoosh(d=.35, g=.3):
    N = int(d * SR); x = rng.standard_normal(N); t = np.arange(N) / SR
    fc = 500 + 4000 * np.sin(np.pi * t / d) ** 2; y = np.zeros(N); z = 0
    for i in range(N): a = np.exp(-2 * np.pi * fc[i] / SR); z = (1 - a) * x[i] + a * z; y[i] = z
    y -= np.convolve(y, np.ones(24) / 24, 'same')
    return y / np.abs(y).max() * np.sin(np.pi * t / d) ** 2 * g
def pop(f=700):
    N = int(.16 * SR); t = np.arange(N) / SR; fr = f * np.exp(-t * 20) + f * .5
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * env(N, .002, .045) * .55
def thud(g=.9):
    N = int(.5 * SR); t = np.arange(N) / SR
    return (np.sin(2 * np.pi * (55 + 70 * np.exp(-t * 28)) * t) * env(N, .002, .16) + rng.standard_normal(N) * env(N, .001, .015) * .3) * g
def impact(g=1.0):
    N = int(1.2 * SR); t = np.arange(N) / SR
    sub = np.sin(2 * np.pi * (40 + 80 * np.exp(-t * 10)) * t) * np.exp(-t / .45)
    crack = lp(rng.standard_normal(N), 3000) * np.exp(-t / .06) * 1.5
    return (sub + crack) * g
def riser(d=.8, g=.25):
    N = int(d * SR); t = np.arange(N) / SR; x = rng.standard_normal(N); y = np.zeros(N); z = 0
    for i in range(N): a = np.exp(-2 * np.pi * (300 + 5000 * (t[i] / d) ** 2) / SR); z = (1 - a) * x[i] + a * z; y[i] = z
    return y / np.abs(y).max() * (t / d) ** 2.2 * g
def kaching():
    N = int(1.0 * SR); t = np.arange(N) / SR
    bell = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t / d) for f, a, d in [(2637, 1, .35), (3520, .6, .3), (5274, .3, .2)])
    k = int(.07 * SR); b2 = np.zeros(N); t2 = t[:N - k]
    b2[k:] = sum(a * np.sin(2 * np.pi * f * t2) * np.exp(-t2 / d) for f, a, d in [(3136, 1, .45), (4186, .5, .3)])
    clank = lp(rng.standard_normal(N), 6000) * np.exp(-t / .03) * .8
    return (bell + b2) * .22 + clank * .35
def ping():
    N = int(.7 * SR); t = np.arange(N) / SR
    return (np.sin(2 * np.pi * 1760 * t) + .5 * np.sin(2 * np.pi * 2637 * t)) * env(N, .002, .18) * .3
def scribble(d):
    N = int(d * SR); t = np.arange(N) / SR; x = lp(rng.standard_normal(N), 4500) - lp(rng.standard_normal(N), 900)
    strokes = (np.sin(2 * np.pi * 5.5 * t + np.sin(t * 13)) > -.2).astype(float); strokes = lp(strokes, 40)
    return x * strokes * .5
def tick():
    N = int(.04 * SR); t = np.arange(N) / SR; return np.sin(2 * np.pi * 2300 * t) * env(N, .0005, .008) * .35
def shutter():
    N = int(.25 * SR); t = np.arange(N) / SR; x = rng.standard_normal(N)
    return x * (env(N, .0005, .01) + np.roll(env(N, .0005, .015), int(.07 * SR)) * .8) * .5
def zap():
    N = int(.5 * SR); t = np.arange(N) / SR
    return (np.sign(np.sin(2 * np.pi * (200 + 1800 * t) * t)) * .3 + lp(rng.standard_normal(N), 5000) * .7) * env(N, .003, .12) * .5
def tone_bed(t0, t1, kind, g):
    N = int((t1 - t0) * SR); t = np.arange(N) / SR; x = rng.standard_normal(N)
    if kind == 'room': y = lp(x, 300) * 1.5
    elif kind == 'park': y = lp(x, 1200) * .6 + sum(np.sin(2 * np.pi * f * t) * (np.sin(2 * np.pi * r * t) > .97) * .15 for f, r in [(3800, 1.3), (4400, .9), (5100, 1.7)])
    else: y = lp(x, 2500) * .25 + np.sin(2 * np.pi * 15734 * t) * .0
    ramp = np.minimum(1, t / .08) * np.minimum(1, (N / SR - t) / .08)
    return y * ramp * g

tl = {l['id']: l for l in json.load(open('timeline.json'))['lines']}
cuts = [3.0, 5.0, 6.1, 6.85, 9.95, 12.15, 13.9, 16.15, 19.6, 21.15, 24.65, 28.0, 36.05, 37.75]
for c in cuts: add(c - .18, whoosh(.34, .28), pan=rng.uniform(-.3, .3))
# room tone per scene
for a, b, k, g in [(0, 9.95, 'room', .02), (9.95, 12.15, 'park', .05), (12.15, 13.9, 'room', .02), (13.9, 30.35, 'room', .02), (36.05, END, 'room', .02)]:
    seg = tone_bed(a, b, k, g); add(a, seg)
# key-word pops / impacts
for t0, kind in [(1.45, 'pop'), (5.0, 'pop'), (8.9, 'pop'), (14.6, 'pop'), (23.7, 'pop'), (25.75, 'pop'), (29.55, 'pop')]:
    add(t0, pop(rng.uniform(600, 900)))
add(6.1, thud(1.0)); add(6.15, pop(1100), .8)                       # PENSION?
add(13.9, thud(.6))                                                  # Momo arms up
add(17.3, riser(.6, .22)); add(17.9, impact(.75)); add(17.9, kaching(), .8)   # DIVIDEND
add(20.5, zap(), 1.0); add(20.5, impact(.5))                          # OP!
add(3.25, kaching(), .9); add(37.85, ping(), 1.0); add(37.95, kaching(), .7)  # phone credited + loop ping
add(28.2, scribble(1.8), .5)                                          # pen ready
# stock card: slam in, scribble under VO, tick-tock, shutter on the way out
add(30.0, riser(.35, .2)); add(30.35, impact(.9)); add(30.36, whoosh(.3, .3))
add(30.6, scribble(4.2), .35)
for k in range(10): add(30.8 + k * .5, tick(), .8, pan=(-.3 if k % 2 else .3))
add(35.85, shutter(), 1.0)
add(36.6, impact(.6)); add(36.6, pop(800))                            # = DIVIDEND
# smoke + TV + park extras
add(9.95, lp(rng.standard_normal(int(1.2 * SR)), 900) * env(int(1.2 * SR), .3, .6) * .15)
add(12.2, lp(rng.standard_normal(int(1.6 * SR)), 1800) * .03)        # TV hiss
for k in range(3): add(12.4 + k * .45, pop(400 + 120 * k), .35)       # cartoon boings on TV
os.makedirs('final', exist_ok=True); os.makedirs('build', exist_ok=True)
sfx = mix[:int(END * SR)]
vo = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', 'vo/vo_full.wav', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                                  capture_output=True).stdout, np.float32)[:len(sfx)]
vo = np.pad(vo, (0, len(sfx) - len(vo)))
# duck SFX under voice
e = np.convolve(np.abs(vo), np.ones(2400) / 2400, 'same'); duck = 1 - np.clip(e / (e.max() * .25), 0, 1) * .45
out = sfx * duck[:, None] * .55 + vo[:, None] * 1.0
out = out / np.abs(out).max() * .95
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', 'build/mix_raw.wav'], input=out.astype(np.float32).tobytes())
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/mix_raw.wav', '-af', 'loudnorm=I=-14:TP=-2.2:LRA=9', '-ar', '48000', 'build/mix.wav'])
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/video_only.mp4', '-i', 'build/mix.wav', '-map', '0:v', '-map', '1:a',
                '-c:v', 'libx264', '-preset', 'slow', '-b:v', '10M', '-maxrate', '12M', '-bufsize', '20M', '-pix_fmt', 'yuv420p',
                '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', 'final/Dada_Dividend_Short.mp4'])
print('ok')
