"""reel.html -> reel_built.html (timeline + asset path); optional snapshots: python3 build.py t1 t2 ..."""
import json, os, sys, asyncio
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__))
TL = json.load(open(f'{D}/vo/timeline.json'))
html = open(f'{D}/reel.html').read().replace('/*TL*/null', json.dumps(TL)).replace("/*ASSET*/''", json.dumps('file://' + D + '/assets'))
open(f'{D}/reel_built.html', 'w').write(html)
ts = [float(x) for x in sys.argv[1:]]
if ts:
    from playwright.async_api import async_playwright
    async def snap():
        os.makedirs(f'{D}/build', exist_ok=True)
        async with async_playwright() as p:
            b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
            pg.on('pageerror', lambda e: print('ERR', e))
            await pg.goto('file://' + f'{D}/reel_built.html'); await pg.wait_for_timeout(600)
            for t in ts:
                await pg.evaluate(f'renderAt({t})'); await pg.wait_for_timeout(40)
                await pg.screenshot(path=f'{D}/build/snap_{t:05.2f}.jpg', type='jpeg', quality=80)
            await b.close()
    asyncio.run(snap())
    ims = [Image.open(f'{D}/build/snap_{t:05.2f}.jpg') for t in ts]
    w, h = 216, 384; cols = min(8, len(ims)); rows = (len(ims) + cols - 1) // cols
    sh = Image.new('RGB', (cols * w, rows * h), 'white')
    for i, im in enumerate(ims): sh.paste(im.resize((w, h)), ((i % cols) * w, (i // cols) * h))
    sh.save(f'{D}/build/sheet.jpg', quality=82); print('sheet ok')
