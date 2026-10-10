# Reference and certificate index

## Mathematical dependency map

The main family theorem is manuscript Theorem 9.1. Its chain is Theorem 7.2, Lemma 7.1, Theorem 6.1, Theorem 3.2, and the finite constants in Appendix A. Each proof appears in the manuscript. Lemma 5.1 proves the inverse identity. Corollary 9.2 additionally uses the fully reproduced disk and resonance proofs in Theorems 4.1 and 5.2. The scalar-bank application has its own complete lower bound, annihilator criterion and universal upper construction in Proposition 10.1.

No theorem in this chain invokes an unpublished “inherited theorem” without its proof. The five-base finite arithmetic is provided as explicit coefficient data, finite determinant reconstruction, and integer gcd witnesses. Its finite nature does not restrict the prime multiplier to a tested census.

## Classical references and priority boundary

- Lubinsky–Saff 1987, DOI 10.1007/BF01890574: Lemma 4.1, p. 343, recurrence and reciprocity; Lemma 4.5, p. 346, equation (4.15), static root-of-unity factorization; Theorem 3.2, p. 340, equations (3.11)–(3.12), chirp Toeplitz determinant and Padé denominator; proofs pp. 354–355. Their G_n is this note's H_n, and their determinant D(M/n) is not the ordinary z-discriminant. The supplied scan's full mathematical body was compared. Journal reference page 360 is missing.
- Zhedanov 1997, DOI 10.1142/S0217751X97000438: full-text comparison remains pending; not used as an unverified proof dependency.
- Spiridonov–Zhedanov, arXiv:q-alg/9605034v2, Duke Math. J. 89 (1997), 283–305: context on complex recurrence and root-of-unity limits. The manuscript proves the particular resonance statement independently.
- Cigler, arXiv:1602.07850: established special values and q-product background; the needed identities are reproduced.
- Sawa–Uchida, arXiv:1802.00605v1, Theorem 4.8: established quasi-Laguerre discriminant theory. Primary title/author metadata were rechecked on 10 October 2026.
- Grosu–Grosu, arXiv:2007.00065v1, Theorem 8: established Wronskian-Hermite congruence background. The note proves its specialized Wronskian identity directly.

Bibliographic links and exact citations appear in Section 12. None of these comparisons is an originality clearance. The prior source statement that LS87 full text was unavailable is superseded by the supplied mathematical-body comparison, while Zhedanov and broader citation chaining remain open.

## Finite certificate map

All exact vectors are in ascending q powers modulo Phi_s. The original exact records carry U, its reciprocal transform P, g, v, delta, the ordinary discriminant of U, the resultant of z^s+1 with U, Gamma, Gamma Gamma^iota, and the augmented product. The independent records reconstruct all primary fields from a different full-degree method and provide integer gcd Bezout witnesses.

- Base 3: c_s^+ = 1; exact data `certificates/EXACT_CONTENT_S3.json`; prior independent data `certificates/INDEPENDENT_EXACT_S3.json`; standalone vectors in Appendix A, Base 3.
- Base 7: c_s^+ = 49; exact data `certificates/EXACT_CONTENT_S7.json`; prior independent data `certificates/INDEPENDENT_EXACT_S7.json`; standalone vectors in Appendix A, Base 7.
- Base 11: c_s^+ = 161051; exact data `certificates/EXACT_CONTENT_S11.json`; prior independent data `certificates/INDEPENDENT_EXACT_S11.json`; standalone vectors in Appendix A, Base 11.
- Base 15: c_s^+ = 1037970703125; exact data `certificates/EXACT_CONTENT_S15.json`; prior independent data `certificates/INDEPENDENT_EXACT_S15.json`; standalone vectors in Appendix A, Base 15.
- Base 19: c_s^+ = 116490258898219; exact data `certificates/EXACT_CONTENT_S19.json`; prior independent data `certificates/INDEPENDENT_EXACT_S19.json`; standalone vectors in Appendix A, Base 19.

`verify_finite_certificates.py` is fresh code written for this note. It reconstructs q-binomial coefficients using q-Pascal, the reciprocal transform, and permutation determinants of size at most four. It reads the copied certificates only to compare outputs and to verify the Bezout witnesses. `FRESH_FINITE_CHECKS.json` records complete agreement. The independent predecessor method used subset enumeration and direct full-degree determinants; its programs were never run here.

The s=7, p=13 boundary calculation in Section 11 can be reconstructed directly from the base-7 coefficients and finite-field polynomial division. It demonstrates why delta and same-component selection are necessary. The general all-component and norm-unit assertions are not premises of any theorem.

## Exact source provenance

The following files were read as inert text or JSON. They are inputs, not public citations or substitutes for the manuscript proofs. Exact hashes allow matching the mathematical draft to its accepted source scope. All source programs remained inert.

- `research_finalization_0923/algebra/final_v1/FINAL_THEOREMS.md`
  SHA-256 `32420b974fe980350a45021097b88259ba9219f81e1dadcf4d4a8094bd611f61`; 21932 bytes
