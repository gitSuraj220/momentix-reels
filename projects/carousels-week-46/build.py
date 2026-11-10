"""4 IG/FB carousels (1080x1350) for the week of 11 Nov 2026. Code-only, no paid credits.
Facts checked 10 Nov 2026 (sources in SOURCES.md)."""
import asyncio, os
from playwright.async_api import async_playwright
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__)); F = 'file://' + os.path.abspath(f'{D}/../../engine/fonts')
M = 'file://' + os.path.abspath(f'{D}/../beat-fd-ladder/art')
BASE = f"""@font-face{{font-family:P;font-weight:800;src:url({F}/poppins-latin-800-normal.woff2)}}
@font-face{{font-family:P;font-weight:500;src:url({F}/poppins-latin-500-normal.woff2)}}
@font-face{{font-family:A;src:url({F}/anton-latin-400-normal.woff2)}}
body{{margin:0;width:1080px;height:1350px;overflow:hidden;font-family:P;color:#fff}}
.bg{{position:absolute;inset:0}}
.brand{{position:absolute;left:70px;top:56px;font:800 28px P;letter-spacing:3px}}
.num{{position:absolute;right:70px;top:56px;font:800 32px P;color:#6b7280}}
.k{{position:absolute;left:70px;top:150px;font:800 32px P;letter-spacing:4px}}
.h{{position:absolute;left:70px;right:70px;top:200px;font:400 104px/1.0 A;letter-spacing:1px}}
.card{{position:absolute;left:70px;right:70px;border-radius:34px;padding:38px 44px;box-sizing:border-box}}
.big{{font:400 120px/1 A}} .mid{{font:800 46px/1.25 P}} .t{{font:500 38px/1.4 P;color:#d6dbe6}} .t b{{color:#fff}}
.fine{{position:absolute;left:70px;right:300px;bottom:44px;font:500 24px/1.3 P;color:#7c8396}}
.sw{{position:absolute;right:70px;bottom:40px;font:800 32px P}}
.row{{display:flex;align-items:center;gap:26px;margin:18px 0}} .pill{{font:800 30px P;padding:8px 20px;border-radius:14px}}
.arrow{{font:800 54px P;color:#6b7280}}"""
def page(theme, n, N, body, swipe=True, fine='Sirf jaankari ke liye'):
    bg, acc, brand = theme
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{BASE}</style></head><body>'
            f'<div class="bg" style="background:{bg}"></div><div class="brand" style="color:{acc}">{brand}</div><div class="num">{n}/{N}</div>{body}'
            f'<div class="fine">{fine}</div>' + (f'<div class="sw" style="color:{acc}">SWIPE →</div>' if swipe else '') + '</body></html>')
C = {}
# ---------- A) GTA 6 asli kharcha ----------
TA = ('radial-gradient(ellipse at 90% 0%,rgba(255,79,216,.28),transparent 55%),radial-gradient(ellipse at 0% 100%,rgba(0,229,255,.18),transparent 50%),#0b0a14', '#ff4fd8', 'GTA 6 · ASLI KHARCHA')
fa = 'Prices: game pre-order (Jun 2026), PS5 after Jul 2026 hike, PS Plus (May 2026) · buy karne se pehle check karo · Sirf jaankari ke liye'
def costcard(top, label, price, note, col):
    return (f'<div class="card" style="top:{top}px;background:#16142a;border:3px solid #2c2850"><div class="k" style="position:static;color:{col}">{label}</div>'
            f'<div class="big" style="margin-top:14px">{price}</div><div class="t" style="margin-top:14px">{note}</div></div>')
