#!/usr/bin/env python3
"""Independent exact audit. Reads supplied JSON/text only; never imports their code.

SymPy supplies matrix multiplication, polynomial canonicalization, exact rational
linear algebra, and determinant computations. This deliberately differs from the
source package's hand-written sparse coefficient and matrix arithmetic.
"""
from pathlib import Path
import hashlib
import json
import platform
import sympy as S

SOURCE = Path('fourier8_kernel_construction_0249')
OUTPUT = Path(__file__).resolve().parent
z = S.Symbol('z')
ts = S.symbols('t0:4')
us = S.symbols('u0:8')
vs = S.symbols('v0:8')
variables = ts + us
PI = [1,2,3,4,5,6,7,0]
SIGMA = [2,7,5,0,6,1,3,4]
P = S.zeros(8); R = S.zeros(8)
for j in range(8):
    P[PI[j],j] = 1
    R[SIGMA[j],j] = 1
PINV = [PI.index(i) for i in range(8)]
SINV = [SIGMA.index(i) for i in range(8)]
KAPPA = [min(set(range(8)) - {j, PI[j], SIGMA[j]}) for j in range(8)]
I = S.eye(8)
checks = []


def require(label, predicate):
    if not predicate:
        raise AssertionError(label)
    checks.append(label)


def reduce_z(expr):
    # Univariate Euclidean remainder over the rational-function coefficient field.
    # Final exported coefficient comparison independently uses multivariate Poly.
    expanded = S.expand(expr)
    return S.Poly(expanded, z).rem(S.Poly(z**4+1,z)).as_expr().expand()


def zero(label, expr):
    numerator, denominator = S.fraction(S.cancel(expr))
    require(label, reduce_z(numerator) == 0)


def canonical(expr):
    return S.Poly(reduce_z(expr), *variables, z, domain=S.ZZ).as_dict()


def stored_polynomial(rows):
    terms = {}
    seen = set()
    for powers, coeff in rows:
        require('stored term format', len(powers)==12 and len(coeff)==4 and
                all(type(x) is int and x >= 0 for x in powers) and
                all(type(x) is int for x in coeff) and any(coeff))
        require('no repeated monomial in stored expression', tuple(powers) not in seen)
        seen.add(tuple(powers))
        for k, value in enumerate(coeff):
            if value:
                terms[tuple(powers)+(k,)] = S.Integer(value)
    return terms


def hashes():
    manifest = {}
    for line in (SOURCE/'SHA256SUMS.txt').read_text().splitlines():
        digest, name = line.split(maxsplit=1)
        actual = hashlib.sha256((SOURCE/name).read_bytes()).hexdigest()
        require('source seal '+name, actual==digest)
        manifest[name] = actual
    manifest['SHA256SUMS.txt'] = hashlib.sha256((SOURCE/'SHA256SUMS.txt').read_bytes()).hexdigest()
    return manifest


source_before = hashes()
require('support maps are permutations', sorted(PI)==list(range(8)) and sorted(SIGMA)==list(range(8)))
for label, perm in [('pi',PI),('sigma',SIGMA)]:
    seen=[]; q=0
    while q not in seen:
        seen.append(q); q=perm[q]
    require(label+' is one Hamiltonian 8-cycle', q==0 and len(seen)==8)
require('edge supports disjoint', all(PI[j] != SIGMA[j] for j in range(8)))
require('support maps noncommute', PI[SIGMA[0]]==3 and SIGMA[PI[0]]==7)
require('pivot list exact', KAPPA==[3,0,0,1,0,0,0,1])
U = I + S.diag(*us)*P
V = I + R*S.diag(*vs)
zero('U determinant formula', U.det() - (1-S.prod(us)))
zero('V determinant formula', V.det() - (1-S.prod(vs)))

