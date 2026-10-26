B=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
for b in 1 2; do timeout 400 npx remotion still src/index.ts SF out/sf$b.png --frame=10 --props="{\"beat\":$b}" --browser-executable=$B --gl=swangle --log=error 2>&1 | grep -v "^\s*at " | tail -4; done
cd out && ffmpeg -v error -y -i sf1.png -i sf2.png -filter_complex "[0]scale=540:-1[a];[1]scale=540:-1[b];[a][b]hstack" pair.jpg; echo done
