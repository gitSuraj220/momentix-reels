"""SFX for the Korea AI alarm reel. Cues mirror reel.html scene logic. VO duck, stems, mux.
usage: python3 sfx.py [preview_end_seconds]"""
import sys, os, json, subprocess, numpy as np
from scipy.signal import butter, sosfilt
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'engine'))
from earshot_bank import bank
TL = json.load(open('timeline.json')); T = TL['T']; W = TL['words']; END = T['end']
SR = 48000; n = int((END + 1) * SR); mix = np.zeros((n, 2)); rng = np.random.default_rng(7)
def add(t, s, g=1.0, pan=0.0):
    i = max(0, int(t * SR)); s = np.asarray(s, float)[:max(0, n - i)]
    l, r = np.cos((pan + 1) * np.pi / 4) * 1.414, np.sin((pan + 1) * np.pi / 4) * 1.414
    mix[i:i + len(s), 0] += s * g * l; mix[i:i + len(s), 1] += s * g * r
bp = lambda x, a, b: sosfilt(butter(4, [a, b], 'band', fs=SR, output='sos'), x)
lp = lambda x, f: sosfilt(butter(4, f, 'low', fs=SR, output='sos'), x)
def wt(w, after=0):
    for o in W:
        if o['s'] >= after and ''.join(c for c in o['w'].lower() if c.isalnum()) == w: return o['s']
    return after
# ---- code-made sounds ----
def clang(seed):  # steel thali hit by a spoon: inharmonic modes, fast attack
    r = np.random.default_rng(seed); d = 0.9; t = np.arange(int(d * SR)) / SR; f0 = r.uniform(420, 560); x = np.zeros_like(t)
    for k, (m, a, dec) in enumerate([(1, 1, 3.2), (2.32, .7, 4.5), (4.25, .5, 6), (6.63, .35, 8), (9.38, .25, 11), (12.6, .15, 14)]):
        x += a * np.sin(2 * np.pi * f0 * m * (1 + r.uniform(-.004, .004)) * t + r.uniform(0, 6)) * np.exp(-dec * t)
    x += 0.6 * bp(r.standard_normal(len(t)), 2500, 9000) * np.exp(-60 * t)
    return x / np.abs(x).max()
def alert(d, muffle=False):  # harsh two-tone emergency alert with tremolo
    t = np.arange(int(d * SR)) / SR; f = np.where((t * 4).astype(int) % 2 == 0, 880, 1046)
    ph = 2 * np.pi * np.cumsum(f) / SR; x = np.tanh(2.2 * (np.sin(ph) + 0.35 * np.sin(2 * ph) + 0.2 * np.sin(3 * ph)))
    x *= 0.8 + 0.2 * np.sin(2 * np.pi * 12 * t); x *= np.minimum(1, t * 200) * np.minimum(1, (d - t) * 60)
    if muffle: x = lp(x, 1200) * 1.6
    return x / np.abs(x).max()
def vibe(d):  # phone vibration buzz
    t = np.arange(int(d * SR)) / SR; x = np.sin(2 * np.pi * 150 * t) * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 2.5 * t)))
    x += 0.3 * bp(rng.standard_normal(len(t)), 120, 400); return x * np.minimum(1, t * 50) * np.minimum(1, (d - t) * 50) / 1.4
def wail(d):  # siren sweep
    t = np.arange(int(d * SR)) / SR; f = 750 + 380 * np.sin(2 * np.pi * 0.9 * t); x = np.tanh(1.5 * np.sin(2 * np.pi * np.cumsum(f) / SR))
    return x * np.minimum(1, t * 8) * np.minimum(1, (d - t) * 8)
def counter(d, k):  # fast ticking counter
    x = np.zeros(int(d * SR)); tk = bank('pro_hover_tick/glass')
    for i in range(k):
        j = int(d * SR * (1 - (1 - i / k) ** 2)); s = tk[:len(x) - j]; x[j:j + len(s)] += s * 0.6
    return x
