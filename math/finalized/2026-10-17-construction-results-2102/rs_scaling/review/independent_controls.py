"""Independent final-review controls. No candidate code is run or imported."""
import json, hashlib
from pathlib import Path
from fractions import Fraction
import sympy as sp
import mpmath as mp
ROOT = Path(__file__).resolve().parent.parent / 'candidate'
OUT = Path(__file__).resolve().parent
report = {'scope':'Independent exact algebraic controls and numerical matrix diagnostics; not a production implementation or universal floating-point error claim.'}
manifest = json.loads((ROOT/'MANIFEST.json').read_text())
pins=[]
for entry in manifest['files']:
    raw = (ROOT/entry['path']).read_bytes()
    assert len(raw)==entry['bytes']
    assert hashlib.sha256(raw).hexdigest()==entry['sha256']
    pins.append(entry)
report['frozen_inputs'] = {'manifest_sha256':hashlib.sha256((ROOT/'MANIFEST.json').read_bytes()).hexdigest(),'members_verified':len(pins),'members':pins}
# An independently constructed normal commuting bank with zero branch and varying signs.
I=sp.I
lambdas=[1,I,-1,-I]
weights=[[2,-1,0,0],[-2,3,0,0],[3,-3,1,0],[5,-2,-2,0]]
b=[[lambdas[k]*weights[k][j] for j in range(4)] for k in range(4)]
chi=max(sum(abs(v) for v in row) for row in b)
assert chi==9
u=sp.Rational(1,18)
delta=[-u,u,u,0]
errors=[sp.expand(sum(delta[j]*b[k][j] for j in range(4))) for k in range(4)]
assert max(abs(v) for v in errors)==u*chi
inverse_errors=[sp.simplify(1/(lambdas[k]+errors[k])-1/lambdas[k]) for k in range(4)]
assert max(abs(v) for v in inverse_errors)==u*chi/(1-u*chi)==1
# Boundary and supercritical radii include a singular perturbation, using <=u.
singular_delta=[-sp.Rational(1,9),sp.Rational(1,9),sp.Rational(1,9),0]
assert lambdas[3]+sum(singular_delta[j]*b[3][j] for j in range(4))==0
blowup=[]
for power in [2,4,8,16]:
    scale=1-sp.Rational(1,2**power)
    perturb=scale*sum(singular_delta[j]*b[3][j] for j in range(4))
    error=sp.simplify(abs(1/(lambdas[3]+perturb)-1/lambdas[3]))
    assert error==2**power-1
    blowup.append({'distance_to_singular_fraction':str(1-scale),'inverse_error':str(error)})
# Two distinctly nonunitary, nondiagonal exact compensated basis changes.
H=sp.diag(*lambdas)
E=sp.diag(*errors)
branches=[sp.diag(*[b[k][j] for k in range(4)]) for j in range(4)]
for S in [sp.Matrix([[1,2,0,0],[0,1,3,0],[0,0,1,4],[0,0,0,1]]),sp.Matrix([[1,I,0,0],[0,2,1,0],[0,0,3,I],[1,0,0,4]])]:
    Si=S.inv()
    transformed=sum(((1+delta[j])*Si*branches[j]*S for j in range(4)),sp.zeros(4))
    assert sp.simplify(S*transformed*Si)==H+E
    assert sp.simplify(S*transformed.inv()*Si)==(H+E).inv()
