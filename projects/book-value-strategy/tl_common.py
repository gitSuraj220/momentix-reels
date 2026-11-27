"""Trig hexagon reel: script words, anchors, caption chunks -> timeline.json"""
import re, json
RAW = open('vo_text.txt').read().split()
norm = lambda w: re.sub(r'[^a-z0-9]', '', w.lower())
WORDS = [w for w in RAW if norm(w)]
S = [norm(w) for w in WORDS]
A = [('boards','boards',1),('bro','bro',1),('n27','sattaees',1),('hexagon','hexagon',1),('left','left',1),('sin1','sine',1),('tan1','tan',1),('sec1','sec',1),
     ('right','right',1),('cos1','cos',1),('cot1','cot',1),('cosec1','cosec',1),('beech','beech',1),('setup','setup',1),
     ('rule1','rule',1),('aamne','aamnesaamne',1),('answer','answer',1),('sin2','sine',1),('cos2','cos',1),('tan2','tan',1),
     ('rule2','rule',1),('ghadi','ghadi',1),('tan3','tan',1),('ulta','ulta',1),('cot3','cot',1),
     ('rule3','rule',1),('koi','koi',1),('padosi','padosi',1),('tan4','tan',1),
     ('rule4','rule',1),('neeche','neeche',1),('upar','upar',1),('sin5','sine',1),('literally','literally',1),('poori','poori',1),('comment','comment',1),('formula','formula',1),('dm','dm',1)]
MAP = {'sattaees': '27', 'one': '1', 'two': '2', 'three': '3', 'four': '4', 'sine': 'sin', 'equals': '=', 'into': '×', 'by': '÷'}
HOT = {'27', 'hexagon', 'sin', 'cos', 'tan', 'sec', 'cot', 'cosec', '1', 'FORMULA', 'DM', 'PDF', 'cheat', 'padosi', 'ghadi', 'aamne-saamne', 'triangles', 'square', 'Boards', 'maths'}
def build(tS, tE, end):
    T = {}; pos = 0
    for name, w, nth in A:
        idx = [i for i in range(pos, len(S)) if S[i] == w]
        if len(idx) < nth: raise SystemExit(f'anchor {name} "{w}" missing after {pos}')
        i = idx[nth-1]; T[name] = round(tS[i], 3); pos = i + 1
    T['end'] = round(end, 3)
    words = []
    for i in range(len(S)):
        w = re.sub(r'[^\w\-\'’]', '', WORDS[i])
        if S[i] in MAP: w = MAP[S[i]]
        words.append({'w': w, 's': round(tS[i], 3), 'e': round(tE[i], 3), 'hot': w.strip('"') in HOT or w.lower().strip('"') in HOT})
    segs, cur = [], []
    for i in range(len(S)):
        cur.append(i)
        if WORDS[i][-1] in '.,?:!"' and not WORDS[i].endswith('..') or WORDS[i].endswith('...'): segs.append(cur); cur = []
    if cur: segs.append(cur)
    chunks = []
    for sg in segs:
        vis = [i for i in sg if words[i]['w']]
        if not vis: continue
        n = len(vis); k = -(-n // 4); size = -(-n // k) if k else 1; part = []
        for j, i in enumerate(vis):
            part.append(i)
            if len(part) >= size and j < n - 1 and (n - j - 1) >= 2: chunks.append(part); part = []
        if part: chunks.append(part)
    caps = [{'i': c, 's': words[c[0]]['s'], 'e': words[c[-1]]['e']} for c in chunks]
    json.dump({'T': T, 'words': words, 'caps': caps}, open('timeline.json', 'w'), ensure_ascii=False)
    return T
