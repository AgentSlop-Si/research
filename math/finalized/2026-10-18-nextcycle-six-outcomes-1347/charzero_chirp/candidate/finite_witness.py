#!/usr/bin/env python3
"""Exact constructive witness in F17[t]/(t^3+8t^2+6t+8)."""
import json,itertools
from pathlib import Path
P=17;Z=(0,0,0);O=(1,0,0)
def add(a,b):return tuple((x+y)%P for x,y in zip(a,b))
def neg(a):return tuple(-x%P for x in a)
def mul(a,b):
 r=[0]*5
 for i,x in enumerate(a):
  for j,y in enumerate(b):r[i+j]=(r[i+j]+x*y)%P
 for k in range(4,2,-1):
  c=r[k]
  for j,v in enumerate([8,6,8]):r[k-3+j]=(r[k-3+j]-c*v)%P
 return tuple(r[:3])
def powf(a,n):
 r=O
 while n:
  if n&1:r=mul(r,a)
  a=mul(a,a);n//=2
 return r
def inv(a):
 if a==Z:raise ValueError('zero')
 r=powf(a,17**3-2);assert mul(a,r)==O;return r
def ev(cs,x):
 y=Z
 for c in reversed(cs):y=add(mul(y,x),(c%17,0,0))
 return y
def conv(a,b):
 out=[Z]*8
 for i,x in enumerate(a):
  for j,y in enumerate(b):out[(i+j)%8]=add(out[(i+j)%8],mul(x,y))
 return out

def make():
 f=[8,6,8,1];g=[1,4,10,1]
 assert all(sum(c*pow(k,j,17) for j,c in enumerate(f))%17 for k in range(17))
 assert all(sum(c*pow(k,j,17) for j,c in enumerate(g))%17 for k in range(17))
 t=(0,1,0);assert ev(f,t)==Z
 u=next(z for z in itertools.product(range(17),repeat=3) if ev(g,z)==Z)
 roots=[(6,0,0),t,powf(t,17),powf(t,17**2),u,powf(u,17),powf(u,17**2)]
 assert len(set(roots))==7
 alphas=[inv(z) for z in roots]
 q=[(pow(3,(-j*j)%16,17),0,0) for j in range(8)]
 prod=[O]+[Z]*7
 for a in alphas:
  assert powf(a,8)!=O
  prod=conv(prod,[O,neg(a)]+[Z]*6)
 assert prod==q
 # Literally execute every legal cyclic resolvent and compare all matrix entries.
 result=[O]+[Z]*7
 for a in alphas:
  den=add(O,neg(powf(a,8)));deninv=inv(den)
  result=conv(result,[mul(powf(a,j),deninv) for j in range(8)])
 result=[mul((8,0,0),z) for z in result]
 C=[(pow(3,j*j%16,17),0,0) for j in range(8)]
 assert result==C
 for i in range(8):
  for j in range(8):assert result[(i-j)%8]==(pow(3,(i-j)**2%16,17),0,0)
 return {'field':'F17[t]/(t^3+8t^2+6t+8)','coordinates':'constant, t, t^2 modulo 17','zeta':3,'scalar_gauge':8,'strides':[1]*7,'roots':roots,'alphas':alphas,'root_polynomials':{'first_cubic':f,'second_cubic':g},'polynomial_factorization_verified':True,'each_alpha_pow8_not_one':True,'full_matrix_entries_verified':64,'exact_minimum':7}
if __name__=='__main__':
 b=Path(__file__).parent;w=make();(b/'FINITE_WITNESS.json').write_text(json.dumps(w,indent=2)+'\n');print(json.dumps(w,indent=2))
