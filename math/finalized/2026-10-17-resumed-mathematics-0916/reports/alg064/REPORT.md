# ALG-064: an exact-data bridge to certified numerical output

17 October 2026. **New bounded reference-integration result. ALG-064 stays TO RESEARCH, priority 42.**

## 1. What this gate resolves

The current owner at repository commit `bcbc3854c9af6bac7ccaf8378c1629ae63889fbb` records an accepted numerical evaluator **conditional on supplied complex dyadic connection coefficients and certified Fourier nodes**. Its remaining interfaces include coefficient discovery/representation, node generation and total certified fallback. This report selects a concrete exact-data bridge through those interfaces. It does not repeat or replace the supplied-coefficient theorem.

The new reference pipeline takes only a finite raw complex dyadic vector, a recurrence cap and a rational absolute tolerance. It obtains an exact rational recurrence when the cap permits one, rounds its possibly non-dyadic coefficients with a proved defect budget, constructs all Fourier nodes with rational error certificates, and applies the accepted evaluator. Cap failure receives a separately charged direct certified transform. Thus neither coefficients nor roots nor fallback are left as free oracles in this reference implementation.

This is **exact rational discovery for exactly represented data**, not stable inference from noisy observations. The discovery is deliberately a slower full rational linear solve, not a replacement claim for the already accepted field-operation synthesizer. The fallback and node constructor are reference algorithms with explicit finite costs, not optimized FFT implementations. No practical-speed, worldwide-priority, historical-source integration, arbitrary-input complexity improvement or whole-owner closure follows.

### Pinned dependencies

