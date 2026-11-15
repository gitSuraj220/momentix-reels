#!/usr/bin/env python3
"""16:9 thumbnails -> final/thumb_v1.jpg, thumb_v2.jpg (1280x720, < 2 MB)."""
import os, asyncio, subprocess
from playwright.async_api import async_playwright
D = os.path.dirname(os.path.abspath(__file__)); os.makedirs(f'{D}/final', exist_ok=True)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get('PW_EXE') or None, args=['--allow-file-access-from-files'])
        pg = await b.new_page(viewport={'width': 1920, 'height': 1080})
        for v in ('1', '2'):
            await pg.goto(f'file://{D}/player/thumb.html?v={v}'); await pg.wait_for_function('window.DONE')
            raw = f'{D}/build/thumb_v{v}.png'; os.makedirs(f'{D}/build', exist_ok=True)
            await (await pg.query_selector('canvas')).screenshot(path=raw)
            subprocess.run(['convert', raw, '-filter', 'Lanczos', '-resize', '1280x720', '-quality', '92', f'{D}/final/thumb_v{v}.jpg'], check=True)
            print('final/thumb_v%s.jpg' % v)
        await b.close()
asyncio.run(main())
