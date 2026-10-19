# F020: accepted boundary b=3p

The actual continuous q-Hermite recurrence P and Gaussian Rogers–Szegő H are squarefree at b=3p whenever q has primitive order p^s and 3p<p^s, for every odd prime p. The original ordinary-square bilinear kernel is nonzero at every P root.

Read [the full proof](candidate/REPORT.md), [independent review](review/INDEPENDENT_REVIEW.md), [exact scope](CLAIM_SCOPE.json), and [acceptance bindings](FINAL_ACCEPTANCE.json). The old strict range is retained; only the boundary case is added. The combined condition is b<=3p AND b<p^s. In particular p=3,s=2 still gives b<9. All separately accepted earlier finite-order results remain intact.

For p>=5 the proof also gives the degree-2p irreducible local factor and v(Disc P_(3p))=3p(3p-2), normalized by v(q-1)=1. At p=3 a separate degree-nine exact certificate is uniform for s>=3; no generic root/discriminant valuation is asserted there.

The author passed 74 fresh exact assertions. Independent controls cover primes 5,7,11,13,17,19,23, exact triple identities at degrees 9,15,21, and a separately reconstructed p=3 certificate. The proofs are symbolic and do not extrapolate from this finite list. F020 remains open at priority 58, with F023 its alias. No historical-originality or performance claim is made.

## Reproduction

Run `python verify_package.py` from this directory to validate public bytes, source/export preservation, explicit omissions, privacy, and acceptance bindings. Candidate mathematical controls are `python candidate/check_boundary.py` and `python candidate/check_p3_certificate.py`. Independent mathematical controls are `python review/check_uniform.py`, `python review/check_exact_identities.py`, and `python review/check_p3.py`. They use Python; the symbolic scripts also use installed SymPy. They write their result files beside themselves. The mathematics scripts are retained byte-for-byte. This packaging pass did not rerun independent mathematics; original execution logs are retained.

Historical candidate/review manifests preserve the exact independently reviewed source identities, including hashes of metadata omitted or projected here. The top-level manifest is authoritative for the public tree. See [source/export ledger](SOURCE_LEDGER.json) and [explicit omissions](OMISSIONS.json). Machine-absolute paths are projected in provenance receipts; the historical `review/verify_bindings.py` helper now takes ORIGINAL_SOURCE_ROOT and requires the complete original source bundle. Use the top-level verifier for this self-contained public payload.

Only raw unrelated/private index captures and scratch work are omitted. All proof, mathematical code, exact data, acceptance texts, and consumed prerequisite proof/acceptance texts are retained. This folder is locally staged; publication is a separate sole-writer step.
