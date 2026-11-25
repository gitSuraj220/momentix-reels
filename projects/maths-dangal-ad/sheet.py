import sys, glob
from PIL import Image, ImageDraw
fs = sorted(glob.glob(sys.argv[1] + '_*.png')); w, h = 360, 640; cols = 4
s = Image.new('RGB', (w * cols, h * ((len(fs) + cols - 1) // cols)), 'black'); d = ImageDraw.Draw(s)
for i, f in enumerate(fs): s.paste(Image.open(f).convert('RGB').resize((w, h)), ((i % cols) * w, (i // cols) * h)); d.text(((i % cols) * w + 6, (i // cols) * h + 6), f.split('_')[-1][:-4], fill='yellow')
s.save(sys.argv[2], quality=85)