# Matrix-level normalization: start from actual F,T,K, never use stored entries.
F = S.Matrix(8,8,lambda r,c: reduce_z(z**(r*c)))
all_systems = {}
system_results = {}
for anchor, pairs in [('adjacent',[(0,1),(2,3),(4,5),(6,7)]),('half',[(0,4),(1,5),(2,6),(3,7)])]:
    supplied=json.loads((SOURCE/(anchor.upper()+'_ANCHOR_ORBIT_SYSTEM.json')).read_text())
    K=S.zeros(8); diagonal=[S.Integer(1)]*8
    for j,(a,b) in enumerate(pairs):
        K[a,a]=K[a,b]=K[b,a]=1; K[b,b]=-1
        diagonal[b]=ts[j]
    T=S.diag(*diagonal)
    require(anchor+' K squared', K*K == 2*I)
    Cpair=S.diag(*[S.Symbol('C'+str(next(j for j,pair in enumerate(pairs) if k in pair))) for k in range(8)])
    require(anchor+' pair-constant diagonals commute', Cpair*K==K*Cpair)
    M=(F*T*K).applyfunc(reduce_z)
    factor_back=(M*K/2)*T.inv()
    for row in range(8):
        for col in range(8):
            zero(anchor+' exact Fourier reconstruction',factor_back[row,col]-F[row,col])
    # Independent legal sparse-mask anchor realization.
    W0=S.zeros(8); W1=S.zeros(8); E1=[0]*8
    for a,b in pairs:
        W0[a,b]=-z**2 # 1/i
        W1[b,a]=(z**2-1)/2 # 1/(-1-i)
        E1[a]=1-z**2; E1[b]=-1-z**2
    require(anchor+' first anchor mask square zero',W0*W0==S.zeros(8))
    require(anchor+' second anchor mask square zero',W1*W1==S.zeros(8))
    for row in range(8):
        for col in range(8):
            zero(anchor+' anchor branch sum', (z**2*(I+W0)+S.diag(*E1)*(I+W1)-K)[row,col])
    require(anchor+' anchor determinants one', (I-W0).det()==1 and (I-W1).det()==1)
    A=(U*M).applyfunc(reduce_z)
    C=A*R
    a=[A[KAPPA[j],j] for j in range(8)]
    c=[C[KAPPA[j],j] for j in range(8)]
    H=S.Matrix(8,8,lambda row,col: reduce_z(c[col]*A[row,col]-a[col]*C[row,col]))
    expected={**{'a_'+str(j):a[j] for j in range(8)}, **{'c_'+str(j):c[j] for j in range(8)}}
    expected.update({'h_'+str(row)+'_'+str(col):H[row,col] for row in range(8) for col in range(8)})
    for row in range(8):
        # Derive diagonal residual by independently substituting reconstructed
        # x and y into H_ii/c_i - x_i - y_i and clearing its actual denominator.
        ell=SINV[row]
        residual=H[row,row]/c[row] + H[row,ell]/a[ell] - H[PI[row],row]/(c[row]*us[PI[row]])
        expected['diag_'+str(row)]=reduce_z(S.cancel(residual*c[row]*a[ell]*us[PI[row]]))
    require(anchor+' exact expression inventory', set(expected)==set(supplied['polynomials']))
    for name, expression in expected.items():
        require(anchor+' coefficient equality '+name, canonical(expression)==stored_polynomial(supplied['polynomials'][name]))
    equation_names=['h_'+str(row)+'_'+str(col) for col in range(8) for row in range(8)
                    if row not in {col,PI[col],SIGMA[col],KAPPA[col]}]+['diag_'+str(row) for row in range(8)]
    require(anchor+' zero equation indexing', equation_names==supplied['zero_equations'] and len(equation_names)==40)
    require(anchor+' trivial pivot minors', all(H[KAPPA[j],j]==0 for j in range(8)))
    poly_guards=['a_'+str(j) for j in range(8)]+['c_'+str(j) for j in range(8)]
    poly_guards+=['h_'+str(PI[j])+'_'+str(j) for j in range(8)]
    poly_guards+=['h_'+str(SIGMA[j])+'_'+str(j) for j in range(8)]
    require(anchor+' full polynomial guards', supplied['nonzero_polynomial_guards']==poly_guards)
    require(anchor+' full variable guards', supplied['nonzero_variable_guards']==[str(v) for v in variables])
    require(anchor+' determinant guards', supplied['additional_nonzero_guards']==['1-product_i(u_i)','product_j(c_j)-product_j(a_j)'])
    require(anchor+' metadata support maps', supplied['pi']=={str(j):PI[j] for j in range(8)} and supplied['sigma']=={str(j):SIGMA[j] for j in range(8)})
    require(anchor+' metadata pivots',supplied['pivot_rows']=={str(j):KAPPA[j] for j in range(8)})
    require(anchor+' metadata anchor', supplied['anchor_pairs']==[list(p) for p in pairs])
    degree=max(S.Poly(expected[name],*variables).total_degree() for name in equation_names)
    count=sum(len(S.Poly(expected[name],*variables).terms()) for name in equation_names)
    require(anchor+' equation counts', degree==7 and count==({'adjacent':890,'half':880}[anchor]))
    require(anchor+' supplied statistics', supplied['stats']=={'number_variables':12,'number_zero_equations':40,'maximum_equation_total_degree':degree,'total_equation_monomials':count})
    all_systems[anchor]=(expected,H)
    system_results[anchor]={'exact_polynomial_matches':len(expected),'zero_equations':40,'variables':12,'degree':degree,'monomials':count,'all_guard_indices_verified':True,'exact_anchor_reconstruction':True}
    print(anchor+': all 88 expressions exactly match; anchors and guards verified.',flush=True)

