Publication derivative of an independently reviewed research report. Private tracking and delivery details are omitted; mathematical scope, attribution, limitations and review method are retained. Original source-report SHA-256: 18a32e408914acab4b30f5cd987cb8f50a22aea21aabfe89969abc045cd9266f.

# Q16 deterministic finite-word bucket arithmetic: bounded independent review

## Verdict and immutable target

Verdict: bounded independent acceptance with the explicit interface and wording
clarifications below. The arithmetic theorem and implementation are accepted
within that contract; no complete sparse-engine claim is accepted.
The sole reviewed candidate is `CANDIDATE.zip`, SHA-256
`e48c95c888742adbfe3aa63f5447b5eb93fc8a7485548db18a09865aee4086a5`
(285377 bytes). Its manifest has SHA-256
`2ea70e3d38c52c533d66b79ff0c74841b71aeb144d3834a4f7e517064e1ba4ea`.
The executed new implementation has SHA-256
`1b0d0c0ebe423a3efa348a2509c94acd745c8ffbcf88691f7c426295a5d1922e`.
No archived HIKP constructor or uploaded original program is executed. Candidate
and dependency archives are read as data, and runs use fresh extracted copies.

## Independent mathematical derivation

Let n=2^m, B=2^b, 2<=b<=m, q>=10, L=8Bq and w=2L+1<n.
Set c=ceil(log2(w)), p=q+c+6 and h_t=a_|t|/2^p for -L<=t<=L.
The theorem requires signed integer taps with |h_t|<1/2 and exact reflection;
HIKP response properties additionally require the separately accepted provenance.
The endpoint m=10,b=2,q=10,p=26 gives Q=56. The support guard and q>=10
imply m>=10 and Q>=56. B=1 is not legal in this inherited family.

For odd sigma, multiplication by sigma is a bijection modulo 2^m. Because w<n,
all signed support indices address distinct samples. Reducing arbitrary signed
sigma and tau modulo n before advancing addresses preserves every exact index.
Grouping the signed support by t mod B gives exactly the unnormalized negative
DFT of the folded array. It introduces neither a support shift nor a 1/B factor.

Let I denote the imaginary unit, I^2=-1. With
F_i=sum_v x_v exp(-2*pi*I*i*v/n), Fourier inversion is
x_v=(1/n)sum_i F_i exp(2*pi*I*i*v/n). Direct substitution therefore gives

    U_j=(1/n)sum_i F_i exp(2*pi*I*tau*i/n) H_(j*n/B-sigma*i).

Consequently n*U, rather than U, has unnormalized-F convolution units. A left
shift by m bits scales the numerical answer and its absolute error by n exactly.
An F-unit target 2^-k is met by requesting kappa=k+m. The candidate makes no
finite-word claim for sqrt(n)*U in unitary coordinates. Cardinal complex-tone
tests verify the sign, translation phase, H argument and factor n independently.

For nearest-bin addressing write u=sigma*i mod n and d=n/B. The candidate's
v=floor((2u+d)/(2d)) obeys -d/2<=u-v*d<d/2, including upward half ties.
Taking v modulo B preserves the congruence. Evenness of real symmetric taps
turns H_(v*d-sigma*i) into H_(u-v*d). Addressing is not a location theorem.

Every sample coordinate is an exact bounded rational, with positive denominator,
integer numerator/denominator of at most ell magnitude bits and absolute value
at most 2^A. Ties-to-even conversion on the 2^-r grid has per-component error
at most 2^(-r-1), hence complex error at most 2^-r. The range endpoints are
exact grid points. Thus conversion alone changes every output by less than
(w/2)2^-r, which is covered by the stated w2^-r. The integer tap products,
residue folding and grid lift are exact. No floating-point coercion is present.

