# Nonconstant sparse-original ALG-034 → genuine-parameter BUCKETS

Candidate extension, 17 October 2026. This packet contains a freshly authored
numerical backend; no predecessor program is imported or executed. Acceptance is
limited to the exact sparse-modal producer family described below.

## 1. Exact operator and original-input binding

Let M=N=2^28 and B_A=N. Singleton blocks give P x=x for every admitted ALG-034
phase state. The separately supplied canonical original input is

    x_n = 2^(-F) c_n,  n in S,  c_n Gaussian integers, |S|≤16.

The live producer executes on that original input and state, validates their
canonical grammar, and constructs the exact modal descriptor for U_negative x.
Let E=Σ|c_n|²>0 and h=ceil(log2(sqrt(E))), equivalently the least integer h≥0
with E≤2^(2h). Set α=2^(h-F). The exact normalized source is

    v_j = (1/sqrt(M)) Σ_(n in S) a_n exp(-2πinj/M),  a_n=c_n/2^h.

Unitarity yields ||v||²=E/2^(2h) in (1/4,1], so ||v||>1/2. This is an exact
modal representation, with no source approximation or re-quantization error.
Any separately exported finite query has its own proved query error and paid
receipt; the BUCKETS evaluator does not pretend to have queried every source
coordinate. The second negative-sign unitary transform targets R x/α, not Ux.

The numerical engine alone cannot authenticate its descriptor. The adapter must
invoke the pinned fresh supplier on separately supplied raw/state, derive these
entries and h from that computed run, retain the original context, and compare
full canonical output on semantic replay. Replacing both the retained original
and claim changes the statement. No claim of historical execution or external
origin authentication follows from a digest.

## 2. All known window/theorem parameters remain genuine

    m=28, β=5/56, βm=5/2≥2, k=2^ceil(2βm)=32,
    M=268435456, B=2^ceil((1/2+β)m)=131072=4096k,
    T=M/B=2048, ell=8B=1048576, g=T/4=512, H=3T/4=1536,
    r=2m+1=57, W=2r(ell-1)+1=119537551<M,
    P=16m+16=464, rho=2^-464.

The implementation checks these exact formulas and all these guards. Every odd
0<σ<M and every 0≤τ<M is accepted. The window's own pass/stop error is distinct:
δ_window=(2H+1)/16^r=3073·2^-228≤M^-4. The integer inequality is checked.
No outer all-length dispatch or its separate t<M condition is established here.

## 3. Frequency identity for arbitrary sparse original indices

Let c_t^box be the exact centered 2r-fold convolution of the normalized length
ell box, supported on |t|≤r(ell-1). Its transform is

    Φ(q)=[sin(π ell q/M)/(ell sin(πq/M))]^(2r),
    Φ(0 mod M)=1.

It is real, nonnegative, even and M-periodic. Define the original window

    C=Σ_(a=-g)^g Φ(a)≥1,
    D_H(t)=Σ_(a=-H)^H exp(2πiat/M),
    w_t=M c_t^box D_H(t)/C.

The same ideal BUCKETS operator as the accepted component is

    bucket_j=(1/sqrt(M)) Σ_t w_t v_(σt+τ) exp(-2πijt/B).

Substituting the exact source and interchanging the finite sums gives

    bucket_j = Σ_(n in S) a_n exp(-2πinτ/M) K(jT+σn),
    K(q) = [Σ_(a=-H)^H Φ(q-a)]/C.

The plus sign in jT+σn and the negative phase sign are essential. This formula
holds for every original support index, including non-quarter-axis indices; it
is not a constant-source shortcut or a different approximate window. W<M also
preserves the original signed-support representation without aliasing. No
rounded root power, approximate FFT or ideal-oracle substitution is hidden.

## 4. O(T+s) expensive scalar preparation, with all B outputs paid

For a mode n, retain a bin j precisely when d=dist_M(jT+σn,0)<2T. There are at
most four retained bins per mode. Five candidates around floor(-σn/T) contain
them all, and an exact circular-distance test rejects the others. Only these
retained terms need numerical evaluation. Their numerator arguments satisfy

    dist_M(jT+σn-a,0)≤d+H≤2T+H-1=5631.

The engine evaluates Φ(d) for d=1,...,5631 once, also retaining exact Φ(0)=1.
There are 129 numerator sine enclosures because |sin(π d/256)| has period 256
and reflection symmetry. Denominator sines are explicitly evaluated and paid.
Cumulative prefix intervals let every shifted K(d) use O(1) interval sums:

    d≥H: sum Φ(d-H),...,Φ(d+H);
    d<H: Φ(0)+sum_(u=1)^(H-d) Φ(u)+sum_(u=1)^(H+d) Φ(u).

These identities use evenness, not subtraction of unrecorded window samples.
At most 4s shifted windows and 2s phase sine calls are needed after preparation;
repeated d values can reuse already paid immutable interval values. All
coefficient products, normalization, source-dependent phases, window products,
accumulation, rounding and certificate checks are charged. Every one of the
B=131072 output pairs is explicitly appended and charged, including zeros.
There is no N-entry source, W-entry tap vector or actual FFT in this path.

