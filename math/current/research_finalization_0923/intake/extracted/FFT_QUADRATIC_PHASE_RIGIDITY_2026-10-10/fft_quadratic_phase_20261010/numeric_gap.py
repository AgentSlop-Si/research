#!/usr/bin/env python3
"""Floating-point diagnostic (not interval certification) of the spectral gap bound.
Independently reconstructs rational Green stages and complex Fourier matrices.
"""
import json,cmath,itertools,math
from pathlib import Path
import sympy as sp
import numpy as np
HERE=Path(__file__).parent

def dense_green(b):
    n=len(b['cycle']); W=sp.eye(n)
    for i,j in enumerate(b['cycle']):W[i,j]-=b['weights'][i]
    G=sp.diag(*b['left_diag'])*W.inv()*sp.diag(*b['right_diag'])
    a=b['row_permutation'];c=b['col_permutation']
    return sp.Matrix([[G[a[i],c[j]] for j in range(n)] for i in range(n)])

def run_one(n):
    c=json.loads((HERE/f'CERT_N{n}.json').read_text())
    Aexact=sum((dense_green(x) for x in c['trace_A']),sp.zeros(n,n))
    Bexact=sum((dense_green(x) for x in c['trace_B']),sp.zeros(n,n))
    A=np.array(Aexact,dtype=np.complex128);B=np.array(Bexact,dtype=np.complex128)
    w=cmath.exp(-2j*math.pi/n)
    F=np.fromfunction(lambda i,j:np.power(w,i*j),(n,n),dtype=int)
    ai=np.linalg.inv(A)
    Ps=[np.diag(1/B[:,j])@ai@np.diag(F[:,j]) for j in range(3)]
    pairs=list(itertools.combinations_with_replacement(range(n),2))
    rows=[]
    for j,k in itertools.combinations(range(3),2):
        for u,v in itertools.combinations(range(n),2):
            row=[]
            for a,b in pairs:
                val=Ps[j][u,a]*Ps[k][v,b]-Ps[k][u,a]*Ps[j][v,b]
                if a!=b:
                    val+=Ps[j][u,b]*Ps[k][v,a]-Ps[k][u,b]*Ps[j][v,a]
                row.append(val)
            rows.append(row)
    Q=np.array(rows,dtype=np.complex128)
    sigma=np.linalg.svd(Q,compute_uv=False)[-1]
    M=math.sqrt(sum(np.linalg.norm(P,2)**2 for P in Ps))
    bound=sigma*np.abs(B).min()/(math.sqrt(2*n)*M*np.linalg.norm(ai,2))
    assert bound>0
    rng=np.random.default_rng(101*n)
    minerr=float('inf');minratio=float('inf')
    for rep in range(30):
        def dg():
            d=np.exp(rng.normal(0,.5,size=n)+1j*rng.uniform(-math.pi,math.pi,size=n))
            return np.diag(d)
        L,D,E=dg(),dg(),dg()
        err=np.linalg.norm(L@A@D@B@E-F,2)
        minerr=min(err,minerr)
        minratio=min(minratio,err/bound)
    result={'N':n,'singular_min_Q':sigma,'spectral_error_lower_bound_numerical':bound,'min_30_sampled_errors':minerr,'min_error_to_bound_ratio':minratio}
    print(result)
    return result

if __name__=='__main__':
    r=[run_one(n) for n in (3,4)]
    (HERE/'NUMERIC_RESULTS.json').write_text(json.dumps(r,indent=2)+'\n')
