"""SFX-only master (Suraj adds music): SFX at -18 LUFS so music has headroom, true peak <= -1 dBTP; mux with video."""
import os, subprocess
D = os.path.dirname(os.path.abspath(__file__))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{D}/audio/sfx_only.wav', '-af', 'loudnorm=I=-18:TP=-1.5:LRA=11,aresample=48000', '-t', '20.9', f'{D}/audio/mix_ln.wav'], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{D}/build/video_only.mp4', '-i', f'{D}/audio/mix_ln.wav',
                '-c:v', 'libx264', '-preset', 'slow', '-b:v', '10M', '-maxrate', '12M', '-bufsize', '20M', '-pix_fmt', 'yuv420p',
                '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', '-shortest', f'{D}/final/SIP_Underwater_Reel.mp4'], check=True)
print('muxed final/SIP_Underwater_Reel.mp4')
