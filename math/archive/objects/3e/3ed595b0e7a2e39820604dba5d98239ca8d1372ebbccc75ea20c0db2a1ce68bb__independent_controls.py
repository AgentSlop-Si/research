"""Reviewer-authored controls; never imports, parses, compiles, or executes uploaded code.

These verify arithmetic facts and control-flow counterexamples used in the static
review. Acceptance of an uploaded function is proved from its cited source lines,
not obtained by invoking that function.
"""
from pathlib import Path
import json

P = 998244353

def trim(values):
    values = [v % P for v in values]
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return values

def convolution(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = (out[i + j] + x * y) % P
    return trim(out)

def add(a, b):
    out = [0] * max(len(a), len(b))
    for i, value in enumerate(a):
        out[i] += value
    for i, value in enumerate(b):
        out[i] += value
    return trim(out)

# Source verify_saved_audit accepts this after build_family returns normally:
# metadata assertion succeeds, then the dictionary iteration is empty.
empty_witness_certificate = {
    'prime': P, 'n': 4, 'seed': 2804, 'full_rank_cases': 576,
    'pivot_witnesses': {},
}
metadata_predicate = (empty_witness_certificate['prime'] == P
                      and empty_witness_certificate['n'] == 4
                      and empty_witness_certificate['full_rank_cases'] == 576)
visited_witnesses = sum(1 for _ in empty_witness_certificate['pivot_witnesses'])
assert metadata_predicate and visited_witnesses == 0

# All listed lengths and the Bezout identity in the source validate() pass;
# both alleged leading coefficients are zero, so the required full degrees fail.
p1 = [1] + [0] * 16
p2 = [0] * 33
bad_slice_certificate = {
    'n': 4, 'slice_P1': p1, 'slice_P2': p2,
    'leading_mu_coefficients': [0, 0], 'bezout_U': [1], 'bezout_V': [0],
}
source_predicate_facts = {
    'lengths_pass': len(p1) == 17 and len(p2) == 33,
    'self_reported_leading_values_match': [p1[-1], p2[-1]] == [0, 0],
    'bezout_identity_passes': add(convolution([1], p1), convolution([0], p2)) == [1],
    'required_nonzero_leading_terms_fail': p1[-1] == 0 and p2[-1] == 0,
}
assert all(source_predicate_facts.values())

# The fixed-N8 C++ break is scoped to the inner range-for only.
limit_counts = {}
for limit in [0, 1, 10, 336, 337, 112896]:
    total = 0
    for row_index in range(336):
        for column_index in range(336):
            total += 1
            if total >= limit:
                break
    limit_counts[str(limit)] = total
assert limit_counts['1'] == 336
assert limit_counts['112896'] == 112896

# Canonical field equality conflicts with the source's raw integer zero count.
target = [[P, 1], [1, 1]]
middle = [[0, 1], [1, 1]]
assert [[v % P for v in row] for row in target] == middle
zero_counts = [sum(v == 0 for row in matrix for v in row)
               for matrix in [target, middle]]
assert zero_counts == [0, 1]

out = {
    'method': 'Reviewer-authored facts only; no uploaded code executed/imported/compiled.',
    'empty_saved_audit': {
        'metadata_predicate_passes': metadata_predicate,
        'witnesses_visited': visited_witnesses,
        'acceptance_proof': 'c118559b lines 145-155; conditional only on normal build_family return.',
    },
    'empty_minor': {
        'source_result_by_inspection': 1,
        'reason': 'c118559b lines 82-103 set out=1; n=0 makes shape and pivot loops empty.',
        'would_bypass_nonempty_witness_check': True,
    },
    'bad_slice': source_predicate_facts,
    'fixed_cpp_limit_actual_mapping_counts': limit_counts,
    'noncanonical_zero_count': {'field_matrices_equal': True, 'raw_zero_counts': zero_counts},
    'packed_default_record': {'actual_bytes': 21, 'docstring_promised_bytes': 25},
}
root = Path(__file__).resolve().parent
(root / 'COUNTEREXAMPLE_EMPTY_WITNESSES.json').write_text(json.dumps(empty_witness_certificate, indent=2) + '\n')
(root / 'COUNTEREXAMPLE_BAD_SLICE.json').write_text(json.dumps(bad_slice_certificate, indent=2) + '\n')
(root / 'INDEPENDENT_CONTROL_RESULTS.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
