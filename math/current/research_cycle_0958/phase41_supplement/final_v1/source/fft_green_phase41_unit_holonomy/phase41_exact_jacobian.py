"""Exact mod-p certificates for the *real* Jacobian of unit-circle edge-gain controls.

Gaussian rational unit gains w=(a+i b)/(a-i b) have modulus exactly one over C.
A split-prime reduction of their rational real/imag Jacobian certifies a
nonzero determinant in characteristic zero when all denominators are units.
"""
from __future__ import annotations
import sys, json, random
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent.parent/'fft_green_phase40_four_middle'))
from phase40_holonomy import random_problem,normalize_gauge,weighted_green_apply
from phase40_local_synthesis import small_rank,det_mod

PRIMES=((998244353,3),(2013265921,31))

def chord_spec(n,seed=41000):
    rng=random.Random(seed+n)
    return [(rng.randrange(2,90),rng.randrange(2,90)) for _ in range(n+1)]

def sqrt_minus_one(p,primitive):
    return pow(primitive,(p-1)//4,p)

def dense_green(c,w,p):
    n=len(c);G=[[0]*n for _ in range(n)]
    for j in range(n):
        v=[0]*n;v[j]=1
        y=weighted_green_apply(c,w,v,p)
        for r in range(n):G[r][j]=y[r]
    return G

def log_jac(n,p,root,abcd,seed=40040,k=4,negate=False):
    c,raw = random_problem(n,p,seed)
    gauge=normalize_gauge(n,c,raw,p)
    assert len(abcd)==n+1
    K=root if not negate else (-root)%p
    weights=[1]*(2*n)
    for idx,(a,b) in zip(gauge['chord'],abcd):
        x=(a+b*K)%p;y=(a-b*K)%p
        assert y!=0
        weights[idx]=x*pow(y,p-2,p)%p
    ws=[weights[:n],weights[n:]]
    G=[dense_green(c[s],ws[s],p) for s in range(2)]
    M=[[(G[0][i][j]+G[1][i][j])%p for j in range(n)] for i in range(n)]
    assert all(M[i][j] for i in (0,1) for j in range(k+1))
    ans=[]
    for j in range(1,k+1):
        row=[]
        for idx in gauge['chord']:
            e=gauge['edges'][idx];u,v,s=e.source,e.target,e.cycle
            factor=K*weights[idx]%p
            def term(r,col):
                return factor*G[s][r][v]%p*G[s][u][col]%p*pow(M[r][col],p-2,p)%p
            row.append((term(0,j)+term(1,0)-term(1,j)-term(0,0))%p)
        ans.append(row)
    return ans, c, gauge['chord']

def real_jac(n,p,primitive,abcd,seed=40040,k=4):
    I=sqrt_minus_one(p,primitive)
    Jp,c,chords=log_jac(n,p,I,abcd,seed,k,False)
    Jm,c2,chords2=log_jac(n,p,I,abcd,seed,k,True)
    assert c==c2 and chords==chords2
    inv2=pow(2,p-2,p);inv2i=pow(2*I%p,p-2,p)
    JR=[[(x+y)*inv2%p for x,y in zip(a,b)] for a,b in zip(Jp,Jm)]
    JI=[[(x-y)*inv2i%p for x,y in zip(a,b)] for a,b in zip(Jp,Jm)]
    return JR+JI,c,chords

def independent_cols(A,p):
    out=[]
    for j in range(len(A[0])):
        trial=out+[j]
        B=[[r[c] for c in trial] for r in A]
        if small_rank(B,p)==len(trial):out=trial
        if len(out)==len(A):break
    return out

def exact_case(n,seed=41000,k=4):
    abcd=chord_spec(n,seed)
    matrix=[];graphs=None;chords=None
    for p,g in PRIMES:
        A,c,t=real_jac(n,p,g,abcd,k=k)
        matrix.append((p,A))
        if graphs is None:graphs=c;chords=t
        else:assert graphs==c and chords==t
    ranks={str(p):small_rank(A,p) for p,A in matrix}
    idx=independent_cols(matrix[0][1],matrix[0][0])
    assert len(idx)==k+2,(n,ranks,idx)
    A2=matrix[1][1]
    if small_rank([[r[j] for j in idx] for r in A2],matrix[1][0])<len(idx):
        # alternate matching index set from second field
        idx=independent_cols(A2,matrix[1][0])
    row_candidates=[[r[j] for j in idx] for r in matrix[0][1]]
    ridx=independent_cols(list(map(list,zip(*row_candidates))),matrix[0][0])
    assert len(ridx)==k+2
    for p,A in matrix:
        if small_rank([[A[r][j] for j in idx] for r in ridx],p)<k+2:
            rows=[[r[j] for j in idx] for r in A]
            ridx=independent_cols(list(map(list,zip(*rows))),p)
    dets={str(p):det_mod([[A[r][j] for j in idx] for r in ridx],p) for p,A in matrix}
    assert all(dets.values()),(n,dets)
    assert all(r==k+2 for r in ranks.values()),(n,ranks)
    return {'N':n,'target_ratios':k,'real_output_dimensions':2*k,
            'max_real_rank_proved':k+2,'real_jacobian_ranks':ranks,
            'unit_edge_gains':True,'tree_phase_edges':n-1,'chord_phase_edges':n+1,
            'common_minor_chord_positions':idx, 'common_minor_real_imag_rows':ridx,
            'common_minor_graph_edge_indices':[chords[j] for j in idx],
            'same_rational_gaussian_gains':True,'modular_determinants':dets,
            'cycle_orders':graphs,'unit_gain_numerators':abcd}

if __name__=='__main__':
    cases=[exact_case(n) for n in (8,16,32,64)]
    out=Path(__file__).with_name('phase41_unit_jacobian_certificates.json')
    out.write_text(json.dumps({'method':'unit-modulus gain, real k+2 rank bound, exact split-prime determinants','cases':cases},indent=2))
    for q in cases:
        print('N',q['N'],'ranks',q['real_jacobian_ranks'],'determinants',q['modular_determinants'], 'chords',q['common_minor_chord_positions'])
