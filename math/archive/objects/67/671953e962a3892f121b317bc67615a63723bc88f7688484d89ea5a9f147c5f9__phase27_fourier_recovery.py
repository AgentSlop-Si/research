"""Phase 27: black-box recovery of Fourier monomial gauges over F_998244353.

If M_ij = l_i*r_j*omega^(p_i q_j), two forward COLUMN probes (for
0 and one primitive-difference column), plus two TRANSPOSE row probes,
recover p,q and all row/column gauges up to the natural affine ambiguity.
Independent random-vector validation gives a one-sided error <=p^-trials.
This is a correctness/synthesis gate, NOT a faster DFT executor.

The 4 core probes are counted after identifying a primitive second column.
Unknown permutations require an expected ~2 second-column trials for true
Fourier matrices, hence ~5 oracle calls total in expectation.
"""
from __future__ import annotations
from dataclasses import dataclass
import random
from typing import Callable

P=998244353
GENERATOR=3


def root(n:int)->int:
    if n<2 or n & (n-1) or (P-1)%n:
        raise ValueError('power-of-two n dividing p-1 required')
    return pow(GENERATOR,-(P-1)//n,P)


def fft_unscaled(x:list[int])->list[int]:
    """Slow-to-beat reference radix-2 FFT, O(n log n), modular and exact."""
    n=len(x)
    w=root(n)
    a=[v%P for v in x]
    j=0
    for i in range(1,n):
        bit=n//2
        while j&bit:j^=bit;bit//=2
        j^=bit
        if i<j:a[i],a[j]=a[j],a[i]
    size=2
    while size<=n:
        twstep=pow(w,n//size,P)
        for off in range(0,n,size):
            tw=1
            for k in range(size//2):
                u=a[off+k];v=tw*a[off+k+size//2]%P
                a[off+k]=(u+v)%P
                a[off+k+size//2]=(u-v)%P
                tw=tw*twstep%P
        size*=2
    return a


def basis(n:int,i:int)->list[int]:
    v=[0]*n;v[i]=1
    return v


def batch_inverse(values:list[int])->list[int]:
    """Invert N nonzero finite-field values using O(N) products and one inverse."""
    n=len(values)
    pref=[1]*(n+1)
    for i,v in enumerate(values):
        if v%P==0:raise ZeroDivisionError('zero encountered')
        pref[i+1]=pref[i]*(v%P)%P
    inv=pow(pref[n],-1,P)
    result=[0]*n
    for i in range(n-1,-1,-1):
        result[i]=inv*pref[i]%P
        inv=inv*values[i]%P
    return result


class MonomialFourier:
    """Positive control M_ij=left[i]*right[j]*omega^(row[i]*col[j])."""
    def __init__(self,row:list[int],col:list[int],left:list[int],right:list[int]):
        self.n=len(row)
        if not (len(col)==len(left)==len(right)==self.n):raise ValueError('size')
        if sorted(row)!=list(range(self.n)) or sorted(col)!=list(range(self.n)):
            raise ValueError('not permutation')
        if any(v%P==0 for v in left+right):raise ValueError('zero gauge')
        self.row=row;self.col=col;self.left=left;self.right=right
    def apply(self,x:list[int])->list[int]:
        n=self.n
        v=[0]*n
        for j in range(n):v[self.col[j]]=self.right[j]*x[j]%P
        ft=fft_unscaled(v)
        return [self.left[i]*ft[self.row[i]]%P for i in range(n)]
    def transpose(self,x:list[int])->list[int]:
        n=self.n
        v=[0]*n
        for i in range(n):v[self.row[i]]=self.left[i]*x[i]%P
        ft=fft_unscaled(v)
        return [self.right[j]*ft[self.col[j]]%P for j in range(n)]


@dataclass
class FourierCertificate:
    n:int
    row_perm:list[int]
    col_perm:list[int]
    first_column:list[int]
    first_row:list[int]
    primitive_col:int
    omega:int

    def predict(self,x:list[int])->list[int]:
        n=self.n
        if len(x)!=n:raise ValueError('bad dimension')
        u=pow(self.first_column[0],-1,P)
        v=[0]*n
        for j in range(n):
            v[self.col_perm[j]]=self.first_row[j]*u%P*x[j]%P
        ft=fft_unscaled(v)
        return [self.first_column[i]*ft[self.row_perm[i]]%P for i in range(n)]

    def predict_transpose(self,x:list[int])->list[int]:
        n=self.n
        u=pow(self.first_column[0],-1,P)
        v=[0]*n
        for i in range(n):v[self.row_perm[i]]=self.first_column[i]*x[i]%P
        ft=fft_unscaled(v)
        return [self.first_row[j]*u%P*ft[self.col_perm[j]]%P for j in range(n)]


@dataclass
class RecoverReport:
    status:str
    reason:str
    oracle_calls_forward:int
    oracle_calls_transpose:int
    certificate:FourierCertificate|None=None
    random_trials:int=0
    mismatching_entries:int=0


def recover(oracle:Callable[[list[int]],list[int]],
            transpose:Callable[[list[int]],list[int]],
            n:int,*,max_other_columns:int|None=None,
            trials:int=2,seed:int=2701,randomize_candidates:bool=True)->RecoverReport:
    """Exact structural rejection, or gauge recovery with randomized validation.

    False acceptance conditional on a nonmatching candidate <= P^-trials;
    uses independent uniform random input vectors. Fixed seed is deterministic
    reproducibility only. For a rigorous randomized statement set seed=None.

    'inconclusive' may occur if too few second columns were tried; 'rejected'
    reports an explicit necessary-condition failure or a witnessed mismatch.
    """
    if n<4 or n&(n-1):raise ValueError('n power of 2>=4')
    if trials<0:raise ValueError('negative trial count')
    c_forward=0;c_transpose=0
    def fwd(v):
        nonlocal c_forward
        c_forward+=1
        ans=oracle(v)
        if len(ans)!=n:raise ValueError('oracle length')
        return [z%P for z in ans]
    def trn(v):
        nonlocal c_transpose
        c_transpose+=1
        ans=transpose(v)
        if len(ans)!=n:raise ValueError('transpose length')
        return [z%P for z in ans]
    first=fwd(basis(n,0))
    if any(z==0 for z in first):
        return RecoverReport('rejected','a Fourier monomial matrix has no zero entries',c_forward,c_transpose)
    omega=root(n)
    roots={}
    phase=1
    for k in range(n):
        roots[phase]=k
        phase=phase*omega%P
    candidates=list(range(1,n))
    rng=random.SystemRandom() if seed is None else random.Random(seed)
    if randomize_candidates:rng.shuffle(candidates)
    if max_other_columns is not None:
        if max_other_columns<1:raise ValueError('bad column budget')
        candidates=candidates[:max_other_columns]
    invfirst=batch_inverse(first)
    rowperm=None;good_col=None
    for j in candidates:
        cj=fwd(basis(n,j))
        if cj[0]==0 or any(z==0 for z in cj):
            return RecoverReport('rejected','encountered a zero Fourier-monomial entry',c_forward,c_transpose)
        rowzero=first[0]*pow(cj[0],-1,P)%P
        phases=[cj[i]*invfirst[i]%P*rowzero%P for i in range(n)]
        if any(z not in roots for z in phases):
            return RecoverReport('rejected','two-column Haagerup ratio not an Nth root',c_forward,c_transpose)
        powers=[roots[z] for z in phases]
        if len(set(powers))==n:
            rowperm=powers;good_col=j
            break
    if rowperm is None:
        status='rejected' if len(candidates)==n-1 else 'inconclusive'
        reason='no primitive-difference column exists' if status=='rejected' else 'no primitive column in sampled budget'
        return RecoverReport(status,reason,c_forward,c_transpose)
    i1=rowperm.index(1)
    firstrow=trn(basis(n,0))
    specialrow=trn(basis(n,i1))
    if any(z==0 for z in firstrow) or any(z==0 for z in specialrow):
        return RecoverReport('rejected','transpose row contains zero entry',c_forward,c_transpose)
    rowratio0=firstrow[0]*pow(specialrow[0],-1,P)%P
    invfirstrow=batch_inverse(firstrow)
    phases=[specialrow[j]*invfirstrow[j]%P*rowratio0%P for j in range(n)]
    if any(z not in roots for z in phases):
        return RecoverReport('rejected','two-row Haagerup ratio not an Nth root',c_forward,c_transpose)
    colperm=[roots[z] for z in phases]
    if len(set(colperm))!=n or colperm[good_col]!=1:
        return RecoverReport('rejected','inconsistent recovered column permutation',c_forward,c_transpose)
    cert=FourierCertificate(n,rowperm,colperm,first,firstrow,good_col,omega)
    mismatches=0
    for _ in range(trials):
        v=[rng.randrange(P) for _ in range(n)]
        actual=fwd(v)
        expected=cert.predict(v)
        mismatches+=sum(x!=y for x,y in zip(actual,expected))
        if mismatches:
            return RecoverReport('rejected','random exact-vector witness differs from recovered Fourier',
                                 c_forward,c_transpose,cert,random_trials=_+1,mismatching_entries=mismatches)
    return RecoverReport('passes_sample',
                         'recovered Fourier monomial normal form; random tests passed (not a proof)',
                         c_forward,c_transpose,cert,random_trials=trials)


if __name__=='__main__':
    for n in (16,64,256):
        rng=random.Random(2700+n)
        row=list(range(n));col=list(range(n));rng.shuffle(row);rng.shuffle(col)
        control=MonomialFourier(row,col,
                              [rng.randrange(1,P) for _ in range(n)],
                              [rng.randrange(1,P) for _ in range(n)])
        r=recover(control.apply,control.transpose,n,max_other_columns=n-1,trials=2)
        print(n,r.status,r.oracle_calls_forward,r.oracle_calls_transpose)
