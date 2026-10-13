# Independent Q16 bridge source and cost review

Date: 2026-10-13 UTC

## Finding

ACCEPT the literal implementation correspondence and the claimed source-model asymptotic cost in sections 1, 2, 4, 6 and 8 of `SUCCESS_BRIDGE_AUDIT.md`, conditional on the explicitly inherited numerical contracts and the stated globally valid immutable fixed normalized source and independent uniform tape. No required repair or counterexample was found in this scope. This is not a new scalar-enclosure audit or a Python interpreter certificate.

No historical/production scientific module or test was imported or executed. Work consisted of source inspection, reading the component contracts, shell SHA-256 checks, and a newly written standard-library archive-byte comparison. No external state was changed.

## Byte correspondence

Fresh SHA-256 calculations agree with all eight section-1 pins: PROOF, ALGORITHM, compact_window, buckets, location_decode, phase_medians, pipeline and fair_tape. The actual local `Q16_Paid_Fair_Bit_Tape_Independent_Acceptance_2026-10-13.zip` has the stated hash `7ce0c1074c2143bf03e33f664d4cadc58ebce62089a3d8b48b3d65d137c2ec47`. Each of the six scientific modules is byte-identical to its recorded member of that ZIP. These are independent read/hash checks, not reliance on accepted labels.

## Executed route and randomness

`run_source_tape` calls `_source_parameters`, which calls `theorem_spec`. `WindowSpec.validate` enforces exact source B, r, P, B>=4096k and the dyadic/divisibility/support guards. q=512k is computed inside this route. There is no caller-provided candidate, bucket, schedule, q, cached preparation or phase row in the source API.

The word recurrence is exactly x -> 2x+bit on MSB-first blocks. The m-1 bit A word maps bijectively to odd sigma=2A+1; the separate m bit word maps bijectively to tau. `_schedule` advances one cursor by exactly 2m-1 positions per round, emits L location pairs and then L estimation pairs, and checks the final cursor. The inverse of the complete decoder is the concatenation of each pair's fixed-width A and tau binary words. Uniformity of the entire input tape therefore gives the full product law, not merely pairwise independence. Fixed source and tape independence remain proper input-law hypotheses.

The pipeline prepares a real BucketEngine once and executes all 2L BUCKETS calls. Internal bindings refer to the same context/source/spec, exact affine tuple, role and ordinal. The actual location results produce the canonical candidate tuple; every estimator and final median uses that same tuple. This suffices for execution provenance within the trusted program model. Global source validity, deep immutability and normalization are promises, so absence of a dense source scan is not a defect.

## Numerical correspondence

The bucket loop reads v[(sigma*t+tau) mod M], folds at t mod B, runs a negative-sign unnormalized B-point FFT and multiplies by 1/sqrt(M). Thus its ideal target is the bridge's supported sum and, after inverse Fourier substitution, has positive spectral tau phase and G[jT-sigma*i]. There is no extra B or M normalization.

Writing Rgrid=2^P, b=log2(B), the stored general certificate numerator is exactly

    (A*Rgrid+2W)*(Rgrid+1)^(b+1)
      - A*Rgrid^(b+2) + Rgrid^(b+1),

over Rgrid^(b+2), hence equals (A+2W*rho)*(1+rho)^(b+1)-A+rho. The bridge's generic-to-source simplification uses only W<M, b<=m, and (m+1)rho<=1/2, so applies to all valid source parameters.

The phase implementation computes tau*i mod M exactly, prepares cos and negative sine on its certified P+2 grid, forms the exact complex product and rounds once to P. It does not divide by G. The transferred error `(1+rho)E_B + A*rho + rho` and its bound by `64(m+1)M^2*rho` are valid without a recovery event. With Rnorm>1/2 and k<=M, eta<a/4 follows as claimed. This use of Rnorm is an analytic promise, not a hidden norm computation.

`nearest_even` uses a floor quotient and nonnegative remainder, with parity on the quotient, so its sign/tie convention agrees with nearest-even rounding for negative and positive inputs alike.

## Selection, fibers, votes and medians

