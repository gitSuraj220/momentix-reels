# Script v1 — "3 dost, ₹1 lakh, 2007: FD vs Gold vs Nifty" (~42 s)

Characters: Bunty (FD), Ravi (Nifty 50 index fund, new: short hair, glasses, checked shirt), Momo (gold). One live race chart runs through the reel (gold = yellow, Nifty = blue, FD = grey).

| # | Time | Caption (Roman) | On screen |
|---|---|---|---|
| 1 | 0–4 s | 2007 mein teen doston ne ₹1 lakh lagaye. Aaj ek ke paas ₹4 lakh hain… aur ek ke paas ₹15 lakh. | Three friends clink chai cups over three envelopes marked ₹1,00,000; counter jumps to ₹4L and ₹15L |
| 2 | 4–8 s | Bunty ne FD li. Ravi ne Nifty index fund. Aur Momo ne… sona. | Each picks: bank passbook / phone with index-fund chart / gold coin |
| 3 | 8–10 s | Kaun jeeta? Aaiye samajhte hain. | Chart axes draw in, three lines start at ₹1L |
| 4 | 10–15 s | 2008 ka crash. Ravi ka ₹1.5 lakh, ek saal mein ₹74 hazaar. Momo ka sona? Upar. | Blue line dives (red flash, thud); Ravi clutches head; yellow line climbs |
| 5 | 15–20 s | Phir 2012 se 2018 tak, sona chhe saal lagbhag wahin ka wahin. Aur Nifty… lagbhag double. | Yellow line goes flat, Momo yawns; blue line climbs past |
| 6 | 20–25 s | 2025 mein sona ek hi saal mein 56% bhaaga… aur Momo sabse aage nikal gaya. | Yellow line rockets; gold coins rain |
| 7 | 25–30 s | Aaj: Momo ₹14.9 lakh, Ravi ₹6.3 lakh, Bunty ₹4 lakh. | Three end labels pop in with counters |
| 8 | 30–36 s | Par Bunty ki "safe" FD? Tax aur mehngai ke baad, asli keemat ₹1 lakh se bhi kam. | Bunty's ₹4L stack shrinks: "−30% tax", "mehngai ×3.15" → ₹84,000 (2007 ke rupaye) |
| 9 | 36–42 s | Jeetne wale ne bhi daraavne saal jhele. Asli sawaal: aap kaunsa crash jhel paoge? Aap Bunty ho, Ravi ya Momo? | Quick flash of the 2008 dive + 2012 flat line; three friends turn to camera; loop back to the chai-cup shot |

On-screen small print (last 6 s): "Approx. Nifty = index fund NAV (dividends, after fees); gold = 24K, no making charges; FD = typical big-bank rate, renewed yearly. Past returns, not a promise. Sirf jaankari ke liye."

## Devanagari voice text (Amrut, numbers spelled as spoken)
दो हज़ार सात में तीन दोस्तों ने एक-एक लाख रुपये लगाए। आज एक के पास चार लाख हैं… और एक के पास पंद्रह लाख। ... ... बंटी ने एफ़डी ली। रवि ने निफ़्टी इंडेक्स फ़ंड। और मोमो ने… सोना। ... ... कौन जीता? आइए समझते हैं। ... ... दो हज़ार आठ का क्रैश। रवि का डेढ़ लाख, एक साल में चौहत्तर हज़ार। मोमो का सोना? ऊपर। ... ... फिर दो हज़ार बारह से दो हज़ार अठारह तक, सोना छह साल लगभग वहीं का वहीं। और निफ़्टी… लगभग डबल। ... ... दो हज़ार पच्चीस में सोना एक ही साल में छप्पन परसेंट भागा… और मोमो सबसे आगे निकल गया। ... ... आज: मोमो चौदह लाख नब्बे हज़ार, रवि छह लाख तीस हज़ार, बंटी चार लाख। ... ... पर बंटी की "सेफ़" एफ़डी? टैक्स और महंगाई के बाद, असली कीमत एक लाख से भी कम। ... ... जीतने वाले ने भी डरावने साल झेले। असली सवाल: आप कौन सा क्रैश झेल पाओगे? आप बंटी हो, रवि या मोमो?

## Claims to verify against data.md (all from race.py)
- ₹4L / ₹15L (14.9L) / ₹6.3L final values ✓
- 2008: ₹1.54L → ₹74k ✓; gold up in 2008 (avg +29%) ✓
- 2012→2018 gold ₹3.33L → ₹3.39L ✓; Nifty ₹1.46L → ₹2.79L (1.9x, "lagbhag double") ✓
- 2025 gold +56% (₹8.19L → ₹12.78L, FY-average basis) ✓ (approx)
- FD after 30% tax + inflation ≈ ₹84k in 2007 rupees ✓ (applies to 30% slab; say so in caption)