# The certificate is regenerated from the matrix-derived half-anchor minors.
_,H=all_systems['half']
ii=z**2; w=us[0]; a=ts[0]; b=ts[2]; t=ts[1]
identities=[]
def cert(label, expr):
    zero(label,expr); identities.append(label)
cert('minor h_2_5',H[2,5]+4*t*z*(w-us[2]))
cert('minor h_3_5',H[3,5]-4*t*z*(ii-w*us[3]))
cert('minor h_4_5',H[4,5]+4*t*z**3*(w-us[4]))
cert('minor h_7_5',H[7,5]+4*t*z*(ii-w*us[7]))
direction={us[2]:w,us[4]:w,us[3]:ii/w,us[7]:ii/w}
def substitute(expr):
    return expr.subs(direction, simultaneous=True)
cert('force t2=-t0',w*substitute(H[4,0]+H[3,4])+4*ii*(a+b))
E=(a*a+1)*(1+ii)*w+ii*(1-a*a)
Rfactor=(a+1)*w-(a-1)
Sfactor=-ii*(a-1)*w-(a+1)
cert('E necessary',w*substitute(H[4,0]).subs(b,-a)+2*E)
cert('R S necessary',substitute(H[2,4]).subs(b,-a)+2*Rfactor*Sfactor)
q=a*a-2*ii*a+1
coef=(a*a+1)*(1+ii)
cert('R branch forces q', (a+1)*E-coef*Rfactor-(a-1)*q)
cert('S branch forces q', ii*(a-1)*E+coef*Sfactor+ii*(a+1)*q)
cert('R q force w squared i', (a+1)**2*(w*w-ii)-(1-ii)*q-Rfactor*((a+1)*w+(a-1)))
J=(t+1)*w*(z**3-z)+(t-1)*(1+ii)
cert('last necessary minor J',w*substitute(H[7,2]).subs(b,-a)-(1-a)*J)
cert('last contradiction 8 i t1',J*((t+1)*w*(z**3-z)-(t-1)*(1+ii))-2*(t+1)**2*(w*w-ii)-8*ii*t)
zero('a=1 ruled out by E',E.subs(a,1)-2*(1+ii)*w)
zero('a=-1 ruled out by E',E.subs(a,-1)-2*(1+ii)*w)
zero('primitive square i',ii**2+1)
zero('zeta expression square two',(z**3-z)**2-2)
zero('one plus i square',(1+ii)**2-2*ii)
zero('one plus i nonzero witness',(1+ii)*(1-ii)-2)
for row,col in [(2,5),(3,5),(4,5),(7,5),(4,0),(3,4),(2,4),(7,2)]:
    require('certificate minor genuinely off support',row not in {col,PI[col],SIGMA[col]})
print('Half-orbit: all 12 exact certificate identities verified.',flush=True)

