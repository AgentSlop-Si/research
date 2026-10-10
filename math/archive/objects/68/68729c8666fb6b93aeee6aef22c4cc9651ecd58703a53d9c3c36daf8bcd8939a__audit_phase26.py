"""Exact full-basis audit independent of the binary and split recurrences."""
import json, random
from pathlib import Path
from phase26_circuits import (root_table, split_radix_dif, scalar_radix2,
    gt3_split,radix2_predicted)
from phase25_source.gt3_deferred import DeferredGT3

fields=[(2013265921,31),(754974721,11)]
records=[]
for p,g in fields:
    for n in (8,16,32,64,128,256):
        w,_=root_table(n,p,g)
        for j in range(n):
            x=[int(i==j) for i in range(n)]
            y,c=split_radix_dif(x,w,p)
            old,d=scalar_radix2(x,w,p)
            lifted,e=scalar_radix2(x,w,p,shear=True)
            assert (y==old==lifted==[w[(j*k)%n] for k in range(n)])
            assert (c.adds,c.muls)==(d.adds,d.muls)
            assert e.muls-d.muls==n*(n.bit_length()-1)//2
        records.append({'p':p,'n':n,'basis_outputs_checked':n*n,'kind':'dyadic'})
    for G in (2,4,8,16,32,64,128):
        n=3*G
        if n>384:continue
        powers,_=root_table(n,p,g)
        for j in range(n):
            x=[int(i==j) for i in range(n)]
            y,c=gt3_split(x,p,g,'split')
            ref,d=gt3_split(x,p,g,'radix2')
            old=DeferredGT3(x,p,g).full()
            assert y==ref==old==[powers[j*k%n] for k in range(n)]
            assert (c.adds,c.muls)==(d.adds,d.muls)
        records.append({'p':p,'n':n,'basis_outputs_checked':n*n,'kind':'mixed-GT3'})

count=sum(r['basis_outputs_checked'] for r in records)
result={'fields':fields, 'basis_matrix_entries_checked':count,'records':records,
    'all_comparisons_passed':True,'model':'exact prime-field matrix equality against direct powers'}
Path(__file__).with_name('PHASE26_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
print('Audited',count,'matrix entries across',len(fields),'prime fields and',len(records),'full Fourier matrices')
