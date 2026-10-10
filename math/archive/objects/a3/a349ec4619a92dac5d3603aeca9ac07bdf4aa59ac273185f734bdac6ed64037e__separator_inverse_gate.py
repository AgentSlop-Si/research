from __future__ import annotations
import itertools
import random
from algebra_utils import MOD, inv_mod, rank_mod, submatrix, primitive_root_of_order


def fourier(n: int, p: int = MOD):
    w = primitive_root_of_order(n, p)
    return [[pow(w, i*j, p) for j in range(n)] for i in range(n)]


def block_separator_matrix(u: int, s: int, v: int, rng: random.Random, p: int = MOD):
    n = u+s+v
    for _ in range(200):
        a = [[0]*n for _ in range(n)]
        # Random full blocks except U-V and V-U, with strong nonzero diagonals.
        for i in range(n):
            a[i][i] = rng.randrange(1, p)
        U = range(0,u); S = range(u,u+s); V = range(u+s,n)
        allowed = [(U,U),(U,S),(S,U),(S,S),(S,V),(V,S),(V,V)]
        for rr, cc in allowed:
            for i in rr:
                for j in cc:
                    if i != j and rng.random() < 0.55:
                        a[i][j] = rng.randrange(p)
        try:
            ainv = inv_mod(a,p)
            inv_mod(submatrix(a,U,U),p)
            return a, ainv, list(U), list(S), list(V)
        except ValueError:
            continue
    raise RuntimeError("failed to build invertible separator matrix")


def separator_checks(seed: int = 1903):
    rng = random.Random(seed)
    out=[]
    for u,s,v in ((5,1,5),(6,2,6),(7,3,7),(8,4,8)):
        a,ainv,U,S,V=block_separator_matrix(u,s,v,rng)
        r=rank_mod(submatrix(ainv,U,V))
        if r>s:
            raise AssertionError((u,s,v,r))
        out.append({"u":u,"separator":s,"v":v,"inverse_cross_rank":r})
    # Fourier regression at N=17: a 7x7 cross block is full rank, exceeding separator 3.
    f=fourier(17)
    U=list(range(7));V=list(range(10,17))
    fr=rank_mod(submatrix(f,U,V))
    if fr != 7:
        raise AssertionError("Fourier cross block not full rank")
    out.append({"fourier_n":17,"u":7,"separator_candidate":3,"v":7,"fourier_cross_rank":fr})
    return out


def treewidth_lower_bound(n: int) -> int:
    """The theorem's necessary lower bound w >= ceil(n/4)-1."""
    return (n + 3)//4 - 1


if __name__ == "__main__":
    import json
    print(json.dumps({"checks":separator_checks(),
                      "treewidth_bounds":[{"n":n,"w_min":treewidth_lower_bound(n)} for n in (17,101,1009)]},indent=2))
