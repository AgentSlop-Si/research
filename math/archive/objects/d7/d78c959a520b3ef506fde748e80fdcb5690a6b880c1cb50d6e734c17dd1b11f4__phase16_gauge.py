"""Hero #0 / Phase 16: exact Fourier monomial centralizer and hidden gauge checks.

All theorems concern SPECIFIED circuit grammars.  No unrestricted FFT upper or
lower bound is claimed. Finite-field arithmetic is exact, and all costs in the
constructive detectors are accounted for.
"""
from __future__ import annotations
from collections import deque
from math import gcd, sin, pi, sqrt
from typing import Sequence
import numpy as np

PRIME = 65537
GEN = 3


def margulis_maps(s: int) -> list[list[int]]:
    if s < 2:
        raise ValueError('side >= 2')
    perms=[]
    for kind in range(4):
        p=[]
        for x in range(s):
            for y in range(s):
                if kind == 0: xx,yy = (x+2*y)%s,y
                elif kind == 1: xx,yy = (x+2*y+1)%s,y
                elif kind == 2: xx,yy = x,(y+2*x)%s
                else: xx,yy = x,(y+2*x+1)%s
                p.append(xx*s+yy)
        assert sorted(p)==list(range(s*s))
        perms.append(p)
    return perms


def half_y(s: int) -> list[int]:
    if s < 2 or s % 2:
        raise ValueError('even s >= 2 required')
    h=s//2
    return [x*s + (y+h)%s for x in range(s) for y in range(s)]


def prime_factors(n:int)->list[int]:
    out=[];p=2
    while p*p<=n:
        if n%p==0:
            out.append(p)
            while n%p==0:n//=p
        p+=1
    if n>1:out.append(n)
    return out


