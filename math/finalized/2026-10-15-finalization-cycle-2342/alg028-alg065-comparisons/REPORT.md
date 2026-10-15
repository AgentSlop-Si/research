# Two remaining Fourier comparison gates

15 October 2026. Read-only source comparison and exact algebraic checks. No supplied program was imported or executed, and no external service was changed.

## Decision

The named comparison subgates for **ALG-028** and **ALG-065** can be marked complete as qualified model nonmatches. Neither complete record can be closed. Keep both **TO RESEARCH**, priority **12**, with their accepted mathematical results unchanged.

- ALG-028 still needs its own certified finite-word phase/table builder, a complete qualified executor, and any further specifically justified historical-priority comparison. Q01's separate successor/refusal does not certify that implementation.
- ALG-065 still needs a faster complete coefficient/short-FFT/scan pipeline and rigorous numerical energy/output enclosures. A comparison with sparse recovery does not supply either.

This is useful completion of two already recorded comparison tasks, not completion of two theories, a new algorithm, or a worldwide-priority judgment. The 68 closed / 259 open snapshot therefore does not change.

## Scope and source identity

Selection used the rebuilt open index at repository commit `e5c9c53f7d34e8d858e781d2d5321393aec7e85c` and the recovered original-category inventory at the same commit. Full live owner rows were read before judging:

