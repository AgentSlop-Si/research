Public derivative of an independently reviewed research report. Private tracking and delivery details are omitted; mathematical statements, source attribution, review method and remaining limitations are retained. Original source-report SHA-256: 3d5faa95ddfa3d6c24880cf9bc8f4c9aab3fd8ac4aa7766ce20a2fd841187ad5.

Review date: 12 October 2026 UTC.

Cumulative-scope note, 12 October 2026: the exact IID-bit-to-parameter primitive is separately accepted (review archive SHA-256 98c27330f248ac75c677700a872a1ab88e7a4985e2d5fc09c56098966ac533e2). Concrete provider quality and composition without biased abort conditioning remain open. The companion [crowding review](q16-actual-filter-crowding.md) supplies bounded event estimates; this collection does not claim a complete recovery algorithm.

# Independent bounded review: Q16 dyadic collision and stopband event

Review date: 2026-10-12. Verdict: **ACCEPT_BOUNDED**. No theorem correction or
implementation change is required for the sealed candidate. This is acceptance
of a probability kernel and a conditional event interface, not acceptance of a
complete randomized recovery algorithm.

## 1. Exact object and safe review procedure

Candidate: `Q16_Dyadic_Collision_Stopband_Event_CANDIDATE_2026-10-12.zip`.
Bytes: 718162. SHA-256:
`1548765fbeeb2c7c2d4c65ef6a5e7931951790a3c46beecd0284b13fcb1a273a`.
The complete 25-member ZIP inventory was checked before extraction; there are
24 hashed payload members plus the manifest. Traversal names, duplicate members,
links, encryption and excessive declared expansion were excluded. The original
source directory was not modified.

Before execution, the reviewer read all of `collision.py`, `check_collision.py`,
`verify_artifact.py`, the proof, source pins, costs, and the relevant accepted
location/companion proofs and route/selection implementation. The new production
module imports only the standard-library Fraction class and contains pure exact
helpers. The author checker has bounded exhaustive loops and local pinned reads;
it neither runs accepted implementations nor performs network or source access.
Its cold replay was allowed only after this inspection.

Independent checks execute only the inspected, hash-bound production helper and
literal mutations of it. No accepted source, tap constructor, bucket, selector,
PRNG or entropy provider is executed. Twelve copied dependency/review records
are byte-compared against the embedded accepted location envelope and its nested
candidate. The accepted location SHA is
`10797360653f5cd171ee8c61fa236f3b961018d361132dd9e23bdd0b6a6eabfc`;
its nested candidate SHA is
`4054c453210c2cb35aca37efc0108c56cc0120b3cbd139562760db7db4fd2305`.
These are dependencies, not newly reviewed full implementations.

## 2. Independent all-m orbit derivation

Let n=2^m and Delta=2^s a, a odd, 0<=s<m. Reduction of an odd sigma modulo
2^(m-s) has 2^s lifts among the n/2 possible odd seeds. Multiplication by a is a
bijection on that reduced odd group. The image is exactly the residues with
2-adic valuation s, uniformly, and its cardinality is 2^(m-s-1).

For 0<=C<n/2, a positive orbit point is 2^s times an odd integer no larger than
floor(C/2^s). The positive count is floor((floor(C/2^s)+1)/2). Positive and negative
points are disjoint below the antipode. Twice that count divided by the orbit
cardinality is the candidate's exact closed-radius formula. At and above n/2
all orbit points are included. In particular an antipodal orbit has one point,
not two. For an arbitrary exact nonnegative rational R, integer distances obey
D<R exactly when D<=ceil(R)-1. R=0 is empty. This proves the strict formula,
including integral radii and radii beyond the antipode, without an approximation.

The classical bound p_s(C)<=min(1,4C/n) also follows: when C<2^s the count is
zero; otherwise the number of positive odd integers is at most C/2^s. The exact
formula is sharper and is the formula actually implemented.

These are ideal probability statements. They assume a uniform odd seed. No
concrete entropy implementation or post-abort conditional distribution is
certified by their derivation or by exhaustive enumeration of possible seeds.

## 3. The actual hash, ties, sharpness, and zero cases

The accepted route reduces u=sigma*i modulo n, rounds u/d to its nearest integer
with upward half ties, and reduces the bucket index modulo B. For even d the
cell centered at jd consists of the d residues represented by offsets
-d/2,...,d/2-1. At the wraparound tie, the upper center is n, representing bucket
0 and offset -d/2. For d=1 the cells are singletons. For B=1 the one cyclic cell
contains every index.

Two different indices sharing a cell have lifts differing by at most d-1.
Their cyclic difference therefore has norm <=d-1. For d=2^r and s<r, the exact
orbit count at d-1 gives 2/B; for s>=r it is zero. The code labels this result an
upper bound, correctly. The radial event need not coincide with collision, and
collision is not determined by the difference orbit alone. For B=2 the bound
may equal 1. For d=1 every distinct pair has bound zero. B=1 is correctly special.

