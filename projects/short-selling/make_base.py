"""Retime the 6 Kling clips onto the VO timeline -> build/base.mp4 (1080x1920, 30 fps, no audio) + build/frames/."""
import json, os, subprocess
D = os.path.dirname(os.path.abspath(__file__)); TL = json.load(open(f'{D}/timeline.json')); END = TL['END']
os.makedirs(f'{D}/build/seg', exist_ok=True)
S = 'scale=1080:1920:flags=lanczos,setsar=1'
def run(i, vf, out, src):
    subprocess.run(['ffmpeg','-v','error','-y','-i',f'{D}/clips/{src}.mp4','-an','-vf',vf+',fps=30,format=yuv420p','-c:v','libx264','-crf','14','-preset','fast',out],check=True)
def seg(n, src, dur, speed=1.0, ss=0.0, crop=None, pingpong=False):
    out = f'{D}/build/seg/s{n:02d}.mp4'; pre = f'trim=start={ss},setpts=PTS-STARTPTS'
    if crop: pre += f',crop={crop}'
    pre += f',{S},setpts=PTS/{speed}'
    if pingpong:
        tmp = f'{D}/build/seg/f{n:02d}.mp4'; run(n, pre, tmp, src)
        subprocess.run(['ffmpeg','-v','error','-y','-i',tmp,'-filter_complex','[0]split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1,trim=duration=%f,setpts=PTS-STARTPTS'%dur,'-c:v','libx264','-crf','14','-preset','fast',out],check=True)
    else: run(n, pre + f',tpad=stop_mode=clone:stop_duration=3,trim=duration={dur},setpts=PTS-STARTPTS', out, src)
    return out
b = {k: v for k, v in TL.items() if k != 'END'}
MC = {'c1':'440:786:276:180','c4':'440:786:276:180','c5':'380:680:336:220','c6':'420:750:296:160'}   # Momo close-up crops
segs = [
 run(0, 'trim=end_frame=1,setpts=PTS-STARTPTS,'+S+',tpad=stop_mode=clone:stop_duration=2,trim=duration=1', f'{D}/build/seg/s00.mp4', 'c1') or f'{D}/build/seg/s00.mp4',  # frozen first frame (hook)
 seg(1,'c1',3.5),                                                   # B1 Bunty talks
 seg(2,'c1',6.04-4.5, ss=3.5, crop=MC['c1']),                       # M1 starts: Momo close-up
 seg(3,'c2',17.0-6.04, speed=.8, pingpong=True),                    # Momo alone (plan)
 seg(4,'c3',19.2-17.0),                                             # B2 Bunty asks
 seg(5,'c4',25.5-19.2, speed=.8, crop=MC['c4']),                    # M2 Momo close-up
 seg(6,'c4',29.9-25.5, speed=.6, ss=2.5, crop='440:786:0:180'),     # B3 shocked Bunty
 seg(7,'c4',31.95-29.9, speed=.6, ss=2.5, crop=MC['c4']),           # M3 sheepish Momo
 seg(8,'c5',35.0-31.95, speed=.9),                                  # B4
 seg(9,'c5',36.05-35.0, speed=.9, ss=2.75, crop=MC['c5']),          # M4 Momo close-up
 seg(10,'c5',42.75-36.05, speed=.9, pingpong=True),                 # B5 lesson
 seg(11,'c6',45.1-42.75, speed=.78, crop=MC['c6']),                 # M5 Momo close-up
 seg(12,'c6',END-45.1, speed=.78, ss=1.8),                          # B6 follow
]
open(f'{D}/build/list.txt','w').write(''.join(f"file '{s}'\n" for s in segs))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',f'{D}/build/list.txt','-c:v','libx264','-crf','14','-preset','fast','-t',str(END),f'{D}/build/base.mp4'],check=True)
os.makedirs(f'{D}/build/frames', exist_ok=True)
for f in os.listdir(f'{D}/build/frames'): os.remove(f'{D}/build/frames/{f}')
subprocess.run(['ffmpeg','-v','error','-y','-i',f'{D}/build/base.mp4','-q:v','2',f'{D}/build/frames/f_%04d.jpg'],check=True)
print('frames', len(os.listdir(f'{D}/build/frames')), 'END', END)
