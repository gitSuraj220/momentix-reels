"""Script words, anchors, caption chunks -> timeline.json (Maths Dangal ad)"""
import re, json
RAW = open('vo_text.txt').read().split()
norm = lambda w: re.sub(r'[^a-z0-9]', '', w.lower())
WORDS = [w for w in RAW if norm(w)]
S = [norm(w) for w in WORDS]
A = [('hook','competitive',1),('ye','ye',1),('teen','teen',1),('dikhao','dikhao',1),('nahi','nahi',1),('dekho','dekho',1),('bas','bas',1),('ulta','ulta',1),
     ('e18','eighteen',1),('barabar','barabar',1),('aadha','aadha',1),('nau','nau',1),('ho','ho',1),('kyun','kyun',1),('sau','sau',1),('guna1','guna',1),('guna2','guna',1),
     ('same','same',1),('par','par',1),('speed','speed',1),('practice','practice',1),('isliye','isliye',1),('maths','maths',1),('saath','saath',1),('pehle','pehle',1),
     ('concept','concept',1),('trick2','trick',1),('practice2','practice',1),('percentage','percentage',1),('time','time',1),('poore','poore',1),('barah','barah',1),
     ('teen2','teen',1),('answer','answer',1),('sirf','sirf',1),('ninety','ninetynine',1),('neeche','neeche',1),('dabao','dabao',1)]
MAP = {'eighteen': '18', 'fifty': '50', 'hundred': '100', 'nau': '9', 'sau': '100', 'barah': '12', 'dangal': 'दंगल', 'ninetynine': '₹99', 'rupaye': ''}
HOT = {'18', '50', '9', 'ulta', 'aadha', 'same', 'speed', 'practice', 'दंगल', 'Maths', '60', '12', '3,378', '₹99', 'button', '3'}
def build(tS, tE, end):
    T = {}; pos = 0
    for name, w, nth in A:
        idx = [i for i in range(pos, len(S)) if S[i] == w]
        if len(idx) < nth: raise SystemExit(f'anchor {name} "{w}" missing after {pos}')
        i = idx[nth-1]; T[name] = round(tS[i], 3); pos = i + 1
    T['end'] = round(end, 3)
    words = []; tTeen = [i for i in range(len(S)) if S[i] == 'teen']
    for i in range(len(S)):
        w = re.sub(r'[^\w\-\'’]', '', WORDS[i]) if S[i] not in MAP else MAP[S[i]]
        if S[i] == 'saath': w = '60' if i == S.index('saath') else 'saath'
        if S[i] == 'teen' and i == tTeen[0]: w = '3'
        if i in tTeen[1:]: w = '3,378' if i == tTeen[1] else ''
        if i > 0 and S[i] in ('hazaar', 'sau', 'athattar') and i > tTeen[1] and i <= tTeen[1] + 4: w = ''
        words.append({'w': w, 's': round(tS[i], 3), 'e': round(tE[i], 3), 'hot': w in HOT})
    segs, cur = [], []
    for i in range(len(S)):
        cur.append(i)
        if WORDS[i][-1] in '.,?:!': segs.append(cur); cur = []
    if cur: segs.append(cur)
    chunks = []
    for sg in segs:
        vis = [i for i in sg if words[i]['w']]; n = len(vis); k = -(-n // 4); size = -(-n // k) if k else 1
        part = []
        for j, i in enumerate(vis):
            part.append(i)
            if len(part) >= size and S[i] != 'maths' and j < n - 1 and (n - j - 1) >= 2: chunks.append(part); part = []
        if part: chunks.append(part)
    caps = [{'i': [i for i in c if words[i]['w']], 's': words[c[0]]['s'], 'e': words[c[-1]]['e']} for c in chunks]
    caps = [c for c in caps if c['i']]
    json.dump({'T': T, 'words': words, 'caps': caps}, open('timeline.json', 'w'), ensure_ascii=False)
    return T
