import sys,itertools,json
sys.path.insert(0,'.');import pilot as a
L=[(0,7),(0,8),(1,7)]
Q,F,g=a.system(L)
def shift(P,centers):
 from math import comb
 R={}
 for e,v in P.items():
  for j in itertools.product(*(range(k+1)for k in e)):
   c=v
   for k in range(3):c=c*comb(e[k],j[k])*pow(centers[k],e[k]-j[k],a.p)%a.p
   R[j]=(R.get(j,0)+c)%a.p
 return {e:v for e,v in R.items()if v}
cent=[]
for j in range(3):
 d=next(d for d in g if tuple(int(k==j)for k in range(3)) in d)
 cent.append(-pow(d[tuple(int(k==j)for k in range(3))],-1,a.p)%a.p)
Qs=[shift(q,cent)for q in Q]
print('shift support',len(set().union(*(q.keys()for q in Qs))))
print('base',a.rank(Qs))
M=[a.mul(q,a.mon(e))for e in [a.ZERO,(1,0,0),(0,1,0),(0,0,1)]for q in Qs]
print('affine',a.rank(M));support=set().union(*(q.keys()for q in M));print('missing',sorted(set(itertools.product(range(5),repeat=3))-support))
print('F shifted',shift(F,cent))
