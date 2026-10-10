#!/usr/bin/env python3
from pathlib import Path
from itertools import permutations,product
import json,hashlib
import sympy as s
HERE=Path(__file__).resolve().parent
SRC=HERE.parent.parent/'joint_orbit/iteration_6_phase_grid/SMALL_BLOCK_RESULTS.json'
I=s.I

def grid_inverse(b,a,c,d):
    U=s.eye(4);U[1,0]=-b;U[2,0]=-a;U[3,1]=-c;U[3,2]=-d
    return U.inv()

def permuted(A,rp,cp):
    out=s.zeros(4)
    for i in range(4):
        for j in range(4):out[rp[i],cp[j]]=A[i,j]
    return out
A=s.diag(s.Rational(1,2),-I,1,-I/2)*grid_inverse(I,1,-2,-2*I)
B=permuted(s.diag(-I/2,-2,-2,s.Rational(1,2))*grid_inverse(s.Rational(1,2),-I/2,2,2),[3,2,1,0],[3,1,2,0])
C=s.diag((1+I)/2,1,1,3)*s.Matrix([[int(j==3-i) for j in range(4)] for i in range(4)])
F=s.Matrix([[(-I)**(r*c) for c in range(4)] for r in range(4)])
assert (A+B+C-F).applyfunc(s.simplify)==s.zeros(4)
source=json.loads(SRC.read_text())
for name,X in [('A',A),('B',B),('C',C)]:
    # Stringified exact data comparison, with no evaluation of source expressions.
    assert [[str(v) for v in X.row(r)] for r in range(4)]==source[name]
assert all(s.simplify(X.det())!=0 for X in [A,B,C])

# Independent support cover enumeration, deriving support from the product order.
S={(i,j) for i,j in product(range(4),repeat=2) if i//2>=j//2 and i%2>=j%2}
allcoords=set(product(range(4),repeat=2));covers=[]
for rp in permutations(range(4)):
    for cp in permutations(range(4)):
        T={(rp[i],cp[j]) for i,j in S}
        if S|T==allcoords:
            overlap=S&T;assert overlap=={(0,0),(3,3)}
            covers.append({'row_route':list(rp),'column_route':list(cp),'overlap':[list(x) for x in sorted(overlap)]})
assert covers==source['all_two_term_structural_covers'] and len(covers)==2

# Verify the exact endpoint-diagonal invariant symbolically.
a,b,c,d=s.symbols('a b c d');L=s.symbols('L0:4',nonzero=True);R=s.symbols('R0:4',nonzero=True)
X=s.diag(*L)*grid_inverse(b,a,c,d)*s.diag(*R)
assert s.cancel(X[3,0]-X[3,1]*X[1,0]/X[1,1]-X[3,2]*X[2,0]/X[2,2])==0
unique=[(3,0),(3,1),(1,0),(1,1),(3,2),(2,0),(2,2)]
assert all(pos in S and pos not in {(0,0),(3,3)} for pos in unique)
permuted_target_controls=0;ratios=set()
for rp in permutations(range(4)):
    for cp in permutations(range(4)):
        T=F.extract(rp,cp)
        u=s.simplify(T[3,1]*T[1,0]/(T[1,1]*T[3,0]))
        v=s.simplify(T[3,2]*T[2,0]/(T[2,2]*T[3,0]))
        assert s.simplify(1-u-v)!=0
        ratios.add((str(u),str(v)));permuted_target_controls+=1
roots=[1,I,-1,-I]
assert all(s.simplify(1-u-v)!=0 for u,v in product(roots,repeat=2))

# Full standard-FFT embedding control, independently form bit-wise butterflies.
B0=s.zeros(4);B1=s.zeros(4)
for i in range(4):
    B0[i,i]=(-1)**(i&1);B0[i,i^1]=1
    B1[i,i]=(-1)**((i>>1)&1);B1[i,i^2]=1
P=s.zeros(4)
for i in range(4):P[i,((i&1)<<1)|(i>>1)]=1
assert B1*s.diag(1,1,1,-I)*B0*P==F

# The all-size quadrant theorem uses a symbolic determinant and exact geometry.
z,Q=s.symbols('z Q')
D=s.Matrix([[1,1,1],[1,Q,z],[1,1,Q]]).det()
assert s.factor(D)==(Q-1)**2
geometric_controls=[]
for m in range(4,65):
    n=m*m;rows=[3*m+3,2*m+3,3*m+2];cols=[0,1,m]
    def admits(row,col,st,su):
        t,u=divmod(row,m);tt,uu=divmod(col,m)
        return st*(t-tt)>=0 and su*(u-uu)>=0
    for row in rows:
        for col in cols:
            assert admits(row,col,1,1)
            assert all(not admits(row,col,st,su) for st,su in [(-1,1),(1,-1),(-1,-1)])
    # Primitive m^2 root has omega^m of exact order m.
    assert m>1 and m<n
    geometric_controls.append({'m':m,'N':n,'isolated_3_by_3_rectangle':True})
# Exact cyclotomic determinant nonzero for representative dyadic/nondyadic sizes.
cyclotomic_controls=[]
for m in [4,5,6,7,8,9,10,12,16]:
    phi=s.Poly(s.cyclotomic_poly(m*m,z),z)
    residue=s.Poly((z**m-1)**2,z).rem(phi)
    assert not residue.is_zero
    cyclotomic_controls.append({'m':m,'N':m*m,'cyclotomic_degree':phi.degree(),'determinant_remainder_nonzero':True})
result={'source':str(SRC.relative_to(HERE.parent.parent)),'source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),
        'F4_three_green_sum_exact':True,'component_determinants':[str(s.simplify(X.det())) for X in [A,B,C]],
        'all_relative_support_covers':covers,'two_term_invariant_symbolically_verified':True,
        'permuted_F4_targets_tested':permuted_target_controls,'observed_root_ratio_pairs':[list(x) for x in sorted(ratios)],
        'standard_two_stage_F4_embedding_verified':True,
        'quadrant_coefficient_determinant':'(Q-1)^2, Q=omega^m',
        'quadrant_exact_geometric_controls':geometric_controls,
        'quadrant_cyclotomic_controls':cyclotomic_controls,
        'scope':'Four-point additive minimum three; four native quadrant-oriented terms fail for every integer m>=4. No product-of-sums or arbitrary-route exclusion.'}
(HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['quadrant_exact_geometric_controls','observed_root_ratio_pairs']},indent=2))
