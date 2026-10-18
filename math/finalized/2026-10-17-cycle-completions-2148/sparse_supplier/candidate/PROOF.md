# Sparse-original, arbitrary-index ALG-034 supplier

17 October 2026 UTC. Fresh candidate; independent final review is separate.

## 1. Completed interface and retained boundary

The previous accepted large-N producer admitted only quarter-axis support at
B_A=N, and its downstream realization admitted the constant delta_0 source.
This new implementation admits canonical sparse complex dyadic original inputs
at **arbitrary indices**, with up to 64 nonzero coordinates, every dyadic length
N=2^m with 2<=m<=64 (odd m included), and singleton B_A=N. It returns an exact
modal description of U_N(Px), a normalization with 1/2<norm<=1, and a live lazy
query method that computes certified dyadic point values at any j in [0,N).

This closes a producer interface beyond the quarter-axis family. It is not a
change to the caps of an old general backend. It is not an arbitrary dense-input
algorithm, support discovery, general B_A, the rounded serial recurrence, or
bit-equivalence with that recurrence. The exact modal expression and a
numerical fixed-point query are deliberately different mathematical objects.

The new production source imports only dataclasses, hashlib, math.isqrt and
json. It imports or executes no historical research program, reads no files,
uses no network, floating arithmetic or transcendental approximation library,
and contains no loop over N, p, D=N or a time-window support radius.

The independent companion bucket packet owns all window construction, bucket
error, output, and downstream theorem claims. It can consume the exact modal
expression directly. A point-query accuracy theorem alone does not prove the
accuracy of arbitrary future computations on those points.

## 2. Original context and exact input

Input schema ALG034_SPARSE_DYADIC_V1 has precisely N,F,entries,schema. Each
entry [n,re,im] denotes x_n=(re+i im)2^(-F), and every omitted coordinate is
exactly zero. This is the supplied original sparse vector, not an unevaluated
callback or a claim to have read an arbitrary dense vector. Entries must be
strictly increasing, unique, in range and nonzero; at least one nonzero
Cartesian numerator is odd. The zero vector has empty entries and F=0.
These conditions make the representation canonical.

Exact built-in types are required. Booleans, floats, subclasses, tuple/list
coercions, duplicate summation, extra keys and noncanonical powers of two are
not admitted. Raw numerators have at most 1024 magnitude bits; F,t,q and caller
p at most 128. The state has exactly N,B,a,beta, with B=N, odd 0<a<N and
0<=beta<N. No quarter-axis restriction remains. All input data is copied into
immutable tuples/bytes before successful return.

The trusted execution model is the pinned unmodified source, correct Python
integer/stdlib semantics, no hostile interpreter reflection, and no concurrent
caller mutation during validation. Frozen dataclasses are not a sandbox or an
attestation protocol.

## 3. Exact source, normalization and transform identities

For singleton balanced blocks, the relative block coordinate t is zero, each
chirp phase is one, and compression/expansion P is the identity. Let c_n=re_n+i
im_n and E=sum |c_n|^2. The ideal target is exactly

    y_j = 2^(-F) N^(-1/2) sum_n c_n exp(-2 pi i n j/N).

This equation, the original integer entries and N,F completely specify an exact
finite algebraic expression. A sparse modal description has representation
error zero without claiming that all its values are dyadic or have been
materialized. For a nonquarter-axis phase, those values will usually be
irrational.

For nonzero E define

    h = ceil(log2(sqrt(E))) = (bit_length(E-1)+1)//2,
    A_norm=2^h, alpha=2^(h-F), z=y/alpha.

Then E<=A_norm^2<4E. Unitarity gives

    ||z||_2^2 = E/2^(2h),       1/2 < ||z||_2 <= 1.

The strict lower inequality is valid even when E is an exact power of four.
The normalization scale remains symbolic when |F| is huge. The descriptor
retains E, h, raw l1 mass, entries and the exact normalized norm squared. In
particular the normalized l1 coefficient mass is

    lambda = sum(|re_n|+|im_n|)/2^h.

It need not equal one; a downstream tail estimate must multiply by the actual
lambda or a proved upper bound. Cauchy-Schwarz gives lambda<=sqrt(2s), but no
consumer is allowed silently to replace it by one.

