"""Fresh symbolic transcription controls; no supplied programs are imported."""
import json
from pathlib import Path
import sympy as sp

u, x, w, z = sp.symbols('u x w z')
I = sp.I
# u=exp(i*t), but the identities below hold in Q(i)(u).
sin_t = (u - 1/u)/(2*I)
sin_3t = (u**3 - 1/u**3)/(2*I)
cos_t = (u + 1/u)/2
cos_3t = (u**3 + 1/u**3)/2
s = sp.factor(sin_3t/(1-sin_t))
L = sp.factor(cos_3t+s*cos_t)
E = -I*u**5
lam = sp.factor(E*L)
a = [E/u**3, s*E/u, s*E*u, E*u**3]

checks = {}
def check(label, expr):
    residue = sp.factor(sp.cancel(expr))
    assert residue == 0, (label, residue)
    checks[label] = {'exact_residue': '0', 'passed': True}

S = [sp.Integer(1), x]
for aj in a:
    S.append(sp.factor(x*S[-1]-aj*S[-2]))
check('lower_S3', S[3]-x*(x*x-E*(L-I*s)))
check('characteristic_S5', S[5]-x*(x*x-lam)**2)
C1 = w-a[0]-a[1]
C2 = sp.expand(w*w-sum(a)*w+a[0]*a[2]+a[0]*a[3]+a[1]*a[3])
beta = a[1]*a[2]
check('contracted_C2', C2-(w-lam)**2)
check('C1_at_double_root', C1.subs(w,lam)-I*s*E)
check('beta_nonzero_expression', beta-s*s*E*E)
K2 = C1*C1+beta
check('kernel_cancellation', K2.subs(w,lam))
check('ordinary_kernel_identity', K2-(sp.diff(C2,w)*C1-C2*sp.diff(C1,w)))
check('reciprocal_identity', (z+1)*z*z*C2.subs(w,z+2+1/z)
      -(z+1)*(z*z+(2-lam)*z+1)**2)
check('simple_zero_derivative', sp.diff(S[5],x).subs(x,0)-lam**2)
q = sp.symbols('q')
d0 = 2-q-q*q
d1 = 2-q**3-q**4
beta_actual = (1-q*q)*(1-q**3)
check('actual_degree2_phase_ratio', (d1-d0)**2/beta_actual
      -q*q*(1+q)**2*(1-q*q)/(1-q**3))

output = {
    'arithmetic': 'exact rational functions over Q(i)(u), plus Q(q)',
    'purpose': 'transcription controls for the displayed analytic proofs',
    'actual_family_discriminant_inference': None,
    'checks': checks,
    'all_passed': all(c['passed'] for c in checks.values()),
}
Path(__file__).with_name('EXACT_CHECKS.json').write_text(
    json.dumps(output, indent=2)+'\n')
print(json.dumps({'checks': len(checks), 'all_passed': output['all_passed']}))
