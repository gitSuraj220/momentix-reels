import json, subprocess, numpy as np
SR=48000; TEMPO=1.13
P=[('momo_a',0.00,2.76,0.00,'h1','Ye samosa mere gaon mein ₹10 ka milta tha'),
 ('momo_a',3.16,4.15,0.10,'h2','aaj ₹20 ka.'),
 ('momo_a',4.64,5.58,0.18,'h3','Samosa wahi,'),
 ('momo_a',5.82,6.99,0.06,'h4','phir daam double kaise?'),
 ('momo_a',7.39,9.59,0.28,'p1','Pehle, ₹100 mein 10 samose.'),
 ('momo_a',9.94,12.59,0.24,'p2','10 saal baad, wahi samosa ₹20 ka.'),
 ('momo_a',13.07,14.48,0.16,'p3','Ab ₹100 mein 10 nahi…'),
 ('momo_a',14.76,15.91,0.06,'p4','sirf 5 samose.'),
 ('momo_a',16.28,18.09,0.26,'t1','Wahi size, wahi swaad…'),
 ('momo_a',18.36,20.93,0.06,'t2','bas tumhare ₹100 ki taakat aadhi ho gayi.'),
 ('momo_a',21.38,23.06,0.16,'t3','Isi ko kehte hain inflation.'),
 ('momo_a',23.41,26.71,0.28,'w1','Kyunki aloo, tel, gas aur halwai ki mehnat'),
 ('momo_a',26.98,28.94,0.06,'w2','sab har saal thode mehnge hote hain.'),
 ('momo_a',29.33,32.42,0.28,'s1','Aur agar tumhare paise 3% wale savings mein pade hain,'),
 ('momo_a',32.70,34.88,0.08,'s2','aur mehngai 7% se badh rahi hai…'),
 ('momo_a',35.31,36.58,0.16,'s3','toh paisa badh nahi raha,'),
 ('momo_a',36.90,37.62,0.04,'s4','ghat raha hai.'),
 ('bunty',0.00,3.05,0.40,'b1','Matlab mere paise se samosa bhi chhota ho gaya!'),
]
def load(src,s,e):
    raw=subprocess.run(['ffmpeg','-v','error','-ss',str(s),'-to',str(e),'-i',f'{src}.mp3','-af',f'atempo={TEMPO},highpass=f=70','-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout
    x=np.frombuffer(raw,dtype=np.float32).copy(); n=int(0.012*SR); x[:n]*=np.linspace(0,1,n); x[-n:]*=np.linspace(1,0,n); return x
t=0.15; segs=[]; cues=[]
for src,s,e,g,i,txt in P:
    x=load(src,s,e); t+=g; segs.append((int(t*SR),x)); cues.append({'id':i,'who':'bunty' if src=='bunty' else 'momo','w':txt,'s':round(t,3),'e':round(t+len(x)/SR,3)}); t+=len(x)/SR
total=t+1.2; out=np.zeros(int(total*SR)+SR,dtype=np.float32)
for st,x in segs: out[st:st+len(x)]+=x
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar',str(SR),'-ac','1','-i','-','-t',str(total),'vo.wav'],input=out.tobytes())
json.dump(cues,open('cues.json','w'),ensure_ascii=False,indent=1)
print(round(total,2)); [print(c['s'],c['e'],c['id'],c['w']) for c in cues]
