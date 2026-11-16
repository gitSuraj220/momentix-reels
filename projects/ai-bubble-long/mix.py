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
# look-ahead limiter, vectorised: gain = box-smoothed running minimum of the needed gain (never overshoots)
def limit(M, ceil_db=-2.0, win=.02):
    from scipy.ndimage import maximum_filter1d, minimum_filter1d, uniform_filter1d
    c = 10 ** (ceil_db / 20); w = int(win * SR)
    need = np.minimum(1, c / np.maximum(np.abs(M).max(1), 1e-9))
    g = uniform_filter1d(minimum_filter1d(need, 2 * w + 1), w + 1)
    return M * g[:, None]
for _ in range(3):
    M *= 10 ** ((-14 - meter.integrated_loudness(M)) / 20); M = limit(M)
tp = np.abs(resample_poly(M, 4, 1, axis=0)).max()
if tp > 10 ** (-1.2 / 20): M *= 10 ** (-1.2 / 20) / tp
f = int(.05 * SR); M[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write(f'{D}/audio/mix.wav', M.astype(np.float32), SR, subtype='PCM_24')
subprocess.run(['cp', f'{D}/audio/mix.wav', f'{D}/audio/mix_ln.wav'], check=True)
x = M
print('mix LUFS', round(meter.integrated_loudness(x), 2), 'TP~', round(20 * np.log10(np.abs(resample_poly(x, 4, 1, axis=0)).max()), 2), 'dBTP')
out = f'{D}/final/AI_Bubble_Long_16x9.mp4'
# colour grade: gentle S-curve + shadow lift, cool shadows / neutral whites, vibrance, luma-only sharpen
# (colorbalance pl=1 speckles saturated reds in this ffmpeg - keep it off)
GRADE = ("curves=master='0/0.012 0.1/0.1 0.3/0.3 0.55/0.575 0.8/0.83 1/1',colorbalance=rs=-0.02:bs=0.025:rm=0.008:bm=-0.008,"
         'vibrance=intensity=0.15,unsharp=5:5:0.45:5:5:0')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{D}/build/video_only.mp4', '-i', f'{D}/audio/mix_ln.wav',
                '-vf', GRADE, '-c:v', 'libx264', '-preset', 'slow', '-tune', 'animation', '-b:v', '12M', '-maxrate', '14M', '-bufsize', '24M', '-pix_fmt', 'yuv420p', '-r', '30',
                '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', '-shortest', out], check=True)
print('muxed', out)
