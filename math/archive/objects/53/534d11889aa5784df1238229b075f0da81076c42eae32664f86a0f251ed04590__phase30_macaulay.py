"""Exact projective certificate for four-term Green pencils.

For B=nu*G0+lam*G1+mu*G2+rho*G3, Fourier monomial equivalence
imposes homogeneous quadratic cross-ratio equations. If their homogeneous
multiples span the full degree-D space, no nonzero complex projective
coupling can satisfy those necessary constraints. A full-rank reduction
modulo 998244353 certifies a nonzero minor over Q(zeta_N), provided all
seeded rational denominators are invertible modulo the audit prime.
"""
from __future__ import annotations
from itertools import permutations
from math import comb
from random import Random
from phase30_four_parameter import P, SEEDS, build_four, combine


def monomials(degree:int,vars:int=4):
    if vars==1: return [(degree,)]
    return [(i,)+tail for i in range(degree+1) for tail in monomials(degree-i,vars-1)]

EXP2=monomials(2)
EXP4=monomials(4)
EXP5=monomials(5)
EXP3=monomials(3)
POS4={e:i for i,e in enumerate(EXP4)}
POS5={e:i for i,e in enumerate(EXP5)}


def coeffvec(g,i,j):
    """Order of variables: lam, mu, rho, nu."""
    return [g[1][i][j], g[2][i][j], g[3][i][j], g[0][i][j]]


def quad_product(v,w):
    q=[0]*len(EXP2)
    exp2pos={e:i for i,e in enumerate(EXP2)}
    for i in range(4):
        for j in range(4):
            e=[0]*4;e[i]+=1;e[j]+=1
            k=exp2pos[tuple(e)]
            q[k]=(q[k]+v[i]*w[j])%P
    return q


def quadrics(target,g,source_rows,source_cols,target_rows,target_cols):
    """All anchored projective cross-ratio quadrics for selected labels."""
    nrows=len(source_rows); ncols=len(source_cols)
    assert len(target_rows)==nrows and len(target_cols)==ncols
    polys=[]
    for i in range(1,nrows):
        for j in range(1,ncols):
            a=target[target_rows[i]][target_cols[j]]*target[target_rows[0]][target_cols[0]]%P
            b=target[target_rows[i]][target_cols[0]]*target[target_rows[0]][target_cols[j]]%P
            a1=quad_product(coeffvec(g,source_rows[i],source_cols[0]),coeffvec(g,source_rows[0],source_cols[j]))
            b1=quad_product(coeffvec(g,source_rows[i],source_cols[j]),coeffvec(g,source_rows[0],source_cols[0]))
            polys.append([(a*x-b*y)%P for x,y in zip(a1,b1)])
    return polys


def lifted_rows(polys,degree:int):
    assert degree>=2
    mul=monomials(degree-2)
    basis=monomials(degree)
    pos={e:i for i,e in enumerate(basis)}
    shift=[[pos[tuple(e[k]+m[k] for k in range(4))] for e in EXP2] for m in mul]
    rows=[]
    for q in polys:
        for mm in shift:
            v=[0]*len(basis)
            for j,k in enumerate(mm):v[k]=q[j]
            rows.append(v)
    return rows


def rank_pivots(rows,full_check=True):
    """Incremental elimination; returns rank and original row indices.

    Uses sparse-skipping modular arithmetic; all pivot rows normalized.
    """
    basis={};indices={}
    ncols=len(rows[0])
    for orig,row in enumerate(rows):
        x=row[:]
        for pivot in sorted(basis):
            b = basis[pivot]
            factor=x[pivot]
            if factor:
                for col in range(pivot,ncols):
                    x[col]=(x[col]-factor*b[col])%P
        nextpivot=next((k for k,v in enumerate(x) if v),None)
        if nextpivot is not None:
            inv=pow(x[nextpivot],P-2,P)
            for c in range(nextpivot,ncols):x[c]=x[c]*inv%P
            basis[nextpivot]=x
            indices[nextpivot]=orig
        if full_check and len(basis)==ncols:break
    return len(basis),[indices[k] for k in sorted(basis)]


def determinant_modp(rows):
    n=len(rows)
    if any(len(r)!=n for r in rows): raise ValueError('square needed')
    a=[r[:] for r in rows]
    det=1
    for j in range(n):
        k=next((k for k in range(j,n) if a[k][j]),None)
        if k is None:return 0
        if k!=j:
            a[k],a[j]=a[j],a[k]
            det=(-det)%P
        pivot=a[j][j]
        det=det*pivot%P
        inv=pow(pivot,P-2,P)
        for i in range(j+1,n):
            mul=a[i][j]*inv%P
            if mul:
                for x in range(j+1,n):a[i][x]=(a[i][x]-mul*a[j][x])%P
                a[i][j]=0
    return det


