#!/usr/bin/env python3
"""Fresh exact boundary checks for the separately frozen supplement v1."""
from fractions import Fraction
from pathlib import Path
import json

def main():
    n = 8
    A = [[Fraction(3 if i == j else 1 if i > j else 2) for j in range(n)] for i in range(n)]
    H = [[255 if i == j else -(2 ** (8 - (j - i))) if i < j else -(2 ** (i - j - 1))
          for j in range(n)] for i in range(n)]
    C = [[Fraction(v, 511) for v in row] for row in H]
    checked = 0
    for i in range(n):
        for j in range(n):
            assert sum(A[i][k] * C[k][j] for k in range(n)) == (i == j)
            checked += 1
            # Explicit source-chart generators: lower l=m=1; upper u=2,v=1.
            assert A[i][j] == (Fraction(3) if i == j else Fraction(1) if i > j else Fraction(2))
    forbidden_entry = C[0][2]
    disjoint_minor = C[0][1] * C[2][3] - C[0][3] * C[2][1]
    assert forbidden_entry == -Fraction(64, 511)
    assert disjoint_minor == Fraction(32, 511)
    assert forbidden_entry != 0 and disjoint_minor != 0
    out = {
        'status': 'PASS: exact witness outside both F8 inverse restrictions',
        'inverse_equations_checked': checked,
        'A': [[str(v) for v in row] for row in A],
        'inverse_numerator_H': H,
        'inverse_denominator': 511,
        'inverse_entry_0_2': str(forbidden_entry),
        'disjoint_minor_rows': [0, 2],
        'disjoint_minor_columns': [1, 3],
        'disjoint_minor': str(disjoint_minor),
        'uniform_theorem': 'For nonnegative integer r and N>=4r+4, no F_N=B P A in the stated chart if either inverse stage is diagonal plus rank at most r.',
        'uniform_theorem_basis': 'Self-contained rank/Vandermonde proof in SUPPLEMENT_V1.md; not inferred from this finite witness.',
        'unrestricted_F8_target_fiber': 'UNSOLVED',
        'historical_programs_run': False,
        'numerical_fitting_used': False
    }
    Path(__file__).with_name('SUPPLEMENT_V1_RESULTS.json').write_text(json.dumps(out, indent=2) + '\n')
    print('PASS: all 64 exact inverse equations; forbidden entry -64/511; disjoint minor 32/511.')
    print('Both restricted obstructions leave the unrestricted F8 target fiber open.')

if __name__ == '__main__':
    main()
