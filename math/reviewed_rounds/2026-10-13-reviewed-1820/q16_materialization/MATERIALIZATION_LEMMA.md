# Exact centered materialization into the accepted Q16 source

13 October 2026 UTC. A bounded finite-input interface lemma, not a new sparse Fourier theorem or an independently accepted executable.

## Purpose and relation to existing proof

The recovered all-length theorem already proves max normalization and centered embedding mathematically. The current sparse acceptance applies to a literal M-tuple DyadicSource, whereas that theorem describes an N-entry implicit source. This lemma makes the representation translation explicit, pays it at the outer level, and shows that no extra spectral, norm-oracle, projected-signal or approximation premise is introduced.

The accepted numerical modules are unchanged. This lemma closes the mathematical representation/cost question. An implementation and independent source-level review of this constructor remain required before calling the executable input gate closed.

## Statement

Fix integer d>=1. Let N>=1, m=ceil(log2(4N)), M=2^m, and let exact bounded binary fields encode common exponent 0<=e<=dm and integers a_j,b_j satisfying |a_j|,|b_j|<=2^(dm), for 0<=j<N. Fields are acquired and globally range-checked before any random tape is drawn. The caller permits the standard growing-word model from the recovered theorem: a fixed d-dependent number of Theta(log(N+2))-bit words per field and exact bounded-word operations; polynomial scalar work on O(m)-bit metadata is paid separately.

There is a deterministic, total construction with O_d(N) growing-word work and storage which either:

1. establishes all a_j=b_j=0 and returns the exact zero-output branch; or
2. constructs the exact pinned buckets.DyadicSource whose values are an immutable tuple of length M and whose exponent-value bound F is k0<=dm, together with integer lambda_exp=k0-e, such that

       x_j=(a_j+i b_j)/2^e,
       lambda=2^lambda_exp,
       v_((j-a0) mod M)=x_j/lambda,  a0=floor((N-1)/2),
       v_r=0 at every other residue,
       max_r max(|Re v_r|,|Im v_r|)<=1,
       1/2 < ||v||_2 = ||x||_2/lambda <= sqrt(2N).

Every value cell has exactly the schema required by the pinned source reader:

       ((real_integer, real_exponent), (imag_integer, imag_exponent)).

All exponents equal k0, including zero cells. Every numerator has magnitude <=2^k0 and at most k0+1 magnitude bits. All nested containers are newly frozen built-in tuples containing exact immutable integer fields. The result is independent of later mutations to mutable input containers under the trusted source-level model.

If the accepted sparse guards also hold and an independent uniform tape is then supplied, the accepted sparse-success theorem applies to this v, with its original error, support, magnitude, probability and auxiliary-resource guarantees. This last implication invokes that accepted theorem rather than reproving recovery.

## Construction

1. Validate N and the declared fixed-width exponent e. Scan all 2N Cartesian integer fields, including the last second field, checking range and retaining exact copied pairs. Compute A=max_j(|a_j|,|b_j|). Do not accept an early all-zero conclusion before completing the scan.
2. If A=0, every validated field is zero. Write N exact complex zeros and stop. Do not invoke the nonzero promised sparse theorem.
3. Otherwise set k0=(A-1).bit_length(), equivalently the smallest integer k>=0 with A<=2^k. Set F=k0 and lambda_exp=k0-e. Store lambda symbolically by this exponent; do not allocate an integer of magnitude lambda when lambda<1 or unnecessarily shift raw fields.
4. Allocate an M-entry temporary source. For each r=0,...,M-1 set j=(r+a0) mod M. If j<N, use cell ((a_j,k0),(b_j,k0)); otherwise use ((0,k0),(0,k0)). Freeze the complete outer tuple and all coordinate tuples. Construct exactly the pinned DyadicSource type with this tuple and F.
5. Return only after source construction and all validation are complete. Freeze any retained metadata relevant to source interpretation before supplying fresh independent randomness.

The loop in step 4 is a full paid materialization. It is not called a sublinear or implicit source.

## Proof of exactness and normalized domain

For A>=1, k0=(A-1).bit_length() is the smallest nonnegative k with A<=2^k. This includes A=1, where k0=0. Thus 0<=k0<=dm and A/2^k0<=1. If k0>0, minimality gives A>2^(k0-1); if k0=0, A=1. In either case A/2^k0>1/2. At least one Cartesian normalized component attains this maximum, so the Euclidean norm is strictly greater than 1/2. Every complex component has modulus at most sqrt(2), giving the upper norm bound sqrt(2N).

