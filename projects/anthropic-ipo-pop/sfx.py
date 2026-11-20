"""Heavy cinematic SFX from the earshot bank (no beds/hum) + mix to -14 LUFS -> final/Nvidia_Earnings_60s.mp4"""
import sys, os, subprocess, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'engine'))
from earshot_bank import bank
SR = 48000; END = 29.76; n = int((END + 1) * SR); mix = np.zeros((n, 2))
def add(t, s, g=1.0, pan=0.0):
    i = int(t * SR); s = s[:max(0, n - i)]
    l, r = np.cos((pan + 1) * np.pi / 4) * 1.414, np.sin((pan + 1) * np.pi / 4) * 1.414
    mix[i:i + len(s), 0] += s * g * l; mix[i:i + len(s), 1] += s * g * r

CUTS = [5.65, 8.25, 12.5, 16.45, 18.95, 22.1, 24.1]
BIG = {5.65, 18.95, 24.1}
for i, c in enumerate(CUTS):
    if c in BIG: add(c - 0.42, bank('pro_whoosh_big/swell'), .40, pan=(-.3 if i % 2 else .3))
    else: add(c - 0.36, bank('whoosh_fast/crisp'), .30, pan=(-.4 if i % 2 else .4))
add(0.0, bank('pro_impact/air'), .4); add(0.05, bank('pro_notify/ding_2296'), .35)          # opening bell
add(1.52, bank('pro_impact/short'), .6); add(1.55, bank('pro_pop_in/knock'), .35)          # $83 tag slam
add(3.4, bank('pro_riser/roll', dur=0.75), .3); add(4.15, bank('pro_impact/deep'), .65)    # $111.50 slam
add(4.9, bank('pro_notify/ding_2045'), .35)                                                # +$28.50
add(5.7, bank('pro_pop_in/round'), .35); add(6.75, bank('pro_impact/deep'), .7); add(6.78, bank('pro_pop_in/double'), .4)  # PLOT TWIST / ₹0 GAIN stamp
add(8.3, bank('pro_pop_in/airy'), .35); add(9.3, bank('pro_shimmer/m3'), .25)              # kyun? / moon
add(10.25, bank('pro_impact/short'), .5); add(10.7, bank('pro_click/snap'), .6)            # $83 locked (click of lock)
add(12.55, bank('pro_riser/roll', dur=0.9), .28); add(13.3, bank('pro_impact/short'), .55); add(13.32, bank('pro_notify/ding_1930'), .35)  # ₹7.6 lakh crore
add(14.4, bank('pro_pop/tink'), .4); add(15.0, bank('pro_pop_in/knock'), .4)               # trophy / Claude chip
add(17.2, bank('whoosh_fast/reverse'), .35); add(17.6, bank('ui_pop/wide'), .4)            # Anthropic exits / investors swap
add(19.0, bank('pro_impact/rumble'), .45)                                                  # crowd rush
add(20.2, bank('pro_riser/roll', dur=0.8), .3); add(20.95, bank('pro_impact/deep'), .65); add(20.97, bank('pro_notify/ding_2296'), .3)   # +34%
add(22.2, bank('whoosh_fast/crisp'), .25); add(23.3, bank('pro_impact/air'), .5)           # chart draw / $97 close
add(24.2, bank('pro_pop_in/airy'), .3); add(25.6, bank('pro_riser/roll', dur=0.8), .28)
add(26.35, bank('pro_impact/short'), .55); add(26.4, bank('pro_notify/ding_2045'), .4)     # ₹1.3 lakh crore + 🤑
add(28.15, bank('pro_impact/deep'), .75); add(28.17, bank('pro_pop_in/double'), .45)       # LITERALLY EK DIN

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
                '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', 'final/Anthropic_IPO_Pop.mp4'])
print('ok')
