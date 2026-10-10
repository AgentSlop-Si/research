# Historical baseline text coverage: rows 80–99

## Coverage and findings

All 20 texts were read completely and matched to their recorded source hashes, totaling 94,742 bytes. Together with the two immutable earlier batches, rows 80–199 comprise **120 inspected texts and 274,349 bytes**. Per-source classifications, substantive claims, and proof/code limitations are recorded in `COVERAGE.json`.

The successive README chain 124 → 108 → 97 → 85 → 81 is verified by exact byte-prefix comparisons. Each new suffix was read. These are historical extensions, rather than wholly new mathematical results or exact duplicates. Saved execution claims are still source-authored evidence, including reports titled “independent review.” No uploaded program was run or imported.

## Hidden-order Green theorem: accepted bounded proof

Row 84 defines tau=(0,m,1,m+1,…) and the permutation Q by that row order. Reordering the natural path precision T gives exactly the distance-two edges plus the bridge (1,N−2). Each prefix cut crosses at most three edges. Real SPD block inversion proves equality of a precision cross-block rank and the inverse cross-block rank; hence QMQᵀ has upper/lower quasiseparable rank at most 1+3=4. A rank-one left reflection increases the bound to at most five, while diagonal endpoint factors preserve it.

For N=4q a power of two at least eight, the selected Fourier row/column sets consist of paired indices a,a+N/2. Adding and subtracting paired equations separates row and column parities. Each resulting q/2-square system is diagonally equivalent to a Vandermonde matrix at distinct powers of omega^4. Therefore both displayed target half-blocks are invertible when the characteristic is not two. This verifies the source’s algebraic hidden-order diagnosis. The numerical two-stage cutoff also invokes the earlier halfcut theorem; that dependency is kept explicit rather than presumed from this excerpt.

Fresh controls check 5,460 reordered precision entries, all 120 prefix cuts through N=64, and eight Fourier half-block ranks. This also supplies the previously missing explicit permutation identity for row 123’s pentadiagonal-plus-rank-two inverse reduction. The earlier batch is not edited. Real positivity does not guarantee modular pivot guards; allowed field specializations still require nonsingularity.

## Bidirectional-sum reduction

For row 87, direct multiplication gives K=A H E⁻¹ C=B E⁻¹ C+A+A D E⁻¹ C, so K is tridiagonal. This holds with zero propagation edges, provided the stated backward-injection diagonal E is invertible. Reversing the product gives H⁻¹=E⁻¹ C K⁻¹ A when the full operator is nonsingular. Fresh controls cover 240 examples with resets, including one singular example retained for the forward identity and 239 valid inverse identities.

The shorter identity using actual invertible scans is equivalent. A general invertible tridiagonal matrix still need not permit unguarded Thomas elimination; appropriate pivoting/guards remain necessary. The source’s separate F4 construction, N≥5 one-stage exclusion and five distance-from-every-diagonal minor witnesses require their companion proofs and were not reconstructed from this summary.

## Pruned comparator and probability/cost scope

Row 93’s active-wire argument yields O(N(1+log k)) sparse-input/all-output arithmetic. Processing only reached butterflies and retaining structural support avoids a full N-slot scan at every sparse level. Our fresh active-set executor checks 129 configurations, including cancellations and zero support, against direct Fourier summation (9,138 coordinates), and checks the structural visit bound.

The conservative fixed-point error argument is analytically sound under its stated bounded-word contract: root-table error O(N tau) and E_(s+1)≤3E_s+O(kN tau+tau) imply E_d=O(kN³ tau). A sufficiently small inverse-polynomial tau has O(log N) precision for polylogarithmic k and inverse accuracy. Standard uniformly generated roots can be prepared in O(N)+polylog(N) word work, with constants and rounding charged. We did not build or certify a particular transcendental/root-rounding implementation here.

For the two stated polylogarithmic sample schedules, the comparator costs O(N loglog N). Thus the later, smaller-error table setting costing O(N log N/loglog N) is asymptotically slower than this comparator at dyadic lengths; the O(N) setting remains a different point. This is a comparison of matching coordinatewise input-mass-scaled approximate guarantees. Padding to a power of two does not preserve an arbitrary requested DFT.

## Other source boundaries

The fixed-field WHT lookup argument in row 89 is consistent: complete b-input tables use O(b p^b) entries/work, group log b tensor layers, and yield O(N log N/loglog N) word operations for fixed p and b=Theta(log N). The naive full-value NTT-table transfer fails because N divides q−1, so q≥N+1; explicit field-output bit writing gives a separate bit-model lower bound, not a word-RAM obstruction. Original source counts, tables, test executions and literature priority are not recertified.

The all-pass and affine-cycle source summaries are linked to the separate helper’s primary-proof review when available; they are not reclassified as accepted implementations from these summaries. In particular, a long factor product may have a cheap fused action. Related-input timings, calibration payback, event-history fixes, memory payload, random-cut searches, graph determinant witnesses and original sanitizer coverage remain source-reported evidence unless individually rechecked. A graph screen survivor is not a Fourier factorization.

The old tabulation checkpoint explicitly has packing/transposition/setup obligations still open; later progress must be linked by a separate exact source identity. External repository commits and bibliography in rows 83/89 were read as source provenance, not freshly browsed or accepted wholesale.

## Replay

Run `python check_hidden_and_pruned.py` to regenerate the fresh exact results, or `python isolated_replay.py` for a clean temporary-directory replay and byte comparison. `python verify_seal.py` checks this frozen package. Original source snapshots are inert text only.
