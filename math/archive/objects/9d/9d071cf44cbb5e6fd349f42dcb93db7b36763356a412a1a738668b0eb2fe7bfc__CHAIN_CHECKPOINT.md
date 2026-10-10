# HERO #17 — RECOVER HERE (Phase 8, 2026-10-10)

## Mission

Find a uniform exact, sequential `O(N)` full-length DFT for arbitrary fresh inputs. User's proposed tools: Graph + Union + Sparse Table + Quantum-inspired phase structures. No input-dependent cached streams, hidden FFTs, free large tables, free root generation, or GPU parallelism. **Goal not achieved.**

## Inherited evidence

- Phase 3: 76 tests; exact O(N) on structured shear/Green input classes.
- Phase 4: 7 tests; rank-one orbit displacement identities, dense square-orbit graph.
- Phase 5: 8 tests; gauge reparameterization can change apparent transition rank 1..M without improving charged circuit cost, and can be ill-conditioned.
- Phase 6: 14 tests; four-index tensor cut ranks and hidden Fourier conversion.
- Phase 7: 11 tests; independent rank-one rectangle incidence optimum `N min_{d|N}(d+N/d)`, plus special independent rank-r cost bounds. No general lower bound.
- All **116** predecessor tests rerun and passed in the present continuation.

## Phase 8 achieved

1. **Fixed-cut multistage rank theorem:** If `T_t=B_t+E_t`, with each B_t block diagonal on the SAME fixed coordinate cut `m|(N-m)` and rank(E_t)≤r_t, any exact Fourier product needs `sum r_t>=min(m,N-m)`. Proof by telescoping rank difference + Vandermonde cross block. Applies to arbitrary L, not changing cuts. Schur decomposition demonstrates rank-sharpness but is dense/expensive; invertible block-diagonal baseline witness also constructed.
2. **Polynomial-CRT bridge theorem for ANY balanced root partition N=2m:** `rank(R_B-R_A)=m` and `T=[[I,R_A],[I,R_B]]` invertible. All Fourier input coefficients are arbitrary.
3. **Unique sparsest coefficient transfer:** `nnz(R_A)+nnz(R_B)>=2m=N`; equality only for even/odd root subsets, returning classical radix-2 DIF butterflies. This concerns monomial-basis transfer support, not general arithmetic complexity.
4. **Exact cyclotomic N=16 enumeration:** 12,870 balanced root polynomials checked in Z[ζ_16], 6,435 complements. Minimum annihilator pair support4 (unique CT split), best nonperiodic support15. All 6,435 CRT bridge rank8 checks independently passed over F_17. Minimum transfer support16 unique CT; nonperiodic >=94 modulo17 and thus >=94 over cyclotomic integers for those 16-point instances.
5. **Functional arbitrary fresh exact DFT:** classical shared-binomial remainder executor with full ledger. Alternative root-partition direct-division executor tested and loses after charging plan/online work; this is NOT a faster general FFT.
6. **Ancillary negative controls:** exact input-independent semantic union has zero proportional forms across classical FFT stages; an O(N)-addition nonunitary star produces an invertible dense transform but not Fourier; finite-field truth tables need >=p^r entries and p>=N+1; Ailon (2013) unitary entropy lower bound independently reproduced, not claimed novel.
7. **Checks:** Phase 8 13/13, predecessors 116/116; 88 independent full DFTs = 4,868 exact outputs, N=65,536 all-output execution with 36 independently checked bins; all 6,435 N16 CRT bridge matrices exact checked.

## Core honest verdict

The network is **not** O(N) for arbitrary fresh inputs. The only demonstrated fully charged general-input executor here is ordinary radix-2 DIF FFT: Θ(N log N). A unique-sparsest *middle matrix* says nothing about general circuit lower bounds when circuits can share algebra across blocks.

## Next useful problem, not a rerun

Target a truly **joint cross-branch contraction** for `R_A high` and `R_B high` inside a recursive polynomial-root tree, allowing intermediate nonunitary operators and cancellation but charging *all* arithmetic and root/plan preparation. Verify against FFT and the OpenAI Math #130 specialized exact complex bound **in matching models**. Search beyond literal matrix sparsity, rank-only interface changes, small truth-table blocks, static exact-value collisions and already-known Bruun/FFT root division.

Novelty is unverified: polynomial-divisor FFTs trace to Fiduccia (1972), and entropy lower bounds to Ailon (2013). Cite them and avoid priority claims.

## Reproduce

`python -m unittest discover -v` then `python independent_audit.py` from this directory. `PROOF_CERTIFICATE.md` contains all assumptions and derivations; `AUDIT_RESULTS.json` contains finite search counts. Prior packages remain separately available and are not bundled here.