A = [
 page(TA, 1, 6, f'''<div class="h" style="top:180px;font-size:132px">GTA 6<br><span style="color:#ff4fd8">SIRF ₹5,999</span><br>KA NAHI HAI…</div>
 <div style="position:absolute;left:70px;top:640px;font:500 44px/1.35 P;color:#d6dbe6;width:600px">Game + console + online — <b style="color:#fff">asli total</b> dekh ke chaunk jaoge.</div>
 <img src="{M}/momo_shocked.png" style="position:absolute;right:10px;bottom:90px;height:600px">''', fine=fa),
 page(TA, 2, 6, '<div class="k" style="color:#ff4fd8">KHARCHA 1 · GAME</div><div class="h">GAME KI<br>KEEMAT</div>' +
      costcard(480, 'STANDARD EDITION', '₹5,999', 'Pre-order price, India.', '#00e5ff') + costcard(860, 'ULTIMATE EDITION', '₹7,499', 'Extra content ke saath.', '#ffd400'), fine=fa),
 page(TA, 3, 6, '<div class="k" style="color:#ff4fd8">KHARCHA 2 · CONSOLE</div><div class="h">PS5 KAHAN<br>SE LAOGE?</div>' +
      costcard(480, 'PS5 STANDARD (JUL 2026 SE)', '₹69,990', 'Pehle <b>₹54,990</b> tha — <b>₹15,000</b> mehenga ho gaya.', '#ff4fd8') +
      '<div class="card" style="top:900px;background:#16142a;border:3px solid #2c2850"><div class="mid">PC version abhi nahi</div><div class="t">Launch pe GTA 6 sirf PS5 aur Xbox pe aa raha hai.</div></div>', fine=fa),
 page(TA, 4, 6, '<div class="k" style="color:#ff4fd8">KHARCHA 3 · ONLINE</div><div class="h">DOSTON KE SAATH<br>ONLINE?</div>' +
      costcard(520, 'PS PLUS ESSENTIAL', '₹3,499<span style="font-size:60px">/saal</span>', 'Online multiplayer ke liye. <b>Story mode</b> ke liye zaroori nahi.', '#00e5ff'), fine=fa),
 page(TA, 5, 6, '''<div class="k" style="color:#ff4fd8">ASLI TOTAL</div><div class="h">PEHLE DIN KA<br>BILL</div>
 <div class="card" style="top:480px;background:#16142a;border:3px solid #2c2850">
  <div class="row"><span class="mid" style="width:520px">Game (Standard)</span><span class="mid">₹5,999</span></div>
  <div class="row"><span class="mid" style="width:520px">PS5 Standard</span><span class="mid">₹69,990</span></div>
  <div class="row"><span class="mid" style="width:520px">PS Plus (1 saal)</span><span class="mid">₹3,499</span></div>
  <div style="height:4px;background:#2c2850;margin:22px 0"></div>
  <div class="row"><span class="mid" style="width:520px;color:#ff4fd8">TOTAL</span><span class="big" style="color:#ff4fd8">₹79,488</span></div></div>
 <div style="position:absolute;left:70px;top:1130px;font:800 46px P">Matlab lagbhag <span style="color:#ffd400">₹80,000!</span></div>''', fine=fa),
 page(TA, 6, 6, f'''<div class="k" style="color:#ff4fd8">SMART TAREEKA</div><div class="h">PAISA KAISE<br>BACHAYEIN?</div>
 <div style="position:absolute;left:70px;right:330px;top:470px;font:500 40px/1.45 P;color:#d6dbe6">
 <p><b style="color:#ff4fd8">1.</b> PS5 pehle se hai? Toh sirf <b style="color:#fff">₹5,999</b> lagenge.</p>
 <p><b style="color:#ff4fd8">2.</b> Story mode akele khelo — PS Plus baad mein lo.</p>
 <p><b style="color:#ff4fd8">3.</b> EMI se pehle total byaaj zaroor jod lo.</p></div>
 <div style="position:absolute;left:70px;bottom:120px;font:800 46px P">Save karo · Gamer dost ko bhejo</div>
 <img src="{M}/momo_pointing.png" style="position:absolute;right:10px;bottom:170px;height:440px">''', swipe=False, fine=fa),
]
C['A_GTA6_Kharcha'] = A
# ---------- B) Free GitHub alternatives ----------
TB = ('radial-gradient(ellipse at 15% 0%,rgba(46,160,67,.28),transparent 55%),radial-gradient(ellipse at 100% 100%,rgba(88,166,255,.18),transparent 50%),#0d1117', '#3fb950', 'FREE · OPEN SOURCE')
fb = 'Free = khud install/host karna padega · kuch tools ko API key ya strong PC chahiye · Nov 2026'
def swap(top, paid, free, note, tag=None):
    tg = f'<span class="pill" style="background:#ffd400;color:#111;margin-left:auto">{tag}</span>' if tag else ''
    return (f'<div class="card" style="top:{top}px;background:#161b22;border:3px solid #30363d"><div class="row" style="margin:0">'
            f'<span class="mid" style="color:#8b949e;text-decoration:line-through">{paid}</span><span class="arrow">→</span><span class="mid" style="color:#3fb950">{free}</span>{tg}</div>'
            f'<div class="t" style="margin-top:14px">{note}</div></div>')
