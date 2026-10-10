"""Numerical controls for the Phase 20 sharp Weyl spectral gap and
sparsity/near-resonance obstructions. Uses NumPy for independent audits.
The actual exact finite-field Green implementations are in weyl_gate.py.
"""
from __future__ import annotations
import numpy as np


def Fhat(n):
    j=np.arange(n)
    return np.exp(-2j*np.pi*np.outer(j,j)/n)/np.sqrt(n)

def Zmat(n):return np.roll(np.eye(n,dtype=complex),1,axis=0)

def Dmat(n):return np.diag(np.exp(-2j*np.pi*np.arange(n)/n))

def defects(M):
    n=M.shape[0];Z=Zmat(n);D=Dmat(n)
    return (np.linalg.norm(M@Z-D@M,'fro'),
            np.linalg.norm(M@D-Z.T@M,'fro'))

def sharp_gap_control(n):
    F=Fhat(n); D=Dmat(n);M=F@D
    c=np.vdot(F,M)/n
    distance=np.linalg.norm(M-c*F,'fro')
    e1,e2=defects(M)
    rhs=(e1*e1+e2*e2)**0.5/(2*np.sin(np.pi/n))
    return dict(n=n,distance=float(distance),upper_bound=float(rhs),
                ratio=float(distance/rhs),first_resid=float(e1),second_resid=float(e2))

def sharp_sparse_weyl_gap(n,s,k):
    """One s-sparse column achieves exactly the Dirichlet path gap."""
    assert 1<=s<n and 0<=k<n
    w=np.exp(-2j*np.pi/n); z=w**k
    b=np.zeros(n,dtype=complex)
    for j in range(s):
        b[j]=(z**(-j))*np.sin(np.pi*(j+1)/(s+1))
    grad=np.roll(b,1)-z*b
    ratio=np.linalg.norm(grad)/np.linalg.norm(b)
    theoretical=2*np.sin(np.pi/(2*(s+1)))
    return dict(n=n,s=s,k=k,ratio=float(ratio),exact_gap=float(theoretical))

def random_sparse_covariance(n,seed=20):
    rng=np.random.default_rng(seed)
    B=np.zeros((n,n),complex)
    for i in range(n):
        B[i,i]=3+rng.random()
        if i>0:B[i,i-1]=0.1+rng.random()*0.2
        if i+1<n:B[i,i+1]=0.1+rng.random()*0.2
    Z=Zmat(n);D=Dmat(n)
    gap=2*np.sin(np.pi/(2*(3+1)))
    actual=np.linalg.norm(Z@B-B@D,'fro')/np.linalg.norm(B,'fro')
    return dict(n=n,s=3,actual=float(actual),guaranteed=float(gap))

def inverse_sparse_floor(n,s,*, t=1,seed=30):
    """Test full operator-norm approximation obstruction for pure products
    of sparse-denominator Green solves; not for sums of inverse solves.
    """
    rng=np.random.default_rng(seed)
    B=np.eye(n,dtype=complex)
    for _ in range(t):
        b=np.eye(n,dtype=complex)*3
        for i in range(n-1):
            b[i,i+1]=rng.uniform(0.1,0.3)
            b[i+1,i]=rng.uniform(0.1,0.3)
        B=B@b
    row_nonzeros=max(np.count_nonzero(abs(B[i])>1e-14) for i in range(n))
    assert row_nonzeros <= s**t
    M=np.linalg.inv(B)
    eps=np.linalg.norm(M-Fhat(n),2)
    delta=np.sqrt(max(0,1-s**t/n))
    floor=delta/(1+delta)
    return dict(n=n,t=t,max_row_nnz=int(row_nonzeros),
                actual_operator_error=float(eps),guaranteed_floor=float(floor))

def near_resonance_real(n):
    """Near-resonant path denominator passes column-norm growth but fails
    Weyl phase equations. Small dense control for transparency."""
    B=np.eye(n)-(1-1/n)/2*(np.diag(np.ones(n-1),1)+np.diag(np.ones(n-1),-1))
    G=np.linalg.inv(B)
    Z=Zmat(n);D=Dmat(n)
    e1=np.linalg.norm(G@Z-D@G,'fro')/np.linalg.norm(G,'fro')
    e2=np.linalg.norm(G@D-Z.T@G,'fro')/np.linalg.norm(G,'fro')
    return dict(n=n,condition=float(np.linalg.cond(B)),
                relative_first_defect=float(e1),relative_second_defect=float(e2),
                green_1_norm=float(np.linalg.norm(G,1)))

if __name__=='__main__':
    import json
    records={
        'sharp_weyl_gap':[sharp_gap_control(n) for n in (8,16,32,64,128)],
        'sparse_column_gap':[sharp_sparse_weyl_gap(64,s,3) for s in (1,2,3,7,15)],
        'sample_sparse':[random_sparse_covariance(n) for n in (8,32,64)],
        'sparse_inverse_error':[inverse_sparse_floor(n,3,t=1) for n in (16,32,64)],
        'two_inverse_error':[inverse_sparse_floor(n,3,t=2) for n in (32,64)],
        'near_resonance':[near_resonance_real(n) for n in (16,32,64,128)]
    }
    print(json.dumps(records,indent=2))
