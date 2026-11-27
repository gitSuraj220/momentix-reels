"""Per-section voice: squeeze + 1.1x each chosen take, align words per section with its own text prompt, concat with chapter gaps.
Writes vo/vo_full.wav and words.json (global times) + vo/sections_meta.json (section starts)."""
import subprocess, numpy as np, json, re
from faster_whisper import WhisperModel
SR = 48000; SPEED = 1.1; MAXGAP = 0.45; GAP = 1.2
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
S = json.load(open('vo/sections.json')); pick = ['s1b', 's2a', 's3b', 's4a', 's5a', 's6a', 's7a', 's8a']
m = WhisperModel('medium', compute_type='int8')
VOC='Hinglish narration, Roman script, not translated. Words: book value, portfolio, market, share, FD, rupaye, saal, mahine, company, PSU banks, Cian Agro, quarter, SEBI, AI, profit book, value trap, recap.'
parts = [np.zeros(int(0.4 * SR), np.float32)]; t = 0.4; W = []; starts = []
for i, (p, txt) in enumerate(zip(pick, S)):
    x = L(f'vo/{p}.mp3'); v = x[np.abs(x) > 0.02]; x = x / np.sqrt((v ** 2).mean()) * 0.12
    y = squeeze(x)
    z = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-af', f'atempo={SPEED}', '-f', 'f32le', '-'], input=y.astype(np.float32).tobytes(), capture_output=True).stdout, np.float32)
    a16 = z[::3].copy(); subprocess.run(['ffmpeg','-y','-v','error','-f','f32le','-ar',str(SR),'-ac','1','-i','-',f'vo/sec{i+1}.wav'],input=z.astype(np.float32).tobytes())
    segs, _ = m.transcribe(a16, language='en', word_timestamps=True, beam_size=5, condition_on_previous_text=False, initial_prompt=VOC)
    for sg in segs:
        for w in sg.words:
            ww = re.sub(r'[^a-z0-9]', '', w.word.lower())
            if ww: W.append({'w': ww, 's': round(t + w.start, 2), 'e': round(t + w.end, 2), 'sec': i + 1})
    starts.append(round(t, 2)); parts += [z, np.zeros(int(GAP * SR), np.float32)]; t += len(z) / SR + GAP
    print(i + 1, p, round(len(z) / SR, 1))
y = np.concatenate(parts); y = y / np.abs(y).max() * 0.89
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', 'vo/vo_full.wav'], input=y.astype(np.float32).tobytes())
json.dump(W, open('words.json', 'w')); json.dump({'pick': pick, 'starts': starts, 'end': round(len(y) / SR, 2)}, open('vo/sections_meta.json', 'w'))
print('total', round(len(y) / SR, 2), 'words', len(W))
