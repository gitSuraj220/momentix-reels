"""IG/FB carousel (1080x1350, 4:5): Saving -> Investing in 5 steps. Notebook paper-collage style, Momo cutouts.
Numbers: Rs1L @3% 20y = 1.81L, @12% = 9.65L; SIP 5000 @12% 20y = 49.96L (12L invested); Nifty Mar-2020 fall ~40%, back to old high Nov 2020."""
import asyncio, os
from playwright.async_api import async_playwright
D = os.path.dirname(os.path.abspath(__file__)); F = 'file://' + os.path.abspath(f'{D}/../../engine/fonts')
CSS = f"""
@font-face{{font-family:PM;src:url({F}/permanent-marker-latin-400-normal.woff2)}}
@font-face{{font-family:CV;font-weight:700;src:url({F}/caveat-latin-700-normal.woff2)}}
@font-face{{font-family:P;font-weight:800;src:url({F}/poppins-latin-800-normal.woff2)}}
body{{margin:0;width:1080px;height:1350px;overflow:hidden;font-family:CV}}
.pg{{position:absolute;inset:0;background:linear-gradient(90deg,transparent 118px,#e5737b 118px,#e5737b 121px,transparent 121px),
 repeating-linear-gradient(180deg,transparent 0 52px,#a9c4dc 52px 54px),#f7f2e5}}
.pg:after{{content:"";position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%,transparent 60%,rgba(90,60,30,.2))}}
.hole{{position:absolute;left:38px;width:40px;height:40px;border-radius:50%;background:#3a2c22}}
.a{{position:absolute}}
.cut{{filter:drop-shadow(3px 0 0 #fff) drop-shadow(-3px 0 0 #fff) drop-shadow(0 3px 0 #fff) drop-shadow(0 -3px 0 #fff) drop-shadow(5px 8px 7px rgba(60,40,20,.28))}}
.note{{box-shadow:6px 10px 14px rgba(60,40,20,.28);border-radius:3px;padding:30px 36px;box-sizing:border-box}}
.tape{{position:absolute;width:150px;height:44px;background:rgba(236,222,180,.8)}}
.mk{{font-family:PM;color:#1d1d1d;line-height:1.05}}
.h{{font-weight:700;color:#1f3d8a;line-height:1.15}}
.hl{{background:linear-gradient(transparent 18%,rgba(255,224,0,.7) 18%,rgba(255,224,0,.7) 88%,transparent 88%);padding:0 8px}}
.num{{position:absolute;right:50px;top:40px;font:40px PM;color:#b5a58a}}
.fine{{position:absolute;left:150px;bottom:36px;font:700 30px CV;color:#7a6a58}}
.swipe{{position:absolute;right:56px;bottom:40px;font:46px PM;color:#c2273a}}
.momo{{position:absolute;height:520px}}
"""
def page(n, body, swipe=True, fine='Sirf jaankari ke liye'):
    holes = ''.join(f'<div class="hole" style="top:{y}px"></div>' for y in (200, 655, 1110))
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="pg">{holes}'
            f'<div class="num">{n}/9</div>{body}<div class="fine">{fine}</div>' + ('<div class="swipe">swipe →</div>' if swipe else '') + '</div></body></html>')
def momo(pose, x, y, h=520, flip=False):
    return f'<img class="momo cut" src="file://{D}/momo_{pose}.png" style="left:{x}px;top:{y}px;height:{h}px;{"transform:scaleX(-1)" if flip else ""}">'
def stepnote(k, color, title, rot):
    return (f'<div class="a note" style="left:160px;top:120px;width:560px;height:250px;background:{color};transform:rotate({rot}deg)">'
            f'<div style="font:44px PM;color:#555">STEP {k}</div><div class="mk" style="font-size:84px;margin-top:10px">{title}</div></div>'
            f'<div class="tape" style="left:360px;top:100px;transform:rotate({-rot*1.5}deg)"></div>')
