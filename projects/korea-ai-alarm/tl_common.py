"""Korea AI alarm reel: script words, anchors, caption chunks -> timeline.json"""
import re, json
RAW = open('vo_text.txt').read().split()
norm = lambda w: re.sub(r'[^a-z0-9]', '', w.lower())
WORDS = [w for w in RAW if norm(w)]
S = [norm(w) for w in WORDS]
A = [('thali','thali',1),('sarkar1','sarkar',1),('phones','phone',1),('yaad','yaad',1),('korea','korea',1),('smart','smart',1),('scene','scene',1),('rank','rank',1),
     ('chhupe','chhupe',1),('ai1','ai',1),('answer','answer',1),('iske','iske',1),('alert','alert',1),('nov','unnees',1),('paanch','paanch',1),('college','college',1),
     ('sarkar3','sarkar',1),('alarm','alarm',1),('teen','teen',1),('silent','silent',1),('jinhone','jinhone',1),('bag','bag',1),('literally','literally',1),
     ('unchaas','unchaas',1),('ek','ek',1),('earphones','earphones',1),('ab','ab',1),('companies','companies',1),('data','data',1),('india','india',1),('disaster','disaster',1)]
MAP = {'unnees': '19', 'paanch': '5', 'unchaas': '49', 'one': '1', 'four': '4K', 'ai': 'AI'}
HOT = {'thali', 'phone', 'Korea', 'smart', 'topper', '1', 'AI', 'camera', 'alert', '19', '5', 'alarm', 'Teen', 'Silent', 'bag', '4K', '49', 'mini', 'earphones', 'data', 'India', 'disaster', 'cheat', 'cheekh'}
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
        if S[i] == 'k' and i > 0 and S[i - 1] == 'four': w = ''
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
