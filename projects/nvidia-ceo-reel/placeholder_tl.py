"""Placeholder timeline (before real VO): estimate each line from its word count -> timeline.js.
build_vo.py overwrites timeline.js with real take timings later."""
import json, os
D = os.path.dirname(os.path.abspath(__file__))
LINES = [('M1', 'Papa, aapko pata hai? Nvidia ka share is hafte kareeb terah percent gir gaya!'),
         ('P1', 'Arre, par kaise?'),
         ('M2', 'Nvidia ke CEO Jensen Huang ke affair ki news aayi. Isliye share neeche aa gaya.'),
         ('P2', 'Achha beta, par isse apan ko kya fayda?'),
         ('M3', 'Dekho papa, aisi news market mein aati rehti hain. CEO ke affair se company ka business abhi tak na ruka hai, na hi profit. Share abhi zyada tar sentiment ki wajah se gira hai.'),
         ('P3', 'Toh phir kya ye iske share mein invest karne ka mauka hai?'),
         ('M4', 'Ho sakta hai. Par risk bhi hai, toh pehle khud samjho, phir faisla lo.'),
         ('P4', 'Par beta, America ka share hum lenge kaise?'),
         ('M5', 'Main batata hoon. IND money ka app use karke aap aaraam se US shares mein directly invest kar sakte ho. Puri process ke liye comment karo STOCK.')]
t, TL = 0.3, {}
for k, s in LINES:
    d = len(s.split()) * 0.31 + 0.35
    TL[k] = [round(t, 3), round(t + d, 3)]; t += d + 0.28
END = round(t + 1.2, 3)
open(f'{D}/timeline.js', 'w').write(f'window.TL={json.dumps(TL)};\nwindow.CUE={{}};\nwindow.END={END};\n')
print(END, TL)
