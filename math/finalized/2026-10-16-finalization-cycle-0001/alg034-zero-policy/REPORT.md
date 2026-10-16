# ALG-034: a paid dyadic exact-zero decision and one-shot precision policy

16 October 2026. Candidate for independent review. Parent ALG-034 remains
TO RESEARCH, priority 48. No table or repository write has been made.

## Result and exact scope

For N = 2^m >= 4 and exact common-grid complex dyadic input, an exact
cyclotomic reduction decides whether the sampled projected signal is zero,
including nonzero inputs in its kernel. On the nonzero branch a computable
algebraic-integer separation bound gives one explicit precision at which the
accepted specified serial producer necessarily returns a nonzero approximation
and passes the mathematical Delta/alpha <= rho allowance of the accepted
normalization bridge.

This fills a restricted mathematical precision/zero-policy gap. It does not
implement or authenticate the serial producer, alter the accepted bounded
wrapper, provide an all-size adapter, or close the original all-length and
arbitrary-data gate. The possible precision is large and its entire cost is
paid. The existing M <= 4096, numerator-width and metadata caps remain genuine
deployment restrictions. Failure of our sufficient width certificate is not
proof that the actual payload exceeds a cap.

The contribution is the explicit connection of exact block-summary zero
testing, an input-dependent separation floor, and the existing numerical
allowance, with a finite cap-aware outcome. Cyclotomic arithmetic, algebraic
norms, and rounding/error inequalities are classical; no priority claim is made.

## 1. Source binding and accepted premises

Repository baseline: AgentSlop-Si/research at
4477338817cf2bd54a32f6bcc7c0d8ab0466ac4a.
The complete pinned v14 source was read from
https://github.com/AgentSlop-Si/research/blob/4477338817cf2bd54a32f6bcc7c0d8ab0466ac4a/math/archive/objects/a0/a0a5d23b1ca51bfe2b2734d64ee4cf0cce61e7735eac04a060a99430749113ef__RESEARCH_20261009-201937_.md
and matches the local source byte-for-byte: SHA-256
a0a5d23b1ca51bfe2b2734d64ee4cf0cce61e7735eac04a060a99430749113ef.
Its historical numerical/space overclaims are not adopted; later accepted
reports govern those boundaries.

Complete local bodies read and hash-checked:

- Accepted serial-producer report: 8dcc83d64316a136cb482fd04cff81ebaf7bf2351ab61fec1f02d8eadaf81cf8.
- Its independent ACCEPT: 31820fc28ff120f5982d4be0a03922600f06c3b7fb1a707b2617ae6e65201bf4.
- Mathematical bridge independent ACCEPT: 128104ac3c626a8b0a7c858704e986da2e2b801ca440564225e1e6e7fb92b488.
- Bounded source-wrapper independent ACCEPT: b481803172638f847edf296cd5d32272bc4a73e730e979cb5ca15cffb3f7b4c7.
- Wrapper input contract: b8add9064ecf19f9656c9ca043003090b557c46608e4d455ca9e0dfb1d9918e5.
- Later binary I/O precision report: inspected to avoid repeating its import,
  underflow and overflow results; this packet retains exact scaled dyadics.

The first five local texts were also compared to their exact accepted ZIP
members. Repository manifests for the precision and wrapper archives were
retrieved at the baseline commit and matched to the local archive SHA-256,
byte counts and Git blob identifiers. This is remote manifest verification
plus local archive/member byte verification, not a new remote binary download.
SOURCE_BINDINGS.json records the exact distinctions and full identities.

The current pinned open-record index and a fresh native read of Catalogue
row 19, novelty row 20 and Research overview row 30 identify this task. The
current Sheet explicitly leaves precision/zero policy open and preserves the
accepted wrapper boundary. The proposed change is confined to existing
overview P30/Q30; no score, status, novelty, owning-row history or other row is
changed by this packet.

Accepted premises used, without re-auditing their implementations:

