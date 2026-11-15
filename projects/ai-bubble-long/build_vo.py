"""Assemble the AI Bubble voice track: narration chunks (Suraj clone) + skit lines (Gaurav/Amrut/Devi).
Output: vo/vo_full.wav (48k mono, mastered later in mix.py), vo/vo_full.mp3, timeline.json.
timeline.json = {"duration": s, "segments": [{id, kind, speaker, text, start, end}], "words": [[start, end, word, seg_id]]}
"""
import json, re, subprocess, numpy as np

SR = 48000
NARR_SPEED = 1.12   # Suraj chose fast pace (~9 min)
SKIT_SPEED = 1.05
GAP_IN, GAP_LINE = 0.35, 0.22  # narration<->skit, between skit lines

def load(path, speed=1.0):
    af = ['-af', f'atempo={speed}'] if speed != 1.0 else []
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, *af, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.float32).copy()

def env(a, hop=480):  # 10 ms RMS
    n = len(a) // hop
    return np.sqrt((a[:n * hop].reshape(n, hop) ** 2).mean(1) + 1e-12)

def silences(a, thr_db=-42, min_len=0.12):
    e = 20 * np.log10(env(a)); q = e < thr_db; out = []; i = 0
    while i < len(q):
        if q[i]:
            j = i
            while j < len(q) and q[j]: j += 1
            if (j - i) * 0.01 >= min_len: out.append((i * 0.01, j * 0.01))
            i = j
        else: i += 1
    return out

def trim(a, pad=0.04):
    e = env(a); idx = np.where(20 * np.log10(e) > -45)[0]
    if not len(idx): return a
    s = max(0, int((idx[0] * 0.01 - pad) * SR)); t = min(len(a), int(((idx[-1] + 1) * 0.01 + pad) * SR))
    return a[s:t]

def skel(t):
    t = t.lower().replace('w', 'v').replace('z', 'j').replace('q', 'k').replace('x', 'ks')
    return re.sub(r'[^a-z0-9]', '', re.sub(r'[aeiouyh]', '', t))

def split_by_words(a, texts, words_json, speed):
    """Align script lines to whisper words (Devanagari -> romanized consonant skeleton) and cut
    in the gap between the last word of a line and the first word of the next."""
    from indic_transliteration import sanscript
    from difflib import SequenceMatcher
    W = json.load(open(words_json))
    wsk = [skel(sanscript.transliterate(w[2], 'devanagari', 'itrans')) for w in W]
    stream, owner = '', []
    for i, s in enumerate(wsk): stream += s; owner += [i] * len(s)
    lsk = [skel(t) for t in texts]; script = ''.join(lsk)
    bounds = np.cumsum([len(s) for s in lsk])[:-1]
    sm = SequenceMatcher(None, script, stream, autojunk=False)
    mp = {}
    for blk in sm.get_matching_blocks():
        for k in range(blk.size): mp[blk.a + k] = blk.b + k
    cuts = []
    for b in bounds:
        # nearest mapped script char at/after the boundary -> its whisper word starts the next line
        k = next((j for j in range(b, len(script)) if j in mp), None)
        wi = owner[mp[k]] if k is not None else len(W) - 1
        wi = max(1, wi)
        cuts.append(((W[wi - 1][1] + W[wi][0]) / 2) / speed)
    edges = [0] + [int(c * SR) for c in cuts] + [len(a)]
    return [trim(a[edges[i]:edges[i + 1]]) for i in range(len(texts))]

def split_at(a, raw_cuts, speed):
    sil = silences(a, min_len=0.06)
    cuts = []
    for c in raw_cuts:
        c /= speed
        near = [s for s in sil if abs((s[0] + s[1]) / 2 - c) < 0.45]
        cuts.append((lambda s: (s[0] + s[1]) / 2)(min(near, key=lambda s: abs((s[0] + s[1]) / 2 - c))) if near else c)
    edges = [0] + [int(c * SR) for c in cuts] + [len(a)]
    return [trim(a[edges[i]:edges[i + 1]]) for i in range(len(edges) - 1)]

