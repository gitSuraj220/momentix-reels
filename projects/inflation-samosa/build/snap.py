import sys,json,asyncio
from playwright.async_api import async_playwright
html=open('reel.html').read().replace('__CUES__',open('cues.json').read())
open('built.html','w').write(html)
ts=[float(x) for x in sys.argv[1:]]
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':1080,'height':1920})
    await pg.goto('file://'+__import__('os').path.abspath('built.html'));await pg.wait_for_timeout(1200)
    for t in ts:
      await pg.evaluate(f'renderAt({t})');await pg.wait_for_timeout(250)
      await pg.screenshot(path=f'snap_{t:05.2f}.jpg',type='jpeg',quality=80)
    await b.close()
asyncio.run(main())
