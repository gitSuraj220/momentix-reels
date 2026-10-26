# Cut the voice takes into phrases, close up pauses, speed up slightly, and write words.json (phrase cues).
import json, subprocess
SR=48000; TEMPO=1.10
P=[ # (src, start, end, gap_before, id, roman text)
 ('momo',0.00,2.62,0.00,'hook1','Jio ke shares bechne se pehle ye dekh lo'),
 ('momo',2.90,4.42,0.10,'hook2','nahi toh bada loss ho jayega'),
 ('bunty_a',0.00,0.80,0.30,'b1','Kaisa loss?'),
 ('bunty_a',1.12,5.77,0.12,'b2','50% upar list hua toh ₹1 lakh ke ₹1.5 lakh'),
 ('bunty_a',6.05,7.84,0.10,'b3','₹50,000 ka profit!'),
 ('momo',4.76,5.14,0.30,'ruko','Ruko.'),
 ('momo',5.62,7.11,0.18,'m1','Ek saal se pehle becha'),
 ('momo',7.31,10.80,0.08,'m2','toh profit pe 20% tax, upar se 4% cess'),
 ('momo',11.15,13.30,0.14,'m3','₹10,400 seedha sarkaar ko'),
 ('momo',13.65,15.47,0.22,'m4','Upar se STT aur charges'),
 ('momo',15.70,17.32,0.06,'m5','lagbhag ₹170 aur'),
 ('momo',17.63,20.48,0.22,'m6','Toh asli profit ₹39,430'),
 ('momo',20.91,21.89,0.14,'m7','50% nahi'),
 ('momo',22.12,23.45,0.08,'m8','sirf 39%'),
 ('momo',23.78,25.22,0.26,'m9','Aur ek saal ke baad becha?'),
 ('momo',25.58,28.62,0.12,'m10','Toh tax 20% nahi, sirf 12.5%'),
 ('momo',28.96,31.58,0.16,'m11','Upar se har saal pehla ₹1.25 lakh ka profit'),
 ('momo',31.74,32.22,0.02,'m12','tax-free'),
 ('momo',32.59,34.18,0.18,'m13','toh is ₹50,000 pe tax'),
 ('momo',34.41,35.00,0.10,'m14','zero!'),
 ('bunty_a',8.05,8.62,0.40,'b4','Wah!'),
 ('bunty_a',9.13,11.21,0.14,'b5','Waise mera tax toh zero hai'),
 ('bunty_a',11.55,13.42,0.08,'b6','kyunki Jio ka share mila hi nahi!'),
]
parts=[]; t=0.25; cues=[]
import numpy as np
def load(src,s,e):
    raw=subprocess.run(['ffmpeg','-v','error','-ss',str(s),'-to',str(e),'-i',f'{src}.mp3','-af',f'atempo={TEMPO},highpass=f=70','-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout
    x=np.frombuffer(raw,dtype=np.float32).copy(); n=int(0.012*SR); x[:n]*=np.linspace(0,1,n); x[-n:]*=np.linspace(1,0,n); return x
segs=[]
for src,s,e,g,i,txt in P:
    x=load(src,s,e); t+=g/TEMPO; segs.append((int(t*SR),x)); cues.append({'id':i,'who':'bunty' if src.startswith('bunty') else 'momo','w':txt,'s':round(t,3),'e':round(t+len(x)/SR,3)}); t+=len(x)/SR
total=t+1.6; out=np.zeros(int(total*SR)+SR,dtype=np.float32)
for st,x in segs: out[st:st+len(x)]+=x
open('vo.raw','wb').write(out.tobytes())
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar',str(SR),'-ac','1','-i','vo.raw','-t',str(total),'vo.wav'])
json.dump(cues,open('cues.json','w'),ensure_ascii=False,indent=1)
print(round(total,2)); [print(c['s'],c['e'],c['id'],c['w']) for c in cues]
