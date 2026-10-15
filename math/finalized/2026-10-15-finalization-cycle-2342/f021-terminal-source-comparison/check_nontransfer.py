"""Fresh bounded algebra controls; no predecessor or downloaded code imported."""
import json
from pathlib import Path
import sympy as s

x, z, q = s.symbols('x z q')
p = [s.Integer(1), x]
for u in (1, -4, 1, 1):
    p.append(s.expand(x*p[-1] - u*p[-2]))
assert p[4] == s.expand((x*x+1)**2)
assert p[5] == s.expand(x*(x*x-1)*(x*x+2))
assert s.gcd(p[4], s.diff(p[4],x)) == x*x+1
assert s.gcd(p[5], s.diff(p[5],x)) == 1
assert s.gcd(p[4],p[5]) == 1
nodes_weights = [(0, s.Integer(2)), (1, -s.Rational(1,6)),
                 (-1, -s.Rational(1,6)), (s.I*s.sqrt(2), -s.Rational(1,3)),
                 (-s.I*s.sqrt(2), -s.Rational(1,3))]
norms = [1,1,-4,-4,-4]
for i in range(5):
    for j in range(5):
        val = s.simplify(sum(w*p[i].subs(x,a)*p[j].subs(x,a) for a,w in nodes_weights))
        assert val == (norms[i] if i == j else 0)

terminal_checks = []
for N in (3, 5, 9):
    phi = s.Poly(s.cyclotomic_poly(N,q),q)
    def red(expr):
        poly = s.Poly(s.expand(expr),z)
        return s.expand(sum(s.rem(s.Poly(c,q),phi).as_expr()*z**j[0]
                            for j,c in poly.terms()))
    t0, t1 = s.Integer(1), z-1
    for n in range(2,N+1):
        t0, t1 = t1, red((z-1)*t1 + (1-q**(n-1))*z*t0)
    assert red(t1-(z**N-1)) == 0
    terminal_checks.append({'N':N, 'identity':'T_N(z)=z^N-1', 'passed':True})

out = {
    'scope':'Fresh bounded symbolic controls of nontransfer arguments; not chirp composite squarefreeness certification.',
    'generic_recurrence_u':[1,-4,1,1],
    'polynomials':[str(s.factor(v)) for v in p],
    'gcd_P4_derivative':str(s.gcd(p[4],s.diff(p[4],x))),
    'gcd_P5_derivative':str(s.gcd(p[5],s.diff(p[5],x))),
    'gcd_P4_P5':str(s.gcd(p[4],p[5])),
    'finite_orthogonality_entries_checked':25,
    'finite_orthogonality_norms':norms,
    'terminal_controls':terminal_checks,
    'sympy_version':s.__version__,
    'formal_verification':False,
}
Path(__file__).with_name('CHECK_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
