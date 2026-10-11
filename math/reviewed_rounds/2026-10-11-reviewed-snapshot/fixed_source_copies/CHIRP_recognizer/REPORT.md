# Independent review of the bounded exact CHIRP recognizer

11 October 2026. Verdict: PASS FOR THE BOUNDED DENSE REFERENCE. No source repair is required for the reviewed bytes. Optimized implementation and production validation remain open.

## Decision and identity

The recognizer and separate checker correctly implement their stated mathematical decision contract, subject to explicit resource exhaustion. This review accepts the immutable candidate v1 code as a bounded exact reference. It does not promote it to the accepted fast Toeplitz, blocked-convolution, dyadic, or Gauss-output implementation, and does not close STR-Q2 production work.

Reviewed Library input: libfile_bf879c07b8208191a33e55429d9675ca, version 1, CHIRP_Bounded_Exact_Recognizer_CANDIDATE_2026-10-11.zip, 42,381 bytes, SHA256 f0f6ab4c1601a2875d48aa61c48fd347154357b95f21cf41e0de351d0a61c9db.

- chirp_exact.py: 7d263f616526bd1123658771afc73bb44fc15282ef8ee0131e48ade0b59d18b7
- check_certificate.py: 556337c6bc1f4215d1782f82fb63bfd67771152a442af1688bf91080f763699f
- Author test program: 969e810c573c9a38df9e1683f1a5b238f9feba555d03683832bb4cc9d07577b0

The review independently materialized the pinned Library file and verified its exact archive hash. All 25 candidate manifest payloads and all five accepted-source pins agree. The candidate archive and payload bytes are preserved; the original pending-review wording and assurance strings remain historical source metadata. This separate reviewed statement supplies the code-review verdict, without silently changing the reviewed source.

## Exact supported input and mathematical family

The API is recognize(problem, limits=Limits()). The problem must be an exact built-in dict with exactly N, p, r, omega, and x. The four header values are exact built-in integers, excluding bool and integer subclasses. The raw vector is an exact built-in list or tuple with N exact built-in integer entries, all canonical residues 0 <= x[j] < p.

The mathematical domain is N >= 2, 1 <= r < N, supplied prime p, N dividing p-1, and canonical omega of exact multiplicative order N. Primality is verified by this implementation, rather than accepted as an unchecked promise. It neither discovers p nor discovers omega. N=1 and r>=N are deliberately outside this API, despite their separate trivial/dense treatment in the mathematical theorem.

The recognized family is

    x[j] = omega^(a*j*j) sum_b gamma[b] omega^(b*j), 0 <= j < N,

with at most r distinct frequencies modulo N and nonzero listed amplitudes. Zero has the empty representation. The returned phase lies in 0 <= a < L, where L=N/gcd(2,N). This removes the universal even-N redundancy, without asserting phase uniqueness.

The order-2N-root curvature extension is excluded. For example N=4, p=17, omega=4, r=1, x=[1,2,16,2] is NONMEMBER here although it equals 2^(j*j) with 2 of order 8.

## Status and output contract

- MEMBER means validated raw input, validated prime and exact-order root, a fully synthesized representation matching all N original coordinates, and all N positive-sign unnormalized DFT entries, sum_j x[j] omega^(j*k).
- NONMEMBER means validated parameters and completed rejection of every canonical phase. Both representation and dft are null. No transform of the rejected input is supplied.
- INVALID_PARAMETERS means a detected header/domain, prime, root, or limit-configuration failure. It is never signal nonmembership.
- INVALID_INPUT means a detected malformed record, unexpected keys, unsupported raw container/type, wrong length, or noncanonical coordinate. It is never signal nonmembership.
- LIMIT means a dimension, modulus-width, work, or CLI-byte cap prevented completion. It is indeterminate and returns neither representation nor transform, including when a representation was found before dense output finished.

The first detected condition controls. A cap can prevent discovering a later invalid parameter; LIMIT does not promise input validity. An earlier accepted phase in a LIMIT log does not convert the outer result into MEMBER. A root/prime validation flag is a progress field, not a decision certificate. Internal arithmetic invariant failures raise exceptions rather than being relabeled NONMEMBER.

The JSON CLI reads one finite record, caps it at 1 MiB, rejects duplicate keys, nonfinite numeric constants, malformed UTF-8/JSON, and trailing JSON values, and emits one JSON result. Exit code zero is transport completion, not membership. There is no gamma-coded bit-record parser.

## Review of mathematical correctness

### Validation and the zero branch

