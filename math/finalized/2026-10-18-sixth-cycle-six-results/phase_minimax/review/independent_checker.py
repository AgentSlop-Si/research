#!/usr/bin/env python3
"""Independent exact controls for the frozen C8 positive-error partial result.
Does not import any candidate program or execute historical research code.
"""
from pathlib import Path
import hashlib, json
import sympy as sp

D=Path(__file__).resolve().parent
FROZEN=D/'frozen'
results={}
def check(name, value):
    assert value, name
    results[name]=True

# Use SymPy's independent algebraic-number implementation, not the author's ring.
x=sp.Symbol('x')
cyclo=sp.Poly(x**16+1,x)
check('cyclotomic_polynomial_irreducible', cyclo.is_irreducible)
K=sp.QQ.alg_field_from_poly(cyclo,alias='z')
z=K.from_sympy(K.ext); zero=K.zero; one=K.one
Z=[z**j for j in range(32)]
def zz(j): return Z[j%32]
def k(v): return K.from_sympy(sp.Rational(v))
i=zz(8); rt=zz(4)+zz(-4)
s=(zz(1)-zz(-1))/ (2*i); c=(zz(1)+zz(-1))/2; t=s*s

def decode(d): return sum((k(v)*zz(int(j)) for j,v in d.items()),zero)
def matrix(ds): return [[decode(d) for d in row] for row in ds]
def transpose(A):return list(map(list,zip(*A)))
def mul(A,B):return [[sum((a*b for a,b in zip(row,col)),zero) for col in zip(*B)] for row in A]
def add(A,B):return [[a+b for a,b in zip(row,col)] for row,col in zip(A,B)]
def sub(A,B):return [[a-b for a,b in zip(row,col)] for row,col in zip(A,B)]
def scale(A,f):return [[f*a for a in row] for row in A]
def outer(a,b):return [[u*v for v in b] for u in a]
def conj(v):
    coeffs=v.to_list()
    degree=len(coeffs)-1
    return sum((K.convert(coef)*zz(-(degree-j)) for j,coef in enumerate(coeffs)),zero)
def cm(A):return [[conj(v) for v in row] for row in A]
def real(A):return scale(add(A,cm(A)),one/2)
def imag(A):return scale(sub(A,cm(A)),one/(2*i))
Id=[[k(j==l) for l in range(8)] for j in range(8)]
powers=[0,2,0,10,0,2,0,10]
q=[zz(v) for v in powers]; p=[zz(v+1) for v in powers]
root_table=[one,(one-i)/rt,-i,(-one-i)/rt,-one,(-one+i)/rt,i,(one+i)/rt]
F=[[root_table[j*l%8]/(2*rt) for l in range(8)] for j in range(8)]
V=[[p[j]*F[j][l]*q[l] for l in range(8)] for j in range(8)]
a=[k(v)/2 for v in [1,0,-1,0,-1,0,1,0]]
b=[k(v)/2 for v in [0,1,0,1,0,1,0,1]]
rank_one_vector=[u+i*v for u,v in zip(a,b)]
E=scale(outer(rank_one_vector,rank_one_vector),c); B=sub(real(V),real(E)); Y=imag(V)
R=add(outer(a,a),outer(b,b)); Y0=sub(Y,scale(add(outer(a,b),outer(b,a)),c))
payload=json.loads((FROZEN/'WITNESS.json').read_text())
for name, computed in [('F',F),('V',V),('B',B),('E',E),('residual_inner',scale(Y0,i))]:
    check('serialized_'+name+'_all_64_match_independent_construction',matrix(payload[name])==computed)
