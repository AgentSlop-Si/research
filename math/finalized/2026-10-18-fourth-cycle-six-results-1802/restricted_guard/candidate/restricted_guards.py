"""Height-aware exact reconstruction from correlated product samples.

Production wide products go through the pinned terminating Karatsuba backend.
Remaining products are explicit shifts/adds by declared short nonnegative integers.
This is a bounded-window bit-cost model, not a Python timing claim.
"""
from dependencies.guarded_sharing import (mul_small, odd_divide_bits,
    horner_mod, interpolate_consecutive, guard_for_degree)
from dependencies.kernel_stream import karatsuba
from dependencies.accepted_product_interface import (shift_mod,
    binary_chunks, reconstruct_binary)


def product_bounds(m, length):
    assert m >= 1 and length >= 1
    # Exact (2**m-1)**2 without an uncharged wide product.
    square = (1 << (2*m)) - (1 << (m+1)) + 1
    cap = 2*m+(length-1).bit_length()+1
    return [mul_small(square, min(j+1, 2*length-1-j, length), cap)
            for j in range(2*length-1)]


def envelope_precision(bounds):
    assert bounds and all(v >= 0 for v in bounds)
    return max(guard_for_degree(j)+max(1,v.bit_length())
               for j,v in enumerate(bounds))


def short_tail_decode(values, bounds, width, stats=None):
    """Leading-coefficient peeling on a short coefficient box.

    All sample and table arithmetic has width `width`, never the large ambient
    chunk width. Requires bounds[j] < 2**(width-v2(j!)); width zero is allowed
    exactly when every coefficient is forced to zero.
    """
    n = len(values)
    assert n == len(bounds) and n >= 1 and width >= 0
    assert all(v >= 0 for v in bounds)
    if width == 0:
        assert all(v == 0 for v in bounds)
        if stats is not None:
            stats.update(tail_width=0, tail_table_small_actions=0,
                         tail_update_small_actions=0, tail_odd_division_steps=0,
                         tail_difference_subtractions=0, tail_max_coefficient=0)
        return [0]*n
    mask = (1 << width)-1
    assert all(0 <= v <= mask for v in values)
    odd, valuation, odds, vals = 1, 0, [], []
    factcap = max(1, (n-1)*max(1,(n-1).bit_length())+1)
    for j in range(n):
        if j:
            v = (j & -j).bit_length()-1
            valuation += v
            odd = mul_small(odd, j >> v, factcap)
        assert valuation <= width
        assert bounds[j] < (1 << (width-valuation))
        odds.append(odd); vals.append(valuation)
    # F[j][k] = Delta**k x**j at zero = k! S(j,k) modulo 2**width.
    F = [[0]*n for _ in range(n)]
    F[0][0] = 1 & mask
    table_actions = 0
    for j in range(1,n):
        for k in range(1,j+1):
            F[j][k] = mul_small((F[j-1][k]+F[j-1][k-1]) & mask,k,width)
            table_actions += 1
    differences = list(values)
    D = []
    for j in range(n):
        D.append(differences[0])
        differences = [(differences[k+1]-differences[k]) & mask
                       for k in range(len(differences)-1)]
    out = [0]*n
    odd_steps = 0
    updates = 0
    for j in range(n-1,-1,-1):
        v, bits = vals[j], width-vals[j]
        assert D[j] & ((1 << v)-1) == 0
        if bits == 0:
            assert bounds[j] == 0
            coefficient = 0
        else:
            coefficient = odd_divide_bits(D[j] >> v, odds[j], bits)
            odd_steps += bits
        assert coefficient <= bounds[j], (j, coefficient, bounds[j])
        out[j] = coefficient
        for k in range(j+1):
            D[k] = (D[k]-mul_small(F[j][k], coefficient,width)) & mask
            updates += 1
        assert D[j] == 0
    assert all(v == 0 for v in D)
    if stats is not None:
        stats.update(tail_width=width, tail_table_small_actions=table_actions,
                     tail_update_small_actions=updates,
                     tail_odd_division_steps=odd_steps,
                     tail_difference_subtractions=n*(n-1)//2,
                     tail_max_coefficient=max(bounds,default=0))
    return out


