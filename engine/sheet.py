# usage: python sheet.py audit/f audit/sheet  -> 24-frame contact sheets with safe-zone box
import sys,glob
from PIL import Image,ImageDraw
pre=sys.argv[1]; out=sys.argv[2]
fs=sorted(glob.glob(pre+'_*.jpg'),key=lambda f:float(f.rsplit('_',1)[1][:-4]))
W,H=270,480
for si in range(0,len(fs),24):
    im=Image.new('RGB',(W*8,H*3),'white')
    for i,f in enumerate(fs[si:si+24]):
        a=Image.open(f).resize((W,H)); dd=ImageDraw.Draw(a); dd.rectangle([35/4,240/4,1045/4,1460/4],outline='red')
        dd.text((6,4),f.rsplit('_',1)[1][:-4],fill='yellow'); im.paste(a,((i%8)*W,(i//8)*H))
    im.save(f'{out}_{si//24:02d}.jpg',quality=85)
