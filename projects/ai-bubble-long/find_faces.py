#!/usr/bin/env python3
"""Detect cartoon eye pairs in art/*.png -> art/faces_auto.json (B's helper for blink / mouth / brow rigs).
Style: dot eyes = dark oval blobs with light skin around them. Pairs: two blobs of similar size and height,
2-7 eye-widths apart. Mouth / brow positions are derived from the pair in the player.
Review the annotated sheets (--sheet DIR) and fix by hand in art/faces.json (that file wins)."""
import os, sys, json, glob
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
HERE = os.path.dirname(os.path.abspath(__file__))


def detect(path):
    im = Image.open(path).convert('RGB'); W, H = im.size
    a = np.asarray(im).astype(np.float32); Y = .299 * a[..., 0] + .587 * a[..., 1] + .114 * a[..., 2]
    sat = a.max(2) - a.min(2)
    dark = (Y < 60) & (sat < 60)
    lab, n = ndi.label(dark)
    objs = ndi.find_objects(lab)
    cands = []
    for i, sl in enumerate(objs, 1):
        h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
        if not (4 <= w <= 40 and 6 <= h <= 55): continue
        if not (.9 <= h / w <= 2.6): continue                       # tall-ish ovals
        m = lab[sl] == i; area = m.sum()
        if area < .55 * w * h: continue                              # solid
        cy = (sl[0].start + sl[0].stop) / 2; cx = (sl[1].start + sl[1].stop) / 2
        # ring around blob must be light skin
        r = max(w, h); y0, y1 = int(max(0, cy - r * 1.3)), int(min(H, cy + r * 1.3)); x0, x1 = int(max(0, cx - r * 1.3)), int(min(W, cx + r * 1.3))
        ring = Y[y0:y1, x0:x1].copy(); inner = lab[y0:y1, x0:x1] == i
        ring_vals = ring[~ndi.binary_dilation(inner, iterations=2)]
        if ring_vals.size == 0 or np.median(ring_vals) < 150: continue
        cands.append((cx, cy, w, h))
    faces = []; used = set()
    cands.sort(key=lambda c: c[0])
    for i, a_ in enumerate(cands):
        if i in used: continue
        best = None
        for j in range(i + 1, len(cands)):
            if j in used: continue
            b = cands[j]; dx = b[0] - a_[0]; dy = abs(b[1] - a_[1]); s = (a_[2] + b[2]) / 2
            if dx < 2 * s or dx > 7.5 * s: continue
            if dy > .6 * s + .15 * dx: continue
            if not (.6 < b[3] / a_[3] < 1.6): continue
            sc = dy + abs(b[3] - a_[3])
            if best is None or sc < best[0]: best = (sc, j)
        if best:
            b = cands[best[1]]; used |= {i, best[1]}
            faces.append({'eyes': [[round(a_[0] / W, 4), round(a_[1] / H, 4)], [round(b[0] / W, 4), round(b[1] / H, 4)]],
                          'eh': round((a_[3] + b[3]) / 2 / H, 4), 'ew': round((a_[2] + b[2]) / 2 / W, 4)})
    return faces


def main():
    out = {}; files = sorted(glob.glob(os.path.join(HERE, 'art', 's*.png')))
    for f in files:
        out[os.path.basename(f)[:-4]] = detect(f)
    json.dump(out, open(os.path.join(HERE, 'art', 'faces_auto.json'), 'w'), indent=0)
    print(sum(len(v) for v in out.values()), 'faces in', len(out), 'images')
    if len(sys.argv) > 2 and sys.argv[1] == '--sheet':
        d = sys.argv[2]; os.makedirs(d, exist_ok=True); tiles = []
        for k, faces in out.items():
            im = Image.open(os.path.join(HERE, 'art', k + '.png')).convert('RGB'); W, H = im.size; dr = ImageDraw.Draw(im)
            for n, fc in enumerate(faces):
                for (x, y) in fc['eyes']:
                    r = fc['eh'] * H * .9; dr.ellipse([x * W - r, y * H - r, x * W + r, y * H + r], outline=(0, 255, 0), width=3)
                (x0, y0), (x1, y1) = fc['eyes']; dr.text(((x0 + x1) / 2 * W - 4, min(y0, y1) * H - 30), str(n), fill=(255, 255, 0))
            dr.text((8, 8), k, fill=(0, 255, 255)); tiles.append(im.resize((672, 376)))
        for p in range(0, len(tiles), 12):
            sh = Image.new('RGB', (672 * 3, 376 * 4))
            for i, t in enumerate(tiles[p:p + 12]): sh.paste(t, ((i % 3) * 672, (i // 3) * 376))
            sh.save(os.path.join(d, 'faces_%02d.jpg' % (p // 12)), quality=82)


if __name__ == '__main__':
    main()
