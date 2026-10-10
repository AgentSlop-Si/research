"""Independent EXACT certificate for the original 256-point four-stage mixer.

No floating point is used. All numerical linear algebra in the verifier is
integer matrix multiplication with a proved conservative no-overflow bound.
Proof: for any symmetric positive definite diagonal-dominant integer H,
H=T^T(50 L-101 I+50 J)T and invertible integer T, the symmetric integer
M=50 L-101 I+50 J is positive definite, hence lambda_2(L)>101/50.

Dependencies: numpy. (The creation script additionally uses scipy.)
Run: python verify_exact.py
"""
from pathlib import Path
import gzip,json
import numpy as np

ROOT=Path(__file__).resolve().parent
N=256

def affine(cols):
    n=1<<len(cols)
    p=np.zeros(n,dtype=np.int64)
    for i in range(n):
        v=0
        for j,c in enumerate(cols):
            if (i>>j)&1:v^=c
        p[i]=v
    assert len(set(map(int,p)))==n
    return p

def scan_path_edges(shuffles):
    n=len(shuffles[0]);idx=np.arange(n,dtype=np.int64)
    out=[]
    for j in range(len(shuffles)+1):
        out.extend((int(a),int(b)) for a,b in zip(idx[:-1],idx[1:]))
        if j<len(shuffles):idx=idx[shuffles[j]]
    return out

def laplacian(edges,n):
    L=np.zeros((n,n),dtype=np.int64)
    for i,j in edges:
        L[i,i]+=1; L[j,j]+=1; L[i,j]-=1;L[j,i]-=1
    return L

def run():
    layout=json.loads((ROOT/'AFFINE_LAYOUT.json').read_text())
    assert layout['k']==8 and len(layout['affine_shuffle_columns'])==3
    perms=[affine(c) for c in layout['affine_shuffle_columns']]
    edges=scan_path_edges(perms)
    assert len(edges)==4*(N-1)
    L=laplacian(edges,N)
    assert np.all(L==L.T) and np.all(L.sum(axis=1)==0)
    assert int(np.trace(L))==2*len(edges)

    with gzip.open(ROOT/'INTEGER_CONGRUENCE_CERTIFICATE.json.gz','rt',encoding='utf-8') as f:
        cert=json.load(f)
    assert (cert['N'],cert['shift_num'],cert['shift_den'])==(256,101,50)
    T=np.array(cert['T'],dtype=np.int64)
    assert T.shape==(N,N)
    assert np.all(T[np.tril_indices(N,-1)]==0), 'T must be upper triangular'
    assert np.all(np.diag(T)!=0), 'T must be invertible over Q'

    M=50*L-101*np.eye(N,dtype=np.int64)+50*np.ones((N,N),dtype=np.int64)
    # Bound EVERY partial dot product in BOTH multiplications below.
    maxrowM=int(np.max(np.sum(np.abs(M),axis=1)))
    maxT=int(np.max(np.abs(T)))
    maxcolT=int(np.max(np.sum(np.abs(T),axis=0)))
    overflow_bound=maxcolT*maxrowM*maxT
    assert overflow_bound < 2**62, 'Cannot safely multiply with int64'

    H=T.T@(M@T)
    assert np.array_equal(H,H.T)
    diagonal=H.diagonal()
    margins=diagonal-(np.abs(H).sum(axis=1)-np.abs(diagonal))
    assert np.all(diagonal>0) and np.all(margins>0)

    # An independent pure-Python big-integer contraction using only paths.
    # Formula follows M=50 Σ_e (e_i-e_j)(e_i-e_j)^T-101 I+50 J.
    checks=[(0,0),(1,10),(17,103),(201,221),(255,255)]
    checks.extend(((i*37+11)%N,(i*83+57)%N) for i in range(24))
    for a,b in checks:
        u=[int(z) for z in T[:,a]]
        v=[int(z) for z in T[:,b]]
        manual=(50*sum((u[i]-u[j])*(v[i]-v[j]) for i,j in edges)
                -101*sum(ua*vb for ua,vb in zip(u,v))
                +50*sum(u)*sum(v))
        assert manual==int(H[a,b]),(a,b,manual,int(H[a,b]))

    result={'N':N,'stages':4,'path_edges':len(edges),
            'threshold_numerator':101,'threshold_denominator':50,
            'exact_T_nonzeros':int(np.count_nonzero(T)),
            'exact_T_max_abs':maxT,'proof_int64_intermediate_absolute_bound':overflow_bound,
            'min_diagonal':int(diagonal.min()),
            'min_strict_diagonal_dominance_margin':int(margins.min()),
            'independent_big_integer_entries_checked':len(checks),
            'guaranteed_minimum_bisection_boundary':130,
            'theorem':'All moving-partition ranks <= available channel capacity for every nontrivial subset; no Fourier factorization claimed.'}
    print(json.dumps(result,indent=2))
    return result
if __name__=='__main__':run()
