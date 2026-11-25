"""Re-align from words.json (no whisper) with digit/spelling map -> timeline.json"""
import json, difflib
from tl_common import S, build
W = json.load(open('words.json')); END = json.load(open('vo/len.json'))['end']
FIX = {'18': 'eighteen', '50': 'fifty', '9': 'nau', '12': 'barah', '99': 'ninetynine', 'kyo': 'kyun', 'saad': 'saath', 'fir': 'phir', 'per': 'par', 'rose': 'roz',
       'bhas': 'bas', 'zolta': 'ulta', 'cheese': 'cheez', 'hoa': 'hua', 'mai': 'main', 'kese': 'kaise', 'kardo': 'do', '3378': 'teen', 'questions': 'sawaal', 'only': 'sirf', 'rupees': 'rupaye', 'sawame': 'sau', '8': 'ek'}
H = [(FIX.get(w['w'], w['w']), w['s'], w['e']) for w in W]
H = [(('hundred' if h[0] == '100' else h[0]), h[1], h[2]) for h in H]
sm = difflib.SequenceMatcher(None, S, [h[0] for h in H], autojunk=False)
tS = [None] * len(S); tE = [None] * len(S)
for b in sm.get_matching_blocks():
    for k in range(b.size): tS[b.a + k] = H[b.b + k][1]; tE[b.a + k] = H[b.b + k][2]
known = [i for i, v in enumerate(tS) if v is not None]
for i in range(len(S)):
    if tS[i] is None:
        lo = max([k for k in known if k < i], default=None); hi = min([k for k in known if k > i], default=None)
        tS[i] = tS[lo] + 0.3 * (i - lo) if hi is None else (tS[hi] - 0.3 * (hi - i) if lo is None else tS[lo] + (tS[hi] - tS[lo]) * (i - lo) / (hi - lo))
for i in range(len(S)):
    if tE[i] is None: tE[i] = tS[i + 1] if i + 1 < len(S) else tS[i] + 0.3
print('matched', sum(b.size for b in sm.get_matching_blocks()), '/', len(S)); T = build(tS, tE, END); print(T)
