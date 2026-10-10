#!/usr/bin/env python3
"""Fresh original-matrix control over Q(q), with generic root traces.
Imports only the reviewer's own arithmetic/reconstruction, never author code.
X and its powers are built by literal sparse matrix multiplication.
"""
from review_n11 import *
t1=time.time()

def eprod(a,b):
 z=prem(pmul(a,b));return z+[Z]*(6-len(z))
tinv=[-g[i]/g[0] for i in range(1,7)]
assert eprod([Z,O],tinv)==[O]+[Z]*5
invpower=[O]+[Z]*5
for _ in range(11):invpower=eprod(invpower,tinv)
guardinv=[-v for v in invpower]
assert eprod([-v for v in powers[11]],guardinv)==[O]+[Z]*5

# If N_K(t)=sum_d K_d sum_{k>d}c_k t^(k-1-d), then
# Tr(N_K(t)/g'(t))=[t^5]N_K modg in the separable algebra.
# Verify the dual interpolation identity on all 36 basis pairings.
def numerator(ks):
 ans=[Z]*6
 for d in range(6):
  for k in range(d+1,7):ans[k-1-d]+=ks[d]*g[k]
 return ans
def lam_prod(a,r):return sum((v*powers[i+r][5] for i,v in enumerate(a)),Z)
for d in range(6):
 e=[Z]*6;e[d]=O;v=numerator(e)
 for r in range(6):assert lam_prod(v,r)==(O if r==d else Z)

# Build all actual amplitude moments, independently of Gaussian row tables.
# Group order ++, -+, +-, --. Sector ell corresponds to b=delta*ell.
signs=[(1,1),(-1,1),(1,-1),(-1,-1)]
sector_moments=[];sector_numerators=[]
for group,(eps,delta) in enumerate(signs):
 seq=[];polys=[]
 for ell in range(11):
  b=delta*ell%11;z=rows[b]
  if group in (0,3):
   ks=z[:6] if group==0 else z[8:]
   poly=numerator(ks)
   vals=[lam_prod(poly,r) for r in range(11)]
   assert vals[:6]==ks
   assert vals==[evalmoment(ks,r) for r in range(11)]
   polys.append(poly)
  else:
   v=z[6 if group==1 else 7];vals=[v]*11;polys.append([v])
  seq.append(vals)
 sector_moments.append(seq);sector_numerators.append(polys)

# Formal polynomial matrices represented by dictionaries (row,col,power_of_t).
def addto(D,key,v):
 if not v:return
 D[key]=D.get(key,Z)+v
 if not D[key]:del D[key]
def xleft(P,eps,delta,j):
 R={}
 for (k,c,r),v in P.items():
  addto(R,(k,c,r),qp[(eps*delta*j+delta*k)%11]*v)
  addto(R,((k+eps)%11,c,r+1),v)
 return R
def xright(P,eps,delta,j):
 R={}
 for (k,c,r),v in P.items():
  addto(R,(k,c,r),qp[(eps*delta*j+delta*c)%11]*v)
  addto(R,(k,(c-eps)%11,r+1),v)
 return R
def minus(A,B):
 R=A.copy()
 for key,v in B.items():addto(R,key,-v)
 return R
I={(i,i,0):O for i in range(11)}
X11={(i,i,r):O for i in range(11) for r in (0,11)}
guardI={(i,i,11):-O for i in range(11)}
original=[[Z]*11 for _ in range(11)]
branch_checks=[]
for group,(eps,delta) in enumerate(signs):
 for j in range(11):
  P=I.copy();R=I.copy()
  for n in range(1,11):
   P=xleft(P,eps,delta,j)
   for key,v in P.items():addto(R,key,v)
  assert xleft(P,eps,delta,j)==X11
  assert minus(R,xleft(R,eps,delta,j))==guardI
  assert minus(R,xright(R,eps,delta,j))==guardI
  # Raw weights have factor C*Delta; Delta cancels the certified inverse.
  # Trace of the weighted root group is calculated using the dual coefficient
  # functional above. For singletons t=1, the same expression is evaluation.
  hphase=[sum((qp[(-eps*delta*j*ell)%11]*sector_moments[group][ell][r] for ell in range(11)),Z) for r in range(11)]
  for (k,c,r),v in R.items():original[k][c]+=C*hphase[r]*v/cv(11)
  branch_checks.append({'group':group,'epsilon':eps,'delta':delta,'phase':j,'X_power_11_identity':True,'left_inverse_product':True,'right_inverse_product':True,'actual_resolvents_represented':6 if group in (0,3) else 1})
 print('Original phase sums finished for orientation',eps,delta,flush=True)
original_checks=[[original[k][t]==qp[(-k*t)%11] for t in range(11)] for k in range(11)]
assert all(all(r) for r in original_checks)
assert sum(r['actual_resolvents_represented'] for r in branch_checks)==154
result={'status':'all_passed','field':'Q(q) with q a primitive eleventh root, and trace from its separable sextic algebra','original_matrix_method':'Literal sparse polynomial-matrix powers at each of 44 group/phase pairs, two-sided inverse identities, dual interpolation trace functional, and direct weighted phase sum. No Gaussian row coefficient formula is used to accumulate the original matrix.', 'all_36_dual_interpolation_basis_checks':True,'alpha_inverse_verified':True,'guard_inverse_verified':True,'branch_checks':branch_checks,'actual_resolvents_covered':154,'original_matrix_entry_checks':original_checks,'all_121_original_entries_pass':True,'seconds':time.time()-t1}
(OUT/'LITERAL_ORIGINAL_MATRIX_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
(OUT/'LITERAL_AMPLITUDE_CERTIFICATE.json').write_text(json.dumps({'g_ascending':[serial(z) for z in g],'alpha_inverse':[serial(z) for z in tinv],'guard_inverse':[serial(z) for z in guardinv],'sector_numerators_group_order_pp_mp_pm_mm':[[[serial(z) for z in poly] for poly in group] for group in sector_numerators]},indent=2)+'\n')
print('All 154 branch inverses and all 121 original Fourier entries passed.',flush=True)
print('Literal seconds:',time.time()-t1,flush=True)
