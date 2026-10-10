"""Exact verified resolvent edges for the sparse grading H R = D H.

One paid H anchor is required. This is a related-query method, not a faster
fresh transform. Cyclic band solves use standard low-rank boundary closure.
"""
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT/'fft_sparse_grading_research'))
from grading import prepare_grading
from fixed_kernel import Counted


@dataclass
class BandPlan:
    n: int
    diagonal: object
    inverse_diagonal: object
    bands: list
    responses: list
    inverse_closure: list
    preparation: dict


def triangular_solve(field, inverse_diagonal, bands, rhs):
    n = len(rhs)
    out = [field.zero]*n
    for i in range(n-1, -1, -1):
        acc = rhs[i]
        for k, band in enumerate(bands, 1):
            if i+k < n:
                acc = field.sub(acc, field.mul(band[i], out[i+k]))
        out[i] = field.mul(inverse_diagonal, acc)
    return out


def prepare_band(field, diagonal, bands):
    """Prepare (diagonal I + sum band[k][i] shift^(k+1))^-1.

    Width is 1 or 2 and N>=4. Scalar diagonal must be nonzero; singular full
    cyclic matrices are rejected by their small closure determinant.
    """
    if len(bands) not in (1, 2) or len(bands[0]) < 4:
        raise ValueError('width 1 or 2 and N>=4 required')
    n = len(bands[0])
    if any(len(b) != n for b in bands) or diagonal == field.zero:
        raise ValueError('equal band lengths and nonzero diagonal required')
    c = Counted(field)
    inverse_diagonal = c.inv(diagonal)
    width = len(bands)
    columns = [[field.zero]*n for _ in range(width)]
    for k, band in enumerate(bands, 1):
        for i in range(n-k, n):
            j = i+k-n
            columns[j][i] = c.add(columns[j][i], band[i])
    responses = [triangular_solve(c, inverse_diagonal, bands, v) for v in columns]
    closure = [[c.add(field.one if i == j else field.zero, responses[j][i])
                for j in range(width)] for i in range(width)]
    if width == 1:
        if closure[0][0] == field.zero:
            raise ValueError('singular cyclic closure')
        inverse = [[c.inv(closure[0][0])]]
    else:
        a, b = closure[0]
        d, e = closure[1]
        determinant = c.sub(c.mul(a, e), c.mul(b, d))
        if determinant == field.zero:
            raise ValueError('singular cyclic closure')
        scale = c.inv(determinant)
        inverse = [[c.mul(e, scale), c.neg(c.mul(b, scale))],
                   [c.neg(c.mul(d, scale)), c.mul(a, scale)]]
    return BandPlan(n, diagonal, inverse_diagonal, [list(b) for b in bands],
                    responses, inverse, dict(c.count))


def apply_band(field, plan, values):
    if len(values) != plan.n:
        raise ValueError('wrong vector length')
    out = []
    for i in range(plan.n):
        value = field.mul(plan.diagonal, values[i])
        for k, band in enumerate(plan.bands, 1):
            value = field.add(value, field.mul(band[i], values[(i+k)%plan.n]))
        out.append(value)
    return out


def solve_band(field, plan, rhs):
    if len(rhs) != plan.n:
        raise ValueError('wrong vector length')
    c = Counted(field)
    z = triangular_solve(c, plan.inverse_diagonal, plan.bands, rhs)
    width = len(plan.bands)
    alpha = []
    for row in plan.inverse_closure:
        acc = c.mul(row[0], z[0])
        for j in range(1, width):
            acc = c.add(acc, c.mul(row[j], z[j]))
        alpha.append(acc)
    out = list(z)
    for response, coefficient in zip(plan.responses, alpha):
        for i in range(plan.n):
            out[i] = c.sub(out[i], c.mul(response[i], coefficient))
    return out, dict(c.count)


@dataclass
class RationalPlan:
    n: int
    q: object
    shift: object
    grading: dict
    source: BandPlan
    target: BandPlan
    preparation: dict


def prepare_rational(field, n, q, shift, grading=None):
    if n < 4 or n & (n-1) or shift == field.zero:
        raise ValueError('dyadic N>=4 and nonzero shift required')
    count = Counter()
    if grading is None:
        grading = prepare_grading(field, n, q)
        count.update(grading['preparation'])
    elif grading['n'] != n or grading['q'] != q:
        raise ValueError('stale grading plan')
    c = Counted(field)
    diagonal = c.neg(shift)
    source = prepare_band(field, diagonal, [grading['r']])
    target = prepare_band(field, diagonal, [grading['d1'], grading['d2']])
    count.update(c.count)
    count.update(source.preparation)
    count.update(target.preparation)
    return RationalPlan(n, q, shift, grading, source, target, dict(count))


def generate_related_pair(field, plan, anchor_input, anchor_output):
    """Both inverses paid; caller's exact anchor_output=H anchor_input is trusted."""
    x, source_count = solve_band(field, plan.source, anchor_input)
    y, target_count = solve_band(field, plan.target, anchor_output)
    count = Counter(source_count)
    count.update(target_count)
    return x, y, dict(field_operations=dict(count), source_solve=source_count,
                      target_solve=target_count, full_vector_outputs=2*plan.n,
                      expensive_transform_calls=0)


def verified_output(field, plan, anchor_input, anchor_output, query_input):
    """Use a supplied shift only after checking its full relation in O(N)."""
    if any(len(x) != plan.n for x in (anchor_input, anchor_output, query_input)):
        raise ValueError('wrong vector length')
    c = Counted(field)
    recovered = apply_band(c, plan.source, query_input)
    if recovered != list(anchor_input):
        raise ValueError('query does not satisfy the proposed rational edge')
    out, solve_count = solve_band(field, plan.target, anchor_output)
    count = Counter(c.count)
    count.update(solve_count)
    return out, dict(field_operations=dict(count), relation_field_operations=dict(c.count),
                     relation_comparisons=plan.n, full_output_writes=plan.n,
                     expensive_transform_calls=0)
