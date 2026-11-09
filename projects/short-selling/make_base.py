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
cuts = [0, 1.0, 6.04, 17.0, 19.2, 25.5, 29.9, 31.95, 42.8, END]
segs = [
 run(0, 'trim=end_frame=1,setpts=PTS-STARTPTS,'+S+',tpad=stop_mode=clone:stop_duration=2,trim=duration=1', f'{D}/build/seg/s00.mp4', 'c1') or f'{D}/build/seg/s00.mp4',  # frozen first frame (hook)
 seg(1,'c1',cuts[2]-cuts[1]),
 seg(2,'c2',cuts[3]-cuts[2], speed=.8, pingpong=True),
 seg(3,'c3',cuts[4]-cuts[3]),
 seg(4,'c4',cuts[5]-cuts[4], speed=.8),
 seg(5,'c4',cuts[6]-cuts[5], speed=.6, ss=2.5, crop='440:786:0:180'),     # push-in on shocked Bunty
 seg(6,'c4',cuts[7]-cuts[6], speed=.6, ss=2.5, crop='440:786:276:180'),   # push-in on sheepish Momo
 seg(7,'c5',cuts[8]-cuts[7], speed=.9, pingpong=True),
 seg(8,'c6',cuts[9]-cuts[8], speed=.78),
]
open(f'{D}/build/list.txt','w').write(''.join(f"file '{s}'\n" for s in segs))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',f'{D}/build/list.txt','-c:v','libx264','-crf','14','-preset','fast','-t',str(END),f'{D}/build/base.mp4'],check=True)
os.makedirs(f'{D}/build/frames', exist_ok=True)
for f in os.listdir(f'{D}/build/frames'): os.remove(f'{D}/build/frames/{f}')
subprocess.run(['ffmpeg','-v','error','-y','-i',f'{D}/build/base.mp4','-q:v','2',f'{D}/build/frames/f_%04d.jpg'],check=True)
print('frames', len(os.listdir(f'{D}/build/frames')), 'END', END)
