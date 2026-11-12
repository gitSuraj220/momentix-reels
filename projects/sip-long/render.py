"""Render reel.html -> build/video_only.mp4 (1920x1080, 30 fps), in K parallel chunks."""
import asyncio, os, subprocess, json, sys
from playwright.async_api import async_playwright
D = os.path.dirname(os.path.abspath(__file__)); FPS = 30
END = json.load(open(f'{D}/timeline.json'))['END']; N = int(END * FPS); K = int(sys.argv[1]) if len(sys.argv) > 1 else 4
async def chunk(p, k):
    a, b = N * k // K, N * (k + 1) // K
    ff = subprocess.Popen(['ffmpeg','-v','error','-y','-f','image2pipe','-framerate',str(FPS),'-c:v','mjpeg','-i','-',
        '-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p',f'{D}/build/part{k}.mp4'], stdin=subprocess.PIPE)
    br = await p.chromium.launch(); pg = await br.new_page(viewport={'width':1920,'height':1080})
    await pg.goto(f'file://{D}/reel.html'); await pg.evaluate('window.READY')
    for f in range(a, b):
        await pg.evaluate(f'renderAt({f/FPS})'); ff.stdin.write(await pg.screenshot(type='jpeg', quality=93))
        if (f - a) % 300 == 0: print(k, f - a, '/', b - a, flush=True)
    await br.close(); ff.stdin.close(); await asyncio.get_event_loop().run_in_executor(None, ff.wait)
async def main():
    os.makedirs(f'{D}/build', exist_ok=True)
    async with async_playwright() as p:
        await asyncio.gather(*[chunk(p, k) for k in range(K)])
    open(f'{D}/build/list.txt','w').write(''.join(f"file 'part{k}.mp4'\n" for k in range(K)))
    subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',f'{D}/build/list.txt','-c','copy',f'{D}/build/video_only.mp4'], check=True)
    print('done', N, flush=True)
asyncio.run(main())
