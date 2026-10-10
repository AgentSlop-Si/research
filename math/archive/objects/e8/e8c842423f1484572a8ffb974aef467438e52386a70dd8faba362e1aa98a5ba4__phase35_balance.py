"""Phase 35 — exact Fourier/Green balancing invariants and first-cross synthesis.

Pure Python finite-field audit. Positive control is a valid algebraic Fourier
factorization; Green controls are NOT exact FFTs. Green pair application takes
linear work including applying its transpose. Depends only on the bundled
phase33_two_sided helper (CyclicGreen + deterministic nonaffine cycles).
"""
from __future__ import annotations
import argparse
import json
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from random import Random
from phase33_two_sided import (P1, GEN1, P2, GEN2, CyclicGreen,
                               make_cycles, root_of_unity, inverse,
                               inverse_small, field_rank)


def transpose_cycle(cycle):
    return [cycle[0]] + list(reversed(cycle[1:]))


@dataclass
class GreenStage:
    greens: list[CyclicGreen]
    weights: list[int]
    def __post_init__(self):
        self.n = self.greens[0].n
        self.p = self.greens[0].p
        assert self.greens and len(self.weights)==len(self.greens)
        assert all(g.n == self.n and g.p == self.p for g in self.greens)
        self.tgreens=[CyclicGreen(transpose_cycle(g.cycle),g.alpha,self.p)
                      for g in self.greens]
        self.weights=[w%self.p for w in self.weights]
        self.mass=sum(w*inverse(1-g.alpha,self.p)
                      for w,g in zip(self.weights,self.greens))%self.p
        assert self.mass != 0

    def apply(self,x):
        assert len(x)==self.n
        out=[0]*self.n
        for w,g in zip(self.weights,self.greens):
            y=g.apply(x)
            for i in range(self.n): out[i]=(out[i]+w*y[i])%self.p
        return out

    def apply_transpose(self,x):
        out=[0]*self.n
        for w,g in zip(self.weights,self.tgreens):
            y=g.apply(x)
            for i in range(self.n): out[i]=(out[i]+w*y[i])%self.p
        return out

    def row_zero(self):
        e0=[1]+[0]*(self.n-1)
        return self.apply_transpose(e0)

    def col_zero(self):
        e0=[1]+[0]*(self.n-1)
        return self.apply(e0)


def make_stage(n,alphas,seed,p=P1,weights=None):
    cycles=make_cycles(n,len(alphas),seed)
    return GreenStage([CyclicGreen(c,a,p) for c,a in zip(cycles,alphas)],
                      weights if weights is not None else [1]*len(alphas))


def normalize_signature(v,mass,p):
    im=inverse(mass,p)
    return [x*im%p for x in v]


def signature_gate(A,B):
    """Necessary and sufficient for *both Fourier boundary vectors* to match.

    If true, returns a permutation in pullback convention: (P x)[i]=x[perm[i]],
    and the uniquely determined middle diagonal. This tests only the first
    Fourier row and column, NOT full Fourier correctness.
    """
    assert A.n == B.n and A.p == B.p
    n=A.n;p=A.p
    r=A.row_zero()
    c=B.col_zero()
    ra=normalize_signature(r,A.mass,p)
    cb=normalize_signature(c,B.mass,p)
    pools=defaultdict(list)
    for j,x in enumerate(cb):pools[x].append(j)
    perm=[]
    for x in ra:
        if not pools[x]:
            return {'possible':False,'mismatch_value':x,
                    'moment2_A':sum(z*z for z in ra)%p,
                    'moment2_B':sum(z*z for z in cb)%p}
        perm.append(pools[x].pop())
    if not all(r):
        return {'possible':False,'reason':'zero in A first row'}
    D=[inverse(B.mass*v%p,p) for v in r]
    return {'possible':True,'perm':perm,'diagonal':D,'row':r,
            'fingerprint':ra}


def apply_calibrated(A,B,gate,x):
    assert gate['possible']
    p=A.p
    y=B.apply(x)
    y=[gate['diagonal'][i]*y[gate['perm'][i]]%p for i in range(A.n)]
    return A.apply(y)


def transpose_calibrated(A,B,gate,x):
    assert gate['possible']
    p=A.p
    y=A.apply_transpose(x)
    y=[gate['diagonal'][i]*y[i]%p for i in range(A.n)]
    # P^T: (P z)_i=z[perm[i]]
    pty=[0]*A.n
    for i,j in enumerate(gate['perm']):pty[j]=y[i]
    return B.apply_transpose(pty)


def balanced_residual(A):
    """No inverse needed: A(1/A[first row]) must equal N*e0."""
    r=A.row_zero();p=A.p
    if any(z==0 for z in r):
        return {'possible':False,'zero_row_entries':sum(z==0 for z in r)}
    result=A.apply([inverse(v,p) for v in r])
    target=[A.n%p]+[0]*(A.n-1)
    return {'possible':result==target,
            'nonzero_coordinates':sum(a!=b for a,b in zip(result,target)),
            'leading_coordinate':result[0], 'expected':A.n%p}


def rowperm_transpose_stage(A,pull):
    """A transpose followed by row permutation: Bx=(A^T x)[pull[i]]."""
    class BTranspose:
        n=A.n
        p=A.p
        mass=A.mass
        def apply(self,x):
            y=A.apply_transpose(x)
            return [y[pull[i]] for i in range(A.n)]
        def apply_transpose(self,x):
            y=[0]*A.n
            for i,j in enumerate(pull): y[j]=x[i]
            return A.apply(y)
        def col_zero(self):
            return self.apply([1]+[0]*(A.n-1))
    return BTranspose()