## 5. Certified omission of distant modal contributions

For any omitted mode-bin pair d=dist_M(jT+σn,0)≥2T. For every |a|≤H, the circular
triangle inequality gives dist_M(jT+σn-a,0)≥2T-H=5T/4. After folding to [0,M/2],
sin(πu/M)≥2u/M and |sin(π ell u/M)|≤1, hence

    Φ(jT+σn-a)≤[M/(2 ell (2T-H))]^(2r)=20^(-114).

Thus K(q)≤η=(2H+1)/20^(114), since C≥1. The exact checked inequality is
η<2^-480. This single certificate covers all omitted bins and every arbitrary
original support position, without scanning N or summing B window tails.

Let λ=Σ(|Re c_n|+|Im c_n|)/2^h. The modulus of the total omitted contribution at
any bin is at most ηλ. By Cauchy-Schwarz and the chosen normalization,
λ≤sqrt(2s)≤sqrt(32)<6. Therefore its modulus is <6·2^-480. The implementation
uses the exact actual λ, with a conservative upward K-grid rounding, rather
than replacing it with an empirical numerical tail. This handles complex
coefficients and cancellation honestly. In particular, far-bin error does not
assume nonnegative coefficients or sum of coefficient magnitudes equal to one.

## 6. Fresh finite interval arithmetic and complex output certificate

All interval endpoints are integers on the fixed K=560 grid. A fresh Machin
π=16 arctan(1/5)-4 arctan(1/239) evaluator uses exactly K+8=568 alternating
terms and encloses the next-term remainder with outward integer divisions.
Rational argument reduction by exact integers handles the full 2π period,
reflection, signs and exact zero/unit axes. The reduced angle lies in [0,π/2].

Every sine uses 128 odd Taylor terms through degree 255. The degree-256 Taylor
polynomial is identical, and its Lagrange remainder on |x|≤2 is at most
2^257/257!. The exact shared factorial certificate checks that this remainder
is at most one K-grid unit. The angle midpoint radius is added using the
1-Lipschitz bound for real sine. Every recurrence endpoint division rounds
outward, and intersecting with [-1,1] uses a separately true analytic bound.

Positive ratio intervals for Φ are raised to power 114 by fresh binary
interval multiplication, with outward division by 2^K at every multiply.
This differs from the old enormous exact endpoint-power temporary; it keeps
integer widths small while preserving containment. Nonnegative clipping to
[0,1] follows the normalized Dirichlet-kernel bound. Prefix subtraction uses
lower minus upper and upper minus lower, so shared-error correlations are never
assumed. Dividing by the strictly positive C interval encloses the true K(d).

The phase uses cos(2πnτ/M)=sin(π(M+4nτ)/(2M)) and
-sin(2πnτ/M). Real and imaginary coefficients, signs and normalization are
propagated as exact outward intervals. Let retained-sum intervals for a bin be
I_R and I_I, and let the returned P-grid pair be (q_R,q_I), rounded separately
by signed ties to even. Define U=2^(K-P) and

    e_R=max(|q_R U-I_R.lo|,|q_R U-I_R.hi|), likewise e_I,
    e_tail=ceil(ηλ·2^K).

The exact integer acceptance test is

    e_R²+e_I²≤(U-e_tail)²,  with e_tail<U.

The triangle inequality proves total complex error at most 2^-P for that bin.
For a bin with no retained terms, zero has error ≤ηλ, so the same budget holds.
Finite accepted computations therefore prove max_j |returned_j-ideal_j|≤rho.
Numerical uncertainty never becomes a guessed small error: a failed radius
check gives no successful result. The actual positive controls must pass.

## 7. Restricted result, not general recovery or serial equivalence

This expands the predecessor's constant δ_0 source to arbitrary original
indices in the supplier's bounded sparse-input family. The nonconstant fixture
x=δ_1+δ_3 has h=1, exact norm squared 1/2, and genuine non-axis phases. Nonzero τ
produces genuinely complex retained bucket values. Changing σ shifts their
windows; changing original support changes the computed exact source. Original
state remains semantically bound even though singleton blocks remove its
mathematical effect.

No general dense ALG-034 supplier, arbitrary-length dispatch, randomized
recovery, location/amplitude estimation, amplification, probability bound,
outer t<M condition or complete Q16 recovery has been proved or executed. This
backend is directly certified against the same ideal target. Equality with the
legacy serial rounded output remains unproved and is never asserted.

## 8. Paid resource and trust boundary

The numerical engine has finite cumulative caps: 30,000,000 metered integer
operations, 20,000-bit observed numeric integers and 8,000,000 logical slots.
It admits at most 16 support entries, each Gaussian component at most 1024 bits,
and the fixed theorem parameter set above. A successful receipt counts source
loading, arithmetic, prefix storage, retained terms, phase roots, full output
construction and cache reuse. Fixed conservative 2^75 work / 2^42 storage
loading envelopes and event-based control envelopes include bounded parsing,
imports and untraced control/index work. These are logical schoolbook bit-work
and cumulative-storage upper bounds, not claims about Python peak RAM or wall
time. A rejected arithmetic operation can form a finite temporary before its
post-operation width check; input widths and operation form bound that effect.

