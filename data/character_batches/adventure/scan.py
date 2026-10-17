from research import *
p=findfile(sys.argv[1]);ls=lines(p);pat=sys.argv[2]
hits=[i for i,s in enumerate(ls) if re.search(pat,s)]
if len(sys.argv)>3:
 n=int(sys.argv[3]);hits=hits[:n] if n>=0 else hits[n:]
idx=set()
for i in hits:idx.update(range(max(0,i-2),min(len(ls),i+6)))
for i in sorted(idx):
 s=ls[i]
 if s and not re.search(r'乳|胴|玉腿|呻吟|胸脯|小腹|热吻|丰臀|赤裸|娇躯|接吻|抚摸|吸吮|床上|股肉|股际',s):print(f'{i+1}: {s}')
