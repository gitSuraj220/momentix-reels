import subprocess,asyncio,json,os
from playwright.async_api import async_playwright
C=json.load(open('cues.json')); END=C[-1]['e']+1.1
async def main():
  async with async_playwright() as p:
    br=await p.chromium.launch();pg=await br.new_page(viewport={'width':1080,'height':1920})
    await pg.goto('file://'+os.path.abspath('built.html'));await pg.wait_for_timeout(1500)
    ff=subprocess.Popen(['ffmpeg','-y','-v','error','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-','-c:v','libx264','-preset','slow','-crf','14','-pix_fmt','yuv420p',__import__('os').environ.get('OUT','v.mp4')],stdin=subprocess.PIPE)
    n=int(__import__("os").environ.get("NFR",int(END*30)))
    for f in range(n):
      await pg.evaluate(f'renderAt({f/30})')
      await pg.evaluate('Promise.all([...document.images].filter(i=>!i.complete).map(i=>new Promise(r=>{i.onload=i.onerror=r})))')
      ff.stdin.write(await pg.screenshot(type='jpeg',quality=95))
      if f%150==0: print(f,n,flush=True)
    ff.stdin.close();ff.wait();await br.close()
asyncio.run(main())
