"""Rich SFX for the long video (no music: Suraj adds it in editing) + stems + mix to -14 LUFS.
Outputs: final/Rupee_Dollar_Long.mp4 (VO+SFX), final/stems/{vo,sfx}.wav, final/stems/video_only.mp4"""
import sys, os, json, subprocess, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'engine'))
from earshot_bank import bank
T = json.load(open('timeline.json')); END = T['end']
SR = 48000; n = int((END + 1) * SR); mix = np.zeros((n, 2))
def add(t, s, g=1.0, pan=0.0):
    i = max(0, int(t * SR)); s = s[:max(0, n - i)]
    l, r = np.cos((pan + 1) * np.pi / 4) * 1.414, np.sin((pan + 1) * np.pi / 4) * 1.414
    mix[i:i + len(s), 0] += s * g * l; mix[i:i + len(s), 1] += s * g * r
def kaching(t, g=1.0): add(t, bank('pro_click/snap'), .45 * g); add(t + 0.04, bank('pro_notify/ding_2296'), .38 * g)
def flip(t, dur=0.8, g=1.0):  # flip-board clatter: sparse clacks, decaying
    k = 0.0
    while k < dur:
        add(t + k, bank('knock/plastic'), .16 * g * (1 - 0.5 * k / dur), pan=np.sin(k * 20) * .3); k += 0.075
    add(t + dur, bank('knock/snap'), .35 * g)
def sad(t): add(t, bank('pro_sub_drop/low'), .45)
def stamp(t, g=1.0): add(t, bank('pro_impact/deep'), .7 * g); add(t + 0.02, bank('pro_pop_in/double'), .35 * g)
def pop(t, g=1.0, pan=0.0): add(t, bank('pro_pop_in/round'), .3 * g, pan)
def bubble(t): add(t, bank('pro_pop_in/airy'), .32)
SCN = ['maza', 'bank', 'black', 'rajesh', 'priya', 'chhotu', 'theory', 'whatsapp', 'wajah', 'twist', 'strong', 'aise']
BIG = {'maza', 'rajesh', 'wajah', 'twist', 'aise'}
for i, k in enumerate(SCN):
    c = T[k] - 0.15
    if k in BIG: add(c - 0.42, bank('pro_whoosh_big/swell'), .36, pan=(-.3 if i % 2 else .3))
    else: add(c - 0.34, bank('whoosh_fast/crisp'), .26, pan=(-.4 if i % 2 else .4))
