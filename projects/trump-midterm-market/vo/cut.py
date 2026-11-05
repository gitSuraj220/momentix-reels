"""Cut Suraj's enhanced take into a tight VO: picks take 2 of 'Aur Indian market...', 0.26 s gaps, atempo."""
import subprocess, sys
TEMPO=float(sys.argv[1]) if len(sys.argv)>1 else 1.08
S=[(2.90,4.50,0.14),   # Trump election haar gaye?
   (8.86,12.08,0.24),  # Aur Indian market mein bull run chalu ho jayega kya? (take 2)
   (12.18,16.28,0.24), # Dekho, Trump abhi bhi President hain...
   (19.93,23.30,0.24), # Matlab ab naye tariff...
   (26.30,33.68,0.24), # Tariff ka darr kam... 4,000 points upar
   (36.68,43.66,0.0)]  # Toh kya bull run pakka?... palat sakta hai (comment line dropped, Suraj 5 Nov)
parts=[];fl=[]
for i,(a,b,g) in enumerate(S):
    fl.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={b-a-0.04}:d=0.04,apad=pad_dur={g}[s{i}]")
    parts.append(f"[s{i}]")
fl.append("".join(parts)+f"concat=n={len(S)}:v=0:a=1,aformat=channel_layouts=mono,atempo={TEMPO},highpass=f=80,equalizer=f=300:t=q:w=1.2:g=-3,equalizer=f=3200:t=q:w=1.0:g=3.5,highshelf=f=8000:g=2.5,acompressor=threshold=-24dB:ratio=2.5:attack=8:release=120:makeup=2[o]")
subprocess.run(['ffmpeg','-v','error','-y','-i','raw_enh.wav','-filter_complex',";".join(fl),'-map','[o]','-ar','48000','vo48.wav'],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-i','vo48.wav','-b:a','192k','vo.mp3'],check=True)
