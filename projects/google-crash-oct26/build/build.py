s=open('reel.html').read().replace('__CUES__',open('../vo/cues.json').read())
open('built.html','w').write(s)
