"""python3 render.py snap 1 5 ... -> build/snap_*.jpg
   python3 render.py [workers=4] -> build/video_only.mp4 (parallel segments, then concat)"""
import asyncio, os, subprocess, sys, http.server, threading, functools, json
from playwright.async_api import async_playwright
D = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(D)
T = json.load(open(f'{D}/timeline.json')); FPS = 30; END = T['end']; N = int(END * FPS); PORT = int(os.environ.get('PORT', 8801))
def serve():
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT); h.log_message = lambda *a: None
    s = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), h); threading.Thread(target=s.serve_forever, daemon=True).start()
WAIT = 'Promise.all([...document.images].filter(i=>!i.complete).map(i=>new Promise(r=>{i.onload=i.onerror=r})))'
async def page(b):
    pg = await b.new_page(viewport={'width': 1920, 'height': 1080})
    pg.on('pageerror', lambda e: print('PAGEERROR', e, flush=True))
    await pg.add_init_script(f'window.__T__={json.dumps(T)}')
    await pg.goto(f'http://127.0.0.1:{PORT}/rupee-dollar/reel.html'); await pg.evaluate('window.READY'); return pg
async def seg(b, k, a, z):
    pg = await page(b)
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                           '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', f'{D}/build/seg{k}.mp4'], stdin=subprocess.PIPE)
    for f in range(a, z):
        await pg.evaluate(f'renderAt({f / FPS})'); await pg.evaluate(WAIT); ff.stdin.write(await pg.screenshot(type='jpeg', quality=93))
        if (f - a) % 300 == 0: print(f'w{k}', f - a, '/', z - a, flush=True)
    ff.stdin.close(); await asyncio.get_event_loop().run_in_executor(None, ff.wait)
async def main():
    os.makedirs(f'{D}/build', exist_ok=True); serve()
    async with async_playwright() as p:
        b = await p.chromium.launch()
        if sys.argv[1:2] == ['snap']:
            pg = await page(b)
            for ts in sys.argv[2:]:
                await pg.evaluate(f'renderAt({float(ts)})'); await pg.evaluate(WAIT)
                await pg.screenshot(path=f'{D}/build/snap_{float(ts):06.2f}.jpg', type='jpeg', quality=80)
            await b.close(); return
        W = int(sys.argv[1]) if len(sys.argv) > 1 else 4; cut = [round(N * i / W) for i in range(W + 1)]
        await asyncio.gather(*[seg(b, k, cut[k], cut[k + 1]) for k in range(W)]); await b.close()
    open(f'{D}/build/segs.txt', 'w').write(''.join(f"file 'seg{k}.mp4'\n" for k in range(W)))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{D}/build/segs.txt', '-c', 'copy', f'{D}/build/video_only.mp4'], check=True)
    print('done', N, 'frames')
asyncio.run(main())
