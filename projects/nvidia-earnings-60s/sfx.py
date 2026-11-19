"""Heavy cinematic SFX from the earshot bank (no beds/hum) + mix to -14 LUFS -> final/Nvidia_Earnings_60s.mp4"""
import sys, os, subprocess, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'engine'))
from earshot_bank import bank
SR = 48000; END = 45.34; n = int((END + 1) * SR); mix = np.zeros((n, 2))
def add(t, s, g=1.0, pan=0.0):
    i = int(t * SR); s = s[:max(0, n - i)]
    l, r = np.cos((pan + 1) * np.pi / 4) * 1.414, np.sin((pan + 1) * np.pi / 4) * 1.414
    mix[i:i + len(s), 0] += s * g * l; mix[i:i + len(s), 1] += s * g * r

CUTS = [3.75, 7.72, 10.55, 13.35, 18.85, 21.2, 25.0, 29.88, 34.05, 38.2]
BIG = {10.55, 25.0, 29.88, 38.2}
for i, c in enumerate(CUTS):
    if c in BIG: add(c - 0.42, bank('pro_whoosh_big/swell'), .40, pan=(-.3 if i % 2 else .3))
    else: add(c - 0.36, bank('whoosh_fast/crisp'), .30, pan=(-.4 if i % 2 else .4))
# hook
add(0.02, bank('pro_impact/deep'), .55)
add(4.3, bank('pro_riser/roll', dur=2.15), .30)                 # counter build (no tick roll: reads as buzz)
add(6.45, bank('pro_impact/short'), .55); add(6.45, bank('pro_notify/ding_2045'), .35)   # ₹10.9 lakh crore lands
add(7.28, bank('pro_impact/air'), .45); add(7.3, bank('pro_pop_in/knock'), .5)             # NO CAP stamp
add(7.85, bank('pro_pop_in/airy'), .35)                                                    # ₹100 note
add(8.72, bank('pro_pop/tink'), .45); add(8.72, bank('pro_impact/short'), .3)              # ₹56 profit
add(10.03, bank('pro_pop_in/round'), .4)                                                   # full savage mode
add(10.62, bank('pro_shimmer/m3'), .30)                                                    # title sting
add(14.7, bank('pro_riser/roll', dur=0.9), .30); add(15.58, bank('pro_impact/short'), .55) # +103%
add(13.65, bank('pro_pop_in/deep'), .3)
add(17.83, bank('pro_pop/boop'), .45)                                                      # literally insane
add(19.0, bank('pro_pop_in/airy'), .3); add(20.75, bank('pro_impact/air'), .45); add(20.75, bank('pro_notify/ding_1930'), .3)  # ₹12,000 cr
for t in np.arange(21.7, 25.0, 1.0): add(t, bank('pro_click/snap'), .55)                   # stopwatch tick each second
add(21.3, bank('pro_pop_in/knock'), .4); add(23.83, bank('pro_pop_in/double'), .45)        # Bro, HAR SECOND
add(25.9, bank('pro_pop_in/deep'), .35)                                                    # ₹12 lakh cr
add(27.0, bank('pro_riser/roll', dur=2.2), .32)                                            # build to plot twist
add(28.58, bank('pro_pop_in/round'), .4)                                                   # magnifier
add(29.18, bank('pro_impact/deep'), .65); add(29.2, bank('pro_pop_in/knock'), .4)          # PLOT TWIST stamp
for k in range(0, 13, 2): add(29.95 + k * 0.05, bank('pro_pop/thup'), .25, pan=(-.3 + .05 * k))   # week boxes
add(31.43, bank('pro_impact/short'), .5); add(31.45, bank('pro_pop/tink'), .4)            # box 14
add(33.23, bank('pro_pop_in/knock'), .45)                                                  # sirf +4%
add(34.6, bank('pro_pop_in/airy'), .3); add(35.78, bank('pro_pop/tink'), .35)              # ₹75
add(36.8, bank('whoosh_fast/reverse'), .3); add(36.98, bank('pro_impact/air'), .5)         # drop to ₹71–72
add(38.18, bank('pro_impact/rumble'), .45)                                                 # jacket chair
add(41.38, bank('pro_pop_in/knock'), .5)                                                   # WANTED note pinned
add(42.93, bank('pro_impact/deep'), .7); add(42.95, bank('pro_pop_in/double'), .4)         # SCENE KHATAM

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
                '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', 'final/Nvidia_Earnings_60s.mp4'])
print('ok')
