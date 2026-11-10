"""Overlay Hinglish captions on the illustrated Momo slides (art/*.png, 4:5) -> out/<carousel>/Slide_XX.jpg (1080x1350)."""
import asyncio, os
from playwright.async_api import async_playwright
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__)); F = 'file://' + os.path.abspath(f'{D}/../../engine/fonts'); ART = f'file://{D}/art'
CSS = f"""@font-face{{font-family:P;font-weight:800;src:url({F}/poppins-latin-800-normal.woff2)}}
@font-face{{font-family:P;font-weight:500;src:url({F}/poppins-latin-500-normal.woff2)}}
@font-face{{font-family:A;src:url({F}/anton-latin-400-normal.woff2)}}
body{{margin:0;width:1080px;height:1350px;overflow:hidden;font-family:P;background:#000}}
img{{position:absolute;inset:0;width:1080px;height:1350px;object-fit:cover}}
.cap{{position:absolute;left:30px;right:30px;text-align:center;font:800 58px/1.12 P;color:#fff;text-shadow:0 4px 0 #000,0 0 22px rgba(0,0,0,.95),0 0 6px #000}}
.cap .y{{color:#ffd400}} .cap .g{{color:#3ee07a}} .cap .r{{color:#ff5c75}}
.sub{{display:block;font:500 34px/1.25 P;color:#f1f1f1;margin-top:6px}}
.band{{position:absolute;left:0;right:0;height:210px;background:linear-gradient(180deg,rgba(0,0,0,0),rgba(0,0,0,.72))}}
.title{{position:absolute;left:40px;right:40px;text-align:center;font:400 112px/1.0 A;color:#fff;text-shadow:0 7px 0 #000,0 0 30px rgba(0,0,0,.9)}}
.title .y{{color:#ffd400}} .title .g{{color:#3ee07a}}
.tag{{position:absolute;left:34px;top:30px;font:800 26px P;color:#111;background:#ffd400;padding:6px 16px;border-radius:10px}}
.num{{position:absolute;right:34px;top:30px;font:800 28px P;color:#fff;background:rgba(0,0,0,.55);padding:4px 14px;border-radius:10px}}
.fine{{position:absolute;left:0;right:0;bottom:12px;text-align:center;font:500 22px P;color:#ddd;text-shadow:0 2px 4px #000}}"""
def two(img, n, N, tag, top, bot, fine=''):
    return (f'<img src="{ART}/{img}.png"><div class="band" style="top:465px"></div><div class="band" style="top:1140px"></div>'
            f'<div class="tag">{tag}</div><div class="num">{n}/{N}</div>'
            f'<div class="cap" style="top:505px">{top}</div><div class="cap" style="top:1180px">{bot}</div><div class="fine">{fine}</div>')
def one(img, n, N, tag, title, sub, top=70, fine='', gap=250, fs=112):
    return (f'<img src="{ART}/{img}.png"><div style="position:absolute;left:0;right:0;top:0;height:560px;background:linear-gradient(180deg,rgba(0,0,0,.75),rgba(0,0,0,0))"></div>'
            f'<div class="tag">{tag}</div><div class="num">{n}/{N}</div><div class="title" style="top:{top}px;font-size:{fs}px">{title}</div>'
            f'<div class="cap" style="top:{top+gap}px;font-size:44px">{sub}</div><div class="fine">{fine}</div>')
