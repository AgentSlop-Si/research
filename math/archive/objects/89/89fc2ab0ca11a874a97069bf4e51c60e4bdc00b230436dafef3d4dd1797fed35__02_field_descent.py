"""EXPLICIT Fourier one-mask factorization over a Galois base field.

For N=16,32,64, K=Q(zeta_8) contains the eigenvalues of the
permutation P_9: x[k] -> x[9k mod N]. Its orbitwise eigenbasis B is
K-valued. With L=N/8, set r_e for each eigenvalue zeta_L^r_e.
Then exactly F_N=B diag(zeta_N^r_e) A, where A is K-valued.

The code verifies this in the field F_{1000000009}[X]/(X^L-zeta_8),
not merely in a prime field containing a primitive Nth root. The
extension has degree L (the chosen prime is 9 modulo 512). Every
coefficient of A is explicitly in the base prime field, matching the
claimed field descent and proving it is not an artifact of reducing
all higher-order roots to one scalar in the base field.

This is a field-algebra identity, NOT an O(N) FFT: A can be dense.
"""
from collections import Counter
from spectral_gate import cycle_lengths
from galois_gate import n_power_of_two

P = 1_000_000_009
assert (P-1)%8 ==0 and (P-1)%16 !=0
assert (P-9)%512==0

def primitive_eighth_root():
    # A quadratic nonresidue exponentiated by (p-1)/8 has exact order eight.
    a=2
    while pow(a,(P-1)//2,P)!=P-1:
        a+=1
    z=pow(a,(P-1)//8,P)
    assert pow(z,8,P)==1 and pow(z,4,P)==P-1
    return z

Z8=primitive_eighth_root()


def power_rep(n, exponent):
    """omega_N^exponent = zeta8^q X^r in extension, X^L=zeta8."""
    L=n//8
    j=exponent%n
    q,r=divmod(j,L)
    return r,pow(Z8,q,P)


def cycles(n):
    seen=bytearray(n)
    groups=[]
    for k in range(n):
        if seen[k]:continue
        cycle=[];j=k
        while not seen[j]:
            seen[j]=1;cycle.append(j);j=9*j%n
        assert j==k
        groups.append(cycle)
    return groups


def exact_single_mask_factor(n, reconstruct=True):
    assert n_power_of_two(n)
    L=n//8
    groups=cycles(n)
    if L>8:
        return dict(n=n,L=L,possible_over_zeta8=False,
                    obstruction='P_9 has a primitive L-th eigenvalue not in K')
    labels=[]
    A=[]
    for orbit in groups:
        d=len(orbit)
        assert L%d==0
        assert 8%d==0
        z_d=pow(Z8,8//d,P)
        inv_d=pow(d,-1,P)
        for e in range(d):
            lam=pow(z_d,e,P)
            r_e=(L//d)*e
            labels.append((orbit,lam,r_e))
            arow=[]
            for j in range(n):
                coeffs=[0]*L
                for t,k in enumerate(orbit):
                    r, coeff=power_rep(n,k*j)
                    coeffs[r]=(coeffs[r]+inv_d*pow(lam,(-t)%d,P)*coeff)%P
                # The character eigenspace is the 1-dimensional base-field
                # span of X^r_e: all other coefficients must cancel exactly.
                assert all(coeffs[r]==0 for r in range(L) if r!=r_e), (n,orbit,e,j,coeffs)
                arow.append(coeffs[r_e])
            A.append(arow)
    assert len(labels)==n and len(A)==n
    if reconstruct:
        for k in range(n):
            for j in range(n):
                lhs=[0]*L
                for (orbit,lam,r),arow in zip(labels,A):
                    if k in orbit:
                        t=orbit.index(k)
                        lhs[r]=(lhs[r]+pow(lam,t,P)*arow[j])%P
                rr,v=power_rep(n,k*j)
                assert all(lhs[r]==(v if r==rr else 0) for r in range(L)),(n,k,j, lhs,rr,v)
    return dict(n=n,L=L,possible_over_zeta8=True,
                orbit_size_histogram=dict(sorted(Counter(len(c) for c in groups).items())),
                eigenbasis_columns=len(labels),
                phase_mask_exponents=Counter(r for _,_,r in labels),
                A_base_field_coefficients=n*n,
                A_nonzero_coefficients=sum(val!=0 for row in A for val in row),
                all_A_rows_single_character=True,
                all_fourier_entries_reconstructed=reconstruct)


if __name__=='__main__':
    import json
    for n in (16,32,64,128,256):
        d=exact_single_mask_factor(n)
        d['phase_mask_exponents']=dict(d.get('phase_mask_exponents',{}))
        print(json.dumps(d,indent=2))
