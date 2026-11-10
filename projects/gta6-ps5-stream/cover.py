"""Cover 1080x1920: Momo with bat, cracked screen, LIVE badge, 'GTA 6 LIVE KARO — SIRF PS5 SE'."""
import asyncio, os
from playwright.async_api import async_playwright
D = os.path.dirname(os.path.abspath(__file__)); F = f'file://{D}/../../engine/fonts'
H = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:P;font-weight:800;src:url({F}/poppins-latin-800-normal.woff2)}}@font-face{{font-family:A;src:url({F}/anton-latin-400-normal.woff2)}}
body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:#000}}
img{{position:absolute;left:0;top:0;width:1080px;height:1930px;object-fit:cover}}
.sh{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.8) 0%,rgba(0,0,0,.25) 34%,rgba(0,0,0,0) 55%)}}
.t1{{position:absolute;left:0;right:0;top:250px;text-align:center;font:400 230px/0.95 A;color:#fff;text-shadow:0 10px 0 #000,0 0 50px rgba(255,79,216,.7)}}
.t1 b{{color:#ff4fd8;font-weight:400}}
.t2{{position:absolute;left:0;right:0;top:500px;text-align:center}}.t2 span{{display:inline-block;font:800 64px P;color:#0b0b14;background:#00e5ff;padding:8px 34px;border-radius:20px;box-shadow:0 12px 0 rgba(0,0,0,.5)}}
.live{{position:absolute;left:70px;top:120px;font:800 54px P;color:#fff;background:#ff1f3d;padding:6px 26px;border-radius:14px;box-shadow:0 0 40px rgba(255,31,61,.8)}}
</style></head><body><img src="{D}/art/gta_kf3.png"><div class="sh"></div><div class="live">● LIVE</div>
<div class="t1">GTA 6 <b>LIVE</b></div><div class="t2"><span>SIRF PS5 SE · 4 STEPS</span></div></body></html>"""
async def main():
    os.makedirs(f'{D}/build', exist_ok=True); open(f'{D}/build/cover.html','w').write(H)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width':1080,'height':1920})
        await pg.goto(f'file://{D}/build/cover.html'); await pg.wait_for_timeout(1500)
        await pg.screenshot(path=f'{D}/Cover_GTA6_Live.jpg', type='jpeg', quality=92); await b.close()
asyncio.run(main())
