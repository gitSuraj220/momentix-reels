"""GTA reel: cut Suraj's enhanced take into a tight VO (best takes picked by level/pace), short gaps, atempo + EQ.
Usage: python3 cut.py [tempo]  -> vo48.wav, vo.mp3"""
import subprocess, sys
TEMPO = float(sys.argv[1]) if len(sys.argv) > 1 else 1.18
S = [(2.40, 6.46, 0.12),   # 19 November, raat 12 baje... download karenge
     (7.56, 9.62, 0.16),   # kya internet ke servers melt ho jayenge?
     (15.90, 19.99, 0.16), # Rockstar ke hisaab se... 200 GB (take 2: tighter, louder)
     (24.04, 29.62, 0.16), # India ka average internet speed 60 Mbps...
     (39.06, 42.05, 0.16), # Aur Jio ke 2 GB... 100 din (take 3: tightest, loudest)
     (42.90, 47.49, 0.16), # Ab socho, 2.5 crore log...
     (48.88, 53.71, 0.16), # Lekin preload 10 November...
     (55.36, 58.86, 0.16), # Isliye game pehle se hi...
     (60.08, 64.75, 0.0)]  # Raat 12 baje unlock key...
parts, fl = [], []
for i, (a, b, g) in enumerate(S):
    fl.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={b-a-0.04}:d=0.04,apad=pad_dur={g}[s{i}]")
    parts.append(f"[s{i}]")
fl.append("".join(parts) + f"concat=n={len(S)}:v=0:a=1,aformat=channel_layouts=mono,atempo={TEMPO},highpass=f=80,"
          "equalizer=f=300:t=q:w=1.2:g=-3,equalizer=f=3200:t=q:w=1.0:g=3.5,highshelf=f=8000:g=2.5,"
          "acompressor=threshold=-24dB:ratio=2.5:attack=8:release=120:makeup=2[o]")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'raw_enh.wav', '-filter_complex', ";".join(fl), '-map', '[o]', '-ar', '48000', 'vo48.wav'], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'vo48.wav', '-b:a', '192k', 'vo.mp3'], check=True)