1. For N >= B >= 3, the longer-blocks-first balanced partition has blocks
   I_b = {s_b,...,s_b+ell_b-1}. With a unit modulo N and beta in [0,N),
   the sampled block map is
   d_b = sum_t S_(b,t) x_(s_b+t),
   (P x)_(s_b+t) = conjugate(S_(b,t)) d_b,
   S_(b,t) = zeta^[a t(t-1)/2 + (a s_b+beta)t] for even N,
   zeta = exp(2 pi i/N). There is NO 1/ell_b normalization in P.
   Hence ||P x||_2^2 = sum_b ell_b |d_b|^2 and Y = U_N P x.
2. For nonzero x_j=(u_j+i v_j)2^(-F), F signed integer, actual maximum
   Cartesian numerator magnitude width W >= 1 and e=W-F, the accepted
   specified serial producer gives
   ||Yhat-Y||_infinity <= Delta = 2^e C 2^(-p),
   H=min(binomial(N+B-1,B),2^(N-B)), C=64 H B 2^B N^2,
   if p >= W and 2 C 2^(-p) <= 2^(-t), integer t >= 0, and every intended-root,
   rounding, index, range, input/state/output-binding premise really holds.
   Its sufficient stored magnitude allowance is I=B+2 ceil(log2 N)+10;
   output is exact scaled integer data with scale exponent e-p.
3. For nonzero Yhat, the accepted bridge selects a power-of-two lambda with
   ||Yhat||_2 <= lambda < 2||Yhat||_2, then d in {1,2} and alpha=lambda/d.
   Consequently alpha >= ||Yhat||_2/2. Its source precision is
   Pq=16m+16, Fq=Pq+1 and rho=2^(-Pq). Under its other premises, the existing
   exact guard Delta/alpha <= rho preserves the published BUCKETS allowance.

The accepted M <= 4096 wrapper already has a completed audit. No such audit
or execution is repeated here. Its ZERO_APPROXIMATION means Yhat=0, not Y=0.
Its EXACT_ZERO_INPUT requires genuinely zero original x, not merely P x=0.

## 2. Exact cyclotomic prepass

Restrict to N=2^m, m>=2, and define D=N/2. Then

Phi_N(X)=X^D+1,    i=zeta^(N/4).

The polynomial is irreducible over Q: its translate (X+1)^D+1 is Eisenstein
at 2. The constant term is 2; modulo 2 the translated polynomial is X^D,
since D is a power of two. Thus 1,zeta,...,zeta^(D-1) form a Q-basis.
The standard prime-power cyclotomic/Eisenstein statement is also verified in
Keith Conrad, Cyclotomic Extensions, Theorem 5.3, printed page 10:
https://kconrad.math.uconn.edu/blurbs/galoistheory/cyclotomic.pdf

For each block form the integer polynomial

g_b(X) = sum_t [u_(s_b+t) X^r_(b,t)
                      + v_(s_b+t) X^(r_(b,t)+N/4)],
r_(b,t) = a t(t-1)/2 + (a s_b+beta)t modulo N.

Reduce it modulo X^D+1, obtaining h_b of degree <D with integer
coefficients. Each monomial is reduced by its exponent modulo N, followed
by X^(D+j)=-X^j. Then

2^F d_b = h_b(zeta),
d_b=0 iff every coefficient of h_b is zero.

Since every ell_b>0 and U_N is invertible,

Y=0 iff P x=0 iff all h_b are zero.                         (Z)

This is an exact decision from the exact original input and state. Neither a
small computed norm, a floating-point equality, a digest, nor a producer's
ZERO_APPROXIMATION supplies (Z). Every input component and every block must
be inspected before claiming the all-zero verdict. A producer declaration
alone is insufficient to establish that the prepass used the intended input.

## 3. Explicit separation on the nonzero branch

For every nonzero h_b let A_b be its integer coefficient l1 norm. Choose a
nonzero block minimizing A_b (ties by block number), and call its value A>=1.
This selection is optional for soundness but improves the bound. Put

K=ceil(log2 A),     G=W+(D-1)K,
mu=2^(-F-(D-1)K)=2^e 2^(-G).                              (S)

All logs of positive integers here mean exact bit-length comparisons,
including K=0 at A=1. The absolute exponent F need not be expanded.

