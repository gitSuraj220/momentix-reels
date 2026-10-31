import asyncio,os,sys,json
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw
ts=[float(x) for x in sys.argv[2:]]; out=sys.argv[1]
async def main():
  async with async_playwright() as p:
    br=await p.chromium.launch();pg=await br.new_page(viewport={'width':1080,'height':1920})
    await pg.goto('file://'+os.path.abspath('built.html'));await pg.wait_for_timeout(1200)
    ims=[]
    for t in ts:
      await pg.evaluate(f'renderAt({t})')
      await pg.evaluate('Promise.all([...document.images].filter(i=>!i.complete).map(i=>new Promise(r=>{i.onload=i.onerror=r})))')
      await pg.screenshot(path='/tmp/_s.png'); im=Image.open('/tmp/_s.png').convert('RGB').resize((360,640)); ImageDraw.Draw(im).text((8,8),f'{t:.1f}',fill=(255,0,0)); ims.append(im)
    cols=min(6,len(ims)); rows=(len(ims)+cols-1)//cols
    sh=Image.new('RGB',(360*cols,640*rows),'white')
    for i,im in enumerate(ims): sh.paste(im,((i%cols)*360,(i//cols)*640))
    sh.save(out,quality=82); await br.close()
asyncio.run(main())
