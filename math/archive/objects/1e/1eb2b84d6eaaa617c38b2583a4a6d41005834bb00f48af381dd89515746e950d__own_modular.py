"""Independent second-audit controls. No research program loaded or executed.
Only the inert JSON parameter certificates named below are read.
"""
from pathlib import Path
from itertools import permutations
from math import gcd,isqrt
import json, random, hashlib
ROOT=Path(__file__).resolve().parent
OUT=ROOT

def eye(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def add(a,b,p): return [[(x+y)%p for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def sub(a,b,p): return [[(x-y)%p for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def mul(a,b,p): return [[sum(x*y for x,y in zip(ar,bc))%p for bc in zip(*b)] for ar in a]
def inverse(a,p):
 n=len(a);t=[r[:]+e for r,e in zip(a,eye(n))]
 for k in range(n):
  s=next(i for i in range(k,n) if t[i][k]%p);t[k],t[s]=t[s],t[k]
  f=pow(t[k][k],-1,p);t[k]=[v*f%p for v in t[k]]
  for i in range(n):
   if i!=k:
    f=t[i][k];t[i]=[(x-f*y)%p for x,y in zip(t[i],t[k])]
 return [r[n:] for r in t]
def rank(a,p):
 if not a:return 0
 t=[r[:] for r in a];k=0
 for j in range(len(t[0])):
  s=next((i for i in range(k,len(t)) if t[i][j]%p),None)
  if s is None: continue
  t[k],t[s]=t[s],t[k];f=pow(t[k][j],-1,p);t[k]=[v*f%p for v in t[k]]
  for i in range(k+1,len(t)):
   f=t[i][j];t[i]=[(x-f*y)%p for x,y in zip(t[i],t[k])]
  k+=1
  if k==len(t):break
 return k

def determinant(a,p):
 t=[r[:] for r in a];d=1;n=len(t)
 for k in range(n):
  s=next((i for i in range(k,n) if t[i][k]%p),None)
  if s is None:return 0
  if s!=k:t[k],t[s]=t[s],t[k];d=-d
  v=t[k][k];d=d*v%p;f=pow(v,-1,p)
  for i in range(k+1,n):
   c=t[i][k]*f%p
   for j in range(k,n):t[i][j]=(t[i][j]-c*t[k][j])%p
 return d%p

def prime(n):return n>=2 and all(n%d for d in range(2,isqrt(n)+1))
def field(n):
 p=n+1
 while not prime(p):p+=n
 for x in range(2,p):
  w=pow(x,(p-1)//n,p)
  if pow(w,n,p)==1 and all(pow(w,n//d,p)!=1 for d in range(2,n+1) if n%d==0 and prime(d)):return p,w
 raise ValueError(n)

