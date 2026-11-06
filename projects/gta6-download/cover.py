"""Cover poster: GTA-style comic-panel grid made from OUR OWN reel art (no game art), with the GTA VI logo
(identification only) + short headline. Output: Cover_GTA6_Download.jpg (1080x1920)."""
import os, asyncio
from PIL import Image
from playwright.async_api import async_playwright
D = os.path.dirname(os.path.abspath(__file__)); B = f'{D}/build'; FONTS = 'file://' + os.path.abspath(f'{D}/../../engine/fonts')
# panel crops from our own frames
Image.open(f'{B}/snap_04.90.jpg').crop((0, 520, 1080, 1560)).save(f'{B}/cov/stuck.jpg', quality=92)
Image.open(f'{B}/snap_16.35.jpg').crop((330, 560, 1080, 1230)).save(f'{B}/cov/days.jpg', quality=92)
Image.open(f'{B}/snap_20.30.jpg').crop((60, 560, 1020, 1360)).save(f'{B}/cov/load.jpg', quality=92)
def P(x, y, w, h, src, pos='center', extra=''):
    return f'<div class="p" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"><img src="file://{B}/cov/{src}" style="object-position:{pos}">{extra}</div>'
HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:P;font-weight:800;src:url({FONTS}/poppins-latin-800-normal.woff2)}}
body{{margin:0;width:1080px;height:1920px;background:#000;overflow:hidden;font-family:P}}
.p{{position:absolute;overflow:hidden;background:#111}} .p img{{width:100%;height:100%;object-fit:cover}}
.st{{position:absolute;font-weight:800;color:#fff;padding:6px 22px;border-radius:12px;white-space:nowrap;
 text-shadow:3px 3px 0 #000;box-shadow:0 6px 20px rgba(0,0,0,.6)}}
</style></head><body>
{P(14, 14, 650, 820, 'melt.jpg', '50% 60%', '<div class="st" style="left:24px;bottom:26px;background:#ff2d55;font-size:62px;transform:rotate(-4deg)">INTERNET MELT? 🔥</div>')}
{P(678, 14, 388, 400, 'days.jpg', '50% 50%')}
{P(678, 428, 388, 406, 'load.jpg', '50% 40%')}
{P(14, 848, 440, 640, 'stuck.jpg', '38% 50%', '<div class="st" style="left:18px;top:22px;background:#ffcc00;color:#111;text-shadow:none;font-size:48px;transform:rotate(3deg)">200 GB 😱</div>')}
{P(468, 848, 598, 640, 'cheer.jpg', '45% 45%', '<div class="st" style="right:18px;top:22px;background:#22c55e;font-size:44px;transform:rotate(-3deg)">PRELOAD 10 NOV</div>')}
<div style="position:absolute;left:0;right:0;top:1502px;height:418px;background:radial-gradient(ellipse at 50% 40%,#3b0a5c,#000 75%)"></div>
<img src="file://{D}/ai/logo_gta6.png" style="position:absolute;left:50%;top:1515px;height:300px;transform:translateX(-50%);filter:drop-shadow(0 0 30px rgba(255,64,200,.7))">
<div style="position:absolute;left:0;right:0;top:1828px;text-align:center;font-weight:800;font-size:58px;color:#fff;letter-spacing:2px;text-shadow:0 0 20px #ff40c8,3px 3px 0 #000">DOWNLOAD KAISE HOGA?</div>
</body></html>"""
async def main():
    open(f'{B}/cover.html', 'w').write(HTML)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        await pg.goto('file://' + f'{B}/cover.html'); await pg.wait_for_timeout(900)
        await pg.screenshot(path=f'{B}/cover.png'); await b.close()
asyncio.run(main())
Image.open(f'{B}/cover.png').convert('RGB').save(f'{D}/Cover_GTA6_Download.jpg', quality=92); print('cover ok')
