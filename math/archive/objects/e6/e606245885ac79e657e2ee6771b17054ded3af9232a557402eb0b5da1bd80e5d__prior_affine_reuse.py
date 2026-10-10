"""Exact reversible q-Weyl affine updates and transparent batched reuse.

Finite-field implementation. All online operations are emitted elementary gates.
Reference ADD_T is explicitly quadratic; no fast T primitive is assumed here.
"""
from collections import Counter


def prepare(n, p=998244353, primitive=3):
    if n < 2 or n & (n - 1) or (p - 1) % n:
        raise ValueError('need a power-of-two N >= 2 dividing p-1')
    q = pow(primitive, (p - 1) // n, p)
    if pow(q, n // 2, p) != p - 1:
        raise ValueError('root has wrong order')
    powers = [1]
    for _ in range(n - 1):
        powers.append(powers[-1] * q % p)
    diagonal = [(1 + powers[-j % n]) % p for j in range(n)]
    weights = [(q - powers[-j % n]) % p for j in range(n - 1)]
    weights.append(-q * pow(n, -1, p) % p)
    assert diagonal[n // 2] == 0 and all(weights)
    f, kernel = 1, [1]
    for j in range(1, n):
        f = f * (1 - powers[j]) % p
        kernel.append(pow(f, -1, p))
    m, word = n // 2, []
    for offset in range(n - 1):
        j = (m - 1 - offset) % n
        ratio = diagonal[j] * pow(weights[j], -1, p) % p
        word.append(('shear', (j + 1) % n, j, ratio))
    for j in range(n - 1):
        word.append(('swap', j, j + 1))
    for j, value in enumerate(weights):
        word.append(('scale', j, value))
    return {'n': n, 'p': p, 'q': q, 'diagonal': diagonal,
            'weights': weights, 'kernel': kernel, 'word': word}


def inverse(word, p):
    out = []
    for gate in reversed(word):
        if gate[0] == 'shear':
            _, i, j, a = gate
            out.append(('shear', i, j, -a % p))
        elif gate[0] == 'scale':
            _, i, a = gate
            out.append(('scale', i, pow(a, -1, p)))
        else:
            out.append(gate)
    return out


def offset(word, start):
    out = []
    for gate in word:
        if gate[0] == 'shear':
            _, i, j, a = gate
            out.append(('shear', i + start, j + start, a))
        elif gate[0] == 'scale':
            _, i, a = gate
            out.append(('scale', i + start, a))
        else:
            _, i, j = gate
            out.append(('swap', i + start, j + start))
    return out


def execute(word, registers, p):
    registers = list(registers)
    for gate in word:
        if gate[0] == 'shear':
            _, i, j, a = gate
            registers[i] = (registers[i] + a * registers[j]) % p
        elif gate[0] == 'scale':
            _, i, a = gate
            registers[i] = a * registers[i] % p
        else:
            _, i, j = gate
            registers[i], registers[j] = registers[j], registers[i]
    return registers


def add_t_word(plan, source, target, sign=1):
    n, p = plan['n'], plan['p']
    return [('shear', target + i, source + j,
             sign * plan['kernel'][i - j] % p)
            for i in range(n) for j in range(i + 1)]


def batched_word(plan, batches):
    """Banks: x, dirty w, then arbitrary targets y_0,...,y_(R-1).

    Net: y_r += T(I+B)^r x, x and w unchanged. Two ADD_T calls.
    """
    if batches < 1:
        raise ValueError('positive batch count required')
    n, p = plan['n'], plan['p']
    jword = offset(plan['word'], n)
    jiword = inverse(jword, p)
    word = []
    def trajectory(sign):
        for r in range(batches):
            word.extend(('shear', (2 + r) * n + i, n + i, sign % p)
                        for i in range(n))
            if r + 1 < batches:
                word.extend(jword)
        for _ in range(batches - 1):
            word.extend(jiword)
    trajectory(-1)
    word.extend(add_t_word(plan, 0, n, 1))
    trajectory(1)
    word.extend(add_t_word(plan, 0, n, -1))
    return word


def independent_word(plan, batches):
    """Comparison: replay ADD_T independently for each related source."""
    n, p = plan['n'], plan['p']
    kword = [('shear', j, j+1, plan['weights'][j]) for j in range(n-1)]
    kiword = inverse(kword, p)
    word = []
    for r in range(batches):
        word.extend(add_t_word(plan, 0, (2+r)*n))
        if r+1 < batches:
            word.extend(kword)
    for _ in range(batches-1):
        word.extend(kiword)
    return word


def serpentine_word(plan, batches):
    """Two affine walks, carrying the source to the far end and restoring it.

    Same net map as batched_word with only 2(R-1) J/J^-1 calls, plus
    2(R-1) cheaper K/K^-1 calls. Both x and arbitrary dirty w are restored.
    """
    if batches < 1:
        raise ValueError('positive batch count required')
    n, p = plan['n'], plan['p']
    jword = offset(plan['word'], n)
    jiword = inverse(jword, p)
    kword = [('shear', j, j+1, plan['weights'][j]) for j in range(n-1)]
    kiword = inverse(kword, p)
    word = []
    for r in range(batches):
        word.extend(('shear', (2+r)*n+i, n+i, p-1) for i in range(n))
        if r+1 < batches:
            word.extend(jword)
            word.extend(kword)
    word.extend(add_t_word(plan, 0, n, 1))
    for r in reversed(range(batches)):
        word.extend(('shear', (2+r)*n+i, n+i, 1) for i in range(n))
        if r > 0:
            word.extend(jiword)
            word.extend(kiword)
    word.extend(add_t_word(plan, 0, n, -1))
    return word


def anchor_word(plan, batches):
    """One ADD_T; use the first arbitrary target as the evolving anchor.

    The legacy dirty w bank is untouched and can be omitted entirely.
    Banks follow the same audit layout x,w,y_0,...,y_(R-1).
    """
    if batches < 1:
        raise ValueError('positive batch count required')
    n, p = plan['n'], plan['p']
    jword = offset(plan['word'], 2*n)
    jiword = inverse(jword, p)
    kword = [('shear', j, j+1, plan['weights'][j]) for j in range(n-1)]
    kiword = inverse(kword, p)
    word = []
    for r in range(1, batches):
        word.extend(jword)
        word.extend(kword)
        word.extend(('shear', (2+r)*n+i, 2*n+i, p-1) for i in range(n))
    word.extend(add_t_word(plan, 0, 2*n, 1))
    for r in reversed(range(1, batches)):
        word.extend(('shear', (2+r)*n+i, 2*n+i, 1) for i in range(n))
        word.extend(jiword)
        word.extend(kiword)
    return word


def expand_scalar(word, p):
    """Reversible source scales and register additions, no destructive moves.

    All emitted coefficients are nonzero; inverses are cached preparation.
    """
    out, reciprocal = [], {}
    for gate in word:
        if gate[0] == 'shear':
            _, i, j, a = gate
            if a == 0:
                continue
            if a not in reciprocal:
                reciprocal[a] = pow(a, -1, p)
            out.extend([('scale', j, a), ('add', i, j),
                        ('scale', j, reciprocal[a])])
        elif gate[0] == 'scale':
            out.append(gate)
        else:
            _, i, j = gate
            out.extend([('add', i, j), ('sub', j, i),
                        ('add', i, j), ('scale', j, p-1)])
    return out


def execute_scalar(word, registers, p):
    registers = list(registers)
    for gate in word:
        kind, i, j = gate
        if kind == 'scale':
            registers[i] = registers[i] * j % p
        elif kind == 'add':
            registers[i] = (registers[i] + registers[j]) % p
        else:
            registers[i] = (registers[i] - registers[j]) % p
    return registers


def charge(word):
    counts = Counter(gate[0] for gate in word)
    # Each shear is charged one multiplication and one addition even for ±1.
    # The reversible scalar expansion uses 3 instructions per shear, one per
    # scale, and 4 per swap. Every instruction has O(1) register addressing.
    return {'shears': counts['shear'], 'scalings': counts['scale'],
            'swaps': counts['swap'],
            'field_multiplications': counts['shear'] + counts['scale'],
            'field_additions': counts['shear'],
            'expanded_scalar_multiplications': 2*counts['shear'] + counts['scale'] + counts['swap'],
            'expanded_scalar_additions': counts['shear'] + 3*counts['swap'],
            'expanded_scalar_instructions': 3*counts['shear'] + counts['scale'] + 4*counts['swap'],
            'gate_count': len(word)}


def apply_t(plan, x):
    n, p = plan['n'], plan['p']
    return [sum(plan['kernel'][i-j] * x[j] for j in range(i+1)) % p
            for i in range(n)]


def apply_k(plan, x):
    n, p = plan['n'], plan['p']
    return [(x[j] + plan['weights'][j] * x[j+1]) % p
            for j in range(n-1)] + [x[-1]]


def apply_j(plan, x):
    n, p = plan['n'], plan['p']
    return [(plan['diagonal'][j] * x[j] +
             plan['weights'][j] * x[(j+1) % n]) % p for j in range(n)]
