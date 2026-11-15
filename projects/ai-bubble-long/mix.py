#!/usr/bin/env python3
"""Mix VO + SFX (no BGM; Suraj adds it) -> -14 LUFS, true peak <= -1 dBTP, mux with build/video_only.mp4.
SFX are ducked ~6 dB under speech (envelope follower on the VO) so whooshes don't mask words."""
import os, subprocess
import numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy.signal import resample_poly, butter, sosfiltfilt
D = os.path.dirname(os.path.abspath(__file__)); SR = 48000
os.makedirs(f'{D}/audio', exist_ok=True); os.makedirs(f'{D}/final', exist_ok=True)
vo_wav = f'{D}/audio/vo48.wav'
src = f'{D}/vo/vo_full.wav' if os.path.exists(f'{D}/vo/vo_full.wav') else f'{D}/vo/vo_full.mp3'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-ac', '1', '-ar', str(SR), vo_wav], check=True)
vo, _ = sf.read(vo_wav); fx, sr = sf.read(f'{D}/audio/sfx_only.wav'); assert sr == SR
n = len(fx); V = np.zeros((n, 2)); m = min(n, len(vo)); V[:m] = vo[:m, None]; F = fx[:n].copy()
meter = pyln.Meter(SR)
V *= 10 ** ((-16.5 - meter.integrated_loudness(V)) / 20)       # voice leads
F *= 10 ** ((-23.5 - meter.integrated_loudness(F)) / 20)       # SFX ~7 LU under voice (heavy cinematic)
env = sosfiltfilt(butter(2, 6, 'low', fs=SR, output='sos'), np.abs(V[:, 0]))
duck = 1 - .5 * np.clip(env / (np.percentile(env[env > 1e-4], 60) + 1e-9), 0, 1)   # up to -6 dB under speech
F *= duck[:, None]
M = V + F
M *= 10 ** ((-14 - meter.integrated_loudness(M)) / 20)
tp = np.abs(resample_poly(M, 4, 1, axis=0)).max()
if tp > 10 ** (-1.2 / 20): M *= 10 ** (-1.2 / 20) / tp
f = int(.05 * SR); M[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write(f'{D}/audio/mix.wav', M.astype(np.float32), SR, subtype='PCM_24')
# loudnorm second pass lands -14 after the peak guard (linear mode keeps dynamics)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{D}/audio/mix.wav', '-af', 'loudnorm=I=-14:TP=-1:LRA=11,aresample=48000', f'{D}/audio/mix_ln.wav'], check=True)
x, _ = sf.read(f'{D}/audio/mix_ln.wav')
print('mix LUFS', round(meter.integrated_loudness(x), 2), 'TP~', round(20 * np.log10(np.abs(resample_poly(x, 4, 1, axis=0)).max()), 2), 'dBTP')
out = f'{D}/final/AI_Bubble_Long_16x9.mp4'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{D}/build/video_only.mp4', '-i', f'{D}/audio/mix_ln.wav',
                '-c:v', 'libx264', '-preset', 'slow', '-b:v', '10M', '-maxrate', '12M', '-bufsize', '20M', '-pix_fmt', 'yuv420p', '-r', '30',
                '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', '-shortest', out], check=True)
print('muxed', out)
