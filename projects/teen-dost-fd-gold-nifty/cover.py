"""Cover 1080x1920 (Reel cover = Shorts thumbnail): picks art + 2-line giant headline (white + yellow, thick stroke). No faces covered."""
import os, asyncio
from PIL import Image
from playwright.async_api import async_playwright
D = os.path.dirname(os.path.abspath(__file__))
a = f'{D}/ai/art_02_picks.png'; w, h = Image.open(a).size
html = f"""<html><head><style>
@font-face{{font-family:P;src:url('file:///usr/share/fonts/truetype/google-fonts/Poppins-Black.ttf');font-weight:900}}
@font-face{{font-family:P;src:url('file:///usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf');font-weight:700}}
html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:#F3EEE4}}
.art{{position:absolute;left:-60px;top:560px;width:1200px;height:1360px;background:url('file://{a}') center 78%/auto 1560px no-repeat;mix-blend-mode:multiply;-webkit-mask-image:linear-gradient(to bottom,transparent 0,#000 120px)}}
.h{{position:absolute;left:0;right:0;text-align:center;font-family:P;font-weight:700;letter-spacing:-3px;line-height:1;
   paint-order:stroke fill;-webkit-text-stroke:16px #14110e}}
.tag{{position:absolute;left:50%;transform:translateX(-50%) rotate(-2deg);top:120px;white-space:nowrap;background:#F29A2E;color:#1d140a;font:700 40px P;padding:8px 26px;border-radius:10px}}
</style></head><body>
<div class="art"></div>
<div class="tag">₹1 LAKH · 2007 → 2026</div>
<div class="h" style="top:230px;font-size:140px;color:#fff">FD vs GOLD</div>
<div class="h" style="top:385px;font-size:140px;color:#FFD23F">vs NIFTY?</div>
</body></html>"""
open(f'{D}/build/cover.html', 'w').write(html)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        await pg.goto('file://' + f'{D}/build/cover.html'); await pg.wait_for_timeout(600)
        await pg.screenshot(path=f'{D}/Cover_Teen_Dost.png'); await b.close()
asyncio.run(main())
Image.open(f'{D}/Cover_Teen_Dost.png').convert('RGB').save(f'{D}/Cover_Teen_Dost.jpg', quality=92)
print('cover ok')
