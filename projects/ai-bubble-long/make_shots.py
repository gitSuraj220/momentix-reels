#!/usr/bin/env python3
"""shots_doc.json + timeline.json + art/index.json -> shots.json + player/shots.js

B (animator). Rerun whenever A adds art or the VO changes:
    python3 make_shots.py
Timing: each doc shot's VO (speaker labels stripped) is matched word-by-word
against the timeline text; word times come from char share inside each VO
segment, then shot starts snap to the nearest real pause in vo/silences.tsv.
No-VO shots: #4 takes the first part of #5, #11 the tail of #10, #167 = 20 s
end screen after the VO.
Art: HF shots use art/index.json (else art/sNNN.png if present); missing art
-> `pending: true` (player draws a labelled placeholder card).
"""
import json, os, re, bisect

HERE = os.path.dirname(os.path.abspath(__file__))
J = lambda f: json.load(open(os.path.join(HERE, f)))
DOC, TL, IDX = J('shots_doc.json'), J('timeline.json'), J('art/index.json')
END_SCREEN = 20.0
SIL = []
if os.path.exists(os.path.join(HERE, 'vo/silences.tsv')):
    for ln in open(os.path.join(HERE, 'vo/silences.tsv')):
        a, b = ln.split()
        SIL.append((float(a), float(b)))

