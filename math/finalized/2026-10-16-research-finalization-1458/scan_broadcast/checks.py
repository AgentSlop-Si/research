"""Self-authored exact checks. No historical research programs imported or run."""
from itertools import combinations, product
import random, json
from pathlib import Path

def rank(A,p):
    A=[[x%p for x in row] for row in A]
    if not A:return 0
    r=0
    for j in range(len(A[0])):
        k=next((k for k in range(r,len(A)) if A[k][j]),None)
        if k is None:continue
        A[r],A[k]=A[k],A[r]
        z=pow(A[r][j],-1,p);A[r]=[x*z%p for x in A[r]]
        for k in range(len(A)):
            if k!=r:
                z=A[k][j];A[k]=[(a-z*b)%p for a,b in zip(A[k],A[r])]
        r+=1
        if r==len(A):break
    return r

def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def mul(A,B,p):return [[sum(a*b for a,b in zip(row,col))%p for col in zip(*B)] for row in A]
def sub(A,B,p):return [[(a-b)%p for a,b in zip(x,y)] for x,y in zip(A,B)]
def block(A,I,J):return [[A[i][j] for j in J] for i in I]
def root(n,p):
    return next(z for z in range(1,p) if pow(z,n,p)==1 and all(pow(z,k,p)!=1 for k in range(1,n)))
def fourier(n,p):
    w=root(n,p);return [[pow(w,i*j,p) for j in range(n)] for i in range(n)]
def rigidity(F,S,p):
    n=len(F);v=[sum(x!=0 for x in row) for row in S];r=rank(sub(F,S,p),p)
    assert n<=min(v)+r*(max(v)+1)

results={"historical_code_executed":False,"external_mutations":False}
# N=3 over F7, every row has at most one nonzero: 19^3 matrices.
p=7;n=3;F=fourier(n,p);rows=[[0]*n]
for i in range(n):
    for a in range(1,p):
        row=[0]*n;row[i]=a;rows.append(row)
count=0
for S in product(rows,repeat=n):rigidity(F,S,p);count+=1
results['exhaustive_one_sparse_N3_F7']=count

# All F8 3-by-5 minors in two fields, plus explicit parity-order cuts.
count=0;cut_results={}
for p in (17,97):
    F=fourier(8,p)
    for I in combinations(range(8),3):
        for J in combinations(range(8),5):
            assert rank(block(F,I,J),p)==3;count+=1
    order=[0,2,4,6,1,3,5,7]
    cuts=[[rank(block(F,order[:k],order[k:]),p),rank(block(F,order[k:],order[:k]),p)] for k in range(1,8)]
    assert cuts==[[z,z] for z in (1,2,3,2,3,2,1)]
    cut_results[str(p)]=cuts
results['F8_3x5_minors']=count;results['F8_parity_cuts']=cut_results

# Random inverse words, keeping a separate broadcast-deleted product.
rng=random.Random(20261016);count=0
for n in (2,3,4,6,8,12):
    p=97;F=fourier(n,p)
    for t in range(7):
        for trial in range(6):
            Q=S=eye(n);B=0
            for step in range(t+1):
                perm=list(range(n));rng.shuffle(perm)
                M=[[0]*n for _ in range(n)]
                for i,j in enumerate(perm):M[i][j]=rng.randrange(1,p)
                Q=mul(Q,M,p);S=mul(S,M,p)
                if rng.randrange(2):
                    while True:
                        u=[rng.randrange(p) for _ in range(n)];v=[rng.randrange(p) for _ in range(n)]
                        if (1+sum(a*b for a,b in zip(u,v)))%p:break
                    K=[[(int(i==j)+u[i]*v[j])%p for j in range(n)] for i in range(n)]
                    Q=mul(Q,K,p);B+=1
                if step<t:
                    D=eye(n);forward=rng.randrange(2)
                    for i in range(n):
                        D[i][i]=rng.randrange(1,p)
                        if forward and i:D[i][i-1]=rng.randrange(p)
                        if not forward and i<n-1:D[i][i+1]=rng.randrange(p)
                    Q=mul(Q,D,p);S=mul(S,D,p)
            supports=[sum(z!=0 for z in row) for row in S]
            assert max(supports)<=2**t
            assert min(supports)<=(2**(t-1) if t else 1)
            assert rank(sub(Q,S,p),p)<=B
            rigidity(F,S,p);count+=1
results['interleaved_inverse_words']=count

# Cyclic-consecutive Vandermonde minors: exhaustive small sizes.
count=0
for n,p in ((2,7),(3,7),(4,17),(6,97),(8,17)):
    F=fourier(n,p)
    for k in range(1,n+1):
        for a in range(n):
            I=[(a+j)%n for j in range(k)]
            for J in combinations(range(n),k):
                assert rank(block(F,I,J),p)==k;count+=1
results['consecutive_vandermonde_minors']=count

# Counterexample: H10=a1*b0=1, H21=a2*b1=1 force H20 !=0.
count=0
for a1,a2,b0,b1 in product(range(7),repeat=4):
    if a1*b0%7==1 and a2*b1%7==1:assert a2*a1*b0%7!=0
    count+=1
results['literal_scan_counterexample_parameter_tuples']=count

# Exact integer threshold and old-versus-refined comparison.
for n in range(2,513):
    for t in range(1,12):
        q=2**t+1;v=max(0,-(-(n-2**(t-1))//q))
        assert v>=n//q
        assert 2**(t-1)+v*q>=n
        assert v==0 or 2**(t-1)+(v-1)*q<n
results['N64_minimum_B']=[32]+[max(0,-(-(64-2**(t-1))//(2**t+1))) for t in range(1,8)]
assert results['N64_minimum_B']==[32,21,13,7,4,2,1,0]
results['all_checks_passed']=True
out=Path(__file__).with_name('CHECK_RESULTS.json');out.write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
