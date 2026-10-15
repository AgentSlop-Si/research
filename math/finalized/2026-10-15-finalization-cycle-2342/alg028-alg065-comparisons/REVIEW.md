# Independent review: ALG-028 and ALG-065 comparison gates

Date: 15 October 2026 UTC. Reviewer scope: the existing named comparison gates only. Base repository commit: `e5c9c53f7d34e8d858e781d2d5321393aec7e85c`.

## Final disposition: ACCEPT, comparison completion only

The independently inspected sources support **completion of two bounded primary-source comparisons with qualified nonmatch conclusions**. They do not support closure of either parent record. The author's final report, source locators and fourteen-cell current-overlay proposal have been reviewed and accepted at their frozen hashes below.

Both overview records must remain `TO RESEARCH`, priority `12`. This review establishes no new theorem, implementation, source-code replay, global novelty judgment, runtime superiority, or production acceptance.

## Owner scope and evidence identity

I independently read the current native Catalogue owner rows 164 and 168, their corresponding overview rows 287 and 294, and attribution rows 199 and 206. Each owner pass/stop condition permits a primary-theorem hypothesis/formula/cost mapping or a qualified nonmatch. The separate remaining-obligations column preserves substantive construction and numerical gates.

The earlier all-79 inventory also leaves these exact comparisons unselected; the current owner text does not record either selected comparison as already completed. The two cases therefore differ from merely repeating the already-completed ALG-080 comparison.

The pinned open-record index was independently retrieved and is semantically identical to the author's local copy. Its count of 68 closed and 259 open is a recorded snapshot, not a new exhaustive proof audit. This review accepts no parent status changes and therefore contributes zero additional closed records.

I independently fetched the two research sources from the pinned GitHub commit and checked their UTF-8 bytes:

- ALG-028: 15,376 bytes; SHA-256 `8512b7be7d104174d737abd279fae61b0a9d3f49b8610376a01fb4096520bfcf`.
- ALG-065: 18,700 bytes; SHA-256 `a313395ea0fee6ffd5fc0405c457ff4e30a7ee26ea2dbd118326dcf120450566`.

Both equal the owner-record identities and the available local source copies. Full native histories remain private and are not reproduced here. Detailed source identity URLs are in `source-identity-check.json`.

## ALG-028: finite-field tabulation and log-RAM multiplication

Primary references independently read:

