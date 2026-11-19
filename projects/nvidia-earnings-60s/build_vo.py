"""Splice take2 + fix2, squeeze pauses, speed up -> vo/vo_full.wav, words.json, env.json"""
import subprocess, numpy as np, json
SR = 48000; SPEED = 1.30; MAXGAP = 0.10
L = lambda f: np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                                           capture_output=True).stdout, np.float32).copy()
t2, fx = L('vo/take2.mp3'), L('vo/fix2.mp3')
S = lambda a, s, e: a[int(s * SR):int(e * SR)]
parts = [S(t2, 0, 29.10),            # lines 1-4
         S(fx, 0, 10.05),            # line 5 (clean retake)
         S(t2, 38.70, 59.20),        # lines 6-8
         S(fx, 10.60, 13.9),         # line 9 (clean retake)
         S(t2, 62.0, len(t2) / SR)]  # line 10
x = np.concatenate(parts)
# squeeze every pause longer than MAXGAP
hop = 480; e = np.array([np.sqrt((x[i:i + hop] ** 2).mean()) for i in range(0, len(x), hop)])
quiet = e < 10 ** (-42 / 20); out = []; i = 0; n = len(e)
while i < n:
    j = i
    while j < n and quiet[j] == quiet[i]: j += 1
    seg = x[i * hop:j * hop]
    if quiet[i] and (j - i) * hop / SR > MAXGAP:
        k = int(MAXGAP * SR / 2); seg = np.concatenate([seg[:k], seg[-k:]])
    out.append(seg); i = j
y = np.concatenate(out)
y = y[int(0.02 * SR):]
p = subprocess.run(['ffmpeg', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-af', f'atempo={SPEED}',
                    '-f', 'f32le', '-'], input=y.tobytes(), capture_output=True)
z = np.frombuffer(p.stdout, np.float32)
z = np.concatenate([np.zeros(int(0.08 * SR), np.float32), z, np.zeros(int(0.35 * SR), np.float32)])
z = z / np.abs(z).max() * 0.89
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', 'vo/vo_full.wav'], input=z.tobytes())
env = [float(np.sqrt((z[i:i + 1600] ** 2).mean())) for i in range(0, len(z), 1600)]; mx = max(env)
json.dump([round(min(1, v / mx * 1.6), 3) for v in env], open('env.json', 'w'))
print('duration', round(len(z) / SR, 2))
