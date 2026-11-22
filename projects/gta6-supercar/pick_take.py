import subprocess, numpy as np, difflib, re
from faster_whisper import WhisperModel
from tl_common import S
m = WhisperModel('small', device='cpu', compute_type='int8')
for f in ['vo/take1.mp3', 'vo/take2.mp3']:
    a = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], capture_output=True).stdout, np.float32)
    segs, _ = m.transcribe(a, language='en', word_timestamps=True)
    ws = [re.sub(r'[^a-z0-9]', '', w.word.lower()) for s in segs for w in s.words]
    r = difflib.SequenceMatcher(None, S, [w for w in ws if w]).ratio()
    print(f, round(len(a) / 16000, 2), 's match', round(r, 3))
