"""Fresh exact adverse component control at s=7,p=13; reads only new result data."""
import json
from pathlib import Path
import sympy as S
q=S.symbols('q')
root=Path('research_cycle_0958/composite_guard')
s7=next(row for row in json.loads((root/'FRESH_AUGMENTED_CONTENT.json').read_text()) if row['s']==7)
poly=lambda text:S.Poly(S.sympify(text),q,modulus=13)
phi=poly(s7['phi']);delta=poly(s7['delta']);pair=poly(s7['pair']);aug=poly(s7['augmented'])
factors=[q*q+3*q+1,q*q+5*q+1,q*q+6*q+1]
assert S.Poly(S.prod(factors),q,modulus=13)==phi
assert S.gcd(phi,delta).monic()==poly(str(factors[2]))
assert S.gcd(phi,pair).degree()==0
assert S.gcd(phi,aug).monic()==poly(str(factors[2]))
rows=[]
for f in factors:
    F=poly(str(f))
    assert F.is_irreducible
    g=poly(s7['g']).rem(F);v=poly(s7['v']).rem(F)
    tau=(v*S.invert(g,F)).rem(F)
    rows.append({'factor':str(F.as_expr()),'tau':str(tau.as_expr()),'residual_pair_unit':not pair.rem(F).is_zero,'delta_nonzero':not delta.rem(F).is_zero})
out={'s':7,'p':13,'phi_factors':[str(f) for f in factors],'gcd_phi_delta':str(S.gcd(phi,delta).monic().as_expr()),'gcd_phi_pair':str(S.gcd(phi,pair).monic().as_expr()),'components':rows,'conclusion':'Exceptional tau=2 occurs in exactly one inverse-stable factor; two other factors pass the augmented selection.'}
(root/'FRESH_EXCEPTION_CONTROL.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