# ---- cue list ----
CUTS = [T[k] for k in ('sarkar1', 'korea', 'scene', 'chhupe', 'iske', 'nov', 'sarkar3', 'jinhone', 'unchaas', 'ek', 'ab', 'india')]
for i, c in enumerate(CUTS): add(c - 0.22, bank('whoosh_fast/crisp' if i % 2 else 'whoosh_fast/tight'), 0.22, pan=.3 if i % 2 else -.3)
# A thali clangs (match glints in reel.html)
gl = [0.15 + i * 0.22 for i in range(8)]; pans = [-.6, -.3, -.5, -.4, -.7, .1, .3, .5]
for i, g in enumerate(gl):
    tt = g
    while tt < T['sarkar1'] - 0.1: add(tt, clang(i * 7 + int(tt * 10)), 0.22 if tt == g else 0.14, pans[i]); tt += 0.7
add(0.35, bank('ui_pop/soft'), 0.25)
# B phone alert: vibration + alert until 'Yaad' (hard stop = silence beat)
a0, a1 = T['phones'] - 0.3, T['yaad'] - 0.05
add(T['sarkar1'] + 0.05, bank('swish/soft'), 0.25); add(a0, alert(a1 - a0), 0.30); add(a0, vibe(a1 - a0), 0.35)
add(T['yaad'] + 0.02, bank('impact/punch'), 0.4); add(T['yaad'], bank('cut_hit/sub'), 0.3)
# C map
add(T['korea'] + 0.1, bank('pro_zip/up'), 0.25)
for i in range(3): add(T['korea'] + 0.7 + i * 0.4, bank('pro_pop/thup'), 0.18)
for i in range(12): add(T['korea'] + 0.75 + i * 0.07, bank('pro_hover_tick/ping'), 0.12, pan=(i % 5 - 2) * .2)
add(T['smart'], bank('toggle/latch'), 0.4); add(T['smart'] + 0.15, bank('pro_impact/short'), 0.3)
# D rank board
for i in range(5): add(T['scene'] + 0.1 + i * 0.12, bank('ui_pop/step'), 0.2, pan=(i - 2) * .15)
add(T['rank'] - 0.1, bank('pro_shimmer/m2'), 0.25); ct = wt('cheat', T['rank'])
add(ct - 0.05, bank('impact/punch'), 0.5); add(ct - 0.05, bank('cut_hit/kick'), 0.3); add(T['scene'] + 1.4, bank('pro_pop_in/round'), 0.2)
# E method
add(T['chhupe'], bank('pro_pop_in/knock'), 0.3); add(wt('photo', T['chhupe']), bank('shutter/snap'), 0.45)
add(T['ai1'] - 0.3, bank('pro_zip/up_hi'), 0.2); add(T['ai1'] - 0.05, bank('glitch/data'), 0.3)
add(T['answer'] - 0.3, bank('pro_zip/up_hi'), 0.2); add(T['answer'] + 0.15, bank('pro_notify/ding_2167'), 0.35)
# F siren
add(T['iske'], bank('whoosh_big/thump'), 0.35); add(T['iske'], wail(T['nov'] - T['iske'] + 0.1), 0.16); add(T['alert'] - 0.1, bank('impact/punch'), 0.45)
# G exam hall
add(T['nov'] + 0.05, bank('pro_pop_in/round'), 0.25); add(T['paanch'] - 0.1, counter(0.9, 18), 0.35); add(T['paanch'] + 0.8, bank('cut_hit/punch'), 0.3)
add(T['college'] - 0.05, bank('pro_pop_in/airy'), 0.22)
# H nationwide alarm
add(T['alarm'] - 0.1, alert(T['teen'] - T['alarm'] - 0.1), 0.22); add(T['alarm'] - 0.1, vibe(T['teen'] - T['alarm']), 0.25)
tb = wt('baar', T['teen'])
for k in range(3): add(T['teen'] + k * (tb - T['teen'] + 0.12) / 2, bank('cut_hit/punch'), 0.4); add(T['teen'] + k * (tb - T['teen'] + 0.12) / 2, alert(0.18), 0.12)
add(T['silent'] - 0.05, bank('toggle/off'), 0.4)
tp = wt('phones', T['sarkar3']) - 0.1
for i in range(8): add(tp + i * 0.1, bank('pro_hover_tick/soft'), 0.12, pan=(i - 3.5) * .2)
# I bag
add(T['bag'] - 0.1, vibe(T['unchaas'] - T['bag']), 0.4); add(T['bag'] - 0.1, alert(T['literally'] - T['bag'] + 0.1, muffle=True), 0.3)
add(T['literally'] - 0.05, bank('shutter/dslr'), 0.45); add(T['literally'] + 0.05, bank('pro_notify/ding_1930'), 0.15)
add(wt('four', T['literally']) - 0.05, bank('impact/punch'), 0.45)
# J 49 counter
add(T['unchaas'] - 0.05, counter(0.65, 24), 0.35); add(T['unchaas'] + 0.6, bank('cut_hit/kick'), 0.35)
# K jacket blueprint
add(T['ek'] - 0.05, bank('swipe/paper'), 0.3); ctm = wt('camera', T['ek'])
add(ctm, bank('pro_pop_in/double'), 0.3); add(T['earphones'] - 0.4, bank('pro_zip/up'), 0.22); add(T['earphones'] + 0.05, bank('pro_pop_in/round'), 0.28)
# L AI data
add(T['ab'] - 0.05, bank('pro_pop_in/deep'), 0.3)
for i in range(4): add(T['companies'] - 0.2 + i * 0.1, bank('ui_pop/blip'), 0.22, pan=(i - 1.5) * .3)
add(T['data'] - 0.9, bank('swipe/paper'), 0.3); add(T['data'] + 0.1, bank('impact/punch'), 0.4)
# M India + loop back
add(T['india'] + 0.05, bank('swish/soft'), 0.25); add(T['disaster'] - 0.2, alert(0.9), 0.18); add(T['disaster'] - 0.2, vibe(0.9), 0.2)
add(END - 0.5, bank('reverse_swell/short'), 0.2)
# ---- mix ----
PREV = float(sys.argv[1]) if len(sys.argv) > 1 else None
os.makedirs('final/stems', exist_ok=True); os.makedirs('build', exist_ok=True)
sfx = mix[:int(END * SR)]
vo = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', 'vo/vo_full.wav', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout, np.float32)[:len(sfx)]
vo = np.pad(vo, (0, len(sfx) - len(vo)))
e = np.convolve(np.abs(vo), np.ones(2400) / 2400, 'same'); duck = 1 - np.clip(e / (e.max() * .25 + 1e-9), 0, 1) * .4
sfxd = sfx * duck[:, None] * .6; out = sfxd + vo[:, None]; g = .95 / (np.abs(out).max() + 1e-9)
w = lambda arr, ch, f: subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', str(ch), '-i', '-', f], input=arr.astype(np.float32).tobytes())
w(out * g, 2, 'build/mix_raw.wav')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/mix_raw.wav', '-af', 'loudnorm=I=-13.6:TP=-2.2:LRA=11', '-ar', '48000', 'build/mix.wav'])
if PREV:
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/video_only.mp4', '-i', 'build/mix.wav', '-t', str(PREV), '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'medium', '-b:v', '10M', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', 'final/hook_preview.mp4'])
    print('preview ok'); sys.exit()
w(vo * g, 1, 'final/stems/vo.wav'); w(sfxd * g, 2, 'final/stems/sfx.wav')
name = 'final/Korea_AI_Alarm.mp4'
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/video_only.mp4', '-i', 'build/mix.wav', '-map', '0:v', '-map', '1:a',
                '-c:v', 'libx264', '-preset', 'slow', '-b:v', '10M', '-minrate', '10M', '-maxrate', '10M', '-bufsize', '10M', '-x264-params', 'nal-hrd=cbr', '-pix_fmt', 'yuv420p', '-r', '30',
                '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', name])
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/video_only.mp4', '-c:v', 'copy', '-an', 'final/stems/video_only.mp4'])
print('ok', name)
