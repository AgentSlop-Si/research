#!/usr/bin/env python3
"""O(N)-work-per-probe self-supervised Fourier phase loss for four Green scans.
Requires torch (CPU). This is a research optimizer, NOT an FFT algorithm.
Exact arithmetic/storage claims do not apply to this floating-point demonstration.
"""
import argparse, json
import numpy as np
import torch


def cycle_order(rng, n):
    o=list(map(int,rng.permutation(n)))
    inv=np.argsort(o)
    return o,list(map(int,inv))


def solve_cycle(b, w, order, inverse_order):
    """(I - diag(w)P)^(-1) b with N-1 recurrence steps and N-1 backsteps."""
    rhs=b[order]
    ww=w[order]
    t=rhs[-1]
    for i in range(len(order)-2, -1, -1):
        t=rhs[i]+ww[i]*t
    first=t/(1-torch.prod(ww))
    y=[None]*len(order)
    y[0]=first
    for i in range(len(order)-1,0,-1):
        y[i]=rhs[i]+ww[i]*y[(i+1)%len(order)]
    return torch.stack(y)[inverse_order]


def train(n=12,steps=35,lr=0.001):
    rng=np.random.default_rng(1944)
    torch.manual_seed(1944)
    order_pairs=[cycle_order(rng,n) for _ in range(4)]
    wr=torch.nn.Parameter(torch.tensor(0.16*rng.standard_normal((4,n)),dtype=torch.float64))
    wi=torch.nn.Parameter(torch.tensor(0.16*rng.standard_normal((4,n)),dtype=torch.float64))
    opt=torch.optim.Adam([wr,wi],lr=lr)
    ix=torch.arange(n,dtype=torch.float64)
    root=torch.exp(-2j*torch.pi*ix/n)
    e0=torch.zeros(n,dtype=torch.complex128);e0[0]=1
    v=torch.ones(n,dtype=torch.complex128)/n**0.5
    def apply(z):
        w=torch.complex(wr,wi)
        def g(t,x):return solve_cycle(x,w[t],*order_pairs[t])
        mid=g(2,z)+g(3,z)
        return g(0,mid)+g(1,mid)
    def seeded(z):
        return apply(z)+(v-apply(e0))*z[0]
    def measure():
        with torch.no_grad():
            eye=torch.eye(n,dtype=torch.complex128)
            M=torch.stack([seeded(eye[:,i]) for i in range(n)],dim=1)
            js=torch.arange(n,dtype=torch.float64)
            U=torch.exp(-2j*torch.pi*js[:,None]*js[None,:]/n)/n**0.5
            lam=torch.trace(U.conj().T@M)/n
            return float(((M-lam*U).abs()**2).sum()),float(torch.linalg.vector_norm(M[:,0]-U[:,0]))
    initial_distance,_=measure()
    losses=[]
    for it in range(steps):
        a=int(rng.integers(n));b=int(rng.integers(n))
        zr=torch.randn(n,dtype=torch.float64)
        zi=torch.randn(n,dtype=torch.float64)
        z=torch.complex(zr,zi)/2**0.5
        # Shift convention S z = roll(z,+1), D^a z = root^(a*j) z
        Wz=torch.roll(z,b)*root**a
        Mz=seeded(z)
        phiy=torch.roll((root**b)*Mz,-a)
        E=seeded(Wz)-phiy
        loss=(E.real.square()+E.imag.square()).sum()/2
        opt.zero_grad();loss.backward()
        assert torch.all(torch.isfinite(wr.grad)) and torch.all(torch.isfinite(wi.grad))
        if it==0:
            print('first_step_grad_l2',float(torch.linalg.vector_norm(wr.grad)+torch.linalg.vector_norm(wi.grad)))
        opt.step()
        losses.append(float(loss.detach()))
    # Dense evaluation here is only for this tiny validation case, never in gradient.
    distance,seed_error=measure()
    assert seed_error<1e-8
    print(json.dumps({'n':n,'iterations':steps,'first_loss':losses[0],
                      'last_loss':losses[-1], 'phase_distance_initial':initial_distance, 'phase_distance_final':distance,
                      'seed_error':seed_error,'note':'No claim of fitting the FFT.'},indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--n',type=int,default=12)
    parser.add_argument('--steps',type=int,default=35)
    a=parser.parse_args();train(a.n,a.steps)
