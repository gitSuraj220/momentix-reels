"""Cut takeA into phrases, tighten pauses, slight speed-up -> vo.wav + cues.json."""
import json, re, subprocess, numpy as np, soundfile as sf
SR = 48000; TEMPO = 1.06
CAP = [
 "Main gold hoon re…", "Dhanteras pe ₹10,000 mein mujhe khareedoge…", "toh main sirf ₹8,100 ka milunga re!",
 "Jewellery banoge mujhe?", "Making charge lagega —", "8 se 25%.", "Is design pe 20%.", "Upar se GST.", "₹1,900 toh yahin gaye.",
 "Wapas bechne aaoge?", "Making ka paisa nahi milega.", "10–15% kat jaayega re.",
 "App pe digital gold banake loge?", "3% GST turant,", "upar se rate ka fark.", "Bechte hi ₹500–600 gaye.",
 "ETF mein loge…", "na making, na GST.", "₹10,000 ke aas-paas ka hi milunga.",
 "Toh hisaab ye hai re:", "jewellery — ₹8,100.", "Digital —", "lagbhag ₹9,400.", "ETF —", "lagbhag ₹9,900.",
 "Pehenna hai toh shauk se lo.", "Invest karna hai…", "toh dimaag se.",
]
BREAK = {2, 8, 11, 15, 18, 24}
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
    cues.append({'id': f'c{i}', 'w': cap, 's': t, 'e': t + len(seg) / SR})
    pieces.append(seg); t += len(seg) / SR
    gap = 0.0 if i == len(CAP) - 1 else (0.42 if i in BREAK else 0.16)
    pieces.append(np.zeros(int(gap * SR))); t += gap
y = np.concatenate(pieces); sf.write('vo_tight.wav', y, SR)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'vo_tight.wav', '-af', f'atempo={TEMPO}', '-ar', str(SR), 'vo.wav'], check=True)
for c in cues: c['s'] = round(c['s'] / TEMPO, 3); c['e'] = round(c['e'] / TEMPO, 3)
json.dump(cues, open('cues.json', 'w'), ensure_ascii=False, indent=1)
print('total', round(len(y) / SR / TEMPO, 2))
for c in cues: print(c['id'], c['s'], c['e'], c['w'])
