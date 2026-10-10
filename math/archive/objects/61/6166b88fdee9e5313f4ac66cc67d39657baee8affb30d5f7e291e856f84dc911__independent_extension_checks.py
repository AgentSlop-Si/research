"""Fresh finite algebra checks; imports no supplied research/checker code.

Reference arithmetic uses polynomial-basis GF(2^d), then explicitly locates
an Artin--Schreier tower. Python is an algebra checker, not a RAM benchmark.
"""
import itertools
import json
import random
from functools import lru_cache


class Field:
    def __init__(self, degree):
        self.d = degree
        self.q = 1 << degree
        self.modulus = {1: 3, 2: 7, 4: 19, 8: 283}[degree]
        generators = []
        trace_one = 1
        for _ in range(degree.bit_length() - 1):
            root = next(a for a in range(self.q)
                        if self.multiply(a, a) ^ a == trace_one)
            generators.append(root)
            trace_one = self.multiply(trace_one, root)
        self.basis = []
        for i in range(degree):
            product = 1
            for j, root in enumerate(generators):
                if (i >> j) & 1:
                    product = self.multiply(product, root)
            self.basis.append(product)
        self.from_tower = []
        for i in range(self.q):
            value = 0
            for j, element in enumerate(self.basis):
                if (i >> j) & 1:
                    value ^= element
            self.from_tower.append(value)
        assert len(set(self.from_tower)) == self.q
        self.to_tower = {value: i for i, value in enumerate(self.from_tower)}

    def multiply(self, a, b):
        value = 0
        while b:
            if b & 1:
                value ^= a
            a <<= 1
            if a & self.q:
                a ^= self.modulus
            b >>= 1
        return value

    def square(self, a):
        return self.multiply(a, a)

    def subspace_value(self, index, a):
        for _ in range(index):
            a = self.square(a) ^ a
        return a

    def horner(self, coefficients, a):
        value = 0
        for c in reversed(coefficients):
            value = self.multiply(value, a) ^ c
        return value


def binary_product(a, b):
    answer = 0
    while a:
        low = a & -a
        answer ^= b << (low.bit_length() - 1)
        a ^= low
    return answer


@lru_cache(None)
def subspace_polynomial(i):
    # Use (F + identity)^i, exploiting binomial parity, independently of
    # the recursive coefficient-polynomial construction in the source.
    answer = 0
    for j in range(i + 1):
        if j & ~i == 0:
            answer ^= 1 << (1 << j)
    return answer


@lru_cache(None)
def novel_polynomial(index):
    answer = 1
    for i in range(index.bit_length()):
        if (index >> i) & 1:
            answer = binary_product(answer, subspace_polynomial(i))
    return answer


def to_novel_reference(coefficients):
    working = coefficients[:]
    novel = [0] * len(working)
    for j in range(len(working) - 1, -1, -1):
        value = working[j]
        novel[j] = value
        support = novel_polynomial(j)
        while support:
            low = support & -support
            working[low.bit_length() - 1] ^= value
            support ^= low
    assert not any(working)
    return novel


def from_novel_reference(novel):
    coefficients = [0] * len(novel)
    for j, value in enumerate(novel):
        support = novel_polynomial(j)
        while support:
            low = support & -support
            coefficients[low.bit_length() - 1] ^= value
            support ^= low
    return coefficients


def representative_transform(field, novel):
    # Iterative DFS, deliberately independent of the supplied checker.
    stack = [(novel, 0, 0)]
    leaves = []
    units = 0
    while stack:
        vector, state, offset = stack.pop()
        if len(vector) == 1:
            leaves.append((offset, vector[0]))
            continue
        k = len(vector).bit_length() - 1
        half = len(vector) // 2
        multiplier = field.subspace_value(k - 1, offset)
        left = [vector[i] ^ field.multiply(multiplier, vector[i + half])
                for i in range(half)]
        units += half
        if state and state & (state - 1) == 0:
            stack.append((left, state + 1, offset))
        else:
            right = [left[i] ^ vector[i + half] for i in range(half)]
            stack.append((right, state + 1, offset ^ field.basis[k - 1]))
            stack.append((left, 0 if state == 0 else state + 1, offset))
    return leaves, units


