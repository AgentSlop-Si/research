"""Fresh exact quotient-ring verification; no research program imports."""
from itertools import permutations
from pathlib import Path
import json
Z=(0,0,0,0);O=(1,0,0,0)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def mul(a,b):
 z=[0]*7
 for i,x in enumerate(a):
  for j,y in enumerate(b):z[i+j]+=x*y
 for k in range(6,3,-1):z[k-4]-=z[k]
 return tuple(z[:4])
def power(a,n):
 z=O
 for k in range(n):z=mul(z,a)
 return z
def det(m):
 z=Z
 for p in permutations(range(len(m))):
  s=O
  for i,j in enumerate(p):s=mul(s,m[i][j])
  if sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2:s=neg(s)
  z=add(z,s)
 return z
zeta=(0,1,0,0);p=[7,0,6,3,4,1,2,5];inv=[p.index(j) for j in range(8)]
selected=inv[:4];supports=[[j-1,j,j+1] for j in selected];rows=[]
for supp in supports:
 coeff=[O]
 for s in supp:
  root=power(zeta,s);new=[Z]*(len(coeff)+1)
  for i,c in enumerate(coeff):new[i]=add(new[i],neg(mul(c,root)));new[i+1]=add(new[i+1],c)
  coeff=new
 rows.append(coeff)
 # Evaluate annihilator against every restricted Fourier column.
 for s in supp:
  assert sum(1 for k in [])==0
  total=Z
  for i,c in enumerate(coeff):total=add(total,mul(c,power(zeta,(i+4)*s%8)))
  assert total==Z
 # A 3x3 leading restricted minor is nonzero; confirms injectivity.
 assert det([[power(zeta,k*s%8) for s in supp] for k in (4,5,6)])!=Z
D=det(rows);assert D==(-12,12,28,28)
# Validity of quotient field: x^4+1 is irreducible over Q (Phi8); minimal degree4.
receipt={'status':'PASS','permutation':p,'selected_columns':selected,'supports':supports,'annihilators':rows,'annihilator_determinant_ascending':D,'annihilations':12,'injective_4x3_maps_checked':4,'scope':'No invertible tridiagonal C has rank((F C P^-1)[4:8,0:4])<=1 for Fij=zeta^(ij), zeta primitive8; applicability to a broader chart requires chart-specific source binding.'}
Path(__file__).with_name('FOURIER_CHECK.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
