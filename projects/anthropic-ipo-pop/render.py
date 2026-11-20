"""python3 render.py snap 1 5 ... -> build/snap_*.jpg ; python3 render.py -> build/video_only.mp4"""
import asyncio, os, subprocess, sys, http.server, threading, functools
from playwright.async_api import async_playwright
D = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(D)
FPS = 30; END = 29.76; N = int(END * FPS); PORT = int(os.environ.get('PORT', 8795))
def serve():
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT); h.log_message = lambda *a: None
    s = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), h); threading.Thread(target=s.serve_forever, daemon=True).start()
async def main():
    os.makedirs(f'{D}/build', exist_ok=True); serve(); snap = sys.argv[1:2] == ['snap']
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        await pg.goto(f'http://127.0.0.1:{PORT}/anthropic-ipo-pop/reel.html'); await pg.evaluate('window.READY')
        wait = 'Promise.all([...document.images].filter(i=>!i.complete).map(i=>new Promise(r=>{i.onload=i.onerror=r})))'
        if snap:
            for ts in sys.argv[2:]:
                await pg.evaluate(f'renderAt({float(ts)})'); await pg.evaluate(wait)
                await pg.screenshot(path=f'{D}/build/snap_{float(ts):05.2f}.jpg', type='jpeg', quality=80)
            await b.close(); return
        ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                               '-c:v', 'libx264', '-preset', 'medium', '-crf', '15', '-pix_fmt', 'yuv420p', f'{D}/build/video_only.mp4'], stdin=subprocess.PIPE)
        for f in range(N):
            await pg.evaluate(f'renderAt({f / FPS})'); await pg.evaluate(wait); ff.stdin.write(await pg.screenshot(type='jpeg', quality=93))
            if f % 150 == 0: print(f, '/', N, flush=True)
        await b.close(); ff.stdin.close(); ff.wait(); print('done')
asyncio.run(main())
