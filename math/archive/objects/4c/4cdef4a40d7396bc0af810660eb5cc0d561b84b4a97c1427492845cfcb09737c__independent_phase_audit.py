#!/usr/bin/env python3
"""Independent modular witness reconstruction with exact structural-zero audit."""
from pathlib import Path
from itertools import combinations
from collections import Counter
import hashlib,json,time
HERE=Path(__file__).resolve().parent
SRC=HERE.parent.parent/'joint_orbit'/'iteration_6_phase_grid'/'PHASE_GRID_COMPATIBILITY.json'
P=97;Q=8;N=16;M=4
assert pow(Q,8,P)==P-1 and pow(Q,16,P)==1

def poly_power(e):
    k=e%16;v=[0]*8;v[k%8]=1 if k<8 else -1;return v

def path_polynomial(i,j,sgn):
    t,u=divmod(i,M);tt,uu=divmod(j,M);dt=t-tt;du=u-uu
    if min(dt,du)<0:return [0]*8
    out=[0]*8
    # Enumerate weighted lattice paths directly instead of solving any recurrence.
    for vertical in combinations(range(dt+du),dt):
        vset=set(vertical);col=uu;exponent=0
        for step in range(dt+du):
            if step in vset:exponent+=col
            else:col+=1
        for k,c in enumerate(poly_power(sgn*exponent)):out[k]+=c
    return out

def eval97(v):return sum(c*pow(Q,i,P) for i,c in enumerate(v))%P

def rev(j):
    out=0
    for k in range(4):out|=((j>>k)&1)<<(3-k)
    return out

def routed(A,s):
    pi=[(rev(j)+s)%N for j in range(N)]
    out=[[None]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):out[pi[i]][pi[j]]=A[i][j]
    return out
plus=[[path_polynomial(i,j,1) for j in range(N)] for i in range(N)]
minus=[[path_polynomial(i,j,-1) for j in range(N)] for i in range(N)]
rightJ=routed(minus,11);leftJ=routed(plus,7)
for A in [plus,minus]:
    for i in range(N):
        for j in range(N):
            structural=i//M>=j//M and i%M>=j%M
            assert any(A[i][j])==structural
            assert (eval97(A[i][j])!=0)==structural
support=[j for j in range(N) if any(minus[1][j]) or any(leftJ[1][j])]
assert support==[0,1,7,9,15]
G=[[eval97(v) for v in r] for r in plus];J=[[eval97(v) for v in r] for r in rightJ]
w=[eval97(poly_power(-j)) for j in range(N)]

def detmod(A):
    a=[list(r) for r in A];d=1;n=len(a)
    for col in range(n):
        pivot=next((k for k in range(col,n) if a[k][col]%P),None)
        if pivot is None:return 0
        if pivot!=col:a[col],a[pivot]=a[pivot],a[col];d=-d
        v=a[col][col]%P;d=d*v%P;iv=pow(v,-1,P)
        for r in range(col+1,n):
            factor=a[r][col]*iv%P
            if factor:
                a[r]=[(a[r][j]-factor*a[col][j])%P for j in range(n)]
    return d%P

def det_integer_bareiss(A):
    # Fraction-free integer determinant: independent arithmetic for resultants.
    a=[list(r) for r in A];n=len(a);sgn=1;previous=1
    for k in range(n-1):
        if a[k][k]==0:
            pivot=next((r for r in range(k+1,n) if a[r][k]),None)
            if pivot is None:return 0
            a[k],a[pivot]=a[pivot],a[k];sgn=-sgn
        v=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                numerator=v*a[i][j]-a[i][k]*a[k][j]
                assert numerator%previous==0
                a[i][j]=numerator//previous
        for i in range(k+1,n):a[i][k]=0
        previous=v
    return sgn*a[-1][-1]

def full_resultant(P1,P2):
    # Retain degree five even when affine leading coefficients vanish.
    d=len(P1)-1;S=[]
    for co in [P1,P2]:
        for shift in range(d):S.append([0]*shift+co[::-1]+[0]*(d-1-shift))
    return det_integer_bareiss(S)%P

def minor_coefficients(rs,cs):
    # Determinant multilinearity, 2^5 pure-row choices; no interpolation.
    coeff=[0]*6
    for mask in range(32):
        A=[[(J if (mask>>k)&1 else G)[r][j] for j in cs] for k,r in enumerate(rs)]
        A.append([w[j] for j in cs])
        degree=mask.bit_count();coeff[degree]=(coeff[degree]+detmod(A))%P
    return coeff

# Homogeneous endpoint and common-root controls.
assert full_resultant([1,0,0,0,0,0],[0,0,0,0,0,1])==P-1
assert full_resultant([1,1,0,0,0,0],[2,0,1,0,0,0])==0 # common infinity
assert full_resultant([P-1,0,0,0,0,1],[P-1,0,0,0,0,1])==0
assert det_integer_bareiss([[2,3],[5,7]])==-1

cert=json.loads(SRC.read_text());assert cert['left_row_structural_support']==support
assert cert['N']==N and cert['M']==M and cert['p']==P and cert['omega_mod_p']==Q
seen=set();counts=Counter();nonzero_residues=Counter();endpoint_degree_counts=Counter();start=time.time()
for ix,c in enumerate(cert['certificates']):
    rs=tuple(c['rows']);assert len(rs)==5 and rs==tuple(sorted(set(rs))) and all(0<=r<N for r in rs)
    assert rs not in seen;seen.add(rs)
    if 'missing' in c:
        j=c['missing'];assert 0<=j<N
        assert all(not any(A[r][j]) for A in (plus,rightJ) for r in rs)
        assert w[j]!=0;counts['exact_structural_missing_coordinate']+=1
    else:
        rebuilt=[]
        for n in [1,2]:
            cs=c[f'columns{n}'];assert len(cs)==6 and len(set(cs))==6 and all(0<=j<N for j in cs)
            coeff=minor_coefficients(rs,cs)
            assert coeff==c[f'minor{n}'],(rs,n,coeff,c[f'minor{n}'])
            rebuilt.append(coeff)
        res=full_resultant(*rebuilt)
        assert res==c['homogeneous_resultant_mod_p'] and res!=0
        nonzero_residues[res]+=1;counts['nonzero_homogeneous_resultant']+=1
        endpoint_degree_counts[str(tuple(bool(p[5]) for p in rebuilt))]+=1
    if ix%750==0:print('verified',ix,'seconds',round(time.time()-start,3),flush=True)
assert seen==set(combinations(range(N),5)) and len(seen)==4368
assert not cert['unresolved'] and cert['certified']==len(seen)
result={'source':str(SRC.relative_to(HERE.parent.parent)),'source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),
        'N':N,'p':P,'zeta_residue':Q,'cyclotomic_relation_verified':'8^8=-1 mod 97',
        'exact_left_row_union_support':support,'left_row_component_exact_vectors':{'G_minus':minus[1],'route7_G_plus':leftJ[1]},
        'all_five_row_subsets_verified':len(seen),'certificate_counts':dict(counts),
        'minor_method':'32 determinant-multilinearity row choices, not interpolation',
        'resultant_method':'10 by 10 fixed-degree Sylvester determinant by integer Bareiss, then mod 97',
        'leading_coefficient_patterns':dict(endpoint_degree_counts),'resultant_residue_histogram':dict(nonzero_residues),
        'missing_coordinate_method':'Exact integer cyclotomic path polynomials, not modular zeros',
        'complete_projective_coverage':True}
(HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['left_row_component_exact_vectors','resultant_residue_histogram']},indent=2))
