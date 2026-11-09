"""Cover 1080x1920: Momo scheming frame + 'DOST KE iPHONE SE ₹20,000 KAMAYE'."""
import asyncio, os
from playwright.async_api import async_playwright
D = os.path.dirname(os.path.abspath(__file__)); F = f'file://{D}/../../engine/fonts'
H = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:P;font-weight:800;src:url({F}/poppins-latin-800-normal.woff2)}}@font-face{{font-family:A;src:url({F}/anton-latin-400-normal.woff2)}}
body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:#000}}
img{{position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover;transform:scale(1.12);transform-origin:60% 62%}}
.sh{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.75) 0%,rgba(0,0,0,.2) 38%,rgba(0,0,0,0) 60%)}}
.t{{position:absolute;left:40px;right:40px;top:270px;text-align:center;font:800 104px/1.05 P;color:#fff;text-shadow:0 7px 0 #000}}
.m{{display:inline-block;margin-top:18px;font:400 190px/1 A;color:#111;background:#3ee07a;padding:10px 40px 4px;border-radius:30px;box-shadow:0 14px 0 rgba(0,0,0,.5)}}
</style></head><body><img src="{D}/build/frames/f_0300.jpg"><div class="sh"></div>
<div class="t">DOST KE iPHONE SE<br><span class="m">₹20,000</span><br>KAMAYE!</div></body></html>"""
async def main():
    open(f'{D}/build/cover.html','w').write(H)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width':1080,'height':1920})
        await pg.goto(f'file://{D}/build/cover.html'); await pg.wait_for_timeout(1500)
        await pg.screenshot(path=f'{D}/Cover_Short_Selling.jpg', type='jpeg', quality=92); await b.close()
asyncio.run(main())
