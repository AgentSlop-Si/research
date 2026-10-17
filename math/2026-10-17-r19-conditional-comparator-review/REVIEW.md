# R19 independent read-only review

Review date: 16 October 2026 UTC
Publication audit: 17 October 2026 UTC
Status: arithmetic accepted; exact-array transfer unresolved; retain as an attributed comparator candidate.
Scope: source inspection and a fresh exact-rational arithmetic check. No historical supplied code was run or imported, no Lean build was run, no external state was changed, and the user's adaptive p^d base/matrix research route was not changed. This is an assistant review, not independent human review or formal verification.

## Decision

R19 has a valid moment calculation for the displayed R480/T16 histogram. If a fully charged arbitrary-input exact-array macro with that histogram is established, the written Fourier transfer gives the displayed exponent. The supplied R19 package does not itself establish that macro's complete exact-array/cost contract.

The strongest defensible label is:

“Attributed R480/T16 comparator candidate, with independently rechecked rational moment and a conditional all-length exponent of 0.9983246; exact-array realization and theorem instantiation remain unclosed.”

The issue is more specific than “Lean integration pending.” A mathematical model/interface proof is still required. Formalization is one way to close and audit it, not a substitute for stating the right obligations.

## Accepted claims

1. The displayed arithmetic is correct.

   m=73; W0=14336;
   H={1:349604, 2:60192, 3:62585, 4:20448, 5:11808, 7:7, 8:1152, 48:4866}.

   There are 510662 positive children per cover class; their rank mass is 1041408. W0*m=1046528, giving deficit 5120 and normalized rank mass 1017/1022. Every positive rank is below m.

2. The claimed root interval is sound for this histogram.

   Define F(a)=sum_r [r H_r/(W0*m)] exp(a log(m/r)).
   A fresh rational calculation, using alternating Mercator bounds rather than the supplied logarithm implementation, establishes:

   - F(0.00167546267680)-1 is between approximately -2.373472503602268e-14 and -2.373472503602255e-14.
   - F(0.00167546267682)-1 is between approximately 3.484405669727861e-14 and 3.484405669727873e-14.
   - F(0.0016754)-1 is approximately -1.83576532101521112436e-7.

   The deciding comparisons used exact fractions. F is continuous and strictly increasing because all nonzero weights and log(m/r) are positive. Therefore the unique root lies strictly in the claimed interval. This is certification of the supplied numerical profile, not certification that a physical algorithm has that profile.

3. The strict Fourier absorption gap can be supplied.

   Use tensor witness a=0.00167546267680 and Fourier delta=0.0016754. The positive gap is 39173/625000000000 = 0.0000000626768. It would be insufficient merely to use the same a and delta in a theorem requiring delta<a; the root bracket supplies the needed distinct witness.

4. The comparison is arithmetically correct.

   100*(0.0016754/0.0012331685-1)
   =35.861400935881836099446263831747... percent.

   This compares proposed versus reported checked exponent savings in the stated exact-arithmetic model. It says nothing about measured runtime, constants, numerical stability, or a practical FFT crossover. Conditional on the macro contract, O(N(log N)^0.9983246) is indeed o(N log N).

5. The source documents contain relevant structural ingredients.

   The pinned complex closure gives an eventwise tensor lift, arbitrary correlated live data, exact recursive children, helper restoration, idle remainders and phase corrections. This supports investigating compatibility rather than extrapolating a finite N=16 fit. It does not, by itself, establish the receiving model's full contract.

6. Administrative status is verified.

   The 16 October 2026 GitHub connected read reported PR2234 and PR2250 merged at 2026-10-15T19:01:30Z, with merge commit aa2ba6a47011cce1d138a1f34fb1e4cf52ac7fb8. Their returned review lists were empty. The pinned proof text still retains review caveats. Merge status is not a proof certificate. A cached public web page then still displayed Open; the recorded direct GitHub metadata controlled that historical status check.

## Unresolved proof obligations

### A. Rebuild the exact-array cost interface

