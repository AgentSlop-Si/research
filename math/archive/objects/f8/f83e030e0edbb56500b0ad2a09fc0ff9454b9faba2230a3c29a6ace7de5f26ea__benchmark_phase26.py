"""Reproduce exact field operation counts; no elapsed-time performance claim."""
import json,random
from pathlib import Path
from phase26_circuits import (P,root_table,split_radix_dif,scalar_radix2,
    radix2_predicted,gt3_split)
from volume_gate import gt3_gate_tolls

rows=[]
for n in (4,8,16,32,64,128,256,512,1024,4096,16384):
    roots,root_setup=root_table(n)
    rng=random.Random(26+n)
    x=[rng.randrange(P) for _ in range(n)]
    radix,rc=scalar_radix2(x,roots)
    split,sc=split_radix_dif(x,roots)
    lifted,lc=scalar_radix2(x,roots,shear=True)
    assert radix==split==lifted
    assert (rc.adds,rc.muls)==(sc.adds,sc.muls)==radix2_predicted(n)
    assert lc.adds==rc.adds and lc.muls-rc.muls==(n//2)*(n.bit_length()-1)
    rows.append(dict(N=n, radix2={'adds':rc.adds,'muls':rc.muls,'total':rc.arithmetic()},
        split_radix={'adds':sc.adds,'muls':sc.muls,'total':sc.arithmetic()},
        lifted_shear={'adds':lc.adds,'muls':lc.muls,'total':lc.arithmetic()},
        root_setup_multiplications=root_setup,split_saving=rc.arithmetic()-sc.arithmetic(),
        shear_extra=lc.arithmetic()-rc.arithmetic()))

mixed=[]
for G in (2,4,16,64,256,1024,4096):
    n=3*G
    rng=random.Random(26+G)
    x=[rng.randrange(P) for _ in range(n)]
    y1,c1=gt3_split(x,method='split')
    y2,c2=gt3_split(x,method='radix2')
    y3,c3=gt3_split(x,method='shear')
    assert y1==y2==y3
    assert (c1.adds,c1.muls)==(c2.adds,c2.muls)
    mixed.append({'N':n,'split':c1.arithmetic(),'phase25_baseline':c2.arithmetic(),
        'nonunitary_shear':c3.arithmetic(),'split_saving':c2.arithmetic()-c1.arithmetic(),
        'shear_extra':c3.arithmetic()-c2.arithmetic(),
        'volume_toll':gt3_gate_tolls(G)})

receipt={'phase':26, 'model':'exact finite field p=2013265921, full scalar additions and multiplications',
    'baseline':'optimized radix2/GT3, no identity twiddle charge',
    'input_independent_asymptotic':'Theta(N log N), no improved upper bound',
    'dyadic':rows,'mixed_3x':mixed}
Path(__file__).with_name('RESULT_SUMMARY.json').write_text(json.dumps(receipt,indent=2)+'\n')
for r in rows:print('N=%6d radix2=%9d split=%9d shear=%9d extra=%9d'%(r['N'],r['radix2']['total'],r['split_radix']['total'],r['lifted_shear']['total'],r['shear_extra']))
for r in mixed:print('GT3 N=%6d old=%9d split=%9d shear=%9d'%(r['N'],r['phase25_baseline'],r['split'],r['nonunitary_shear']))
