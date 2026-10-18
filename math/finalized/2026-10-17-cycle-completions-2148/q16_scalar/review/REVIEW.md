# Independent final review of the fresh Q16 scalar/coefficient kernel

17 October 2026 UTC. **PASS for this numerical component and its stated binary-cost model.** This is a fresh independent rational-oracle run and a source/proof review, not an inherited historical acceptance.

## Reviewed identity and boundaries

The reviewed production file is exactly 19,568 bytes with SHA-256
`73b3bb0bebf41f7a810bf2470e9ae520bdc3e7593516850d8933dd307500091e`.
The author packet manifest is
`b9095e3cb1631cb22a90372bc9d52dc9a2cdeab51d9f202d283aa08b022e3359`.
All 28 manifest members were verified before and after the independent run.

The complete fresh production source was read before execution. The reviewer authored `independent_oracle.py` and `launch_review.py`; only this fresh oracle, a byte-identical copy of the newly authored production scalar, and Python standard-library dependencies were executed. Historical contract/archive/source material was read as inert evidence. No historical uploaded implementation was imported or executed. No external write occurred.

The reviewed parameters are N=2^55-1, M=2^57, D=5, m=57, s=285, J=587, K=623, A=456, p=459. The three selected incidences are, in order:

1. (ell,k)=(0,0), the exact zero-residue branch.
2. (ell,k)=(2^53,2^55+1), whose modular residue is exactly one.
3. (ell,k)=(0,1710), the negative-ratio odd-power witness.

The wrapper packet was checked read-only against manifest
`f14e4bbd92c98063902e262ce699bfa58c6ba4333562bbbe683deb97714dff8f`.
All 13 manifest members match. Its RESULTS hash is
`54191cc7da1439e06f39ea35fe7d4292236cfdae2ffb151156c835b5b1e198b8`.
All fields of all three wrapper CoefficientResult records exactly equal both the fresh independent-run production records and the author packet records. The wrapper scalar file is byte-identical. This establishes numerical result/source equality; acceptance of its concrete producer association and incidence iterator belongs to the separate wrapper review.

## Independent rational oracle and its guarantee

The oracle uses Fraction arithmetic and an 840-bit outward dyadic grid. Its numerical functions do not call a production numerical helper, use production scalar values as inputs, or copy production interval endpoints.

Pi is bounded using **pi=4 atan(1/2)+4 atan(1/3)**. Each arctangent is an exact 500-term rational alternating sum, bounded on the appropriate side by its exact first omitted term. The identity follows because the tangent of the sum is (1/2+1/3)/(1-1/6)=1 and the sum lies in (0,pi/2), hence equals pi/4. The combined exact rational bounds are rounded outward once. This is independent of the production Machin 1/5 and 1/239 series.

Sine arguments are reduced as Fractions modulo two and folded into [0,1/2]. Zero and half-period values are exact. For other arguments, the entire rational angle interval is evaluated with a **128-term interval Horner polynomial** for sin(x). Every interval multiplication/addition rounds outward. Its exact uniform remainder is 2^257/257!, proved by exact arithmetic smaller than 2^-840. Taylor's theorem through degree 256 applies; the even coefficient at degree 256 is zero. The oracle neither chooses a production-style angle midpoint nor uses its forward Taylor-term recurrence or Lipschitz angle-radius construction.

The root uses `math.isqrt(floor(M*2^1680/N))`; its result z is separately checked with z^2*N <= M*2^1680 < (z+1)^2*N. This gives a guaranteed [z,z+1]/2^840 enclosure without production bisection. Signed powers use exact Fraction endpoint powers, with zero included for even exponents on crossing intervals. All quotient/product operations are independent rational corner arithmetic. No floating point or empirical tolerance participates in acceptance.

For every selected incidence, each oracle real, imaginary, F, R, powered-R and nonzero denominator interval is contained in the corresponding production interval. The oracle pi and root intervals are also contained in their production counterparts. These comparisons are exact rational inequalities.

For the returned dyadic complex value, the maximum rational distance to each independent oracle coordinate interval was computed, squared, and summed. All three exact sums are at most eta^2. The complete rational bounds, independent oracle intervals, fresh production records, and recomputed production radius integers are in RESULTS.json. Oracle containment is stronger than mere overlap and is not substituted for the separate exact distance check.

## Actual controls

- Actual production `signed_power([-1/2,-1/4],285)` returns exactly **(-2^338,-2^53)** on the K=623 grid. Both endpoints are strictly negative; an absolute-power substitution cannot pass this check. The independent rational result is [-2^-285,-2^-570].
- 945 endpoint-power controls cover odd/even exponents, negative/positive intervals, zero crossings, degenerate intervals, and multiple grids; production endpoints equal separately computed rational outward endpoints.
- 3,507 signed nearest-even rounding controls pass, including 408 exact ties. The independent rule chooses the closest integer and breaks an exact tie by even parity, rather than repeating production's remainder branch.
- Each selected midpoint output is independently rederived. Its exact production-grid coordinate radii and squared-radius threshold are independently recomputed and match every stored field.
- An exact squared-radius equality passes; a one-unit larger centered interval raises CertificateError.
- The minimum nonzero modular residue is one and its production denominator lower endpoint is strictly positive.
- The zero-residue result takes exact F and R limits with no denominator division.
- The independently enclosed odd witness has F<0, R<0, R^285<0, and a strictly positive real coefficient. Its returned real/imaginary numerators are still both zero. **This is not an eta-violating final-output counterexample for an absolute-power mutant.**
- Empty construction pays header work but performs no pi/root setup. Dense rejection also performs neither setup. Repeated prepare adds charges without resetting the ledger or repeating numerical setup.

## Independent source and universal error-budget review

