"""Fresh exact checks for the quantitative C8 all-phase lower-bound proof.
No historical checker or optimization code is imported or executed.
The analytical inequalities and their hypotheses are proved in PROOF.md;
this file checks identities and exact numerical margins, not global sampling.
"""
from pathlib import Path
import sympy as s
import json, time, hashlib

start=time.perf_counter()
ROOT=Path(__file__).resolve().parent
checks=[]
def zero(expr,label):
    assert s.simplify(s.expand(expr)) == 0, (label,expr)
    checks.append(label)
def pos(expr,label):
    value=s.factor(expr)
    assert value.is_positive is True, (label,value)
    checks.append(label)
def neq(expr,label):
    assert s.simplify(s.expand(expr)) != 0, label
    checks.append(label)
R=s.Rational; I=s.I

# Exact arithmetic margins. Every comparison involves rational values or
# squaring positive bounds, rather than numerical angle evaluation.
eps=R(1,500000)
pos(R(283,200)**2-2,'sqrt(2) < 283/200')
pos((2-R(283,200))/4-R(191,500)**2,'cos(theta0) > 191/500')
pos(R(231,250)**2-(2+R(283,200))/4,'sin(theta0) < 231/250')
pos(R(191,500)-eps,'positive cosine denominator')
pos(R(5,2)*(R(191,500)-eps)-(R(231,250)+eps),'tan(theta) < 5/2')
pos(R(9,2000)-eps,'positive rho comparison')
pos((R(9,2000)-eps)**2-10*eps,'rho < 9/2000')
pos(R(8,625)**2-8*R(9,2000)**2,'eta < 8/625')
pos(R(1,50)-R(8,625),'eta < 1/50')
pos(2-(4*eps)**2-R(199,100),'2 cos(4epsilon) > 199/100 by cos(t)>=1-t^2/2')
pos(R(24,25)*R(4,5)*R(47,50)-R(21,25)**2,'normalized-product denominator > 21/25')
zero(4*R(101,50)/R(21,25)/5-R(202,105),'phase-product constant')
pos(R(199,100)-R(202,105),'phase-product contradiction margin')
pos(R(17,12)**2-2,'sqrt(2) < 17/12')
pos(R(13,50)-(R(9,2000)+14*R(17,12)*R(8,625)),'r < 13/50')
pos(R(191,500)-eps-R(19,50),'c > 19/50')
pos(1-225*R(8,625)**2-R(49,50)**2,'beta magnitude > 49/50')
pos((R(19,50)*R(49,50))**2-2*R(13,50)**2,'final lower threshold > 13/50')

# Recurrences with unequal opposite cycle offsets. Formally lambda_o=-i/lambda_e.
le,e0=s.symbols('lambda_e e0',nonzero=True)
lo=-I/le; Lam=-I
x=[s.Integer(1),*s.symbols('x1:4',nonzero=True)]
y=[s.Integer(1),*s.symbols('y1:4',nonzero=True)]
e=[e0*Lam**t/(x[t]*y[t]) for t in range(4)]
d=[e0/lo*Lam**t/(x[t]*y[(t-1)%4]) for t in range(4)]
for t in range(4):
    zero(le*e[t]/d[(t+1)%4]*x[t]-x[(t+1)%4],f'even recurrence {t}')
    zero(lo*d[(t+1)%4]/e[(t+1)%4]*y[t]-y[(t+1)%4],f'odd recurrence {t}')
    zero(e[t]*x[t]*y[t]-e0*Lam**t,f'product e identity {t}')
    zero(d[t]*x[t]*y[(t-1)%4]-e0/lo*Lam**t,f'product d identity {t}')
neq(d[0]*x[0]*y[3]-e0/le,'destructive control: wrong lambda in d identity')

# Unit-circle conjugation is represented by inversion of coordinate phases.
for k in range(4):
    D=sum(d[t]*x[t]*I**(-k*t) for t in range(4))/2
    E=sum(e[t]*y[t]*I**(-k*t) for t in range(4))/2
    CY=sum(I**((-k-1)*t)/y[t] for t in range(4))/2
    CX=sum(I**((-k-1)*t)/x[t] for t in range(4))/2
    zero(D-e0/lo*I**(-k-1)*CY,f'D Fourier identity {k}')
    zero(E-e0*CX,f'E Fourier identity {k}')
zero(1/lo/I-le,'elimination coefficient is lambda_e')

