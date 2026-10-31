"""Cut takeB (IPO) into phrases, tighten pauses, slight speed-up -> vo.wav + cues.json."""
import json, re, subprocess, numpy as np, soundfile as sf
SR = 48000; TEMPO = 1.16
CAP = [
 "2008 ki mandi…", "Covid ka crash…", "Google ka share kabhi ek din mein itna nahi gira…", "jitna 29 October ko gira.", "12.6%!",
 "Ek din mein ₹46 lakh crore saaf.",
 "Aur akela Google nahi gira.", "China ka CSI 300,", "11 hafte lagataar neeche.", "Gold,", "record se 27% neeche.", "Bitcoin,", "2014 ke baad sabse bura October.",
 "Toh kya AI bubble phat raha hai?",
 "Google ka business toh badh raha hai.", "Kamai 25% upar,", "cloud double.",
 "Phir dikkat kya?", "Ek:", "3 mahine mein AI data centres pe $51 billion.",
 "Do:", "Kharcha kamai se zyada,", "free cash flow minus mein,", "lagataar doosri baar.",
 "Teen:", "Search,", "Google ki asli kamai,", "uski growth 17% se 12% pe aa gayi.",
 "Aur jab AI ki sabse badi company pe shak ho…", "log sab bechkar cash dhoondhte hain.",
 "Bubble phata ya nahi, waqt batayega.", "Par ab dikhana padega… ye kharcha wapas kab aayega.",
]
BREAK = {5, 12, 13, 16, 23, 27, 29}
LINE = [0,0,0,0,0,1, 2,3,3,4,4,5,5, 6, 7,7,7, 8,8,8, 9,9,9,9, 10,10,10,10, 11,11, 12,12]
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'takeB.mp3', '-ar', str(SR), '-ac', '1', 'takeB.wav'], check=True)
x, _ = sf.read('takeB.wav')
out = subprocess.run(['ffmpeg', '-v', 'info', '-i', 'takeB.wav', '-af', 'silencedetect=noise=-38dB:d=0.25', '-f', 'null', '-'], capture_output=True, text=True).stderr
st = [float(v) for v in re.findall(r'silence_start: ([\d.]+)', out)]
en = [float(v) for v in re.findall(r'silence_end: ([\d.]+)', out)]
segs = []; cur = 0.0
for a, b in zip(st, en):
    if a > cur + 0.05: segs.append((cur, a))
    cur = b
if cur < len(x) / SR - 0.05: segs.append((cur, len(x) / SR))
print(len(segs), 'segments'); assert len(segs) == len(CAP), (len(segs), len(CAP))
PAD = 0.06; pieces = []; cues = []; t = 0.25
pieces.append(np.zeros(int(0.25 * SR)))
for i, ((a, b), cap) in enumerate(zip(segs, CAP)):
    a2, b2 = max(0, a - PAD), min(len(x) / SR, b + PAD)
    seg = x[int(a2 * SR):int(b2 * SR)]
    seg = seg.copy(); F = int(0.008 * SR); r = np.linspace(0, 1, F); seg[:F] *= r; seg[-F:] *= r[::-1]
    cues.append({'id': f'c{i}', 'w': cap, 'line': LINE[i], 's': t, 'e': t + len(seg) / SR})
    pieces.append(seg); t += len(seg) / SR
    gap = 0.0 if i == len(CAP) - 1 else (0.30 if i in BREAK else 0.07)
    pieces.append(np.zeros(int(gap * SR))); t += gap
y = np.concatenate(pieces); sf.write('vo_tight.wav', y, SR)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'vo_tight.wav', '-af', f'atempo={TEMPO}', '-ar', str(SR), 'vo.wav'], check=True)
for c in cues: c['s'] = round(c['s'] / TEMPO, 3); c['e'] = round(c['e'] / TEMPO, 3)
json.dump(cues, open('cues.json', 'w'), ensure_ascii=False, indent=1)
print('total', round(len(y) / SR / TEMPO, 2))
for c in cues: print(c['id'], c['s'], c['e'], c['w'])
