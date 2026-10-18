from itertools import product
from math import comb

def cv(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return tuple(c)
def sig(c,w):
 q=1<<w
 # d+1 consecutive samples suffice to identify full integer function mod q
 return tuple(sum(x*pow(j,k,q) for k,x in enumerate(c))%q for j in range(len(c)))
for m,L in [(1,2),(1,3),(1,4),(1,5),(1,6),(2,3),(2,4),(3,2),(3,3)]:
 aa=list(product(range(1<<m),repeat=L)); P={}
 for i,a in enumerate(aa):
  for b in aa[i:]:P.setdefault(cv(a,b),(a,b))
 H=2*m+(L-1).bit_length(); gamma=2*L-2-(2*L-2).bit_count()
 bad=[]
 for W in range(1,H+gamma+1):
  seen={}; collision=None
  for c,ab in P.items():
   s=sig(c,W)
   if s in seen and seen[s][0]!=c:
    collision=(seen[s],(c,ab));break
   seen[s]=(c,ab)
  if collision:bad.append((W,collision))
  else:break
 print(m,L,'H',H,'products',len(P),'minW',W,'guard',max(0,W-H),'lastcollision',bad[-1] if bad else None,flush=True)
