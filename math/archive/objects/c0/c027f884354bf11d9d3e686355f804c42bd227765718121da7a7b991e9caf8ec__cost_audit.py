"""Exact fresh-input executor for the certified generic scan-stage networks.
This is a cost and correctness control, not an FFT algorithm or speedup.
"""
from pathlib import Path
import json,random
import numpy as np
from independent_verifier import find_product_and_jacobian
HERE=Path(__file__).resolve().parent

def one_stage(par,x,p):
    n=len(x);x=[int(v)%p for v in x]
    L=np.asarray(par['L'],dtype=np.int64).reshape(n)
    V=np.asarray(par['V'],dtype=np.int64).reshape(n)
    U=np.asarray(par['U'],dtype=np.int64).reshape(n)
    W=np.asarray(par['W'],dtype=np.int64).reshape(n)
    d=np.asarray(par['d'],dtype=np.int64)
    y=[0]*n
    right=0; upper=[0]*n
    for i in range(n-1,-1,-1):
        upper[i]=int(U[i])*right%p
        right=(right+int(W[i])*x[i])%p
    left=0
    for i in range(n):
        low=int(L[i])*left%p
        y[i]=(low+upper[i]+int(d[i])*x[i])%p
        left=(left+int(V[i])*x[i])%p
    return y

def audit(n,p=12289,seed=8112):
    t=n//4+1
    w=json.loads((HERE/f'WITNESS_N{n}_T{t}.json').read_text())
    M,_,_=find_product_and_jacobian(w,p)
    rng=random.Random(seed+n*17+p)
    for _ in range(14):
        x=[rng.randrange(p) for _ in range(n)]
        y=x[:]
        for k,par in enumerate(w['stages']):
            if k:y=[y[i] for i in w['permutation']]
            y=one_stage(par,y,p)
        expected=list(map(int,(M@np.array(x,dtype=np.int64))%p))
        assert y==expected
    return {'n':n,'stages':t,'p':p,'fresh_input_vectors':14,
            'counted_scalar_multiplications':5*n*t,
            'counted_scalar_additions':4*n*t,
            'counted_scalar_total':9*n*t,
            'permutation_reads_upper_bound':(t-1)*n,
            'exact_results':'passed'}

if __name__=='__main__':
    out=[audit(n,p) for n in (8,16,32) for p in (12289,65537)]
    for item in out:print(item)
    (HERE/'COST_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
