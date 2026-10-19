"""Independent controls of the all-phase quantitative C8 lower gap.
Written for this review. No candidate/historical code is imported or executed.
All proof assertions use symbolic identities or exact rational inequalities.
The concrete full-matrix control is a diagnostic of universal identities, not
sampling evidence for the theorem; the all-phase reasoning is in REVIEW.md.
"""
from pathlib import Path
import hashlib, json, time
import sympy as sp

ROOT=Path(__file__).resolve().parent
CAND=Path('/workspace/shared/phase_rankzero_quantitative_20261019_1347')
UPPER=Path('/workspace/shared/phase_rankzero_exact_review_20261019_1227')
UPROOF=Path('/workspace/shared/phase_rankzero_exact_20261019_1220/PROOF.md')
OLD=Path('/workspace/shared/phase_rankzero_20261019_1053/PROOF.md')
start=time.perf_counter(); checks=[]; controls=[]
R=sp.Rational; I=sp.I

def clean(x): return sp.cancel(sp.expand(x))
def zero(x,name):
    y=clean(x)
    assert y == 0, (name,y)
    checks.append(name)
def matzero(M,name):
    for j in range(M.rows):
        for k in range(M.cols): zero(M[j,k],f'{name} [{j},{k}]')
def positive(x,name):
    y=sp.simplify(x)
    assert y.is_positive is True, (name,y)
    checks.append(name)
def reject(x,name):
    y=clean(x)
    assert y != 0, (name,y)
    checks.append(name); controls.append(name)
