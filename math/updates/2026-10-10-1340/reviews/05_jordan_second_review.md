# Phase 22 Jordan-jet construction: second mathematical review

Date: 10 October 2026.

## Verdict

**Pass, with the qualifications stated in the reviewed audit.** No counterexample or remaining substantive error was found in its scoped full/interval jet identities, bounded-order raw-input recognition theorem, arithmetic upper bound, or corrected finite-field representability count.

This verdict applies to `PROOF_AUDIT.md` with SHA-256 `d5319a2983e1e23a15ed94b3783fcb0bb434731aa9be578c3e5439f2c7575903`. The earlier audit version `50ebc18b9d4a45fbbd1272e34dcd45eaaebad9ae5fb476a63030bede20a06a6f` lacked the now-added factorial qualification. The uploaded source archive has SHA-256 `fb61f3e27dedda64c71adb56e335021c2e9809c7575bfa7db588848339e20668`.

The result remains a restricted-input exact field-arithmetic theorem. It is not a universal exact linear-time DFT, a bit-complexity bound, a numerical-stability result, a verified implementation-wide benchmark, or a historical-priority determination.

## Mathematical checks

1. **Kernel and polynomial identities.** Since N is odd, eta primitive of order 2N implies eta^8 has order N. Thus every kernel denominator through t=N-1 is nonzero. The ratio `(1-q^t)h_t = eta^(4t-2)h_(t-1)` proves the full identity by coefficient comparison. The upper endpoint coefficient is `eta^(4N-2)=eta^(-2)`. On `[a,b)`, the missing lower coefficient and excess upper coefficient give exactly the displayed lower positive and upper negative polynomial corrections. After solving for the k+8 spectral value their signs reverse as stated.

2. **Jets and parity recurrences.** The Euler operator obeys `D^j(zf)=z(D+1)^j f`. This gives the binomial coupling and the endpoint factors a^j and b^j, including j=0 with 0^0=1. Addition by 4 modulo 2N has two cycles of length N. Two seeds per cycle suffice: at each new step the same-degree middle value is already known, and all lower-degree values were computed earlier. Preparing coefficients, root powers, kernel values, seeds, binomial coefficients, and output leaves the claimed `O(N(d+1)^2)` bound intact. The source's interval expression `O(Nd^2+d(b-a))` should be read with d+1 in place of d when degree zero is allowed; the audited bound already uses d+1.

3. **Positive-characteristic generating functions.** The binomial recurrence needs no factorial inverses. Its exponential-generating-function reformulation does: in positive characteristic p it requires d<p. This is automatic when d<R and 2R<=N<p, but it is not automatic for unrestricted jet degree. This second review raised the point, and the reviewed audit incorporates it explicitly.

4. **Hankel nonsingularity.** For exact orders r_i and nonzero leading coefficients, expanding P_i(t+s) gives `H=V M V^T`, with columns `t^j u_i^t`. Within each block, the anti-diagonal coefficients are the leading polynomial coefficient times `binom(r_i-1,j)`, and all entries beyond that anti-diagonal vanish. The characteristic hypothesis makes those anti-diagonal factors nonzero. Changing ordinary powers t^j to falling factorials gives the usual confluent Vandermonde matrix, with nonzero determinant for distinct nonzero u_i and characteristic greater than R. Therefore the leading R-square Hankel matrix is nonsingular.

5. **Recognition and cost.** With a supplied cap Rmax and 2Rmax<=N, the first 2Rmax normalized samples identify the minimal recurrence on the promised family. The 2N-root scan is charged, rather than supplied as an oracle. Horner evaluation over that grid costs O(NRmax); successful repeated linear-factor deflations cost at most O(Rmax^2). Standard recurrence recovery costs O(Rmax^2), a confluent linear solve costs O(Rmax^3), and generation plus rechecking of all raw entries costs O(NRmax). Jet generation dominates at `O(NRmax^2+Rmax^3)`. The shorthand R denotes the configured bound in a blind-recognition cost claim; no unknown order is provided by an oracle. Multiplication by each grid mode shifts the spectral index, and ordinary N-point outputs are the even indices.

6. **Piecewise scope.** Full segment verification and a genuine partition ensure sound accepted outputs. They do not ensure that the greedy recognition procedure accepts every vector having a small-piece representation. For a concrete example, take N=7, p=29, eta=4, Rmax=1, and normalized data `(1,2,2,2,2,2,2)`. This has two order-one constant pieces `[0,1)` and `[1,7)`. But fitting the first two samples demands geometric ratio 2, which is outside the order-14 grid because `2^14=-1 mod 29`. The specified greedy first fit therefore rejects. This is a mathematical example for the described algorithm, not a run of the submitted implementation.

## Finite-field counting correction

A finite union of proper linear subspaces can cover a finite vector space; subspace dimensions alone cannot establish the claimed properness. The audited replacement is valid. For at most s nonempty pieces with per-piece order at most R and no literal tail, the represented proportion in F_p^N is at most

    min(1, sum_(j=1)^s binom(N-1,j-1) binom(2N+R,R)^j p^(jR-N)).

There are `binom(N-1,j-1)` interval partitions and at most `binom(2N+R,R)` root-multiplicity choices per piece. Each fixed description has at most p^(jR) outputs. Multiplication by the nonzero kernel is invertible, so the same count applies to raw inputs. Duplicate descriptions and dimension losses only make this bound looser.

For fixed s and R, once N>sR the exponent jR-N is negative. With p>=2N+1, each summand is at most a polynomial in N times `(2N+1)^(jR-N)`, and the sum tends to zero. The bound establishes properness when it is strictly below one, not from jR<N alone. A literal tail needs separate counting of its free coefficients and possible locations. This is a representability estimate, not an unrestricted Fourier lower bound.

## Independently authored exact controls

[second_review_controls.py](../controls/jordan_second/second_review_controls.py) was newly written for this review. It neither imports nor executes the uploaded programs or the first review's verifier. Across nine odd lengths and compatible prime fields, all checks pass:

- 50,440 coefficient entries in full and every nonempty interval polynomial identities
- 94,840 direct-sum spectral recurrence checks
- 405 blind Berlekamp–Massey/grid-factor/amplitude reconstructions
- 405 full-verification rejections of altered suffixes with unchanged recognition prefixes
- 3 off-grid geometric-mode rejections
- 4,545 reconstructed ordinary N-point bins
- 2 small exhaustive representability counts

These counts are independent new controls, not reproduction of the uploaded regression tests or performance ledgers. Small finite tests corroborate the proof; they do not replace it or certify every implementation path.

## Provenance, benchmarks, and review limits

All entries of the first review's manifest and all 17 listed source-text hashes match the materialized files. The ordinary N-point count pairs for N=6,561, 59,049, and 177,147 agree with the uploaded JSON: respectively 295,345 versus 181,578; 2,657,323 versus 2,027,424; and 7,971,747 versus 6,672,626. This is a static transcription check. Neither source programs nor their operation counters were rerun. The reported padded-task crossover is a different 2N-output workload and establishes no ordinary N-point crossover.

The first audit's prior-art checks are explicitly limited to the cited q-holonomic abstracts and the Peter–Plonka introduction/scope discussion. This second review does not expand them into a full-text priority search. It also does not independently audit the external Math 130 result or certify an all-length fast fallback.

The original uploaded source and the first audit's verifier/results remain unmodified by this reviewer. No remote mutation or publication was performed. The accompanying [SECOND_REVIEW_RECEIPT.json](../receipts/JORDAN_SECOND_REVIEW_RECEIPT.json) records the reviewed bytes and this deliverable's hashes.
