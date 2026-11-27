"""python3 snap.py page.html out_prefix t1 t2 ...  -> PNG frames (1920x1080) via renderAt(t)"""
import sys, threading, http.server, socketserver, os, time
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.abspath(__file__)); os.chdir(ROOT)
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.TCPServer(('127.0.0.1', 0), Q); threading.Thread(target=srv.serve_forever, daemon=True).start()
ARGS = ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist']
page, pre, ts = sys.argv[1], sys.argv[2], [float(x) for x in sys.argv[3:]]
with sync_playwright() as p:
    b = p.chromium.launch(args=ARGS); pg = b.new_page(viewport={'width': 1920, 'height': 1080})
    pg.on('console', lambda m: print('C', m.text) if m.type in ('error', 'warning') else None); pg.on('pageerror', lambda e: print('ERR', e))
    pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/{page}'); pg.wait_for_function('window.READY', timeout=120000)
    for t in ts:
        t0 = time.time(); pg.evaluate(f'renderAt({t})'); pg.screenshot(path=f'{pre}_{t:05.2f}.png'); print(t, round(time.time() - t0, 2))
    b.close()
srv.shutdown()
