# A support-blind finite recovery gate for the accepted sparse-original family

18 October 2026. New recovery result; candidate pending independent review.

## 1. What is newly closed, and the exact contract

The accepted supplier and nonconstant BUCKETS evaluator are dependencies, not
new results of this packet. The new construction consumes **only finite bucket
values**, locates unknown frequencies by finite sign decisions, and produces a
sparse coefficient approximation. It never reads the supplier's support list,
active-bin list, modal descriptor, or source coefficients. The local integration
driver retains those privately to supply the already accepted measurements and
to check the returned answer. This is a deliberate value-only recovery interface;
the raw source is already sparse, so no algorithmic speed advantage is inferred
from solving this interface rather than reading the original entries.

Keep the accepted parameters

    M=N=2^28, B=2^17, T=M/B=2048, s<=16,
    H=1536, g=512, r=57, ell=2^20, rho=2^-464.

The nonzero original input has singleton B_A=N and canonical dyadic Gaussian
integer coefficients at arbitrary indices, at most 1024 bits per component.
The accepted live supplier gives normalized Fourier-mode coefficients

    a_n=c_n/2^h, sum |a_n|^2 in (1/4,1], lambda=sum(|Re a_n|+|Im a_n|)<6.

The target of recovery is the second negative unitary transform R(x)/alpha:
output index k=-n mod M carries a_n. It is not the original first Fourier
transform. Neither F nor the possibly huge alpha exponent is expanded here.

For every legal sigma,tau, the finite provider returns all B P-grid complex
values b_j(tau), P=464, with

    |b_j(tau)-sum_n a_n exp(-2 pi i n tau/M) K(jT+sigma n)|<=rho.

The K here is exactly the accepted original ideal window, not a substitute.
The provider additionally evaluates the public, source-independent scalar K(d)
on demand with the accepted 560-bit interval of width at most 2^82 grid units.
All calls, preparation, parsing, values, scans, roots, intervals and outputs are
paid. A uniform random odd sigma is sampled independently of the fixed input.
The provided executable accepts that sigma as an explicit tape value; the
demonstration tape is fixed and does **not** purport to generate randomness.
Supplying an actual uniform sigma needs 27 unbiased random bits and the paid
map sigma=2u+1. This is an explicit randomness interface assumption.

Set theta=2^-400. With probability at least 2033/2048, the decoder returns at
most s genuine target locations, contains every |a_n|>=2 theta, and has:

    each returned coefficient error <=4 rho,
    ||returned_sparse_vector - R(x)/alpha||_2 <=9 theta.

The guarantee is joint successful return and accuracy. On the complementary
bad event, the decoder may reject or return an inaccurate result. The output
does not claim to contain an observed isolation certificate. No independent
amplification theorem, arbitrary dense case, non-singleton blocks, all-length
dispatch, outer transfer, rounded-serial equivalence, or full N-coordinate
output is established.

## 2. Window facts reused and one exact passband observation

The accepted identity is

    K(q)=sum_{a=-H}^H Phi(q-a)/C,
    C=sum_{a=-g}^g Phi(a)>=1, 0<=Phi<=1.

Therefore 0<=K(q)<=3073 everywhere. At circular distance d>=2T, the accepted
far-tail proof gives K(q)<=eta=3073/20^114<2^-480.

There is also an exact lower bound needed here. If dist_M(q,0)<=T/2=1024,
the interval [q-H,q+H] contains [-g,g] after choosing the signed representative
of q. All Phi terms are nonnegative, so K(q)>=C/C=1. No approximate flatness
or unproved reciprocal conditioning is needed. A nearest bucket to -sigma n
always has distance <=T/2, including the half-grid tie and circular wrap.

## 3. Exact odd-multiplier isolation probability