F1 = 'Amounts sirf example hain · Sirf jaankari ke liye'
C1 = [
 one('c1_01', 1, 8, 'SAME PAISA', 'SAME PAISA,<br><span class="y">ALAG SOCH</span>', 'Kharcha karo ya future banao — <span class="y">choice aapki</span>', fine=F1),
 two('c1_02', 2, 8, 'SAME PAISA', 'Weekend Zomato: <span class="r">₹2,000</span>', 'SIP har mahine: <span class="g">₹2,000</span>', F1),
 two('c1_03', 3, 8, 'SAME TIME', 'Reels scrolling: <span class="r">2 ghante</span>', 'Nayi skill: <span class="g">2 ghante</span>', F1),
 two('c1_04', 4, 8, 'SAME PAISA', 'GTA 6: <span class="r">₹5,999</span>', 'Online course: <span class="g">₹5,999</span>', F1),
 two('c1_05', 5, 8, 'SAME PAISA', 'Roz chai-snacks: <span class="r">₹1,500/mahina</span>', 'Ek achhi kitaab: <span class="g">₹300, ek baar</span>', F1),
 two('c1_06', 6, 8, 'SAME PAISA', 'Naya phone, <span class="r">EMI pe</span>', '<span class="g">Emergency fund</span> pehle', F1),
 two('c1_07', 7, 8, 'SAME TIME', 'Motivation video: <span class="r">1 ghanta</span>', 'Asli kaam: <span class="g">1 ghanta</span>', F1),
 one('c1_08', 8, 8, 'SAVE KARO', 'KHARCHA KARO,<br><span class="g">PAR SOCH KE</span>', 'Mazaa bhi zaroori hai — bas <span class="y">pehle khud ko pay karo</span>.<br>Save karo · Share karo', fine=F1),
]
F2 = 'Kamai skill, time aur clients pe depend karti hai · Sirf jaankari ke liye'
C2 = [
 one('c2_01', 1, 7, 'SIDE HUSTLE', '<span class="y">10 SIDE HUSTLES</span><br>JO AAJ SHURU<br>HO SAKTE HAIN', 'Ek skill + ek laptop/phone = <span class="g">extra income ka raasta</span>', fine=F2, gap=330, fs=100),
 two('c2_02', 2, 7, '1–2', '1. Short video editing<span class="sub">Creators ko Reels/Shorts editor chahiye</span>', '2. Thumbnail design<span class="sub">Achha thumbnail = zyada clicks</span>', F2),
 two('c2_03', 3, 7, '3–4', '3. Online tutoring<span class="sub">Jo subject aata hai, wahi padhao</span>', '4. Freelance writing<span class="sub">Hindi/English blogs, scripts, captions</span>', F2),
 two('c2_04', 4, 7, '5–6', '5. Social media manager<span class="sub">Local shops ka Insta sambhalo</span>', '6. Website banana<span class="sub">Chhote business ki online dukaan</span>', F2),
 two('c2_05', 5, 7, '7–8', '7. Voiceover<span class="sub">Achhi awaaz + ek mic</span>', '8. Product photography<span class="sub">Online sellers ko saaf photos chahiye</span>', F2),
 two('c2_06', 6, 7, '9–10', '9. Excel &amp; reports<span class="sub">Data saaf karo, reports banao</span>', '10. Online reselling<span class="sub">Sasta kharido, sahi jagah becho</span>', F2),
 one('c2_07', 7, 7, 'SAVE KARO', 'EK CHUNO,<br><span class="g">AAJ SHURU KARO</span>', 'Pehle free mein 2–3 sample kaam banao, phir clients dhoondo.<br>Comment karo: aap kaunsa try karoge?', fine=F2),
]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1350})
        for name, S in [('Same_Paisa_Alag_Soch', C1), ('10_Side_Hustles', C2)]:
            od = f'{D}/out/{name}'; os.makedirs(od, exist_ok=True)
            for i, body in enumerate(S, 1):
                open(f'{od}/s{i}.html', 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>')
                await pg.goto(f'file://{od}/s{i}.html'); await pg.wait_for_timeout(500)
                await pg.screenshot(path=f'{od}/Slide_{i:02d}.jpg', type='jpeg', quality=93)
            n = len(S); W = Image.new('RGB', (216 * n, 270))
            for i in range(n): W.paste(Image.open(f'{od}/Slide_{i+1:02d}.jpg').resize((216, 270)), (216 * i, 0))
            W.save(f'/tmp/claude-0/ss/{name}.jpg', quality=82)
        await b.close()
asyncio.run(main()); print('ok')
