# Order-eleven independent review

Accepted upper bound: fourteen whole signed banks, or 154 original phase resolvents, over the splitting field of the explicit sextic over Q(q). No minimum or runtime improvement is claimed.

Start with `INDEPENDENT_REVIEW.md` and `ACCEPTANCE_RECEIPT.json`.

- `review_n11.py`: fresh characteristic-zero derivation, all eleven row recipes, all 121 Weyl equations, good-reduction determinants and restricted-quintic controls.
- `review_literal_n11.py`: fresh literal matrix powers, all 154 two-sided resolvents, amplitude/trace conversion and all 121 original matrix entries.
- `EXACT_REVIEW_RESULTS.json`, `LITERAL_ORIGINAL_MATRIX_RESULTS.json`, `LITERAL_AMPLITUDE_CERTIFICATE.json`: exact controls and certificates.
- `sources/`: frozen inert author mathematics and accepted precedent. No author source programs are included or executed.
- `REVIEWED_SOURCE_HASHES.json`, `MANIFEST.json`: byte-level provenance and final packet hashes.

Reproduce in a writable copy with Python and SymPy by running both reviewer scripts. They write only within this review directory. Expanded rational-basis row coefficients with denominators divisible by 23 must not be reduced termwise; use the original unit-denominator formulas described in the review.
