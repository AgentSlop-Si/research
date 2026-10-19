"""Fresh exact controls for the C8 rank-zero strict obstruction.
No historical scripts, phase optimization, floating-point matrices, or external writes.
"""
import json
from pathlib import Path
import sympy as s

OUT = Path(__file__).resolve().parent
I=s.I
lam=(-1+I)/s.sqrt(2)
omega=I
zeta=(1+I)/s.sqrt(2)
checks=[]

def zero(expr, label):
    val=s.simplify(s.expand(expr))
    if val != 0:
        raise AssertionError((label,val))
    checks.append(label)

def matzero(mat,label):
    for j in range(mat.rows):
        for k in range(mat.cols):
            zero(mat[j,k],f'{label}[{j},{k}]')

zero(lam**4+1,'endpoint lambda^4=-1')
zero(lam**2-omega**-1,'endpoint lambda^2=omega^-1')
zero(lam**-2-omega,'endpoint opposite modulation')

# Generic formal unimodular b_0,...,b_6, with b_7 chosen so Gamma=-1.
bvar=s.symbols('b0:7',nonzero=True)
b=list(bvar)+[-bvar[0]*bvar[2]*bvar[4]*bvar[6]/(bvar[1]*bvar[3]*bvar[5])]
def star(q):
    return s.conjugate(q).subs({s.conjugate(v):1/v for v in bvar},simultaneous=True)

def clean(q):
    return s.simplify(s.expand(q))

d=b[::2]; e=b[1::2]
x=[s.Integer(1)];y=[s.Integer(1)]
for t in range(3):
    x.append(clean(lam*e[t]/d[t+1]*x[-1]))
    y.append(clean(lam*d[t+1]/e[t+1]*y[-1]))
for t in range(4):
    zero(x[(t+1)%4]-lam*e[t]/d[(t+1)%4]*x[t],f'even endpoint recurrence {t}')
    zero(y[(t+1)%4]-lam*d[(t+1)%4]/e[(t+1)%4]*y[t],f'odd endpoint recurrence {t}')
    zero(x[t]*star(x[t])-1,f'formal unimodularity even {t}')
    zero(y[t]*star(y[t])-1,f'formal unimodularity odd {t}')
    zero(e[t]*x[t]*y[t]-e[0]*lam**(2*t),f'endpoint product e {t}')
    zero(d[t]*x[t]*y[(t-1)%4]-e[0]*lam**(2*t-1),f'endpoint product d {t}')

K=s.zeros(8)
for j in range(8): K[(j-2)%8,j]=b[j]/b[(j-1)%8]
for parity,v in [(0,x),(1,y)]:
    vfull=s.zeros(8,1); vopp=s.zeros(8,1)
    for t in range(4):
        vfull[2*t+parity]=v[t]
        vopp[2*t+parity]=omega**t*v[t]
    matzero(K*vfull-lam*vfull,f'K endpoint parity {parity}')
    matzero(K*vopp-lam**-1*vopp,f'K opposite endpoint parity {parity}')

# Normalization 1/2 is exact for the four-point Fourier transform.
def four(v,k): return clean(sum(v[t]*omega**(-k*t) for t in range(4))/2)
X=[four(x,n) for n in range(4)]; Y=[four(y,n) for n in range(4)]
D=[four([d[t]*x[t] for t in range(4)],n) for n in range(4)]
E=[four([e[t]*y[t] for t in range(4)],n) for n in range(4)]
for k in range(4):
    zero(D[k]-e[0]*lam**-1*omega**(-k-1)*star(Y[(-k-1)%4]),f'Fourier D identity {k}')
    zero(E[k]-e[0]*star(X[(-k-1)%4]),f'Fourier E identity {k}')

# Elimination coefficient in equation (4.5), independent of unknown a_j.
for n in range(4):
    zero(lam**-1*omega**(n-1)*omega**(-n)-lam,f'nondividing elimination coefficient {n}')

# Conditional complementary support signs imply period four for B.
xx,yy=s.symbols('x y',nonzero=True)
for eta in [1,-1]:
    xv=[1,xx,eta,eta*xx]; yv=[1,yy,-eta,-eta*yy]
    ev=[clean(lam**(2*t)/(xv[t]*yv[t])) for t in range(4)]
    dv=[clean(lam**(2*t-1)/(xv[t]*yv[(t-1)%4])) for t in range(4)]
    for t in range(2):
        zero(dv[t+2]-dv[t],f'support implies even B periodic eta={eta} t={t}')
        zero(ev[t+2]-ev[t],f'support implies odd B periodic eta={eta} t={t}')
    zero(s.prod(dv)/s.prod(ev)+1,f'support reconstructed Gamma=-1 eta={eta}')