S = []
# 1 cover
S.append(page(1, f'''
<div class="a mk" style="left:160px;top:110px;font-size:92px;width:860px">₹1 lakh savings mein pada hai?</div>
<div class="a h" style="left:165px;top:360px;font-size:74px;width:820px">Saal ka interest: <span class="hl" style="color:#c2273a">sirf ~₹3,000</span></div>
<div class="a note" style="left:160px;top:560px;width:540px;height:400px;background:#9fe6a8;transform:rotate(-4deg)">
 <div class="mk" style="font-size:66px">Saving → Investing</div><div class="mk" style="font-size:130px;color:#1f3d8a;margin-top:8px">5 steps</div></div>
<div class="tape" style="left:330px;top:540px;transform:rotate(5deg)"></div>
{momo('shocked', 690, 640, 600)}'''))
# 2 maths
S.append(page(2, f'''
<div class="a mk" style="left:160px;top:100px;font-size:78px;width:860px">Same ₹1 lakh, 20 saal</div>
<div class="a cut" style="left:180px;top:300px;width:300px;height:760px">
 <div style="position:absolute;bottom:120px;left:40px;width:200px;height:110px;background:#9aa7b4"></div>
 <div class="mk" style="position:absolute;bottom:250px;left:0;width:280px;text-align:center;font-size:72px">₹1.8 L</div>
 <div class="h" style="position:absolute;bottom:20px;left:0;width:280px;text-align:center;font-size:52px;color:#333">Savings 3%</div></div>
<div class="a cut" style="left:520px;top:300px;width:300px;height:760px">
 <div style="position:absolute;bottom:120px;left:40px;width:200px;height:520px;background:#2fa65a"></div>
 <div class="mk" style="position:absolute;bottom:660px;left:0;width:280px;text-align:center;font-size:72px;color:#1d8a3a">₹9.6 L</div>
 <div class="h" style="position:absolute;bottom:20px;left:0;width:280px;text-align:center;font-size:52px;color:#333">Invest 12%*</div></div>
<div class="a h" style="left:160px;top:1110px;font-size:46px;color:#c2273a">Farak: ~₹8 lakh</div>
{momo('pointing', 830, 640, 460)}''', fine='*12% sirf example hai, guarantee nahi · Sirf jaankari ke liye'))
# 3 emergency
S.append(page(3, stepnote(1, '#ffe36e', 'Emergency fund', -3) + f'''
<div class="a h" style="left:170px;top:450px;font-size:70px;width:820px">Pehle <span class="hl">3–6 mahine</span> ka kharcha alag rakho.</div>
<div class="a h" style="left:170px;top:680px;font-size:54px;width:560px;color:#333">Job gayi? Hospital? Bike repair?<br>Isi paise se kaam chalega.</div>
<div class="a h" style="left:170px;top:950px;font-size:54px;width:520px;color:#c2273a">Log loss pe nahi, zaroorat pe bechte hain.</div>
{momo('thinking', 730, 720, 540)}'''))
# 4 buckets
S.append(page(4, stepnote(2, '#ffa9c6', 'Do bucket', 4) + f'''
<div class="a note" style="left:160px;top:470px;width:400px;height:420px;background:#cfe3f7;transform:rotate(-3deg)">
 <svg width="110" height="120" viewBox="0 0 160 190"><path d="M80 8 L150 34 V92 C150 140 118 170 80 184 C42 170 10 140 10 92 V34Z" fill="#3f6f98"/><path d="M45 96 L72 124 L120 70" stroke="#fff" stroke-width="16" fill="none" stroke-linecap="round"/></svg><div class="mk" style="font-size:58px">Suraksha</div><div class="h" style="font-size:46px;color:#333">ye paisa hilta nahi</div></div>
<div class="a note" style="left:600px;top:500px;width:400px;height:420px;background:#c9f2cf;transform:rotate(3deg)">
 <svg width="110" height="120" viewBox="0 0 120 130"><path d="M60 125 V55" stroke="#1d8a3a" stroke-width="10"/><path d="M60 70 C20 70 10 35 15 20 C45 20 60 40 60 70Z" fill="#2fa65a"/><path d="M60 60 C95 60 110 30 105 10 C75 10 60 30 60 60Z" fill="#3cb46a"/><rect x="25" y="110" width="70" height="20" rx="6" fill="#8a5a33"/></svg><div class="mk" style="font-size:58px">Badhne wala</div><div class="h" style="font-size:46px;color:#333">upar-neeche hoga, chalega</div></div>
<div class="a h" style="left:170px;top:1010px;font-size:60px;width:840px">Dimaag mein alag = <span class="hl">darr aadha</span></div>'''))
# 5 small SIP
S.append(page(5, stepnote(3, '#9fe6a8', 'Chhote se shuru', -4) + f'''
<div class="a h" style="left:170px;top:450px;font-size:70px;width:820px">Lakhon nahi chahiye.</div>
<div class="a mk" style="left:170px;top:570px;font-size:150px;color:#1f3d8a">₹500</div>
<div class="a h" style="left:175px;top:760px;font-size:58px;width:560px">se bhi SIP shuru ho jaati hai.</div>
<div class="a h" style="left:175px;top:960px;font-size:58px;width:560px;color:#c2273a">Pehle aadat, phir profit.</div>
{momo('happy', 720, 700, 560)}'''))
# 6 keep simple
S.append(page(6, stepnote(4, '#ffe36e', 'Simple rakho', 3) + f'''
<div class="a note" style="left:160px;top:470px;width:820px;height:230px;background:#ffd0cc;transform:rotate(-2deg)">
 <div class="mk" style="font-size:58px;color:#c2273a">✗ F&amp;O · Intraday · Crypto tips</div><div class="h" style="font-size:48px;color:#333;margin-top:14px">beginners sabse zyada yahin jalte hain</div></div>
<div class="a note" style="left:180px;top:760px;width:820px;height:250px;background:#c9f2cf;transform:rotate(2deg)">
 <div class="mk" style="font-size:58px;color:#1d8a3a">✓ Index fund</div><div class="h" style="font-size:48px;color:#333;margin-top:14px">ek saath top companies — kaunsa share jeetega, guess nahi karna</div></div>
<div class="a h" style="left:170px;top:1090px;font-size:56px">Boring hai… <span class="hl">par kaam karta hai.</span></div>'''))
# 7 SIP magic
S.append(page(7, stepnote(5, '#ffa9c6', 'SIP band mat karo', -3) + f'''
<div class="a h" style="left:170px;top:440px;font-size:62px;width:820px">₹5,000 har mahine × 20 saal (12%*)</div>
<div class="a mk" style="left:170px;top:560px;font-size:170px;color:#1d8a3a">≈ ₹50 L</div>
<div class="a cut" style="left:180px;top:800px;width:520px;height:100px;background:#9aa7b4"><div class="h" style="padding:18px 24px;font-size:52px;color:#fff">Aapne daala: ₹12 L</div></div>
<div class="a cut" style="left:180px;top:930px;width:520px;height:100px;background:#2fa65a"><div class="h" style="padding:18px 24px;font-size:52px;color:#fff">Compounding: ₹38 L</div></div>
{momo('pointing', 740, 720, 520)}''', fine='*12% sirf example hai, guarantee nahi · Sirf jaankari ke liye'))
# 8 crash
S.append(page(8, f'''
<div class="a mk" style="left:160px;top:100px;font-size:86px;width:860px">"Market crash ho gaya toh?"</div>
<svg class="a" style="left:160px;top:330px" width="860" height="440"><path d="M10 120 L180 90 L300 380 L470 330 L640 170 L840 70" stroke="#1f3d8a" stroke-width="12" fill="none" stroke-linejoin="round" stroke-linecap="round"/>
 <circle cx="300" cy="380" r="16" fill="#c2273a"/><circle cx="840" cy="70" r="16" fill="#1d8a3a"/></svg>
<div class="a h" style="left:300px;top:740px;font-size:52px;color:#c2273a">Mar 2020: Nifty ~40% gira</div>
<div class="a h" style="left:600px;top:300px;font-size:52px;color:#1d8a3a">Nov 2020: wapas high pe</div>
<div class="a h" style="left:170px;top:880px;font-size:58px;width:820px">SIP wale ko girte market mein <span class="hl">sasti units</span> milti hain.</div>
<div class="a mk" style="left:170px;top:1080px;font-size:58px">Saalon mein socho, dino mein nahi.</div>'''))
# 9 CTA
S.append(page(9, f'''
<div class="a note" style="left:160px;top:120px;width:400px;height:360px;background:#ffe36e;transform:rotate(-4deg)">
 <svg width="130" height="100" viewBox="0 0 560 430"><ellipse cx="280" cy="230" rx="215" ry="150" fill="#f4a3b5"/><ellipse cx="478" cy="235" rx="52" ry="44" fill="#ee8fa5"/><circle cx="395" cy="180" r="13" fill="#222"/><rect x="230" y="92" width="90" height="14" rx="7" fill="#a8495d"/><rect x="140" y="345" width="50" height="62" rx="12" fill="#ee8fa5"/><rect x="340" y="345" width="50" height="62" rx="12" fill="#ee8fa5"/></svg><div class="mk" style="font-size:66px">Gullak</div><div class="h" style="font-size:44px;color:#333">safe, par kuch ugta nahi</div></div>
<div class="a note" style="left:600px;top:150px;width:400px;height:360px;background:#9fe6a8;transform:rotate(3deg)">
 <svg width="110" height="110" viewBox="0 0 120 120"><rect x="52" y="70" width="16" height="45" fill="#8a5a33"/><circle cx="60" cy="50" r="38" fill="#2fa65a"/><circle cx="35" cy="62" r="22" fill="#3cb46a"/><circle cx="85" cy="62" r="22" fill="#3cb46a"/></svg><div class="mk" style="font-size:66px">Khet</div><div class="h" style="font-size:44px;color:#333">time do, ped banega</div></div>
<div class="a mk" style="left:170px;top:600px;font-size:84px;width:560px">Aap abhi kis stage pe ho?</div>
<div class="a h" style="left:175px;top:850px;font-size:54px;width:500px">Comment karo<br>Save karo<br>Us dost ko bhejo jo sirf FD karta hai</div>
{momo('happy', 720, 680, 580)}''', swipe=False, fine='Sirf jaankari ke liye, financial advice nahi.'))

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1350}, device_scale_factor=1)
        os.makedirs(f'{D}/out', exist_ok=True)
        for i, h in enumerate(S, 1):
            open(f'{D}/out/s{i}.html', 'w').write(h); await pg.goto(f'file://{D}/out/s{i}.html'); await pg.wait_for_timeout(500)
            await pg.screenshot(path=f'{D}/out/slide_{i}.png')
        await b.close()
asyncio.run(main())
from PIL import Image
ims = [Image.open(f'{D}/out/slide_{i}.png').convert('RGB') for i in range(1, 10)]
for i, im in enumerate(ims, 1): im.save(f'{D}/out/Slide_{i:02d}.jpg', quality=93)
W = Image.new('RGB', (360 * 5, 450 * 2), 'black')
for i, im in enumerate(ims): W.paste(im.resize((360, 450)), ((i % 5) * 360, (i // 5) * 450))
W.save('/tmp/claude-0/car.jpg', quality=85); print('ok')
