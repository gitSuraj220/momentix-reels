#!/usr/bin/env python3
"""Render player -> build/video_only.mp4 (1920x1080, 30 fps). Parallel chunks:
    python3 render.py [--workers N] [--from S --to S]   (PW_EXE = chromium headless_shell path if needed)
Each worker grabs canvas.toDataURL JPEG frames and pipes them to its own ffmpeg; chunks are concatenated losslessly."""
import os, sys, json, base64, asyncio, argparse, subprocess, time
from playwright.async_api import async_playwright
D = os.path.dirname(os.path.abspath(__file__)); FPS = 30
ap = argparse.ArgumentParser(); ap.add_argument('--workers', type=int, default=max(1, (os.cpu_count() or 2) - 1))
ap.add_argument('--from', dest='a', type=float, default=0); ap.add_argument('--to', dest='b', type=float, default=None)
ap.add_argument('--out', default=f'{D}/build/video_only.mp4')
A = ap.parse_args()
DUR = json.load(open(f'{D}/shots.json'))['duration']
f0, f1 = int(A.a * FPS), int(round((A.b or DUR) * FPS))
os.makedirs(f'{D}/build/chunks', exist_ok=True)


async def worker(k, a, b, pw):
    out = f'{D}/build/chunks/c{k:02d}.mp4'
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                           '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', str(FPS), out], stdin=subprocess.PIPE)
    br = await pw.chromium.launch(executable_path=os.environ.get('PW_EXE') or None, args=['--allow-file-access-from-files'])
    pg = await br.new_page(viewport={'width': 1920, 'height': 1080})
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    await pg.goto('file://' + f'{D}/player/index.html'); await pg.evaluate('READY')
    t = time.time()
    for f in range(a, b):
        u = await pg.evaluate(f"(renderAt({f / FPS}), document.getElementById('c').toDataURL('image/jpeg', .93))")
        ff.stdin.write(base64.b64decode(u.split(',', 1)[1]))
        if k == 0 and (f - a) % 300 == 0:
            print(f'w0 {f - a}/{b - a} frames, {(time.time() - t) / max(1, f - a) * 1000:.0f} ms/frame', flush=True)
    ff.stdin.close(); ff.wait(); await br.close()
    if errs: print('worker', k, 'errors', errs[:3])
    return out


async def main():
    n = A.workers; step = (f1 - f0 + n - 1) // n
    async with async_playwright() as pw:
        outs = await asyncio.gather(*[worker(k, f0 + k * step, min(f1, f0 + (k + 1) * step), pw) for k in range(n) if f0 + k * step < f1])
    lst = f'{D}/build/chunks/list.txt'
    open(lst, 'w').write(''.join(f"file '{o}'\n" for o in outs))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', A.out], check=True)
    print('wrote', A.out, f'{(f1 - f0) / FPS:.1f}s')

t0 = time.time(); asyncio.run(main()); print(f'render took {time.time() - t0:.0f}s')