# Full generic matrix identity for necessity, with no division or pivot assumptions.
# Any legal decomposition obeys U*M*V=U*Dy+Dx*V, whose columns off
# the support union give linear pairs annihilated by (1,v_j).
X=S.diag(*S.symbols('x0:8')); Y=S.diag(*S.symbols('y0:8'))
B=U*Y+X*V
for col in range(8):
    for row in range(8):
        if row not in {col,PI[col],SIGMA[col]}:
            require('generic right side has zero off support',B[row,col]==0)
        elif row==col:
            require('generic diagonal exactly x+y',B[row,col]==X[row,row]+Y[col,col])
        elif row==PI[col]:
            require('generic pi edge exactly u y',B[row,col]==us[row]*Y[col,col])
        else:
            require('generic sigma edge exactly x v',B[row,col]==X[row,row]*vs[col])
alpha,beta,gamma,delta,v=S.symbols('alpha beta gamma delta v')
zero('pivot-free necessary minor identity', delta*(alpha+v*beta)-beta*(gamma+v*delta)-(delta*alpha-gamma*beta))

# Generic open-chart sufficiency, independently at every matrix entry. These
# symbols are arbitrary; this is not a special numerical control or Fourier solve.
ga = S.symbols('ga0:8'); gc = S.symbols('gc0:8')
gh = S.Matrix(8,8,lambda r,c:S.Symbol('gh_'+str(r)+'_'+str(c)))
gv = [-ga[j]/gc[j] for j in range(8)]
gx = [-gh[r,SINV[r]]/ga[SINV[r]] for r in range(8)]
gy = [gh[PI[j],j]/(gc[j]*us[PI[j]]) for j in range(8)]
gV = I+R*S.diag(*gv)
gresidual = gh*S.diag(*[1/value for value in gc])-U*S.diag(*gy)-S.diag(*gx)*gV
for col in range(8):
    for row in range(8):
        if row in {PI[col],SIGMA[col]}:
            zero('generic support equation closes exactly',gresidual[row,col])
        elif row==col:
            l=SINV[row]
            diagonal_eq=us[PI[row]]*ga[l]*gh[row,row]+gc[row]*us[PI[row]]*gh[row,l]-ga[l]*gh[PI[row],row]
            zero('generic diagonal equation has exactly guarded denominator',gresidual[row,col]-diagonal_eq/(gc[row]*ga[l]*us[PI[row]]))
        else:
            zero('generic off-support equation has exactly c denominator',gresidual[row,col]-gh[row,col]/gc[col])
zero('V determinant guard clears only nonzero c factors',1-S.prod(gv)-(S.prod(gc)-S.prod(ga))/S.prod(gc))

# Exact controls use new parameters, rational signs/fractions, plus degenerate edges.
def inspect(M,u):
    Um=I+S.diag(*u)*P
    A=Um*M; C=A*R
    aa=[A[KAPPA[j],j] for j in range(8)]; cc=[C[KAPPA[j],j] for j in range(8)]
    h=S.Matrix(8,8,lambda r,c:cc[c]*A[r,c]-aa[c]*C[r,c])
    eq=[h[r,c] for c in range(8) for r in range(8) if r not in {c,PI[c],SIGMA[c],KAPPA[c]}]
    eq += [u[PI[r]]*aa[SINV[r]]*h[r,r]+cc[r]*u[PI[r]]*h[r,SINV[r]]-aa[SINV[r]]*h[PI[r],r] for r in range(8)]
    guards=[*u,*aa,*cc,*[h[PI[c],c] for c in range(8)],*[h[SIGMA[c],c] for c in range(8)],1-S.prod(u),S.prod(cc)-S.prod(aa)]
    recovered=None
    if all(aa) and all(cc) and all(u):
        recovered=([-aa[j]/cc[j] for j in range(8)],[-h[i,SINV[i]]/aa[SINV[i]] for i in range(8)],
                   [h[PI[j],j]/(cc[j]*u[PI[j]]) for j in range(8)])
    return h,eq,guards,recovered,aa,cc

