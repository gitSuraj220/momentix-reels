"""Buy vs Rent reel: cut Suraj's enhanced take into a tight VO (best takes picked by level/pace), short gaps, atempo + EQ.
Usage: python3 cut.py [tempo]  -> vo48.wav, vo.mp3"""
import subprocess, sys
TEMPO = float(sys.argv[1]) if len(sys.argv) > 1 else 1.17
S = [(11.10, 16.89, 0.16),  # L1 Ghar khareedna... chaunk jaoge (take 4, the only full one)
     (33.42, 37.63, 0.10),  # L2 Bunty ek 80 lakh ka flat... down payment (take 2)
     (38.15, 40.92, 0.10),  #    upar se 6 lakh stamp duty aur registration
     (41.64, 43.13, 0.16),  #    so total 22 lakh
     (47.33, 50.15, 0.10),  # L3 Phir aati hai har mahine 53,000 ki EMI
     (52.41, 53.30, 0.10),  #    20 saal ke liye
     (61.80, 64.46, 0.16),  #    matlab 64 lakh interest seedha bank ko (last take)
     (68.19, 72.24, 0.10),  # L4 Momo wahi flat 20,000 rent pe leta hai
     (75.25, 78.12, 0.16),  #    aur bacha hua saara paisa... invest karta hai (retake)
     (80.27, 83.39, 0.10),  # L5 20 saal baad Bunty ka flat 3 crore
     (83.91, 87.29, 0.16),  #    Momo ka investment 12% pe 5 crore
     (89.94, 94.49, 0.10),  # L6 Momo Bunty se aage tabhi nikla...
     (95.14, 98.91, 0.10),  #    market upar ho ya neeche...
     (104.51, 107.73, 0.16),#    isliye SIP mein discipline... (take 2)
     (108.25, 117.78, 0.0)] # L7 Matlab rent hamesha sahi nahi...
parts, fl = [], []
for i, (a, b, g) in enumerate(S):
    fl.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={b-a-0.04}:d=0.04,apad=pad_dur={g}[s{i}]")
    parts.append(f"[s{i}]")
fl.append("".join(parts) + f"concat=n={len(S)}:v=0:a=1,aformat=channel_layouts=mono,atempo={TEMPO},highpass=f=80,"
          "equalizer=f=300:t=q:w=1.2:g=-3,equalizer=f=3200:t=q:w=1.0:g=3.5,highshelf=f=8000:g=2.5,"
          "acompressor=threshold=-24dB:ratio=2.5:attack=8:release=120:makeup=2[o]")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'raw_enh.wav', '-filter_complex', ";".join(fl), '-map', '[o]', '-ar', '48000', 'vo48.wav'], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'vo48.wav', '-b:a', '192k', 'vo.mp3'], check=True)
