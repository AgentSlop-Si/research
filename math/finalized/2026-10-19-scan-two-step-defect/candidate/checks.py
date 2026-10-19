"""Exact checks of the new boundary identities; never constructs H_N."""
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent

def rev(x,m):
    out=0
    for _ in range(m): out=(out<<1)|(x&1); x>>=1
    return out

def add(out,k,v):
    out[k]=out.get(k,0)+v
    if not out[k]: del out[k]

def T_apply(v,n):
    out={}
    for x,c in v.items():
        add(out,x,(4 if x==0 else 3)*c)
        if x: add(out,x-1,c)
        if x+1<n: add(out,x+1,c)
    return out

def P_apply(v,m): return {rev(x,m):c for x,c in v.items()}
def Tp_apply(v,n,m): return P_apply(T_apply(P_apply(v,m),n),m)
def actual_column(x,n,m):
    left=T_apply(Tp_apply({x:1},n,m),n)
    right=Tp_apply(T_apply({x:1},n),n,m)
    for k,v in right.items():add(left,k,-v)
    return left

def predicted(m):
    n=1<<m
    a=[(1<<r)-1 for r in range(m+1)]
    b=[n-(1<<r) for r in range(m+1)]
    c=[1<<r for r in range(m)]
    d=[n-1-(1<<r) for r in range(m)]
    K={}
    def wedge(i,j,v):
        add(K,(i,j),v);add(K,(j,i),-v)
    for r in range(1,m-1):
        wedge(a[r],b[r+1],1);wedge(a[r+1],b[r],-1)
    for r in range(m-1):
        wedge(c[r],d[r+1],-1);wedge(c[r+1],d[r],1)
    for k,v in [(a[1],-1),(a[m-1],-1),(b[1],1),(b[m-1],1)]:wedge(0,k,v)
    wedge(a[1],n-1,-1);wedge(b[m-1],n-1,1)
    S=[0,n-1]+a[1:m]+b[1:m]+c[1:m-1]+d[1:m-1]
    assert len(S)==len(set(S))==4*m-4
    return K,S,(a,b,c,d)

def rank(matrix,p=None):
    A=[[Fraction(x) if p is None else x%p for x in row] for row in matrix]
    rows=len(A);cols=len(A[0]);r=0
    for j in range(cols):
        pivot=next((i for i in range(r,rows) if A[i][j]),None)
        if pivot is None:continue
        A[r],A[pivot]=A[pivot],A[r]
        c=1/A[r][j] if p is None else pow(A[r][j],-1,p)
        A[r]=[x*c if p is None else x*c%p for x in A[r]]
        for i in range(r+1,rows):
            c=A[i][j]
            A[i]=[x-c*y if p is None else (x-c*y)%p for x,y in zip(A[i],A[r])]
        r+=1
    return r

def kernel_vector(m,parameters,labels):
    a,b,c,d=labels;n=1<<m
    if m%2==0:
        av,z=parameters;v={0:z,n-1:2*z}
        for r in range(1,m):v[a[r]]=v[b[r]]=av+(z if r%2==0 else 0)
        for r in range(1,m-1):v[c[r]]=v[d[r]]=av
    else:
        av,bv,z,w=parameters;v={0:z,n-1:w}
        for r in range(1,m):v[a[r]]=av if r%2 else bv;v[b[r]]=bv if r%2 else av
        for r in range(1,m-1):v[c[r]]=bv-z if r%2 else av;v[d[r]]=av+z-w if r%2 else bv
    return v

results=[]
for m in range(3,13):
    n=1<<m;K,S,labels=predicted(m)
    predicted_columns={x:{} for x in S}
    for (i,j),v in K.items():predicted_columns[j][i]=v
    for x in range(n):assert actual_column(x,n,m)==predicted_columns.get(x,{}),(m,x)
    assert {i for i,j in K}==set(S)=={j for i,j in K}
    mat=[[K.get((i,j),0) for j in S] for i in S]
    expected=4*m-(6 if m%2==0 else 8)
    assert rank(mat)==expected
    for p in (2,3,5):assert rank(mat,p)==expected
    dker=2 if m%2==0 else 4
    for r in range(dker):
        par=[0]*dker;par[r]=1;v=kernel_vector(m,par,labels)
        for i in S:assert sum(K.get((i,j),0)*v[j] for j in S)==0
    results.append({'m':m,'N':n,'support_size':len(S),'rational_rank':expected,'modular_rank_control_primes':[2,3,5],'kernel_parameterization':'verified','all_original_columns_match_symbolic_formula':True})

record={'scope':'New commutator identity only; no H_N construction or rank check. Uniform proofs are in REPORT.md.','checks':results,'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
(HERE/'RESULTS.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
