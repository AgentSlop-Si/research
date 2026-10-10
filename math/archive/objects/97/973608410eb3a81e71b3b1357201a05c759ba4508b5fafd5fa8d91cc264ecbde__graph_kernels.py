"""Exact cold/warm same-B integer products via a verified correction graph.

Arithmetic counters use a declared word/field-operation model, not CPU time.
NTT modulus 65537 permits exact digit convolution when n*(base-1)^2 < p.
All roots, B's transform, graph discovery, and full product digits are charged.
"""
from collections import Counter
from dataclasses import dataclass


class Counts(Counter):
    def arithmetic(self):
        return sum(self[k] for k in ('mod_mul','mod_add','mod_sub',
                                     'int_mul','int_add','int_sub','int_neg','divmod'))


def power(a, e, p, c):
    out = 1
    while e:
        c['root_exponent_steps'] += 1
        if e & 1:
            out = out*a % p
            c['mod_mul'] += 1
        e >>= 1
        if e:
            a = a*a % p
            c['mod_mul'] += 1
    return out


@dataclass
class Context:
    n: int
    base: int
    m: int
    p: int
    roots: list
    permutation: list
    inverse_m: int
    b: list
    fb: list


def fft(x, ctx, c, inverse=False):
    m, p = ctx.m, ctx.p
    out = [x[j] for j in ctx.permutation]
    c['fft_permutation_reads'] += m
    c['fft_permutation_writes'] += m
    width = 2
    while width <= m:
        half, stride = width//2, m//width
        for start in range(0, m, width):
            for j in range(half):
                exponent = j*stride
                if inverse:
                    exponent = (-exponent) % m
                u = out[start+j]
                v = out[start+j+half]*ctx.roots[exponent] % p
                out[start+j] = (u+v) % p
                out[start+j+half] = (u-v) % p
                c['mod_mul'] += 1
                c['mod_add'] += 1
                c['mod_sub'] += 1
                c['butterfly_register_reads'] += 2
                c['butterfly_register_writes'] += 2
                c['root_table_reads'] += 1
                c['butterflies'] += 1
        width *= 2
    if inverse:
        out = [a*ctx.inverse_m % p for a in out]
        c['mod_mul'] += m
        c['inverse_scale_reads'] += m
        c['inverse_scale_writes'] += m
    return out


