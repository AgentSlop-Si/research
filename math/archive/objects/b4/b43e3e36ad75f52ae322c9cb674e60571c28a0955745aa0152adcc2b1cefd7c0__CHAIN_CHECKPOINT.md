# RECOVER HERE — HERO #17 Phase 17, 2026-10-10

## Core goal remains open

Find an exact `O(N)` sequential algorithm for the full DFT on every fresh arbitrary dense input, or a rigorously charged genuine improvement on the exact-arithmetic frontier. Count input reads, precomputation, shared intermediate computations and all N output writes. Do not mistake O(N) Green, a sparse middle graph, a rank certificate, memoized repeats or special signal families for a general FFT speedup.

## Immediate predecessor

`fft_hero17_phase16_fourier_green_interface_2026-10-10.zip`: proved the local-band quotient barrier using Fourier polynomial zeros; equality examples hide an inverse chirp convolution. Its 19 tests pass in the present session. Stored intact as `PHASE16_PREDECESSOR.zip`.

## New mathematically proved Phase 17 results

1. **General support/Hall-Vandermonde cut**: if consecutive-in-frequency row set I and column set B satisfy P[I,B]=0 and |neighborhood_Q(B)| <= |I|, then `rank(E_P)+rank(E_Q)>=|B|` in any exact monomial-Fourier quotient `(P+E_P)(Q+E_Q)^-1`.
2. **Uniform sparse degree**: for col-degrees `t` and `s`, rank feedback `r_P+r_Q >= floor(N/(1+st))`, valid for arbitrary long-range sparse supports, arbitrary N, and arbitrary monomial Fourier endpoint gauges (including independent permutations).
3. **Aligned cyclic bands**: if numerator radius a and denominator radius b, `r_P+r_Q >= max(0, floor(N/2)-a-b)`; stronger than Phase16 for small nonzero rank budget.
4. **Covariance defect**: `D(A)=AS-T^-1 A`, so correcting A to Fourier by additive rank-r needs `r>=ceil(rank D(A)/2)`. For invertible `Q=I-alpha*S-beta*T`, alpha nonzero, `rank D(Q^-1)>=N-2` by exact 2nd-order recurrence. Generic even N has rank N.
5. **Rank-one Green feedback**: a mixed/noncommuting cyclic Green recurrence + Sherman-Morrison global rank-one feedback executes exactly in O(N) field work on arbitrary fresh inputs. For a supplied valid root: complete preparation `15N+5`, each online RHS `9N+2` counted arithmetic operations; **NOT** an FFT.
6. **Fast Fourier candidate rejection** via independent random intertwining probes; Freivalds-type screen, not proof of identity.

## Independent checking

`python -m unittest -v test_phase17` — 19 tests.
`python independent_audit.py` — independent modular rank and dense Gaussian evaluator, support certificates including exhaustive permutation-support pairs and arbitrary endpoint permutations; field-op counts in `AUDIT_RESULTS.json`.
Rerun Phase16 predecessor via README instructions.

## Traps to avoid again

- Per-column *graph degree* vs bandwidth: degrees can be constant for long-range shifts, but a low-rank feedback correction still fails this quotient model. No assertion about unrestricted circuit time follows.
- Green feedback produces a dense operator in O(N) but does not satisfy `M S=T^-1 M`; do not call it FFT.
- Theorem statements on `F` use **monomial Fourier gauges**, not arbitrary dense input/output basis changes.
- The covariance rank theorem as written uses the bare mixed Green baseline. Arbitrary endpoint diagonal gauges must be included in the defect before reusing the lower bound.
- A field-operation ledger assumes a supplied valid root and field. It does not count bit complexity or primitive-root discovery; root powers and every plan arithmetic operation are charged.
- Neither this phase nor Phases 1–16 establish historical novelty or a general O(N) Fourier transform.

## Exact surviving Phase 18 target

Find **a multibranch, noncommuting Green/Clifford feedback network whose global operator is NOT an arbitrary sparse quotient plus O(1)-rank feedback**. It must satisfy both `M S=T^-1 M` and `M e0=ones` for all N; pass the cheap randomized operator probes before full-basis exact verification; and exhibit a recurrence whose *entire* charged sequential work improves on conventional FFT and the published exact-complex asymptotic frontier. Try to exploit global reuse across the branches, not symbolic compression of a submatrix.

Priority subproblem: jointly evaluate the quadratic-chirp convolution hidden in Phase16's sharp band factorization. A fast chirp kernel **generator** is not a fast arbitrary-input chirp **convolver**.
