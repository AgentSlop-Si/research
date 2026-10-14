# New Q16 m=57 signed-power and minimum-residue regression

**Verdict: ACCEPT_NEW_REFERENCE_REGRESSION_ONLY.**

New, self-contained local code successfully evaluated the three prescribed
coefficients and checked them against a separately implemented exact enclosure
oracle. All returned reference rectangles contain the tighter oracle rectangles;
all integer squared-radius certificates pass. No historical scientific code was
imported or executed. This is a same-agent, implementation-diverse experiment,
not an independent-agent review or integration of a production outer wrapper.

## Exact tested metadata and outcomes

D=5, m=57, M=2^57, N=2^55-1, s=285, J=587, K=623, p=459,
eta=2^-456. The four-element sorted support is
{0,1710,2^55+1,2^57-1}. The fresh exact lifted enumerator emitted 9,123
incidences. Each was checked against the exact row-first stencil; only the three
selected coefficients below were evaluated.

- (ell,k)=(0,0): the exact zero-residue limit branch was used. The guaranteed
  absolute complex error is at most 2^-496.
- (ell,k)=(0,1710): the normalized D_q interval is strictly negative and the
  exponent is odd. The guaranteed absolute complex error is at most 2^-693.
  The rounded output is exactly zero. This confirms why sign reversal here
  alone is not an eta-violating final-output counterexample.
- (ell,k)=(2^53,2^55+1): ell*M-k*N=1 exactly, the minimum nonzero residue.
  The guaranteed absolute complex error is at most 2^-460, below eta by a
  factor of at least 16.

These bounds are certified dyadic upper bounds, not floating approximations to
the errors. RESULTS.json retains the exact squared-error numerator and binary
denominator exponent for every coordinate pair, together with every returned
Cartesian enclosure and grid numerator. No assertion equates an upper bound
with the exact unknown transcendental error.

The actual new reference signed_power on [-1/2,-1/4]^285 returned exact K-grid
integer endpoints -2^338 and -2^53. A newly authored absolute-power mutant
fails this sentinel. A newly authored even-only mutant produces the exact error
`even exponent required`; the historical helper was not executed.

An empty-support call has zero scalar preparation and zero sine calls, but
retains positive header/validation charges. Both nonempty engines prepare pi
and sqrt once and make 12 sine calls for the three selected coefficients.

## Why the second enclosure is independently formulated

The new reference implements the statically accepted contract using Machin
pi=16 atan(1/5)-4 atan(1/239), point-Taylor sine with an angle-radius enclosure,
fixed bisection sqrt, and square-and-multiply signed endpoint powers. Its
mathematical precision argument is the previously accepted static review in
the companion static acceptance, identified and linked in README.md.

The separate oracle uses B=900 fractional bits and the following different
choices. It does not call the reference Scalar, sine, quotient, square-root,
power or coefficient methods.

1. Pi uses pi=4 atan(1/2)+4 atan(1/3). This identity follows from the tangent
   addition formula: (1/2+1/3)/(1-1/6)=1, and both angles sum into (0,pi/2).
   Each arctangent has exactly B+16 alternating terms, outward rounded term by
   term with the signed next-term tail. Thus its enclosure is rigorous.
2. Sine reduces the exact rational argument using its integer part/parity and
   a reflected fractional part. Zero and half-integer inputs are exact branches.
   A positive K-grid interval X encloses the reduced angle in [0,2]. Sine's
   degree-(2n-1) polynomial is evaluated by interval Horner recursion

       Y=1; Y=1-X^2*Y/((2j)(2j+1)), j=n-1,...,1; result=X*Y.

   Every multiplication and division rounds outward. Shared occurrences of X
   may enlarge the interval but cannot invalidate containment. Taylor's
   degree-2n remainder has magnitude at most 2^(2n+1)/(2n+1)!; the final even
   coefficient is zero. A separately calculated integer factorial yields a
   conservative grid-radius tail of at most one. Both endpoints are widened by
   that tail before analytically justified clipping to [-1,1]. This method
   requires no midpoint-angle Lipschitz argument from the reference.
