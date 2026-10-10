"""Fresh exact rational-polynomial verification of the N=9 proof identities."""
import json
from pathlib import Path
import sympy as s
q,v=s.symbols('q v');phi=q**6+q**3+1
red=lambda e:s.rem(s.expand(e),phi,q)
R=s.Poly(q**4*s.prod(v-q**(((a+1)*5)%9) for a in range(1,5)),v)
p={k:red(R.nth(k)*q**((-k*k*7)%9)) for k in range(5)}
expected={0:q**2,1:q**4-q**2+q+1,2:-q**4+2*q**2-1,3:-q**5+q**3-q**2-q+1,4:1}
assert all(red(p[k]-expected[k])==0 for k in p)
E=red((1+q)**2*(p[2]-1-q*q)-q*p[3]*p[3]);V=2*q**5-q**4+3*q*q-3*q+2
checks={
 'p1_equals_q_p3':red(p[1]-q*p[3])==0,
 'p3_inverse':red(p[3]*(q*q+1)-1)==0,
 'E_formula':E==q**5-q**4+2*q*q-2*q-3,
 'bezout_residue_is_three':red(E*V)==3,
 'all_characteristic_scope':'The identities have integer coefficients. Characteristic not dividing 9 makes the residue 3 nonzero.'
}
assert all(v for v in checks.values())
result={'N':9,'cyclotomic_polynomial':str(phi),'recurrence_coefficients':{str(k):str(v) for k,v in p.items()},'obstruction':str(E),'bezout_multiplier':str(V),'bezout_quotient':str(s.div(s.expand(E*V-3),phi,q)[0]),'checks':checks}
Path(__file__).with_name('fresh_nine_certificate_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
