"""Insert breathing pauses after given words (from words.json) at the nearest quiet point."""
import json, subprocess, numpy as np
SR = 48000; W = json.load(open('words.json'))
x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', 'vo/vo_full.wav', '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True).stdout, np.float32).copy()
def after(word, near):  # end time of the matching word closest to `near`
    c = [w for w in W if w['w'] == word]; return min(c, key=lambda w: abs(w['s'] - near))['e']
P = [(after('hai', 5.9), 0.45), (after('hai', 14.3), 0.35), (after('trick', 20.9), 0.35)]
def quiet_point(t):
    i0 = int(t * SR); hop = 240; best = i0; be = 9
    for i in range(i0 - 2400, i0 + 9600, hop):
        e = np.sqrt((x[i:i + 1200] ** 2).mean())
        if e < be: be = e; best = i + 600
    return best
out = []; last = 0
for t, d in sorted(P):
    q = quiet_point(t); out += [x[last:q], np.zeros(int(d * SR), np.float32)]; last = q
out.append(x[last:]); y = np.concatenate(out)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', 'vo/vo_full.wav'], input=y.tobytes())
print('pauses at', [round(p[0], 2) for p in P], 'new duration', round(len(y) / SR, 2))
