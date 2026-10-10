# 01. General eight-coordinate open chart

Exact SHA-256: `474b84028eb1e98aad8d3972d43211ac5c1b02e9efbd2f79fa56a3d269605140`

Source: `additions/1646/extracted/fft_spectral_determinant_gate_2026-10-09/general_onion.py`

Read scope: lines 1–123, complete. Supplied source was not executed, imported, compiled or parsed.

## Mathematical scope

Builds a separated-generator, diagonal-one C and B=F C[:,perm] modulo p. Four anchored families are eliminated; the remaining (n−4)(n−5) identities are explicitly not solved. For n=8 the reduction is 30→12 equations. For n=64 it leaves 3,540 identities. The eight coordinates describe the guarded patch, not a complete parameterization of every possible FFT factorization.

## Guards and acceptance

Lines 18–20 assert n≥6, eight coordinates, a true permutation with prefix (n−1,0,n−2). Lines 22–26 invert z, t, h0 and z−1. Every S1[k], the boundary determinant, every interior Delta and alpha must be nonzero (42–66). alpha=0 is rejected as a singular column pair. The returned denominator list omits z−1 and alpha; alpha is a separate field. Primality of p and exact root order are caller preconditions, not validated by build. Det(C), B corner anchors and inverse-A corners are not acceptance guards in build.

## Tests and certificate limits

verify (84–114) samples nonzero coordinates, skips ZeroDivisionError without replenishment, counts C rank and B anchors, and checks coordinate recovery only when both B anchors are nonzero. Its main mode has no minimum valid-sample assertion. The companion unittest does demand four valid, full-rank, B-anchored samples. Assertions are Python assert and disappear with optimization.

## Cost and implementation

O(n²) scalar construction/prefix-tail sums and dense storage; dense F@C and rank checks are O(n³). NumPy int64 modular reduction occurs after products/sums; require an overflow bound such as n(p−1)²≤2^63−1, plus elimination bounds. Supplied n≤64 and p≤65537 lie safely below those elementary bounds, but the public generic API does not enforce them.

Finding IDs: F01, F02, F03, F05, F08.
