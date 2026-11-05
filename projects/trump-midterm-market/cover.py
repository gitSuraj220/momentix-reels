"""Cover: ChatGPT still (Trump dazed on the lawn + sweating bull) + bold headline in the sky."""
import os, asyncio
from PIL import Image
from playwright.async_api import async_playwright
D = os.path.dirname(os.path.abspath(__file__))
FONTS = 'file://' + os.path.abspath(f'{D}/../../engine/fonts')
HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:P;font-weight:800;src:url({FONTS}/poppins-latin-800-normal.woff2)}}
body{{margin:0;width:1080px;height:1920px;overflow:hidden;font-family:P}}
img{{position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover}}
.t{{position:absolute;left:0;right:0;text-align:center;font-weight:800;color:#fff;
 text-shadow:0 8px 0 #000,6px 6px 0 #000,-6px -6px 0 #000,6px -6px 0 #000,-6px 6px 0 #000}}
.tag{{position:absolute;left:50%;top:170px;transform:translateX(-50%) rotate(-2deg);background:#c8102e;color:#fff;font-weight:800;
 font-size:48px;padding:10px 30px;border-radius:12px;border:4px solid #fff;letter-spacing:3px;white-space:nowrap}}
</style></head><body><img src="file://{D}/ai/tr_6_cover.png">
<div class="tag">BREAKING · SATIRE</div>
<div class="t" style="top:290px;font-size:122px;white-space:nowrap;line-height:1">TRUMP <span style="color:#FF4D6D">HAARE?</span></div>
<div class="t" style="top:440px;font-size:112px;white-space:nowrap;line-height:1"><span style="color:#4ADE80">BULL RUN?</span> 📈</div>
</body></html>"""
async def main():
    open(f'{D}/build/cover.html', 'w').write(HTML)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        await pg.goto('file://' + f'{D}/build/cover.html'); await pg.wait_for_timeout(800)
        await pg.screenshot(path=f'{D}/build/cover.png'); await b.close()
asyncio.run(main())
Image.open(f'{D}/build/cover.png').convert('RGB').save(f'{D}/Cover_Trump_Sensex.jpg', quality=92); print('cover ok')
