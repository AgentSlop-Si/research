"""One-time discovery of an INTEGER congruence witness.
Only the independent verify_exact.py is necessary for the proof;
Cholesky here is merely a convenient way to search for integer T.
"""
from pathlib import Path
import json,gzip
import numpy as np
from scipy.linalg import solve_triangular
BASE=Path(__file__).resolve().parent
rec=json.loads((BASE/'AFFINE_LAYOUT.json').read_text())
k=rec['k'];n=1<<k

def affine_permutation(cols):
    p=np.zeros(n,dtype=np.int64)
    for i in range(n):
        x=0
        for bit in range(k):
            if (i>>bit)&1:x^=cols[bit]
        p[i]=x
    assert len(set(map(int,p)))==n
    return p

perms=[affine_permutation(cols) for cols in rec['affine_shuffle_columns']]
idx=np.arange(n,dtype=np.int64)
L=np.zeros((n,n),dtype=np.int64)
for j in range(len(perms)+1):
    for a,b in zip(idx[:-1],idx[1:]):
        L[a,a]+=1;L[b,b]+=1;L[a,b]-=1;L[b,a]-=1
    if j<len(perms):idx=idx[perms[j]]
M=50*L-101*np.eye(n,dtype=np.int64)+50*np.ones((n,n),dtype=np.int64)
C=np.linalg.cholesky(M.astype(np.float64))
# Compute upper-triangular inverse of lower-triangular Cholesky transpose.
R=solve_triangular(C.T,np.eye(n),lower=False,check_finite=True)
T=np.rint((1<<12)*R).astype(np.int64)
assert (np.tril(T,-1)==0).all() and (T.diagonal()!=0).all()
H=T.T@(M@T)
diag=np.diag(H)
margins=diag-(np.abs(H).sum(axis=1)-np.abs(diag))
assert np.all(margins>0), int(np.min(margins))
with gzip.open(BASE/'INTEGER_CONGRUENCE_CERTIFICATE.json.gz','wt',encoding='utf-8',compresslevel=9) as f:
    json.dump({'N':n,'shift_num':101,'shift_den':50,'rounding_scale':4096,'T':T.tolist()},f,separators=(',',':'))
print('N=',n,'T nz=',int(np.count_nonzero(T)),'max abs T=',int(np.max(np.abs(T))))
print('H positive diag minimum=',int(diag.min()),'strict SDD margin=',int(margins.min()))
print('lambda_2(L) > 101/50 certified by INTEGER symmetric diagonal dominance.')
