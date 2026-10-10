"""Fresh independent, bounded exact lower-base controls; no supplied program imports."""
import sympy as S
import json, hashlib
from pathlib import Path
q,z=S.symbols('q z')
outputs=[]
for s in [3,7,11]:
    b=(s-1)//2;r=(s-3)//4;phi=S.cyclotomic_poly(s,q)
    rem=lambda f:S.rem(S.expand(f),phi,q)
    h0,h1=S.Integer(1),1+z
    for n in range(2,b+1): h0,h1=h1,S.expand((1+z)*h1+(q**(n-1)-1)*z*h0)
    U,R=S.div(h1,z+1,z);assert R==0
    g=rem(U.subs(z,-1))
    v=rem(S.prod(1-q**(2*k) for k in range(1,r+1))*S.prod(1-q**(2*k+1) for k in range(b)))
    delta=rem(2*g-v)
    disc=S.discriminant(U,z) if b>1 else S.Integer(1)
    res=S.resultant(z**s+1,U,z)
    gamma=rem(disc*res)
    pair=rem(gamma*gamma.subs(q,q**(s-1)))
    aug=rem(pair*delta)
    content=lambda f:int(S.Poly(f,q).content())
    vbar=rem(v.subs(q,q**(s-1)))
    gbar=rem(g.subs(q,q**(s-1)))
    assert rem(g*vbar+gbar*v-v*vbar)==0
    out={'s':s,'b':b,'phi':str(phi),'g':str(g),'v':str(v),'delta':str(delta),'gamma':str(gamma),'pair':str(pair),'augmented':str(aug),'pair_content':content(pair),'augmented_content':content(aug),'delta_norm':int(S.resultant(phi,delta,q)),'inverse_identity':True}
    outputs.append(out);print(json.dumps(out),flush=True)
Path('research_cycle_0958/composite_guard/FRESH_AUGMENTED_CONTENT.json').write_text(json.dumps(outputs,indent=2)+'\n')
