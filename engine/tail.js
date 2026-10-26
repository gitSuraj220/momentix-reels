const DEFS=`<defs>
<linearGradient id="night" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#050816"/><stop offset=".45" stop-color="#0E1638"/><stop offset=".62" stop-color="#2A1745"/><stop offset=".64" stop-color="#3A1B3F"/><stop offset="1" stop-color="#070A16"/></linearGradient>
<linearGradient id="lab" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#060A18"/><stop offset=".5" stop-color="#0B1430"/><stop offset="1" stop-color="#060A18"/></linearGradient>
<radialGradient id="centerglow"><stop offset="0" stop-color="#1E3A8A" stop-opacity=".45"/><stop offset="1" stop-color="#1E3A8A" stop-opacity="0"/></radialGradient>
<radialGradient id="cyanglow"><stop offset="0" stop-color="#22D3EE" stop-opacity=".35"/><stop offset="1" stop-color="#22D3EE" stop-opacity="0"/></radialGradient>
<radialGradient id="redglow"><stop offset="0" stop-color="#F43F5E" stop-opacity=".55"/><stop offset="1" stop-color="#F43F5E" stop-opacity="0"/></radialGradient>
<radialGradient id="moonglow"><stop offset="0" stop-color="#F4EFD9" stop-opacity=".35"/><stop offset="1" stop-color="#F4EFD9" stop-opacity="0"/></radialGradient>
<radialGradient id="scrim"><stop offset="0" stop-color="#05070F" stop-opacity=".75"/><stop offset=".7" stop-color="#05070F" stop-opacity=".4"/><stop offset="1" stop-color="#05070F" stop-opacity="0"/></radialGradient>
<radialGradient id="vig" cx=".5" cy=".45" r=".75"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/></radialGradient>
<linearGradient id="brick" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C2643A"/><stop offset="1" stop-color="#5A2410"/></linearGradient>
<linearGradient id="rim" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4A5068"/><stop offset=".5" stop-color="#1A1D28"/><stop offset="1" stop-color="#3A3F55"/></linearGradient>
<linearGradient id="callbg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1A2147"/><stop offset="1" stop-color="#0B1124"/></linearGradient>
<linearGradient id="qgrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#67E8F9"/><stop offset="1" stop-color="#2563EB"/></linearGradient>
</defs>`;
const S=document.getElementById('s');
window.renderAt2=t=>{S.innerHTML=DEFS+frame(t);return true};
</script></body></html>
