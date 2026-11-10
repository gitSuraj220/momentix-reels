"""Hook (Kling c1 walk-in + c2 smash) and ending still (kf3) -> build/base.mp4 + frames. UI middle is drawn in reel.html."""
import os, subprocess
D = os.path.dirname(os.path.abspath(__file__)); os.makedirs(f'{D}/build/seg', exist_ok=True)
S = 'scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p'
def ff(args): subprocess.run(['ffmpeg','-v','error','-y']+args, check=True)
H1, H2, UI_END, END = 3.2, 9.2, 44.5, 47.0
ff(['-i',f'{D}/clips/c1.mp4','-an','-vf',f'trim=0:{H1},setpts=PTS-STARTPTS,{S}','-c:v','libx264','-crf','14',f'{D}/build/seg/a.mp4'])
ff(['-i',f'{D}/clips/c2.mp4','-an','-vf',f'setpts=PTS/0.84,{S},tpad=stop_mode=clone:stop_duration=2,trim=duration={H2-H1}','-c:v','libx264','-crf','14',f'{D}/build/seg/b.mp4'])
ff(['-f','lavfi','-i',f'color=c=black:s=1080x1920:r=30:d={UI_END-H2}','-vf','format=yuv420p','-c:v','libx264','-crf','14',f'{D}/build/seg/c.mp4'])
# ending: kf3 slow push-in toward the bat
ff(['-loop','1','-i',f'{D}/art/gta_kf3.png','-vf',f"scale=2160:-1,zoompan=z='1+0.0016*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={int((END-UI_END)*30)}:s=1080x1920:fps=30,format=yuv420p",
    '-frames:v',str(int((END-UI_END)*30)),'-c:v','libx264','-crf','14',f'{D}/build/seg/d.mp4'])
open(f'{D}/build/list.txt','w').write(''.join(f"file '{D}/build/seg/{x}.mp4'\n" for x in 'abcd'))
ff(['-f','concat','-safe','0','-i',f'{D}/build/list.txt','-c:v','libx264','-crf','14','-t',str(END),f'{D}/build/base.mp4'])
os.makedirs(f'{D}/build/frames', exist_ok=True)
for f in os.listdir(f'{D}/build/frames'): os.remove(f'{D}/build/frames/{f}')
ff(['-i',f'{D}/build/base.mp4','-q:v','2',f'{D}/build/frames/f_%04d.jpg']); print('frames', len(os.listdir(f'{D}/build/frames')))
