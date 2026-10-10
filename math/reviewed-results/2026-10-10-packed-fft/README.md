# Packed finite-word Fourier theorem and source bundle

10 October 2026. Local combined review candidate, version 3. No remote publication is implied.

## Result and limits

The accepted paired proofs establish a uniform deterministic all-integer-length approximate DFT theorem. With n=ceil(log2(N+1)), supplied 2<=t<=n, and the specified O(log N)-bit dyadic input format and polynomial dynamic range, they explicitly output all N coordinates with relative-l2 error at most 2^-t, using cold O(N(t+log(n+1))) word operations and O(N) words. N=1 is an exact copy.

The RAM has sufficiently large Theta(log N)-bit words and scalar integer multiplication/division, shifts, Boolean operations and random access. Fixed t gives the formal O(N log log N) bound in that model. This is not exact arbitrary-complex arithmetic, a bit-complexity result, a fixed-hardware speed claim, a production implementation, or a historical-priority claim.

The practical-scope note shows why this literal conservative eager-table proof is not an industrial implementation. At its smallest allowed accuracy exponent t=2, the packed-branch guard first becomes eligible at v=5120, or N=2^5120, and its mandatory response table already has between 2^674 and 2^675 model words. Eligibility is not successful completion of the charged build. These are properties of this proof's constants, not lower bounds for optimized algorithms.

## Read in this order

1. `COMBINED_STATUS.md`: current combined scope and the exact discharge of backend hypothesis H; explains historical language left unchanged in frozen sources.
2. `theorems/DYADIC_PACKED_THEOREM.md`: complete packed radix-2 layout, Q-1 twiddle catalogue, total response semantics, error proof, charged preparation and scalar fallback.
3. `theorems/CONDITIONAL_ALL_LENGTH_THEOREM.md`: one-call interpolation composition and the independently charged conventional all-length fallback. Its conditional title is retained verbatim; the accepted dyadic theorem supplies H.
4. `reviews/FROZEN_PROOF_REVIEW.md`, `reviews/ALL_LENGTH_INDEPENDENT_ACCEPTANCE.md`, and `reviews/ALL_LENGTH_REVIEW_RECEIPT.json`: exact-byte internal independent mathematical acceptance.
5. `limits/PACKED_RUNTIME_SCOPE.md`: conservative practical guard calculations, explicitly not a benchmark.
6. `prior_art/PRIOR_ART_AUDIT.md`: bounded primary-source comparison and unresolved external priority.

The dyadic theorem SHA-256 is `bb40decffd28b87a88065880363ff099b0d22071ef976bc67a8195c9b9db6d6f`.

The all-length theorem SHA-256 is `71d85d704058bd245d14ce5aad65f747cb1a5b038e69510b21b41d3c8a217927`.

## Fresh controls and what they establish

- Constructor controls: 132,258 exact catalogue identities, 21,844 symbolic DFT matrix entries, 197,952 complete tiny toy responses, 1,696 packed/scalar executions, and 32,766 bit-reversal positions.
- Independent dyadic controls: eight eagerly materialized P=2 complex-state tables with 524,288 cross-table responses plus 256 small responses; 210 stagewise packed/scalar executions; 65,536 padded/overflow keys; and additional exact layout and uncertified numerical stress checks.
- All-length author's controls: 90,127 finite parameter pairs, original source hashes, and guarded large-bit-length inequalities.
- Independent all-length controls: 8 Bluestein identities, 48 exact-integer fixed-lattice fallback executions with high-precision reference values, 45,149 exact aggregate-budget checks, and 4 interpolation/tail controls.
- Practical-scope controls: exact scalar guard thresholds and table-entry counts; no FFT or response tables are allocated.

The sources and recorded results are included. These genuinely construct tiny eager tables and finite scalar controls. They do not instantiate the theorem's full target-precision eager catalogue or certified production transcendental generator, benchmark a practical crossover, or replace the proofs. Decimal/ordinary floating trigonometric references are identified as falsification evidence rather than certified coefficient construction. No predecessor/uploaded research programs were executed to obtain these fresh results.

See `REPRODUCE.md` before running anything. In particular, the all-length author's immutable script expects its original research-source layout; it is not directly runnable from its relocated bundle directory. The reproduction note maps every required source to an included byte-identical copy. Several scripts write new JSON results beside themselves, so use working copies.

## Prior work and immutable history

Chan, Jin, Vassilevska Williams and Xu already retain compact FFT arrays through stages and use universal tables with charged preprocessing; see [Appendix B, Lemmas B.6-B.7](https://arxiv.org/html/2310.13174v2). This bundle does not claim invention of that mechanism. The finite complex-state error/catalogue contract is proved directly, and external priority remains unresolved.

The prior-art audit's early “unproved candidate” language, initial research question, initial reviewed draft, and historical root review are preserved without rewriting history. `COMBINED_STATUS.md` explains their relationship to the final accepted proofs. The accepted older unpacked/interpolation manuscript and Q01 documents are included as historical mathematical provenance, not alternative current runtime claims.

## Integrity

`MANIFEST.json` records every payload's role, bytes, SHA-256 and original research-source mapping. `BUILD_PROVENANCE.json` records the local byte-copy and packaging checks. `SHA256SUMS` covers all bundle files except itself. The ZIP contains only this release tree with relative paths.

All frozen mathematical sources, reviews, control source files and recorded control outputs are included byte-for-byte. No private conversation URLs, Library identifiers, credentials, hidden assistant notes, or third-party full-text PDFs are included. Original relative research paths inside immutable sources remain provenance references; use the manifest's mapping for relocated copies.
