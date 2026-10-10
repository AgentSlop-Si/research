"""Independent Phase23 bounded-seed candidate correction. No source imports.
Only enumerates candidate residues; caller retains raw verification and fallback.
"""
from math import gcd
from bisect import bisect_left

def _integer(x, name):
    if not isinstance(x, int) or isinstance(x, bool):
        raise TypeError(name + ' must be an integer')

def _domain(n, budget):
    _integer(n, 'n'); _integer(budget, 'seed_budget')
    if n < 3 or n % 2 == 0: raise ValueError('n must be odd and at least 3')
    if budget < 0: raise ValueError('seed_budget must be nonnegative')

def planned_seed_bound(n, s):
    """Existing strategy bound, not minimum seeds for every particular phase."""
    _domain(n, 0); _integer(s, 's')
    if not 0 <= s < n: raise ValueError('s must be a canonical residue')
    if s == 4: return 2
    return min(max(4, s), n-s+4 if s>4 else n, n//gcd(n,s))

def eligible_chirps(n, seed_budget, supported_s=None):
    """Exactly {s: 0<=s<n, planned_seed_bound(n,s)<=B}, optionally restricted.

    Enumerates O(B^2) integer candidates, plus gcd/sort factors, without an N
    scan for fixed B. Optional supported_s is consumed once; its length L adds
    O(L log(B+2)) validation/intersection work and is not assumed free.
    """
    _domain(n, seed_budget); b = seed_budget; candidates = []
    if b >= 4: candidates.extend(range(min(n, b+1)))
    candidates.extend(range(max(5, n+4-b), n))
    if n > 4 and b >= 2: candidates.append(4)
    for d in range(1, min(b,n)+1):
        if n % d == 0:
            step = n//d
            candidates.extend(k*step for k in range(d) if gcd(k,d)==1)
    candidates.sort()
    unique = []
    for s in candidates:
        if not unique or s != unique[-1]: unique.append(s)
    if supported_s is None: return tuple(unique)
    keep = [False] * len(unique)
    for s in supported_s:
        _integer(s, 'supported chirp')
        if not 0 <= s < n: raise ValueError('supported chirps must be canonical')
        i = bisect_left(unique, s)
        if i < len(unique) and unique[i] == s: keep[i] = True
    return tuple(s for s, included in zip(unique, keep) if included)
