# AI Bubble long video — HANDOFF (two Claude accounts)

Read CLAUDE.md and `.claude/skills/momentix-reels/SKILL.md` first. Channel rules apply unless this file says otherwise.

## Who does what
| Account | Has access to | Owns |
|---|---|---|
| **A — art director** (Suraj's main Claude) | GitHub, Higgsfield, ElevenLabs, Chrome, Suraj's Mac | Style lock, all Higgsfield images (`art/`), all voice (`vo/`), word timings, final QC |
| **B — animator** (second Claude account) | GitHub only | The reusable player, every shot's animation, SFX, render, mix, cover frame |

A never edits B's code; B never generates images or voice. Talk through commits + the STATUS table below.

## Sources of truth
- Script (VO text): `script_suraj_v2.md` (Suraj approved the flow; later edits live in the doc).
- Shot list (VO line | visual | asset, 167 shots): Claude Doc "AI Bubble — VO + Visual Script"
  https://claude.ai/artifact/VBtfwBRxvWDUf7t5xstV53 . Suraj: share it with account B, or Export → Markdown and commit it here as `shots.md`.
- Decisions (Suraj, 15 Nov 2026): Hinglish, global angle, 4–5 skits, real brand logos allowed, NO real-person likeness
  (Sam-type = generic young exec in grey sweater; Nvidia CEO = generic cartoon in black leather jacket with "NVIDIA CEO" label;
  Gemini–Modi joke is text-only on a chat screen; YC pitch uses an ORIGINAL dark wizard; shot 142 uses an ORIGINAL giant dinosaur monster).

## Specs
- **THIS IS A LONG-FORM YOUTUBE VIDEO (~10–12 min), LANDSCAPE 16:9.** It overrides the 1080x1920 Shorts default in CLAUDE.md.
  Every image, layout, text size and the player canvas are 1920x1080. Not a Short/Reel; no vertical crop.
- Cover = YouTube thumbnail 1280x720 (16:9), not a 9:16 reel cover. Chapters at each section start (00:00 Hook …) for the description.
- 1920x1080, 30 fps, 8–12 Mbps H.264, AAC 256k. Voice + SFX mastered to -14 LUFS, true peak <= -1 dBTP. No BGM (Suraj adds it).
- Something moves every 0.5 s. One shot per VO line (avg 2–4 s).
- Look (Suraj, 15 Nov): **cinematic 2.5D** — same round-white-head cartoon characters with bold outlines, but deep lighting,
  every HF shot split into 3 parallax layers (bg / mid / fg), camera dolly + push-ins, depth blur on bg, light rays/dust, film grain + vignette.
- Pace: **fast, ~9 min** (Gen-Z cuts). Narration is generated at a quick pace; shots cut on word times.
- On-screen text: **only key words + every number** (big counters, punch words). No full subtitles.
- No channel intro — open straight on the hook. End screen 20 s (shot 167).
- SFX: **heavy cinematic** — whoosh every cut, risers into reveals, impacts on numbers, foley in skits, room tone per scene.
- Voices: narrator = Suraj's clone; skits = Gaurav / Amrut / Devi, Suraj's clone may also play a skit role.
- Section 10: Suraj chose **"do tarah ke"** — two trigger cards only; card 3 and the dinosaur monster are dropped (shot 142 = two cards).
- Thumbnail: decide later.

## What A delivers (into this folder)
- `art/style_frame.png`, `art/character_sheet.png` (style lock).
- `art/sNNN.png` — one image per HF shot (NNN = shot number in the doc; shared images are listed in `art/index.json` as {"shot": file}).
  Where a shot needs layers: `art/sNNN_bg.png` + `art/sNNN_fg.png` (background removed).
- `vo/narration_*.mp3` (Suraj's cloned voice, best ElevenLabs model available), `vo/skit_*.mp3` (Gaurav / Amrut / Devi),
  `vo/words_*.json` (faster-whisper word times), and `timeline.json` = {shot: [start, end]} + cue times. A builds this with `build_vo.py`.

## What B builds
1. `player/` — ONE reusable Canvas/HTML player (`renderAt(t)`, `window.READY`, like `projects/nvidia-ceo-reel/reel.html`) that reads
   `shots.json` and draws each shot from a small set of templates:
   - `image` — HF still with Ken Burns / parallax (bg + fg), optional blink/mouth flap on characters, shake, whip-pan.
   - `counter` — big number roll (₹/$, Indian commas), `bars` (green/red), `split` (block splits into parts), `race` (runners/rocket),
     `chat` (phone chat UI typing), `tweet` (card), `calendar` (page flip), `stamp`, `title` (neon / black card), `balloon` (the AI bubble: inflate, crack, tighten), `cards` (numbered flip cards), `logos` (logo tiles).
   - Captions off by default (Suraj decides).
2. `shots.json` from the shot list: {id, start, end, template, params}. Timings come from A's `timeline.json`.
3. SFX with `engine/earshot_bank.py` like `projects/nvidia-ceo-reel/sfx.py` (whooshes on cuts, risers before reveals, impacts on numbers, record scratch at shot 73, crack at 96, mosquito buzz at 121).
4. Render with `render.py` (parallel chunks), mix with `mix.py` (duck SFX under voice, loudnorm -14), cover frame.
5. QA: snapshot grid every section (`snap.py`), check no text under 40 px, nothing outside 16:9 safe area, every number matches the doc.

## Order of work
A: style lock → Suraj approves → narration + skits → timeline.json → images section by section (commit after each).
B: player + templates with placeholder art and a placeholder timeline FIRST (doesn't need A) → swap in real art/timeline as A commits.

## Repo rules
- Commit to `main`, small commits, message prefix `ai-bubble:`. Never commit MP4/WAV (see .gitignore); mp3 + png are fine.
- End commit messages with the attribution lines your session asks for.

## STATUS (update when you finish something)
| Item | Owner | State |
|---|---|---|
| Script v2 | A | done |
| Shot list doc | A | done (share/export pending — Suraj) |
| Style frame + character sheet | A | done (art/) |
| Narration + skit voices | A | done (vo/vo_full.wav, 10:37) |
| timeline.json | A | done (50 VO segments; shot-level split = B maps doc shots onto segments) |
| HF images (≈70) | A | done — all sections (81 files in art/, see art/index.json) |
| Player + templates | B | done (player/: 30 templates, 0 errors on all 167 shots; HF shots without art show a labelled placeholder) |
| shots.json | B | done (make_shots.py; rerun after new art lands, it picks up art/sNNN.png automatically) |
| SFX, render, mix, 16:9 thumbnail frame | B | todo |
