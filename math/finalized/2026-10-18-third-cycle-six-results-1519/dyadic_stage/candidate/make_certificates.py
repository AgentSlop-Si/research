"""Generate exact rational ideal certificates. Not needed for verification."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,time
N=16;ORDER=(1,3,7,5)

def add(a,b,c=F(1)):
 d=a.copy()
 for m,v in b.items():
  d[m]=d.get(m,F(0))+c*v
  if not d[m]:del d[m]
 return d

def shift(a,m,c=F(1)):
 return {tuple(x+y for x,y in zip(u,m)):v*c for u,v in a.items() if v*c}

def mul(a,b):
 d={}
 for m,c in b.items():d=add(d,shift(a,m,c))
 return d

def submon(a,b):return tuple(x-y for x,y in zip(a,b))
def divides(a,b):return all(x<=y for x,y in zip(a,b))
def reduce_poly(p,rep,basis):
 p=p.copy();r={}
 while p:
  m=max(p);c=p[m]
  for q,qr in basis:
   lm=max(q)
   if divides(lm,m):
    diff=submon(m,lm);fac=c/q[lm]
    p=add(p,shift(q,diff),-fac)
    rep=[add(u,shift(v,diff),-fac) for u,v in zip(rep,qr)]
    break
  else:r[m]=p.pop(m)
 return r,rep

def cert(fs,n):
 z=(0,)*n;basis=[];pairs=[]
 def insert(p,rep):
  p,rep=reduce_poly(p,rep,basis)
  if not p:return None
  c=p[max(p)];p={m:v/c for m,v in p.items()};rep=[{m:v/c for m,v in u.items()} for u in rep]
  if p=={z:F(1)}:return rep
  j=len(basis);pairs.extend((i,j) for i in range(j));basis.append((p,rep));return None
 for i,f in enumerate(fs):
  rep=[{} for _ in fs];rep[i]={z:F(1)}
  ans=insert(f,rep)
  if ans:return ans
 while pairs:
  pairs.sort(key=lambda ij:sum(max(a,b) for a,b in zip(max(basis[ij[0]][0]),max(basis[ij[1]][0]))))
  i,j=pairs.pop(0);a,ar=basis[i];b,br=basis[j];ma=max(a);mb=max(b)
  if all(min(x,y)==0 for x,y in zip(ma,mb)):continue
  lcm=tuple(max(x,y) for x,y in zip(ma,mb));da=submon(lcm,ma);db=submon(lcm,mb)
  p=add(shift(a,da),shift(b,db),F(-1));rep=[add(shift(u,da),shift(v,db),F(-1)) for u,v in zip(ar,br)]
  ans=insert(p,rep)
  if ans:return ans
 raise ValueError('Not a unit ideal')

def equations(ns):
 n=sum(ns);z=(0,)*n;one={z:F(1)};cs=[{} for _ in range(N)];cs[0]=one;var=0;names=[]
 for stride,count in zip(ORDER,ns):
  terms=[(0,one)]
  for j in range(1,count+1):
   e=tuple(int(i==var) for i in range(n));var+=1;terms.append((stride*j,{e:F(1)}));names.append(f'a{stride}_{j}')
  ds=[{} for _ in range(N)]
  for i,a in enumerate(cs):
   for k,b in terms:ds[(i+k)%N]=add(ds[(i+k)%N],mul(a,b))
  cs=ds
 return names,[add({m:(-1)**i*c for m,c in cs[i].items()},cs[i+8],F(-1)) for i in range(8)]

def pack(p):return [[list(m),c.numerator,c.denominator] for m,c in sorted(p.items())]

def main():
 out={'N':16,'stride_order':list(ORDER),'coefficient_domain':'Q','parity_sign':1,'patterns':[]}
 for ns in product(range(6),repeat=4):
  if sum(ns)!=5 or ns!=max(ns[i:]+ns[:i] for i in range(4)):continue
  names,fs=equations(ns);tt=time.time();hs=cert(fs,5)
  check={}
  for f,h in zip(fs,hs):check=add(check,mul(f,h))
  assert check=={(0,)*5:F(1)}
  record={'counts':list(ns),'variables':names,'inputs':[pack(p) for p in fs],'multipliers':[pack(p) for p in hs],'target':pack(check)}
  out['patterns'].append(record)
  print(ns,'terms',sum(map(len,hs)),'degree',max((sum(m)+sum(k) for f,h in zip(fs,hs) for m in f for k in h),default=0),'sec',round(time.time()-tt,3),flush=True)
 (Path(__file__).parent/'PARITY_CERTIFICATES.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