The source implements the contract's mathematical recurrence faithfully. Exact built-in integer headers and incidence indices are validated. The M expression is the smallest power of two at least 4N; t>=M is rejected before numerical preparation. The retained row stencil is checked before setup.

Production pi uses K+8 terms per arctangent, outward rounding of each term and the alternating next-term remainder on its correct side. Its width is at most 20(K+9) grid units. Sine uses exact congruence reduction; the angle midpoint radius encloses the full angle interval. For x in [0,2], the forward nonnegative term multiplier is initially at most 2/3 and then smaller. Each term has width at most six grid units, and the fixed factorial loop computes exactly (2n+1)! for n=K+8. The tail 2^(2n+1)/(2n+1)! and angle radius are both included. Analytic clipping preserves the target. The resulting sine width is at most 64(K+9)*2^-K.

Let c_s=bit_length(s), b=bit_length(J+1). Then K=J+2b+16 and J<=2^b-2 imply K+9<=14*2^b and 64(K+9)<=2^(K-J). Hence the sine width is at most epsilon=2^-J. This argument is universal for the successful domain, not an inference from tested values.

For nonzero residue, Q=NM and the exact positive denominator is at least 2/Q. Since epsilon<1/Q, its entire containing production interval has lower endpoint greater than zero. The all-corner quotient routine therefore divides only by positive endpoints. The normalized exact targets obey |F|<=1 and |R|<=1. Each rounded quotient interval has width at most

    w0 = 4Q epsilon + 2 delta,  delta=2^-K.

For x in [-1,1], x^s is s-Lipschitz. The source correctly selects ordered signed endpoints for odd s, and absolute endpoints with a zero minimum when appropriate for even s; its paid integer powers and binary divisor then give an enclosing K-grid interval. Subsequent four-corner products, root multiplication and phase multiplication are outward-rounded and clipped only to valid analytic bounds. The phase formulas equal cos(2*pi*a0*ell/N) and -sin(2*pi*a0*ell/N).

Combining widths gives each Cartesian coefficient interval width at most

    wC = 3(s+1)w0 + 3epsilon + 17delta
       <= 4(s+1)M^2 epsilon <= eta/64.

Because p=A+3, nearest-even midpoint rounding moves at most eta/16. Each coordinate's farthest endpoint radius is at most eta/128+eta/16=9eta/128; the sum of squared coordinate radii is therefore less than eta^2. The runtime check uses exactly this complex squared norm, with integer threshold 2^(2(K-A)); it is neither an unsquared coordinate bound nor a floating-point surrogate. Failure is correctly classified as a deterministic certificate defect.

The concrete budget is checked using exact Fractions in RESULTS.json. An additional 1,785 (D,m) combinations validate the precision inequalities as supplementary implementation controls; they do not replace the universal reasoning above.

## Source loops, memory and paid preparation

The AST inventory in RESULTS.json confirms the only production import is dataclasses. The complete variable loops are:

- K+8 arctangent terms, twice during one preparation;
- K+7 sine recurrence iterations and 2(K+8) factorial steps per non-exact sine;
- K+2 square-root bisections;
- exponent halving in endpoint square-and-multiply.

Other loops are at most four interval corners or the fixed-size operand/result tuple in the ledger. There is no N- or M-iteration loop, dense vector, row/phase table, cache of per-row phases, or retained stream of outputs. Persistent numerical preparation is one pi interval and one root interval. Preparing those constants once is explicitly charged; repeated access is also charged. The implementation does not hide setup behind a free constructor or reset charges after validation.

For fixed D, s,K=O_D(m). Rational argument integers have O_D(m) bits, arctangent denominators O(K) bits, the Taylor factorial O(K log(K+2)) bits, and signed-power numerators/divisors O(sK) bits. Thus a valid common width is H=O_D(m^2), not O(m). A coefficient and one-time setup each use O_D(m) primitive/control events. Charging a schoolbook upper bound O(H^2) per primitive yields O_D(m^5) bit work and O_D(m^3) cumulative produced bits. The source's conservative control/copy envelope preserves these orders. Its report counters, comparison/copy work, shifts and exponentiation intermediates are included rather than treated as unit-cost real arithmetic.

The declared ledger is a binary arithmetic/control model, not an exact accounting of Python allocation, instructions, wall time or peak RSS. Report serialization and the independent audit harness are outside the production-complexity statement. Downstream E-record retention, N accumulators and N outputs remain separately payable. The fixed-D qualification is essential; no uniform m^5 bound over arbitrary D is accepted.

The three production evaluations use 12 sine calls, 1,262 arctangent terms, 625 root bisections, 5,040 sine recurrence steps and 10,096 factorial steps. These exact counts agree with the expected branches and schedule. Maximum recorded signed integer width is 177,557 bits. The independent run's complete monotone ledger is retained in RESULTS.json.

## Process result and acceptance scope

The final independent process exited zero with empty stderr and unchanged source hashes. Limits were 90 CPU seconds soft / 100 hard, 180 wall seconds, 512 MiB address space, and 32 MiB output files. Observed wall time was about 1.84 seconds and maximum RSS 15,680 KiB. These host measurements are safety/process evidence only, not complexity or speed claims.

The frozen scalar numerical gate is accepted: independent guaranteed enclosures for all three requested coefficients, the actual odd signed-power sentinel, positivity, signed ties, exact complex-radius certification, faithful source recurrence, finite setup and the qualified source-cost bound.

This review does **not** execute or accept the complete outer coefficient stream, a theorem-scale sparse-recovery run, every-tape estimate formation, scatter, paid N-output accumulation, scale-back, dense/all-length executable dispatch, independent amplification, or a new FFT/theorem/novelty claim. Producer provenance and enumeration acceptance remain the companion wrapper review's responsibility.
