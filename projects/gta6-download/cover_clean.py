"""Clean cover: one full-bleed 'internet melt' scene + GTA VI logo (identification) + one short headline."""
import os, asyncio
from PIL import Image
from playwright.async_api import async_playwright
D = os.path.dirname(os.path.abspath(__file__)); B = f'{D}/build'; FONTS = 'file://' + os.path.abspath(f'{D}/../../engine/fonts')
HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:P;font-weight:800;src:url({FONTS}/poppins-latin-800-normal.woff2)}}
body{{margin:0;width:1080px;height:1920px;overflow:hidden;font-family:P;background:#000}}
</style></head><body>
<img src="file://{B}/cov/melt_hd.jpg" style="position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover;transform:scale(1.06);transform-origin:50% 55%">
<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(7,2,26,.9) 0%,rgba(7,2,26,0) 30%,rgba(7,2,26,0) 68%,rgba(7,2,26,.92) 100%)"></div>
<img src="file://{D}/ai/logo_gta6.png" style="position:absolute;left:50%;top:110px;height:330px;transform:translateX(-50%);filter:drop-shadow(0 0 34px rgba(255,64,200,.75))">
<div style="position:absolute;left:0;right:0;top:1500px;text-align:center;font-weight:800;font-size:132px;line-height:1;color:#fff;
 text-shadow:0 0 30px #ff2d55,5px 5px 0 #000,-5px -5px 0 #000,5px -5px 0 #000,-5px 5px 0 #000">INTERNET<br><span style="color:#ff4d6d">MELT?</span> 🔥</div>
</body></html>"""
async def main():
    open(f'{B}/cover_clean.html', 'w').write(HTML)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        await pg.goto('file://' + f'{B}/cover_clean.html'); await pg.wait_for_timeout(900)
        await pg.screenshot(path=f'{B}/cover_clean.png'); await b.close()
asyncio.run(main())
Image.open(f'{B}/cover_clean.png').convert('RGB').save(f'{D}/Cover_GTA6_Clean.jpg', quality=93); print('ok')
