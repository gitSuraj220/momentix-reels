import threading, http.server, socketserver, os
from playwright.sync_api import sync_playwright
os.chdir(os.path.dirname(os.path.abspath(__file__)))
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.TCPServer(('127.0.0.1', 0), Q); threading.Thread(target=srv.serve_forever, daemon=True).start()
ARGS = ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist']
SHOTS = {'garage': 51.9, 'button': 4.75, 'smash': 2.02, 'heat': 43.0}
with sync_playwright() as p:
    b = p.chromium.launch(args=ARGS); pg = b.new_page(viewport={'width': 1080, 'height': 1920}); port = srv.server_address[1]
    pg.goto(f'http://127.0.0.1:{port}/reel.html'); pg.wait_for_function('window.READY', timeout=180000); pg.evaluate('window.COVER=1')
    for k, t in SHOTS.items(): pg.evaluate(f'renderAt({t})'); pg.screenshot(path=f'build/cbg_{k}.png')
    for name, bg, big, small, col in [('WORST_CAR', 'garage', 'WORST<br>CAR?', 'GTA 6 SUPERCAR', '#5b9dff'), ('WONT_START', 'button', "WON'T<br>START", 'GTA 6 CAR CHORI', '#ff2a4d'), ('CHORI_FAIL', 'heat', 'CHORI<br>FAIL?', 'GTA 6 SUPERCAR', '#ffb347')]:
        pg.set_content(f"""<html><head><style>@font-face{{font-family:A2;src:url(http://127.0.0.1:{port}/fonts/anton.woff2)}}@font-face{{font-family:P;font-weight:700;src:url(http://127.0.0.1:{port}/fonts/p700.woff2)}}
        body{{margin:0;width:1080px;height:1920px;background:url(http://127.0.0.1:{port}/build/cbg_{bg}.png) center/cover;font-family:A2;overflow:hidden}}
        .v{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.55) 0%,rgba(0,0,0,0) 38%,rgba(0,0,0,0) 62%,rgba(0,0,0,.6) 100%)}}
        .s{{position:absolute;left:64px;top:{1060 if bg=='heat' else 330}px;font:700 46px P;letter-spacing:6px;color:{col};text-shadow:0 4px 20px rgba(0,0,0,.8)}}
        .b{{position:absolute;left:58px;top:{1120 if bg=='heat' else 390}px;font-size:270px;line-height:.92;color:#fff;letter-spacing:3px;text-shadow:0 12px 50px rgba(0,0,0,.8),0 0 4px rgba(0,0,0,.6)}}
        .b span{{color:{col}}}</style></head><body><div class="v"></div><div class="s">— {small}</div><div class="b">{big.split('<br>')[0]}<br><span>{big.split('<br>')[1]}</span></div></body></html>""")
        pg.wait_for_timeout(800); pg.screenshot(path=f'final/cover_{name}.png')
    b.close()
srv.shutdown()
