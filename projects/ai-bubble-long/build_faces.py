#!/usr/bin/env python3
"""art/faces_auto.json (find_faces.py) + hand-marked speaking faces -> art/faces.json and player/faces.js,
plus player/vo_env.js (voice loudness envelope, 100 Hz) for mouth movement.
faces.json: {src: [{eyes:[[x,y],[x,y]], eh, ew, mouth:[x,y,w] | None, skin:[r,g,b], blink:bool}]}  (0-1 image coords)
SPEAK: shot id -> (src, face index) whose mouth moves with the voice in that shot.
REACT: per-shot extras (brow jump, sweat drop)."""
import os, json, subprocess
import numpy as np
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__))
auto = json.load(open(f'{D}/art/faces_auto.json'))

# hand-marked (from 5% grid sheets): eyes, mouth centre + width; blink False where eyes are drawn closed/squinting
MAN = {
 's014': [dict(eyes=[[.1851, .4249], [.2257, .4249]], mouth=[.2036, .467, .047], exact=1),
          dict(eyes=[[.8036, .3364], [.8359, .3444]], mouth=[.8197, .39, .028], exact=1)],
 's022': [dict(eyes=[[.5005, .308], [.546, .305]], mouth=[.523, .365, .058], exact=1)],
 's024': [dict(eyes=[[.5929, .447], [.6614, .4633]], mouth=[.614, .553, .053], exact=1)],
 's038': [dict(eyes=[[.2135, .383], [.2325, .375]], mouth=[.222, .425, .02])],
 's040': [dict(eyes=[[.465, .150], [.506, .150]], mouth=[.491, .247, .082], blink=False, exact=1)],
 's042': [dict(eyes=[[.281, .345], [.294, .345]], mouth=[.287, .378, .012], blink=False)],
 's043': [dict(eyes=[[.4074, .3466], [.4707, .3067]], mouth=[.4483, .4032, .05], blink=False, exact=1)],
 's045': [dict(eyes=[[.436, .2779], [.4714, .2633]], mouth=[.446, .378, .045])],
 's091': [dict(eyes=[[.1769, .427], [.2217, .4157]], mouth=[.2006, .4957, .04], exact=1),
          dict(eyes=[[.5054, .319], [.5476, .319]], exact=1)],
 's092': [dict(eyes=[[.3508, .3285], [.3787, .3152]], mouth=[.37, .40, .03])],
 's097': [dict(eyes=[[.3206, .34], [.3917, .34]], mouth=[.368, .458, .1], blink=False, exact=1)],
 's098': [dict(eyes=[[.1525, .3737], [.2341, .3644]], mouth=[.2025, .4689, .05], exact=1)],
 's099': [dict(eyes=[[.45, .297], [.533, .292]], mouth=[.4915, .4495, .09], blink=False, exact=1)],
 's117': [dict(eyes=[[.0949, .5698], [.1153, .5605]]),
          dict(eyes=[[.3214, .4275], [.3553, .4215]], mouth=[.342, .458, .035])],
}
SPEAK = {14: ('s014', 0), 15: ('s014', 1), 22: ('s022', 0), 23: ('s022', 0), 24: ('s024', 0), 25: ('s022', 0),
         38: ('s038', 0), 39: ('s038', 0), 40: ('s040', 0), 42: ('s042', 0), 43: ('s043', 0), 45: ('s045', 0),
         91: ('s091', 0), 92: ('s092', 0), 97: ('s097', 0), 98: ('s098', 0), 99: ('s099', 0), 117: ('s117', 1)}
REACT = {15: {'brow': [.15]}, 45: {'brow': [.1]}, 24: {'sweat': 1}, 113: {'sweat': 1}, 82: {'sweat': 1}, 49: {'sweat': 1}}


from scipy import ndimage as ndi


