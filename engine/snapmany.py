# usage (in video dir): python snapmany.py ts.json audit/f
import sys, json, asyncio
from playwright.async_api import async_playwright
ts=json.load(open(sys.argv[1])); outp=sys.argv[2]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1920})
        msgs=[]; pg.on('pageerror',lambda e: msgs.append(str(e)))
        await pg.goto('file://'+__import__('os').path.abspath('scene_built.html')); await pg.wait_for_timeout(600)
        for t in ts:
            await pg.evaluate(f'renderAt2({t})'); await pg.screenshot(path=f'{outp}_{t:05.1f}.jpg',type='jpeg',quality=80)
        print('errors:',msgs[:3])
        await b.close()
asyncio.run(main())