def split_lines(a, texts):
    """Split a take of paragraph-separated lines: choose n-1 pauses (DP) so each piece's length
    matches its line's share of characters, rewarding long pauses (paragraph breaks)."""
    n = len(texts)
    if n == 1: return [trim(a)]
    dur = len(a) / SR
    sil = [s for s in silences(a, min_len=0.12) if s[0] > 0.2 and s[1] < dur - 0.2]
    cand = [((s0 + s1) / 2, s1 - s0) for s0, s1 in sil]
    w = np.array([len(t) + 8 for t in texts], float); cum = np.concatenate([[0], np.cumsum(w)]) / w.sum() * dur
    m = len(cand); INF = 1e18
    # D[j][k]: best cost with j cuts, last cut = cand k
    D = np.full((n, m), INF); P = np.zeros((n, m), int)
    for k, (c, L) in enumerate(cand): D[1][k] = ((c - cum[1]) / dur) ** 2 * 400 - L * 3
    for j in range(2, n):
        for k, (c, L) in enumerate(cand):
            best, arg = INF, -1
            for p in range(k):
                if D[j - 1][p] < best: best, arg = D[j - 1][p], p
            if arg >= 0: D[j][k] = best + ((c - cum[j]) / dur) ** 2 * 400 - L * 3; P[j][k] = arg
    k = int(np.argmin(D[n - 1])); cuts = []
    for j in range(n - 1, 0, -1): cuts.append(cand[k][0]); k = P[j][k]
    edges = [0] + [int(c * SR) for c in sorted(cuts)] + [len(a)]
    return [trim(a[edges[i]:edges[i + 1]]) for i in range(n)]

# ---------- script ----------
L = open('script_suraj_v2.md').read().split('\n')
blocks = []  # ('N', chunk_text) or ('S', speaker, text)
for l in L[3:]:
    s = l.strip()
    if s.startswith('#'): blocks.append(('H',)); continue
    if not s or s.startswith('[SCENE') or s.startswith('SKIT'): continue
    m = re.match(r'^([A-Z][A-Z ]+)( \([^)]*\))?:\s*(.*)', s)
    if m: blocks.append(('S', m.group(1), m.group(3)))
    elif blocks and blocks[-1][0] == 'N': blocks[-1] = ('N', blocks[-1][1] + ' ' + s)
    else: blocks.append(('N', s))
blocks = [b for b in blocks if b[0] != 'H']

VOICE = {'BETA': 'gaurav', 'ENGINEER': 'gaurav', 'USER': 'gaurav', 'STARTUP': 'gaurav', 'PITCHER': 'gaurav', 'SAM': 'gaurav',
         'AI COMPANY': 'gaurav', 'PAPA': 'amrut', 'BOSS': 'amrut', 'INVESTOR': 'amrut', 'YC DESK': 'amrut',
         'BOARD MEMBER': 'amrut', 'GEMINI': 'devi', 'ARTIST': 'devi'}

# ---------- skit audio, line by line ----------
TAKE = json.load(open('vo/takes.json'))  # chosen take per file
skit = {}
for v in ['gaurav', 'amrut', 'devi']:
    tx = [b[2] for b in blocks if b[0] == 'S' and VOICE[b[1]] == v]
    f = f"skit_{v}_{TAKE['skit_' + v]}"
    CUTS = json.load(open('vo/cuts.json'))
    if f in CUTS:
        skit[v] = split_at(load(f'vo/{f}.mp3', SKIT_SPEED), CUTS[f], SKIT_SPEED); assert len(skit[v]) == len(tx), (f, len(skit[v]))
    else:
        skit[v] = split_by_words(load(f'vo/{f}.mp3', SKIT_SPEED), tx, f'vo/words_{f}.json', SKIT_SPEED)
