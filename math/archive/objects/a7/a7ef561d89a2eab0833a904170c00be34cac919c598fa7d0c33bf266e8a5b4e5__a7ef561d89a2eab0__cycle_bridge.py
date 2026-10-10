#!/usr/bin/env python3
"""Hero #0: Bessel/Fourier operator bridge and exact Cauchy minors.

No unconditional O(N) FFT is claimed here. Uses NumPy FFT only as a
correctness oracle; dense spectral differentiation is not an O(N) primitive.
"""
import json
import math
from pathlib import Path
import numpy as np
from scipy.special import jv
import mpmath as mp

MOD = 998244353
GEN = 3


def rank_mod(matrix, p=MOD):
    a = [[int(x) % p for x in row] for row in matrix]
    if not a:
        return 0
    nr, nc = len(a), len(a[0]); rank = 0
    for col in range(nc):
        pivot = next((i for i in range(rank, nr) if a[i][col] != 0), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inv = pow(a[rank][col], p - 2, p)
        a[rank] = [(x * inv) % p for x in a[rank]]
        for i in range(rank + 1, nr):
            if a[i][col]:
                factor = a[i][col]
                a[i] = [(v - factor * w) % p for v, w in zip(a[i], a[rank])]
        rank += 1
        if rank == min(nr, nc):
            break
    return rank


def make_A_exact(K):
    """A = U diag(0,...,K-1) U^-1 over F_p; U is DFT matrix."""
    assert (MOD - 1) % K == 0
    zeta = pow(GEN, (MOD-1)//K, MOD)
    assert pow(zeta,K,MOD)==1 and (K==1 or pow(zeta,K//2,MOD)!=1)
    roots = [pow(zeta,i,MOD) for i in range(K)]
    invK = pow(K,MOD-2,MOD)
    coeff = []
    for d in range(K):
        q = pow(zeta,d,MOD)
        val = 0; power = 1
        for b in range(K):
            val = (val+b*power)%MOD
            power = power*q % MOD
        coeff.append(val*invK % MOD)
    A = [[coeff[(i-j)%K] for j in range(K)] for i in range(K)]
    return A, roots


def check_exact_cauchy(K, rng):
    A, roots = make_A_exact(K)
    inv2 = pow(2, MOD - 2, MOD)
    for i in range(K):
        for j in range(K):
            expected = ((K - 1) * inv2) % MOD if i == j else roots[j] * pow((roots[i]-roots[j]) % MOD, MOD-2, MOD) % MOD
            assert A[i][j] == expected, (K,i,j,A[i][j],expected)
    checked=0
    for t in range(1, min(K//2, 9)):
        for trial in range(6):
            perm = rng.permutation(K)
            I = sorted(map(int,perm[:t])); J = sorted(map(int,perm[t:2*t]))
            minor = [[A[i][j] for j in J] for i in I]
            assert rank_mod(minor)==t, (K,t,I,J)
            checked+=1
    for s in (1,2,3):
        for trial in range(3):
            S=[[0]*K for _ in range(K)]
            for i in range(K):
                js=rng.choice(K,size=s,replace=False)
                for j in js:
                    S[i][int(j)] = int(rng.integers(1,MOD))
            residual = [[(A[i][j]-S[i][j])%MOD for j in range(K)] for i in range(K)]
            r=rank_mod(residual)
            assert K <= (s+2)*(r+1)-1, (K,s,r)
    return {'K':K,'exact_entries':K*K,'disjoint_cauchy_minors':checked,'sparse_rank_tests':9}


def normalized_fft(y):
    return np.fft.fft(y,norm='ortho')


def apply_H_oracle(Y):
    """H=U diag(0,1,1/2,...,1/(K-1)) U^-1.

    This intentionally performs TWO FFTs and IS NOT a fast O(K) solution.
    """
    K=len(Y)
    z=np.fft.ifft(Y,norm='ortho')
    coeff=np.zeros(K,dtype=float)
    coeff[1:] = 1 / np.arange(1,K)
    return normalized_fft(z*coeff)


def check_bessel_recurrence(K, rng, orders=6):
    lam=math.pi/K
    g=rng.standard_normal(K)+1j*rng.standard_normal(K)
    z=lam*np.arange(K)
    true=[normalized_fft(g*jv(r,z)) for r in range(orders+1)]
    computed=[true[0],true[1]]
    for r in range(1,orders):
        nxt=(2*r/lam)*apply_H_oracle(computed[-1])-computed[-2]
        if r==1:
            # Bessel J_1(z)/z tends to 1/2 at z=0.
            nxt=nxt + (g[0]/np.sqrt(K))*np.ones(K)
        computed.append(nxt)
    errors=[float(np.max(np.abs(a-b))) for a,b in zip(computed,true)]
    scale=max(float(np.linalg.norm(g)), 1e-15)
    return {'K':K,'orders':orders,'max_absolute_error':max(errors),
            'max_error_per_input_l2':max(errors)/scale,'per_order':errors}



def check_bessel_mp(K=16, orders=6, dps=65):
    """Independent high-precision direct-matrix oracle for the exact cycle."""
    mp.mp.dps=dps
    rt=mp.sqrt(K); pi=mp.pi; i=mp.j
    omega=mp.exp(-2*pi*i/K)
    F=[[omega**(k*b)/rt for b in range(K)] for k in range(K)]
    Fi=[[omega**(-b*k)/rt for k in range(K)] for b in range(K)]
    g=[mp.mpc((b%7)-3,(b%5)-2) for b in range(K)]
    def mat_vec(M,v):
        return [mp.fsum(M[t][j]*v[j] for j in range(K)) for t in range(K)]
    base=[mat_vec(F,[g[b]*mp.besselj(r,pi*b/K) for b in range(K)]) for r in range(orders+1)]
    weights=[mp.mpf(0)]+[mp.mpf(1)/b for b in range(1,K)]
    def H(y):
        z=mat_vec(Fi,y)
        return mat_vec(F,[weights[b]*z[b] for b in range(K)])
    vals=[base[0],base[1]]
    for r in range(1,orders):
        q=[(2*r*K/pi)*a-b for a,b in zip(H(vals[-1]),vals[-2])]
        if r==1:
            q=[v+g[0]/rt for v in q]
        vals.append(q)
    error=max(abs(a-b) for x,y in zip(vals,base) for a,b in zip(x,y))
    assert error < mp.mpf(10)**(-(dps-25)), error
    return {'K':K,'orders':orders,'digits':dps,'max_abs_error':mp.nstr(error,10)}

def odd_grid_test(N):
    Q=1 << (N-1).bit_length()
    assert N%2==1 and math.gcd(N,Q)==1
    # Avoid floating rounding: residue class of Q*k mod N.
    distinct={((Q*k)%N) for k in range(N)}
    assert len(distinct)==N
    return {'N':N,'Q':Q,'distinct_fractional_offsets':len(distinct)}


def main():
    rng=np.random.default_rng(20261009)
    exact=[check_exact_cauchy(n,rng) for n in [8,16,32,64]]
    numerical=[check_bessel_recurrence(n,rng,6) for n in [8,16,32,64,128]]
    precise=[check_bessel_mp(n,6,65) for n in [8,16,32]]
    grid=[odd_grid_test(n) for n in [15,17,23,31,37,63,127]]
    assert max(x['per_order'][2] for x in numerical)<1e-11
    results={'status':'verified identities and restricted no-go only; NO O(N) FFT',
             'exact_cauchy':exact,'bessel_recurrence':numerical,'mp_bessel_recurrence':precise,
             'odd_length_grid':grid,'modulus':MOD}
    here=Path(__file__).resolve().parent
    (here/'results.json').write_text(json.dumps(results,indent=2),encoding='utf8')
    print(json.dumps({'checks':'PASSED','exact_sizes':[x['K'] for x in exact],
                      'max_bessel_relative_to_input_l2':max(x['max_error_per_input_l2'] for x in numerical),
                      'odd_grid_sizes':[x['N'] for x in grid], 'high_precision_cycle':precise},indent=2))

if __name__=='__main__':
    main()
