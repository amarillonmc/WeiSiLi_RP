from research import *
def paras(p):
 out=[];acc=[];start=1
 for i,s in enumerate(lines(p),1):
  if s.strip():
   if not acc:start=i
   acc.append(s.strip())
  elif acc:out.append((start,i-1,''.join(acc)));acc=[]
 if acc:out.append((start,len(lines(p)),''.join(acc)))
 return out
if __name__=='__main__':
 p=findfile(sys.argv[1]);pat=sys.argv[2];ps=[(a,b,t) for a,b,t in paras(p) if re.search(pat,t)]
 n=int(sys.argv[3]) if len(sys.argv)>3 else 20
 if len(sys.argv)>4:ps=ps[-n:]
 else:ps=ps[:n]
 print(p.name)
 for a,b,t in ps:print(f'{a}-{b}: {t[:600]}')
