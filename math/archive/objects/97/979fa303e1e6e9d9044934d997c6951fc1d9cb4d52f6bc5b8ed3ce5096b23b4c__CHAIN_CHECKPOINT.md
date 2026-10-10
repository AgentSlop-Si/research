# HERO #17 — RECOVER HERE: Phase 12, Green–Union rank-sparsity gate

**2026-10-10, exact restricted result.** **NO universal O(N) FFT.** Previous branch: Phase 11 `fft_hero17_phase11_lazy_union_green_rank_gate_2026-10-10.zip` and independent Green Phase 23.

## New exact theorem

If `F_N = H_L ... H_1`, with all factors invertible, `H_i=G_i+R_i`, rank(R_i)<=r_i, and the inverse of `G_i` having <=s_i nonzeros per column, then with `r=sum r_i`, `s=prod s_i`:

- General N over complex scalars: `s(r+1)^2 >= N`.
- Prime N over complex scalars: `(s+1)(r+1) >= N+1`.

For monomially gauged/permuted one-pole Green stages, `s<=2^L` regardless of long-range shift or noncommutation. This **extends** the plain Green inverse-sparsity restriction in earlier Phase23 to low-rank corrections inserted at ANY stage. The proof is three steps: inverse rank perturbation, telescoping rank of products, and Fourier uncertainty applied to an (r+1)-supported kernel vector.

## Quantum/Weyl anti-shortcut

`TS=omega ST`, `G_S=(I-alpha S)^-1`, `G_T=(I-beta T)^-1`. Then `rank([G_S,G_T])=N` for invertible factors and alpha,beta!=0. But the inverse of their product is 2-sparse per column; the new rank bound survives maximal noncommutativity. A FULL 65,536-vector Green pair was executed/checked against its exact recurrence, 18 direct dense-kernel rows, and four nonmatching DFT bins. Do not call it a faster Fourier transform.

## Positive scoped fusion

For every K|N: `(1/K) sum_{j<K} U^j (I-alpha*S)^-1 U^(-j) = (I-alpha^K*S^K)^-1` with U the Kth-root modulation. This fuses K independent dense Green passes into one O(N) long-range solve for every input. Exact full-output check N=65,536 K=16 passed. **But the result is another sparse-inverse Green operator, not an FFT.**

## Reproduction

From the package directory:

`python -m unittest -v test_phase12`

`python independent_audit.py`

`python large_green_audit.py`

Read `PROOF_CERTIFICATE.md` and `RESEARCH.md`. Exact certificates in `AUDIT_RESULTS.json` and `LARGE_AUDIT_RESULTS.json`; 14 new test groups and 45 predecessor test groups passed.

## The STOP list

- Old dyadic quotient lazy refinement: already an FFT, N log N.
- Ordinary Green product inverse column sparsity: Phase23 already identified; do not relabel as new.
- Rank alone is NOT a complexity lower bound; high-rank corrections can be cheap.
- Weyl/Gaussian quantum noncommutativity is not evidence of an O(N) DFT.
- Bluestein chirp: known D C D identity; its circulant must still be evaluated.
- Product-of-Green-plus-low-rank circuits: necessary tradeoff now established; don't spend cycles randomly searching shallow variants contradicted by inequality.
- Finite-field full-spark cert n<=7 does NOT prove prime complex rank bound from finite-field samples; that proof uses Chebotarev/Tao.

## Phase 13 target

Go OUTSIDE the certified model: multi-branch **sums of independently structured Green paths**, noninvertible overlapping stages, or globally joint evaluators of high-support inverse kernels. Must produce a valid sequential arithmetic schedule for arbitrary fresh x and every Fourier output, with all costs charged. Test every basis vector and random/adversarial dense inputs. Avoid #130/CrocSwap/Swapnil-style rediscovery; treat external published result as benchmark only.
