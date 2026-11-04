"""Cover: ₹45,000 burst frame (captions hidden) + big headline."""
import os, asyncio
from PIL import Image
from playwright.async_api import async_playwright
D = os.path.dirname(os.path.abspath(__file__))
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        await pg.goto('file://' + f'{D}/reel_built.html'); await pg.wait_for_timeout(600)
        await pg.evaluate('renderAt(33.9)')
        await pg.evaluate("""()=>{const s=document.getElementById('s');for(const g of [...s.querySelectorAll('g')]){if(g.querySelector('rect[fill="rgba(25,25,30,.82)"]')&&g.parentNode===s)g.remove()}
          s.insertAdjacentHTML('beforeend',`<g transform="translate(540,1480) rotate(-2)"><rect x="-470" y="-150" width="940" height="270" rx="30" fill="#1b1b1f"/><text x="0" y="-40" font-size="88" font-weight="700" fill="#fff" text-anchor="middle" font-family="P">HOW BANKS</text><text x="0" y="70" font-size="96" font-weight="700" fill="#FFD84D" text-anchor="middle" font-family="P">MAKE MONEY 🏦</text></g>`)}""")
        await pg.wait_for_timeout(200)
        await pg.screenshot(path=f'{D}/build/cover.png'); await b.close()
asyncio.run(main())
Image.open(f'{D}/build/cover.png').convert('RGB').save(f'{D}/Cover_How_Banks_Make_Money.jpg', quality=92); print('cover ok')
