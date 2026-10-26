#!/bin/bash
# usage: ./snap2.sh outdir sec...   (bundles once, renders stills at half scale, makes sheet)
set -e; out=$1; shift; mkdir -p $out
B=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
npx remotion bundle src/index.ts --out-dir /tmp/rbundle --log=error >/dev/null
for s in "$@"; do fr=$(python3 -c "print(round($s*30))"); npx remotion still /tmp/rbundle Film $out/t$s.png --frame=$fr --scale=0.5 --browser-executable=$B --gl=swangle --log=error; done
python3 sheet.py $out/sheet.png $(for s in "$@"; do echo $out/t$s.png; done)