# Exact half-shift identities before bounding the small Fourier coefficients.
X=s.symbols('X0:4')
ix=[sum(X[n]*I**(n*t) for n in range(4))/2 for t in range(4)]
for sign in (1,-1):
    for t in range(4):
        rhs=-sign*sum(X[n]*I**(n*t) for n in range(4) if (-1)**n != sign)
        zero(ix[(t+2)%4]-sign*ix[t]-rhs,f'half-shift identity {sign},{t}')

# Arbitrary cyclic-Hankel matrix and arbitrary diagonal B, not periodic.
cs=s.symbols('c0:8'); bs=s.symbols('b0:8',nonzero=True)
C=s.Matrix(8,8,lambda j,k:cs[(j+k)%8])
B=s.diag(*bs); U=C*B
S=s.zeros(8)
for j in range(8): S[(j+1)%8,j]=1
for j in range(8):
    for k in range(8): zero((C*S-S.T*C)[j,k],f'Hankel shift {j},{k}')
K=S.T*B.inv()*S.T*B
for j in range(8):
    for k in range(8):
        expected=bs[k]/bs[(k-1)%8] if j==(k-2)%8 else 0
        zero(K[j,k]-expected,f'weighted shift {j},{k}')

beta0=(bs[0]+bs[4])/2; beta2=(bs[2]+bs[6])/2
for sign in (1,-1):
    E=s.zeros(8,2)
    for col,j in enumerate((0,2)):
        E[j,col]=1/s.sqrt(2); E[j+4,col]=sign/s.sqrt(2)
    M=E.T*U*E
    zero(M[0,0]-(cs[0]+sign*cs[4])*beta0,f'compression first diagonal {sign}')
    zero(M[1,1]-(cs[4]+sign*cs[0])*beta2,f'compression second diagonal {sign}')
    if sign == -1:
        neq(M[1,1]-(cs[0]-cs[4])*beta2,'destructive control: minus-sector diagonal sign')

# Flat-vector diagonal identity for an arbitrary, possibly nonnormal compression.
z=s.symbols('z',nonzero=True)
M=s.Matrix(2,2,s.symbols('m0:4'))
v=s.Matrix([1,z])/s.sqrt(2); w=s.Matrix([1,-z])/s.sqrt(2)
vh=s.Matrix([[1,1/z]])/s.sqrt(2); wh=s.Matrix([[1,-1/z]])/s.sqrt(2)
zero((vh*M*w+wh*M*v)[0]-(M[0,0]-M[1,1]),'flat-vector arbitrary-compression identity')

# Exact rational external bound comparisons, with decimals informational only.
theta0=3*s.pi/8
rho=s.sqrt(10*eps)+eps; eta=2*s.sqrt(2)*rho
r=rho+14*s.sqrt(2)*eta
lower=s.sin(3*s.pi/16+eps/2)
upper=s.sqrt(1+s.sqrt(s.sqrt(2)-1))/2
sources={
 'inherited_lower_proof':Path('/workspace/shared/phase_rankzero_20261019_1053/PROOF.md'),
 'accepted_upper_proof':Path('/workspace/shared/phase_rankzero_exact_20261019_1220/PROOF.md'),
 'independent_upper_review':Path('/workspace/shared/phase_rankzero_exact_review_20261019_1227/REVIEW.md'),
}
source_receipts={key:{'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size} for key,path in sources.items()}
result={
 'status':'PASS', 'assertions':len(checks),
 'claim':'All-phase strict explicit lower bound, not exact global optimality',
 'lower_bound_exact':'sin(3*pi/16 + 1/1000000)',
 'lower_bound_decimal':str(s.N(lower,40)),
 'improvement_over_old_lower':str(s.N(lower-s.sin(3*s.pi/16),40)),
 'inherited_upper_bound_decimal':str(s.N(upper,40)),
 'rho_decimal':str(s.N(rho,25)), 'eta_decimal':str(s.N(eta,25)),
 'flat_residual_upper_decimal':str(s.N(r,25)),
 'contradicting_threshold_decimal':str(s.N(s.cos(theta0+eps)*s.sqrt(1-225*eta**2)/s.sqrt(2),25)),
 'source_receipts':source_receipts,
 'runtime_seconds':time.perf_counter()-start,
 'controls':[
  'Reject substitution of lambda_e for lambda_o in asymmetric-cycle product identity',
  'Reject wrong second diagonal sign in the minus-sector compression',
 ],
 'scope':'Exact identities and rational inequality margins. No numerical optimization, sampling, global periodicity assumption, external write, or historical checker execution.'
}
(ROOT/'CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
(ROOT/'ASSERTIONS.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(result,indent=2))