Let G be the event that all distinct input positions n,n' satisfy

    dist_M(sigma(n-n'),0)>=4T=2^13.

For a nonzero difference d=2^v u with u odd, multiplication by uniform odd
sigma makes sigma d uniform among the M/2^(v+1) residues of valuation v.
If v>=13, every such nonzero residue has circular distance >=2^13, so the
bad-pair probability is zero. If v<13, the residues strictly inside
(-2^13,2^13) with valuation v number exactly 2^(13-v). The probability is

    2^(13-v) / 2^(27-v) = 2^-14 = 8/B.

No independence of different pairs is asserted. The union bound gives

    Pr(G fails)<=binom(s,2)/16384<=120/16384=15/2048.

On G, a bucket cannot have two modes at distances <2T: the circular triangle
inequality would make their pair distance <4T. A mode has at most four such
bins, as already established for BUCKETS. Thus the retained neighborhoods are
disjoint and their union has at most 4s<=64 bins.

## 4. Thresholding gives a finite list with one true mode per candidate

Call BUCKETS at tau=0 and scan every B coordinate. A bin is a candidate when
|b_j(0)|>=theta, tested by exact squared integers. If it has no retained mode,
its ideal value has magnitude <=lambda eta, so its finite value has magnitude
at most

    epsilon=rho+6 eta <2 rho <<theta.

It cannot pass the threshold. On G every candidate therefore has one true
retained mode n, with A=a_n K(jT+sigma n), and for every later tau

    b_j(tau)=A exp(-2 pi i n tau/M)+e_tau, |e_tau|<=epsilon.

Thresholding gives |A|>=theta-epsilon>theta/2. This remains true for complex
coefficients and all cancellation in the omitted tail. There is no positivity
assumption on a_n. The decoder rejects more than 64 candidates, a condition
that cannot happen on G. The s<=16 source bound is not inferred from the
number of successful numerical tests.

For every |a_n|>=2 theta, choose its nearest bucket. K>=1 there, and G makes
all other modes far. Hence |b_j(0)|>=2 theta-epsilon>theta: the mode necessarily
has a candidate. Modes below this threshold may or may not appear.

## 5. Finite, general bit decisions locate a candidate's unknown frequency

For bit ell=0,...,27, request tau_ell=M/2^(ell+1). Suppose the previously
decoded low ell bits equal n_low=n mod 2^ell. Then

    exp(-2 pi i n/2^(ell+1)) exp(+2 pi i n_low/2^(ell+1))
       =(-1)^(bit_ell(n)).

With exact observations, the real part of

    b_j(tau_ell) conjugate(b_j(0)) exp(+2 pi i n_low/2^(ell+1))

would be (-1)^bit |A|^2. The cross product of the two actually returned
P-grid values is computed as exact integers, not a rounded quotient or angle.
Its complex difference from |A|^2 exp(-2 pi i n/2^(ell+1)) is at most

    2 |A| epsilon+epsilon^2.

Since |A|>theta/2 and epsilon<2 rho,

    epsilon/|A| <4 rho/theta=2^-62.

The decoder encloses the correcting unit root by positive half-angle square
roots and outward integer arithmetic at 256 bits, using the independently
accepted supplier's pinned primitive implementation. These are separate root
calls with their own ledger; no original entries or descriptor are passed.
The accepted elementary root-width proof gives Cartesian error at most
2^(3m+9-256)=2^-163 for m<=28 (its prerequisite b sufficiently above m is
amply met). Consequently every point in the root rectangle is within 2^-162
of the exact root. An outward scalar product with this rectangle differs
from the exact corrected cross product by at most

    2^-162 (|A|+epsilon)^2.

Combining the last two displays makes the total deviation strictly smaller
than |A|^2/2. Every endpoint of the final real interval has the true bit sign.
The finite comparison lo>0 or hi<0 therefore necessarily succeeds on G.
The interval includes the exact corrected cross product, so an uncertain sign
is rejected rather than guessed. Induction recovers all 28 bits of n.

There are exactly 29 full bucket calls: tau=0 and the 28 dyadic shifts. The
decoder deduplicates recovered indices, checks every candidate is within its
decoded retained neighborhood, and rejects more than 16 distinct indices.
These guards do not purport to detect every bad isolation event.

## 6. Conditioned amplitude recovery and compact-output error

For every recovered n, use its nearest bin j*. It is available in the retained
tau=0 array. Evaluate K(d), d<=1024, with the accepted interval [L,U] on the
560-bit grid. Intersect L with 1 using the exact passband bound. The interval
contains the true K, remains nonempty, and has width <=2^-478. Its integer
midpoint kappa satisfies kappa>=1 and |kappa-K|<=2^-478.

Compute b_j*(0)/kappa by exact integer divisions and nearest-ties-to-even
rounding separately to the P-grid. With |a_n|<=1 and K>=1,

    |b_j*(0)/kappa-a_n|
       <=epsilon/kappa + |a_n| |K-kappa|/kappa
       <=epsilon+2^-478.

The complex rounding error is at most rho/sqrt(2)<rho. Total error is therefore
<3 rho and in particular <=4 rho. The implementation records the more
conservative 4 rho contract. The scalar window is freshly called and paid;
dividing at the candidate's potentially tiny K is deliberately avoided.

There are at most s returned entries, so their error norm is <=4 sqrt(s) rho
<=16 rho. All omitted entries have |a_n|<2 theta, giving omitted norm <8 theta.
Thus total error is <8 theta+16 rho<9 theta. Both support positions and
coefficients are newly computed by the recovery decoder. The compact output
is a list with default zero elsewhere, not an unmaterialized claim to have
written N outputs. Scaling back would multiply this norm bound by |alpha|;
no separate outer error budget or final grid has been proved here.

## 7. Exact obstruction to unconditional support recovery at this radius

Let c=2^1023+1, and take canonical originals

    x^(0)=c delta_0,
    x^(1)=c delta_0+delta_1,
    F=0, N=B_A=M.

Both are admitted: c is odd with 1024 bits; support sizes are 1 and 2.
Both normalizers have h=1024, so their normalized targets differ by exactly
2^-1024 delta_(M-1), and their supports differ. For **every** legal sigma,tau
and bucket j, their ideal buckets differ by at most

    3073*2^-1024 < rho/4.

Round each ideal bucket of x^(0) to the nearest complex Cartesian P-grid point.
This common response function is within rho/sqrt(2)<3rho/4 of x^(0)'s ideal
values and, by the triangle inequality, within rho of x^(1)'s ideal values.
It is therefore a legal finite-value provider for either input, at every
schedule, including adaptively chosen schedules and arbitrarily many calls.
An algorithm whose only information is this radius-bounded value interface
sees identical transcripts on the two cases and cannot guarantee exact support
on both. For randomized exact recovery, any shared transcript also forces at
least one of the two inputs to have success probability at most 1/2.

This is an information-theoretic counterexample to a **radius-only exact-support
claim**. It is not a claim that the particular accepted deterministic interval
implementation returns byte-identical outputs for this pair, and it does not
apply to a consumer that is handed the raw source support or other exact side
information. It does not obstruct approximate recovery proved above. Any exact
support extension needs a minimum-amplitude/precision contract or stronger
observations; the fixed 464-bit error promise alone is insufficient.

## 8. Full preparation, numerical, movement, output and replay costs

No prior sparse-FFT speedup is imported. At these fixed parameters, one run
requests 29*131072=3,801,088 explicitly produced complex bucket coordinates.
The consumer reads and validates all of them, even though only at most 64
candidate coordinates are used per phase. Thresholding pays B exact squared
norm tests. At most 1792 finite phase signs and 16 amplitude divisions/window
queries are performed. Returned source-index witnesses are auxiliary; only
the reversed sparse output indices are the target coefficients.

The accepted engine has cumulative caps. The live driver does not reset a
ledger or pretend indefinite free cache reuse. It uses five fresh adapters,
with call groups 6,6,6,6,5. For one group the accepted source-level bounds give:

    preparation slots <2^19;
    six runs' slots <6*2^20;
    total <6,815,744 <8,000,000;

    preparation numeric ops <(5631+129)*2048+20000;
    six source stages <6*16*8192;
    total <12,602,912 <30,000,000.

All numerical integers remain below the accepted 9000-bit first-run bound.
The final 16 scalar windows add fewer than 4096 arithmetic operations and
fewer than 4096 slots, within the remaining margin. Five sets of 5631 Phi
terms and 129 numerator roots are prepared; no uncharged reuse crosses groups.
The supplier is actually run 29 times, as required by this straightforward live
adapter. Each call's supplier, canonical header, exports and retention costs
are included in the five adapter receipts. The driver adds a fixed 2^110
binary-work and 2^60 cumulative-storage envelope for bounded source copies,
headers/hashes, schedule/receipt handling and writing the delivered artifacts.
These are deliberately loose finite bounds, not runtime or practical speed.

The new consumer uses a separate paid root ledger. At most
64*sum_(ell=0)^27 ell=24,192 complex root products are possible. Each uses 11
records in the pinned implementation; setup adds fewer than 1000. This is well
below the primitive one-million-record cap. Root data stay below 1024 bits;
the surrounding exact cross products and divisions stay below 4096 bits after
the enforced 480-bit bucket-input and 580-bit window-endpoint guards.

Consumer bookkeeping records every coordinate visit, threshold test, phase
decision, scalar-window request, retained slot, source byte, and output write.
Let E be the reported charged_units; it includes 4096 units per phase decision
and scalar request, 10 per threshold test, all root records, all coordinate
visits, retained logical slots, source/result bytes and a 65536-unit reserve.
With V=4096+bit_length(E)+64, the additional 2^16 E V^3 work and 4096 E V storage
bounds conservatively cover schoolbook operations, counters, addresses,
dictionary/sort scans, validation, movement and serialization. The separately
reported root receipt is added. A 2^100-work/2^50-storage output envelope covers
the complete returned receipt and one serialization, including fields appended
after the first byte estimate. Counts are cumulative logical storage, not RAM.
The accepted provider's full array writes are added to these consumer reads;
neither is treated as the other. Original input acquisition is assumed supplied
locally; no remote I/O is claimed or performed.

Production total is the sum of all five provider receipts, the caller envelope,
and the consumer receipt. A semantic replay must run the entire schedule and
decoder again against independently retained original input/state/sigma, then
pay canonical comparison and both sets of production costs. No replay was
silently credited in the one-run evidence. The replay helper executes
and charges this explicitly; REPLAY_RESULTS.json confirms a complete fresh
29-call replay and exact canonical packet equality. Production plus replay
therefore produced and read 7,602,176 bucket coordinates in 58 calls. Arbitrary future exports, dense N-coordinate
scatter, original-scale materialization and outer consumers remain additional
work. A required dense output costs at least N coordinate writes, irrespective
of this compact result. No theorem of sublinear full-output recovery follows.

## 9. Evidence, trust and limits

The complete accepted production dependencies were read and pinned before
execution. live_checks.py is new recovery work, not a rerun of the accepted
BUCKETS or supplier test suites. It checks the exact 2-adic counting identity
exhaustively at small moduli, runs the complete 29-call original-bound pipeline
on a nonconstant 16-support source with very large dynamic range, and checks
all output support and squared-error bounds against the independently retained
raw input. It also checks the indistinguishability inequalities and strict
float/uncertain-sign rejection. Tiny omitted coefficients are recorded honestly.

The actual finite run and cumulative receipts are RECOVERY_RUN.json; its input
is ORIGINAL_INPUT.json; CHECK_RESULTS.json and RUN_LOG.txt record the controls.
REPLAY_RESULTS.json and REPLAY_RUN_LOG.txt record the separate whole-schedule
replay and its added costs, with changed coefficient and context-hash rejection.
The demonstration multiplier is fixed and verified good by the test harness;
that verification is not available to the decoder and is not used by its
algorithm. The exact probability proof, not this selected tape, supplies the
randomized success statement. No production randomness source is attested.

Trusted execution of pinned source, correct Python/stdlib arithmetic, no hostile
private-state mutation, and a correct provider contract are assumed. The
integration's retained-original binding is caller-relative, not authentication
of an external origin or historical execution. Replacing both retained input
and answer changes the mathematical statement. This packet is a new restricted
recovery gate, not closure of ALG-034 or any dense/general Q16 pipeline.
