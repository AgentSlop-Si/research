"""Independent, brute-force GF(17)^4 completeness/soundness check."""
import itertools,json,time
from math import gcd
from blind_discovery import blind_one_defect

p,n=17,4
count=0;all_nonzero=0;oracle_yes=0;detector_yes=0;misses=0;false=0
for r in itertools.product(range(p), repeat=n):
    count+=1
    if not all(r):continue
    all_nonzero+=1
    oracle=False
    for d in range(1,n):
        if gcd(d,n)!=1:continue
        if oracle:break
        for a in range(1,p):
            bad=sum((r[j]-a*r[(j-d)%n])%p!=0 for j in range(n))
            if bad<=1:
                oracle=True
                break
    found,stats=blind_one_defect(r,p)
    pred=found is not None
    if oracle:oracle_yes+=1
    if pred:detector_yes+=1
    if oracle and not pred:misses+=1
    if pred and not oracle:false+=1
    if misses or false:
        print('MISMATCH',r,oracle,found)
        raise AssertionError('independent brute-force oracle disagree')
result={'field':'GF(17)','N':4,'total_vectors':count,'nowhere_zero_vectors':all_nonzero,
        'brute_force_compressible_K_le1':oracle_yes,'detector_accepted':detector_yes,
        'misses':misses,'false_acceptances':false,
        'oracle':'Enumerate all coprime cyclic shifts and all 16 nonzero slopes for each signal, independently count defects.'}
with open('EXHAUSTIVE_GATE.json','w') as f:json.dump(result,f,indent=2)
print(json.dumps(result,indent=2))
