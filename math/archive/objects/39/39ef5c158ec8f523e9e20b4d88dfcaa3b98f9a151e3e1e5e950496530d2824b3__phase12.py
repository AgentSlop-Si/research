"""Hero #17 Phase 12: reproducible *restricted* FFT Green-Union rigidity.

Conventions: F[k,j] = omega^(k*j), all matrices use mod prime q.
The unconditional mathematical results in RESEARCH.md are over C;
finite-field additive-uncertainty runs require independently audited full spark.
"""
from __future__ import annotations
from itertools import combinations
from math import gcd
import random


def prime_factors(n: int) -> list[int]:
    fs, d = [], 2
    while d*d <= n:
        if n % d == 0:
            fs.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        fs.append(n)
    return fs


def primitive_root_of_order(n: int, q: int) -> int:
    if (q-1) % n:
        raise ValueError('n must divide q-1')
    for root in range(2, q):
        w = pow(root, (q-1)//n, q)
        if pow(w,n,q)==1 and all(pow(w,n//d,q)!=1 for d in prime_factors(n)):
            return w
    raise ValueError('primitive nth root absent')


def eye(n):
    return [[int(i==j) for j in range(n)] for i in range(n)]


def mult(A,B,q):
    n=len(A); k=len(B); m=len(B[0]);
    assert len(A[0])==k
    Bt=list(zip(*B))
    return [[sum(x*y for x,y in zip(A[i],Bt[j]))%q for j in range(m)] for i in range(n)]


def add(A,B,q):
    return [[(x+y)%q for x,y in zip(rowA,rowB)] for rowA,rowB in zip(A,B)]


def subtract(A,B,q):
    return [[(x-y)%q for x,y in zip(rowA,rowB)] for rowA,rowB in zip(A,B)]


def rank(A,q):
    C=[row[:] for row in A]
    if not C:return 0
    nr=len(C); nc=len(C[0]); r=0
    for c in range(nc):
        piv=next((i for i in range(r,nr) if C[i][c]%q),None)
        if piv is None:continue
        C[r],C[piv]=C[piv],C[r]
        inv=pow(C[r][c],-1,q)
        C[r]=[(v*inv)%q for v in C[r]]
        for i in range(nr):
            if i!=r and C[i][c]:
                z=C[i][c]
                C[i]=[(a-z*b)%q for a,b in zip(C[i],C[r])]
        r+=1
        if r==nr:break
    return r


def inverse(A,q):
    n=len(A); C=[row[:]+eye(n)[i] for i,row in enumerate(A)]
    for c in range(n):
        piv=next((r for r in range(c,n) if C[r][c]%q),None)
        if piv is None:raise ValueError('matrix singular')
        C[c],C[piv]=C[piv],C[c]
        v=pow(C[c][c],-1,q)
        C[c]=[(z*v)%q for z in C[c]]
        for i in range(n):
            if i!=c and C[i][c]:
                a=C[i][c]
                C[i]=[(x-a*y)%q for x,y in zip(C[i],C[c])]
    return [row[n:] for row in C]


def fourier(n,q,inv=False):
    w=primitive_root_of_order(n,q)
    if inv:w=pow(w,-1,q)
    N_inv=pow(n,-1,q) if inv else 1
    return [[N_inv*pow(w,i*j,q)%q for j in range(n)] for i in range(n)]


def green_inverse(n,q,alpha,shift):
    """I-alpha S^shift; 2-sparse per row and column when shift!=0."""
    B=eye(n)
    for j in range(n):
        B[(j+shift)%n][j]=(B[(j+shift)%n][j]-alpha)%q
    return B


def monomial(n,q,rng):
    perm=list(range(n));rng.shuffle(perm)
    out=[[0]*n for _ in range(n)]
    for j,r in enumerate(perm):out[r][j]=rng.randrange(1,q)
    return out


def column_support(A):
    return max((sum(A[i][j]!=0 for i in range(len(A))) for j in range(len(A[0]))),default=0)


def build_sparse_inverse(n,q,L,seed=2026):
    """Product of L sparse Green inverse matrices interleaved with gauges."""
    rng=random.Random(seed);B=eye(n)
    for _ in range(L):
        shift=rng.randrange(1,n)
        alpha=next(a for a in (rng.randrange(1,q) for __ in range(100)) if pow(a,n//gcd(n,shift),q)!=1)
        K=green_inverse(n,q,alpha,shift)
        P=monomial(n,q,rng)
        B=mult(K,mult(P,B,q),q)
    return B


def full_spark_audit(n,q):
    """Exhaustive nonzero-minor check, only practical for small n."""
    F=fourier(n,q)
    count=0
    for k in range(1,n+1):
        for rr in combinations(range(n),k):
            for cc in combinations(range(n),k):
                sub=[[F[i][j] for j in cc] for i in rr]
                count+=1
                if rank(sub,q)!=k:
                    return {'full_spark':False,'minor_count':count,'first_zero_minor':{'rows':rr,'cols':cc}}
    return {'full_spark':True,'minor_count':count}


def matvec(A,x,q):
    return [sum(a*b for a,b in zip(row,x))%q for row in A]


def rank_correction_demo(n,q,L,seed=2026):
    B=build_sparse_inverse(n,q,L,seed)
    FI=fourier(n,q,inv=True)
    r=rank(subtract(FI,B,q),q)
    s=column_support(B)
    return {'n':n,'q':q,'L':L,'s_bound':min(n,2**L),'s_measured':s,'r_needed':r,
        'prime_inequality_LHS_bound':(2**L+1)*(r+1),
        'prime_inequality_LHS_measured':(s+1)*(r+1),
        'composite_inequality_LHS_bound':(2**L)*(r+1)**2}


def weyl_generators(n,q):
    """S e_j=e_(j+1), T e_j = w^j e_j. Thus TS=w ST."""
    w=primitive_root_of_order(n,q)
    S=[[int(i==(j+1)%n) for j in range(n)] for i in range(n)]
    T=[[pow(w,j,q) if i==j else 0 for j in range(n)] for i in range(n)]
    return S,T,w


def green_commutator_audit(n,q,alpha,beta):
    S,T,w=weyl_generators(n,q)
    A=subtract(eye(n),[[alpha*x%q for x in row] for row in S],q)
    B=subtract(eye(n),[[beta*x%q for x in row] for row in T],q)
    As=inverse(A,q);Bt=inverse(B,q)
    # [G_S,G_T] = A^-1 B^-1 [A,B] B^-1 A^-1 ; every factor invertible
    left=subtract(mult(As,Bt,q),mult(Bt,As,q),q)
    ab=subtract(mult(A,B,q),mult(B,A,q),q)
    rhs=mult(mult(mult(mult(As,Bt,q),ab,q),Bt,q),As,q)
    return {'n':n,'q':q,'commutator_rank':rank(left,q),'qcommutation_residual':subtract(mult(T,S,q),[[w*z%q for z in row] for row in mult(S,T,q)],q)==[[0]*n for _ in range(n)],'inverse_identity':left==rhs}


def chirp(n,q):
    """Odd n: chirp C_{i,j}=w^(-(i-j)^2/2)."""
    assert n%2==1
    w=primitive_root_of_order(n,q); inv2=pow(2,-1,n)
    return [[pow(w,(-inv2*((i-j)%n)**2)%n,q) for j in range(n)] for i in range(n)]


def chirp_inversion_audit(n,q):
    C=chirp(n,q)
    Ci=inverse(C,q)
    return {'n':n,'q':q,'inverse_all_entries_nonzero':all(a!=0 for row in Ci for a in row),
            'inverse_column_support':column_support(Ci),
            'forward_column_support':column_support(C)}


def direct_dft(x,q):return matvec(fourier(len(x),q),x,q)

if __name__=='__main__':
    for n,q in [(3,7),(5,11),(7,29)]:
        print('fullspark',n,q,full_spark_audit(n,q))
        a=next(z for z in range(2,q) if pow(z,n,q)!=1)
        print('weyl',green_commutator_audit(n,q,a,a))
        print('chirp',chirp_inversion_audit(n,q))
        for L in [1,2]:print('near_green',rank_correction_demo(n,q,L))

# ----- Auxiliary independently checkable execution kernels -----

def shift_green_apply(x, alpha, q):
    """Exact cyclic solve (I-alpha*S)y=x, O(N) scalar field work.
    Assumes shift S e_j=e_(j+1), and alpha^N!=1.
    """
    n=len(x)
    if pow(alpha,n,q)==1:raise ValueError('singular cyclic Green operator')
    z=0
    for j in range(1,n):
        z=(alpha*z+x[j])%q
    y=[0]*n
    y[0]=(x[0]+alpha*z)*pow((1-pow(alpha,n,q))%q,-1,q)%q
    for j in range(1,n):
        y[j]=(alpha*y[j-1]+x[j])%q
    return y


def batch_inverse(values,q):
    """One modular inversion + O(N) multiplications; all inputs nonzero."""
    n=len(values); prefixes=[1]*(n+1)
    for i,v in enumerate(values):
        if v%q==0:raise ValueError('zero value')
        prefixes[i+1]=prefixes[i]*v%q
    inv=pow(prefixes[-1],-1,q)
    out=[0]*n
    for i in range(n-1,-1,-1):
        out[i]=inv*prefixes[i]%q
        inv=inv*values[i]%q
    return out


def modulation_green_apply(x,beta,q):
    n=len(x);omega=primitive_root_of_order(n,q)
    values=[(1-beta*pow(omega,j,q))%q for j in range(n)]
    inv=batch_inverse(values,q)
    return [(a*b)%q for a,b in zip(x,inv)]


def stage_correction_network(n,q,L,r_each=1,seed=12):
    """Build invertible Green+rank-r stages with arbitrary monomial gauges.
    Inspect the difference of their inverse full products from the sparse
    inverse of their baseline products. Matrices are for *audit only*.
    """
    rng=random.Random(seed)
    Gproduct=eye(n); Hproduct=eye(n)
    stages=[]
    for _ in range(L):
        for attempt in range(100):
            shift=rng.randrange(1,n)
            alpha=rng.randrange(1,q)
            if pow(alpha,n//gcd(n,shift),q)==1:continue
            sparse=green_inverse(n,q,alpha,shift)
            G0=inverse(sparse,q)
            gauged=mult(monomial(n,q,rng),G0,q)
            corr=[[0]*n for _ in range(n)]
            for __ in range(r_each):
                u=[rng.randrange(q) for _ in range(n)]
                v=[rng.randrange(q) for _ in range(n)]
                for i in range(n):
                    for j in range(n):
                        corr[i][j]=(corr[i][j]+u[i]*v[j])%q
            H=add(gauged,corr,q)
            if rank(H,q)==n:
                stages.append({'baseline':gauged,'updated':H,'r':rank(corr,q)})
                Gproduct=mult(gauged,Gproduct,q)
                Hproduct=mult(H,Hproduct,q)
                break
        else:raise RuntimeError('could not find invertible rank-update stage')
    Binv=inverse(Gproduct,q)
    Hinv=inverse(Hproduct,q)
    delta_rank=rank(subtract(Hinv,Binv,q),q)
    rank_budget=sum(z['r'] for z in stages)
    s=column_support(Binv)
    return {'n':n,'L':L,'r_each':r_each,'rank_budget':rank_budget,
            'inverse_difference_rank':delta_rank,'s_bound':min(n,2**L),
            's_measured':s, 'rank_telescoping_valid':delta_rank<=rank_budget,
            'sparsity_valid':s<=2**L}


def lower_rank_budget(n,s,prime=False):
    """Smallest integer r satisfying the necessary uncertainty inequality."""
    if prime:
        return max(0,(n+1+s)//(s+1)-1)
    from math import isqrt
    k=isqrt((n+s-1)//s)
    while s*k*k<n:k+=1
    return max(0,k-1)

def stride_green_apply(x,alpha,stride,q):
    """Exact O(N) solve (I-alpha*S^stride)y=x for any stride 1..N-1.
    Charge one inversion per *cycle length* (shared denominator).
    """
    n=len(x); d=gcd(n,stride);m=n//d
    if pow(alpha,m,q)==1:raise ValueError('singular stride Green operator')
    inv_den=pow((1-pow(alpha,m,q))%q,-1,q)
    y=[0]*n
    for offset in range(d):
        indices=[];j=offset
        for _ in range(m):
            indices.append(j)
            j=(j+stride)%n
        trial=0
        for j in indices[1:]:trial=(alpha*trial+x[j])%q
        y[indices[0]]=(x[indices[0]]+alpha*trial)*inv_den%q
        for index,prev in zip(indices[1:],indices[:-1]):
            y[index]=(alpha*y[prev]+x[index])%q
    return y


def green_orbit_union_apply(x,alpha,K,q):
    """Explicit average of K conjugate one-pole Greens, O(KN).
    Equal to stride_green_apply(x, alpha**K, K, q) when K|N.
    """
    n=len(x)
    if n%K:raise ValueError('K must divide N for Weyl-twirl interpretation')
    w=primitive_root_of_order(n,q);z=pow(w,n//K,q)
    total=[0]*n
    for j in range(K):
        y=shift_green_apply(x,alpha*pow(z,j,q)%q,q)
        for i in range(n):total[i]=(total[i]+y[i])%q
    invK=pow(K,-1,q)
    return [(v*invK)%q for v in total]
