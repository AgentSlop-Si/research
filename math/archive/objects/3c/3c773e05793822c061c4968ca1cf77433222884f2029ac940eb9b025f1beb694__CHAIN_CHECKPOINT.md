# RECOVER HERE — HERO #17 Phase 16 (2026-10-10)

**Canonical bundle:** `fft_hero17_phase16_fourier_green_interface_2026-10-10.zip`.

## Original goal — still open

Fresh arbitrary complex inputs; all N exact DFT coefficients; fully charged sequential work `O(N)` or any new general improvement over exact sub-NlogN frontier. Avoid unrelated fast Green operators, low-rank input families, isolated sparse bridges, free coefficient recovery, uncharged tables, free chirp kernel evaluation, or multiple processors. **Still no universal O(N) FFT.**

## Recovered baseline

Phase 15: Weyl support (`3^L>=N²/2` for even length) under products of q-atom inverse Green stages; chirp cyclic convolution shift-only product requires `L>=log2 N+1` when N=2^m; multiscale dyadic Green fusion really eliminates log N passes for a different operator. Phase 15 precursor zip is retained and 21 predecessor tests passed again.

## What Phase 16 *proved*

1. For any field with N distinct Fourier roots, a nonzero vector supported in q cyclic **consecutive** sites has at most q-1 zeros in its DFT.
2. If `F=D_L P Q^-1 D_R` with invertible diagonal endpoint gauges and Q invertible, columns of Q consecutive-support size <=s, and columns of P support size <=t, then `s+t>=N+1`. In particular cyclic band radii `a+b>=ceil((N-1)/2)`. Coefficients can be position-dependent and P,Q need not commute.
3. For any cyclic nearest-neighbor matrix H, a rational Fourier representation `F=D_L p(H)q(H)^-1 D_R` needs `deg p + deg q >= ceil((N-1)/2)`.
4. At odd-length equality, each Q column is uniquely the coefficient polynomial with zeros at all forbidden Fourier roots. The explicit matrices satisfy `FQ=P` and have prescribed bands. **Q invertibility is conditional**.
5. For odd N, Q in this boundary construction is explicitly `D_left C_h D_right`, a chirp-gauged circular convolution. Its inverse remains unaccelerated.
6. Quadratic chirps obey `D_c S^s D_c^-1=omega^(cs²) S^s T^(2cs)`; paired chirp conjugation only permutes Weyl directions.

## Verified finite-field details

- New 19/19 tests; predecessor 21/21.
- Independent audit 120 full DFTs, 1,368 coefficients, 4,912 exhaustive supported-vector tests, 13 Harper algebra certificates.
- Invertible boundary Q small odd N=3,5,7,9,11,13,15,17; also N=45 over GF(271). Mod-p nonzero determinant certifies nonzero complex determinant for those explicit cyclotomic matrices.
- Critical field exception N=45: Q rank 43 over GF(181), rank 45 over GF(271). More exceptions at N=49/53. Never infer invertibility merely from interpolation identities.
- Harper finite-field finding: for tested N=4,8,12,16, span of powers of Harper H has rank N-1; adding Fourier increases to N. **Do not generalize to all complex N without proof.**

## What this does NOT prove

- Not an unrestricted FFT arithmetic lower bound: dense or long-range Green and branching networks evade this quotient grammar.
- Not a universal exact O(N) algorithm: Q^-1 hides convolution; boundary bands each grow linearly with N.
- Not all-length denominator nonsingularity; specific exact counterexamples exist in valid finite fields.
- Not historical novelty: links to known uncertainty/Harper literature supplied.

## Exact target for Phase 17

Find a genuinely *branched* chirp-Green feedback architecture **not expressible as D_L P Q^-1 D_R with P,Q low local bandwidth**, yet satisfying `M S=T^-1 M, M e0=ones`. Try small exact finite-field candidates first, independently verify all basis inputs, charge the entire shared evaluator. Avoid returning to disguised Cooley–Tukey and do not assume q-binomial convolutions are free.

## Reproduce

`python -m unittest -v test_phase16`
`python independent_audit.py`

Earlier lineage: extract `PHASE15_PREDECESSOR.zip` and run `python -m unittest -q test_phase15` in that extracted root.
