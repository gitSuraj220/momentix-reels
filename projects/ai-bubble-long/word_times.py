#!/usr/bin/env python3
"""Real word times on the assembled VO -> vo/word_times.json [[t_start, t_end, skeleton, seg_id, word], ...]
Narration: per chunk (vo/narration_0N.txt take), whisper words (Devanagari) -> consonant skeletons; the roman text of
all timeline segments cut from that chunk is aligned to the whole chunk in ONE pass (order-preserving), then each
segment is shifted so its first matched word starts 40 ms after the segment start (build_vo.py trims to onset - 40 ms).
Skit lines are short single lines: words spread by character share. Unmatched words are interpolated."""
import json, os, re
from difflib import SequenceMatcher
D = os.path.dirname(os.path.abspath(__file__))
TL = json.load(open(f'{D}/timeline.json')); TAKE = json.load(open(f'{D}/vo/takes.json'))
NS = TL['narr_speed']
DEV = {'क': 'k', 'ख': 'k', 'ग': 'g', 'घ': 'g', 'ङ': 'n', 'च': 'c', 'छ': 'c', 'ज': 'j', 'झ': 'j', 'ञ': 'n', 'ट': 't', 'ठ': 't',
       'ड': 'd', 'ढ': 'd', 'ण': 'n', 'त': 't', 'थ': 't', 'द': 'd', 'ध': 'd', 'न': 'n', 'प': 'p', 'फ': 'f', 'ब': 'b', 'भ': 'b',
       'म': 'm', 'य': '', 'र': 'r', 'ल': 'l', 'व': 'v', 'श': 's', 'ष': 's', 'स': 's', 'ह': '', 'ड़': 'r', 'ढ़': 'r',
       'ं': 'n', 'ँ': 'n', '०': '0', '१': '1', '२': '2', '३': '3', '४': '4', '५': '5', '६': '6', '७': '7', '८': '8', '९': '9'}


def dev_skel(w):
    w = w.replace('ड़', 'ड़').replace('़', '')
    return ''.join(DEV.get(c, c.lower() if c.isascii() and c.isalnum() else '') for c in w)


def rom_skel(t):
    t = t.lower()
    for a, b in [('ph', 'f'), ('sh', 's'), ('ch', 'c'), ('th', 't'), ('dh', 'd'), ('kh', 'k'), ('gh', 'g'), ('bh', 'b'),
                 ('w', 'v'), ('z', 'j'), ('q', 'k'), ('x', 'ks')]:
        t = t.replace(a, b)
    return re.sub(r'[^a-z0-9]', '', re.sub(r'[aeiouyh]', '', t))


def chunk_of(seg):
    for i in range(1, 6):
        txt = re.sub(r'\s+', ' ', open(f'{D}/vo/narration_0{i}.txt').read()).strip()
        if seg['text'][:40] in txt: return i
    return None


def main():
    res = {}   # seg id -> list of [a, b, skel, seg, word]
    segs = TL['segments']
    by_chunk = {}
    for s in segs:
        if s['kind'] == 'narr':
            c = chunk_of(s)
            if c: by_chunk.setdefault(c, []).append(s)
    for c, ss in by_chunk.items():
        W = json.load(open(f"{D}/vo/words_n0{c}_{TAKE[f'n0{c}']}.json"))
        stream, owner = '', []
        for i, w in enumerate(W):
            sk = dev_skel(w[2]); stream += sk; owner += [i] * len(sk)
        script, tok_of, toks = '', [], []   # toks: (seg, word, skel)
        for s in ss:
            for x in re.findall(r'[A-Za-z0-9]+', s['text']):
                k = rom_skel(x); toks.append((s, x, k)); script += k; tok_of += [len(toks) - 1] * len(k)
        sm = SequenceMatcher(None, script, stream, autojunk=False)
        tw, tb = {}, {}
        for b in sm.get_matching_blocks():
            if b.size < 2: continue
            for k in range(b.size):
                ti = tok_of[b.a + k]
                if ti not in tw: tw[ti] = owner[b.b + k]; tb[ti] = b.size
        # independent anchor per segment: first strongly matched token near the start
        C = {}
        for s_ in ss:
            idx = [i for i, t in enumerate(toks) if t[0] is s_]
            tot = sum(len(toks[i][1]) for i in idx) or 1; dur = s_['end'] - s_['start']; before = 0
            for i in idx[:12]:
                if i in tw and tb[i] >= 4 and len(toks[i][2]) >= 2:
                    C[s_['id']] = W[tw[i]][0] / NS - before / tot * dur - .04; break
                before += len(toks[i][1])
            else:
                m0 = next((i for i in idx if i in tw), None)
                C[s_['id']] = (W[tw[m0]][0] / NS - .04) if m0 is not None else None
        for s in ss:
            idx = [i for i, t in enumerate(toks) if t[0] is s]
            m = [i for i in idx if i in tw]
            if not m: print('WARN no words for seg', s['id']); continue
            rows = []; c0 = C[s['id']]; dur = s['end'] - s['start']
            for i in idx:
                t0 = W[tw[i]][0] / NS if i in tw else None
                if t0 is not None and c0 - .25 <= t0 <= c0 + dur + .25:
                    rows.append([t0 - c0 + s['start'], W[tw[i]][1] / NS - c0 + s['start'], toks[i][2], s['id'], toks[i][1].lower(), 1])
                else: rows.append([None, None, toks[i][2], s['id'], toks[i][1].lower(), 0])
            # enforce order
            last = -1
            for r in rows:
                if r[5] and r[0] < last: r[0] = r[1] = None; r[5] = 0
                elif r[5]: last = r[0]
            m = [r for r in rows if r[5]]
            for i, r in enumerate(rows):
                if r[0] is None:
                    p = next((rows[j][1] for j in range(i - 1, -1, -1) if rows[j][5]), s['start'])
                    nx = next(((j, rows[j][0]) for j in range(i + 1, len(rows)) if rows[j][5]), (len(rows), s['end']))
                    r[0] = r[1] = p + (nx[1] - p) / (nx[0] - i + 1)
            for r in rows: r[0] = round(r[0], 3); r[1] = round(max(r[1], r[0]), 3)
            res[s['id']] = [r[:5] for r in rows]; res[s['id'] + 1000] = len(m) / len(idx)
    out = []
    for s in segs:
        if s['id'] in res: out += res[s['id']]; continue
        toks = re.findall(r'[A-Za-z0-9]+', s['text']); L = sum(len(x) for x in toks) or 1; t = s['start']
        for x in toks:
            d = (s['end'] - s['start']) * len(x) / L; out.append([round(t, 3), round(t + d, 3), rom_skel(x), s['id'], x.lower()]); t += d
    json.dump(out, open(f'{D}/vo/word_times.json', 'w'))
    cov = {k - 1000: round(v, 2) for k, v in res.items() if k >= 1000}
    print(len(out), 'words; narr match coverage:', cov)


if __name__ == '__main__':
    main()
