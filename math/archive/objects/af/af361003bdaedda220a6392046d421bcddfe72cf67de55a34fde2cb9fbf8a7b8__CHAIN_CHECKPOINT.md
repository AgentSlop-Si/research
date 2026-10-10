# HERO #17 — Recover here: Phase 13 (2026-10-10)

**Status:** 21 Phase-13 unit tests passed, two independent audit suites completed. Proven scoped Weyl/Hankel branching restrictions; exact full-vector branching Green positive control. **No general O(N) DFT.**

## Starting point / lineage

Previous: `fft_hero17_phase12_green_union_rank_gate_2026-10-10.zip`. Phase12: products of L invertible sparse-inverse Green stages plus total rank-r corrections cannot equal exact Fourier unless `s(r+1)^2>=N` (and stronger prime variant). Phase13 moves **outside this product model**, to parallel path sums and noncommuting ordered Weyl factors.

## New proven results

1. For odd N, canonical Weyl coefficients of unnormalized DFT: `C_F[a,b]=gamma*omega^(-(a-b)^2/4)`; coefficient matrix rank exactly N.
2. Any sum of B **ordered** `G_S(alpha) * G_T(beta)` paths, even with Weyl monomial endpoint gauges, needs `B>=N` to equal F_N. No statement for reversed, mixed, or deeper paths.
3. For arbitrary ordered generating Weyl directions `U=S^uT^v`, `V=S^rT^s`, rank(C')=`N/gcd(N,delta)`, with `delta=(us-vr-ur-vs)/2`. A good basis can make the Fourier coefficient matrix rank **one**. This is a key anti-shortcut.
4. For **odd prime N=p**, **every fixed generating Weyl pair** still needs at least `(p+1)/2` ordered `G_U * G_V` resolvent paths: either rank is p or a residual nondegenerate quadratic chirp has full nonwrapping Hankel rank `(p+1)/2`. Assumptions: same U,V for every branch, no free arbitrary endpoint gauges, nonzero denominators, exact field arithmetic.
5. `G_T * G_S` and `G_S * G_T * G_S` can already have full canonical Weyl coefficient rank N and nonetheless execute in O(N). Never treat Weyl rank alone as an arithmetic-circuit lower bound.
6. Branch sum `H=G_S(alpha)+G_T(beta)` has generic **completely dense inverse** for every N>=2 over C and can still be applied in O(N) on arbitrary input; proven by specializing beta=0 and continuity. This is a genuine branch witness not representable by a constant-length *uncorrected* chain of inverse-two-sparse Green factors as N grows. **H IS NOT THE DFT.**

## Reproduction

From `hero17_phase13_weyl_branch/`:

`python -m unittest -v test_phase13`

`python independent_audit.py`

`python orientation_audit.py`

Proofs in `PROOF_CERTIFICATE.md`, complete interpretation in `RESEARCH.md`, finite-field costs in `AUDIT_RESULTS.json`. `SHA256SUMS.txt` covers frozen source/report artifacts in the final zip.

## Verification

- 21 new test groups.
- 47 full matrix reconstructions (5,423 entries) over independently chosen transformed Weyl bases.
- 15,744 GL2 direction pairs enumerated at p=3,5,7,11.
- 7 exact dense inverse modular witnesses.
- 201 orientation basis-vector checks plus 56 independent random vector checks.
- N=65,536 arbitrary-input Green sum: all recurrence equations checked, 9 direct kernel rows checked, 9 direct FFT coefficients evaluated and all differed. Batch preparation + full execution: 851,967 field ops including two inversions.

## Stop list

- Never announce linear-time DFT from Green surrogate O(N) numbers: its outputs differ from F_N.
- Do not promote coefficient rank or commutator rank to a general arithmetic lower bound: reverse/triple paths violate that inference.
- Do not claim fixed-basis lower bound for branches with different Weyl directions, opposite order, or arbitrary gauges.
- Rank-one coordinate rotations do not produce geometric coefficients for free; price the chirp/Prony Hankel signature.
- Do not re-prove Phase12's sparse-inverse-product obstruction or Phase10/11's lazy projector-to-FFT recurrence.
- No historical novelty priority without independent literature review and peer criticism.

## Exact next target (Phase 14)

Mixed-orientation, noncommuting **multi-branch Green** schedules with truly shared evaluation. Derive an invariant of **short recurrence composition** that survives gauge changes but does not falsely label O(N) reverse/triple Green products as hard. Build an end-to-end full DFT candidate for arbitrary raw input. Test on all basis vectors and independent random vectors, with full preprocessing, output, memory and scalar accounting. A rank-only shortcut is not enough.