# S1 hook
add(0.0, bank('pro_impact/air'), .35); add(T['rate'] + 0.25, bank('pro_impact/short'), .55); add(T['rate'] + 0.27, bank('pro_notify/ding_2045'), .3)
pop(T['iphone'] - 0.2); add(T['gyaarah'] - 0.35, bank('swish/stick'), .3); kaching(T['gyaarah']); pop(T['dubai'], pan=-.3)
# S2 dark side
add(T['maza'], bank('pro_pop_in/knock'), .35); add(T['dark'] - 0.05, bank('pro_glitch/crunchy'), .35); add(T['dark'], bank('pro_impact/deep'), .7)
for d in range(7): add(T['hafte'] + d * 0.12, bank('knock/wood'), .26, pan=-.45 + .15 * d)
# S3 bank rush + vault
add(T['bank'], bank('pro_impact/rumble'), .4); bubble(T['mujhe']); add(T['rbi'] - 0.3, bank('pro_riser/roll', dur=0.6), .22); add(T['rbi'], bank('pro_impact/short'), .45)
pop(T['bahut']); add(T['bahattar'] - 0.4, bank('pro_typing_key/soft'), .3); add(T['bahattar'] + 0.1, bank('pro_notify/ding_1930'), .3)
for k in range(6): add(T['crores'] + k * 0.28, bank('knock/desk'), .2, pan=-.3 + .12 * k)
add(T['dopahar'], bank('mallet/glock'), .25); stamp(T['game'])
# S4 black market
add(T['black'] - 0.05, bank('pro_whoosh_big/reverse'), .3); flip(T['asli'] - 0.1, 0.8); pop(T['matlab'] - 0.3); sad(T['matlab'] + 0.2)
add(T['setting'] - 0.6, bank('whoosh_big/thump_deep'), .35); bubble(T['setting'])
# S5 Papa
bubble(T['dirham'] - 0.2); pop(T['dirham']); add(T['chhihattar'] - 0.3, bank('pro_typing_key/soft'), .3); kaching(T['chhihattar'] + 0.2)
add(T['kal'], bank('pro_typing_key/soft'), .3); add(T['aath'] - 0.1, bank('pro_sub_drop/quick'), .55); stamp(T['bigl'])
for k in range(3): pop(T['emi'] - 0.1 + k * 0.15, .8, pan=-.2 + .2 * k)
for k in range(6): add(T['kahani'] + 0.2 + k * 0.12, bank('whoosh_fast/crisp'), .12, pan=-.5 + .2 * k)
add(T['paintees'] - 0.3, bank('pro_impact/short'), .5); stamp(T['sabse1'], .8); add(T['sabse1'] + 0.05, bank('pro_notify/ding_2296'), .3)
# S6 Priya
pop(T['priya']); pop(T['dassau'] - 0.4); add(T['poore'], bank('pro_impact/short'), .55); kaching(T['poore'] + 0.05, .6)
stamp(T['tiraanve']); bubble(T['tiraanve'] + 0.6); add(T['shift'], bank('pro_whoosh_big/swell'), .3); sad(T['shift'] + 0.4)
# S7 Chhotu
pop(T['pachaas'] - 0.3); add(T['chhiyaalees'], bank('pro_impact/short'), .45); add(T['kagaz'], bank('swish/stick'), .3); pop(T['kagaz'] + 0.05)
bubble(T['kahan'] - 0.2)
# S8 Zimbabwe
add(T['zimbabwe'] - 0.2, bank('whoosh_fast/crisp'), .25); pop(T['zimbabwe'] + 0.4); add(T['barabarz'], bank('pro_notify/ding_2167'), .3)
add(T['bazaar'] - 0.3, bank('reverse_swell/dark'), .25); sad(T['bazaar'] + 0.9); add(T['kanoon'], bank('pro_impact/air'), .45)
# S9 myth
add(T['whatsapp'] - 0.1, bank('pro_notify/ding_1822'), .35); stamp(T['cap'] - 0.3); pop(T['tees'] - 0.5)
add(T['pahunche'] - 0.8, bank('pro_riser/roll', dur=1.0), .25); add(T['pahunche'] + 0.2, bank('pro_impact/short'), .45)
# S10 reasons
for k in ['mehngai', 'tel', 'jhatke']: add(T[k], bank('pro_pop_in/knock'), .4)
add(T['mehngai'] + 0.6, bank('pro_riser/roll', dur=1.0), .22); add(T['mehngai'] + 1.6, bank('pro_impact/short'), .45); add(T['america'] + 0.5, bank('pro_pop/tink'), .35)
add(T['tel'] - 0.2, bank('pro_impact/rumble'), .35); add(T['athaasi'] - 0.2, bank('pro_riser/roll', dur=0.8), .22); add(T['athaasi'] + 0.6, bank('pro_impact/short'), .45)
add(T['jhatke'] - 0.2, bank('pro_impact/deep'), .55); add(T['ikyaanve'] - 0.2, bank('whoosh_fast/crisp'), .25); add(T['sona'] - 0.3, bank('mallet/marimba'), .25)
add(T['jung'] - 0.3, bank('pro_impact/rumble'), .45); pop(T['jung']); pop(T['investors']); sad(T['investors'] + 0.3)
flip(T['may'], 0.9); add(T['may'] + 0.95, bank('pro_impact/deep'), .6)
# S11 twist
add(T['twist'] - 0.15, bank('pro_glitch/fastroll'), .3); stamp(T['twist'] - 0.1, .9); add(T['yen'] - 0.4, bank('whoosh_fast/crisp'), .25)
add(T['amir'] - 0.3, bank('pro_notify/ding_2045'), .35); pop(T['number'] - 0.2); add(T['turkey'] - 0.2, bank('whoosh_fast/crisp'), .25)
for k in range(6): add(T['zero'] - 0.2 + k * 0.13, bank('pro_typing_key/soft'), .3)
add(T['naya'] - 1.6, bank('whoosh_fast/crisp'), .25); add(T['priya2'] + 0.5, bank('pro_sub_drop/quick'), .5)
# S12 strong
add(T['strong'] - 0.4, bank('pro_whoosh_big/swell'), .3); add(T['nawaasi'] - 0.2, bank('pro_riser/roll', dur=0.9), .22); add(T['nawaasi'] + 0.7, bank('pro_impact/short'), .45)
for k in ['made', 'tel2', 'control', 'bane']: pop(T[k] - 0.3, 1.1)
# S13 end
add(T['aise'] - 0.2, bank('pro_impact/air'), .4); add(T['kamaana'] - 0.1, bank('pro_impact/deep'), .75); add(T['kamaana'], bank('mallet/flourish'), .3)

os.makedirs('final/stems', exist_ok=True)
sfx = mix[:int(END * SR)]
vo = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', 'vo/vo_full.wav', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                                  capture_output=True).stdout, np.float32)[:len(sfx)]
vo = np.pad(vo, (0, len(sfx) - len(vo)))
e = np.convolve(np.abs(vo), np.ones(2400) / 2400, 'same'); duck = 1 - np.clip(e / (e.max() * .25), 0, 1) * .4
sfxd = sfx * duck[:, None] * .6
out = sfxd + vo[:, None]; pk = np.abs(out).max(); g = .95 / pk
w = lambda arr, ch, f: subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', str(ch), '-i', '-', f], input=arr.astype(np.float32).tobytes())
w(sfx, 2, 'build/sfx_only.wav'); w(out * g, 2, 'build/mix_raw.wav')
# stems at the same gain as the mix, so they line up with the final when Suraj adds music
w(vo * g, 1, 'final/stems/vo.wav'); w(sfxd * g, 2, 'final/stems/sfx.wav')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/mix_raw.wav', '-af', 'loudnorm=I=-14:TP=-2.2:LRA=11', '-ar', '48000', 'build/mix.wav'])
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/video_only.mp4', '-i', 'build/mix.wav', '-map', '0:v', '-map', '1:a',
                '-c:v', 'libx264', '-preset', 'slow', '-b:v', '12M', '-minrate', '10M', '-maxrate', '14M', '-bufsize', '24M', '-x264-params', 'nal-hrd=vbr', '-pix_fmt', 'yuv420p',
                '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', 'final/Rupee_Dollar_Long.mp4'])
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'build/video_only.mp4', '-c:v', 'copy', '-an', 'final/stems/video_only.mp4'])
print('ok')
