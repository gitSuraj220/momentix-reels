import json, re, subprocess, numpy as np
import sys
# usage: python align.py fragments.json [OFF]   (run in the video folder with vo.mp3)
# fragments.json = [[line_no, "Roman caption fragment"], ...] split at … ? . , boundaries, in spoken order
# optional speak.json = {"13 crore":"terah karod", "SIR":"es aai aar", ...} to weight acronyms/numbers by how they are spoken
FR=[tuple(x) for x in json.load(open(sys.argv[1]))]
OFF_ARG=float(sys.argv[2]) if len(sys.argv)>2 else 0.35
import os
SPEAK=json.load(open('speak.json')) if os.path.exists('speak.json') else {}
def spoken_len(s):
    for k,v in SPEAK.items(): s=s.replace(k,v)
    return len(re.sub(r'[^A-Za-z]','',s))
out=subprocess.run(['ffmpeg','-v','info','-i','vo.mp3','-af','silencedetect=noise=-38dB:d=0.25','-f','null','-'],capture_output=True,text=True).stderr
st=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',out)]; en=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',out)]
dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','vo.mp3'],capture_output=True,text=True).stdout)
segs=[]; cur=0.0
for a,b in zip(st,en):
    if a>cur+0.05: segs.append((cur,a))
    cur=b
if cur<dur-0.05: segs.append((cur,dur))
L=[spoken_len(f) for _,f in FR]; S=[e-s for s,e in segs]
rate=sum(S)/sum(L); n,m=len(FR),len(segs)
INF=1e18; D=np.full((n+1,m+1),INF); P={}; D[0,0]=0
for i in range(n+1):
  for j in range(m+1):
    if D[i,j]>=INF: continue
    for k in range(1,5):
      for q in range(1,4):
        if k>1 and q>1: continue
        if i+k>n or j+q>m: continue
        c=(sum(S[j:j+q])-rate*sum(L[i:i+k]))**2 + 0.15*(k+q-2)
        if D[i,j]+c<D[i+k,j+q]: D[i+k,j+q]=D[i,j]+c; P[(i+k,j+q)]=(i,j)
i,j=n,m; groups=[]
while (i,j)!=(0,0):
    pi,pj=P[(i,j)]; groups.append((pi,i,pj,j)); i,j=pi,pj
groups.reverse(); frag_t=[None]*n
for a,b,c,d in groups:
    t0,t1=segs[c][0],segs[d-1][1]; tot=sum(L[a:b]); t=t0
    for f in range(a,b):
        dd=(t1-t0)*L[f]/tot; frag_t[f]=(round(t,3),round(t+dd,3)); t+=dd
for (ln,f),(a,b) in zip(FR,frag_t): print(ln,f"{a:6.2f}-{b:6.2f}",f)
OFF=OFF_ARG
fr=[{'line':ln,'text':f,'s':round(a+OFF,3),'e':round(b+OFF,3)} for (ln,f),(a,b) in zip(FR,frag_t)]
chunks=[]
for f in fr:
    words=f['text'].split(); groups=[]; g=[]
    for w in words:
        g.append(w)
        if len(g)>=3 or len(' '.join(g))>=17 or w[-1] in ',…?.!:': groups.append(g); g=[]
    if g: groups.append(g)
    tot=sum(len(' '.join(x)) for x in groups); t=f['s']
    for x in groups:
        d=(f['e']-f['s'])*len(' '.join(x))/tot
        chunks.append({'t':round(t,3),'e':round(t+d,3),'text':' '.join(x),'line':f['line']}); t+=d
for a,b in zip(chunks,chunks[1:]):
    if b['t']-a['e']<0.7: a['e']=b['t']
lines={}
for f in fr: lines.setdefault(f['line'],[f['s'],f['e']]); lines[f['line']][1]=f['e']
json.dump({'off':OFF,'frags':fr,'chunks':chunks,'lines':lines,'end':round(fr[-1]['e']+1.6,2)},open('timeline.json','w'),ensure_ascii=False,indent=1)
print('segs',m,'frags',n,'end',fr[-1]['e']+1.6)
