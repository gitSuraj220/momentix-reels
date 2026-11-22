"""SFX for the GTA6 supercar reel, cued from timeline.json; VO ducking; stems; mux.
Music: Suraj adds it himself -> deliver final (VO+SFX) + stems (vo.wav, sfx.wav, video_only.mp4).
usage: python3 sfx.py [--novo]"""
import sys, os, json, subprocess, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'engine'))
from earshot_bank import bank
TL = json.load(open('timeline.json')); T = TL['T']; END = T['end']; NOVO = '--novo' in sys.argv or not os.path.exists('vo/vo_full.wav')
SR = 48000; n = int((END + 1) * SR); mix = np.zeros((n, 2))
def L(name): return np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', f'sfx_lib/{name}.wav', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout, np.float32)
LIB = {k[:-4]: L(k[:-4]) for k in os.listdir('sfx_lib') if k.endswith('.wav')}
def add(t, s, g=1.0, pan=0.0, fade=None):
    i = max(0, int(t * SR)); s = s[:max(0, n - i)].astype(float).copy()
    if fade: s *= np.interp(np.arange(len(s)) / SR, [0, fade[0], fade[1], fade[1] + 0.01], [0, 1, 1, 0])
    l, r = np.cos((pan + 1) * np.pi / 4) * 1.414, np.sin((pan + 1) * np.pi / 4) * 1.414
    mix[i:i + len(s), 0] += s * g * l; mix[i:i + len(s), 1] += s * g * r
tSmash = T['glass'] + 0.32
B = dict(press=tSmash + 0.75, hero=T['aur'], retro=T['purane'], xray=T['wajah'], two=T['isliye'], clone=T['cloner'] - 0.45, run=T['engine'],
         chase=T['police'], pas=T['main'], track=T['kyunki'], map=T['matlab'], heat=T['heat'], garage=T['basically'])
# cut whooshes on every shot change
for i, (k, c) in enumerate(B.items()):
    big = k in ('hero', 'chase', 'garage', 'xray')
    add(c - (0.42 if big else 0.3), bank('pro_whoosh_big/swell' if big else 'whoosh_fast/crisp'), 0.3 if big else 0.22, pan=-.3 if i % 2 else .3)
