# Chain recovery: resume at Phase 41

## Current verified state

- Phase 39's 18 tests pass after compiling its native checker from the previous research archive. Phase 39 excludes a specific three-middle-generator, two-coupling masked/permuted Green pencil at N=4,8,16.
- Phase 40 adds a **fourth middle generator**, three arbitrary complex scalar coefficients, and **two freely chosen internal diagonal masks/permutations**. All eight cycle Green solves together have O(N) online field-work for fixed parameters.
- Five non-star projective 2x2 minors on a cycle, each multiplied by four homogeneous variables, produce a square 20x20 degree-3 coefficient certificate. Full rank implies **no** nonzero projective coupling fits that mapping.
- **All 376,320** ordered 2-row/5-column mappings at N=8 are excluded at **both split primes**. This is an exact characteristic-zero **fixed-family** result for all masks/permutations/couplings. No universal all-ordering result.
- One fixed five-cycle occasionally has rank 19 at N=16. Example: rows (2,8), columns (8,10,3,2,5), over both primes. Another five-cycle restores rank 20; do not misreport sparse-certificate failures as valid factorizations.
- With the adaptive two-cycle certificate, packaged N=16 samples: **1,000,000 mappings at p=998244353 and 250,000 at p=2013265921**, all excluded. At N=32/64/128 the packaged sample counts per prime are 100,000/50,000/25,000, respectively; all excluded. These are **sampled**, not exhaustive.
- Independent weighted-cycle result: a common vertex diagonal gauge reduces 2N edge weights on two Hamiltonian cycles to **N+1 gauge-invariant chord holonomies**, with an exact union-find tree normalization and O(N) weighted Green execution. This is **established gain-graph switching mathematics**, applied here.
- The 4x(N+1) Jacobian of four local projective cross-ratios wrt those chord weights has rank 4 for **explicit integer edge weights and fixed cycle orders at N=8,16,32**. Explicit nonzero minors survive two primes for the *same integer problem*. Therefore the local cross-ratio map is dominant over C for those graph orders. **No specific Fourier target solution has been constructed. Gains are arbitrary nonzero complex parameters; **unit-modulus phase-only control is not proved**.**
- Sampled product of 3 pairs of independently weighted Green resolvents fails both exact Fourier Weyl identities at N=8..128 (two primes). Positive radix-2 Fourier control passes.
- **No general-input o(N log N) FFT**, no new integer multiplication bit bound.

## Reproduction

From the extracted Phase 40 directory:

```sh
g++ -O3 -std=c++17 phase40_exact_audit.cpp -o phase40_exact_audit
python -m unittest -v tests_phase40
./phase40_exact_audit N8_p998244353.txt 0 0 rescue
./phase40_exact_audit N8_p2013265921.txt 0 0 rescue
./phase40_exact_audit N16_p998244353.txt 0 100000 rescue
python phase40_holonomy.py
python phase40_local_synthesis.py
python phase40_weyl_control.py
sha256sum -c SHA256SUMS.txt
```

All audited inputs and short output records are packaged. The previous Phase 39 chain is in `previous_full_phase39_checkpoint.zip`.

## Phase 41 target: actual Fourier phase synthesis

- Keep the two noncommuting weighted Hamiltonian cycles and their N+1 canonical holonomies. Attempt to **solve the actual Fourier cross-ratios** rather than only generic local ratios.
- If a local solution is found, extend it to all rows/columns and test Weyl identities MZ=DM and MD=Z^-1M in exact arithmetic, with seeded positive/negative controls.
- Explicitly count the cost of finding/precomputing holonomies. Parameter-existence or local Jacobian dominance is **not** an FFT algorithm.
- Do not revisit a single common-generator Green sum or random scalar coupling searches without a new mathematical reason. Avoid treating an underspecified Macaulay rank loss as a genuine factorization.
