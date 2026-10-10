import json
import math
from pathlib import Path
import numpy as np


def normalized_dft(n):
    j=np.arange(n)[:,None]
    k=np.arange(n)[None,:]
    return np.exp(-2j*np.pi*j*k/n)/math.sqrt(n)


def add_map(M):
    """Matrix of (x,y)->(x,y+Mx)."""
    n=M.shape[0]
    I=np.eye(n,dtype=np.complex128)
    Z=np.zeros_like(I)
    return np.block([[I,Z],[M,I]])


def generalized_swap(U):
    # A1: y += Ux
    # A2: x += -U^{-1} y
    # A3: y += Ux
    A1=add_map(U)
    # add_map acts source first -> target second. For x += M y, swap banks.
    n=U.shape[0]
    I=np.eye(n,dtype=np.complex128); Z=np.zeros_like(I)
    Uinv=U.conj().T
    A2=np.block([[I,-Uinv],[Z,I]])
    A3=add_map(U)
    return A3@A2@A1, [A1,A2,A3]


def expected_swap(U):
    n=U.shape[0]
    Z=np.zeros((n,n),complex)
    return np.block([[Z,-U.conj().T],[U,Z]])


def shear_condition_bound(alpha):
    # For E = I + alpha e_j e_i^T, ||E||_2 <= 1+|a| and
    # ||E^-1||_2 <= 1+|a|, hence kappa <= (1+|a|)^2.
    return (1+abs(alpha))**2


def main():
    rows=[]
    for B in (2,4,8,16):
        U=normalized_dft(B)
        W, factors=generalized_swap(U)
        E=expected_swap(U)
        rows.append({
            'B':B,
            'identity_error_fro':float(np.linalg.norm(W-E)),
            'unitarity_error_fro':float(np.linalg.norm(W.conj().T@W-np.eye(2*B))),
            'swap_condition':float(np.linalg.cond(W)),
            'factor_conditions':[float(np.linalg.cond(A)) for A in factors],
        })
    p=Path(__file__).with_name('transparent_swap_results.json')
    p.write_text(json.dumps(rows,indent=2))
    for r in rows: print(r)
    print('example single-shear upper bounds:')
    for a in (0.1,1,10,1e3): print(a,shear_condition_bound(a))

if __name__=='__main__': main()