- [ALG-028 owner](https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit#gid=214001001&range=A164:AF164), with [overview](https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit#gid=1731260011&range=A287:Q287).
- [ALG-065 owner](https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit#gid=214001001&range=A168:AF168), with [overview](https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit#gid=1731260011&range=A294:Q294).

Their existing pass/stop condition permits an exact primary-theorem hypothesis/formula/cost map **or a qualified nonmatch**. Their owner-column Z obligations are broader and remain open. The report does not replace the owners with easier tasks.

ALG-080 was screened out because its owner already records the Ailon/Morgenstern comparison. The specifically excluded F021, N256, C02/tree/Q16 updates and missing-byte PACK-01/ALG-074/ALG-075/Q34 gates were not redispatched.

## 1. ALG-028: quantized stage-template tabulation

### Accepted object being compared

The exact source is [Fresh-Input Fourier Reuse, sections A–B](https://github.com/AgentSlop-Si/research/blob/e5c9c53f7d34e8d858e781d2d5321393aec7e85c/math/archive/objects/85/8512b7be7d104174d737abd279fae61b0a9d3f49b8610376a01fb4096520bfcf__005_8512b7be7d104174.md), SHA-256 `8512b7be7d104174d737abd279fae61b0a9d3f49b8610376a01fb4096520bfcf`, 15,376 bytes. Its two assigned companion notes were also read in full; their locators are in `SOURCE_LOCATORS.json`.

The accepted object has dyadic N, represented complex inputs with |x_j|≤1, fixed absolute error ε for the complete F_N x/N output, and an address-capable O(log N)-bit word RAM. With L=log₂N, q=(2R+1)², R=ceil(8(L+1)/ε), and grouped width K, the source charges Kq^K stored words, O(K log K q^K) table construction, O(N) phase preparation/storage, and all K values at every query. Its conditional O(N log N/log log N) word bound retains a guarded coefficient/precision-printer premise.

The independent recorded review, SHA-256 `d232c10a78a5e9a87ca5c7543a6401641e5635c60781f5026a6c31635be46db4`, explicitly excludes free K-valued lookups and says the Q01 overlay is not inherited. Its matching local bytes were verified. No theorem-scale table or historical executable was run.

### Named primary comparison

[Chan, Jin, Vassilevska Williams and Xu, v3](https://arxiv.org/html/2310.13174v3), Lemma 2.2 and Appendix B, gives exact convolution over F_p, for prime p≤n^{O(1)}, in O(n log p) time. Lemma B.6 batches t_i=floor(0.1 log n/(m_i L₂ log p)) finite-field DFTs into compact O(1)-word input/output; its stated preprocessing is n^(0.2+o(1)), with DFT enumeration n^(0.1+o(1)). Lemma B.7 explicitly charges transpositions, twiddles and reversal. This credits paid packing and table reuse as antecedents. It supplies no numerical rounding/error map to ALG-028's complex alphabet. Its packed return cannot replace K decoded complex outputs at unit cost. Matching word-width order alone does not identify the tasks; setting log p equal to precision would omit the arithmetic/representation conversion. Thus the exact named comparison is a qualified nonmatch, not an access failure.

[Fürer, v1](https://arxiv.org/pdf/1402.1811v1), Definitions 1–2 and Theorem 1(a), uses O(log B)-bit unit-cost log-RAM operations and gives O(B) exact integer multiplication, where B is input **bit length**. The proof includes input/output and finite-precision FFT work. ALG-028 permits Θ(log N)-bit components, so its worst-format input has B=Θ(N log N). Substitution yields an O(N log N) multiplication bound, not the required O(N log N/log log N) complex-vector interface. An additional reduction, with rounding, roots, output and setup charged, remains necessary.

### Exact contract checks

These are algebraic consequences of the recorded ALG-028 contract, not new claims about the cited papers:

1. With fixed ε, log q=Θ(log L). The source's constraint K log₂q+log₂K≤cL gives K=Θ(L/log L) and log₂K=Θ(log L). Therefore Θ(L/log L) full passes remain. This is the all-level table mechanism; it is not the leaf-only expression log(N/K).
2. If the complete table has at most N^c words and q≥2, then K≤c log₂N. Consequently a pass-based implementation that reads/writes all N entries still takes Ω(N log N/log log N) accesses inside this specified family. This is not an unrestricted FFT lower bound.
3. Let U_N=F_N/√N. Scaling an ε-accurate F_N/N output by √N only certifies ||error||∞≤√Nε and ||error||₂≤Nε. Dividing by ||x||₂ gives no uniform relative error for arbitrarily small nonzero represented inputs. The accepted absolute-error theorem must not silently be replaced by Q01's distinct relative-norm contract.

**Disposition:** the requested Chan/Fürer model comparison ends here with precise mismatches. Complete only that comparison subgate. Preserve the historical phase-builder/executor and exact complete-contract attribution questions.

## 2. ALG-065: orthogonal-bank projectors

### Accepted object being compared

The exact source is [HERO1 Phase14 audit, sections 2–7 and 9](https://github.com/AgentSlop-Si/research/blob/e5c9c53f7d34e8d858e781d2d5321393aec7e85c/math/archive/objects/a3/a313395ea0fee6ffd5fc0405c457ff4e30a7ee26ea2dbd118326dcf120450566__001_HERO1_PHASE14_AUDIT.md), SHA-256 `a313395ea0fee6ffd5fc0405c457ff4e30a7ee26ea2dbd118326dcf120450566`, 18,700 bytes, read in full and hash-matched.

For full-column-rank supplied V over C, P=V(V*V)^−1V* is the orthogonal projector. The normalized Fourier map U is unitary, so ||Ux−UPx||₂²=||x||₂²−||Px||₂². This is an exact input-dependent energy identity. Every proper fixed P has worst-case relative error 1. The q=M construction is exact on all inputs but its accepted complete evaluator is FFT-scale. Numerical subtraction of nearly equal energies is not a certified error enclosure.

### Named primary comparison

[Hassanieh–Indyk–Katabi–Price, arXiv:1201.2501v2](https://arxiv.org/pdf/1201.2501v2), §2 and Theorem 4.9 (printed p19), treats dyadic n and unitary Fourier normalization. It returns a data-dependent sparse approximation with probability 2/3 and error at most (1+ε)Err(x̂,k)+δ||x̂||₂, in O((k/ε)log(n/k)log(n/δ)) time. The algorithm's samples are non-adaptive; the support/decoder is data-dependent. The additive δ term must be retained unless the stated precision/tail assumption removes it. This is not the fixed-projector error identity, a full numerical executor certificate, or N explicit output writes for free.

Theorem 6.1 (printed p21) allows adaptive **coordinate samples of an orthonormal flat transform** and proves Ω(k log(n/k)/log log n) samples for its factor-2 best-k-tail recovery guarantee, with success at least 3/4. ALG-065's arbitrary block sketches and all-input relative-error demand do not meet that measurement/guarantee pair. It yields no scalar-arithmetic or arbitrary-sketch lower bound for this pipeline. This completes the named sparse-recovery/sampling comparison as a qualified nonmatch.

### Exact error and quantifier mapping

The following arguments independently check the attempted transfer using the owner's own formulas.

**Fixed subspace versus best support.** For a fixed Fourier support S, write D_S for its coordinate projector. The squared best approximation error on that fixed support is x*U*(I−D_S)Ux. The ALG-065 error is x*(I−P)x. These quadratic forms agree for all x exactly when P=U*D_SU. A general chirp-bank frame is not given this identity. Minimizing over supports S is an input-dependent operation and cannot be replaced by a single fixed P without proof and cost.

**A precise obstruction to importing the sparse guarantee.** Suppose one attempted to give a single fixed rank-r projector P the inequality

||U(I−P)x||₂ ≤ C Err(Ux,k)+δ||x||₂

for every x, with k≥1. Set x_j=U*e_j for j=1,…,N. Each Ux_j is one-sparse, so its tail is zero. The sum of squared left sides is

Σ_j ||(I−P)U*e_j||₂² = trace(I−P)=N−r.

The claimed inequality would therefore require r≥N(1−δ²). In particular, the zero-additive-tail version requires r=N. This is a deterministic, same-fixed-projector necessary condition. It is not a lower bound against a randomized algorithm that may choose different effective maps for each input/run, and it does not assert such a rank condition for HIKP.

**Why the familiar coordinate bound is weaker.** On one M-dimensional orthogonal bank with q chosen columns and equal coordinate leverage, each coordinate impulse loses squared energy 1−q/M. A nonzero kernel vector instead loses all its energy. Thus sqrt(1−q/M) can be the exact impulse error while the all-input supremum is 1. Neither statement is contradicted by sparse recovery's different comparator.

**Zero-transcript scope.** For deterministic adaptively chosen linear sketches of rank at most N/M, chosen solely from prior sketch responses, the zero-transcript common kernel has dimension at least N−rN/M. If r<M, it contains a nonzero h indistinguishable from zero. A uniform relative-error bound below 1 forces zero output at zero and then fails at h. Extra raw reads, random per-input success and different output guarantees are separate models; Theorem 6.1 cannot erase these distinctions.

**Disposition:** complete the named error/sampling comparison only. Keep construction and numerical qualification open. No new lower-bound theorem, worldwide novelty, production readiness or measured speedup is claimed.

## Native-table proposal and verification boundary

The minimal proposal updates AE/AF in the two owner rows; F/P/Q in their two overview rows; and Y/Z in the same records’ novelty-view rows, fourteen current text cells in total. The older novelty-view O text remains preserved and is superseded by the dated Y/Z overlays. The proposal retains the remaining gates and links the exact primary versions. No status, priority, formula or proof acceptance is changed. Each new current update is prefixed to the complete prior text, preserving history. The extra overview F and novelty-view Y/Z targets prevent stale current instructions from redispatching the completed comparisons. Full before-text is retained privately for guarded application; it is not included in this publishable report. Apply only after fresh equality checks and independent review.

Local checks consisted of full exact owner reads, pinned repository reads, byte/hash comparison, primary theorem inspection and the displayed symbolic deductions. They did not include production execution, finite-word certification, historical-program replay or a global literature exhaustiveness claim.
