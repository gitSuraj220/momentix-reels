"""Whisper word times on vo/vo_full.wav aligned to vo_text.txt -> timeline.json (via tl_common.build)."""
import json, re, difflib, subprocess, numpy as np
from faster_whisper import WhisperModel
from tl_common import S, build, norm
a = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', 'vo/vo_full.wav', '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], capture_output=True).stdout, np.float32)
m = WhisperModel('small', compute_type='int8')
segs, _ = m.transcribe(a, language='en', word_timestamps=True, beam_size=5, condition_on_previous_text=False, initial_prompt='Hinglish mein: Exam se pehle ChatGPT pe ye teen codes daalo, puri padhai half time mein.')
H = [(norm(w.word), w.start, w.end) for s in segs for w in s.words if norm(w.word)]
json.dump([{'w': h[0], 's': round(h[1], 2), 'e': round(h[2], 2)} for h in H], open('words.json', 'w'))
sm = difflib.SequenceMatcher(None, S, [h[0] for h in H], autojunk=False)
tS = [None] * len(S); tE = [None] * len(S)
for blk in sm.get_matching_blocks():
    for k in range(blk.size): tS[blk.a + k] = H[blk.b + k][1]; tE[blk.a + k] = H[blk.b + k][2]
known = [i for i, v in enumerate(tS) if v is not None]
for i in range(len(S)):
    if tS[i] is None:
        lo = max([k for k in known if k < i], default=None); hi = min([k for k in known if k > i], default=None)
        if lo is None: tS[i] = tS[hi] - 0.3 * (hi - i)
        elif hi is None: tS[i] = tS[lo] + 0.3 * (i - lo)
        else: tS[i] = tS[lo] + (tS[hi] - tS[lo]) * (i - lo) / (hi - lo)
for i in range(len(S)):
    if tE[i] is None: tE[i] = (tS[i + 1] if i + 1 < len(S) else tS[i] + 0.3)
matched = sum(b.size for b in sm.get_matching_blocks()); end = len(a) / 16000
T = build(tS, tE, end); print(f'matched {matched}/{len(S)}; end {end:.2f}'); print({k: round(v, 2) for k, v in T.items()})
