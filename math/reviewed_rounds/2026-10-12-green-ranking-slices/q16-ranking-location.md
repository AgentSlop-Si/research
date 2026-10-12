Publication derivative of an independently reviewed research report. Private tracking and delivery details are omitted; mathematical proof, source attribution, evidence and limitations are retained. Original source-report SHA-256: 6797c1241c06b2d748a18b11ebd575f38d444527961ecde3ef79ccde0ebd39dd.

Review date: 12 October 2026 UTC.

Editorial cost clarification: trusted tap preparation remains separately charged when not already available, as stated in the accompanying accepted cost ledger (SHA-256 b84773b77fd67f3744936c03923a0a986ec9213a5dea77495db20186438289f1).

# Q16 perturbed ranking and exact location fibers: independent bounded acceptance

## Verdict and immutable review target

**ACCEPT_BOUNDED.** The exact ranking implementation, its sharp perturbation
theorem, the deterministic location-event transfer, and exact inverse-affine
candidate enumeration are accepted on the stated dependency and source
contract. No mathematical correction to the candidate theorem is required.
This completes one bounded deterministic component. Full sparse recovery remains open.

The immutable author candidate is `CANDIDATE.zip`, 631,244 bytes, SHA-256
`4054c453210c2cb35aca37efc0108c56cc0120b3cbd139562760db7db4fd2305`.
Its selector has SHA-256
`9291649dd250a2f68d09601a870917e921d34c671c71414e44031f83c90c7e97`.
No candidate byte or accepted dependency was modified. Deliberately mutated
copies used as negative tests existed only in fresh temporary directories.

The accepted companion archive is byte-bound at
`60f9168baa667446dc00be46e809b4b8c6c270613a124029b59293f387348718`.
Its unchanged accepted bucket code has SHA-256
`1b0d0c0ebe423a3efa348a2509c94acd745c8ffbcf88691f7c426295a5d1922e`.
The manifest, complete member inventory, all seven fixture hashes, nested
accepted companion candidate, bucket review and bucket cost ledger, and the
accepted-companion dependency were independently checked. The old
constructor and old archive checkers were never executed by the new checker.

## Accepted theorem, with quantifiers and endpoints

Fix an admitted accepted-constructor window, n=2^m, B=2^b, q>=10,
L=8Bq, w=2L+1<n, p=q+ceil(log2 w)+6. Retain Qmin=56. Fix one stable rational
complex signal, odd integer sigma, integer tau, precision k>=1, r in [0,B],
and a nonnegative explicit candidate cap. Each queried real and imaginary
component a/d must have d>0, numerator and denominator magnitude widths at
most ell, and absolute value at most 2^A, with integer A>=0 and ell>=1.

For a successful nonempty call with sufficient cap, let

    U_j = sum_t h_t x_(sigma*t+tau) exp(-2*pi*i*j*t/B),
    Z_j = n U_j,
    epsilon = n e_raw <= (15/512) 2^-k.

Every reported Z-approximation is on the common dyadic grid o_B=k+m+6 and
satisfies |Z_tilde_j-Z_j|<=epsilon simultaneously. Sorting integer squared
numerators exactly selects the first r approximate magnitudes, using increasing
bucket index for every equality. It does not generally select the exact top-r
truth magnitudes.

For each selected a and omitted b,

    |Z_b| <= |Z_a| + 2epsilon.

This follows by chaining the two complex triangle inequalities through
|Z_tilde_b|<=|Z_tilde_a|. No distribution, isolation assumption, or generic
position assumption enters the argument. If theta_t is the t-th largest true
magnitude with multiplicity and 0<r<B, the candidate's strict inclusion and
exclusion inequalities are valid. In particular, a strict exact boundary
theta_r-theta_(r+1)>2epsilon forces the unique exact top-r set.

