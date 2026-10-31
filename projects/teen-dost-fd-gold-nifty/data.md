# 3 dost, ₹1 lakh, 1 Jan 2007 — FD vs Gold vs Nifty 50 (data sheet, 31 Oct 2026)

Inspired by the "three friends, three portfolios" format (@finance_90seconds, Nasdaq vs S&P vs 60/40). Our version is Indian, with our own characters and numbers. Computed in `race.py`.

## Result (31 Oct 2026, ~19.8 years)

| Dost | Kahan lagaya | ₹1 lakh bana | Guna | CAGR | Inflation ke baad (2007 ke rupaye) |
|---|---|---|---|---|---|
| Momo | Gold | **₹14.9 lakh** | 14.9x | 14.6% | ~₹4.7 lakh |
| Ravi | Nifty 50 index fund | **₹6.3 lakh** | 6.3x | 9.7% | ~₹2.0 lakh |
| Bunty | FD (har saal renew) | **₹4.0 lakh** | 4.0x | 7.2% | ~₹1.26 lakh |

- FD after 30% tax every year ≈ ₹2.66 lakh → inflation ke baad ~₹84,000. **Real terms mein FD ne paisa ghataya.**
- Prices rose ~3.15x (Cost Inflation Index 122 → 384).

## Story beats the data supports
- **2008:** Nifty −52% in the year (Jan–Oct 2008 peak-to-trough −60%); Ravi's ₹1.54 lakh → ₹74k. Gold +29% that year (avg). Bunty's FD steady.
- **2012→2019:** Gold barely moved for ~7 years (₹3.33 lakh in 2012, ₹3.39 lakh in 2018; it dipped ~19% from 2012 to 2015). Nifty doubled in that time.
- **2020 COVID:** Nifty fell −38% (Jan→Mar 2020) and recovered by Nov 2020; gold jumped (+28% avg).
- **2025:** Gold's huge year (₹8.2 lakh → ₹12.8 lakh, +56%) is what puts Momo far ahead.
- **2026 so far:** Nifty −11.1% YTD (to 30 Oct); gold ~−16% from its Aug 2026 high (₹1,64,571 on 24 Aug → ₹1,38,419 on 31 Oct).
- **Lesson:** the winner depends a lot on the end date. Before 2025, gold and Nifty were close (end-2024: gold ₹8.2L, Nifty ₹6.4L). Every winner had scary years.

## Year-end values (₹)
| Year | Nifty | Gold* | FD |
|---|---|---|---|
| 2007 | 1,53,600 | 1,14,387 | 1,08,250 |
| 2008 | 73,728 | 1,47,113 | 1,17,587 |
| 2011 | 1,13,417 | 2,94,970 | 1,46,917 |
| 2015 | 1,98,254 | 2,69,088 | 2,03,839 |
| 2019 | 3,15,738 | 4,22,105 | 2,65,631 |
| 2020 | 3,64,677 | 5,41,295 | 2,81,436 |
| 2024 | 6,37,057 | 8,18,586 | 3,55,021 |
| 2025 | 7,10,956 | 12,78,154 | 3,78,097 |
| Oct 2026 | 6,32,040 | 14,93,999 | 3,97,790 |
(full series in race.py output)

## Method and caveats (put a short version on screen and in caption)
- **Nifty:** calendar-year total returns of UTI Nifty 50 Index Fund (Regular, growth NAV), i.e. with dividends, after fund costs; 2026 = YTD to 30 Oct. Source: integrato.in Nifty 50 page (checked 31 Oct 2026).
- **Gold:** start ₹9,265/10g (2006 average, proxy for Jan 2007). Intermediate points are yearly averages (calendar 2007–2023: Forbes India gold history; 2024–2025: RBI FY averages via indiagraphs). End = ₹1,38,419/10g 24K spot, 31 Oct 2026 (goldpriceindia.com; MCX spot ₹1,41,615 on 29 Oct). No making charges/GST/storage assumed (i.e. like gold ETF/digital gold, not jewellery).
- **FD:** each year at the typical big-bank 1–3 yr deposit rate (midpoint of range, 31 Mar each year, 2007–2023, MoneySeth/RBI); 2024 6.8%, 2025 6.5%, 2026 6.25% (SBI 1-yr, RateScan; 10 months). Pre-tax unless stated.
- **Inflation:** CBDT Cost Inflation Index FY2006-07 = 122, FY2026-27 = 384.
- Approximate, illustrative, past returns. "Sirf jaankari ke liye, investment advice nahi."

## Sources
- Nifty 50 returns: https://integrato.in/mfic-app/mktpage.php?p=nifty-50
- Gold 2005–2024 averages: https://www.forbesindia.com/article/explainers/gold-rate-history-india/92539/1
- Gold FY averages + MCX spot: https://indiagraphs.com/data-stories/gold-price-history-india
- Gold today: https://www.goldpriceindia.com/
- FD rate history: https://www.moneyseth.com/blogs/Fixed-Deposit-Interest-Rate-History-from-2000
- SBI current FD: https://ratescan.in/bank/sbi/fixed-deposit-interest-rates/
- CII: https://www.incometaxindia.gov.in/w/view-all-cii ; FY2026-27 = 384: https://a2ztaxcorp.net/?p=35034
