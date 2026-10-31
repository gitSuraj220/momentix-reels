"""Inject timeline + art into reel.html -> reel_built.html; optional snapshot frames.
usage: python3 build.py [t1 t2 ...]   (snapshots to build/snap_<t>.jpg)"""
import json, sys, os, glob, asyncio
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__))
TL = json.load(open(f'{D}/vo/timeline.json'))
KEYS = {'sheet': 'art_00_sheet', 'hook': 'art_01_hook', 'picks': 'art_02_picks', 'v2008': 'art_03_2008',
        'vflat': 'art_04_flat', 'vcovid': 'art_05_covid', 'v2025': 'art_06_2025', 'v2026': 'art_07_2026'}
art = {}
for k, stem in KEYS.items():
    p = f'{D}/ai/{stem}.png'
    if os.path.exists(p):
        w, h = Image.open(p).size
        art[k] = {'src': 'file://' + p, 'w': w, 'h': h}
html = open(f'{D}/reel.html').read().replace('/*TL*/null', json.dumps(TL)).replace('/*ART*/{}', json.dumps(art))
open(f'{D}/reel_built.html', 'w').write(html)
print('built; art:', sorted(art))
ts = [float(x) for x in sys.argv[1:]]
if ts:
    from playwright.async_api import async_playwright
    async def snap():
        os.makedirs(f'{D}/build', exist_ok=True)
        async with async_playwright() as p:
            b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
            await pg.goto('file://' + f'{D}/reel_built.html'); await pg.wait_for_timeout(800)
            for t in ts:
                await pg.evaluate(f'renderAt({t})'); await pg.wait_for_timeout(120)
                await pg.screenshot(path=f'{D}/build/snap_{t:05.2f}.jpg', type='jpeg', quality=85)
            await b.close()
    asyncio.run(snap())
    ims = [Image.open(f) for f in sorted(glob.glob(f'{D}/build/snap_*.jpg')) if float(os.path.basename(f)[5:-4]) in ts]
    w, h = 270, 480; cols = min(6, len(ims)); rows = (len(ims) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * w, rows * h), 'white')
    for i, im in enumerate(ims): sheet.paste(im.resize((w, h)), ((i % cols) * w, (i // cols) * h))
    sheet.save(f'{D}/build/sheet.jpg', quality=85); print('sheet saved')
