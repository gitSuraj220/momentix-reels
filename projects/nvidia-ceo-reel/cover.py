import asyncio, os
from playwright.async_api import async_playwright
D=os.path.dirname(os.path.abspath(__file__))
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1920})
        await pg.goto(f'file://{D}/reel.html'); await pg.evaluate('window.READY'); await pg.evaluate('renderCover()')
        await pg.screenshot(path=f'{D}/final/Cover_Nvidia_CEO.jpg',type='jpeg',quality=92); await b.close()
asyncio.run(main())
