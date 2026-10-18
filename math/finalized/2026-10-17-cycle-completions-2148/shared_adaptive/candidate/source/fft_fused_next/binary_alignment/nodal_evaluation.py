#!/usr/bin/env python3
"""Balanced exact Lagrange evaluation for consecutive integer node values.

Inputs are values at falling x=0,...,r-1 (equivalently rising X=0,-1,...).
The prepared target is falling x=-point, so the output is the rising value
at the positive integer point. All denominator clearing is explicit.
"""
from dataclasses import dataclass


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


@dataclass
class LagrangeCounts:
    setup_products: int = 0
    setup_exact_divisions: int = 0
    setup_subtractions: int = 0
    leaf_products: int = 0
    tree_products: int = 0
    tree_additions: int = 0
    final_exact_divisions: int = 0
    peak_arithmetic_bits: int = 0

    def see(self, *values):
        self.peak_arithmetic_bits = max(self.peak_arithmetic_bits,
                                       *(abs(value).bit_length() for value in values))


@dataclass(frozen=True)
class LagrangeNode:
    start: int
    stop: int
    product: int
    left: object = None
    right: object = None


@dataclass(frozen=True)
class LagrangePlan:
    r: int
    point: int
    target: int
    denominator: int
    weights: tuple
    tree: LagrangeNode


def prepare_lagrange(r, point, counts=None):
    """Prepare the fixed denominator tree once for both output vectors."""
    counts = LagrangeCounts() if counts is None else counts
    require(isinstance(r, int) and r >= 2, 'rank must be an integer >=2')
    require(isinstance(point, int), 'evaluation point must be an integer')
    target = -point
    def product_range(start, stop):
        if stop - start <= 1:
            return start if start < stop else 1
        middle = (start + stop) // 2
        first, second = product_range(start, middle), product_range(middle, stop)
        product = first * second
        counts.setup_products += 1
        counts.see(first, second, product)
        return product

    denominator = product_range(1, r)
    weight = -1 if (r - 1) % 2 else 1
    weights = [weight]
    for j in range(r - 1):
        numerator = -weight * (r - 1 - j)
        weight, remainder = divmod(numerator, j + 1)
        require(remainder == 0, 'nonintegral binomial weight recurrence')
        counts.setup_products += 1
        counts.setup_exact_divisions += 1
        counts.see(numerator, weight)
        weights.append(weight)

    def build(start, stop):
        if stop - start == 1:
            product = target - start
            counts.setup_subtractions += 1
            counts.see(product)
            return LagrangeNode(start, stop, product)
        middle = (start + stop) // 2
        left, right = build(start, middle), build(middle, stop)
        product = left.product * right.product
        counts.setup_products += 1
        counts.see(left.product, right.product, product)
        return LagrangeNode(start, stop, product, left, right)

    return LagrangePlan(r, point, target, denominator, tuple(weights), build(0, r))


def evaluate_lagrange(values, prepared, counts=None):
    """Evaluate degree<r interpolation polynomial; demand an integer result.

    Every nodal vector from the integral compact quotient passes the exact
    final division. Arbitrary integer nodal vectors also interpolate an
    integer-valued polynomial because consecutive-node finite differences
    are integers, so integer target points satisfy the same requirement.
    """
    counts = LagrangeCounts() if counts is None else counts
    require(len(values) == prepared.r, 'wrong nodal vector length')
    require(all(isinstance(value, int) for value in values), 'nodal values must be integers')

    def ascend(node):
        if node.stop - node.start == 1:
            value = prepared.weights[node.start] * values[node.start]
            counts.leaf_products += 1
            counts.see(prepared.weights[node.start], values[node.start], value)
            return value
        low, high = ascend(node.left), ascend(node.right)
        first, second = low * node.right.product, high * node.left.product
        value = first + second
        counts.tree_products += 2
        counts.tree_additions += 1
        counts.see(low, high, first, second, value)
        return value

    numerator = ascend(prepared.tree)
    value, remainder = divmod(numerator, prepared.denominator)
    counts.final_exact_divisions += 1
    counts.see(numerator, prepared.denominator, value)
    require(remainder == 0, 'Lagrange value at integer target was nonintegral')
    return value
