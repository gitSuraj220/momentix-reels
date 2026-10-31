"""Cut takeA (IPO) into phrases, tighten pauses, slight speed-up -> vo.wav + cues.json."""
import json, re, subprocess, numpy as np, soundfile as sf
SR = 48000; TEMPO = 1.08
CAP = [
 "IPO kaam kaise karta hai?", "Ek chai wale se samajhte hain.",
 "Raju ki chai ki 50 dukaan hain…", "aur use 500 kholni hain.",
 "Paisa chahiye ₹100 crore.", "Bank se loan?", "Mehenga.", "Toh Raju laata hai…", "IPO.",
 "Step 1:", "SEBI ko poori kundli do —", "DRHP.", "Kamai, karza, khatre, sab.",
 "Step 2:", "Price band.", "₹95 se ₹100 ke beech.",
 "Step 3:", "Log bid karte hain.", "Demand zyada,", "toh price ₹100 fix.",
 "1 crore shares × ₹100 —", "₹100 crore Raju ki company ko.", "Bas.", "Company ka kaam khatam.",
 "Step 4:", "Listing.", "Pehle hi din share ₹121 pe khula.",
 "Wo ₹21 crore extra…", "Raju ko?", "Ek rupaya bhi nahi.", "Wo gaya jinhe share allot hua.",
 "Aur ye sirf kahani nahi.", "28 October ko Jio ke saath bilkul yahi hua.",
 "₹1,119 ka share ₹1,358 pe khula —", "21% upar.", "Jio ko mile ₹30,213 crore.",
 "Listing ka ~₹6,450 crore ka uchaal?", "Investors ki jeb mein.",
]
BREAK = {1, 3, 8, 12, 15, 19, 23, 26, 30, 32}
# line index for each cue (script rows 0-10)
LINE = [0,0, 1,1, 2,2,2,2,2, 3,3,3,3, 4,4,4, 5,5,5,5, 6,6,6,6, 7,7,7, 8,8,8,8, 9,9, 10,10,10,10,10]
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'takeA.mp3', '-ar', str(SR), '-ac', '1', 'takeA.wav'], check=True)
x, _ = sf.read('takeA.wav')
out = subprocess.run(['ffmpeg', '-v', 'info', '-i', 'takeA.wav', '-af', 'silencedetect=noise=-38dB:d=0.25', '-f', 'null', '-'], capture_output=True, text=True).stderr
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
    cues.append({'id': f'c{i}', 'w': cap, 'line': LINE[i], 's': t, 'e': t + len(seg) / SR})
    pieces.append(seg); t += len(seg) / SR
    gap = 0.0 if i == len(CAP) - 1 else (0.38 if i in BREAK else 0.12)
    pieces.append(np.zeros(int(gap * SR))); t += gap
y = np.concatenate(pieces); sf.write('vo_tight.wav', y, SR)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'vo_tight.wav', '-af', f'atempo={TEMPO}', '-ar', str(SR), 'vo.wav'], check=True)
for c in cues: c['s'] = round(c['s'] / TEMPO, 3); c['e'] = round(c['e'] / TEMPO, 3)
json.dump(cues, open('cues.json', 'w'), ensure_ascii=False, indent=1)
print('total', round(len(y) / SR / TEMPO, 2))
for c in cues: print(c['id'], c['s'], c['e'], c['w'])
