"""Hero #17 Phase 16: exact Fourier/Green interface audits.

Every computation uses prime-field arithmetic, with n|(p-1). No FFT oracle
is invoked. The universal theorems themselves are algebraic and are not inferred
from the finite tests. No sub-nlogn algorithm is claimed.
"""
from __future__ import annotations


def prime_factors(n: int) -> list[int]:
    out = []
    k = 2
    while k*k <= n:
        if n % k == 0:
            out.append(k)
            while n % k == 0:
                n //= k
        k += 1
    if n > 1: out.append(n)
    return out


def nth_root(n: int, p: int) -> int:
    """Return primitive n-th root in F_p; raise if unavailable."""
    if n <= 1 or (p-1) % n:
        raise ValueError("Require n>1 and n | p-1")
    pf = prime_factors(p-1)
    g = next(g for g in range(2,p) if all(pow(g,(p-1)//q,p)!=1 for q in pf))
    w = pow(g,(p-1)//n,p)
    assert pow(w,n,p)==1 and all(pow(w,n//q,p)!=1 for q in prime_factors(n))
    return w


def identity(n: int) -> list[list[int]]:
    return [[int(i==j) for j in range(n)] for i in range(n)]


def fourier(n: int, p: int, w: int | None = None) -> list[list[int]]:
    if w is None: w = nth_root(n,p)
    return [[pow(w,(-k*j)%n,p) for j in range(n)] for k in range(n)]


def mm(A: list[list[int]], B: list[list[int]], p: int) -> list[list[int]]:
    if not A or not B: return []
    n, k, m = len(A), len(B), len(B[0])
    assert len(A[0]) == k
    C = [[0]*m for _ in range(n)]
    for i in range(n):
        for t in range(k):
            v = A[i][t]
            if v:
                for j in range(m): C[i][j] = (C[i][j]+v*B[t][j])%p
    return C


def mv(A: list[list[int]], v: list[int], p: int) -> list[int]:
    return [sum(a*x for a,x in zip(row,v))%p for row in A]


def rank_mod(A: list[list[int]], p: int) -> int:
    A = [list(map(lambda a:a%p,row)) for row in A]
    if not A:return 0
    r=0; nr=len(A);nc=len(A[0])
    for c in range(nc):
        pivot = next((i for i in range(r,nr) if A[i][c]),None)
        if pivot is None:continue
        A[r],A[pivot] = A[pivot],A[r]
        z=pow(A[r][c],-1,p)
        A[r]=[(a*z)%p for a in A[r]]
        for i in range(r+1,nr):
            if A[i][c]:
                z=A[i][c]
                A[i]=[(a-z*b)%p for a,b in zip(A[i],A[r])]
        r+=1
        if r==nr:break
    return r


def solve(A: list[list[int]], b: list[int], p: int) -> list[int]:
    n = len(A)
    if n==0: return []
    assert all(len(row)==n for row in A) and len(b)==n
    C = [[A[i][j]%p for j in range(n)] + [b[i]%p] for i in range(n)]
    for k in range(n):
        pivot=next((i for i in range(k,n) if C[i][k]),None)
        if pivot is None:raise ValueError("matrix singular")
        C[k],C[pivot] = C[pivot],C[k]
        inv=pow(C[k][k],-1,p)
        C[k]=[(v*inv)%p for v in C[k]]
        for i in range(n):
            if i!=k and C[i][k]:
                z=C[i][k]
                C[i]=[(a-z*b)%p for a,b in zip(C[i],C[k])]
    return [C[i][-1] for i in range(n)]


def nullspace(A: list[list[int]], p: int) -> list[list[int]]:
    """Exact modular RREF kernel basis; columns in increasing free-index order."""
    a=[list(map(lambda x:x%p,row)) for row in A]
    if not a:return []
    rows=len(a);cols=len(a[0]);piv=[];r=0
    for c in range(cols):
        i=next((i for i in range(r,rows) if a[i][c]),None)
        if i is None:continue
        a[i],a[r]=a[r],a[i]
        inv=pow(a[r][c],-1,p);a[r]=[(x*inv)%p for x in a[r]]
        for j in range(rows):
            if j!=r and a[j][c]:
                z=a[j][c]
                a[j]=[(x-z*y)%p for x,y in zip(a[j],a[r])]
        piv.append(c);r+=1
        if r==rows:break
    free=[c for c in range(cols) if c not in piv]
    basis=[]
    for c in free:
        v=[0]*cols;v[c]=1
        for i,j in enumerate(piv):v[j]=(-a[i][c])%p
        basis.append(v)
    return basis


def cyclic_distance(t:int, j:int, n:int)->int:
    delta=(t-j)%n
    return min(delta,n-delta)


def column_band_valid(A: list[list[int]], radius:int)->bool:
    n=len(A)
    return all(A[i][j]==0 or cyclic_distance(i,j,n)<=radius
               for i in range(n) for j in range(n))


def boundary_pair(n:int, a:int, p:int):
    """Construct the unique column-wise interface at n=2(a+b)+1.

    The returned Q may be singular in some finite fields. Rank is deliberately
    checked by caller; never divide by Q without checking it.
    """
    if n%2!=1 or not 0<=a<=(n-1)//2:raise ValueError("odd n and valid a needed")
    b=(n-1)//2-a;w=nth_root(n,p)
    F=fourier(n,p,w)
    Q=[[0]*n for _ in range(n)]
    for j in range(n):
        allowed={(j+t)%n for t in range(-a,a+1)}
        forbidden=[k for k in range(n) if k not in allowed]
        coeffs=[1]
        for k in forbidden:
            root=pow(w,(-k)%n,p)
            nxt=[0]*(len(coeffs)+1)
            for r,c in enumerate(coeffs):
                nxt[r]=(nxt[r]-c*root)%p
                nxt[r+1]=(nxt[r+1]+c)%p
            coeffs=nxt
        assert len(coeffs)==2*b+1
        for r,c in enumerate(coeffs):Q[(j-b+r)%n][j]=c
    P=mm(F,Q,p)
    return P,Q


def intertwining_check(M:list[list[int]], p:int, w:int)->bool:
    """MS=T^-1 M, M e_0=all ones iff M is negative-exponent DFT."""
    n=len(M)
    if any(M[i][0]%p!=1 for i in range(n)):return False
    for i in range(n):
        u=pow(w,(-i)%n,p)
        for j in range(n):
            if M[i][(j+1)%n]%p != (u*M[i][j])%p:return False
    return True


def harper(n:int, p:int,w:int|None=None):
    if w is None:w=nth_root(n,p)
    H=[[0]*n for _ in range(n)]
    for i in range(n):
        H[i][(i-1)%n]=(H[i][(i-1)%n]+1)%p
        H[i][(i+1)%n]=(H[i][(i+1)%n]+1)%p
        H[i][i]=(H[i][i]+pow(w,i,p)+pow(w,(-i)%n,p))%p
    return H


def harper_powers(n:int,p:int,w:int|None=None):
    H=harper(n,p,w);cur=identity(n);out=[]
    for _ in range(n):
        out.append(cur);cur=mm(cur,H,p)
    return out


def harper_algebra_audit(n:int,p:int):
    w=nth_root(n,p);powH=harper_powers(n,p,w);F=fourier(n,p,w)
    columns=[[A[i][j] for i in range(n) for j in range(n)] for A in powH]
    K=[list(row) for row in zip(*columns)]
    f=[F[i][j] for i in range(n) for j in range(n)]
    return rank_mod(K,p),rank_mod([row+[f[i]] for i,row in enumerate(K)],p)


def harper_rational_witness(n:int,p:int,max_degree:int|None=None):
    """Find exact P(H)=F Q(H), with invertible Q(H), if short witness exists.

    Searches kernel *basis vectors*, not arbitrary kernel combinations.
    Failing to find one is not a proof of nonexistence. Matrix F in alg(H)
    is tested separately and definitively via harper_algebra_audit.
    """
    w=nth_root(n,p);F=fourier(n,p,w)
    powers=harper_powers(n,p,w);fp=[mm(F,A,p) for A in powers]
    for d in range(n if max_degree is None else min(max_degree+1,n)):
        mats=powers[:d+1]+fp[:d+1]
        A=[[U[i][j] if k<=d else (-U[i][j])%p for k,U in enumerate(mats)]
           for i in range(n) for j in range(n)]
        for coefficients in nullspace(A,p):
            a,b=coefficients[:d+1],coefficients[d+1:]
            P=[[sum(a[k]*powers[k][i][j] for k in range(d+1))%p for j in range(n)] for i in range(n)]
            Q=[[sum(b[k]*powers[k][i][j] for k in range(d+1))%p for j in range(n)] for i in range(n)]
            if rank_mod(Q,p)==n and mm(F,Q,p)==P:return (d,a,b)
    return None


def evaluated_poly(coeffs:list[int],H:list[list[int]],p:int):
    n=len(H);identity_n=identity(n);out=[[0]*n for _ in range(n)]
    for c in reversed(coeffs):
        out=mm(out,H,p)
        for i in range(n):out[i][i]=(out[i][i]+c)%p
    return out


def boundary_circulant_gauge(n:int,a:int,p:int,Q:list[list[int]]|None=None):
    """For odd n, Q = D_left C_h D_right, a chirp-gauged convolution.

    This is an algebraic representation, NOT an O(n) evaluator for general data.
    Evaluating the C_h inverse is potentially the FFT-hard part.
    """
    if n%2 != 1:raise ValueError("This simple chirp gauge uses odd n")
    b=(n-1)//2-a;w=nth_root(n,p)
    if Q is None:_,Q=boundary_pair(n,a,p)
    DL=[pow(w,t*(t-1)//2%n,p) for t in range(n)]
    DR=[pow(w,(-j*(j-1)//2-b*j)%n,p) for j in range(n)]
    h=[Q[s][0]*pow(DL[s],-1,p)%p for s in range(n)]
    pred=[[DL[t]*h[(t-j)%n]*DR[j]%p for j in range(n)] for t in range(n)]
    return pred,h,DL,DR


def shift(n:int,s:int):
    M=[[0]*n for _ in range(n)]
    for j in range(n):M[(j+s)%n][j]=1
    return M


def modulation(n:int,b:int,p:int,w:int|None=None):
    if w is None:w=nth_root(n,p)
    D=[[0]*n for _ in range(n)]
    for j in range(n):D[j][j]=pow(w,b*j%n,p)
    return D


def chirp(n:int,a:int,p:int,w:int|None=None):
    if w is None:w=nth_root(n,p)
    D=[[0]*n for _ in range(n)]
    for j in range(n):D[j][j]=pow(w,a*j*j%n,p)
    return D
