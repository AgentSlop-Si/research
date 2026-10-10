# Local discriminants and composite squarefreeness research draft

The standalone mathematical note is manuscript.md. It contains proofs of the local splitting and ordinary-discriminant coefficients, the characteristic-zero parameter disk, uniform resonance, the finite-characteristic inverse-pair exception, exact cyclotomic bridges, and the five fixed-base infinite families. It includes a complete, grammar-scoped scalar-bank application and a finite certificate appendix.

Main theorem: for s in {3, 7, 11, 15, 19}, prime p congruent to 1 modulo 4 and p not dividing s, H_((sp-1)/2)(z; zeta_(sp)) is squarefree. The s=15 family excludes p=5. Arbitrary composite and repeated-prime orders remain open.

Mathematical proof completion and publication priority are different statuses. The text has passed independent review as a self-contained mathematical research draft at its exact recorded hash. This remains a research draft. Classical ingredients are attributed to Lubinsky and Saff 1987; Zhedanov 1997 and the earlier citation chain remain comparison tasks. No author, journal acceptance, or first-publication claim is assigned.

## Contents

- manuscript.md: complete mathematical text and bibliography
- REFERENCE_CERTIFICATE_INDEX.md: sources, formula locations, finite data, and scope
- SOURCE_PROVENANCE.json: exact source hashes; source programs were inert
- certificates/: exact coefficient data and prior independent reconstructions
- verify_finite_certificates.py: freshly authored exact reconstruction, using local JSON only
- FRESH_FINITE_CHECKS.json: successful results of that reconstruction
- MANIFEST.json: hashes of the current files

The fresh checker uses Python's standard library. From this directory run `python verify_finite_certificates.py`. It constructs cyclotomic polynomials by exact division, reconstructs Gaussian coefficients by q-Pascal, uses reciprocal degree reduction, evaluates permutation determinants of size at most four, and compares every exact coefficient field. It does not execute the predecessor programs. The manuscript provides the reconstruction procedure independently of this code.

The original third-party papers are not redistributed in this directory. The bibliography links to legitimate sources; the supplied scan is represented only by its provenance hash and the attribution comparison.

The publication export records the independent mathematical acceptance scope and exact manuscript hash in [the public review-status certificate](../../MANUSCRIPT_REVIEW_STATUS.json). Independently authored mathematical controls are in ../../current/independent_manuscript_controls/. This status does not certify publication priority or journal acceptance.
