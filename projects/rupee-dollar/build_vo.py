"""3 picked takes -> join with section pauses, squeeze long gaps, speed 1.15x -> vo/vo_full.wav, env.json
usage: python3 build_vo.py p1b p2a p3b"""
import subprocess, numpy as np, json, sys
SR = 48000; SPEED = 1.15; MAXGAP = 0.32; JOIN = 0.45
L = lambda f: np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                                           capture_output=True).stdout, np.float32).copy()
def squeeze(x):
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
    # trim leading/trailing silence
    nz = np.where(np.abs(y) > 10 ** (-40 / 20))[0]
    return y[max(0, nz[0] - 480):nz[-1] + 2400]
parts = [squeeze(L(f'vo/{p}.mp3')) for p in sys.argv[1:4]]
gap = np.zeros(int(JOIN * SR), np.float32)
y = np.concatenate([parts[0], gap, parts[1], gap, parts[2]])
p = subprocess.run(['ffmpeg', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-af', f'atempo={SPEED}',
                    '-f', 'f32le', '-'], input=y.tobytes(), capture_output=True)
z = np.frombuffer(p.stdout, np.float32)
z = np.concatenate([np.zeros(int(0.25 * SR), np.float32), z, np.zeros(int(0.6 * SR), np.float32)])
z = z / np.abs(z).max() * 0.89
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', 'vo/vo_full.wav'], input=z.tobytes())
env = [float(np.sqrt((z[i:i + 1600] ** 2).mean())) for i in range(0, len(z), 1600)]; mx = max(env)
json.dump([round(min(1, v / mx * 1.6), 3) for v in env], open('env.json', 'w'))
print('duration', round(len(z) / SR, 2))