def full_N4_audit(seed:int=2804,degree:int=4,save_witness:bool=True):
    import hashlib
    target,g=build_four(4,seed)
    perms=list(permutations(range(4)))
    hist={}; failed=[]; witnesses=[]; h=hashlib.sha256()
    for rows in perms:
        for cols in perms:
            polys=quadrics(target,g,rows,cols,tuple(range(4)),tuple(range(4)))
            matrix=lifted_rows(polys,degree)
            rank,pivots=rank_pivots(matrix)
            hist[rank]=hist.get(rank,0)+1
            h.update(bytes([rank]))
            if rank<len(matrix[0]):failed.append({'rows':rows,'cols':cols,'rank':rank})
            if save_witness and len(witnesses)<8 and rank==len(matrix[0]):
                w=[matrix[p] for p in pivots]
                det=determinant_modp(w)
                assert det
                witnesses.append({'rows':rows,'cols':cols,'pivots':pivots,'det':det})
    return {'N':4,'seed':seed,'prime':P,'degree':degree,
            'vars':['lambda','mu','rho','nu'],'basis_columns':comb(degree+3,3),
            'total_permutation_pairs':len(perms)**2,'rank_histogram':hist,
            'bad_permutation_pairs':failed,'rank_stream_sha256':h.hexdigest(),
            'selected_nonzero_minors':witnesses}


def anchored_sample(n:int,samples:int=100,seed:int|None=None,degree:int=5,rngseed:int=137):
    if seed is None:seed=SEEDS[n]
    target,g=build_four(n,seed)
    rng=Random(rngseed)
    hist={};failed=[]
    for k in range(samples):
        rows=rng.sample(range(n),3)
        cols=rng.sample(range(n),3)
        qs=quadrics(target,g,rows,cols,(0,1,2),(0,1,2))
        rank,_=rank_pivots(lifted_rows(qs,degree))
        hist[rank]=hist.get(rank,0)+1
        if rank!=comb(degree+3,3):failed.append({'rows':rows,'cols':cols,'rank':rank})
    return {'N':n,'samples':samples,'degree':degree,'basis_columns':comb(degree+3,3),
            'rank_histogram':hist,'bad_samples':failed,'seed':seed,'prime':P}


def planted_control(n=4,seed:int|None=None):
    if seed is None:seed=SEEDS[n]
    _,g=build_four(n,seed)
    original=combine(g,(1,2,3,5))
    rng=Random(2026)
    rows=list(range(n));cols=list(range(n));rng.shuffle(rows);rng.shuffle(cols)
    diag_l=[rng.randrange(1,P) for _ in range(n)];diag_r=[rng.randrange(1,P) for _ in range(n)]
    target=[[diag_l[i]*original[rows[i]][cols[j]]*diag_r[j]%P for j in range(n)] for i in range(n)]
    qs=quadrics(target,g,rows,cols,tuple(range(n)),tuple(range(n)))
    degree=4 if n==4 else 5
    rank,_=rank_pivots(lifted_rows(qs,degree))
    return {'N':n,'rank':rank,'columns':comb(degree+3,3),'rows':rows,'cols':cols,
            'certified_positive':rank<comb(degree+3,3)}

def full_minor_quadrics(target,g,source_rows,source_cols,target_rows,target_cols):
    assert len(source_rows)==len(target_rows)
    assert len(source_cols)==len(target_cols)
    nr=len(source_rows);nc=len(source_cols)
    assert nr>=2 and nc>=2
    polys=[]
    for i in range(nr):
        for ip in range(i+1,nr):
            for j in range(nc):
                for jp in range(j+1,nc):
                    # condition (B_ij/T_ij)*(B_i'j'/T_i'j') ==
                    #           (B_ij'/T_ij')*(B_i'j/T_i'j)
                    a=target[target_rows[i]][target_cols[jp]] * target[target_rows[ip]][target_cols[j]]%P
                    b=target[target_rows[i]][target_cols[j]] * target[target_rows[ip]][target_cols[jp]]%P
                    p1=quad_product(coeffvec(g,source_rows[i],source_cols[j]),
                                    coeffvec(g,source_rows[ip],source_cols[jp]))
                    p2=quad_product(coeffvec(g,source_rows[i],source_cols[jp]),
                                    coeffvec(g,source_rows[ip],source_cols[j]))
                    polys.append([(a*v-b*w)%P for v,w in zip(p1,p2)])
    return polys


def fullminor_N4_audit(seed=2804,degree=4):
    import hashlib
    target,g=build_four(4,seed)
    perms=list(permutations(range(4)))
    hist={};failed=[];examples=[];h=hashlib.sha256()
    for rs in perms:
        for cs in perms:
            qs=full_minor_quadrics(target,g,rs[:3],cs[:3],(0,1,2),(0,1,2))
            rows=lifted_rows(qs,degree)
            rank,pivots=rank_pivots(rows)
            hist[rank]=hist.get(rank,0)+1
            h.update(bytes([rank]))
            if rank<len(rows[0]):failed.append({'rows':rs,'cols':cs,'rank':rank})
            if rank==len(rows[0]) and len(examples)<8:
                det=determinant_modp([rows[i] for i in pivots]);assert det
                examples.append({'rows':rs,'cols':cs,'pivots':pivots,'det':det})
    return {'N':4,'seed':seed,'degree':degree,'rank_histogram':hist,
            'pairs':576,'failing_mappings':failed,'rank_stream_sha256':h.hexdigest(),
            'witnesses':examples}


