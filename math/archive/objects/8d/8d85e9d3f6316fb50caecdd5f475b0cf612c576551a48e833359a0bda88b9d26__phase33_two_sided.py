"""Phase 33: exact two-sided Hamiltonian Green/Fourier gates.

Self-contained; Python stdlib only. No asymptotic FFT breakthrough claimed.
The two-resolvent certificate is a *necessary* condition for full two-sided
Fourier equality. All field calculations are exact.
"""
from __future__ import annotations
from dataclasses import dataclass
from random import Random
from typing import Sequence
from math import sqrt
import argparse, json

P1, GEN1 = 998244353, 3
P2, GEN2 = 2013265921, 31


def inverse(a: int, p: int) -> int:
    a %= p
    if a == 0: raise ZeroDivisionError('zero in field')
    return pow(a, p - 2, p)


def root_of_unity(n: int, p: int, primitive: int) -> int:
    assert n > 1 and n & (n-1) == 0 and (p-1) % n == 0
    w = pow(primitive, (p-1)//n, p)
    assert pow(w, n, p) == 1 and pow(w, n//2, p) != 1
    return w


def is_affine_cycle(cycle: Sequence[int]) -> bool:
    n = len(cycle)
    nxt = [0]*n
    for k,x in enumerate(cycle): nxt[x] = cycle[(k+1)%n]
    a=(nxt[1]-nxt[0])%n
    return all(nxt[i] == (a*i+nxt[0])%n for i in range(n))


def make_cycles(n: int, q: int, seed: int = 330033) -> list[list[int]]:
    rng = Random(seed + n*17)
    cycles = []; maps = []
    for s in range(q):
        for attempt in range(10000):
            cyc=list(range(n));rng.shuffle(cyc)
            if is_affine_cycle(cyc): continue
            succ=[0]*n
            for t,j in enumerate(cyc): succ[j]=cyc[(t+1)%n]
            if succ in maps: continue
            if any(all(succ[old[x]] == old[succ[x]] for x in range(n)) for old in maps): continue
            cycles.append(cyc);maps.append(succ);break
        else: raise RuntimeError('could not draw nonaffine noncommuting cycles')
    return cycles


@dataclass
class CyclicGreen:
    cycle: list[int]
    alpha: int
    p: int = P1
    def __post_init__(self):
        self.n=len(self.cycle)
        assert sorted(self.cycle)==list(range(self.n))
        self.alpha%=self.p
        assert self.alpha and pow(self.alpha,self.n,self.p)!=1
        self.denom=inverse(1-pow(self.alpha,self.n,self.p), self.p)
        self.pos=[0]*self.n
        for k,i in enumerate(self.cycle):self.pos[i]=k
        self.powers=[1]*self.n
        for k in range(1,self.n): self.powers[k]=self.powers[k-1]*self.alpha%self.p

    def entry(self,i:int,j:int)->int:
        return self.powers[(self.pos[i]-self.pos[j])%self.n]*self.denom%self.p

    def apply(self,x:Sequence[int])->list[int]:
        assert len(x)==self.n
        acc=0
        for j in self.cycle:
            acc=(x[j]+self.alpha*acc)%self.p
        carry=acc*self.denom%self.p
        out=[0]*self.n
        for j in self.cycle:
            carry=(x[j]+self.alpha*carry)%self.p
            out[j]=carry
        return out


def determinant(A:Sequence[Sequence[int]],p:int)->int:
    B=[[x%p for x in row] for row in A]
    n=len(B);ans=1
    for c in range(n):
        row=next((r for r in range(c,n) if B[r][c]),None)
        if row is None:return 0
        if row!=c:B[c],B[row]=B[row],B[c];ans=(-ans)%p
        z=B[c][c];ans=ans*z%p;zi=inverse(z,p)
        for r in range(c+1,n):
            factor=B[r][c]*zi%p
            if factor:
                for j in range(c,n):B[r][j]=(B[r][j]-factor*B[c][j])%p
    return ans


def field_rank(A:Sequence[Sequence[int]],p:int)->int:
    B=[[x%p for x in row] for row in A]
    if not B:return 0
    nrow=len(B);ncol=len(B[0]);r=0
    for c in range(ncol):
        pr=next((i for i in range(r,nrow) if B[i][c]),None)
        if pr is None:continue
        B[pr],B[r]=B[r],B[pr]
        z=inverse(B[r][c],p)
        for i in range(r+1,nrow):
            fac=B[i][c]*z%p
            if fac:
                for j in range(c,ncol):B[i][j]=(B[i][j]-fac*B[r][j])%p
        r+=1
        if r==nrow:break
    return r


def first_three_column_certificate(n:int,cycles:list[list[int]],p:int,primitive:int,
                                   alphas:tuple[int,int]=(3,5)) -> dict:
    g,h=[CyclicGreen(cycles[s],alphas[s],p) for s in range(2)]
    w=root_of_unity(n,p,primitive)
    K=[]
    for i in range(n):
        A,C,E=(g.entry(i,j) for j in range(3))
        B,D,H=(h.entry(i,j) for j in range(3))
        f1=pow(w,(-i)%n,p);f2=pow(w,(-2*i)%n,p)
        # Det [[A,B,1], [a*C,b*D,f1], [c*E,d*H,f2]] = K[i] .
        # [a*d, b*c, a, b, c, d].
        K.append([C*H%p,-D*E%p, -B*C*f2%p,A*D*f2%p,
                  B*E*f1%p,-A*H*f1%p])
    K=[[v%p for v in row] for row in K]
    rank=field_rank(K,p)
    witness=[];det=0
    if rank==6:
        # Build a lexicographic independent row set, then independently validate.
        for i,row in enumerate(K):
            if field_rank([K[k] for k in witness]+[row],p)>len(witness):witness.append(i)
            if len(witness)==6:break
        det=determinant([K[i] for i in witness],p)
        assert det
    return {'N':n,'prime':p,'rank':rank,'pivots':witness,'determinant_mod_p':det,
            'alphas':list(alphas), 'cycles':cycles, 'nonaffine':all(not is_affine_cycle(c) for c in cycles)}


def solve(A:Sequence[Sequence[int]],b:Sequence[int],p:int)->list[int]:
    n=len(A);assert len(b)==n
    B=[[int(v)%p for v in A[i]]+[int(b[i])%p] for i in range(n)]
    for k in range(n):
        pivot=next((i for i in range(k,n) if B[i][k]),None)
        if pivot is None:raise ValueError('singular')
        B[k],B[pivot]=B[pivot],B[k]
        z=inverse(B[k][k],p)
        B[k]=[x*z%p for x in B[k]]
        for i in range(n):
            if i==k:continue
            f=B[i][k]
            if f:B[i]=[(x-f*y)%p for x,y in zip(B[i],B[k])]
    return [B[i][-1] for i in range(n)]


def inverse_small(A:Sequence[Sequence[int]],p:int)->list[list[int]]:
    n=len(A)
    B=[[v%p for v in A[i]] + [int(i==j) for j in range(n)] for i in range(n)]
    for k in range(n):
        pivot=next((i for i in range(k,n) if B[i][k]),None)
        if pivot is None:raise ValueError('singular')
        B[k],B[pivot]=B[pivot],B[k]
        z=inverse(B[k][k],p);B[k]=[x*z%p for x in B[k]]
        for i in range(n):
            if i==k:continue
            f=B[i][k]
            if f:B[i]=[(x-f*y)%p for x,y in zip(B[i],B[k])]
    return [row[n:] for row in B]


def setup_left_gauges(greens:Sequence[CyclicGreen],columns:Sequence[int],p:int,primitive:int):
    n=greens[0].n;q=len(greens);assert len(columns)==q
    w=root_of_unity(n,p,primitive)
    gauges=[[0]*n for _ in range(q)]
    for i in range(n):
        A=[[g.entry(i,j) for g in greens] for j in columns]
        b=[pow(w,(-i*j)%n,p) for j in columns]
        x=solve(A,b,p)
        if not all(x):raise ValueError('zero left gauge')
        for s in range(q):gauges[s][i]=x[s]
    return gauges


def extra_column_extension(n:int,q:int=5,seed:int=320031,p:int=P1,
                           primitive:int=GEN1)->dict:
    assert n>q
    cycles=make_cycles(n,q,seed)
    alphas=[7+2*s for s in range(q)]
    greens=[CyclicGreen(c,alpha,p) for c,alpha in zip(cycles,alphas)]
    columns=list(range(q))
    left=setup_left_gauges(greens,columns,p,primitive)
    w=root_of_unity(n,p,primitive)
    jstar=q
    A=[[left[s][i]*greens[s].entry(i,jstar)%p for s in range(q)] for i in range(q)]
    b=[pow(w,(-i*jstar)%n,p) for i in range(q)]
    v=solve(A,b,p)
    assert all(v)
    mismatches=0;pred=[]
    for i in range(n):
        y=sum(left[s][i]*greens[s].entry(i,jstar)*v[s] for s in range(q))%p
        pred.append(y)
        if y!=pow(w,(-i*jstar)%n,p):mismatches+=1
    assert all(pred[i]==b[i] for i in range(q))
    return {'N':n,'q':q,'matched_whole_columns':q,'extra_column_exact_rows':q,
            'extra_column_mismatched_rows':mismatches,
            'right_gauge_extra_column':v}


def q_column_tangent(n:int,q:int=5,seed:int=320031,p:int=P1,
                     primitive:int=GEN1) -> dict:
    assert n>q
    cycles=make_cycles(n,q,seed)
    greens=[CyclicGreen(c,7+2*s,p) for s,c in enumerate(cycles)]
    left=setup_left_gauges(greens,list(range(q)),p,primitive)
    w=root_of_unity(n,p,primitive)
    J=[];resid=[];mismatch=0
    for i in range(n):
        B=[[g.entry(i,j) for g in greens] for j in range(q)]
        BI=inverse_small(B,p)
        h=[g.entry(i,q) for g in greens]
        z=[sum(h[s]*BI[s][ell] for s in range(q))%p for ell in range(q)]
        l=[left[s][i] for s in range(q)]
        y=sum(h[s]*l[s] for s in range(q))%p
        f=pow(w,(-i*q)%n,p)
        mismatch+=int(f!=y)
        dr=[]
        for ell in range(1,q):
            for s in range(q):dr.append((-z[ell]*B[ell][s]*l[s])%p)
        dr.extend(h[s]*l[s]%p for s in range(q))
        J.append(dr);resid.append((f-y)%p)
    rank=field_rank(J,p)
    augmented=field_rank([row+[v] for row,v in zip(J,resid)],p)
    return {'N':n,'q':q,'parameter_dimension':q*q,'jacobian_rank':rank,
            'rank_with_residual':augmented,'missing_column_mismatch':mismatch}


def phase17_bound(n:int,q:int)->dict:
    # Valid for cyclic Hamiltonian Green solves, regardless of coupling and both gauges.
    m=n//(1<<q) if q < n.bit_length() else 0
    rank_cap=q
    exact_ruled_out = (m*m > q*n)
    err=0.0
    if m>q and exact_ruled_out:
        err=sqrt((m*m/n-q)/(m-q))
    return {'N':n,'q':q,'guaranteed_common_group_size':m,
            'fourier_rank_lower':m*m/n,'green_rank_upper':rank_cap,
            'exact_Fourier_ruled_out':exact_ruled_out,
            'normalized_DFT_spectral_error_floor':err}


def audit():
    results={'two_green':[],'five_green_tangent':[], 'five_green_extension':[], 'asymptotic':[]}
    for n in [8,16,32,64,128,256,512,1024]:
        cycles=make_cycles(n,2)
        for p,g in [(P1,GEN1),(P2,GEN2)]:
            item=first_three_column_certificate(n,cycles,p,g)
            # Keep huge cycles in implementation but omit from human-friendly JSON.
            item.pop('cycles')
            results['two_green'].append(item)
    for n in [32,64,128,256,1024]:
        results['five_green_tangent'].append(q_column_tangent(n))
    for n in [8,16,32,64,128,256,1024]:
        results['five_green_extension'].append(extra_column_extension(n))
    for q in range(2,7):
        n=1 << ((q*(4**q)).bit_length())
        results['asymptotic'].append(phase17_bound(n,q))
    return results

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',default=None)
    args=parser.parse_args()
    result=audit()
    output=json.dumps(result,indent=2)
    if args.output:
        with open(args.output,'w') as f:f.write(output+'\n')
    else:print(output)
