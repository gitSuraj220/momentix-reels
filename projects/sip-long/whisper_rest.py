from faster_whisper import WhisperModel
import json, subprocess, numpy as np, sys
m = WhisperModel('small', device='cpu', compute_type='int8', cpu_threads=4)
for f in sys.argv[1:]:
    raw = subprocess.run(['ffmpeg','-v','error','-i',f'vo/{f}.mp3','-ac','1','-ar','16000','-f','f32le','-'], capture_output=True).stdout
    a = np.frombuffer(raw, np.float32)
    segs, _ = m.transcribe(a, language='hi', word_timestamps=True, vad_filter=False, initial_prompt='SIP, mutual fund, units, Large cap, Mid cap, Small cap, KYC, PAN, Aadhaar, UPI Autopay, step one, step two')
    W = [[round(w.start,2), round(w.end,2), w.word.strip()] for s in segs for w in s.words]
    json.dump(W, open(f'vo/words_{f}.json','w'), ensure_ascii=False)
    print(f, round(len(a)/16000,1), ' '.join(f'{w[2]}@{w[0]}' for w in W), flush=True); print(flush=True)
