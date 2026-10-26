import asyncio,sys
from playwright.async_api import async_playwright
TS=[float(x) for x in sys.argv[1:]]
async def main():
  async with async_playwright() as p:
    br=await p.chromium.launch();pg=await br.new_page(viewport={'width':1080,'height':1920})
    pg.on('pageerror',lambda e:print('ERR',e))
    await pg.goto('file:///home/claude/roll/reel.html');await pg.wait_for_timeout(1200)
    for t in TS:
      await pg.evaluate(f'renderAt({t})');await pg.screenshot(path=f'p_{t:05.2f}.png')
    await br.close()
asyncio.run(main())