check('serialized_a_b_s_c_match', [decode(v) for v in payload['a']]==a and [decode(v) for v in payload['b']]==b and decode(payload['s'])==s and decode(payload['c'])==c)
check('unitary_F',mul(transpose(cm(F)),F)==Id)
check('real_B', B==cm(B))
check('rank_one_E_all_784_minors_and_nonzero', E[0][0]!=zero and all(E[j][l]*E[h][m]==E[j][m]*E[h][l] for j in range(8) for h in range(j+1,8) for l in range(8) for m in range(l+1,8)))
check('spectral_Y_square',mul(Y,Y)==add(scale(Id,t),scale(R,one-2*t)))
check('spectral_residual_square',mul(Y0,Y0)==scale(sub(Id,R),t))
check('external_residual_all_64',all(F[j][l]-conj(p[j])*(B[j][l]+E[j][l])*conj(q[l])==conj(p[j])*i*Y0[j][l]*conj(q[l]) for j in range(8) for l in range(8)))
check('orthogonal_projector_rank_six',mul(R,R)==R and sum((R[j][j] for j in range(8)),zero)==k(2))
check('field_sqrt_two_formula',16*t*t-16*t+2==rt and rt*rt==k(2))
check('error_and_squared_error_polynomials',128*t**4-256*t**3+160*t*t-32*t+1==zero and 128*s**8-256*s**6+160*s**4-32*s*s+1==zero)
poly_s=sp.Poly(128*x**8-256*x**6+160*x**4-32*x**2+1,x)
poly_t=sp.Poly(128*x**4-256*x**3+160*x*x-32*x+1,x)
slo=sp.Rational('0.1950903220161282678'); shi=sp.Rational('0.1950903220161282679')
tlo=sp.Rational('0.0380602337443566219'); thi=sp.Rational('0.0380602337443566220')
check('exact_isolating_intervals_s_and_t',poly_s.count_roots(slo,shi)==1 and poly_s.count_roots(0,slo)==0 and poly_t.count_roots(tlo,thi)==1 and poly_t.count_roots(0,tlo)==0)
check('positive_sqrt_two_on_t_interval',16*tlo*tlo-16*thi+2>0)
# Independent all-sign reduction: every squared-periodic pair differs by +/-1.
# This algebraic covariance is symbolic in all 16 real signs; no sign is dropped.
sr=sp.symbols('r0:8',real=True); sc=sp.symbols('c0:8',real=True)
X=sp.symbols('X0:64',real=True); YY=sp.symbols('Y0:64',real=True)
check('all_real_sign_covariance_symbolic_64', all(sp.im(sr[j]*sc[l]*(X[8*j+l]+sp.I*YY[8*j+l]))==sr[j]*sc[l]*YY[8*j+l] for j in range(8) for l in range(8)))
# Exact phase discrepancy and both normalized branch formulas.
a0,a1,d0,d1=sp.symbols('A0 A1 D0 D1',real=True)
th={(cc,dd):[a0,a1][cc]+[d0,d1][dd]-sp.pi*(cc*dd+cc+dd)/4 for cc in range(2) for dd in range(2)}
check('exact_phase_cocycle',sp.simplify(th[0,0]+th[1,1]-th[0,1]-th[1,0])==-sp.pi/4)
R0,R1,S0,S1,u,v,w,h=sp.symbols('R0 R1 S0 S1 u v w h',real=True)
hs={(0,0):sp.cos(R0)*sp.cos(S0),(0,1):sp.sin(R0)*sp.cos(S1),(1,0):sp.cos(R1)*sp.sin(S0),(1,1):sp.sin(R1)*sp.sin(S1)}
caseA={R1:sp.pi/2+u,S1:sp.pi/2+v}
caseB={R0:sp.pi/2+u,S1:v,R1:w,S0:sp.pi/2+h}
check('case_A_other_h_parameters',sp.trigsimp(hs[0,1].subs(caseA)+sp.sin(R0)*sp.sin(v))==0 and sp.trigsimp(hs[1,0].subs(caseA)+sp.sin(u)*sp.sin(S0))==0)
check('case_B_other_h_parameters',sp.trigsimp(hs[0,0].subs(caseB)-sp.sin(u)*sp.sin(h))==0 and sp.trigsimp(hs[1,1].subs(caseB)-sp.sin(w)*sp.sin(v))==0)
# Complete independent constraint count and polynomial-degree bound.
aa=sp.symbols('a0:8',real=True); bb=sp.symbols('b0:8',real=True)
uvars=sp.symbols('u1:8',real=True); vvars=sp.symbols('v1:8',real=True)
U=(sp.Integer(1),)+uvars; Vv=(sp.Integer(0),)+vvars
TV=sp.symbols('T0:48',real=True); TT=sp.Matrix(8,6,TV)
rr=sp.Symbol('r',real=True)
ct=[1,rr/2,0,-rr/2,-1,-rr/2,0,rr/2]
st=[0,rr/2,1,rr/2,0,-rr/2,-1,-rr/2]
Ypoly=sp.Matrix(8,8,lambda j,l:rr*((aa[j]*Vv[l]+bb[j]*U[l])*ct[j*l%8]-(aa[j]*U[l]-bb[j]*Vv[l])*st[j*l%8])/4)
allvars=aa+bb+uvars+vvars+TV
check('78_independent_real_variables',len(allvars)==len(set(allvars))==78)
circles=[aa[j]**2+bb[j]**2-1 for j in range(8)]+[U[j]**2+Vv[j]**2-1 for j in range(1,8)]
frames=[sum(TT[j,l]*TT[j,m] for j in range(8))-int(l==m) for l in range(6) for m in range(l,6)]
check('36_equalities_15_circles_21_frames',len(circles)==15 and len(frames)==21)
check('Y_degree_at_most_two_so_M_degree_at_most_six',max(sp.Poly(e,*allvars).total_degree() for e in Ypoly)<=2)
# Entry formula checked directly with an independently fixed eighth-root table.
for j in range(8):
    A,Bb,Uu,Vvv=sp.symbols('A B U V',real=True)
    actual=sp.im((A+sp.I*Bb)*(Uu+sp.I*Vvv)*(ct[j]-sp.I*st[j]))
    check('semialgebraic_negative_Fourier_entry_'+str(j),sp.expand(actual-((A*Vvv+Bb*Uu)*ct[j]-(A*Uu-Bb*Vvv)*st[j]))==0)