The negative-sign unitary transform squares to reversal, so

    U_N z = R(x)/alpha.

Its nonzero frequencies are -n mod N with coefficients c_n/2^h. Thus the live
source has an exactly specified sparse second-transform target. Zero input
returns EXACT_INPUT_ZERO and no normalized descriptor, no p and no query;
P=I implies there is no nonzero projected-zero case in this family.

## 4. Exact root enclosures, without a root table of length N

Set b to the query working precision and D_b=2^b. Every interval [l,u] below
means the exact real interval [l/D_b,u/D_b]. Products take all four integer
endpoint products and round their extrema outwards by floor/ceiling division
by D_b. Negation reverses endpoints. Integer scaling and addition are exact.
Complex multiplication uses (ac-bd,ad+bc) and these outward operations.

For a nonnegative dyadic interval a, sqrt_interval computes

    floor(sqrt(l D_b)), ceil(sqrt(u D_b))

with integer square root and an exact perfect-square check. This encloses the
true square root because squaring is monotone on nonnegative numbers.

The setup retains m+1 roots, not N roots. Roots of order one, two and four are
exact. Starting with c=0, s=1 for pi/2, a step from order 2^(ell-1) to 2^ell is

    c_new=sqrt((1+c)/2),    s_new=s/(2 c_new).

The positive branch is correct for these half angles. The code uses outward
halving, square root, and division by the positive cosine interval. The sine
formula avoids subtraction of two numbers close to one. The stored complex
root is (c_new,-s_new), hence has the negative DFT sign.

If k=sum_t bit_t 2^t, then

    exp(-2 pi i k/2^m) = product_{t:bit_t=1} exp(-2 pi i/2^(m-t)).

root_at evaluates precisely this product using at most m stored roots. This
identity covers all quadrants, wraparound and arbitrary original indices;
there is no approximation to pi in production. An original query phase is
computed exactly as n*j mod N before root evaluation.

For even m, N^(-1/2) is an exact dyadic. For odd m the supplier encloses sqrt(2)
by the same integer-square-root procedure and divides it by 2^((m+1)/2). Thus
odd dyadic lengths introduce an explicitly paid algebraic enclosure, not a
floating sqrt or a hidden even-exponent assumption.

## 5. Query rounding and certified error

For requested normalized error exponent R in [8,4096], the code sets

    b = R + W + bit_length(s) + 4m + 32,

where W is the maximum raw Cartesian numerator width. It sums the certified
complex character products with the exact integer coefficients, multiplies by
the certified N^(-1/2), and divides outwards by 2^h. The resulting rectangle
contains the exact z_j.

A point is selected on the coarser grid 2^(-G), G=R+3, by rounding each
rectangle midpoint. Let the rectangle endpoints, rescaled point and maximum
Cartesian distances in units of 2^(-b) be l_d,u_d,v_d and
r_d=max(|v_d-l_d|,|u_d-v_d|). The code checks the exact integer inequality

    r_re^2+r_im^2 <= 2^(2(b-R)).

Only then does it return the claim |z_hat_j-z_j|<=2^(-R). This check uses the
entire enclosing rectangle, not a heuristic or a comparison with floating
truth. A resource or precision failure returns no successful query certificate.
A query receipt charges the complete evaluation and its serialization.

The guard precision is ample throughout the declared domain. For completeness,
one conservative enclosure-width argument is as follows. Since b>=50 and m<=64,
all half-angle cosine lower endpoints exceed D_b/2. The cosine interval width
in integer units grows by at most three per step (the square-root map is
1-Lipschitz on its arguments here, including outward rounding). For the sine
quotient, width grows by at most four times the current cosine width plus two;
the previous sine's endpoints are at most 2D_b. Induction bounds every primitive
Cartesian width by 128m^2 units. The premise endpoints<=2D_b is preserved because
128m^2<<D_b.

