"""SFX for the book-value documentary (cues mirror reel.html). VO + SFX mix, stems, mux.
Suraj adds music himself, so SFX stay sparse and low. usage: python3 sfx.py [preview_end_seconds]"""
import sys, os, json, subprocess, numpy as np
from scipy.signal import butter, sosfilt
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'engine'))
from earshot_bank import bank
os.chdir(os.path.dirname(os.path.abspath(__file__)))
WORDS = json.load(open('words.json')); END = json.load(open('timeline.json'))['T']['end']
PREV = float(sys.argv[1]) if len(sys.argv) > 1 else None
LEN = PREV or END
SR = 48000; n = int((LEN + 1) * SR); mix = np.zeros((n, 2)); rng = np.random.default_rng(11)
def W(w, k=1, after=0):
    c = 0
    for x in WORDS:
        if x['s'] >= after and x['w'] == w:
            c += 1
            if c == k: return x['s']
    raise SystemExit(f'word {w} {k} {after}')
def add(t, s, g=1.0, pan=0.0):
    i = max(0, int(t * SR))
    if i >= n: return
    s = np.asarray(s, float)[:n - i]; l, r = np.cos((pan + 1) * np.pi / 4) * 1.414, np.sin((pan + 1) * np.pi / 4) * 1.414
    mix[i:i + len(s), 0] += s * g * l; mix[i:i + len(s), 1] += s * g * r
lp = lambda x, f: sosfilt(butter(4, f, 'low', fs=SR, output='sos'), x)
bp = lambda x, a, b: sosfilt(butter(4, [a, b], 'band', fs=SR, output='sos'), x)
def fade(x, a=0.3, b=0.5):
    t = np.arange(len(x)) / SR; return x * np.minimum(1, t / a) * np.minimum(1, (len(x) / SR - t) / b)
def rain(d):  # soft rain on glass for the cold open
    x = bp(rng.standard_normal(int(d * SR)), 900, 7000) * 0.5 + lp(rng.standard_normal(int(d * SR)), 400) * 0.6
    drops = np.zeros(int(d * SR))
    for j in rng.integers(0, len(drops) - 2000, int(d * 22)): drops[j:j + 400] += rng.uniform(.2, .7) * np.exp(-np.arange(400) / 60) * rng.standard_normal(400)
    return fade(x / np.abs(x).max() * 0.6 + bp(drops, 2000, 9000) * 1.5, .6, .4)
def drone(d, f=55):
    t = np.arange(int(d * SR)) / SR; x = np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 1.5 * t + 1) + .25 * np.sin(2 * np.pi * f * 2 * t)
    return fade(x * (0.8 + 0.2 * np.sin(2 * np.pi * 0.3 * t)) / 1.8, 1.0, 0.6)
def counter(d, k):
    x = np.zeros(int(d * SR)); tk = bank('pro_hover_tick/glass')
    for i in range(k):
        j = int(d * SR * (1 - (1 - i / k) ** 2)); s = tk[:len(x) - j]; x[j:j + len(s)] += s * 0.6
    return x

# ---- anchors (same words as reel.html) ----
T = dict(literally=W('literally'), kuch=W('kuch'), aur1=W('aur'), ye1=W('ye'), screenshot=W('screenshot'), app=W('app'), zerodha=W('zerodha'),
         yeraha=W('raha'), actual=W('actual'), ret1=W('return', 2), live=W('live'), ab=W('ab'), sau=W('sau'), aaj=W('aaj'), ek=W('ek'),
         paanch=W('paanch'), fd=W('fd'), zyadatar=W('zyadatar'), laal=W('laal'), wahin=W('wahin'), question=W('question'), mera3=W('mera', 3),
         aaj2=W('aaj', 2), isi=W('isi'), par=W('par'), free=W('free'), isme=W('isme'), data=W('data'), video=W('video'), ai=W('ai'),
         hoon2=W('hoon', 1, 55), step1=W('step'), book1=W('book'))