B = [
 page(TB, 1, 6, f'''<div class="h" style="top:190px;font-size:126px">PAID APPS<br>CHHODO?<br><span style="color:#3fb950">YE FREE HAIN</span></div>
 <div style="position:absolute;left:70px;top:660px;font:500 44px/1.35 P;color:#c9d1d9;width:600px">8 popular apps ke <b style="color:#fff">open-source</b> versions — GitHub pe free.</div>
 <img src="{M}/momo_thinking.png" style="position:absolute;right:10px;bottom:90px;height:600px">''', fine=fb),
 page(TB, 2, 6, '<div class="k" style="color:#3fb950">KAAM KE LIYE</div><div class="h">NOTES +<br>SCREEN VIDEO</div>' +
      swap(470, 'Notion', 'AppFlowy', 'Notes, docs, to-do — Notion jaisa, data aapke paas.') + swap(800, 'Loom', 'Cap', 'Screen record karke link share karo.'), fine=fb),
 page(TB, 3, 6, '<div class="k" style="color:#3fb950">MEETING + VOICE</div><div class="h">BOOKING +<br>BOLKE LIKHO</div>' +
      swap(470, 'Calendly', 'Cal.diy', 'Meeting booking link — Cal.com ka free community version.') + swap(800, 'Wispr Flow', 'OpenWhispr', 'Bolo, aur text type ho jaayega.'), fine=fb),
 page(TB, 4, 6, '<div class="k" style="color:#3fb950">TEAM + CUSTOMERS</div><div class="h">PROJECTS +<br>SUPPORT CHAT</div>' +
      swap(470, 'Asana', 'OpenProject', 'Tasks, timelines, team planning.') + swap(800, 'Intercom', 'Chatwoot', 'Website pe customer support chat.'), fine=fb),
 page(TB, 5, 6, '<div class="k" style="color:#3fb950">AI VOICE + SEO</div><div class="h">DHYAAN SE<br>CHUNO</div>' +
      swap(470, 'ElevenLabs', 'VoiceStudio', 'AI voice apne computer pe — strong PC/GPU chahiye.', 'HEAVY') +
      swap(800, 'Semrush', 'OpenSEO', 'SEO tool free hai, par data ke liye paid API lag sakti hai.', 'API'), fine=fb),
 page(TB, 6, 6, f'''<div class="k" style="color:#3fb950">SACH BHI JAANO</div><div class="h">FREE HAI,<br>PAR…</div>
 <div style="position:absolute;left:70px;right:320px;top:470px;font:500 40px/1.45 P;color:#c9d1d9">
 <p><b style="color:#3fb950">1.</b> Khud install ya server pe host karna padta hai.</p>
 <p><b style="color:#3fb950">2.</b> Kuch tools AI ke liye paid API key maangte hain.</p>
 <p><b style="color:#3fb950">3.</b> Pehle free trial jaisa test karo, phir switch.</p></div>
 <div style="position:absolute;left:70px;bottom:120px;font:800 46px P">Save karo · Developer dost ko bhejo</div>
 <img src="{M}/momo_pointing.png" style="position:absolute;right:10px;bottom:170px;height:440px">''', swipe=False, fine=fb),
]
C['B_Free_Alternatives'] = B
# ---------- C) Short Selling 5 rules ----------
TC = ('radial-gradient(ellipse at 85% 0%,rgba(255,59,92,.26),transparent 55%),radial-gradient(ellipse at 0% 100%,rgba(255,212,0,.14),transparent 50%),#0f0b0c', '#ff5c75', 'SHORT SELLING · 5 RULES')
fc = 'Sirf jaankari ke liye · Investment/trading advice nahi · SEBI study (FY26)'
def rule(n, N, k, title, body):
    return page(TC, n, N, f'<div class="k" style="color:#ff5c75">{k}</div><div class="h">{title}</div>'
                f'<div class="card" style="top:560px;background:#1c1416;border:3px solid #3a2a2d"><div class="t" style="font-size:44px">{body}</div></div>', fine=fc)
