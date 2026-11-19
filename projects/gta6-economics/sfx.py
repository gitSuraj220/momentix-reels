"""Heavy cinematic SFX from the earshot bank (no beds/hum) + mix to -14 LUFS -> final/Nvidia_Earnings_60s.mp4"""
import sys, os, subprocess, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'engine'))
from earshot_bank import bank
SR = 48000; END = 33.5; n = int((END + 1) * SR); mix = np.zeros((n, 2))
def add(t, s, g=1.0, pan=0.0):
    i = int(t * SR); s = s[:max(0, n - i)]
    l, r = np.cos((pan + 1) * np.pi / 4) * 1.414, np.sin((pan + 1) * np.pi / 4) * 1.414
    mix[i:i + len(s), 0] += s * g * l; mix[i:i + len(s), 1] += s * g * r

CUTS = [3.5, 9.95, 13.9, 16.95, 19.5, 24.62, 30.55]
BIG = {9.95, 19.5, 30.55}
for i, c in enumerate(CUTS):
    if c in BIG: add(c - 0.42, bank('pro_whoosh_big/swell'), .40, pan=(-.3 if i % 2 else .3))
    else: add(c - 0.36, bank('whoosh_fast/crisp'), .30, pan=(-.4 if i % 2 else .4))
# hook: fly-in
add(0.0, bank('pro_whoosh_big/swell'), .35); add(0.45, bank('pro_impact/deep'), .55)       # GTA VI logo slam
add(2.6, bank('pro_pop_in/round'), .4)                                                     # internet pagal
# cost vs price
add(4.3, bank('pro_riser/roll', dur=1.0), .28); add(5.3, bank('pro_impact/short'), .55)    # ₹14,000 crore
add(5.6, bank('pro_pop_in/knock'), .35)                                                    # Rockstar logo
add(7.85, bank('pro_pop/tink'), .45); add(9.3, bank('pro_pop_in/double'), .4)              # ₹7,500 / kamai kaise
# store cut
add(10.1, bank('pro_pop_in/airy'), .35); add(10.4, bank('ui_pop/wide'), .35)               # bar + console logos
add(10.85, bank('pro_impact/air'), .5); add(11.2, bank('whoosh_fast/reverse'), .3)         # 30% chopped, falls
add(12.9, bank('pro_notify/ding_2045'), .4); add(12.9, bank('pro_impact/short'), .35)      # ₹5,250
# copies
add(14.9, bank('pro_riser/roll', dur=0.9), .28); add(15.8, bank('pro_impact/short'), .5)   # 2.7 crore copies
add(16.35, bank('pro_pop/boop'), .45)                                                      # sounds crazy
add(17.9, bank('pro_impact/deep'), .55); add(17.95, bank('pro_notify/ding_2296'), .3)      # 23 crore+
# twist + in-game shop (game UI sounds)
add(19.88, bank('pro_impact/deep'), .6); add(19.9, bank('pro_pop_in/knock'), .4)           # ASLI TWIST stamp
add(20.75, bank('pro_pop_in/round'), .35)                                                  # Take-Two logo
for k, t in enumerate([21.2, 22.0, 22.8, 23.5]):                                           # menu clicks + purchase dings
    add(t, bank('pro_click/snap'), .5); add(t + 0.12, bank('pro_notify/ding_1930' if k % 2 else 'pro_notify/ding_2167'), .28)
add(23.1, bank('ui_pop/blip'), .4)
# ₹81 of ₹100
add(24.8, bank('pro_pop_in/airy'), .3); add(25.3, bank('pro_riser/roll', dur=0.7), .25)
add(25.9, bank('pro_impact/short'), .55); add(25.92, bank('pro_notify/ding_2045'), .35)    # ₹81
for t in (28.8, 29.4, 29.95): add(t, bank('ui_pop/wide'), .45); add(t, bank('pro_click/tink'), .3)   # gaadiyan/skins/ghar = purchases
# old GTA 5 still earning
add(30.6, bank('pro_impact/rumble'), .4); add(31.95, bank('pro_shimmer/m3'), .3); add(32.2, bank('pro_notify/ding_1822'), .35)

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
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/mix_raw.wav', '-af', 'loudnorm=I=-14:TP=-2.2:LRA=9', '-ar', '48000', 'build/mix.wav'])
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/video_only.mp4', '-i', 'build/mix.wav', '-map', '0:v', '-map', '1:a',
                '-c:v', 'libx264', '-preset', 'slow', '-b:v', '10M', '-maxrate', '12M', '-bufsize', '20M', '-pix_fmt', 'yuv420p',
                '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', 'final/GTA6_Paisa_60s.mp4'])
print('ok')
