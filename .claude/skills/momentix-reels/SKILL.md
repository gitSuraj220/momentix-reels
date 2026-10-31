---
name: "momentix-reels"
description: "Make, schedule and analyze Momentix by Suraj Hinglish YouTube Shorts and Instagram Reels end to end: animation-first visuals, ElevenLabs voice, mix, cover, Metricool."
---

# Momentix Reels pipeline (YouTube Shorts + Instagram Reels)

Channel: **Momentix by Suraj** — YouTube `UC7CsAnrzevaMh-aCbNkaaFg` (@SURU2200, a *Brand Account* under suraj220.kr@gmail.com), Instagram **@momentixbysuraj** (Creator), Facebook page **Momentix By Suraj**. Faceless, Hindi voice (or pure animation), Roman-Hinglish captions. **Animation-first** (since Oct 2026). No stock footage, no real people's likeness.

The helper scripts (align.py, build_scene.py, render.py, snapmany.py, sheet.py, audio_lib.py, mix.py, render_cover.py, lib.js, head.html, tail.js), example frames and Poppins fonts ship in the `momentix-reels.zip` package; unpack it and use its folder as `<skill>`. Work in a fresh folder per video. Make a task list; send drafts (script, preview frames, video) as soon as they exist. Ask before anything public; once Suraj says "post/schedule", do it and report.

| # | Step | Suraj's checkpoint |
|---|---|---|
| 1 | Topic research (trending + facts with sources) | picks / OKs topic |
| 2 | Script (hook + body + loop ending), Roman + Devanagari | approves script — never generate voice before this |
| 3 | ElevenLabs voice (Chrome) → `vo.mp3` | listens once |
| 4 | Align voice → `timeline.json` | — |
| 5 | Hook clip + `frame.js` → build → audit contact sheets → fix | — |
| 6 | Render + SFX/music + mix (-14 LUFS) + mux | reviews MP4 |
| 7 | Cover (Reel cover = Shorts thumbnail) | — |
| 8 | **SEO** title/description/tags + IG caption | — |
| 9 | Schedule (Studio + Business Suite, or Metricool) | says "post"/"schedule" |
| 10 | Analytics (Metricool + Studio/IG fallback) | — |

---
## 1. Topic
* Best performers: **"how does this work" mechanisms on a current hook**, and **simple money/trading lessons told as a visual metaphor** (SIP 25 vs 35 coin balls, stop-loss tide). Political controversy flopped. Pair the trend with a **useful payoff** that earns saves/shares.
* Research with WebSearch (extended for recent events). Note numbers + source + month. Never assert a contested claim as fact.
* **Political/news topics:** neutral only. No politician faces/logos, no party branding, no real-person caricatures.
* **Health topics:** stable facts only, cite WHO/MoHFW, add "sirf jaankari ke liye, doctor se salah lein".
* **Money/trading topics:** "Sirf jaankari ke liye, investment/trading advice nahi" in description + caption (in-video only if Suraj wants it). Show example returns as "example", never guaranteed.

## 2. Script (target 35–45 s; pure-animation reels 13–16 s)
1. **Hook in the first 2 s, voice on frame 1** — shocking number or "you" scenario.
2. Story beat → "ye hota kaise hai? Aaiye samajhte hain." (Suraj prefers **samajhte**).
3. Mechanism in very simple metaphors, numbers with source.
4. Payoff by ~15–20 s, then a **loop ending** calling back to the hook.
Rules: tight, flowing lines; deliver *Caption (Roman) | On screen* plus **Devanagari voice text** (numbers spelled as spoken). **Show the script and wait for approval before generating voice.**

## 3. Voice — ElevenLabs (Claude in Chrome)
* Narrator **Amrut Deshmukh – Educational Hindi Voice** (never "Dixit Jii"), model **Eleven v4**, stability 50, similarity 75. Bunty lines: **"Bunty – Funny Best Friend"**. Other narrator used: "Ajay – Rich, Dramatic & Expressive".
* Put several lines in ONE paragraph separated by " ... ... " (newlines make it read only the first paragraph). Set text via JS `execCommand('insertText')` on `.ProseMirror`. Download both generations.

## 4. Align
`fragments.json` + `align.py` (silencedetect DP alignment) → `timeline.json`; words get char-share timing for one-word captions.

## 5. Visuals (HTML/SVG → Playwright)
Render with `device_scale_factor=1.25` and ffmpeg lanczos downscale, export 8–12 Mbps. Something moves every 0.5 s; impacts get shake/flash; safe zone x 35–1045, y 240–1460. Audit frames before full render. Headless Chromium has no emoji font.

