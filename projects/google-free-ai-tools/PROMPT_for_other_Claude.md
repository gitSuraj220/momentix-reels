Build me ONE self-contained HTML file named `reel.html` for a vertical Instagram/YouTube Short (1080×1920, 30 fps, 29.0 s). It is a code animation that a renderer will screenshot frame by frame, so follow the contract exactly. Give me the complete file in one go (no placeholders, no "rest stays the same").

## Render contract (must follow)
- Page is exactly 1080×1920, `html,body{margin:0;width:1080px;height:1920px;overflow:hidden}`.
- Expose `window.renderAt = async (t) => {...}` that draws the frame for time `t` seconds (0 ≤ t ≤ 29). It must be DETERMINISTIC: no CSS animations/transitions, no `requestAnimationFrame`, no `Date.now()`, no `Math.random()` (use a seeded hash like `R(i)=fract(sin(i*127.1)*43758.5453)`). Everything is computed from `t`.
- If you use images, `await img.decode()` before returning.
- Also add a preview mode: if the URL has `?play`, run a loop that calls `renderAt` in real time and plays `vo.mp3` (same folder) so I can watch it in a browser.
- Allowed external: Google Fonts only (Poppins 500/700/800, Lora italic 600). Logos: draw them yourself as inline SVG (simple faithful recreations). Images in the same folder: `momo_shocked.png`, `momo_pointing.png` (382×687, cartoon character with a dark navy background, NOT transparent).

## Timeline (seconds) — the voiceover is already recorded; sync to this
```json
{"end":29.0,"lines":{"1":[0.0,6.53],"2":[6.86,11.42],"3":[11.74,14.39],"4":[14.72,17.77],"5":[18.1,21.26],"6":[21.59,23.7],"7":[24.04,26.45]},"chunks":[[0.0,1.25,"ChatGPT aur Claude"],[1.25,2.16,"sab use karte"],[2.16,2.84,"hain…"],[2.84,3.65,"par Google ne"],[3.65,4.21,"chupchaap"],[4.21,4.87,"10 free AI"],[4.87,6.2,"coding tools nikaale"],[6.2,6.86,"hain!"],[6.86,7.91,"Antigravity —"],[7.91,8.83,"Cursor jaisa AI"],[8.83,9.93,"code editor."],[9.93,10.76,"Prompt likho,"],[10.76,11.74,"poori app ready."],[11.74,12.81,"AI Studio —"],[12.81,13.93,"seconds mein apna"],[13.93,14.72,"AI app."],[14.72,15.6,"Stitch —"],[15.6,16.59,"prompt se poora"],[16.59,17.44,"UI design aur"],[17.44,18.1,"code."],[18.1,18.8,"Opal —"],[18.8,19.95,"n8n aur Lovable"],[19.95,20.65,"ka combo,"],[20.65,21.59,"bina code."],[21.59,22.27,"Aur ye 12"],[22.27,23.18,"mein se sirf"],[23.18,24.04,"4 hain."],[24.04,25.09,"Poori list chahiye?"],[25.09,26.45,"Comment karo \"AI\"!"]]}
```
Paste this JSON into the file as `const TL = ...`. Beat n starts at `TL.lines[n][0]` and lasts until the next beat starts (beat 7 lasts to 29.0). Never hard-code other times; derive from TL.