The complex l1 mass of the folded, converted signal is at most R=w2^A: each
sample has magnitude at most sqrt(2)2^A and each tap has magnitude below 1/2.
Every exact butterfly intermediate is a unit-modulus weighted sum of a subset
of those folds and has magnitude at most R. Each certified root has complex
error at most 2^(1-s). Each complex-product rounding contributes at most 2^-s.
Hence the stagewise maximum error satisfies

    e_(k+1) <= (2+2^(1-s))*e_k +(2R+1)2^-s
            <= 3e_k +(2R+1)2^-s.

Starting from exact lifted folds, e_b<=((3^b-1)/2)(2R+1)2^-s,
which is less than B^2(2R+1)2^-s. Final component rounding contributes complex
error at most 2^-o. With r=kappa+c+4, s>=A+kappa+c+2b+6 and o=kappa+3,
use w<=2^c and 2R+1<=3w2^A to obtain respectively

    E_conversion <= 2^-kappa/16,
    E_FFT <= 3*2^-kappa/64,
    E_output <= 2^-kappa/8.

The sum is at most (15/64)2^-kappa. The result holds simultaneously for all B
outputs and every admitted rational input, odd sigma and integer tau. Finite
tests supplement this derivation and do not supply its universal quantifier.

## Certified roots and totality

The identity pi=4(atan(1/2)+atan(1/3)) has the correct branch because the two
positive angles sum to arctan(1). At Npi=s+12 terms the summed alternating-tail
majorant is below 2^(-2s-22). The subsequent dyadic compression contributes
at most 2^(-s-17), and their sum is below 2^(-s-16). For 0<=k<B/2, angle
error is no larger and the midpoint angle has magnitude below 4.

Taylor truncation after N=max(32,s+12) terms has the displayed factorial
remainders: append the zero coefficient at the appropriate parity to apply
Taylor's theorem. Since (2N)!>=N^N and N>=32, both remainders are at most
2^-N. Lipschitz propagation of phase error and final real rounding therefore
leave each root component strictly within 2^-s. The exact rational certificate
check terminates and passes for every admitted precision. Cardinal roots are
exact. No probabilistic numerical abort, transcendental oracle, recurrence
stability assumption or unbounded refinement loop is used.

The review's oracle deliberately uses a different construction: rational
outward intervals for nested square roots from repeated half-angle identities,
followed by exact interval multiplication. It uses no pi identity, Taylor
series, author direct-DFT test or floating FFT.

## Range and paid resources

The common FFT error majorant is below one at all earlier stages as well as the
last. Thus stored s-grid components fit within (R+1)2^s, and the supplied signed
width s+A+c+4 has slack. A root numerator is at most 2^s+1 in magnitude.
Each exact real multiplication and the two-product sum fit the supplied scratch
width 2s+A+c+6. The output grid uses o+A+c+4 signed bits; optional n scaling
adds m. Tiny values rounding to zero cause no exceptional underflow case.
Input encodings, long indices and rational-root scratch have separate bounds.

The O((w+Bb)V^2+B*T^10+lambda_sigma^2+lambda_tau^2) elementary-bit bound is
conservative and valid with the stated V and T, provided its expressly additional
source acquisition, any unpaid accepted tap construction, and textual parsing
are actually charged. Rational Taylor numerators and denominators admit the
stated loose O(T^3)-bit bound, making the O(T^10) root-work allowance adequate.
The table is paid once and reused only at the same B and s. No length-n response
bank or signal allocation is hidden in the arithmetic implementation.

The storage statement is for packed retained numeric data, with the stated
rational scratch and additional source storage. Python headers are not zero.
At the JSON fixture interface, whole-file bytes, decoded text and parsing
objects also consume temporary memory depending on serialized size D; they
are not an O(1)-memory streaming loader. Treat actual parse memory separately,
just as actual parse work is separately charged. In particular arbitrary
whitespace or ignored metadata cannot be charged only to wp. This interface
qualification does not change the packed arithmetic theorem or canonical
pinned-fixture costs.

