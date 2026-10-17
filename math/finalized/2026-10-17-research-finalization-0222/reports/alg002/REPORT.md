# ALG002 publication worthiness assessment

17 October 2026 UTC. Record: ALG-002, Aggregate-budget fiber recognition.

## Decision

**Retain as a mathematically useful exact structured-input algorithm; do not promote to a standalone new-algorithm publication on the present evidence.** The proof supports a complete recognition and evaluation contract. The elementary identities are established ingredients, and the broad complex-arithmetic polylogarithmic-budget headline already has an accepted prior-method composition in the project. The remaining possible contribution is the sharper complete finite-parameter interface over a supplied-root field, with adversarial rejection accounting. Its external priority and application value are unestablished.

This assessment completes one new named-source comparison: Arnold, Giesbrecht and Roche, *Sparse interpolation over finite fields via low-order roots of unity*. It is a qualified interface nonmatch, not evidence of worldwide novelty. ALG-002 remains open. No numeric novelty score or status change is proposed.

## Source and review scope

The authoritative record was read from the open index at repository commit `e3f3fd2fde808e577989907f00740c16905dbeb1`. Its current gate requests an exact primary-theorem comparison of Section 9, including raw input, total budget, full output, roots, negative instances and the last heavy fiber.

The actual proof body read was [F015 original theory](https://github.com/AgentSlop-Si/research/blob/e3f3fd2fde808e577989907f00740c16905dbeb1/math/archive/objects/a5/a5c0da63f7761f91c26cf7662afb0ba5f7874f330db36791addde9bf6c58f045__F015-original-theory.md), especially Sections 1–9 and 11–14. Its saved UTF-8 bytes have SHA-256 `a5c0da63f7761f91c26cf7662afb0ba5f7874f330db36791addde9bf6c58f045`.

Two historical reports were also read to avoid repeating completed work: the independent 13 October F015 solver review, and the 16 October Q14 Plonka–von Wulffen cancellation comparison. They are copied into `evidence/` with source hashes in the manifest. Their accepted claims are historical evidence, not newly certified implementation results. The Plonka comparison is not redispatched here. ALG-063, ALG-064 and C03 were excluded.

This is a proof-and-interface appraisal. The original research implementation and external algorithms were not run. Fresh self-contained modular and integer controls were authored separately; they do not establish asymptotic results by testing.

## What the proof actually establishes

Let N=2^k≥4, Q=2^floor(k/2), M=N/Q. The field has characteristic not dividing N and a supplied primitive Nth root w. Every raw fiber y_t[u]=x[t+Qu] has a unique expansion in M characters, with r_t nonzero coefficients and total K=sum r_t. Root construction, arbitrary-precision costs and numerical recognition are outside the model.

The cap recognizer with b≤M/2 takes a 2b prefix, recovers a recurrence, evaluates its polynomial on the entire root grid, recovers amplitudes, and then compares every original fiber coordinate with a pruned reconstruction. The last step is indispensable. A fitting prefix alone cannot certify arbitrary raw data.

The determinant argument is sound: for a genuine r-mode fiber, its r by r Hankel matrix factors as V diag(a) V^T. Distinct nodes and nonzero amplitudes make it nonsingular over the supplied field. Thus the recurrence is determined from 2r samples even when initial samples cancel. At a reciprocal node z_h=eta^h, the rational generating function gives a_h=−lambda_h A(z_h)/C′(z_h); distinct roots make its denominator nonzero.

The final identity is

    F_w(x)[h+Mv] = M sum_t a[t,h] w^(ht) theta^(vt),
    eta=w^Q, theta=w^M.

Pruned synthesis and concavity give the cap cost O(N log(b+2)+Qb²), including discovery, all raw comparisons and all N outputs. This is a valid upper-bound composition in the exact field/word model, not an arithmetic lower bound for competing methods.

For the aggregate variant, ell=log2 M, a=max(1,ceil(K0/Q)) and B=min(M/2,a ell). Each failed *complete* light recognizer implies r_t>B. Full transforms before budget overflow therefore consume at least B+1 actual modes each. On rejection only the final processed fiber can exceed the remaining budget. Consequently heavy transforms are bounded by floor(K0/(B+1)) on success and that quantity plus one on rejection.

The resulting all-input success-or-rejection bound is

    O(N log(B+2)+QB²+M ell(1+K0/B)+N log(1+K0/M)).

When K0=O(Q log^c N), fixed c≥0, the unsaturated regime eventually applies and yields O_c(N log log N). The finite-size bound remains necessary when B=M/2. For K0=0, even the first nonzero heavy fiber can require the extra transform; deleting the +1 would invalidate the ledger. A numerical failure, incorrect candidate or incomplete solver refusal is not a heaviness certificate.

I found no blocking mathematical defect in these inspected derivations. That is narrower than a fresh verification of all implementation and historical acceptance claims.

## New primary source comparison

Arnold–Giesbrecht–Roche [arXiv:1401.4744v2](https://arxiv.org/pdf/1401.4744v2), Theorem 1.1, takes a division-free straight-line program of length L for an unknown finite-field polynomial, with degree bound D and term bound T. It returns the sparse polynomial with probability at least 1−epsilon in soft-O(LT log²D (log D+log q) log(1/epsilon)) bit operations. Section 2 computes polynomial images by executing that program in extension rings; Section 6 states the probabilistic recovery algorithm. These are not fixed-grid array reads.

For one ALG-002 fiber the natural unknown is f(z)=sum_h a_h z^h, D=M−1, T=B, with available values f(eta^(−u))=y[u]. No short program for f is supplied. The theorem therefore cannot directly replace the light recognizer. Furthermore its probabilistic guarantee does not give deterministic completeness on every light input; exact candidate checking repairs soundness, not that implication. Its finite-field bit bound also cannot be read as an arbitrary-field unit-cost bound. This is a qualified contract nonmatch, not a refutation or a lower bound on possible adaptations.

## Why the missing input interface is substantive

The following elementary derivation is an audit aid, not a novelty claim. Invert the M-point transform to write the degree-less-than-M polynomial at a scalar z:

    f(z) = (1/M) sum_u y[u] sum_(h=0)^(M−1) (z eta^u)^h.

When z^M≠1, the inner coefficient is (1−z^M)/(1−z eta^u), and every one is nonzero. Thus unrestricted off-grid evaluation depends on every raw coordinate. It cannot be identified with a single available array entry. This says neither that preprocessing is impossible nor that promised sparsity cannot help; it says that a new conversion/evaluation construction and its cost must be supplied. The extension-ring images require their own explicit simulation as well.

A safe but unhelpful bridge is to recover all M coefficients by an ordinary transform and construct an evaluation program from them. This already pays the per-fiber ordinary transform that the proposed sparse composition was meant to avoid. It is not a proof that every bridge is expensive.

Similarly, a capped probabilistic recovery followed by exact verification may reject a truly light fiber. Replacing every such rejection by a full transform preserves correctness, but the B+1 debit has not been justified. Without a deterministic completeness theorem, all Q fallbacks remain possible in a worst-case accounting. An expected/probabilistic aggregate algorithm could be a separate legitimate task, but would require a new failure and cost contract; it is not the current theorem.

## Known ingredients and the possible remaining contribution

**Established mathematics and reusable composition.** Vandermonde/Hankel identification, Prony recurrences, rational residues, Fourier orthogonality, Cooley–Tukey factorization, pruning, concavity and light/heavy amortization are standard. The proof already attributes the first ingredients. The [FFTW authors’ pruning discussion](https://fftw.org/pruned.html) explicitly separates O(N log K) arithmetic savings with known sparsity from practical performance. The precise blind-discovery and rejection wrapper is additional work, but adding a wrapper does not automatically establish publication novelty.

**Potentially distinctive lemma or interface, with priority unresolved.** The useful candidate is the *whole* deterministic supplied-root-field recognition/rejection and dense-output theorem with its finite-parameter ledger, including a final over-budget heavy fiber. No individual elementary identity is promoted as new. This review identifies no new theorem increment beyond the original proof. A nonmatch to one input model is insufficient to certify that the complete interface has not appeared elsewhere.

**Why the headline is too broad for a novelty claim.** The previously accepted exact-complex conservative solver costs D_M(b)=O((b+1)^3(1+log M)^3). Its accepted composition with the same verification and synthesis wrapper already reaches the polylogarithmic-budget O_c(N log log N) headline. It does not uniformly match the sharper Qb² term or establish arbitrary-field transfer. These distinctions should be stated explicitly in any manuscript rather than advertising the headline as an independently new principle.

## Mathematical usefulness and practical limits

The class is not restricted to sparse final spectra. In the balanced square case Q=M, choosing only a[t,t]≠0 in each fiber makes every final coefficient nonzero by the synthesis identity. Section 10 supplies stronger dense-input, dense-output, full-reshaped-rank examples. That is a real mathematical distinction and could support a useful example or exact-algebra application.

It is still a finite union of low-dimensional support subspaces when K0<N. A finite fixed bank of invertible preconditioners cannot cover all complex inputs. Endpoint conditioning of the optional Green preconditioner says nothing by itself about Prony recognition stability.

A plausible use is exact batch processing of signals with a verified sparse intermediate character bank, for instance algebraically generated channels. No real workload, producer guarantee or engineering advantage is established here. The original report itself records 7,516,160 operations against 7,340,032 at N=262144,b=18, about 2.4 percent more, for a cap-variant profile rather than an aggregate benchmark. Those historical counts were not rerun. There is no matched wall-clock speedup, finite-word bit theorem, robust near-sparse recovery guarantee or production qualification.

## Fresh controls and stopping rule

The independent controls passed 40 modular factorization cases, 255 amplitude checks and 992 output coordinates; 887,797 exact integer support-profile/cap/budget combinations, including 99,021 needing the final-heavy allowance; and 62 nonzero off-grid coefficient checks. These support normalization and accounting. They do not test Berlekamp–Massey code, the original implementation, the primary-source algorithm, floating point or performance.

**Stop now:** the Arnold–Giesbrecht–Roche comparison has reached a concrete input/completeness/model nonmatch. Preserve the accepted theorem and open parent; make no publication-priority promotion, practical claim or new record. Do not launch another broad search just to accumulate nonmatches.

**Next action only on new evidence:** select one complete deterministic raw-grid solver or a concrete exact-algebra application. For a solver, prove a cost-preserving full-contract comparison, including preparation P, ingestion L, all Q discovery attempts T(M,B), root supply, full verification, explicit outputs and O(N) storage. The target is the entire finite-parameter envelope, not merely Q T≤QB². For an application, freeze a producer and workload that actually guarantee the intermediate support budget and demonstrate a benefit under fully charged, matched baselines. If neither is supplied, the publication gate stays on hold. An expository technical note remains possible with honest classical attribution, but this audit does not establish research-publication novelty.

No external write, upload, commit or workbook edit was made.
