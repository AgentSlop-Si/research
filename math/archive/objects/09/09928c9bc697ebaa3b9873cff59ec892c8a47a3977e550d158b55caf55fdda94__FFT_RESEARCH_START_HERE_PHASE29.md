# FFT graph-reuse research — Phase 29 entrypoint (2026-10-10)

**Primary file:** `fft_green_research_phase29_2026-10-10.zip`.

## Problem

Seek a new general-input Fourier/integer multiplication algorithm using noncommuting, independently ordered Green computation graphs and shared intermediate operations, ultimately with genuinely `o(N log N)` total cost, including preprocessing, movement and precision. This goal has **not** yet been achieved.

## Phase 29 results

1. **Two tunable middle couplings:** `B(lambda,mu)=G0+lambda G1+mu G2` between fixed outer Green sums. Trace-moment projective constraints yield bivariate polynomials of total degrees at most `N^2` and `2N^2`. Exact one-parameter slice Bézout certificates imply a **finite exceptional complex pair locus** at N=4,8,16 (maximum 512,8192,131072 solutions counted with multiplicity). This does not prove the locus empty.
2. **Complete N=4 no-go:** all **576** full row/column permutation pairs have full-rank 54-by-15 homogeneous Macaulay matrices. This excludes **all complex lambda,mu and arbitrary two internal diagonal masks and permutations** for the fixed seeded A,C,G0,G1,G2.
3. **Complete N=8 no-go:** all **112,896** ordered mappings of three chosen target rows and three chosen target columns have full-rank 24-by-15 homogeneous Macaulay matrices. Every full permutation induces one such pair, so this excludes all complex lambda,mu and both internal monomial masks for the N=8 seeded family.
4. **Only finite-locus theorem at N=16**; 2000 sampled anchors do not prove universal exclusion.
5. Three-term Green candidate still has an exact `O(N)` forward executor, tested against dense arithmetic. It is **not** a Fourier algorithm.

## Reproduce

Extract the ZIP. Read `fft_green_phase29_two_parameter/THEOREM.md`, then `CHECKPOINT.md`. `RUN.md` has direct Python commands. No third-party Python packages are needed. The entire Phase 28 archive is included nested as `previous_full_phase28_checkpoint.zip`.

The new phase's exact small-instance negative results are not externally peer-reviewed, and standard projective/Macaulay techniques have extensive prior art. Keep any claims about novelty and complexity carefully qualified.
