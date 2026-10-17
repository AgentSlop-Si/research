"""Reviewer-authored exact rational matrix controls, no project-code imports."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

def eye(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def lin(A,a,B,b):return [[a*x+b*y for x,y in zip(ar,br)] for ar,br in zip(A,B)]
def mm(A,B):return [[sum(x*y for x,y in zip(ar,bc)) for bc in zip(*B)] for ar in A]
def transpose(A):return list(map(list,zip(*A)))
def rank(A):
 B=[r[:] for r in A];i=0
 for j in range(len(B[0])):
  q=next((k for k in range(i,len(B)) if B[k][j]),None)
  if q is None:continue
  B[i],B[q]=B[q],B[i];v=B[i][j];B[i]=[x/v for x in B[i]]
  for k in range(len(B)):
   if k!=i:
    v=B[k][j];B[k]=[x-v*y for x,y in zip(B[k],B[i])]
  i+=1
  if i==len(B):break
 return i

def inv(A):
 n=len(A);B=[r[:]+e for r,e in zip(A,eye(n))]
 for j in range(n):
  k=next((k for k in range(j,n) if B[k][j]),None)
  if k is None:return None
  B[j],B[k]=B[k],B[j];v=B[j][j];B[j]=[x/v for x in B[j]]
  for k in range(n):
   if k!=j:
    v=B[k][j];B[k]=[x-v*y for x,y in zip(B[k],B[j])]
 return [r[n:] for r in B]

def cycle(order,w):
 n=len(order);Q=[[F(0) for j in order] for i in order]
 for j in range(n):Q[order[(j+1)%n]][order[j]]=F(w[j])
 return Q

def block(A,I,J):return [[A[i][j] for j in J] for i in I]
count=0;cuts=0;degenerate_cases=set();max_gram=0
for n in [4,6,8]:
 I=eye(n)
 orders=[list(range(n)),list(range(0,n,2))+list(range(1,n,2))]
 weights=[[1]*(n-1)+[-1],[2,F(1,2)]+[1]*(n-2),[0]+[1]*(n-1),[0,1,0]+[1]*(n-3)]
 for order,w in product(orders,weights):
  Q=cycle(order,w)
  for a,b,c,d in product([-1,0,1],repeat=4):
   A=lin(I,F(a),Q,F(b));B=lin(I,F(c),Q,F(d));Ai=inv(A);Bi=inv(B)
   if Ai is None or Bi is None:continue
   R=mm(B,Ai);C=mm(A,Bi)
   assert mm(R,C)==I
   G=mm(transpose(R),R)
   count+=1
   if a==0:degenerate_cases.add('a=0')
   if b==0:degenerate_cases.add('b=0')
   if a*d==b*c:degenerate_cases.add('ad-bc=0')
   if 0 in w:degenerate_cases.add('zero cycle weight')
   for j in range(n):
    S=[order[(j+k)%n] for k in range(n//2)];T=[i for i in range(n) if i not in S]
    assert rank(block(R,S,T))<=1 and rank(block(R,T,S))<=1
    rg=rank(block(G,S,T));assert rg<=2;max_gram=max(max_gram,rg);cuts+=1
# Pair separation on every circular arrangement reduces to distinct positions.
sep=0
for n in [4,6,8,10]:
 for i in range(n):
  for j in range(n):
   if i!=j:
    assert any(i in [(s+k)%n for k in range(n//2)] and j not in [(s+k)%n for k in range(n//2)] for s in range(n))
    sep+=1
# Explicit higher-degree boundary: it is not a blanket rational-function gate.
Q=cycle(list(range(8)),[2,3,5,7,11,13,17,19]);I=eye(8);Q2=mm(Q,Q)
H=lin(lin(I,F(1),Q,F(1)),F(1),Q2,F(1));G=mm(transpose(H),H)
boundary={'factor_cross_rank':rank(block(H,list(range(4)),list(range(4,8)))),'gram_cross_rank':rank(block(G,list(range(4)),list(range(4,8)))),'factor_invertible':inv(H) is not None}
assert boundary['gram_cross_rank']>2
out={'verdict':'PASS','exact_mobius_instances':count,'exact_contiguous_cuts':cuts,'degenerate_cases':sorted(degenerate_cases),'largest_observed_gram_cross_rank':max_gram,'circular_pair_separation_controls':sep,'higher_degree_countercontrol':boundary}
(Path(__file__).parent/'INDEPENDENT_MOBIUS_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
