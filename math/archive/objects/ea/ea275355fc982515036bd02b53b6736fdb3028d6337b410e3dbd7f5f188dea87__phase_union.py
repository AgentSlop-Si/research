"""Hero #17: exact O(N) quadratic-phase + rank-2 character detector/DFT.

Research implementation over F_p for odd N dividing p-1 (N>=7). A root of
exact order N must be supplied, and field arithmetic is counted at unit cost.

Outputs are UNNORMALIZED DFT coefficients F[k] = sum_j x[j] * omega^(-k*j).

A certified hit has input form
    x[j] = omega^(a*j*j) * sum_(b,c in modes) c*omega^(b*j)
with at most two modes, and with a=0 or gcd(a,N)=1.

All raw inputs are read and checked. Rejection is INCONCLUSIVE and must use
some fallback FFT/NTT for arbitrary inputs. No generic O(N) claim.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import gcd
from typing import Optional, Sequence


@dataclass(frozen=True)
class Certificate:
    n: int
    p: int
    omega: int
    a: int
    modes: tuple[tuple[int, int], ...]  # (frequency b, weight c)
    witness_start: int  # -1 for all-zero input
    candidate_count: int


def phase_table(n: int, p: int, omega: int) -> list[int]:
    """O(N) time/space; exact-order verification is charged, no oracle."""
    if n < 7 or n % 2 != 1 or p <= n:
        raise ValueError('Require odd N >= 7 and prime p > N')
    powers = [1] * n
    for j in range(1, n):
        powers[j] = powers[j-1] * omega % p
    if powers[-1] * omega % p != 1 or len(set(powers)) != n:
        raise ValueError('omega does not have exact multiplicative order N')
    return powers


def witness_coefficients(x: Sequence[int], p: int):
    """Find first *nonzero* quartic P_s(t) for length-5 Hankel minor.

    For t=omega^(-2*a), a quadratic dechirp gives y_j=x_j*t^{j(j-1)/2}
    locally, modulo a geometric factor.  Then det[y_(i+j)]_(i,j=0..2)
    = t^3 * (A*t^4 + B*t^3 + D*t + E), with this tuple (A,B,D,E).
    """
    for s in range(len(x) - 4):
        x0, x1, x2, x3, x4 = (x[s+i] % p for i in range(5))
        a = x0 * x2 * x4 % p
        b = (-x0*x3*x3 - x1*x1*x4) % p
        d = (2*x1*x2*x3) % p
        e = (-x2*x2*x2) % p
        if a or b or d or e:
            return s, (a,b,d,e)
    return None


def _eval_quartic(co: tuple[int,int,int,int], t: int, p:int) -> int:
    a,b,d,e = co
    return (((((a*t+b) % p)*t) % p)*t*t + d*t + e) % p


def _find_char_modes(y: Sequence[int], powers: Sequence[int], p: int):
    """Find exact <=2 Fourier-character decomposition in O(N) time."""
    n = len(y)
    if all(v % p == 0 for v in y):
        return ()
    # Rank 1: check each admissible phase by using the second sample.
    if y[0] % p:
        z = y[1] * pow(y[0], -1, p) % p
        for b, root in enumerate(powers):
            if root != z:
                continue
            v = y[0] % p
            for sample in y:
                if sample % p != v:
                    break
                v = v*root%p
            else:
                return ((b, y[0]%p),)
            break
    # Rank 2: solve one 2x2 recurrence system, then verify all N terms.
    delta = (y[1]*y[1] - y[0]*y[2]) % p
    if delta == 0:
        return None
    inv_delta = pow(delta,-1,p)
    u = (y[2]*y[1] - y[0]*y[3])*inv_delta%p
    v = (y[1]*y[3] - y[2]*y[2])*inv_delta%p
    roots = [(b, z) for b,z in enumerate(powers) if (z*z-u*z-v)%p==0]
    if len(roots) != 2:
        return None
    (b1,z1),(b2,z2)=roots
    c1 = (y[1]-z2*y[0])*pow((z1-z2)%p,-1,p)%p
    c2 = (y[0]-c1)%p
    if not c1 or not c2:
        return None
    t1=t2=1
    for yi in y:
        if (c1*t1+c2*t2-yi)%p:
            return None
        t1=t1*z1%p; t2=t2*z2%p
    return ((b1,c1),(b2,c2))


def recognize(x: Sequence[int], p: int, omega: int) -> Optional[Certificate]:
    """O(N) worst-case recognition on EVERY input, not only accepted ones."""
    n = len(x)
    powers = phase_table(n,p,omega)  # a fair fresh-input preparation charge
    x = [v%p for v in x]
    if not any(x):
        return Certificate(n,p,omega,0,(),-1,0)
    witness = witness_coefficients(x,p)
    if witness is None:
        return None
    start,coefficients=witness
    candidates=[]
    # a -> omega^(-2a) is bijective for odd N. Nonzero degree<=4
    # polynomial ensures at most FOUR candidate a values.
    for a in range(n):
        t=powers[(-2*a)%n]
        if _eval_quartic(coefficients,t,p)==0:
            candidates.append(a)
    assert len(candidates)<=4  # catches implementation errors
    for a in candidates:
        if a and gcd(a,n)!=1:
            continue   # this fast evaluator uses unit quadratic phases
        y=[x[j]*powers[(-a*j*j)%n]%p for j in range(n)]
        modes=_find_char_modes(y,powers,p)
        if modes is not None:
            return Certificate(n,p,omega,a,modes,start,len(candidates))
    return None


def transform_certified(cert: Certificate) -> list[int]:
    """Exact O(N) full DFT of a verified certificate. Never used unverified."""
    n,p,a=cert.n,cert.p,cert.a
    powers=phase_table(n,p,cert.omega)
    out=[0]*n
    if not cert.modes:
        return out
    if not a:
        for b,c in cert.modes:
            out[b] = (out[b]+n*c)%p
        return out
    if gcd(a,n)!=1:
        raise ValueError('non-unit quadratic coefficient unsupported')
    # Single reusable quadratic Gauss sum G(a), O(N).
    gauss = sum(powers[(a*j*j)%n] for j in range(n))%p
    inv4a = pow((4*a)%n, -1,n)
    for k in range(n):
        total=0
        for b,c in cert.modes:
            exponent=(-inv4a*(b-k)*(b-k))%n
            total += c*powers[exponent]
        out[k]=gauss*(total%p)%p
    return out


def transform_if_recognized(x:Sequence[int],p:int,omega:int):
    """Return (output,certificate) on success, or (None,None) for fallback."""
    cert=recognize(x,p,omega)
    if cert is None: return None,None
    return transform_certified(cert),cert


def direct_dft(x:Sequence[int],p:int,omega:int):
    """Quadratic reference O(N^2), for tests only."""
    n=len(x)
    phase=phase_table(n,p,omega)
    result=[]
    for k in range(n):
        z=phase[-k%n]
        factor=1;total=0
        for v in x:
            total=(total+v*factor)%p
            factor=(factor*z)%p
        result.append(total)
    return result


def make_signal(n,p,omega,a,modes):
    phase=phase_table(n,p,omega)
    return [sum(c*phase[(a*j*j+b*j)%n] for b,c in modes)%p
            for j in range(n)]
