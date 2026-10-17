"""Reviewer-authored Laurent arithmetic. Does not import author or historical code."""
from itertools import combinations, permutations
from pathlib import Path
import json
N=8

def add(a,b):
 c=a.copy()
 for k,v in b.items():
  c[k]=c.get(k,0)+v
  if c[k]==0: del c[k]
 return c

def scale(a,x):return {k:v*x for k,v in a.items() if v*x}
def mul(a,b):
 c={}
 for k,v in a.items():
  for l,w in b.items(): c[k+l]=c.get(k+l,0)+v*w
 return {k:v for k,v in c.items() if v}
def star(a):return {-k:v for k,v in a.items()}
def zero():return [[{} for j in range(N)] for i in range(N)]
def ident():
 r=zero()
 for i in range(N):r[i][i]={0:1}
 return r

def mm(A,B):
 R=zero()
 for i in range(N):
  for j in range(N):
   s={}
   for k in range(N):s=add(s,mul(A[i][k],B[k][j]))
   R[i][j]=s
 return R

def dag(A):return [[star(A[j][i]) for j in range(N)] for i in range(N)]
def lin(A,c,B,d):return [[add(scale(A[i][j],c),scale(B[i][j],d)) for j in range(N)] for i in range(N)]
def cycle(order,weights):
 R=zero()
 for j in range(N):R[order[(j+1)%N]][order[j]]=weights[j]
 return R
M1=cycle(list(range(8)),[{0:1}]*7+[{0:-1}])
M2=cycle([0,1,3,4,5,6,2,7],[{1:1}]+[{0:1}]*5+[{-1:1},{0:-1}])
I=ident()

def knum(M,sgn):
 coeff=([3]+[1]*7) if sgn==1 else [129,-64,-32,-16,-8,-4,-2,-1]
 out=zero();power=I
 for c in coeff:
  out=lin(out,1,power,c);power=mm(power,M)
 assert power==lin(I,-1,I,0)
 return out, (2 if sgn==1 else 257)

perms=list(permutations(range(3)))
def det3(A,rows,cols):
 z={}
 for p in perms:
  v={0:1}
  for i in range(3):v=mul(v,A[rows[i]][cols[p[i]]])
  inv=sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
  z=add(z,scale(v,(-1)**inv))
 return z

results=[];all_minors={};grams={}
for s1,s2 in [(-1,-1),(-1,1),(1,-1),(1,1)]:
 K1,d1=knum(M1,s1);K2,d2=knum(M2,s2)
 T=mm(K1,K2);L=mm(dag(T),T)
 # Independent inverse identity check, not using a matrix inverse algorithm.
 J2,e2=knum(M2,-s2);J1,e1=knum(M1,-s1)
 U=mm(J2,J1)
 assert mm(T,U)==lin(I,d1*d2*e1*e2,I,0)
 assert mm(U,T)==lin(I,d1*d2*e1*e2,I,0)
 key=f'{s1},{s2}';grams[key]={'denominator':(d1*d2)**2,'entries':L}
 for extras in combinations(range(2,8),3):
  A=(0,)+extras;B=tuple(x for x in range(8) if x not in A)
  candidates=[]
  for rows in combinations(A,3):
   for cols in combinations(B,3):
    p=det3(L,rows,cols)
    if not p:continue
    dominant=max(abs(v) for v in p.values())
    bound=2*dominant-sum(abs(v) for v in p.values())
    candidates.append({'rows':rows,'cols':cols,'polynomial':p,'reverse_triangle_numerator':bound})
  winner=max(candidates,key=lambda x:x['reverse_triangle_numerator'])
  results.append({'signs':[s1,s2],'cut':A,'complement':B,'denominator':(d1*d2)**6,**winner})
  all_minors[key+'/'+str(A)]=candidates
out=Path(__file__).parent
(out/'FRESH_CUT_RESULTS.json').write_text(json.dumps({'method':'Integer Laurent ring reconstruction, exact factor inverse identities, all 16 cubic minors per cut, independent coefficient-dominance checks','tested_cuts':len(results),'positive_dominance_certificates':sum(r['reverse_triangle_numerator']>0 for r in results),'results':results},indent=2)+'\n')
(out/'FRESH_GRAMS.json').write_text(json.dumps(grams,indent=2)+'\n')
(out/'FRESH_ALL_MINORS.json').write_text(json.dumps(all_minors,indent=2)+'\n')
print('Cuts:',len(results),'dominance-positive:',sum(r['reverse_triangle_numerator']>0 for r in results))
print('Unresolved:',[(r['signs'],r['cut'],r['reverse_triangle_numerator']) for r in results if r['reverse_triangle_numerator']<=0])
