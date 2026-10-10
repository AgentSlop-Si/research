"""Independent exact finite-field checks of orbit identities.

IMPORTANT: these tests do NOT prove complex-valued closeness or packing;
those follow analytically and are illustrated separately at high precision.
"""
from __future__ import annotations

import random
from orbit_stability import complementary_signal, folded_odd_coefficients, canonical_representatives

P=998244353
PRIMITIVE=3


def direct_dft(x:list[int], root:int) -> list[int]:
    n=len(x)
    out=[]
    for k in range(n):
        w=pow(root,k,P)
        cur=1
        acc=0
        for v in x:
            acc=(acc+v*cur)%P
            cur=(cur*w)%P
        out.append(acc)
    return out


def signed_orbit_powerbasis(coeffs:tuple[int,...], k:int)->tuple[int,...]:
    m=len(coeffs);n=2*m
    if k%2!=1:
        raise ValueError("odd k only")
    out=[0]*m
    for j,c in enumerate(coeffs):
        i=(k*j)%n
        if i>=m:
            out[i-m]-=c
        else:
            out[i]+=c
    assert sorted(map(abs,out))==sorted(map(abs,coeffs))
    return tuple(out)


def run_exact_audit()->dict:
    rng=random.Random(20261009)
    tested=0
    orbit_checks=0
    even_checks=0
    tests={}
    for n in (8,16,32,64):
        assert (P-1)%n==0
        omega=pow(PRIMITIVE,(P-1)//n,P)
        assert pow(omega,n,P)==1 and pow(omega,n//2,P)==P-1
        reps=canonical_representatives(n)
        assert len(reps)==n.bit_length()
        masks=[0,(1<<(n//2))-1,1]+[rng.randrange(1<<(n//2)) for _ in range(25)]
        for u in masks:
            x=complementary_signal(u,n)
            all_bins=direct_dft(list(x),omega)
            assert all_bins[0] == n//2
            assert all(v==0 for v in all_bins[2::2])
            even_checks+=n//2
            coeff=folded_odd_coefficients(u,n)
            for k in range(1,n,2):
                form=signed_orbit_powerbasis(coeff,k)
                val=sum(c*pow(omega,j,P) for j,c in enumerate(form))%P
                direct=sum(c*pow(omega,(k*j)%n,P) for j,c in enumerate(coeff))%P
                assert val == direct == all_bins[k]
                orbit_checks+=1
            tested+=1
        tests[str(n)]={"representatives":reps,"vectors":len(masks)}
    return {"sizes":tests,"vectors":tested,"even_coordinate_checks":even_checks,"odd_orbit_checks":orbit_checks}


if __name__=="__main__":
    print(run_exact_audit())
