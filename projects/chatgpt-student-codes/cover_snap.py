import threading, http.server, socketserver, os
from playwright.sync_api import sync_playwright
os.chdir(os.path.dirname(os.path.abspath(__file__)))
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.TCPServer(('127.0.0.1', 0), Q); threading.Thread(target=srv.serve_forever, daemon=True).start()
ARGS = ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist']
SHOTS = {'gold': 24.95}
with sync_playwright() as p:
    b = p.chromium.launch(args=ARGS); pg = b.new_page(viewport={'width': 1080, 'height': 1920}); port = srv.server_address[1]
    pg.goto(f'http://127.0.0.1:{port}/reel.html'); pg.wait_for_function('window.READY', timeout=180000); pg.evaluate('window.COVER=1')
    for k, t in SHOTS.items(): pg.evaluate(f'renderAt({t})'); pg.screenshot(path=f'build/cbg_{k}.png')
    for bg, top in [('gold', 1050)]:
        pg.set_content(f"""<html><head><style>@font-face{{font-family:A2;src:url(http://127.0.0.1:{port}/fonts/anton.woff2)}}@font-face{{font-family:P;font-weight:800;src:url(http://127.0.0.1:{port}/fonts/p800.woff2)}}
        body{{margin:0;width:1080px;height:1920px;background:url(http://127.0.0.1:{port}/build/cbg_{bg}.png) center/cover;font-family:A2;overflow:hidden}}
        .v{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.6) 0%,rgba(0,0,0,0) 34%,rgba(0,0,0,0) 50%,rgba(0,0,0,.7) 80%,rgba(0,0,0,.4) 100%)}}
        .w{{position:absolute;left:60px;right:40px;top:{top}px}}
        .s{{font:800 44px P;letter-spacing:5px;color:#ffd23f;text-shadow:0 4px 20px rgba(0,0,0,.9)}}
        .b{{font-size:150px;line-height:.95;color:#fff;letter-spacing:2px;text-shadow:0 12px 50px rgba(0,0,0,.85),0 0 4px rgba(0,0,0,.7);margin-top:8px}}
        .b span{{display:block;font-size:172px;color:#7dffcf;white-space:nowrap}}
        .t{{display:inline-block;margin-top:18px;padding:10px 22px;border-radius:14px;background:#ffd23f;color:#1a1200;font:800 44px P;letter-spacing:3px}}</style></head>
        <body><div class="v"></div><div class="w"><div class="s">— EXAM SE PEHLE</div><div class="b">CHATGPT KE 3<span>SECRET CODES</span></div><div class="t">FOR STUDENTS</div></div></body></html>""")
        pg.wait_for_timeout(800); pg.screenshot(path=f'final/cover_{bg}.png')
    b.close()
srv.shutdown()
