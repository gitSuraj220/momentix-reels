"""Room 3D reel: script words, anchors, caption chunks -> timeline.json"""
import re, json
RAW = open('vo_text.txt').read().split()
norm = lambda w: re.sub(r'[^a-z0-9]', '', w.lower())
WORDS = [w for w in RAW if norm(w)]
S = [norm(w) for w in WORDS]
A = [('ghar','ghar',1),('architect','architect',1),('free','free',1),('bas','bas',1),('teen','teen',1),('claude','claude',1),('poora','poora',1),('3d','3d',1),
     ('measuring','measuring',1),('noneed','no',1),('darwaza','darwaza',1),('andaza','andaza',1),('phir','phir',1),('browser','browser',1),('bed','bed',1),('almirah','almirah',1),
     ('full','full',1),('poocho','poocho',1),('sofa','sofa',1),('fit','fit',1),('deewar','deewar',1),('darwaza2','darwaza',1),('chalne','chalne',1),('check','check',1),
     ('room2','room',1),('colour','colour',1),('sage','sage',1),('mummy','mummy',1),('peach','peach',1),('do','do',1),('layout','layout',1),('size','size',1),('batata','batata',1),
     ('comment','comment',1),('roomcta','room',1),('setup','setup',1),('prompts','prompts',1),('dunga','dunga',1)]
MAP = {'seven': '7', 'teen': '3', '3d': '3D', 'do': '2', 'room': 'ROOM'}
HOT = {'2-3', 'free', '3', '3D', 'size', 'browser', 'full', '7', 'sofa', 'check', 'colour', 'peach', 'layout', 'guess', 'ROOM', 'Claude', 'andaza', 'sage', 'fit'}
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
        if S[i] == 'room' and i < len(S) - 12: w = 'room'  # only the CTA ROOM is caps
        if S[i] == 'do': w = '2-3' if (i + 1 < len(S) and S[i + 1] == 'teen') else WORDS[i]
        if S[i] == 'teen' and i > 0 and S[i - 1] == 'do': w = ''
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