If a product's endpoints are within delta of its exact Cartesian coordinates
and a primitive root's are within epsilon, outward complex multiplication
bounds the new Cartesian error by 4delta+2epsilon+4/D_b, using epsilon<=1.
With at most m products and epsilon<=128m^2/D_b, a loose bound is
256m^2*4^m/D_b <=2^(3m+9-b), since m^2<=2^(m+1) for m>=2. Raw l1 mass is less
than 2s*2^W. Normalizer rounding adds at most a few units divided by D_b;
dividing by 2^h does not enlarge error. The chosen b leaves over twenty bits
beyond R even under these loose bounds. Midpoint rounding to G=R+3 therefore
comfortably passes the exact final squared-radius check. Correctness of any
successful query does not depend on the tightness of this auxiliary width
estimate: it follows from enclosure arithmetic and the checked inequality.

## 6. Accepted policy, original grid and its honest limitation

The inherited all-length policy is retained and specialized by proof, not by
running the old serial implementation. The prior accepted producer and final
review supplied with this task contain the verified original policy report
hash 7153cde50511545ea2b63b3ab7a67efc0b7222ba0b96c1ef76d1612635564062.

For any admitted dyadic N, L=2N and Phi_(2N)=X^N+1, D=N. Every singleton
polynomial is re+im X^(N/2), already reduced. Its nonzero status and aggregated
l1 mass are exact. Choose the smallest positive mass A_policy over explicit
entries, tie-breaking by index. Then

    K=bit_length(A_policy-1), G_policy=W+(N-1)K,
    H=1, C=2^c, c=N+3m+6,
    p_min=max(W,c+t+1,c+q+G_policy+2),
    I=N+2m+10, kappa=W-F-p.

The code checks t>=0,q>=m and p>=p_min, with bounded-width p metadata. It never
constructs C, a cyclotomic polynomial of degree N, or a p-bit numerator.

A normalized query is point_base*2^(-G). Multiplication by alpha gives an
original-target approximation with error at most 2^(h-F-R). When

    shift = p+h-W-G >=0,

its exact original p-grid integer is point_base*2^shift, since adding kappa to
the shift gives h-F-G. The code returns this symbolic integer and verifies its
formal width is <=p+I. It does not expand shift zeros into memory.

The point meets the accepted serial radius C*2^kappa exactly when the certified
budget comparison R>=p-c-W+h also holds. `query(j,True)` requires both conditions
and otherwise rejects. The packet reports whether they hold. Even an accepted
query does **not** claim to equal the rounded serial algorithm's output.

This distinction matters for inputs with A_policy>1: G_policy can make the
inherited serial radius fantastically small. A bounded 4096-bit numerical
query cannot be advertised as achieving every such p-dependent budget. The
exact modal description remains exact; the normalized numerical query still
has its stated independently checked error; an original serial-radius query
may be unsupported. Merely storing inherited p metadata is not a numerical
certificate. No such general equivalence or unrestricted precision claim is
made here.

## 7. Actual nonconstant theorem-scale instance

The fresh executed fixture is

    N=B_A=2^28, a=1, beta=0,
    x=delta_1+delta_3, F=0, t=16, q=464.

Both support indices are non-quarter-axis. E=2, h=1, alpha=2, norm(z)^2=1/2,
and

    z_j = (exp(-2 pi i j/N)+exp(-6 pi i j/N))/(2 sqrt(N)).

This is a nonconstant source. Its second transform is exactly
(delta_(N-1)+delta_(N-3))/2. The source therefore meets the norm condition and
has a genuine two-sparse second-transform target (also within k=32).

The policy is p=268436013, c=268435546, kappa=-268436012, and accepted original
radius 2^-466. Default R=q+4=468 gives G=471 and b=615. Numeric point error is
<=2^-468 normalized and <=2^-467 in the original target, strictly below the
accepted radius. The symbolic original-grid shift is 268435542. No integer
with that many physical trailing zeros is allocated.

Fresh source setup, replay and six actual queries j=0,1,17,2048,2^27-1,N-1
were executed. The nonzero-phase queries require nonaxis roots. They were
cross-checked against a separately implemented rational Machin-pi/Taylor
oracle, including independent verification of their point error budgets.
The companion integration uses the same exact raw support with nonzero tau
and emits its own complete 131072-bin result and receipts. That downstream
result is outside this producer proof.

## 8. Caller-relative semantic verification

`verify(raw,state,t,q,packet,p=None,query_bits=None)` validates the complete
packet grammar, freshly runs this producer on the separately supplied original
arguments, and compares the complete canonical packet, including exact modal
entries, original state, normalization, policy and every root enclosure.
`verify_query` similarly redoes setup and the exact requested point query.
A digest is only a label; the soundness argument is equality with a recomputed
correct result for the independently retained original context.

