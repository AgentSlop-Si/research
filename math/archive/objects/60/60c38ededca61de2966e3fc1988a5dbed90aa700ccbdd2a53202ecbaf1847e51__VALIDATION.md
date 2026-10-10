# Phase 29 validation record — October 10, 2026

## Explicitly rerun

- Phase 28 inherited suite: **17 tests passed**, before modifying the code base.
- Phase 29 new suite: **11 tests passed**, including full N=8 re-enumeration of **112,896** ordered triple mapping pairs, 576 saved N=4 nonzero minor witnesses, seeded O(N) executor comparisons through N=128, the three saved Bézout identities, and deliberately planted positive controls.
- N=4 homogeneous Macaulay gate: **576/576 full-rank** for `p=998244353`, and **576/576 full-rank** for `p=2013265921` independently. Correct planted family has rank 14 for its true mapping.
- N=8 homogeneous anchored gate: **112,896/112,896 full rank** over `p=998244353`. The saved audit includes deterministic rank-stream SHA256, full histogram, 32 independently recomputed 15x15 determinants. Every full permutation induces one tested triple pair.
- N=16: two-coupling **slice** Bézout certificate with gcd 1 and full degrees `256,512`. Separately, **2000 sampled** anchored triple pairs had rank 15; **NOT** exhaustive.
- One slice N=4 (`lambda=0`) has a spurious linear gcd factor caused by 3 vanished B entries. This is explicitly tested, and not counted as a Fourier candidate.

## Mathematical integrity

Full modular rank means a concrete coefficient minor reduces to a nonzero element in Fp. Since all rational/cyclotomic denominators used in constructing the Green matrices and the DFT were invertible mod p, the corresponding characteristic-zero minor is nonzero. The homogeneous degree-four ideal therefore contains every degree-four form, forbidding common nonzero projective solutions for the specified mapping. This is exact exclusion over complex parameters, not a floating-point test.

The one-slice polynomial argument similarly uses nonzero parameter-independent leading coefficients in the second coupling and a modular Bézout identity; this proves no bivariate common polynomial factor and hence a finite algebraic exceptional locus, but it does **not** prove that the locus is empty at N=16.

No algorithmic speedup over `N log N` is claimed. The `O(N)` executor applies a **candidate Green-sum matrix** that the new theorems show cannot, in the specified configurations, be the Fourier transform.

## Fresh-extraction validation

The final Phase 29 archive was extracted to a new directory; `sha256sum -c SHA256SUMS.txt` succeeded for all packaged sources and artifacts. The **full Phase 29 11-test suite passed again** there in approximately 31 seconds, including complete regeneration of the 112,896 N=8 rank checks. ZIP integrity check (`unzip -t`) passed. Inherited Phase 28 regression suite was independently run before the Phase 29 changes and passed all 17 tests. Earlier phases are bundled but not all rerun in this phase.
