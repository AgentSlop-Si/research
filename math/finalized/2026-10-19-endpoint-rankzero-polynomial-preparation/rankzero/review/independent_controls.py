"""Original independent exact controls. Does not import/run any candidate code."""
from pathlib import Path
import json, hashlib, sympy as s
ROOT=Path(__file__).resolve().parent
SRC=Path('/workspace/shared/phase_rankzero_20261019_1053')
checks=0

def check(condition, name):
    global checks
    if not condition: raise AssertionError(name)
    checks+=1

def zero(expr,name): check(s.cancel(s.expand(expr))==0,name)

manifest=json.loads((SRC/'MANIFEST.json').read_text())
source=[]
for row in manifest['files']:
    data=(SRC/row['path']).read_bytes()
    sha=hashlib.sha256(data).hexdigest()
    check(len(data)==row['bytes'] and sha==row['sha256'],'source integrity '+row['path'])
    source.append({'path':row['path'],'bytes':len(data),'sha256':sha,'matches':True})
(ROOT/'SOURCE_HASH_VERIFICATION.json').write_text(json.dumps({'manifest_sha256':hashlib.sha256((SRC/'MANIFEST.json').read_bytes()).hexdigest(),'files':source},indent=2)+'\n')

# First route: direct formal 8-point Fourier sums and explicit sector embeddings.
a=s.symbols('a0:4',nonzero=True); b=s.symbols('b0:4',nonzero=True)
i=s.I; rt=(1+i)/s.sqrt(2)
powers=[s.expand(rt**k) for k in range(8)]
C=s.Matrix(8,8,lambda j,k:s.expand(sum(a[l%4]*powers[(-l*(j+k))%8] for l in range(8))/8))
B=s.diag(*(b[j%4] for j in range(8))); U=C*B
S=s.zeros(8)
for j in range(8): S[(j+1)%8,j]=1
H=S**4
check(C*S==S.T*C,'formal cyclic-Hankel')
check(C*H==H*C and B*H==H*B,'formal half shift commutation')
alpha=(a[0]+a[2])/2; beta=(a[0]-a[2])/2
gamma=(a[1]+a[3])/2; delta=i*(a[3]-a[1])/2
expected={
(0,1):s.Matrix([[alpha,beta],[beta,alpha]])*s.diag(b[0],b[2]),
(0,-1):s.Matrix([[gamma,delta],[delta,-gamma]])*s.diag(b[0],b[2]),
(1,1):s.Matrix([[beta,alpha],[alpha,beta]])*s.diag(b[1],b[3]),
(1,-1):s.Matrix([[delta,-gamma],[-gamma,-delta]])*s.diag(b[1],b[3])}
K=S.T*B.inv()*S.T*B
rho=b[0]*b[2]/(b[1]*b[3]); x=s.Symbol('x')
for p in (0,1):
  for eta in (1,-1):
    Q=s.zeros(8,2)
    for col,j in enumerate((p,p+2)): Q[j,col]=1; Q[j+4,col]=eta
    block=s.simplify(Q.T*U*Q/2)
    for entry in block-expected[p,eta]: zero(entry,'sector identity')
    for entry in U*Q-Q*block: zero(entry,'sector invariance')
    kb=Q.T*K*Q/2
    target=x*x-eta*(rho if p==0 else 1/rho)
    zero(kb.charpoly(x).as_expr()-target,'commutator sector polynomial')
    check(kb[0,0]==0 and kb[1,1]==0,'commutator sector zero diagonal')
