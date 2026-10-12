Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: a0e9a0de8a3efd78bae44299652ed8d86cdbcd2d8f8d6b288f642e10ed24aa59

---

# Q19 exact-rational curvature certifier: independent source-bound review

Date: 11 October 2026. Verdict: **ACCEPT, bounded reference-implementation scope**.

This review accepts the successful certificates returned by the frozen revision-2 implementation of the already accepted P11 §2.7 rational-data construction. It does not establish a new curvature theorem, certify the original NumPy program, establish worldwide novelty, or close production implementation. Admission caps are not a promise that every admissible input completes: a mathematically valid input may exceed the rational-work budget and return no certificate.

## 1. Frozen review targets

- `evidence/curvature_certificate.py`, SHA-256 `2a1c13756fc7ba0ea4cd3deb0b0ec70a2232c6d80b6fb3459501fcdfd2ac6760`.
- `evidence/CONTRACT.md`, SHA-256 `b1b2a7c26e560abc1c305e48746b31bf1fa6532ce1fdadd063085bca464f48e0`.
- Accepted predecessor: `evidence/P11_ACCEPTED_PROOF.md`, SHA-256 `9be4a2795988244f0658fc9e90c0e7181d5d02a0325a738ee2045e3b4377ddfa`, especially §§2.2–2.4 and 2.7.
- Acceptance record: `evidence/BASELINE_REVIEW_DECISIONS.json`, SHA-256 `bdc860f29e131a0eeeb99e06a2c21506a0ef54a61ca7d1c6c121eaf569b20d0c`, entry R29.

Snapshots above were copied after the author's explicit freeze, hashed before testing, and checked against the unchanged author files afterward. The author's fresh-controls script was not used as an independent oracle. The reviewer executed only newly authored candidate/reviewer code and installed ordinary libraries. No original uploaded research program was executed, imported, compiled, or AST-parsed.

## 2. Exact accepted scope

The supported interfaces are `certify(data)` and the JSON-file CLI. Arithmetic helper functions are internal, not separately capped public APIs.

- Even integer `4 <= s <= 32`, `N=s²`, and the declared half-row shift `tau(sx+y)=sx+(y+s/2 mod s)`.
- Normalized complex Fourier target `U[k,j]=exp(-2πikj/N)/sqrt(N)` with negative exponential; it is unitary, and `sqrt(N)=s`.
- One through eight nonempty layers, at most 64 total occurrences; each occurrence contains a fully supplied route and all N weights.
- Exact complex coordinates represented as JSON integers or rational strings, with each input numerator and denominator bounded by 256 bits. Floats and booleans in numeric fields are rejected. This is not an enclosure of uncertain measured input.
- A rational nonnegative `beta >= |alpha|` per complex coefficient; a single exactly unit-modulus rational-complex phase vector d shared by all occurrences.
- Every pi must be a bijection of 0,…,N−1 and commute exactly with tau.
- A common rational `0 <= rho < 1` bounds both every actual weight modulus and every reference constant modulus.
- The actual/reference matrices, layer order, and common-gauge construction are precisely those in the frozen contract. Precision p is an integer from zero through 256.

The actual target is the network declared by this data, with no additional unstated endpoint transforms. A returned positive floor bounds both `||U−T||₂` and `||U−T||F/sqrt(N)`. A zero floor is inconclusive, not evidence of equality.

## 3. Mathematical and code audit

### Validation and normalization

`integer` uses exact Python-int type, preventing bool indices, dimensions, and precisions. The rational reader similarly rejects bools, floats, unsupported coordinate types, malformed rationals, and input integers above its bit cap. Complex pairs must be lists of length two. The route checks validate every index, uniqueness, and exact tau commutation. Every phase and occurrence weight is checked, including zero-coefficient occurrences. The size cap is checked before forming the tau array.

The exact squared-modulus test with beta nonnegative is equivalent to the required coefficient bound. The exact unit test makes conjugation a legitimate phase inverse. Thus the computed reference weight is exactly `c*d_i/d_pi(i)`. Strict damping and permutation support imply `||P||₂ <= rho` and `||P0||₂ <= rho`; Neumann's series gives legitimate actual and reference inverses with common norm upper bound `g=1/(1−rho)`. No approximate invertibility check or unstated conditioning assumption is used.

### Energies and propagation

For the stated row-route convention, exact tau commutation gives

`||[P,Pi]||F² = sum_i |w_i−w_tau(i)|²`.

The reference energy is exactly `||P−P0||F²`. Both are summed over all occurrence edges and weighted by beta, not by an approximate coefficient modulus. Put `a=max_l sum_t beta`, `A=sum beta`, and `B=(a*g)^(m−1) g²`. Resolvent and product identities, triangle inequalities, and weighted Cauchy–Schwarz imply

`||[T,Pi]||F <= B sqrt(A E_raw)` and `||T−T0||F <= B sqrt(A E_flat)`.

The predecessor's all-size normalized commutator identity is `||[U,Pi]||F=sqrt(2N)`. Therefore the raw relative-Frobenius bound is

`max(0, (sqrt(2)−B sqrt(A E_raw/N))/2)`.

For the flat reference, conjugating all terms by the same unitary D produces a Pi-commuting network. The predecessor's unitary-gauge estimate, together with `2/[s sin(pi/s)] <= 1/sqrt(2) < 3/4`, supplies the conservative uniform floor 1/4. This gives

`max(0, 1/4−B sqrt(A E_flat/N))`.