def receipt(p):
    raw=p.read_bytes()
    return {'path':str(p),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def bindings():
    paths=sorted(CAND.glob('*'))+sorted(UPPER.glob('*'))+[UPROOF,OLD]
    return {str(p):receipt(p) for p in paths if p.is_file()}
before=bindings()
(ROOT/'SOURCE_BINDINGS_BEFORE.json').write_text(json.dumps(before,indent=2)+'\n')
manifest=json.loads((CAND/'MANIFEST.json').read_text())
for filename,data in manifest.items():
    now=receipt(CAND/filename)
    assert all(now[k]==data[k] for k in ('sha256','bytes')), filename
    checks.append('candidate manifest '+filename)
assert receipt(UPROOF)['sha256']=='22f8462ed90c58119b0b3abf36d5d47416dd31747716a66d3b0f0a931be0f6e2'
checks.append('accepted upper witness proof binding')
accepted=json.loads((UPPER/'VERDICT.json').read_text())
assert accepted['verdict']=='ACCEPT' and accepted['candidate_proof_sha256']==receipt(UPROOF)['sha256']
checks.append('accepted upper review verdict and target match')

# Exact full eight-point Fourier control, with explicitly nonperiodic gauges.
zeta=[1,(1+I)/sp.sqrt(2),I,(-1+I)/sp.sqrt(2),-1,(-1-I)/sp.sqrt(2),-I,(1-I)/sp.sqrt(2)]
F=sp.Matrix(8,8,lambda j,k:zeta[(-j*k)%8]/sp.sqrt(8))
Id=sp.eye(8)
mats=lambda M:M.applyfunc(clean)
mats_zero=lambda M,name:matzero(mats(M),name)
matzero(F.H*F-Id,'normalized F adjoint F')
matzero(F*F.H-Id,'normalized F F adjoint')
matzero(F.T-F,'Fourier symmetry')
p=[1,I,1,1,1,1,1,1]; q=[1,1,I,1,I,1,1,1]
P=sp.diag(*p); Q=sp.diag(*q); A=P*P; B=Q*Q
V=mats(P*F*Q); U=mats(F*A*F*B); W=mats(V.T*V)
Y=mats((V-sp.conjugate(V))/(2*I)); X=mats((V+sp.conjugate(V))/2)
matzero(U.H*U-Id,'actual U unitary')
matzero(W.H*W-Id,'W unitary')
matzero(W.T-W,'W symmetric')
matzero(Q.H*W*Q-U,'W unitarily similar to actual U')
matzero(Y.T*Y-(Id-(W+W.H)/2)/2,'imaginary part Gram spectral identity')
res=mats(F-P.H*X*Q.H)
matzero(res-P.H*(I*Y)*Q.H,'actual external residual identity')
matzero(res.H*res-Q*(Y.T*Y)*Q.H,'actual external Gram unitarily conjugate')
reject((sp.sqrt(8)*F).H.__mul__(sp.sqrt(8)*F)[0,0]-1,'control: unnormalized Fourier is not unitary')

S=sp.zeros(8)
for j in range(8): S[(j+1)%8,j]=1
T=B.H*S*B
K=mats(U*T*U.H*T.H)
matzero(K-S.T*B.H*S.T*B,'actual unitary commutator weighted shift')
matzero(K-Id-(U*T-T*U)*U.H*T.H,'commutator norm-preserving product identity')
D=mats(T*U.H*T.H)
matzero((D+D.H)/2-T*(U+U.H)*T.H/2,'D accretivity conjugation identity')

# Generic weighted-shift cycle products, with independent symbolic phase values.
b=sp.symbols('b0:8',nonzero=True); Bs=sp.diag(*b)
Ks=S.T*Bs.inv()*S.T*Bs
for row in range(8):
    for col in range(8):
        zero(Ks[row,col]-(b[col]/b[(col-1)%8] if row==(col-2)%8 else 0),f'generic weighted shift [{row},{col}]')
Gamma=sp.prod(b[j] for j in range(0,8,2))/sp.prod(b[j] for j in range(1,8,2))
matzero(Ks**4-sp.diag(*[Gamma if j%2==0 else 1/Gamma for j in range(8)]),'fourth power cycle products')
xpoly=sp.symbols('xpoly')
for parity,gamma in ((0,Gamma),(1,1/Gamma)):
    inds=list(range(parity,8,2))
    zero(Ks.extract(inds,inds).charpoly(xpoly).as_expr()-(xpoly**4-gamma),f'cycle characteristic polynomial {parity}')

# Generic endpoint recurrences. All x_t,y_t,e0,le are unit phases;
# inverse is therefore the algebraic representation of conjugation.
le,e0=sp.symbols('le e0',nonzero=True); lo=-I/le; Lam=-I
xx=[sp.Integer(1),*sp.symbols('x1:4',nonzero=True)]
yy=[sp.Integer(1),*sp.symbols('y1:4',nonzero=True)]
ee=[e0*Lam**t/(xx[t]*yy[t]) for t in range(4)]
dd=[e0*Lam**t/(lo*xx[t]*yy[(t-1)%4]) for t in range(4)]
bxy=[val for pair in zip(dd,ee) for val in pair]
Kxy=S.T*sp.diag(*[1/v for v in bxy])*S.T*sp.diag(*bxy)
for vals,parity,lam in ((xx,0,le),(yy,1,lo)):
    for power in (0,1):
        vec=sp.zeros(8,1)
        for t in range(4):vec[2*t+parity]=I**(power*t)*vals[t]/2
        matzero(Kxy*vec-I**power*lam*vec,f'endpoint eigenvector parity {parity} modulation {power}')
for t in range(4):
    zero(ee[t]*xx[t]*yy[t]-e0*Lam**t,f'e phase recurrence product {t}')
    zero(dd[t]*xx[t]*yy[(t-1)%4]-e0*Lam**t/lo,f'd phase recurrence product {t}')
reject(dd[0]*xx[0]*yy[3]-e0/le,'control: exchanging the two cycle eigenvalues is invalid')

# Independent Fourier normalization checks before using the recurrence identities.
xd=sp.symbols('dx0:4'); ye=sp.symbols('ey0:4')
xe=sp.Matrix([xx[j//2]/2 if j%2==0 else 0 for j in range(8)])
yo=sp.Matrix([yy[j//2]/2 if j%2==1 else 0 for j in range(8)])
dxe=sp.Matrix([xd[j//2]/2 if j%2==0 else 0 for j in range(8)])
eyo=sp.Matrix([ye[j//2]/2 if j%2==1 else 0 for j in range(8)])
Xf=[sum(xx[t]*I**(-n*t) for t in range(4))/2 for n in range(4)]
Yf=[sum(yy[t]*I**(-n*t) for t in range(4))/2 for n in range(4)]
Df=[sum(xd[t]*I**(-n*t) for t in range(4))/2 for n in range(4)]
Ef=[sum(ye[t]*I**(-n*t) for t in range(4))/2 for n in range(4)]
for j in range(8):
    k=j%4
    zero((F*dxe)[j]-Df[k]/sp.sqrt(8),f'even input eight-point factor {j}')
    zero((F.H*xe)[j]-Xf[(-k)%4]/sp.sqrt(8),f'even output eight-point factor {j}')
    zero((F*eyo)[j]-zeta[(-j)%8]*Ef[k]/sp.sqrt(8),f'odd input eight-point factor {j}')
    zero((F.H*yo)[j]-zeta[j%8]*Yf[(-k)%4]/sp.sqrt(8),f'odd output eight-point factor {j}')
    zero(zeta[j%8]**2-I**k,f'odd equation phase ratio {j}')
for k in range(4):
    dft=sum(dd[t]*xx[t]*I**(-k*t) for t in range(4))/2
    eft=sum(ee[t]*yy[t]*I**(-k*t) for t in range(4))/2
    cy=sum(I**((-k-1)*t)/yy[t] for t in range(4))/2
    cx=sum(I**((-k-1)*t)/xx[t] for t in range(4))/2
    zero(dft-e0/lo*I**(-k-1)*cy,f'recurrence D Fourier identity {k}')
    zero(eft-e0*cx,f'recurrence E Fourier identity {k}')
a,u,Xn,Yn,Xprevbar,Yprevbar=sp.symbols('a u Xn Yn Xprevbar Yprevbar')
for n in range(4):
    dn=e0/lo*I**(n-1)*Yprevbar; en=e0*Xprevbar
    r1=a*dn-u*Xn; r2=a*en-u*I**(-n)*Yn
    target=Xn*Xprevbar-le*Yn*Yprevbar
    zero(en*r1-dn*r2+u*e0*target,f'no-division error elimination {n}')
zero(1/lo/I-le,'correct lambda in eliminated phase relation')

# Universal scalar identities used in quantitative inequalities.
s0=sp.symbols('s0',real=True); ar,ai=sp.symbols('ar ai',real=True)
endpoint=ar+sp.cos(2*s0)*ar+sp.sin(2*s0)*ai-2*sp.cos(s0)*(sp.cos(s0)*ar+sp.sin(s0)*ai)
assert sp.trigsimp(sp.expand_trig(endpoint))==0
checks.append('endpoint accretivity expectations sum identity')
r1,r2,cosdiff=sp.symbols('r1 r2 cosdiff',real=True)
zero(r1*r1+r2*r2-2*r1*r2*cosdiff-r1*r2*(2-2*cosdiff)-(r1-r2)**2,'normalized complex phase-distance identity')
p4=sp.symbols('p0:4');q4=sp.symbols('q0:4')
zero(sp.prod(p4)-sp.prod(q4)-sum((p4[n]-q4[n])*sp.prod(p4[:n])*sp.prod(q4[n+1:]) for n in range(4)),'four-factor product-difference identity')
phi=sp.symbols('phi',nonzero=True)
zero(2+phi**2+phi**(-2)-(phi+1/phi)**2,'commutator phase mismatch squared identity')

# Half-shift inversion and both actual, generally non-invariant compressions.
coeff=sp.symbols('H0:4'); inverse=[sum(coeff[n]*I**(n*t) for n in range(4))/2 for t in range(4)]
for sign in (1,-1):
    for t in range(4):
        zero(inverse[(t+2)%4]-sign*inverse[t]+sign*sum(coeff[n]*I**(n*t) for n in range(4) if (-1)**n!=sign),f'half-shift inverse transform {sign},{t}')
cs=sp.symbols('c0:8'); H=sp.Matrix(8,8,lambda j,k:cs[(j+k)%8]); HBs=H*Bs
matzero(H*S-S.T*H,'generic cyclic-Hankel intertwining')
compressions={}
for sign in (1,-1):
    basis=sp.zeros(8,2)
    for col,j in enumerate((0,2)):
        basis[j,col]=1/sp.sqrt(2);basis[j+4,col]=sign/sp.sqrt(2)
    matzero(basis.H*basis-sp.eye(2),f'orthonormal even sector basis {sign}')
    M=basis.H*HBs*basis
    beta0=(b[0]+b[4])/2; beta2=(b[2]+b[6])/2
    zero(M[0,0]-(cs[0]+sign*cs[4])*beta0,f'actual compression first diagonal {sign}')
    zero(M[1,1]-(cs[4]+sign*cs[0])*beta2,f'actual compression second diagonal {sign}')
    actual=mats(basis.H*U*basis); compressions[sign]=actual
    if sign==1:
        leak=mats(U*basis-basis*actual)
        nonzero=[v for v in leak if clean(v)!=0]
        assert nonzero
        checks.append('nonperiodic exact control has non-invariant even plus subspace')
        gram=mats(actual.H*actual-sp.eye(2))
        assert any(clean(v)!=0 for v in gram)
        checks.append('nonperiodic exact control compression is not unitary')
        controls.append('control: treating a non-invariant compression as unitary fails')
    else:reject(M[1,1]-(cs[0]-cs[4])*beta2,'control: wrong minus-sector second-diagonal sign fails')
M=sp.Matrix(2,2,sp.symbols('m0:4')); z=sp.symbols('z',nonzero=True)
v=sp.Matrix([1,z])/sp.sqrt(2);w=sp.Matrix([1,-z])/sp.sqrt(2)
vstar=sp.Matrix([[1,1/z]])/sp.sqrt(2);wstar=sp.Matrix([[1,-1/z]])/sp.sqrt(2)
zero((vstar*M*w+wstar*M*v)[0]-(M[0,0]-M[1,1]),'flat-vector diagonal identity for arbitrary compression')
for j in (0,2):
    beta=(b[j]+b[j+4])/2; betastar=(1/b[j]+1/b[j+4])/2
    diff=b[j]-b[j+4];diffstar=1/b[j]-1/b[j+4]
    zero(beta*betastar+diff*diffstar/4-1,f'unit-phase average magnitude identity {j}')
zero((r1+r2)**2+(r1-r2)**2-2*(r1*r1+r2*r2),'real part of complex parallelogram identity')

# All endpoint margins, by rational arithmetic and positive squaring.
eps=R(1,500000)
positive(R(3,8)-eps,'theta below pi/2 using pi > 3')
positive(6-16*eps,'cycle offset inverse-product uniqueness using 2*pi > 6')
positive(R(283,200)**2-2,'sqrt2 upper enclosure')
positive((2-R(283,200))/4-R(191,500)**2,'cos(3pi/8) exceeds 191/500')
positive(R(231,250)**2-(2+R(283,200))/4,'sin(3pi/8) below 231/250')
positive(R(191,500)-eps,'cosine Lipschitz lower enclosure positive')
positive(R(5,2)*(R(191,500)-eps)-(R(231,250)+eps),'tan(theta) below 5/2 via Lipschitz enclosures')
positive((R(9,2000)-eps)**2-10*eps,'rho below 9/2000 by positive squaring')
positive(R(9,2000)-eps,'rho squaring uses positive side')
positive(R(8,625)**2-8*R(9,2000)**2,'eta below 8/625 by positive squaring')
positive(R(1,50)-R(8,625),'eta below 1/50')
positive(R(24,25)*R(4,5)*R(47,50)-R(21,25)**2,'phase-product denominator margin')
zero(4*R(101,50)/R(21,25)/5-R(202,105),'phase-product upper constant')
positive(R(199,100)-R(202,105),'phase-product contradiction strict margin')
positive(2-(4*eps)**2-R(199,100),'phase-product lower cosine margin')
positive(R(17,12)**2-2,'secondary sqrt2 upper enclosure')
positive(R(13,50)-(R(9,2000)+14*R(17,12)*R(8,625)),'candidate separated r upper bound')
rho=sp.sqrt(10*eps)+eps;eta=2*sp.sqrt(2)*rho;rr=rho+14*sp.sqrt(2)*eta
zero(rr-57*rho,'independent simplification r = 57 rho')
positive(R(13,50)-57*R(9,2000),'independent stronger r upper bound')
positive(R(191,500)-eps-R(19,50),'c above 19/50')
positive(1-225*R(8,625)**2-R(49,50)**2,'beta lower radius above 49/50')
positive((R(19,50)*R(49,50))**2-2*R(13,50)**2,'final contradiction via positive squaring')
zero(2*(14*eta)**2/4-(7*sp.sqrt(2)*eta)**2,'flat-vector coordinate replacement norm constant')
zero((30*eta)**2/4-225*eta**2,'beta average 225 coefficient')

# Verify that the updated interval is nonempty without numerical evaluation.
positive(R(139,250)**2-(1-R(191,500))/2,'old lower endpoint below 0.556')
positive(R(14,25)-(R(139,250)+eps/2),'new lower endpoint below 0.56')
positive(2-R(7,5)**2,'sqrt2 above 7/5')
positive(R(7,5)-1-R(11,25)**2,'h above 11/25')
zero((1+R(11,25))/4-R(3,5)**2,'accepted upper endpoint above 0.6')

# Informational decimals, not used to pass any proof assertion.
lower=sp.sin(3*sp.pi/16+eps/2);upper=sp.sqrt(1+sp.sqrt(sp.sqrt(2)-1))/2
threshold=sp.cos(3*sp.pi/8+eps)*sp.sqrt(1-225*eta**2)/sp.sqrt(2)
after=bindings()
assert before==after
checks.append('all frozen source bytes unchanged after independent controls')
(ROOT/'SOURCE_BINDINGS_AFTER.json').write_text(json.dumps(after,indent=2)+'\n')
result={
 'status':'PASS','assertions':len(checks),'destructive_controls':controls,
 'candidate_proof_sha256':receipt(CAND/'PROOF.md')['sha256'],
 'candidate_or_historical_checker_executed':False,'source_immutability_verified':True,
 'all_phase_reasoning':'REVIEW.md; exact controls supplement rather than replace the analytical proof',
 'lower_bound_exact':'sin(3*pi/16 + 1/1000000)',
 'inherited_upper_bound_exact':'sqrt(1+sqrt(sqrt(2)-1))/2',
 'lower_decimal':str(sp.N(lower,40)),
 'improvement_decimal':str(sp.N(lower-sp.sin(3*sp.pi/16),40)),
 'upper_decimal':str(sp.N(upper,40)),
 'r_decimal':str(sp.N(rr,30)),
 'contradiction_threshold_decimal':str(sp.N(threshold,30)),
 'runtime_seconds':time.perf_counter()-start,
 'global_periodicity_assumed':False,'periodic_surrogate_used':False,
 'numerical_sampling_or_optimization':False,'external_writes':False,
}
(ROOT/'ASSERTIONS.json').write_text(json.dumps(checks,indent=2)+'\n')
(ROOT/'INDEPENDENT_EXACT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
