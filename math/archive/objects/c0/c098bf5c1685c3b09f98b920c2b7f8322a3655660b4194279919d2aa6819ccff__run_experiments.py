"""Exact finite-field multi-stage Jacobian experiments and independent checks."""
import json,random,subprocess,sys,tempfile
from pathlib import Path
import numpy as np
from multistage_jacobian import materialize,check_differences,rank_minor

ROOT=Path(__file__).resolve().parent
BIN=ROOT/'rankmod'

def field_case(n,t,p,seed=99017):
    rng=random.Random(seed+n*31+t*997)
    perms=[]
    for _ in range(t-1):
        a=list(range(n));rng.shuffle(a);perms.append(a)
    base,J,pars,mats=materialize(n,t,perms,seed,p)
    check_differences(n,t,perms,pars,base,J,seed+299,p,num=30)
    with tempfile.TemporaryDirectory() as temp:
        path=Path(temp)/'jac.int32'
        J.astype(np.int32).tofile(path)
        stdout=subprocess.check_output([str(BIN),str(path),str(n*n),str(5*n*t),str(p)],text=True)
    head,cols=stdout.strip().splitlines()
    parts=dict(tok.split('=') for tok in head.split())
    rk=int(parts['rank']);det=int(parts['det'])
    pivots=[int(x) for x in cols.removeprefix('pivots=').split(',')]
    bound=min(n*n,t*(5*n-6)-(t-1)*n)
    assert rk<=bound,(n,t,rk,bound)
    if n<=16:
        rk2,p2,det2=rank_minor(J,p)
        assert rk2==rk and p2==pivots
        if rk==n*n: assert det2==det
    return {'n':n,'t':t,'p':p,'seed':seed,'permutations':perms,
            'rank':rk,'gauge_upper_bound':bound,'codimension':n*n-rk,
            'full_minor_det':det if rk==n*n else None,
            'full_minor_columns':pivots if rk==n*n else None,
            'rank_equivalent_over_two_routines':n<=16,
            'verified_coordinate_derivatives':30}

if __name__=='__main__':
    cases=[]
    for n,t in [(8,2),(8,3),(16,2),(16,3),(16,4),(16,5),
                (32,3),(32,4),(32,5),(32,6),(32,7),(32,8),(32,9)]:
        for p in [12289,65537]:
            item=field_case(n,t,p)
            cases.append(item)
            print('n',n,'t',t,'p',p,'rank',item['rank'],'bound',item['gauge_upper_bound'], 'det',item['full_minor_det'],flush=True)
    (ROOT/'EXACT_RESULTS.json').write_text(json.dumps(cases,indent=2)+'\n')