Because N<M, the residues j-a0 modulo M for j=0,...,N-1 are distinct: congruent residues would imply that a nonzero integer j-j' with absolute value <M is divisible by M. The inverse map is exactly j=(r+a0) mod M, and its occupied set is precisely j<N. Thus step 4 preserves every input pair exactly once and inserts only zeros elsewhere. It preserves the Euclidean norm. The occupied signed indices satisfy |j-a0|<=N/2<=M/8, including even N; this is the P05 centered-support premise.

The exact dyadic value returned at an occupied coordinate is (a_j+i b_j)/2^k0. Since lambda=2^(k0-e), this equals x_j/lambda. There is no rounding, no additional error term, and no approximate-norm computation. All source numerator and exponent-value bounds follow directly from k0<=dm and A<=2^k0. In particular, the exponent-value condition F=O_d(m) is established, not merely a bound on the number of bits used to write F.

Every constructed numerical field is an exact integer and every nested cell is immutable. Freezing an independent outer tuple and independent tuple cells prevents later replacement or mutation of input containers from changing the source. This is the ordinary trusted source-level immutability model, not a claim against reflective tampering or host corruption. The actual source object must be constructed with the exact imported pinned class, because the accepted code checks type identity; a lookalike dataclass or callback does not satisfy its interface.

## Paid resource proof

Each raw numerical field occupies O_d(1) growing words. The complete validation/max scan and exact retention of 2N fields therefore cost O_d(N) word operations and words. Metadata such as M, a0, A, k0 and lambda_exp has O_d(m) bits. Computing m and k0 by a simple bounded bit scan costs O_d(m) operations; even conservative fixed polynomial bit cost for this finite metadata is O_d(N), since (log(N+2))^c/N has a finite supremum for each fixed c. No scan per coordinate is needed to recompute k0.

In step 4, r+a0<2M, so the modular reduction can be implemented by one comparison and at most one subtraction. Every lookup and cell construction uses O_d(1) growing-word operations. The M initial slots, M cell constructions and final M-reference tuple copy are all charged. Even retaining the input copy and temporary plus frozen source simultaneously requires only O_d(N+M) words. Since 4N<=M<8N, construction and cumulative finite-copy storage are O_d(N). This is a growing-word bound; the numerical data and addresses can occupy Theta_d(N log(N+2)) bits.

Zero-cell aliasing is unnecessary for the proof. Constructing every nested zero cell separately remains O(M), so the conclusion does not depend on a special allocator, pointer interning or shared mutable state. Host allocation failure and interpreter timings remain outside the finite-word theorem exactly as in the accepted components.

The sparse theorem's own auxiliary bound is unchanged, because it begins after this construction with a represented source. The combined outer bound must add the O_d(N) constructor and source storage explicitly. Claiming that the constructor fits the standalone sublinear sparse cost would be false.

## Consequence and limits

For nonzero x and eligible sparse parameters, accepted sparse output zhat therefore approximates U_M v simultaneously with probability >=1-M^(-3). The target is still the padded centered M-transform, not U_N x. Reconstructing U_N x requires the separately inherited P05 interpolation, finite active coefficients, accumulation, scale back and independent outer repetitions described in the gap ledger.

The proof does not remove any sparse branch guard, certify arbitrary source callbacks, extend the bounded ALG034 adapter, provide a physical entropy source, or supply the dense exceptional branch. It does not prove that the existing bounded harness is a total all-length executable. It supports a minimal all-size exact-input wrapper candidate that can preserve the current accepted sparse scientific source bytes.

## Source bindings

The required cell schema and exact type/length checks are in q16_success_bridge_audit_20261013/sources/buckets.py lines 19-29 and 168-181 and pipeline.py lines 103-116. The promise contract is q16_success_independent_1633/INDEPENDENT_REVIEW.md lines 11-21 and 43-49. The input domain and mathematical normalization are RECOVERED_EDITION.md Sections 1-2. Exact paths and SHA-256 values are in EVIDENCE.json.

Fresh exact finite controls in controls.py corroborate power-of-two boundaries, centered residues, exponent ranges, strict norm, copy isolation, scale reconstruction and zero handling. They do not import or execute the scientific sources, and their finite pass count is not the universal proof above or an implementation acceptance.
