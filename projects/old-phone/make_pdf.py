"""guide.html -> final/Old_Phone_Desk_Panel_Guide.pdf"""
import asyncio, os, http.server, threading, functools
from playwright.async_api import async_playwright
D = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(D); PORT = 8797
h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT); h.log_message = lambda *a: None
s = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), h); threading.Thread(target=s.serve_forever, daemon=True).start()
async def main():
    os.makedirs(f'{D}/final', exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.goto(f'http://127.0.0.1:{PORT}/old-phone/guide.html'); await pg.evaluate('document.fonts.ready')
        await pg.pdf(path=f'{D}/final/Old_Phone_Desk_Panel_Guide.pdf', format='A4', print_background=True, prefer_css_page_size=True)
        await b.close()
asyncio.run(main())
