"""Hero #17 Phase 17: certified sparse-graph Fourier feedback gates.

All exact experiments are over prime fields with a primitive n-th root.
Theorems are field algebra and do not claim a new all-input FFT bound.

Two certificates:
 (1) Arbitrary sparse-column P/Q support + low-rank corrections.
 (2) Intertwining-defect rank for arbitrary additive operator corrections.
Positive control: exact O(n) cyclic magnetic-Green solve with rank-one feedback.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import floor


def factors(n: int) -> list[int]:
    out = []
    d = 2
    while d*d <= n:
        if n % d == 0:
            out.append(d)
            while n%d == 0: n //= d
        d += 1
    if n > 1: out.append(n)
    return out


def nth_root(n: int, p: int) -> int:
    """Primitive n-th root in F_p (p is required to be prime)."""
    if n < 2 or (p-1)%n: raise ValueError('require n >= 2, n divides p-1')
    ps=factors(p-1)
    gen=next(g for g in range(2,p) if all(pow(g,(p-1)//q,p)!=1 for q in ps))
    w=pow(gen,(p-1)//n,p)
    assert pow(w,n,p)==1 and all(pow(w,n//q,p)!=1 for q in factors(n))
    return w


def fourier(n: int, p: int, w: int|None=None) -> list[list[int]]:
    if w is None: w=nth_root(n,p)
    return [[pow(w,(-i*j)%n,p) for j in range(n)] for i in range(n)]


def rank(A: list[list[int]], p: int) -> int:
    if not A: return 0
    C=[[z%p for z in row] for row in A]
    rows=len(C); cols=len(C[0]); r=0
    assert all(len(row)==cols for row in C)
    for j in range(cols):
        q=next((i for i in range(r,rows) if C[i][j]),None)
        if q is None: continue
        C[r],C[q]=C[q],C[r]
        inv=pow(C[r][j],-1,p)
        C[r]=[(x*inv)%p for x in C[r]]
        for i in range(r+1, rows):
            if C[i][j]:
                v=C[i][j]
                C[i]=[(x-v*y)%p for x,y in zip(C[i],C[r])]
        r+=1
        if r==rows:break
    return r


def mm(A: list[list[int]], B: list[list[int]],p:int) -> list[list[int]]:
    if not A or not B:return []
    k=len(A[0]); assert k==len(B)
    out=[[0]*len(B[0]) for _ in A]
    for i,row in enumerate(A):
        for j,val in enumerate(row):
            if val:
                for l,v in enumerate(B[j]):out[i][l]=(out[i][l]+val*v)%p
    return out


def mat_add(A,B,p,sign=1):
    return [[(u+sign*v)%p for u,v in zip(ra,rb)] for ra,rb in zip(A,B)]


def eye(n:int):
    return [[int(i==j) for j in range(n)] for i in range(n)]


def cyclic_shift(n:int, stride:int=1):
    return [[int(i==(j+stride)%n) for j in range(n)] for i in range(n)]


def sparse_degrees(P):
    n=len(P)
    return max(sum(P[i][j]!=0 for i in range(n)) for j in range(n))


def graph_certificate(P, Q, t:int|None=None, s:int|None=None,
                      row_order:list[int]|None=None):
    """Construct a graph/Hall/Vandermonde feedback-rank witness.

    Returns an interval I and columns B with P[I,B]=0 and
    |union supp Q[:,B]| <= |I|, for b = floor(N/(1+s*t)).
    The coefficient values are irrelevant; only permitted nonzero supports matter.
    row_order can be an arbitrary permutation mapping Fourier-frequency order
    to physical row labels, supporting arbitrary endpoint permutations.
    """
    n=len(P)
    assert len(Q)==n and all(len(z)==n for z in P+Q)
    if t is None:t=sparse_degrees(P)
    if s is None:s=sparse_degrees(Q)
    if s<1 or t<1: raise ValueError('s,t must be positive upper bounds')
    assert sparse_degrees(P)<=t and sparse_degrees(Q)<=s
    if row_order is None:row_order=list(range(n))
    if sorted(row_order)!=list(range(n)):
        raise ValueError('row_order must permute all n physical Fourier rows')
    b=n//(1+s*t)
    if b==0: return {'bound':0,'rows':[],'columns':[],'neighbors':[],'s':s,'t':t}
    L=s*b
    assert L<=n
    for start in range(n):
        rows=[row_order[(start+z)%n] for z in range(L)]
        good=[j for j in range(n) if all(P[i][j]==0 for i in rows)]
        if len(good)<b:continue
        cols=good[:b]
        neighbors=sorted({i for j in cols for i in range(n) if Q[i][j]!=0})
        assert len(neighbors)<=s*b==L
        return {'bound':b,'rows':rows,'columns':cols,'neighbors':neighbors,
                's':s,'t':t,'rows_length':L,'qualifying_columns':len(good)}
    raise AssertionError('graph double-counting certificate failed')


def local_band_certificate(n:int, a:int, b:int):
    """Stronger rank-feedback bound when P/Q have cyclic band radii a/b."""
    if a<0 or b<0:raise ValueError('nonnegative radii required')
    L=max(0,n//2-a-b)
    if L==0:return {'bound':0,'rows':[],'columns':[],'neighbors':[]}
    m=(n-2*a+2*b+1)//2  # ceil((n-2a+2b)/2)
    rows=list(range(m))
    cols=list(range(m+a,n-a))
    assert len(cols)==L
    neigh=sorted({(j+offset)%n for j in cols for offset in range(-b,b+1)})
    assert len(neigh)<=m
    return {'bound':L,'rows':rows,'columns':cols,'neighbors':neigh}


def check_submatrix_vandermonde(rows:list[int],cols:list[int],n:int,p:int,w:int):
    """Exact test for certificate; rows must be a cyclic interval."""
    if not cols:return True
    assert len(rows)>=len(cols)
    assert all(rows[i]==(rows[0]+i)%n for i in range(len(rows)))
    A=[[pow(w,(-i*j)%n,p) for j in cols] for i in rows]
    return rank(A,p)==len(cols)


def intertwining_defect(M:list[list[int]],p:int,w:int):
    """Delta(M) = M S - T^-1 M; for a Fourier matrix it is zero."""
    n=len(M)
    return [[(M[i][(j+1)%n]-pow(w,-i%n,p)*M[i][j])%p for j in range(n)] for i in range(n)]


def mixed_green_denominator(n:int,p:int,w:int,alpha:int,beta:int):
    """Q = I - alpha*S - beta*T; S e_j = e_(j+1)."""
    Q=[[0]*n for _ in range(n)]
    for j in range(n):
        Q[j][j]=(Q[j][j]+1-beta*pow(w,j,p))%p
        Q[(j+1)%n][j]=(Q[(j+1)%n][j]-alpha)%p
    return Q


def covariance_defect_rank_via_denominator(Q,p,w):
    """rank(Delta(Q^-1))=rank(S Q-Q T^-1) for invertible Q.
    This avoids explicitly inverting Green Q during the rank certificate.
    """
    n=len(Q)
    assert rank(Q,p)==n
    # (S Q)[i,j] = Q[i-1,j]; (Q T^-1)[i,j] = Q[i,j]*w^-j
    B=[[(Q[(i-1)%n][j]-Q[i][j]*pow(w,-j%n,p))%p for j in range(n)] for i in range(n)]
    return rank(B,p)


@dataclass
class FieldCount:
    adds:int=0
    mults:int=0
    inversions:int=0
    def add(self,x,y,p):
        self.adds+=1
        return (x+y)%p
    def sub(self,x,y,p):
        self.adds+=1
        return (x-y)%p
    def mul(self,x,y,p):
        self.mults+=1
        return (x*y)%p
    def inv(self,x,p):
        if x%p==0:raise ZeroDivisionError('field inverse does not exist')
        self.inversions+=1
        return pow(x,-1,p)
    def work(self):return self.adds+self.mults+self.inversions
    def report(self):return {'add_sub':self.adds,'multiply':self.mults,'invert':self.inversions,'total_field_ops':self.work()}


class MagneticGreenPlan:
    """Charged O(N) executor for (I-alpha*S-beta*T)^-1.

    Preconditions: beta^N != 1 and alpha^N+beta^N != 1 mod p.
    Other invertible cases may need alternative pivoting and are not claimed.
    """
    def __init__(self,n,p,w,alpha,beta,c:FieldCount|None=None):
        self.n,self.p,self.w=n,p,w
        self.alpha,self.beta=alpha%p,beta%p
        self.counter=c or FieldCount()
        c=self.counter
        phases=[1]*n
        for j in range(1,n):phases[j]=c.mul(phases[j-1],w,p)
        d=[c.sub(1,c.mul(self.beta,z,p),p) for z in phases]
        if 0 in d:raise ValueError('zero pivot; this executor requires all nonzero diagonal pivots')
        pref=[1]
        for z in d:pref.append(c.mul(pref[-1],z,p))
        accum=c.inv(pref[-1],p)
        invd=[0]*n
        for j in range(n-1,-1,-1):
            invd[j]=c.mul(pref[j],accum,p)
            accum=c.mul(accum,d[j],p)
        pr=[c.mul(self.alpha,z,p) for z in invd]
        A=[];v=1
        for z in pr:
            v=c.mul(v,z,p)
            A.append(v)
        end_inv=c.inv(c.sub(1,A[-1],p),p)
        self.inv_d,self.pr,self.A,self.end_inv=invd,pr,A,end_inv
    def solve(self,x:list[int], c:FieldCount|None=None):
        assert len(x)==self.n
        c=c or self.counter
        p=self.p
        B=[];v=0
        for j in range(self.n):
            v=c.add(c.mul(self.pr[j],v,p),c.mul(x[j],self.inv_d[j],p),p)
            B.append(v)
        z=c.mul(B[-1],self.end_inv,p)
        return [c.add(c.mul(self.A[j],z,p),B[j],p) for j in range(self.n)]


class RankOneFeedbackPlan:
    """Sherman-Morrison rank-one global feedback around MagneticGreenPlan."""
    def __init__(self, green:MagneticGreenPlan, u:list[int],v:list[int],c:FieldCount|None=None):
        self.green=green;self.v=v
        c=c or green.counter
        self.counter=c;self.p=green.p
        if len(u)!=green.n or len(v)!=green.n:raise ValueError('wrong feedback width')
        self.z=green.solve(u,c)
        dot=0
        for a,b in zip(v,self.z):dot=c.add(dot,c.mul(a,b,self.p),self.p)
        self.inv_den=c.inv(c.add(1,dot,self.p),self.p)
    def solve(self,x:list[int],c:FieldCount|None=None):
        c=c or self.counter
        y=self.green.solve(x,c)
        dot=0
        for a,b in zip(self.v,y):dot=c.add(dot,c.mul(a,b,self.p),self.p)
        lam=c.mul(dot,self.inv_den,self.p)
        return [c.sub(yj,c.mul(lam,zj,self.p),self.p) for yj,zj in zip(y,self.z)]


def mixed_feedback_residual(y,x,n,p,w,alpha,beta,u,v):
    """Verify (Q+u v^T)y=x in O(N), independent of plan recurrences."""
    dot=sum(a*b for a,b in zip(v,y))%p
    return [( (1-beta*pow(w,j,p))*y[j]-alpha*y[(j-1)%n]+u[j]*dot-x[j])%p for j in range(n)]


def covariance_blackbox_probe(apply,n:int,p:int,w:int,trials:int=3,seed:int=0):
    """Monte-Carlo screen for MS=T^-1M and M e0=1.

    This is a rejection test, NOT a deterministic proof of Fourier equality.
    If the covariance defect is nonzero, passing t uniform independent trials
    has probability at most p^(-t); the e0 check is deterministic.
    """
    from random import Random
    rng=Random(seed)
    e0=[1]+[0]*(n-1)
    if apply(e0)!=[1]*n:
        return False
    w_inv=pow(w,-1,p)
    inv_phases=[1]*n
    for j in range(1,n):inv_phases[j]=(inv_phases[j-1]*w_inv)%p
    for _ in range(trials):
        x=[rng.randrange(p) for _ in range(n)]
        sx=[x[(j-1)%n] for j in range(n)] # (Sx)_j=x_(j-1)
        left=apply(sx)
        right=apply(x)
        if any((u-inv_phases[i]*right[i])%p for i,u in enumerate(left)):
            return False
    return True
