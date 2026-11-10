# HANDOFF — Anthropic IPO reel (build in the other Claude account)

Paste this to the other Claude: **"Clone https://github.com/gitSuraj220/momentix-reels (public), read CLAUDE.md + `.claude/skills/momentix-reels/SKILL.md`, then build the reel described in `projects/anthropic-ipo-loss/HANDOFF.md`. Ask me before spending any paid credits."**

## 0. What it is
Vertical Hinglish Short/Reel, ~45 s, 1080×1920, 30 fps, "Momentix by Suraj" channel. Topic: Anthropic's first operating profit + $66B (mostly non-cash) loss, and the lesson "headline mein loss dekh ke darna mat".
Look: **full 3D cinematic** using 15 stills (option C = NO AI video; all motion is code: push-in/pull-out, parallax, particles, light flashes, shake), fast cuts every 2–3 s, big numbers + 2–3 keywords in code. No BGM (Suraj adds it).

## 1. Final script (Suraj's exact words — do not change)
1. AI ki sabse popular company ne pehli baar profit kamaya… aur usi 3 mahine mein 66 billion dollar ka loss bhi dikhaya! 🤯
2. Ye hai Anthropic — Claude AI banane wali company — jisne abhi stock market mein aane ke liye file kiya hai.
3. April se June mein kamai: 11.6 billion dollar. Sirf 3 mahine pehle ye 4.7 billion thi.
4. Har 100 dollar ki kamai pe… 8 dollar ka operating profit. Pehli baar!
5. Toh 66 billion ka loss? Zyaadatar kaagaz pe hai. Investors ko future mein shares dene ka wada tha — company ki value uchhli, toh wo wada accounts mein mehenga ho gaya.
6. Matlab itna paisa jeb se gaya nahi — ye non-cash loss hai.
7. Par July se September mein kamai badhkar 17 billion… phir bhi operating loss wapas aa gaya.
8. Toh agli baar headline mein "company ko itne crore ka loss" padho — darna mat. Pehle 2 cheezein dekho: operating profit hai ya nahi, aur loss cash ka hai ya sirf kaagaz ka.
On-screen small print (bottom, from line 2 onward): "Source: Anthropic S-1 (26 Oct 2026) + Amendment 1 (2 Nov 2026). IPO price abhi tay nahi. Sirf jaankari ke liye."

Facts (verified): Q1 2026 revenue $4.73B; Q2 (Apr–Jun) $11.56B, operating income $974M (8.4%), net loss $66.3B of which ~$59.6B non-cash fair-value charges (convertible notes/SAFEs/derivatives); Q3 (Jul–Sep) $16.96B, operating loss $567M, net loss $23.3B. Nasdaq ticker "ANT". On 9 Nov a $70–80 range was emailed then retracted; price not set.

## 2. Voice (ElevenLabs, Suraj's browser — Chrome extension)
- Voice: **"Amrut Deshmukh – Educational Hindi Voice"**, model **Eleven v4**, default stability/similarity. Generate makes 2 takes; download both; pick the clean one (check every word).
- Paste this text (numbers spelled for TTS):
```
AI ki sabse popular company ne pehli baar profit kamaya… aur usi teen mahine mein chhiyaasath billion dollar ka loss bhi dikhaya! ... ... Ye hai Anthropic — Claude AI banane wali company — jisne abhi stock market mein aane ke liye file kiya hai. ... ... April se June mein kamai: gyaarah point chhe billion dollar. Sirf teen mahine pehle ye chaar point saat billion thi. ... ... Har sau dollar ki kamai pe… aath dollar ka operating profit. Pehli baar! ... ... Toh chhiyaasath billion ka loss? Zyaadatar kaagaz pe hai. Investors ko future mein shares dene ka wada tha — company ki value uchhli, toh wo wada accounts mein mehenga ho gaya. ... ... Matlab itna paisa jeb se gaya nahi — ye non-cash loss hai. ... ... Par July se September mein kamai badhkar satrah billion… phir bhi operating loss wapas aa gaya. ... ... Toh agli baar headline mein 'company ko itne crore ka loss' padho — darna mat. Pehle do cheezein dekho: operating profit hai ya nahi, aur loss cash ka hai ya sirf kaagaz ka.
```
- DONE: both Amrut takes are in the repo: `vo/vo.mp3` (take 1) and `vo/vo_alt.mp3` (take 2). Pick the cleaner one (check every word); no new ElevenLabs spend needed.
- Voice chain (phone-speaker clarity), apply before mixing:
  `highpass=f=80,equalizer=f=250:t=q:w=1:g=-2.5,equalizer=f=3000:t=q:w=1.2:g=4,highshelf=f=7000:g=2,acompressor=threshold=-24dB:ratio=4:attack=4:release=70:makeup=3`
- Get line start times with `ffmpeg silencedetect` (noise=-38dB:d=0.3) and build the visual timeline on them.

