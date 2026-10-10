# RECOVER HERE — HERO #17 Phase 15 (2026-10-10)

**Canonical artifact:** `fft_hero17_phase15_multiscale_weyl_chirp_2026-10-10.zip`.

## Primary target

Fresh arbitrary complex (or exact finite-field) length-N input; all N exact Fourier coefficients; strictly better fully charged **sequential** work than the best known all-input DFT algorithm; ideally O(N). **Still not solved.** Do not use parallelism, hidden precomputation, amortization over repeated inputs, unrelated Green operators, or selected-bin queries as substitutions.

## Correctly recovered lineage

- Phase 12: sparse-inverse Green-product + low-rank correction gate; Weyl twirl of commuting Green paths.
- Phase 13: two-Green Weyl/Hankel branch grammar obstruction; changing Weyl basis can alter the rank of a *reshaped* coefficient array; a reverse-oriented Green composition can have full Weyl matrix rank while being linear-work.
- Phase 14: quantum-binomial mixed magnetic Green solve O(N), four signed-orientation span, nearest-neighbor cut bound, and long-range-shift escape. All 22 Phase 14 new tests passed again in this session. The untouched predecessor ZIP is included.
- **Phase 15:** Weyl-support count invariant under Weyl-monomial frame permutations and 3-term-inverse chain product: `3^L >= N²/2` for even N, `>=N²` odd N. This survives arbitrary long strides and different Weyl directions at every Green stage, plus Weyl monomial gauges; not arbitrary diagonal gauges or branch sums.
- **Phase 15:** Exact chirp-convolution `C=D F_- D` with inverse kernel `zeta^(-j²)/N`. For N=2^m>=4, any pure cyclic-shift Green factorization (arbitrary shift sizes, scalar params) needs `L>=m+1`. The `m` case fails by distinct subset-sum valuations and the nontrivial chirp parallelogram ratio. Does not prove `m+1` suffices.
- **Phase 15:** The inverse chirp kernel has full tensor cut rank `2^min(a,m-a)` despite O(N) generation. High rank is not an inherent generation-time lower bound.
- **Phase 15:** Positive control: `prod_j(I+alpha^(2^j)S^(2^j))=(1-alpha^N)(I-alpha S)^-1`; exact one-recurrence O(N) executor saves 5.33× charged field operations vs literal full-vector dyadic stages at N=65,536, but **the operator is not Fourier**.

## Proof and verification

Read `PROOF_CERTIFICATE.md`, run `python -m unittest -v test_phase15` and `python independent_audit.py`. At checkpoint: **21/21 new tests**, **22/22 predecessor Phase 14 tests**, direct Gauss/Weyl support (odd/even primes), 3,150 exhaustive shift multisets, 756 full reference DFT coefficients, 29 binary digit rank checks, arbitrary oriented Weyl coefficient products, large 65,536-output positive-control equality, and all 65,536 recurrence residuals.

## Specific false shortcuts excluded

- A large number of Weyl coefficient terms does not prove large evaluation cost; dyadic Green fusion is the counterexample.
- Balanced binary cut rank sqrt(N) of chirp *kernel* does not prove convolution needs superlinear time, or that forming the kernel is costly.
- The 3^L support gate excludes a **single product of q-atom inverse factors**. Branching sums may have dense inverses and escape it.
- Root-of-unity, finite-field coefficient width, scalar preparation, output writes and all operations must be charged before claiming a faster full transform.
- Do not mistake Fourier operator equality for equality of a few random outputs. Use `M S=T^-1 M` and `M e0=ones` as the exact matrix identity certificate under our negative-exponent convention; next phase must prove it symbolically for any proposed compact executor.

## Phase 16 productive target

Construct a **branching, mixed-direction** Green network (not a pure product), potentially with genuinely non-Weyl diagonal chirp gauges, whose **joint evaluator** satisfies both Fourier intertwining identities. Search small N with exact modular basis-vector tests before any asymptotic claim. Crucially find a recurrence that evaluates the whole network in less than N log N charged operations, not a sparse-looking internal basis or one different fast operator. Compare to all-length exact-complex benchmark `O(N (log N)^(1-1e-13))` in its actual model.

Do not claim novelty without a separate deep literature check; Bluestein, quadratic Gauss sums, Weyl/Clifford algebra and dyadic binomial factorization are classical.
