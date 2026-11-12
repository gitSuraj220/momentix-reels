"""Join chosen takes (a1_1, d1_1, a2_2, d2_1, a3a_2, a3b_1) with breathing gaps -> vo/vo48.wav,
and write timeline.js (scene starts TL + scene-relative CUE times) for reel.html."""
import json, os, subprocess
import numpy as np, soundfile as sf
D = os.path.dirname(os.path.abspath(__file__)); SR = 48000
CH = ('highpass=f=80,equalizer=f=250:t=q:w=1:g=-2.5,equalizer=f=3000:t=q:w=1.2:g=4,highshelf=f=7000:g=2,'
      'acompressor=threshold=-24dB:ratio=4:attack=4:release=70:makeup=3')
LEAD = 0.5
# part, take, gap after part, [(word-start time in take where an extra pause is inserted before, pause s)]
PARTS = [('a1', 'a1_1', .7, [(20.14, .8), (32.48, .5)]),
         ('d1', 'd1_1', .45, []),
         ('a2', 'a2_2', .7, [(3.16, .5), (17.1, .5), (25.74, .4), (37.68, .6), (58.96, .5)]),
         ('d2', 'd2_1', .45, []),
         ('a3a', 'a3a_2', .6, [(7.74, .8), (15.17, .5), (23.98, .4), (29.8, .4), (36.3, .4), (42.82, .4), (51.86, .4), (58.3, .4)]),
         ('a3b', 'a3b_1', 2.2, [(1.7, .3), (9.22, .3), (14.12, .3), (17.38, .3), (22.38, .8), (35.66, .6)])]
# scene anchors: scene -> (part, time in take)
SC = {'hook': ('a1', 0), 'sipdef': ('a1', 20.14), 'units': ('a1', 32.48), 'devi1': ('d1', 0), 'mftitle': ('a2', 0), 'tokri': ('a2', 3.16),
      'cats': ('a2', 17.1), 'rank': ('a2', 25.74), 'cars': ('a2', 37.68), 'fall': ('a2', 58.96), 'devi2': ('d2', 0), 'answer': ('a3a', 0),
      'appintro': ('a3a', 7.74), 'st1': ('a3a', 15.17), 'st2': ('a3a', 23.98), 'st3': ('a3a', 29.8), 'st4': ('a3a', 36.3), 'st5': ('a3a', 42.82),
      'st6': ('a3a', 51.86), 'bas': ('a3a', 58.3), 'galti': ('a3b', 0), 'recap': ('a3b', 22.38), 'like': ('a3b', 35.66)}
CUES = {'hook': {'h_chalu': ('a1', 5.42), 'h_samajh': ('a1', 7.84), 'h_ye': ('a1', 9.46), 'h_doubt': ('a1', 12.38)},
        'sipdef': {'d_har': ('a1', 25.18), 'd_apne': ('a1', 27.9)},
        'units': {'u_fayda': ('a1', 37.36), 'u_neeche': ('a1', 39.68), 'u_upar': ('a1', 43.84), 'u_long': ('a1', 47.12)},
        'tokri': {'t_hazaar': ('a2', 5.44), 't_expert': ('a2', 8.42), 't_units': ('a2', 14.7)},
        'cats': {'c_0': ('a2', 22.64), 'c_1': ('a2', 23.6), 'c_2': ('a2', 24.6)},
        'rank': {'r_100': ('a2', 26.28), 'r_101': ('a2', 28.82), 'r_251': ('a2', 33.08)},
        'cars': {'k_suv': ('a2', 39.08), 'k_sedan': ('a2', 47.04), 'k_bike': ('a2', 52.04)},
        'fall': {'f_ghabra': ('a2', 64.04)},
        'answer': {'a_kam': ('a3a', .3), 'a_zyada': ('a3a', 3.42)},
        'appintro': {'ai_6': ('a3a', 10.05), 'ai_har': ('a3a', 11.19)},
        'st1': {'k1_ek': ('a3a', 21.57)}, 'st3': {'k3_sip': ('a3a', 31.02), 'k3_amt': ('a3a', 33.78)},
        'st4': {'k4_salary': ('a3a', 38.1)}, 'st5': {'k5_upi': ('a3a', 44.9), 'k5_approve': ('a3a', 48.0)}, 'st6': {'k6_confirm': ('a3a', 52.88)},
        'galti': {'g_0': ('a3b', 1.7), 'g_1': ('a3b', 9.22), 'g_2': ('a3b', 14.12), 'g_3': ('a3b', 17.38)},
        'recap': {'rc_0': ('a3b', 23.32), 'rc_1': ('a3b', 26.94), 'rc_2': ('a3b', 28.72), 'rc_3': ('a3b', 30.52), 'rc_4': ('a3b', 32.96)},
        'like': {'l_sub': ('a3b', 37.98)}}

def load(take):
    out = f'{D}/vo/{take}_c.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{D}/vo/{take}.mp3', '-ac', '1', '-ar', str(SR), '-af', CH, out], check=True)
    return sf.read(out)[0]

pieces, t, maps = [np.zeros(int(LEAD * SR))], LEAD, {}
for part, take, gap_after, gaps in PARTS:
    x = load(take); W = json.load(open(f'{D}/vo/words_{take}.json'))
    cuts = []
    for ws, g in gaps:   # cut in the silence between the previous word's end and this word's start
        prev = max([w[1] for w in W if w[1] <= ws + .01] or [ws - .1]); cuts.append(((prev + ws) / 2, g))
    start, prev_i, add = t, 0, []
    for c, g in cuts:
        i = int(c * SR); pieces += [x[prev_i:i], np.zeros(int(g * SR))]; prev_i = i; add.append((c, g))
    pieces.append(x[prev_i:]); pieces.append(np.zeros(int(gap_after * SR)))
    maps[part] = (start, add)
    t = start + len(x) / SR + sum(g for _, g in add) + gap_after

def at(part, tt):
    s, add = maps[part]; return round(s + tt + sum(g for c, g in add if tt > c), 3)

y = np.concatenate(pieces); sf.write(f'{D}/vo/vo48.wav', y.astype(np.float32), SR)
order = list(SC)
TL = {}
for i, k in enumerate(order):
    a = at(*SC[k]) - (0 if k == 'hook' else .15)
    TL[k] = [0 if k == 'hook' else round(a, 3), None]
for i, k in enumerate(order):
    TL[k][1] = TL[order[i + 1]][0] if i + 1 < len(order) else round(len(y) / SR, 3)
CUE = {}
for sc, d in CUES.items():
    for k, v in d.items(): CUE[k] = round(at(*v) - TL[sc][0], 3)
open(f'{D}/timeline.js', 'w').write('window.TL=' + json.dumps(TL) + ';\nwindow.CUE=' + json.dumps(CUE) + ';\n')
json.dump({'TL': TL, 'CUE': CUE, 'END': round(len(y) / SR, 3)}, open(f'{D}/timeline.json', 'w'), indent=1)
print('vo', round(len(y) / SR, 2), 's'); print(TL)
