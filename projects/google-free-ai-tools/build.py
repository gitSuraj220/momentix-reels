"""reel.html (from second Claude) -> reel_built.html with local fonts; optional snapshots: python3 build.py t1 t2 ..."""
import os, sys, asyncio, re
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__)); F = 'file:///usr/share/fonts/truetype/google-fonts/'
html = open(f'{D}/reel.html').read()
html = re.sub(r'<link[^>]*fonts\.(googleapis|gstatic)\.com[^>]*>', '', html)
faces = ''.join(f"@font-face{{font-family:'Poppins';src:url('{F}{f}');font-weight:{w}}}" for f, w in
                [('Poppins-Regular.ttf', 400), ('Poppins-Medium.ttf', 500), ('Poppins-Bold.ttf', 600), ('Poppins-Bold.ttf', 700), ('Poppins-Bold.ttf', 800), ('Poppins-Bold.ttf', 900)])
faces += f"@font-face{{font-family:'Lora';src:url('{F}Lora-Italic-Variable.ttf');font-style:italic;font-weight:400 700}}@font-face{{font-family:'Lora';src:url('{F}Lora-Variable.ttf');font-weight:400 700}}"
html = html.replace('<style>', '<style>' + faces, 1)
open(f'{D}/reel_built.html', 'w').write(html)
ts = [float(x) for x in sys.argv[1:]]
if ts:
    from playwright.async_api import async_playwright
    async def snap():
        os.makedirs(f'{D}/build', exist_ok=True)
        async with async_playwright() as p:
            b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
            pg.on('pageerror', lambda e: print('ERR', e)); pg.on('console', lambda m: print('console:', m.text) if m.type == 'error' else None)
            await pg.goto('file://' + f'{D}/reel_built.html'); await pg.wait_for_timeout(800)
            for t in ts:
                await pg.evaluate(f'renderAt({t})'); await pg.wait_for_timeout(50)
                await pg.screenshot(path=f'{D}/build/snap_{t:05.2f}.jpg', type='jpeg', quality=85)
            await b.close()
    asyncio.run(snap())
    ims = [Image.open(f'{D}/build/snap_{t:05.2f}.jpg') for t in ts]
    w, h = 270, 480; cols = min(6, len(ims)); rows = (len(ims) + cols - 1) // cols
    sh = Image.new('RGB', (cols * w, rows * h), 'white')
    for i, im in enumerate(ims): sh.paste(im.resize((w, h)), ((i % cols) * w, (i // cols) * h))
    sh.save(f'{D}/build/sheet.jpg', quality=85); print('sheet ok')
