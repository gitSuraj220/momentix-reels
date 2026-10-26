import json, os, sys
# usage: python build_scene.py <video_dir>   (expects frame.js + timeline.json there) -> scene.html, scene_built.html
D=os.path.abspath(sys.argv[1]); S=os.path.dirname(os.path.abspath(__file__)); FONTS=os.path.join(os.path.dirname(S),'fonts')
r=lambda n: open(os.path.join(S,n)).read()
html=r('head.html').replace('__FONTS__',FONTS)+r('lib.js')+open(os.path.join(D,'frame.js')).read()+'\n'+r('tail.js')
open(os.path.join(D,'scene.html'),'w').write(html)
open(os.path.join(D,'scene_built.html'),'w').write(html.replace('__TIMELINE__',json.dumps(json.load(open(os.path.join(D,'timeline.json'))),ensure_ascii=False)))
print('built',D)
