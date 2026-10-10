"""Exact rational witness proving full Macaulay rank is Zariski-generic.
This witnesses genericity for unrestricted ternary 2x4 pencils, NOT for
seven-Green constrained parametrizations at every N.
"""
from phase39_bivariate import macaulay, MON2
import numpy as np
import sympy as s

p=998244353
rows=[
 [(-1,1,0),(1,0,0),(-1,0,-1),(1,1,0)],
 [(0,-1,1),(-1,1,-1),(1,-1,0),(1,-1,-1)]
]
Bs=[]
for k in range(3):
 b=np.zeros((4,4),dtype=np.int64)
 for i in range(2):
  for j in range(4):b[i,j]=rows[i][j][k]
 Bs.append(b)
inst={'p':p,'T':np.ones((4,4),dtype=np.int64),
      'B0':Bs[0], 'B1':Bs[1], 'B2':Bs[2]}
# Build integer coefficient matrix directly rather than modulo p and remap.
from phase39_bivariate import MON1,MON3,MON4,FOUR,PATH
x=s.symbols('x0 x1 x2')
B=s.Matrix(2,4,lambda i,j:sum(rows[i][j][k]*x[k] for k in range(3)))

def matrix(kind):
 if kind=='cubic':pairs=FOUR;fact=MON1;mons=MON3
 else:pairs=PATH;fact=MON2;mons=MON4
 out=[]
 for a,b in pairs:
  polynomial=s.Poly(B[0,a]*B[1,b]-B[0,b]*B[1,a],*x)
  for f in fact:
   v=[]
   for m in mons:
    rem=tuple(q-r for q,r in zip(m,f))
    v.append(polynomial.coeff_monomial(s.prod(x[i]**rem[i] for i in range(3))) if min(rem)>=0 else 0)
   out.append(v)
 return s.Matrix(out)

if __name__=='__main__':
 for kind,full in [('cubic',10),('quartic',15)]:
  A=matrix(kind)
  assert A.rank()==full
  print(kind,'rational rank',A.rank(),'/',full)
