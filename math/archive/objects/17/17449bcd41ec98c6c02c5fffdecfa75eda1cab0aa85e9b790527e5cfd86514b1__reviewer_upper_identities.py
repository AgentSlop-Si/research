"""Exact independent polynomial checks of the C01 uniform upper identities."""
import json
from pathlib import Path
import sympy as s
a,b,g,e,d=s.symbols('alpha beta gamma epsilon d')
L=b*b-g*e;M=-2*a*b+a*g+a*e+b*g+b*e-2*g*e;J=(b-g)**2
lhs=(b-g)*(b*d*d+(b-a)*d+b-g)-(e-b)*d*(g*d+2*g-a-b)
assert s.expand(lhs-(L*d*d+M*d+J))==0
h=a+b
norm_identity=J*(g*g*L-g*h*M+h*h*J)-(g*g*J*L-g*(2*g-h)*M*L+(2*g-h)**2*L*L)
assert s.expand(norm_identity)==0
Path(__file__).with_name('reviewer_upper_identity_results.json').write_text(json.dumps({'coefficient_ring':'Z[alpha,beta,gamma,epsilon,d]','expanded_identities':2,'both_zero':True},indent=2)+'\n')
