import asyncio, os, sys
from playwright.async_api import async_playwright
D = os.path.dirname(os.path.abspath(__file__)); T = [float(x) for x in sys.argv[1:]]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width':1080,'height':1920})
        await pg.goto(f'file://{D}/reel.html'); await pg.wait_for_timeout(5000)
        for t in T:
            await pg.evaluate(f'renderAt({t})'); await pg.screenshot(path=f'/tmp/claude-0/ss/r_{t}.jpg', type='jpeg', quality=70)
        await b.close()
asyncio.run(main())
