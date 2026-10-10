"""Hero #17 Phase 8: exact multistage Fourier cross-cut and polynomial-CRT audits.

All claimed general-FFT bounds are carefully *restricted* to their declared grammar.
The executable fast baseline is radix-2 decimation via binomial remainder union.
No universal sub-NlogN FFT is claimed.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, asdict
from itertools import combinations
from math import isqrt, log2, pi, sqrt
from cmath import exp
import random


def is_prime(n: int) -> bool:
    if n < 2: return False
    for k in range(2, isqrt(n) + 1):
        if n % k == 0: return False
    return True


def factors(n: int) -> set[int]:
    out=set();k=2
    while k*k<=n:
        if n%k==0:
            out.add(k)
            while n%k==0:n//=k
        k+=1
    if n>1:out.add(n)
    return out


def fixture(n: int) -> tuple[int,int]:
    """Find prime p and primitive Nth root; explicitly OUTSIDE online executor."""
    for c in range(1,10000):
        p=c*n+1
        if not is_prime(p): continue
        for g in range(2,p):
            w=pow(g,(p-1)//n,p)
            if all(pow(w,n//q,p)!=1 for q in factors(n)):
                return p,w
    raise RuntimeError('no fixture field')


@dataclass
class Ledger:
    adds:int=0
    muls:int=0
    root_prep_muls:int=0
    inputs:int=0
    writes:int=0
    butterflies:int=0
    plan_adds:int=0
    plan_muls:int=0
    def record(self):return asdict(self)
    def add(self,a,b,p,plan=False):
        if plan:self.plan_adds+=1
        else:self.adds+=1
        return (a+b)%p
    def sub(self,a,b,p,plan=False):
        if plan:self.plan_adds+=1
        else:self.adds+=1
        return (a-b)%p
    def mul(self,a,b,p,plan=False):
        if plan:self.plan_muls+=1
        else:self.muls+=1
        return (a*b)%p


def roots_table(n:int,p:int,w:int,log:Ledger|None=None)->list[int]:
    out=[1]*n
    for i in range(1,n):
        out[i]=out[i-1]*w%p
        if log:log.root_prep_muls+=1
    return out


def dft_ref(x:list[int],p:int,w:int)->list[int]:
    n=len(x);roots=roots_table(n,p,w)
    return [sum(x[j]*roots[(-k*j)%n] for j in range(n))%p for k in range(n)]


def dft_matrix(n:int,p:int,w:int)->list[list[int]]:
    roots=roots_table(n,p,w)
    return [[roots[(-k*j)%n] for j in range(n)] for k in range(n)]


def matmul(A:list[list[int]],B:list[list[int]],p:int)->list[list[int]]:
    if not A or not B:return []
    assert len(A[0])==len(B)
    return [[sum(A[i][k]*B[k][j] for k in range(len(B)))%p
             for j in range(len(B[0]))] for i in range(len(A))]


def matrank(A:list[list[int]],p:int)->int:
    if not A:return 0
    W=[row.copy() for row in A];m=len(W);n=len(W[0]);r=0
    for j in range(n):
        pivot=next((i for i in range(r,m) if W[i][j]%p),None)
        if pivot is None:continue
        W[r],W[pivot]=W[pivot],W[r]
        inv=pow(W[r][j],-1,p)
        W[r]=[(a*inv)%p for a in W[r]]
        for i in range(r+1,m):
            c=W[i][j]
            if c:W[i]=[(a-c*b)%p for a,b in zip(W[i],W[r])]
        r+=1
        if r==m:break
    return r


def matinv(A:list[list[int]],p:int)->list[list[int]]:
    n=len(A)
    assert all(len(a)==n for a in A)
    W=[a.copy()+[int(i==j) for j in range(n)] for i,a in enumerate(A)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if W[i][j]%p),None)
        if pivot is None:raise ValueError('singular matrix')
        W[j],W[pivot]=W[pivot],W[j]
        inv=pow(W[j][j],-1,p)
        W[j]=[(a*inv)%p for a in W[j]]
        for i in range(n):
            if i==j:continue
            c=W[i][j]
            if c:W[i]=[(a-c*b)%p for a,b in zip(W[i],W[j])]
    return [row[n:] for row in W]


def submat(A, rows, cols):return [[A[i][j] for j in cols] for i in rows]

def matrix_sub(A,B,p):return [[(a-b)%p for a,b in zip(ar,br)] for ar,br in zip(A,B)]

def blockdiag(A,B,p):
    a=len(A);b=len(B)
    return [A[i]+[0]*b for i in range(a)]+[[0]*a+B[i] for i in range(b)]


def outer(u:list[int],v:list[int],p:int)->list[list[int]]:
    return [[x*y%p for y in v] for x in u]


def schur_cut_certificate(n:int,p:int,w:int)->dict:
    """F_N=blockdiag(0,S)+UV exactly, rank(UV)=m, n even.

    Construction costs dense elimination; *not* a fast FFT algorithm.
    """
    assert n%2==0
    m=n//2;F=dft_matrix(n,p,w)
    A=submat(F,range(m),range(m));B=submat(F,range(m),range(m,n))
    C=submat(F,range(m,n),range(m));D=submat(F,range(m,n),range(m,n))
    CAi=matmul(C,matinv(A,p),p)
    S=matrix_sub(D,matmul(CAi,B,p),p)
    U=[[int(i==j) for j in range(m)] for i in range(m)]+CAi
    V=[A[i]+B[i] for i in range(m)]
    UV=matmul(U,V,p)
    base=blockdiag([[0]*m for _ in range(m)],S,p)
    reconstructed=[[(base[i][j]+UV[i][j])%p for j in range(n)] for i in range(n)]
    assert reconstructed==F
    assert matrank(UV,p)==m
    assert matrank(submat(F,range(m),range(m,n)),p)==m
    # Stronger sharpness certificate: a rank-m residual even when the
    # block-diagonal baseline itself is invertible. The baseline is dense,
    # and constructing it is NOT counted as a cheap operation.
    H=matmul(CAi,B,p)
    witness=None
    for t in range(2,p):
        inv=pow((1-t)%p,-1,p)
        X=[[(t*v)%p for v in row] for row in A]
        Y=[[(D[i][j]-inv*H[i][j])%p for j in range(m)] for i in range(m)]
        if matrank(Y,p)<m:continue
        full_base=blockdiag(X,Y,p)
        residual=matrix_sub(F,full_base,p)
        assert matrank(full_base,p)==n
        assert matrank(residual,p)==m
        witness=t
        break
    assert witness is not None
    return {'n':n,'cut':m,'cross_rank':m,'bridge_rank':m,
            'invertible_block_baseline_witness':witness,
            'baseline_lower_rank':matrank(S,p),'construction':'Schur complement; dense elimination charged'}


def dense_star(n:int,p:int)->tuple[list[list[int]],int]:
    """O(N)-gate full-support invertible nonunitary transform; not F_N."""
    A=[[int(i==j) for j in range(n)] for i in range(n)]
    for j in range(1,n):A[0]=[(a+b)%p for a,b in zip(A[0],A[j])]
    for j in range(1,n):A[j]=[(a+b)%p for a,b in zip(A[j],A[0])]
    return A,2*(n-1)


def bridge_network(n:int,p:int,w:int,seed:int=44,steps:int=5)->dict:
    """Random numerical verification of telescoping rank sum on same fixed cut."""
    rng=random.Random(seed); m=n//2
    acc=[[int(i==j) for j in range(n)] for i in range(n)]
    base=[[int(i==j) for j in range(n)] for i in range(n)]
    rank_budget=0
    for t in range(steps):
        left=[[rng.randrange(p) for _ in range(m)] for _ in range(m)]
        right=[[rng.randrange(p) for _ in range(n-m)] for _ in range(n-m)]
        B=blockdiag(left,right,p)
        r=1 if t%2==0 else 2
        E=[[0]*n for _ in range(n)]
        for h in range(r):
            v=[rng.randrange(p) for _ in range(n)]
            u=[rng.randrange(p) for _ in range(n)]
            E=[[E[i][j]+u[i]*v[j] for j in range(n)] for i in range(n)]
        E=[[v%p for v in row] for row in E]
        T=[[(B[i][j]+E[i][j])%p for j in range(n)] for i in range(n)]
        acc=matmul(T,acc,p);base=matmul(B,base,p)
        rank_budget+=r
    residual_rank=matrank(matrix_sub(acc,base,p),p)
    off_rank=matrank(submat(acc,range(m),range(m,n)),p)
    assert residual_rank<=rank_budget and off_rank<=rank_budget
    return {'n':n,'stages':steps,'rank_budget':rank_budget,
            'residual_rank':residual_rank,'offdiag_rank':off_rank}


def eval_radix2_remainder(x:list[int],p:int,w:int)->tuple[list[int],Ledger]:
    """Classical DIF FFT interpreted as *shared binomial remainder* graph.

    Each split roots z^r=c vs z^r=-c and reuses the multiplication c*x_high.
    Charged O(N log N); not an improved general FFT.
    """
    n=len(x)
    if n<2 or n&(n-1):raise ValueError('power-of-two N required')
    ledger=Ledger(inputs=n);roots=roots_table(n,p,w,ledger)
    out=[None]*n
    def rec(poly,labels):
        s=len(labels)
        if s==1:
            out[labels[0]]=poly[0]%p;ledger.writes+=1;return
        m=s//2
        left=labels[::2];right=labels[1::2]
        c=roots[(-left[0]*m)%n]
        L=[];R=[]
        for j in range(m):
            tw=ledger.mul(c,poly[j+m],p)
            L.append(ledger.add(poly[j],tw,p))
            R.append(ledger.sub(poly[j],tw,p))
            ledger.butterflies+=1
        rec(L,left);rec(R,right)
    rec([v%p for v in x],list(range(n)))
    return out,ledger


def _vanish_poly(labels,roots,p,ledger,cache):
    key=tuple(labels)
    if key in cache:return cache[key]
    P=[1]
    n=len(roots)
    for j in labels:
        z=roots[(-j)%n]
        Q=[0]*(len(P)+1)
        for i,v in enumerate(P):
            zprod=ledger.mul(v,z,p,plan=True)
            Q[i]=ledger.sub(Q[i],zprod,p,plan=True)
            Q[i+1]=ledger.add(Q[i+1],v,p,plan=True)
        P=Q
    cache[key]=P
    return P


def _remainder(P,Q,p,ledger):
    """Monic polynomial remainder; Q annihilates one child root set."""
    d=len(Q)-1;W=P.copy()
    assert Q[-1]==1
    for k in range(len(W)-1,d-1,-1):
        c=W[k]
        if not c:continue
        for j in range(d):
            if not Q[j]:continue
            prod=ledger.mul(c,Q[j],p)
            W[k-d+j]=ledger.sub(W[k-d+j],prod,p)
        W[k]=0
    return W[:d]


def eval_generic_remainder(x:list[int],p:int,w:int,policy='contiguous')->tuple[list[int],Ledger]:
    """Exact alternative full-input circuit with charged root polynomials and divisions.

    Unoptimized independent divisions; tests whether unconventional root partitions
    help before shared-quotient arithmetic circuit synthesis.
    """
    n=len(x)
    if n<2 or n&(n-1):raise ValueError('power of two N required')
    ledger=Ledger(inputs=n);roots=roots_table(n,p,w,ledger)
    out=[None]*n;cache={}
    special=(0,1,2,3,4,8,10,12)
    def rec(P,labels,top=False):
        if len(labels)==1:
            out[labels[0]]=P[0]%p;ledger.writes+=1;return
        s=len(labels)
        if policy=='noncoset16' and top and n==16:
            L=list(special);R=sorted(set(labels)-set(special))
        elif policy=='contiguous':L=labels[:s//2];R=labels[s//2:]
        else:L=labels[::2];R=labels[1::2]
        VL=_vanish_poly(L,roots,p,ledger,cache)
        VR=_vanish_poly(R,roots,p,ledger,cache)
        rec(_remainder(P,VL,p,ledger),L)
        rec(_remainder(P,VR,p,ledger),R)
    rec([v%p for v in x],list(range(n)),True)
    return out,ledger


def _mul_zeta_vec(v:list[int],j:int,n:int)->list[int]:
    """Multiply cyclotomic integer by zeta^j modulo Phi_{2^m}(z)=z^(n/2)+1."""
    d=n//2; out=[0]*d
    for i,c in enumerate(v):
        t=(i+j)%n
        if t>=d:out[t-d]-=c
        else:out[t]+=c
    return out


def exact_cyclotomic_root_poly(labels:tuple[int,...],n:int)->list[list[int]]:
    """Vanishing P(z)=product(z-zeta^j), coefficients in Z[zeta_N].

    Only for n a power of two; exact integer arithmetic; no finite-field
    spurious coefficient cancellations.
    """
    if n<2 or n&(n-1):raise ValueError('n=2^m only')
    d=n//2
    P=[[1]+[0]*(d-1)]
    for j in labels:
        Q=[[0]*d for _ in range(len(P)+1)]
        for i,v in enumerate(P):
            scaled=_mul_zeta_vec(v,j,n)
            Q[i]=[a-b for a,b in zip(Q[i],scaled)]
            Q[i+1]=[a+b for a,b in zip(Q[i+1],v)]
        P=Q
    return P


def coeff_support(P:list[list[int]])->int:
    return sum(any(v) for v in P)


def exhaustive_root_split(n:int=16)->dict:
    """All binomial/balanced-half subset possibilities, exact cyclotomic ring.

    n=16 involves 12870 distinct subsets, 6435 complement-pairs.
    """
    if n not in (4,8,16):raise ValueError('limit exhaustive set size')
    m=n//2;full=set(range(n))
    supports={}
    for A in combinations(range(n),m):
        supports[A]=coeff_support(exact_cyclotomic_root_poly(A,n))
    hist=Counter(supports.values());paired=Counter(); examples={}
    min_non_periodic=(10**9,None)
    for A,sa in supports.items():
        B=tuple(sorted(full-set(A)))
        if A>B:continue
        sb=supports[B]
        periodic=any({(j+t)%n for j in A}==set(A) for t in range(1,n))
        key=(sa+sb,periodic)
        paired[key]+=1
        if sa+sb not in examples:examples[sa+sb]=list(A)
        if not periodic and sa+sb<min_non_periodic[0]:
            min_non_periodic=(sa+sb,list(A))
    return {'n':n,'half':m,'subsets':len(supports),
            'complement_pairs':sum(paired.values()),
            'support_histogram':{str(k):v for k,v in sorted(hist.items())},
            'pair_support_histogram':{f'{k[0]}_{"periodic" if k[1] else "nonperiodic"}':v for k,v in sorted(paired.items())},
            'best_split_total_support':min(x[0] for x in paired),
            'best_nonperiodic_total_support':None if min_non_periodic[1] is None else min_non_periodic[0],
            'best_nonperiodic_subset':min_non_periodic[1],
            'example_subsets':{str(k):v for k,v in sorted(examples.items())[:5]}}


def radix2_symbolic_merges(n:int,p:int,w:int)->dict:
    """Number of identical/proportional linear forms across all FFT stages.

    Stage inputs are basis vectors in bit-reversed order; each stage remains
    invertible, and each wire has support exactly 2^stage. Thus zero merges.
    """
    if n<2 or n&(n-1):raise ValueError('n must be power of two')
    roots=roots_table(n,p,w);ell=n.bit_length()-1
    def bitrev(i):return int(f'{i:0{ell}b}'[::-1],2)
    state=[[int(j==bitrev(i)) for j in range(n)] for i in range(n)]
    seen={};duplicate=0;per_stage=[]
    def canonical(v):
        pivot=next(a for a in v if a%p)
        inv=pow(pivot,-1,p)
        return tuple(a*inv%p for a in v)
    for stage in range(ell+1):
        rows=[canonical(v) for v in state]
        stage_dup=sum(r in seen for r in rows)
        duplicate+=stage_dup
        for r in rows:seen[r]=stage
        per_stage.append({'stage':stage,'forms':n,'support':1<<stage,'duplicate':stage_dup})
        if stage==ell:break
        span=1<<(stage+1);m=span//2
        for base in range(0,n,span):
            for k in range(m):
                i=base+k;j=i+m
                u=state[i];v=state[j];tw=roots[(-k*n//span)%n]
                scaled=[a*tw%p for a in v]
                state[i]=[(a+b)%p for a,b in zip(u,scaled)]
                state[j]=[(a-b)%p for a,b in zip(u,scaled)]
    assert state==dft_matrix(n,p,w)
    return {'n':n,'total_forms':n*(ell+1),'unique_forms':len(seen),
            'proportional_merges':duplicate,'layers':per_stage}


def unitary_entropy_audit(n:int)->dict:
    """Reproduce Ailon 2013 unitary 2-wire entropy lower bound on classical FFT."""
    if n<2 or n&(n-1):raise ValueError('n must be power of two')
    ell=n.bit_length()-1
    def bitrev(i):return int(f'{i:0{ell}b}'[::-1],2)
    state=[[complex(j==bitrev(i)) for j in range(n)] for i in range(n)]
    def ent(v):
        return -sum((abs(a)**2)*log2(abs(a)**2) for a in v if abs(a)>1e-12)
    increases=[]
    for stage in range(ell):
        span=1<<(stage+1);m=span//2
        for base in range(0,n,span):
            for k in range(m):
                i=base+k;j=i+m
                u=state[i];v=state[j]
                old=ent(u)+ent(v)
                tw=exp(-2j*pi*k/span)
                state[i]=[(a+tw*b)/sqrt(2) for a,b in zip(u,v)]
                state[j]=[(a-tw*b)/sqrt(2) for a,b in zip(u,v)]
                inc=ent(state[i])+ent(state[j])-old
                assert inc<=2+1e-7
                increases.append(inc)
    final=sum(ent(v) for v in state)
    assert abs(final-n*log2(n))<1e-6
    return {'n':n,'gates':len(increases),'max_entropy_increment':max(increases),
            'min_entropy_increment':min(increases),'total_entropy':final,
            'lower_bound':n*log2(n)/2}


def lut_gate_bound(n:int,p:int,table_exponent:int=2)->dict:
    """Explicit truth-table r-input blocks over Fp, at most n^c entries.

    Polynomial table => r <= floor(c log(n)/log(p)); stage-only grammar.
    No statement about unrestricted algebraic circuits.
    """
    budget=n**table_exponent
    width=0
    while p**(width+1)<=budget:width+=1
    return {'n':n,'field_size':p,'table_entries_budget':budget,
            'max_complete_block_arity':width,'necessary_levels_if_full_width':
            None if width<2 else __import__('math').ceil(log2(n)/log2(width)),
            'proof':'explicit full table size p^r; stage influence <=r^d'}


def remainder_transfer(P:list[int],p:int)->list[list[int]]:
    """High-coefficient transfer z^(m+t) mod monic P, for t=0,...,m-1."""
    m=len(P)-1
    R=[[0]*m for _ in range(m)]
    for t in range(m):
        coeff=[0]*(2*m);coeff[m+t]=1
        for k in range(2*m-1,m-1,-1):
            c=coeff[k]
            if c:
                for j in range(m):
                    coeff[k-m+j]=(coeff[k-m+j]-c*P[j])%p
                coeff[k]=0
        for i in range(m):R[i][t]=coeff[i]
    return R


def root_poly_mod(labels:tuple[int,...],roots:list[int],p:int)->list[int]:
    n=len(roots);P=[1]
    for j in labels:
        z=roots[(-j)%n];Q=[0]*(len(P)+1)
        for i,a in enumerate(P):
            Q[i]=(Q[i]-a*z)%p
            Q[i+1]=(Q[i+1]+a)%p
        P=Q
    return P


def crt_bridge_certificate(n:int,p:int,w:int,root_a:tuple[int,...])->dict:
    """Matrix for coefficient CRT: [[I,R_A],[I,R_B]]; difference full rank."""
    assert n%2==0
    m=n//2;root_a=tuple(sorted(root_a))
    assert len(root_a)==m and len(set(root_a))==m
    b=tuple(j for j in range(n) if j not in root_a)
    roots=roots_table(n,p,w)
    PA=root_poly_mod(root_a,roots,p);PB=root_poly_mod(b,roots,p)
    RA=remainder_transfer(PA,p);RB=remainder_transfer(PB,p)
    difference=matrix_sub(RB,RA,p)
    rank=matrank(difference,p)
    assert rank==m
    support_a=sum(v!=0 for row in RA for v in row)
    support_b=sum(v!=0 for row in RB for v in row)
    return {'n':n,'a':list(root_a),'b':list(b),
            'transfer_rank':rank,'support_a':support_a,'support_b':support_b,
            'combined_support':support_a+support_b,
            'poly_support_a':sum(v!=0 for v in PA),
            'poly_support_b':sum(v!=0 for v in PB)}


def enumerate_crt_transfer_supports(n:int,p:int,w:int)->dict:
    """Exhaustive finite-field transfer-matrix sparsity, all balanced root splits.

    Unlike exact cyclotomic root-polynomial search, nonzero counts here are
    F_p-specific and may decrease accidentally modulo p.
    """
    if n not in (4,8,16):raise ValueError('limited exact search')
    m=n//2;roots=roots_table(n,p,w)
    hist=Counter();samples={};best_non=(10**9,None)
    for a in combinations(range(n),m):
        b=tuple(j for j in range(n) if j not in a)
        if a>b:continue
        PA=root_poly_mod(a,roots,p);PB=root_poly_mod(b,roots,p)
        RA=remainder_transfer(PA,p);RB=remainder_transfer(PB,p)
        nnz=sum(v!=0 for row in RA for v in row)+sum(v!=0 for row in RB for v in row)
        periodic=any({(j+t)%n for j in a}==set(a) for t in range(1,n))
        hist[(nnz,periodic)]+=1
        if nnz not in samples:samples[nnz]=list(a)
        if not periodic and nnz<best_non[0]:best_non=(nnz,list(a))
    return {'n':n,'p':p,'pairs':sum(hist.values()),
            'histogram':{f'{v}_{"periodic" if periodic else "nonperiodic"}':cnt
                         for (v,periodic),cnt in sorted(hist.items())},
            'minimum_transfer_nnz':min(k[0] for k in hist),
            'best_nonperiodic_transfer_nnz':best_non[0] if best_non[1] else None,
            'best_nonperiodic_subset':best_non[1],
            'first_support_examples':{str(k):v for k,v in sorted(samples.items())[:6]}}
