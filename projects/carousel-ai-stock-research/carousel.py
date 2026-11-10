"""IG/FB carousel 1080x1350: 'AI ko apna stock research assistant banao' - 5 copy-paste prompts (works in ChatGPT/Claude/Gemini).
Inspired by @raycfu's Claude stock-market carousel; ours is homework-only for Indian stocks, no buy/sell calls, verify on NSE/BSE."""
import asyncio, os
from playwright.async_api import async_playwright
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__)); F = 'file://' + os.path.abspath(f'{D}/../../engine/fonts')
M = 'file://' + os.path.abspath(f'{D}/../beat-fd-ladder/art')
N = 7
CSS = f"""@font-face{{font-family:P;font-weight:800;src:url({F}/poppins-latin-800-normal.woff2)}}
@font-face{{font-family:P;font-weight:500;src:url({F}/poppins-latin-500-normal.woff2)}}
@font-face{{font-family:C;font-weight:400;src:url({F}/courier-prime-latin-400-normal.woff2)}}
@font-face{{font-family:C;font-weight:700;src:url({F}/courier-prime-latin-700-normal.woff2)}}
body{{margin:0;width:1080px;height:1350px;overflow:hidden;font-family:P;background:#0a0f0d;color:#fff}}
.bg{{position:absolute;inset:0;background:radial-gradient(ellipse at 85% 0%,rgba(0,200,120,.22),transparent 55%),
 linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px) 0 0/100% 54px,#0a0f0d}}
.num{{position:absolute;right:70px;top:56px;font:800 34px P;color:#5b6b63}}
.brand{{position:absolute;left:70px;top:56px;font:800 30px P;color:#00d18b;letter-spacing:3px}}
.k{{position:absolute;left:70px;top:150px;font:800 34px P;color:#00d18b;letter-spacing:4px}}
.h{{position:absolute;left:70px;right:70px;top:200px;font:800 78px/1.05 P}}
.box{{position:absolute;left:70px;right:70px;top:440px;background:#121a16;border:3px solid #1f3a2e;border-radius:34px;padding:40px 44px 44px}}
.box .bar{{display:flex;gap:12px;margin-bottom:26px}} .box .bar i{{width:18px;height:18px;border-radius:50%;display:block}}
.box .copy{{position:absolute;right:30px;top:26px;font:800 24px P;color:#0a0f0d;background:#00d18b;padding:6px 18px;border-radius:999px}}
.pr{{font:700 54px/1.38 C;color:#e8fff4}} .pr b{{color:#ffd400}}
.tip{{position:absolute;left:70px;right:70px;bottom:120px;font:500 36px/1.35 P;color:#b7c9c0}} .tip b{{color:#fff}}
.fine{{position:absolute;left:70px;bottom:44px;font:500 25px P;color:#5b6b63}}
.sw{{position:absolute;right:70px;bottom:38px;font:800 32px P;color:#ffd400}}"""
def page(n, body, swipe=True, fine='Sirf jaankari ke liye · Investment advice nahi'):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="bg"></div>'
            f'<div class="brand">AI × STOCKS</div><div class="num">{n}/{N}</div>{body}<div class="fine">{fine}</div>'
            + ('<div class="sw">SWIPE →</div>' if swipe else '') + '</body></html>')
DOTS = '<div class="bar"><i style="background:#ff5f57"></i><i style="background:#febc2e"></i><i style="background:#28c840"></i></div>'
def prompt(n, k, title, text, tip):
    return page(n, f'<div class="k">PROMPT {k}/5</div><div class="h">{title}</div>'
                   f'<div class="box">{DOTS}<div class="copy">COPY</div><div class="pr">{text}</div></div><div class="tip">{tip}</div>')