The sharpness pair is valid throughout B>=4,d>=4. Put i=1 and l=n/2-1. For an
odd sigma, the two image points are u and n/2-u. If their bucket centers coincide,
the sum of the two centered offsets is n/2-2jd modulo n. Its allowed range is
[-d,d-2], so among the possible even multiples of d only zero can occur; thus
j=B/4 or 3B/4. Both offsets can belong to their common half-open cell exactly
when u is strictly within d/2 of that center. The centers and endpoints are even
and d is divisible by four, giving d/2 odd points in each interval. There are d
favorable odd seeds among n/2, hence probability 2/B. The independent checker
also verifies 15 admitted cases with q=10, n from 1024 through 16384 and d>=256.
The sharpness is not restricted to inadmissible tiny windows.

A union bound over a fixed explicit competitor set requires no independence of
pair events. Canonical duplicate/self indices are rejected. A set chosen from
the observed seed is outside the theorem. Marginal buckets are not uniform:
0 always routes to 0, and n/2 always routes to B/2 when B>=2. Tau supplies phases
and a time-domain translation; it never translates the frequency cells.

## 4. True-filter geometry and exact endpoints

For B>=4 and even d=2^r, the guard event uses the **strict** radius 3d/2. Counting
positive odd multiples strictly below that radius yields 3/B for s<=r-2, 2/B
for s=r-1, 4/B for s=r, and zero above r. Since 3d/2<n/2, no antipodal branch is
needed in this specialization. The implemented general radius law also handles
d=1 and other helper endpoints correctly.

On the complement, cyclic distance from the competitor to the target image is
at least 3d/2. The target is at distance at most d/2 from its chosen center.
Reverse triangle inequality in the cyclic metric gives competitor-to-center
distance at least d. The accepted stopband includes equality at d, so no
strictness is lost. This is sufficient geometry for true H, not an exact law
for actual leakage. Replacing the guard by mere different-bucket status would
be invalid.

The q=10,n=1024,B=4 accepted fixture was independently evaluated at all 1024
frequency offsets using outward integer interval arithmetic with 160 fractional
bits. Cosine roots were built by eight positive half-angle square roots from
cos(pi/2)=0; integer square roots bound every radical. Complex interval
multiplication then encloses every root power. Signed tap sums are outward
intervals. Every response enclosure has width below 2^-100. All closed passband,
closed stopband and global magnitude bounds hold for this fixture. This finite
check supplements, and does not replace, the accepted all-window proof.

Exact checks give H_0=16777217/16777216 and H_d=-1/33554432. At d/2, the enclosed
response is above 1-rho, with rho=5/65536. Thus at sigma=1 the pair i=127,l=128
routes into different buckets while the competitor lies at the target bucket's
closed passband edge. Replacing true H by companion D=1 or claiming negligible
interference from different buckets is unsupported.

## 5. Phase moments and the conditional location bridge

With the stated negative-sign unnormalized Fourier convention, Fourier inversion
in the time-domain bucket gives

    Z_j = sum_l F_l exp(2*pi*i*tau*l/n) H_(jd-sigma*l),  Z=nU.

Removing the target phase and using real-even H yields H_o F_i+C_i exactly.
The independent checker verifies 672 such identities in exact cyclotomic rings,
using separate direct time-domain sums and full spectral expressions for n=4,8,16.
These test identities are algebraic tests; their toy taps are not advertised as
admitted accepted windows.

For each fixed sigma, retain the actual filter weights in C_R. Expanding
|C_R|^2 and averaging over uniform tau kills precisely the off-diagonal terms:
for distinct j,l modulo n the sum of the character exp(2*pi*i*tau*(j-l)/n) is
zero. Composite n causes no difficulty; a nonzero character may have lower
order but its full n-term sum is still zero. Individual characters need not be
independent. The diagonal sum is sum |F_l|^2 |H_(jd-sigma*l)|^2. The phase tests
use unequal nonunit weights and preserve all cross terms until averaging.

Conditional uniformity of tau given sigma follows from the expressly required
independence. Averaging over sigma and dividing into the radial guard and its
complement gives the coefficient

    rho^2 + ((1+rho)^2-rho^2) p_l = rho^2+(1+2rho)p_l.

Thus V_R is a valid upper bound for the unconditional second moment. Multiplying
by the sigma-only good-event indicator can only decrease that nonnegative
moment. Markov's inequality yields the candidate's bound on G and |C_R|>eta
without dividing by Pr(G), silently conditioning the seed law, or assuming
independence of isolation and interference.

On G and |C_R|<=eta, triangle inequality supplies |C_i|<=rho L_A+eta. The target
condition therefore remains

    (1-rho)|F_i|-rho L_A-eta >= T+2epsilon.

Together with at most r_select buckets satisfying |Z_j|>=T, this guarantees the
target bucket is selected: otherwise the r_select selected buckets and the
omitted target would all have magnitude at least T, a contradiction. The >=T
crowding count and the full 2epsilon arithmetic margin are essential, including
at ties. Exact counterexamples in the independent checks kill changing >= to >
and replacing 2epsilon by epsilon.