## 3. Stills (already generated here — in `projects/anthropic-ipo-loss/art/`)
Files `s01.png … s14.png` + `cover_bg.png` (752×1344, 9:16, NO text). If some are missing, they are still being generated in the main account and will be pushed — pull again.
| Line | Shots (cut every ~2–3 s) | Code motion idea | Big text overlay (code) |
|---|---|---|---|
| 1 | s01 Momo celebrating, green cash rocket → s02 floor cracks, red wave | s01 fast push-in + green particle rain; s02 whip-pan in, red flash, shake | "PEHLI BAAR PROFIT ✓" (green) → "$66 BILLION LOSS" (red slam, glitch) |
| 2 | s03 AI tower (blank cream panel on facade) → s04 Momo at bell podium | s03 slow rise (pan up), put the **real Anthropic wordmark small** on the blank panel area or as a small tag at top; s04 push-in | "ANTHROPIC" + small "Claude AI" · "IPO FILING" stamp |
| 3 | s05 small orb vs huge gold orb → s06 Momo on rising green pillar | s05 zoom on orb + light burst; s06 tilt-up parallax | "$4.7B → $11.6B" with counting number, "APR–JUN" |
| 4 | s07 coin tower, coins to Momo | slow orbit-like pan + coin sparkle | "HAR $100 PE → $8 PROFIT" (coin counter 8/100) |
| 5 | s08 silhouette hands sealed scroll → s09 scroll balloon huge, red | s08 over-shoulder push; s09 pull-back + red pulse | "$66B LOSS = ZYAADATAR KAAGAZ PE" · "WADA (shares) → MEHENGA" |
| 6 | s10 wallet safe, red papers flying | rotate-zoom + paper particles blowing out | "NON-CASH LOSS" + "JEB SE NAHI GAYA ✓" |
| 7 | s11 Momo runs up green bars → s12 gauge needle in red | s11 side tracking pan; s12 needle wobble + red beacon flash | "JUL–SEP: $17B" then "OPERATING LOSS WAPAS ✗" |
| 8 | s13 Momo panics at red newspaper → s14 calm, magnifying glass, 2 checks | s13 shake + push; s14 warm push-in | Checklist pops: "1. OPERATING PROFIT?" "2. CASH YA KAAGAZ?" |
Logo: download the official Anthropic wordmark SVG (e.g. Wikimedia Commons "Anthropic logo.svg"), render white/cream, small (≤300 px wide), shown only on line 2. Never let AI draw it.

## 4. Build pipeline (copy from `projects/short-selling/`)
- `reel.html` with `window.renderAt(t)` (images as layers, all motion as functions of t), `render.py` (Playwright → frames → `build/video_only.mp4`, set END), `sfx.py` (uses `engine/earshot_bank.bank()` ids: pro_pop/boop, pro_pop/tink, swipe/paper, whoosh_fast/crisp, cut_hit/punch|kick|sub, impact/punch, glitch/hit, ui_pop/step, pro_notify/ding_2045), `mix.py` (voice at −17, SFX ~8 LU under, then **loudnorm I=−14, TP=−1, LRA=7**, mux libx264 10M + AAC 256k).
- Safe area: x 35–1045, y 240–1460. Something moves every 0.5 s.
- Fonts in `engine/fonts`: Poppins 500/700/800 only (no 400/600), Anton, Caveat, Permanent Marker, Courier Prime. Headless Chromium has **no emoji font** → no emojis in rendered text (use SVG). ₹ and $ are fine.
- SFX: rich money pack — cash register "ka-ching" on numbers, glitch/impact on "$66B LOSS", whooshes on cuts, paper flutter on line 6, alarm blip on gauge, stamp on checklist. No music.
- Check final loudness: `ffmpeg -i final.mp4 -af ebur128=peak=true -f null -` → about −14 LUFS, peak ≤ −1.

## 5. Cover (1080×1920)
`cover_bg.png` (Momo lit half green / half red) + text top: "PROFIT BHI," (green) / "$66B LOSS BHI?" (red), Anton/Poppins 800, no emoji.

## 6. Upload details (write `Upload_Details.txt`)
- YouTube title in **proper English starting with the search phrase**, e.g. "Anthropic IPO Explained: First Profit and a $66 Billion Loss #shorts".
- Description Hinglish + "Sirf jaankari ke liye" + sources line + Suraj's default block at the bottom (copy exactly from `.claude/skills/momentix-reels/SKILL.md`, Groww + My Gears).
- IG/FB caption Hinglish, never mention Suraj or the YouTube channel, include "Sirf jaankari ke liye". Altered content: Yes. Language: Hindi.
- Note in the description: no buy/sell advice. (Claude is made by Anthropic — keep it strictly factual.)

## 7. Deliver
Final files: `final/Anthropic_IPO_66B_Loss.mp4`, `Cover_Anthropic_IPO.jpg`, `Upload_Details.txt` → send to Suraj (and his Mac `Downloads/AnthropicIPO/` if connected). Don't commit MP4/WAV (see .gitignore). Commit code to the repo.