The source's stated theorem concerns bounded dyadic Gaussian coefficients, spaced address bits, long records and a fixed-tape model. Its internal nonrecursive bill is O(V((e log p)^tau+1)); record preparation is absorbed using a long-record assumption.

The receiving Fourier contract instead requires a finite macro for every f, on arbitrary complex arrays, with nonrecursive cost at most A W 2^k, where A is independent of f and k. A tape-layer bound is not a proof of this different bill.

The Fourier framework's digit-prefix adapter lemma is a promising route: fixed columnwise binary affine maps and quarter phases can be executed with charged linear array work. A transfer proof must explicitly use that array implementation for every R480 adapter and show no per-entry scan over all f columns remains. It may thereby avoid the ordinary-interchange/compact-tape dependencies rather than formalizing them. Until one route is actually discharged, closing PR2234 and PR2250 alone is insufficient.

### B. Make the cover physical

The source uses Gamma=|O(73,2)| and W0*Gamma stock. A literal fixed-cover Fourier witness should state W_eff=14336*Gamma and n_eff,r=Gamma*H_r, or prove an equivalent implementation. Gamma cancels in the moment, so this is not an arithmetic objection. It does not cancel from allocation, dispatch or constructive preparation. Do not silently treat per-cover accounting as a physical 14336-array implementation.

### C. Bind the histogram to the complete endpoint

Pin and inspect the full selected witness, then account for every recursive call, copied-register transformation, helper wrapper, positive idle remainder and endpoint correction. Prove common-label/owner compatibility on arbitrary correlated arrays, with exact axes and chronological windows. In particular, a zero-rank idle remainder can still require a translation; it is not a free omission.

The neighboring height-ledger note corroborates the same histogram from the event inventory, but explicitly assumes native endpoints and dispatch semantics. It is useful supporting evidence, not a closure of those assumptions.

R19's moment checker hardcodes H and does not load the upstream event ledger or even the certificate JSON. Its PASS therefore does not authenticate physical provenance.

### D. Distinguish live dirty helpers from fresh scratch

State which arrays are arbitrary live inputs that must receive the final tensor, which copies are temporary, and which private centers are initialized clean. Charge initialization, copy, clear, gather/scatter, storage and restoration. Establish spectators and inactive row coordinates are fixed, and arbitrary complex values are allowed. An algebraic extension from a data-independent Q[i]-linear circuit is plausible, but should be written down rather than inferred from the dyadic tape theorem's headline.

### E. Complete the recurrence and all-length boundary

Use actual W_eff and n_eff in fiber batching, leftover-fiber handling, small widths and fewer-than-m leftover axes. Supply linear overhead, constructive fixed preparation, linear live storage and O(k)-bit address bounds. Then apply the tensor recurrence and the Fourier compiler with its supplied-root, scalar-preparation and movement costs, using a>delta.

### F. A Lean instantiation has additional obligations

The inspected PR588 result is a different circuit and geometry. It uses source copies and dedicated banks, and expressly avoids native idle-data hosting as an unproved premise. Its formal engine requires a stricter finite-fill inequality (reported fill parameter s=40), not merely the ordinary moment test.

Consequently one cannot replace its histogram and inherit its theorem. Either encode and discharge the R480 native hosting geometry, or convert it into an admitted geometry, recount all added costs, and recertify the applicable rate. A changed invoice could change the exponent. Any claim of formal verification requires the actual instantiated theorem, build, statement/axiom checks and source bindings.

## Rejected interpretations

- “R19 is already a proved or Lean-verified all-length DFT improvement.”
- “The only remaining task is clerical formal integration.”
- “Merged PR2234/2250 validate the mathematics.”
- “The PR588 Lean receipt verifies R480/T16.”
- “A 35.8614% larger exponent saving means a 35.8614% runtime improvement.”
- “The borrowed R480 network or transfer theorem is the user's new invention.”
- “R19 establishes a growing-size improvement for the user's original adaptive p^d base/matrix construction.”

