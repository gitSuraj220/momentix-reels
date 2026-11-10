"""Snap preview frames of reel.html at given times -> build/snap_<t>.jpg. Usage: python3 snap.py 1.0 5.5 ..."""
import asyncio, os, sys
from playwright.async_api import async_playwright
D = os.path.dirname(os.path.abspath(__file__))
async def main():
    os.makedirs(f'{D}/build', exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get('PW_EXE') or None); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('file://' + f'{D}/reel.html'); await pg.wait_for_timeout(2500)
        for t in sys.argv[1:]:
            await pg.evaluate(f"renderAt({t})"); await pg.screenshot(path=f'{D}/build/snap_{t}.jpg', type='jpeg', quality=85)
        print(errs or 'no errors'); await b.close()
asyncio.run(main())
