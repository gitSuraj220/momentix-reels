"""SFX for the 3-dost reel, cued from the same beat times as reel.html. earshot bank first, no bed.
writes audio/sfx_only.wav (-16 LUFS target applied in mix.py)"""
import json, os, sys
import numpy as np, soundfile as sf
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(D, '../../engine'))
from earshot_bank import bank
SR = 48000
TL = json.load(open(f'{D}/vo/timeline.json'))
B = [0] + [TL['lines'][str(i)][0] for i in range(1, 10)] + [TL['end']]
END = TL['end']
mix = np.zeros((int((END + 1) * SR), 2), np.float32)

def add(t, x, g=1.0, pan=0.0):
    i = int(max(0, t) * SR); x = x * g
    l, r = np.sqrt(0.5 * (1 - pan)), np.sqrt(0.5 * (1 + pan))
    n = min(len(x), len(mix) - i)
    if n > 0: mix[i:i + n, 0] += x[:n] * l; mix[i:i + n, 1] += x[:n] * r

def peak_at(x):  # seconds to peak (for whooshes: land peak on the cut)
    return int(np.argmax(np.abs(x))) / SR

def clink(f, g=.3, seed=0):  # coin clink (hand synth: bank lacks coins)
    t = np.arange(int(.45 * SR)) / SR
    return (sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t / d) for m, a, d in
                [(1, 1, .11), (1.48, .6, .08), (2.3, .35, .05), (3.1, .2, .035)]) * np.minimum(1, t / .001) * g).astype(np.float32)

# --- beat 1: envelopes slide in, counters
add(0.0, bank('swish/soft'), .35)
add(0.12, bank('pro_pop_in/knock'), .35, -.3); add(0.28, bank('pro_pop_in/knock'), .35, 0); add(0.44, bank('pro_pop_in/knock'), .35, .3)
add(B[1] + 3.0, bank('pro_pop/tink'), .45, -.3)
for k in range(5): add(B[1] + 3.1 + k * .26, bank('ui_pop/blip'), .18, -.3)
add(B[1] + 5.1, bank('pro_pop_in/round'), .5, .3)
for k in range(7): add(B[1] + 5.2 + k * .2, bank('ui_pop/blip'), .18, .3)
add(B[1] + 6.6, bank('pro_notify/ding_2045'), .4, .3)
# --- beat 2: three choice labels
for off, pan in [(.2, -.5), (1.3, 0), (3.0, .5)]: add(B[2] + off, bank('pro_pop_in/airy'), .45, pan)
add(B[2] + 3.0, clink(2600, .25), 1, .5)
# --- headline / scene changes (whoosh peak on the beat)
for i in range(3, 10):
    w = bank('whoosh_fast/tight'); add(B[i] - peak_at(w), w, .32)
# beat 3: chart draws in
add(B[3] + .1, bank('swish/flick'), .3)
# beat 4: 2008 crash, then gold up
add(B[4] + 3.0, bank('pro_impact/short'), .5); add(B[4] + 3.0, bank('cut_hit/sub'), .35)
add(B[4] + 5.4, bank('pro_pop/chirp'), .4, .3)
# beat 5: flat band + Nifty overtakes
add(B[5] + 2.1, bank('pro_pop_in/knock'), .4)
add(B[5] + 4.6, bank('mallet/up4'), .25, -.2)
# beat 6: COVID drop
add(B[6] + 2.7, bank('pro_impact/air'), .5)
add(B[6] + 4.8, bank('pro_pop/thup'), .4)
# beat 7: gold rocket (riser lands on the +56% card) + coins
r = bank('pro_riser/roll', dur=1.0); add(B[7] + 2.7 - len(r) / SR, r, .3)
add(B[7] + 2.7, bank('pro_notify/ding_2045'), .45, .3)
rng = np.random.default_rng(3)
for k in range(10): add(B[7] + 2.8 + k * .09, clink(1900 + rng.random() * 1500, .18, k), 1, rng.uniform(-.6, .6))
# beat 8: both fall
add(B[8] + 2.6, bank('pro_impact/short'), .4, -.2)
add(B[8] + 4.7, bank('pro_impact/short'), .4, .2)
# beat 9: final score cards (Momo, Ravi, Bunty) + shimmer
for off, sid, pan in [(.6 + .5, 'pro_pop/tink', .5), (1.8 + .5, 'pro_pop/tink', 0), (3.1 + .5, 'pro_pop/tink', -.5)]:
    add(B[9] + off, bank(sid), .5, pan)
add(B[9] + 1.1, bank('pro_shimmer/m3'), .3, .4)
add(END - 1.2, bank('pro_pop_in/round'), .25)

pk = np.abs(mix).max()
if pk > .89: mix *= .89 / pk
os.makedirs(f'{D}/audio', exist_ok=True)
sf.write(f'{D}/audio/sfx_only.wav', mix, SR, subtype='PCM_24')
print('sfx ok', round(END, 2), 'peak', round(float(np.abs(mix).max()), 3))