All buckets use one P grid. Ranking compares exact `real^2+imag^2` integer scores, descending, with increasing index tie priority. No approximate square root enters the order. The robust-selection proof only compares computed magnitudes and their uniform errors, so it does not need the ideal and computed rankings to agree.

For T even the implemented hash is floor((residue+T/2)/T) mod B. The decoder enumerates jT-T/2 through jT+T/2-1 and multiplies these residues by the Euclidean inverse of odd sigma. This is precisely the hash fiber, including both wraparound half-cells. Tau correctly does not enter the frequency preimage. Odd multiplication is a permutation, giving qT distinct indices per round.

Aggregation explicitly verifies per-round distinctness, sorts the complete list, and retains occurrence counts at `(L+1)//2`. For source L=4m+1 this is the strict-majority threshold 2m+1. Its exact cardinality inequality is Kcand*ceil(L/2)<=LqT, giving Kcand<=2qT<=M/4. This is all-tape combinatorics.

Estimation parses the actual canonical candidates and returns in that order. Medians sort each signed coordinate separately and take index floor(L/2) for positive odd L, without further numerical rounding or deleting zero values. A strict majority inside each coordinate interval puts the selected middle value inside it, irrespective of whether good rows vary between candidates. Existing numerator components are returned; medians cannot enlarge their coordinate widths.

## Width and cumulative-cost derivation

The source cost hypothesis concerns the VALUE F, not its encoding length: 0<=e<=F=O_d(m). Since |n|<=2^e, source numerators have O_d(m) bits. Exact alignment to F costs a shift of at most F bits and produces at most F+1 numerator bits. Folding has denominator exponent F+P, and after b stages and scaling the unrounded exponent is exactly F+P+(b+1)(P+2)=O_d(m^2). Every aligned product/butterfly numerator is bounded by that exponent plus O(m) magnitude growth. Arbitrarily large standalone F would increase the cost; it is explicitly excluded from the stated fixed-parameter bound.

Exact box-power coefficients have at most 2r*log2(ell)+1=O(m^2) bits. Window powering with O(m)-bit endpoints and exponent O(m) also gives O(m^2)-bit intermediates. Scalar factorial intermediates have O(m log m) bits. The generic bucket certificate denominator exponent P(b+2) is O(m^2); its numerator, including cancellation operands, is polynomial width. Address products, sort indices and loop bounds have O(m+log m) bits. Exact rational beta fields of width h are charged before use, and their arithmetic is polynomial in m+h.

Each ideal b has magnitude <=2M^2, and the actual phase estimate has magnitude <=2M^2+eta<3M^2 on every tape. Every median Cartesian component is therefore <3M^2, so its P-grid numerator is strictly smaller than 2^(P+2m+2). This all-tape output-width statement does not assume successful recovery or small actual z_i.

The implementation contains O(r^2 ell)=O(Bm^2) coefficient cells, O(T) normalizer work, O(W)=O(Bm) tap work, O(B) root preparation, 2L(W+B log B) bucket work, L bucket sorts and inversions, LqT explicit memberships plus their sorts, L*Kcand freshly paid phases, and per-candidate coordinate medians. Scalar calls and integer operations contribute polynomial factors in m+h. Consequently total event count is `(B+T+qT) poly(m)`; all widths are polynomial in m+h.

The code retains location/estimation bucket traces, memberships, candidate references and estimate rows. This storage is not treated as an unimplemented streaming algorithm. Each component uses cumulative produced-integer and allocation charges, and the adapter adds the complete numerical and schedule ledgers. Sorted arrays, copies and retained diagnostics contribute polynomial factors already present in the event bound. Thus cumulative auxiliary storage as well as work is `(B+T+qT) poly_d(m+h)+poly(m+h)`. The source/tape objects are referenced caller-owned inputs; their construction is expressly excluded, not an omitted working array.

Finally B<2M^(1/2+beta), T<=M^(1/2-beta), and qT=512kM/B<=1024M^(1/2+beta). For fixed beta this yields the claimed `O_(beta,d)(M^(1/2+beta) poly(m))` cost. Decoder O(m^4) work and O(m^3) cumulative storage are lower-order polynomial terms. Nothing in this reasoning establishes all-length dense dispatch, raw normalization, outer transfer execution, physical entropy or host-memory totality.
