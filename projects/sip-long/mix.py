"""Mix VO + SFX (no bed; Suraj adds BGM) to -14 LUFS, true peak <= -1 dBTP, and mux with the video."""
import json, os, subprocess
import numpy as np, soundfile as sf, pyloudnorm as pyln
D = os.path.dirname(os.path.abspath(__file__))
SR = 48000
import json
END = json.load(open(f'{D}/timeline.json'))['END']
vo, sr = sf.read(f'{D}/vo/vo48.wav'); assert sr == SR
if vo.ndim > 1: vo = vo.mean(1)
fx, sr = sf.read(f'{D}/audio/sfx_only.wav'); assert sr == SR
n = int(END * SR)
V = np.zeros((n, 2)); V[:min(n, len(vo)), :] = vo[:n, None]
F = np.zeros((n, 2)); F[:min(n, len(fx))] = fx[:n]
meter = pyln.Meter(SR)
V *= 10 ** ((-17 - meter.integrated_loudness(V)) / 20)      # voice leads
F *= 10 ** ((-25 - meter.integrated_loudness(F)) / 20)      # SFX ~8 LU under voice
# duck SFX ~6 dB while the voice is speaking (pauses keep full-size hits)
from scipy.ndimage import maximum_filter1d, uniform_filter1d
env = uniform_filter1d(np.abs(V[:, 0]), int(.03 * SR)); act = (env > 10 ** (-42 / 20)).astype(float)
act = maximum_filter1d(act, int(.25 * SR)); act = uniform_filter1d(act, int(.08 * SR))
F *= (1 - .5 * act)[:, None]
M = V + F
M *= 10 ** ((-14 - meter.integrated_loudness(M)) / 20)
# true-peak guard (4x oversampled estimate)
from scipy.signal import resample_poly
tp = np.abs(resample_poly(M, 4, 1, axis=0)).max()
if tp > 10 ** (-1 / 20): M *= 10 ** (-1 / 20) / tp
fade = int(.03 * SR); M[-fade:] *= np.linspace(1, 0, fade)[:, None]
sf.write(f'{D}/audio/mix.wav', M.astype(np.float32), SR, subtype='PCM_24')
print('mix LUFS', round(meter.integrated_loudness(M), 2), 'peak dBFS', round(20 * np.log10(np.abs(M).max()), 2))
os.makedirs(f'{D}/final', exist_ok=True)
subprocess.run(['ffmpeg','-v','error','-y','-i',f'{D}/audio/mix.wav','-af','loudnorm=I=-14:TP=-1:LRA=7,aresample=48000',f'{D}/audio/mix_ln.wav'],check=True)  # peak guard leaves it quieter; loudnorm lands -14
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{D}/build/video_only.mp4', '-i', f'{D}/audio/mix_ln.wav',
                '-c:v', 'libx264', '-preset', 'slow', '-b:v', '10M', '-maxrate', '12M', '-bufsize', '20M', '-pix_fmt', 'yuv420p',
                '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', '-shortest', f'{D}/final/SIP_Kaise_Shuru_Karein.mp4'], check=True)
print('muxed final/SIP_Kaise_Shuru_Karein.mp4')
