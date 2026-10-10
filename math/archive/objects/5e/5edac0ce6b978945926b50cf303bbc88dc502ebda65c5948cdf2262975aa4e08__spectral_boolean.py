"""Exact finite-field tests of Boolean spectral completion.

Objective: fresh binary x; all N Fourier bins; no cached answers.
All operations are in an odd-characteristic prime field containing Nth roots.
"""
from __future__ import annotations
from collections import OrderedDict
from itertools import combinations_with_replacement
from math import comb


def primitive_root(n: int, p: int) -> int:
    if n < 2 or n & (n - 1) or (p - 1) % n:
        raise ValueError("n must be a power of 2 dividing p-1")
    for base in range(2, p):
        r = pow(base, (p - 1)//n, p)
        if pow(r, n//2, p) != 1 and pow(r, n, p) == 1:
            return r
    raise ValueError("primitive Nth root not found")


def dft(x: list[int] | tuple[int,...], p: int, root: int | None = None) -> tuple[int, ...]:
    n = len(x)
    w = primitive_root(n, p) if root is None else root
    return tuple(sum(int(value)*pow(w, (k*j)%n,p) for j,value in enumerate(x)) % p
                 for k in range(n))


def all_binary(n: int):
    for code in range(1<<n):
        yield tuple((code>>i)&1 for i in range(n))


def spectrum_self_convolution(x_bins: list[int] | tuple[int,...], p:int) -> tuple[int,...]:
    n=len(x_bins)
    return tuple(sum(x_bins[a]*x_bins[(k-a)%n] for a in range(n))%p for k in range(n))


def recover_one_from_others(spectrum: list[int] | tuple[int,...], k:int, p:int):
    """Computes X[k] from every other X[a] and X[0], if 0 != k and N-2X[0]!=0.
    Does not read X[k]; unlike k=0, it has no hidden input dependence.
    """
    n=len(spectrum)
    if k <= 0 or k>=n:
        raise ValueError("only nonzero missing frequencies")
    divisor=(n-2*spectrum[0])%p
    if not divisor:
        return None
    numerator=sum(spectrum[a]*spectrum[(k-a)%n]
                  for a in range(n) if a!=0 and a!=k) %p
    return numerator*pow(divisor,-1,p)%p


def signature_collision(n:int, seen_indices:tuple[int,...], missing_index:int, p:int):
    """Exact injectivity counterexample. 2^n brute-force only for small n."""
    if n>16:raise ValueError("n>16 requires exponential enumeration")
    w=primitive_root(n,p)
    seen={}
    for x in all_binary(n):
        f=dft(x,p,w)
        key=tuple(f[i] for i in seen_indices)
        prev=seen.get(key)
        if prev is None:
            seen[key]=(x, f[missing_index])
        elif prev[1]!=f[missing_index]:
            return {"x":list(prev[0]), "y":list(x), "same_bins":list(seen_indices),
                    "missing":missing_index,"x_missing":prev[1],"y_missing":f[missing_index]}
    return None


def _monomial_indice_tuples(q:int,max_degree:int):
    yield ()
    for degree in range(1,max_degree+1):
        yield from combinations_with_replacement(range(q),degree)


def _field_eliminate(col:list[int], coeffs:dict[int,int], pivots:OrderedDict,
                     p:int):
    """Elimination with algebraic combination trace for independent certificates."""
    c=col[:]
    combo=coeffs.copy()
    for pivot,(basis,bcomb) in pivots.items():
        x=c[pivot]
        if not x:continue
        c=[(a-x*b)%p for a,b in zip(c,basis)]
        for idx,mul in bcomb.items():
            combo[idx]=(combo.get(idx,0)-x*mul)%p
            if combo[idx]==0:del combo[idx]
    lead=next((i for i,v in enumerate(c) if v),None)
    if lead is None:return None
    inv=pow(c[lead],-1,p)
    norm=([(v*inv)%p for v in c], {i:(v*inv)%p for i,v in combo.items()})
    pivots[lead]=norm
    return lead


def _try_reduce_goal(goal:list[int],pivots:OrderedDict,p:int):
    v=goal[:]
    solution={}
    for lead,(base,combo) in pivots.items():
        x=v[lead]
        if not x:continue
        v=[(a-x*b)%p for a,b in zip(v,base)]
        for idx,coef in combo.items():
            solution[idx]=(solution.get(idx,0)+x*coef)%p
            if solution[idx]==0:del solution[idx]
    return solution if not any(v) else None


def exact_poly_completion(n:int,p:int,known_modes:tuple[int,...],missing:int,max_degree:int=3):
    """Small exhaustive Boolean cube polynomial synthesis and rank certificates.

    Returns a polynomial in the known DFT bins if possible, with exact coefficients.
    The computational search grows exponentially with n. This is NOT a fast FFT.
    """
    if n>8:raise ValueError("exhaustive witness generation limited to n<=8")
    if missing in known_modes or not known_modes:raise ValueError("invalid source/target")
    if len(set(known_modes))!=len(known_modes):raise ValueError("duplicate source")
    w=primitive_root(n,p)
    vectors=list(all_binary(n))
    full=[dft(x,p,w) for x in vectors]
    obs=[tuple(f[s] for s in known_modes) for f in full]
    goal=[f[missing] for f in full]
    pivots=OrderedDict()
    mons=[];stats=[];winner=None
    for degree in range(max_degree+1):
        for indexset in ( [()] if degree==0 else combinations_with_replacement(range(len(known_modes)),degree) ):
            mons.append(indexset)
            col=[1]*len(vectors)
            for t in indexset:
                col=[(a*v[t])%p for a,v in zip(col,obs)]
            _field_eliminate(col,{len(mons)-1:1},pivots,p)
        winner=_try_reduce_goal(goal,pivots,p)
        stats.append({"degree":degree,"features":len(mons),"rank":len(pivots),"recoverable":winner is not None})
        if winner is not None:break
    witness=[] if winner is None else [ (tuple(known_modes[t] for t in mons[idx]),coef)
                                       for idx,coef in sorted(winner.items()) ]
    return {"n":n,"p":p,"known_modes":known_modes,"missing_mode":missing,
            "rank_audit":stats,"witness":witness,"found":winner is not None}


def evaluate_witness(spectrum, witness, p:int):
    out=0
    for modes,coef in witness:
        x=coef
        for m in modes:x=x*spectrum[m]%p
        out=(out+x)%p
    return out


def witness_upper_operation_count(witness):
    """Naive scalar-arithmetic gate count, assuming source frequency values given.
    Nonunit coefficients are one multiplication. Summation of terms takes T-1 adds.
    """
    mul=sum(max(0,len(modes)-1)+(coef not in (0,1)) for modes,coef in witness)
    add=max(0,len(witness)-1)
    return {"multiplications":mul,"additions":add,"total":mul+add,
            "nonzero_monomials":len(witness)}


def sumset_access(n:int,source_modes:tuple[int,...],depth:int)->set[int]:
    """Necessary one-hot Fourier-character frequency support for degree<=depth."""
    reach={0}
    for _ in range(depth):
        reach|={(a+b)%n for a in tuple(reach) for b in source_modes}
    return reach


def quadratic_rigidity_theorem(n:int,source_modes:tuple[int,...],target:int):
    """Returns theorem applicability, NOT a numerical proof of complexity.
    Any quadratic P of the known modes representing target on Boolean cube
    would have A^T C A diagonal; its diagonal must vanish because the proper
    Fourier rowspace contains no coordinate basis vector.
    """
    if len(set(source_modes))!=len(source_modes) or target in source_modes:
        raise ValueError("target must be unseen, source modes distinct")
    if any(k<0 or k>=n for k in source_modes):raise ValueError("out of range")
    return {"n":n,"proper_subset":len(source_modes)<n,
            "no_degree_le_2_completion":len(source_modes)<n,
            "proof":"Any quadratic term A^T C A with zero off-diagonal has diagonal image in span(F_S). An N-point Fourier rowspace omitting any frequency contains no standard basis vector, hence the diagonal is zero and no new frequency is generated."}


def half_complement_family(n:int):
    """2^(N/2) fresh binary inputs with identical even frequency spectra."""
    if n%2 or n>24:raise ValueError
    h=n//2
    for bits in all_binary(h):
        yield tuple(bits)+tuple(1-b for b in bits)


def balance_failure_fraction(n):
    return (comb(n,n//2),1<<n) if n%2==0 else (0,1<<n)
