# ALG-008 independent review: paid Prony-interface comparison

14 October 2026 UTC.
Decision: ACCEPT_SCOPE_LIMITED. No required repair.

The completed sub-scope is ALG-008::BenOrTiwari-Prony-interface-comparison,
with disposition CLOSED_COMPLETED_SOURCE_COMPARISON. This accepts the exact
comparison, its self-contained recognition theorem and bounded-attempt scalar
ledger. Parent ALG-008 remains TO RESEARCH at priority 42. No new canonical
claim, discovery count, global novelty, production or unrestricted FFT result
is accepted.

## 1. Exact reviewed objects

Author report: alg008_prony_comparison_2006/COMPARISON_AND_PROOF.md
SHA256 0cc96f93aba054317deb5df0903db04016ac9f722387998901f33835308443e2.

Fresh author source: alg008_prony_comparison_2006/check_fresh.py
SHA256 5d3e5d7b9f69ed7220428744c6f3ae33c4d37b0d3cd0061ea3365d501f02b628.

Recorded author results: FRESH_CHECK_RESULTS.json
SHA256 bcb2cea6c4745eb6c86da6bd9f4913d2a70fd10d54db2666820ec93e8b4b7a76.

I read the report, fresh source, result record, pinned integrated summary,
Phase19 theorem and cost ledger. The older bodies were independently inspected
from the saved Phase19 ZIP as data. Neither author code nor historical programs
were executed in this review. The author files were not edited. My separately
written control source and its output are included here.

## 2. Primary-source check

I reopened Ben-Or and Tiwari's primary paper:
https://www.cecm.sfu.ca/personal/monaganm/teaching/TopicsinCA15/BenOrTiwari.pdf

Sections 3–4 and Figure 1 (printed pp.303–304) supply the moment/Hankel and
Vandermonde reconstruction, including unknown actual sparsity below a bound.
Section 6 (p.305) distinguishes direct cubic linear algebra from the quadratic
Berlekamp–Massey variant. Section 9 (pp.307–308) identifies finite-field
root/encoding complications. The candidate accurately separates the paper's
prime-power monomial encoding from enumeration in a supplied cyclic subgroup.
The raw Fourier probes, reciprocal data, all-coordinate certificate, and full
output cost are not supplied free by that comparator. The paper's general
sampling lower bound is correctly not transferred to this restricted grid.
This is a justified source-specific match/nonmatch, not a novelty survey.

Massey's primary paper was also reopened:
https://www.isiweb.ee.ethz.ch/archive/massey_pub/pdf/BI411.pdf

Sections II–III explicitly allow finite or infinite fields and construct a
minimal shift register. That supports the cited background only. The candidate
uses Gaussian linear algebra, so its correctness and count do not depend on
an unexamined BM implementation. No inaccessible primary body is needed for
this verdict; no downloaded primary PDF byte hash is asserted.

## 3. Independent algebra audit

All crucial hypotheses are explicit: N>=2, characteristic not dividing N,
supplied primitive Nth root and validated complete power table, exact field
arithmetic, resident raw r, 1<=s<=floor(N/2), and a nonzero sparse polynomial C
with distinct exponents modulo N, at most s taps, satisfying C(S)r=e0.
The Fourier convention is positive-sign and unnormalized. It matches the
shift (Sr)_j=r_(j-1), so the spectral identity is C(omega^k)R_k=1.

This identity proves every promised spectral probe is nonzero. Computing 2s
probes uses the original N coordinates each time. Their reciprocals form an
exact sum of t distinct nonzero-node exponentials, with nonzero amplitudes.
For H_s=V_s diag(c)V_s^T, V_s is injective and its transpose is surjective;
hence rank(H_s)=t over any permitted characteristic. The leading H_t is
invertible by its squared Vandermonde determinant times the amplitudes.
No positivity, conjugation, generic-position or first-minor stopping argument
is being smuggled into that statement.

