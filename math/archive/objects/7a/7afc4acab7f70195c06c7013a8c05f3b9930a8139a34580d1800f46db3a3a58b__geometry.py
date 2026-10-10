"""Reviewer-authored N16-to-N64 orders, shared by independent checks."""
LABELS=[(axis,c,s) for axis in ('H','V') for c in (0,1) for s in (-1,1)]
def cycles(p):
 seen=set();out=[]
 for v in range(len(p)):
  if v in seen:continue
  c=[];w=v
  while w not in seen:seen.add(w);c.append(w);w=p[w]
  assert w==v;out.append(c)
 return out

def cover(a,b,label):
 axis,c,s=label
 return [b*((x+s*(2*y+c))%a)+y if axis=='H' else b*x+(y+s*(2*x+c))%b for x in range(a) for y in range(b)]
def projection(v):
 x,y=divmod(v,8);return 4*(x%4)+y%4

def routes():
 out=[]
 for label in LABELS:
  ts=cover(4,4,label);small=ts[:];tails=[min(c) for c in cycles(ts)]
  for j,t in enumerate(tails):small[t]=ts[tails[(j+1)%len(tails)]]
  assert len(cycles(small))==1
  eta=[None]*16
  for v,w in enumerate(ts):eta[w]=small[v]
  pre=[]
  for w in cover(8,8,label):
   x,y=divmod(w,8);xx,yy=divmod(eta[4*(x%4)+y%4],4)
   pre.append(8*(xx+4*(x//4))+yy+4*(y//4))
  cc=cycles(pre);assert len(cc)==4 and all(len(c)==16 for c in cc)
  tails=sorted(next(v for v in c if projection(v)==0) for c in cc);assert tails==[0,4,32,36]
  p=pre[:]
  for j,v in enumerate(tails):p[v]=pre[tails[(j+1)%4]]
  assert len(cycles(p))==1 and all(projection(p[v])==small[projection(v)] for v in range(64))
  out.append(p)
 return out
