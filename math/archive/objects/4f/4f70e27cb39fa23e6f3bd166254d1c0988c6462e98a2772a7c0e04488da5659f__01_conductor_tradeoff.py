"""Sparse Galois descent, generalized from K=Q(zeta_8) to K_B=Q(zeta_B).

N=2^m, B=2^b, 3<=b<m<=2*b and L=N/B<=B. Let a=1+B.
There is a factorization F_N = B_orbit * Q * A with entries of
B_orbit and A in Q(zeta_B), and Q=diag(zeta_N^r). The Galois orbit
basis B_orbit is an orbitwise Fourier transform of lengths <=L.

Under the threshold m<=2b, (1+B)^t = 1+B*t (mod N) and A is sparse:
for each orbit starting k0 and column j, exactly one eigenrow is
nonzero, with value zeta_B^((k0*j-r)//L) where r=k0*j mod L.
Thus A has exactly N*c(N,B) nonzeros, c=B+(B/2)*(m-b).

The counts + congruence identities below are verified with integer
modular arithmetic only: no floating error or FFT oracle is involved.
This factorization is not an o(N log N) algorithm. Direct A application
costs Theta(N B(1+log(N/B))), which grows if B grows with N.
"""
from collections import Counter


def is_pow2(x):return x>0 and x&(x-1)==0


def conductor_orbits(n,B):
    assert is_pow2(n) and is_pow2(B) and B>=8 and B<n
    L=n//B
    visited=bytearray(n);group=[]
    a=1+B
    for k in range(n):
        if visited[k]:continue
        orbit=[];j=k
        while not visited[j]:
            visited[j]=1;orbit.append(j);j=(a*j)%n
        assert j==k
        group.append(orbit)
    return group


def cycle_count_formula(n,B):
    assert is_pow2(n) and is_pow2(B) and B<=n
    m=n.bit_length()-1
    b=B.bit_length()-1
    return B+(B//2)*(m-b)


def explicit_sparse_galois_factor(n,B,full_check=True):
    assert is_pow2(n) and is_pow2(B) and B>=8 and B<n
    L=n//B
    m=n.bit_length()-1
    b=B.bit_length()-1
    if L>B:
        return dict(n=n,B=B,L=L,one_mask_over_KB=False,
                    cause='a primitive L-th permutation eigenvalue is not in Q(zeta_B)')
    cycles=conductor_orbits(n,B)
    assert len(cycles)==cycle_count_formula(n,B)
    hist=Counter(len(c) for c in cycles)
    # Each cycle starting k0 length d has eigencharacters r_e=e*(L/d).
    # Every input index j chooses exactly e=(k0*j)/(L/d) mod d.
    nonzero=0
    max_cycle=max(len(c) for c in cycles)
    for orbit in cycles:
        k0=orbit[0];d=len(orbit)
        assert L%d==0
        assert d==L//__import__('math').gcd(L,k0)
        for t,k in enumerate(orbit):
            assert k==(k0*(1+B*t))%n
        if full_check:
            for j in range(n):
                r=k0*j%L
                assert r%(L//d)==0
                e=r//(L//d)
                assert 0<=e<d
                # Explicit coefficient A_{orbit,e,j}=zeta_B^h,
                # h=(k0*j-r)/L, with all other e-rows zero.
                h=(k0*j-r)//L
                assert (k0*j - r)%L==0
                for t,k in enumerate(orbit):
                    # B component zeta_L^(r*t) times Q zeta_N^r,
                    # times A zeta_B^h: compare exponents modulo N.
                    reconstructed_exponent=(B*r*t + r + L*h)%n
                    assert reconstructed_exponent==(k*j)%n
                nonzero+=1
        else:
            nonzero+=n
    assert nonzero==n*len(cycles)
    return dict(n=n,B=B,L=L,one_mask_over_KB=True,
                cycles=len(cycles),cycle_formula=cycle_count_formula(n,B),
                cycle_lengths=dict(sorted(hist.items())),
                nonzero_residual_A=nonzero,
                maximal_orbit_fourier_size=max_cycle,
                all_phase_exponents_verified=full_check,
                work_of_naive_residual_A='Theta(N*(B+B/2*log2(N/B)))')


if __name__=='__main__':
    import json
    for n,B in ((16,8),(32,8),(64,8),(128,8),(128,16),
                (256,16),(256,32),(512,32),(1024,32),(1024,16)):
        print(json.dumps(explicit_sparse_galois_factor(n,B),indent=2))
