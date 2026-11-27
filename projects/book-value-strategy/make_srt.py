"""YouTube CC: aligned words (words.json) + punctuation from vo/sections.json -> final/Book_Value_Strategy.hinglish.srt"""
import json, re
S = json.load(open('vo/sections.json')); W = json.load(open('words.json'))
REP = [(r'\bPichhle do saal\b', 'Pichhle 2 saal'), (r'\bDo saal pehle\b', '2 saal pehle'), (r'\bsau rupaye\b', '₹100'), (r'ek sau chaar, ek sau paanch rupaye', '₹104-105'),
       (r'\bdo minute\b', '2 minute'), (r'\bpachaas lakh\b', '50 lakh'), (r'\btees lakh\b', '30 lakh'), (r'\bbees lakh\b', '20 lakh'), (r'\bpandrah lakh\b', '15 lakh'),
       (r'\bteen saal\b', '3 saal'), (r'\bteen-chaar saal\b', '3-4 saal'), (r'\bdas saal\b', '10 saal'), (r'\bchhe mahine\b', '6 mahine'), (r'\bbook value sau\b', 'book value 100'),
       (r'\btarget do sau\b', 'target 200'), (r'\bStep one\b', 'Step 1'), (r'\bstep two\b', 'step 2'), (r'\bstep three\b', 'step 3'), (r'\bRule one\b', 'Rule 1'), (r'\bRule two\b', 'Rule 2'),
       (r'\bdo-teen baar\b', '2-3 baar'), (r'\bdo simple rules\b', '2 simple rules'), (r'CIAN Agro', 'Cian Agro'), (r'\bgovt\b', 'govt')]
toks = []
for sec, txt in enumerate(S):
    ms = list(re.finditer(r"[A-Za-z0-9']+", txt))
    for i, m in enumerate(ms):
        tail = txt[m.end():ms[i + 1].start() if i + 1 < len(ms) else len(txt)]
        toks.append((m.group(), tail.strip(), sec))
assert len(toks) == len(W), (len(toks), len(W))
chunks, cur = [], []
for i, (w, tail, sec) in enumerate(toks):
    cur.append(i)
    end = any(p in tail for p in '.?!:') or (',' in tail and len(cur) >= 4) or len(cur) >= 8 or i + 1 == len(toks) or toks[i + 1][2] != sec
    if end and i + 1 < len(toks) and (toks[i + 1][0] in ('sau', 'chaar', 'paanch', 'rupaye') or (toks[i + 1][0] == 'ek' and i + 2 < len(toks) and toks[i + 2][0] == 'sau')) and not any(p in tail for p in '.?!'): end = False
    if end: chunks.append(cur); cur = []
f = lambda s: f"{int(s // 3600):02d}:{int(s % 3600 // 60):02d}:{int(s % 60):02d},{int(round((s % 1) * 1000)) % 1000:03d}"
out = []; prev_end = True
for k, c in enumerate(chunks):
    txt = ''
    for i in c:
        w, tail, _ = toks[i]; tail = tail.replace('...', '…') if tail.startswith('...') else tail
        txt += w + (tail if tail else '') + ('' if tail == '-' else ' ')
    txt = txt.strip()
    for a, b in REP: txt = re.sub(a, b, txt)
    txt = re.sub(r'\s*\.\.\.$', '', re.sub(r'([.?!])\s*\.\.\.', r'\1', txt)).strip()
    if prev_end and not txt.startswith('iPad'): txt = txt[0].upper() + txt[1:]
    prev_end = txt[-1] in '.?!…:'
    s = W[c[0]]['s']; e = W[c[-1]]['e'] + 0.15
    if k + 1 < len(chunks): e = min(e, W[chunks[k + 1][0]]['s'] - 0.02)
    out.append(f"{k + 1}\n{f(s)} --> {f(e)}\n{txt}\n")
open('final/Book_Value_Strategy.hinglish.srt', 'w').write('\n'.join(out)); print(len(out), 'cues')
