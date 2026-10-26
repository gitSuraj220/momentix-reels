# usage (in video dir): nohup python render.py > render.log 2>&1 &   -> video_only.mp4 (~0.13 s/frame)
import asyncio, json, subprocess, sys
from playwright.async_api import async_playwright
FPS=30
END=json.load(open('timeline.json'))['end']
N=int(END*FPS)
async def main():
    ff=subprocess.Popen(['ffmpeg','-v','error','-y','-f','image2pipe','-framerate',str(FPS),'-c:v','mjpeg','-i','-',
        '-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','video_only.mp4'],stdin=subprocess.PIPE)
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1080,'height':1920})
        await pg.goto('file://'+__import__('os').path.abspath('scene_built.html')); await pg.wait_for_timeout(800)
        for f in range(N):
            await pg.evaluate(f'renderAt2({f/FPS})')
            ff.stdin.write(await pg.screenshot(type='jpeg',quality=93))
            if f%300==0: print(f,'/',N,flush=True)
        await b.close()
    ff.stdin.close(); ff.wait()
asyncio.run(main())
