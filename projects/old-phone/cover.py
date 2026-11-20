"""Cover: reel frame at the dashboard moment + big title -> final/cover.jpg"""
import asyncio, os, http.server, threading, functools
from playwright.async_api import async_playwright
D = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(D); PORT = 8798
h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT); h.log_message = lambda *a: None
s = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), h); threading.Thread(target=s.serve_forever, daemon=True).start()
JS = """() => { renderAt(10.05);
 for (const id of ['hC','stC','hnd']) { const e=document.getElementById(id); if(e) e.style.display='none'; }
 document.getElementById('flash').style.opacity=0;
 const d=document.createElement('div'); d.innerHTML=`
 <div style="position:absolute;left:70px;top:230px;font-weight:800;font-size:132px;line-height:.98;letter-spacing:-3px">Purana phone<br><span style="color:#FF4D5A">mat feko</span> 🛑</div>
 <div style="position:absolute;left:70px;top:540px;font-family:Ka;font-weight:700;font-size:78px;color:#2DE2E6;text-shadow:0 0 30px rgba(45,226,230,.5)">desk panel bana do ⚡</div>
 <img src="art/logos/android.png" style="position:absolute;left:830px;top:600px;width:150px;transform:rotate(10deg)">
 <div style="position:absolute;left:70px;top:1470px;display:flex;gap:22px;align-items:center">
   <img src="art/logos/claudesym.png" style="width:90px"><div style="font-weight:800;font-size:64px">+ Claude = <span style="color:#2BE37A">free setup</span></div></div>`;
 document.getElementById('st').appendChild(d); return true }"""
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        await pg.goto(f'http://127.0.0.1:{PORT}/old-phone/reel.html'); await pg.evaluate('window.READY'); await pg.evaluate(JS)
        await pg.wait_for_timeout(400); await pg.screenshot(path=f'{D}/final/cover.jpg', type='jpeg', quality=92); await b.close()
asyncio.run(main())