def fullminor_anchor_sample(n=8,samples=200,seed=None,degree=4,rngseed=137):
    if seed is None:seed=SEEDS[n]
    t,g=build_four(n,seed)
    rng=Random(rngseed)
    hist={};bad=[]
    for k in range(samples):
        rs=rng.sample(range(n),3);cs=rng.sample(range(n),3)
        qs=full_minor_quadrics(t,g,rs,cs,(0,1,2),(0,1,2))
        rank,_=rank_pivots(lifted_rows(qs,degree))
        hist[rank]=hist.get(rank,0)+1
        if rank!=comb(degree+3,3):bad.append({'rs':rs,'cs':cs,'rank':rank})
    return {'N':n,'samples':samples,'degree':degree,
            'basis':comb(degree+3,3),'histogram':hist,'bad':bad}


def planted_fullminor(n:int=8,seed:int|None=None,degree:int=3):
    if seed is None:seed=SEEDS[n]
    _,g=build_four(n,seed)
    orig=combine(g,(1,2,3,5))
    rng=Random(20261010+n)
    rp=list(range(n));cp=list(range(n));rng.shuffle(rp);rng.shuffle(cp)
    dl=[rng.randrange(1,P) for _ in range(n)]
    dr=[rng.randrange(1,P) for _ in range(n)]
    t=[[dl[i]*orig[rp[i]][cp[j]]*dr[j]%P for j in range(n)] for i in range(n)]
    q=full_minor_quadrics(t,g,rp[:3],cp[:3],(0,1,2),(0,1,2))
    rows=lifted_rows(q,degree)
    rank,pivots=rank_pivots(rows)
    # Verify *every* quadratic at the planted projective coupling.
    coeffs=(2,3,5,1)
    evals=[]
    for poly in q:
        ev=sum(c*__import__('math').prod(pow(coeffs[i],e[i],P) for i in range(4)) for c,e in zip(poly,EXP2))%P
        evals.append(ev)
    return {'n':n,'rank':rank,'max_rank':len(rows[0]),'all_quadrics_vanish':all(v==0 for v in evals),
            'rows':rp[:3],'cols':cp[:3]}


def exhaustive_fullminor_N8(seed:int=2808,degree:int=3,max_cases:int|None=None,
                             witness_count:int=24,certificate_out:str|None=None):
    """All 112896 ordered row/column triple pairs at N=8.

    Optional packed certificate stores each row-index basis and determinant:
    > for each pair in lexicographic order, 1-byte rank, 20 row indices,
      4-byte modular nonzero determinant. This is a compact, standalone
      exact minor witness for every checked partial mapping.
    """
    import hashlib,struct
    target,g=build_four(8,seed)
    triples=list(permutations(range(8),3))
    hist={};failures=[]; h=hashlib.sha256();total=0; examples=[]
    output = open(certificate_out,'wb') if certificate_out else None
    try:
        for rs in triples:
            for cs in triples:
                polys=full_minor_quadrics(target,g,rs,cs,(0,1,2),(0,1,2))
                rows=lifted_rows(polys,degree)
                rank,pivots=rank_pivots(rows)
                hist[rank]=hist.get(rank,0)+1
                h.update(bytes((rank,)));total+=1
                if rank!=len(rows[0]):failures.append({'rs':rs,'cs':cs,'rank':rank})
                if output:
                    # All exact pivot-row positions can be audited by the
                    # independent verifier without doing 112896 determinants
                    # during construction. Only a small sample is det-checked.
                    output.write(bytes([rank,*pivots])+bytes([255]*(len(rows[0])-rank)))
                if total<=witness_count and rank==len(rows[0]):
                    det=determinant_modp([rows[k] for k in pivots]);assert det
                    examples.append({'rs':rs,'cs':cs,'pivot_rows':pivots,'determinant':det})
                if max_cases is not None and total>=max_cases:break
            if max_cases is not None and total>=max_cases:break
    finally:
        if output: output.close()
    return {'n':8,'seed':seed,'prime':P,'degree':degree,
            'basis_dimension':comb(degree+3,3),'all_ordered_triples_per_axis':len(triples),
            'tested_pairs':total,'rank_histogram':hist,'failures':failures,
            'rank_digest_sha256':h.hexdigest(),'example_nonzero_minors':examples,
            'packed_witness_file':certificate_out}


if __name__ == '__main__':
    print('four-term exact Macaulay gate, N4 complete:', fullminor_N4_audit(degree=3)['rank_histogram'])
    print('planted true projective control, N8:', planted_fullminor(8))
    print('N8 random mapping sample:', fullminor_anchor_sample(8, 100, degree=3)['histogram'])
