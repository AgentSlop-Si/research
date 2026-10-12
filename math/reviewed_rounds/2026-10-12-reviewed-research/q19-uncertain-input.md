Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: e5dfd49aa2534c92204d3a549a13a22d99d061b8f6a2bb365785046a032b0c5d

---

# Q19 rational-box curvature certificate: independent review

Date: 2026-10-11. Verdict: **ACCEPT, strictly scoped to the bounded reference implementation below.**

## Decision and frozen identity

The frozen candidate returns valid common lower bounds for operator error and relative Frobenius error against the specified normalized complex Fourier matrix, for every simultaneous real-coordinate selection in each admitted complex coefficient/weight rectangle. The quantifier includes irrational interior values. This is successful-output correctness for a bounded reference implementation, not a guarantee that every mathematically admissible input completes.

- Candidate archive: `Q19_Uncertain_Input_Curvature_Candidate_2026-10-11.zip`
- Archive SHA-256: `4ec5d5f5e23fe4c7a6e9e164da9b6cc6e1476b35777da5d38f6dc1d3ccd13bbf`
- Candidate code SHA-256: `9aa83f98e3bb8e4e86f77ddc7201ca97741b2dfce2b197f836f268deec95c096`
- Candidate contract SHA-256: `ee11829dc487fb759dfec2a5bcda8a2b13a6ff6bcb145c0489f7993d0f105e55`
- Candidate manifest SHA-256: `a22fcd1d41729450f6fb3f84dc5d77dc8f67f8f2445ba702f48fe325f603cb2d`
- Exact predecessor code SHA-256: `2a1c13756fc7ba0ea4cd3deb0b0ec70a2232c6d80b6fb3459501fcdfd2ac6760`
- Exact predecessor accepted review archive SHA-256: `e425303862a72004fba841d64cc18b6ae2972be00c4698cec41e1b94d1edd405`

I verified all 33 payload entries, all 35 archive members, the manifest and checksum list, the nested predecessor review checksums, and byte identity of the retained predecessor with both the accepted review and the existing accepted source. Review execution uses a fresh extraction of the frozen candidate. No original uploaded research program was executed, imported, compiled or AST-parsed. The executable reuse is the separately authored, independently accepted exact predecessor only. No candidate or predecessor source change was necessary.

## Scope and admission

The accepted wrapper schema is `q19-rational-box-v1`: even 4 <= s <= 8, N=s^2, one to four nonempty layers, at most eight total occurrences, precision 0..128, exact integer/rational endpoints with 64-bit written numerator/denominator caps, and strict rational 0 <= rho < 1. All represented alpha and weight coordinates may vary independently over their closed rectangles. Correlated subsets are covered as subsets of that Cartesian family, but correlations are not used to sharpen the result.

The common reference phase vector, each reference constant, and every route must be exact singletons. Reference phases have exactly unit squared modulus; routes must be genuine permutations commuting with the half-grid involution. Nontrivial rational unit phases are accepted. Nearly unit singletons, nonsingleton references, ambiguous routes and noncommuting permutations are refused. No tolerance, projection onto the unit circle, route rounding or nearly-unit normalization occurs.

For each actual weight rectangle W, the exact corner maximum must be <= rho^2. Every reference constant must obey the same damping bound. Every coefficient rectangle must have corner maximum <= beta^2 with beta >= 0. Equality at rho is admitted; rho=1 is refused. A zero beta never skips phase, route, coefficient, damping or shape validation. These are sufficient family guards, so refusal makes no claim that every physical member is invalid.

## Independent mathematical reconstruction

### 1. Universal outward geometry

For real intervals [l,u] and [v,w], every difference lies in [l-w,u-v]. On any interval, the maximum of x^2 occurs at an endpoint. Thus the sum of the two coordinate endpoint-square maxima is an upper bound on squared complex modulus. These statements hold for every real coordinate, with no rationality assumption on the selected value. Repeated use of an interval, shared coordinates or self-differences can enlarge the computed bound; dependency cannot turn it into an underestimate.

