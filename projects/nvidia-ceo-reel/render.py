"""Render reel.html -> build/video_only.mp4 (1080x1920, 30 fps)."""
import asyncio, os, subprocess
from playwright.async_api import async_playwright
D = os.path.dirname(os.path.abspath(__file__)); FPS = 30; END = 49.02; N = int(END * FPS)
async def main():
    os.makedirs(f'{D}/build', exist_ok=True)
    ff = subprocess.Popen(['ffmpeg','-v','error','-y','-f','image2pipe','-framerate',str(FPS),'-c:v','mjpeg','-i','-',
        '-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p',f'{D}/build/video_only.mp4'], stdin=subprocess.PIPE)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width':1080,'height':1920})
        await pg.goto(f'file://{D}/reel.html'); await pg.evaluate('window.READY')
        for f in range(N):
            await pg.evaluate(f'renderAt({f/FPS})'); ff.stdin.write(await pg.screenshot(type='jpeg', quality=93))
            if f % 300 == 0: print(f, '/', N, flush=True)
        await b.close()
    ff.stdin.close(); ff.wait(); print('done', N)
asyncio.run(main())
