# Momentix by Suraj — reel engine

This repo holds everything for the Momentix by Suraj Hinglish Shorts/Reels channel (YouTube, Instagram, Facebook).
Suraj gives all orders in one chat. At the start of a session, read these two skills:

- `.claude/skills/momentix-reels/SKILL.md` — channel rules, SEO-first titles/descriptions, upload + scheduling flow.
- `.claude/skills/video-script/SKILL.md` — ideas + scripts from analytics; its profile is `video-script/profile.md` (use instead of ~/.video-script/profile.md).
- `.claude/skills/animated-video/SKILL.md` — Remotion animation pipeline (from cstack by Charles Zheng, MIT).

## Layout
- `engine/` — HTML/SVG → Playwright render scripts, `audio_lib.py` SFX synth, align/mix/cover scripts, Poppins fonts.
- `characters/momo/` — Momo (glass bulb head, navy hoodie) sheets and cutouts. Bunty: curly hair, black tee, joggers.
- `projects/<reel>/` — one folder per reel: `reel.html` (or Remotion src), render/sfx scripts, timeline/cues, cover.

## Standing rules (short)
- Quality over quantity, premium animation, save credits (code animation first, Higgsfield only for key shots).
- Export 1080×1920, 30 fps, 8–12 Mbps. Something moves every 0.5 s.
- Money content: "Sirf jaankari ke liye" in description + caption. No real-person caricatures, no trademark logos.
- IG captions never name Suraj or the YouTube channel.
- YouTube title starts with the exact English search phrase, then the Hinglish hook.
- Suraj uploads videos himself; Claude fills details and schedules (6 PM IST default). Never type passwords.
- Don't commit MP4/WAV renders (see .gitignore); finished videos go to ~/Downloads/<Project>/ on Suraj's Mac.
