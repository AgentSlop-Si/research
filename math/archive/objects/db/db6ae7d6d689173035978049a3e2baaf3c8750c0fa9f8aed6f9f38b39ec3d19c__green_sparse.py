"""Phase17 -- exact Fourier evaluation with sparse noncommuting Green forcing.

Finite-field implementation, not a new worst-case FFT algorithm.
For omega a primitive N-th root in F_p, N=2^t:
    L = a I + b S + c D
    P = a I + c S + b D^{-1}
    L * F = F * P
where (Sx)[j] = x[j-1 mod N], (Dx)[j] = omega^j x[j].
If P*x has K nonzeros, compute its DFT by input-pruned radix-2,
then solve L*y = F*(P*x). Every output equals F*x exactly.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

P0 = 2013265921
G0 = 31


def primitive_root(n: int, p=P0, generator=G0):
    if n < 2 or n & (n - 1) or (p - 1) % n:
        raise ValueError("n must be power of two dividing p-1")
    omega = pow(generator, (p-1)//n, p)
    if pow(omega, n, p) != 1 or pow(omega, n//2, p) == 1:
        raise ValueError("generator does not yield primitive root")
    return omega


def root_powers(n, omega, p=P0):
    out = [1] * n
    for j in range(1, n):
        out[j] = out[j-1] * omega % p
    return out


def inv_all(nonzero, p=P0):
    """Batch inversion with 1 modular inverse and O(n) modular multiplies."""
    n = len(nonzero)
    prefix = [1] * (n+1)
    for i,d in enumerate(nonzero):
        prefix[i+1] = prefix[i] * d % p
    if prefix[-1] == 0:
        raise ValueError("zero diagonal entry")
    invtot = pow(prefix[-1], -1, p)
    result = [0]*n
    for i in range(n-1,-1,-1):
        result[i] = invtot * prefix[i] % p
        invtot = invtot * nonzero[i] % p
    return result


@dataclass
class Cost:
    root_mults: int=0
    split_entries: int=0
    node_size_sum: int=0
    full_butterflies: int=0
    odd_only_butterflies: int=0
    even_only_butterflies: int=0
    ntt_mults: int=0
    ntt_adds: int=0
    ntt_negs: int=0
    output_writes: int=0
    preconditioner_mults: int=0
    preconditioner_adds: int=0
    solve_mults: int=0
    solve_adds: int=0
    forward_direct_mults: int=0
    forward_direct_adds: int=0
    support_checks: int=0
    field_inversions: int=0
    def arithmetic(self):
        return sum((self.root_mults,self.ntt_mults,self.ntt_adds,self.ntt_negs,
                    self.preconditioner_mults,self.preconditioner_adds,
                    self.solve_mults,self.solve_adds,self.forward_direct_mults,
                    self.forward_direct_adds))


class SparseInputDFT:
    def __init__(self, n, omega, p=P0):
        self.n,self.omega,self.p = n,omega,p
        self.powers = root_powers(n,omega,p)

    def from_entries(self, entries: dict[int,int], cost: Optional[Cost]=None):
        """Sparse DIT FFT returning all outputs. Count nontrivial work and writes.
        The root table is charged explicitly even if cached by a caller.
        """
        if cost is None:
            cost=Cost()
        n,p,powers=self.n,self.p,self.powers
        cost.root_mults += n-1
        clean = {j:(v%p) for j,v in entries.items() if v%p}
        if any(j < 0 or j >= n for j in clean):
            raise ValueError('index outside [0,N)')
        cost.support_checks += n
        def rec(m, d, co):
            co.node_size_sum += m
            if not d:
                co.output_writes+=m
                return [0]*m
            if m==1:
                co.output_writes+=1
                return [next(iter(d.values()))]
            even,odd = {},{}
            for j,v in d.items():
                if j&1: odd[j>>1]=v
                else: even[j>>1]=v
            co.split_entries+=len(d)
            h=m//2
            if not odd:
                e=rec(h,even,co)
                co.even_only_butterflies+=h
                co.output_writes+=m
                return e+e
            if not even:
                o=rec(h,odd,co)
                step=n//m
                y=[0]*m
                for k in range(h):
                    t=o[k]*powers[k*step]%p
                    y[k],y[k+h] = t,(-t)%p
                co.ntt_mults+=h
                co.ntt_negs+=h
                co.odd_only_butterflies+=h
                co.output_writes+=m
                return y
            e=rec(h,even,co)
            o=rec(h,odd,co)
            step=n//m
            y=[0]*m
            for k in range(h):
                t=o[k]*powers[k*step]%p
                y[k]=(e[k]+t)%p
                y[k+h]=(e[k]-t)%p
            co.ntt_mults+=h
            co.ntt_adds+=m
            co.full_butterflies+=h
            co.output_writes+=m
            return y
        return rec(n,clean,cost),cost

    def transform(self, v, cost: Optional[Cost]=None):
        if len(v)!=self.n: raise ValueError('wrong input size')
        return self.from_entries({j:z for j,z in enumerate(v) if z%self.p},cost)

    def direct_sparse(self,entries: dict[int,int],cost: Optional[Cost]=None):
        """K geometric phase streams: O(NK) arithmetic, attractive for K<=2."""
        if cost is None: cost=Cost()
        n,p=self.n,self.p
        cost.root_mults+=n-1
        cost.support_checks+=n
        y=[0]*n
        cost.output_writes+=n
        for j,v in entries.items():
            v=v%p
            if not v:continue
            alpha=self.powers[j]
            current=v
            for k in range(n):
                y[k]=(y[k]+current)%p
                cost.forward_direct_adds+=1
                current=current*alpha%p
                cost.forward_direct_mults+=1
                cost.output_writes+=1
        return y,cost


class CyclicSolver:
    """(diag + shift*S)^-1 on vectors; O(N) input-dependent field work."""
    def __init__(self, diag, shift, p=P0):
        self.diag=[a%p for a in diag]
        self.shift=shift%p
        self.p=p
        self.n=len(diag)
        self.invdiag=inv_all(self.diag,p)
        self.h=[]
        cur=1
        for u in self.invdiag:
            cur=(-self.shift*cur*u)%p
            self.h.append(cur)
        factor=(1-self.h[-1])%p
        if not factor: raise ValueError('singular cyclic recurrence')
        self.inv_factor=pow(factor,-1,p)

    def apply(self,x):
        if len(x)!=self.n: raise ValueError('wrong length')
        return [(self.diag[i]*x[i]+self.shift*x[(i-1)%self.n])%self.p
                for i in range(self.n)]

    def solve(self,rhs,cost: Optional[Cost]=None):
        if len(rhs)!=self.n: raise ValueError('wrong length')
        p=self.p
        z=[0]*self.n
        previous=0
        for i,(b,inv) in enumerate(zip(rhs,self.invdiag)):
            previous=((b-self.shift*previous)*inv)%p
            z[i]=previous
        c=z[-1]*self.inv_factor%p
        result=[(v+h*c)%p for v,h in zip(z,self.h)]
        if cost is not None:
            cost.solve_mults+=3*self.n+1
            cost.solve_adds+=2*self.n
            cost.output_writes+=2*self.n
        return result


class GreenSparse:
    def __init__(self,n,a=7,b=2,c=1,p=P0):
        self.n,self.a,self.b,self.c,self.p=n,a,b,c,p
        self.omega=primitive_root(n,p)
        self.powers=root_powers(n,self.omega,p)
        self.pruned=SparseInputDFT(n,self.omega,p)
        ld=[(a+c*self.powers[j])%p for j in range(n)]
        pd=[(a+b*self.powers[-j%n])%p for j in range(n)]
        self.L=CyclicSolver(ld,b,p)
        self.P=CyclicSolver(pd,c,p)

    def residual(self,x,cost: Optional[Cost]=None):
        v=self.P.apply(x)
        if cost is not None:
            cost.preconditioner_mults+=2*self.n
            cost.preconditioner_adds+=self.n
            cost.output_writes+=self.n
            cost.support_checks+=self.n
        return v

    def transform(self,x,method='auto'):
        co=Cost()
        r=self.residual(x,co)
        nz={j:a for j,a in enumerate(r) if a}
        if method=='auto': method='direct' if len(nz)<=2 else 'pruned'
        if method=='direct': forcing,_=self.pruned.direct_sparse(nz,co)
        elif method=='pruned': forcing,_=self.pruned.from_entries(nz,co)
        else: raise ValueError('method must auto, direct or pruned')
        return self.L.solve(forcing,co),{'K':len(nz),'method':method,'cost':co}

    def structured_dense(self,nonzero_entries):
        """Construct dense x=P^{-1}r from a sparse forcing residual r."""
        r=[0]*self.n
        for j,v in nonzero_entries.items(): r[j]=v%self.p
        return self.P.solve(r)


def direct_dft(x,omega,p=P0):
    """Independent O(N^2) reference, no pruned recursion or Green machinery."""
    n=len(x)
    out=[]
    for k in range(n):
        step=pow(omega,k,p)
        ph=1
        val=0
        for v in x:
            val=(val+v*ph)%p
            ph=ph*step%p
        out.append(val)
    return out


def candidate_library(n):
    return [GreenSparse(n,b=2,c=1),GreenSparse(n,b=1,c=2),
            GreenSparse(n,b=-2,c=1)]


def transform_adaptive(x, candidates=None):
    """Always exact. Test a constant-size bank of sparsifiers and identity.
    Cost for candidate scanning is charged even if the best one is identity.
    """
    n=len(x)
    if candidates is None: candidates=candidate_library(n)
    p=candidates[0].p
    roots=candidates[0].pruned
    best=[z%p for z in x]
    best_kind='identity'
    best_engine=None
    support_scans=n
    candidate_work=0
    for i,engine in enumerate(candidates):
        residual=engine.residual(x)
        candidate_work+=3*n
        support_scans+=n
        if sum(bool(z) for z in residual)<sum(bool(z) for z in best):
            best=residual
            best_engine=engine
            best_kind=f'green-{i}'
    nz={i:z for i,z in enumerate(best) if z}
    co=Cost()
    co.preconditioner_mults=candidate_work//3*2
    co.preconditioner_adds=candidate_work//3
    co.support_checks=support_scans
    co.output_writes=len(candidates)*n
    if len(nz)<=2: f,_=roots.direct_sparse(nz,co)
    else: f,_=roots.from_entries(nz,co)
    y=f if best_engine is None else best_engine.L.solve(f,co)
    return y,{'K':len(nz),'selected':best_kind,'cost':co}
