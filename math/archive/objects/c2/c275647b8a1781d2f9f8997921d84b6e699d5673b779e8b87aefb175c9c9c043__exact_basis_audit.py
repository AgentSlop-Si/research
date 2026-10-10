"""Independent direct DFT across numerous independently constructed K=2 inputs."""
import json
from annihilator_engine import RecurrenceGreen,dense_from_shift_defects
from resultant_gate import transform_resultant
from rational_forcing import direct_dft_any

CASES=[(998244353,3,17,5,None,0),
       (2013265921,31,30,7,None,0),
       (2013265921,31,60,17,17,60),
       (2013265921,31,128,63,47,128),
       (2013265921,31,384,191,145,48)]

def main():
  total=0;records=[]
  for p,g,n,delta,offset,cap in CASES:
    e=RecurrenceGreen(n,p,g)
    if offset is None:
      pairs=[(j,k) for j in range(n) for k in range(j+1,n)]
    else:
      pairs=[(j,(j+offset)%n) for j in range(cap)]
    fast=0;slow=0
    for j,k in pairs:
      h=[0]*n;h[j]=7;h[k]=11
      r=dense_from_shift_defects(h,delta,2,p)
      x=e.P.solve(r)
      y,info=transform_resultant(e,x)
      reference=direct_dft_any(x,e.omega,p)
      if y!=reference:raise AssertionError((n,delta,j,k))
      if info['selected']=='blind-resultant-2defects':fast+=1
      else:slow+=1
    count=len(pairs)*n
    total+=count
    records.append({'N':n,'p':p,'delta':delta,'defect_pairs':len(pairs),
      'success_fast':fast,'fallback_correct':slow,'exact_output_entries':count})
    print('EXACT-DIRECT',n,'pairs',len(pairs),'fast',fast,'fallback',slow,
          'entries',count,flush=True)
  result={'cases':records,'total_exact_direct_dft_entries':total,
          'meaning':'Each adaptively selected output compared against an independent O(N^2) direct DFT; verifies tested inputs, not all complex inputs or a complexity theorem.'}
  with open('EXACT_BASIS_AUDIT.json','w') as f:json.dump(result,f,indent=2)
  return result
if __name__=='__main__':main()
