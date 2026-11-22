from playwright.sync_api import sync_playwright
import os
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':2560,'height':1440})
    pg.goto('file://'+os.path.abspath('banner.html'));pg.wait_for_timeout(800)
    pg.screenshot(path='banner.png');b.close()
from PIL import Image,ImageDraw
im=Image.open('banner.png').convert('RGB');im.save('banner.jpg',quality=92)
d=ImageDraw.Draw(im);d.rectangle([507,508,2053,931],outline=(255,0,0),width=4);im.resize((1280,720)).save('/tmp/claude-0/-home-claude/999831f8-532d-5a5d-b8a0-edc9695392d6/scratchpad/banner_check.png')
print(os.path.getsize('banner.jpg'))
