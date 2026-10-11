# Independent implementation review: finite RS/Q08 certificate validator

Review date: 11 October 2026 UTC.

## Decision

**ACCEPT the narrowly repaired reference API, version `rs-q08-reference-1.1`, at SHA-256 `7cf350bfa8037e2addb3f26454a0e047b4f8df501500158292f45b9020d8a60c`, with the corrected contract below.**

The original version at SHA-256 `f18686ac29522782269c283a042ba5d42d9e9f73bd73870cc23ebae37f9ddfae` receives **REPAIR**, for two precisely reproduced API/resource-contract issues. Neither finding yielded a false mathematical certificate. The repair changes no acceptance inequality, supported profile, mathematical bound, source pin, or numerical budget. The original archive, exact patch, and both rounds of evidence are retained.

Acceptance is for a bounded standard-library reference validator on the documented Python/JSON interfaces. It is not a production, hostile-service, peak-memory, wall-time, root-solver, floating-point RS, or growing-degree stability certificate. The accepted finite mathematical theorem and Q08 fixed-degree proof remain dependencies, not new results.

## Frozen evidence and methods

- Original implementation archive: SHA-256 `940cbfb306f7cc358b4edae703cad7cf032858af0c4af2c53ea04f381105bd44`; original Library item `libfile_e3e23d9f6c888191818b94e5892f79d6`, version 0.
- All 44 original manifest members were verified by byte count and SHA-256 against the sealed archive and supplied local package. The checker was 21,280 bytes.
- Accepted finite proof: SHA-256 `3b472a7adb4a157c52c6ad4f8da5e1d94717e360bce8326e8c4d8732cfbcc100`.
- Accepted independent proof review: SHA-256 `a412af68fbeffe1d6f332280a5b59e3ac74d91481c492232981319c51e0b6033`.
- Accepted Q08 envelope, P05 Section S3: SHA-256 `02ec40df49f0585c57f98d3af7cbb9867216773f98a2998db9d51237fd69b787`.
- All eight source pins, totaling 168,073 bytes, were verified. No inherited research program was imported, compiled, AST-parsed, or executed. Historical `.py.txt` members and nested source archives remained inert evidence.
- Fresh execution used the archive-extracted checker, fresh author tests/build script, and independently authored review controls. The original candidate files were not edited. The repaired implementation was reviewed as a separate exact identity.

The reviewer read the implementation report, certificate contract, Q08 row proposal, source proof and acceptance report, and every relevant executable branch. Formula controls use direct Fraction algebra independently of the checker's Arithmetic class. The exact local-jet controls enumerate weighted subsets and work in Q(w), w^2+w+1=0; they do not import the historical controls or copy their implementation.

## Mathematical and implementation soundness

### Exact arithmetic and outward enclosures

Every positive decision is based on integer/rational arithmetic; no binary floating-point root estimate contributes to acceptance. Canonical request rationals are reduced strings with positive denominators and restricted syntax. Integer-square-root geometry computes dyadic floor/ceiling bounds and verifies their squares exactly. For b=0, the accepted radius bound is rounded upward and the gap bound downward after replacing pi by 3. The center gap 4/d is a valid conservative bound from concavity of sine on [0,pi/2]. A=1 correctly uses the zero direction, with no nonexistent direction-gap factor.

The checker uses B=(1+s^2)^h(2+sX)^n with h at least floor(n^2/4)/d. Its integer exponent therefore rounds the accepted majorant outward. The separated and overlap examples retain their previously accepted conservative exponents 3 and 4. There is no uncertified fractional-power computation.

### Strict analytic certificate

The supported geometry supplies genuine lower leading-coefficient moduli, enclosing direction radii, direction gaps, and static-center separations. The tests X>=radius+eta and 2eta<gap establish coverage and disjointness. The local comparison is exactly

    E = B r / [s^m (s-r)] < mu = c_lower eta (gap_lower-eta)^(m-1).

The factor s^(-m) is present. Exact threshold equality is INDETERMINATE. A control at r=1/1000 would pass after improperly dropping that factor, while the reviewed implementation correctly refuses certification. This is a normalization falsification control, not evidence of an actual root collision.

The code requires Delta=center_gap-2rX>0 and counts every admitted root: 3*2=6 for the separated example; 1*2+2*1=4 for the overlap example; and d*A for b=0. Thus the accepted Rouché proof supplies all roots, with no unaccounted residual roots. Unsupported residual and overlap families never inherit an asserted guard from the request.

### Complex embeddings and norm factors

The embedding index is an integer k with 1<=k<d and gcd(k,d)=1. Both primitive cubic embeddings are included. In the exceptional cubic case tau=1-w has tau*conjugate(tau)=3 and Disc(J_2) has norm 48. These are complex conjugation norms, not algebraic values incorrectly treated as positive real moduli. The ordinary overlap leading modulus 3sqrt(3) is conservatively lowered to 3. Thirty freshly computed exact local jets verify the b=0 cases A=1,2,3,4 at all three centers and both cubic embeddings, plus all six overlap center/embedding cases.

The squared inverse envelope includes n, corresponding to the required sqrt(n) before squaring. Every cluster has its own exponent m-1 and the cross-cluster exponent n-m. Singleton factors are exactly one. The forward bound is n*sum(R^(2k)), and the squared condition bound is the product of the two squared bounds.

The root tubes apply for all complex arguments with 0<|epsilon|<=r. Norm bounds apply only on epsilon_min<=|epsilon|<=r, with epsilon_min strictly positive. Shrinking epsilon_min affects the inverse envelope and does not change the root-tube proof. A requested norm ceiling is checked against the sufficient upper bound; failure does not prove the actual norm exceeds the target.

