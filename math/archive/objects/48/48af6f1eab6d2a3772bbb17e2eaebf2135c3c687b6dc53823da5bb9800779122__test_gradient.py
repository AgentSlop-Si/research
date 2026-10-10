"""Finite-difference test of linear-work projective phase loss/gradient.
The global optimizer is NOT claimed to converge to an FFT factorization.
"""
import json
from pathlib import Path
import numpy as np
from verify import Stage

HERE=Path(__file__).resolve().parent
rng=np.random.default_rng(76302)

def loss_grad(stage,b0,b1,phase,d):
    u=stage.apply(b0*d)
    v=stage.apply(b1*d)
    denom=np.abs(u)**2+np.abs(v)**2
    if np.any(denom<1e-16):raise ArithmeticError('degenerate row')
    ell=(np.conj(u)+np.conj(v)*phase)/denom
    r0=ell*u-1
    r1=ell*v-phase
    loss=float(np.sum(np.abs(r0)**2+np.abs(r1)**2))
    q0=np.conj(ell)*r0
    q1=np.conj(ell)*r1
    g=np.conj(b0)*stage.adjoint(q0)+np.conj(b1)*stage.adjoint(q1)
    return loss,g

def main():
    data=[]
    for n in (8,16,32):
        A=Stage(n,rng);B=Stage(n,rng)
        basis=np.eye(n,dtype=complex)
        b0=B.apply(basis[:,0]);b1=B.apply(basis[:,1])
        omega=np.exp(-2j*np.pi/n); phase=omega**np.arange(n)
        d=(.8+.5*rng.random(n))*np.exp(2j*np.pi*rng.random(n))
        z=rng.normal(size=n)+1j*rng.normal(size=n)
        z/=np.linalg.norm(z)
        f,g=loss_grad(A,b0,b1,phase,d)
        eps=1e-6
        fp=loss_grad(A,b0,b1,phase,d+eps*z)[0]
        fm=loss_grad(A,b0,b1,phase,d-eps*z)[0]
        numeric=(fp-fm)/(2*eps)
        analytic=float(2*np.real(np.vdot(g,z)))
        err=abs(analytic-numeric)
        assert err<1e-5 * max(1,abs(numeric),abs(analytic)),(n,analytic,numeric,err)
        data.append({'N':n,'loss':f,'finite_difference_directional':numeric,'analytic_directional':analytic,'abs_difference':err})
    (HERE/'GRADIENT_RESULTS.json').write_text(json.dumps(data,indent=2))
    print(json.dumps(data,indent=2))

if __name__=='__main__':main()
