#!/usr/bin/env python3
"""Reconstruct the data certificate; never execute or import the producer's code."""
from pathlib import Path
from itertools import combinations, permutations
from math import comb
from collections import Counter
import hashlib, json
import sympy as sp
HERE=Path(__file__).resolve().parent
SRC=HERE.parent/'joint_orbit'/'iteration_5_shifted_grid'/'TWO_ROW_CERTIFICATES.json'
z,x=sp.symbols('z x'); phi=sp.Poly(z**8+1,z,domain=sp.ZZ)
def residue(expr):
    return sp.Poly(expr,z,domain=sp.ZZ).rem(phi).as_expr()
def power(j):
    return residue(z**(j%16))
def decode(vec):
    assert len(vec)==8 and all(isinstance(a,int) for a in vec)
    return sum(a*z**i for i,a in enumerate(vec))
def encode(expr):
    p=sp.Poly(residue(expr),z); return [int(p.nth(i)) for i in range(8)]
def sign(p):
    return (-1)**sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))
def ring_determinant(A):
    n=len(A); out=0
    for p in permutations(range(n)):
        term=sign(p)
        for i,j in enumerate(p): term=residue(term*A[i][j])
        out=residue(out+term)
    return out

def sylvester_resultant(P,Q):
    # Build a Sylvester matrix, independent of the producer's quadratic formula.
    while P and P[-1]==0:P=P[:-1]
    while Q and Q[-1]==0:Q=Q[:-1]
    assert P and Q
    m,n=len(P)-1,len(Q)-1
    A=[]
    for k in range(n): A.append([0]*k+P[::-1]+[0]*(n-1-k))
    for k in range(m): A.append([0]*k+Q[::-1]+[0]*(m-1-k))
    return ring_determinant(A)

def reverse(j,bits):
    out=0
    for _ in range(bits):out=2*out+(j&1);j//=2
    return out

def green(M,a,b):
    N=M*M
    def entry(i,j):
        dt=i//M-j//M;du=i%M-j%M
        return comb(dt+du,dt)*a**dt*b**du if min(dt,du)>=0 else 0
    return [[entry(i,j) for j in range(N)] for i in range(N)]
G=green(4,2,3);J0=green(4,5,7)
route=[(reverse(j,4)+1)%16 for j in range(16)]
inv=[route.index(i) for i in range(16)]
J=[[J0[inv[i]][inv[j]] for j in range(16)] for i in range(16)]
f=[power(-j) for j in range(16)]
def minor(rows,cols):
    r,s=rows
    A=sp.Matrix([[G[r][j]+x*J[r][j] for j in cols],
                 [G[s][j]+x*J[s][j] for j in cols],
                 [f[j] for j in cols]])
    p=sp.Poly(sp.expand(A.det()),x)
    return [residue(p.nth(k)) for k in range(3)]
def compare_polynomial(P,stored):
    assert [encode(c) for c in P]==stored

# Direct arithmetic controls, in addition to checking every stored resultant.
assert residue(power(7)*power(7))==power(14)
assert sylvester_resultant([-z,1],[-z**2,0,1])==0
assert sylvester_resultant([-z,1],[-z**2,1])!=0
assert sylvester_resultant([2],[3,1])==2
assert sylvester_resultant([-1,0,1],[-4,0,1])==9
assert sp.Poly(phi.as_expr(),z).is_irreducible
cert=json.loads(SRC.read_text()); assert cert['route']==route
seen=set(); kinds=Counter(); finite_kinds=Counter(); records=[]
for c in cert['certificates']:
    pair=tuple(c['rows']);assert pair in set(combinations(range(16),2)) and pair not in seen
    seen.add(pair);kinds[c['kind']]+=1
    if c['kind']=='missing_coordinate':
        j=c['column'];assert all(A[r][j]==0 for A in (G,J) for r in pair)
        assert f[j]!=0
        records.append({'rows':pair,'kind':c['kind'],'verified':True});continue
    assert c['kind']=='algebraic_certificate'
    v=c['finite'];finite_kinds[v['kind']]+=1
    if v['kind']=='nonzero_constant_minor':
        P=minor(pair,v['columns']);compare_polynomial(P,v['polynomial'])
        assert P[0]!=0 and P[1]==P[2]==0
    else:
        assert v['kind']=='nonzero_resultant'
        P=minor(pair,v['columns1']);Q=minor(pair,v['columns2'])
        compare_polynomial(P,v['polynomial1']);compare_polynomial(Q,v['polynomial2'])
        res=sylvester_resultant(P,Q)
        assert encode(res)==v['resultant'] and res!=0
    inf=c['infinity'];P=minor(pair,inf['columns'])
    assert encode(P[2])==inf['minor_value'] and P[2]!=0
    # A separately formed determinant must match the leading coefficient.
    rows=[[J[pair[0]][j] for j in inf['columns']],
          [J[pair[1]][j] for j in inf['columns']],
          [f[j] for j in inf['columns']]]
    assert ring_determinant(rows)==P[2]
    records.append({'rows':pair,'kind':c['kind'],'finite_kind':v['kind'],'verified':True})
assert seen==set(combinations(range(16),2))
assert G[1]==[3,1]+[0]*14 and J[1]==[0,1]+[0]*14
# Structural support is completely dense after two stages, yet the span gate excludes F.
H=[[G[i][j]+J[i][j] for j in range(16)] for i in range(16)]
assert all(sum(H[i][k]*H[k][j] for k in range(16))>0 for i in range(16) for j in range(16))
# Verify inherited seal without executing its verification program.
old=HERE.parent/'review_orbits_iteration3'
seal=json.loads((old/'SEAL.json').read_text())
seal_verified=[]
for c in seal['files']:
    data=(old/c['path']).read_bytes()
    assert len(data)==c['bytes'] and hashlib.sha256(data).hexdigest()==c['sha256']
    seal_verified.append(c['path'])
result={'source':str(SRC),'source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),
        'field':'Q[z]/(z^8+1), independently verified irreducible',
        'matrix_reconstruction':'Closed binomial path formula, bitwise permutation',
        'resultant_reconstruction':'Full Sylvester determinant, reduced modulo z^8+1',
        'N':16,'route':route,'all_row_pairs_verified':len(seen),
        'certificate_kinds':dict(kinds),'finite_certificate_kinds':dict(finite_kinds),
        'projective_infinity_certificates_verified':kinds['algebraic_certificate'],
        'left_row_1':'3 alpha e_0 + (alpha+beta) e_1',
        'positive_H_squared_full_support':True,'prior_sealed_files_verified':seal_verified,
        'records':records}
(HERE/'CERTIFICATE_AUDIT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