The strict sign cannot become non-strict: take exact magnitudes 1 and
1+2epsilon, approximate both by 1+epsilon, and let the lower-magnitude bucket
have index 0. The implementation selects it. For any proposed constant c<2,
choose a rational gap delta in (max(c,0)epsilon,2epsilon), exact values 1 and
1+delta, and observations 1+epsilon and 1+delta-epsilon. There is a strict
approximate rank reversal. This proves sharpness uniformly, beyond the finite
test examples.

For the reported boundary certificate, A and B0 are squared integer
numerators at the approximate selection boundary, t=2epsilon*2^o_B, and
D=A-B0-t^2. The exact predicate D>0 and D^2>4t^2 B0 is equivalent to
sqrt(A)>sqrt(B0)+t. The sign test is essential before squaring. Strictness is
essential at equality. The predicate certifies a strict true separation for
every selected/omitted pair, hence the exact top-r set. A false flag means
inconclusive; it does not mean the set is wrong. r=B is trivially certified.
r=0 returns the empty set without roots, source reads, ranking or inversion.

## Why equality in the location event is correct

For T>=0 and 1<=r<=B, suppose

    #{j : |Z_j| >= T} <= r,
    |Z_h(i)| >= T+2epsilon.

If the target bucket were omitted, all r selected buckets would have true
magnitude at least T by the pairwise inequality. The omitted target is a
distinct (r+1)-st bucket at least T, a contradiction. Both displayed signs
are correctly non-strict. No strict global rank gap is needed. The checker
contains 78,750 nonvacuous exact-target-boundary implications.

Preserve the crowding predicate exactly. Replacing its >=T by >T is false
at the endpoint: true magnitudes (1,3), approximations (2,2), epsilon=1,
T=1 and r=1 satisfy the weakened crowding condition and target equality,
but the index-1 target is omitted. Conversely a condition counting >T can
be used with a strictly greater target >T+2epsilon. This is a downstream
warning, not a repair to the author's already correct statement.

## Exact routing, output size and affine normalization

Put d=n/B, u=sigma*i mod n, v=floor((2u+d)/(2d)), j=v mod B,
o=u-vd. The offset is -d/2<=o<d/2. Every upward half tie belongs to the next
bucket, including the wraparound half tie. In the admitted family d is even
and d>16q. The generic helper also correctly handles d=1 and b=0.

For bucket j the d lifted coordinates j*d-floor(d/2)+t, 0<=t<d, form precisely
that half-open cell. Odd sigma has one inverse modulo n. Multiplication by
this inverse preserves the partition into disjoint cells. Therefore the
returned set is exactly {i : h_sigma(i) is selected}, with J=r*n/B distinct
indices. The first element of each fiber uses one modular product; each of
the d emitted elements pays one modular addition. The implementation performs
one final unused addition per fiber, and counts it: the total is exactly J.
Output order is selected-bucket rank order followed by ascending lifted
offset. It is not increasing-frequency order.

Newton lifting uses 1-sigma*a*(2-sigma*a)=(1-sigma*a)^2 and therefore doubles
valid precision. Reducing sigma at each precision keeps operands bounded;
the final exact invariant is checked. Huge positive and negative affine
inputs reduce once in the main call. Tau affects sample addresses and
spectral phases; it does not change which inverse-sigma frequency fiber
belongs to a bucket.

The preflight cap compares against J before calling the bucket or preparing
its roots. J equal to the cap is accepted. J greater than the cap rejects.
Selecting every bucket emits n indices. No replacement of J by r, hidden
frequency scan, or free output encoding is allowed.

## Fourier identity, true response and interference remain visible

In the declared negative-sign unnormalized transform convention,
F_l=sum_v x_v exp(-2*pi*i*l*v/n), substitution of Fourier inversion gives

    Z_j = sum_l F_l exp(2*pi*i*tau*l/n) H_(j*d-sigma*l).

For target i, tap symmetry gives

    exp(-2*pi*i*tau*i/n) Z_h(i) = H_o F_i + C_i.