Proof of the floor: z=h_b(zeta) is a nonzero algebraic integer. Multiplication
by h_b on Q[X]/(X^D+1) has an integer D-by-D matrix; its nonzero determinant
is an integer, so its absolute value is >=1. Its D eigenvalues over C are
h_b(zeta^j), j odd, 1<=j<N. Every one has absolute value at most A, since
the roots have modulus one. Isolating the chosen embedding therefore gives

|h_b(zeta)| >= A^(-(D-1)) >= 2^(-(D-1)K).

Since ||Y||_2=||P x||_2 >= |d_b|, it follows that ||Y||_2 >= mu>0.
The determinant is a proof device, not an algorithmic step in the prepass.
No determinant, resultant or high-precision root evaluation is needed to
compute A,K,G or the certified floor.

With ell=ceil(N/B), a coarse input-only bound is
A_b <= sum_(j in I_b)(|u_j|+|v_j|) < 2 ell 2^W.
Thus K <= W+ceil(log2(2ell)); all reduced coefficients, partial sums and l1
norms have width O(W+log N). The separation exponent is at worst
G=O(N(W+log N)). This is a sufficient representation-dependent bound, not a
precision lower bound or a claimed sharp condition number.

The old absence of a width-independent projected-signal floor is unchanged.
At N=64,B=3,a=1,beta=0, x=e_0-e_1 is an exact nonzero-input kernel vector.
For x_k=e_0-(1-2^-k)e_1 on grid F=k, W=k+1, the first reduced block polynomial
is exactly 1 and all others vanish. Here A=1,K=0,G=k+1 and mu=2^-k, while
the actual norm is sqrt(22)2^-k. Width and precision grow with k. This does
not contradict the already accepted near-kernel obstruction.

## 4. One-shot precision theorem

Let c=ceil(log2 C), computed from the exact accepted C, and retain any requested
internal t>=0. On the nonzero branch choose

p_star=max{ W, c+t+1, c+Pq+G+2 }.                           (P)

If a genuine instance of the accepted specified producer runs at any
p>=p_star with its full arithmetic/range premises, then its output is nonzero
and its accepted mathematical bridge allowance necessarily passes:

Delta/alpha <= rho.                                       (A)

Proof. C<=2^c makes (P) imply exact loading p>=W, the accepted upstream
condition 2C2^-p<=2^-t, and

Delta <= 2^e 2^(-Pq-G-2) = rho mu/4.

For N=2^m,m>=2 and Pq=16m+16 we have sqrt(N)rho<1. Therefore

||Yhat||_2 >= ||Y||_2 - sqrt(N)Delta
             > mu - mu/4 = 3mu/4 > 0.

The bridge exists and alpha>=||Yhat||_2/2>3mu/8. Hence
Delta/alpha < (2/3)rho <= rho. This has slack, including rounding/doubling;
no heuristic relation between p and the returned normalization exponent is
substituted for the true bridge inequalities.

This is a one-shot existence/precision contract for the already specified
serial algorithm. It is not an executable producer, a validated implementation
of this prepass in a production wrapper, or acceptance of historical FFT code.
No retry is necessary mathematically when (P) can be realized; resource or
interface failure does not become successful execution by virtue of the proof.
An optional adaptive strategy could pay additional runs, but none is claimed
or needed by this contract.

## 5. Total mathematical policy and bounded deployment outcomes

The following are proposed POLICY outcomes, not installed wrapper API values.

1. Validate exact dyadic/common-grid input, N=2^m>=4, 3<=B<=N, odd a with
   0<a<N, integer 0<=beta<N, exact phase embedding, intended longer-first partition, and
   nonnegative integer t. Reject out-of-domain data with the work already
   reached paid. Physical input uncertainty and arbitrary real-oracle inputs
   are outside this exact-input contract.
2. If every original numerator is zero, return EXACT_INPUT_ZERO. This alone
   can use the accepted wrapper's separately truthful exact-zero-input branch.
