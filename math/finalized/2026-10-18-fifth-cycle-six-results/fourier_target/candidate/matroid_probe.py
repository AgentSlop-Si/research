import numpy as np, json
p=1000003;n=8;perm=[7,0,6,3,4,1,2,5]
rng=np.random.default_rng(123)
z=rng.integers(1,99,size=(2,5,8)).astype(np.int64)
def stage(v):
 d,l,m,u,w=v;return np.diag(d)+np.tril(np.outer(l,m),-1)+np.triu(np.outer(u,w),1)
A,B=map(stage,z)
J=[]
for k in range(80):
 zz=z.copy();zz.flat[k]+=1;AA,BB=map(stage,zz)
 J.append((((BB-B)[:,perm]@A+B[:,perm]@(AA-A))%p).ravel().tolist())
M=[[J[i][j] for j in range(64)] for i in range(80)]
row=0;piv=[]
for c in range(64):
 k=next((k for k in range(row,80) if M[k][c]),None)
 if k is None:continue
 M[k],M[row]=M[row],M[k];u=pow(M[row][c],-1,p);M[row]=[v*u%p for v in M[row]]
 for k in range(80):
  if k!=row and M[k][c]:
   u=M[k][c];M[k]=[(a-u*b)%p for a,b in zip(M[k],M[row])]
 piv.append(c);row+=1
free=[c for c in range(64) if c not in piv]
N=[]
for f in free:
 v=[0]*64;v[f]=1
 for k,c in enumerate(piv):v[c]=-M[k][f]%p
 N.append(v)
print('rank',row,'free',free,'fundamental_supports',[[i for i,v in enumerate(a) if v] for a in N])
# Each rank-one normal subspace coordinate condition hyperplanes; find N-combinations with 3 prescribed zero rows.
from itertools import combinations
best=[];small=65
for zero in combinations(range(64),3):
 R=[[N[k][i] for k in range(4)] for i in zero]; r=0;pv=[]
 for c in range(4):
  j=next((j for j in range(r,3) if R[j][c]),None)
  if j is None:continue
  R[j],R[r]=R[r],R[j];u=pow(int(R[r][c]),-1,p);R[r]=[v*u%p for v in R[r]]
  for j in range(3):
   if j!=r and R[j][c]:
    u=R[j][c];R[j]=[(a-u*b)%p for a,b in zip(R[j],R[r])]
  pv.append(c);r+=1
  if r==3:break
 if r!=3:continue
 f=next(k for k in range(4) if k not in pv);coef=[0]*4;coef[f]=1
 for k,c in enumerate(pv):coef[c]=-R[k][f]%p
 v=[sum(coef[k]*N[k][i] for k in range(4))%p for i in range(64)]
 sup=[i for i,x in enumerate(v) if x]
 if len(sup)<small:small=len(sup);best=sup
print('smallest support',small,best,'entries',[(i//8,i%8) for i in best])
open('MATROID_PROBE.json','w').write(json.dumps(dict(rank=row,smallest_generic_normal_support=small,entries=[(i//8,i%8) for i in best]),indent=2)+'\n')
