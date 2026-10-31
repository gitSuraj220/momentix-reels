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


def render(raw, out, top_text, bottom_text, top_y=560, bottom_y=1170):
    art = crop_to_slide(Path(raw))
    buf = io.BytesIO(); art.save(buf, "PNG")
    bg = base64.b64encode(buf.getvalue()).decode()
    font = base64.b64encode(FONT.read_bytes()).decode()
    html = f"""<html><head><style>
@font-face {{ font-family: P; src: url(data:font/woff2;base64,{font}); font-weight: 800; }}
html,body {{ margin:0; width:{W}px; height:{H}px; overflow:hidden; }}
body {{ background:url(data:image/png;base64,{bg}) 0 0/{W}px {H}px no-repeat; position:relative; }}
.t {{ position:absolute; left:70px; right:70px; transform:translateY(-50%); text-align:center;
      font-family:P; font-weight:800; color:#fff; font-size:64px; line-height:1.18; letter-spacing:-0.5px;
      text-shadow: 0 3px 0 rgba(0,0,0,.35), 0 0 22px rgba(0,0,0,.55), 0 0 6px rgba(0,0,0,.6); }}
</style></head><body>
<div class="t" style="top:{top_y}px">{top_text}</div>
<div class="t" style="top:{bottom_y}px">{bottom_text}</div>
</body></html>"""
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        pg.set_content(html); pg.wait_for_timeout(300)
        pg.screenshot(path=out, type="png")
        b.close()


if __name__ == "__main__":
    a = sys.argv[1:]
    render(a[0], a[1], a[2], a[3], *(int(x) for x in a[4:6]))
