"""SFX for the Room 3D reel (screen-demo). Cues mirror reel.html scene logic. VO duck, stems, mux."""
import sys, os, json, subprocess, numpy as np
from scipy.signal import butter, sosfilt
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'engine'))
from earshot_bank import bank
T = json.load(open('timeline.json'))['T']; END = T['end']
SR = 48000; n = int((END + 1) * SR); mix = np.zeros((n, 2))
def add(t, s, g=1.0, pan=0.0):
    i = max(0, int(t * SR)); s = np.asarray(s, float)[:max(0, n - i)]
    l, r = np.cos((pan + 1) * np.pi / 4) * 1.414, np.sin((pan + 1) * np.pi / 4) * 1.414
    mix[i:i + len(s), 0] += s * g * l; mix[i:i + len(s), 1] += s * g * r
lp = lambda x, f: sosfilt(butter(4, f, 'low', fs=SR, output='sos'), x)
def buzz():
    m = int(0.4 * SR); t = np.arange(m) / SR; x = np.zeros(m)
    for s0 in (0, 0.18):
        k = (t >= s0) & (t < s0 + 0.14); u = t[k] - s0; x[k] += (np.sin(2 * np.pi * 196 * u) + 0.4 * np.sin(2 * np.pi * 392 * u)) * np.minimum(1, u * 80) * np.minimum(1, (0.14 - u) * 80)
    return x * 0.6
def marker(d):  # marker strike scribble
    m = int(d * SR); t = np.arange(m) / SR; x = sosfilt(butter(4, [1500, 6000], 'band', fs=SR, output='sos'), np.random.default_rng(3).standard_normal(m))
    return x / np.abs(x).max() * np.sin(np.pi * t / d) ** 0.4
S = dict(photos=T['bas'] - 0.1, size=T['measuring'] - 0.12, browse=T['phir'] - 0.08, sofa=T['poocho'] - 0.1, color=T['room2'] - 0.1, layout=T['do'] - 0.12, table=T['size'] - 0.2, cta=T['comment'] - 0.12)
for i, (k, t0) in enumerate(S.items()): add(t0 - 0.25, bank('whoosh_fast/crisp'), 0.2, pan=.3 if i % 2 else -.3)
# hook
add(0.02, bank('ui_pop/soft'), 0.3); add(T['architect'] + 0.35, marker(0.5), 0.3); add(T['free'] - 0.05, bank('cut_hit/punch'), 0.5); add(T['free'], bank('pro_shimmer/m3'), 0.25)
# photos fan + Claude pill + 3D build
for i in range(3): add(T['bas'] + 0.05 + i * 0.28, bank('ui_pop/soft'), 0.35, pan=(i - 1) * 0.4)
add(T['claude'] - 0.05, bank('pro_pop_in/round'), 0.3); add(T['3d'] - 0.45, bank('pro_whoosh_big/swell'), 0.3); add(T['3d'] + 0.1, bank('pro_impact/air'), 0.3)
# size reading
add(T['darwaza'] - 0.05, bank('swish/soft'), 0.25); add(T['darwaza'] + 0.4, bank('pro_notify/ding_2045'), 0.3)
for i in range(4): add(T['andaza'] - 0.25 + i * 0.12, bank('pro_hover_tick/glass'), 0.25)
add(T['andaza'] + 0.25, bank('ui_pop/soft'), 0.3)
# browser: clicks + drags
for t0 in (T['bed'], T['almirah']): add(t0 - 0.02, bank('pro_click/snap'), 0.4); add(t0 + 0.05, bank('swish/flick'), 0.22)
add(T['full'] + 0.1, bank('whoosh_fast/crisp'), 0.15)
# sofa: typing, drop thud, checks
q = int((T['sofa'] - 0.2 - T['poocho']) / 0.06)
for i in range(q): add(T['poocho'] + i * 0.06, bank('pro_typing_key/soft', seed=i), 0.18)
add(T['sofa'] - 0.1, bank('swish/soft'), 0.25); add(T['sofa'] + 0.33, bank('knock/desk'), 0.45); add(T['sofa'] + 0.35, bank('cut_hit/kick'), 0.25)
add(T['deewar'] - 0.05, bank('pro_notify/ding_2296'), 0.3); add(T['darwaza2'] - 0.05, buzz(), 0.35); add(T['chalne'] - 0.05, bank('pro_notify/ding_2296'), 0.3)
add(T['check'] - 0.3, bank('pro_click/snap'), 0.35); add(T['check'] - 0.25, bank('swish/flick'), 0.2); add(T['check'] + 0.3, bank('mallet/marimba', pitch='C6'), 0.35)
# colours
for t0 in (T['sage'], T['peach']): add(t0 - 0.02, bank('pro_click/snap'), 0.35); add(t0 + 0.02, bank('reverse_swell/short'), 0.18)
# layouts
for t0 in (T['layout'] + 0.15, T['layout'] + 0.75): add(t0, bank('whoosh_fast/crisp'), 0.2)
# size table rows
for i in range(6): add(S['table'] + 0.15 + i * 0.13, bank('pro_hover_tick/glass'), 0.22)
add(T['size'] + 0.25, bank('pro_pop_in/double'), 0.25)
# CTA
add(S['cta'], bank('pro_impact/short'), 0.4)
for i in range(4): add(T['roomcta'] - 0.1 + i * 0.11, bank('pro_typing_key/soft', seed=10 + i), 0.35)
add(T['setup'] - 0.1, bank('pro_pop_in/round'), 0.3); add(T['dunga'], bank('mallet/flourish'), 0.25)
os.makedirs('final/stems', exist_ok=True)
sfx = mix[:int(END * SR)]
vo = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', 'vo/vo_full.wav', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout, np.float32)[:len(sfx)]
vo = np.pad(vo, (0, len(sfx) - len(vo)))
e = np.convolve(np.abs(vo), np.ones(2400) / 2400, 'same'); duck = 1 - np.clip(e / (e.max() * .25 + 1e-9), 0, 1) * .35
sfxd = sfx * duck[:, None] * .6; out = sfxd + vo[:, None]; g = .95 / (np.abs(out).max() + 1e-9)
w = lambda arr, ch, f: subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', str(ch), '-i', '-', f], input=arr.astype(np.float32).tobytes())
w(out * g, 2, 'build/mix_raw.wav'); w(vo * g, 1, 'final/stems/vo.wav'); w(sfxd * g, 2, 'final/stems/sfx.wav')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/mix_raw.wav', '-af', 'loudnorm=I=-13.6:TP=-2.2:LRA=11', '-ar', '48000', 'build/mix.wav'])
name = 'final/Room_3D_Claude.mp4'
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/video_only.mp4', '-i', 'build/mix.wav', '-map', '0:v', '-map', '1:a',
                '-c:v', 'libx264', '-preset', 'slow', '-b:v', '10M', '-minrate', '10M', '-maxrate', '10M', '-bufsize', '10M', '-x264-params', 'nal-hrd=cbr', '-pix_fmt', 'yuv420p', '-r', '30',
                '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', name])
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/video_only.mp4', '-c:v', 'copy', '-an', 'final/stems/video_only.mp4'])
print('ok', name)
