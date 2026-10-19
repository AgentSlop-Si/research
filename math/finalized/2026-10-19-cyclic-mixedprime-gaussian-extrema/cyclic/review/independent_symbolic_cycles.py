#!/usr/bin/env python3
"""New symbolic-variable tests of the all-phase cyclic identity."""
import json
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parent
out=[]
x=s.Symbol('x')
for n in [3,4,5,6,7,8,9,10,12]:
    b=s.symbols(f'b0:{n}',nonzero=True)
    c=s.symbols(f'c0:{n}')
    S=s.zeros(n)
    for j in range(n):S[(j+1)%n,j]=1
    C=s.Matrix(n,n,lambda j,k:c[(j+k)%n])
    B=s.diag(*b)
    assert C*S==S.T*C
    K=S.T*B.inv()*S.T*B
    for j in range(n):
        for k in range(n):
            expected=b[j]/b[(j-1)%n] if k==(j-2)%n else 0
            assert s.cancel(K[k,j]-expected)==0
    if n%2==0:
        g=s.prod(b[::2])/s.prod(b[1::2])
        expected=(x**(n//2)-g)*(x**(n//2)-1/g)
    else:expected=x**n-1
    got=K.charpoly(x).as_expr()
    assert s.cancel(got-expected)==0
    out.append({'N':n,'generic_hankel_shift_identity':True,'symbolic_weighted_cycle_action':True,
                'symbolic_characteristic_polynomial':True,'cycle_lengths':[n//2,n//2] if n%2==0 else [n]})
result={'status':'PASS','variables':'Independent formal nonzero b_j and formal Hankel entries c_j',
        'arithmetic':'Exact symbolic rational functions; no numerical phase sampling',
        'author_or_historical_code_executed':False,'checks':out}
(ROOT/'INDEPENDENT_SYMBOLIC_CYCLES.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
