# Independent, exact rational-basis exploration. No imported research source.
import sympy as S
from itertools import combinations
n=6
# encode real cos values with c5=-1/2-c1-c2-c3-c4, exact symbolic linear in them
cs=S.symbols('c1:5'); cos=[None,*cs,-S.Rational(1,2)-sum(cs)]
E=S.zeros(n)
for i in range(n):
 for j in range(n):
  if i*j==0:E[i,j]=1
  else:
   k=(i*j)%11;k=min(k,11-k);E[i,j]=cos[k]
w=[1,2,2,2,2,2]
def nnz(X):return sum(x!=0 for x in X)
def nzA(P):return sum(w[j] for i in range(n) for j in range(n) if P[i,j]!=0)
def nzC(Q):return sum(w[i] for i in range(n) for j in range(n) if Q[i,j]!=0)
# Family: anchor input on x0 with parameter a, then differences to a selected sum row.
Ps=[]
for a in [0,1,-1,2,-2,S.Rational(1,2),-S.Rational(1,2)]:
 for mask in range(32):
  P=S.eye(n)
  for j in range(1,6):
   if mask>>(j-1)&1:P[j,0]=a
  for anchor in range(6):
   for mask2 in range(32) if anchor else [0]:
    R=P.copy()
    for j in range(1,6):
     if j!=anchor and (mask2>>(j-1)&1):R[j,:]=P[j,:]-P[anchor,:]
    Ps.append(R)
# remove duplicates
Ps=list({tuple(P):P for P in Ps}.values())
print('candidates',len(Ps),flush=True)
# Single sided trivial identities can be pruned cost budgets. Symmetric P/Q family expensive use first cheap subset
best=(58,None)
for P in Ps:
 B=E*P.inv();B=B.applyfunc(S.expand)
 cost=nzA(P)+nnz(B)+11
 if cost<best[0]:
  best=(cost,P);print('best single',cost,P.tolist(),flush=True)
print(best[0])