# ---------------------------------------------------------------- spec ----
# id -> (tpl, params). HF shots default to ('image', {}). 'ov' = code overlays
# drawn on top of HF art; rect = [x,y,w,h] in 0-1 of the image.
SIGN21 = [.405, .146, .295, .14]
SCR31 = [.283, .155, .627, .615]
PLQ37 = [.77, .28, .065, .055]
SCR38 = [.285, .107, .475, .493]
S = {
 1: ('image', {'kb': 'in', 'ov': [{'k': 'stamp', 'text': 'LOSS', 'at': .7, 'x': .78, 'y': .3, 'small': 1}]}),
 2: ('map', {'mode': 'world', 'logo': 'ChatGPT'}),
 3: ('map', {'mode': 'world', 'logo': 'ChatGPT', 'freeze': 1, 'stamp': 'LOSS'}),
 4: ('windows', {'srcs': ['s004a', 's004b', 's004c'], 'labels': ['USA', 'EUROPE', 'INDIA']}),
 5: ('title', {'text': 'AI ERA', 'style': 'neon', 'sub': 'WELCOME TO THE'}),
 6: ('balloon', {'mode': 'inflate', 'counter': {'prefix': '$', 'to': 7e12}, 'label': 'KA GAMBLE'}),
 7: ('calendar', {'wd': 'WED', 'day': 30, 'month': 'NOV', 'year': 2022}),
 8: ('image', {'kb': 'r'}),
 9: ('image', {'cuts': [[0, .05, .36, .8], [.3, .1, .4, .75], [.62, .05, .38, .8]]}),
 10: ('launch', {'logo': 'OpenAI', 'title': 'ChatGPT', 'type': 'Today we launched ChatGPT.', 'time': '8:38 PM'}),
 11: ('tweet', {'name': 'Sam Altman', 'handle': '@sama', 'text': 'today we launched ChatGPT. try talking with it here: chat.openai.com', 'time': '30 Nov 2022'}),
 12: ('notif', {'clock': '24 HRS', 'app': 'ChatGPT'}),
 13: ('image', {'cuts': [[0, 0, .34, 1], [.33, 0, .34, 1], [.66, 0, .34, 1]]}),
 14: ('image', {'kb': 'in'}),
 15: ('image', {'crop': [.48, .08, .52, .62], 'kb': 'in'}),
 16: ('chat', {'app': 'ChatGPT', 'type': 'Mujhe 1 minute mein 100 crore ka business bana ke do. Profit 100% ho. Aur koi galti nahi honi chahiye.', 'think': 1, 'kw': 'FACEPALM'}),
 17: ('counter', {'to': 1000000, 'indian': 1, 'suffix': ' USERS', 'tag': '5 DAYS'}),
 18: ('counter', {'from': 1000000, 'to': 100000000, 'indian': 1, 'suffix': ' USERS', 'tag': '2 MONTHS'}),
 19: ('race', {'title': '10 CRORE USERS TAK', 'items': [['Instagram', 30, '2.5 YRS'], ['Facebook', 54, '4.5 YRS']]}),
 20: ('race', {'title': '10 CRORE USERS TAK', 'items': [['Instagram', 30, '2.5 YRS'], ['Facebook', 54, '4.5 YRS'], ['ChatGPT', 2, '2 MONTHS']], 'win': 'FASTEST EVER'}),
 21: ('image', {'kb': 'up', 'ov': [{'k': 'logo', 'name': 'Google', 'rect': SIGN21}, {'k': 'alarm'}]}),
 22: ('image', {'kb': 'in', 'shake': .25}),
 23: ('image', {'crop': [.3, 0, .5, .62], 'kb': 'in', 'ov': [{'k': 'phone', 'logo': 'ChatGPT', 'x': .3, 'y': .5}]}),
 24: ('image', {'kb': 'r'}),
 25: ('image', {'kb': 'out', 'ov': [{'k': 'namecards', 'items': ['Bard', 'Gemini']}]}),
 26: ('image', {'kb': 'l', 'speed': 1, 'ov': [{'k': 'speedlines'}]}),
 27: ('image', {'kb': 'in'}),
 28: ('cards', {'style': 'bubbles', 'items': [['speech', '???'], ['gavel', 'CASE'], ['paper', 'MEDIA']]}),
 29: ('image', {'kb': 'in', 'ov': [{'k': 'confetti'}]}),
 30: ('money', {'from': 'Microsoft', 'to': 'OpenAI', 'bags': ['$10B', '$3B']}),
 31: ('image', {'kb': 'in', 'ov': [{'k': 'logo', 'name': 'Bard', 'rect': SCR31}]}),
 32: ('chat', {'app': 'Gemini', 'msgs': [['me', 'Gemini, ye batao duniya ka sabse popular insaan kaun hai?']]}),
 33: ('chat', {'app': 'Gemini', 'msgs': [['me', 'Gemini, ye batao duniya ka sabse popular insaan kaun hai?'], ['bot', 'Modi Ji.']], 'old': 1}),
 34: ('chat', {'app': 'Gemini', 'msgs': [['me', 'Modi Ji kaun?'], ['bot', 'Modi sarkaar.']], 'blank': 1}),
 35: ('image', {'kb': 'in', 'shake': .3}),
 36: ('money', {'from': 'Amazon', 'to': 'Anthropic', 'bags': ['$$$ BILLIONS'], 'mode': 'vault'}),
 37: ('image', {'kb': 'in', 'ov': [{'k': 'plaque', 'text': 'VC — We fund AI', 'rect': PLQ37}]}),
 38: ('image', {'kb': 'r', 'ov': [{'k': 'slide', 'mode': 'dogwalk', 'rect': SCR38}]}),
 39: ('image', {'crop': [.12, .02, .75, .75], 'kb': 'in', 'ov': [{'k': 'slide', 'mode': 'mlmap', 'rect': SCR38}]}),
 40: ('image', {'kb': 'in', 'shake': .15, 'ov': [{'k': 'tag', 'text': '$5 CRORE', 'x': .2, 'y': .7}]}),
 41: ('image', {'crop': [.5, .15, .5, .7], 'kb': 'r', 'flip': 1}),
 42: ('image', {'kb': 'in', 'ov': [{'k': 'tag', 'text': '2023', 'x': .08, 'y': .12}]}),
 43: ('image', {'kb': 'out'}),
 44: ('title', {'text': 'AI', 'style': 'sparkle'}),
 45: ('image', {'kb': 'in', 'shake': .3}),
 46: ('reveal', {'text': '$100M', 'label': 'YE LO'}),
 47: ('image', {'kb': 'in', 'ov': [{'k': 'tag', 'text': '$30M', 'x': .7, 'y': .25}]}),
 48: ('image', {'kb': 'l'}),
 50: ('image', {'kb': 'in', 'ov': [{'k': 'tag', 'text': 'GPU > SONA > TEL', 'x': .5, 'y': .12}]}),
 51: ('podium', {'logo': 'NVIDIA'}),
 53: ('image', {'kb': 'out', 'ov': [{'k': 'tag', 'text': '#1', 'x': .8, 'y': .2}]}),
 54: ('gpu', {'n': 1, 'tag': '$3 / hr'}),
 55: ('gpu', {'n': 1, 'tag': '$3 / hr', 'wiggle': 1, 'kw': 'SASTA?'}),
 56: ('gpu', {'n0': 1, 'n': 48}),
 57: ('gpu', {'n0': 48, 'n': 500, 'tag': 'x500'}),
 58: ('counter', {'prefix': '$', 'to': 1500, 'suffix': ' / hr', 'style': 'bill', 'tag': 'GPU RENT'}),
 59: ('counter', {'prefix': '$', 'from': 1500, 'to': 36000, 'suffix': ' / day', 'style': 'bill', 'tag': 'GPU RENT'}),
 60: ('counter', {'prefix': '$', 'from': 36000, 'to': 1100000, 'suffix': '+ / month', 'style': 'bill', 'tag': 'SIRF GPU KIRAYA', 'slam': 1}),
 63: ('counter', {'to': 12, 'suffix': ' MONTHS', 'style': 'token', 'tag': 'YOUR WAIT'}),
 66: ('stickers', {'year': '2024', 'text': 'AI-POWERED'}),
 67: ('image', {'kb': 'in', 'ov': [{'k': 'tag', 'text': '+10% EFFICIENCY', 'x': .7, 'y': .2}]}),
 68: ('calendar', {'mode': 'app', 'text': 'AI suggests: 3:00 AM meeting'}),
 70: ('image', {'kb': 'in', 'ov': [{'k': 'tag', 'text': 'MACHINE LEARNING', 'x': .5, 'y': .2}]}),
 72: ('image', {'kb': 'in', 'ov': [{'k': 'confetti', 'cheques': 1}]}),
 73: ('image', {'freeze': .35, 'sfx': ['scratch']}),
 74: ('image', {'kb': 'in', 'ov': [{'k': 'spot'}]}),
 75: ('calendar', {'month': 'JAN', 'year': 2025}),
 76: ('tweet', {'name': 'Sam Altman', 'handle': '@sama', 'text': 'OpenAI ke Pro subscription pe humein loss ho raha hai.', 'meter': 'BP'}),
 77: ('tweet', {'name': 'Sam Altman', 'handle': '@sama', 'text': 'OpenAI ke Pro subscription pe humein loss ho raha hai. Log ise humari expectation se kahin zyada use kar rahe hain.', 'hl': 1}),
 78: ('title', {'text': 'YES, REALLY.', 'style': 'shake'}),
 79: ('counter', {'prefix': '$', 'to': 200, 'suffix': ' / month', 'style': 'price', 'tag': 'PRO PLAN', 'sub': '− LOSS PER USER'}),
 80: ('title', {'text': 'PAR RUKO...', 'style': 'tilt', 'sfx': ['dundun']}),
 81: ('bars', {'mode': 'updown', 'title': 'OpenAI 2024', 'items': [['REVENUE', 3.7, '$3.7B'], ['LOSS', -5, '$5B']]}),
 83: ('title', {'text': 'ASLI SHOCK', 'style': 'curtain'}),
 84: ('counter', {'prefix': '$', 'to': 6.7, 'dec': 1, 'suffix': ' TRILLION', 'tag': 'BY 2030', 'city': 1}),
 85: ('split', {'mode': 'block', 'total': '$6.7T', 'a': ['$5.2T', 'AI INFRA', ['gpu', 'chip', 'bolt', 'snow', 'building']], 'b': ['$1.5T', 'CLOUD', ['cloud']], 'hl': 'a'}),
 86: ('split', {'mode': 'block', 'total': '$6.7T', 'a': ['$5.2T', 'AI INFRA', ['gpu', 'chip', 'bolt', 'snow', 'building']], 'b': ['$1.5T', 'CLOUD', ['cloud']], 'hl': 'b', 'old': 1}),
 87: ('logos', {'items': ['Microsoft', 'Google', 'Amazon', 'Meta'], 'center': '$350B', 'sub': 'IN 2025'}),
 88: ('bars', {'mode': 'target', 'items': [['NEEDED / YEAR', 2000, '$2T']]}),
 89: ('bars', {'mode': 'target', 'items': [['NEEDED / YEAR', 2000, '$2T'], ['TODAY', 200, '$200B']], 'old': 1}),
 90: ('bars', {'mode': 'target', 'items': [['NEEDED / YEAR', 2000, '$2T'], ['TODAY', 200, '$200B']], 'old': 2, 'arrow': '10x'}),
 92: ('image', {'kb': 'in', 'ov': [{'k': 'drawline'}]}),
 93: ('hockey', {'mode': 'morph'}),
 94: ('counter', {'prefix': '$', 'to': 115, 'suffix': 'B', 'tag': 'CASH BURN TILL 2029', 'fire': 1}),
 95: ('calendar', {'mode': 'fast', 'years': [2029, 2030, 2031]}),
 96: ('hockey', {'mode': 'snap', 'sfx': ['crack']}),
 100: ('funnel', {'from': '2021', 'to': 'AI'}),
 101: ('funnel', {'from': '2021', 'to': 'AI', 'balloons': 10, 'label': '+$1 TRILLION'}),
 103: ('title', {'text': 'GADBADIYAN', 'style': 'crack'}),
 106: ('paper', {'mode': 'dust', 'title': 'Study, 2031'}),
 109: ('chat', {'app': 'Search', 'msgs': [['me', 'cheese not sticking to pizza'], ['bot', 'Add 1/8 cup of non-toxic glue to the sauce.']]}),
 110: ('chat', {'app': 'Forum', 'msgs': [['bot', 'lol just use glue']], 'upvote': 1}),
 111: ('image', {'kb': 'in', 'shake': .2, 'sfx': ['gavel']}),
 113: ('image', {'kb': 'in', 'ov': [{'k': 'bubble', 'text': 'umm... haan.', 'x': .55, 'y': .25}]}),
 114: ('split', {'mode': 'lawsuit', 'pairs': [['The New York Times', 'OpenAI'], ['Getty Images', 'Stability AI']]}),
 119: ('balloon', {'mode': 'crack', 'sfx': ['hiss']}),
 120: ('split', {'mode': 'megaphone'}),
 121: ('image', {'kb': 'in', 'ov': [{'k': 'mosquito'}], 'sfx': ['buzz']}),
 122: ('title', {'text': 'Ye bubble phootega kab?', 'style': 'black'}),
 123: ('meter', {'mode': 'valuation'}),
 124: ('balloon', {'mode': 'hold', 'browser': 1, 'kw': 'KYUN?'}),
 127: ('image', {'kb': 'up', 'ov': [{'k': 'logorow', 'items': ['Microsoft', 'Google', 'Amazon', 'Meta']}]}),
 129: ('logos', {'items': ['Microsoft'], 'mode': 'rain', 'sub': 'AZURE CLOUD'}),
 130: ('logos', {'items': ['Google'], 'mode': 'coins', 'sub': 'ADS'}),
 132: ('meter', {'mode': 'profit'}),
 134: ('cards', {'style': 'morph', 'items': [['phone', 'iPhone moment?'], ['search', 'Google moment?'], ['chip', 'AI moment?']]}),
 136: ('image', {'kb': 'in', 'ov': [{'k': 'tag', 'text': 'BlackBerry', 'x': .3, 'y': .15}]}),
 137: ('image', {'kb': 'in', 'ov': [{'k': 'logorow', 'items': ['Google', 'Microsoft', 'Meta', 'Amazon']}]}),
 138: ('image', {'ov': [{'k': 'spotmove', 'n': 4}]}),
 140: ('balloon', {'mode': 'hold', 'needle': 1}),
 142: ('cards', {'style': 'fan', 'items': [['1', 'PAISA BAND'], ['2', 'BADA FAIL']]}),
 143: ('cards', {'style': 'flip', 'items': [['1', 'PAISA BAND'], ['2', 'BADA FAIL']], 'flip': 0}),
 144: ('paper', {'mode': 'site', 'title': 'www.startup1999.com'}),
 146: ('cards', {'style': 'icons', 'items': [['rate', 'INTEREST RATES ↑'], ['tag', 'LOAN MEHENGA'], ['bag', 'FUNDING GAYAB']]}),
 147: ('grid', {'mode': 'signs'}),
 148: ('image', {'kb': 'in', 'ov': [{'k': 'tag', 'text': 'GAME OVER', 'x': .5, 'y': .5, 'at': .65, 'red': 1}]}),
 149: ('cards', {'style': 'flip', 'items': [['1', 'PAISA BAND'], ['2', 'BADA FAIL']], 'flip': 1}),
 151: ('paper', {'mode': 'earnings', 'title': 'Q4 1999 RESULTS'}),
 155: ('map', {'mode': 'timeline'}),
 157: ('meter', {'mode': 'seismo'}),
 158: ('balloon', {'mode': 'crack', 'thin': 1}),
 159: ('balloon', {'mode': 'notch'}),
 160: ('balloon', {'mode': 'hold', 'megaphones': 1}),
 163: ('balloon', {'mode': 'tighten'}),
 166: ('title', {'text': 'NEXT: SEASON FINALE', 'style': 'tv'}),
 167: ('endscreen', {}),
}
HEADS137 = {'k': 'headlogo', 'heads': [[.09, .39, .052, 'Google'], [.375, .375, .052, 'Microsoft'], [.68, .385, .052, 'Meta'], [.915, .4, .048, 'Amazon']]}
S.update({
 49: ('image', {'kb': 'in', 'ov': [{'k': 'plaque', 'text': 'GPU — SOLD OUT', 'rect': [.53, .13, .245, .1], 'col': '#8b1a1a', 'chip': 0}]}),
 52: ('image', {'kb': 'in', 'ov': [{'k': 'tag', 'text': 'NVIDIA CEO', 'x': .66, 'y': .2}]}),
 70: ('image', {'kb': 'in', 'ov': [{'k': 'plaque', 'text': 'MACHINE LEARNING', 'rect': [.305, .075, .065, .09], 'col': '#1d4ed8', 'chip': 0}, {'k': 'tag', 'text': 'MACHINE LEARNING', 'x': .55, 'y': .14, 'at': .45}]}),
 117: ('image', {'kb': 'r', 'ov': [{'k': 'plaque', 'text': 'THE INTERNET', 'rect': [.69, .24, .21, .12], 'col': '#1a1a1a', 'chip': 0}]}),
 126: ('image', {'kb': 'in', 'ov': [{'k': 'plaque', 'text': 'REVENUE: $0', 'rect': [.71, .06, .24, .28], 'col': '#b91c1c', 'chip': 0}, {'k': 'tag', 'text': '1999', 'x': .1, 'y': .12}, {'k': 'tag', 'text': '17 FOOSBALL TABLES', 'x': .35, 'y': .9, 'at': .55}]}),
 136: ('image', {'kb': 'in', 'ov': [{'k': 'plaque', 'text': 'BlackBerry', 'rect': [.40, .065, .37, .11], 'col': '#f5f5f5', 'chip': 0}]}),
 137: ('image', {'kb': 'in', 'ov': [HEADS137]}),
 138: ('image', {'ov': [HEADS137, {'k': 'spotmove', 'n': 4}]}),
 156: ('image', {'kb': 'out', 'ov': [HEADS137]}),
 98: ('image', {'kb': 'r', 'ov': [{'k': 'logo', 'name': 'Microsoft', 'rect': [.30, .07, .12, .06]}, {'k': 'plaque', 'text': 'SAUDI', 'rect': [.545, .075, .13, .07], 'chip': 0}, {'k': 'plaque', 'text': 'PENSION FUND', 'rect': [.78, .08, .12, .055], 'chip': 0}]}),
})
S.update({
 148: ('image', {'kb': 'in', 'ov': [{'k': 'plaque', 'text': 'BUDGET', 'rect': [.32, .585, .14, .05], 'col': '#ffd23f', 'chip': 0}, {'k': 'tag', 'text': 'GAME OVER', 'x': .5, 'y': .5, 'at': .7, 'red': 1}]}),
 150: ('image', {'kb': 'in', 'ov': [{'k': 'plaque', 'text': 'BADA FAIL', 'rect': [.56, .03, .39, .27], 'col': '#d11', 'chip': 0}]}),
 152: ('image', {'kb': 'l', 'ov': [{'k': 'plaque', 'text': 'LEHMAN BROTHERS', 'rect': [.54, .045, .33, .12], 'col': '#222', 'chip': 0}, {'k': 'tag', 'text': '2008', 'x': .1, 'y': .12}]}),
 153: ('image', {'kb': 'in', 'ov': [{'k': 'plaque', 'text': 'FTX', 'rect': [.46, .06, .48, .24], 'col': '#222', 'chip': 0}]}),
 154: ('image', {'cuts': [[0, 0, .36, 1], [.32, 0, .36, 1], [.64, 0, .36, 1]], 'ov': [{'k': 'plaque', 'text': 'STOP', 'rect': [.84, .3, .1, .3], 'col': '#fff', 'chip': 0, 'cut': 2}]}),
 161: ('image', {'kb': 'in', 'ov': [{'k': 'headlogo', 'heads': [[.13, .32, .045, 'Google'], [.53, .335, .045, 'Microsoft'], [.7, .355, .045, 'Meta'], [.885, .355, .045, 'Amazon']]}]}),
 162: ('image', {'kb': 'up', 'ov': [{'k': 'plaque', 'text': 'AI', 'rect': [.43, .16, .14, .16], 'col': 'rgba(255,255,255,.85)', 'chip': 0}]}),
})
SPEAKER_RE = re.compile(r'(?:SKIT(?:\s*\([^)]*\))?\s*[—-]+\s*)?(?:^|(?<=/ )|(?<=^))[A-Z][A-Z ]{1,20}(?:\s*\([^)]*\))?(?: typing)?:\s*')


