"""Exact modular Jacobian witness for four necessary Fourier-gate polynomials."""
from __future__ import annotations
import json,random,itertools
from pathlib import Path
from dual_support import primitive_root
from column_minor import build_polynomial
from upper_minor import generate
from inverse_quartic import rankmod
import numpy as np

def witness(p=12289,w=None,trials=10):
    if w is None:w=primitive_root(p,8)
    RR,uu=generate(p,w)
    Rq,q=build_polynomial(p,w)
    QQ=RR.from_dict({tuple(list(k)+[0,0]):c for k,c in q.terms()})
    K=[4,1,2,5]
    conditions=[QQ]+[uu[K[0]][0]*uu[k][1]-uu[k][0]*uu[K[0]][1] for k in K[1:]]
    r=random.Random(1103+p+w)
    for _ in range(trials):
        params=[r.randrange(1,p) for _ in range(8)]
        point=list(zip(RR.gens,params))
        D=np.array([[int(poly.diff(x).evaluate(point))%p for x in RR.gens] for poly in conditions],dtype=np.int64)
        if rankmod(D,p)==4:
            for cols in itertools.combinations(range(8),4):
                sub=D[:,cols]
                if rankmod(sub,p)==4:
                    # Elimination gives actual nonzero determinant modulo p.
                    A=sub.copy();det=1
                    for i in range(4):
                        j=next((k for k in range(i,4) if A[k,i]%p),None)
                        assert j is not None
                        if i!=j:A[[i,j]]=A[[j,i]];det=(-det)%p
                        pivot=int(A[i,i]);det=det*pivot%p
                        z=pow(pivot,-1,p)
                        for j in range(i+1,4):
                            fac=int(A[j,i])*z%p
                            A[j,i:]=(A[j,i:]-fac*A[i,i:])%p
                    assert det
                    return dict(prime=p,root=w,params=params,selected_columns=list(cols),jacobian_rows=D.tolist(),nonzero_minor=int(det),condition_names=['Q_lower_quartic','R_upper_4_1','R_upper_4_2','R_upper_4_5'],status='four polynomials algebraically independent over Q(zeta8)')
    raise ValueError('none found')
if __name__=='__main__':
    v=witness()
    Path(__file__).with_name('independence_witness.json').write_text(json.dumps(v,indent=2)+'\n')
    print(json.dumps({k:v[k] for k in v if k!='jacobian_rows'},indent=2))
