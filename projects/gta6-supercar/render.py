"""Parallel frame render of reel.html -> build/video_only.mp4 (1080x1920, 30 fps).
usage: python3 render.py [workers] [t0 t1]"""
import sys, os, json, subprocess, threading, http.server, socketserver, time
from multiprocessing import Process
ROOT = os.path.dirname(os.path.abspath(__file__)); os.chdir(ROOT)
FPS = 30; T = json.load(open('timeline.json'))['T']; END = T['end']
NW = int(sys.argv[1]) if len(sys.argv) > 1 else 4
T0, T1 = (float(sys.argv[2]), float(sys.argv[3])) if len(sys.argv) > 3 else (0, END)
ARGS = ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist']
def work(k, f0, f1):
    from playwright.sync_api import sync_playwright
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    srv = socketserver.TCPServer(('127.0.0.1', 0), Q); threading.Thread(target=srv.serve_forever, daemon=True).start()
    out = f'build/seg_{k:02d}.mp4'
    ff = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'png', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    with sync_playwright() as p:
        b = p.chromium.launch(args=ARGS); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.on('pageerror', lambda e: print('ERR', k, e))
        pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/reel.html'); pg.wait_for_function('window.READY', timeout=180000)
        st = time.time()
        for f in range(f0, f1):
            pg.evaluate(f'renderAt({f / FPS})'); ff.stdin.write(pg.screenshot(type='png'))
            if (f - f0) % 60 == 0: print(f'w{k} {f - f0}/{f1 - f0} {time.time() - st:.0f}s', flush=True)
        b.close()
    ff.stdin.close(); ff.wait(); srv.shutdown()
if __name__ == '__main__':
    os.makedirs('build', exist_ok=True)
    F0, F1 = int(T0 * FPS), int(T1 * FPS); n = F1 - F0; per = -(-n // NW)
    ps = [Process(target=work, args=(k, F0 + k * per, min(F1, F0 + (k + 1) * per))) for k in range(NW) if F0 + k * per < F1]
    [p.start() for p in ps]; [p.join() for p in ps]
    open('build/list.txt', 'w').write(''.join(f"file 'seg_{k:02d}.mp4'\n" for k in range(len(ps))))
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', 'build/list.txt', '-c', 'copy', 'build/video_only.mp4'])
    print('done', subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', 'build/video_only.mp4'], capture_output=True, text=True).stdout)
