"""Produce independently computed nonzero determinant witnesses for selected mappings."""
from __future__ import annotations
import json
from itertools import permutations
from random import Random
from pathlib import Path
from phase31_rectangular import ROOT,family,rectangular_quadrics
from phase30_dimension_gate import lifted_general
from phase30_macaulay import determinant_modp
SEVEN=((0,1,0,1),(0,1,0,2),(0,1,0,3),(0,2,1,2),
       (0,2,2,3),(1,2,0,1),(1,2,0,3))

def run(n,count=60,seed=13123):
    t,g=family(n)
    rows=list(permutations(range(n),3));cols=list(permutations(range(n),4))
    rng=Random(seed+n)
    total=len(rows)*len(cols)
    selected={0,1,total-1}
    selected.update(rng.sample(range(total),min(count,total-3)))
    outputs=[]
    for idx in sorted(selected):
        rr=rows[idx//len(cols)];cc=cols[idx%len(cols)]
        mat=lifted_general(rectangular_quadrics(t,g,rr,cc,pairs=SEVEN),5,3)
        det=determinant_modp(mat)
        assert det!=0,(n,idx)
        outputs.append({'index':idx,'rows':rr,'columns':cc,'nonzero_determinant_mod_p':det})
    return {'N':n,'prime':998244353,'sampled_mapping_count':len(outputs),
            'determinants':outputs}

if __name__=='__main__':
    import sys
    n=int(sys.argv[1]);output=Path(sys.argv[2]);output.write_text(json.dumps(run(n),indent=2)+'\n')
    print('saved',output,'N',n)
