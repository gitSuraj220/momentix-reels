# Script v3 — "3 dost, ₹1 lakh, 2007: FD vs Gold vs Nifty" (~40 s)

## Brief (Suraj's answers, 31 Oct 2026)
- Style: pencil-sketch (B&W hatching) + one orange accent, serif headline with one red-italic word, sources small at the bottom. Format inspired by @finance_90seconds; characters, story and numbers are ours.
- Characters: Bunty (FD), Ravi (new: short hair, round glasses, checked shirt; Nifty index fund), Momo in sketch style (bulb with a soft orange glow; gold).
- Voice: Amrut narrator only. Length ~40 s.
- Captions: serif headline at top + one-word captions below.
- Chart: values in ₹ lakh (₹1L, ₹4L, ₹14.9L). Gold = orange (accent), Nifty = ink blue, FD = grey.
- Hook frame: three envelopes of ₹1 lakh. Ending: hold on the final result (~2 s).
- Sound: earshot SFX on every visual event, no continuous bed, mix −16 LUFS (Suraj adds BGM).
- Posting: next vacant slot.

| # | Time | Caption (Roman) | On screen |
|---|---|---|---|
| 1 | 0–4 s | 2007 mein teen doston ne ek-ek lakh lagaye. Aaj ek ke paas ₹4 lakh hain… aur ek ke paas ₹15 lakh. | Three envelopes "₹1,00,000" slide onto a café table; three hands take one each; two counters flick up to ₹4L and ₹15L |
| 2 | 4–8 s | Bunty ne FD li. Ravi ne Nifty index fund. Aur Momo ne… sona. | Bunty stamps a passbook / Ravi taps "Nifty 50 index fund" on phone / Momo holds an orange-glinting gold coin |
| 3 | 8–10 s | Kaun jeeta? Aaiye samajhte hain. | Chart axes draw in (2007 → 2026), three lines start at ₹1L |
| 4 | 10–15 s | 2008 ka crash. Ravi ka ₹1.5 lakh, ek saal mein ₹74 hazaar. Momo ka sona? Upar. | Blue line dives (thud + red flash); Ravi grips his head; orange line climbs |
| 5 | 15–20 s | Phir 2012 se 2018 tak, sona chhe saal lagbhag wahin ka wahin. Aur Nifty… lagbhag double. | Orange line flat, Momo yawns at a calendar flipping; blue line overtakes |
| 6 | 20–25 s | 2020 mein COVID. Nifty do mahine mein 38% gira… par November tak wapas. Aur sona? Phir upar. | Lockdown window sketch; blue line drops and bounces back; orange line steps up |
| 7 | 25–29 s | 2025 mein sona ek hi saal mein 56% bhaaga… aur Momo sabse aage nikal gaya. | Orange line rockets; coins rain onto Momo |
| 8 | 29–34 s | Par 2026 mein? Nifty is saal 11% neeche. Aur sona, August se ab tak 16% gira. | Both lines dip at the end; Momo's label slides ₹17.8L → ₹14.9L; Ravi's ₹7.1L → ₹6.3L |
| 9 | 34–40 s | Aaj: Momo ₹14.9 lakh, Ravi ₹6.3 lakh, Bunty ₹4 lakh. | Three final labels pop with counters; hold ~2 s. Small print appears |

Small print (beats 8–9): "Approx. ₹1 lakh on 1 Jan 2007 → 31 Oct 2026. Nifty = index fund NAV (dividends, after fees). Gold = 24K price, no making charges/GST. FD = typical big-bank rate, renewed yearly, before tax. Past returns, not a promise. Sirf jaankari ke liye."

## Devanagari voice text (Amrut; one paragraph, lines separated by " ... ... ")
दो हज़ार सात में तीन दोस्तों ने एक-एक लाख लगाए। आज एक के पास चार लाख हैं… और एक के पास पंद्रह लाख। ... ... बंटी ने एफ़डी ली। रवि ने निफ़्टी इंडेक्स फ़ंड। और मोमो ने… सोना। ... ... कौन जीता? आइए समझते हैं। ... ... दो हज़ार आठ का क्रैश। रवि का डेढ़ लाख, एक साल में चौहत्तर हज़ार। मोमो का सोना? ऊपर। ... ... फिर दो हज़ार बारह से दो हज़ार अठारह तक, सोना छह साल लगभग वहीं का वहीं। और निफ़्टी… लगभग डबल। ... ... दो हज़ार बीस में कोविड। निफ़्टी दो महीने में अड़तीस परसेंट गिरा… पर नवंबर तक वापस। और सोना? फिर ऊपर। ... ... दो हज़ार पच्चीस में सोना एक ही साल में छप्पन परसेंट भागा… और मोमो सबसे आगे निकल गया। ... ... पर दो हज़ार छब्बीस में? निफ़्टी इस साल ग्यारह परसेंट नीचे। और सोना, अगस्त से अब तक सोलह परसेंट गिरा। ... ... आज: मोमो चौदह लाख नब्बे हज़ार, रवि छह लाख तीस हज़ार, बंटी चार लाख।

## Claims check (all from race.py / data.md)
- Final ₹14.9L / ₹6.3L / ₹4.0L; hook "₹15 lakh" = 14.9L rounded ✓
- 2008: ₹1.54L → ₹74k (−52%) ✓; gold up 2008 (avg +29%) ✓
- 2012→2018: gold ₹3.33L → ₹3.39L ✓; Nifty ₹1.46L → ₹2.79L (1.9x) ✓
- 2020: Nifty −38% Jan→Mar, regained peak Nov 2020 (integrato) ✓; gold 2020 avg +28% ✓
- 2025: gold +56% (₹8.19L → ₹12.78L, FY-avg basis, approx) ✓
- 2026: Nifty −11.1% YTD to 30 Oct ✓; gold ₹1,64,571 (24 Aug) → ₹1,38,419 (31 Oct) = −15.9% ✓; Momo ₹17.8L → ₹14.9L ✓; Ravi ₹7.1L → ₹6.3L ✓
