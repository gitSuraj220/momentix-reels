import sys,re,subprocess,numpy as np,soundfile as sf
src,dst=sys.argv[1],sys.argv[2]; MAXP=float(sys.argv[3]) if len(sys.argv)>3 else 0.32
subprocess.run(['ffmpeg','-v','error','-y','-i',src,'-ar','48000','-ac','1','tmp.wav'])
x,sr=sf.read('tmp.wav')
out=subprocess.run(['ffmpeg','-i','tmp.wav','-af','silencedetect=noise=-40dB:d=0.2','-f','null','-'],capture_output=True,text=True).stderr
st=[float(v) for v in re.findall(r'silence_start: ([\d.]+)',out)]; en=[float(v) for v in re.findall(r'silence_end: ([\d.]+)',out)]
keep=[]; cur=0
for a,b in zip(st,en):
    if a<0.01: cur=b-0.05; continue   # trim lead silence (keep 50ms)
    if b-a>MAXP:
        keep.append((cur,a+MAXP/2)); cur=b-MAXP/2
keep.append((cur,len(x)/sr))
fade=int(0.01*sr); parts=[]
for a,b in keep:
    seg=x[int(a*sr):int(b*sr)].copy()
    seg[:fade]*=np.linspace(0,1,fade); seg[-fade:]*=np.linspace(1,0,fade); parts.append(seg)
y=np.concatenate(parts); sf.write(dst,y,sr)
print(src, 'orig',round(len(x)/sr,2),'->',round(len(y)/sr,2),'pauses cut',len(keep)-1)
