"""Forced-align the exact TTS text of each section to vo/secN.wav (MMS CTC aligner) -> words.json (global times)."""
import json, re
from ctc_forced_aligner import AlignmentSingleton, load_audio, generate_emissions, preprocess_text, get_alignments, get_spans, postprocess_results
S = json.load(open('vo/sections.json')); meta = json.load(open('vo/sections_meta.json'))
A = AlignmentSingleton(); model, tok = A.alignment_model, A.alignment_tokenizer
W = []
for i, txt in enumerate(S):
    a = load_audio(f'vo/sec{i+1}.wav')
    em, stride = generate_emissions(model, a, batch_size=4)
    clean = re.sub(r'\s+', ' ', re.sub(r'[^A-Za-z0-9\' ]', ' ', txt)).strip()
    ts, tx = preprocess_text(clean, romanize=True, language='eng')
    seg, sc, blank = get_alignments(em, ts, tok)
    sp = get_spans(ts, seg, blank)
    for w in postprocess_results(tx, sp, stride, sc):
        W.append({'w': w['text'].lower(), 's': round(meta['starts'][i] + w['start'], 2), 'e': round(meta['starts'][i] + w['end'], 2), 'sec': i + 1})
    print(i + 1, len([w for w in W if w['sec'] == i + 1]))
json.dump(W, open('words.json', 'w'))