def inverse_representative_transform(field, values, m):
    iterator = iter(values)

    def recover(k, state, offset):
        if k == 0:
            return [next(iterator)]
        multiplier = field.subspace_value(k - 1, offset)
        child = recover(k - 1, 0 if state == 0 else state + 1, offset)
        if state and state & (state - 1) == 0:
            mask = (1 << state) - 1
            constant = multiplier ^ field.basis[state]
            low, high = [], []
            for value in child:
                coordinates = field.to_tower[value]
                assert coordinates >> (2 * state) == 0
                a = field.from_tower[coordinates & mask]
                b = field.from_tower[coordinates >> state]
                low.append(a ^ field.multiply(constant, b))
                high.append(b)
        else:
            sibling = recover(k - 1, state + 1, offset ^ field.basis[k - 1])
            high = [a ^ b for a, b in zip(child, sibling)]
            low = [a ^ field.multiply(multiplier, b)
                   for a, b in zip(child, high)]
        return low + high

    result = recover(m, 0, 0)
    assert next(iterator, None) is None
    return result


def binary_evaluation(field, coefficients):
    novel = to_novel_reference(coefficients)
    leaves, units = representative_transform(field, novel)
    evaluation = {}
    for alpha, value in leaves:
        start = alpha
        while True:
            assert alpha not in evaluation
            evaluation[alpha] = value
            alpha, value = field.square(alpha), field.square(value)
            if alpha == start:
                break
    assert len(evaluation) == len(coefficients)
    assert inverse_representative_transform(field, [v for _, v in leaves],
                                            len(coefficients).bit_length() - 1) == novel
    return evaluation, units


def coordinate_evaluation(field, coordinates, multipliers, origin=0):
    n = len(coordinates)
    result = {a: 0 for a in range(field.q)}
    total_units = 0
    # This checker evaluates on the full field; the report uses cyclic order.
    for lane, multiplier in enumerate(multipliers):
        plane = [(x >> lane) & 1 for x in coordinates]
        values, units = binary_evaluation(field, plane)
        total_units += units
        for alpha, value in values.items():
            result[alpha] ^= field.multiply(multiplier, value)
    if origin:
        constant_coefficients = [origin] * n
        for alpha in result:
            result[alpha] ^= field.horner(constant_coefficients, alpha)
    return result, total_units


def adaptive_affine_coordinates(values):
    origin = values[0]
    basis = []
    pivot_order = []
    labels = []
    elimination_steps = 0
    for value in values:
        residual = value ^ origin
        label = 0
        for pivot, index in pivot_order:
            elimination_steps += 1
            if (residual >> pivot) & 1:
                residual ^= basis[index]
                label ^= 1 << index
        if residual:
            index = len(basis)
            basis.append(residual)
            pivot_order.append((residual.bit_length() - 1, index))
            pivot_order.sort(reverse=True)
            label ^= 1 << index
        labels.append(label)
    for original, label in zip(values, labels):
        reconstructed = origin
        for index, vector in enumerate(basis):
            if (label >> index) & 1:
                reconstructed ^= vector
        assert reconstructed == original
    assert elimination_steps <= len(values) * len(basis)
    return origin, basis, labels