# 1 hook: rain bed only under the hook, glass smash, flash
add(0, LIB['rain'], 0.10, fade=(0.05, tSmash + 0.6)); add(tSmash - 0.03, LIB['glass'], 0.95, 0.15); add(tSmash, bank('pro_impact/short'), 0.45)
# press -> fail buzz x blink; WON'T START slam
tp = T['phir'] + 0.25; add(tp - 0.01, bank('pro_click/snap'), 0.5); add(tp + 0.02, LIB['startfail'], 0.55)
add(T['nahi'] - 0.05, bank('pro_impact/deep'), 0.65); add(T['nahi'] - 0.03, LIB['sub'], 0.35)
# hero: headlight flick + shimmer
add(T['next'] - 0.1, bank('pro_click/snap'), 0.35); add(T['next'], bank('pro_shimmer/m3') if True else None, 0.25)
# retro: 8-bit-ish blips, press, success, glitch to modern, stamp
add(T['button'] - 0.15, bank('pro_pop_in/round'), 0.35); add(T['button'] + 0.2, bank('pro_typing_key/blip'), 0.6)
add(T['tumhari'] - 0.1, bank('pro_notify/ding_2045'), 0.4); add(T['gta2'] - 0.05, bank('pro_glitch/fastroll'), 0.4)
add(T['khatam'] - 0.05, bank('pro_impact/short'), 0.6); add(T['khatam'], bank('pro_pop_in/double'), 0.35)
# x-ray: labels pop, pulses tick, fail
for k in ('wajah', 'immobilizer', 'computer', 'chaabi'): add(T[k] + (0.25 if k == 'wajah' else -0.1), bank('pro_pop_in/airy'), 0.3)
for k in range(int((T['code'] - T['andar2']) / 0.35)): add(T['andar2'] + k * 0.35, bank('pro_hover_tick/glass'), 0.18, pan=np.sin(k) * .3)
add(T['code'] - 0.02, LIB['startfail'], 0.5); add(T['fuel'], bank('pro_sub_drop/quick'), 0.45)
add(T['game'] - 0.05, bank('pro_impact/deep'), 0.7); add(T['game'] - 0.03, LIB['sub'], 0.4)
# two cars: hotwire sparks + easy tick; keyless label
for k in range(5): add(T['hotwire'] + k * 0.11, bank('pro_typing_key/crackle'), 0.35, pan=-.3)
add(T['easy'] - 0.1, bank('pro_notify/ding_2296'), 0.4); add(T['mehengi'] - 0.1, bank('pro_pop_in/knock'), 0.35)
# key cloner scan chirps -> cloned
for k in range(int((T['engine'] - 0.35 - B['clone']) / 0.18)): add(B['clone'] + 0.1 + k * 0.18, LIB['scan'], 0.18)
add(T['engine'] - 0.38, bank('pro_notify/ding_2045'), 0.4)
# engine on: press + engine start; RUNNING slam
add(T['engine'] - 0.06, bank('pro_click/snap'), 0.45); add(T['engine'] - 0.55, LIB['enginestart'], 0.55)
add(T['engine'] + 0.05, bank('pro_impact/short'), 0.45)
# chase: rev away + chirp + far sirens fading
add(T['police'] - 0.1, LIB['chirp'], 0.35); add(T['police'] - 0.05, LIB['revaway'], 0.55)
add(T['police'], LIB['siren_far'], 0.22, fade=(0.3, T['main'] - T['police'] + 0.6))
# pass: low whoosh as car passes; dikkat = sub drop + silence
add(T['main'] + 0.6, bank('pro_whoosh_big/swell'), 0.35); add(T['dikkat'] - 0.05, bank('pro_sub_drop/low'), 0.55)
# tracker: blips; map pings
for k in range(int((T['matlab'] - T['tracker']) / 0.5)): add(T['tracker'] + k * 0.5, bank('pro_hover_tick/ping'), 0.3)
for k in range(int((T['heat'] - T['matlab']) / 0.9) + 1): add(T['matlab'] + 0.1 + k * 0.9, LIB['ping'], 0.3)
# heat: outline hum swell + label pops + scary glitch
add(T['heat'] + 0.1, bank('reverse_swell/dark'), 0.3)
for k in ('kapde', 'look'): add(T[k] - 0.1, bank('pro_pop_in/airy'), 0.3)
add(T['heat'] + 0.3, bank('pro_pop_in/airy'), 0.3); add(T['lowkey'] - 0.05, bank('pro_glitch/crunchy'), 0.3)
# garage: headlights, police roll in with siren, WORST CAR slam, end
add(T['fast'] - 0.1, bank('pro_click/snap'), 0.3); add(T['bekaar'] - 0.5, LIB['siren'], 0.38, fade=(0.2, END - T['bekaar'] + 0.5))
add(T['bekaar'] + 0.12, bank('pro_impact/deep'), 0.75); add(T['bekaar'] + 0.14, LIB['sub'], 0.4); add(T['nocap'] - 0.05, bank('pro_impact/air'), 0.4)

os.makedirs('final/stems', exist_ok=True); os.makedirs('build', exist_ok=True)
sfx = mix[:int(END * SR)]
if NOVO: vo = np.zeros(len(sfx))
else:
    vo = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', 'vo/vo_full.wav', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout, np.float32)[:len(sfx)]
    vo = np.pad(vo, (0, len(sfx) - len(vo)))
e = np.convolve(np.abs(vo), np.ones(2400) / 2400, 'same'); duck = 1 - np.clip(e / (e.max() * .25 + 1e-9), 0, 1) * .4
sfxd = sfx * duck[:, None] * .6; out = sfxd + vo[:, None]; g = .95 / (np.abs(out).max() + 1e-9)
w = lambda arr, ch, f: subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', str(ch), '-i', '-', f], input=arr.astype(np.float32).tobytes())
w(sfx, 2, 'build/sfx_only.wav'); w(out * g, 2, 'build/mix_raw.wav')
w(vo * g, 1, 'final/stems/vo.wav'); w(sfxd * g, 2, 'final/stems/sfx.wav')
target = '-16' if NOVO else '-12.8'
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/mix_raw.wav', '-af', f'loudnorm=I={target}:TP=-2.2:LRA=11', '-ar', '48000', 'build/mix.wav'])
name = 'final/GTA6_Supercar_DRAFT_novoice.mp4' if NOVO else 'final/GTA6_Supercar.mp4'
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/video_only.mp4', '-i', 'build/mix.wav', '-map', '0:v', '-map', '1:a',
                '-c:v', 'libx264', '-preset', 'slow', '-b:v', '10M', '-minrate', '10M', '-maxrate', '10M', '-bufsize', '10M', '-x264-params', 'nal-hrd=cbr', '-pix_fmt', 'yuv420p',
                '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', name])
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/video_only.mp4', '-c:v', 'copy', '-an', 'final/stems/video_only.mp4'])
print('ok', name)