# cold open
add(0, rain(T['ye1'] + 0.2), 0.10); add(0, drone(T['ye1'] + 0.3, 49), 0.05)
# S2 chart
add(T['literally'] - 0.2, bank('swish/soft'), 0.25); add(T['literally'], bank('pro_riser/air_gate', dur=1.6), 0.10)
for fr in (0.02, 0.62, 1.0): add(T['literally'] + 1.6 * fr ** 0.8, bank('pro_hover_tick/glass'), 0.22, pan=-.4 + .8 * fr)
add(T['kuch'], bank('pro_impact/short'), 0.30)
# S3 reveal
add(T['ye1'] - 0.02, bank('impact/punch'), 0.42); add(T['ye1'], bank('cut_hit/sub'), 0.35)
add(T['screenshot'], bank('shutter/snap'), 0.30)
for k in ('app', 'zerodha', 'yeraha'): add(T[k], bank('ui_pop/soft'), 0.22, pan=-.3)
add(T['actual'] - 0.3, bank('whoosh_fast/tight'), 0.22, pan=.3); add(T['ret1'] - 0.15, bank('pro_logo_sting/swell_sting'), 0.20)
add(T['ret1'] - 0.02, bank('pro_impact/swell'), 0.25); add(T['live'], bank('pro_click/glass'), 0.3)
# chapter 01
add(T['ab'] - 0.25, bank('whoosh_big/thump'), 0.30); add(T['ab'], bank('pro_sub_drop/soft'), 0.25)
# S4 note
add(T['ab'] + 1.1, bank('swish/soft'), 0.18); add(T['sau'] - 0.1, bank('pro_pop_in/round'), 0.25)
add(T['aaj'] - 0.05, bank('swipe/paper'), 0.25); add(T['ek'], counter(T['paanch'] + 0.3 - T['ek'], 10), 0.3)
add(T['fd'] - 0.1, bank('pro_zip/up'), 0.2, pan=.4); add(T['fd'] + 0.6, bank('pro_pop_in/knock'), 0.2, pan=.4)
# S5 cards
s5 = T['zyadatar'] - 0.2
for i in range(12): add(s5 + .15 + i * .17, bank('ui_pop/step'), 0.14, pan=((i % 4) - 1.5) * .25)
add(T['laal'] - 0.05, bank('cut_hit/kick'), 0.25); add(T['wahin'] - 0.05, bank('pro_pop_in/deep'), 0.2)
# S6 question
add(T['question'] - 0.3, bank('swish/soft'), 0.22); add(T['mera3'], bank('pro_impact/air'), 0.25); add(T['question'] - .2, drone(T['aaj2'] - T['question'], 55), 0.04)
# S7 tags + FREE stamp
for i in range(3): add(T['isi'] + .25 + i * .55, bank('pro_pop_in/knock'), 0.25, pan=-.5 + .5 * i)
for i in range(3): add(T['par'] + i * .08, bank('swipe/paper'), 0.18, pan=-.5 + .5 * i)
add(T['free'] - 0.12, bank('whoosh_fast/tight'), 0.2); add(T['free'] + 0.05, bank('impact/punch'), 0.45); add(T['free'] + 0.05, bank('cut_hit/punch'), 0.3)
# S8 typewriter
for st, txt in ((T['isme'] + .1, 'No rocket science.'), (T['data'] - .1, 'Sirf data.')):
    for j, ch in enumerate(txt):
        if ch != ' ': add(st + j * .045, bank('pro_typing_key/soft' if j % 2 else 'pro_typing_key/glass'), 0.16, pan=-.2 + .4 * (j / len(txt)))
# S9 clock
k0, k1 = T['ai'] - 0.1, T['hoon2']; tt = k0
while tt < k1: add(tt, bank('pro_hover_tick/detent'), 0.12); tt += 0.07
add(k1, bank('pro_notify/ding_2167'), 0.22); add(T['video'] - 0.1, bank('swish/soft'), 0.2)
# chapter 02 + factory
add(T['step1'] - 0.35, bank('whoosh_big/thump'), 0.30); add(T['step1'] - 0.1, bank('pro_sub_drop/soft'), 0.25)
add(T['step1'] + 1.4, bank('swish/soft'), 0.18); add(T['book1'], bank('pro_impact/deep'), 0.22)

