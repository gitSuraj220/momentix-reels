"""Cover 1080x1920: money-bag frame from our hook clip + '₹4 CRORE?' + Instagram vs YouTube icons (identification)."""
import os, asyncio
from PIL import Image
from playwright.async_api import async_playwright
D = os.path.dirname(os.path.abspath(__file__)); F = 'file://' + os.path.abspath(f'{D}/../../engine/fonts')
HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:P;font-weight:800;src:url({F}/poppins-latin-800-normal.woff2)}}
@font-face{{font-family:A;src:url({F}/anton-latin-400-normal.woff2)}}
body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:#000;font-family:P}}
.bg{{position:absolute;inset:0;background:url(file://{D}/build/frames/f_0110.jpg) center/cover}}
.sh{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.85) 0%,rgba(0,0,0,.2) 38%,rgba(0,0,0,.25) 62%,rgba(0,0,0,.9) 100%)}}
</style></head><body><div class="bg"></div><div class="sh"></div>
<svg width="0" height="0" style="position:absolute"><defs>
<radialGradient id="g" cx="30%" cy="107%" r="150%"><stop offset="0" stop-color="#fdf497"/><stop offset=".05" stop-color="#fdf497"/><stop offset=".45" stop-color="#fd5949"/><stop offset=".6" stop-color="#d6249f"/><stop offset=".9" stop-color="#285AEB"/></radialGradient></defs></svg>
<div style="position:absolute;left:0;right:0;top:250px;text-align:center;font:800 70px P;color:#fff;text-shadow:0 5px 0 #000">INSTAGRAM DE RAHA HAI</div>
<div style="position:absolute;left:0;right:0;top:340px;text-align:center;font:400 270px/1 A;color:#ffd400;text-shadow:0 0 50px rgba(255,212,0,.5),0 10px 0 #000">₹4 CRORE?</div>
<svg style="position:absolute;left:110px;top:1180px" width="250" height="250" viewBox="0 0 100 100"><rect width="100" height="100" rx="24" fill="url(#g)"/><rect x="22" y="22" width="56" height="56" rx="17" fill="none" stroke="#fff" stroke-width="7"/><circle cx="50" cy="50" r="13.5" fill="none" stroke="#fff" stroke-width="7"/><circle cx="68" cy="32" r="4.5" fill="#fff"/></svg>
<div style="position:absolute;left:440px;top:1230px;font:400 150px A;color:#fff;text-shadow:0 0 30px #ff4fa3,0 8px 0 #000">VS</div>
<svg style="position:absolute;left:640px;top:1205px" width="320" height="230" viewBox="0 0 140 100"><rect y="6" width="140" height="88" rx="26" fill="#ff0000"/><path d="M56 30 L94 50 L56 70Z" fill="#fff"/></svg>
<div style="position:absolute;left:0;right:0;top:1480px;text-align:center"><span style="font:800 54px P;background:#e0182b;color:#fff;padding:10px 30px;border-radius:14px">YOUTUBERS KE LIYE DEAL</span></div>
</body></html>"""
async def main():
    os.makedirs(f'{D}/build', exist_ok=True); open(f'{D}/build/cover.html', 'w').write(HTML)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        await pg.goto(f'file://{D}/build/cover.html'); await pg.wait_for_timeout(900); await pg.screenshot(path=f'{D}/build/cover.png'); await b.close()
asyncio.run(main())
Image.open(f'{D}/build/cover.png').convert('RGB').save(f'{D}/Cover_Instagram_4_Crore.jpg', quality=92); print('cover ok')
