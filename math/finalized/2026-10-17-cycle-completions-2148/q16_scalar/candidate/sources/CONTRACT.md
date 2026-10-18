# Q16 outer active-coefficient candidate contract

13 October 2026 UTC. **RECOVERED CANDIDATE; independent static review required.**

This supplies explicit incidence, coefficient and preparation recurrences for the next source-pinned gate. It is not an implementation acceptance, an all-length executable, an exact DFT contract, or a new FFT complexity/novelty claim. No research score is changed. The prior interrupted draft is preserved as inert evidence; its recorded test totals are not reported as fresh results.

## 1. Inputs, domain and output binding

Fix the theorem's integer D >= 5. Receive exact built-in integer N >= 1 and M = 2^ceil(log2(4N)); let m = log2(M), a0 = floor((N-1)/2), s = Dm, h = 16s+1, t = 2h+2, L = M/4, and q = floor(M/(8s)). This component requires t < M. A failed guard returns `OUTER_DENSE_REQUIRED` before scalar preparation; the all-length caller must route to its separate dense branch. It is not a theorem-domain abort. The other sparse guards and beta are caller obligations; this component does not label an arbitrary reduced fixture theorem-valid.

Receive an exact built-in tuple of distinct built-in integer support indices k in [0,M), strictly increasing, bound to one accepted sparse-output object/run. S is its length. Indices associated with exactly zero estimates may be retained; this only overpays. The front-end support bound remains a caller obligation. Validate the entire tuple, including exact built-in integer types, strict ordering and range, before numerical preparation. Charge reading/copying all accepted input fields and validation; do not hash/scan an M-entry vector to bind sparse support. Rejected malformed input has a prefix receipt; no successful-domain claim includes malicious arbitrary-object callbacks.

For this standalone mathematical interface, run_binding is an exact built-in bytes object of length 32 chosen by the caller, copied once and echoed with each record. This is an association label, not proof of provenance or a cryptographic attestation. The trusted caller must associate the label, frozen parameter header and support with the actual accepted sparse-output object before invoking this stage. A future production adapter must verify that association against its concrete source-pinned API. The length cap keeps binding work within the stated bit budget; longer metadata, human-readable identifiers, hashing and serialization require their own input-length charges. The component receives no beta encoding and makes no uncharged beta validation claim. If the producer's support is not already sorted, the adapter must charge canonicalization separately; this component does not declare that work free.

Emit a stream of records `(run_binding, k, ell, real_integer, imag_integer, p, real_enclosure, imag_enclosure)` in support order then lifted-index order. The grid exponent is p=(D+3)m+3. Each unique pair (ell,k) is exactly one retained incidence, with

    C[ell,k] = exp(-2*pi*i*a0*ell/N) * sqrt(M/N)
               * D_L(u)/M * (D_q(u)/(2q+1))^s,
    u = ell/N-k/M,  D_j(u) = sum_{v=-j}^j exp(-2*pi*i*v*u).

The returned dyadic complex number must have absolute complex error <= eta=2^(-(D+3)m). Its exact Cartesian K-grid enclosures and a final squared-radius check certify that error; no floating tolerance is used. The downstream scatter must reject mixed run bindings, wrong grid/parameters, or substituted indices. It is not implemented here. This contract neither multiplies estimates nor initializes/rounds/scales N accumulators.

## 2. Exact, duplicate-free enumeration

For each support index k compute, using signed integer ceilings,

    r0 = ceil(N*(k-h-1)/M),
    r1 = ceil(N*(k+h+1)/M).

Loop over r0 <= r < r1 and emit ell = r mod N. No filtering, sort, deduplication, scan over N rows, or scalar preparation on non-incidences is needed. This is an equivalent sharpened implementation of the recovered edition's three clipped candidate intervals, not a change to its retained matrix. There are at most ceil(N*t/M) records for each k and at most S*ceil(N*t/M) <= S*t overall. Every row receives at most t records because support indices are distinct. See PROOF.md for endpoints and injectivity.

Use division with positive denominator and mathematical floor: ceil(a/b) = -floor((-a)/b), valid for negative a. A host's truncation-toward-zero division must not be substituted.

## 3. Fixed preparation schedule

Let A=(D+3)m, c_s=ceil(log2(s+1)) = bit_length(s), and define

    J = (D+5)m + c_s + 8,
    K = J + 2*bit_length(J+1) + 16,
    n = K+8, U = 2^K, epsilon = 2^(-J), delta = 2^(-K).

All scalar calls return enclosing intervals on the K-grid. Prepare one Machin pi enclosure and one sqrt(M/N) enclosure only if at least one coefficient will be emitted. A two-pass scheme may first count incidences; this adds only O(S) endpoint work. Alternatively initialize scalar state lazily at the first emission. If S=0 or there are no emissions, do no transcendental/square-root preparation. Loop limits are prescribed from parameters, never tolerance-driven.

The scalar recurrence is the pinned compact-window Scalar lemma, restated in PROOF.md. It uses n terms of each of two Machin arctangent sums and n sine Taylor terms after exact integer reduction. It certifies each sine interval width <=64(K+9)*delta <= epsilon. Calling Scalar at this new K and rational arguments needs the forthcoming wrapper/source review; the compact-window acceptance alone is not an acceptance of the outer wrapper.

