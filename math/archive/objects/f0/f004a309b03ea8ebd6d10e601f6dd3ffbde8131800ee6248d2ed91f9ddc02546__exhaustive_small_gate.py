"""Fixed finite-parameter exhaustive sweep of two-defect support pairs.

Not an exhaustive sweep over all GF(p)^N (impractical), but enumerates all
C(8,2) defect supports across a fixed catalog of alpha/delta/amplitudes.
"""
import json
from itertools import combinations
from annihilator_engine import RecurrenceGreen,dense_from_shift_defects
from resultant_gate import transform_resultant
from rational_forcing import direct_dft_any

def main():
 p,n,g=97,8,5
 engine=RecurrenceGreen(n,p,g)
 alpha_values=[2,3,5,7,11]
 delays=[1,3,5,7]
 amplitudes=[(2,3),(5,7),(11,13),(17,19)]
 total=0;fast=0;fallback=0
 for d in delays:
  for alpha in alpha_values:
   for j,k in combinations(range(n),2):
    for u,v in amplitudes:
     h=[0]*n;h[j]=u;h[k]=v
     r=dense_from_shift_defects(h,d,alpha,p)
     x=engine.P.solve(r)
     y,m=transform_resultant(engine,x)
     if y!=direct_dft_any(x,engine.omega,p):raise AssertionError((d,alpha,j,k,u,v))
     fast+=(m['selected']=='blind-resultant-2defects')
     fallback+=(m['selected']=='fallback')
     total+=1
 out={'p':p,'N':n,'pairs_per_parameter':28,'delays':delays,
      'alphas':alpha_values,'amplitudes':amplitudes,'cases_checked':total,
      'fast_branch':fast,'correct_fallback':fallback,'output_entries_checked':total*n,
      'exhaustive_scope':'All 28 support pairs for the listed finite parameter choices only.'}
 with open('EXHAUSTIVE_SMALL_GATE.json','w') as f:json.dump(out,f,indent=2)
 print('SMALL-PARAMETER SWEEP',out,flush=True)
 return out
if __name__=='__main__':main()
