# ALG-007: common-support interpolation comparison

16 October 2026 UTC. Stable owner: **ALG-007, Raw sparse global-phase support recognition**. This report completes its selected primary-source comparison. It does **not** close the parent record: the separately recorded compatible-model fallback implementation obligation remains open at priority 42.

## Result

After the fixed block chirp is removed, ALG-007 is exactly a vector-valued sparse polynomial sampled on a known root-of-unity grid. Its common-support annihilator is the classical block-Prony object. The selected published common-support theorem matches that algebra, but does not establish the complete ALG-007 raw-input recognizer, negative-instance ledger, finite-field implementation or all-output Green bank. This is a qualified nonmatch of the full package, not a novelty or priority claim.

The accepted scoped correctness review is preserved. No historical program was executed or imported, and no optimized implementation, floating stability, bit-cost advantage or unrestricted FFT result is certified here.

## 1. Primary result and source boundary

The selected formal result is **Barbotin, Hormati, Rangan and Vetterli, _Estimation of Sparse MIMO Channels with Common Support_, arXiv:1107.1339v1, §II.B, Proposition 1, supported by Lemma 1 and equations (4)–(8)**. The [primary manuscript](https://arxiv.org/pdf/1107.1339v1) presents a common annihilating filter for noiseless complex channels with distinct shared delay nodes. Its block-Prony construction stacks channel equations; its recovery procedures use an estimated path count, numerical TLS/SVD and subsequent Vandermonde solves. The published version is [IEEE Transactions on Communications 60(12), 3705–3716 (2012)](https://doi.org/10.1109/TCOMM.2012.091112.110439). We use only the noiseless algebraic proposition, not the statistical model, numerical recovery guarantees or Proposition 2's rank argument. Forward and reciprocal characteristic polynomials are distinguished below rather than silently inheriting the filter-root convention.

For the polynomial terminology, **van der Hoeven and Lecerf, _Sparse polynomial interpolation: Faster strategies over finite fields_, final version 2 May 2024**, explicitly discusses vector coefficients in §3.2. Its §5 Algorithm 4 connects geometric samples, rational generating functions, Padé recovery, roots and exponents. That input includes a polynomial black box, degree/sparsity bounds and suitable evaluation capabilities; root finding and discrete logarithms retain their costs. We do not treat a coefficient vector space as a field or inherit scalar-operation counts, probabilistic bounds or heuristic assumptions as unconditional ALG-007 bounds. [Primary text](https://www.texmacs.org/joris/ffsparse/ffsparse.pdf)

These are source-specific comparisons. They do not constitute an exhaustive literature search.

## 2. Pinned original and governing accepted scope

The recovered original archive is `fft_hero0_phase6_sparse_phase_support_2026-10-10.zip`, 94,306 bytes, SHA-256 `0eda6f3c099d736e3ee2439c531cdfcc6b83f672ea3a2ff9dcb5afeda5d4cd5e`. Its original `THEOREMS.md` is SHA-256 `9ac946c12d23bf47aa90c577a4d800420d3a6dec85dd6734b2e198caf29db273`. The archive identity matches the prior audit. All 22 entries of its supplied hash manifest were checked without running them. The theorem body, especially §§1–3, was read as data.

The governing corrected audit is pinned at repository commit `8172ebf0371ef83a6c5aaa2de778358c89088b22`:

- [Phase6 audit](https://github.com/AgentSlop-Si/research/blob/8172ebf0371ef83a6c5aaa2de778358c89088b22/math/archive/objects/f8/f8a630d61c469188c1c33a1e5fcd57b0cc39ea251fff78aba08b2cc7c7e29f3a__f8a630d61c469188c1c33a1e5fcd57b0cc39ea251fff78aba08b2cc7c7e29f3a__PHASE6_SPARSE_SUPPORT_AUDIT.md). Original identity `f8a630…`; the documented sanitized export actually read has SHA-256 `65a7d9cdc728cf62725bd03344b814bf8e1f37b9dec04b52ebfcfe083b6bfc6d`. The two hashes are not interchangeable.
- [Integrated result, §2](https://github.com/AgentSlop-Si/research/blob/8172ebf0371ef83a6c5aaa2de778358c89088b22/math/archive/objects/2d/2d2a67a3ec1f72c32ac39b54ce853048a195e0b90ddf2543fd8d5f83c34794ae__2d2a67a3ec1f72c32ac39b54ce853048a195e0b90ddf2543fd8d5f83c34794ae__INTEGRATED_RESULTS.md), SHA-256 `2d2a67a3ec1f72c32ac39b54ce853048a195e0b90ddf2543fd8d5f83c34794ae`.

Corrections in that accepted audit control over the original prose's broader implementation wording. In particular, the shipped path returns rejection and does not execute its claimed ordinary-FFT fallback. Seed additions and setup cannot be removed from the ledger.

## 3. Exact hypothesis and formula map

Use the owner's symbols: Q=KM is even, K≥M≥2; a is a supplied unit modulo Q; β and the factorization are fixed/supplied; ζ is a supplied primitive Qth root in a field F with characteristic not dividing 2Q. Define ξ=ζ^K and, for 0≤b<K and 0≤t<M,

    s[b,t] = ζ^(a t(t−1)/2 + (aMb+β)t)
    y_b(t) = s[b,t] x[bM+t]
    D[b,j] = Σ_(t=0)^(M−1) y_b(t) ξ^(jt).

The raw input is x, not D, a support set, an oracle or synthesized sparse examples. Its analysis coordinates obey

    y_b(t) = Σ_(j∈S) c[b,j] z_j^t,
    c[b,j] = D[b,j]/M,    z_j=ξ^(−j),
    S={j : D[:,j] is a nonzero vector}.

Equivalently, P_b(Z)=Σ_(j∈S)c[b,j]Z^j has degree <M and y_b(t)=P_b(ξ^(−t)). The vector polynomial P=(P_0,…,P_(K−1)) has union support S and r=|S|. Each fixed-support space has Kr free scalar coefficients, not r. A block may omit any subset of the global modes, and a mode may first appear in the last block.

In the complex specialization, the manuscript's channel count corresponds to K, its path count to r, and its distinct unit-circle nodes to z_j. The dechirped within-block sample index corresponds to the spectral sample index. This is **not** an assertion that the raw flattened x itself has order-r ordinary recurrence. Its ordinary Hankel rank may be maximal.

### Joint annihilator, with zero coefficients handled

Let A(Z)=∏_(j∈S)(Z−z_j)=Σ_(ℓ=0)^r A_ℓZ^ℓ, A_r=1. Direct substitution yields

    Σ_(ℓ=0)^r A_ℓ y_b(t+ℓ)=0    for every b,t.

Extend each row periodically modulo M. This extension is determined by the full known M-grid, because all nodes have order dividing M; repeated grid samples are legitimate. Therefore r>M/2 is not, by itself, a sample-availability obstruction.

For minimality, if a scalar polynomial B annihilates every row for all t, the first r equations give V_r·(c[b,j]B(z_j))_j=0. The Vandermonde V_r is invertible. Hence c[b,j]B(z_j)=0 for every b,j. For each j∈S some c[b,j]≠0, forcing B(z_j)=0. Thus the least common annihilator is exactly A, although an individual block can have smaller minimal degree. This proof uses field arithmetic in F and does not divide coefficient vectors.

The rational sequence form is Σ_(t≥0)y_b(t)u^t=Σ_(j∈S)c[b,j]/(1−z_ju). Its joint denominator is q(u)=∏_(j∈S)(1−z_ju); its roots are z_j^(−1), whereas A's roots are z_j. A fixed scalar projection of P can erase a mode: c[:,j]=(1,−1,0,…,0) is nonzero although its coordinate sum vanishes. No free support-preserving scalar projection is assumed.

## 4. Discovery, verification, rejection and full-output costs

### What the primary algebra supplies

The mapped shared-annihilator equations supply a classical support-recovery mechanism. They do not replace raw membership validation. For a completely explicit cost comparison, one can apply the scalar construction separately to the K rows and take the union, without assuming any block contains all modes.

Here is a deliberately nonoptimized **derived comparator**, not a claim about the published numerical implementation. For a chosen cap 1≤R≤M, form each R×R Hankel matrix from cyclically indexed moments y_b(0),…,y_b(2R−1). Under support ≤R its rank is t_b, and its leading t_b×t_b moment matrix is nonsingular by Vandermonde factorization. Gaussian rank and recurrence solves cost O(R³). Scan the M known grid nodes against the recurrence in O(MR), recover amplitudes with a Vandermonde solve, and reconstruct all M entries exactly. Reject singular/unusable candidates, non-grid or wrong root counts, failed raw reconstruction, or a union exceeding R. Every true union-support ≤R input passes; a false short candidate cannot survive the complete reconstruction. R=0 is the direct all-zero test.

Consequently the derived bounded recognition attempt costs O(Q+KR³+QR) field operations, including dechirping, root tables and full certificates, with O(Q+R²)=O(Q) field words under K≥M. The cost applies to negative instances as well. It is an elementary paid comparison, not a better replacement for the accepted adaptive recognizer; no executable fallback is thereby supplied.

### What ALG-007 additionally supplies and must pay

The original adaptive method maintains the discovered union. Each failed restricted block certificate triggers a full short transform which reveals a new mode. The accepted corrected bounds remain:

- Accepted support r: O(Q+rQ+rK log K+(r+1)M log M).
- Cap-R rejection, before decoding: O(Q+RQ+(R+1)M log M).
- At most r full short discoveries on acceptance and R+1 before rejection.
- O(Q) field-word storage and every raw coordinate checked.

These statements assume suitable short-transform backends in the declared model; no arbitrary-length backend follows merely from supplying ζ. If only the abstract field/root is supplied, write the accepted ledger as O(Q+rQ+r T(K)+(r+1)T(M)), and rejection as O(Q+RQ+(R+1)T(M)), with each backend cost T(n) separately justified. The dyadic fixed-field executable is narrower than the even-composite identity.

After discovery, the **full output** is

    F_Q x = (1/M) Σ_(j∈S) F_Q P_jx,
    (P_jx)[bM+t]=s[b,t]^(−1) ξ^(−jt)D[b,j].

For mode j, use β_j=β+jK. Its K-transform B_j forces the Green equation

    Y_j[k]−ζ^(−k−β_j)Y_j[k+a]
      = B_j[k mod K]
        −ζ^(−M(k+β_j)−aM(M−1)/2)B_j[(k+aM) mod K].

The gauge g_j(h)=ζ^(a h(h−1)/2+β_jh) has g_j(Q)=−1. This is where even Q, a unit (hence odd), and invertibility of 2 enter the decoder. The block-Prony algebra does not supply this Q-cycle solution. All r K-transforms, r Q-scans, seed sums, normalization, accumulation and Q writes remain paid; at least r(Q−1) omitted seed additions must be restored to the old operation proxy. Attaching the same bank to the derived comparator gives O(Q+KR³+QR+rQ+rK log K), plus separately declared scalar inversions/backend setup.

The supplied factorization, chirp and root are prerequisites; finding favorable ones, field extensions and growing parameter searches are additional work. M=Θ(log Q) is an eligible-factorization specialization, not free padding for every Q. The full r=M bank has the known ordinary-FFT algebraic endpoint and gives no sub-FFT guarantee; the literal r-fold scan ledger must still be charged and can be larger for other M. Exact finite-field equalities do not prove floating support certification, finite-bit complexity or hardware speed.

### Fallback remains a real implementation obligation

If a compatible exact full-transform backend is separately admitted, a wrapper pays C_reject(Q,R)+C_fallback(Q) on rejection. Neither a primary interpolation theorem nor an O(Q log Q) prose label constructs that backend in every field/length model. The original source's fallback claim was corrected to rejection-only by the accepted audit. This comparison has not installed or executed a wrapper.

## 5. Verification and owner disposition

The newly authored `check_common_support.py` uses only the Python standard library. It checks the new comparison identities, not previously accepted Green/recognition gates. Its 81 finite cases span Q=4,12,16,24,32,48,64 and exact prime fields; all 81 joint-rank checks, 4,776 recurrence-coordinate checks and 2,388 dechirped-coordinate checks pass. Zero, disjoint, late and full support, periodic extension, scalar-projection cancellation and reciprocal-root orientation are included. These finite controls illustrate the independent algebra above; they are not asymptotic, production or numerical certificates.

The live owner was resolved by stable ID in all three views. Its current one-primary-comparison pass/stop condition is met by the explicit map and qualified nonmatch. However, Catalogue X still explicitly lists a remaining compatible-field/length fallback implementation/charging obligation. The newer comparison scope says implementation repairs are separate; it does not document their discharge or transfer. Therefore:

- **Comparison: complete, qualified nonmatch of the entire package.**
- **ALG-007 parent: TO RESEARCH, priority 42 unchanged.**
- **Remaining owned work: implement and charge the compatible-model rejection/fallback wrapper, or establish its specific source/interface blocker.**
- No new stable ID, no additional discovery, no closure-count change, and no worldwide-priority conclusion.

The wider cross-mode contraction, growing chirp search, floating stability and unrestricted FFT questions are preserved as limitations/separate work; this report launches none of them. The guarded native proposal changes only current action/stop/completion overlays, with prior text preserved verbatim. It does not change formulas, notes, accepted proof statements, priorities or source histories.