Both imply the operator lower bound because `||X||₂ >= ||X||F/sqrt(N)`. The flat constant requires unitary phases; the implementation explicitly enforces that restriction. Neither optimization over reference gauges nor arbitrary nonunitary gauges is claimed.

If A=0, every beta and alpha is zero, and m≥1 implies T=0. Both target distances then equal one. The implementation's special branch is valid. A vanishing layer or coefficients with loose positive beta can also make T zero without triggering this branch; returning a weaker floor remains sound.

### Outward radicals and downward floors

For nonnegative x=n/d and scale q=2^p, `k=isqrt(floor(n q²/d))` is exactly the largest integer satisfying `k²d <= n q²`. Hence k/q is a lower endpoint; k/q itself is the upper endpoint only when equality holds, otherwise (k+1)/q is an upper endpoint. This is integer reasoning, independent of floating-point error models.

The implementation takes a lower endpoint for sqrt(2), upper endpoints for subtracted energy radicals, and then rounds the nonnegative floor downward to the p-bit dyadic grid. It takes the maximum of two separately valid floors. No operation can increase the certified bound. This proof covers all successful admitted calls, not merely the finite tests.

## 4. Resource repair and boundaries

The initial source could accept small exact input whose accumulated denominator exceeded Python's default 4,300-digit integer serialization limit. This caused output failure to be classified as invalid input. The reviewer identified the gap before acceptance.

The frozen revision adds `ResourceExhausted`, checks stored rational numerators/denominators against 4,096 bits throughout accumulation and final expressions, and gives CLI exit code 3 with `resource_exhausted`, without a floor or Fourier-rejection decision. A fresh 4,018-byte fixture with s=8 and 64 distinct 127-bit prime weight denominators independently exercises this path. Callable and CLI behavior both pass. This is an arithmetic-budget abort on data that can be mathematically valid.

The cap is checked after the corresponding exact arithmetic expression. Temporary integers can exceed 4,096 bits, notably in complex products and in the bounded-exponent construction of B. The input object and JSON parser also consume memory outside that arithmetic budget. This is therefore a logical stored-rational cap, not a physical-memory, wall-time, operation-count, or hostile-input service guarantee. The contract states these boundaries.

The CLI reads at most 2 MiB plus a sentinel before JSON parsing. API callers already own their Python objects; the CLI byte cap is not an API acquisition guarantee. Parsed input is O(E) cells and per-occurrence temporary arrays are O(N). Route validation is paid. Exact-arithmetic operation count is O(E+N+m), with bounded exponentiation and three integer square roots; gcd, integer bit growth, parsing, and serialization costs are additional. No O(E) bit-time claim follows.

The runtime used for testing has Python's default 4,300-digit serialization threshold. Every completed stored-rational output is below that threshold; square-root endpoints are also bounded by the guarded radicands and p<=256. Arbitrary external modification of interpreter state, out-of-memory termination, OS/I/O errors, and hostile-environment hardening are outside this acceptance.

## 5. Fresh independent checks

All checks passed; evidence and runnable test scripts are included.

1. `tests/independent_matrix_checks.py` imports no candidate code. Four independently generated networks with nine total occurrences produce 18 exact rational-complex constituent inverses. It verifies both-sided inverses, the commutator and resolvent-difference identities, raw/flat Frobenius energies, common-gauge conjugation, Pi commutation after conjugation, and four pairs of full-network propagation inequalities. Coefficients and phases include genuinely nonreal rational values; one test has zero network and another has an exactly flat reference.
2. The same script constructs the N=16 target in the exact cyclotomic field `Q[z]/(z^8+1)`, with no floating Fourier matrix. It checks unitarity, exact commutator Frobenius square 32, and `(Pi U⁻¹ Pi U)^4 = −I`. This finite calculation checks conventions; the all-size result remains the predecessor theorem.
3. `tests/candidate_adversarial_checks.py` independently recomputes all certificate energies, bounds, radicals via integer binary search, and rounded floors for 96 generated inputs at s=4,6,8,10. Four additional cases cover loose zero coefficients, a vanishing layer, exact complex coefficient/damping boundaries, and N=1,024 with maximum precision.
4. The same script checks 42 malformed/unsupported inputs, the distinct denominator-growth resource abort, the CLI input-byte cap, and SHA-256 binding of successful CLI output to the exact input bytes.
5. `tests/outward_root_checks.py` checks 1,135 outward radical enclosures against a separately written exact integer binary-search oracle, including zero, exact squares, near-square values, small/large numerators and denominators, and p=0 through 256. It also checks the oversize-radicand budget guard.

Test evidence supports the implementation audit but is not a substitute for the inequalities and rounding proof. The author's separate test counts are not counted as reviewer tests.

## 6. Disposition and permitted status wording

**ACCEPT:** bounded exact-rational reference certifier implementing existing P11 §2.7, with a 4,096-bit stored-rational budget, exact validated inputs, rigorous dyadic floors, and explicit resource-exhaustion semantics.

Suggested Q19 status addendum:

> Independent source-bound review accepts the bounded exact-rational reference certifier for the existing P11 §2.7 theorem. Successful outputs rigorously bound operator and relative-Frobenius distance; valid inputs can instead return resource_exhausted. General uncertain-input certification, optimized/streaming production implementation, practical performance and physical-resource guarantees remain open. The original NumPy diagnostic remains uncertified.

Do not change the mathematical proof's acceptance, novelty rank, canonical theorem counts, or distinct projective/phase-cone theorem identities on account of this implementation review. No Sheet or GitHub edits were performed by this reviewer.