def planted_control(n,seed=35100,p=P1,primitive=GEN1):
    alpha,beta=inverse(4,p),inverse(5,p)
    A=make_stage(n,[alpha,beta],seed,p)
    pull=list(range(n));Random(seed+n).shuffle(pull)
    B=rowperm_transpose_stage(A,pull)
    gate=signature_gate(A,B)
    assert gate['possible']
    e0=[1]+[0]*(n-1)
    seedout=apply_calibrated(A,B,gate,e0)
    seedrow=transpose_calibrated(A,B,gate,e0)
    assert seedout==[1]*n and seedrow==[1]*n
    allone=apply_calibrated(A,B,gate,[1]*n)
    w=root_of_unity(n,p,primitive)
    e1=[0,1]+[0]*(n-2)
    second=apply_calibrated(A,B,gate,e1)
    f1=[pow(w,i,p) for i in range(n)]
    bal=balanced_residual(A)
    invpull=[0]*n
    for i,j in enumerate(pull): invpull[j]=i
    return {'N':n,'prime':p,'n_greens':4,'online_complexity':'O(N) field operations',
            'first_row_and_column_exact':True,
            'balance_defect_coordinates':bal['nonzero_coordinates'],
            'second_column_mismatch_coordinates':sum(a!=b for a,b in zip(second,f1)),
            'allones_transform_mismatch_coordinates':sum(a!=b for a,b in zip(allone,[n%p]+[0]*(n-1))),
            'permutation_recovered_correctly':gate['perm']==invpull}


def independent_control(n,seed=3601,p=P1):
    A=make_stage(n,[inverse(4,p),inverse(5,p)],seed,p)
    B=make_stage(n,[inverse(7,p),inverse(11,p)],seed+1000,p)
    gate=signature_gate(A,B)
    bal=balanced_residual(A)
    return {'N':n,'prime':p,'B_signature_match':gate['possible'],
            'A_balanced':bal['possible'],
            'balance_defect_coordinates':bal.get('nonzero_coordinates'),
            'moment2_equal':gate['possible'] or gate['moment2_A']==gate['moment2_B']}


def hadamard4_positive_control(p=P1,primitive=GEN1):
    n=4;w=root_of_unity(n,p,primitive)
    A=[[1-2*int(i==j) for j in range(n)] for i in range(n)]
    A=[[v%p for v in row] for row in A]
    # A=J-2I, A^2=4I and row/col sums=2.
    D=[inverse(A[0][i],p) for i in range(n)]
    ADinv=[[(A[0][i]*A[i][j]*inverse(4,p))%p for j in range(n)] for i in range(n)]
    F=[[pow(w,i*j,p) for j in range(n)] for i in range(n)]
    B=[[sum(ADinv[i][k]*F[k][j] for k in range(n))%p
        for j in range(n)] for i in range(n)]
    C=[[sum(A[i][k]*D[k]*B[k][j] for k in range(n))%p
        for j in range(n)] for i in range(n)]
    assert C==F
    assert all(sum(row)%p==1 for row in B)
    assert all(sum(B[i][j] for i in range(n))%p==1 for j in range(n))
    AI=[[A[i][j]*inverse(4,p)%p for j in range(n)] for i in range(n)]
    assert all(A[0][i]*AI[i][0]%p==inverse(4,p) for i in range(n))
    return {'N':4,'prime':p,'exact_Fourier_factorization':True,
            'outer_stage_is_Green_sum':False,'right_stage_row_and_col_sums':1}


def analytic_weak_coupling_bound(rho):
    """Positive weighted average of Green resolvents with |alpha_s|<=rho."""
    assert 0 <= rho < Fraction(1,3)
    delta=rho/(1-rho)
    deviation=delta*delta/(1-delta)
    return {'rho':str(rho),'delta':str(delta),
            'diag_leverage_deviation_upper_bound':str(deviation),
            'diag_leverage_abs_lower_bound':str(1-deviation),
            'excludes_all_sizes_N_at_least_2':deviation<Fraction(1,2)}


def exact_individual_couplings_bound():
    # Specific phases used by the earlier expander construction.
    e=Fraction(1,2)*(Fraction(1,4)/Fraction(3,4)+Fraction(1,5)/Fraction(4,5))
    return {'normalized_perturbation_norm_upper':str(e),
            'leverage_defect_upper':str(e*e/(1-e)),
            'leverage_modulus_lower':str(1-e*e/(1-e))}


def audit():
    sizes=[8,16,32,64,128,256,512,1024,2048,4096]
    return {'phase':35,'theorem':'one-mask balanced Fourier iff outer seed projector has flat diagonal',
            'analytic':{'rho_one_quarter':analytic_weak_coupling_bound(Fraction(1,4)),
                        'specific_expander':exact_individual_couplings_bound()},
            'true_fourier_controls':[hadamard4_positive_control(p,g) for p,g in ((P1,GEN1),(P2,GEN2))],
            'planted_green_first_cross':[planted_control(n) for n in sizes],
            'independent_green_gate':[independent_control(n) for n in sizes],
            'second_prime_spotchecks':[independent_control(n,seed=3601,p=P2) for n in (8,32,128,512)]}


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',default='audit.json')
    args=ap.parse_args()
    out=audit();open(args.output,'w').write(json.dumps(out,indent=2)+'\n')
    for entry in out['planted_green_first_cross']:
        print('N={N} first row/col exact, next-column defects={second_column_mismatch_coordinates}, balanced defects={balance_defect_coordinates}, inferred permutation correct={permutation_recovered_correctly}'.format(**entry))
    print('wrote',args.output)