def find_root(n:int, p:int)->int:
    if n<2 or (p-1)%n:
        raise ValueError('requested order must divide p-1')
    for candidate in range(2,p):
        z=pow(candidate,(p-1)//n,p)
        if pow(z,n,p)==1 and all(pow(z,n//d,p)!=1 for d in prime_factors(n)):
            return z
    raise AssertionError('primitive root missing')


def fourier_mod(n:int,p:int=PRIME)->np.ndarray:
    z=find_root(n,p)
    power=np.array([pow(z,k,p) for k in range(n)],dtype=np.int64)
    ind=np.arange(n,dtype=np.int64)
    return power[np.outer(ind,ind)%n]


def rank_mod(A:np.ndarray,p:int=PRIME)->int:
    M=np.array(A,copy=True,dtype=np.int64)%p
    m,n=M.shape;row=0
    for col in range(n):
        if row==m:break
        inds=np.flatnonzero(M[row:,col])
        if not len(inds):continue
        pivot=row+int(inds[0]);M[[row,pivot]]=M[[pivot,row]]
        M[row,col:]=M[row,col:]*pow(int(M[row,col]),-1,p)%p
        if row+1<m:
            factors=M[row+1:,col].copy()
            M[row+1:,col:]=(M[row+1:,col:]-factors[:,None]*M[None,row,col:])%p
        row+=1
    return row


def monomial_centralizer_cases(n:int)->list[tuple[int,int]]:
    if n<2:raise ValueError('n')
    return [(a,b) for a in range(n) if a*a%n==1
            for b in range(n) if 2*b%n==0 and b*b%n==0]


def monomial_commutator_mod(F:np.ndarray,tau:Sequence[int],a:Sequence[int],p:int=PRIME)->np.ndarray:
    n=len(tau)
    if F.shape!=(n,n) or len(a)!=n or sorted(tau)!=list(range(n)):
        raise ValueError('invalid shape or permutation')
    inv=np.argsort(np.array(tau,dtype=np.int64))
    w=np.asarray(a,dtype=np.int64)%p
    return (F[:,tau]*w[None,:] - w[inv,None]*F[inv,:])%p


def gauge_alpha(tau:Sequence[int],d:Sequence[int],p:int=PRIME)->list[int]:
    return [int(d[tau[j]])*pow(int(d[j]),-1,p)%p for j in range(len(tau))]


def make_gauge_weights(perms:list[list[int]],constants:Sequence[int],d:Sequence[int],p:int=PRIME)->list[list[int]]:
    return [[int(c)*int(d[i])*pow(int(d[pi[i]]),-1,p)%p for i in range(len(pi))]
            for pi,c in zip(perms,constants)]


def recover_common_gauge(perms:list[list[int]],weights:list[list[int]],constants:Sequence[int],p:int=PRIME)->list[int]|None:
    """O(total edges) field operations, given each nonzero reference scalar c_t.

    Solve d_pi(i)=(c_t/w_t(i))*d_i.  All inversions, components and checks
    are charged. Return any gauge (one normalization per component) or None.
    """
    if not perms:return []
    n=len(perms[0])
    if not(len(perms)==len(weights)==len(constants)):
        raise ValueError('mismatched lengths')
    edges=[[] for _ in range(n)]
    for perm,w,c in zip(perms,weights,constants):
        if len(perm)!=n or len(w)!=n:raise ValueError('edge length')
        if c%p==0 or any(int(x)%p==0 for x in w):return None
        for i,j in enumerate(perm):
            r=int(c)*pow(int(w[i]),-1,p)%p
            edges[i].append((j,r))
            edges[j].append((i,pow(r,-1,p)))
    d=[None]*n
    for root in range(n):
        if d[root] is not None:continue
        d[root]=1;queue=deque([root])
        while queue:
            i=queue.popleft()
            for j,r in edges[i]:
                proposed=d[i]*r%p
                if d[j] is None:
                    d[j]=proposed
                    queue.append(j)
                elif d[j]!=proposed:return None
    assert all(x is not None for x in d)
    return d


def cycles(perm:Sequence[int])->list[list[int]]:
    n=len(perm);seen=[False]*n;ans=[]
    for i in range(n):
        if seen[i]:continue
        cyc=[];j=i
        while not seen[j]:
            seen[j]=True;cyc.append(j);j=perm[j]
        if j!=i:raise ValueError('not a permutation')
        ans.append(cyc)
    return ans


def green_apply(perm:Sequence[int],w:Sequence[int],v:Sequence[int],p:int=PRIME)->list[int]:
    n=len(perm)
    if len(w)!=n or len(v)!=n:raise ValueError('length mismatch')
    ans=[0]*n
    for cyc in cycles(perm):
        product=1;rhs=0
        for i in cyc:
            rhs=(rhs+product*int(v[i]))%p
            product=product*int(w[i])%p
        den=(1-product)%p
        if not den:raise ZeroDivisionError('singular cyclic Green matrix')
        ans[cyc[0]]=rhs*pow(den,-1,p)%p
        for k in range(len(cyc)-1,0,-1):
            i=cyc[k]
            ans[i]=(int(v[i])+int(w[i])*ans[perm[i]])%p
    return ans


def apply_network_stages(perms:list[list[int]],stage_weights:list[list[list[int]]],v:Sequence[int],p:int=PRIME)->list[int]:
    """Asymmetric two-stage mixed network; the 8 resolvent occurrences
    have independent weight vectors (essential for accurate edit counts).
    """
    n=len(v);x=list(v);quarter=pow(4,-1,p)
    for weights,order in zip(stage_weights,(range(4),range(3,-1,-1))):
        acc=[0]*n
        for j in order:
            a=green_apply(perms[j],weights[j],x,p)
            for i in range(n):acc[i]=(acc[i]+a[i])%p
        x=[value*quarter%p for value in acc]
    return x


def apply_network(perms:list[list[int]],weights:list[list[int]],v:Sequence[int],p:int=PRIME)->list[int]:
    """Two noncommuting mixed-axis stages: four Green resolvents each.

    All 8 applies cost O(N) for a fixed generator count.
    """
    return apply_network_stages(perms,[weights,weights],v,p)



def commutator_rank_for_gauge(s:int,d:Sequence[int],p:int=PRIME)->int:
    tau=half_y(s); F=fourier_mod(s*s,p)
    return rank_mod(monomial_commutator_mod(F,tau,gauge_alpha(tau,d,p),p),p)


def phase_gauge_commutator_lower_bound(s:int)->float:
    """Universal spectral distance for UNITARY diagonal-gauge networks.

    If T=D T0 D* with |D_ii|=1 and [T0,Pi_y]=0, then
    ||U_(s^2)-T||_2 >= this value, for even s>=4.
    """
    if s<4 or s%2:raise ValueError('even s>=4')
    sq=max(0.0,2-2*sqrt(2)/(s*sin(pi/(2*s))))
    return sqrt(sq)/2


def phase_gauge_e0_commutator(s:int,d:Sequence[complex])->float:
    """Direct ||[U,Q] e_0||, with Q=D Pi_y D* and |d_i|=1."""
    n=s*s;tau=half_y(s)
    d=np.asarray(d,dtype=np.complex128)
    if len(d)!=n or np.max(np.abs(np.abs(d)-1))>1.e-11:
        raise ValueError('unitary gauge only')
    a=d[np.array(tau)]/d
    z=np.exp(-2j*pi/n)
    idx=np.arange(n,dtype=np.int64)
    return float(np.linalg.norm((a[0]*z**(idx*tau[0])-a[np.array(tau)])/sqrt(n)))


def sparse_fourier_row_zeros(n:int,i:int,j:int,weight:int,p:int)->tuple[int,int]:
    """Count zero entries in row i of (I-P)F when Pi(i)=j.

    If j!=i, count is zero or gcd(n,j-i), never more.
    """
    z=find_root(n,p)
    zeros=0
    for col in range(n):
        if (pow(z,(i*col)%n,p)-weight*pow(z,(j*col)%n,p))%p==0:
            zeros+=1
    bound=n if i==j else gcd(n,(j-i)%n)
    return zeros,bound


def one_green_rook_no_go(s:int)->dict:
    """Rook row/column support is 2s-1; exact F cannot equal G X or X G
    with invertible single weighted-permutation G and arbitrary rook X, s>=3.
    """
    if s<3:raise ValueError('s>=3')
    n=s*s;d=2*s-1;pmin=prime_factors(n)[0]
    minimum=n-n//pmin
    assert d<minimum
    return {'s':s,'N':n,'rook_row_degree':d,'minimum_row_support':minimum,
            'minimum_column_support':minimum,'support_gap':minimum-d}


def best_row_sparse(X:np.ndarray,d:int)->np.ndarray:
    ans=np.zeros_like(X)
    for i in range(len(X)):
        indices=np.argsort(np.abs(X[i]))[-d:]
        ans[i,indices]=X[i,indices]
    return ans


def one_green_approx_lower_bound(n:int,d:int,rho:float)->float:
    """Relative Frobenius lower bound, fixed-point-free P and ||P||<=rho.

    Applies when X has <=d nonzeros per row and T=(I-P)^(-1)X.
    """
    if n<=0 or not(0<=d<n/2) or rho<0:raise ValueError('range')
    alpha=d/n
    return sqrt((1-2*alpha)/(1-alpha))/(1+rho)


def numerical_one_green_check(s:int,rho:float=.30)->dict:
    n=s*s;d=2*s-1
    if d>=n/2:raise ValueError('s>=4 needed')
    z=np.exp(-2j*pi/n);indices=np.arange(n)
    U=z**np.outer(indices,indices)/sqrt(n)
    P=np.zeros((n,n),dtype=np.complex128)
    P[indices,(indices+1)%n]=rho
    I=np.eye(n,dtype=np.complex128)
    A=I-P
    X=best_row_sparse(A@U,d)
    T=np.linalg.solve(A,X)
    err=float(np.linalg.norm(T-U,'fro')/sqrt(n))
    bound=one_green_approx_lower_bound(n,d,rho)
    assert err+1.e-10>=bound
    return {'s':s,'N':n,'degree':d,'rho':rho,'observed_rel_fro_error':err,'proved_lower_bound':bound}


def spanning_gauge_residuals(perms:list[list[int]],weights:list[list[int]],constants:Sequence[int],p:int=PRIME)->dict:
    """A linear-work common-diagonal gauge normalizer and holonomy residual list.

    Builds a spanning forest of the MULTIgraph of generator edges and solves its
    potential equations exactly.  Non-tree edges that disagree identify genuine
    gauge curvature relative to that forest, even for vertex-dependent weights.
    This is a gauge-coordinate change, not a Fourier factorization.
    """
    if not perms:return {'potentials':[], 'defects':[], 'components':0}
    n=len(perms[0])
    if not(len(perms)==len(weights)==len(constants)):
        raise ValueError('mismatched generator arrays')
    edges=[[] for _ in range(n)]
    for t,(perm,w,c) in enumerate(zip(perms,weights,constants)):
        if len(perm)!=n or len(w)!=n or not c%p:raise ValueError('invalid edge data')
        for i,j in enumerate(perm):
            if not w[i]%p:raise ValueError('zero edge weights')
            r=int(c)*pow(int(w[i]),-1,p)%p
            edges[i].append((j,r));edges[j].append((i,pow(r,-1,p)))
    d=[None]*n;components=0
    for start in range(n):
        if d[start] is not None:continue
        d[start]=1;components+=1;queue=deque([start])
        while queue:
            i=queue.popleft()
            for j,r in edges[i]:
                if d[j] is None:
                    d[j]=d[i]*r%p
                    queue.append(j)
    expected=make_gauge_weights(perms,constants,d,p)
    defects=[{'generator':t,'vertex':i,'actual':int(weights[t][i]),
              'gauged_expected':int(expected[t][i])}
             for t in range(len(perms)) for i in range(n)
             if int(weights[t][i])%p != expected[t][i]]
    return {'potentials':d,'defects':defects,'components':components,
            'generator_edge_occurrences':n*len(perms)}
