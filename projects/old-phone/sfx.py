"""Heavy cinematic SFX from the earshot bank (no beds/hum) + mix to -14 LUFS -> final/Old_Phone_Desk_Panel.mp4"""
import sys, os, subprocess, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'engine'))
from earshot_bank import bank
SR = 48000; END = 21.8; n = int((END + 1) * SR); mix = np.zeros((n, 2))
def add(t, s, g=1.0, pan=0.0):
    i = int(t * SR); s = s[:max(0, n - i)]
    l, r = np.cos((pan + 1) * np.pi / 4) * 1.414, np.sin((pan + 1) * np.pi / 4) * 1.414
    mix[i:i + len(s), 0] += s * g * l; mix[i:i + len(s), 1] += s * g * r

CUTS = [2.42, 6.22, 10.3, 12.15, 14.95, 17.88, 19.7]
BIG = {6.22, 17.88}
for i, c in enumerate(CUTS):
    if c in BIG: add(c - 0.42, bank('pro_whoosh_big/swell'), .38, pan=(-.3 if i % 2 else .3))
    else: add(c - 0.36, bank('whoosh_fast/crisp'), .28, pan=(-.4 if i % 2 else .4))
# A hook: throw, STOP freeze, rewind
add(0.0, bank('pro_impact/air'), .4); add(0.15, bank('whoosh_fast/crisp'), .3, pan=.3)
add(1.2, bank('pro_impact/deep'), .75); add(1.22, bank('pro_pop_in/double'), .45)
add(1.86, bank('whoosh_fast/reverse'), .4)
# B: USB + Claude link/prompt + DONE
add(2.5, bank('pro_pop_in/round'), .3); add(3.55, bank('pro_click/snap'), .65)
add(4.04, bank('ui_pop/wide'), .4); add(4.48, bank('pro_pop/tink'), .35); add(5.08, bank('pro_pop/tink'), .35)
add(5.5, bank('pro_click/snap'), .45); add(5.64, bank('pro_impact/deep'), .7); add(5.66, bank('pro_notify/ding_2296'), .35)
# C: panel boots, widgets
add(6.55, bank('pro_shimmer/m3'), .3); add(7.8, bank('pro_pop_in/knock'), .4)
for k in range(4): add(8.0 + k * 0.12, bank('pro_click/snap'), .25, pan=(-.3 + .2 * k))
add(8.5, bank('ui_pop/wide'), .35); add(9.16, bank('pro_pop_in/airy'), .35)
add(9.58, bank('pro_impact/short'), .6); add(9.6, bank('pro_pop_in/double'), .4)
# D: music skip + volume
add(11.06, bank('pro_click/snap'), .55); add(11.08, bank('pro_pop/tink'), .3); add(11.5, bank('pro_click/snap'), .45)
# E: permission Allow
add(13.7, bank('pro_click/snap'), .6); add(13.72, bank('pro_notify/ding_2045'), .4); add(14.32, bank('pro_pop/tink'), .3)
# F: limit ring + LIVE
add(15.5, bank('pro_riser/roll', dur=1.0), .26); add(16.6, bank('pro_impact/air'), .4); add(17.22, bank('pro_notify/ding_1930'), .35)
# G: widget wall + 124 + 30 pages
for k in range(6): add(17.96 + k * 0.11, bank('ui_pop/wide'), .22, pan=(-.4 + .16 * k))
add(18.7, bank('pro_impact/short'), .55); add(18.8, bank('pro_pop_in/double'), .4)
# H: typing PHONE + send
for k in range(5): add(20.55 + k * 0.08, bank('pro_click/snap'), .3, pan=(.1 * k - .2))
add(21.35, bank('pro_click/snap'), .55); add(21.37, bank('pro_notify/ding_2296'), .4)

os.makedirs('final', exist_ok=True); os.makedirs('build', exist_ok=True)
sfx = mix[:int(END * SR)]
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', 'build/sfx_only.wav'], input=sfx.astype(np.float32).tobytes())
vo = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', 'vo/vo_full.wav', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                                  capture_output=True).stdout, np.float32)[:len(sfx)]
vo = np.pad(vo, (0, len(sfx) - len(vo)))
e = np.convolve(np.abs(vo), np.ones(2400) / 2400, 'same'); duck = 1 - np.clip(e / (e.max() * .25), 0, 1) * .4
out = sfx * duck[:, None] * .6 + vo[:, None]
out = out / np.abs(out).max() * .95
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', 'build/mix_raw.wav'], input=out.astype(np.float32).tobytes())
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/mix_raw.wav', '-af', 'loudnorm=I=-13.5:TP=-2.2:LRA=9', '-ar', '48000', 'build/mix.wav'])
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/video_only.mp4', '-i', 'build/mix.wav', '-map', '0:v', '-map', '1:a',
                '-c:v', 'libx264', '-preset', 'slow', '-crf', '9', '-maxrate', '12M', '-bufsize', '24M', '-pix_fmt', 'yuv420p',
                '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', 'final/Old_Phone_Desk_Panel.mp4'])
print('ok')