## Look — clean editorial "tech explainer" (like popular AI-tools reels)
- Alternating WHITE cards (soft vertical gradient #F6F6F4 → #E4E4E1, subtle vignette) and BLACK cards (#050505 with a faint drifting dot-particle field).
- Big italic serif titles: Lora Italic 600, ~120 px, black on white / white on black, slide-up + fade in over 0.3 s.
- Word-by-word captions: Poppins 700, 54 px, white text in a dark translucent rounded box (rgba(35,35,35,.75), radius 12, padding 6px 18px), centred at y≈1480. Show the current `TL.chunks` item only; pop in with a 0.12 s scale 0.9→1 back-ease. Highlight tool names in yellow (#FFD84D): Antigravity, AI Studio, Stitch, Opal, n8n, Lovable, Google, "AI" in the CTA.
- Motion rule: something moves at least every 0.5 s — slow push-in on every card (scale 1.00→1.05), logo pops (back-ease), typing cursors, parallax layers, sparkles.
- Transitions between beats: 8-frame blur-whip (outgoing slides left with CSS filter blur(0→24px), incoming slides in from right, blur 24→0).
- Small print from beat 2 to the end: "Free tiers have limits and can change. Checked 2 Nov 2026." (Poppins 500, 20 px, 50% opacity, centred, y≈1870).
- Use real-looking logos as inline SVG: Google "G" (4 colours), Antigravity (rainbow arch "A"), Google AI Studio (sparkle-in-square icon + wordmark), Stitch (wordmark + "BETA" pill), Opal (simple gem/oval mark + wordmark), n8n (pink node chain + wordmark), Lovable (gradient heart + wordmark), ChatGPT (knot), Claude (orange starburst), plus small icons for the carousel: Gemini Notebook, Code Wiki, Flow Music, Jules (octopus), Mixboard, Pomelli.

## Beats
1. HOOK (beat 1, 0–6.86 s), white card.
   - 0–2.8 s: ChatGPT and Claude logo chips (rounded white cards with shadow) bounce in side by side at the top half; "sab use karte hain" — small crowd of tiny avatar dots gathers under them.
   - At "par Google ne" (2.84 s): both chips shrink, desaturate and slide to the top corners; Google "G" (220 px) slams into the centre with a soft shockwave ring.
   - 3.65–6.86 s: 10 tool icons orbit the G on a dashed circle (radius 330 px), each popping in one by one; big text "10 FREE AI CODING TOOLS" above (Poppins 800, 84 px, "FREE" in green #1E9E5A with a hand-drawn underline that draws on).
   - Momo badge bottom-left: circle 300 px at (60, 1120) with navy (#0F1C37) fill, golden ring 6 px, `momo_shocked.png` inside (cover-fit, clipped to circle), pops in at 0.3 s and wobbles at 2.84 s.
2. ANTIGRAVITY (beat 2), black card.
   - Rainbow-arch logo glows in centre top (y≈380), title "AI Code Editor" under it.
   - RICH MOCKUP (y 620–1380): dark IDE window (macOS dots, file tabs, line numbers). A prompt box at the bottom types "Login wala e-commerce page banao" (character by character, ~18 chars/s, blinking caret), then the window splits: left half renders a tiny shop page (header "ShopKart", login button, 4 product cards with prices ₹499/₹799/₹1,299/₹299), right half streams React/HTML code lines with syntax colours.
   - Small chip "≈ Cursor" flashes next to the title when "Cursor jaisa" is spoken (7.91 s). A green "App ready ✓" toast slides in at "poori app ready" (10.76 s).
3. AI STUDIO (beat 3), black card.
   - Sparkle icon + "Google AI Studio" wordmark and "ai.studio/build" in blue (#4C8DFF) at top.
   - RICH MOCKUP: a light "Build" panel: prompt "Ek photo caption app banao" → spinner 0.4 s → a phone-sized app preview pops in (upload box with a sample photo-like gradient, a "Generate caption" button, and a caption bubble typing out "Sunset at Marine Drive 🌅").
   - Stopwatch chip counts 0.0 → 3.2 s ("seconds mein").
4. STITCH (beat 4).
   - 14.72–15.6 s: black card, "Stitch" wordmark + "BETA" pill.
   - Then white card with italic title "AI UI Designer" and three phone mockups sliding in (staggered 0.12 s): a dark-mode fintech app (balance ₹2,45,000, chart line, cards), a transactions list, a profile screen. At "aur code" (17.44 s) a "</> Export code" button gets pressed (cursor click ripple) and a code snippet card slides up.
5. OPAL (beat 5), white card.
   - n8n logo slides in from the left, Lovable logo from the right; at "ka combo" (19.95 s) they collide and merge into the Opal logo with a flash.
   - RICH MOCKUP: 4 rounded workflow nodes connected by animated dashed lines: "Input: Topic" → "Gemini: Script" → "Veo 3: Video" → "Output: Reel". Little packets travel along the lines. A "No code" chip with a crossed-out </> icon at "bina code" (20.65 s).
6. "12 MEIN SE SIRF 4" (beat 6), black card.
   - Fast horizontal carousel of icon tiles (Gemini Notebook, Code Wiki, Flow Music, Jules, Mixboard, Pomelli, …) whipping past with motion blur; big counter in the centre "4 / 12" (the 4 pulses; the 12 ticks up from 4 to 12 between 21.59 and 23.2 s).
7. CTA (beat 7 → 29.0 s), white card.
   - Huge "Comment" (Poppins 800, 120 px) and below it a big rounded comment bubble containing "AI" (200 px, gradient #4C8DFF → #A142F4), bubble pulses every 0.6 s, arrow bouncing down towards the bottom-right where the comment button usually is.
   - Line under: "poori list DM mein milegi 👇" (Poppins 600, 44 px).
   - Momo badge bottom-left with `momo_pointing.png`, pops in at 24.04 s.
   - Keep everything gently moving until 29.0 s.

## Deliver
Just the full `reel.html` file contents. I will save it next to `vo.mp3`, `momo_shocked.png` and `momo_pointing.png`.