## 5a. ANIMATION-FIRST + premium quality
Suraj wants **quality over quantity**: clean, premium, unique animation. Options proven to work:
* **Code-only animation** (0 credits): split panels, live counters, rolling coin balls ("Same ₹10,000, Alag Start"), stick-figure story on a night beach with a curling wave and underwater typed ending ("Stop Loss").
* **Illustrated story stills** from ChatGPT (Suraj's Plus account, Work mode, GPT-6 Astra; free) + code camera moves, one-word captions, palette shifts.
* Higgsfield (Kling 3.0 Pro ≈7.5 credits / 5 s clip; gpt_image_2_5 ≈2.75) only for a few key motion moments; save credits.
* Characters: **Momo** (glass bulb head, two black oval eyes, no mouth, gold screw neck, navy hoodie/joggers/gloves, white-navy sneakers; 3D kit + 2D sheet in `~/Downloads/Momo`, `~/Downloads/MoneyDopamine`) and **Bunty** (curly hair, black tee, joggers, grey sneakers). No copyrighted look-alikes, no trademark logos.

## 6. Render, sound, mix
SFX via earshot bank (below) + `audio_lib.py` (`boom`, `whoosh`, `thud`, `tick`, `ting`, `pop`, `riser`, `glitch`, `blip`, `failtone` …) cued to every visual event; Motion Array (Suraj signed in) for music/SFX — avoid Content-ID-registered tracks if possible. Mix to -14 LUFS (or -16 SFX-only when Suraj adds music himself). Deliver to `~/Downloads/<Project>/`.

**SFX = earshot sound bank first** (Suraj, 31 Oct 2026; repo github.com/Leonxlnx/earshot, MIT). 252 designed sounds render offline by id — no models, no network. Setup once per session: `git clone --depth 1 https://github.com/Leonxlnx/earshot ~/earshot && pip install --break-system-packages -e ~/earshot --no-deps && pip install --break-system-packages soxr librosa pyloudnorm scikit-learn`. In SFX scripts: `sys.path.insert(0,'engine'); from earshot_bank import bank; add(t, bank('pro_impact/short')*.45)`. Good picks: transitions `whoosh_fast/crisp`, `pro_whoosh_big/*`; card/label pop-ins `pro_pop_in/airy|knock`; number pops `pro_pop/tink`; stamps/hits `pro_impact/short|air`; reveal `pro_notify/ding_2045`; build-ups `pro_riser/roll` (dur param); end shimmer `pro_shimmer/m3`; endings `pro_logo_sting/swell_sting`. List all: `python3 -m earshot sfx list`. **QA every SFX stem:** `python3 -m earshot sfx check sfx_only.wav` (flags clicks, clipping, DC, ring, cheap rising whips; "digital silence inside" is normal for a stem). Keep hand-synth only for sounds the bank lacks (coin clinks, sizzle, pencil scratch). **Never add a continuous bed/hum** (Suraj: buzz irritates). earshot's listening tools (describe/match/critique) and its `real-sound` skill need Hugging Face models / Freesound / Mixkit, which this environment blocks — skills are copied in `.claude/skills/earshot` and `.claude/skills/real-sound` for when access exists.

## 7. Cover (1080×1920)
Hero frame + 2-line giant headline (white + yellow/red, thick stroke). **Never cover faces** — put text in empty sky or at the bottom.

## 8. Metadata — SEO FIRST (Suraj's standing rule)
* **YouTube title must START with the exact search phrase people type**, in English, then the Hinglish hook. Examples: "Importance of Stop Loss in Trading 🌊 | Stop Loss Kabhi Mat Khiskao (Hindi)", "SIP at 25 vs 35: Same ₹10,000, Alag Start", "Why Can't I Save Money? Dopamine Trap Explained | Paise Kyun Nahi Bachte". ≤100 chars.
* **Description:** first line repeats the search phrase ("Importance of Stop Loss in trading — simple Hindi mein samjho!") + "X kya hai" question; hook story; a "📌 Is short mein:" checklist of 3–4 search-intent points (what is X, why it matters, mistake, rule); end line; comment prompt; disclaimer; hashtags including the search-phrase hashtag (#importanceofstoploss #stoplosskyahai) and #shorts. **Keep Suraj's default block (Groww link + My Gears) at the bottom** — never delete it.
* **Tags:** the search phrase + variants ("importance of X", "what is X", "how to use X", "X in hindi", "X kya hai") + topic keywords + momentix. Keep the existing "SUraj" default tag.
* **IG/FB caption:** hook + emoji bullets + comment prompt + share prompt + disclaimer + ~8 hashtags. **Never name Suraj or the YouTube channel in IG captions.**
* YouTube settings: not made for kids, no paid promotion; altered/synthetic = **Yes** only for realistic AI video/images, **No** for code-drawn animation.

## 9. Publishing
**Current flow:** Suraj uploads the HQ video himself (quality), Claude opens the pages and does the rest:
* **YouTube Studio:** set title/description via JS on `#textbox[contenteditable]`; thumbnail: un-hide `input#file-loader`, give it an aria-label, `find` + `file_upload`; radios via JS; Show more → tags input; `#next-button` ×3; Schedule → date picker → time → Schedule. "We had trouble saving" retries itself — verify in `videos/short` list.
* **Meta Business Suite reels composer:** caption by clicking the Text box and typing; thumbnail: patch `HTMLInputElement.prototype.click` to capture the file input, Upload image → Upload Image, attach the captured input to body, `file_upload`; Next ×2; Schedule → FB + IG date/time (calendar may open upward; use › for next month) → final Schedule.
* Default slot **6:00 PM IST**, one reel per day, keep gaps; check the existing schedule first. Instagram trending audio can't be added from the desktop — for those, Suraj posts IG from the app.
* Metricool (brand `7365256`) remains an option for API scheduling.

## 10. Analytics
Metricool `getAnalyticsDataByMetrics` brand 7365256 (IG Reels IGRE*, YouTube YTVP*); fallbacks: IG `/reels/`, YouTube Studio `/videos/short`. Judge by avg watch ÷ length and reach vs previous videos.

## Lessons log
* Voice on frame 1; 74 s videos held ~9 s — aim 35–45 s, or 13–16 s pure animation loops.
* Mechanism + trend + utility beats political controversy.
* SEO: search phrase first in title and first line of description (Oct 2026).
* Never type passwords; Suraj signs in himself.* Sound: earshot bank SFX + `sfx check` QA; no continuous bed (Oct 2026).