Lines 248-288 of chirp_exact.py validate shape, exact types, ranges, configured dimensions, N dividing p-1, every raw coordinate, primality, and the supplied root. Trial division tests 2 and every odd divisor through sqrt(p). If it exhausts the meter, the result is LIMIT, not composite or NONMEMBER. For a validated prime, the root recurrence multiplies exactly N times, rejects an earlier return to 1, and requires the Nth value to be 1. This also rejects omega=0.

The zero branch occurs only after every raw coordinate, primality, and order validation. Its empty representation and all-zero transform are exact. The first nonzero center is selected from a full scan; no theorem promise is inferred from a short zero prefix.

### Cyclic eliminant and phase coverage

Lines 307-332 evaluate the accepted (r+1)-square cyclic matrix using x[(c+i-j) mod N] and omega^(-a*(i-j)*(i-j-1)). The implementation's integer product delta*(delta-1)//2 is exact for positive and negative delta, and equals the accepted f(delta). No index is reduced modulo p.

For a genuine signal at phase a, the quadratic exponent after this multiplier becomes a*c*c+(2*a*c+a)*(i-j); each frequency adds b*(c+i-j). Thus the matrix is a sum of at most s <= r rank-one matrices and its determinant vanishes. The wrapped lookup is legitimate because the entire represented signal is N-periodic. Dense Gaussian determinant evaluation is exact over the already validated field.

The loop a=0,...,L-1 covers all representations. When N is even, adding N/2 to a is absorbed by adding N/2 to every frequency, since j*j-j is even. A nonzero determinant safely rejects a phase. A zero determinant only enters candidate recovery and never directly accepts.

### Hankel rank, roots, recurrence, and weights

Lines 157-218 dechirp every raw entry and build the r-square Hankel matrix from periodic lookups. A true s-mode dechirped signal has H=V diag(gamma) V^T with r>=s and distinct grid nodes. V has full column rank; the leading s-square Vandermonde is invertible. Consequently rank(H)=s and the leading s-square Hankel block is nonsingular, including 2r>N.

The leading solve recovers the monic node polynomial. Exactly s roots on the supplied distinct N-root grid are required, so repeated or off-grid nodes cannot pass. All N-s ordinary unwrapped residuals are checked. Weights are recovered from a distinct-node Vandermonde solve and zero weights are omitted. A zero Hankel rank cannot accept nonzero later raw entries. A singular leading block rejects the candidate, never the entire signal before other phases are tried.

For arbitrary negative inputs, the final synthesis at lines 206-217 compares every original raw coordinate against the recovered legal phase and at most r legal modes. This gives direct acceptance soundness independent of the earlier eliminant or recurrence tests. A separately injected wrong-weight solve was caught by full synthesis. On true inputs, the rank, node, recurrence, and weight steps above cannot reject the true canonical phase unless the resource meter expires. Therefore, complete NONMEMBER is sound as well as MEMBER; successful recognition is complete subject to finishing the bounded computation.

### Dense output

Lines 336-350 evaluate sum_j x[j] omega^(j*k) from the original raw vector for every k, using positive sign and no N^-1 factor. The result is installed only after the last output write. The independently tested N=512/r=128 case returns MEMBER at 8,104,359 work units; one unit less returns LIMIT at accepted_dense_dft with both public outputs withheld.

## Separate checker and distrust of certificates

The checker imports no recognizer code. It independently validates primality and exact order with direct powers. MEMBER verification checks phase/mode legality, distinct frequencies, nonzero canonical amplitudes, all raw samples, and every dense DFT coordinate. NONMEMBER verification requires a complete canonical phase log and computes the Fourier support of each dechirped raw input directly. The omitted N^-1 factor does not affect support because N is nonzero in the field.

The checker does not trust asserted validation flags, center, eliminant values, ranks, work totals, or rejection reasons as mathematical evidence. Tampering with those fields can still leave a mathematically correct decision verifiable, intentionally. Its VERIFIED_NONMEMBER certifies the actual support test, not a truthful execution transcript or a compact proof of each recorded reason. Its input hash binds canonical JSON content but is neither authentication nor a proof of valid input.

Malformed or false mathematical certificates are rejected. The checker has independent hard dimensions and a term cap, so a valid recognizer certificate can return CHECKER_LIMIT. INVALID_INPUT, INVALID_PARAMETERS, and LIMIT results are not mathematical decision certificates; depending on missing binding/schema, they can fail certificate validation before NO_DECISION is reached.

## Resource contract and cost

Defaults are max_n=128, max_r=64, max_p_bits=32, max_work_units=2,000,000. Each configurable cap is an exact nonnegative integer and cannot exceed the hard caps 512, 128, 64, and 20,000,000 respectively. A zero cap is allowed but may make all nontrivial inputs return LIMIT. The checker uses the hard dimension/width caps and a default 2,000,000-term budget, configurable up to 20,000,000.

