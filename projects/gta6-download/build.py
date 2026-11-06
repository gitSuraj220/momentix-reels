"""Inject timeline, stills, clip frames and anchor positions into reel.html -> reel_built.html.
usage: python3 build.py [t1 t2 ...]   (snapshots -> build/snap_<t>.jpg + build/sheet.jpg)"""
import json, sys, os, glob, asyncio, subprocess
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__))
TL = json.load(open(f'{D}/vo/timeline.json'))
art = {os.path.basename(p)[:-4]: {'src': 'file://' + p} for p in sorted(glob.glob(f'{D}/ai/*.png'))}
clips = {}
for mp4 in sorted(glob.glob(f'{D}/clips/c_*.mp4')):
    name = os.path.basename(mp4)[:-4]; out = f'{D}/build/frames/{name}'
    if not os.path.exists(f'{out}/0001.jpg') or os.path.getmtime(mp4) > os.path.getmtime(f'{out}/0001.jpg'):
        os.makedirs(out, exist_ok=True)
        for f in glob.glob(f'{out}/*.jpg'): os.remove(f)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', mp4, '-vf', 'fps=30,scale=1080:1920:flags=lanczos', '-q:v', '2', f'{out}/%04d.jpg'], check=True)
    clips[name] = {'dir': 'file://' + out, 'n': len(glob.glob(f'{out}/*.jpg'))}
pos = json.load(open(f'{D}/pos.json')) if os.path.exists(f'{D}/pos.json') else {}
html = open(f'{D}/reel.html').read()
for k, v in [('/*TL*/null', json.dumps(TL)), ('/*ART*/{}', json.dumps(art)), ('/*CLIPS*/{}', json.dumps(clips)),
             ('/*FONTS*/', 'file://' + os.path.abspath(f'{D}/../../engine/fonts'))]:
    html = html.replace(k, v)
open(f'{D}/reel_built.html', 'w').write(html)
print('built; art:', sorted(art), 'clips:', {k: v['n'] for k, v in clips.items()})
ts = [float(x) for x in sys.argv[1:]]
if ts:
    from playwright.async_api import async_playwright
    async def snap():
        async with async_playwright() as p:
            b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
            pg.on('console', lambda m: print('console:', m.text)); pg.on('pageerror', lambda e: print('ERR', e))
            await pg.goto('file://' + f'{D}/reel_built.html'); await pg.wait_for_timeout(1000)
            for t in ts:
                await pg.evaluate(f'renderAt({t})'); await pg.wait_for_timeout(60)
                await pg.screenshot(path=f'{D}/build/snap_{t:05.2f}.jpg', type='jpeg', quality=85)
            await b.close()
    asyncio.run(snap())
    ims = [Image.open(f'{D}/build/snap_{t:05.2f}.jpg') for t in ts]
    w, h = 270, 480; cols = min(6, len(ims)); rows = (len(ims) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * w, rows * h), 'white')
    for i, im in enumerate(ims): sheet.paste(im.resize((w, h)), ((i % cols) * w, (i // cols) * h))
    sheet.save(f'{D}/build/sheet.jpg', quality=85); print('sheet saved')
