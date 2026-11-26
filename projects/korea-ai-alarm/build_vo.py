"""One take -> squeeze long gaps, 1.15x -> vo/vo_full.wav.  usage: python3 build_vo.py take1"""
import subprocess, numpy as np, sys
SR = 48000; SPEED = 1.25; MAXGAP = 0.16
L = lambda f: np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout, np.float32).copy()
def squeeze(x):
    hop = 480; e = np.array([np.sqrt((x[i:i + hop] ** 2).mean()) for i in range(0, len(x), hop)]); quiet = e < 10 ** (-42 / 20); out = []; i = 0; n = len(e)
    while i < n:
        j = i
        while j < n and quiet[j] == quiet[i]: j += 1
        seg = x[i * hop:j * hop]
        if quiet[i] and (j - i) * hop / SR > MAXGAP: k = int(MAXGAP * SR / 2); seg = np.concatenate([seg[:k], seg[-k:]])
        out.append(seg); i = j
    y = np.concatenate(out); nz = np.where(np.abs(y) > 10 ** (-40 / 20))[0]; return y[max(0, nz[0] - 480):nz[-1] + 2400]
y = squeeze(L(f'vo/{sys.argv[1]}.mp3'))
z = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-af', f'atempo={SPEED}', '-f', 'f32le', '-'], input=y.tobytes(), capture_output=True).stdout, np.float32)
z = np.concatenate([np.zeros(int(0.25 * SR), np.float32), z, np.zeros(int(0.9 * SR), np.float32)]); z = z / np.abs(z).max() * 0.89
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', 'vo/vo_full.wav'], input=z.tobytes())
print('duration', round(len(z) / SR, 2))
