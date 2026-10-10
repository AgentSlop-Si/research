from __future__ import annotations
import random
from algebra_utils import (
    MOD, GENERATOR, eye, mat_add, mat_mul, mat_pow, mat_scale, mat_sub,
    inv, inv_mod, permutation_matrix, primitive_root_of_order, zeros,
)


def green(pmat, alpha: int, p: int = MOD):
    n = len(pmat)
    return inv_mod(mat_sub(eye(n), mat_scale(alpha, pmat, p), p), p)


def character_packet_direct(pmat, alpha: int, b: int, s: int, p: int = MOD):
    """(1/b) sum_r xi^(-rs) (I-alpha xi^r P)^-1."""
    xi = primitive_root_of_order(b, p, GENERATOR)
    out = zeros(len(pmat), len(pmat))
    for r in range(b):
        weight = pow(xi, (-r * s) % b, p)
        gr = green(pmat, alpha * pow(xi, r, p) % p, p)
        out = mat_add(out, mat_scale(weight, gr, p), p)
    return mat_scale(inv(b, p), out, p)


def character_packet_fused(pmat, alpha: int, b: int, s: int, p: int = MOD):
    ap = mat_scale(alpha, pmat, p)
    numerator = mat_pow(ap, s, p)
    denominator = mat_sub(eye(len(pmat)), mat_pow(ap, b, p), p)
    return mat_mul(numerator, inv_mod(denominator, p), p)


def weight_dft(weights: list[int], p: int = MOD):
    """hat[s]=(1/b) sum_r weights[r] xi^(r s)."""
    b = len(weights)
    xi = primitive_root_of_order(b, p, GENERATOR)
    ib = inv(b, p)
    return [ib * sum(weights[r] * pow(xi, (r * s) % b, p) for r in range(b)) % p
            for s in range(b)]


def weighted_packet_direct(pmat, alpha: int, weights: list[int], p: int = MOD):
    b = len(weights)
    xi = primitive_root_of_order(b, p, GENERATOR)
    out = zeros(len(pmat), len(pmat))
    for r, c in enumerate(weights):
        gr = green(pmat, alpha * pow(xi, r, p) % p, p)
        out = mat_add(out, mat_scale(c, gr, p), p)
    return out


def weighted_packet_fused(pmat, alpha: int, weights: list[int], p: int = MOD):
    b = len(weights)
    hats = weight_dft(weights, p)
    ap = mat_scale(alpha, pmat, p)
    den_inv = inv_mod(mat_sub(eye(len(pmat)), mat_pow(ap, b, p), p), p)
    numerator = zeros(len(pmat), len(pmat))
    power = eye(len(pmat))
    for s, hs in enumerate(hats):
        if hs:
            numerator = mat_add(numerator, mat_scale(b * hs % p, power, p), p)
        power = mat_mul(power, ap, p)
    return mat_mul(numerator, den_inv, p)


def random_permutation(n: int, rng: random.Random):
    x = list(range(n)); rng.shuffle(x); return x


def run_packet_checks(seed: int = 1901):
    rng = random.Random(seed)
    cases = []
    for n in (5, 7, 9, 12):
        perm = random_permutation(n, rng)
        pmat = permutation_matrix(perm)
        for b in (2, 4, 8):
            alpha = rng.randrange(2, MOD - 1)
            # retry only if a denominator is singular
            for _ in range(50):
                try:
                    for s in range(b):
                        lhs = character_packet_direct(pmat, alpha, b, s)
                        rhs = character_packet_fused(pmat, alpha, b, s)
                        if lhs != rhs:
                            raise AssertionError("packet identity failed")
                    weights = [rng.randrange(MOD) for _ in range(b)]
                    lhs = weighted_packet_direct(pmat, alpha, weights)
                    rhs = weighted_packet_fused(pmat, alpha, weights)
                    if lhs != rhs:
                        raise AssertionError("weighted packet identity failed")
                    hats = weight_dft(weights)
                    cases.append({
                        "n": n, "b": b,
                        "character_cases": b,
                        "weight_spectrum_support": sum(v != 0 for v in hats),
                    })
                    break
                except ValueError:
                    alpha = rng.randrange(2, MOD - 1)
            else:
                raise RuntimeError("could not find nonsingular packet")
    return cases


if __name__ == "__main__":
    import json
    print(json.dumps(run_packet_checks(), indent=2))


def perm_power_map(perm: list[int], e: int) -> list[int]:
    n=len(perm)
    out=list(range(n)); base=perm[:]
    while e:
        if e&1:
            out=[base[out[j]] for j in range(n)]
        base=[base[base[j]] for j in range(n)]
        e>>=1
    return out


def apply_perm(perm: list[int], x: list[int], p: int = MOD):
    out=[0]*len(x)
    for j,i in enumerate(perm):
        out[i]=x[j]%p
    return out


def solve_green_permutation(perm: list[int], gamma: int, x: list[int], p: int = MOD):
    """Solve (I-gamma P)y=x in O(N) field operations for any permutation P."""
    n=len(perm); gamma%=p
    seen=[False]*n; y=[0]*n
    for start in range(n):
        if seen[start]: continue
        cyc=[]; j=start
        while not seen[j]:
            seen[j]=True;cyc.append(j);j=perm[j]
        L=len(cyc)
        # Equations along P-cycle: y[v_k]-gamma*y[v_{k-1}]=x[v_k].
        # Close at k=0 and solve for y[v_0].
        rhs=x[cyc[0]]%p
        gp=gamma
        for kk in range(L-1,0,-1):
            rhs=(rhs+gp*(x[cyc[kk]]%p))%p
            gp=gp*gamma%p
        den=(1-pow(gamma,L,p))%p
        y[cyc[0]]=rhs*inv(den,p)%p
        for kk in range(1,L):
            y[cyc[kk]]=(x[cyc[kk]]+gamma*y[cyc[kk-1]])%p
    return y


def character_packet_apply_direct(perm, alpha:int, b:int, s:int, x:list[int], p:int=MOD):
    xi=primitive_root_of_order(b,p,GENERATOR)
    out=[0]*len(x); ib=inv(b,p)
    for r in range(b):
        weight=pow(xi,(-r*s)%b,p)
        yr=solve_green_permutation(perm,alpha*pow(xi,r,p)%p,x,p)
        for i,v in enumerate(yr): out[i]=(out[i]+weight*v)%p
    return [ib*v%p for v in out]


def character_packet_apply_fused(perm,alpha:int,b:int,s:int,x:list[int],p:int=MOD):
    pb=perm_power_map(perm,b)
    z=solve_green_permutation(pb,pow(alpha,b,p),x,p)
    ps=perm_power_map(perm,s)
    z=apply_perm(ps,z,p)
    scale=pow(alpha,s,p)
    return [scale*v%p for v in z]


def run_apply_checks(seed:int=1904):
    rng=random.Random(seed); rec=[]
    for n in (31,127,509):
        perm=list(range(1,n))+[0]  # Hamiltonian cycle
        x=[rng.randrange(MOD) for _ in range(n)]
        for b in (2,4,8,16):
            alpha=7
            for s in (0,1,b//2,b-1):
                try:
                    a=character_packet_apply_direct(perm,alpha,b,s,x)
                    c=character_packet_apply_fused(perm,alpha,b,s,x)
                except ZeroDivisionError:
                    alpha+=2; continue
                if a!=c: raise AssertionError((n,b,s))
                rec.append({"n":n,"b":b,"s":s,"match":True})
    return rec
