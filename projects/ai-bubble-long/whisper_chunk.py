from faster_whisper import WhisperModel
import json, subprocess, numpy as np, sys
m = WhisperModel('small', device='cpu', compute_type='int8', cpu_threads=4)
for f in sys.argv[1:]:
    raw = subprocess.run(['ffmpeg','-v','error','-i',f'vo/{f}.mp3','-ac','1','-ar','16000','-f','f32le','-'], capture_output=True).stdout
    a = np.frombuffer(raw, np.float32); W=[]
    # cut at quiet points near every ~12 s
    e=np.array([np.sqrt(np.mean(a[i:i+800]**2)) for i in range(0,len(a),800)])
    cuts=[0]; t=12*20
    while t < len(e)-60:
        w=e[t-40:t+40]; k=t-40+int(np.argmin(w)); cuts.append(k*800); t=k+12*20
    cuts.append(len(a))
    for c0,c1 in zip(cuts,cuts[1:]):
        segs,_=m.transcribe(a[c0:c1], language='hi', word_timestamps=True, condition_on_previous_text=False)
        W+=[[round(w.start+c0/16000,2), round(w.end+c0/16000,2), w.word.strip()] for s in segs for w in s.words]
    json.dump(W, open(f'vo/words_{f}.json','w'), ensure_ascii=False)
    print(f, ' '.join(f'{w[2]}@{w[0]}' for w in W), flush=True); print(flush=True)
