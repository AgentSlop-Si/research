"""Fresh bounded symbolic controls of the new parity-complete pairing statement."""
import sympy as S
import json
from pathlib import Path
y,t=S.symbols('y t');rows=[]
for p in [3,5,7,11,13]:
    A=(p-1)//2
    h0,h1=S.Integer(1),y
    for k in range(2,A+1): h0,h1=h1,S.expand(y*h1-(k-1)*h0)
    h=h1
    J=S.expand(y*h-t*S.diff(h,y))
    disc=S.Poly(S.discriminant(J,y),t,modulus=p)
    ell=disc.degree()
    reflected=S.Poly(S.expand(sum(int(c)*t**i*(t-1)**(ell-i) for (i,),c in disc.terms())),t,modulus=p)
    gcd=S.gcd(disc,reflected).monic()
    predicted=S.Poly(t if p%4==3 else (t-2)**3,t,modulus=p).monic()
    assert gcd==predicted
    # V=i^-A H(iy) changes the coefficient of y^(A-2j) by (-1)^j.
    V=S.expand(sum(c*(-1)**((A-k)//2)*y**k for (k,),c in S.Poly(h,y).terms()))
    W=S.Poly(S.diff(h,y)*V-h*S.diff(V,y)-y*h*V+y**p,y,modulus=p)
    assert W.is_zero
    rows.append({'p':p,'A':A,'disc':str(disc.as_expr()),'paired_discriminant_gcd':str(gcd.as_expr()),'expected_gcd':str(predicted.as_expr()),'wronskian_identity':True})
Path('research_cycle_0958/composite_guard/FRESH_PAIRING_CONTROLS.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
