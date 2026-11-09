"""IG/FB carousel 1080x1350: 10 free Google AI tools (from the 7 Nov reel). Dark tech style, Google 4-colour accents, Momo cutouts.
Facts (Nov 2026, from projects/google-free-ai-tools/script.md + earlier checks): free tiers have limits; Mixboard/Pomelli limited countries."""
import asyncio, os
from playwright.async_api import async_playwright
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__)); F = 'file://' + os.path.abspath(f'{D}/../../engine/fonts')
M = 'file://' + os.path.abspath(f'{D}/../beat-fd-ladder/art')
CSS = f"""@font-face{{font-family:P;font-weight:800;src:url({F}/poppins-latin-800-normal.woff2)}}
@font-face{{font-family:P;font-weight:500;src:url({F}/poppins-latin-500-normal.woff2)}}
body{{margin:0;width:1080px;height:1350px;overflow:hidden;font-family:P;background:#0b0d14;color:#fff}}
.bg{{position:absolute;inset:0;background:radial-gradient(ellipse at 20% 0%,rgba(66,133,244,.28),transparent 55%),radial-gradient(ellipse at 100% 100%,rgba(52,168,83,.22),transparent 50%),#0b0d14}}
.dots{{position:absolute;left:70px;top:60px;display:flex;gap:14px}} .dots i{{width:22px;height:22px;border-radius:50%;display:block}}
.num{{position:absolute;right:70px;top:52px;font:800 34px P;color:#6b7280}}
.card{{position:absolute;left:70px;right:70px;height:500px;border-radius:40px;background:#151926;border:3px solid #232a3d;padding:44px 50px;box-sizing:border-box}}
.tile{{width:120px;height:120px;border-radius:30px;display:flex;align-items:center;justify-content:center;font:800 64px P;color:#fff}}
.t{{font:800 64px/1.05 P;margin-top:26px}} .d{{font:500 40px/1.3 P;color:#c9cfdc;margin-top:16px}}
.u{{position:absolute;left:50px;bottom:40px;font:800 34px P;color:#8ab4f8}}
.tag{{position:absolute;right:46px;top:46px;font:800 28px P;padding:8px 22px;border-radius:999px}}
.fine{{position:absolute;left:70px;bottom:40px;font:500 26px P;color:#7c8396}}
.sw{{position:absolute;right:70px;bottom:36px;font:800 34px P;color:#fbbc05}}"""
G = ['#4285F4', '#EA4335', '#FBBC05', '#34A853']
def page(n, body, swipe=True):
    dots = ''.join(f'<i style="background:{c}"></i>' for c in G)
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="bg"></div><div class="dots">{dots}</div>'
            f'<div class="num">{n}/6</div>{body}<div class="fine">Free tiers mein limits hain · Nov 2026</div>' + ('<div class="sw">SWIPE →</div>' if swipe else '') + '</body></html>')
def card(top, k, name, desc, url, col, tag=None, tagc='#34A853'):
    tg = f'<div class="tag" style="background:{tagc};color:#0b0d14">{tag}</div>' if tag else ''
    return (f'<div class="card" style="top:{top}px">{tg}<div class="tile" style="background:{col}">{k}</div>'
            f'<div class="t">{name}</div><div class="d">{desc}</div><div class="u">{url}</div></div>')
S = []
S.append(page(1, f'''
<div style="position:absolute;left:70px;top:170px;font:800 64px P;color:#9aa0a6">GOOGLE KE</div>
<div style="position:absolute;left:70px;top:240px;font:800 210px/0.95 P">10 FREE</div>
<div style="position:absolute;left:70px;top:450px;font:800 150px/1 P;background:linear-gradient(90deg,#4285F4,#EA4335,#FBBC05,#34A853);-webkit-background-clip:text;color:transparent">AI TOOLS</div>
<div style="position:absolute;left:70px;top:640px;font:500 46px/1.35 P;color:#c9cfdc;width:560px">Code, design, apps, music — sab free mein try karo!</div>
<img src="{M}/momo_shocked.png" style="position:absolute;right:30px;bottom:110px;height:640px">'''))
pairs = [
    [('A', 'Antigravity', 'AI code editor — Cursor jaisa. Prompt do, app ban jaati hai.', 'antigravity.google', G[0], 'CODING'),
     ('S', 'Google AI Studio', 'Seconds mein chhote AI apps banao aur test karo.', 'aistudio.google.com', G[1], 'APPS')],
    [('St', 'Stitch', 'Prompt ya sketch do — UI design + front-end code ready.', 'stitch.withgoogle.com', G[2], 'DESIGN'),
     ('O', 'Opal', 'Bina code ke AI mini-apps. India mein available.', 'opal.google', G[3], 'NO-CODE')],
    [('J', 'Jules', 'GitHub coding agent — features banata, bugs fix karta. 15 tasks/day free.', 'jules.google', G[0], 'AGENT'),
     ('N', 'NotebookLM', 'Apne PDFs aur notes se sawaal poocho, audio summary suno.', 'notebooklm.google.com', G[1], 'STUDY')],
    [('W', 'Code Wiki', 'GitHub repo ko samajhne layak docs mein badlo.', 'codewiki.google', G[2], 'DOCS'),
     ('F', 'Flow Music', 'AI se music banao — roz free credits.', 'labs.google', G[3], 'MUSIC')],
    [('Mx', 'Mixboard', 'AI mood board — ideas ko visual board mein.', 'labs.google', G[0], 'LIMITED', '#fbbc05'),
     ('P', 'Pomelli', 'Apne business ke liye AI marketing posts.', 'labs.google.com/pomelli', G[1], 'LIMITED', '#fbbc05')],
]
for i, pr in enumerate(pairs):
    body = ''.join(card(150 + j * 560, *c) for j, c in enumerate(pr))
    S.append(page(i + 2, body, i < len(pairs) - 1))
async def main():
    os.makedirs(f'{D}/out', exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1350})
        for i, h in enumerate(S, 1):
            open(f'{D}/out/s{i}.html', 'w').write(h); await pg.goto(f'file://{D}/out/s{i}.html'); await pg.wait_for_timeout(500)
            await pg.screenshot(path=f'{D}/out/slide_{i}.png')
        await b.close()
asyncio.run(main())
ims = [Image.open(f'{D}/out/slide_{i}.png').convert('RGB') for i in range(1, 7)]
for i, im in enumerate(ims, 1): im.save(f'{D}/out/Slide_{i:02d}.jpg', quality=93)
W = Image.new('RGB', (360 * 4, 450 * 2), 'black')
for i, im in enumerate(ims): W.paste(im.resize((360, 450)), ((i % 4) * 360, (i // 4) * 450))
W.save('/tmp/claude-0/gcar.jpg', quality=85); print('ok')
