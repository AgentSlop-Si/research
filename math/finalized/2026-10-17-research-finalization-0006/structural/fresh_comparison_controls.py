"""Fresh exact controls; no imports of historical research programs or data."""
from fractions import Fraction as Q
from itertools import combinations
import json
from pathlib import Path

def rank(A):
    a=[[Q(x) for x in row] for row in A]
    if not a:return 0
    r=0
    for c in range(len(a[0])):
        p=next((i for i in range(r,len(a)) if a[i][c]),None)
        if p is None:continue
        a[r],a[p]=a[p],a[r]
        z=a[r][c];a[r]=[v/z for v in a[r]]
        for i in range(len(a)):
            if i!=r:
                z=a[i][c];a[i]=[x-z*y for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a):break
    return r

def prod(A,B):return [[sum(x*y for x,y in zip(r,c)) for c in zip(*B)] for r in A]
def block(A,I,J):return [[A[i][j] for j in J] for i in I]
def demand(ok,label):
    if not ok:raise RuntimeError(label)

checks={}
# Ordinary-order quasiseparability is not invariant under independent endpoint permutations.
I=[[int(i==j) for j in range(4)] for i in range(4)]
P=block(I,range(4),[2,3,0,1])
demand(rank(block(I,[0,1],[2,3]))==0,'diagonal upper cut')
demand(rank(block(P,[0,1],[2,3]))==2,'independent permutation raises cut rank')
checks['independent_endpoint_permutation']={'ordinary_rank_before':0,'ordinary_rank_after':2,'same_transported_order_rank':0}
# A scalar full-support row can be killed by a legal singular first-order difference.
for n in range(3,21):
    B=[[int(i==j)-int(j==(i+1)%n) for j in range(n)] for i in range(n)]
    demand(prod([[1]*n],B)==[[0]*n],'constant scalar row killed')
checks['scalar_support_does_not_survive_difference']={'lengths':list(range(3,21)),'all_pass':True}
# Exact Cauchy target, sparse mixing and sufficient column count; arbitrary fields not inferred.
n=5;T=[[Q(1,i+j+1) for j in range(n)] for i in range(n)]
minor_count=0
for k in range(1,n+1):
    for X in combinations(range(n),k):
        for Y in combinations(range(n),k):
            demand(rank(block(T,X,Y))==k,'Cauchy full spark');minor_count+=1
mix_count=0
for shift in [Q(-2),Q(0),Q(3,2)]:
    P=[[Q(int(i==j))+ (shift if j==i+1 else 0) for j in range(n)] for i in range(n)]
    M=prod(P,T)
    for m in [1,2]:
        for X in combinations(range(n),m):
            for c in range(2*m,n+1):
                for Y in combinations(range(n),c):
                    demand(rank(block(M,X,Y))==m,'sparse mix rank');mix_count+=1
checks['sparse_mixing']={'cauchy_minors':minor_count,'rectangles':mix_count,'all_pass':True}
# Exact counterexample if the sufficient c>=s*m guard is discarded.
P=[[Q(1),Q(-2),0,0,0]]+[[Q(int(i==j)) for j in range(n)] for i in range(1,n)]
demand(rank(P)==n,'P invertible')
demand(prod(P,T)[0][0]==0,'too few columns cancel')
checks['insufficient_column_guard']={'N':5,'m':1,'s':2,'columns':1,'rank':0,'P_first_row':['1','-2','0','0','0']}
# Cyclic Green off-diagonal ranks follow from block equations, allowing zero weights.
# Explicit inverse by exact Gaussian elimination is fresh and bounded.
def inv(A):
    n=len(A);a=[[Q(v) for v in row]+[Q(i==j) for j in range(n)] for i,row in enumerate(A)]
    for c in range(n):
        p=next((i for i in range(c,n) if a[i][c]),None)
        if p is None:raise ValueError('singular')
        a[c],a[p]=a[p],a[c]
        z=a[c][c];a[c]=[v/z for v in a[c]]
        for i in range(n):
            if i!=c:
                z=a[i][c];a[i]=[x-z*y for x,y in zip(a[i],a[c])]
    return [row[n:] for row in a]
count=0
for n in range(3,9):
    for weights in [[Q(1,2)]*n,[0]+[Q(1,2)]*(n-1),[Q(-1,3)]*n]:
        A=[[Q(int(i==j))-(weights[i] if j==(i+1)%n else 0) for j in range(n)] for i in range(n)]
        G=inv(A)
        for k in range(1,n):
            for X,Y in [(range(k),range(k,n)),(range(k,n),range(k))]:
                demand(rank(block(G,X,Y))==rank(block(A,X,Y))<=1,'same-cut inverse rank');count+=1
checks['cyclic_green_same_cut_nullity']={'checked_blocks':count,'zero_weight_cases':6,'all_pass':True}
result={'verdict':'PASS','scope':'Finite exact controls of comparison boundaries; no historical code execution, new uniform proof, performance measurement or novelty conclusion.','checks':checks}
print(json.dumps(result,indent=2))
Path(__file__).with_name('CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