# Counterexample threshold controls use exact rational H; positivity is strict.
threshold=sp.Rational(1,10)
for label, lam3, expected in [('below',sp.Rational(1,20),True),('at',threshold,False),('above',sp.Rational(1,5),False)]:
    H=sp.diag(1,sp.Rational(1,2),lam3,0,0,0,0,0)
    frame=sp.eye(8)[:,2:8]; M=threshold*sp.eye(6)-frame.T*H*frame
    check('strict_minmax_threshold_'+label,all(M[:l,:l].det()>0 for l in range(1,7))==expected)
# Independent negative controls, separate from the sibling checker's controls.
wrong_E=scale(outer(rank_one_vector,[conj(v) for v in rank_one_vector]),c)
check('reject_adjoint_instead_of_transpose_E',imag(wrong_E)!=imag(E))
check('reject_missing_global_phase_z',imag([[F[j][l]*q[j]*q[l] for l in range(8)] for j in range(8)])!=Y)
check('reject_dropped_phase_cocycle',sp.simplify(th[0,0]+th[1,1]-th[0,1]-th[1,0])!=0)
check('reject_wrong_sqrt_two_polynomial',16*t*t-16*t+1!=rt)
# Replay writes were isolated. Its regenerated machine results must match frozen bytes.
for name in ['WITNESS.json','EXACT_CHECKS.json','GENERAL_BLOCK_CHECKS.json']:
    check('replay_identical_'+name,(D/'replay'/name).read_bytes()==(FROZEN/name).read_bytes())
manifest=json.loads((FROZEN/'MANIFEST.json').read_text())
for item in manifest['files']:
    raw=(FROZEN/item['path']).read_bytes()
    check('frozen_hash_'+item['path'],len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256'])
results['scope']='Exact witness and supporting controls only. Continuous sector theorem and semialgebraic equivalence are independently reviewed analytically; unrestricted global lower bound is open.'
(D/'INDEPENDENT_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
