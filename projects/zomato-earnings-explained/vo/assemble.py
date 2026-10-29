"""Cut take1 into phrases (silencedetect), tighten pauses, speed up slightly, write vo.wav + cues.json."""
import json, re, subprocess, numpy as np, soundfile as sf
SRC = 'take1.mp3'; SR = 48000; TEMPO = 1.07
# caption text per detected speech segment (34 segments incl. one breath at ~13.2 s -> None)
CAP = [
 "Zomato ne sirf 3 mahine mein ₹24,000 crore kamaaye…", "Aur profit?", "Har ₹100 mein se…", "sirf 52 paise.",
 "Saal bhar pehle 3 mahine ki kamai thi ₹13,590 crore…", None, "ab ₹24,138 crore.", "Seedha 78% upar.",
 "Aur sabse bada surprise —", "Blinkit ab khaane se bada ho gaya.", "Blinkit pe ₹20,940 crore ke order,", "khaane pe ₹11,445 crore.",
 "Par kharcha?", "₹24,166 crore.", "Matlab jitna kamaya,", "usse ₹28 crore zyada uda diya.",
 "Toh profit aaya kahaan se?", "Khaana ya saamaan bech ke nahi…", "company ke paas pade ₹16,475 crore pe milne wali doosri kamai se —", "jaise byaaj.",
 "Market ko umeed thi ₹250 crore ki.", "Mila aadha.", "Share 3.5% gir gaya.",
 "Toh kya Zomato fail?", "Nahi.", "Ye jaan-boojh ke kharch kar raha hai —", "naye store,", "aur ads pe ₹1,138 crore.",
 "Pehle aadat…", "phir kamai.",
 "Toh agli baar jab 10 minute mein delivery aaye…", "yaad rakhna,", "uska kharcha abhi company utha rahi hai.",
]
# scene breaks: longer pause AFTER these caption indices
BREAK = {3, 7, 11, 15, 19, 22, 29}
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', SRC, '-ar', str(SR), '-ac', '1', 'take1.wav'], check=True)
x, _ = sf.read('take1.wav')
out = subprocess.run(['ffmpeg', '-v', 'info', '-i', 'take1.wav', '-af', 'silencedetect=noise=-38dB:d=0.25', '-f', 'null', '-'], capture_output=True, text=True).stderr
st = [float(v) for v in re.findall(r'silence_start: ([\d.]+)', out)]
en = [float(v) for v in re.findall(r'silence_end: ([\d.]+)', out)]
segs = []; cur = 0.0
for a, b in zip(st, en):
    if a > cur + 0.05: segs.append((cur, a))
    cur = b
if cur < len(x) / SR - 0.05: segs.append((cur, len(x) / SR))
print(len(segs), 'segments')
assert len(segs) == len(CAP), (len(segs), len(CAP))
PAD = 0.06
pieces = []; cues = []; t = 0.0; k = 0
for i, ((a, b), cap) in enumerate(zip(segs, CAP)):
    a2, b2 = max(0, a - PAD), min(len(x) / SR, b + PAD)
    seg = x[int(a2 * SR):int(b2 * SR)]
    if cap is None:            # breath: keep it short and tie it to the previous line
        pieces.append(seg); t += len(seg) / SR; continue
    cues.append({'id': f'c{k}', 'i': i, 'w': cap, 's': t, 'e': t + len(seg) / SR}); k += 1
    pieces.append(seg); t += len(seg) / SR
    gap = 0.55 if i in BREAK else 0.20
    if i == len(CAP) - 1: gap = 0.0
    pieces.append(np.zeros(int(gap * SR))); t += gap
y = np.concatenate(pieces)
sf.write('vo_tight.wav', y, SR)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'vo_tight.wav', '-af', f'atempo={TEMPO}', '-ar', str(SR), 'vo.wav'], check=True)
for c in cues:
    c['s'] = round(c['s'] / TEMPO, 3); c['e'] = round(c['e'] / TEMPO, 3)
json.dump(cues, open('cues.json', 'w'), ensure_ascii=False, indent=1)
print('total', round(len(y) / SR / TEMPO, 2), 's')
for c in cues: print(c['id'], c['s'], c['e'], c['w'])