# Exact full C8 Fourier construction for arbitrary four-periodic A,B.
a=s.symbols('a0:4'); bb=s.symbols('beta0:4')
Z=s.Matrix(8,8,lambda j,k:zeta**(-j*k))
A=s.diag(*(list(a)*2)); B=s.diag(*(list(bb)*2))
C=(Z*A*Z)/8
C=C.applyfunc(clean)
U=C*B
S=s.zeros(8)
for j in range(8): S[(j+1)%8,j]=1
H=S**4
matzero(C*S-S.T*C,'cyclic Hankel intertwining')
matzero(U*H-H*U,'half-shift commutation')
for j in range(8):
    for k in range(8):
        if (j-k)%2: zero(C[j,k],f'opposite-parity C zero {j},{k}')
p=(a[0]+a[2])/2; q=(a[0]-a[2])/2
r=(a[1]+a[3])/2; t=-I*(a[1]-a[3])/2
expected={
    (0,1):s.Matrix([[p*bb[0],q*bb[2]],[q*bb[0],p*bb[2]]]),
    (0,-1):s.Matrix([[r*bb[0],t*bb[2]],[t*bb[0],-r*bb[2]]]),
    (1,1):s.Matrix([[q*bb[1],p*bb[3]],[p*bb[1],q*bb[3]]]),
    (1,-1):s.Matrix([[t*bb[1],-r*bb[3]],[-r*bb[1],-t*bb[3]]])}
for parity in [0,1]:
    for eta in [1,-1]:
        V=s.zeros(8,2)
        for col,j in enumerate([parity,parity+2]):
            V[j,col]=1;V[j+4,col]=eta
        block=(V.T*U*V)/2
        matzero(U*V-V*expected[(parity,eta)],f'invariant block action {(parity,eta)}')
        matzero(block-expected[(parity,eta)],f'block formula {(parity,eta)}')

# Flat unitary-eigenvector spectral decomposition has equal diagonal entries.
z,z1,z2=s.symbols('z z1 z2',nonzero=True)
P=s.Matrix([[1,1/z],[z,1]])/2
Q=s.eye(2)-P
matzero(P*P-P,'flat projector idempotence')
zero((z1*P+z2*Q)[0,0]-(z1*P+z2*Q)[1,1],'flat eigenvector forces equal diagonals')
pp,rr,b0,b2=s.symbols('p r b0 b2')
zero(rr*(pp*(b0-b2))+pp*(rr*(b0+b2))-2*pp*rr*b0,'explicit nonzero-factor contradiction certificate')

# Legal original-model upper witness, exact real core and residual Gram.
F=Z/s.sqrt(8); V=zeta*F
Y=(V-s.conjugate(V))/(2*I)
Y=Y.applyfunc(clean)
Xcore=((V+s.conjugate(V))/2).applyfunc(clean)
matzero(s.conjugate(Xcore)-Xcore,'upper core is real')
matzero(F-(s.conjugate(zeta)*Xcore)-s.conjugate(zeta)*I*Y,'external residual identity')
matzero(Y.T*Y-s.eye(8)/2,'upper residual Gram exactly I/2')

result={
 'verdict':'PASS',
 'exact_assertions':len(checks),
 'arithmetic':'SymPy exact symbolic rational expressions in formal unit phases and Q(i,sqrt(2))',
 'coverage':[
  'generic Gamma=-1 weighted endpoint cycles and opposite modulation',
  'formal unimodularity and product recurrences',
  'exact four-point Fourier identities and nondividing elimination coefficient',
  'both complementary-support signs imply half-periodicity',
  'arbitrary four-periodic A,B full eight-point Fourier invariant blocks',
  'flat two-dimensional projector and explicit contradiction certificate',
  'legal real-core external residual with exact norm 1/sqrt(2)'],
 'limits':'Finite exact controls check algebraic identities; the all-phase exclusion and strictness follow from PROOF.md, not sampling or optimization.'}
(OUT/'EXACT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
