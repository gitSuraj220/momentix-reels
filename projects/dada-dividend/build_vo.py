"""Cut the two takes into lines, speed up, and assemble the Short's VO track + timeline.json.
Run: python3 build_vo.py  ->  vo/vo_full.wav, timeline.json"""
import json, subprocess, numpy as np

SR = 48000
SPEED = 1.10          # quick Gen-Z pace
GAP = 0.12            # between lines (after speed-up)
PAD = 0.03

def load(f):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.float32).copy()

def speed(x):
    p = subprocess.run(['ffmpeg', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-',
                        '-af', f'atempo={SPEED}', '-f', 'f32le', '-'], input=x.tobytes(), capture_output=True)
    return np.frombuffer(p.stdout, np.float32).copy()

dada, beta = load('vo/dada_take2.mp3'), load('vo/beta_take1.mp3')
# raw (start, end) seconds, from silencedetect + energy check
LINES = [
    ('B1', beta, 0.03, 6.30, 'Dada ji, aapki govt naukri toh lagi nahi, phir bhi har mahine pension aati rehti hai? Scene kya hai?'),
    ('D1', dada, 0.04, 0.58, 'Pension?'),
    ('B2', beta, 6.66, 16.83, 'Haan! Aap din bhar ghar pe full chill karte ho, shaam ko doston ke saath bidi phookte ho, aur raat ko Doraemon dekhte ho. Phir bhi har mahine pension aa jaati hai!'),
    ('D2', dada, 0.96, 4.53, 'Arre, woh pension nahi, dividend hai meri jaan!'),
    ('B3', beta, 17.36, 22.75, 'Dada ji, ye toh OP hai! Batao na, mujhe bhi jaanna hai, ye dividend milta kaise hai?'),
    ('D3', dada, 5.09, 11.12, 'Beta, aisi 5 companies bata raha hoon jo saalon se accha dividend deti aayi hain. Likh:'),
    ('D4', dada, 11.99, 17.94, 'Ye companies apne profit ka ek hissa regular apne shareholders ke saath baant-ti rehti hain...'),
    ('D5', dada, 18.67, 20.16, 'Isi ko dividend kehte hain.'),
]

def fade(x, n=int(0.008 * SR)):
    x = x.copy(); r = np.linspace(0, 1, n, dtype=np.float32)
    x[:n] *= r; x[-n:] *= r[::-1]; return x

parts, tl, t = [], [], 0.25        # 0.25 s breath before the first word
out = np.zeros(int(t * SR), np.float32)
for i, (k, src, a, b, text) in enumerate(LINES):
    seg = speed(fade(src[int((a - PAD) * SR):int((b + PAD) * SR)]))
    gap = GAP
    if k == 'D4': gap = 0.20        # card slams in on "Likh!", then the line starts under it
    if k == 'D5': gap = 0.25        # card out -> punch-in on Dada ji
    if i: out = np.concatenate([out, np.zeros(int(gap * SR), np.float32)]); t += gap
    tl.append({'id': k, 'start': round(t, 3), 'end': round(t + len(seg) / SR, 3), 'text': text})
    out = np.concatenate([out, seg]); t += len(seg) / SR
tail = 1.0                          # phone ping + loop back
out = np.concatenate([out, np.zeros(int(tail * SR), np.float32)])
out = out / max(1e-6, np.abs(out).max()) * 0.89
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', 'vo/vo_full.wav'],
               input=out.tobytes())
json.dump({'duration': round(len(out) / SR, 3), 'lines': tl}, open('timeline.json', 'w'), indent=1)
for l in tl: print(l['id'], l['start'], l['end'])
print('total', round(len(out) / SR, 2))