Union over isolation failure, the good-isolation residual event, and crowding
failure proves max(0,1-alpha-V_R/eta^2-delta_crowd). This is a conditional theorem
whose crowding antecedent and useful spectral/parameter margin remain external
obligations. No crowding estimate or general support recovery is inferred from
pair collision. A zero lower bound is vacuous.

Operational use must cover all sampled seeds with the admitted deterministic
call and sufficient output cap J=r_select*n/B. A source that fails on some
values needs a separate unconditional abort bound or justified joint model;
arbitrary value-dependent exceptions cannot be conditioned away. The fixed
whole signal and fixed competitor sets must precede the fresh seeds. Prior
adaptive history is permissible only through a justified fresh conditional seed
law. The companion amplitude guarantee keeps |C_i|+rho|F_i|+(63/512)2^-k.

## 6. Independent verification evidence and mutations

`INDEPENDENT_RESULTS.json` records 44,439 closed-radius cases, 133,317 strict
rational-radius cases, 54 large-integer cases through m=4097, 18,204 independent
nearest-center route checks, 17,820 all-small-pair bounds, 12,486 exact neighbor
probabilities, 521,096 oriented stopband implications, 5,160 fixed-set union
checks, 1,024 true-response offsets, 672 Fourier identities, 170 weighted phase
moments and 16 malformed-input checks. Fifteen admitted sharpness cases are
listed individually. Negative very long signed indices also reduce correctly.

Fourteen adversarial mutations or strengthened assertions are rejected: missing
negative orbit points; doubled antipode; closed-for-strict radius; downward ties;
missing bucket wrap; universal 1/B collision; d instead of d-1 collision radius;
shrinking the guard to d; closing its endpoint; accepting zero difference;
dropping filter weights; dropping 2rho from the moment coefficient; using >T
crowding; and halving the arithmetic margin. The first ten are literal production
code mutations; the final four are exact theorem-counterexample probes.

The author checker was separately cold-extracted and rerun. Its result is
byte-identical to the sealed AUTHOR_RESULTS.json, SHA-256
`063ef55b39e47aa14ca6576e977d9d18b661371978f802e6dcbc885a41d6249f`.
The author inventory also reports 24 payload members. The independent results
are generated from a separately written checker, not inferred from that replay.

Finite checks support the proof and can detect implementation errors. They do
not prove a universal theorem from a tested maximum m, establish entropy quality,
authenticate arbitrary source data, or measure an online sparse runtime.

## 7. Costs and residual obligations

Accept the candidate's conservative O(L^2) single-query classical bit cost, with
actual argument widths and parsing paid. All probability denominators are powers
of two. Across N explicit competitors, accumulated numerator widths add at most
log(N+1), while deterministic sorting costs O(N log(N+1)) integer comparisons.
The stated O(N*(L+log(N+1))^2) bound is conservative. Retain canonical lists,
sorted copies, all returned terms, actual serialized inputs, Python headers and
output serialization. An empty list still has parameter/target validation work;
the set bound is understood with this ordinary O(L^2) setup additive, or N
replaced by N+1 when writing a bound covering N=0 literally. This is a bookkeeping
interpretation, not a theorem or implementation defect.

The spectral quantities L_A and V_R in the interface are symbolic antecedents,
not authenticated or freely computed statistics. Computing a dense complement
sum separately must pay its actual work. No source reads or fresh random bits
are implemented by this helper. Add all
accepted tap preparation/provenance, Qmin=56, per-call roots, numeric widths,
source acquisition/indexing (possibly Omega(n*ell)), read/decode, hash/parse,
source-abort prefix work, reports and J explicit outputs. Dense verification is
paid offline. Actual o(n) work needs sufficient polylogarithmic slack in B and
J. No prior charge is retired by a probability lemma.

The accepted components are the exact odd-dilation orbit kernel, sharp 2/B collision bound, true-filter 3d/2 isolation law and conditional >=T-crowding location bridge. Full sparse recovery, concrete entropy certification and downstream integration remain open. No speed, novelty or priority determination follows.

Still required: independent source acceptance/composition and provider evidence;
source-bound crowding and useful interference/margin parameters; finite-word
repetitions, medians/voting and outer-loop support/output composition; all abort
costs/probabilities; downstream unitary normalization and S6; the distinction
between weak-coordinate and all-input relative-l2 guarantees; trusted response
provenance and unresolved priority assessment. 

## 8. Primary-source attribution check

The reviewer independently reopened the [Hassanieh–Indyk–Katabi–Price primary
paper](https://people.csail.mit.edu/haitham/Papers/sFFT.pdf) on 2026-10-12. Its
Section 3(b), Claim 3.5 and Lemma 3.6 describe odd dilation, phase translation and
the dyadic orbit bound. Section 4.1 uses nearest buckets, magnitude selection and
inverse fibers; later lemmas and repetitions supply further recovery analysis.
The candidate's exact endpoint counts and finite-word bridge are local
derivations. PDF screenshot requests failed with a cache miss, so this review
claims text-level primary-source verification only, not a visual or PDF-byte
certificate. No novelty claim is established.
