import asyncio, sys, os
from playwright.async_api import async_playwright
from PIL import Image
D=os.path.dirname(os.path.abspath(__file__)); TS=[float(x) for x in sys.argv[2:]]; out=sys.argv[1]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1920})
        msgs=[]; pg.on('console',lambda m:msgs.append(m.text)); pg.on('pageerror',lambda e:msgs.append('ERR '+str(e)))
        await pg.goto(f'file://{D}/reel.html'); await pg.evaluate('window.READY')
        ims=[]
        for i,t in enumerate(TS):
            await pg.evaluate(f'renderAt({t})'); f=f'/tmp/claude-0/ss/s{i}.jpg'; await pg.screenshot(path=f,type='jpeg',quality=80); ims.append(Image.open(f).resize((270,480)))
        await b.close(); print('\n'.join(msgs[:10]))
    cols=6; rows=(len(ims)+cols-1)//cols; S=Image.new('RGB',(270*cols,480*rows))
    for i,im in enumerate(ims): S.paste(im,((i%cols)*270,(i//cols)*480))
    S.save(out,quality=80)
asyncio.run(main())
