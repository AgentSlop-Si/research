"""Fresh exact controls for the frozen kernel-metric mechanism review.
No historical program imports. No ordinary-squarefreeness census.
"""
from pathlib import Path
import hashlib, json
import sympy as S
BASE=Path('/workspace/shared/f020_kernel_metric_obstruction_20261019_0038')
OUT=Path(__file__).resolve().parent
EXPECTED='0021b58bc86300759b5bc0640082525b531220244abdfbce07bfc8bc27cedaaf'
checks=[]
def record(name, condition, **details):
    assert condition, (name,details)
    checks.append(dict(name=name,passed=True,**details))
def eq(name, value):
    val=S.cancel(S.expand(value))
    record(name,val==0,exact_difference=str(val))
def digest(data): return hashlib.sha256(data).hexdigest()
manifest=json.loads((BASE/'MANIFEST.json').read_text())
record('frozen manifest digest',digest((BASE/'MANIFEST.json').read_bytes())==EXPECTED)
for item in manifest['files']:
    raw=(BASE/item['path']).read_bytes()
    record('frozen bytes: '+item['path'],len(raw)==item['bytes'] and digest(raw)==item['sha256'])
for source in json.loads((BASE/'SOURCE_BINDINGS.json').read_text())['sources']:
    copy=(BASE/source['file']).read_bytes()
    original=Path(source['source_local_path']).read_bytes()
    record('source local binding: '+source['file'],copy==original and digest(copy)==source['sha256'])
record('author replay output byte match',(OUT/'author_replay/CHECKS.json').read_bytes()==(BASE/'CHECKS.json').read_bytes())
record('author replay code byte match',(OUT/'author_replay/check_metric_obstructions.py').read_bytes()==(BASE/'check_metric_obstructions.py').read_bytes())

# Reconstruct symmetric Jacobi matrices with independent formal edge roots.
x,q=S.symbols('x q')
a,b,c=S.symbols('a b c',nonzero=True)
J=S.Matrix([[0,a,0,0],[a,0,b,0],[0,b,0,c],[0,0,c,0]])
char=J.charpoly(x).as_expr()
eq('symmetric J4 characteristic polynomial',char-(x**4-(a*a+b*b+c*c)*x*x+a*a*c*c))
p=[S.Integer(1),x]
for k in range(1,4): p.append(S.expand(x*p[-1]-(1-q**k)*p[-2]))
eq('formal symmetric edges recover actual P4',char.subs({a*a:1-q,b*b:1-q*q,c*c:1-q**3})-p[4])
v=S.Matrix([1,x/a,(x*x-a*a)/(a*b),(x**3-(a*a+b*b)*x)/(a*b*c)])
res=J*v-x*v
for k in range(3): eq('Jacobi eigenvector recursion row '+str(k),res[k])
eq('Jacobi eigenvector terminal row',res[3]+char/(a*b*c))
AA=3-q-q**2-q**3; BB=(1-q)*(1-q**3)
eq('quartic discriminant',S.discriminant(p[4],x)-16*BB*(AA**2-4*BB)**2)

# Rational unit-circle parameter avoids using the author's c,s reduction.
t=S.symbols('t',real=True)
qq=(1+S.I*t)/(1-S.I*t)
rat=S.cancel((BB/AA**2).subs(q,qq))
imag=S.factor(S.cancel((rat-S.conjugate(rat))/(2*S.I)))
cc=(1-t*t)/(1+t*t); ss=2*t/(1+t*t)
formula=-(1+2*cc)*ss*cc*(cc+2)/(4*((1+2*cc)**2+ss**2)**2)
eq('independent rational-unit-circle imaginary invariant',imag-formula)
record('invariant not identically real',imag!=0,factored_imaginary_part=str(imag))
eq('actual edge-product ratio',S.cancel((1-q**2)/(1-q))-(1+q))

# Generic diagonal similarity: edge products do not change.
d0,d1,d2,d3=S.symbols('d0:4',nonzero=True)
DD=S.diag(d0,d1,d2,d3); TT=DD.inv()*J*DD
for k,edge in enumerate([a,b,c]): eq('diagonal similarity product '+str(k),TT[k,k+1]*TT[k+1,k]-edge**2)

# Full noncommutative block bookkeeping, not scalar-block stand-in.
MM=S.Matrix(2,2,S.symbols('m0:4')); NN=S.Matrix(2,2,S.symbols('n0:4'))
LL=S.Matrix(2,2,S.symbols('l0:4')); CC=S.Matrix([[0,0],[S.Symbol('edge'),0]])
JJ=S.Matrix([[0,S.Symbol('a')],[S.Symbol('a'),0]])
KK=S.Matrix([[0,S.Symbol('b')],[S.Symbol('b'),0]])
FULL=JJ.row_join(CC).col_join(CC.T.row_join(KK))
WW=MM.row_join(NN).col_join(NN.H.row_join(LL))
defect=WW*FULL-FULL.H*WW
expected=MM*JJ-JJ.H*MM+NN*CC.T-S.conjugate(CC)*NN.H
for i in range(2):
    for j in range(2): eq('full matrix compression entry '+str(i)+str(j),defect[i,j]-expected[i,j])

# Source recurrence checks at already covered orders, merely transcription controls.
# Every full-order identity below is independently proved symbolically in the review.
for order in [3,5,9]:
    phi=S.cyclotomic_poly(order,q)
    pp=[S.Integer(1),x]
    hh=[S.Integer(1),1+x]
    for k in range(1,order):
        pp.append(S.rem(S.expand(x*pp[-1]-(1-q**k)*pp[-2]),phi,q))
        hh.append(S.rem(S.expand((1+x)*hh[-1]-x*(1-q**k)*hh[-2]),phi,q))
    eq('full-order Chebyshev transcription d='+str(order),pp[order]-2*S.chebyshevt(order,x/2))
    eq('full-order H transcription d='+str(order),hh[order]-(1+x**order))

# Telescoping rational identity for the finite sine sum, with independent unit roots.
z,r=S.symbols('z r',nonzero=True)
# z=e^(i theta/2), r=z^(b-1). Then sum sin(k theta)=
# ((z^2-z^(2b))/(1-z^2) - (z^-2-z^-2b)/(1-z^-2))/(2i).
geom=((z**2-z**2*r**2)/(1-z**2)-(z**-2-z**-2*r**-2)/(1-z**-2))/(2*S.I)
prod=((r-r**-1)/(2*S.I))*((r*z-(r*z)**-1)/(2*S.I))/((z-z**-1)/(2*S.I))
eq('uniform finite sine-sum rational identity',geom-prod)
# Residual reflection holds without imposing root order and explicitly preserves defect.
Q=S.symbols('Q',nonzero=True)
eq('residual reflection identity',(1-Q/z)-((1-Q)+Q*(1-1/z)))

# Reverify frozen input after all execution.
for item in manifest['files']:
    raw=(BASE/item['path']).read_bytes()
    record('post-run frozen bytes: '+item['path'],len(raw)==item['bytes'] and digest(raw)==item['sha256'])
record('post-run frozen manifest digest',digest((BASE/'MANIFEST.json').read_bytes())==EXPECTED)
result={'all_passed':True,'assertion_count':len(checks),'checks':checks,'root_order_census':False,'external_writes':False,'historical_programs_executed':False}
(OUT/'INDEPENDENT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS:',len(checks),'independent exact/source-integrity assertions')
print('Independent rational-unit-circle factorization:',imag)