### Provenance and decisions

The source-pin set must exactly match the eight hard-coded names and hashes. Each file is re-read and hashed for each evaluation. The checker recomputes every certificate field, including input hash, checker hash, decisions, rational bounds, and cost trace, and compares canonical bytes. Eight individually modified and eight individually missing source files fail closed. Mutating each of 85 scalar leaves of a positive certificate is detected.

CERTIFIED alone means the stated mathematics is certified. REJECT denotes a broken input/provenance/certificate contract. INDETERMINATE denotes an unsupported family/cap or an unmet sufficient inequality/target. PRECISION_EXHAUSTED denotes the checked bit, step, or dyadic-resolution limit. A verified negative-decision certificate remains negative; verified=true is not an acceptance bit. Early resource exhaustion need not diagnose every other defect in the request.

## Findings and verified repairs

### R1: incorrect temporary-width claim, corrected by narrowing the contract

The original Arithmetic docstring and implementation report claimed every temporary integer was at most 2*max_bits+1 bits. This is false before checked arithmetic admission:

1. With max_bits=32 and a 256-digit input rational, parsing constructs an 851-bit integer before reporting PRECISION_EXHAUSTED. The stated bound would have been 65 bits.
2. With otherwise ordinary valid b0-hermite parameters A=2,d=3, geometry_bits=64 and max_bits=32, geometry preparation constructs a 131-bit scaled numerator before reporting PRECISION_EXHAUSTED.

Exact requests/results are in `results/R1_*`. Neither path returns CERTIFIED. The version 1.1 comments and corrected documentation now explicitly define a checked-arithmetic admission limit, not a hard allocation/peak-memory bound. The repair intentionally does not change these fail-closed outcomes or promise a tighter peak bound. This resolves R1 by making the real resource contract accurate.

### R2: non-JSON Python input escaped make_certificate, repaired

For a Python request containing s=float('nan'), evaluate correctly returned REJECT/NON_JSON_REQUEST, but make_certificate repeated canonical serialization outside its exception boundary and raised ValueError. Version 1.1 catches TypeError, ValueError and RecursionError at that boundary and returns an error envelope with exactly `format` and `result`, using format `rs-q08-certificate-error-v1`.

That object is explicitly not a decision certificate. It contains no unserializable request or request hash. verify_certificate rejects it, and its embedded status is REJECT. Ten non-JSON cases, including NaN/infinities, unsupported Python objects, mixed-key mappings, and cyclic containers, confirm the repaired behavior. Seven JSON-serializable invalid cases retain ordinary negative decision envelopes. The strict CLI parser continues rejecting inadmissible JSON directly; not every negative envelope constructible through the Python API is admissible CLI input.

### Exact identity and unchanged mathematics

Version 1.1 changes the explanatory comments, version string, and the guarded serialization/error-envelope branch only. All eleven original example outcomes, mathematical bounds, and arithmetic cost traces are identical after removing the necessary checker-version/hash/byte-count differences. New example certificates bind the repaired checker hash. Old checker-bound certificates intentionally do not transfer to a changed implementation.

The repaired implementation retains the literal `implementation_review: PENDING_INDEPENDENT_REVIEW` in deterministic results. This historical self-report is not the authority for review acceptance; this external report and its exact implementation hash are. Altering that literal would create another source identity and require re-verification.

## Fresh evidence

Both original and repaired versions pass all 30 author test groups. Independently authored controls pass on both versions, with the repaired API cases added:

- All 131 admitted (A,d) pairs, one prepared request each: 97 CERTIFIED, 34 PRECISION_EXHAUSTED.
- 300 primitive-embedding cases over prime and composite odd d: 232 CERTIFIED, 68 PRECISION_EXHAUSTED.
- 48 additional separated/overlap cases varying s, eta, X and annulus: all CERTIFIED.
- 665 outward-square-root cases, including exact dyadic boundaries and close rational neighbors through geometry precision 64.
- 30 exact cyclotomic local jets, including both cubic conjugate embeddings.
- 12 exact strictness, normalization, annulus, bit and step-budget boundary controls; the Rouché neighbors are at relative distance 10^(-70).
- 85 individually mutated certificate leaves and 16 individual source missing/modified controls: all fail closed.
- 1,500 independently seeded recursive request-leaf mutations.
- Eleven API and CLI certificate roundtrips with correct exit codes for all four decision statuses.
- Original cold regeneration: all 22 example request/certificate files byte-identical to the sealed candidate.
- Repaired non-JSON/error-envelope checks and unchanged-output comparisons described above.

The repaired independent suite completed in approximately 14.33 seconds in this environment, with observed child maximum RSS about 16,128 KiB. These are observations of this test run, not timing, peak-memory, or complexity guarantees. Tests supplement the source/proof review and do not prove arbitrary future implementations sound.

## Accepted API boundary and next step

ACCEPT covers the two published profiles and the capped b=0 Hermite family: 1<=A<=16, odd 3<=d<=31, Ad<=128, primitive embeddings, canonical rational requests, exact pinned sources, and the stated budgets and inequalities. A request inside those caps may still exhaust or be indeterminate. Source reading/JSON handling are separately bounded/documented; arithmetic-step counts are instrumented primitive counts, not bit-operation or CPU budgets.

General residual/overlap root preparation, a floating-point RS evaluation/decoding executor, production/service hardening, useful growing-degree efficiency/stability, resonance legality, and historical novelty remain open or separate. No new proof/fusion identifier is created. Q08 stays Proof closed, with an additive implementation note limited to this accepted reference API. A fresh row read is required before any consolidation. No Sheet or GitHub write was performed in this review.