Every permutation-weighted P has operator norm max_i |w_i| because PP* is diagonal with entries |w_i|^2. Hence ||P|| <= rho < 1 and the Neumann series gives ||(I-P)^-1|| <= g=1/(1-rho). The exact unit reference gauge gives the identical bound for all reference resolvents. Beta bounds imply all actual and reference layer norms are at most a*g, where a is the largest layer beta sum. No numerical norm estimate is trusted.

### 2. Direct energy floors

Fix an arbitrary simultaneous selection from the input boxes, including an irrational one. The accepted P11 identities give the raw commutator and flat-reference estimates for that selection. Replacing each |alpha| by its supplied nonnegative beta and each squared difference by its uniform rectangular upper bound preserves the inequalities:

||[T,Pi]||_F <= B sqrt(A E_raw),

||T-T_ref||_F <= B sqrt(A E_flat),

where A is the sum of all beta and B=(a*g)^(m-1)*g^2. In the flat comparison, T_ref uses the same selected coefficients as T. Its phase gauge remains the single supplied common exact unitary gauge. This is essential: no coefficient uncertainty is omitted from the flat argument.

The Fourier commutator has squared Frobenius norm 2N. The triangle/commutator bound therefore gives relative Frobenius error at least (sqrt(2)-B sqrt(A E_raw/N))/2, truncated at zero. Operator error is at least relative Frobenius error. The accepted unitary-gauge Fourier floor is at least 1/4 for every even s>=4; the flat comparison then gives 1/4-B sqrt(A E_flat/N), also truncated at zero. The uniform 1/4 follows from s sin(pi/s) >= 2 sqrt(2), hence 2/(s sin(pi/s)) <= 1/sqrt(2) < 3/4. No new extension of the predecessor's gauge theorem is assumed.

Because the same computed upper bounds work for the arbitrary chosen selection, these conclusions are uniform over all real/complex values in the represented boxes. Sampling is not used to obtain this quantifier.

### 3. Midpoint-family transfer

A rectangle's rational center is inside it. Its coordinate half-width sum r bounds distance from every selected complex point to that center. Thus epsilon_t=max_i r(W_i) bounds ||P_t-Pbar_t||, and eta_t=r(alpha_t) bounds |alpha_t-alphabar_t|. The resolvent identity gives ||G_t-Gbar_t|| <= g^2 epsilon_t. Splitting the coefficient-weight difference gives the layer bound

D_l = sum_t (beta_t g^2 epsilon_t + eta_t g).

Both actual and midpoint layer norms are <= a*g. Product telescoping proves

||T-Tbar||_2 <= H=(a*g)^(m-1) sum_l D_l.

The relative Frobenius difference is also <= H because ||M||_F/sqrt(N) <= ||M||_2. Reverse triangle inequalities separately for the two error norms transfer the pinned midpoint certificate Cbar to max(0,Cbar-H). Reference data and routes are unchanged at the midpoint, so no unsupported phase or topology approximation enters this call. Rational midpoints have at most 130-bit coordinates, safely within the unchanged 256-bit predecessor input limit. If that call exhausts its own budget, the wrapper issues no floor.

The maximum of the two energy floors and the midpoint transfer remains a valid lower bound on each target error norm. It need not be monotone as an algorithmic function of arbitrary box reparameterizations; no such promise is made.

### 4. Zero case and outward roots

If A=0, all beta vanish. The coefficient corner guards force every coefficient rectangle to be the singleton zero, so every layer is zero and T=0. Both Fourier error norms are exactly one. The branch is reached only after complete structural/damping validation.

For nonnegative x=n/d and precision p, the integer-root construction yields dyadic endpoints whose squares straddle x exactly. The lower endpoint is used for sqrt(2), upper endpoints for subtracted radicals, and every final candidate floor is rounded down. Exact independent binary-search reconstruction matched all tested roots and complete certificate values. Low precision may lose a positive mathematical floor; this is valid inconclusion, not a false equality conclusion.

## Independent controls and results

