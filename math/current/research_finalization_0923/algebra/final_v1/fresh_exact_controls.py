"""Fresh self-authored controls, 2026-10-10. No archived code imported or executed.
Compute Rogers-Szego discriminants/resultants directly in cyclotomic fields,
and reduced integral-coordinate contents; not unreduced polynomial contents.
"""
import json, math, time
from pathlib import Path
import sympy as S
from sympy.polys.domains import AlgebraicField
from sympy.polys.rings import ring
OUT=Path(__file__).resolve().parent
q=S.symbols('q')
def coordinates(a,dim):
    c=a.to_list(); assert all(x.denominator==1 for x in c)
    c=[int(x) for x in c][::-1]
    return c+[0]*(dim-len(c))
def content(c): return abs(math.gcd(*c))
def valuation(a,p):
    assert a
    k=0
    while a%p==0: k+=1;a//=p
    return k
def one(s,p):
    N=s*p;n=(N-1)//2;t=time.monotonic()
    phi=S.Poly(S.cyclotomic_poly(N,q),q)
    K=AlgebraicField(S.QQ,(phi,S.Symbol('w'))); R,z=ring('z',K);w=K.unit
    f0,f1=R.one,1+z
    for j in range(2,n+1): f0,f1=f1,(1+z)*f1+(R(w**(j-1))-1)*z*f0
    D=f1.discriminant(); RR=(z**N+1).resultant(f1)
    # Distinct fresh route for resultant: product of evaluations at all -w^j.
    Rp=K.one
    for j in range(N): Rp*=f1.evaluate(z,-w**j)
    assert RR==Rp
    arrays=[coordinates(a,phi.degree()) for a in (D,RR,D*RR)]
    cont=[content(a) for a in arrays]; vals=[valuation(a,p) for a in cont]
    predicted=[s*(p-3)//8,N//4,3*s*(p-1)//8]
    assert vals==predicted
    assert vals[2]-vals[0]-vals[1]==int(p%8==1)
    return dict(s=s,p=p,N=N,contents=[str(a) for a in cont],p_valuations=vals,predicted=predicted,
      carry=vals[2]-vals[0]-vals[1],coordinate_arrays=[[str(a) for a in b] for b in arrays],
      resultant_product_crosscheck=True,elapsed_seconds=round(time.monotonic()-t,3))
results=[]
for s,p in [(1,5),(1,13),(1,17),(9,5)]:
    row=one(s,p);results.append(row)
    (OUT/'fresh_exact_results.json').write_text(json.dumps(dict(method=__doc__,results=results),indent=2))
    print({k:row[k] for k in ['s','p','N','p_valuations','carry','elapsed_seconds']},flush=True)
# Pure rational-floor check; supplements the written symbolic proof, not a theorem by enumeration.
floors=[]
for s in [1,5,9,13,17,21]:
 for p in list(S.primerange(5,150)):
  if p%4==1 and s%p:
   a=s*(p-3)//8;b=s*p//4;c=3*s*(p-1)//8
   assert c-a-b==int(p%8==1)
   floors.append([s,p,a,b,c])
(OUT/'fresh_floor_controls.json').write_text(json.dumps(dict(check_count=len(floors),rows=floors),indent=2))
