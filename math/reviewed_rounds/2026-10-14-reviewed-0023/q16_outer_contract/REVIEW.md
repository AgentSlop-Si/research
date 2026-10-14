# Independent Q16 outer-contract precision review

Verdict: **ACCEPT_STATIC_CONTRACT_ONLY**.

The recovered candidate's exact incidence rule, signed odd/even power treatment,
fixed precision J and schoolbook bit-work bound are mathematically sound in their
declared domain. No counterexample or required mathematical repair was found.
This accepts a static contract and its argument, not a production outer evaluator.
The candidate documents and historical source were not modified or executed.

## Reviewed object and integrity

The target is `q16_outer_contract_recovered_2330/` and
`Q16_Outer_Active_Coefficient_Contract_Recovered_Candidate_2026-10-13.zip`.
The ZIP SHA-256 is
`0c7f8c8c4eedf4a4f6e332e429c4a785c02c952ba1ffe4c87a51537b00f502bc`.
All 24 archive members match the corresponding directory bytes. The 22 manifest
payload hashes, manifest seal, and external ZIP seal verify. These establish
byte integrity and binding, not a digital signature or original-host attestation.

Primary audited sources are CONTRACT.md, PROOF.md, MISSING_TEST.md, README.md,
the pinned compact-window source, and the relevant all-length theorem guard and
outer-coefficient sections. Candidate and interrupted receipts are evidence to
read, not fresh independent executions. No historical Python was imported,
compiled to run, or executed; AST parsing of the source was data-only.

## 1. Exact incidence: accepted

The defining row-first stencil is k = floor(ell*M/N)+j modulo M for
-h <= j <= h+1. Lifting ell to r = ell+vN converts this exactly to
k-h-1 <= floor(r*M/N) <= k+h. For integer bounds this is equivalent to

    N*(k-h-1)/M <= r < N*(k+h+1)/M.

The proposed lower and upper signed ceilings therefore enumerate precisely the
correct integers. Since its real length is Nt/M < N, two emitted lifted indices
cannot be congruent modulo N. This proves injectivity without a deduplication
pass. An interval of length Nt/M contains at most ceil(Nt/M) integers. Each row's
t distinct retained residues give the independent per-row cap of t. Negative
endpoints require floor-based division, as stated.

The fresh independent exhaustive controls cover 121,980 (N,M,h,k) cases, including
near-maximal h, signed wraps and boundary coincidences. Both floor-upper and
closed-upper mutants are rejected. These are generic incidence fixtures, not
claims that every small fixture satisfies the theorem's sparse guards.

References: CONTRACT.md lines 23-32; PROOF.md lines 3-15.

## 2. Odd exponents and phase: accepted with explicit implementation gap

The signed endpoint formulas are the correct range of x^s on [-1,1]. Odd powers
are monotone even across zero; even powers take their minimum at zero when the
interval crosses zero. The derivative bound gives s-Lipschitz width propagation.
The pinned historical helper rejects odd exponents; it cannot implement the
required API. Both absolute-value substitution and silently forcing an even
exponent change the exact operator.

For D=5, m=57, s=285, k=1710 and ell=0, both normalized Dirichlet factors are
negative, so the signed target has the asserted positive sign. As the packet
correctly cautions, this is not by itself an eta-violating output example: the
285th power can make the coefficient tiny. The negative interval operator test
is decisive for the primitive's sign behavior, and the old helper's odd-input
rejection is decisive for API incompatibility.

The independent signed-power controls cover 32,109 intervals/exponents. The
K=623 sentinel [-1/2,-1/4]^285 has exact K-grid endpoints -2^338 and -2^53,
matching the candidate's decimal receipt. The phase formulas correctly produce
cos(2*pi*a0*ell/N) and -sin(2*pi*a0*ell/N).

References: CONTRACT.md lines 50-70; PROOF.md lines 72-76 and 112-122;
compact_window.py.txt lines 136-143.

## 3. Scalar precision and final certificate: accepted

The Scalar text agrees with the reconstructed finite recurrence: maintained
Machin powers, exact rational reduction, a K-grid midpoint with angle radius,
fixed point-Taylor intervals, factorial remainder, and analytic clipping.
The proof pays rounding width instead of assuming exact transcendental calls.
The Taylor tail proof legitimately uses the degree-2n Taylor polynomial whose
even final coefficient is zero. Fixed K+2-step sqrt bisection also encloses the
exact sqrt(M/N), with the specified strict initial upper endpoint.

