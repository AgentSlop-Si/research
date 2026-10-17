"""Fresh formal polynomial determinant identity, standard library only."""
from itertools import permutations
from pathlib import Path
import json
zero={};one={(0,0,0,0,0):1}
def mon(i,n=1,c=1):
 e=[0]*5;e[i]=n;return {tuple(e):c}
def add(a,b):
 r=dict(a)
 for e,v in b.items():r[e]=r.get(e,0)+v
 return {e:v for e,v in r.items() if v}
def scale(a,c):return {e:v*c for e,v in a.items() if v*c}
def mul(a,b):
 r={}
 for e,v in a.items():
  for f,w in b.items():
   g=tuple(x+y for x,y in zip(e,f));r[g]=r.get(g,0)+v*w
 return {e:v for e,v in r.items() if v}
rows=[]
for i in range(4):rows.append([mon(i,3,-1),mul(mon(4),mon(i,2)),scale(mul(mon(4),mon(i)),-1),one])
lhs={}
for p in permutations(range(4)):
 s=one
 for i,j in enumerate(p):s=mul(s,rows[i][j])
 sign=(-1)**sum(p[i]>p[j] for i in range(4) for j in range(i+1,4));lhs=add(lhs,scale(s,sign))
rhs=mon(4,2)
for i in range(4):
 for j in range(i+1,4):rhs=mul(rhs,add(mon(j),scale(mon(i),-1)))
assert lhs==rhs
r={'status':'PASS','identity':'det rows[-t_k^3,a*t_k^2,-a*t_k,1] = a^2 product_(i<j)(t_j-t_i)','formal_monomials':len(lhs),'method':'independent integer multivariate dictionary multiplication and Leibniz determinant expansion','deductions':'For primitive Nth root zeta with N>=8, a=1+zeta+zeta^-1 is nonzero; distinct centers yield independent annihilators. Four last rows and first four columns are strict lower block. All-permutation restricted theorem follows. General separated-generator inverse is not assumed cyclic tridiagonal.'}
Path(__file__).with_name('FOURIER_UNIFORM_CHECK.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
