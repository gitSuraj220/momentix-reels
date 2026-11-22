"""Estimated timing (no VO yet): ~3.0 words/s after 1.15x, pauses at punctuation."""
from tl_common import *
t = 0.35; tS = []; tE = []
for w in WORDS:
    d = 0.16 + 0.055 * len(norm(w)); tS.append(t); tE.append(t + d); t += d
    if w.endswith('...'): t += 0.35
    elif w[-1] in '.?!': t += 0.22
    elif w[-1] in ',:': t += 0.1
k=(165/3.35)/t; tS=[x*k for x in tS]; tE=[x*k for x in tE]
T = build(tS, tE, t*k + 0.8)
print(T['end']); print(T)
