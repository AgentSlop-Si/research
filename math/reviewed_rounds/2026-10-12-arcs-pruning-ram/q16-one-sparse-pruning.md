# Independent review of the Q16 exactly-one-sparse pruning repair

Date: 2026-10-12. Verdict: **ACCEPT_BOUNDED** after independent sealed-candidate inspection and
cold replay. The accepted v2 candidate SHA-256 is
54bf4bb33a0e00b4892a4826ed9f3dd185827f8da22d7238e77dc7196dd517c7.
Its 61 manifest payloads and 45 accepted-source member bindings verify. The
author checker and all ten author mutations reproduce exactly; reviewer checks
and ten separately authored mutations also pass. The original v1 candidate is
superseded solely for the explicit A/c and log(t) cost-ledger correction; code
and theorem bytes are unchanged apart from that documentation correction. No external write is
performed by this review.

## Main finding and precise scope

The original unthresholded top-two intersection argument is false on the actual
accepted n=1024, B=4, q=10 fixture. At k=24 the constant signal's exact computed
responses are 16777217/16777216, -1/33554432, -1/8388608, -1/33554432. Top two
selects buckets 0 and 2. The false index n/2 always routes to bucket 2 under an
odd dilation, so repetitions never remove it. This is an actual-interface
counterexample, not an idealized filter construction. Its B=4 coarse 4/B bound
is vacuous; what the example refutes is the unthresholded radial-event implication
and the claimed removal of all false support.

The repair is valid under the explicit exact-one-sparse, trusted-tap,
whole-stable-source and strict-margin promises. It adds an exact half-magnitude
threshold to the top-two list before intersecting complete fibers. The actual
rational-complex API restricts the promised signal class to four cardinal
frequencies. A two-sample exact algorithm already recovers that class, so this
is a narrow API/composition repair and obstruction audit, not a competitive
sparse FFT, a general Q16 closure, or a novelty claim.

## Independent uniform proof

Write a=|F_f|>0 and use the accepted uniform bucket error epsilon and actual
filter leakage rho. The computed nearest true bucket has magnitude at least
L=(1-rho)a-epsilon; all bucket magnitudes are at most U=(1+rho)a+epsilon;
buckets with centers at distance at least d from sigma*f have magnitude at most
S=rho*a+epsilon. The supplied strict margin

    (1-3rho)*a_min > 3epsilon, with 0<a_min<=a,

implies both 2L>U and L>2S. In particular L>0. There are at most two centers
strictly within d of sigma*f, and the nearest true bucket is among them. It
strictly outranks every other center, apart from possibly the one other near
center, so it occurs in the exact top two regardless of ties among near centers.
If P is the largest computed magnitude, L>P/2 follows from P<=U, while
S<P/2 follows from P>=L. Thus thresholding at magnitude >=P/2 keeps the true
bucket and rejects every far bucket. Squared integer numerators implement this
exactly as 4*score>=peak_score; replacing 4 by 2 would be a different threshold.

The retained fibers use the accepted half-open offsets [-d/2,d/2). Their routed
indices have distance at most d/2 from the selected center. That center's distance
to sigma*f is strictly below d. Therefore a fixed false survivor g satisfies

    ||sigma*(g-f)||_n < 3d/2.

Let h=log2(d) and s=v2(g-f modulo n). Under a uniform odd sigma, the nonzero
orbit consists of n/2^(s+1) equally likely residues. Counting its elements in
the strict radius gives 3/B for s<h-1, 2/B for s=h-1, 4/B for s=h, and zero
otherwise. Both signs of a strict boundary are excluded, and B>=4 keeps this
radius below the antipode. Across independent sigma draws, the necessary-event
probabilities multiply for each fixed false index. Different indices need not
be independent. Union bound gives the coarse (n-1)(4/B)^t and the sharper sum

    (n-2B)(3/B)^t + B(2/B)^t + (B/2)(4/B)^t.

These are geometric upper bounds, not exact failure probabilities, and the
abstract complex lemma does not enlarge the executable rational sample API.

The strict margin cannot be changed to a non-strict certificate argument. At
equality, admissible magnitude-error balls can place the nearest bucket at L
and a far bucket at S=L/2, so the inclusive threshold retains the far bucket.
This witnesses insufficiency of the error certificate at equality; it does not
assert that the actual constructor attains all those simultaneous extremal values.

## Exact rational API and the sharper law

Exact one-sparsity implies x_v=(F_f/n)*zeta^(fv). Since x_0 is a nonzero Gaussian
rational and x_1 is a Gaussian rational, zeta^f=x_1/x_0 belongs to Q(i). There
are only four roots of unity in Q(i). One elementary proof tailored to this
power-of-two setting is: a root of order at least eight has a power that is a
primitive eighth root; such a root is (plus or minus 1 plus or minus i)/sqrt(2),
which is not in Q(i). Thus f is 0, n/4, n/2 or 3n/4. This deduction requires the
whole fixed signal promise; rationality only at queried positions is insufficient.

For B>=4 these four frequencies are multiples of d, and any odd sigma maps f
to a bucket center. Exactly one center is strictly within d. Therefore exactly
one bucket survives thresholding. A fixed false g survives a successful trial
if and only if sigma*(g-f) is in [-d/2,d/2) modulo n. For s<h this half-open
interval contains d/2^(s+1) of the n/2^(s+1) orbit residues, giving exactly 1/B.
When s=h-1 the negative endpoint is included and the positive endpoint excluded,
so the probability remains exactly 1/B. For s>=h no orbit residue belongs to
the cell. Precisely n-B nonzero differences have s<h. Consequently

    Pr[full support is not the singleton {f}] <= min(1,(n-B)/B^t)

