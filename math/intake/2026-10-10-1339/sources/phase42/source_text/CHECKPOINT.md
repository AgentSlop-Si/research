# Phase 43 chain recovery — start here

**Date:** October 10, 2026. **Research goal:** a genuinely faster exact Fourier transform using noncommuting Green resolvents and reusable computation graphs. **Status:** No general-input `o(N log N)` FFT and no bit-complexity breakthrough proved.

## What Phase 42 proved (and tested)

1. **General finite-signature theorem for sums.** For `q` arbitrary weighted Hamiltonian-cycle Green inverses, even with arbitrary per-term monomial input/output gauges and arbitrary outer monomial equivalence, exact `N`-point DFT requires `N <= q (q+1)^q`. This uses projective-signature partitions and full-rank consecutive Fourier Vandermonde minors. It is a restricted *representation* obstruction, not a lower bound against arbitrary FFT circuits.
2. **Fixed graph family `N=128`: a complete exclusion for three summands.** The source file `graph_N128.txt` stores the three Phase41 cycles. A C++ all-row combinatorial audit examined **every one of 10,668,000 four-row subsets**. Every subset contains four input columns with identical joint signatures, so all three-term Green sums built from these exact orders have a forced rank-3 `4x4` block. No edge weights, scalar coefficients, per-term input/output **diagonal** gauges, or external monomial gauges can repair it. Additional independent per-term permutations would change the graph orders, so are outside this fixed-order certificate.
3. **Phase 41 three-cycle sum, three-row differential.** Exact rational-Gaussian unit phases give total real Jacobian rank `2N+1` for three-row anchored ratios, compared with `2N-2` for two-row ratios, at `N=8,16,32,64`, in **both** independent finite fields. Only three tangent directions remain locally after matching the first pair at a regular point.
4. **Three-row spectral-capacity refinement.** For a fixed three-row selection, graph signature classes and a nontrivial quadratic-spectral consistency polynomial bound each nonexceptional class to four Fourier frequencies. The seeded `N=64,128` examples have 11 combinatorial classes, all with exact nonzero cofactor-phase discrepancy residues, so this bounds them by 44 frequencies. Unlike the full `N=128` all-row collision result, it is specific to the selected three rows.
5. **Positive escape route:** A product of two noncommuting three-Green sums restores the forced `4x4` minor rank to 4. Its three-row projective real Jacobian has **full rank `4(N-1)`** at `N=8,16,32,64`, with common exact rational-Gaussian parameters in both primes. Independent finite differences at `N=8,16` agree with derivative formulas to `<7e-10` relative error. The sample product fails the Fourier Weyl equation at all tested coordinates and is **not** a Fourier algorithm.

## Explicit prohibitions on interpretation

- Do not call the local Jacobian rank an exact Fourier interpolation or a fast general-purpose DFT.
- Do not assume the `N=128` fixed-cycle certificate covers all possible graph cycles.
- Do not infer an `N log N` arithmetic lower bound for products from an obstruction to sums.
- Do not count fixed input weights as free when assessing bit complexity or preprocessing.
- Do not claim mathematical publication priority without independent literature checking.

## Next target

**Construct and certify actual *three-row* Fourier coherence inside the two-stage six-cycle product**. The full local Jacobian rank supplies a regular point where small arbitrary target perturbations can be realized, but not a proof of reaching the specific Fourier projective target. Test small sizes with interval/alpha theory or exact algebraic certificates. If the three rows can be matched, check a fourth Fourier row and both Weyl identities, including input/output row and column normalization. Always track parameter synthesis cost, condition numbers, edge bit-lengths, and online operations.

## Reproduce

From `fft_green_phase42_three_row`: `bash RUN.sh`. Compiles `phase42_all_row_audit.cpp` from source, reruns `9` Phase 42 regression tests (including the exhaustive `N=128` sweep), and can rerun the `11` preserved Phase 41 tests from the nested archive with `bash RUN.sh historical`.

For complete mathematical proof and assumptions see `THEOREM.md`, especially §2–§7. All audit JSON files are independent test data, not theorem assumptions.
