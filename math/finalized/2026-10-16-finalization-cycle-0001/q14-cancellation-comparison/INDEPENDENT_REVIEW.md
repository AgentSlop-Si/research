# Q14: independent review of the periodization-based prior interface

Date: 16 October 2026 UTC.

## Verdict

**ACCEPT the bounded nonmatch and its limited record update.** The selected primary result does not supply Q14's complete light-fiber recognition and rejection interface. A two-mode witness defeats the candidate substitution before any numerical or implementation question arises. This is a precise new comparison outcome; it is not a closure of full-interface historical priority, a new Fourier lower bound, or a repeat of the accepted bounded N15 and conservative dyadic implementations.

Final author report reviewed: *Q14: exact intermediate-fiber recognition versus cancellation-pruned recovery*, SHA-256 4d371bab6b022702240b9e1c13d1c3074aa325b97c7c8c6167cd63afe901f9d9. Its storage accounting, positive-threshold semantics, exact sparsity versus cap distinction, and M≥8 witness were checked. A separate local-only proposal review verifies two exact current-cell preimages and preservation of all preceding text. No external update was performed by this reviewer.

## Independently read sources

Primary: G. Plonka and T. von Wulffen, *Deterministic Sparse Sublinear FFT with Improved Numerical Stability*, Results in Mathematics 76, article 53 (2021), [DOI](https://doi.org/10.1007/s00025-020-01330-0), [publisher PDF](https://link.springer.com/content/pdf/10.1007/s00025-020-01330-0.pdf). Theorem 2.1 and equation (2), printed p.3; Remark 2.2, p.5; Algorithm 3.1, pp.6–7.

The source studies complex dyadic vectors and significant entries defined by a positive threshold. Its multiscale recovery requires significant coefficients to survive every periodization. Theorem 2.1 recovers a finer level under that condition and an invertible restricted matrix. Algorithm 3.1 returns a zero vector when the zeroth Fourier datum falls below the threshold. Remark 2.2 discusses a cancellation repair when exact sparsity is known: direct transforms continue until cancellation disappears, potentially reaching ordinary FFT cost. These are the source facts used below; the counterexample and wrapper analysis are independent deductions.

Project target: *Certified growing-fiber Fourier theory*, sections 1–9 and 11, SHA-256 a5c0da63f7761f91c26cf7662afb0ba5f7874f330db36791addde9bf6c58f045. Prior comparison report SHA-256 81e92e015531708938576ade41cc043e9f2c92a06b8be865c26fbf9a71e46b4a; independent STR-Q5 repair review SHA-256 787960e75967cc6e2bec564bdd72a92fc937ad853a4611408e430442eb002ff9. The latter already accepts the different conservative tree-recognition route; it is not new evidence from this pass.

## Exact orientation and witness

Use the target's allowed complex specialization N=M², Q=M, M=2^ell≥8, and supplied root w=exp(2πi/N). Put eta=w^Q. A fiber is

    y_t[u] = sum_h a_(t,h) eta^(-hu).

Thus the source's unknown sparse vector is a_t and its available negative-sign Fourier data are exactly y_t. This mapping needs no transformed-input oracle: datum u is the saved raw coordinate x[t+Qu]. The choice of one valid root is enough to test a purported universal plug-in; no conversion from an arbitrary primitive-root encoding is being assumed.

For one fiber set

    a[0]=1, a[M/2]=-1, and all other a[h]=0.

Then

    y[u]=1-(-1)^u.

Its exact support is two. At every proper periodization length 2^j, j<ell, the two indices coincide modulo 2^j and their amplitudes sum to zero. Hence every such periodization is identically zero, including the penultimate one. The raw data are not zero: y[1]=2.

Choose any 0<epsilon<1. Both nonzero coefficients are significant, while y[0]=0. The displayed source initialization therefore returns a zero candidate immediately. This is an off-promise input to the source, not a counterexample to its theorem. We do not replace epsilon by zero: the published strict comparison would then have different behavior and would require a new exact algorithm specification.

The original Q14 recognizer must accept this fiber whenever 2≤b≤M/2. A complete raw comparison rejects the source's zero candidate, since at least y[1] differs. That comparison establishes candidate failure, but cannot establish support greater than b. The implication

    failed light call ⇒ actual support ≥b+1

is false for this proposed substitution. A timeout, exception, matrix guard, or numerical threshold cannot repair that missing completeness implication.

## Aggregate charging obstruction

Repeat this exact fiber in all Q=M fibers and choose K0=2Q. Every fiber has support two and the total support is exactly K0, so this is an accepted Q14 aggregate input. For M≥16 its target threshold is

    B=min(M/2, 2 log2 M) ≥ 2.

If each failed comparison is followed by an ordinary M-point transform, all Q fibers require that recovery branch, although none is genuinely heavy. The valid F015 bound floor(K0/(B+1)) on successful heavy recoveries is strictly smaller than Q. The additional final over-budget-fiber allowance is irrelevant: this input never exceeds K0.

Even granting the source exact sparsity two, which is more information than a cap B, its stated cancellation-repair route reaches the final level on this witness. A literal serial use of ordinary M-point recovery in all Q fibers pays Θ(Q M log M)=Θ(N log N) under the ordinary radix implementation. This is a cost of that specified repair path. It is not a lower bound on recovering this simple witness, on modified sparse algorithms, or on Fourier circuits.

## Complete interface ledger

1. **Input and construction.** Read and retain the validated original N-vector; a fiber coordinate is an indexed read x[t+Qu]. This costs O(N) total input storage/read preparation, plus all repeated accesses made by attempts. If Green residuals are used, form the specified residual in O(N) and retain the original for any global fallback. No previously transformed vector or support list is supplied.
2. **Every attempt.** All source queries, periodizations, restricted-system setup/solves, comparisons, allocations and emitted candidates must be charged, including failed attempts. Its promise-domain discovery cost cannot be extended to arbitrary Q14 fibers merely by naming a budget.
3. **Certification.** Validate bounded explicit integer indices and amplitudes, normalize the Fourier convention, then use the accepted pruned synthesis and compare all M raw coordinates. This charges O(M log(b+2)) per bounded attempt, including an O(M) zero-candidate scan. It gives soundness, but the witness proves completeness remains missing.
4. **Denominators and Green closure.** A source-system invertibility condition is not a substitute for Q14's own local guards. In Q14's cyclic solve check each d_j before division and the closure denominator 1−product_j(-beta/d_j). Guard refusal is a domain outcome, never evidence of a heavy fiber. A valid matrix elsewhere does not imply any of these denominators are nonzero. Their O(N) preparation/check/solve work remains charged.
5. **Aggregate accounting.** Failed attempts are not free. Without the missing complete recognition theorem, the number of resulting ordinary transforms is at most Q, rather than the support-amortized F015 bound. The source's exact-known-sparsity premise cannot be replaced silently by an upper bound B.
6. **Fallback and errors.** A separately selected full transform of the saved original input preserves correctness after a valid refusal and pays its full O(N log N) work. A residual cannot be mistaken for that original input. Malformed data, unhandled exceptions and resource failures are not mathematical support certificates and must not silently become accepted fallback behavior.
7. **Output.** A recovered sparse fiber list is an intermediate object. On successful Q14 recognition, retain the established identity X[h+Mv]=M sum_t a_(t,h) w^(ht) theta^(vt), its phases and residue grouping, and all N explicit output writes. Their accepted bound is O(N+K+Q sum_h log(kappa_h+1)). None is supplied at zero cost by the candidate source.
8. **Storage.** The retained Q14 arrays and bounded mode records require O(N) words. A serial wrapper can reserve only one current fiber and bounded solve workspace; every allocation still needs a specified bound. A runtime statement or sparse output alone does not certify storage, precision or arbitrary-coefficient representation costs. This review makes no new implementation-space claim for the unbuilt substitution.

These checks locate a decisive first failure without pretending to have implemented or benchmarked the candidate. Full raw verification and paid fallback are available correctness repairs; neither restores the promised acceptance class and its aggregate cost.

## Disposition

Record the new named source and explicit cancellation/refusal mismatch as a bounded completed comparison. Retain the existing Q14 and STR-Q5 parent gates, the F015 proof status, the accepted N15 and dyadic milestones, and all historical counts/ranks. This pass establishes neither worldwide novelty nor a numerical-stability, finite-word, arbitrary-length binning or production theorem. No secondary prior-art comparison is included in this verdict.

Review method: independent publisher HTML/PDF text reads, original project-theorem and prior-review reads, exact symbolic deductions. No supplied program was executed, no software was installed, and no external state was changed. Publisher screenshot retrieval was unavailable; the theorem and algorithm were checked in the independently retrieved PDF text instead. A retained retrieval-response hash identifies a local capture, not publisher PDF bytes.