def main():
    rng = random.Random(20002026)
    output = {"field_model": "independent polynomial-basis arithmetic and searched tower embeddings"}
    field_counts, transform_count, convolution_count = [], 0, 0
    for d in [1, 2, 4, 8]:
        field = Field(d)
        for i in range(d):
            assert field.subspace_value(i, field.basis[i]) == 1
            for a in field.from_tower[:1 << i]:
                assert field.subspace_value(i, a) == 0
        # Independent field axiom sample and full small inverse checks.
        for a in range(1, field.q):
            assert any(field.multiply(a, b) == 1 for b in range(1, field.q))
        field_counts.append({"d": d, "basis": field.basis})
        for m in range(d + 1):
            n = 1 << m
            samples = list(itertools.product([0, 1], repeat=n)) if n <= 8 else [
                [rng.randrange(2) for _ in range(n)] for _ in range(12)]
            for coefficients in samples:
                coefficients = list(coefficients)
                values, _ = binary_evaluation(field, coefficients)
                domain = field.from_tower[:n]
                assert set(values) == set(domain)
                assert all(values[a] == field.horner(coefficients, a) for a in domain)
                transform_count += 1
            for _ in range(15):
                length_a = rng.randrange(1, n + 1)
                length_b = rng.randrange(1, n - length_a + 2)
                a = [rng.randrange(2) for _ in range(length_a)]
                b = [rng.randrange(2) for _ in range(length_b)]
                aa = a + [0] * (n - len(a))
                bb = b + [0] * (n - len(b))
                left, _ = representative_transform(field, to_novel_reference(aa))
                right, _ = representative_transform(field, to_novel_reference(bb))
                assert [x for x, _ in left] == [x for x, _ in right]
                products = [field.multiply(x[1], y[1]) for x, y in zip(left, right)]
                reconstructed = from_novel_reference(
                    inverse_representative_transform(field, products, m))
                expected = [0] * n
                for i, ai in enumerate(a):
                    for j, bj in enumerate(b):
                        expected[i + j] ^= ai & bj
                assert reconstructed == expected
                convolution_count += 1
    output["fields"] = field_counts
    output["binary_transform_and_inverse_cases"] = transform_count
    output["binary_polynomial_convolution_cases"] = convolution_count

    growing = []
    for d in [2, 4, 8]:
        field = Field(d)
        for width in sorted(set([1, min(2, d), min(3, d), d])):
            multipliers = field.basis[:width]
            cases = 0
            for _ in range(12):
                coordinates = [rng.randrange(1 << width) for _ in range(field.q - 1)] + [0]
                values, units = coordinate_evaluation(field, coordinates, multipliers)
                coefficients = [field.from_tower[v] for v in coordinates]
                assert all(values[a] == field.horner(coefficients, a) for a in range(field.q))
                # Also exercise a non-subfield linear coefficient subspace.
                if d >= 4 and width == 2:
                    irregular = [field.basis[0], field.basis[d - 1]]
                    values2, _ = coordinate_evaluation(field, coordinates, irregular)
                    coefficients2 = [((irregular[0] if x & 1 else 0) ^
                                      (irregular[1] if x & 2 else 0)) for x in coordinates]
                    assert all(values2[a] == field.horner(coefficients2, a)
                               for a in range(field.q))
                cases += 1
            growing.append({"d": d, "coordinate_bits": width,
                            "alphabet_size": 1 << width, "cases": cases,
                            "coefficient_work_units": units})
    output["growing_alphabet_cases"] = growing

    affine_cases = []
    for d in [2, 4, 8]:
        field = Field(d)
        for intended_width in range(d + 1):
            for _ in range(5):
                origin = rng.randrange(field.q)
                independent = field.basis[:]
                rng.shuffle(independent)
                values = []
                for _ in range(field.q - 1):
                    value = origin
                    label = rng.randrange(1 << intended_width)
                    for lane in range(intended_width):
                        if (label >> lane) & 1:
                            value ^= independent[lane]
                    values.append(value)
                beta, basis, labels = adaptive_affine_coordinates(values)
                assert len(basis) <= intended_width
                transformed, _ = coordinate_evaluation(field, labels + [0], basis)
                # The all-one polynomial of length Q-1 evaluates to one at
                # 0 and 1, and zero at every other field point.
                transformed[0] ^= beta
                transformed[1] ^= beta
                coefficients = values + [0]
                assert all(transformed[a] == field.horner(coefficients, a)
                           for a in range(field.q))
            affine_cases.append({"d": d, "intended_affine_dimension": intended_width,
                                 "cases": 5})
    output["adaptive_affine_cases"] = affine_cases

    field = Field(8)
    chunk_width = 2
    chunks = 4
    tables = {}
    for i in range(chunks):
        for j in range(chunks):
            tables[i, j] = [[field.to_tower[field.multiply(
                field.from_tower[a << (chunk_width * i)],
                field.from_tower[b << (chunk_width * j)])]
                for b in range(1 << chunk_width)] for a in range(1 << chunk_width)]
    pairs = 0
    for a in range(field.q):
        for b in range(field.q):
            reconstructed = 0
            for i in range(chunks):
                for j in range(chunks):
                    reconstructed ^= tables[i, j][(a >> (2 * i)) & 3][(b >> (2 * j)) & 3]
            assert field.from_tower[reconstructed] == field.multiply(
                field.from_tower[a], field.from_tower[b])
            pairs += 1
    output["positional_product_pairs"] = pairs
    mu = field.basis[-1]
    assert mu != field.square(mu)
    output["naive_growing_alphabet_frobenius_failure"] = {
        "constant_coefficient_polynomial_basis": mu,
        "f(alpha_squared)": mu, "f(alpha)_squared": field.square(mu)}
    output["integer_convolution_obstruction"] = {
        "input_a": [1, 1], "input_b": [1, 1],
        "integer_convolution": [1, 2, 1], "characteristic_two_convolution": [1, 0, 1]}
    output["status"] = "all independent finite checks passed"
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
