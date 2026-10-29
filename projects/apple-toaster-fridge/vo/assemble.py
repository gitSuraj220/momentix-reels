import json, subprocess, numpy as np
SR=48000; TEMPO=1.08
P=[('bunty',0.00,2.76,0.00,'b1','Apple ne aaj touchscreen MacBook launch kiya!'),
 ('momo',0.00,0.90,0.30,'m1','Wahi Apple…'),
 ('momo',1.09,4.27,0.08,'m2','jisne 14 saal pehle Microsoft ka mazaak udaya tha 😂'),
 ('momo',4.63,7.44,0.26,'m3','Microsoft ne laptop aur tablet ko ek bana diya,'),
 ('momo',7.75,9.11,0.06,'m4','toh Apple ke CEO bole —'),
 ('momo',9.56,12.21,0.10,'m5','ye toh aisa hai jaise toaster aur fridge ko jod do.'),
 ('momo',12.54,13.37,0.16,'m6','Ban toh jayega…'),
 ('momo',13.78,15.13,0.10,'m7','par kisi ko pasand nahi aayega.'),
 ('momo',15.59,17.56,0.30,'m8','Usse pehle Steve Jobs bole the —'),
 ('momo',17.86,20.49,0.06,'m9','screen ko touch karte karte haath hi thak jaayega.'),
 ('momo',20.85,21.35,0.30,'m10','Aur aaj?'),
 ('momo',21.67,23.99,0.10,'m11','Apple ne khud wahi toaster-fridge bana diya —'),
 ('momo',24.35,25.67,0.08,'m12','touchscreen MacBook Pro…'),
 ('momo',26.16,28.44,0.12,'m13','₹3,49,900 se shuru!'),
 ('bunty',3.18,7.08,0.35,'b2','Matlab ab toast bhi banega aur thanda bhi rahega?'),
 ('momo',28.78,29.14,0.30,'m14','Haan…'),
 ('momo',29.39,30.89,0.08,'m15','bas ₹3.5 lakh mein. 😂'),
]
def load(src,s,e):
    raw=subprocess.run(['ffmpeg','-v','error','-ss',str(s),'-to',str(e),'-i',f'{src}.mp3','-af',f'atempo={TEMPO},highpass=f=70','-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout
    x=np.frombuffer(raw,dtype=np.float32).copy(); n=int(0.012*SR); x[:n]*=np.linspace(0,1,n); x[-n:]*=np.linspace(1,0,n); return x
t=0.12; segs=[]; cues=[]
for src,s,e,g,i,txt in P:
    x=load(src,s,e); t+=g; segs.append((int(t*SR),x)); cues.append({'id':i,'who':src,'w':txt,'s':round(t,3),'e':round(t+len(x)/SR,3)}); t+=len(x)/SR
total=t+1.0; out=np.zeros(int(total*SR)+SR,dtype=np.float32)
for st,x in segs: out[st:st+len(x)]+=x
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar',str(SR),'-ac','1','-i','-','-t',str(total),'vo.wav'],input=out.tobytes())
json.dump(cues,open('cues.json','w'),ensure_ascii=False,indent=1)
print(round(total,2)); [print(c['s'],c['e'],c['id'],c['w']) for c in cues]
