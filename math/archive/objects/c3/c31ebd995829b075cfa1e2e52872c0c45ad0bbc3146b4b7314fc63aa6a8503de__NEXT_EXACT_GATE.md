# Next exact-FFT synthesis gate

## What this round decisively changed

Stop treating missing rank expansion as the only obstacle. A saved four-Green network has *every* square submatrix nonsingular, yet an exact 8x8 two-column determinant excludes all invertible middle gauges for its fixed stages. Phase 18/19 already had diagonal-similarity graph gates. The additional `K_0` pencil lets us reject bad fixed stage parameters without computing either stage inverse or searching gauge values.

## Best remaining constructive question

Find an all-length, exact, genuinely non-affine parameterized family of two Green sums `A_N,B_N` such that

`K_j(A_N,B_N) d_N=0` for every column j,

with `d_N` invertible coordinatewise. Then output-normalize `A_N diag(d_N) B_N e_0`, prove roots/weights/permutations and d_N generated in O(N), and prove full O(N) sequential application, not merely O(N) pre-specified matrix-vector work.

## How to reject an entire parametric family rather than a random instance

For each fixed permutation wiring, `det K_0` is rational in the weights and endpoint gauges. To show **generic impossibility** for that wiring it is enough to find one admissible nonzero finite-field specialization, as done for the N8 witness. To show **universal impossibility** over all admissible parameters one must prove that `det K_0` and the other phase constraints cannot simultaneously vanish on the nondegenerate locus. A single generic witness does NOT prove universal impossibility.

Use exact elimination/ideal certificates for small N, not numerical optimization failure. Check singular/zero-denominator branches separately rather than canceling denominators without saturation.

## Mandatory acceptance criteria for an exact O(N) FFT

1. all fresh arbitrary x over the stated exact field;
2. all N outputs explicitly materialized;
3. identity holds for every N in an infinite uniform family;
4. preprocessing and coefficient generation O(N);
5. O(N) sequential arithmetic applying all stages and normalization;
6. no hidden F_N, FFT black box, uncharged lookup table, or massive coefficients in bit-complexity claims;
7. stability/precision separately analyzed;
8. publication novelty verified beyond classical Weyl diagonal similarity and Edmonds' rank theorem.
