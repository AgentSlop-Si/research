"""Numerical exploratory comparisons. NOT part of exact theorem.
Outputs a JSON table contrasting affine/nonlinear/shuffle families.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh
ROOT=Path(__file__).resolve().parent
from verify_exact import affine,scan_path_edges
LAYOUT=json.loads((ROOT/'AFFINE_LAYOUT.json').read_text())

def make_matrix(paths,n=256):
    edges=scan_path_edges(paths)
    a=np.array([v[0] for v in edges]);b=np.array([v[1] for v in edges])
    rr=np.r_[a,b,a,b];cc=np.r_[a,b,b,a]
    vv=np.r_[np.ones(2*len(a),dtype=np.int64),-np.ones(2*len(a),dtype=np.int64)]
    return coo_matrix((vv,(rr,cc)),shape=(n,n)).tocsr()

def lam(p):
    L=make_matrix(p)
    return float(sorted(eigsh(L,k=2,which='SM',tol=1e-9,return_eigenvectors=False))[1])

def gf2_rank_cols(cols,k):
    rank=0;basis={}
    for x in cols:
        v=int(x)
        while v:
            b=v.bit_length()-1
            if b in basis:v^=basis[b]
            else:
                basis[b]=v;rank+=1;break
    return rank

def random_cols(rng,k):
    while True:
        v=[int(i) for i in rng.integers(0,1<<k,size=k)]
        if gf2_rank_cols(v,k)==k:return v

def mcnot(k,controls,target):
    n=1<<k;p=np.arange(n,dtype=np.int64)
    cm=sum(1<<c for c in controls)
    t=1<<target
    for i in range(n):
        if (i&cm)==cm:p[i]=i^t
    return p

base=[affine(cols) for cols in LAYOUT['affine_shuffle_columns']]
modified=[p.copy() for p in base]
for gate in LAYOUT['toffoli_gate_sequence_in_shuffle_2']:
    modified[2]=modified[2][mcnot(8,gate['controls'],gate['target'])]
out={'base':lam(base),'five_toffoli_modified':lam(modified)}
rng=np.random.default_rng(776619)
for kind in ('random_affine','random_permutation'):
 vals=[]
 for trial in range(20):
    if kind=='random_affine':p=[affine(random_cols(rng,8)) for _ in range(3)]
    else:p=[rng.permutation(256).astype(np.int64) for _ in range(3)]
    vals.append(lam(p))
 out[kind]={'n':len(vals),'min':min(vals),'median':float(np.median(vals)),'max':max(vals),'certifiable_by_gap_gt_2':sum(v>2 for v in vals),'all':vals}
(ROOT/'EXPLORATORY_SPECTRAL_RESULTS.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:v if isinstance(v,float) else {t:vv for t,vv in v.items() if t!='all'} for k,v in out.items()},indent=2))
