"""Fresh bounded exact controls; never imports or executes supplied research code."""
import json
from pathlib import Path
import sympy as sp

q, z, x, y = sp.symbols('q z x y')
rows=[]
for N in (3,5,7,9,11,13,15,17,21,25):
    m=(N-1)//2
    h=(N+1)//2
    phi=sp.Poly(sp.cyclotomic_poly(N,q),q,domain=sp.ZZ)
    def red(v):
        return sp.Poly(v,q,domain=sp.ZZ).rem(phi).as_expr()
    def add(a,b):
        return [red((a[j] if j<len(a) else 0)+(b[j] if j<len(b) else 0))
                for j in range(max(len(a),len(b)))]
    polys=[[sp.Integer(1)],[sp.Integer(-1),sp.Integer(1)]]
    for n in range(2,N+1):
        p=polys[-1]
        first=add([0]+p,[-c for c in p])
        second=[0]+[red((1-q**(n-1))*c) for c in polys[-2]]
        polys.append(add(first,second))
    tm=polys[m]
    assert tm[0]==(-1)**m and tm[-1]==1
    assert all(red(tm[j]-(-1)**m*tm[m-j])==0 for j in range(m+1))
    for k in range(m):
        assert red(sum(tm[j]*q**((h*(k+j+1)**2)%N) for j in range(m+1)))==0
    # Direct ordinary differential apolarity, independent of moment-matrix indexing.
    d=2*m-1
    F=sum(sp.binomial(d,k)*q**((h*(k+1)**2)%N)*x**(d-k)*y**k for k in range(d+1))
    AF=sum(tm[j]*sp.diff(F,x,m-j,y,j) for j in range(m+1))
    assert all(red(coef)==0 for coef in sp.Poly(sp.expand(AF),x,y).coeffs())
    terminal=polys[N]
    assert terminal[0]==-1 and terminal[N]==1 and all(c==0 for c in terminal[1:N])
    # Variable conversion uses a formal square-root r, checked as a Laurent identity.
    r=sp.Symbol('r')
    ss=[sp.Integer(1),x]
    for n in range(2,m+1):
        ss.append(sp.expand(x*ss[-1]-(1-q**(n-1))*ss[-2]))
    conv=sp.expand((sp.I*r)**m*ss[m].subs(x,(r*r-1)/(sp.I*r)))
    expected=sum(tm[j]*r**(2*j) for j in range(m+1))
    assert all(red(c)==0 for c in sp.Poly(sp.expand(conv-expected),r).coeffs())
    resonant=[]
    for k in range(N):
        if red(sum(tm[j]*q**((k*j)%N) for j in range(m+1)))==0:
            resonant.append(k)
    assert resonant==([0] if m%2 else [])
    if m%2:
        assert red(sum(j*tm[j] for j in range(1,m+1)))!=0
    rows.append({'N':N,'m':m,'phi_degree':phi.degree(),
                 'annihilator_rows_checked':m,'ordinary_derivative_apolarity':True,
                 'reciprocity_and_nonzero_constant':True,'chirp_hermite_map':True,
                 'terminal_polynomial':'z^N-1','resonant_exponents':resonant,
                 'resonant_root_simple': bool(m%2) if resonant else None})

us=[None,1,-1,1,2]
p=[sp.Integer(1),x]
for n in range(1,5):
    p.append(sp.expand(x*p[-1]-us[n]*p[-2]))
g3=sp.gcd(p[3],sp.diff(p[3],x))
g5=sp.gcd(p[5],sp.diff(p[5],x))
assert p[3]==x**3 and p[5]==x**5-3*x**3+x and g3==x*x and g5==1
assert sp.discriminant(p[5],x)==400
pe=[sp.Integer(1),x]
for u in (1,-4,1,1):
    pe.append(sp.expand(x*pe[-1]-u*pe[-2]))
assert pe[4]==(x**4+2*x*x+1)
assert sp.gcd(pe[4],sp.diff(pe[4],x))==x*x+1
assert sp.gcd(pe[4],pe[3])==1
assert sp.gcd(pe[5],sp.diff(pe[5],x))==1
assert sp.discriminant(pe[5],x)==-10368
nodes=[0,1,-1,sp.I*sp.sqrt(2),-sp.I*sp.sqrt(2)]
weights=[2,-sp.Rational(1,6),-sp.Rational(1,6),-sp.Rational(1,3),-sp.Rational(1,3)]
gram=sp.Matrix([[sp.simplify(sum(w*(pe[i]*pe[j]).subs(x,t) for t,w in zip(nodes,weights)))
                 for j in range(5)] for i in range(5)])
assert gram==sp.diag(1,1,-4,-4,-4)
result={'method':'Fresh SymPy exact integer cyclotomic quotient checks; no archived programs imported or run',
        'scope':'Bounded identity and nontransfer controls, not all-composite squarefreeness',
        'chirp_controls':rows,
        'generic_not_chirp_counterexample':{'u':[1,-1,1,2], 'b':[0]*5,
               'polynomials':[str(t) for t in p], 'gcd_P3_derivative':str(g3),
               'gcd_P5_derivative':str(g5),'disc_P5':400},
        'candidate_even_degree_counterexample_independently_checked':{
             'u':[1,-4,1,1],'b':[0]*5,
             'polynomials':[str(t) for t in pe],
             'gcd_P4_derivative':'x**2 + 1','gcd_P4_P3':'1',
             'gcd_P5_derivative':'1','disc_P5':-10368,
             'finite_functional_entries_checked':25,
             'finite_orthogonality_norms':[1,1,-4,-4,-4]}}
path=Path(__file__).with_name('CHECK_RESULTS.json')
path.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'PASS':True,'N_cases':len(rows),'annihilator_rows':sum(v['m'] for v in rows),
                  'generic_counterexample_discriminant':400,'results_file':str(path)}))
