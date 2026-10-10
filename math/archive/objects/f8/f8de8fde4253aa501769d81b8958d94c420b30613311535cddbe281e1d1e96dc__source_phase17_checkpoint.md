# BROKEN-CHAIN RECOVERY — PHASE 17 (October 9, 2026)

## User's continuing goal
An exact Fourier transform asymptotically faster than `N log N` via the original graph/Green/Haar computation-sharing idea, **not** restating OpenAI or CrocSwap and **not** presenting constant-factor savings as a breakthrough. The user repeatedly loses long conversation chains; save hard checkpoints. No such FFT has been found.

## Read these files first
1. `THEOREM.md` — FULL PROOFS, including the stronger all-length theorem and its important restrictions.
2. `product_escape_probe.py` — the first concrete surviving candidate family: **products of noncommuting Green sums**; demonstrates escaping the newly proved rank obstruction, but FAILS the Fourier covariance condition.
3. `RUN.md` and `tests/test_phase17.py` — reproduction.
4. `previous_full_phase16_checkpoint.zip` at the Phase 17 archive's top level: full Phase 16 and all earlier archives (16 includes 15; 15 includes 14; etc.).

## Main new theorem (not a universal FFT lower bound)
For any q orders, there exist two disjoint coordinate groups R,C, each size `m>=floor(N/2^q)`, separated in **every** order. This is proved by recursive two-color *median bisection*, stronger than the previous prime-only Erdős–Szekeres chain proof.

Let `A_N=Σ L_r P_r^{-1} B_r^{-1}P_r R_r`, with B_r invertible banded half-width w_r, L/R diagonal arbitrary, P independent permutations. Put W=Σw_r. The inverse-banded nullity theorem gives `rank(A[R,C]) <= W`. The normalized DFT F has Frobenius squared `m²/N` on EVERY m-by-m submatrix and spectral norm <=1, hence Fourier block rank >= m²/N. Therefore **exact equality** requires

`floor(N/2^q)^2 <= W*N`.

If `2^q | N`, necessarily `N<=4^q W`; q tridiagonal terms give `N<=q4^q`, requiring **Ω(log N)** terms. This holds for arbitrary N, complex coefficients, noncommuting and nonunitary terms, arbitrary path permutations and gauges, PROVIDED each summand uses the **same coordinate order for rows and columns**; independent row/column permutations per term are not covered. It is only a **lower bound on term count**, NOT an unconditional scalar-arithmetic lower bound if algorithms share work among terms.

Stronger: if `m0=floor(N/2^q)>W` and `m0²>W N`, any such candidate has

`||A_N-Fhat_N||_2 >= sqrt((m0²/N-W)/(m0-W))`.

For fixed q and fixed widths, asymptotic spectral-norm approximation error stays >=`2^(-q/2)`; q2 gives >=0.5 in the limit.

## Other verified Phase17 facts
- First weaker prime-only minor theorem via Chebotarev + common monotone chain: `N<=(2q+1)^(2^(q-1))` necessary for prime N; q2 impossible for primes >=29. Retained as an independent small-size control. This is NOT the main theorem now.
- Same-path-order Green terms need at least `N/2` to match a Fourier matrix's consecutive half-cut full-rank minor (valid for all even N).
- Bluestein chirp convolution cannot equal a sum of fewer than `N/2` elementary cyclic shift resolvents: exact Hankel/Vandermonde rank argument. Useful *subfamily* obstruction, not general FFT lower bound.
- Adversarial interleaving permutations attain the worst-case balanced-set size exactly: N64/q2 yields m16, N256/q3 yields m32, and N2048/q4 yields m128. This verifies sharpness of the bisection CONSTANT, not optimality of the Fourier rank bound.
- Direct two/three-path Green sums passed exact rank-obstruction certificates at various lengths including 29,31,41,67,103 and 211; direct power-of-two witnesses for 16..1024.
- Stronger all-length balanced-cut theorem independently tested in exact modular arithmetic at q2/N64, q3/N256, and q4/N2048. Analytic robust gap compared to numerical SVD at multiple sizes.
- **Surviving escape route:** `M=(G1+G2)(G3+G4)` is O(N)-apply via four Green solves and can have FULL crosscut rank, so the additive theorem cannot apply. Exact modular demonstrations: n32 additive-rank2 → product-rank9, n64 rank2 → rank17. But `MZ-DM` has FULL rank in each test. It is NOT a Fourier factorization and cannot be claimed as speedup.

## NEXT research gate: Phase 18
Investigate Fourier **phase covariance of products of sums** and shared-state DAGs, because rank growth alone has now been proven insufficient. Start with exact `MZ=DM` and appropriate diagonal/permutation masks; seek a symbolic invariant or constructive factorization, certify FULL matrix identity, then charge all solves, preprocessing, phases, and memory. DO NOT repeat entropy-optimal radix-2 folding, pure sums of bounded-bandwidth Green inverses, path-Cayley tuning, or conditional infinite-caching models.

## What's NOT proved
- No new exact FFT below `O(NlogN)` in standard scalar arithmetic.
- No lower bound on arbitrary linear circuits, arbitrary nonunitary algorithms, products of sums, or shared-state solver DAGs.
- No theorem for infinite-preprocessing/unbounded-word lookup models.
- No claim the combined Phase17 theorem is previously unknown in mathematical literature.

## Commands
`cd fft_green_phase17_nonunitary_sum`

`OPENBLAS_NUM_THREADS=1 PYTHONPATH=. python -m unittest discover -s tests -v`

`python green_sum_cert.py`

`python chirp_hankel.py`

`OPENBLAS_NUM_THREADS=1 python approximation_gap.py`

`python product_escape_probe.py`

**Checkpoint status:** strong architecture-specific exact + robust numerical no-go, surviving products-of-sums model identified, full chain preserved. No new sub-NlogN FFT.
