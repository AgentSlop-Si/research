"""Phase 22: exact Fourier-bilinear Gram gate, permutation recovery, and
independently ordered O(N)-apply weighted-cycle Green experiments.

All exact calculations are over F_998244353. This is a RESEARCH VERIFIER,
not a new FFT. Dense diagnostics are cubic, while GreenSum.apply is linear.
"""
from __future__ import annotations
import random
from dataclasses import dataclass

MOD = 998244353
GEN = 3


def root(n: int) -> int:
    if n < 2 or n & (n - 1) or (MOD - 1) % n:
        raise ValueError('length must be a power of two dividing MOD-1')
    return pow(GEN, -(MOD - 1)//n, MOD)


def sqrt_mod(a: int) -> int:
    a %= MOD
    if a == 0: return 0
    if pow(a, (MOD - 1)//2, MOD) != 1: raise ValueError('not a square')
    q = MOD-1; s = 0
    while q % 2 == 0: q //= 2; s += 1
    z = 2
    while pow(z, (MOD-1)//2, MOD) != MOD-1: z += 1
    c = pow(z, q, MOD)
    x = pow(a, (q+1)//2, MOD)
    t = pow(a, q, MOD)
    m = s
    while t != 1:
        i=1; y=t*t%MOD
        while y != 1:
            y = y*y%MOD; i += 1
        b = pow(c, 1<<(m-i-1), MOD)
        x = x*b%MOD
        t = t*b*b%MOD
        c = b*b%MOD
        m = i
    return x


def fft_matrix(n: int) -> list[list[int]]:
    w=root(n)
    scale=pow(sqrt_mod(n), -1, MOD)
    return [[scale*pow(w, i*j, MOD)%MOD for j in range(n)] for i in range(n)]


def identity(n:int)->list[list[int]]:
    return [[int(i==j) for j in range(n)] for i in range(n)]


def transpose(a:list[list[int]])->list[list[int]]:
    return [list(row) for row in zip(*a)]


def matmul(a:list[list[int]],b:list[list[int]])->list[list[int]]:
    n=len(a); p=len(b); m=len(b[0]);bt=transpose(b)
    return [[sum(a[i][k]*bt[j][k] for k in range(p))%MOD for j in range(m)] for i in range(n)]


def invert(a:list[list[int]])->list[list[int]]:
    n=len(a)
    z=[row[:]+identity(n)[i] for i,row in enumerate(a)]
    for k in range(n):
        j=next((j for j in range(k,n) if z[j][k]),None)
        if j is None: raise ValueError('matrix singular')
        z[k],z[j]=z[j],z[k]
        inv=pow(z[k][k],-1,MOD)
        z[k]=[(v*inv)%MOD for v in z[k]]
        for i in range(n):
            if i==k or z[i][k]==0:continue
            factor=z[i][k]
            z[i]=[(u-factor*v)%MOD for u,v in zip(z[i],z[k])]
    return [row[n:] for row in z]


def reverse_matrix(n:int)->list[list[int]]:
    return [[int(j == (-i)%n) for j in range(n)] for i in range(n)]


def dense_from_apply(oracle,n:int)->list[list[int]]:
    cols=[]
    for j in range(n):
        e=[0]*n;e[j]=1
        cols.append(oracle(e))
    return transpose(cols)


def quadratic_form_data(A:list[list[int]],B:list[list[int]])->tuple[list[list[int]],list[list[int]]]:
    """For F=A Q P B, C=B^-T J B^-1 must equal P^T Q K Q P."""
    K=matmul(transpose(A),A)
    Bi=invert(B)
    C=matmul(matmul(transpose(Bi),reverse_matrix(len(A))),Bi)
    return K,C


def quadratic_fingerprint(K:list[list[int]])->list[list[int]]:
    """h_ij=K_ij^2/(K_ii*K_jj), defined when all diagonals nonzero.
    Invariant under arbitrary invertible diagonal congruence.
    """
    n=len(K)
    if any(K[i][i]==0 for i in range(n)):
        raise ValueError('diagonal-isotropic form; this fast gate is inconclusive')
    invd=[pow(K[i][i],-1,MOD) for i in range(n)]
    return [[K[i][j]*K[i][j]*invd[i]*invd[j]%MOD for j in range(n)] for i in range(n)]


def permutation_fingerprint_gate(K,C):
    """Return (status, recovered permutation-or-None).
    'excluded' is a mathematically definitive all-permutation/no-phase veto.
    'ambiguous' means fingerprint did not identify a unique ordering.
    'candidate' means an exact necessary invariant matched; not sufficient.
    """
    n=len(K)
    zK=sum(K[i][i]==0 for i in range(n))
    zC=sum(C[i][i]==0 for i in range(n))
    if zK != zC:return 'excluded',None
    if zK:return 'inconclusive',None
    h=quadratic_fingerprint(K);g=quadratic_fingerprint(C)
    rh=[tuple(sorted(row)) for row in h]
    rg=[tuple(sorted(row)) for row in g]
    if sorted(rh)!=sorted(rg):return 'excluded',None
    n=len(K)
    if len(set(rh))!=n: return 'ambiguous',None
    lookup={v:i for i,v in enumerate(rh)}
    perm=[lookup[v] for v in rg]  # P e_i=e_(perm[i])
    if any(g[i][j]!=h[perm[i]][perm[j]] for i in range(n) for j in range(n)):
        return 'excluded',None
    return 'candidate',perm


def recover_mask(K,C,perm):
    """If possible, recover Q such that C=P^T Q K Q P (over F_p).
    If K_ij zero, inconclusive rather than dividing by zero.
    Global sign ambiguity is unavoidable from the Gram equation alone.
    """
    n=len(K)
    invperm=[0]*n
    for i,p in enumerate(perm):invperm[p]=i
    d=[[C[invperm[i]][invperm[j]] for j in range(n)] for i in range(n)]
    if any(K[i][j]==0 for i in range(n) for j in range(n)):
        return None
    ratios=[[d[i][j]*pow(K[i][j],-1,MOD)%MOD for j in range(n)] for i in range(n)]
    if any(ratios[i][j]*ratios[0][0]%MOD != ratios[i][0]*ratios[0][j]%MOD
           for i in range(n) for j in range(n)):
        return None
    try:q0=sqrt_mod(ratios[0][0])
    except ValueError:return None
    if not q0:return None
    inv=pow(q0,-1,MOD)
    q=[ratios[i][0]*inv%MOD for i in range(n)]
    if any(q[i]*K[i][j]*q[j]%MOD != d[i][j] for i in range(n) for j in range(n)):
        return None
    return q


def permute_rows_inverse(M,perm):
    """P e_i=e_perm[i]; return P^-1 M."""
    return [M[perm[i]][:] for i in range(len(perm))]


def make_positive_control(A,perm,q,target):
    """B=P^-1 Q^-1 A^-1 target, for a known exact factorization.
    B generally DENSE: mathematical positive control, NOT a fast circuit.
    """
    B=matmul(invert(A),target)
    B=[[v*pow(q[i],-1,MOD)%MOD for v in row] for i,row in enumerate(B)]
    return permute_rows_inverse(B,perm)


def apply_sandwich(A,q,perm,B):
    n=len(q)
    PB=[B[i][:] for i in range(n)]
    # matrix for QP B, with row perm[i] from B[i]
    QPB=[[0]*n for _ in range(n)]
    for i,p in enumerate(perm):
        QPB[p]=[q[p]*v%MOD for v in PB[i]]
    return matmul(A,QPB)


def weyl_defect_counts(M):
    """Two exact Weyl equations for normalized negative-exponent DFT."""
    n=len(M);w=root(n)
    defect1=0;defect2=0
    for i in range(n):
        for j in range(n):
            # (M Z)_ij=M_i,j+1; (Z^-1 M)_ij=M_i+1,j
            if M[i][(j+1)%n]!=pow(w,i,MOD)*M[i][j]%MOD:defect1+=1
            if pow(w,j,MOD)*M[i][j]%MOD!=M[(i+1)%n][j]:defect2+=1
    return defect1,defect2


@dataclass
class WeightedCyclicGreen:
    """Solve (I-S)y=x in O(N), where S advances along permutation cycle.
    S x at order-position j equals weights[j]*x[j-1 mod N].
    """
    order:list[int]
    weights:list[int]
    left:list[int]
    right:list[int]
    inv_den:int

    @classmethod
    def prepare(cls,order,weights,left=None,right=None):
        n=len(order)
        if sorted(order)!=list(range(n)):raise ValueError('invalid order')
        weights=[v%MOD for v in weights]
        product=1
        for w in weights:product=product*w%MOD
        den=(1-product)%MOD
        if not den:raise ValueError('singular weighted cycle')
        if left is None:left=[1]*n
        if right is None:right=[1]*n
        return cls(list(order),weights,list(left),list(right),pow(den,-1,MOD))

    def apply(self,x):
        n=len(self.order)
        inp=[self.right[j]*x[self.order[j]]%MOD for j in range(n)]
        a=1;b=0
        aa=[1]+[0]*(n-1);bb=[0]*n
        for j in range(1,n):
            weight=self.weights[j]
            a=a*weight%MOD
            b=(inp[j]+weight*b)%MOD
            aa[j]=a;bb[j]=b
        y0=(inp[0]+self.weights[0]*b)*self.inv_den%MOD
        out=[0]*n
        for j in range(n):
            val=(aa[j]*y0+bb[j])%MOD
            out[self.order[j]]=self.left[j]*val%MOD
        return out


class GreenSum:
    def __init__(self,terms):
        self.terms=terms;self.n=len(terms[0].order)
    def __call__(self,x):
        out=[0]*len(x)
        for g in self.terms:
            v=g.apply(x)
            out=[(a+b)%MOD for a,b in zip(out,v)]
        return out


def seeded_green_sum(n,seed,q=2):
    """Independent random cycles, arbitrary nonzero weights and gauges.
    Exact O(qN)-time APPLY; dense reconstruction only for testing.
    """
    rng=random.Random(seed)
    w=root(n)
    roots=[pow(w,k,MOD) for k in range(n)]
    terms=[]
    for _ in range(q):
        order=list(range(n));rng.shuffle(order)
        # phases are high-order roots, with edge product != 1.
        for attempt in range(50):
            weights=[rng.choice(roots) for _ in range(n)]
            prod=1
            for v in weights:prod=prod*v%MOD
            if prod !=1:break
        else:raise RuntimeError('bad random generator')
        left=[rng.choice(roots) for _ in range(n)]
        right=[rng.choice(roots) for _ in range(n)]
        terms.append(WeightedCyclicGreen.prepare(order,weights,left,right))
    return GreenSum(terms)


def demo(n=16,seed=2026):
    rng=random.Random(seed)
    A=dense_from_apply(seeded_green_sum(n,seed),n)
    B=dense_from_apply(seeded_green_sum(n,seed+1),n)
    K,C=quadratic_form_data(A,B)
    status,perm=permutation_fingerprint_gate(K,C)
    good_perm=list(range(n));rng.shuffle(good_perm)
    good_q=[rng.randrange(1,MOD) for _ in range(n)]
    F=fft_matrix(n)
    Bgood=make_positive_control(A,good_perm,good_q,F)
    K2,C2=quadratic_form_data(A,Bgood)
    sg,p=permutation_fingerprint_gate(K2,C2)
    qr=recover_mask(K2,C2,p) if p else None
    good_M=apply_sandwich(A,qr,p,Bgood) if qr else None
    if good_M is not None and good_M!=F:
        qr=[(-v)%MOD for v in qr]
        good_M=apply_sandwich(A,qr,p,Bgood)
    return {'n':n,'green_gate':status,'control_gate':sg,
            'permutation_recovered':p==good_perm,
            'mask_recovered':qr==good_q,
            'exact_dft':good_M==F,
            'control_weyl':weyl_defect_counts(good_M) if good_M is not None else None}


if __name__=='__main__':
    for n in (8,16,32,64):
        print(demo(n))
