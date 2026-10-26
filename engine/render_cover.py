import asyncio, os, sys
from playwright.async_api import async_playwright
# usage (in video dir): python render_cover.py cover.html Cover.jpg   (cover.html = scene_built.html + a window.cover() script, see examples/)
async def m():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1920})
        errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
        await pg.goto('file://'+os.path.abspath(sys.argv[1])); await pg.wait_for_timeout(800)
        await pg.evaluate('cover()'); await pg.wait_for_timeout(300)
        await pg.screenshot(path=sys.argv[2],type='jpeg',quality=94); print('errors:',errs); await b.close()
asyncio.run(m())
