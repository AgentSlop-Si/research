# F020: accepted single successor b=3p+1

For every odd prime p and primitive p^s-th root q with 3p+1<p^s, the actual recurrence P_(3p+1) and Gaussian Rogers–Szego H_(3p+1) are squarefree, and the original ordinary-square bilinear Christoffel–Darboux kernel is nonzero.

Read [the proof](candidate/REPORT.md), [independent review](review/INDEPENDENT_REVIEW.md), [scope](CLAIM_SCOPE.json), and [acceptance bindings](FINAL_ACCEPTANCE.json). The prior accepted range b<=3p AND b<p^s is retained. The combined range is b<=3p+1 AND b<p^s. Earlier separately accepted d=9/d=25 and fixed-residual results remain intact. For p=3,s=2 this range still means b<9.

For p>=5 the three root valuations are (2p−1)/(2p), 1, (p+1)/4, with counts 2p, p−1, 2. The ordinary X-discriminant valuation is 9p²+(p−7)/2, normalized by v(q−1)=1. Prime 3 uses a separate exact degree-ten certificate; no generic local formula is asserted there. This is not a q-discriminant claim.

F020 remains open at priority 58; F023 stays its alias. No b>=3p+2 result, entire fourth-block theorem, unrestricted all-A closure, performance improvement, or historical-originality conclusion is added.

## Verification and fresh replay

Run `python verify_package.py` from this directory to check the frozen public tree, all exported source bindings, explicit omissions, claim guards and original acceptance hashes. This is a packaging check, not a proof replay.

Run `python replay_checks.py` for all five final mathematical checker programs in isolated temporary copies. It rebuilds actual recurrences and exact certificates, comparing every output field except the explicitly nondeterministic `elapsed_seconds`; all SymPy versions and every mathematical field must match. It never overwrites frozen evidence. Python 3 and SymPy 1.14.0 were used. The checkers are byte-for-byte originals. Author finite controls cover p=5,7,11,13,17,19,23; independent finite controls additionally cover 29,31. Both exact identity programs cover degrees 10,16,22. The p=3 certificates cover orders 27,81 directly and all higher 3-power orders by degree. The unlimited-prime theorem is the written symbolic proof, not a finite-prime extrapolation.

The author/reviewer source-manifest replay helpers are administrative and omitted: they require full historical local bundles. Use the top-level verifier for this self-contained exported payload. No earlier accepted checker is rerun by the public replay. See [dependencies](DEPENDENCIES.json) for precise prior-proof/replay scope.

## Original preservation and administrative projections

All final mathematical checkers, exact data, scientific review, and consumed prerequisite texts are retained byte-for-byte. The proof's two machine-local provenance locators are replaced with neutral `original-source/` labels; all mathematical text is unchanged. The same explicit path-only projection is applied to administrative provenance receipts and one verdict directory field. [The source ledger](SOURCE_LEDGER.json) records every original/export hash and [the omissions record](OMISSIONS.json) lists every omitted development or local-only administrative file. Original historical manifests and seals are retained exactly; they describe the originals, including explicitly omitted/projected files. The top-level manifest alone describes this public tree.

Fresh native workbook captures and the inert additive proposal are excluded from publication. This is local staging. Publication and any later native application require their separate verified release steps.
