"""Cover: hook frame (G + orbiting tools + Momo) with captions hidden and a big bottom headline."""
import os, asyncio
from PIL import Image
from playwright.async_api import async_playwright
D = os.path.dirname(os.path.abspath(__file__))
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        await pg.goto('file://' + f'{D}/reel_built.html'); await pg.wait_for_timeout(800)
        await pg.evaluate('renderAt(6.4)')
        await pg.evaluate("""()=>{for(const e of document.querySelectorAll('*')){const s=getComputedStyle(e);if(e.textContent.trim()==='hain!'&&e.children.length===0){let n=e;while(n&&n.parentElement&&n.parentElement.id!=='stage')n=n.parentElement;n.style.display='none'}}
          const d=document.createElement('div');d.style.cssText='position:absolute;left:0;right:0;top:1360px;text-align:center;z-index:99;font-family:Poppins;font-weight:800';
          d.innerHTML='<div style="display:inline-block;background:#111;color:#fff;font-size:92px;line-height:1.05;padding:26px 44px;border-radius:28px;transform:rotate(-2deg);box-shadow:0 20px 40px rgba(0,0,0,.25)">GOOGLE ke<br><span style=\\'color:#3DDC84\\'>FREE</span> AI TOOLS 🤯</div>';
          document.body.appendChild(d)}""")
        await pg.wait_for_timeout(300)
        await pg.screenshot(path=f'{D}/build/cover.png'); await b.close()
asyncio.run(main())
Image.open(f'{D}/build/cover.png').convert('RGB').save(f'{D}/Cover_Google_Free_AI_Tools.jpg', quality=92); print('cover ok')