Sublinearity applies only under the declared growing regime and logarithmic
numeric/index widths, and excludes separately charged source acquisition.
Reading/indexing a sequential dense source may itself cost Omega(n*ell).
Operational resource exhaustion is neither a small-probability event nor an
accepted guarantee of availability for every finite parameter value.

## Explicit trust and wording clarifications

1. In candidate proof section 1, “nonnegative stored integer taps” must mean
   taps stored at nonnegative support indices, not nonnegative tap values.
   Tap values are signed. The code, fixtures and proof all use absolute values,
   so this wording clarification changes no algorithm or inequality.
2. `Window` checks the essential parameter/tap arithmetic contract. It does not
   certify a HIKP response. `load_pinned_taps` verifies equality to the hash
   supplied by its caller; that hash must come from a trusted accepted source.
   Computing a new hash for arbitrary taps does not create HIKP provenance.
3. Redundant JSON fields n,B,L,w,Q and coefficient_sha256 are ignored by the
   loader. Effective n,B,L,w,Q are recomputed from validated m,b,q,p. Essential
   malformed fields are rejected. False redundant metadata cannot override
   those computations, but is not itself rejected. Consumers must not describe
   this loader as a complete redundant-metadata authenticator.
4. Certified reusable `Prepared` values are trusted in-process immutable
   objects created by the candidate constructor. Their exact class and B,s
   are checked. Arbitrary serialized, reflectively forged or externally
   mutated Python objects are outside the certified-cache contract; this is
   not an untrusted-cache authentication protocol.
5. Stable sample access and bounded read/decode work are explicit assumptions.
   The code cannot establish a callback's stability from one read per address.
   Missing samples propagate source failure. Runtime, hardware and process
   limits do not receive invented failure probabilities.

## Source and remaining boundary

The accepted dependency is byte-bound at SHA-256
60518ee0ac6d10ed796dff586da7ac414dab7c2a78b9634c1cead6ec13826e98, including its
unchanged explicit Qmin=56 erratum and all seven pinned fixture members.

Primary source checked 2026-10-12: Hassanieh, Indyk, Katabi and Price,
[Simple and Practical Algorithm for Sparse Fourier Transform](https://people.csail.mit.edu/haitham/Papers/sFFT.pdf).
Claim 3.5 supplies the affine permutation operation; Claim 3.7 supplies folding
for a subsampled DFT; section 4.1 steps 2–4 supply product, buckets and nearest-bin
addressing. These locate the classical operation. The finite-word implementation,
negative-sign normalization bridge, numerical proof and bit ledger are local
derivations, not claims attributed to the paper.

Full Q16::flat-window-engine and STR-Q1 remain open. This review does not prove
perturbed ranking/selection, recovered support, estimation or division,
companion-response error propagation, phase correction, unbiased independent
randomness, outer-loop success/aborts, unitary arithmetic, interpolation or the
complete S6 interface. Preserve accepted ideal-arithmetic results and the
weak-coordinate-error versus all-input relative-l2 distinction. There is no
new priority/novelty claim or source-absence claim.

## Independent finite evidence

The frozen implementation passed 53 new exact interval-certified cases and 392
complex outputs. Cases cover all seven accepted fixtures, Q=56, signed rational
components, both component range endpoints, complex conversion half ties,
non-cardinal roots, 1536-bit signed permutation inputs, and A=192 amplitudes.
Additional signed-near-half and all-zero structural tap controls test the
arithmetic theorem only and explicitly make no HIKP response claim.

The small-boundary suite independently compares 3,096 complex FFT outputs with
a recursive FFT and neighbor-distance rounding, encountering 413 complex-product
half ties. It checks 992 precision-budget parameter combinations. The author
suite also passes from a cold candidate extraction, with all mathematical
fields identical to sealed FINAL_RESULTS.json. Exact count and rejection
details are recorded in REVIEW_RESULTS.json, BOUNDARY_RESULTS.json and
AUTHOR_REPLAY_RESULTS.json. The cold replay receipt binds the independent
scripts and the implementation to a further fresh-directory run.