def height_decode(values, bounds, width=None, stats=None):
    """Recover all bounded nonnegative monomial coefficients exactly.

    n consecutive integer samples 0,...,n-1, each modulo 2**width.
    width >= max_j(v2(j!)+bit_length(bounds[j])) is sufficient.
    """
    n = len(values)
    assert n == len(bounds) and n >= 1
    minimum = envelope_precision(bounds)
    if width is None:
        width = minimum
    assert width >= minimum
    gamma = guard_for_degree(n-1)
    low_bits = width-gamma
    assert low_bits >= 1
    mask = (1 << width)-1
    assert all(0 <= x <= mask for x in values)
    low_stats = {}
    residues = interpolate_consecutive(values, low_bits, low_stats)
    tail_samples = []
    for point, value in enumerate(values):
        difference = (value-horner_mod(residues,point,width)) & mask
        assert difference & ((1 << low_bits)-1) == 0
        tail_samples.append(difference >> low_bits)
    tail_bounds = [v >> low_bits for v in bounds]
    tail_stats = {}
    tails = short_tail_decode(tail_samples,tail_bounds,gamma,tail_stats)
    out = [r+(q << low_bits) for r,q in zip(residues,tails)]
    assert all(x <= b for x,b in zip(out,bounds))
    if stats is not None:
        stats.update(W=width,Gamma=gamma,low_bits=low_bits,
                     coefficient_count=n,
                     low_interpolation=low_stats,
                     residual_horner_small_actions=n*n, **tail_stats)
    return out


def horner_signed(coefficients, point, width):
    if point >= 0:
        return horner_mod(coefficients,point,width)
    mask, out = (1 << width)-1, 0
    for c in reversed(coefficients):
        out = (c-mul_small(out,-point,width)) & mask
    return out


def restricted_convolution(left, right, m, product=karatsuba, stats=None,
                           translated=False):
    """Exactly 2L-1 sample products plus a height-aware final coefficient decoder.

    If translated=True, inputs are first transformed by the accepted paid
    Taylor map at precision W. Sampling at -1,...,2L-3 then produces the same
    original-product samples at 0,...,2L-2. The inverse Taylor step is fused
    with the height-aware reconstruction; it is not a raw arbitrary-ring API.
    """
    L = len(left)
    assert L >= 1 and len(right) == L and m >= 1
    assert all(0 <= x < (1 << m) for x in left+right)
    bounds = product_bounds(m,L)
    W = envelope_precision(bounds)
    H = 2*m+(L-1).bit_length()
    mask = (1 << W)-1
    if translated:
        c = shift_mod(left,1,W,product)
        d = shift_mod(right,1,W,product)
    else:
        c, d = list(left), list(right)
    samples, maximum = [], 0
    for r in range(2*L-1):
        point = r-1 if translated else r
        a = horner_signed(c,point,W)
        b = horner_signed(d,point,W)
        maximum = max(maximum,a.bit_length(),b.bit_length())
        samples.append(product(a,b) & mask)
    ledger = {}
    out = height_decode(samples,bounds,W,ledger)
    if stats is not None:
        stats.update(ledger,H=H,m=m,L=L,guard=max(0,W-H),
                     evaluation_products=2*L-1,maximum_sample_bits=maximum,
                     input_horner_small_actions=2*(2*L-1)*L,
                     forward_taylor_shifts=2 if translated else 0,
                     inverse_taylor_shifts=0)
    return out


def multiply_restricted(x,y,m,length,product=karatsuba,stats=None):
    a,b = binary_chunks(x,m,length), binary_chunks(y,m,length)
    ledger = {}
    coefficients = restricted_convolution(a,b,m,product,ledger,translated=True)
    out = reconstruct_binary(coefficients,m)
    if stats is not None:
        stats.update(ledger,final_coefficients=coefficients)
    return out