For sqrt(M/N), let Z=floor(M*2^(2K)/N). Starting with lo=0, hi=2^(K+2), repeat exactly K+2 times: mid=floor((lo+hi)/2); replace lo by mid if mid^2<=Z, else hi by mid. Return [lo,lo+1]/U. The initial upper endpoint is strict since M/N<8<16. After the fixed loop hi-lo=1. This enclosure has width delta. Intersect with [0,3].

## 4. Per-incidence coefficient recurrence

Set Q=N*M and n_u=(ell*M-k*N) mod Q. Reduction modulo one is valid for both integer-order Dirichlet kernels. Define an outward K-grid rounding of any rational interval by floor/ceil of U times its endpoints. Intersect only with proved analytic ranges.

If n_u=0, set F=[(2L+1)/M,(2L+1)/M] and R=[1,1]. These are exactly K-grid representable because K>=m. Do not divide sine intervals at a zero denominator.

Otherwise compute b=sin_pi(n_u,Q), a=sin_pi((2L+1)*n_u,Q), and c=sin_pi((2q+1)*n_u,Q). The denominator is positive and its lower endpoint is strictly positive by the proof. Form all four rational corners for a/(M*b) and c/((2q+1)*b), round their min/max outward to the K-grid, and intersect both with [-1,1]. Call the results F and R. An exact numerator zero may return [0,0] directly. The exact zero/half-integer sine branches are decided by integer congruences, not approximate equality.

Compute `signed_power(R,s)` as follows. For R=[lo,hi]/U:
- If s is odd, output outward rounding of [lo^s,hi^s]/U^s.
- If s is even, let v=min(|lo|,|hi|), or v=0 if lo<=0<=hi; let w=max(|lo|,|hi|). Output outward rounding of [v^s,w^s]/U^s.
- Intersect the result with [-1,1]; for even s it may additionally be intersected with [0,1].

Integer powers use square-and-multiply; U^(s-1) is a paid binary shift. The existing compact-window `even_power` is not this API: it rejects odd s, and replacing odd powers by absolute/even powers changes the exact target.

Multiply F and signed_power(R,s) by all-corner interval multiplication, round outward to K-grid, and intersect with [-1,1]. Multiply by the prepared sqrt enclosure, round outward, and intersect with [-3,3]. Call the real amplitude interval H.

Evaluate the phase components as

    phase_real = sin_pi(N-4*a0*ell, 2*N),
    phase_imag = sin_pi(-2*a0*ell, N).

These are cos(2*pi*a0*ell/N) and -sin(2*pi*a0*ell/N), respectively. Multiply H by each phase interval, round outward to K-grid, and intersect with [-3,3]. Never prepare phases for inactive rows; per-incidence evaluation is acceptable and avoids cache complexity. There are at most five sine calls per coefficient, three for kernels and two for phase, with fewer for exact-zero branches.

For each Cartesian K-grid interval [a,b]/U select its exact midpoint and round nearest-even to the p-grid. Explicitly, set d_round=2^(K+1-p), v=floor((a+b)/d_round), and rem=a+b-v*d_round. Return v+1 if 2*rem>d_round or if 2*rem=d_round and v is odd; otherwise return v. The nonnegative remainder and floor convention make this correct for negative ties too. The following exact integer check is required. Let z_r,z_i be the rounded p-grid numerators and lift each to K-grid via z*2^(K-p). Let R_r=max(|z_r*2^(K-p)-a_r|,|z_r*2^(K-p)-b_r|), and analogously R_i. Verify

    R_r^2 + R_i^2 <= 2^(2*(K-A)).

This proves the absolute complex eta bound, even when the rectangle is conservative. The proof below makes failure unreachable on the successful input domain; a runtime failure is an implementation/certificate defect and must not be silently called the theorem's allowed failure event.

## 5. Charging and stopping condition

In the declared schoolbook binary model, fixed D gives O_D(m^5) bit work and O_D(m^3) cumulative produced-integer bits per coefficient, using a conservative O_D(m^2) maximum integer width and O_D(m) primitive count. One-time pi/sqrt setup is also O_D(m^5) bit work; header/support validation and enumeration cost O_D((S+E+1)*m^2), where E is the incidence count. Thus the total is O_D((S+1)*m^2 + 1_{E>0}*m^5 + E*m^5), with no N-sized transcendental pass. The +1 is necessary even for empty support: reading and checking the N/M header is paid. It is O_D((S+1)*t*m^5) in the sparse regime, not a host CPU/RSS claim. See the proof for why the exponent is justified and which constants depend on D. If D is runtime-variable, use the explicit bounds in s,K,m; do not claim a D-uniform m^5 bound.

A future source ledger must charge all setup, signed powers, scalar iterations, divisions, argument products/reductions, exact-type validation, tuple copies, returned certificates and loop/control/address work. Repeated validation/preparation must not reset or subtract prior charges. Stream records to the caller, or explicitly pay E record storage. Any cache/table creation is additional charged work. N accumulator/output costs belong to the separate outer-composition gate.

The next stopping condition is independent acceptance of this static contract and precision/cost argument, or a precise counterexample. Then author and review a production wrapper and run only separately authorized source-pinned integration. The accepted observer-v2 run remains unchanged and is not rerun.