# ===== PART B (after first minute) =====
a = lambda w, after, k=1: W(w, k, after)
if LEN > 64:
    q = a('book', 63.5); add(q - .05, bank('pro_pop_in/round'), 0.25)
    for w_, af in (('saamaan', 66), ('factory', 66), ('sab', 68)): add(a(w_, af), bank('pro_pop_in/knock'), 0.22, pan=-.4)
    add(a('sab', 68) + .35, bank('pro_pop_in/knock'), 0.22, pan=-.4); add(a('karz', 69), bank('pro_pop_in/deep'), 0.25, pan=.4)
    add(a('bachega', 70) - .3, bank('whoosh_fast/tight'), 0.2); add(a('wahi', 72), bank('pro_impact/short'), 0.28)
    add(a('divide', 73), bank('pro_click/glass'), 0.25); add(a('mil', 75), bank('pro_notify/ding_2167'), 0.2)
    ex = a('example', 77); add(ex - .3, bank('swish/soft'), 0.22)
    for w_, af in (('pachaas', 79), ('tees', 80), ('bees', 83)): add(a(w_, af), bank('pro_typing_key/soft'), 0.25)
    add(a('pandrah', 85) - .1, bank('swipe/paper'), 0.25); add(a('sale', 87), bank('cut_hit/punch'), 0.3)
    so = a('socho', 88); add(so - .2, bank('swish/soft'), 0.2); add(a('price', 89), bank('downlifter/sub_sink', dur=1.2), 0.12)
    add(a('sale', 96), bank('impact/punch'), 0.35)
    pr = a('par', 98.5); add(pr - .1, bank('swish/soft'), 0.2)
    for i in range(12): add(pr + .5 + i * .18, bank('pro_hover_tick/soft'), 0.12, pan=-.3 + .05 * i)
    st = a('step', 104); add(st - .3, bank('whoosh_big/thump'), 0.28); add(st - .05, bank('pro_sub_drop/soft'), 0.22)
    add(a('list', 105), bank('pro_zip/up'), 0.15)
    qu = a('quarter', 108)
    for i in range(12): add(qu + .1 + i * .08, bank('ui_pop/step'), 0.12, pan=-.5 + i * .09)
    add(a('best', 111), bank('pro_logo_sting/swell_sting'), 0.16); add(a('rare', 118), bank('impact/punch'), 0.3)
    for w_, af in (('sasti', 115), ('peak', 117)): add(a(w_, af), bank('pro_pop_in/round'), 0.2)
    add(a('chill', 122) - .1, bank('swipe/paper'), 0.22)
    ab4 = a('ab', 126); add(ab4 - .3, bank('whoosh_big/thump'), 0.28); add(ab4 - .05, bank('pro_sub_drop/soft'), 0.22)
    add(a('sawaal', 132), bank('swipe/paper'), 0.22)
    ci = a('cian', 139)
    for j in range(9): add(ci - .1 + j * .06, bank('pro_typing_key/glass'), 0.16)
    for w_, af in (('quarterly', 141), ('growth', 143), ('hype', 148), ('doubt', 156)): add(a(w_, af), bank('pro_typing_key/double'), 0.2)
    add(a('personal', 145), bank('swipe/paper'), 0.2); add(a('hype', 148) - .6, bank('pro_riser/air_gate', dur=1.4), 0.08)
    add(a('gir', 153) - .3, bank('downlifter/sub_sink', dur=0.9), 0.14); add(a('invest', 158), bank('impact/punch'), 0.32)
    ul = a('ulta', 164); add(ul - .2, bank('swish/soft'), 0.22); add(a('kai', 166), bank('pro_click/glass'), 0.2)
    ind = a('india', 173)
    for i in range(6): add(ind + .1 + i * .15, bank('ui_pop/step'), 0.14)
    add(a('kitna', 179), bank('swipe/paper'), 0.2); add(a('tikega', 182), bank('pro_impact/air'), 0.22); add(a('haan', 184), bank('pro_notify/ding_2167'), 0.24)
    c5 = a('company', 186); add(c5 - .3, bank('whoosh_big/thump'), 0.28); add(c5 - .05, bank('pro_sub_drop/soft'), 0.22)
    add(a('khareedta', 191) + .3, bank('pro_pop_in/round'), 0.22)
    for i in range(3): add(a('tick', 193) + i * .12, bank('pro_click/glass'), 0.18)
    add(a('profit', 204), bank('pro_notify/ding_2167'), 0.24); add(a('rule', 206.5) - .2, bank('swish/soft'), 0.2)
    add(a('hold', 210), bank('pro_click/snap'), 0.2); add(a('double', 213), bank('impact/punch'), 0.3); add(a('sau', 216), bank('pro_pop_in/round'), 0.2)
    add(a('pro', 219) - .2, bank('swish/soft'), 0.2)
    for w_, af in (('update', 221), ('balance', 223)): add(a(w_, af), bank('swipe/paper'), 0.2)
    c6 = a('ab', 228.5); add(c6 - .3, bank('whoosh_big/thump'), 0.28); add(c6 - .05, bank('pro_sub_drop/soft'), 0.22)
    sl = a('saalon', 232)
    for i in range(8): add(sl + i * .35, bank('pro_hover_tick/detent'), 0.14)
    add(a('trap', 236) - .1, bank('impact/deep'), 0.3); add(a('three', 237), bank('pro_pop_in/round'), 0.2)
    rc = a('recap', 239); add(rc - .3, bank('swish/soft'), 0.2)
    for w_, af in (('ek', 240), ('do', 243), ('teen', 246), ('chaar', 249)): add(a(w_, af), bank('pro_pop_in/round'), 0.24)
    add(a('yahi', 253), bank('pro_logo_sting/swell_sting'), 0.18)
    ab7 = a('ab', 256); add(ab7 - .2, bank('swish/soft'), 0.2)
    for i in range(5): add(a('filtering', 258) + i * .25, bank('ui_pop/step'), 0.14)
    add(a('description', 262), bank('pro_notify/ding_2167'), 0.22)
    for w_, af in (('like', 265), ('subscribe', 267)): add(a(w_, af) - .1, bank('pro_pop_in/round'), 0.22)
    add(a('baar', 269) - .3, bank('pro_pop_in/knock'), 0.2)
    p8 = a('par', 272); add(p8 - .2, bank('swish/soft'), 0.2); add(a('sebi', 273) - .2, bank('pro_impact/air'), 0.2)
    th = a('thank', 281); add(th - .2, bank('pro_logo_sting/swell_sting'), 0.2)