- [Current open owner](https://github.com/AgentSlop-Si/research/blob/bcbc3854c9af6bac7ccaf8378c1629ae63889fbb/math/finalized/2026-10-15-rebuilt-open-record-index/open-record-index.json), ALG-064 only.
- [Accepted supplied-coefficient numerical theorem](https://github.com/AgentSlop-Si/research/blob/5f76c073d35877c12d4d57be1e5e0cb3321dfa35/math/finalized/2026-10-17-research-finalization-0110/reports/alg064/REPORT.md), Sections 2, 4–6.
- [Accepted capped exact-field constructor](https://github.com/AgentSlop-Si/research/blob/bcbc3854c9af6bac7ccaf8378c1629ae63889fbb/math/finalized/2026-10-16-research-finalization-1412/algorithms/REPORT.md), Section 2, including the declared-span convention and completed classical synthesis comparison.

Those dependencies were read as text. No historical code was imported, executed or compiled. `reference_pipeline.py` and `checks.py` were newly authored for this gate. The source register binds the read bytes. Public proof/source links contain no new native owner mapping.

## 2. Input/output contract

Let N>=1 and 0<=d<N. Each component of x_j is an exactly represented integer multiple of 2^(-b), with the actual numerator and denominator lengths charged. Let 0<epsilon<=1 be an exactly represented positive rational. The target is the complete unnormalized **positive-exponent** DFT:

    X_k = sum_(j=0)^(N-1) x_j exp(2 pi i kj/N),  0<=k<N.

The result contains all N complex dyadic outputs y_k, with max_k |y_k-X_k|<=epsilon. Neither a relative-error guarantee nor real-transform normalization is implied. N=1 is exact copying. Cap d=0 accepts only the zero vector; otherwise it uses the certified fallback. Empty input, non-dyadic raw data, malformed cap and out-of-range tolerance are rejected as invalid interface calls.

For d>=1 the returned connection always has **declared span d**, even when its degree r is smaller. The recurrence is asserted for j>=d and the boundary polynomial retains d coefficients. A startup impulse with C=1 is not silently treated as a span-zero recurrence.

No fixed RAM/time/word budget is promised for arbitrary-size input. The mathematical algorithm terminates for every finite valid input under sufficient storage and unbounded exact integers. A host allocation failure is an execution failure, never a certified answer. The reported finite regression has its own explicit bounds.

## 3. Exact discovery and the coefficient-height guard

Build every equation

    x_j + sum_(i=1)^d c_i x_(j-i) = 0,  d<=j<N,

with c_0=1. Write c_i=u_i+i v_i. For x_(j-i)=a+i b, insert the real block [[a,-b],[b,a]] in a real linear system with 2(N-d) rows and 2d unknowns. Multiply the entire system by 2^b to obtain integer matrix and right-hand side.

Exact rational Gauss–Jordan elimination uses row swaps and the first available nonzero pivot column, with exact zero comparisons. Set free variables to zero. A zero coefficient row with nonzero right-hand side rejects the cap. Otherwise the resulting coefficients are verified against **all** original tail equations before conversion.

**Soundness/completeness at the cap.** A consistent system returns a span-d recurrence. Conversely, any recurrence of declared span L<=d can be zero-padded to length d and satisfies every equation beginning at d. Thus consistency is equivalent to existence of some admitted span at most d. The solver is not claimed to return the minimal span. Prefix-only fitting is insufficient and is never substituted.

**Height bound.** Let U>=1 bound the absolute integer entries after clearing the raw dyadic denominator, including the right-hand side, and let B=ceil(log2(U+1)). For a selected pivot set of size s<=2d, its nonsingular integer submatrix has determinant of modulus at least one. Every s-minor is bounded by s! U^s, and the same bound applies to the column-replaced Cramer numerators. Hence each returned real/imaginary coefficient has reduced numerator and denominator length

    H_c = O(d(B+log(d+1))).

This includes arbitrarily small nonzero pivots without treating their inverses as unit-cost numbers. During elimination, normalized pivot rows are rows of B_s^(-1) A and other rows are Schur complements. Their entries are ratios of minors of size at most s+1 of the augmented integer matrix. Therefore stored reduced fractions and temporary arithmetic products have length

    H_solve = O((d+1)(B+log(d+1))).

The determinant statements here are elementary proofs of the reference ledger, not a novelty claim or an unverified citation to a floating-point conditioning theorem. The exact rational operations, including fraction reduction, are charged in Section 6.

**Conditioning obstruction.** Already N=2,d=1 and x=(2^(-q),1) require c_1=-2^q. A perturbation of the first datum by 2^(-q) halves that coefficient. There is no input-uniform bounded-coefficient or finite relative-condition-number claim. Exact bit arithmetic pays for this case; it does not resolve stable numerical recognition.

## 4. New rational-to-dyadic bridge lemma

Put S=sum_j nu(x_j), where nu(z)=|Re z|+|Im z|, and use the conservative threshold

    tau=(2N)^(-d).

Let exact discovery return c_0=1,c_1,...,c_d. Choose b_c>=b and h=2^(-b_c) satisfying

    h <= epsilon*tau / [8 d(S+1)].

Round each real/imaginary part of c_i, i>=1, to the nearest multiple of h. Retain c_0=1 exactly. Then nu(c_hat_i-c_i)<=h, including halfway ties. Denote the rounded connection by C_hat and retain declared span d.

For the exact defects of the rounded coefficients,

    e_j = x_j + sum_(i=1)^d c_hat_i x_(j-i),  d<=j<N,

submultiplicativity of nu and the exact original recurrence give

    R = sum_(j=d)^(N-1) nu(e_j)
      <= sum_(i=1)^d nu(c_hat_i-c_i) sum_(j=d)^(N-1) nu(x_(j-i))
      <= d h S
      <= epsilon*tau/8.

This is the missing coefficient-conversion interface. It does not assume the rational coefficients are already dyadic, well-conditioned or small. Actual R is recomputed exactly across the full tail. If a future adapter supplies bad coefficients or a failed residual certificate, the result cannot enter the certified recurrence branch.

The rounded degree r may drop or remain below d. Since tau=(2N)^(-d)<=(2N)^(-r), the accepted denominator lemma still bounds the suspect set by r<=d. The proof is applied with a conservative smaller threshold, not with an incorrect identification r=d. The exact boundary polynomial A retains the declared length d. With the common grid 2^(-b_c), its coefficients are exact at grid 2^(-2b_c).

Choose p>=2b_c and rho=2^(-p) by exact comparisons until the accepted evaluator's inequalities hold:

    rho <= 1/N,
    3d(H+2)rho <= min(tau/4, epsilon*tau/[8(S+1)]),
    3d(K+2)rho <= epsilon*tau/8,
    3N(S+2)rho <= epsilon,
    rho <= epsilon/4,

where H=sum nu(c_hat_i) and K=sum nu(A_j), computed exactly. The previous theorem now supplies every regular/suspect-bin error bound. The implementation uses exact squared-modulus classification and separately rounded division. It does not inherit floating batch-inversion stability.

## 5. Paid certified nodes and total fallback

The node constructor is freshly implemented with rational arithmetic. It uses

    pi = 16 atan(1/5) - 4 atan(1/239).

This identity follows from rational tangent addition/doubling and locating the angle in the first quadrant. The alternating arctangent series has error at most its first omitted term. Each series stops when that term is <=rho/1280. Thus the exact rational sum has pi-error <=rho/64. Rounding it to grid 2^(-(p+8)) adds its explicitly computed absolute rounding difference; call the resulting bound e_pi.

For centered k, |2k/N|<=1, set a=(2k/N) pi_hat, and verify |a|<4. Choose a Taylor degree m with

    4^(m+1)/(m+1)! <= rho/64.

Compute sine/cosine Taylor sums exactly at the rational a, then round their components to grid 2^(-(p+4)). Derivative magnitudes of sine/cosine are at most one, so each component receives angle error <=e_pi and Taylor error <=rho/64. The computed l1 node radius is

    2 e_pi + 2*4^(m+1)/(m+1)! + actual l1 final rounding error <= rho.

This is also a Euclidean-complex radius and meets the evaluator's node premise for every N, including odd and non-power-of-two lengths. There is no running-root error accumulation and no uncharged precomputed root table. Every node is constructed, certified and read.

When the cap is inconsistent (or an injected adapter coefficient fails verification), select p>=b with rho<=1/N and 3N(S+2)rho<=epsilon. Construct the same certified node table and evaluate the original N-term polynomial separately at every node by grid-rounded Horner. The accepted elementary Horner bound certifies each output. This is an explicitly **O(N^2)**-arithmetic fallback. All failed discovery work is retained in the invoice. It makes the exact-data reference total, without claiming FFT-speed fallback or improved arbitrary-input complexity.

## 6. Complete cost and storage ledger

Let A(t) bound a rational/integer operation on O(t)-bit operands, including actual multiplication M(t), integer division D(t), gcd/fraction reduction G(t), addition, comparison and copying. For example one can conservatively take A(t)=O(M(t)+D(t)+G(t)+t). The word model never treats large exact fractions as constant cost. Let E be the input encoding length (including epsilon), H_solve as above, and B_eval cover actual input, rounded coefficients, boundary data, p-bit fractions, the encoded tolerance and tau. A sufficient conservative form is

    B_eval = O(H_solve + B + b_c + p + log(N+d+1) + d log(2N)
               + bitlength(epsilon) + log(2+S+H+K)).

The node constructor uses O((p+1)^2+N(p+1)) exact arithmetic operations. This includes its deliberately simple repeated factorial/power work in degree selection and arctangent terms. With m=O(p+1), a conservative rational operand bound is

    H_root = O((p+1)^2 * (p+log(N+1)+log(p+2))).

This loose bound follows by bounding all denominator products, factorials and powers in the finite sums; no cancellation is needed to justify it. It is intentionally not advertised as an optimal root-generation algorithm.

Cumulative successful recurrence-branch costs are:

| Stage | Operation count / charged width | Storage |
|---|---|---|
| Read/validate raw data and clear dyadic scale | O(E) bit reading plus O(N) exact operations | O(N) data words |
| Full cap system and exact Gauss–Jordan solve | O(N(d+1)^2) operations at H_solve bits | O(N(d+1)) fractions |
| Full exact verification, coefficient rounding, boundary/defect formation | O(N(d+1)+b_c+p) operations at the relevant bounded widths | O(N+d) beyond solver |
| Certified pi and N nodes | O((p+1)^2+N(p+1)) operations at H_root bits | O(N) node words |
| N denominator/boundary evaluations and regular divisions | O(N(d+1)) operations at B_eval bits | O(N) output/node words |
| At most r<=d direct suspect evaluations | O(Nd) operations at B_eval bits | O(1) extra beyond input |
| Output | N writes and actual output bit length | N output words |

Thus one explicit conservative successful-branch bit bound is

    O(E + N(d+1)^2 A(H_solve)
       + (N(d+1)+b_c+p) A(B_eval)
       + ((p+1)^2+N(p+1)) A(H_root)),

with actual output-bit writing included or added explicitly. Solver memory may be released before numerical evaluation, but its O(N(d+1)) fraction allocation is still charged. The Fraction implementation is a reference for this bound, not a claim of minimum-gcd or minimum-division execution.

A rejecting run pays all performed solver/validation work, then its separately selected fallback root cost plus O(N^2 A(B_eval_fallback)) and N output writes. The algorithm does not reuse a nonexistent successful solve or discard the cost of failed prefixes. The exact constant factors and Python wall time are not performance evidence.

## 7. Verification and stopping condition

Run `python checks.py` inside this directory. Only the newly authored reference module is imported. The checker writes `CHECK_RESULTS.json` and `OUTPUT_VECTORS.json`, with exact rational raw data, outputs and error bounds. Its output oracle uses a direct power-sum at tighter certified nodes, distinct from the pipeline Horner path. Independent review must not treat that common node implementation as an independent transcendental oracle; a separately authored node formula can validate the saved outputs as inert data.

Controls include non-dyadic discovered coefficients, complex rational recurrences, repeated roots, near resonance, odd lengths, trailing-zero connections with longer declared span, late-tail cap rejection, tiny pivots, absolute sign/normalization sentinels, malformed domains and deliberate coarse coefficient rounding. The frozen author regression passes 102 pipeline cases, including 70 recurrence branches, 21 certified direct fallbacks, 10 zero cases and one N=1 copy. It checks 1,001 numerical output bins, 1,089 exhaustive cap-one decisions, 28 cases with non-dyadic exact coefficients, 21 suspect bins and 12 negative controls. Maximum working fractional precision is 298 bits; tested N ranges from 1 to 32. Full exact counts and case data are stated in `CHECK_RESULTS.json`; these support transcription and integration, not an all-size proof by testing.

During expanded testing, exporting the exact internal node-radius fractions exceeded Python's integer-to-decimal safety limit; all mathematical checks before serialization had passed. The final implementation compresses only the receipt radius by outward dyadic rounding, verifies that rounded bound remains <=rho, and reruns the entire regression. The frozen output files were produced by those repaired bytes.

**Bounded gate disposition:** the exact raw-dyadic discovery-to-rounded-coefficient numerical reference interface, paid rational node constructor and paid direct fallback are complete at this report's proved and tested scope, subject to independent artifact-bound acceptance. Keep ALG-064 TO RESEARCH and priority 42 unchanged.

**Remaining separate obligations:** stable/noisy numerical recurrence recognition and conditioning guarantees; better bit-cost or efficient certified root/FFT fallback construction; non-dyadic raw encodings; normalized real-residual adaptation; integration with the original historical implementation and resource-limited production certification; machine speed and broader arbitrary-input/noncommuting targets. Do not redispatch the same exact-data reference bridge as an open oracle, and do not label these remaining broader obligations closed by it.
