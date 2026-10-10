"""Exact audit of replacing FFT phases by a shared sign-only butterfly core.

This is an offline matrix/certificate laboratory, not a new fast transform.
Finite-field nonzero minors lift to the cyclotomic field for these matrices.
"""
from __future__ import annotations
import math
import numpy as np


def power_two(n):
    if type(n) is not int or n<2 or n&(n-1):raise ValueError('power-of-two n >= 2')
    return n.bit_length()-1


def is_prime(p):
    return type(p) is int and p>=3 and all(p%d for d in range(2,math.isqrt(p)+1))


def root_of_unity(n,p,generator=3):
    power_two(n)
    if not is_prime(p) or (p-1)%n:raise ValueError('prime must support this length')
    if p>=2**31:raise ValueError('int64 arithmetic bound requires p < 2**31')
    w=pow(generator,(p-1)//n,p)
    if pow(w,n,p)!=1 or pow(w,n//2,p)==1:raise ValueError('root not primitive')
    return w


def bit_reverse(n):
    bits=power_two(n)
    return [int(f'{j:0{bits}b}'[::-1],2) for j in range(n)]


def matrices(n,p=65537):
    w=root_of_unity(n,p)
    powers=[pow(w,j,p) for j in range(n)]
    f=np.array([[powers[(i*j)%n] for j in range(n)] for i in range(n)],dtype=np.int64)
    rev=bit_reverse(n)
    c=np.array([[1 if (i&rev[j]).bit_count()%2==0 else p-1 for j in range(n)]
                for i in range(n)],dtype=np.int64)
    return f,c


def mm(a,b,p):
    """Accumulate one outer product at a time to avoid int64 dot overflow."""
    a=np.asarray(a,dtype=np.int64)%p;b=np.asarray(b,dtype=np.int64)%p
    if a.ndim!=2 or b.ndim!=2 or a.shape[1]!=b.shape[0]:raise ValueError('matrix shape')
    if p>=2**31:raise ValueError('int64 arithmetic bound')
    out=np.zeros((a.shape[0],b.shape[1]),dtype=np.int64)
    for k in range(a.shape[1]):out=(out+a[:,k,None]*b[k,None,:])%p
    return out


def elimination_certificate(a,p):
    """Return pivot original rows/columns and the determinant of their minor."""
    a=np.asarray(a,dtype=np.int64).copy()%p
    row_ids=list(range(a.shape[0]));rows=[];cols=[];pivot_values=[];r=0
    for c in range(a.shape[1]):
        hits=np.flatnonzero(a[r:,c])
        if len(hits)==0:continue
        at=r+int(hits[0]);a[[r,at]]=a[[at,r]]
        row_ids[r],row_ids[at]=row_ids[at],row_ids[r]
        rows.append(row_ids[r]);cols.append(c)
        pivot=int(a[r,c]);pivot_values.append(pivot)
        a[r]=(a[r]*pow(pivot,-1,p))%p
        if r+1<a.shape[0]:a[r+1:]=(a[r+1:]-a[r+1:,c,None]*a[r])%p
        r+=1
        if r==a.shape[0]:break
    determinant=1
    for v in pivot_values:determinant=determinant*v%p
    return {'rank_mod_p':r,'rows':rows,'columns':cols,'minor_determinant_mod_p':determinant}


def determinant_python(a,p):
    """Independent arbitrary-precision implementation for certificate replay."""
    a=[[int(x)%p for x in row] for row in a];n=len(a);out=1
    if any(len(row)!=n for row in a):raise ValueError('square matrix')
    for col in range(n):
        pivot=next((i for i in range(col,n) if a[i][col]),None)
        if pivot is None:return 0
        if pivot!=col:a[col],a[pivot]=a[pivot],a[col];out=-out%p
        v=a[col][col];out=out*v%p;inv=pow(v,-1,p)
        for i in range(col+1,n):
            factor=a[i][col]*inv%p
            if factor:
                for j in range(col+1,n):a[i][j]=(a[i][j]-factor*a[col][j])%p
            a[i][col]=0
    return out


def kernel_basis(n):
    """e_0 and indicators of the distinct 2-adic valuation classes."""
    bits=power_two(n);out=np.zeros((n,bits+1),dtype=np.int64);out[0,0]=1
    for s in range(bits):out[2**s::2**(s+1),s+1]=1
    return out


def make_certificate(n,p=65537):
    f,c=matrices(n,p);error=(f-c)%p
    cert=elimination_certificate(error,p)
    return {'n':n,'p':p,'root':root_of_unity(n,p),
            'definition':'F[k,j]=w^(k*j); C[k,j]=(-1)^popcount(k & bitreverse(j))',
            'general_lower_bound':n//2-1,'general_upper_bound':n-power_two(n)-1,
            'nonzero_entries':int(np.count_nonzero(error)),
            'kernel_dimension':power_two(n)+1,**cert}


def verify_certificate(cert):
    n=cert['n'];p=cert['p'];f,c=matrices(n,p);e=(f-c)%p
    if cert['root']!=root_of_unity(n,p):return False
    rows=cert['rows'];cols=cert['columns'];rank=cert['rank_mod_p']
    if len(rows)!=rank or len(cols)!=rank:return False
    if len(set(rows))!=rank or len(set(cols))!=rank:return False
    if any(type(i) is not int or i<0 or i>=n for i in rows+cols):return False
    if rank!=n-power_two(n)-1:return False
    if cert['general_upper_bound']!=rank or cert['general_lower_bound']!=n//2-1:return False
    if cert['kernel_dimension']!=power_two(n)+1:return False
    if cert['nonzero_entries']!=n*(n-power_two(n)-1):return False
    if np.count_nonzero(e)!=cert['nonzero_entries']:return False
    det=determinant_python(e[np.ix_(rows,cols)],p)
    if not det or det!=cert['minor_determinant_mod_p']:return False
    return not np.any(mm(e,kernel_basis(n),p))


def stages(n,p=65537,*,phases=True):
    """Iterative radix-two stages; bit reversal is the initial permutation."""
    power_two(n);out=[]
    for bits in range(1,n.bit_length()):
        size=1<<bits;half=size//2;w=root_of_unity(size,p)
        stage=np.zeros((n,n),dtype=np.int64)
        for start in range(0,n,size):
            for k in range(half):
                a=start+k;b=a+half;v=pow(w,k,p) if phases else 1
                stage[a,a]=stage[b,a]=1;stage[a,b]=v;stage[b,b]=-v%p
        out.append(stage)
    return out


def telescope(n,p=65537):
    """Keep the true future stages in the correction; no missing mixed terms."""
    bs=stages(n,p);cs=stages(n,p,phases=False)
    error=np.zeros((n,n),dtype=np.int64);core=np.eye(n,dtype=np.int64)
    full=np.eye(n,dtype=np.int64)
    for b,c in zip(bs,cs):
        error=(mm(b,error,p)+mm((b-c)%p,core,p))%p
        full=mm(b,full,p);core=mm(c,core,p)
    reverse=bit_reverse(n)
    return full[:,reverse],core[:,reverse],error[:,reverse]


def naive_single_corrections(n,p=65537):
    """Intentionally incomplete expansion used only as a negative control."""
    bs=stages(n,p);cs=stages(n,p,phases=False);error=np.zeros((n,n),dtype=np.int64)
    for i in range(len(bs)):
        term=(bs[i]-cs[i])%p
        for j in range(i-1,-1,-1):term=mm(term,cs[j],p)
        for j in range(i+1,len(bs)):term=mm(cs[j],term,p)
        error=(error+term)%p
    return error[:,bit_reverse(n)]


def shared_core_audit(n,g,d0,p=65537):
    """General bound for [[G,D0 G],[G,-D0 G]] after an even/odd split."""
    m=n//2;f=matrices(m,p)[0] if m>1 else np.ones((1,1),dtype=np.int64)
    d=np.array([pow(root_of_unity(n,p),k,p) for k in range(m)],dtype=np.int64)
    d0=np.asarray(d0,dtype=np.int64)%p;g=np.asarray(g,dtype=np.int64)%p
    a=(f-g)%p;b=(d[:,None]*f-d0[:,None]*g)%p
    ra=elimination_certificate(a,p)['rank_mod_p'];rb=elimination_certificate(b,p)['rank_mod_p']
    mismatches=int(np.count_nonzero((d-d0)%p))
    assert ra+rb>=mismatches
    return {'n':n,'rank_first_residual':ra,'rank_second_residual':rb,
            'rank_full_residual':ra+rb,'different_twiddles':mismatches}