For n_u != 0, b >= 2/Q with Q=NM <= M^2/4. Since epsilon=2^-J < 1/Q,
every denominator corner is positive. The crucial normalization |a/(c*b)| <= 1
gives corner error <= 2Q*epsilon; a generic unnormalized quotient derivative
would incorrectly waste another factor Q. Outward quotient width is therefore
w0 <= 4Q*epsilon+2delta.

The signed power, amplitude, and phase propagation yields

    wC <= 4*(s+1)*M^2*epsilon <= eta/64.

Thus J=(D+5)m+bit_length(s)+8 is sufficient. The selected
K=J+2*bit_length(J+1)+16 gives 64(K+9)2^-K <= 2^-J universally by the
displayed elementary bit-length argument, not by extrapolating finite tests.
Midpoint rounding to p=(D+3)m+3 has Cartesian radius at most 9eta/128.
Consequently the exact squared-radius certificate always passes for the valid
mathematical recurrence, because 2*(9/128)^2 < 1.

The floor/remainder nearest-even formula works for negative ties. Exact zero
residues take the dyadic limiting branch before division; phase zero/unit
branches likewise use exact congruences. Fresh controls include 2,700 precision
budgets, 270 normalized-quotient cases, 7,317 signed-rounding cases and 516
fixed-loop square-root cases. They supplement, rather than replace, the universal
argument.

References: CONTRACT.md lines 34-76; PROOF.md lines 17-95;
compact_window.py.txt lines 178-248.

## 4. Paid resource bound: accepted in the stated fixed-D binary model

For fixed D, s,K,n are O_D(m). Scalar calls have O(K) primitive operations,
including their Taylor and factorial loops; one-time Machin preparation and
sqrt bisection are also O(K). Each coefficient needs at most five sine calls and
O(log(s+1)) square-and-multiply steps for endpoint powers.

The controlling widths are O(K log(K+2)) for factorials and O(sK) for signed
endpoint powers and their binary denominators. Therefore

    H = O(m + K log(K+2) + sK + log(s+1)) = O_D(m^2).

Schoolbook multiplication/division/shift allocation may conservatively be
charged O(H^2). With O_D(m) operations, this gives O_D(m^5) bit work and
O_D(m^3) cumulative produced-integer bits per coefficient. The proof does not
confuse O(log s) multiplication count with constant-width powers.

Valid support has S<=M; E<=St and t=O_D(m), so control/address counters have
O_D(m) bits. Header checks, accepted-field copying, support validation and
incidence enumeration cost O_D((S+E+1)m^2). This includes the necessary header
cost at S=E=0. Lazy or two-pass setup occurs only if E>0. Absorbing Em^2 into
Em^5 establishes the exact advertised total:

    O_D((S+1)m^2 + 1_{E>0}m^5 + E*m^5).

The 32-byte association label, O(K)-bit enclosures and streamed records fit the
bound. Extra serialization, unbounded metadata, support canonicalization,
retained E-record storage and any cache/table construction must still be paid
as specified. The bound is not D-uniform and is not a CPU/RSS measurement.
No N-row preparation pass appears in the mathematical recurrence. Its absence
from future production code must be separately checked.

A second independent static check of the cost proof and Scalar source reached
the same scoped result; its concise report is included in COST_SECOND_REVIEW.txt.

References: CONTRACT.md lines 9-15 and 78-84; PROOF.md lines 97-110.

## 5. Production boundary and disposition

The static gate is closed by this review. The source-pinned outer wrapper and
its odd-exponent/minimum-residue regression remain absent. MISSING_TEST.md is an
appropriate next gate, subject to separate authorization/source inspection.
The large mathematical fixture is valid: ell=2^53 and k=2^55+1 give residue 1,
J=587, K=623, p=459, and the beta=1/8 sparse guards hold. The independent
enumerator emits 9,123 incidences across the four specified support indices
without an N-vector; this is still no production coefficient evaluation.

PRODUCTION_OBLIGATIONS.md lists what remains. This review changes no accepted
observer/front-end scope, research table, repository, novelty score or claim of
exact DFT/relative-l2 accuracy. It does not close full stream integration,
finite accumulation, scale-back, dense fallback, all-length dispatch or fresh
independent amplification.

Run timing and counter availability are recorded in STATUS.json. Only actual
observable counters are reported; no model token-use counter was exposed.
