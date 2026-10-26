#!/bin/bash
# Render the film in 150-frame chunks; skips chunks already done so a rerun resumes.
cd "$(dirname "$0")"; mkdir -p out/chunks
B=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
TOTAL=$(python3 -c "import json;c=json.load(open('src/cues.json'));print(round((c[-1]['e']+1.6)*30))")
for ((s=0; s<TOTAL; s+=150)); do e=$((s+149)); [ $e -ge $TOTAL ] && e=$((TOTAL-1))
  f=out/chunks/c$(printf %05d $s).mp4; [ -s $f ] && continue
  npx remotion render /tmp/rbundle Film $f.tmp.mp4 --frames=$s-$e --codec=h264 --crf=14 --concurrency=2 --browser-executable=$B --gl=swangle --log=error && mv $f.tmp.mp4 $f
  echo "$(date +%T) chunk $s-$e done" >> out/chunks/progress.log
done
ls out/chunks/c*.mp4 | sed "s/^/file '/;s/$/'/;s#file 'out/chunks/#file '#" > out/chunks/list.txt
ffmpeg -v error -y -f concat -safe 0 -i out/chunks/list.txt -c copy out/video.mp4 && echo ALLDONE >> out/chunks/progress.log
