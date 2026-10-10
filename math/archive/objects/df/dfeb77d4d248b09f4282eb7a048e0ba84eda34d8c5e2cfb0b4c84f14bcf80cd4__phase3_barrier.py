"""Phase 3: exact NTT/tabulation barrier and input-independent low-rank sharing.

The arithmetic identities are exact over prime fields. This module does NOT
claim to improve general DFT/NTT asymptotic complexity.
"""
from __future__ import annotations

from itertools import product
from math import isqrt, log2


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


def choose_ntt_prime(n: int) -> int:
    """Smallest prime q with n | (q-1), using trial division (small n)."""
    if n < 2 or (n & (n - 1)):
        raise ValueError("n must be a power of two >= 2")
    multiplier = 1
    while True:
        q = multiplier * n + 1
        if is_prime(q):
            return q
        multiplier += 1


def distinct_prime_factors(m: int) -> list[int]:
    result = []
    d = 2
    while d * d <= m:
        if m % d == 0:
            result.append(d)
            while m % d == 0:
                m //= d
        d += 1
    if m > 1:
        result.append(m)
    return result


def primitive_root(q: int) -> int:
    if not is_prime(q):
        raise ValueError("q must be prime")
    factors = distinct_prime_factors(q - 1)
    for candidate in range(2, q):
        if all(pow(candidate, (q - 1) // p, q) != 1 for p in factors):
            return candidate
    raise RuntimeError("primitive root not found")


def ntt_root(n: int, q: int) -> int:
    if (q - 1) % n:
        raise ValueError("n must divide q-1")
    root = pow(primitive_root(q), (q - 1) // n, q)
    assert pow(root, n, q) == 1
    assert n == 1 or pow(root, n // 2, q) != 1
    return root


def direct_ntt(a: list[int], q: int, root: int) -> list[int]:
    n = len(a)
    return [sum(a[j] * pow(root, j*k, q) for j in range(n)) % q
            for k in range(n)]


def radix2_ntt(a: list[int], q: int, root: int) -> list[int]:
    n = len(a)
    if n < 1 or (n & (n - 1)):
        raise ValueError("power of two needed")
    values = [x % q for x in a]
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            values[i], values[j] = values[j], values[i]
    m = 2
    while m <= n:
        wstep = pow(root, n // m, q)
        for start in range(0, n, m):
            w = 1
            for k in range(m // 2):
                u = values[start+k]
                v = (values[start+k + m//2] * w) % q
                values[start+k] = (u+v) % q
                values[start+k + m//2] = (u-v) % q
                w = (w * wstep) % q
        m *= 2
    return values


def inverse_ntt(spectrum: list[int], q: int, root: int) -> list[int]:
    n = len(spectrum)
    inv = pow(root, -1, q)
    inv_n = pow(n, -1, q)
    return [(x * inv_n) % q for x in radix2_ntt(spectrum, q, inv)]


def tabulate_butterfly(q: int) -> list[tuple[int,int]]:
    """All possible 2-point transforms over F_q; q^2 stored pairs."""
    return [((a+b) % q, (a-b) % q) for a in range(q) for b in range(q)]


def hadamard_matrix(n: int, modulus: int = 3) -> list[list[int]]:
    if n < 1 or n & (n - 1):
        raise ValueError("power of two required")
    return [[(1 if (i & j).bit_count() % 2 == 0 else -1) % modulus
             for j in range(n)] for i in range(n)]


def rank_one_sign_sparse(n: int, modulus: int = 3) -> dict:
    """Search rank-one sign matrices +/-u*v for sparse residual WHT.

    Exact for the *restricted* family where u,v have only +/-1 values.
    This is NOT a search over all rank-one matrices or all circuits.
    """
    H = hadamard_matrix(n, modulus)
    best = None
    for bits in product((-1, 1), repeat=n-1):
        u = (1,) + bits  # remove global sign symmetry
        v = []
        missed = 0
        for col in range(n):
            plus = sum(1 for row in range(n) if H[row][col] == (u[row] % modulus))
            minus = n - plus
            if plus >= minus:
                v.append(1)
                missed += minus
            else:
                v.append(-1)
                missed += plus
        if best is None or missed < best[0]:
            best = (missed, u, tuple(v))
    sparse = []
    for i in range(n):
        for j in range(n):
            val = (H[i][j] - best[1][i]*best[2][j]) % modulus
            if val:
                sparse.append((i,j,val))
    assert len(sparse) == best[0]
    return {"n":n,"p":modulus,"u":list(best[1]),"v":list(best[2]),
            "sparse":sparse,"nonzero":len(sparse),"dense":n*n}


def apply_rank_one_sparse(cert: dict, x: list[int]) -> list[int]:
    p = cert["p"]
    n = cert["n"]
    if len(x) != n:
        raise ValueError("bad input length")
    scalar = sum(cert["v"][j]*x[j] for j in range(n)) % p
    out = [cert["u"][i]*scalar % p for i in range(n)]
    for i,j,value in cert["sparse"]:
        out[i] = (out[i] + value*x[j]) % p
    return out


def run_summary() -> None:
    print("Exact NTT: required field size and all-input table growth")
    print("N       q       q^2 entries for a complete 2-point lookup")
    for n in (8,16,32,64,128,256,512,1024):
        q = choose_ntt_prime(n)
        print(f"{n:<7} {q:<7} {q*q:,}")
    print("\nLow-rank + sparse WHT decomposition over F_3 (restricted sign-rank-one search)")
    for n in (2,4,8):
        c = rank_one_sign_sparse(n)
        print(f"n={n}: dense={c['dense']} sparse_residual={c['nonzero']} rank=1")
    print("\nNo general NTT or complex-FFT sub-NlogN claim.")


if __name__ == "__main__":
    run_summary()
