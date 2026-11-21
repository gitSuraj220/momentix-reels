"""Align the VO script text to whisper word times -> words.json + timeline.json (anchor name -> seconds).
Each anchor = (name, word, nth occurrence counted after the previous anchor's word index)."""
import json, re, difflib, subprocess, numpy as np
from faster_whisper import WhisperModel
txt = open('script.md').read().split('## VO text')[1]
parts = re.split(r'### Part \d[^\n]*\n', txt)[1:4]
norm = lambda w: re.sub(r'[^a-z0-9]', '', w.lower())
S = [norm(w) for w in ' '.join(parts).split() if norm(w)]
a = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', 'vo/vo_full.wav', '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'],
                                 capture_output=True).stdout, np.float32)
m = WhisperModel('small', compute_type='int8', cpu_threads=8)
segs, _ = m.transcribe(a, language='en', word_timestamps=True, beam_size=1, initial_prompt=' '.join(S[:60]))
H = [(norm(w.word), w.start, w.end) for s in segs for w in s.words if norm(w.word)]
json.dump([{'w': h[0], 's': round(h[1], 2), 'e': round(h[2], 2)} for h in H], open('words.json', 'w'))
sm = difflib.SequenceMatcher(None, S, [h[0] for h in H], autojunk=False)
tS = [None] * len(S)
for blk in sm.get_matching_blocks():
    for k in range(blk.size): tS[blk.a + k] = H[blk.b + k][1]
# fuzzy fill for unmatched words, then interpolate
known = [i for i, v in enumerate(tS) if v is not None]
for i in range(len(S)):
    if tS[i] is None:
        lo = max([k for k in known if k < i], default=None); hi = min([k for k in known if k > i], default=None)
        if lo is None: tS[i] = tS[hi]
        elif hi is None: tS[i] = tS[lo] + 0.3 * (i - lo)
        else: tS[i] = tS[lo] + (tS[hi] - tS[lo]) * (i - lo) / (hi - lo)
A = [('hook', 'aap', 1), ('rate', 'rupaya', 1), ('iphone', 'iphone', 1), ('gyaarah', 'gyaarah', 1), ('dubai', 'dubai', 1),
     ('maza', 'maza', 1), ('dark', 'dark', 1), ('hafte', 'hafte', 1), ('bank', 'bank', 1), ('mujhe', 'mujhe', 1), ('rbi', 'rbi', 1),
     ('bahut', 'bahut', 1), ('bahattar', 'bahattar', 1), ('crores', 'crores', 1), ('dopahar', 'dopahar', 1), ('game', 'game', 1),
     ('black', 'black', 1), ('asli', 'asli', 1), ('matlab', 'matlab', 1), ('setting', 'setting', 1), ('rajesh', 'rajesh', 1),
     ('dirham', 'dirham', 1), ('chhihattar', 'chhihattar', 1), ('kal', 'kal', 1), ('aath', 'aath', 1), ('bigl', 'big', 1),
     ('emi', 'emi', 1), ('kahani', 'kahani', 1), ('paintees', 'paintees', 1), ('sabse1', 'sabse', 1),
     ('priya', 'priya', 1), ('dassau', 'das', 1), ('poore', 'poore', 1), ('tiraanve', 'tiraanve', 1), ('koi', 'koi', 1), ('shift', 'shift', 1),
     ('chhotu', 'chhotu', 1), ('pachaas', 'pachaas', 1), ('chhiyaalees', 'chhiyaalees', 1), ('kagaz', 'kagaz', 1), ('kahan', 'kahan', 1),
     ('theory', 'theory', 1), ('zimbabwe', 'zimbabwe', 1), ('barabarz', 'barabar', 1), ('bazaar', 'bazaar', 1), ('kanoon', 'kanoon', 1), ('bharosa1', 'bharosa', 1),
     ('whatsapp', 'whatsapp', 1), ('cap', 'cap', 1), ('tees', 'tees', 1), ('pahunche', 'pahunche', 1),
     ('wajah', 'wajah', 1), ('mehngai', 'mehngai', 1), ('america', 'america', 1), ('tel', 'tel', 1), ('athaasi', 'athaasi', 1),
     ('jhatke', 'jhatke', 1), ('ikyaanve', 'ikyaanve', 1), ('sona', 'sona', 1), ('jung', 'jung', 1), ('investors', 'investors', 1),
     ('may', 'may', 1), ('neeche', 'neeche', 1), ('twist', 'twist', 1), ('yen', 'yen', 1), ('amir', 'amir', 1), ('number', 'number', 1),
     ('turkey', 'turkey', 1), ('zero', 'zero', 1), ('badla', 'badla', 1), ('naya', 'naya', 1), ('priya2', 'priya', 1),
     ('strong', 'strong', 1), ('nawaasi', 'nawaasi', 1), ('made', 'made', 1), ('tel2', 'tel', 1), ('ev', 'ev', 1),
     ('control', 'control', 1), ('bane', 'bane', 1), ('aise', 'aise', 1), ('kamaana', 'kamaana', 1)]
T = {}; pos = 0
for name, w, nth in A:
    idx = [i for i in range(pos, len(S)) if S[i] == w]
    if len(idx) < nth: raise SystemExit(f'anchor {name}: "{w}" not found after word {pos}')
    i = idx[nth - 1]; T[name] = round(tS[i], 2); pos = i + 1
T['end'] = round(len(a) / 16000, 2)
json.dump(T, open('timeline.json', 'w'), indent=0)
matched = sum(b.size for b in sm.get_matching_blocks())
print(f'matched {matched}/{len(S)} script words; end {T["end"]}s')
print(' '.join(f'{k}={v}' for k, v in T.items()))