def clean_vo(vo):
    if vo.startswith('('):
        return ''
    vo = re.sub(r'SKIT(?:\s*\([^)]*\))?\s*[—-]+\s*', '', vo)
    vo = re.sub(r'(^|/\s*)[A-Z][A-Z ]{1,20}(?:\s*\([^)]*\))?(?: typing)?:\s*', ' ', vo)
    return vo.replace(' / ', ' ')


def norm(t):
    return re.findall(r'[a-z0-9]+', t.lower())


def art_for(n):
    v = IDX.get(str(n))
    if v:
        return v.split()[0].replace('.png', ''), v
    f = 's%03d' % n
    if os.path.exists(os.path.join(HERE, 'art', f + '.png')):
        return f, ''
    m = re.search(r'reuse (\d+)', next(d['asset'] for d in DOC if d['id'] == n))
    if m:
        return art_for(int(m.group(1)))
    return None, ''


def main():
    # word list with estimated times
    words = []
    for seg in TL['segments']:
        toks = [(m.group(0).lower(), m.start()) for m in re.finditer(r'[A-Za-z0-9]+', seg['text'])]
        L = len(seg['text']) or 1
        for w, c in toks:
            words.append((w, seg['start'] + (seg['end'] - seg['start']) * c / L, seg['id'], seg['kind']))
    ws = [w[0] for w in words]
    p, starts = 0, {}
    for d in DOC:
        toks = norm(clean_vo(d['vo']))
        if not toks:
            continue
        best, bi = -1, p
        for i in range(p, min(len(ws), p + 120)):
            sc = sum(1 for k in range(min(6, len(toks))) if i + k < len(ws) and ws[i + k] == toks[k]) - (i - p) * 0.002
            if sc > best:
                best, bi = sc, i
        if best < 2 and len(toks) >= 2:
            print('WARN weak match shot', d['id'], toks[:6], '->', ws[bi:bi + 6])
        starts[d['id']] = (bi, words[bi][1], words[bi][2], words[bi][3])
        p = bi + max(1, len(toks) - 3)
    ends = [b for a, b in SIL]

    def snap(t):
        i = bisect.bisect_left(ends, t)
        cands = [ends[j] for j in (i - 1, i) if 0 <= j < len(ends)]
        c = min(cands, key=lambda e: abs(e - t)) if cands else t
        return c - 0.06 if abs(c - t) < 0.7 else t
    shots = []
    for d in DOC:
        n = d['id']
        tpl, prm = S.get(n, ('image', {}))
        prm = json.loads(json.dumps(prm))
        sh = {'id': n, 'tpl': tpl, 'p': prm, 'vo': d['vo'], 'visual': d['visual'], 'asset': d['asset']}
        if n in starts:
            bi, t, seg, kind = starts[n]
            # first shot of a segment starts at the segment start (pause before it is silence)
            first = bi == 0 or words[bi - 1][2] != seg
            sh['t0'] = next(s['start'] for s in TL['segments'] if s['id'] == seg) if first else snap(t)
            sh['seg'], sh['kind'] = seg, kind
        if 'HF' in d['asset'] and tpl in ('image', 'counter'):
            src, note = art_for(n)
            if src:
                prm.setdefault('src', src)
            else:
                prm['pending'] = 1
        shots.append(sh)
    # no-VO shots
    by = {s['id']: s for s in shots}
    dur = TL['duration']
    nxt = lambda i: next((s['t0'] for s in shots if s['id'] > i and 't0' in s), dur)
    # hook: windows (#4) + AI ERA (#5) + balloon (#6) share 3's end -> 7
    a, b = by[4]['t0'] if 't0' in by[4] else by[5]['t0'], nxt(6)
    a = by[5]['t0']; by[4]['t0'] = a; by[5]['t0'] = a + 1.7; by[6]['t0'] = a + 3.0
    by[11]['t0'] = by[10]['t0'] + 0.55 * (nxt(11) - by[10]['t0'])
    by[167]['t0'] = dur
    shots[0]['t0'] = 0.0
    # keep order + a minimum length: a too-short shot borrows from the next one
    MIN = 1.1
    for i in range(1, len(shots) - 1):
        lo = shots[i - 1]['t0'] + MIN
        if shots[i]['t0'] < lo:
            shots[i]['t0'] = lo
    for i in range(len(shots) - 2, 0, -1):    # never run into the next shot
        if shots[i]['t0'] > shots[i + 1]['t0'] - 0.6:
            shots[i]['t0'] = shots[i + 1]['t0'] - 0.6
    for a, b in zip(shots, shots[1:]):
        a['t1'] = round(b['t0'], 3)
        a['t0'] = round(a['t0'], 3)
    shots[-1]['t1'] = round(dur + END_SCREEN, 3)
    # transitions in
    for i, s in enumerate(shots):
        prev = shots[i - 1] if i else None
        if not prev:
            s['tr'] = 'cut'
        elif s['tpl'] in ('counter', 'bars', 'stickers', 'reveal') or s['tpl'] == 'title' and s['p'].get('style') in ('shake', 'black'):
            s['tr'] = 'flash'
        elif prev['tpl'] == s['tpl'] and s['p'].get('old') or s['p'].get('src') and s['p'].get('src') == prev['p'].get('src'):
            s['tr'] = 'punch'
        else:
            s['tr'] = 'whip'
    bad = [(s['id'], round(s['t1'] - s['t0'], 2)) for s in shots if s['t1'] - s['t0'] < 0.8]
    if bad:
        print('WARN short shots', bad)
    out = {'w': 1920, 'h': 1080, 'fps': 30, 'duration': shots[-1]['t1'], 'shots': shots}
    json.dump(out, open(os.path.join(HERE, 'shots.json'), 'w'), ensure_ascii=False, indent=1)
    os.makedirs(os.path.join(HERE, 'player'), exist_ok=True)
    with open(os.path.join(HERE, 'player', 'shots.js'), 'w') as f:
        f.write('window.SHOTS=' + json.dumps(out, ensure_ascii=False) + ';\n')
    from collections import Counter
    c = Counter(s['tpl'] for s in shots)
    pend = [s['id'] for s in shots if s['p'].get('pending')]
    durs = [s['t1'] - s['t0'] for s in shots[:-1]]
    print(len(shots), 'shots |', dict(c))
    print('dur min %.2f max %.2f mean %.2f' % (min(durs), max(durs), sum(durs) / len(durs)))
    print('art pending (%d):' % len(pend), pend)


if __name__ == '__main__':
    main()