- `research_cycle_0958/composite_guard/final_v1/COMPOSITE_GUARD_EXTENSION.md`
  SHA-256 `ef48feecd50dfcccba0c8fc7345c256d2cffb2800d5ae5bec63019a541db8b97`; 13051 bytes
- `research_cycle_0958/augmented_content_followup/final_v1/AUGMENTED_CONTENT_FOLLOWUP.md`
  SHA-256 `acd4ef8a962a5401d74fea98d7e712830b96aedde3fc786661e9750a19d335a8`; 9283 bytes
- `research_cycle_0958/review/augmented_content_followup/final_v1/REVIEW_SUMMARY.md`
  SHA-256 `75a6e7e99e1576a5698cc8b50062e7e56699f5cfb1f041a4414b1ac2b8392571`; 7863 bytes
- `research_cycle_0958/review/augmented_content_followup/final_v1/ACCEPTANCE_RECEIPT.json`
  SHA-256 `5467e5b4671cd0c12ec4a5a8855bfc831875e89da786c6467ae04fe7f467b167`; 7819 bytes
- `research_cycle_0958/uploaded_primary_1040/lubinsky_comparison/PRIMARY_COMPARISON.md`
  SHA-256 `dcbf36d214e6e17bd225159d16bd5c20995a9d0b4a56c8f42e2fe383cf34b0c3`; 20710 bytes
- `novelty_catalogue_0825/master/fft_research_master_20261009/additions/0322_exact_code_and_chirp_results/diagonal_chirp_classification_0246/CLASSIFICATION.md`
  SHA-256 `c64b813620686131f520339c14a0e5efc1c859999c228c823faf68e943d5a0b1`; 18257 bytes
- `research_cycle_0958/augmented_content_followup/final_v1/EXACT_CONTENT_S3.json`
  SHA-256 `951e09ec296bee0c318d402d2e38f1b5e7039cf7a488a044e9af88b8318b9cc1`; 871 bytes
- `research_cycle_0958/review/augmented_content_followup/final_v1/INDEPENDENT_EXACT_S3.json`
  SHA-256 `d316c9baa6895ce7053f024dbc13f122e12bdc1cb357995119842664478ecc7f`; 1332 bytes
- `research_cycle_0958/augmented_content_followup/final_v1/EXACT_CONTENT_S7.json`
  SHA-256 `2332ef12ae67bbd8cef61288ee802e019feb33820854097fa82eb5cd71a0a2da`; 1566 bytes
- `research_cycle_0958/review/augmented_content_followup/final_v1/INDEPENDENT_EXACT_S7.json`
  SHA-256 `42cec020ecb45f85e93d2f1dfeb384b53ae3e6bce763db1840a8618ea977f42a`; 1999 bytes
- `research_cycle_0958/augmented_content_followup/final_v1/EXACT_CONTENT_S11.json`
  SHA-256 `2dceb53f5db511496325aa4484710bef234095f2ee08e6d1779f325d826e8b9f`; 2827 bytes
- `research_cycle_0958/review/augmented_content_followup/final_v1/INDEPENDENT_EXACT_S11.json`
  SHA-256 `f7336b950e79c92098782f58c2548c49bb1675e9b2c6f35600325670a9466b49`; 3266 bytes
- `research_cycle_0958/augmented_content_followup/final_v1/EXACT_CONTENT_S15.json`
  SHA-256 `d4493a2250a00ccb7b5c7ab6448199dbb2e5cfd5c6acc143da5b0366a9f4924a`; 3341 bytes
- `research_cycle_0958/review/augmented_content_followup/final_v1/INDEPENDENT_EXACT_S15.json`
  SHA-256 `6ce053653cc168da344b54c66f67ddf91fc66c56ee28910fa57397ab86da448a`; 3764 bytes
- `research_cycle_0958/augmented_content_followup/final_v1/EXACT_CONTENT_S19.json`
  SHA-256 `d897395e87df445c2558f2c78b13463d6f80fd4be9bb63410441fee12f466c8b`; 8174 bytes
- `research_cycle_0958/review/augmented_content_followup/final_v1/INDEPENDENT_EXACT_S19.json`
  SHA-256 `45d18f02c2fe70337d12ecf19a481222b0720e4b5a9d36fe7590173fcd176dcd`; 8533 bytes

## Current independent review

The completed manuscript was independently accepted on 10 October 2026 as a self-contained mathematical research draft at SHA-256 `155434da08c53789edce92664c825e72c2ef7641ce405a96ec8fed4b1e0a641b`. The copied receipt and summary are in `review/`. Direct full-degree cyclotomic-field discriminants and resultants independently match every fixed-base coordinate; all printed Appendix A vectors and gcd witnesses pass. Nine exact local leading-polynomial/discriminant controls and finite-characteristic pairing/exception controls also pass. The proof review found no unreproduced inherited dependency within the stated scope.

The receipt is a joint review of this note and a separate endpoint note; the other manuscript entry is not part of this note's theorem scope. Journal acceptance, worldwide priority, arbitrary-base support and repeated-prime assertions are expressly not certified.
