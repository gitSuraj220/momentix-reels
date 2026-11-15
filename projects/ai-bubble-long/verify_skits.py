import json,subprocess,numpy as np
from faster_whisper import WhisperModel
m=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=4)
T=json.load(open('timeline.json'))
raw=subprocess.run(['ffmpeg','-v','error','-i','vo/vo_full.wav','-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
a=np.frombuffer(raw,np.float32)
for s in T['segments']:
    if s['kind']!='skit': continue
    r,_=m.transcribe(a[int(s['start']*16000):int(s['end']*16000)],language='hi')
    print(f"{s['id']:2d} {s['speaker'][:8]:8s} | {s['text'][:40]:40s} | {' '.join(x.text for x in r)}",flush=True)