- Chan, Jin, Vassilevska Williams and Xu, [arXiv:2310.13174v3](https://arxiv.org/html/2310.13174v3), Lemma 2.2 and Appendix B, especially B.6–B.8.
- Fürer, [arXiv:1402.1811v1](https://arxiv.org/pdf/1402.1811v1), Definitions 1–2 and Theorem 1(a).

Chan's Lemma 2.2 computes convolution over a supplied prime field with polynomially bounded prime in `O(n log p)` word time. Appendix B includes charged table construction and compact finite-field DFT I/O. B.6 permits constant-time batches only when inputs and outputs fit in a constant number of words; B.7 retains its preprocessing term. These are exact finite-field operations. They do not supply the historical complex quantizer, a normalized absolute-error guarantee, or an uncharged collection of unpacked complex outputs. Appendix B explicitly repairs a gap in the earlier cited packing argument; attributing the complete general-prime result to that earlier argument alone would be wrong.

Fürer's linear bound concerns multiplication of bit strings on the specified log-RAM, with bounded-width integer operations. Its input-size variable counts bits. It is not a theorem that an arbitrary complex vector's full transform takes linear time in the number of coordinates. A reduction must charge encoding, precision, recovery and output.

Independent mathematical checks of the comparison: a finite field's exact operations have no complex approximation norm without an additional representation map. In the historical table model, `q=(2R+1)^2`, every entry contains K outputs, and polynomial table storage forces `K log q=O(log N)`. Thus `log K=O(log log N)` and visiting N explicit outputs per grouped pass cannot be made free by relabeling a finite-field lookup. This is a restriction of the stated design, not a general FFT lower bound or a proof that adaptation is impossible.

The named comparison can finish as a qualified interface nonmatch. Remaining parent gates are the certified finite-word phase/table builder, fully paid successful executor/fallback/output path, and any separately selected reduction or priority question. The related Q01 proof/refusal overlay does not certify this historical implementation.

## ALG-065: sparse recovery versus fixed projections

Primary reference independently read: Hassanieh, Indyk, Katabi and Price, [arXiv:1201.2501v2](https://arxiv.org/pdf/1201.2501v2), equation (1), Theorem 4.9 and Theorem 6.1.

Theorem 4.9 has a best-k-term Fourier-error comparator plus the additive `delta ||xhat||_2` term, success probability `2/3`, and stated time `O((k/epsilon) log(n/k) log(n/delta))`. Its observations are non-adaptive, while the recovered support depends on the data. Theorem 6.1 separately allows adaptive Fourier-coordinate sampling and lower-bounds samples under its probabilistic sparse-recovery guarantee. Neither theorem identifies arbitrary linear sketches with Fourier-coordinate samples or gives an unrestricted arithmetic lower bound. The correct general-error locator is 4.9, not 4.4.

Independent mathematical checks: for an orthogonal projector P, `||I-P||_2=1` whenever its kernel is nonzero. A unit kernel vector attains relative error one after a unitary Fourier transform. A coordinate-impulse leverage calculation may give `sqrt(1-q/M)` in an orthogonal bank, but it is not the supremum over all inputs. The kernel witness depends on the fixed frame; it cannot be silently turned into a lower bound for a randomized per-input guarantee. Likewise, a deterministic zero-transcript rank argument does not automatically cover independent raw-input reads or arbitrary randomized quantifiers.

Accordingly, the sparse-recovery theorem and the fixed-projector result are compatible. The named comparison can finish as a qualified nonmatch. The parent still needs a faster complete full-rank coefficient/short-FFT/scan pipeline and rigorous numerical energy/output enclosures. Local frame conditioning and rounded energy subtraction do not close those gates.

## Publication and update boundary

Only a concise comparison-complete note, exact primary references, and the already-owned remaining gates may be added. Preserve source identities, frozen proof qualifications, historical evidence, scores and both parent statuses. Do not rename a parent as a finite comparison, create a replacement task to claim closure, or generalize this review to all source-comparison work.

The accepted fourteen targets are Catalogue AE/AF on rows 164 and 168; Research overview F/P/Q on rows 287 and 294; and novelity breakthough Y/Z on rows 199 and 206. Every proposed preimage matches my independently captured native read. Apply the accepted text only as a leading dated prefix, followed by the agreed history delimiter and the entire exact preimage. Fresh read/equality checks are still required at application time. The overview F and current Y/Z mirrors now name the true remaining gates; older novelty O text remains historical and is superseded by the dated current overlays.

The final author report includes the prime-size hypothesis in Chan's Lemma 2.2 and correctly identifies Corollary B.8. Its fixed-projector transfer test is sound: summing squared residuals for the Fourier basis vectors gives `N-r`, so the stated same-fixed-projector guarantee requires `r >= N(1-delta^2)`. This does not apply to HIKP's randomized per-input success. The additional absolute-to-relative error conversion is also correctly an absence of an implication, not an error lower bound for the accepted implementation.

Frozen author artifact SHA-256 identities:

- Report: `8079f09ceb910a852e0dd82f8dcd537d06b7a025e7b342dbca1913d225a2bf04`.
- Source locators: `21c4961e6f653f7b3192452f8b28d5f53e394dd49cfd1427bbe3eaf45d2be9be`.
- Fourteen-cell proposal: `168d2001b25810afbacce16bee272fe188576bc1804d3036081b410fc5100c87`.

The accepted prefixes and their hashes are fixed in `ACCEPTED_TARGETS.json`; no raw preimage history is included there. I also verified the two ALG-028 companion-note hashes and the recorded review hash `d232c10a78a5e9a87ca5c7543a6401641e5635c60781f5026a6c31635be46db4`. Its ALG-028 entry confirms the guarded theorem and remaining builder/executor obligations used here.

No supplied research program was run, no package installed, and no external state changed. Review artifacts intended for publication are this report, `ACCEPTED_TARGETS.json`, `source-identity-check.json`, and `independent-checks.json`. The private evidence directory is excluded.
