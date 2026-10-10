from __future__ import annotations

from collections import deque
from finite_field import (
    flatten,
    mat_identity,
    mat_mul,
    matrix_inverse,
    solve_linear_columns,
)


def directed_support(a: list[list[int]]) -> list[list[int]]:
    """Arc j->i when A[i,j] is nonzero."""
    n = len(a)
    out = [[] for _ in range(n)]
    for j in range(n):
        for i in range(n):
            if a[i][j] != 0:
                out[j].append(i)
    return out


def directed_distances(a: list[list[int]], source: int) -> list[int]:
    graph = directed_support(a)
    n = len(a)
    inf = 10**9
    dist = [inf] * n
    dist[source] = 0
    q: deque[int] = deque([source])
    while q:
        v = q.popleft()
        for w in graph[v]:
            if dist[w] == inf:
                dist[w] = dist[v] + 1
                q.append(w)
    return dist


def directed_diameter(a: list[list[int]]) -> int:
    result = 0
    for source in range(len(a)):
        d = directed_distances(a, source)
        if max(d) >= 10**9:
            raise ValueError("support graph is not strongly connected")
        result = max(result, max(d))
    return result


def max_outdegree(a: list[list[int]]) -> int:
    return max(len(v) for v in directed_support(a))


def reachable_bound(delta: int, steps: int) -> int:
    if delta <= 1:
        return steps + 1
    return (delta ** (steps + 1) - 1) // (delta - 1)


def krylov_degree_lower_bound_from_size(n: int, delta: int) -> int:
    d = 0
    while reachable_bound(delta, d) < n:
        d += 1
    return d


def support_radius_gate(a: list[list[int]], inverse: list[list[int]] | None = None) -> dict:
    """Exact theorem diagnostic for dense inverse and graph-distance propagation."""
    inv_a = inverse if inverse is not None else None
    if inv_a is None:
        raise ValueError("pass an exact inverse from the field helper")
    dense = all(v != 0 for row in inv_a for v in row)
    diameter = directed_diameter(a)
    delta = max_outdegree(a)
    return {
        "dense_inverse": dense,
        "directed_diameter": diameter,
        "max_outdegree": delta,
        "size_lower_bound": krylov_degree_lower_bound_from_size(len(a), delta),
    }


def minimal_inverse_polynomial_degree(a: list[list[int]], p: int) -> int | None:
    """Least d with A^-1 in span(I,A,...,A^d), for small exact tests."""
    n = len(a)
    target = flatten(matrix_inverse(a, p))
    power = mat_identity(n)
    columns: list[list[int]] = []
    for d in range(n * n):
        columns.append(flatten(power))
        if solve_linear_columns(columns, target, p) is not None:
            return d
        power = mat_mul(power, a, p)
    return None


def cycle_denominator(n: int, p: int, alpha: int) -> list[list[int]]:
    a = mat_identity(n)
    for j in range(n):
        a[(j + 1) % n][j] = (a[(j + 1) % n][j] - alpha) % p
    return a


def multishift_denominator(n: int, p: int, shifts: list[int], weights: list[int]) -> list[list[int]]:
    if len(shifts) != len(weights):
        raise ValueError("length mismatch")
    a = mat_identity(n)
    for shift, weight in zip(shifts, weights):
        for j in range(n):
            i = (j + shift) % n
            a[i][j] = (a[i][j] - weight) % p
    return a