controls=[]
for seed in [7,11,19,23]:
    u=[S.Rational((-1)**i*(seed+i+2),i+2) for i in range(8)]
    v=[S.Rational((-1)**(i+1)*(2*seed+i+3),i+3) for i in range(8)]
    x=[S.Rational(seed+3*i+2,2*i+3) for i in range(8)]
    y=[S.Rational((-1)**i*(seed+5*i+4),i+5) for i in range(8)]
    Um=I+S.diag(*u)*P; Vm=I+R*S.diag(*v)
    M=Um.inv()*S.diag(*x)+S.diag(*y)*Vm.inv()
    h,eq,guards,rec,aa,cc=inspect(M,u)
    require('rational all guards',all(guards))
    require('rational all 40 equations',not any(eq))
    require('rational recover all scales and directions',rec==(v,x,y))
    vr,xr,yr=rec
    Q0=S.diag(*[1/s for s in xr])*Um
    Q1=Vm*S.diag(*[1/s for s in yr])
    require('rational full inverse sum',Q0.inv()+Q1.inv()==M)
    rejected=0
    for row,col in [(0,0),(2,5),(4,0),(7,7)]:
        bad=M.copy(); bad[row,col]+=S.Rational(1,13)
        require('rational perturbation rejection',any(inspect(bad,u)[1]))
        rejected+=1
    controls.append({'seed':seed,'exact_full_inverse_sum':True,'directions_and_scales_recovered':True,'full_guards':True,'forty_equations':True,'negative_controls_rejected':rejected})

# Explicit excluded-endpoint controls: equations alone can admit x=0/y=0,
# so h_sigma and h_pi guards must not be dropped.
endpoint_tests=[]
for which in ['x','y']:
    xc=x[:]; yc=y[:]
    if which=='x':xc[0]=0
    else:yc[0]=0
    M=Um.inv()*S.diag(*xc)+S.diag(*yc)*Vm.inv()
    h,eq,guards,rec,aa,cc=inspect(M,u)
    require('zero endpoint still satisfies forty equations',not any(eq))
    require('zero endpoint rejected by complete guards',not all(guards))
    if which=='x':require('x endpoint numerator vanishes',h[0,SINV[0]]==0)
    else:require('y endpoint numerator vanishes',h[PI[0],0]==0)
    endpoint_tests.append({'zero_endpoint':which+'0','equations_pass':True,'full_guards_reject':True})

# Edge-zero and pivot-zero cases are legitimate for necessary-minor reasoning.
degenerate=[]
for mode in ['all_edges_zero','some_edges_zero']:
    du=[S.Integer(0)]*8 if mode=='all_edges_zero' else u[:]
    dv=[S.Integer(0)]*8 if mode=='all_edges_zero' else v[:]
    if mode=='some_edges_zero':du[2]=0; dv[5]=0
    DU=I+S.diag(*du)*P; DV=I+R*S.diag(*dv)
    M=DU.inv()*S.diag(*x)+S.diag(*y)*DV.inv()
    h,eq,guards,rec,aa,cc=inspect(M,du)
    require('zero-edge controls all necessary minors',all(h[r,c]==0 for c in range(8) for r in range(8) if r not in {c,PI[c],SIGMA[c]}))
    if mode=='all_edges_zero':require('identically zero pivot pairs admitted',not any(aa) and not any(cc))
    degenerate.append({'mode':mode,'all_off_support_minors_zero':True,'zero_pivot_pairs':sum(aa[j]==0 and cc[j]==0 for j in range(8))})

require('source seals unchanged',hashes()==source_before)
result={'verdict':'PASS for both precisely stated claims; no adjacent solvability claim',
        'source_directory':str(SOURCE),'source_hashes_before_and_after':source_before,
        'runtime':{'python':platform.python_version(),'sympy':S.__version__},
        'supplied_code_executed_or_imported':False,
        'systems':system_results,'half_orbit_certificate':{'identities':identities,'count':len(identities),'pivot_nonvanishing_used':False,'edge_nonvanishing_used':False,'Green_determinant_guards_used':False,'essential_nonzero_values':['2','zeta','t0','t1','w (derived)','a-1 (derived)','a+1 (derived)','1+i (derived)']},
        'rational_positive_controls':controls,'zero_endpoint_controls':endpoint_tests,'zero_edge_controls':degenerate,
        'checks_completed':len(checks)}
(OUTPUT/'AUDIT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
(OUTPUT/'SOURCE_SEALS.json').write_text(json.dumps(source_before,indent=2)+'\n')
print(json.dumps(result,indent=2))