# ---- mix ----
os.makedirs('final/stems', exist_ok=True); os.makedirs('build', exist_ok=True)
L = int(LEN * SR); sfx = mix[:L]
vo = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', 'vo/vo_full.wav', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout, np.float32)[:L]
vo = np.pad(vo, (0, L - len(vo)))
e = np.convolve(np.abs(vo), np.ones(2400) / 2400, 'same'); duck = 1 - np.clip(e / (e.max() * .25 + 1e-9), 0, 1) * .45
sfxd = sfx * duck[:, None] * .6; out = sfxd + vo[:, None]; g = .95 / (np.abs(out).max() + 1e-9)
w = lambda arr, ch, f: subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', str(ch), '-i', '-', f], input=arr.astype(np.float32).tobytes())
w(out * g, 2, 'build/mix_raw.wav')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/mix_raw.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000', 'build/mix.wav'])
if PREV:
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/video_only.mp4', '-i', 'build/mix.wav', '-t', str(PREV), '-map', '0:v', '-map', '1:a',
                    '-c:v', 'libx264', '-preset', 'medium', '-b:v', '10M', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', 'final/first_minute_preview.mp4'])
    print('preview ok'); sys.exit()
w(vo * g, 1, 'final/stems/vo.wav'); w(sfxd * g, 2, 'final/stems/sfx.wav')
name = 'final/Book_Value_Strategy.mp4'
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/video_only.mp4', '-i', 'build/mix.wav', '-map', '0:v', '-map', '1:a',
                '-c:v', 'libx264', '-preset', 'slow', '-b:v', '10M', '-minrate', '10M', '-maxrate', '10M', '-bufsize', '10M', '-x264-params', 'nal-hrd=cbr', '-pix_fmt', 'yuv420p', '-r', '30',
                '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', name])
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/video_only.mp4', '-c:v', 'copy', '-an', 'final/stems/video_only.mp4'])
print('ok', name)