3. Square root uses the restoring base-4 integer algorithm on
   floor(M*2^(2B)/N), rather than bisection. Its invariant is processed-prefix
   = root^2+remainder with root equal to the integer floor square root. The final
   [root,root+1]/2^B interval rigorously encloses sqrt(M/N).
4. Odd powers use 285 repeated integer multiplications at each endpoint, then
   outward division by 2^(B*(s-1)), rather than square-and-multiply. Monotonicity
   for odd s justifies the signed endpoint enclosure.
5. Independently written coefficient assembly applies the exact normalized
   Dirichlet ratios, zero limit, phase and sqrt. Positivity of every nonzero
   denominator lower bound is asserted exactly. Oracle bounds are compared on
   a common binary grid with no floating tolerances.

The two implementations share only basic paid integer-operation helpers and
the mathematical target. They were authored by the same reviewer. Correlated
author errors remain possible; this experiment does not substitute for a
separate reviewer examining the new source.

## Paid preparation and scope of resource evidence

All pi, sqrt, argument reduction, quotient, power, factorial, interval and output
certificate arithmetic is recorded. The reference ledger also includes support
validation, lifted enumeration and exact diagnostic membership arithmetic.
The empty-support ledger is separate. The oracle ledger includes its own
complete preparation, not free reuse of reference pi/sqrt. Exact comparison
arithmetic has another paid ledger.

Each instrumented integer arithmetic operation is conservatively charged
16*(sum of operand/result bit widths+2)^2. A deliberately loose control,
index, copy, allocation and ledger-bookkeeping envelope is
4096*(events+256)*(maximum bit width+bit_length(events+256)+16)^2.
This covers the fixed-width 32-byte run label and ordinary constant-many
untraced comparisons/formulas per instrumented step. It is an arithmetic model,
not a claim about Python CPU time, JSON serialization or resident memory.

Measured maximum numeric integer widths are 177,556 bits for the reference
and 256,501 bits for the oracle. Full operation counters and conservative work
charges are retained in RESULTS.json. Large polynomial intermediates are paid;
they are not mislabeled O(m)-bit words. These finite counters do not prove an
asymptotic bound from a single run. The fixed-D mathematical m^5 proof remains
the separate static result.

Neither code path creates an N/M-sized array or iterates over N/M. Incidence
enumeration is over the bounded lifted intervals, numerical evaluation is over
three records, scalar loops have prescribed precision-dependent limits, and
the source has no tolerance-driven refinements. The source and its inspection
provide this structural evidence; the elapsed runtime alone would not.

## Execution, integrity and exact errors

The final bounded launcher exited normally with code 0, no stderr and no
timeout. Its cap was 180 seconds. Source hashes before and after agree; the
exact hash and measured monotonic runtime are in EXECUTION_RECEIPT.json.
No software or scientific failure occurred. This experiment did not receive a separate independent-author review.

UTC review times and unavailable token counters are in STATUS.json. The source
hash, complete exact outputs, stdout, empty stderr, launcher and this report are
bound by the publication manifest and seal. Original source-document hashes are separately retained in ORIGINAL_SOURCE_MANIFEST.json. This is a publication-safe documentation projection, not the unchanged original packet. Hashes establish integrity, not signatures.

## Next gap

This closes only the new reference-regression experiment. It has not exercised
a source-pinned production outer wrapper or its accepted sparse-output adapter.
Its 32-byte label is fixture metadata, not proof that an actual accepted sparse
front-end object produced the support. Before production acceptance:

- Independently review the new evaluator/oracle source and its ledger; this
  same-agent experiment has not received that separate review.
- Implement or identify the concrete production wrapper, preserve/review its
  scalar dependencies, and bind the real accepted sparse output, immutable
  parameters and support through the production API.
- Repeat the source-pinned regression through that actual wrapper, including
  every required negative/control and malformed-input gate, with its own paid
  preparation and pre/post source hashes.
- Complete the separate full-stream scatter, accumulation, scale-back, dense
  fallback, all-length dispatch and independent amplification gates.

No research table, GitHub repository or external document was changed. Existing
norm/probability claims, accepted observer scopes and production exclusions are
unchanged.
