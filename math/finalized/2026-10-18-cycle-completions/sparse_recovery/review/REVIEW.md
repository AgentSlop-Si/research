# Independent final review: support-blind restricted sparse recovery

Date: 18 October 2026 UTC.

## Verdict

ACCEPT_RESTRICTED_SUPPORT_BLIND_APPROXIMATE_RECOVERY.

No blocking mathematical, production, original-binding, or stated-resource defect was found in the frozen 17-file candidate. Acceptance covers the declared nonzero, at-most-16-support, singleton-block family at M=N=2^28 and the trusted finite BUCKETS interface. With an independently uniform odd multiplier, the decoder jointly returns successfully and meets its accuracy guarantee with probability at least 2033/2048. On that event it returns at most s genuine target indices, includes every coefficient of modulus at least 2^-399, has complex error at most 2^-462 at each returned location, and has total sparse-vector error at most 9*2^-400 for R(x)/alpha.

The exact-support obstruction is also accepted, specifically for an oracle specified only by its fixed 2^-464 error radius. It is not a byte-indistinguishability assertion about the particular deterministic supplier.

This does not close ALG-034, a dense/general-block pipeline, an outer error transfer, a rounded-serial equivalence claim, or a full-N-output theorem. No practical or asymptotic speedup, amplification theorem, observed isolation certificate, external authentication, historical execution attestation, or attested random acquisition is accepted here.

## Frozen inputs and inspection

The reviewed author manifest SHA-256 is:

904fadf2b7096cd7477d2c99571db794982fdf34e1ad5f3e4a654032dba0e384

All 17 manifest entries matched their byte lengths and SHA-256 values before execution. A byte-identical local snapshot was retained. The new production decoder, author integration and replay drivers, proof, contract, status, receipts, source provenance, and relevant accepted dependency proofs and final reviews were inspected. The dependency hashes match the previously accepted supplier and nonconstant BUCKETS scopes. The new independent controls import production modules only; neither the author control drivers nor predecessor test suites were imported or executed.

The new decoder pin is:

4c45b4c85ac07a4be8d74bdc4a26846633b9e13aa5993025e51cbc83cf02ee1d

All work and artifacts are local. The author files were not changed.

## Mathematical review

### Isolation probability and retained geometry

For a nonzero difference of valuation v, multiplication by a uniform odd residue is uniform over the 2^(27-v) residues of that valuation. When v<13, precisely 2^(13-v) such residues have circular distance strictly below 8192. Their probability is therefore 1/16384. When v>=13, there are none. The strict boundary matters: distance exactly 8192 is good. A union bound over at most 120 pairs yields failure probability at most 15/2048; independence between different pairs is unnecessary.

On this event no bucket can have two source frequencies at distances strictly below 2T. The retained neighborhoods are disjoint, each has at most four bins, and there are at most 64 candidates. The exact passband observation is valid: for every signed q with |q|<=1024, [q-1536,q+1536] contains [-512,512], so the nonnegative numerator sum contains the entire denominator and K(q)>=1. Circular wrap and ties are covered.

### Thresholding and all 28 finite phase decisions

The far modes contribute at most lambda*eta with lambda<6. Thus epsilon=rho+6*eta<2*rho. A candidate cannot be a far-only bin; its unique retained amplitude satisfies |A|>=theta-epsilon>theta/2. Every mode of modulus at least 2*theta has a nearest-bin candidate because K>=1 there. Complex coefficients and arbitrary allowed tail cancellation are covered.

The implementation computes the exact integer cross product b(tau)*conjugate(b(0)). Its correction uses the conjugate of the pinned negative-sign root, giving the required positive phase. The low-bit induction and tau=M/2^(ell+1) isolate the next bit with real sign (-1)^bit. Both endpoint products are bounded in the correct outward directions; an interval containing zero is rejected.

The accepted primitive root-width argument applies at m<=28, b=256. Its Cartesian error bound is 2^-163, hence every point of the root rectangle is within 2^-162 of the true root. With epsilon/|A|<2^-62, the exact rational expression 2r+r^2+2^-162(1+r)^2 is strictly below 1/2. Consequently every returned sign interval has the correct strict sign on the good event. There are exactly 29 full calls, with no division by a noisy phase value or angle rounding.

### Amplitude conditioning and the coefficient floor

Deduplication occurs only after all 28 bits have been decoded. Geometry and distinct-support guards are valid but are correctly not advertised as complete isolation certificates. The decoder obtains each amplitude from the nearest tau=0 bin, where the exact K>=1 bound conditions the division. Intersecting the window enclosure with that bound preserves containment. The midpoint differs from K by at most 2^-478, including integer midpoint rounding. Signed nearest-ties-to-even division is correctly implemented.