# Spectral-projector proof independently parametrized by a unit phase t.
t,z1,z2=s.symbols('t z1 z2',nonzero=True)
Pv=s.Matrix([[1,1/t],[t,1]])/2; Pw=s.eye(2)-Pv
check(Pv*Pv==Pv and Pw*Pw==Pw and Pv*Pw==s.zeros(2),'flat complementary projectors')
flat=z1*Pv+z2*Pw
zero(flat[0,0]-flat[1,1],'flat eigenvector equal diagonal')
check(flat.subs(z2,z1)==z1*s.eye(2),'repeated eigenvalue included')
# Saturation equations lead to the exact certificate 2*alpha*gamma*b0=0.
f=alpha*(b[0]-b[2]); g=gamma*(b[0]+b[2])
zero(gamma*f+alpha*g-2*alpha*gamma*b[0],'even-sector contradiction certificate')
# Destructive control: flatness is essential to equal diagonals.
r=s.Symbol('r',positive=True)
nonflat=s.Matrix([[1,r],[r,r*r]])/(1+r*r)
check(s.cancel((z1*nonflat+z2*(s.eye(2)-nonflat))[0,0]-(z1*nonflat+z2*(s.eye(2)-nonflat))[1,1])!=0,'nonflat control rejects equal-diagonal extension')

