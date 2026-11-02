# BUILD BRIEF — "Google ke 10 Free AI Vibe Coding Tools" (for the second Claude session)

You are building ONLY the picture (animation → `build/video_only.mp4`). Voice, timeline, SFX, mix, cover and scheduling are done in the main session.

## Read first
- `CLAUDE.md` (repo root) and `.claude/skills/momentix-reels/SKILL.md` §8a (monetization guard).
- `projects/google-free-ai-tools/script.md` — the 8 beats.
- Template to copy: `projects/nexon-4-fuel/{reel.html, build.py, render.py}` — HTML/DOM → Playwright `renderAt(t)` (async) → ffmpeg. Same pipeline, same render settings (1.25× device scale, lanczos to 1080×1920, 30 fps, libx264 crf 15).
- Timing: `projects/google-free-ai-tools/vo/timeline.json` (lines 1–8 start/end, chunks for word-by-word captions). Use `TL.lines[n][0]` for beat starts and `TL.chunks` for captions. Never hard-code seconds.

## Look (match the reference reel, but our own build)
- Clean editorial: alternating WHITE soft-gradient cards (#F4F4F2 → #E6E6E3) and BLACK cards (#050505 with faint dot-particle field).
- Big italic serif titles (Lora Italic 600, ~120 px, black on white / white on black) that slide/scale in: "AI Code Editor", "AI App Builder", "AI UI Designer", "No-Code AI Apps".
- Word-by-word captions: Poppins Bold 56 px, white text in a dark translucent rounded box (rgba(40,40,40,.72), radius 10, padding 6/16), centred at y≈1500 — one chunk at a time from `TL.chunks`, pop-in 0.12 s.
- Something moves every 0.5 s: card push-ins (1.0→1.06), logo pop (back-ease), parallax, typing cursors, blur-whip transitions (8 frames, motion blur via CSS filter blur + translateX).
- Real tool logos ARE allowed for this video (Suraj's exception): Google "G", Antigravity, AI Studio, Stitch, Opal, Jules, n8n, Lovable, Gemini Notebook, Code Wiki, Flow Music. Draw them as clean SVG recreations or use official press/brand assets saved to `projects/google-free-ai-tools/assets/logos/`. No real people, no founder clip.
- Momo (our character, `characters/momo/`): small cutout bottom-left in beats 1 and 7 only — shocked (1), pointing down at "Comment AI" (7). Momo is a curious user, never an expert.

## Beats (start = TL.lines[n][0]; 7 beats, ~29 s — Jules was cut by Suraj)
Voice is final: `vo/vo.mp3` (Amrut, take A, pauses tightened). Captions = `TL.chunks` (word groups) — show exactly that text.
1. Hook (0–6.5 s) — "ChatGPT aur Claude sab use karte hain… par Google ne chupchaap 10 free AI coding tools nikaale hain!" Google "G" centre, 8–10 tool icons orbit on a dashed circle (like ref 0:03); ChatGPT + Claude chips slide in then get dimmed/pushed aside when "par Google" lands; big "10 FREE AI CODING TOOLS". Momo shocked, bottom-left.
2. Antigravity — black card, logo glows in, title "AI Code Editor"; RICH mockup: editor window, prompt box types "Login wala e-commerce page banao" → split view: shop page renders on the left, code streams on the right. "Cursor jaisa" can flash a small "≈ Cursor" chip.
3. AI Studio — black card "Google AI Studio" + "ai.studio/build"; RICH mockup: Build mode prompt → an app preview (e.g. image-caption or chatbot app) pops in within 1 s, timer chip "3 sec".
4. Stitch — black card "Stitch BETA" → white card, italic title "AI UI Designer", 3 phone screens slide in (finance app in dark mode) + a "</> Export code" button press.
5. Opal — white card: n8n logo + Lovable logo slide together and merge into "Opal"; RICH mockup: 4 workflow nodes (Input → Gemini → Veo 3 → Output) connect with animated lines; "No code" chip.
6. "12 mein se sirf 4" — fast horizontal icon carousel with motion blur (Gemini Notebook, Code Wiki, Flow Music, Jules, Mixboard, Pomelli…); big counter "4 / 12" ticking.
7. CTA (to TL.end) — white card, huge "Comment  AI" with pulsing comment bubble + arrow down; Momo points down. Hold to the end.
Small print from beat 2 to end (20 px, 50% opacity, bottom): "Free tiers have limits and can change. Checked 2 Nov 2026."
Momo appears ONLY in beats 1 and 7.

## Output
- `projects/google-free-ai-tools/build/video_only.mp4` (1080×1920, 30 fps, length = TL.end, no audio).
- Contact sheet `build/sheet.jpg` (12 frames) for review.
- Commit code (not mp4/png renders — see .gitignore) and push. Copy the mp4 to `~/Downloads/GoogleAI/video_only.mp4` on Suraj's Mac.
