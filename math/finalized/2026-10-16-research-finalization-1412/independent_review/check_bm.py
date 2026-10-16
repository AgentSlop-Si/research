"""New independent small finite-field synthesis control, no project imports."""
from itertools import product
import json

def fit(x,L,p):
 for tail in product(range(p),repeat=L):
  C=(1,)+tail
  if all(sum(C[j]*x[t-j] for j in range(L+1))%p==0 for t in range(L,len(x))):return C
 return None

def synth(x,p,cap):
 n=len(x);C=[1];old=[1];span=0;shift=1;inv=1;inversions=0
 for t in range(n):
  delta=(x[t]+sum((C[j] if j<len(C) else 0)*x[t-j] for j in range(1,span+1)))%p
  if not delta:shift+=1;continue
  newspan=max(span,t+1-span)
  if newspan>cap:return None,inversions
  before=C[:]
  need=shift+len(old)
  C += [0]*max(0,need-len(C))
  for j,a in enumerate(old):C[j+shift]=(C[j+shift]-delta*inv*a)%p
  if 2*span<=t:
   span=t+1-span;old=before;inv=pow(delta,-1,p);inversions+=1;shift=1
  else:shift+=1
  while len(C)>1 and C[-1]==0:C.pop()
  assert len(C)-1<=span
 return (span,C),inversions
seqs=decisions=untapped=0
for p,maxn in [(2,7),(3,5)]:
 for n in range(1,maxn+1):
  for x in product(range(p),repeat=n):
   seqs+=1
   L=next(L for L in range(n+1) if fit(x,L,p) is not None)
   for cap in range(n):
    r,iv=synth(x,p,cap);decisions+=1
    assert (r is not None)==(L<=cap)
    assert iv<=cap
    if r is not None:
     span,C=r;assert span==L
     assert all(sum((C[j] if j<len(C) else 0)*x[t-j] for j in range(span+1))%p==0 for t in range(span,n))
     untapped+=len(C)-1<span
print(json.dumps({'sequences':seqs,'cap_decisions':decisions,'accepted_untapped_cases':untapped,'passed':True,'scope':'Finite independent transcription controls, not universal proof or production audit.'},indent=2))
