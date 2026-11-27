"""Mask Suraj's raw Kite recording: keep only the P&L % pill; hide names, amounts, client ID, other apps.
usage: python3 mask.py  (reads ref/raw.mp4, writes footage/zerodha_masked.mp4, source 13.2-28.3 s)"""
import subprocess
T0, T1 = 13.2, 28.3
BLUR = [(0, 0, 1640, 2360, 13.2, 16.3), (0, 280, 1640, 1980, 21.9, 24.0), (0, 660, 1640, 1530, 24.0, 28.3)]
BOX = [(60, 360, 620, 62, 24.0, 28.3), (1290, 360, 300, 62, 24.0, 28.3), (1150, 468, 278, 66, 24.0, 28.3), (1320, 2140, 320, 72, 24.0, 28.3), (1360, 2200, 280, 140, 19.4, 28.3)]
f = [f"[0:v]trim={T0}:{T1},setpts=PTS-STARTPTS,fps=30,format=rgb24[v0]"]; cur = 'v0'
for i, (x, y, w, h, a, b) in enumerate(BLUR):
    a -= T0; b -= T0
    f.append(f"[{cur}]split[{cur}a][{cur}b]")
    f.append(f"[{cur}b]crop={w}:{h}:{x}:{y},scale={w//24}:{h//24},scale={w}:{h}:flags=bicubic,gblur=sigma=10[r{i}]")
    f.append(f"[{cur}a][r{i}]overlay={x}:{y}:enable='between(t,{a:.3f},{b:.3f})'[v{i+1}]"); cur = f'v{i+1}'
for j, (x, y, w, h, a, b) in enumerate(BOX):
    a -= T0; b -= T0
    f.append(f"[{cur}]drawbox=x={x}:y={y}:w={w}:h={h}:color=0xE4E6EC@1:t=fill:enable='between(t,{a:.3f},{b:.3f})'[b{j}]"); cur = f'b{j}'
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'ref/raw.mp4', '-filter_complex', ';'.join(f), '-map', f'[{cur}]', '-an', '-c:v', 'libx264', '-crf', '14', '-preset', 'medium', '-pix_fmt', 'yuv420p', 'footage/zerodha_masked.mp4'], check=True)
