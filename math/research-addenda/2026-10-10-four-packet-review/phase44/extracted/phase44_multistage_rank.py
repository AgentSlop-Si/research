"""Exploratory exact real Jacobian ranks for multi-stage Green products.

Architecture: S_(d-1) D_(d-2) ... D_0 S_0; every S is the sum of
three gauge-fixed unit-edge Hamiltonian-cycle Green resolvents; each D is
an independent arbitrary nonzero complex diagonal modulo global scalar.

All calculation uses prime-field residues of rational Gaussian evaluations.
No Fourier-target existence is implied by a full rank result.
"""
from __future__ import annotations
import json,random,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
PHASE42=ROOT.parent/'fft_green_phase42_three_row'
sys.path.insert(0,str(PHASE42))
from phase42_product_jacobian import setup,matmul
from phase41_three_cycle import graph
from phase41_exact_jacobian import PRIMES,sqrt_minus_one


def specs(n,depth):
    rng=random.Random(44099+n+depth*71)
    result=[]
    for layer in range(depth):
        cycles,edges,chords=graph(n,seed=44321+997*layer)
        ab=[(rng.randrange(2,500),rng.randrange(2,500)) for _ in chords]
        result.append((cycles,edges,chords,ab))
    return result


def mm(A,B,p):return matmul(A,B,p)

def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]

def diag_right(M,diag,p):return [[v*diag[j]%p for j,v in enumerate(row)] for row in M]

def diag_left(diag,M,p):return [[v*diag[i]%p for v in row] for i,row in enumerate(M)]


def diag_data(n,depth,p,I):
    d=[]
    for ell in range(depth-1):
        v=[1]
        for k in range(1,n):
            a=19+((k*17+ell*11)%151)
            b=23+((k*13+ell*23)%149)
            c=(a+b*I)%p*pow((a-b*I)%p,-1,p)%p
            numer=3+((k*7+ell*5)%23)
            denom=4+((k*5+ell*3)%17)
            c=c*numer%p*pow(denom,-1,p)%p
            v.append(c)
        d.append(v)
    return d


def field_log_jacobian(n,depth,p,primitive,params,negative):
    layers,I=setup(n,p,primitive,params,negative)
    D=diag_data(n,depth,p,I)
    S=[layer[1] for layer in layers]
    R=[eye(n)]*depth
    R[0]=eye(n)
    for l in range(depth-1):R[l+1]=diag_left(D[l],mm(S[l],R[l],p),p)
    L=[eye(n)]*depth
    L[-1]=eye(n)
    for l in reversed(range(depth-1)):
        L[l]=diag_right(mm(L[l+1],S[l+1],p),D[l],p)
    M=mm(S[-1],R[-1],p)
    assert all(M[i][j] for i in range(n) for j in range(n))
    minv=[[pow(v,-1,p) for v in row] for row in M]
    nr=(n-1)*(n-1)
    rows=[[] for _ in range(nr)]
    def add_derivative(col,row,factor):
        c0=col[0]%p;u0=row[0]%p
        t00=(c0*u0*factor*minv[0][0])%p
        for r in range(1,n):
            tr0=(col[r]*u0*factor*minv[r][0])%p
            for j in range(1,n):
                trj=(col[r]*row[j]*factor*minv[r][j])%p
                t0j=(c0*row[j]*factor*minv[0][j])%p
                rows[(r-1)*(n-1)+j-1].append((trj+t00-t0j-tr0)%p)
    # All cycle phases, in layer-major order.
    for ell,(gs,Sell,w,edges,chords) in enumerate(layers):
        for idx in chords:
            e=edges[idx];g=gs[e.cycle]
            gcol=[g[k][e.target] for k in range(n)]
            col=[sum(L[ell][r][k]*gcol[k] for k in range(n))%p for r in range(n)]
            row=[sum(g[e.source][k]*R[ell][k][j] for k in range(n))%p for j in range(n)]
            add_derivative(col,row,I*w[idx]%p)
    # Diagonal interstage phases and log-amplitudes, ordered in pairs per interstage.
    for ell in range(depth-1):
        left=mm(L[ell+1],S[ell+1],p)
        right=mm(S[ell],R[ell],p)
        for mode in ('phase','amplitude'):
            for k in range(1,n):
                factor=D[ell][k]*(I if mode=='phase' else 1)%p
                add_derivative([left[r][k] for r in range(n)],right[k],factor)
    expected=depth*(2*n+1)+2*(depth-1)*(n-1)
    assert all(len(row)==expected for row in rows)
    return rows


def real_rank(n,depth,p,primitive):
    params=specs(n,depth)
    A=field_log_jacobian(n,depth,p,primitive,params,False)
    B=field_log_jacobian(n,depth,p,primitive,params,True)
    I=sqrt_minus_one(p,primitive)
    inv2=pow(2,-1,p)
    inv2i=pow(2*I%p,-1,p)
    J=np.array([[(a+b)*inv2%p for a,b in zip(ar,br)] for ar,br in zip(A,B)]+[
       [(a-b)*inv2i%p for a,b in zip(ar,br)] for ar,br in zip(A,B)],dtype=np.int64)
    return fast_rank(J,p)


def fast_rank(A,p):
    """Exact elimination with vectorized modular row updates; no int64 overflow."""
    A=A.copy().astype(np.int64);nrow,ncol=A.shape
    rank=0
    for c in range(ncol):
        nz=np.flatnonzero(A[rank:,c])
        if len(nz)==0:continue
        pivot=rank+int(nz[0]);A[[rank,pivot]]=A[[pivot,rank]]
        pv=pow(int(A[rank,c]),-1,p)
        for k in range(rank+1,nrow):
            if A[k,c]:
                factor=int(A[k,c])*pv%p
                # Products and subtraction lie inside signed int64 range for p <= 2^31.
                A[k,c:]=(A[k,c:]-factor*A[rank,c:])%p
        rank+=1
        if rank==nrow:break
    return rank


def certify(n,depth):
    nvar=depth*(2*n+1)+2*(depth-1)*(n-1)
    nrow=2*(n-1)**2
    records=[]
    for p,g in PRIMES:
        rank=real_rank(n,depth,p,g)
        records.append({'prime':p,'rank':rank,'max_possible':min(nrow,nvar)})
    return {'N':n,'layers':depth,'Greens_per_layer':3,
          'phase_edge_parameters':depth*(2*n+1),
          'interstage_complex_parameters':2*(depth-1)*(n-1),
          'total_real_parameters':nvar,'full_projective_target_dimension':nrow,
          'records':records,'maximal_rank_over_R_certified':all(rec['rank']==min(nrow,nvar) for rec in records),
          'exact_Fourier_target_existence':False}

if __name__=='__main__':
    cases=[]
    for n,d in ((8,2),(8,3),(8,4)):
        result=certify(n,d)
        print('n=',n,'depth=',d,'nvar=',result['total_real_parameters'],'ranks=',result['records'],flush=True)
        cases.append(result)
    (ROOT/'phase44_multistage_rank_audit.json').write_text(json.dumps({'cases':cases},indent=2)+'\n')