report['exact_adversarial_branch_model']={'chi':str(chi),'u':str(u),'forward_supremum':str(u*chi),'inverse_supremum':str(u*chi/(1-u*chi)),'zero_branch_included':True,'nondiagonal_similarities_checked':2,'singular_boundary_checked':True,'near_boundary_checks':blowup}
# Exact independent rational flat unitary, complex diagonal ranges, and physical output errors.
U=sp.Matrix([[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]])/2
assert U*U.H==sp.eye(4)
flat_cases=[]
mp.mp.dps=70
for ds in [[1,2*I,-3,4*I],[sp.Rational(1,8),2*I,-sp.Rational(3,2),-4],[8**j for j in range(4)]]:
    ds=[sp.sympify(v) for v in ds]
    D=sp.diag(*ds);Di=D.inv();A=Di*U*D;Ai=Di*U.H*D
    magnitudes=[abs(v) for v in ds];lo=min(range(4),key=lambda k:magnitudes[k]);hi=max(range(4),key=lambda k:magnitudes[k]);kappa=magnitudes[hi]/magnitudes[lo]
    assert A*Ai==sp.eye(4)
    assert abs(A[lo,hi])==abs(Ai[lo,hi])==kappa/2
    uu=sp.Rational(1,1000)
    ei=sp.eye(4)[:,lo];ej=sp.eye(4)[:,hi]
    dz=uu/magnitudes[lo]*ej
    vector_norm=lambda v:sp.sqrt(sp.expand((v.H*v)[0]))
    for target in [U,U.H]:
        x=target.H*ei
        z=Di*target*x
        assert vector_norm(dz)==uu*vector_norm(z)
        assert sp.simplify(vector_norm(D*dz)/vector_norm(target*x))==uu*kappa
    # Absolute-error control has factor ||D||, not kappa(D), unless input normalization matches.
    eta=sp.Rational(1,100)
    assert vector_norm(D*(eta*ej))==eta*max(magnitudes)
    vals=mp.svd(mp.matrix([[complex(v.evalf(50)) for v in row] for row in A.tolist()]),compute_uv=False)
    cond=vals[0]/vals[3]
    assert cond>=mp.mpf(str(kappa*kappa))/4*(1-mp.mpf('1e-12'))
    flat_cases.append({'diagonal':[str(v) for v in ds],'kappa_D':str(kappa),'condition_lower_bound':str(kappa*kappa/4),'numerical_condition':mp.nstr(cond,20),'exact_both_direction_amplification':str(kappa)})
report['flat_unitary_and_decode_cases']=flat_cases
# Radial-generator and wrap controls with poles both inside and outside unit disk.
radial_count=0
for N in [4,6,10]:
    T=sp.zeros(N)
    for k in range(N-1):T[k+1,k]=1
    T[0,N-1]=-1
    assert T**N==-sp.eye(N)
    r=sp.Integer(8);D=sp.diag(*[r**k for k in range(N)]);S=D.inv()*T*D
    assert S[0,N-1]==-r**(N-1)
    assert all(S[k+1,k]==1/r for k in range(N-1))
    assert S**N==-sp.eye(N)
    for alpha in [sp.Rational(1,2),sp.Rational(3,2),3+4*I]:
        normalized=alpha/r
        assert sp.expand(normalized**N*r**N-alpha**N)==0
        original=sp.eye(N)-alpha*T
        assert original==sp.eye(N)-normalized*(r*T)
        assert D*(sp.eye(N)-alpha*S).inv()*D.inv()==original.inv()
        assert original!=sp.eye(N)-normalized*T
        radial_count+=1
report['radial_resolvent_cases']=radial_count
# Symbolic exponent and threshold arithmetic, not extrapolated finite data.
n=sp.symbols('n',integer=True,positive=True)
assert sp.expand(7*n/sp.Integer(11)-2-sp.Rational(9,8)*(n/2+1))==13*n/sp.Integer(176)-sp.Rational(25,8)
assert (13*n/sp.Integer(176)-sp.Rational(25,8)).subs(n,44)==sp.Rational(1,8)
for N in [4,44,128,1024]:
    assert 8**(N-1)==2**(3*(N-1))
    assert 64**(N-1)==2**(6*(N-1))
    p=53
    required=Fraction(1,2**(p+3*(N-1)))
    assert required*8**(N-1)==Fraction(1,2**p)
report['range_accuracy_bits_checked']=[4,44,128,1024]
report['all_checks_passed']=True
(OUT/'RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'all_checks_passed':True,'manifest_members':len(pins),'exact_branch_cases':1,'basis_changes':2,'flat_unitary_cases':len(flat_cases),'radial_cases':radial_count}))