Tests reject changed source/root/policy/query fields, added attestation claims,
oversized packet trees, wrong query indices, and a wholly self-consistent fresh
packet for another original input. Mutable copies and later raw-input mutation
cannot alter a returned frozen run. Replacing both the independently retained
context and answer changes the statement being checked; the verifier cannot
authenticate an external origin or attest a historical process. Both false
claims are explicitly denied.

## 9. Work, storage, serialization and complete-output accounting

Setup reads all s supplied entries and creates O(m) root rectangles at b bits.
Each point query performs at most sm root products, O(s) coefficient products
and normalization. Setup therefore has O(s+m) logical arithmetic records and
a query O(s(m+1)), with integer-width-dependent costs. Since m<=64 here this
is bounded-constant times s; asymptotically one must retain the log N factor.
It is not an O(s) bit-time or a free transcendental-oracle claim.

Every record expands into at most 32 elementary integer operations and is
charged 4096*(sum of operand/result widths+32)^3 binary work units. Products
and square-root radicands are separately recorded so intermediate widths are
included. The cubic envelope conservatively covers schoolbook operations,
integer-square-root algorithms and copying under the stated binary model.
It is not a statement about exact Python instructions or wall time.

Let E_cost=records+serialized_bytes+logical_slots+4096 and
V=max_recorded_width+bit_length(E_cost)+64. An additional 2^16 E_cost V^3 work
and 4096 E_cost V cumulative-storage allowance covers bounded validation,
branch/index scans, metadata arithmetic, JSON conversion/copying, hashes and
receipt counters. A 16 KiB ledger reserve is paid before returning. The final
result includes these conservative (intentionally loose) bounds.

Caps are: 64 entries, m<=64, 1024-bit raw numerators, 128-bit input metadata,
8<=R<=4096, working b<=6000, recorded arithmetic width<=12288 and at most one
million records per successful API call. Canonical serialization permits at
most 50000 tree nodes, depth16, lists256, dictionaries64, bounded4096-character
strings, 12288-bit integers and2 MiB total bytes. All these are enforced before
successful canonical packet handling. No historical cap was silently removed.

One public packet export has a separately advertised conservative bound of
2^100 bit-work and2^50 cumulative-storage units for this bounded domain. Calling
execute or query alone does not pay future exports. Replay pays its own full
setup/query, canonicalizations and one export; executing then replaying requires
adding both receipts. Source loading/pin checks, outside input acquisition,
consumer loops, output writes and downstream windows are additional costs.

For Q requested indices, total work is setup plus all Q query receipts, all
exports and actual destination serialization/writes. There is no query cache
or uncharged batch reuse. If the task requires every DFT coordinate, Q=N and
the full cost has the N factor and at least N output writes (and their bit
length). The representation is compact because it is an expression, not
because a full output has been produced sublinearly. SMALL_FULL_DFT.json
contains all16 paid coordinate queries of a fresh N=16 arbitrary-support
example; its accounting includes16 queries,16 exports and destination work.
The theorem-scale run deliberately does not claim a full268435456-point output.

Exceptions on grammar, scope, resource, precision or arithmetic invariant
failure yield no success certificate. Host allocation/interruption likewise
cannot become a successful numerical result. There is no retry that loosens
policy or normalizes an approximate zero.

## 10. Fresh controls and scope of evidence

The check suite includes independent rational root/query oracles, arbitrary
complex coefficients and both odd/even small dyadic lengths; actual large-N
nonconstant queries and original-grid budgets; original-context replay;
complete small-N output; maximum m64/s64/1024-bit-input/4096-bit-query execution;
zero and resource cases; and adversarial source/query substitution. Source
loading of this new module is the only research-program import. The oracle is
fresh test code and is not part of the production runtime receipt.

CHECK_RESULTS.json records exact counts, receipts, source hash and observations.
Finite checks corroborate the algebraic/enclosure proof; they do not prove
arbitrary dense input, general blocks, serial rounded equivalence, all requested
query precisions, external source authenticity, full sparse recovery, a
sublinear full DFT, universal FFT speedup or novelty.
