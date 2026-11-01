"""Cover 1080x1920 (Reel cover = Shorts thumbnail): hook frame (Papa ji stopping the pen) + giant 2-line headline in the dark desk area, faces clear."""
import os, asyncio
from PIL import Image
from playwright.async_api import async_playwright
D = os.path.dirname(os.path.abspath(__file__))
a = f'{D}/ai/s01.png'
html = f"""<html><head><style>
@font-face{{font-family:P;src:url('file:///usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf');font-weight:900}}
@font-face{{font-family:P;src:url('file:///usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf');font-weight:700}}
html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:#120c06}}
.art{{position:absolute;inset:0;background:url('file://{a}') center top/1080px 1920px no-repeat}}
.shade{{position:absolute;left:0;right:0;top:1060px;bottom:0;background:linear-gradient(to bottom,rgba(10,5,0,0),rgba(10,5,0,.75) 180px,rgba(10,5,0,.9))}}
.h{{position:absolute;left:0;right:0;text-align:center;font-family:P;font-weight:900;letter-spacing:-2px;line-height:1;
   paint-order:stroke fill;-webkit-text-stroke:14px #140b04;text-shadow:0 10px 30px rgba(0,0,0,.6)}}
.tag{{position:absolute;left:50%;transform:translateX(-50%) rotate(-2deg);top:1130px;white-space:nowrap;background:#FFC44D;color:#2b1708;font:700 42px P;padding:10px 30px;border-radius:12px;letter-spacing:1px}}
.stamp{{position:absolute;left:690px;top:250px;transform:rotate(-8deg);background:#B3261E;color:#fff;font:900 70px P;padding:12px 34px;border-radius:46px;border:6px solid #FFE3A0;box-shadow:0 12px 30px rgba(0,0,0,.5)}}
</style></head><body>
<div class="art"></div><div class="shade"></div>
<div class="stamp">RUKO!</div>
<div class="tag">DHANTERAS PE CAR LENE SE PEHLE</div>
<div class="h" style="top:1240px;font-size:112px;white-space:nowrap"><span style="color:#FF6B57">PETROL</span> <span style="color:#fff;font-size:96px">vs</span> <span style="color:#C9D1DB">DIESEL</span></div>
<div class="h" style="top:1380px;font-size:160px"><span style="color:#fff;font-size:110px">vs</span> <span style="color:#3FE0CF">EV?</span></div>
</body></html>"""
os.makedirs(f'{D}/build', exist_ok=True)
open(f'{D}/build/cover.html', 'w').write(html)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        await pg.goto('file://' + f'{D}/build/cover.html'); await pg.wait_for_timeout(600)
        await pg.screenshot(path=f'{D}/build/cover.png'); await b.close()
asyncio.run(main())
Image.open(f'{D}/build/cover.png').convert('RGB').save(f'{D}/Cover_Petrol_Diesel_EV.jpg', quality=92)
print('cover ok')