These interpretations exceed the evidence. They do not refute the conditional candidate.

## Attribution and source discipline

The package acknowledges upstream ownership, which is appropriate. Its provenance is not yet an immutable complete-witness manifest: “inspected revision around” a commit and unpinned CrocSwap paths are weaker than the receiving project's stated requirements. This review resolves exact pins below, but does not authenticate all transitive finite input archives.

The complex closure is credited to Jose Manuel (jmbarrancoml), with its native R480/T16 and supporting lineage preserved in its NOTICE. The Fourier comparison/transfer project is Ryan Shea's integration, with the PR588 circuit credited to Jeremy Kothe and predecessors, the formal engine to Jacob Sussman, geometry to Dugongue and jacklightChen, gauged extension to Nil Mamano's submission, and model/reduction to OpenAI. The source notices provide further contributor-specific credits.

R19's possible contribution is a compatibility proposal and moment pricing. No novelty, priority or exhaustive absence-of-prior-transfer claim is established by this review. Preserve it as an attributed comparator alongside, rather than a replacement for, the original research route.

## Immutable sources and retained evidence

- Original R19 package ZIP SHA256: edffde4302c84c8fded1f13644ca6f53a0c3eb0dc20103133f0763f92b1958ad. All six manifest member hashes matched. This validates package integrity, not upstream theorem truth.
- [Exact-array framework, §§1–3](https://github.com/shea256/fourier-transform-below-nlogn/blob/0e61af6ce0ef712494c93c902baefa314ef7e23c/paper/framework.md#L1-L107). Blob e7923fa949cb50bb817a8b3923c402dcc82407df.
- [PR588 result, especially §§6.2–6.3](https://github.com/shea256/fourier-transform-below-nlogn/blob/0e61af6ce0ef712494c93c902baefa314ef7e23c/results/complex588.md#L47-L81). Blob c90444e89d87d25627a2f3ef5af321a6b62787d7.
- [R480 closure](https://github.com/CrocSwap/integer-mult-bounds/blob/8c60765b5dea9d862b3b190d55da102a576031bf/research/selected-complex-layer-closure/PROOF.md): §1 model, §2 lift, §§3–5 physical realization, §7 bill. Blob d7ec0d101405a5f099f55f6a73e9791731737fd0; matches the inspected source text after removal of one extra trailing linefeed in the retained text copy, as documented in `INTEGRITY.json`.
- [Closure source manifest](https://github.com/CrocSwap/integer-mult-bounds/blob/8c60765b5dea9d862b3b190d55da102a576031bf/research/selected-complex-layer-closure/SOURCES.json) and [attribution](https://github.com/CrocSwap/integer-mult-bounds/blob/8c60765b5dea9d862b3b190d55da102a576031bf/research/selected-complex-layer-closure/NOTICE.md).
- [Conditional event/height ledger](https://github.com/CrocSwap/integer-mult-bounds/blob/97d1b23a69c9488d0667a4e666fe3875d56113c3/research/selected-complex-height-ledger/PROOF.md), especially retained hypotheses and evidence limits.
- [PR2234](https://github.com/CrocSwap/integer-mult-bounds/pull/2234), head d047ef86fbc5b1614d3d8e2b8d3441413beab73f; [PR2250](https://github.com/CrocSwap/integer-mult-bounds/pull/2250), head d404b48a1e7b147556b309497d55089c837dddb2.
- A second fresh arithmetic implementation is included as `fresh_r19_check.py`, with output in `fresh_r19_receipt.json`. It independently reproduces the rank mass, root bracket and absorption gap using exact rational decisions. Source metadata and the review-date PR status are retained in `SOURCE_PINS.json`. No supplied historical code was run. Source-text byte normalization is documented in `INTEGRITY.json`.

## Stopping condition

The requested read-only review is complete. The evidence supports arithmetic acceptance and a comparator-only conditional status. Closing the exact-array witness or changing the primary research route would be separate work; neither was performed here.