All controls passed, including a second cold run with byte-identical result JSON. The author's original controls were also rerun on the frozen extraction and reproduced their sealed result JSON byte-for-byte. That reproduction is supplementary; the following reviewer controls were newly authored.

- 106 complete independent certificate recomputations, including all admitted s values, 1..4 layers, up to eight occurrences, p=0/1/31/128, asymmetric boxes, genuine zero-crossings and nonidentity exact gauges
- 37 singleton regressions preserving the exact predecessor floor
- 600 independent corner/difference/dependency cases, enumerating all complex endpoint combinations
- 3,000 standalone radical checks using an independent rational binary search, plus 318 full-certificate radical checks
- 47 independently specified typed-input/refusal controls, including unknown keys, 65-bit values, floats/booleans, unsupported structural uncertainty, near-unit phases and complex corners outside beta/rho
- A wide-box case with a positive exact midpoint floor but an inconclusive universal floor, preventing midpoint certification from leaking to the family
- Exact zero-family floor one; five zero-beta late-entry controls confirming validation is never skipped
- Strict damping equality, rho=0, near-one damping, and 64-bit endpoint/large rational midpoint controls
- A newly generated prime-denominator family triggering the 1024-bit arithmetic abort without producing a floor
- 15 CLI cases: input SHA binding, certified/inconclusive/refused/resource outcomes, nested duplicate keys, NaN/infinities, malformed UTF-8, deep JSON, oversized bytes/tokens, trailing JSON and source tampering
- 63 newly reconstructed exact complex-rational inverse checks via permutation-cycle geometric sums, with both inverse products checked
- 12 exact dense matrix inequality triples for raw commutator, flat distance and midpoint distance
- Exact Hermitian Schur/LDL positivity checks: 12 operator perturbation bounds, 54 resolvent operator bounds, 18 layer perturbation bounds and 18 layer norm bounds
- 12 exact common-gauge commutation checks
- Four additional networks with genuinely irrational complex coordinates in Q(sqrt(2),i), using 1..4 layers: exact box membership, energy and operator perturbation inequalities, and actual Fourier relative-Frobenius error checks. For N=16 the trace calculation is exact from squared-index residue counts, giving tr(U)=1-i. No floating approximation supplies these checks.

The first irrational test draft needed a reflected-comparison correction in the review harness. The corrected test was cold-rerun successfully. This was not a candidate defect or candidate edit.

## Failure semantics and resources

The public certify API is a trusted-interpreter JSON-style data API, not a hostile-object or concurrent-mutation sandbox. CLI-only byte/token/parser controls are correctly distinguished from API input acquisition. Unknown fields are rejected. The CLI's explicit invalid/refused/resource/source-integrity outputs have no metric floor; the source-tamper check rejects before executing altered predecessor bytes. Missing/unreadable source or input may produce a process error, which cannot be mistaken for a successful certificate.

The wrapper cap is 1024 bits per stored arithmetic rational and the unchanged exact predecessor cap is 4096 bits. Temporary integer operations and dyadic root scaling can exceed the stored cap before checking; this is disclosed. Denominator growth can abort even within finite shape and endpoint caps. Resource exhaustion need not mean every later mathematical guard has already been validated.

The operation-count claim is bounded exact-arithmetic O(E+N+m), including route checks, zero-beta occurrences, midpoint creation, source hashing/loading and serialization. It is not a constant-bit, physical-memory, wall-time or cancellation guarantee. Parsed input, midpoint copies and per-occurrence arrays are retained; this is not streaming certification.

## Scope and remaining work

Do not label broad Q19 implementation, uncertain topology/reference gauges, phase-cone certification, projective Fourier equivalence, primitive-holonomy rank certification, arbitrary outer endpoint gauges, hardware calibration or optimized/streaming production integration complete. No new theorem or novelty promotion is supported by this implementation review.

Only the bounded rational-box Q19 implementation scope advances. Existing exact-input acceptance and the distinct mathematical theorems remain unchanged; phase-cone, projective Fourier and primitive-holonomy claims are not cross-certified.
