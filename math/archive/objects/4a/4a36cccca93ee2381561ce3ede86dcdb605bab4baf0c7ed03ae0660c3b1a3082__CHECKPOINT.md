# BROKEN-CHAIN RECOVERY — PHASE 19 — 9 October 2026

## Target and exclusions
The user is researching FFT/large integer multiplication via graph-based arithmetic sharing, especially **nonunitary, noncommuting Green resolvents**, not the CrocSwap / Swapnil-jain integer-multiplication proof architecture. No verified sub-`N log N` FFT yet. **Do not restart** phases 1–18 or falsely claim a new FFT upper bound.

## Read order
1. `THEOREM.md` — exact assumptions and proofs for the new gates, norm/conditioning barrier, and Harper no-go.
2. `joint_gate.py` and `audit.py` — exact finite-field simultaneous Weyl monomial verifier and positive controls.
3. `green_product_audit.py` — fixed Green-sum product samples; 12 exact negative examples; not universal parameter no-go.
4. `spectral_green.py` — non-diagonally-dominant singular-value control.
5. `near_resonance.py` — high-gain escape counterexample that still fails Fourier phase coherence.
6. `harper_monomial.py` — monomial centralizer of Harper and exact modular witnesses.
7. `previous_full_phase18_checkpoint.zip` — full prior Phase 18 plus nested Phase 17–12 history and original materials.

## Key theorems and limitations
- A fixed `M=A Q P B` satisfies BOTH Fourier intertwiners iff a single monomial `Q P` simultaneously conjugates the operator pair `(B T B^-1, B V B^-1)` to `(A^-1 V A, A^-1 T A)`. Joint vertex signatures and a cocycle solver give exact generic permutation/phase recovery or a rigorous veto. Never confuse *one* intertwiner with two, or two with calibrated F.
- Let `M=prod S_j`, each `S_j` a sum of phase/permutation-gauged inverses of `w`-banded `B_jr` whose singular values stay in `[a,b]`, with fixed positive `a,b`. Every summand has induced 1-norm at most `C=(b/a²)(1+2w(b/a)²)`. Then `||M-F||_2>=max(0,1-prod_j(q_j C)/sqrt(N))`. In particular fixed `q` and `t=o(log N)` yield error lower bound tending to **1**. No diagonal dominance or commutativity assumed.
- If `sigma_max(B)=1` and max denominator condition number K, exact normalized F with t stages/q summands forces `K>=N^(1/(8t))/[q(1+2w)]^(1/4)`. Assumes bounded gains and fixed w.
- Monomial centralizer of the Harper H is `{cI,cJ}`. Thus **no** `f(H) Q P g(H)` can equal F for `4|N`, with any invertible rational scalar functions f,g and any nonzero monomial. Multiple masks/noncommuting resolvents not ruled out.
- The near-resonant counterexample has norm growth `Theta(N)` but severe covariance failure. High norm alone is not Fourier phase coherence.

## Verification
`OPENBLAS_NUM_THREADS=1 python -m unittest discover -s tests -v` from the Phase 19 directory. `OPENBLAS_NUM_THREADS=1 python audit.py > audit.json` outputs a reproducible audit record. The new deterministic suite contains 29 tests; previous Phase 12–18 suites contain 99 inherited tests. Fresh-extraction nested-lineage validation succeeded: 29 new plus 99 inherited = 128 passing tests through all Phases 12–19. Log: `phase19_full_lineage_validation.log`.

## Phase 20 next task
Investigate **symbolic shared-state noncommuting near-resonant resolvent circuits** and calculate whether the induced phase transfer operators can realize both `MT=VM` and `MV=TM` with fewer than logarithmically many O(N) stages. Include operator norm, precision/conditioning, precompute and memory movement. Keep the exact joint gate and the one-full-column calibration. Do not claim fewer operations merely because a matrix has fewer distinct coefficients, graph nodes or phase masks.
