"""Exact characteristic-zero Jacobian certificates for THREE unit-phase Green
cycles, reaching full real rank 2(N-1) for *all* two-row projective ratios.
Uses rational Gaussian circle parameters and two split-prime images.
"""
from __future__ import annotations
from pathlib import Path
import json,random
from phase41_three_cycle import graph
from phase41_exact_jacobian import dense_green,PRIMES,sqrt_minus_one,independent_cols
from phase40_local_synthesis import small_rank,det_mod

def gaussian_spec(n,seed=41003):
    rng=random.Random(n+seed)
    return [(rng.randrange(2,100),rng.randrange(2,100)) for _ in range(2*n+1)]

def compute_jac(n,p,primitive,spec,negative=False):
    c,edges,chords=graph(n)
    assert len(spec)==len(chords)==2*n+1
    iota=sqrt_minus_one(p,primitive)
    I=(-iota)%p if negative else iota
    weights=[1]*(3*n)
    for idx,(a,b) in zip(chords,spec):
        den=(a-b*I)%p
        assert den!=0
        weights[idx]=(a+b*I)*pow(den,p-2,p)%p
    G=[dense_green(c[s],weights[s*n:(s+1)*n],p) for s in range(3)]
    M=[[(G[0][r][j]+G[1][r][j]+G[2][r][j])%p for j in range(n)] for r in range(2)]
    assert all(z!=0 for row in M for z in row)
    inv=[[pow(z,p-2,p) for z in row] for row in M]
    J=[]
    for j in range(1,n):
        row=[]
        for idx in chords:
            e=edges[idx];g=G[e.cycle];u,v=e.source,e.target
            factor=I*weights[idx]%p
            def term(r,k):return factor*g[r][v]%p*g[u][k]%p*inv[r][k]%p
            row.append((term(0,j)+term(1,0)-term(1,j)-term(0,0))%p)
        J.append(row)
    return J,c,chords

def real_jac(n,p,g,spec):
    Jp,c,ch=compute_jac(n,p,g,spec,False)
    Jm,c2,ch2=compute_jac(n,p,g,spec,True)
    assert c==c2 and ch==ch2
    i=sqrt_minus_one(p,g)
    inv2=pow(2,p-2,p);inv2i=pow(2*i%p,p-2,p)
    JR=[[(a+b)*inv2%p for a,b in zip(r,s)] for r,s in zip(Jp,Jm)]
    JI=[[(a-b)*inv2i%p for a,b in zip(r,s)] for r,s in zip(Jp,Jm)]
    return JR+JI,c,ch

def certify(n):
    spec=gaussian_spec(n)
    mats=[];orders=None;chords=None
    for p,g in PRIMES:
        A,c,ch=real_jac(n,p,g,spec)
        mats.append((p,A))
        if orders is None:orders=c;chords=ch
        else:assert orders==c and chords==ch
    ranks={str(p):small_rank(A,p) for p,A in mats}
    target=2*(n-1)
    assert all(rank==target for rank in ranks.values()),(n,ranks)
    sel=independent_cols(mats[0][1],mats[0][0])
    assert len(sel)==target
    dets={str(p):det_mod([[row[j] for j in sel] for row in A],p) for p,A in mats}
    if not all(dets.values()):
        # select a different minor over second prime; both ranks still prove dominance
        sel=independent_cols(mats[1][1],mats[1][0])
        dets={str(p):det_mod([[row[j] for j in sel] for row in A],p) for p,A in mats}
    assert all(dets.values()),(n,dets)
    return {'N':n,'unit_phase_edges':3*n,'common_gauge_phase_redundancy':n-1,
            'independent_phase_holonomies':2*n+1,
            'two_row_complex_ratios':n-1,'target_real_dimensions':target,
            'exact_real_jacobian_rank':ranks,
            'common_nonzero_minor_columns':sel,
            'nonzero_minor_mod_two_primes':dets,
            'same_integer_gain_spec':True,
            'cycle_orders':orders,'gaussian_rational_unit_gain_ab':spec}

if __name__=='__main__':
    cases=[]
    for n in (8,16,32,64):
        data=certify(n);cases.append(data)
        print('N',n,'rank',data['exact_real_jacobian_rank'], 'det',data['nonzero_minor_mod_two_primes'],flush=True)
    Path(__file__).with_name('phase41_three_cycle_certificates.json').write_text(json.dumps({'cases':cases},indent=2))
