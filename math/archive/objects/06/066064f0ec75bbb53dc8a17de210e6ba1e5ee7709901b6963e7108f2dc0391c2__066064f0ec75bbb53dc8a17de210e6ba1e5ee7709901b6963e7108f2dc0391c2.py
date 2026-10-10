#!/usr/bin/env python3
"""All-input algebraic identity verifier; deliberately uses M K-NTTs (NOT fast)."""
from __future__ import annotations
import json,random
from phase9_dense_cycle import P,exact_reference_dft,root_of_unity
from phase8_weyl_cycle import exact_ntt
from test_phase9 import matrix_rank_mod


def verify(n,m,seed,singularity=False):
    k=n//m;rng=random.Random(seed)
    wn=root_of_unity(n);wk=pow(wn,m,P);wi=pow(wk,P-2,P)
    tab=[pow(wn,j,P) for j in range(n)]
    x=[rng.randrange(P) for _ in range(n)]
    cols=[[x[b*m+t] for b in range(k)] for t in range(m)]
    # These M full K-FFTs are *explicitly* charged to the oracle/check,
    # and are the outstanding obstacle for an unrestricted input.
    f=[exact_ntt(v,wi) for v in cols]
    lam=[rng.randrange(1,P) for _ in range(k)]
    if singularity:
        lam[0]=1
        lam[1]=tab[(1+k)%n]
    e=[[ (f[t+1][ell]-lam[ell]*f[t][ell])%P for ell in range(k)]
       for t in range(m-1)]
    oracle=exact_reference_dft(x)
    singular_count=0
    checks=0
    for ell in range(k):
        for j in range(m):
            index=ell+j*k;z=tab[(-index)%n]
            r=lam[ell]*z%P
            den=(1-r)%P
            # Valid for all inputs, but H requires all fresh column spectra.
            H=0;zp=1;B=0
            for t in range(m-1):
                H=(H+e[t][ell]*zp)%P
                B=(B+e[t][ell]*pow(lam[ell],m-1-t,P))%P
                zp=zp*z%P
            if den:
                numerator=(f[0][ell]*(1-pow(r,m,P)) + z*H-pow(z,m,P)*B)%P
                value=numerator*pow(den,P-2,P)%P
                # Telescoping numerator is a second independent formulation.
                reduced=(f[0][ell]+z*H-lam[ell]*pow(z,m,P)*f[m-1][ell])%P
                assert numerator==reduced
            else:
                singular_count+=1
                value=(m*f[0][ell]+sum(
                    e[t][ell]*pow(z,t+1,P)*(m-1-t) for t in range(m-1)))%P
            direct=sum(f[t][ell]*pow(z,t,P) for t in range(m))%P
            assert direct==value==oracle[index]
            checks+=1
    rank=matrix_rank_mod([[e[t][ell] for t in range(m-1)] for ell in range(k)])
    return {'n':n,'k':k,'m':m,'seed':seed,'singularity_forced':singularity,
            'all_output_checks':checks,'singular_denominators':singular_count,
            'innovation_matrix_column_rank':rank,'maximum_possible_innovation_rank':m-1,
            'naive_full_K_NTTs_required_by_this_verifier':m,'identity_residuals':0}


def main():
    records=[]
    for k,m in [(8,4),(16,4),(16,8),(32,8),(64,8),(64,16)]:
        for seed in (10,27,51):
            records.append(verify(k*m,m,seed,singularity=seed==27))
    assert all(r['innovation_matrix_column_rank']==r['maximum_possible_innovation_rank']
               for r in records)
    summary={'tested_records':len(records),'output_equalities':sum(x['all_output_checks'] for x in records),
             'records':records,
             'no_asymptotic_claim':
             'Each all-input identity check computes M K-FFTs. This is an exact identity, not a sub-NlogN algorithm.'}
    open('UNIVERSAL_IDENTITY_AUDIT.json','w').write(json.dumps(summary,indent=2))
    print('ALL INPUTS UNIVERSAL RATIONAL IDENTITY PASSED')
    print('records:',len(records),'exact entries:',summary['output_equalities'])
    print('innovation matrix full column rank in all',len(records),'records')
    print('singular denominator cases:',sum(r['singular_denominators'] for r in records))

if __name__=='__main__':main()
