#!/usr/bin/env python3
"""Separate fresh control of the fixed-order two-parameter extension."""
from review_n11 import *
affine_rhs=[[-m[4],-m[5],-m[6],-n[4]],[-m[5],-m[6],-m[7],-n[5]]]
u,v=[solve(A,rhs) for rhs in affine_rhs]
base=g[:6];lslope=u+[O,Z];mslope=v+[Z,O]
for r in range(3):
 assert m[r+6]+sum((base[k]*m[r+k] for k in range(6)),Z)==Z
 assert sum((lslope[k]*m[r+k] for k in range(6)),Z)==Z
 assert sum((mslope[k]*m[r+k] for k in range(6)),Z)==Z
assert n[6]+sum((base[k]*n[k] for k in range(6)),Z)==Z
assert sum((lslope[k]*n[k] for k in range(6)),Z)==Z
assert sum((mslope[k]*n[k] for k in range(6)),Z)==Z
# Additional exact specializations are optional controls, not the general proof.
samples=[]
for lam,mu in [(0,0),(1,0),(0,1),(1,1)]:
 coeff=[base[k]+cv(lam)*lslope[k]+cv(mu)*mslope[k] for k in range(6)]+[O]
 pr=[]
 for r in range(11):
  p=prem([Z]*r+[O],coeff);pr.append(p+[Z]*(6-len(p)))
 mats={b:[[gaussian(1,1,a,b)*p for p in pr[a]]+[gaussian(-1,1,a,b),gaussian(1,-1,a,b)]+[gaussian(-1,-1,a,b)*p for p in pr[-a%11]] for a in range(11)] for b in range(11)}
 minors=[]
 for b in [0,3,4,5]:
  inds=MC['full_row_minors'][str(b)]['columns']
  minors.append(detmod([[md(row[i]) for i in inds] for row in mats[b]]))
 cg=[md(c) for c in coeff];dg=[i*cg[i]%23 for i in range(1,7)]
 sy=[[0]*i+cg[::-1]+[0]*(4-i) for i in range(5)]+[[0]*i+dg[::-1]+[0]*(5-i) for i in range(6)]
 resultant=detmod(sy)
 pp=cg[0]*resultant
 for d in minors:pp=pp*d%23
 # Exact edge recipes with all coefficient positions retained.
 c=coeff
 k0=-H*(m[5]+sum((c[k]*m[k-1] for k in range(1,6)),Z))/c[0]
 z1=[k0]+[H*m[k-1] for k in range(1,6)]+[H,f(0,1)-k0-H]+[Z]*6
 l1=-(n[5]+sum((c[k]*n[k-1] for k in range(1,6)),Z))/c[0]
 l0=-(n[4]+c[1]*l1+sum((c[k]*n[k-2] for k in range(2,6)),Z))/c[0]
 p=(f(1,2)-gaussian(1,1,1,2)*l1)/gaussian(1,-1,1,2)
 q1=(f(10,2)-T*gaussian(-1,1,10,2))/gaussian(-1,-1,10,2)
 z2=[l0,l1]+n[:4]+[T,p,f(0,2)-l0-T-p,q1]+[Z]*4
 for b,z in [(1,z1),(2,z2)]:
  assert all(sum((u*v for u,v in zip(row,z)),Z)==f(a,b) for a,row in enumerate(mats[b]))
 samples.append({'lambda':lam,'mu':mu,'constant_mod23':cg[0],'resultant_mod23':resultant,'selected_minors_mod23':minors,'P_mod23':pp,'nonzero_guard_certified_by_this_prime':bool(pp),'zero_residue_means_inconclusive_not_excluded':not bool(pp),'all_22_exact_edge_equations_pass':True})
assert samples[0]['P_mod23']==17
FOUT=OUT/'parametric_family'
source=FOUT/'sources/PARAMETRIC_FAMILY_ADDENDUM.md'
result={'status':'all_passed','independence':'Fresh separate reviewer algebra, imports only own review_n11.py','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'all_four_recurrences_hold_coefficientwise_in_lambda_mu':True,'affine_sextic_ascending':{'constant':[serial(z) for z in base],'lambda':[serial(z) for z in lslope],'mu':[serial(z) for z in mslope],'t6':[serial(O)]},'specializations':samples,'general_proof_basis':'Coefficientwise affine recurrences, nonempty polynomial guard P, monic remainder and determinant formulas, and the accepted universal edge/interpolation/reflection/raw-weight identities. Sample points are additional controls only.','fixed_order_only':11}
(FOUT/'FAMILY_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print('Family recurrence identities passed. Guard residues:',[(s['lambda'],s['mu'],s['P_mod23']) for s in samples])
