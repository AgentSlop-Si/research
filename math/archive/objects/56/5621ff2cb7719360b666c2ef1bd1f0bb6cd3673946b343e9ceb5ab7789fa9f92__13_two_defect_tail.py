"""Exact Fourier-tail identity after the j=2 low-frequency recurrence.

For i>=3, B[i,0] = d_(n-2) z^(-2i) + d_(n-1) z^(-i),
where d_(n-2)=h_(n-2)-h*_(n-2),
d_(n-1)=C[n-1,n-1]-h*_(n-1) (normalized diagonal=1).
This is a Fourier-support statement, not a cost improvement.
"""
import json,random
from pathlib import Path
from general_onion import build
from dual_support import primitive_root,P8

def verify():
 stats=[]
 for n in (8,16,32,64):
  for p in (12289,65537):
   w=primitive_root(p,n)
   rng=random.Random(n*10_000+p)
   perm=P8 if n==8 else [n-1,0,n-2]+list(range(1,n-2))
   valid=0
   for trial in range(12):
    x=[rng.randrange(1,p) for _ in range(8)]
    try:C,B,extra=build(n,p,w,perm,x)
    except ZeroDivisionError:continue
    d1=(int(extra['H'][n-2])-int(extra['star'][n-2]))%p
    d2=(1-int(extra['star'][n-1]))%p
    for i in range(3,n):
     want=(d1*pow(w,-2*i,p)+d2*pow(w,-i,p))%p
     assert int(B[i,0])%p==want,(n,p,i)
    valid+=1
   assert valid>=7
   stats.append(dict(n=n,field=p,root=w,samples=valid,checked_rows=valid*(n-3)))
 return stats
if __name__=='__main__':
 s=verify();Path(__file__).with_name('two_defect_tail_results.json').write_text(json.dumps(s,indent=2)+'\n')
 for row in s:print(row)
