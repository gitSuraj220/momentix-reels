"""Script words, anchors, caption chunks -> timeline.json"""
import re, json
RAW = open('vo_text.txt').read().split()
norm = lambda w: re.sub(r'[^a-z0-9]', '', w.lower())
WORDS = [w for w in RAW if norm(w)]
S = [norm(w) for w in WORDS]
A = [('hook','exam',1),('chatgpt','chatgpt',1),('teen','teen',1),('padhai','padhai',1),('half','half',1),('last','last',1),('best','best',1),
     ('pehla','pehla',1),('quiz','quiz',1),('chapter','chapter',1),('mcq','mcq',1),('galat','galat',1),('wahin','wahin',1),('personal','personal',1),
     ('doosra','doosra',1),('snapnotes','snapnotes',1),('textbook','textbook',1),('photo','photo',1),('seconds','seconds',1),('trick','trick',1),
     ('teesra','teesra',1),('op','op',1),('examiner','examiner',1),('answer','answer',1),('examiner2','examiner',1),('marks','marks',1),
     ('batayega','batayega',1),('kat','kat',1)]
def build(tS, tE, end):
    T = {}; pos = 0
    for name, w, nth in A:
        idx = [i for i in range(pos, len(S)) if S[i] == w]
        if len(idx) < nth: raise SystemExit(f'anchor {name} "{w}" missing after {pos}')
        i = idx[nth-1]; T[name] = round(tS[i], 3); pos = i + 1
    T['end'] = round(end, 3)
    words = []
    for i in range(len(S)):
        w = WORDS[i].upper().replace('...', '…')
        if S[i] == 'slash': w = ''
        elif i and S[i-1] == 'slash': w = '/' + w
        if S[i] == 'teen': w = '3'
        words.append({'w': w, 's': round(tS[i], 3), 'e': round(tE[i], 3)})
    chunks, cur = [], []
    for i in range(len(S)):
        cur.append(i); raw = WORDS[i]
        if raw[-1] in '.,?:!' or raw.endswith('...') or len([c for c in cur if words[c]['w']]) >= 4: chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    caps = [{'i': [i for i in c if words[i]['w']], 's': words[c[0]]['s'], 'e': words[c[-1]]['e']} for c in chunks]
    caps = [c for c in caps if c['i']]
    json.dump({'T': T, 'words': words, 'caps': caps}, open('timeline.json', 'w'))
    return T