3. Otherwise perform the exact full prepass. If all h_b vanish, return
   EXACT_PROJECTED_ZERO with the original input/state binding and proof (Z).
   It is legitimate to report Y=0 and the reflected projected target=0.
   Do NOT mark original_input_zero=1, do NOT fabricate a producer receipt,
   and do NOT construct a normalized nonzero Q16 source. Writing a requested
   explicit length-N zero output still costs N writes. This zero policy
   discharges a mathematical target, not an unchanged-wrapper API extension.
4. On the nonzero branch compute (S),(P), choose the actual planned p=p_star,
   and compute the inherited magnitude allowance I and actual metadata width
   checks. Return NONZERO_PRECISION_PLAN with
   all parameters and the conditional theorem. Without an authentic producer
   and exact source binding this is a plan, never an execution certificate.
5. For the inherited bounded wrapper require 4<=N<=4096. A sufficient universal
   output-numerator width certificate for this planned run is p_star+I<=65536,
   since the producer's grid numerators have strict magnitude <2^(p+I).
   If a larger actual p is used, recheck p+I<=65536 and kappa=W-F-p at that p;
   the theorem's validity for all p>=p_star does not make the smaller width
   certificate apply to a higher-precision run. Retain the 256-bit scalar
   metadata and 16384-bit C cap, supported exact in-memory types, digest,
   rounding, immutable-source and input consistency requirements unchanged.
   In particular check signed F, kappa=W-F-p and every actual integer field;
   an accepted F near a metadata boundary need not imply accepted kappa.
6. If a deployment constraint is unavailable, return DOMAIN_BLOCKED or
   SUFFICIENT_CAP_NOT_ESTABLISHED as appropriate. If p_star+I>65536, it only
   means this universal width estimate does not establish the cap. Actual
   output might still fit, and would need its own paid exact scan. No claim
   of actual numerical failure or impossibility follows. If an actual scalar
   field or actual numerator exceeds its exact cap, that is a genuine
   interface rejection, not a mathematical refutation.

The mathematical policy is a finite decision and finite precision construction
for every finite input in its restricted domain. A bounded deployment is not
promised to return a usable source for every such input. The theorem does not
relax caps or guarantee physical memory/time availability. All accepted sparse
Q16 eligibility conditions are still separate, and no theorem-scale sparse
Q16 instance is covered by the inherited M<=4096 cap.

For example, N=4096, B=3, t=0 and an input with a single real numerator
2^53-1 give W=K=53 and p_star=108823, so p_star+I=108860 exceeds 65536.
The input itself is modest-width; the separation-based plan is conservative.
This is SUFFICIENT_CAP_NOT_ESTABLISHED, not a proof that the actual payload
is overwidth or that another paid plan cannot work. It prevents presenting
the new theorem as an unrestricted success policy for the old wrapper.

## 6. Complete paid cost and storage ledger

No zero test or separation oracle is free. Let J=ceil(log2(N+1)),
Lz=W+ceil(log2(2ell))+2, and E be total state/tolerance/exponent metadata bits.
Use exact dense D-coefficient scratch for one block, clear it each time, add
at most 2ell monomials, scan it for zero and A_b, and retain the best A/index.
No D-by-D norm matrix is constructed in the actual policy.

A straightforward schoolbook bit upper bound for this prepass is

O(NW + N J^2 + B D Lz + E).

This pays original input reads, exact integer phase/index calculation and
reduction, coefficient additions, each full clear/scan/l1 accumulation, and
metadata. A retained exact common-grid input plus streaming coefficient work
uses O(NW + D Lz + B J + E) bits. If every coefficient vector is serialized as
a proof trace, add O(BD Lz) writes/storage rather than claiming the streaming
bound. An independent full verifier pays the prepass again. Conversion to a
common dyadic grid, if needed, also pays its actual shifts and exponent spread;
W is not a conventional floating significand width.

Compute K by integer bit length, G by exact multiplication, and p_star by
exact comparisons. With V the largest actual planning-integer width, pay
O(M(V)log(V+2)) for these constant-many arithmetic operations plus the accepted
H/C planning. No number of magnitude 2^|F|, 2^G or 2^p needs to be materialized
merely to plan. Actual production at p bits certainly is not unit cost.

