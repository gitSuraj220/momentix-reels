import asyncio, sys
from playwright.async_api import async_playwright
from PIL import Image
T=[float(x) for x in sys.argv[1].split(',')]; out=sys.argv[2]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,"height":1920})
        msgs=[]; pg.on('pageerror',lambda e:msgs.append(str(e)))
        await pg.goto('file:///home/claude/momentix-reels/projects/instagram-features-500k/reel.html'); await pg.wait_for_timeout(1200)
        ims=[]
        for t in T:
            await pg.evaluate(f'renderAt({t})'); await pg.screenshot(path='/tmp/claude-0/s.png'); ims.append(Image.open('/tmp/claude-0/s.png').convert('RGB').resize((360,640)))
        await b.close(); print(msgs[:3])
    cols=3; rows=(len(ims)+cols-1)//cols; W=Image.new('RGB',(360*cols,640*rows),'black')
    for i,im in enumerate(ims): W.paste(im,((i%cols)*360,(i//cols)*640))
    W.save(out,quality=85)
asyncio.run(main())