H is the actual response, not the companion denominator 1. On the routed
closed passband, 1-rho<=H_o<=1+rho, rho=(5/64)2^-q. Hence
(1-rho)|F_i|-|C_i|>=T+2epsilon is a sufficient target condition. An independent
true-response ideal-estimator event |E_i-F_i|<=E instead gives the sufficient
condition |F_i|>=E+(T+2epsilon)/(1-rho). Its additional finite-word inflation
is 2epsilon/(1-rho), as stated. No bound on actual C_i is inferred from
selection or from the arithmetic certificate.

For an omitted frequency and 0<r<B, a selected bucket of magnitude at most
theta_r exists. The pairwise inequality and reverse triangle inequality give

    |F_i| <= (theta_r+2epsilon+|C_i|)/(1-rho).

This is conditional on actual interference. The previously accepted estimator
still separately satisfies |Y_i-F_i|<=|C_i|+rho|F_i|+a, with
a<=(63/512)2^-k. Its later phase and output rounding do not belong in the
selection epsilon.

A fresh missing-impulse control queries 641 addresses at n=1024, sigma=7,
tau=19 and puts the unit impulse at unqueried address 4. Every bucket is
zero, but all 1024 Fourier coefficients have magnitude 1. The returned
256-index set omits 768 nonzero coefficients. At i=0 the exact response is
16777217/16777216, and C_0 is its negative. This confirms the dependency's
existing obstruction to unconditional support discovery; it does not refute
the source's randomized sparse-recovery theorem.

## Exact-word range and complete cost audit

Each queried component is bounded by 2^A; consequently |x_v|<=sqrt(2)2^A.
Together with |h_t|<1/2, this implies |U_j|<=R=w*2^A and |Z_j|<=M=nR.
Since epsilon<1 and w<=2^c, c=ceil(log2 w), the signed scaled-numerator
width W=o_B+m+A+c+3 is conservative. Squared-norm width 2W+1 is also safe.
Scaling by n is an exact m-bit left shift. The inherited raw total
(15/64)2^-kappa, with kappa=k+m+3, yields the claimed 15/512 bound.

The new classical bit-work bound is accepted:

    O(lambda_sigma^2 + lambda_tau^2 + B W^2 + B log(B) W
      + r log(r+1) m + m^2 + r m^2 + J m + V^2).

It charges affine reduction; all 2B integer squares and exact merge-sort
comparisons/moves; duplicate detection in the generic fiber helper; the
geometric precision sum for Newton inversion; one product per fiber; every
index and modular addition; and the rational boundary certificate. Merge sort
needs at most B*ceil(log2 B) score comparisons. Index movement is covered since
W>=m>=b. Scalar validation and every serialized input's parsing/representation
remain separately paid as the candidate explicitly requires.

For the main locate call, epsilon and t are dyadic, and every boundary
predicate denominator remains a power of two. Thus the O(V^2) allowance is
consistent with classical exact arithmetic, including reductions; it is not
a constant-time claim about arbitrary-size rational helper inputs. The
generic helpers remain exact for their accepted finite inputs, with costs
depending on those inputs' actual widths.

Add the accepted bucket ledger in full, particularly fresh root preparation
on every nonempty call, and pay trusted tap construction if not already available. There is no
prepared-cache argument. Preserve actual source access and decoding,
potential Omega(n*ell) dense source acquisition/indexing, parser and hash work,
source storage, runtime headers, and full output serialization. The extra
packed-storage bound includes B scaled buckets and scores, rank arrays,
J m-bit outputs, r bucket identifiers, and conservative arithmetic scratch;
the retained raw bucket report and inherited storage are additional.

O((B+J)polylog n) is a conditional arithmetic bound when numeric/index widths
are logarithmic and q=O(log n). Actual o(n) arithmetic requires the appropriate
polylogarithmic slack in both B and J. The phrase 'J is sublinear' alone must
not be promoted into a proof that J*polylog n=o(n). No whole-engine or S6
runtime follows here.

