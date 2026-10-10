"""Failure mode at near-resonant spectral division in ordinary complex double.

Shows why a correct finite-field algorithm is not a floating-point stability
certificate. The r sequence is a single exponential along one permutation
cycle; its exact resonant Fourier value is sum_{t=0}^{N-1}exp(epsilon*t).
"""
import cmath, math, json
from mpmath import mp


def run():
    n=128;shift=63;k0=7
    phase=cmath.exp(-2j*math.pi*(k0*shift % n)/n)
    node=cmath.exp(2j*math.pi*(k0*shift % n)/n)
    records=[]
    for epsilon in [1e-6,1e-8,1e-10,1e-12,1e-14]:
        alpha=phase*math.exp(epsilon)
        h=1-alpha**n
        denom=1-alpha*node
        naive=h/denom
        with mp.workdps(90):
            eps=mp.mpf(str(epsilon))
            reference=mp.fsum([mp.exp(t*eps) for t in range(n)])
            ref=float(reference)
        rel=abs(naive-ref)/abs(ref)
        records.append({'epsilon':epsilon,'abs_denominator':abs(denom),
                        'abs_numerator':abs(h),'ratio_real':naive.real,
                        'ratio_imag':naive.imag,'reference_real':ref,
                        'relative_error':rel})
    out={'N':n,'shift':shift,'near_resonance_frequency':k0,
         'records':records,
         'warning':'Complex double cancellation in 1-alpha^N / (1-alpha*root^k). No general forward-error certificate for the near-resonant branch; finite field exact arithmetic not affected.'}
    with open('PRECISION_GATE.json','w') as f:json.dump(out,f,indent=2)
    for row in records:print(row)
    return out
if __name__=='__main__':run()