# Second route: independent cyclotomic computations for many even L.
# ANP arithmetic is exact rational arithmetic modulo a cyclotomic polynomial.
family=[]
for N in (4,8,12,16,20,24):
  L=N//2; m=N//4; order=4*N
  root=s.exp(2*s.pi*i/order); polynomial=s.Poly(s.cyclotomic_poly(order,s.Symbol('q')),s.Symbol('q'))
  field=s.QQ.algebraic_field((polynomial,root))
  z=field.unit; one=field.one; nul=field.zero
  Z=[one]
  for _ in range(1,order): Z.append(Z[-1]*z)
  def pw(n): return Z[n%order]
  def conj(v):
    out=nul
    for coeff in v.to_list(): out=out*Z[-1]+field.convert(coeff)
    return out
  omega=Z[8]; lam=Z[4*L-4]; u=Z[2*L-2]; zeta=Z[4]
  check(lam**2==omega**-1 and lam**L==-one and u**2==lam,'endpoint cyclotomic parameters')
  (ROOT/'CURRENT_STAGE.txt').write_text(str(N)+' root field ready')
  # Arbitrary flat endpoint cycles, deliberately not assuming Fourier parity support.
  xx=[Z[(q*q+3*q)%order] for q in range(L)]
  yy=[Z[(3*q*q+5*q)%order] for q in range(L)]
  e0=Z[7]
  dd=[e0*pw((4*L-4)*(2*q-1))*conj(xx[q])*conj(yy[(q-1)%L]) for q in range(L)]
  ee=[e0*pw((4*L-4)*(2*q))*conj(xx[q])*conj(yy[q]) for q in range(L)]
  bb=[val for pair in zip(dd,ee) for val in pair]
  gam=one
  for d,e in zip(dd,ee): gam*=d*conj(e)
  check(gam==-one,'two cycle products')
  for q in range(L):
    check(xx[(q+1)%L]==lam*ee[q]*conj(dd[(q+1)%L])*xx[q],'generic x recurrence')
    check(yy[(q+1)%L]==lam*dd[(q+1)%L]*conj(ee[(q+1)%L])*yy[q],'generic y recurrence')
    check(ee[q]*xx[q]*yy[q]==e0*pw((4*L-4)*(2*q)),'first product identity')
    check(dd[q]*xx[q]*yy[(q-1)%L]==e0*pw((4*L-4)*(2*q-1)),'second product identity')
  def ft(v): return [sum((v[q]*pw(-8*k*q) for q in range(L)),nul) for k in range(L)]
  X=ft(xx); Y=ft(yy); D=ft([dd[q]*xx[q] for q in range(L)]); E=ft([ee[q]*yy[q] for q in range(L)])
  bad_index=False
  for k in range(L):
    n=(-k)%L
    check(D[k]==e0*pw(-(4*L-4))*pw(8*(-k-1))*conj(Y[(-k-1)%L]),'D Fourier identity')
    check(E[k]==e0*conj(X[(-k-1)%L]),'E Fourier identity')
    aa=Z[(k*k+1)%order]
    r1=aa*D[k]-u*X[n]; r2=aa*E[k]-u*pw(8*k)*Y[n]
    elimination=E[k]*r1-D[k]*r2
    target=u*e0*(lam*Y[n]*conj(Y[(n-1)%L])-X[n]*conj(X[(n-1)%L]))
    check(elimination==target,'nondividing elimination identity')
    if E[k]!=e0*conj(X[(-k+1)%L]): bad_index=True
  if L>2: check(bad_index,'destructive Fourier index control')
  (ROOT/'CURRENT_STAGE.txt').write_text(str(N)+' Fourier elimination passed')
  # Full N-point transform residuals, including the odd-coordinate zeta factor.
  vx=[xx[j//2] if j%2==0 else nul for j in range(N)]
  vy=[yy[j//2] if j%2 else nul for j in range(N)]
  for j in range(N):
    aa=Z[(j*j+3*j)%order]; k=j%L
    for parity,v,expected_residual in [
      (0,vx,aa*D[k]-u*X[-k%L]),
      (1,vy,pw(-4*j)*(aa*E[k]-u*pw(8*k)*Y[-k%L]))]:
      direct=sum((aa*pw(-4*j*q)*bb[q]*v[q]-u*pw(4*j*q)*v[q] for q in range(N)),nul)
      check(direct==expected_residual,'full Fourier equation '+str(parity))
  (ROOT/'CURRENT_STAGE.txt').write_text(str(N)+' full Fourier residuals passed')
  # Converse support construction checks both signs and the shift of the second identity.
  for eta in (1,-1):
    xa=[Z[(q*q+q)%order] for q in range(m)]
    ya=[Z[(2*q*q+q)%order] for q in range(m)]
    xa=xa+[eta*v for v in xa]; ya=ya+[-eta*v for v in ya]
    d=[e0*pw((4*L-4)*(2*q-1))*conj(xa[q])*conj(ya[(q-1)%L]) for q in range(L)]
    e=[e0*pw((4*L-4)*(2*q))*conj(xa[q])*conj(ya[q]) for q in range(L)]
    for q in range(L):
      check(d[(q+m)%L]==d[q] and e[(q+m)%L]==e[q],'both support signs force half periodicity')
    xp=[pw(8*q)*xa[q] for q in range(L)]
    yp=[pw(8*q)*ya[q] for q in range(L)]
    for q in range(L): check(xp[(q+m)%L]==-eta*xp[q] and yp[(q+m)%L]==eta*yp[q],'opposite endpoint swaps sector signs')
  family.append({'N':N,'L':L,'arithmetic':'exact cyclotomic','passed':True})
  (ROOT/'PROGRESS.json').write_text(json.dumps(family,indent=2)+'\n')

# Third route: explicit upper-control residual using entrywise imaginary part.
F=s.Matrix(8,8,lambda j,k:powers[(-j*k)%8]/s.sqrt(8))
phase=(1+i)/s.sqrt(2); V=s.simplify(phase*F)
Y=V.applyfunc(lambda v:s.simplify(s.im(v)))
X=V.applyfunc(lambda v:s.simplify(s.re(v)))
check(s.simplify(Y.T*Y)==s.eye(8)/2,'upper-control imaginary Gram')
check(s.simplify(F-s.conjugate(phase)*X-s.conjugate(phase)*i*Y)==s.zeros(8),'external residual exactly unitary-rotated imaginary part')
check(s.simplify((F-s.conjugate(phase)*X).conjugate().T*(F-s.conjugate(phase)*X))==s.eye(8)/2,'upper-control external Gram')
# The theorem's non-sharp lower bound is strictly below this legal witness.
check(s.simplify(s.Rational(1,2)-s.sin(3*s.pi/16)**2).is_positive,'displayed interval correctly ordered by exact algebra (not a proof of strict optimum)')
report={'verdict':'PASS','assertions':checks,'family':family,'symbolic_sectors':'All four formal C8 sectors and characteristic polynomials','negative_controls':['Nonflat eigenvector rejects equal-diagonal extension','Incorrect Fourier index fails for L>2'],'legal_upper_control':'Exact external residual Gram I/2','limits':'Finite exact controls check algebraic identities only. The analytic review proves all-phase strictness and the infinite-family necessary condition. No candidate or historical code was executed.'}
(ROOT/'INDEPENDENT_EXACT_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
