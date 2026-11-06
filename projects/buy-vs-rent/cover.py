"""Cover: split Bunty (bought a flat) vs Momo (rent + SIP), headline + both 20-year numbers. Everything inside the safe area."""
import os, asyncio
from PIL import Image
from playwright.async_api import async_playwright
D = os.path.dirname(os.path.abspath(__file__)); B = f'{D}/build'; FONTS = 'file://' + os.path.abspath(f'{D}/../../engine/fonts')
HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:P;font-weight:800;src:url({FONTS}/poppins-latin-800-normal.woff2)}}
body{{margin:0;width:1080px;height:1920px;overflow:hidden;font-family:P;background:#0b0e18;color:#fff}}
.t{{text-shadow:5px 5px 0 #0b0e18,-5px -5px 0 #0b0e18,5px -5px 0 #0b0e18,-5px 5px 0 #0b0e18}}
.chip{{position:absolute;font-weight:800;border-radius:22px;padding:10px 30px;white-space:nowrap;box-shadow:0 10px 30px rgba(0,0,0,.45)}}
</style></head><body>
<div style="position:absolute;left:0;top:0;width:1080px;height:960px;overflow:hidden;background:#2a1a10">
 <img src="file://{D}/ai/bvr_1_bunty_keys.png" style="position:absolute;left:0px;top:140px;width:1460px;height:973px;object-fit:cover;object-position:20% 0"></div>
<div style="position:absolute;left:0;top:960px;width:1080px;height:960px;background:linear-gradient(180deg,#0f4c4a,#0b2f3a)">
 <img src="file://{D}/ai/momo_wave_cutout.png" style="position:absolute;left:90px;top:40px;height:820px"></div>
<div style="position:absolute;left:0;top:930px;width:1080px;height:60px;background:#0b0e18;border-top:6px solid #E8742A;border-bottom:6px solid #13a98a"></div>
<div class="t" style="position:absolute;left:50px;top:300px;font-weight:800;font-size:120px;line-height:1">GHAR<br>LO?</div>
<div class="t" style="position:absolute;left:0;right:0;top:1000px;text-align:center;font-weight:800;font-size:110px;line-height:1;color:#4FF0C8">YA RENT?</div>
<div class="chip" style="left:50px;top:640px;background:#E8742A;font-size:84px">₹3 Cr 🏠</div>
<div class="chip" style="left:560px;top:1250px;background:#13a98a;font-size:84px">₹5 Cr 📈</div>
<div class="chip" style="left:600px;top:1380px;background:#FFE14D;color:#1a1a1a;font-size:40px">20 SAAL KA HISAAB</div>
</body></html>"""
async def main():
    open(f'{B}/cover.html', 'w').write(HTML)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        await pg.goto('file://' + f'{B}/cover.html'); await pg.wait_for_timeout(900)
        await pg.screenshot(path=f'{B}/cover.png'); await b.close()
asyncio.run(main())
Image.open(f'{B}/cover.png').convert('RGB').save(f'{D}/Cover_Buy_vs_Rent.jpg', quality=92); print('ok')
