import sys,json,math
from pathlib import Path
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R.parent/'candidate'))
import restricted_guards as rg

def direct_shift(a):
 return [sum(math.comb(i,j)*a[i] for i in range(j,len(a))) for j in range(len(a))]
def evaluate(c,x):
 return sum(v*pow(x,i) for i,v in enumerate(c))
rows=[]
for m,L in [(2,8),(2,12),(3,16),(8,24),(65,8)]:
 a=[(1<<m)-1]*L; H=2*m+(L-1).bit_length()
 W=rg.envelope_precision(rg.product_bounds(m,L))
 exact=direct_shift(a)
 h=[v% (1<<H) for v in exact]
 recovered=rg.shift_mod(h,-1,H)
 assert recovered==a
 w=rg.shift_mod(recovered,1,W)
 assert w==[v%(1<<W) for v in exact]
 bad=list(h); bad[0]+=1<<H
 # Bad arbitrary H-bit lifts represent the same H-precision array but are not
 # promised W-precision lifts of the original bounded polynomial.
 assert all((x-y)%(1<<H)==0 for x,y in zip(bad,h))
 assert any((evaluate(bad,r-1)-evaluate(a,r))%(1<<W) for r in range(2*L-1))
 rows.append({'m':m,'L':L,'H':H,'W':W,'canonical_H_truncates':exact!=h,'inverse_recovery_pass':True,'arbitrary_lift_fails_honesty':True})
(R/'LIFT_RESULTS.json').write_text(json.dumps({'status':'PASS','controls':rows},indent=2)+'\n')
print(json.dumps({'status':'PASS','controls':len(rows)}))
