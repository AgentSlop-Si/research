"""Exact fresh-input DFT fast path from weighted affine-cycle defects.

This is a detected input class, not an arbitrary-input faster FFT.
Every field operation performed by the evaluator, including setup, is counted.
"""
from collections import Counter


class Counted:
    def __init__(self, field):
        self.field = field
        self.zero, self.one = field.zero, field.one
        self.count = Counter()
    def add(self, a, b): self.count['add'] += 1; return self.field.add(a, b)
    def sub(self, a, b): self.count['sub'] += 1; return self.field.sub(a, b)
    def mul(self, a, b): self.count['mul'] += 1; return self.field.mul(a, b)
    def inv(self, a): self.count['inverse'] += 1; return self.field.inv(a)


def cycle_order(permutation):
    n = len(permutation); order = []; seen = [False]*n; j = 0
    while not seen[j]:
        seen[j] = True; order.append(j); j = permutation[j]
    if j != 0 or len(order) != n:
        raise ValueError('required one full cycle')
    return order


def solve_cycle(c, permutation, coefficients, rhs):
    """Solve y_j - coefficients[j] y_perm(j) = rhs_j.

    Returns None exactly when the one-cycle matrix is singular. No divisions
    by edge weights are needed, including when all edge weights are zero.
    """
    order = cycle_order(permutation)
    product = c.one
    for j in order: product = c.mul(product, coefficients[j])
    denominator = c.sub(c.one, product)
    if denominator == c.zero: return None
    value = c.zero
    for j in reversed(order): value = c.add(rhs[j], c.mul(coefficients[j], value))
    value = c.mul(value, c.inv(denominator))
    result = [c.zero] * len(order)
    for j in reversed(order):
        value = c.add(rhs[j], c.mul(coefficients[j], value))
        result[j] = value
    return result


def try_affine_fourier(field, query, q, max_defects=1, a=5, b=1, shift=1,
                       supplied_lambda=None):
    """Return complete DFT or an explicit decline, with a cold operation bill.

    Mx[j] = q**(b*j) * x[(a*j+shift) mod N].
    Fourier-conjugate Mhat y[k] = q**(-shift*a^-1*(k+b))
                                  * y[a^-1*(k+b)].
    For a=1 mod 4, odd b,shift, both permutations are full dyadic cycles.
    """
    n = len(query)
    if n < 4 or n & (n-1): raise ValueError('dyadic N >= 4 required')
    if not isinstance(max_defects, int) or max_defects < 0: raise ValueError('invalid defect budget')
    if any(not isinstance(v, int) for v in (a,b,shift)): raise ValueError('integer affine parameters required')
    if a % 4 != 1 or b % 2 != 1 or shift % 2 != 1:
        raise ValueError('a=1 mod 4 and odd b,shift required')
    c = Counted(field); stages = {}; previous = {}
    def checkpoint(name):
        nonlocal previous
        stages[name] = {k:v-previous.get(k,0) for k,v in c.count.items() if v != previous.get(k,0)}
        previous = dict(c.count)
    def finish(result, reason, **extra):
        meta = dict(accepted=result is not None, reason=reason, stages=stages,
                    field_operations=dict(c.count), all_input_rows_read=n,
                    full_output_writes=n if result is not None else 0,
                    ordinary_fft_calls=0, maximum_defects=max_defects,
                    source_a=a % n, source_b=b % n, source_shift=shift % n)
        meta.update(extra)
        return result, meta
    powers = [c.one]
    for _ in range(1,n): powers.append(c.mul(powers[-1],q))
    if c.mul(powers[-1],q) != c.one or powers[n//2] == c.one:
        raise ValueError('primitive Nth root required')
    source = [(a*j+shift) % n for j in range(n)]
    inverse_a = pow(a,-1,n)
    target = [(inverse_a*(k+b)) % n for k in range(n)]
    cycle_order(source); cycle_order(target)
    checkpoint('roots_and_graphs')
    weighted = [c.mul(powers[(b*j) % n], query[source[j]]) for j in range(n)]
    if all(v == c.zero for v in query):
        checkpoint('zero_input_check')
        return finish([c.zero]*n, 'zero_input', actual_defects=0)
    parameter = supplied_lambda
    nonzero_denominators = sum(v != c.zero for v in weighted)
    if parameter is None:
        if nonzero_denominators <= 2*max_defects:
            checkpoint('discovery')
            return finish(None, 'insufficient_majority_support')
        candidate = None; votes = 0
        for numerator, denominator in zip(query, weighted):
            if denominator == c.zero: continue
            if votes == 0:
                candidate = (numerator, denominator); votes = 1
            elif c.mul(numerator, candidate[1]) == c.mul(candidate[0], denominator):
                votes += 1
            else: votes -= 1
        parameter = c.mul(candidate[0], c.inv(candidate[1]))
    checkpoint('discovery')
    residual = [c.sub(value, c.mul(parameter, weighted[j])) for j,value in enumerate(query)]
    defects = [(j,v) for j,v in enumerate(residual) if v != c.zero]
    checkpoint('complete_residual_verification')
    if len(defects) > max_defects:
        return finish(None, 'defect_budget_exceeded', actual_defects=len(defects))
    forcing = [c.zero]*n
    for j,value in defects:
        for k in range(n): forcing[k] = c.add(forcing[k], c.mul(value,powers[(j*k)%n]))
    coefficients = [c.mul(parameter,powers[(-shift*j)%n]) for j in target]
    checkpoint('sparse_defect_transform_and_target')
    result = solve_cycle(c,target,coefficients,forcing)
    checkpoint('weighted_cycle_solve')
    return finish(result, 'accepted' if result is not None else 'singular_target_cycle',
                  actual_defects=len(defects), parameter=field.encode(parameter),
                  nonzero_input_entries=sum(v != c.zero for v in query))


def ordinary_fft(field, query, q):
    """Independent iterative radix-2 comparator, also with cold root preparation."""
    n=len(query); c=Counted(field); powers=[c.one]
    for _ in range(1,n): powers.append(c.mul(powers[-1],q))
    if c.mul(powers[-1],q)!=c.one or powers[n//2]==c.one: raise ValueError('bad root')
    result=list(query); j=0
    for i in range(1,n):
        bit=n//2
        while j&bit: j^=bit;bit//=2
        j^=bit
        if i<j: result[i],result[j]=result[j],result[i]
    width=2
    while width<=n:
        half=width//2
        for base in range(0,n,width):
            for i in range(half):
                even=result[base+i]; odd=c.mul(powers[i*n//width],result[base+i+half])
                result[base+i]=c.add(even,odd); result[base+i+half]=c.sub(even,odd)
        width*=2
    return result,dict(c.count)


def affine_fft_or_fallback(field, query, q, **kwargs):
    """All-input exact wrapper; for a fixed defect budget declines cost O(N)."""
    result,meta=try_affine_fourier(field,query,q,**kwargs)
    meta['fast_path_accepted']=meta['accepted']
    if result is not None: return result,meta
    result,baseline=ordinary_fft(field,query,q)
    meta['fallback_field_operations']=baseline
    meta['field_operations']=dict(Counter(meta['field_operations'])+Counter(baseline))
    meta['ordinary_fft_calls']=1
    meta['full_output_writes']=len(query)
    meta['accepted']=True
    return result,meta