The separate adapter adds the live supplier's paid receipt and bounded
canonicalization/replay/export envelopes. Trusted correct Python/stdlib,
correctly executing pinned fresh sources, no hostile monkeypatching or private
state mutation, and independently retained original context are assumed.

## 9. Uniform first-run precision and finite resource sufficiency

The family statement is stronger than success of the two-support controls.
Here are deliberately loose a priori bounds for one fresh admitted ≤16-mode
execution. Widths below are measured in K-grid integer units.

The 568-term Machin interval has width at most 20(568+1)<2^14. Reduced angle
width is at most half that plus two rounding units. In the midpoint Taylor
recurrence, an individual term width is at most six: the largest recurrence
factor is ≤4/6 and each floor/ceiling pair adds at most two units. Summing 128
terms and adding the angle radius and shared tail gives sine width <2^14.

For 1≤d≤5631, ell sin(πd/M)≥ell·2/M=2^-7. Its lower endpoint is therefore at
least 2^-8, and its width is at most 2^34 grid units. The normalized sine ratio
interval has width <2^52, including outward quotient rounding. Since all
nonnegative multiplication operands stay in [0,1], a product's grid width is
at most the sum of the input widths plus two. Binary power 114 therefore has
width ≤114·2^52+2·113<2^59. Every Φ interval obeys this bound.

A prefix width is <5632·2^59<2^72. C has width ≤1024·2^59=2^69 and lower endpoint
at least 1. Every retained numerator has width <2^74 and upper endpoint <3074.
The quotient K(d) consequently has width <2^74+3074·2^69+2<2^82.

For either real or imaginary normalized modal coefficient, summed interval
width over all modes is at most λ·2^14+2s<2^17, while the sum of maximum absolute
endpoint magnitudes is <7. A product interval's width is bounded by maximum
magnitude of its first factor times the second width plus the analogous other
term, plus two outward grid units. Therefore each final retained complex
component has width <7·2^82+3073·2^17+2s<2^87.

P-grid midpoint rounding gives e_R,e_I≤U/2+2^86. Since U=2^96,

    2(U/2+2^86)^2 < (3U/4)^2.

Also e_tail≤ceil(6·2^-480·2^560)<U/4. Thus the exact per-bin radius acceptance
check necessarily passes for every admitted ≤16-mode input and every legal
σ,τ on a fresh sufficient-budget engine. The run-time checks independently
verify the actual, much tighter inequalities; they do not replace this bound.

A direct source-level bound is fewer than 2048 recorded arithmetic operations
per expensive Φ or numerator-sine preparation, fewer than 20000 additional
Machin/factorial/setup operations, and fewer than 8192 per admitted mode in the
source-dependent stage. Hence a fresh run has fewer than

    (5631+129)·2048 + 20000 + 16·8192 < 2^24 < 30000000

metered arithmetic operations. Its recorded integers stay below 9000 bits:
the largest are the fixed 239-power Machin terms; coefficient, energy,
phase, normalization and interval-product integers stay below that bound even
at the 1024-bit coefficient cap. Preparation allocates fewer than 2^19 logical
slots and one run fewer than 2^20 further slots, below the 8000000 cap. The
full B output is included in these counts. Cumulative repeated calls can
reach the declared cap and then reject; no infinite free reuse is promised.

The actual fixture ran with 8,035,044 recorded numeric operations, maximum
8994-bit integers and 947,891 logical slots. A separate multi-call live
integration control run executed eleven complete B-output evaluations, with
1,441,792 paid coordinate writes, 8,090,691 numeric operations and 7,504,083
logical slots. The latter is a test workload, not an assertion that eleven
calls are the only possible useful deployment schedule.

## 10. Exact modal source versus separately finite point queries

The pinned fresh supplier also exposes finite certified point queries. Their
requested accuracy, accepted original-grid compliance and cost are separate
from the exact descriptor consumed here. In particular, default q=464 supplies
query_bits=468 on the fixture, which passes the accepted-radius check. A coarse
query_bits=8 setup still computes the same exact modal descriptor and hence the
same certified BUCKETS output, but an attempted accepted-radius finite query is
rejected. This distinction is an explicit successful control. No finite-query
accuracy or original-grid equivalence is inferred from the mere existence of
the descriptor, and no query cost is silently omitted when a query is made.

The pinned supplier was newly authored in the paired task, read in full before
loading, then vendored at SHA256
5c1454ef006d34c91be02643a57ebf4cd47adaf9aaaf85fb951e98095ca439ed.
The adapter checks this pin before import and records it in every packet.
`NUMERICAL_CHECK_RESULTS.json` reports 262222 author-run assertions with an
independent numerical algorithm (704-bit endpoint recurrence/exact powers and
a direct signed-window small fixture). `INTEGRATION_CHECK_RESULTS.json` reports
41 live integration/binding assertions. These are author controls, not a claim
of acceptance by a separate independent reviewer.
