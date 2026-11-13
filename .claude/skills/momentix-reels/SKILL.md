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
* Higgsfield (Kling 3.0 Pro ≈7.5 credits / 5 s clip; std + sound off = 6.25, 720×1280; gpt_image_2_5 ≈2.75) only for a few key motion moments; save credits.
  - Network: neither the container nor the Mac shell can reach upload.higgsfield.ai / the cloudfront result URLs. Upload: in Chrome on a higgsfield.ai tab, inject an `<input type=file>`, `file_upload` the /home/claude/... file, then JS `fetch(upload_url,{method:'PUT',headers:{'Content-Type':'image/png'},body:file})` → `media_confirm`. Download: navigate a tab to the result .mp4 URL, inject `<a href=location.href download=name>` and click → lands in ~/Downloads (fresh navigation each time, or Chrome blocks repeat downloads).
  - Kling invents actions on character shots (Bunty "signed" the paper instead of being stopped). For people: pass the same still as start_image AND end_image and ask only for subtle motion; for scenes with numbers overlaid, same trick keeps anchors fixed. Pure camera/vehicle shots can use start_image only.
  - ChatGPT batch stills: grab them with JS from the chat (`main img` blob URLs → fetch → `<a download>`); outputs arrive out of order, so identify each by looking before renaming.
* Characters: **Momo** (glass bulb head, two black oval eyes, no mouth, gold screw neck, navy hoodie/joggers/gloves, white-navy sneakers; 3D kit + 2D sheet in `~/Downloads/Momo`, `~/Downloads/MoneyDopamine`) and **Bunty** (curly hair, black tee, joggers, grey sneakers). No copyrighted look-alikes, no trademark logos.

* **Style recipes:** `styles/` has proven looks (Stat Chart, Paper Desk, Headline Highlight, Timeline — palettes, fonts, motion, "Never" lists). Pick one per reel; obey the anti-AI-look rules in `styles/README.md`.
* **finance_90seconds notebook style** (lined paper, serif headlines, rough.js hatched charts, sources under every chart) worked for the Zomato earnings reel; talking 3D object + paper cards worked for Dhanteras gold.

## 6. Render, sound, mix
SFX via earshot bank (below) + `audio_lib.py` (`boom`, `whoosh`, `thud`, `tick`, `ting`, `pop`, `riser`, `glitch`, `blip`, `failtone` …) cued to every visual event; Motion Array (Suraj signed in) for music/SFX — avoid Content-ID-registered tracks if possible. Mix to -14 LUFS (or -16 SFX-only when Suraj adds music himself). Deliver to `~/Downloads/<Project>/`.

**SFX = earshot sound bank first** (Suraj, 31 Oct 2026; repo github.com/Leonxlnx/earshot, MIT). 252 designed sounds render offline by id — no models, no network. Setup once per session: `git clone --depth 1 https://github.com/Leonxlnx/earshot ~/earshot && pip install --break-system-packages -e ~/earshot --no-deps && pip install --break-system-packages soxr librosa pyloudnorm scikit-learn`. In SFX scripts: `sys.path.insert(0,'engine'); from earshot_bank import bank; add(t, bank('pro_impact/short')*.45)`. Good picks: transitions `whoosh_fast/crisp`, `pro_whoosh_big/*`; card/label pop-ins `pro_pop_in/airy|knock`; number pops `pro_pop/tink`; stamps/hits `pro_impact/short|air`; reveal `pro_notify/ding_2045`; build-ups `pro_riser/roll` (dur param); end shimmer `pro_shimmer/m3`; endings `pro_logo_sting/swell_sting`. List all: `python3 -m earshot sfx list`. **QA every SFX stem:** `python3 -m earshot sfx check sfx_only.wav` (flags clicks, clipping, DC, ring, cheap rising whips; "digital silence inside" is normal for a stem). Keep hand-synth only for sounds the bank lacks (coin clinks, sizzle, pencil scratch). **Never add a continuous bed/hum** (Suraj: buzz irritates). **Listening works** (31 Oct 2026, after Suraj allowed huggingface.co, *.hf.co, cas-server.xethub.hf.co, us.aws.cdn.hf.co, mixkit, freesound): torch from PyPI (`pip install --break-system-packages torch transformers`; download.pytorch.org is blocked), then `python3 -m earshot doctor --fetch` (~1.1 GB, cached per session). Use `earshot describe/match/rank/critique/timeline` to check voice takes, SFX picks and the final mix before saying how anything sounds. Skills: `.claude/skills/earshot`, `.claude/skills/real-sound` (real recordings from Mixkit/Freesound with licence checks).

