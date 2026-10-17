"""Fresh exact full DFT with a verified sparse Galois-defect fast path.

This finite-field prototype takes a caller-certified prime and primitive Nth
root. It verifies the root's order, prepares its powers, scans every input,
and counts discovery, all arithmetic, and all explicit outputs. The theorem
also holds over C. No primality proof or root-construction oracle is hidden
in the counters: those two supplied-field hypotheses are explicit.
"""
from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class Field:
    n: int
    p: int
    powers: tuple
    root_stride: int = 1


def power(a, exponent, p, counts):
    result = 1
    while exponent:
        counts['root_verification_index_steps'] += 1
        if exponent & 1:
            result = result * a % p
            counts['mul'] += 1
        exponent >>= 1
        if exponent:
            a = a * a % p
            counts['mul'] += 1
    return result


def prepare(n, p, root, counts):
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n & (n-1):
        raise ValueError('length must be a positive power of two')
    if isinstance(p, bool) or not isinstance(p, int) or p < 3 or not p & 1:
        raise ValueError('caller must supply an odd prime')
    if isinstance(root, bool) or not isinstance(root, int) or not 0 < root < p:
        raise ValueError('root must be a nonzero canonical residue')
    if power(root, n, p, counts) != 1 or (n > 1 and power(root, n//2, p, counts) == 1):
        raise ValueError('supplied root does not have the requested order')
    powers = [1]
    for _ in range(1, n):
        powers.append(powers[-1] * root % p)
        counts['mul'] += 1
        counts['root_table_reads'] += 1
    counts['root_table_writes'] += n
    return Field(n, p, tuple(powers))


def validate(values, n, p, counts):
    if len(values) != n:
        raise ValueError('length does not match the field context')
    for value in values:
        counts['input_reads'] += 1
        if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value < p:
            raise ValueError('input coefficients must be canonical residues')


def signed_action(values, p, counts):
    """P_5: coefficient action of z -> z^5 modulo z^(q/2)+1."""
    m = len(values)
    q = 2*m
    out = [0]*m
    for j, value in enumerate(values):
        exponent = (5*j) & (q-1)
        if exponent >= m:
            value = -value % p
            counts['neg'] += 1
        out[exponent & (m-1)] = value
        counts['action_reads'] += 1
        counts['action_writes'] += 1
        counts['action_index_steps'] += 1
    return out


def discover(values, field, max_defect, counts):
    if isinstance(max_defect, bool) or not isinstance(max_defect, int) or max_defect < 0:
        raise ValueError('max_defect must be a nonnegative integer')
    state = list(values)
    counts['input_copy_reads'] += len(state)
    counts['input_copy_writes'] += len(state)
    levels = []
    while len(state) > 1:
        q, m = len(state), len(state)//2
        reduced, sums = [], []
        for j in range(m):
            reduced.append((state[j]-state[j+m]) % field.p)
            sums.append((state[j]+state[j+m]) % field.p)
            counts['sub'] += 1
            counts['add'] += 1
            counts['pair_reads'] += 2
            counts['pair_writes'] += 2
        support = []
        if q >= 4:
            acted = signed_action(reduced, field.p, counts)
            for j, (a, b) in enumerate(zip(acted, reduced)):
                difference = (a-b) % field.p
                counts['sub'] += 1
                counts['defect_reads'] += 2
                counts['zero_tests'] += 1
                if difference:
                    support.append((j, difference))
                    counts['support_records_written'] += 1
            if len(support) > max_defect:
                return None
        levels.append((q, tuple(reduced), tuple(support)))
        counts['retained_reduced_values'] += m
        state = sums
    return tuple(levels), state[0]


def emit_orbit(q, reduced, support, field, counts, out):
    m, stride = q//2, field.n//q
    # The odd units have two P_5 orbits, represented by 1 and 3.
    defects = [0]*m
    for k in range(1, q, 2):
        value = 0
        for j, coefficient in support:
            value = (value + coefficient*field.powers[((j*k) & (q-1))*stride]) % field.p
            counts['mul'] += 1
            counts['add'] += 1
            counts['root_table_reads'] += 1
            counts['sparse_terms'] += 1
        defects[k//2] = value
        counts['defect_value_writes'] += 1
    for representative in (1, 3):
        value = 0
        for j, coefficient in enumerate(reduced):
            value = (value + coefficient*field.powers[((j*representative) & (q-1))*stride]) % field.p
            counts['mul'] += 1
            counts['add'] += 1
            counts['root_table_reads'] += 1
            counts['anchor_terms'] += 1
        k = representative
        out[k*stride] = value
        counts['output_writes'] += 1
        for _ in range(q//4-1):
            value = (value+defects[k//2]) % field.p
            counts['add'] += 1
            counts['orbit_edges'] += 1
            k = (5*k) & (q-1)
            out[k*stride] = value
            counts['output_writes'] += 1


def evaluate(levels, dc, field, counts):
    out = [None]*field.n
    out[0] = dc
    counts['output_writes'] += 1
    for q, reduced, support in levels:
        m, stride = q//2, field.n//q
        if q == 2:
            out[stride] = reduced[0]
            counts['output_writes'] += 1
            continue
        emit_orbit(q, reduced, support, field, counts, out)
    assert all(value is not None for value in out)
    counts['output_coverage_reads'] += field.n
    return out


def radix_two(values, field, counts, count_outputs=True):
    n, p = field.n, field.p
    out = list(values)
    counts['fft_copy_reads'] += n
    counts['fft_copy_writes'] += n
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
            counts['permutation_index_steps'] += 1
        j ^= bit
        counts['permutation_index_steps'] += 1
        if i < j:
            out[i], out[j] = out[j], out[i]
            counts['permutation_reads'] += 2
            counts['permutation_writes'] += 2
    width = 2
    while width <= n:
        half, stride = width//2, n//width
        for start in range(0, n, width):
            for j in range(half):
                a = out[start+j]
                b = out[start+j+half]*field.powers[j*stride*field.root_stride] % p
                out[start+j] = (a+b) % p
                out[start+j+half] = (a-b) % p
                counts['mul'] += 1
                counts['add'] += 1
                counts['sub'] += 1
                counts['butterflies'] += 1
                counts['root_table_reads'] += 1
                counts['fft_reads'] += 2
                counts['fft_writes'] += 2
        width <<= 1
    if count_outputs:
        counts['output_writes'] += n
    return out


def transform(values, p, root, max_defect=2, use_fast_path=True):
    counts = Counter()
    field = prepare(len(values), p, root, counts)
    validate(values, field.n, p, counts)
    preparation = dict(counts)
    plan = discover(values, field, max_defect, counts) if use_fast_path else None
    discovery = dict(counts)
    if plan is None:
        result = radix_two(values, field, counts)
        accepted, supports = False, []
    else:
        levels, dc = plan
        result = evaluate(levels, dc, field, counts)
        accepted = True
        supports = [{'q': q, 'support': len(support)} for q, _, support in levels]
    return {'values': result, 'accepted': accepted, 'supports': supports,
            'counts': dict(counts), 'preparation_counts': preparation,
            'after_discovery_counts': discovery,
            'field_operations': sum(counts[key] for key in ('add', 'sub', 'mul', 'neg'))}


def hybrid_transform(values, p, root):
    """Choose the cheaper emitted evaluator at every dyadic conductor.

    Discovery is always fully charged and is O(N). The comparison uses exact
    emitted field-operation counts, not claimed runtime or bit-cost optimality.
    The dense alternative uses the same original-root table through a strided
    view; no extra twiddle preparation is assumed free.
    """
    counts = Counter()
    field = prepare(len(values), p, root, counts)
    validate(values, field.n, p, counts)
    preparation = dict(counts)
    levels, dc = discover(values, field, field.n, counts)
    discovery = dict(counts)
    out = [None]*field.n
    out[0] = dc
    counts['output_writes'] += 1
    choices = []
    for q, reduced, support in levels:
        m, stride = q//2, field.n//q
        if q == 2:
            out[stride] = reduced[0]
            counts['output_writes'] += 1
            continue
        orbit_cost = 5*m+2*m*len(support)-2
        fft_cost = m+3*(m//2)*(m.bit_length()-1)
        counts['planner_cost_comparisons'] += 1
        before = sum(counts[key] for key in ('add', 'sub', 'mul', 'neg'))
        if orbit_cost <= fft_cost:
            emit_orbit(q, reduced, support, field, counts, out)
            method, expected = 'orbit', orbit_cost
        else:
            modulated = []
            for j, coefficient in enumerate(reduced):
                modulated.append(coefficient*field.powers[j*stride] % p)
                counts['mul'] += 1
                counts['root_table_reads'] += 1
                counts['modulation_reads'] += 1
                counts['modulation_writes'] += 1
            local = Field(m, p, field.powers, 2*stride)
            odd_values = radix_two(modulated, local, counts, count_outputs=False)
            for k, value in enumerate(odd_values):
                out[(2*k+1)*stride] = value
                counts['output_writes'] += 1
                counts['scatter_reads'] += 1
            method, expected = 'modulated_fft', fft_cost
        after = sum(counts[key] for key in ('add', 'sub', 'mul', 'neg'))
        assert after-before == expected
        choices.append({'q':q, 'support':len(support), 'method':method,
                        'orbit_field_operations':orbit_cost,
                        'modulated_fft_field_operations':fft_cost})
    assert all(value is not None for value in out)
    counts['output_coverage_reads'] += field.n
    return {'values':out, 'choices':choices, 'counts':dict(counts),
            'preparation_counts':preparation, 'after_discovery_counts':discovery,
            'field_operations':sum(counts[key] for key in ('add', 'sub', 'mul', 'neg'))}
