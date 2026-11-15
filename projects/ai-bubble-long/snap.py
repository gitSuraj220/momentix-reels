#!/usr/bin/env python3
"""QA contact sheets: python3 snap.py [out_dir] [--ids 1,2,3] [--at 0.5] [--qa]
Renders each shot at fraction --at of its length (default 0.6) and tiles 4x4 sheets."""
import os, sys, json, asyncio, argparse, subprocess
from playwright.async_api import async_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser(); ap.add_argument('out', nargs='?', default='/tmp/aib_snap')
ap.add_argument('--ids'); ap.add_argument('--at', type=float, default=.6); ap.add_argument('--qa', action='store_true')
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
shots = json.load(open(os.path.join(HERE, 'shots.json')))['shots']
ids = [int(x) for x in a.ids.split(',')] if a.ids else [s['id'] for s in shots]


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get('PW_EXE') or None, args=['--allow-file-access-from-files'])
        pg = await b.new_page(viewport={'width': 1920, 'height': 1080})
        errs = []
        pg.on('console', lambda m: m.type in ('error', 'warning') and errs.append(m.text))
        pg.on('pageerror', lambda e: errs.append('PAGEERROR ' + str(e)))
        await pg.goto('file://' + os.path.join(HERE, 'player', 'index.html') + ('?qa=1' if a.qa else ''))
        await pg.evaluate('READY')
        files = []
        for s in shots:
            if s['id'] not in ids:
                continue
            t = s['t0'] + (s['t1'] - s['t0']) * a.at
            await pg.evaluate(f'renderAt({t})')
            f = os.path.join(a.out, 's%03d.jpg' % s['id'])
            el = await pg.query_selector('canvas')
            await el.screenshot(path=f, type='jpeg', quality=80)
            files.append(f)
        await b.close()
    for i in range(0, len(files), 16):
        subprocess.run(['montage', *files[i:i + 16], '-tile', '4x4', '-geometry', '480x270+3+3', '-background', '#222',
                        os.path.join(a.out, 'sheet_%02d.jpg' % (i // 16))], check=True)
    print('rendered', len(files), 'errors:', len(errs))
    for e in sorted(set(errs))[:30]:
        print(' ', e[:300])

asyncio.run(main())
