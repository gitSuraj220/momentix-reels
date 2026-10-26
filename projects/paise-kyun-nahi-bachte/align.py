import json, re, subprocess, numpy as np, sys
def spoken_len(s):
    s=s.replace('10','das').replace('24','chaubees')
    s=re.sub(r'\bSIP\b','es aai pee',s)
    return len(re.sub(r'[^A-Za-z]','',s))
def segs_of(f,d=0.25,db=-38):
    out=subprocess.run(['ffmpeg','-v','info','-i',f,'-af',f'silencedetect=noise={db}dB:d={d}','-f','null','-'],capture_output=True,text=True).stderr
    st=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',out)]; en=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',out)]
    dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
    segs=[];cur=0.0
    for a,b in zip(st,en):
        if a>cur+0.05: segs.append((cur,a))
        cur=b
    if cur<dur-0.05: segs.append((cur,dur))
    return segs,dur
def align(f,FR):
    segs,dur=segs_of(f)
    L=[spoken_len(x) for _,x in FR]; S=[e-s for s,e in segs]; rate=sum(S)/sum(L)
    n,m=len(FR),len(segs);INF=1e18;D=np.full((n+1,m+1),INF);P={};D[0,0]=0
    for i in range(n+1):
      for j in range(m+1):
        if D[i,j]>=INF: continue
        for k in range(1,5):
          for q in range(1,4):
            if k>1 and q>1: continue
            if i+k>n or j+q>m: continue
            c=(sum(S[j:j+q])-rate*sum(L[i:i+k]))**2+0.15*(k+q-2)
            if D[i,j]+c<D[i+k,j+q]: D[i+k,j+q]=D[i,j]+c;P[(i+k,j+q)]=(i,j)
    i,j=n,m;g=[]
    while (i,j)!=(0,0):
        pi,pj=P[(i,j)];g.append((pi,i,pj,j));i,j=pi,pj
    g.reverse();ft=[None]*n
    for a,b,c,d in g:
        t0,t1=segs[c][0],segs[d-1][1];tot=sum(L[a:b]);t=t0
        for x in range(a,b):
            dd=(t1-t0)*L[x]/tot;ft[x]=(round(t,3),round(t+dd,3));t+=dd
    return [{'line':ln,'text':x,'s':a,'e':b} for (ln,x),(a,b) in zip(FR,ft)],dur
B=[(1,'Salary aayi…'),(1,'aur 10 din mein gayab.'),(1,'Paise tikte kyun nahi?'),(3,'Mithai?'),(3,'Matlab…'),(3,'samjha nahi.')]
M=[(2,'Kyunki tumhara dimaag…'),(2,'mithai ka aadi ho gaya hai.'),(4,'Dekho…'),(4,'10 minute delivery…'),(4,'sale…'),(4,'ek tap pe order.'),(5,'Har order pe dopamine ka jhatka.'),(5,'Turant maza.'),(6,'Aur SIP?'),(6,'Paisa jaata hai…'),(6,'par kuch dikhta nahi.'),(6,'Isliye pheeka lagta hai.'),(7,'Toh dimaag ko harao…'),(7,'salary aate hi SIP auto-debit.'),(8,'App se card hatao…'),(8,'aur khareedne se pehle 24 ghante ruko.'),(9,'Shuru mein boring…'),(9,'par yahi chhota paudha…'),(9,'ek din ped banta hai.')]
for f,FR in [('bunty_1.mp3',B),('momo_1.mp3',M)]:
    r,d=align(f,FR); print('==',f,d)
    for x in r: print(x['line'],x['s'],x['e'],x['text'])
    json.dump(r,open(f.replace('.mp3','_frags.json'),'w'),ensure_ascii=False,indent=1)
print(segs_of('momo_1.mp3')[0])