For the nonzero production branch retain the FULL inherited producer ledger.
Let Aop=NB+B^2+N, L=p+I+4, L_H=O(B log(N+B+1)), and
T=O((p+1)^3 log(p+2)+(p+1)J). One accepted conservative bound is

O(NW + log(|F|+2)
  +(N+B^2) M(J)log(J+2)
  +B M(L_H)log(L_H+2)
  +N(p+1) M(T)log(T+2)
  +Aop M(L)log(L+2)).

It pays normalization, phase/index and partition work, H/C construction,
certified roots and inverse square root, B^2 coefficient/seed preparation,
NB serial recurrence, reconstruction/gauge scan, and all N exact scaled outputs.
The accepted native fixed-integer main arithmetic can omit the final log
factor, but no new fast-backend implementation is asserted here. The retained
producer storage is O(NW+(N+B)L+T+L_H+log(|F|+2)), plus metadata. Add the exact
prepass work/storage above, rather than charging it to a free upstream source.
Widths may be O(N(W+log N)+t), and the elementary root engine can dominate.

Then pay the wrapper anew: dense payload scan/hash, H/C consistency
reconstruction, norm accumulation, signed requantization, any doubling,
immutable source copies and retained O(N(Fq+log(Fq+2))) numerical bits plus
container/metadata representation. Its accepted conservative source-level
work envelope is O((N+B)(q+N+Dmeta+log(N+2))^2+Nq+Dmeta), with q the actual
payload width and Dmeta the actual metadata width; reached rejected prefixes
stay charged. We do not re-prove this accepted implementation ledger.

Any downstream window/phase preparation, scalar certification, schedule and
rational-parameter bits, actual BUCKETS calls, estimate reconstruction,
outer transfer, storage, final output and scale-back remain additional and
cumulative. Physical I/O, host memory, actual wall time and repeat runs are
not hidden in scalar operation counts. Exact original input/state and returned
payload binding must be genuine; hashing an untrusted declaration is not
producer authentication. No total end-to-end speed advantage is inferred.

## 7. Correct target and unchanged limitations

Both ideal Fourier stages use the same unitary negative-sign transform, so
U_N^2=R. The second ideal target is

R P_(a,beta)x / alpha,

not U_N x. Projected-zero inputs remain nonzero original inputs in general;
an exact zero projected target is not a successful full-input Fourier recovery.
The precision result addresses numerical approximation of the sampled row,
not projection/sampling error or a stronger decoder.

Open: authentic executable/certified producer and policy binding, the original
all-length and arbitrary-data precision/zero gate, compatible all-size source
adapter, actual valid downstream integration, fast polynomial/FFT numerical
backend, historical executor/helper repair, full recovery, practical resource
guarantees, speed and worldwide novelty. Parent status and priority stay fixed.

## 8. Fresh bounded controls and proposed existing-cell update

fresh_checks.py was authored for this task and imports only Python standard
library modules. It executes no supplied producer, accepted wrapper, historical
program, old check suite, downstream code, or installation. The controls use
exact integer polynomial reduction versus independently formed long-division
polynomials, exact integer multiplication-matrix determinants, known kernel
and near-kernel inputs, and exact symbolic planning inequalities. The norm
determinants occur only in these small corroborating controls.

CHECK_RESULTS.json records 104,976 exhaustive N=4 reductions, 400 larger
reductions, 3,150 norm/zero tests, 7 near-kernel widths through k=65000, and
7,020 precision plans across dyadic N through 4096, including input widths
65536. Five targeted semantic mutations are detected. Those finite checks
do not establish the universal theorem by extrapolation, instantiate a
production policy, or test a real accepted producer run. They intentionally
do not re-test completed wrapper behavior.

PROPOSED_EXISTING_CELL_UPDATE.json contains exact freshly read prior values,
two proposed prefixes, and preservation rules for overview P30/Q30 only.
Application is conditional on independent acceptance and a fresh conflict
check. No application, publication or remote write was done here.
