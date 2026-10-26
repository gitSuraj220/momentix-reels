import subprocess,asyncio,json
from playwright.async_api import async_playwright
END=json.load(open('timeline.json'))['end']
async def main():
  async with async_playwright() as p:
    br=await p.chromium.launch();pg=await br.new_page(viewport={'width':1080,'height':1920},device_scale_factor=1.25)
    await pg.goto('file:///home/claude/mdop/built.html');await pg.wait_for_timeout(2000)
    ff=subprocess.Popen(['ffmpeg','-y','-v','error','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-','-vf','scale=1080:1920:flags=lanczos','-c:v','libx264','-preset','slow','-crf','15','-pix_fmt','yuv420p','v.mp4'],stdin=subprocess.PIPE)
    n=int(END*30)
    for f in range(n):
      await pg.evaluate(f'renderAt({f/30})');ff.stdin.write(await pg.screenshot(type='jpeg',quality=95))
      if f%150==0: print(f,n,flush=True)
    ff.stdin.close();ff.wait();await br.close()
asyncio.run(main())
