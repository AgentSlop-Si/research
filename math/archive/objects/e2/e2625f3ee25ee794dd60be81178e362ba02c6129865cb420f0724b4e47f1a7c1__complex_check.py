"""Independent complex-number spot check for entropy, volume and FFT gates.

Proofs are analytic; this numerical diagnostic is *not* an exact certificate.
It is separated from exact_audit.py to avoid confusing finite-field operations
with complex moduli or Shannon entropy.
"""
from __future__ import annotations
import cmath
import json
from math import log2, pi, sqrt


def fourier(n):
    return [[cmath.exp(2j*pi*i*j/n) for j in range(n)] for i in range(n)]


def entropy_of_matrix(mat):
    return -sum(p*log2(p) for row in mat for v in row if (p:=abs(v)**2)>1.e-28)


def log2_determinant_magnitude(mat):
    a=[row[:] for row in mat]
    n=len(a)
    total=0.0
    for i in range(n):
        pivot=max(range(i,n),key=lambda r:abs(a[r][i]))
        if abs(a[pivot][i])<1.e-12:
            raise AssertionError('singular')
        a[i],a[pivot]=a[pivot],a[i]
        pv=a[i][i]
        total+=log2(abs(pv))
        for r in range(i+1,n):
            factor=a[r][i]/pv
            if factor:
                for j in range(i+1,n):
                    a[r][j]-=factor*a[i][j]
                a[r][i]=0j
    return total


def bit_rev(j,bits):
    answer=0
    for _ in range(bits):
        answer=(answer<<1)|(j&1)
        j>>=1
    return answer


def normalized_fft_gate_stages(n):
    if n<2 or n & (n-1):
        raise ValueError('power of two >=2')
    bits=n.bit_length()-1
    identity=[]
    for i in range(n):
        idx=bit_rev(i,bits)
        identity.append([complex(1 if j==idx else 0) for j in range(n)])
    stages=[entropy_of_matrix(identity)]
    width=2
    while width<=n:
        half=width//2
        for start in range(0,n,width):
            for j in range(half):
                a,b=start+j,start+j+half
                w=cmath.exp(2j*pi*j/width)
                ra,rb=identity[a],identity[b]
                identity[a]=[(x+w*y)/sqrt(2) for x,y in zip(ra,rb)]
                identity[b]=[(x-w*y)/sqrt(2) for x,y in zip(ra,rb)]
        stages.append(entropy_of_matrix(identity))
        width*=2
    goal=fourier(n)
    max_err=max(abs(identity[i][j]-goal[i][j]/sqrt(n)) for i in range(n) for j in range(n))
    return stages,max_err


def run(ns=(2,4,8,16,32)):
    records=[]
    for n in ns:
        stages,error=normalized_fft_gate_stages(n)
        for t,h in enumerate(stages):
            if abs(h-n*t)>1.e-8:
                raise AssertionError(('entropy',n,t,h,n*t))
        matrix=fourier(n)
        det=log2_determinant_magnitude(matrix)
        wanted=n*log2(n)/2
        if abs(det-wanted)>1.e-8:
            raise AssertionError(('volume',n,det,wanted))
        if error>1.e-10:
            raise AssertionError(('DFT',n,error))
        records.append({'n':n,'entropy_by_stage':stages,'max_spectrum_entry_error':error,
                        'log2_det_magnitude':det,'theoretical_log2_det':wanted})
    return records

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