def snap_eyes(im, fc):
    # find the best dark eye-blob PAIR within +-10% of the rough hand mark; keeps mouth offset to the eyes
    W, H = im.size; a = np.asarray(im).astype(np.float32); Y = .299 * a[..., 0] + .587 * a[..., 1] + .114 * a[..., 2]
    mx = (fc['eyes'][0][0] + fc['eyes'][1][0]) / 2; my = (fc['eyes'][0][1] + fc['eyes'][1][1]) / 2
    x0, x1 = int(max(0, (mx - .1) * W)), int(min(W, (mx + .1) * W)); y0, y1 = int(max(0, (my - .12) * H)), int(min(H, (my + .14) * H))
    lab, n = ndi.label(Y[y0:y1, x0:x1] < 62); c = []
    for i, sl in enumerate(ndi.find_objects(lab), 1):
        h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
        if not (7 <= h <= 70 and 4 <= w <= 50 and .85 <= h / w <= 2.9): continue
        if (lab[sl] == i).sum() < .5 * w * h: continue
        c.append((x0 + (sl[1].start + sl[1].stop) / 2, y0 + (sl[0].start + sl[0].stop) / 2, w, h))
    best = None; hdx = abs(fc['eyes'][1][0] - fc['eyes'][0][0]) * W
    for i, p in enumerate(c):
        for q in c[i + 1:]:
            L_, R = (p, q) if p[0] < q[0] else (q, p); dx = R[0] - L_[0]; s_ = (p[3] + q[3]) / 2
            if not (1.6 * s_ * .5 <= dx <= 6 * s_ and abs(p[1] - q[1]) < .45 * s_ + .12 * dx and .65 < p[3] / q[3] < 1.5): continue
            mid = ((L_[0] + R[0]) / 2 / W, (L_[1] + R[1]) / 2 / H)
            cost = ((mid[0] - mx) / .05) ** 2 + ((mid[1] - my) / .07) ** 2 + abs(p[3] - q[3]) / s_ + .3 * abs(dx - hdx) / max(hdx, 1)
            if best is None or cost < best[0]: best = (cost, L_, R)
    if not best: return False
    _, L_, R = best
    ox = (L_[0] + R[0]) / 2 / W - mx; oy = (L_[1] + R[1]) / 2 / H - my
    fc['eyes'] = [[round(L_[0] / W, 4), round(L_[1] / H, 4)], [round(R[0] / W, 4), round(R[1] / H, 4)]]
    fc['eh'] = round((L_[3] + R[3]) / 2 / H, 4); fc['ew'] = round((L_[2] + R[2]) / 2 / W, 4)
    if fc.get('mouth'): fc['mouth'] = [round(fc['mouth'][0] + ox, 4), round(fc['mouth'][1] + oy, 4), fc['mouth'][2]]
    return True


def skin(im, fc):
    # most skin-like light sample among cheeks / between the eyes / forehead
    W, H = im.size; a = np.asarray(im).astype(np.float32)
    (x0, y0), (x1, y1) = fc['eyes']; xm, ym = (x0 + x1) / 2, (y0 + y1) / 2; eh = fc['eh']; dx = x1 - x0
    pts = [(xm, ym), (x0, ym + eh * 1.4), (x1, ym + eh * 1.4), (xm, ym - eh * 1.6), (x0 - dx * .3, ym + eh * .6), (x1 + dx * .3, ym + eh * .6)]
    cs = []
    for x, y in pts:
        X, Yp = int(min(W - 2, max(1, x * W))), int(min(H - 2, max(1, y * H)))
        c = np.median(a[Yp - 1:Yp + 2, X - 1:X + 2].reshape(-1, 3), 0); lum = .299 * c[0] + .587 * c[1] + .114 * c[2]
        cs.append((lum - .5 * (c.max() - c.min()) * 0, c))
    c = max(cs, key=lambda z: z[0])[1]
    return [int(v) for v in c]


def main():
    out = {}
    for f in sorted(set(auto) | set(MAN)):
        im = Image.open(f'{D}/art/{f}.png').convert('RGB')
        faces = [dict(fc, _man=1) for fc in MAN.get(f, [])]
        for fc in auto.get(f, []):          # add auto faces not already hand-marked
            if not any(abs(fc['eyes'][0][0] - m['eyes'][0][0]) < .02 and abs(fc['eyes'][0][1] - m['eyes'][0][1]) < .02 for m in faces):
                faces.append(dict(eyes=fc['eyes'], eh=fc['eh'], ew=fc['ew']))
        for fc in faces:
            dx = abs(fc['eyes'][1][0] - fc['eyes'][0][0]); W, H = im.size
            fc.setdefault('eh', round(dx * W / H * .55, 4)); fc.setdefault('ew', round(dx * .3, 4))
            fc.setdefault('blink', True); fc.setdefault('mouth', None)
            if fc.get('_man') and not fc.get('exact') and not snap_eyes(im, fc): print('  keep hand eyes', f, fc['eyes'])
            fc.pop('_man', None); fc.pop('exact', None)
            fc['skin'] = skin(im, fc)
        if faces: out[f] = faces
    json.dump(out, open(f'{D}/art/faces.json', 'w'), indent=0)
    with open(f'{D}/player/faces.js', 'w') as fh:
        fh.write('window.FACES=' + json.dumps(out) + ';\nwindow.SPEAK=' + json.dumps({str(k): v for k, v in SPEAK.items()}) +
                 ';\nwindow.REACT=' + json.dumps({str(k): v for k, v in REACT.items()}) + ';\n')
    # voice envelope 100 Hz (0..1, sqrt-compressed)
    src = f'{D}/vo/vo_full.wav' if os.path.exists(f'{D}/vo/vo_full.wav') else f'{D}/vo/vo_full.mp3'
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], capture_output=True).stdout
    x = np.frombuffer(raw, np.float32); hop = 160; n = len(x) // hop
    e = np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)); e = np.sqrt(e / (np.percentile(e, 98) + 1e-9)); e = np.clip(e, 0, 1)
    with open(f'{D}/player/vo_env.js', 'w') as fh:
        fh.write('window.VOENV="' + ''.join(chr(48 + int(v * 60)) for v in e) + '";\n')   # 1 char / 10 ms
    print(sum(len(v) for v in out.values()), 'faces in', len(out), 'images;', len(SPEAK), 'speaking shots; env', n, 'frames')


if __name__ == '__main__':
    main()
