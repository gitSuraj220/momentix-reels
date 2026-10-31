"""Compose carousel slides: ChatGPT raw art (two stacked panels) + code-set text.

Usage: python3 compose.py raw.png out.png "Top line," "Bottom line." [top_y] [bottom_y]
top_y / bottom_y are the vertical centres of the two text blocks (px in the 1080x1350 slide).
"""
import base64, io, sys
from pathlib import Path

import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

W, H = 1080, 1350
ROOT = Path(__file__).resolve().parents[2]
FONT = ROOT / "engine/fonts/poppins-latin-800-normal.woff2"


def crop_to_slide(raw: Path) -> Image.Image:
    im = Image.open(raw).convert("RGB")
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    rows = np.asarray(im).mean(axis=(1, 2))
    mid = im.height // 2
    div = min(range(mid - 90, mid + 90), key=lambda y: rows[y])  # darkest row = panel divider
    top = min(max(div - H // 2, 0), im.height - H)
    return im.crop((0, top, W, top + H))


def render(raw, out, top_text, bottom_text, top_y=560, bottom_y=1170, style="scrim"):
    art = crop_to_slide(Path(raw))
    buf = io.BytesIO(); art.save(buf, "PNG")
    bg = base64.b64encode(buf.getvalue()).decode()
    font = base64.b64encode(FONT.read_bytes()).decode()
    html = f"""<html><head><style>
@font-face {{ font-family: P; src: url(data:font/woff2;base64,{font}); font-weight: 800; }}
html,body {{ margin:0; width:{W}px; height:{H}px; overflow:hidden; }}
body {{ background:url(data:image/png;base64,{bg}) 0 0/{W}px {H}px no-repeat; position:relative; }}
.t {{ position:absolute; left:60px; right:60px; transform:translateY(-50%); text-align:center;
      font-family:P; font-weight:800; font-size:64px; line-height:1.18; letter-spacing:-0.5px; }}
.scrim .t {{ color:#fff; -webkit-text-stroke:3px rgba(20,10,0,.85); paint-order:stroke fill;
      text-shadow:0 4px 14px rgba(0,0,0,.6); }}
.scrim .band {{ position:absolute; left:0; right:0; height:300px; transform:translateY(-50%);
      background:linear-gradient(to bottom, rgba(15,8,2,0) 0%, rgba(15,8,2,.62) 30%, rgba(15,8,2,.62) 70%, rgba(15,8,2,0) 100%); }}
.pill .t {{ color:#1a1530; }}
.pill .t span {{ background:#FFF4DC; padding:4px 22px; border-radius:14px; box-decoration-break:clone; -webkit-box-decoration-break:clone;
      box-shadow:0 6px 18px rgba(0,0,0,.35); line-height:1.5; }}
</style></head><body class="{style}">
<div class="band" style="top:{top_y}px"></div><div class="band" style="top:{bottom_y}px"></div>
<div class="t" style="top:{top_y}px"><span>{top_text}</span></div>
<div class="t" style="top:{bottom_y}px"><span>{bottom_text}</span></div>
</body></html>"""
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        pg.set_content(html); pg.wait_for_timeout(300)
        pg.screenshot(path=out, type="png")
        b.close()


if __name__ == "__main__":
    a = sys.argv[1:]
    nums=[int(x) for x in a[4:6]]; style=a[6] if len(a)>6 else "scrim"
    render(a[0], a[1], a[2], a[3], *nums, style=style)