# year lines regenerated with years spelled out (TTS read 2029 ambiguously)
g2 = split_by_words(load(f"vo/fix_gaurav_{TAKE['fix_gaurav']}.mp3", SKIT_SPEED),
                 ['Do hazaar untees tak, ek sau pandrah billion dollar ka cash burn.',
                  'Do hazaar untees mein. Shayad do hazaar tees mein. Ya do hazaar iktees?'],
                 f"vo/words_fix_gaurav_{TAKE['fix_gaurav']}.json", SKIT_SPEED)
skit['gaurav'][11], skit['gaurav'][12] = g2
skit['amrut'][8] = trim(load(f"vo/fix_amrut_{TAKE['fix_amrut']}.mp3", SKIT_SPEED))

# ---------- narration chunks, split where skits interrupt ----------
groups = [[0, 1], [2, 3, 4], [5, 6], [7, 8], [9, 10]]  # section indexes per chunk (same as vo/narration_0N.txt)
chunk_txt = [open(f'vo/narration_0{i}.txt').read().replace('\n\n', ' ').strip() for i in range(1, 6)]
chunk_audio = [trim(load(f"vo/n0{i}_{TAKE[f'n0{i}']}.mp3", NARR_SPEED)) for i in range(1, 6)]

def norm(t): return re.sub(r'\s+', ' ', t).strip()
# walk the blocks; each 'N' block is a substring of one chunk -> cut chunk audio at proportional point snapped to a pause
pieces = []  # (kind, speaker, text, audio)
ci, cpos, cut_s = 0, 0, 0.0
used = {'gaurav': 0, 'amrut': 0, 'devi': 0}
for b in blocks:
    if b[0] == 'S':
        v = VOICE[b[1]]; pieces.append(('skit', b[1], b[2], skit[v][used[v]])); used[v] += 1; continue
    t = norm(b[1]); full = norm(chunk_txt[ci])
    k = full.find(t, cpos)
    if k < 0:  # block starts the next chunk
        ci += 1; cpos = 0; cut_s = 0.0; full = norm(chunk_txt[ci]); k = full.find(t)
    assert k >= 0, t[:60]
    end_c = k + len(t); a = chunk_audio[ci]; dur = len(a) / SR
    if end_c >= len(full) - 2: end_s = dur
    else:
        guess = dur * end_c / len(full)
        sil = [s for s in silences(a, min_len=0.15) if abs((s[0] + s[1]) / 2 - guess) < 3.0]
        end_s = max(sil, key=lambda s: (s[1] - s[0]) - 0.15 * abs((s[0] + s[1]) / 2 - guess))
        end_s = (end_s[0] + end_s[1]) / 2
    pieces.append(('narr', 'NARRATOR', t, trim(a[int(cut_s * SR):int(end_s * SR)])))
    cut_s, cpos = end_s, end_c

# ---------- assemble ----------
out, segs, t = [], [], 0.0
for i, (kind, spk, text, a) in enumerate(pieces):
    if i:
        prev = pieces[i - 1][0]
        gap = GAP_LINE if (kind == 'skit' and prev == 'skit') else (GAP_IN if kind != prev else 0.18)
        out.append(np.zeros(int(gap * SR), np.float32)); t += gap
    segs.append({'id': i, 'kind': kind, 'speaker': spk, 'text': text, 'start': round(t, 3), 'end': round(t + len(a) / SR, 3)})
    out.append(a); t += len(a) / SR
full = np.concatenate(out)
full.astype('<f4').tofile('/tmp/vo_full.f32')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '/tmp/vo_full.f32', 'vo/vo_full.wav'])
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'vo/vo_full.wav', '-b:a', '192k', 'vo/vo_full.mp3'])
json.dump({'duration': round(t, 3), 'narr_speed': NARR_SPEED, 'skit_speed': SKIT_SPEED, 'segments': segs},
          open('timeline.json', 'w'), ensure_ascii=False, indent=1)
print(f'{len(segs)} segments, {t:.1f} s ({t/60:.2f} min)')
for s in segs: print(f"{s['start']:7.2f} {s['end']:7.2f} {s['speaker']:12s} {s['text'][:70]}")
