"""Momentix helper for the earshot sound bank (github.com/Leonxlnx/earshot, MIT).

252 designed SFX that render offline by id (no models, no network). Use instead of hand-synth SFX.
    from earshot_bank import bank
    x = bank('pro_impact/short')            # mono float32 @ 48 kHz, peak-normalised to -1 dBFS
    x = bank('pro_riser/roll', dur=0.8)     # exact length for 'dur param' sounds
List ids:  python3 -m earshot sfx list   |   QA a take:  python3 -m earshot sfx check <wav>
Install (once per session): git clone --depth 1 https://github.com/Leonxlnx/earshot ~/earshot
  && pip install --break-system-packages -e ~/earshot --no-deps && pip install --break-system-packages soxr librosa pyloudnorm scikit-learn
Note: earshot's listening tools (describe/match/critique) need CLAP/AST models from Hugging Face, which this
environment cannot download; the bank and `sfx check` work without them.
"""
import hashlib, os, subprocess
import numpy as np, soundfile as sf

CACHE = os.path.expanduser('~/.cache/momentix_sfx')
SR = 48000

def bank(sid, dur=None, seed=None, pitch=None):
    os.makedirs(CACHE, exist_ok=True)
    key = hashlib.md5(f'{sid}|{dur}|{seed}|{pitch}'.encode()).hexdigest()[:12]
    path = os.path.join(CACHE, sid.replace('/', '_') + '_' + key + '.wav')
    if not os.path.exists(path):
        cmd = ['python3', '-m', 'earshot', 'sfx', 'render', sid, '-o', path, '--sr', str(SR)]
        if dur is not None: cmd += ['--dur', str(dur)]
        if seed is not None: cmd += ['--seed', str(seed)]
        if pitch is not None: cmd += ['--pitch', str(pitch)]
        subprocess.run(cmd, check=True, capture_output=True, cwd='/tmp')
    x, sr = sf.read(path, dtype='float32')
    if x.ndim > 1: x = x.mean(1)
    assert sr == SR, sr
    return x