The recognizer counts field additions/multiplications, inversions, the actual square-and-multiply inversion work, exponent iterations, trial divisions, root generation/tests, raw validations, matrix preparation, phase attempts, candidate work, and output writes. The sum of named counts equals work_units. Each started phase receives a subtotal, including an interrupted phase whose subtotal can be zero if the first charge cannot be paid. Accepted dense output is charged globally after the successful phase, not incorrectly folded into a rejected-phase subtotal.

Every configured cutoff tested, across 15 stages, returned LIMIT with no partial mathematical output. The cap is checked before each metered event or bulk charge. Root and prime validation remain paid even for zero. Large valid primes can exhaust trial division, and even mathematically admissible parameters inside the hard dimension/bit caps need not finish within the largest permitted budget.

For completed dense recognition, write B=bitlen(p), L=N/gcd(2,N). A conservative arithmetic bound is O(L*(r^3+N*r)+N^2+N) field additions/multiplications before implemented inversion internals, O(L*r) inversions, and another O(L*r*B) field multiplications for Fermat inversion. The accepted-output N^2 term is absent on NONMEMBER. Live arrays use O(N+r^2) field entries plus O(L) phase records. Trial-division and ordinary integer/control work are additional.

The work meter is deterministic instrumentation, not wall time, a complete machine-instruction count, a process memory limit, or the corrected bit-cost RAM theorem. Python copies, comparisons, JSON parsing/serialization, set construction, allocations, and interpreter overhead are not each fully charged. The public Python input is already resident; arbitrary hostile object construction, huge malformed mappings, operating-system errors, concurrent mutation, or catastrophic process-memory failure are not hardened by this meter. The finite CLI byte cap is not a network timeout. These are scope boundaries, not mathematical rejection bugs.

## Independent test evidence

The independent controls passed 643,632 complete differential decisions. Their exhaustive oracle explicitly generates every <=r representation over all N phases, so it does not share the recognizer's eliminant/recovery logic or rely on the author's Fourier-support oracle.

The exhaustive portion covers 640,921 raw vectors:

- N=5, p=11, r=1: all 161,051 vectors; 251 members
- N=5, p=11, r=2: all 161,051 vectors; 5,251 members
- N=4, p=17, r=1: all 83,521 vectors; 129 members
- N=6, p=7, r=1: all 117,649 vectors; 109 members
- N=6, p=7, r=3: all 117,649 vectors; 13,321 members

Of these, 22,268 decisions were passed through the separate checker, including every exhaustive member and a deterministic sample of exhaustive nonmembers. Additional controls include 168 constructed cases through N=128, 492 raw-coordinate mutations, 2,048 one-mode representations over every phase/frequency/amplitude with two exact-order roots, and 726 small-root/zero validation cases. A nonzero ambiguity witness N=3,p=7,r=2,x=[0,1,3] has support 2 at all three canonical phases, confirming that no uniqueness claim is appropriate.

Other independent checks passed: 46 malformed/domain cases, 19 invalid limit configurations, four explicit dimension/bit caps, 27 corrupt decision certificates, two intentional untrusted-telemetry cases, three nondecision cases, four invalid checker budgets, 1,366 individual recognizer cutoffs, 802 checker cutoffs, and ten CLI records. Boundary controls separately passed the full N=512/r=128 model, final-output withholding, 64-bit trial-division exhaustion, forced wrong-weight rejection, and forged MEMBER rejection.

The complete author suite was replayed in a separate copy and passed unchanged: 121,187 complete decisions, 120,219 exhaustive cases, 445 cutoffs, 13 corrupt certificates, five adversarial phase guards, and the full-synthesis fault guard. Only the fresh candidate and fresh review programs were executed. Historical uploaded source scripts were neither imported nor run. Execution durations are provenance only, not performance benchmarks.

## Publication disposition and open work

Q13 can record an independently reviewed bounded dense exact reference implementation. Its accepted proof statuses are preserved. STR-Q2 remains scoped proof complete with optimized production validation open. The candidate's old pending-review wording should be superseded by this review as a dated evidence entry, not rewritten inside the accepted immutable archive.

No Sheet or GitHub edits were made. Recommended later consolidation must re-read affected rows, preserve historical evidence, bind this review and the candidate by immutable Library identity/hash, and avoid changing proof rank, novelty, priority, numerical, fast-runtime, or production statuses. Actual optimized kernels, dispatcher integration, full implementation cost validation, and appropriate benchmarks remain separate work.