S = [page(1, f'''
<div style="position:absolute;left:70px;top:170px;font:800 54px P;color:#9fb3aa">AI ko apna</div>
<div style="position:absolute;left:70px;top:240px;font:800 128px/0.98 P;width:900px">STOCK<br><span style="color:#00d18b">RESEARCH</span><br>ASSISTANT</div>
<div style="position:absolute;left:70px;top:640px;font:800 54px P">banao → <span style="color:#ffd400">5 prompts</span></div>
<div style="position:absolute;left:70px;top:740px;font:500 40px/1.35 P;color:#b7c9c0;width:560px">Copy-paste karo — ChatGPT, Claude ya Gemini, kisi mein bhi chalega.</div>
<img src="{M}/momo_thinking.png" style="position:absolute;right:20px;bottom:100px;height:600px">''')]
S += [
 prompt(2, 1, 'Results ko simple<br>bhasha mein samjho',
        'Is company ke latest quarterly results simple Hindi mein samjhao: <b>revenue, profit, margin</b> — pichhle saal se kya badla?',
        '<b>Tip:</b> NSE/BSE se results ka PDF download karke upload karo — AI tab asli numbers padhega.'),
 prompt(3, 2, 'Business model<br>2 minute mein',
        'Ye company paise kaise kamati hai? <b>Top 3 revenue sources</b> aur <b>3 sabse bade risks</b> batao.',
        '<b>Kyun:</b> Jo business samajh nahi aata, usme paisa lagana andhere mein teer hai.'),
 prompt(4, 3, '2 stocks ka<br>side-by-side table',
        '<b>Company A vs Company B</b>: sales growth, debt, ROE aur profit margin ka table banao — 5 saal ka trend.',
        '<b>Tip:</b> Same sector ki companies compare karo — bank vs IT ka comparison bekaar hai.'),
 prompt(5, 4, 'Red flags<br>dhoondo',
        'Is annual report mein <b>red flags</b> dhoondo: debt badh raha hai? promoter pledge? related-party deals? auditor ki remarks?',
        '<b>Kyun:</b> Achhi kahaani sab sunate hain — kamzori dhoondhna asli homework hai.'),
 prompt(6, 5, 'Concall ka<br>saar nikaalo',
        'Is earnings call transcript se batao: management ne <b>agle 1–2 saal</b> ke baare mein kya kaha — <b>5 points</b> mein.',
        '<b>Tip:</b> Company ki website ke "Investors" section mein transcript milta hai.'),
 page(7, f'''
<div class="k">3 RULES — ZAROOR YAAD RAKHO</div>
<div class="h" style="font-size:70px">AI = homework,<br><span style="color:#ffd400">faisla aapka</span></div>
<div style="position:absolute;left:70px;right:300px;top:470px;font:500 42px/1.4 P;color:#d8e6df">
<p><b style="color:#ff5f57">1.</b> AI galat numbers bhi bata sakta hai — hamesha <b style="color:#fff">NSE/BSE filing</b> se check karo.</p>
<p><b style="color:#ff5f57">2.</b> "Kaunsa share khareedun?" AI se mat poocho — wo aapki halat nahi jaanta.</p>
<p><b style="color:#ff5f57">3.</b> Research ke baad bhi risk rehta hai. Utna hi lagao jitna kho sakte ho.</p></div>
<div style="position:absolute;left:70px;bottom:120px;font:800 48px P">Save karo · Share karo</div>
<img src="{M}/momo_pointing.png" style="position:absolute;right:10px;bottom:150px;height:470px">''', swipe=False,
      fine='Sirf jaankari ke liye · Investment advice nahi · Nov 2026'),
]
async def main():
    os.makedirs(f'{D}/out', exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1350})
        for i, h in enumerate(S, 1):
            open(f'{D}/out/s{i}.html', 'w').write(h); await pg.goto(f'file://{D}/out/s{i}.html'); await pg.wait_for_timeout(500)
            await pg.screenshot(path=f'{D}/out/slide_{i}.png')
        await b.close()
asyncio.run(main())
ims = [Image.open(f'{D}/out/slide_{i}.png').convert('RGB') for i in range(1, N + 1)]
for i, im in enumerate(ims, 1): im.save(f'{D}/Slide_{i:02d}.jpg', quality=93)
W = Image.new('RGB', (360 * 4, 450 * 2), 'black')
for i, im in enumerate(ims): W.paste(im.resize((360, 450)), ((i % 4) * 360, (i // 4) * 450))
W.save('/tmp/claude-0/ss/aicar.jpg', quality=85); print('ok')
