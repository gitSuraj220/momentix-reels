"""3 dost, ₹1 lakh each on 1 Jan 2007: FD vs Gold vs Nifty 50. Values at each year-end (gold: yearly avg proxy)."""
import json
START=100000
# Nifty 50 calendar-year total returns (UTI Nifty 50 Index Fund Regular NAV, after costs) — integrato.in, checked 31 Oct 2026
nifty={2007:53.6,2008:-52.0,2009:73.8,2010:17.7,2011:-24.8,2012:28.3,2013:6.9,2014:31.8,2015:-3.3,2016:4.0,
       2017:29.7,2018:4.3,2019:13.2,2020:15.5,2021:25.2,2022:5.3,2023:20.9,2024:9.6,2025:11.6,2026:-11.1}
# Gold ₹/10g: calendar-year averages 2006–2023 (Forbes India table); 2024–25 = RBI FY avgs (indiagraphs, FY24-25, FY25-26); 2026 = spot 31 Oct 2026 24K (goldpriceindia)
gold={2006:9265,2007:10598,2008:13630,2009:16686,2010:20728,2011:27329,2012:30859,2013:28422,2014:26703,2015:24931,
      2016:27445,2017:29156,2018:31391,2019:39108,2020:50151,2021:48099,2022:55017,2023:63203,2024:75842,2025:118421,2026:138419}
# FD: typical big-bank 1–3 yr rate (midpoint of RBI-sourced range at 31 Mar each year, moneyseth); 2024 6.8, 2025 6.5, 2026 6.25 (SBI 1-yr)
fdr={2007:8.25,2008:8.625,2009:7.75,2010:6.75,2011:8.625,2012:8.875,2013:8.25,2014:8.625,2015:8.375,2016:7.25,
     2017:6.75,2018:6.5,2019:6.875,2020:5.95,2021:5.2,2022:5.3,2023:6.625,2024:6.8,2025:6.5,2026:6.25*10/12}
rows=[]; n=g=f=START
for y in range(2007,2027):
    n*=1+nifty[y]/100; g=START*gold[y]/gold[2006]; f*=1+fdr[y]/100
    rows.append((y,round(n),round(g),round(f)))
for r in rows: print(r)
yrs=19+10/12
for name,v in zip(['Nifty','Gold','FD'],rows[-1][1:]):
    print(f"{name}: ₹{v:,} = {v/START:.2f}x, CAGR {((v/START)**(1/yrs)-1)*100:.1f}%")
# inflation: CII FY2006-07=122 -> FY2026-27=384
infl=384/122; print('prices x',round(infl,2))
for name,v in zip(['Nifty','Gold','FD'],rows[-1][1:]):
    print(f"  real {name}: ₹{v/infl:,.0f} in 2007 rupees")
# FD after 30% tax (approx: rate*0.7 each year)
f2=START
for y in range(2007,2027): f2*=1+fdr[y]*0.7/100
print('FD after 30% tax ≈', round(f2), 'real', round(f2/infl))
# drawdowns
print('Nifty end-2008', rows[1][1], 'peak end-2007', rows[0][1])
json.dump({'rows':rows},open('race.json','w'))