Solving H_t a=-(b_t,...,b_(2t-1)) identifies the monic polynomial A. Multiplying
out the moment equations gives V_t diag(c)(A(z_a))=0, so A has precisely the t
promised distinct nodes as roots. Enumerating all N labelled powers finds the
exponents directly. No logarithm, factorization, or source-position oracle is
needed. The second Vandermonde solve recovers the amplitudes.

On a nonpromised input the finite prefix can be misleading. The full cyclic
identity check is therefore essential, and the source implements every one of
its N equations before acceptance. Once it succeeds, Fourier diagonalization
proves all N denominators nonzero and all returned reciprocals correct. An
invalid prefix, non-grid/repeated root, singular leading system or failed
cyclic equation can decline safely. An accepted combined polynomial is unique
modulo z^N-1; this does not identify a unique graph factorization or delay
orientation.

## 4. Independent operation-count derivation

The stated bound applies to the actual counted fresh routine, not the old
historical counters. I inspected each counted call and independently obtain:

- 2s dense probes: 6Ns
- Reciprocal samples: 6s+1
- s-by-s rank reduction: at most 2s^3-s^2+s
- Two augmented solves: at most 4s^3+2s^2
- Right-hand-side negation and Vandermonde build: s+(s^2-s)
- N-node polynomial scan, cyclic certificate, denominator streams: 6Ns
- N output inverses: 3N+1

The sum is exactly 6s^3+2s^2+12Ns+7s+3N+2. The rank term includes up to s
pivot inversions, s^2 normalization products and 2s^2(s-1) elimination
operations. Each augmented solve costs at most 2s^3+s^2. Early exit and skipped
zero pivots/elimination factors cannot increase these estimates. The extra
backward product at each batch-inverse step is included.

Thus O(Ns+s^3) covers both complete promised recovery and a bounded attempt on
arbitrary input. Supplied roots/field validation, indexing, comparisons,
containers, bit widths, memory and physical-resource behavior remain separate.
O(N+s^2) stored field entries is stated accurately. The paper does not silently
replace s^2 by N. A primitive Nth root alone does not justify the historical
Bluestein fallback; the report explicitly withholds that general-field claim.
For growing s, an all-input fallback also retains the s^3 attempt cost.

## 5. Independent fresh controls

I wrote independent_controls.py without importing the author's or historical
code. It uses a small exact field implementation, direct Fourier oracles and a
leading-order reconstruction loop. The latter is deliberately a control
algorithm and is not claimed to achieve the accepted O(s^3) implementation
ledger. Its output INDEPENDENT_CONTROL_RESULTS.json is PASS:

- Every one of the 64 GF(4)^3 inputs, with a characteristic-two extension field,
  agrees with a full-spectrum inverse-support oracle; 9 are accepted
- Every one/two-tap polynomial over GF(13) at N=6 is examined: 2,232 total;
  720 singular polynomials are excluded and all 1,512 invertible cases recover
  their exact support, coefficients and all six outputs
- A changed Fourier coefficient outside the four training probes preserves
  those probes exactly but is rejected by the complete cyclic certificate
- 2,500 exact ledger-polynomial identities check the independently summed
  count against the displayed closed form

These controls add extension-field and non-power-of-two coverage; they do not
establish the theorem by extrapolation or validate any historical executable.
The author's 29,204 decisions and 10,506 output checks were read as a separate
record and statically cross-checked against source, not represented as my run.

## 6. Disposition

Accept the one-primary-comparator stopping condition and the accurately paid,
exact recognition contract at the frozen source hashes. No repair is required.
Keep the parent TO RESEARCH/42, historical source qualifications and all
broader unresolved gates. In particular, this does not certify a general
sparse rational numerator/denominator algorithm, stable floating-point
recovery, a bit-complexity improvement, arbitrary-field FFT fallback, historical
Green admissibility, production wiring, practical speed or worldwide priority.
No external state was changed by this review.
