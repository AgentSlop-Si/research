"""Phase 32: exact partial Fourier synthesis by row-gauged, independently ordered cyclic Green solves.

All operations are exact in the field F_998244353. Nothing here is a
worst-case sub-NlogN FFT; this is partial-column interpolation only.

For k designated Fourier input columns and q=k or q=k+1 non-affine
Hamiltonian cycles, find nonzero row-by-row gauges L_s so that sum L_s G_s
agrees exactly with those k columns. Setup O(N q k^3), online O(Nq)
for fixed k.
"""
from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
from random import Random
from typing import Sequence
import argparse, json

P = 998244353
PRIMITIVE = 3


def inv(a:int)->int:
    a %= P
    if not a:raise ZeroDivisionError('zero')
    return pow(a,P-2,P)


def root_of_unity(n:int)->int:
    assert n > 0 and (n & (n-1))==0 and (P-1)%n==0
    return pow(PRIMITIVE,(P-1)//n,P)


def is_affine_cycle(cycle: Sequence[int])->bool:
    n=len(cycle)
    nxt=[0]*n
    for t,x in enumerate(cycle):nxt[x]=cycle[(t+1)%n]
    b=nxt[0]
    a=(nxt[1]-b)%n
    return all(nxt[i]==(a*i+b)%n for i in range(n))


@dataclass
class CyclicGreen:
    cycle:list[int]
    alpha:int
    def __post_init__(self):
        self.n=len(self.cycle)
        assert sorted(self.cycle)==list(range(self.n))
        self.alpha%=P
        if not self.alpha:raise ValueError('alpha=0')
        self.denom=inv(1-pow(self.alpha,self.n,P))
        self.position=[0]*self.n
        for t,x in enumerate(self.cycle):self.position[x]=t
        self.powers=[1]*self.n
        for t in range(1,self.n):self.powers[t]=self.powers[t-1]*self.alpha%P

    def entry(self,i:int,j:int)->int:
        return self.powers[(self.position[i]-self.position[j])%self.n]*self.denom%P

    def apply(self,x:Sequence[int])->list[int]:
        assert len(x)==self.n
        accumulator=0
        for j in self.cycle:
            accumulator=(x[j]+self.alpha*accumulator)%P
        carry=accumulator*self.denom%P
        y=[0]*self.n
        for j in self.cycle:
            carry=(x[j]+self.alpha*carry)%P
            y[j]=carry
        return y


def solve2(A:list[list[int]],b:list[int],c:list[int])->tuple[list[int],list[int]]:
    """Solve A x=b and A z=c simultaneously for a small square matrix."""
    n=len(A)
    aug=[[*(t%P for t in A[i]),b[i]%P,c[i]%P] for i in range(n)]
    for t in range(n):
        pivot=next((r for r in range(t,n) if aug[r][t]),None)
        if pivot is None: raise ValueError('singular interpolation minor')
        aug[t],aug[pivot]=aug[pivot],aug[t]
        scale=inv(aug[t][t]);aug[t]=[v*scale%P for v in aug[t]]
        for r in range(n):
            if r==t:continue
            a=aug[r][t]
            if a:aug[r]=[(v-a*w)%P for v,w in zip(aug[r],aug[t])]
    return [aug[r][n] for r in range(n)],[aug[r][n+1] for r in range(n)]


def modular_rank(A:Sequence[Sequence[int]])->int:
    b=[list(map(lambda x:x%P,row)) for row in A]
    if not b:return 0
    R=len(b);C=len(b[0]);r=0
    for col in range(C):
        pivot=next((i for i in range(r,R) if b[i][col]),None)
        if pivot is None:continue
        b[r],b[pivot]=b[pivot],b[r]
        z=inv(b[r][col]);b[r]=[v*z%P for v in b[r]]
        for i in range(r+1,R):
            factor=b[i][col]
            if factor:
                b[i]=[(v-factor*w)%P for v,w in zip(b[i],b[r])]
        r+=1
        if r==R:break
    return r


class InterpolatedGreen:
    """O(qN) exact online operator fitting k Fourier columns, q=k or k+1."""
    def __init__(self,n:int,columns:Sequence[int],seed:int=320031,allow_affine:bool=False,extra:int=0):
        assert extra in (0,1)
        self.extra=extra
        self.n=n;self.columns=tuple(columns);self.k=len(self.columns);self.q=self.k+extra
        assert n>=self.q and len(set(self.columns))==self.k
        assert min(self.columns)>=0 and max(self.columns)<n
        rng=Random(seed+n*17+self.k)
        self.rng=rng
        self.root=root_of_unity(n)
        self.greens=[]
        used=set()
        successor_maps=[]
        for s in range(self.q):
            for _ in range(10000):
                cycle=list(range(n));rng.shuffle(cycle)
                successor=[0]*n
                for t,j in enumerate(cycle):successor[j]=cycle[(t+1)%n]
                key=tuple(successor)
                if key in used or (not allow_affine and is_affine_cycle(cycle)):continue
                # A stronger experimental control: chosen cycle matrices do not
                # commute pairwise (not required by the interpolation theorem).
                if any(all(successor[other[x]]==other[successor[x]] for x in range(n))
                       for other in successor_maps):continue
                used.add(key);successor_maps.append(successor);break
            else:raise ValueError('not enough distinct nonaffine cycles')
            self.greens.append(CyclicGreen(cycle,2))
        # Keep cycles, resample independent algebraic parameters until all
        # per-row kxk minors are invertible (equivalently, null vector full support).
        for attempt in range(50):
            for s,g in enumerate(self.greens):
                while True:
                    alpha=rng.randrange(2,P-1)
                    if pow(alpha,n,P)!=1:break
                g.__init__(g.cycle,alpha)
            try:
                gauges=self._build_gauges()
                self.gauges=gauges
                self.parameter_resamples=attempt
                break
            except ValueError:
                continue
        else:raise ValueError('failed to find admissible generic Green parameters')

    def response(self,i:int)->list[list[int]]:
        return [[g.entry(i,j) for g in self.greens] for j in self.columns]

    def _build_gauges(self)->list[list[int]]:
        n=self.n;k=self.k
        gauges=[[0]*n for _ in range(self.q)]
        for i in range(n):
            response=self.response(i)
            a=[row[:k] for row in response]
            rhs=[pow(self.root,(-i*j)%n,P) for j in self.columns]
            if self.extra==0:
                # Square q=k system. Cramer's rule generically gives a
                # fully nonzero solution whenever all target entries are nonzero.
                values,_=solve2(a,rhs,[0]*k)
                if not all(values):raise ValueError('gauge zero: resample couplings')
            else:
                # q=k+1: the extra null direction lets us avoid zero gauges.
                x0,shift=solve2(a,rhs,[-row[k]%P for row in response])
                if any(v==0 for v in shift):raise ValueError('zero component in null vector')
                for t in range(1,k+5):
                    values=[(x0[s]+t*shift[s])%P for s in range(k)]+[t]
                    if all(values):break
                else:raise ValueError('cannot obtain invertible output gauges')
            assert all(sum(response[j][s]*values[s] for s in range(self.q))%P == rhs[j] for j in range(k))
            for s in range(self.q):gauges[s][i]=values[s]
        return gauges

    def apply(self,x:Sequence[int])->list[int]:
        assert len(x)==self.n
        out=[0]*self.n
        for s,g in enumerate(self.greens):
            v=g.apply(x)
            gauge=self.gauges[s]
            for i in range(self.n):out[i]=(out[i]+gauge[i]*v[i])%P
        return out

    def entry(self,i:int,j:int)->int:
        return sum(self.gauges[s][i]*g.entry(i,j) for s,g in enumerate(self.greens))%P

    def expected_fourier_entry(self,i:int,j:int)->int:
        return pow(self.root,(-i*j)%self.n,P)

    def fingerprint(self)->str:
        h=sha256()
        for g in self.greens:
            h.update(str((g.cycle,g.alpha)).encode())
        for gate in self.gauges:h.update(str(gate).encode())
        return h.hexdigest()


def reference_ntt(x:list[int])->list[int]:
    n=len(x);root=root_of_unity(n);a=x[:];j=0
    for i in range(1,n):
        bit=n>>1
        while j & bit:j ^= bit;bit>>=1
        j ^= bit
        if i<j:a[i],a[j]=a[j],a[i]
    sz=2
    while sz<=n:
        wlen=pow(root,-n//sz,P)
        for start in range(0,n,sz):
            w=1
            for i in range(start,start+sz//2):
                u=a[i];v=a[i+sz//2]*w%P
                a[i]=(u+v)%P;a[i+sz//2]=(u-v)%P
                w=w*wlen%P
        sz*=2
    return a


def audit(n:int,k:int=5,seed:int=320031,extra:int=0):
    # Columns deliberately nonconsecutive once n>=8.
    columns=tuple(range(k))
    assert max(columns)<n
    m=InterpolatedGreen(n,columns,seed,extra=extra)
    for j in columns:
        e=[0]*n;e[j]=1
        v=m.apply(e)
        assert all(v[i]==m.expected_fourier_entry(i,j) for i in range(n))
    # Exact online Fourier comparison on a fresh dense random vector.
    rng=Random(9000+n+k)
    vec=[rng.randrange(P) for _ in range(n)]
    actual=m.apply(vec);reference=reference_ntt(vec)
    mismatch=sum(a!=b for a,b in zip(actual,reference))
    assert mismatch>0,'accidental complete transform -- investigate!'
    # Strong column counterexample: select first unused input basis column.
    j=next(j for j in range(n) if j not in columns)
    probe=m.apply([int(t==j) for t in range(n)])
    mismatch_col=sum(probe[i]!=m.expected_fourier_entry(i,j) for i in range(n))
    assert mismatch_col>0
    # Phase 20 full Weyl equations on random vector, direct sparse shifts/phase operators.
    # Here reference F Z=D F: Z e_j=e_(j+1); D_j=omega^{-j}; our exact inverse root convention means
    # D_j=omega^{-j}, consistent with F_(i,j+1)=omega^{-i} F_(i,j).
    zvec=[vec[(i-1)%n] for i in range(n)]
    def phase(x):return [x[i]*pow(m.root,-i%n,P)%P for i in range(n)]
    x1=m.apply(zvec)
    x2=phase(actual)
    weyl_mismatch=sum(u!=v for u,v in zip(x1,x2))
    assert weyl_mismatch>0
    # Check independent non-affine pairwise-noncommuting cycle operators,
    # and invertibility of every output diagonal gate.
    assert all(not is_affine_cycle(g.cycle) for g in m.greens)
    succ=[]
    for g in m.greens:
        nxt=[0]*n
        for t,j in enumerate(g.cycle):nxt[j]=g.cycle[(t+1)%n]
        assert all(any(nxt[oth[x]]!=oth[nxt[x]] for x in range(n)) for oth in succ)
        succ.append(nxt)
    assert all(all(v!=0 for v in gate) for gate in m.gauges)
    return {'N':n,'interpolated_columns':columns,'greens':m.q,
            'parameter_resamples':m.parameter_resamples,
            'basis_columns_exact':len(columns),
            'out_of_sample_basis_column':j,
            'out_of_sample_column_mismatches':mismatch_col,
            'dense_input_mismatches':mismatch,
            'Weyl_shift_defect_nonzeros':weyl_mismatch,
            'fingerprint_sha256':m.fingerprint()}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--sizes',nargs='+',type=int,default=[8,16,32,64,128,256])
    p.add_argument('--k',type=int,default=5)
    p.add_argument('--extra',type=int,choices=[0,1],default=0)
    p.add_argument('--output',default=None)
    args=p.parse_args()
    results=[audit(n,args.k,extra=args.extra) for n in args.sizes]
    text=json.dumps(results,indent=2)
    print(text)
    if args.output:
        with open(args.output,'w') as fh:fh.write(text+'\n')

if __name__=='__main__':main()
