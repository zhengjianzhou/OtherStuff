#!/usr/bin/python3
### multi mpv player: e.g.: mmpv.py 2r.3x.2p
import os,sys,random
from time import sleep

os.system('killall mpv > /dev/null 2> /dev/null')
pp=r'/media/full/path'

if len(sys.argv) <=1: exit()
sys.argv[1] = sys.argv[1].replace('.','_')

args = [a+'x' if a[-1] not in 'rxp' else a for a in sys.argv[1].split('_')]
ps,cols = ['p']*100,[0]*100

if len(args) == 1:
  c = int(args[0].replace('p','').replace('r','').replace('x',''))
  cx = int(c*1.777778)
  args.append(str(cx)+args[0][-1])

for i in range(len(args)):
  cols[i] = int(args[i].replace('p','').replace('r','').replace('x',''))
  ps[i]   = args[i][-1]

screens = [
# top_left : tl, screen_size : ss
# [      tlx, tly,  ssx,  ssy,    cols, pause] # pause: random r, play x, pause p
  [        0,   0, 2160, 3820, cols[0], ps[0]],
  [     2160, 867, 3840, 2160, cols[1], ps[1]],
  [2160+3840, 867, 1920, 1080, cols[2], ps[2]],
]

TTx='mpv --panscan=1 --no-osc         --no-border -ss 90 --mute=yes -quiet -shuffle --geometry={2}x{3}+{0}+{1} --autofit={2}x{3} {PATH}/* > /dev/null 2> /dev/null &'.replace('{PATH}', pp)
TTp='mpv --panscan=1 --no-osc --pause --no-border -ss 90 --mute=yes -quiet -shuffle --geometry={2}x{3}+{0}+{1} --autofit={2}x{3} {PATH}/* > /dev/null 2> /dev/null &'.replace('{PATH}', pp)

ijxyp = []
for tlx,tly,ssx,ssy,cols,p in screens:
  try:
    x= int(ssx/cols)
    y= int(round(ssy/round(ssy/(x/1.777778)),0))

    for i in range(tlx,tlx+ssx-50,x):
      for j in range(tly,tly+ssy-50,y):
        ijxyp.append([i,j,x,y,p,cols])
  except:
    pass

random.shuffle(ijxyp)
noofmpv=len(ijxyp)
for i,j,x,y,p,c in ijxyp:
  TTr = TTx if random.randint(0,int(noofmpv/10)) == 0 else TTp
  runner = TTp if p == 'p' else ( TTr if p == 'r' else TTx )
  os.system('cd {} & {}'.format(pp,runner.format(i,j,x,y)))
  sleep(0.003*noofmpv)