The complex amplitude error is less than epsilon+2^-478+rho<3*rho, so the stated 4*rho bound is conservative. At most 16 returned errors contribute at most 16*rho in norm, while omitted modes have modulus below 2*theta and contribute less than 8*theta. Their sum is below 9*theta. The guarantee is approximate recovery with a stated inclusion floor; it is not exact recovery of every arbitrarily small nonzero mode.

### Exact-support impossibility

Both c*delta_0 and c*delta_0+delta_1 with c=2^1023+1 are canonical admitted inputs and have h=1024. Their normalized targets differ by exactly 2^-1024 at index M-1. Every ideal bucket differs by at most 3073*2^-1024<rho/4, uniformly over all schedules. A nearest Cartesian P-grid rounding of the first ideal response has error at most rho/sqrt(2)<3*rho/4 and is therefore a legal response to either input. This common response function works for adaptive schedules and unlimited calls. It prevents an unconditional exact-support guarantee; under shared random tapes, the two success probabilities sum to at most one. This argument does not assert identical outputs from the particular pinned implementation.

## Fresh independent execution evidence

The independent suite completed in about 171 seconds and passed. It executed 58 fresh actual BUCKETS calls and read 7,602,176 explicitly returned coordinates:

1. A complete 29-call replay against the independently copied original raw input, state, and sigma reproduced the entire author packet exactly under canonical serialization. This includes all output coefficients, phase margins, schedule, original-context hash, 29 supplier/header hashes, numerical ledgers, and combined costs. It returned 14 genuine locations from 16 source locations, with 36 candidates and 1008 phase decisions. Separate exact-integer comparisons verify the inclusion floor, each returned complex-error bound, and the full l2 bound. Six changed-field controls fail canonical equality: coefficient, source hash, sigma, phase schedule, provider header, and receipt.
2. A new 16-support original exercised zero frequency, a half-grid tie, alternating frequency-bit patterns, signed complex coefficients, an exact 2^-399 normalized coefficient, smaller coefficients, and a huge symbolic F=-(2^120+1). Its independent fixed sigma=1 has minimum pair separation 10240. It returned 14 genuine locations, with 34 candidates and 952 phase decisions; the exact-floor coefficient was included. Both omitted coefficients are below the required floor. All error comparisons were exact integer comparisons on a common grid.

These are one original replay and one new edge schedule, not a claim that the original production schedule was independently executed twice. The author's distinct production-plus-replay 58-call ledger was verified by the fresh exact packet reproduction, canonical packet hash, and exact sum-of-two-production-receipts-plus-comparison-envelope identities. Historical execution attestation remains excluded.

Additional controls passed: 330 exact modular-orbit/strict-boundary cases, 4020 signed nearest-rounding cases, 36 nearest-bin wrap/tie cases, all 2049 integer passband containment cases, exact rational proof-margin and resource-bound inequalities, and nine fail-closed grammar/width/candidate/window/sign probes. Source-level inspection and an AST check confirm the decoder accesses only provider.buckets and provider.window. This is a logical API property under trusted execution, not an adversarial operating-system isolation claim.

## Cost and binding review

Five provider preparations with groups [6,6,6,6,5] respect the accepted cumulative caps. The conservative six-call numeric bound is 12,602,912 below 30,000,000. The preparation/six-call/extra-window slot bound is 6,819,840 below 8,000,000. The original replay's observed maxima were 8,300,552 numeric operations, 4,238,851 allocated slots per adapter, and 8994-bit provider integers. Its separate root ledger has 77,070 records; the general conservative bound is 267,112 below the one-million cap. The 480-bit bucket and 580-bit window guards are sufficient throughout the admitted range. Consumer intermediate arithmetic fits the stated 4096-bit envelope.

All B outputs are actually produced per call and separately read/validated by the consumer. There is no free reuse across provider groups; each supplier execution, preparation, root decision, source loading, serialization, and output has a bounded charge. The very large fixed envelopes are logical binary-work/cumulative-storage bounds, not runtime or peak-memory measurements. Dense output and future exports remain additional work.

The retained-context replay binds the complete result to the supplied original raw/state/sigma. Replacing both independently retained context and result changes the statement. Correct Python arithmetic, pinned source, the accepted numerical provider contract, and no hostile private-state mutation remain necessary assumptions. The fixed demonstrations do not instantiate the independent uniform randomness assumption.

## Deliverable and release boundary

INDEPENDENT_RESULTS.json, EXACT_MARGIN_RESULTS.json, INTEGRITY_CHECK.json, retained fresh outputs, new edge input, independent source scripts, run log, VERDICT.json, and SAFE_MANIFEST.json contain the review evidence. The immutable reviewed snapshot is separately retained. Acceptance is confined to the contract summarized above. The author's sealed candidate is left intact; this independent verdict supplies acceptance without rewriting its historical pending-review status.