def prepare(b, base, c):
    n, p = len(b), 65537
    m = 1 << (2*n-1).bit_length()
    if n < 1 or n*(base-1)**2 >= p or (p-1) % m:
        raise ValueError('digit bound or supported NTT length violated')
    root = power(3, (p-1)//m, p, c)
    assert power(root, m, p, c) == 1
    assert power(root, m//2, p, c) != 1
    roots = [1]
    for _ in range(1, m):
        roots.append(roots[-1]*root % p)
        c['mod_mul'] += 1
        c['root_table_writes'] += 1
    perm = [0]*m
    for i in range(1, m):
        perm[i] = (perm[i>>1]>>1) | ((i & 1)*(m>>1))
        c['permutation_index_steps'] += 1
    inverse_m = power(m, p-2, p, c)
    ctx = Context(n, base, m, p, roots, perm, inverse_m, list(b), [])
    padded = list(b)+[0]*(m-n)
    c['padding_writes'] += m
    ctx.fb = fft(padded, ctx, c)
    return ctx


def fresh(a, ctx, c):
    padded = list(a)+[0]*(ctx.m-ctx.n)
    c['padding_writes'] += ctx.m
    fa = fft(padded, ctx, c)
    prod = [a*b % ctx.p for a,b in zip(fa, ctx.fb)]
    c['mod_mul'] += ctx.m
    c['pointwise_reads'] += 2*ctx.m
    c['pointwise_writes'] += ctx.m
    c['fresh_products'] += 1
    return fft(prod, ctx, c, inverse=True)[:2*ctx.n-1]


def update(parent_product, patch, ctx, c):
    if not patch:
        c['identical_product_copy_reads'] += len(parent_product)
        c['identical_product_copy_writes'] += len(parent_product)
        c['correction_products'] += 1
        return list(parent_product)
    delta = [0]*len(parent_product)
    c['correction_zero_writes'] += len(delta)
    for j, difference in patch:
        for k, value in enumerate(ctx.b):
            delta[j+k] += difference*value
            c['int_mul'] += 1
            c['int_add'] += 1
            c['correction_updates'] += 1
    out = [v+d for v,d in zip(parent_product, delta)]
    c['int_add'] += len(out)
    c['correction_merge_reads'] += 2*len(out)
    c['correction_merge_writes'] += len(out)
    c['correction_products'] += 1
    return out


def normalize(coefficients, n, base, c):
    carry, digits = 0, []
    for j in range(2*n):
        value = (coefficients[j] if j < len(coefficients) else 0)+carry
        carry, digit = divmod(value, base)
        c['int_add'] += 1
        c['divmod'] += 1
        c['full_output_digit_writes'] += 1
        digits.append(digit)
    assert carry == 0
    return digits


def fresh_weight(n, m):
    # Two transforms (three scalar ops per butterfly), inverse scaling,
    # and pointwise multiplication. B's FFT is charged in shared preparation.
    return 3*m*(m.bit_length()-1)+2*m


def validate(queries, b, base, c):
    n = len(b)
    if not isinstance(base,int) or isinstance(base,bool) or base < 2:
        raise ValueError('base must be an integer at least two')
    if not queries:
        raise ValueError('at least one query required')
    for vector in [b]+list(queries):
        if len(vector) != n:
            raise ValueError('all block vectors must have the same length')
        for value in vector:
            c['input_digit_reads'] += 1
            c['validation_comparisons'] += 2
            if not isinstance(value, int) or not 0 <= value < base:
                raise ValueError('inputs must be canonical nonnegative digits')


def numeric_difference(a, b, base, c):
    """Canonical signed blocks of B-A, using only bounded block operations."""
    sign=0
    for j in range(len(a)-1,-1,-1):
        c['numeric_difference_order_comparisons'] += 1
        c['numeric_difference_digit_reads'] += 2
        if a[j] != b[j]:
            sign=1 if b[j]>a[j] else -1
            break
    if not sign:
        return []
    larger,smaller=(b,a) if sign>0 else (a,b)
    borrow=0
    patch=[]
    for j,(large,small) in enumerate(zip(larger,smaller)):
        c['numeric_difference_digit_reads'] += 2
        value=large-small-borrow
        c['int_sub'] += 2
        c['numeric_difference_borrow_tests'] += 1
        if value < 0:
            value += base
            c['int_add'] += 1
            borrow=1
        else:
            borrow=0
        if value:
            if sign<0:
                value=-value
                c['int_neg'] += 1
            patch.append((j,value))
    assert borrow==0
    return patch


def discover(queries, ctx, c, numeric_patches=False, candidate_edges=None):
    patches = {}
    if candidate_edges is None:
        pairs=[(i,j) for i in range(len(queries)) for j in range(i+1,len(queries))]
    else:
        pairs=[]
        seen=set()
        for edge in candidate_edges:
            c['candidate_edge_records_read'] += 1
            if len(edge)!=2 or not all(isinstance(v,int) and not isinstance(v,bool)
                    and 0<=v<len(queries) for v in edge) or edge[0]==edge[1]:
                raise ValueError('invalid candidate edge')
            edge=tuple(sorted(edge))
            if edge not in seen:
                seen.add(edge); pairs.append(edge)
    for i,j in pairs:
            patch = []
            for k, (a,b) in enumerate(zip(queries[i],queries[j])):
                delta = b-a
                c['int_sub'] += 1
                c['discovery_digit_reads'] += 2
                c['discovery_zero_tests'] += 1
                if delta:
                    patch.append((k,delta))
                    c['stored_patch_records'] += 1
            if numeric_patches:
                alternative=numeric_difference(queries[i],queries[j],ctx.base,c)
                c['numeric_patch_records_created'] += len(alternative)
                c['patch_representation_comparisons'] += 1
                if len(alternative)<len(patch):
                    patch=alternative
                    c['numeric_patches_selected'] += 1
                else:
                    c['coordinate_patches_selected'] += 1
            patches[i,j] = patch
            patches[j,i] = [(k,-v) for k,v in patch]
            c['int_neg'] += len(patch)
            c['stored_patch_records'] += len(patch)
    return patches


def plan_mst(queries, patches, ctx, c, warm_index=None, merge_length=None):
    q = len(queries)
    weights = [fresh_weight(ctx.n,ctx.m)]*q
    parent = [-1]*q
    if warm_index is not None:
        weights[warm_index] = 0
    done, order = set(), []
    for _ in range(q):
        best = None
        for j in range(q):
            c['scheduler_membership_tests'] += 1
            if j not in done:
                c['scheduler_weight_comparisons'] += 1
                if best is None or (weights[j],j) < (weights[best],best):
                    best = j
        done.add(best)
        order.append((best,parent[best],weights[best]))
        for j in range(q):
            c['scheduler_membership_tests'] += 1
            if j in done:
                continue
            if (best,j) not in patches:
                continue
            patch = patches[best,j]
            merge=2*ctx.n-1 if merge_length is None else merge_length
            weight = 2*ctx.n*len(patch)+merge if patch else 0
            c['scheduler_edge_cost_evaluations'] += 1
            c['scheduler_weight_comparisons'] += 1
            if weight < weights[j]:
                weights[j], parent[j] = weight,best
    return order


def run(queries, b, base=16, graph=True, warm_index=None, warm_state=None,
        numeric_patches=False, candidate_edges=None):
    c = Counts()
    validate(queries,b,base,c)
    if warm_index is not None and (not isinstance(warm_index,int)
            or isinstance(warm_index,bool) or not 0 <= warm_index < len(queries)):
        raise ValueError('warm index must name an existing query')
    if warm_state is None:
        ctx = prepare(b,base,c)
        cached = {}
    else:
        ctx, index, anchor_digits, coefficients = warm_state
        if (not isinstance(index,int) or isinstance(index,bool)
                or not 0 <= index < len(queries)):
            raise ValueError('cached index must name an existing query')
        c['warm_cache_key_comparisons'] += 2*len(b)+3
        if (ctx.b != list(b) or ctx.base != base or warm_index != index
                or queries[index] != anchor_digits):
            raise ValueError('warm state does not match B/base/anchor value/index')
        expected_length=2*ctx.n if numeric_patches else 2*ctx.n-1
        if len(coefficients)!=expected_length:
            raise ValueError('warm product representation mode mismatch')
        cached = {index:list(coefficients)}
        c['warm_coefficient_reads'] += len(coefficients)
    if warm_index is not None and warm_index not in cached:
        raise ValueError('warm anchor must be supplied explicitly')
    prep_arithmetic = c.arithmetic()
    if graph:
        patches = discover(queries,ctx,c,numeric_patches,candidate_edges)
        order = plan_mst(queries,patches,ctx,c,warm_index,
                         2*ctx.n if numeric_patches else None)
    else:
        patches = {}
        order = [(i,-1,0 if i in cached else fresh_weight(ctx.n,ctx.m))
                 for i in range(len(queries))]
    plan_arithmetic = c.arithmetic()-prep_arithmetic
    outputs = [None]*len(queries)
    for i,parent,weight in order:
        before = c.arithmetic()
        if parent == -1:
            if i not in cached:
                cached[i] = fresh(queries[i],ctx,c)
        else:
            patch = patches[parent,i]
            cached[i] = update(cached[parent],patch,ctx,c)
        assert c.arithmetic()-before == weight
        outputs[i] = normalize(cached[i],ctx.n,base,c)
        if numeric_patches:
            cached[i]=outputs[i]
    return {'outputs':outputs,'coefficients':cached,'context':ctx,
        'counts':dict(c),'total_arithmetic':c.arithmetic(),
        'preparation_arithmetic':prep_arithmetic,'discovery_arithmetic':plan_arithmetic,
        'schedule':order,'product_arithmetic':sum(x[2] for x in order),
        'correction_supports':[len(v) for v in patches.values()]}


def as_integer(digits, base):
    """Verification only; not called by the counted algorithm."""
    value = 0
    for digit in reversed(digits):
        value = value*base+digit
    return value
