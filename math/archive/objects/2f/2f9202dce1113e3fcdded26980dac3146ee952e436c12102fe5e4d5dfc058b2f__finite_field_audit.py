"""Exact modular verification of the M-phase resolution-of-identity construction.

No SciPy/NumPy and no floating point. For several mixed-radix lengths, checks
EVERY input basis column and output frequency of the exact Fourier matrix,
using explicit finite-field roots and all M deterministic beta frames.
This is a finite certificate, NOT a general symbolic theorem.
"""
from __future__ import annotations
import json
import math
from pathlib import Path


def prime_factors(v:int)->list[int]:
    r=[];f=2
    while f*f<=v:
        if v%f==0:
            r.append(f)
            while v%f==0:v//=f
        f+=1
    if v>1:r.append(v)
    return r


def n_root(N:int,p:int)->int:
    if (p-1)%N:
        raise ValueError('N does not divide p-1')
    pf=prime_factors(p-1)
    gen=next(a for a in range(2,p)
             if all(pow(a,(p-1)//f,p)!=1 for f in pf))
    z=pow(gen,(p-1)//N,p)
    assert pow(z,N,p)==1 and all(pow(z,N//f,p)!=1 for f in prime_factors(N))
    return z


def phase_exp(g:int,M:int,a:int,beta:int,r:int,t:int)->int:
    return (a*(t*(t-1)//2) + (a*M*r+beta)*t)%g


def verify_case(N:int,p:int,M:int)->dict:
    g=N&-N;m=N//g;K=g//M
    assert K>=M and K*M==g
    z=n_root(N,p)
    zg=pow(z,m,p)
    a=[((2*s+1)%g) or 1 for s in range(m)]
    beta=[(3*s+1)%g for s in range(m)]
    # Check full rank-M local resolution of identity, all (u,v).
    local_checks=0
    for s in range(m):
        for r in range(K):
            for u in range(M):
                for v in range(M):
                    total=0
                    for t in range(M):
                        b=(beta[s]+t*K)%g
                        e=(phase_exp(g,M,a[s],b,r,v)-phase_exp(g,M,a[s],b,r,u))%g
                        total+=pow(zg,e,p)
                    assert total%p == (M if u==v else 0)
                    local_checks+=1
    # For each input e_n, do M projected-input Fourier transforms,
    # compare the complete N outputs with the direct primitive-root basis.
    entry_checks=0
    invM=pow(M,-1,p)
    for n in range(N):
        r=n//m//M;u=(n//m)%M;s=n%m
        for k in range(N):
            y=0
            for t in range(M):
                b=(beta[s]+t*K)%g
                p_u=phase_exp(g,M,a[s],b,r,u)
                for v in range(M):
                    e=(phase_exp(g,M,a[s],b,r,v)-p_u)%g
                    input_n=(r*M+v)*m+s
                    y+=pow(zg,e,p)*pow(z,(-k*input_n)%N,p)
            y=(y*invM)%p
            assert y==pow(z,(-k*n)%N,p), (N,p,M,k,n)
            entry_checks+=1
    # Mutation: wrong phase spacing must fail for M>1 (certifier not vacuous)
    corrupted=0
    if M>1:
        s=0;r=0;u=0;v=1
        val=0
        for t in range(M):
            b=(beta[s]+t*(K+1))%g
            e=(phase_exp(g,M,a[s],b,r,v)-phase_exp(g,M,a[s],b,r,u))%g
            val+=pow(zg,e,p)
        assert val%p!=0
        corrupted=1
    return {'N':N,'G':g,'odd_part':m,'M':M,'p':p,'primitive_Nth_root':z,
            'basis_entries_verified':entry_checks,'local_projector_entries_verified':local_checks,
            'corrupted_spacing_rejected':bool(corrupted)}


def main():
    cases=[(24,97,2),(40,641,2),(48,97,4),(80,641,4),(96,97,4),(160,641,4)]
    res=[verify_case(*p) for p in cases]
    out={'scope':'Exact finite-field all-basis check of tight M-state beta frame, not full general proof',
         'cases':res,'total_basis_entries':sum(x['basis_entries_verified'] for x in res),
         'total_local_entries':sum(x['local_projector_entries_verified'] for x in res)}
    (Path(__file__).parent/'FIELD_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
