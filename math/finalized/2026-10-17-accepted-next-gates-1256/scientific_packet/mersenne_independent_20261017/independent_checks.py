#!/usr/bin/env python3
"""Fresh standard-library checks for Taylor packing; no historical code imported."""
import hashlib
import itertools
import json
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
counts = {}
def count(name, n=1):
    counts[name] = counts.get(name, 0) + n

def shift_direct(a):
    k = len(a)
    return [sum(math.comb(i, j) * a[i] for i in range(j, k)) for j in range(k)]

def shift_horner(a):
    c = []
    for x in reversed(a):
        old = c
        c = [0] * (len(old) + 1)
        for j, value in enumerate(old):
            c[j] += value
            c[j+1] += value
        c[0] += x
    return c

def pack(c, p, s):
    return [sum(value * p**t for t, value in enumerate(c[r:r+s]))
            for r in range(0, len(c), s)]

def unpack_value(u, p, s):
    return sum(value * p**(s*r) for r, value in enumerate(u))

def binary_value(a, m):
    return sum(value << (m*i) for i, value in enumerate(a))

def divisors(k):
    return [s for s in range(1, k+1) if k % s == 0]

def check_one(a, m, s):
    p = (1 << m) - 1
    k = len(a)
    c = shift_direct(a)
    assert c == shift_horner(a)
    u = pack(c, p, s)
    assert unpack_value(u, p, s) == binary_value(a, m)
    assert all(x >= 0 for x in u)
    cmax = [p * math.comb(k, j+1) for j in range(k)]
    umax = pack(cmax, p, s)
    assert all(x <= xmax for x, xmax in zip(u, umax))
    h = m*s + k + 1
    assert all(value.bit_length() <= h for value in u)
    w = sum(value.bit_length() for value in u)
    wmax = sum(value.bit_length() for value in umax)
    assert w <= wmax
    if k % s == 0:
        # Integer forms of the candidate's uniform constants.
        assert w <= m*k + 2*k*k//s
        assert 64*s*wmax >= 3*(m*k*s + k*k)
        # Independent binomial-log lower bound, avoiding floating point.
        assert sum(min(j, k-j) for j in range(1,k+1)) == k*k//4
        assert all(math.comb(k,j) >= 1 << min(j,k-j) for j in range(1,k+1))
    count('individual_representation_checks')
    return tuple(u)

# Exhaustive legal inputs, including the all-maximum simultaneous witness.
for m, largest_k in [(2, 6), (3, 4), (4, 3)]:
    p = (1 << m) - 1
    for k in range(1, largest_k+1):
        seen = {s: {} for s in divisors(k)}
        for a in itertools.product(range(p+1), repeat=k):
            x = binary_value(a, m)
            for s in divisors(k):
                state = check_one(a, m, s)
                assert state not in seen[s] or seen[s][state] == x
                seen[s][state] = x
                count('legal_injectivity_checks')
        for s in divisors(k):
            assert len(seen[s]) == (p+1)**k

rng = random.Random(20261017)
for _ in range(800):
    m = rng.choice([2,3,4,5,7,13,31])
    k = rng.randint(1,128)
    p = (1 << m) - 1
    s = rng.choice(divisors(k))
    a = [rng.randrange(p+1) for _ in range(k)]
    check_one(a,m,s)
    check_one([p]*k,m,s)
    check_one([0]*k,m,s)

# Witness checked in its correct degree-safe domain, s | K and 1 < s < K.
for m in [2,3,4,7,13]:
    p = (1 << m) - 1
    for k in range(2,70):
        for s in divisors(k):
            if not 1 < s < k:
                continue
            f = [0]*k
            f[s-1], f[s-2] = 1, -p
            assert s-1 <= k-2
            ef = pack(f,p,s)
            g = [f[j] + (f[j-1] if j else 0) for j in range(k)]
            eg = pack(g,p,s)
            assert ef == [0]*(k//s)
            assert eg == [-p**s,1]+[0]*(k//s-2)
            # f(z)=A(z+1) implies A(x)=f(x-1). This is not a legal-input difference.
            inverse = [sum(math.comb(j,i)*f[j]*(-1)**(j-i) for j in range(i,k))
                       for i in range(k)]
            assert shift_direct(inverse) == f
            assert abs(inverse[0]) == p+1 > p
            count('degree_safe_nonintertwining_witnesses')

# Fully materialized product volume and exact diagonal reconstruction.
volume_rows=[]
for m in [2,3,4,7,13]:
    p = (1<<m)-1
    for d in [1,2,3]:
        for M in [2,3,4,7]:
            k,s = d*M*M,d*M
            a=[p]*k
            u=pack(shift_direct(a),p,s)
            n=m*k
            W=sum(x.bit_length() for x in u)
            Q=sum((x*y).bit_length() for x in u for y in u)
            assert 2*M*W-M*M <= Q <= 2*M*W
            assert 2*Q >= 3*M*W
            count('eager_product_volume_checks')
            volume_rows.append({'m':m,'d':d,'M':M,'N':n,'input_block_bits':W,
                                'eager_pair_product_bits':Q})
            for pair in range(4):
                aa=a if pair==0 else [rng.randrange(p+1) for _ in range(k)]
                bb=a if pair==0 else [rng.randrange(p+1) for _ in range(k)]
                uu=pack(shift_direct(aa),p,s)
                vv=pack(shift_direct(bb),p,s)
                diag=[0]*(2*M-1)
                for i,x in enumerate(uu):
                    for j,y in enumerate(vv):
                        diag[i+j]+=x*y
                exact=binary_value(aa,m)*binary_value(bb,m)
                assert unpack_value(diag,p,s)==exact
                value=diag[-1]
                max_shift=value.bit_length()
                for coeff in reversed(diag[:-1]):
                    for _ in range(s):
                        shifted=value<<m
                        max_shift=max(max_shift,shifted.bit_length())
                        value=shifted-value
                        assert value<=exact
                    value+=coeff
                    assert value<=exact
                assert value==exact
                assert max_shift<=2*n+1
                count('full_matrix_reconstruction_checks')

# Explicit off-by-one scratch-width counterexample to the initial draft.
m,d,M,k,s=2,1,2,4,2
u=pack(shift_direct([3]*4),3,2)
assert u==[66,21]
diag=[4356,2772,441]
assert 20223*4==80892 and (80892).bit_length()==17
assert (255*255).bit_length()==16
counterexample={'m':2,'d':1,'M':2,'K':4,'s':2,'X':255,'Y':255,
                'blocks':u,'diagonal_sums':diag,'pre_shift_value':20223,
                'shift_temporary':80892,'shift_temporary_bits':17,
                'product':65025,'product_bits':16}

result={'status':'PASS','seed':20261017,'counts':counts,
        'scope':'New exact-arithmetic controls; not timing or a proof assistant.',
        'scratch_width_counterexample':counterexample,'volume_rows':volume_rows}
(HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','counts':counts},indent=2))
