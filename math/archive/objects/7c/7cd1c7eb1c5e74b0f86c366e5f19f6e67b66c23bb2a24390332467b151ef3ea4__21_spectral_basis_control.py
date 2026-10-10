"""Independent floating-point positive control: one four-phase mask suffices
between a real orthogonal Fourier eigenbasis and its transpose. NOT a fast FFT."""
import json
import numpy as np


def audit(n):
    omega=np.exp(-2j*np.pi/n);ix=np.arange(n)
    F=np.power(omega,np.outer(ix,ix))/np.sqrt(n)
    Z=np.roll(np.eye(n),1,axis=0)
    D=np.diag(omega**ix)
    H=(Z+Z.T+D+D.conj().T).real
    E=np.zeros((n,n//2+1));E[0,0]=1;E[n//2,-1]=1
    O=np.zeros((n,n//2-1))
    for j in range(1,n//2):
        E[j,j]=E[n-j,j]=2**(-.5)
        O[j,j-1]=2**(-.5);O[n-j,j-1]=-2**(-.5)
    ev,Ue=np.linalg.eigh(E.T@H@E)
    ov,Uo=np.linalg.eigh(O.T@H@O)
    W=np.hstack((E@Ue,O@Uo))
    diagonal=np.diag(W.T@F@W)
    allowed=[1,-1,1j,-1j]
    phases=np.array([min(allowed,key=lambda z:abs(z-x)) for x in diagonal])
    reconstructed=(W*phases)@W.T
    err=float(np.max(abs(reconstructed-F)))
    assert err<1e-10
    assert np.max(abs(W.T@F@W-np.diag(diagonal)))<1e-10
    counts={str(z):int(sum(abs(phases-z)<.1)) for z in allowed}
    return {'n':n,'max_abs_reconstruction_error':err,
            'max_orthogonality_defect':float(np.max(abs(W.T@W-np.eye(n)))),
            'phases':counts,'only_four_center_phases':True,
            'warning':'Dense real eigenbasis is not an O(N) application algorithm'}

if __name__=='__main__':
    print(json.dumps([audit(n) for n in (8,16,32,64,128)],indent=2))
