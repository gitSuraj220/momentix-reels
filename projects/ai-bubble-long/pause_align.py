#!/usr/bin/env python3
"""Anchor script sentence ends to real pauses in vo_full (no ASR needed) -> vo/anchors.json
For every VO segment: sentence / ellipsis ends in the text get an expected time by character share; a monotonic DP
assigns each to a distinct detected pause (vo/silences.tsv), preferring near + long pauses (a boundary may stay
unassigned). Output per segment: [[char_pos, time], ...] incl. segment start/end -> piecewise-linear char->time map.
make_shots.py uses it to place every shot (sentence starts land exactly on the pause end)."""
import json, os, re
D = os.path.dirname(os.path.abspath(__file__))
TL = json.load(open(f'{D}/timeline.json'))
SIL = [tuple(map(float, l.split())) for l in open(f'{D}/vo/silences.tsv')]
SIG, SKIP, LONG = 1.6, 3.0, 2.0


def align(seg):
    txt = seg['text']; s0, s1 = seg['start'], seg['end']; L = len(txt) or 1
    b = [m.end() for m in re.finditer(r'(\.\.\.|[.?!:])["”]?\s+(?=\S)', txt)]   # positions where the next sentence starts
    if not b: return [[0, s0], [L, s1]]
    P = [(a, e) for a, e in SIL if s0 + .2 < e < s1 - .1 and e - a >= .15]
    if not P: return [[0, s0], [L, s1]]
    exp = [s0 + (s1 - s0) * c / L for c in b]
    K, M = len(b), len(P); INF = 1e18
    # dp[i][j]: best cost for boundaries[:i+1] with boundary i on pause j; skip handled via best-so-far
    dp = [[INF] * M for _ in range(K)]; bk = [[None] * M for _ in range(K)]
    def cost(i, j): return ((P[j][1] - exp[i]) / SIG) ** 2 - LONG * min(P[j][1] - P[j][0], .8)
    for i in range(K):
        for j in range(M):
            c = cost(i, j)
            best, arg = SKIP * i, None                 # all earlier boundaries skipped
            for ii in range(i):
                for jj in range(j):
                    v = dp[ii][jj] + SKIP * (i - ii - 1)
                    if v < best: best, arg = v, (ii, jj)
            dp[i][j] = best + c; bk[i][j] = arg
    # end: pick best last assignment (+ skips after)
    best, end = SKIP * K, None
    for i in range(K):
        for j in range(M):
            v = dp[i][j] + SKIP * (K - 1 - i)
            if v < best: best, end = v, (i, j)
    pairs = []
    while end:
        i, j = end; pairs.append((b[i], P[j][1])); end = bk[i][j]
    pairs.sort()
    return [[0, s0]] + [[c, t] for c, t in pairs] + [[L, s1]]


def main():
    out = {}; n = 0
    for seg in TL['segments']:
        a = align(seg); out[str(seg['id'])] = a; n += len(a) - 2
    json.dump(out, open(f'{D}/vo/anchors.json', 'w'))
    print(n, 'sentence starts anchored to real pauses')


if __name__ == '__main__':
    main()