under the ideal all-success source model. This is a union bound on correlated
false-index events, not an exact whole-support failure law.

The same promise permits exact recovery from x_0 and x_1 alone: compare x_1
with x_0, i*x_0, -x_0, and -i*x_0, choose the unique match, and return the
corresponding cardinal frequency and coefficient n*x_0. Sign changes and swaps
suffice; root finding, randomness, filters and repetition are unnecessary. A
passing two-sample comparison does not validate global one-sparsity. The baseline
is stronger in exact arithmetic and query count under comparable access costs;
no universal wall-time order is asserted for arbitrary address-dependent source
providers.

## Probability, aborts and amplitudes

The stable whole input, trusted taps, widths, trial count, lower bound and caps
must be fixed before the full independent bit tape. Under that ideal tape,
each accepted sampler consumes a disjoint block of 2m-1 bits. Tau is irrelevant
to the mathematical support law; its phases are already covered by the uniform
arithmetic guarantee. No ranking/phase/noise independence is needed within a trial.
The returned first-trial amplitude for the true index obeys

    |Y_f-F_f| <= rho*|F_f| + (63/512)*2^(-k).

The response bias is not erased by repetitions. On singleton support this is
also the unnormalized Fourier l2 error of the returned sparse vector. The
algorithm does not exactly recover the coefficient, unlike the cardinal baseline.

An unconditional bound beta for any operational abort in a coupling to the
full ideal bit tape is added to the relevant geometric failure bound and then
capped at one. No independence between aborts and tape values is assumed.
Conditioning on returned successes instead can bias sigma and preserve false
indices. Arbitrary correlated bits are not repaired by adding beta. A hanging
or unavailable provider has no automatically certified beta or runtime bound.
Reusing the same sigma never gives an exponent t.

## Executable and cost audit

The adapter leaves its accepted dependencies byte-identical. Every trial calls
the existing r=2 single_trial and therefore computes all J=2n/B amplitude/phase
records, two complete bucket passes and two fresh root preparations before
postprocessing. It does not silently use a cached bucket or roots. Cumulative
caps are preflighted before source access. Source exceptions propagate with
identity; completed work and consumed prefixes remain paid, and no retry occurs.

Thresholding forms B integer squared scores. Filtering is linear in J, sorting
is deterministic bottom-up merge sort, and intersection is a sorted linear
merge that preserves the first-trial records. There is no dense n-length
membership bank. Sorting adds O(t*J*log(J+1)) comparisons at m-bit index cost;
the current/previous pools use O(J) records and the trace uses O(t) records.
Those are record counts, not constant-bit-space statements. Actual score widths,
phase precision, all source and bit-provider work, numerical parsing and
serialization, Python allocations, hashing/provenance and cold tap construction
remain paid. Consecutive full trial reports can transiently coexist during
assignment, a constant-factor footprint already covered by O(J+B) live records.

No public status string authenticates one-sparsity, trusted taps, ideal entropy,
or the whole source. Returning a singleton under violated promises is not a
certificate that the singleton is correct.

## Independently authored evidence

The reviewer checker uses its own half-cell and orbit enumerations, including
5,115 nonzero valuation cases, 19,584 protected-center/fiber endpoint checks and
960 half-cell tie checks. It exhausts all 1,024 independent two-seed pairs at
n=64,B=4 and verifies each false-index survival probability exactly. These
particular two-trial parameters have whole-support failure probability one;
the census is not represented as an operational success demonstration.

The reviewer found the deterministic endpoint-fixture sigma sequence
[1,7,43,129]. Actual execution with it isolates every cardinal frequency,
including non-dyadic complex coefficient cases, in four trials. Every case
independently meters eight root preparations, 5,128 sample calls, 76 bits and
2,048 pre-threshold amplitude/phase records. It compares every trace intersection
to a separate exact fiber oracle and checks the final amplitude error.

Fourteen invalid preflight variants consume no sources or roots. Cross-trial
exceptions test bit positions 19,20,38 and sample positions 641,1283,2564,
checking exact exception identity, source counts and already-paid roots. There are also 148 exact probability-helper cases. Twelve
exact baseline cases include abstract dimension m=127 and non-dyadic complex
amplitudes. Ten fresh literal mutations are killed, covering strictness,
squared-score thresholding, filler retention, repetition/abort/false-count
formulas, first-trial amplitude preservation, frequency scaling and the second
sample pass. These bounded checks supplement, rather than prove, the uniform
mathematics and source assumptions.

## Scope and remaining work

The accepted result is the actual top-two-only obstruction and narrowly scoped threshold
repair, with the cardinal restriction and exact two-sample baseline. The result
is exact support with the displayed conditional probability and bounded amplitude
error; it does not establish unqualified exact full recovery or all-input l2 recovery. General noisy/multi-sparse aggregation,
concrete providers, source acquisition, full Q16/STR-Q1 closure, unitary/S6
integration and novelty/priority remain open. 

Public derivative note: private tracking instructions are omitted; the mathematical proof and remaining limits are retained. Original report SHA-256: `4bee9f3437cd7dda6717bb259da447876f757b68917668818ae5847123063e14`.
