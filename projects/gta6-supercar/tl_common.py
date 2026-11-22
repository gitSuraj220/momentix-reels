"""Shared: script words, anchors, caption chunks -> timeline.json for reel.html"""
import re, json
RAW = open('vo_text.txt').read().split()
norm = lambda w: re.sub(r'[^a-z0-9]', '', w.lower())
WORDS = [w for w in RAW if norm(w)]
S = [norm(w) for w in WORDS]
A = [('hook','gta',1),('glass','glass',1),('phir','phir',1),('nahi','nahi',1),('aur','aur',1),('next','next',1),('purane','purane',1),
     ('button','button',1),('tumhari','tumhari',1),('gta2','gta',1),('khatam','khatam',1),('wajah','wajah',1),('immobilizer','immobilizer',1),
     ('andar2','andar',1),('computer','computer',1),('chaabi','chaabi',1),('code','code',1),('fuel','fuel',1),('game','game',1),
     ('isliye','isliye',1),('purani','purani',1),('hotwire','hotwire',1),('easy','easy',1),('mehengi','mehengi',1),('cloner','cloner',1),
     ('engine','engine',1),('police','police',1),('main','main',1),('dikkat','dikkat',1),('kyunki','kyunki',1),('tracker','tracker',1),
     ('matlab','matlab',1),('dhoondh','dhoondh',1),('heat','heat',1),('kapde','kapde',1),('look','look',1),('lowkey','lowkey',1),
     ('basically','basically',1),('fast','fast',1),('bekaar','bekaar',1),('nocap','no',1)]
def disp(i):
    w = WORDS[i]
    if norm(w) == 'six' and i and norm(WORDS[i-1]) == 'gta': return '6' + re.sub(r'[A-Za-z]', '', w)
    return w
def build(tS, tE, end):
    T = {}; pos = 0
    for name, w, nth in A:
        idx = [i for i in range(pos, len(S)) if S[i] == w]
        if len(idx) < nth: raise SystemExit(f'anchor {name} "{w}" missing after {pos}')
        i = idx[nth-1]; T[name] = round(tS[i], 3); pos = i + 1
    T['end'] = round(end, 3)
    words = [{'w': disp(i).upper().replace('...', '…'), 's': round(tS[i],3), 'e': round(tE[i],3)} for i in range(len(S))]
    # caption chunks: 2-4 words, break after punctuation
    chunks = []; cur = []
    for i, wd in enumerate(words):
        cur.append(i); raw = WORDS[i]
        if raw[-1] in '.,?:!' or raw.endswith('...') or len(cur) >= 4 or (len(cur) >= 3 and len(WORDS[i]) > 6):
            chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    # merge "GTA 6" split
    caps = [{'i': c, 's': words[c[0]]['s'], 'e': words[c[-1]]['e']} for c in chunks]
    json.dump({'T': T, 'words': words, 'caps': caps}, open('timeline.json', 'w'))
    return T
