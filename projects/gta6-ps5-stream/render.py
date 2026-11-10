"""Render reel_built.html -> build/video_only.mp4 (1080x1920, 30 fps; rendered at 1.25x then lanczos downscale)."""
import asyncio, json, os, subprocess
from playwright.async_api import async_playwright
D = os.path.dirname(os.path.abspath(__file__))
FPS = 30
END = 47.0
N = int(END * FPS)

async def main():
    os.makedirs(f'{D}/build', exist_ok=True)
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                           '-vf', 'scale=1080:1920:flags=lanczos', '-c:v', 'libx264', '-preset', 'slow', '-crf', '15',
                           '-pix_fmt', 'yuv420p', f'{D}/build/video_only.mp4'], stdin=subprocess.PIPE)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1080, 'height': 1920}, device_scale_factor=1.25)
        await pg.goto('file://' + f'{D}/reel.html'); await pg.wait_for_timeout(5000)
        for f in range(N):
            await pg.evaluate(f"renderAt({f / FPS})")
            ff.stdin.write(await pg.screenshot(type='jpeg', quality=95))
            if f % 150 == 0: print(f, '/', N, flush=True)
        await b.close()
    ff.stdin.close(); ff.wait(); print('done', N)

asyncio.run(main())
