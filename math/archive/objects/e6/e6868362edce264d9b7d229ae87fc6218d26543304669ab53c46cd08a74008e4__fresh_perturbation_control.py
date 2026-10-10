"""Synthetic countercontrol to deductions from four special values alone.
This is NOT a counterexample for the actual Rogers-Szego polynomial.
"""
import time,json
import sympy as sp
from fresh_controls import Ring,gaussian,contract,peval,pmul,padd,modular_poly,HERE,q

def run():
 t=time.perf_counter();d=25;p=3;R=Ring(d);Q=R.elt([0,1])
 P=contract(gaussian(12,R),R)
 eta1=R.neg(R.add(Q,R.pow(Q,24)))
 eta12=R.neg(R.add(R.pow(Q,12),R.pow(Q,13)))
 F=pmul(pmul([R.elt(-4),R.zero,R.one],[R.neg(eta1),R.one],R),[R.neg(eta12),R.one],R)
 phi=sp.Poly(sp.cyclotomic_poly(d,q),q,modulus=p)
 inv=sp.invert(modular_poly(F[0],p),phi)
 def lift(T):return R.elt([int(T.nth(i)) for i in range(R.m)])
 A=lift((-modular_poly(P[0],p)*inv).rem(phi))
 B=lift((-(modular_poly(P[1],p)+modular_poly(F[1],p)*modular_poly(A,p))*inv).rem(phi))
 modified=padd(P,pmul(F,[A,B],R),R)
 assert len(modified)==len(P) and modified[-1]==R.one
 checks={}
 for name,x in [('2',R.elt(2)),('-2',R.elt(-2)),('eta1',eta1),('eta12',eta12)]:
  checks[name]=peval(P,x,R)==peval(modified,x,R);assert checks[name]
 assert modular_poly(modified[0],p).is_zero and modular_poly(modified[1],p).is_zero
 result={'d':d,'p':p,'purpose':'Synthetic control, not an actual Gaussian-polynomial counterexample','P':[list(x) for x in P],'perturbing_factor_F':[list(x) for x in F],'A':list(A),'B':list(B),'modified_P':[list(x) for x in modified],'exact_special_value_preservation':checks,'double_root_zero_mod_p':True,'ring_operation_counts':R.ops,'elapsed_seconds':time.perf_counter()-t}
 (HERE/'SYNTHETIC_PERTURBATION_CONTROL.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:result[k] for k in ['d','p','purpose','exact_special_value_preservation','double_root_zero_mod_p','ring_operation_counts','elapsed_seconds']},indent=2))
if __name__=='__main__':run()
