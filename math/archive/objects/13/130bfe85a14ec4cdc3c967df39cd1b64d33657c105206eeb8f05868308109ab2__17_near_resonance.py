"""Demonstration: norm-growth escape by near-singular path resolvent is NOT DFT phase coherence.
All reported numeric calculations are illustrative, NOT a factorization.
"""
import numpy as np


def audit(n:int):
    assert n>=8
    T=np.zeros((n,n),dtype=np.complex128)
    for j in range(n-1):T[j,j+1]=T[j+1,j]=1
    B=np.eye(n,dtype=np.complex128)-(1-1/n)/2*T
    G=np.linalg.inv(B)
    s=np.linalg.svd(B,compute_uv=False)
    kappa=float(s.max()/s.min())
    Gnorm=float(np.linalg.norm(G,ord=1))
    # Fourier primitive operators with FZ=DF.
    shift=np.roll(np.eye(n,dtype=np.complex128),1,axis=0)
    D=np.diag(np.exp(-2j*np.pi*np.arange(n)/n))
    defect=float(np.linalg.norm(G@shift-D@G,'fro')/np.linalg.norm(G,'fro'))
    assert Gnorm>np.sqrt(n)
    assert defect>0.1
    return {'n':n,'green_inv_l1':Gnorm,'sqrt_n':float(np.sqrt(n)),
            'system_kappa2':kappa,'normalized_shift_modulation_defect':defect,
            'norm_budget_escaped':True,'DFT_phase_coherence_failed':True}

if __name__=='__main__':
    import json
    print(json.dumps([audit(n) for n in (8,16,32,64,128,256)],indent=2))