## 7. Cover (1080×1920)
Hero frame + 2-line giant headline (white + yellow/red, thick stroke). **Never cover faces** — put text in empty sky or at the bottom.

## 8. Metadata — SEO FIRST (Suraj's standing rule)
* **YouTube title in proper English (Suraj, 4 Nov 2026): START with the exact search phrase people type, then an English hook.** Examples: "Petrol vs Diesel vs EV: Which Car Is Cheapest Over 5 Years?", "Importance of Stop Loss in Trading: Never Move Your Stop Loss". No Hinglish in titles from now on; description and IG caption can stay Hinglish. ≤100 chars, aim ≤70 so phones don't cut it.
* **Description:** first line repeats the search phrase ("Importance of Stop Loss in trading — simple Hindi mein samjho!") + "X kya hai" question; hook story; a "📌 Is short mein:" checklist of 3–4 search-intent points (what is X, why it matters, mistake, rule); end line; comment prompt; disclaimer; hashtags including the search-phrase hashtag (#importanceofstoploss #stoplosskyahai) and #shorts. **Keep Suraj's default block (Groww link + My Gears) at the bottom** — never delete it.
* **Tags:** the search phrase + variants ("importance of X", "what is X", "how to use X", "X in hindi", "X kya hai") + topic keywords + momentix. Keep the existing "SUraj" default tag.
* **IG/FB caption:** hook + emoji bullets + comment prompt + share prompt + disclaimer + ~8 hashtags. **Never name Suraj or the YouTube channel in IG captions.**
* YouTube settings: not made for kids, no paid promotion; altered/synthetic = **Yes** only for realistic AI video/images, **No** for code-drawn animation.

## 8a. YouTube monetization guard — "inauthentic content" (Suraj's standing rule, 1 Nov 2026)
YouTube (16 Jul 2026) renamed "repetitious" to **inauthentic content**: channels with too much of it can't earn. AI voice itself is allowed; what loses monetization is (1) repetitive/template content where only the words change, (2) distressing/manipulative content made to chase views, (3) AI personas of real-looking people on finance/health/legal, or synthetic voices presented as credentialed experts. Apply it while making every video — at topic/script stage and again before delivery:
* **Original input in every video:** own sourced data, comparison, timeline, twist or opinion. No swap-the-topic templates (format can repeat, substance must not).
* **Unique hook, title, description and tags per video.** Never copy-paste metadata with a few words changed.
* **Never call Amrut's voice, Momo or any character an "advisor/expert/CA/doctor".** Keep "Sirf jaankari ke liye" on money/health content.
* **No realistic AI humans** speaking on finance/health/legal. Momo/Bunty/Ravi cartoon characters are fine.
* **No fear-bait or shock-for-views** framing; hooks must be paid off truthfully on screen.
* Sources: TechCrunch 20 Jul 2026; creatorblade.com policy summary. Re-check YouTube's official policy page before applying for YPP.

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

## Long videos: borrowed from MoneyPrinterTurbo (Suraj, 7 Nov 2026), only the useful parts
Do NOT use the tool itself: AI script + stock clips + AI voice is exactly the "mass-produced" pattern YouTube demonetizes (§8a).
1. **Stock B-roll, sparingly:** for 16:9 long videos, up to ~10% real footage between animated chapters (bank branch, city, phone in hand). Source: Pexels/Pixabay (free licence, no attribution needed; never logos or recognisable brands in focus). The container can't reach them, so fetch via Chrome (anchor download) → Mac Downloads → device_stage_files. Pexels API needs a free key from Suraj (store in env, never type it into pages).
2. **Whisper for takes + subtitles:** transcribe each recorded part per pause-segment (whisper-small, language=hindi) to find retakes; keep the LAST complete take unless a measured one is cleaner; cut repeats before timing captions.
3. **Shorts from every long video:** plan 3–4 vertical cut-downs at script time (each with its own hook line + 9:16 re-layout inside the safe area x 35–1045, y 240–1460), so one recording feeds the week's Shorts.

### Meta post/carousel composer gotcha (8 Nov 2026)
- In the Create post (photo/carousel) composer, a JS ClipboardEvent paste shows text in the box but is NOT saved — the post went out with no caption. Reels composer paste still works.
- Reliable: click the editor, then `computer type` the caption. Typing "₹" scrambles the editor — write "Rs" in typed captions.
- Fix after publishing: Content → row ⋯ → Facebook post / Instagram post → Manage post → Edit Post (both IG and FB feed posts are editable).
- Carousel upload: arm the file-input click capture, click "Add photo/video", then file_upload all slides in one call (order is kept).

### Loudness standard (Suraj, 9 Nov 2026)
- Reels were too quiet vs other reels (we mastered at -16 LUFS; YT/IG play ~-14). NEW DEFAULT: master to **-14 LUFS integrated, true peak <= -1 dBTP** (loudnorm I=-14:TP=-1:LRA=7 after mix).
- Phone-speaker voice chain: highpass 80 Hz, -2.5 dB @250 Hz, +4 dB @3 kHz (q 1.2), +2 dB high shelf @7 kHz, compressor -24 dB 4:1 attack 4 ms release 70 ms makeup 3 dB.
- Tell Suraj: in CapCut keep our track at 100%, BGM 15-20%, no "normalize loudness".

### Suraj's default YouTube description block (always keep at the bottom; captured 9 Nov 2026)
```
Open a free demat account in Groww.
💁 ♂️ -: https://app.groww.in/v3cO/jxw0y7md

My Gears-
🎤 Mic: https://amzn.to/3oKRGsT
💡 Ring Ligth: https://amzn.to/3AtIc82
Tripod: https://amzn.to/41DuZFR
Camera: iPhone 14 Pro Max
```

## Visual default: realistic photos (Suraj, 11 Nov 2026 — overrides the 2D style for new videos)
Use realistic photo visuals from now on (cinematic, photoreal), not cartoon/2D, unless Suraj asks for Momo/animation.
Keep it monetization-safe (§8a):
* Real stock photos/footage (Pexels, Unsplash, Pixabay — free licence) are first choice for people and places; note the source.
* AI photoreal images (Higgsfield gpt_image_2_6) are fine for scenes, objects, places, hands, backs, silhouettes, crowds out of focus.
  No sharp, front-facing realistic AI faces as the subject, and never an AI human "speaking" or posing as an expert on money topics.
* No AI fakes of real public figures. Real people only via licensed/press-kit photos or just their name on screen.
* No clips or frames from other creators/news channels (copyright + inauthentic content).
* Mark YouTube "Altered or synthetic content: Yes" whenever AI photoreal images are used.
Proven look (HFT video, 11 Nov): photoreal hero stills + code motion on top (push-ins, parallax, grain, glow, glitch, big numbers, captions).

## Long-form story format (from Paper Billions, @PaperBillionsTV — 11 Nov 2026)
Cold-open scene with stakes + "but here's the strange part" in the first 30 s; every big number gets a desi analogy or
"har Indian ke ₹X"; tiny 2–3 line dialogues every 10–20 s; a catchphrase that returns; ending loops back to the opening image;
"ye aapki jeb tak kaise aata hai" section near the end; film-style chapter names; description = question hook + chapters +
"Figures as of <date>" + sources. Publish within 1–3 days of the news. Thumbnail: one huge number top (red/white) + strong emotion image.

## Style reference: 2D metaphor explainer (Suraj, 10 Nov 2026 — use for future money explainers)
Reference: YouTube zEUKLSrbRZk "Why the Stock Market Just Crashed". Flat 2D hand-drawn cartoon: thick black outlines,
muted warm palette (cream walls, dusty greens/reds), handwritten-style labels on objects (e.g. "WEDNESDAY'S RALLY" tag on a
balloon, "DATA CENTER" sign), simple stick-ish characters with tiny faces, one visual METAPHOR per idea (balloon about to
pop = rally/bubble, stopwatch = time pressure, factory conveyor = new chips every year, VIX "fear gauge" dial, split-screen
company icons, map + smiling water tower = small town). Slow camera pans/push-ins between metaphor scenes, papers flying,
red mood lighting for panic. Build it in code (SVG/HTML or Remotion) — 0 credits; adapt Momo/Bunty into the flat style.

## Paper Billions story style (Suraj, 13 Nov 2026) — for reels and long videos
Reference: Paper Billions "Why Nvidia Would Fail Without Jensen Huang" (14:20, 245 cuts, avg shot 3.5 s, hook 1.6 s/shot, -14.4 LUFS, LRA 2.3).
- One flat 2D cartoon art style, locked per video; the character is created to fit each script (Suraj's call) — never a real-person caricature, no brand logos.
- Script is a story, not a list: line 1 = character + problem + number; sentences under ~10 words; 1-2 short dialogue lines; one recurring motif object; hook ends on a question, then title card.
- One shot per sentence (reel: 12-18 shots, 2-3 s; long: ~1 shot / 3 s). Every shot moves: camera push/pan, counters, items popping in.
- Data lives inside the world (price tags, boards, objects in grids, strings), not chart overlays. Punch lines on black in a handwritten font. Few or no subtitles.
- Build: Higgsfield backgrounds + props on separate layers in one style, animated in code (parallax, camera, counters). Voice: Amrut narrator + short character dialogue lines.
