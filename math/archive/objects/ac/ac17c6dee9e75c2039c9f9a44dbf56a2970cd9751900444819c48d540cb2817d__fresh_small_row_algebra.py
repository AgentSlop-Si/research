"""New exact symbolic row-only controls; imports no project research programs."""
import json, time
import sympy as s
from sympy.polys.domains import QQ
q,x,y=s.symbols('q x y')
results=[]
for N in [3,5,7]:
    start=time.time();phi=s.Poly(s.cyclotomic_poly(N,q),q)
    if N==3:
        results.append({'N':N,'interior_equations':0,'status':'row condition vacuous'})
        continue
    K=QQ.alg_field_from_poly(phi); root=K.ext.as_expr()
    eq=[]; input_polynomials=[]
    for a in range(2,N-1):
        E=q**(((a+1)**2*pow(4,-1,N))%N)*(1-q**2)*(1-q**(N-2))-q*x**(a-1)*(1-q**(a+1))*(1-q**(N-2))-y**(N-a-1)*(1-q**(a-1))*(1-q**2)
        E=s.Poly(E,q); E=s.rem(E,phi).as_expr(); input_polynomials.append(str(s.expand(E))); E=E.subs(q,root)
        eq.append(E)
    G=s.groebner(eq,x,y,domain=K)
    data={'N':N,'coefficient_field':str(K),'minimal_polynomial':str(phi.as_expr()),'input_polynomials_reduced_in_q':input_polynomials,'guard_localization':'None. Full K[x,y] tested, including zero parameters. Denominator clearing uses only nonzero root-of-unity factors.','interior_equations':len(eq),'groebner_basis':[str(v) for v in G.polys],'ideal_is_unit':G==s.groebner([1],x,y,domain=K),'elapsed_seconds':time.time()-start}
    print(json.dumps(data),flush=True);results.append(data)
open('research_cycle_0958/signed_magnetic_fusion/fresh_small_row_algebra_results.json','w').write(json.dumps(results,indent=2)+'\n')
