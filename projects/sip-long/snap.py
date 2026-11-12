import asyncio, sys, os
from playwright.async_api import async_playwright
from PIL import Image
D=os.path.dirname(os.path.abspath(__file__)); TS=[float(x) for x in sys.argv[2:]]; out=sys.argv[1]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1920,'height':1080})
        msgs=[]; pg.on('console',lambda m:msgs.append(m.text)); pg.on('pageerror',lambda e:msgs.append('ERR '+str(e)))
        await pg.goto(f'file://{D}/reel.html'); await pg.evaluate('window.READY')
        ims=[]
        for i,t in enumerate(TS):
            await pg.evaluate(f'renderAt({t})'); f=f'/tmp/claude-0/ss/q{i}.jpg'; await pg.screenshot(path=f,type='jpeg',quality=80); ims.append(Image.open(f).resize((480,270)))
        await b.close(); print('\n'.join(msgs[:10]))
    cols=4; rows=(len(ims)+cols-1)//cols; S=Image.new('RGB',(480*cols,270*rows))
    for i,im in enumerate(ims): S.paste(im,((i%cols)*480,(i//cols)*270))
    S.save(out,quality=82)
asyncio.run(main())
