"""cover.html -> final/Cover_Anthropic_IPO.jpg (1080x1920)."""
import asyncio, os
from playwright.async_api import async_playwright
D = os.path.dirname(os.path.abspath(__file__))
async def main():
    os.makedirs(f'{D}/final', exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get('PW_EXE') or None); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        await pg.goto('file://' + f'{D}/cover.html'); await pg.wait_for_timeout(1500)
        await pg.screenshot(path=f'{D}/final/Cover_Anthropic_IPO.jpg', type='jpeg', quality=93); await b.close()
asyncio.run(main())