CC = [
 page(TC, 1, 7, f'''<div class="h" style="top:190px;font-size:130px">GIRTE DAAM SE<br><span style="color:#ff5c75">KAMAI?</span></div>
 <div style="position:absolute;left:70px;top:520px;font:500 46px/1.35 P;color:#e6d6d9;width:600px">Short selling karne se pehle ye <b style="color:#fff">5 rules</b> samajh lo.</div>
 <img src="{M}/momo_shocked.png" style="position:absolute;right:10px;bottom:90px;height:600px">''', fine=fc),
 rule(2, 7, 'RULE 1 · MATLAB', 'PEHLE BECHO,<br>BAAD MEIN KHAREEDO', 'Dost ka iPhone udhaar liya, <b>₹80,000</b> mein becha, daam gira toh <b>₹60,000</b> mein wapas khareed ke lauta diya = <b>₹20,000 profit</b>.<br><br>Share market mein yahi share ke saath hota hai.'),
 rule(3, 7, 'RULE 2 · INDIA MEIN', 'SIRF<br>INTRADAY', 'Cash market mein aam investor <b>usi din</b> short position band karta hai.<br><br>Band nahi ki aur share deliver nahi hua? <b>Auction + penalty</b> lag sakti hai.'),
 rule(4, 7, 'RULE 3 · OVERNIGHT', 'RAAT BHAR<br>SHORT?', 'Uske liye <b>F&amp;O</b> (futures/options) ya <b>SLB</b> (share udhaar lene ka exchange system) chahiye.<br><br>Dono mein margin aur rules alag hain.'),
 rule(5, 7, 'RULE 4 · RISK', 'LOSS KI<br>LIMIT NAHI', 'Share kharido toh zyada se zyada <b>100%</b> doob sakta hai.<br><br>Short karo aur daam <b>2x, 3x</b> ho jaaye — loss usse bhi zyada ho sakta hai.'),
 rule(6, 7, 'RULE 5 · DATA', '10 MEIN SE<br>~9 HAARE', 'SEBI study (FY26): <b>87.7%</b> individual F&amp;O traders ko loss hua.<br><br>Average loss: <b>₹1.17 lakh</b> per trader.'),
 page(TC, 7, 7, f'''<div class="k" style="color:#ff5c75">YAAD RAKHO</div><div class="h">SAMJHO PEHLE,<br>TRADE BAAD MEIN</div>
 <div style="position:absolute;left:70px;right:320px;top:500px;font:500 42px/1.45 P;color:#e6d6d9">
 <p>Short selling ek <b style="color:#fff">tool</b> hai — shortcut nahi.</p><p>Paper trading se seekho, aur utna hi lagao jitna kho sakte ho.</p></div>
 <div style="position:absolute;left:70px;bottom:120px;font:800 46px P">Save karo · Share karo</div>
 <img src="{M}/momo_pointing.png" style="position:absolute;right:10px;bottom:170px;height:440px">''', swipe=False, fine=fc),
]
C['C_Short_Selling_Rules'] = CC
# ---------- D) Loss headline kaise padhein ----------
TD = ('radial-gradient(ellipse at 10% 0%,rgba(62,224,122,.22),transparent 55%),radial-gradient(ellipse at 100% 100%,rgba(255,59,92,.22),transparent 50%),#0a0f0d', '#3ee07a', 'RESULTS PADHNA SEEKHO')
fd = 'Source: Anthropic S-1 (26 Oct 2026) + Amendment 1 (2 Nov 2026) · Sirf jaankari ke liye · Buy/sell advice nahi'
DD = [
 page(TD, 1, 5, f'''<div class="h" style="top:190px;font-size:118px">"COMPANY KO<br><span style="color:#ff3b5c">CRORE KA LOSS"</span><br>DARNA MAT</div>
 <div style="position:absolute;left:70px;top:620px;font:500 44px/1.35 P;color:#d6e6dc;width:600px">Headline ke peeche ka sach <b style="color:#fff">2 checks</b> mein pakdo.</div>
 <img src="{M}/momo_thinking.png" style="position:absolute;right:10px;bottom:90px;height:600px">''', fine=fd),
 page(TD, 2, 5, '''<div class="k" style="color:#3ee07a">EXAMPLE · ANTHROPIC (APR–JUN 2026)</div><div class="h">PROFIT BHI,<br>LOSS BHI?</div>
 <div class="card" style="top:480px;background:#111a15;border:3px solid #23352b">
  <div class="row"><span class="mid" style="width:560px">Kamai (revenue)</span><span class="mid">$11.6B</span></div>
  <div class="row"><span class="mid" style="width:560px;color:#3ee07a">Operating profit</span><span class="mid" style="color:#3ee07a">+$974M</span></div>
  <div class="row"><span class="mid" style="width:560px;color:#ff3b5c">Net loss</span><span class="big" style="color:#ff3b5c">$66.3B</span></div></div>
 <div style="position:absolute;left:70px;top:1050px;font:800 44px P">Dono sach hain. Kaise?</div>''', fine=fd),
 page(TD, 3, 5, '''<div class="k" style="color:#3ee07a">WAJAH</div><div class="h">ZYAADATAR<br>KAAGAZ PE</div>
 <div class="card" style="top:480px;background:#111a15;border:3px solid #23352b"><div class="t" style="font-size:44px">
 Investors ko future mein shares dene ka <b>wada</b> tha. Company ki value uchhli, toh wo wada accounts mein mehenga dikhaya gaya.<br><br>
 <b style="color:#3ee07a">$59.6B</b> = non-cash charge. Paisa jeb se gaya nahi.</div></div>''', fine=fd),
 page(TD, 4, 5, '''<div class="k" style="color:#3ee07a">2 CHECKS</div><div class="h">HEADLINE KE<br>BAAD YE DEKHO</div>
 <div class="card" style="top:480px;background:#111a15;border:3px solid #23352b"><div class="mid" style="color:#3ee07a">1. Operating profit hai?</div><div class="t">Core business kama raha hai ya nahi.</div></div>
 <div class="card" style="top:800px;background:#111a15;border:3px solid #23352b"><div class="mid" style="color:#ffd400">2. Loss cash ka ya kaagaz ka?</div><div class="t">Cash flow statement mein dekho — paisa sach mein gaya ya nahi.</div></div>''', fine=fd),
 page(TD, 5, 5, f'''<div class="k" style="color:#3ee07a">TWIST BHI</div><div class="h">AGLE 3 MAHINE<br>MEIN?</div>
 <div style="position:absolute;left:70px;right:320px;top:480px;font:500 42px/1.45 P;color:#d6e6dc">
 <p>Jul–Sep: kamai <b style="color:#fff">$17B</b>, par operating <b style="color:#ff3b5c">loss</b> wapas.</p>
 <p>Isliye ek quarter nahi — <b style="color:#fff">trend</b> dekho.</p></div>
 <div style="position:absolute;left:70px;bottom:120px;font:800 46px P">Save karo · Share karo</div>
 <img src="{M}/momo_pointing.png" style="position:absolute;right:10px;bottom:170px;height:440px">''', swipe=False, fine=fd),
]
C['D_Loss_Headline'] = DD
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1350})
        for name, slides in C.items():
            od = f'{D}/out/{name}'; os.makedirs(od, exist_ok=True)
            for i, h in enumerate(slides, 1):
                open(f'{od}/s{i}.html', 'w').write(h); await pg.goto(f'file://{od}/s{i}.html'); await pg.wait_for_timeout(400)
                await pg.screenshot(path=f'{od}/Slide_{i:02d}.jpg', type='jpeg', quality=93)
        await b.close()
asyncio.run(main())
for name, slides in C.items():
    n = len(slides); W = Image.new('RGB', (240 * n, 300), 'black')
    for i in range(n): W.paste(Image.open(f'{D}/out/{name}/Slide_{i+1:02d}.jpg').resize((240, 300)), (i * 240, 0))
    W.save(f'/tmp/claude-0/ss/{name}.jpg', quality=82)
print('ok')