Malformed inputs, even sigma, invalid selected counts and insufficient caps
deterministically reject. Bool is rejected at integer-contract boundaries.
Source exceptions propagate with no successful result: the tests fail reads
1, 7 and 641 separately, and all consumed prefix/preparation work remains
chargeable. Physical memory/interpreter/hardware limits are execution limits,
not assigned random failure probabilities or promised infinite resources.

## Trust boundary and independent test evidence

A Window instance authenticates structural parameters only. A fresh zero-tap
structural Window returns zero while the API still reports formulaic rho.
This is explicitly out of the accepted response theorem. Only unchanged
accepted-constructor taps, or the seven specifically pinned fixtures, qualify.
Ignored redundant JSON metadata is not newly authenticated. Single-query
sample stability and one fixed whole signal are assumptions, not measured
properties. The source hash check is not protection against malicious Python
module injection or reflective runtime modification. The reviewer loads the
verified bucket explicitly under its expected name in an isolated process.

The independent checker imports no author test oracle or expected counts.
Its 384-bit outward rational radical intervals use integer square roots and
algebraic half-angle identities for all B<=16 fixture roots. They do not reuse
the production pi/Taylor root construction. Direct signed-support transform
enclosures cover noncardinal phases as well as cardinal roots, 21 integrated
cases over all seven fixtures, A up to 128, k up to 61, and huge signed sigma
and tau. The new checks passed:

- 54,127 exact ranking cases, including non-power-of-two lengths and huge ties
- 42,875 complex perturbation vectors and 210,000 crowding implications
- 78,750 exact-target-boundary implications
- 45,927 independent radical comparisons, including non-dyadic helper radii
- 364 full/partial fiber parameter cases, 57,244 full-fiber outputs
- Eight additional inverse cases through m=4097 and 6002-bit affine inputs
- 40 invalid-input cases, three source-prefix failures, zero-source/root preflight
- Seven hostile ZIP-layout rejections
- Twelve killed source mutations covering imaginary magnitude, tie direction,
  float scores, radical strictness/sign, inverse direction, both cell endpoints,
  n scaling, error scaling, and both output-cap boundary/timing errors

The author's checker was separately rerun; its JSON exactly matched the
pinned expected output. That agreement is supplementary evidence, not the
independent oracle. Finite tests support the uniform proofs above; they do not
prove a probability theorem or replace accepted tap provenance.

The portable final cold replay verifies the review manifest, validates the
candidate seal and nested dependencies, creates new private temporary source
files, reruns every independent check and every mutation, and compares the
result with `INDEPENDENT_RESULTS.json`. The separate sealed cold receipt binds
the final review ZIP digest and the exact replay result digest. No workspace
absolute path or network access is needed to reproduce the checks.

## Source alignment and remaining obligation

The primary HIKP paper's Section 4.1 steps 4-5 (PDF page 6) defines nearest
bucket hashing, selects the largest buckets, and outputs their inverse
fibers. Lemma 4.2 (PDF page 8) supplies probabilistic location context; Section
4.2 adds repeated trials and aggregation. This source alignment was checked
against primary PDF text on 2026-10-12. No source screenshot or whole-PDF byte
authentication is claimed. The new finite-word and perturbation proofs are
local derivations, not attributed to the paper.

Primary source: [Hassanieh, Indyk, Katabi and Price, Simple and Practical
Algorithm for Sparse Fourier Transform](https://people.csail.mit.edu/haitham/Papers/sFFT.pdf).

Still open: certified unbiased independent random bits/sampling and all costs;
accepted-window recovery and crowding events under that sampler and declared
normalization; repetition, medians, aggregation/pruning and all outer failures;
unitary conversion, downstream S6 arithmetic and complete output accounting.
Preserve the ideal-arithmetic theorem, weak-coordinate versus all-input
relative-l2 distinction, Qmin=56, and unresolved priority/novelty. No broader recovery or historical-priority conclusion follows.
