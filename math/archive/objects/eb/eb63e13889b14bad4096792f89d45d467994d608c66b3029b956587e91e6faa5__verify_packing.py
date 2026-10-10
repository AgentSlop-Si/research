"""Independent, bounded-word guarded-field addition checks (standard library)."""
from __future__ import annotations

import itertools
import json
import random
from pathlib import Path


def packed_sum(rows: list[list[int]], bound: int, word_bits: int):
    groups = len(rows)
    width = len(rows[0])
    field_bits = (2 * bound * groups).bit_length()
    lanes = word_bits // field_bits
    if not lanes:
        raise ValueError("a lane does not fit in one word")
    mask = (1 << field_bits) - 1
    totals = [0] * ((width + lanes - 1) // lanes)
    additions = 0
    for row in rows:
        assert len(row) == width
        for first in range(0, width, lanes):
            packed = 0
            for offset, value in enumerate(row[first:first + lanes]):
                assert -bound <= value <= bound
                packed |= (value + bound) << (offset * field_bits)
            assert packed.bit_length() <= word_bits
            position = first // lanes
            totals[position] += packed
            additions += 1
            assert totals[position].bit_length() <= word_bits
    result = []
    for first in range(0, width, lanes):
        total = totals[first // lanes]
        for offset in range(min(lanes, width - first)):
            result.append(((total >> (offset * field_bits)) & mask) - groups * bound)
    assert result == [sum(row[j] for row in rows) for j in range(width)]
    assert additions == groups * ((width + lanes - 1) // lanes)
    return result


def main():
    counts = {"exhaustive_cases": 0, "random_cases": 0, "boundary_cases": 0}
    for groups, width in itertools.product(range(1, 4), range(1, 4)):
        for flat in itertools.product((-1, 0, 1), repeat=groups * width):
            rows = [list(flat[i * width:(i + 1) * width]) for i in range(groups)]
            packed_sum(rows, 1, 16)
            counts["exhaustive_cases"] += 1
    rng = random.Random(20261009)
    for _ in range(1000):
        bound = rng.choice((1, 2, 3, 8, 127, 1024))
        groups = rng.choice((1, 2, 3, 7, 16, 31, 101, 500))
        width = rng.randint(1, 151)
        word_bits = max((2 * bound * groups).bit_length(), rng.choice((8, 16, 32, 64, 127)))
        rows = [[rng.randint(-bound, bound) for _ in range(width)] for _ in range(groups)]
        packed_sum(rows, bound, word_bits)
        counts["random_cases"] += 1
    for bound, groups, width, sign in itertools.product((1, 3, 17, 1024), (1, 3, 16, 101), (1, 13, 129), (-1, 1)):
        bits = max(32, (2 * bound * groups).bit_length())
        packed_sum([[sign * bound] * width for _ in range(groups)], bound, bits)
        counts["boundary_cases"] += 1
    report = {"status": "PASS", **counts, "random_seed": 20261009}
    Path(__file__).with_name("packing_results.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
