"""Suraj's 16:9 edit (trading_trap.mp4) -> 9:16 Reel: blurred fill, centred video, hook headline, word-timed captions."""
import os, subprocess
D = os.path.dirname(os.path.abspath(__file__)); SRC = '/mnt/user-data/uploads/trading_trap.mp4'; END = 84.5
G, RD, YL, CY = r'{\c&H7AE03E&}', r'{\c&H5C3BFF&}', r'{\c&H00D4FF&}', r'{\c&HFFE838&}'; Wt = r'{\c&HFFFFFF&}'
CAPS = [(3.12, 'INDIA MEIN ' + YL + '2 CRORE'), (4.88, 'F&O TRADERS'), (6.14, 'HAR 100 MEIN SE'), (7.7, 'SIRF ' + G + '1 PROFIT' + Wt + ' MEIN'),
 (9.64, '100 LOG TRADE KARTE HAIN'), (11.04, RD + '99 KO LOSS'), (13.26, 'AUR ' + G + '1 KO PROFIT'), (14.8, 'PAR AISA KYUN?'),
 (16.46, 'ISKE PEECHHE'), (17.04, 'EK BAHUT BADA SYSTEM'), (18.86, 'SYSTEM OF ' + CY + 'HFTs'),
 (21.9, 'AAPKO LAGTA HOGA'), (23.04, 'TRADE AISE HOTA HOGA…'), (27.82, 'PAR ' + CY + 'REALITY' + Wt + ' MEIN…'),
 (30.76, 'ISE KEHTE HAIN'), (32.34, CY + 'HIGH FREQUENCY TRADING'), (34.2, 'JAB AAP TRADING KARTE HO'), (35.74, 'AUR ' + G + 'BUY' + Wt + ' DABATE HO'),
 (37.78, 'AAPKE OPPOSITE MEIN'), (38.92, 'YE ' + CY + 'GIANTS'), (39.56, 'APNI ' + CY + 'ALGORITHM' + Wt + ' SE TRADE'),
 (42.12, 'SYSTEM FAST BANANE KE LIYE'), (44.32, 'SERVERS EXCHANGE KE'), (45.92, YL + 'DATA CENTRE KE ANDAR'),
 (47.92, 'AUR TEZ PRIVATE'), (48.9, CY + 'NETWORK LINES'), (51.08, 'NANOSECONDS KA DELAY BHI'), (52.9, RD + 'MANZOOR NAHI'),
 (53.48, 'EK REPORT KE HISAAB SE'), (55.1, 'EK SAAL MEIN'), (56.2, 'IN FIRMS NE'), (56.88, G + '$7 BILLION' + Wt + ' KA PROFIT'),
 (60.42, 'SAME UTNA HI PAISA'), (61.78, 'INDIAN TRADERS NE'), (62.76, RD + 'LOSS MEIN GAWAYA'),
 (64.64, 'KYUNKI INDIA MEIN'), (65.34, 'OFFICE WALA'), (66.48, 'CHAI WALA'), (67.34, 'AUTO-RICKSHAW WALA'), (68.42, 'SAB TRADE KAR RAHE HAIN'),
 (69.86, 'AUR INKE CHANCES'), (70.48, CY + 'HFT FIRMS' + Wt + ' KE SAAMNE'), (72.28, RD + 'NULL'),
 (74.42, 'TOH EK CHHOTI SI REQUEST'), (77.56, 'BINA PROPER KNOWLEDGE'), (78.44, 'AUR LEARNING KE'), (79.28, 'APNI MEHNAT KI KAMAI'),
 (80.66, 'IS MARKET MEIN'), (81.52, YL + 'MAT LAGANA'), (82.16, 'THANK YOU')]
def ts(t): h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60; return f'{h}:{m:02d}:{s:05.2f}'
ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "WrapStyle: 2", "",
 "[V4+ Styles]", "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
 "Style: Cap,Poppins ExtraBold,74,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,7,3,5,40,40,0,1",
 "Style: Head,Anton,118,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,6,0,5,40,40,0,1",
 "Style: Fine,Poppins ExtraBold,30,&H00B0A69A,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,2,0,1,2,0,5,40,40,0,1",
 "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
pop = r'{\pos(540,1400)\fscx78\fscy78\t(0,110,\fscx106\fscy106)\t(110,190,\fscx100\fscy100)}'
for i, (t, s) in enumerate(CAPS):
    e = min(CAPS[i + 1][0] if i + 1 < len(CAPS) else END, t + 2.6)
    ass.append(f'Dialogue: 1,{ts(t)},{ts(e)},Cap,,0,0,0,,{pop}{s}')
ass.append(f'Dialogue: 0,{ts(0)},{ts(END)},Head,,0,0,0,,' + r'{\pos(540,400)\fad(200,0)}100 MEIN SE SIRF 1')
ass.append(f'Dialogue: 0,{ts(0)},{ts(END)},Head,,0,0,0,,' + r'{\pos(540,535)\fad(200,0)\c&H7AE03E&}PROFIT MEIN KYUN?')
ass.append(f'Dialogue: 0,{ts(0)},{ts(END)},Fine,,0,0,0,,' + r'{\pos(540,1292)}Sirf jaankari ke liye')
open(f'{D}/caps.ass', 'w').write('\n'.join(ass) + '\n')
os.makedirs(f'{D}/final', exist_ok=True)
fc = ("[0:v]split[a][b];[a]scale=-2:1920,crop=1080:1920,boxblur=30:3,eq=brightness=-0.18:saturation=1.2[bg];"
      "[b]scale=1080:608[fg];[bg][fg]overlay=0:656,"
      "drawbox=x=0:y=654:w=1080:h=2:color=0x38e8ff@0.5:t=fill,drawbox=x=0:y=1264:w=1080:h=2:color=0x38e8ff@0.5:t=fill,"
      f"ass={D}/caps.ass:fontsdir={D}/fonts[v]")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', SRC, '-filter_complex', fc, '-map', '[v]', '-map', '0:a', '-t', str(END),
                '-af', 'loudnorm=I=-14:TP=-1.5:LRA=9', '-ar', '48000', '-c:v', 'libx264', '-preset', 'medium', '-b:v', '10M', '-maxrate', '12M',
                '-bufsize', '20M', '-pix_fmt', 'yuv420p', '-r', '30', '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart',
                f'{D}/final/HFT_Reel_9x16.mp4'], check=True)
print('ok')
