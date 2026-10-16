# Independent N=13 signed-bank review

Review date: 14 October 2026. **Verdict: ACCEPT within the precise scope below.**

The two polynomial-minor certificates, complete base-field degree-seven census,
and twenty-four-bank original-grammar witness all pass fresh independent
arithmetic. No mathematical repair was needed. This is a bounded exact
representation-count result, not an exact optimum or an arithmetic-speed result.

## 1. Accepted theorem and its domain

Let K be any field of characteristic 53. Fix N=13 and q=16 in its prime
subfield. All indices below are modulo 13. Put

    S e_t = e_(t+1),   T e_t = 16^t e_t,
    F[k,t] = 16^(-kt).

One counted physical bank is exactly

    B_(epsilon,delta)(alpha,beta;w)
      = (1/13) sum_(j=0)^12 w_j
        (I-alpha S^epsilon-beta q^(epsilon delta j) T^delta)^(-1),
    Delta = 1-alpha^13-beta^13 != 0,

where epsilon,delta belong independently to {+1,-1}, and alpha,beta and all
thirteen raw weights belong to K. Every legal beta is allowed, including zero.
No transformed target, new generator, pre/post map, derivative node, singular
limit, or product of banks is part of this grammar.

Within an orientation, group banks by their common alpha, adding their
normalized Weyl-sector amplitude vectors. A node is effective when this grouped
vector is nonzero. Require exactly one effective node in (-,+) and exactly one
in (+,-). Their locations y and z are independently free. There is no
singleton restriction in (++) or (--). Grouping is only lower-bound
bookkeeping: all physical banks are counted, including repeated banks.

If B(K) denotes the minimum physical-bank count in this domain, the accepted
conclusions are

    16 <= B(K) <= 24 for every field K of characteristic 53,
    18 <= B(F53) <= 24.

In fact each same-sign orientation requires at least seven nonzero effective
nodes over K, and at least eight over F53. Both cross nodes must be nonzero.
The upper witness has allocation (11,1,1,11), in (++,-+,+-,--) order, and lies
already in F53. Thus the upper bound persists under scalar extension.

These statements do not determine B(K), optimize unrestricted cross supports,
vary q or the characteristic, classify extension degrees, establish a
characteristic-zero lift, claim historical novelty, or give an FFT speedup.

## 2. Scope and independence of the audit

Only the newly written `independent_review.py` was executed for this review.
No candidate or historical program was executed, imported, compiled, or
evaluated. Candidate code was read as inert text. Candidate JSON was read as
data. The reviewer had seen the claimed numerical results before writing its
checker, so this is not a blinded review; numerical agreement was not its
evidence source.

The fresh computational routes differ in important ways:

1. Gaussian coefficients are rebuilt by **left multiplication** in the Weyl
   algebra, rather than the candidate's right-multiplication recurrence.
2. Polynomial determinants are reconstructed by scalar Gaussian elimination
   and Lagrange interpolation with independently established formal degree
   bounds. The candidate's polynomial Bareiss implementation is not used.
3. Every degree-seven solution is independently enumerated by fixing its t^6
   coefficient and solving the remaining six coefficients. This verifies the
   entire affine line, not only a supplied particular vector or null basis.
4. Every witness branch is freshly inverted from the original alpha, beta,
   sign and q parameters. Raw weights are then applied with the original
   factor 1/13. The claimed aggregate and claimed inverse matrices are only
   comparison targets.
5. Twelve additional legal-bank controls cover alpha=0, beta=0, and beta=3 in
   all four orientations. Four synthetic recurrence controls cover ordinary,
   repeated, and zero nodes.

`sources/` contains exact snapshots of the candidate contract, program,
numerical certificates, and summary. `outputs/SOURCE_BINDINGS.json` binds
their lengths and SHA-256 hashes. The final candidate report is also frozen as
`sources/CANDIDATE_REPORT.md` and its complete archive as
`sources/CANDIDATE_SOURCE.zip`. The candidate ZIP has 271,301 bytes and SHA-256
`42f9adb15f5f011286ea32b9e892f56f788452b52ea7135fbc2323f008148662`.
`CANDIDATE_INTEGRITY.json` verifies its inner manifest and correspondence to
every reviewed snapshot. Acceptance is tied to these exact source bytes,
not to a moving directory.

## 3. Derivation from the original bank, including arbitrary beta

The fresh checker verifies that 53 is prime and 16 has exact order 13. More
generally, for odd N and a primitive Nth root q in a field of characteristic
not dividing N, put U=S^epsilon, V=T^delta and omega=q^(epsilon delta).
Then VU=omega UV. Write D(r,l) for the coefficient of U^r V^l in
(U+V)^(r+l). Left multiplication gives

    D(r,l) = D(r-1,l) + omega^r D(r,l-1),   D(0,0)=1.

The root-of-unity quantum-binomial identity gives zero interior coefficients
at degree N and endpoint coefficients one. For N=13 this was rebuilt and
checked in all four orientations. For arbitrary alpha,beta and branch j,

    X_j = alpha S^epsilon + beta q^(epsilon delta j) T^delta
    X_j^N = (alpha^N+beta^N) I.

Consequently, whenever Delta is nonzero, telescoping proves the two-sided
inverse formula

    (I-X_j)^(-1) = (I+X_j+...+X_j^(N-1))/Delta.

Set r=[epsilon a]_N and l=[delta b]_N. Define G_(epsilon,delta)(a,b) to
be D(r,l) if r+l<N and zero otherwise. The bank coefficient at S^a T^b is

    alpha^r G_(epsilon,delta)(a,b)
      * beta^l/(N Delta) * sum_j w_j q^(epsilon b j).

There is no division by beta. This formula therefore covers beta=0, alpha=0,
and all legal nonzero parameters. Legal beta only affects the sector amplitude
at each b. Different beta values within a common-alpha group may be added
without changing the ensuing common-node recurrence necessity. The zeroth
power convention is the usual polynomial convention, including 0^0=1.

Direct extraction of the target Weyl coefficients gives

    (1/N) sum_t q^(-bt) F[t+a,t]
      = gamma q^(h(a+b)^2),
    h = 4^(-1) mod N,   gamma = (1/N) sum_t q^(-t^2).

For odd N, gamma is nonzero: the product of the two unnormalized Gauss sums
with exponents t^2 and -t^2 is N, by the invertible substitution
(u,v)=(s-t,s+t) and root-of-unity orthogonality. This is a coefficient
normalization, not a modification of the target or generators. Here h=10 and
gamma=7. All 169 direct coefficient extractions agree.

## 4. Forced windows and support bookkeeping

Let y be the sole effective (-,+) node. For b=1,...,6, at (a,b)=(13-b,b)
only that orientation is supported, and the normalized target coefficient is
one. Thus y is nonzero and its normalized amplitude is forced to be

    T_b = 1/[y^b G_-+(13-b,b)].

All indicated G factors are nonzero. For b<=a<=12-b, both negative-delta
orientations vanish and G_++ is nonzero, so

    v_b(a) = [q^(10(a+b)^2)
              - y^(13-a-b) G_-+(a,b)/G_-+(13-b,b)] / G_++(a,b)
           = sum_x A_(b,x) x^a.

The common set X comprises the distinct nonzero effective (++) alpha nodes.
Repeated nodes merge by amplitude addition, without creating derivative
atoms. A zero node contributes zero throughout these positive-exponent
windows; ignoring it in this necessary condition does not remove any axis
constraint from the original representation problem.

The six sequence lengths, in increasing b order, are 11,9,7,5,3,1. A support
annihilator h(t)=product_(x in X)(t-x) gives every consecutive recurrence
window of the matching length. A support with at most six nodes can be padded
to a monic degree-six annihilator by multiplying by a power of t. No splitting
or squarefreeness claim is needed for this degree-six padding.

All degree-six windows are used: five for b=1, three for b=2, and one for b=3.
They form the 9-by-7 polynomial augmented matrix E6(y). All degree-seven
windows are also used: four for b=1 and two for b=2, forming E7(y), of size
6-by-8. The checker independently rebuilt every entry and label and compared
them to the supplied matrices. There is no omitted recurrence window of these
degrees among the forced moment sequences.

The candidate's general equation-count formula is also correct. For
0<=m<=N-1, the number of windows is

    sum_b max(N-2b-m,0) = floor((N-m-1)^2/4).

Writing d=N-m-1, the positive summands are descending odd numbers when d is
even, and descending even numbers when d is odd. Their sums are respectively
(d/2)^2 and (d^2-1)/4. This general identity and the odd-N bank/target
identities above are accepted algebraic statements; they do not transfer the
specific numerical lower bounds to untested lengths or roots.

## 5. All-extension degree-six obstruction

The two reviewed 7-by-7 minors use zero-based row sets

    (0,1,2,3,4,5,6),  (0,1,2,3,4,5,7).

For each minor, the reviewer enumerates all 7! column assignments solely to
bound the degree of every Leibniz term. The formal degree bounds are 41 and
40, respectively. It then evaluates the determinant by scalar elimination at
all 53 field points and interpolates from the first bound+1 values. The degree
bounds are below 53, so this establishes the exact polynomial determinants,
not merely agreement as functions on F53. Both recovered polynomials have
degree 39 and agree coefficient by coefficient with the supplied minors.

The supplied two Bézout multiplier polynomials are then multiplied by these
freshly recovered determinants. Their exact coefficientwise sum is 1 in
F53[y]. Hence the two minors have no common zero in any extension field,
including at y=0. At every y in every characteristic-53 field, E6(y) has full
column rank seven and no nonzero recurrence vector. In particular no padded
monic degree-six annihilator can exist.

Thus (++) needs at least seven distinct nonzero effective nodes for every
legal nonzero singleton y, including extension-valued y. Simultaneous
reflection (a,b,epsilon,delta) to (-a,-b,-epsilon,-delta) preserves the G
coefficients and normalized target and exchanges (++) with (--), and (-+)
with (+-). The checker verifies all 676 G identities. Applying the same
argument separately to z requires seven (--) nodes. Independent cross
singletons therefore give at least 7+1+1+7=16 physical banks. No equality
y=z is imposed.

## 6. Complete F53 degree-seven gate

For each of the 52 nonzero y values, the first six coefficient columns of
E7(y) have nonzero determinant. Therefore the six equations on the seven
non-leading coefficients of a monic degree-seven polynomial have rank six
and form exactly one affine line. Independently fixing its t^6 coefficient
to each element of F53 enumerates all 53 members. Each polynomial is checked
against all six recurrence equations.

The reviewer checks all 52*53=2,756 polynomials and evaluates each at all 52
nonzero field elements: 143,312 exact root evaluations. None has seven
distinct nonzero F53 roots. The entire independently generated
polynomial-to-root-set mapping agrees with the supplied census, not merely
the reported survivor count.

If an F53 representation had at most seven nonzero effective (++) nodes,
its support could be padded with distinct nonzero F53 elements to size seven,
since F53 has 52 nonzero elements. The product of their seven linear factors
would be a compatible monic polynomial with seven distinct nonzero roots.
The complete census excludes this. Therefore eight nodes are required on
each same-sign side, yielding 8+1+1+8=18 physical banks over F53. This
splitting obstruction is not exported to extension-valued support nodes.

Passing a necessary recurrence gate is never treated as sufficient for a
bank representation. In this experiment no degree-seven base-field support
survived, so no small-support full-sector case was promoted to attainment.

## 7. Literal twenty-four-bank upper witness

The witness has both same-sign supports {1,2,...,11}, both cross nodes 1,
and beta=1 in every bank. Its denominators are -alpha^13, hence nonzero.
The supplied raw weights are stored in `sources/BASELINE.json`.

The fresh reviewer rebuilds each original 13-by-13 inverse matrix from these
parameters and computes 312 inverses, with 624 separate two-sided inverse
product identities. It then forms each bank with its original 1/13 factor.
All claimed inverse matrices and bank matrices agree with the independently
computed matrices. All twenty-four banks are nonzero, and their grouped
effective allocation is exactly (11,1,1,11). In particular the witness meets
the precise cross-singleton constraint.

The aggregate equals F in all 169 entries. Separately, its weights are
converted back to sector amplitudes, each original-bank coefficient is
checked, and all thirteen full-sector systems are rebuilt and verified. Each
sector has rank thirteen. This establishes actual full-bank attainment at
twenty-four, independently of the necessary recurrence tests.

Falsification controls detect 169 mismatches when the 1/13 normalization is
omitted, 144 when the opposite Fourier sign is substituted, and 91 when the
first raw weight is incremented by one. Deleting any individual witness bank
also changes the target; the exact nonzero-entry counts are recorded for all
twenty-four banks.

Twelve additional original-bank controls use (alpha,beta)=(0,2),(2,0),(2,3)
for every orientation. All are legal. Their 156 literal inversions and 312
two-sided inverse identities pass, as do all 2,028 coefficient checks. These
finite controls support implementation correctness; the symbolic formula in
Section 3 is what justifies arbitrary legal beta over arbitrary extensions.

## 8. Separate arithmetic-accounting check

The candidate's explicit cyclic-solve schedule is a valid, unoptimized upper
bound after constant preprocessing. For alpha nonzero, the row equation can
be written, in the order t_(s+1)=t_s-epsilon,

    x_(t_(s+1)) = a_s x_(t_s)+b_s,
    a_s=(1-beta q^(epsilon delta j+delta t_s))/alpha,
    b_s=-v_(t_s)/alpha.

The cycle multiplier is (1-beta^N)/alpha^N. Its difference from one is
nonzero precisely because Delta is nonzero, so closure is legal even if an
individual diagonal coefficient vanishes. For alpha zero, legal branches
are diagonal and all diagonal entries are nonzero.

The input-dependent b values cost N multiplications per bank and are shared
by that bank's N branches. Each branch uses N-1 multiplications/additions
for closure accumulation, one multiplication for the starting value,
N-1 multiplications/additions for propagation, and N weight multiplications.
Summing its N branch vectors adds N(N-1) additions per bank. Thus the
claimed per-bank upper budget is 3N^2 multiplications and 3N^2-3N additions.

For this witness, twenty-four banks plus their vector summation give 12,168
multiplications and 11,531 additions per application. The fresh reviewer
implements this schedule and checks it on all thirteen input basis vectors,
obtaining the target Fourier column each time and the stated counts each
time. `outputs/PAID_SCHEDULE.json` records these checks. No zero/one scalar
simplification is used in those counts. The preprocessing/storage costs are
excluded explicitly; this schedule is not an optimality or lower-bound claim.

The candidate's odd-length chirp identity is also correct:

    q^(-kt) = q^(-h2 k^2) q^(h2(k-t)^2) q^(-h2 t^2),
    h2 = 2^(-1) mod N.

Expansion of the exponent proves it for every permitted odd N; the reviewer
also checks all 169 entries in this instance. It gives one cyclic convolution
and two diagonal scalings, so a fair paid baseline is the convolution cost
over the same field plus 2N multiplications and preprocessing. The direct
dense baseline, with precomputed coefficients, costs at most 169
multiplications and 156 additions here. The supplied literal bank schedule
therefore supplies no arithmetic improvement. A lower bank count alone is
not a speed result, and no joint fast evaluator is established by this review.

The report's finite-field side observation is correct as well: the order of
23 modulo 13 is six, so primitive thirteenth roots over F23 first occur in
degree six. This does not constitute a calculation in that field.

## 9. Replay, integrity, and limits

Run from any directory:

    python /path/to/independent_review.py --out /path/to/new-output-directory

The checker needs only Python's standard library and its sibling `sources/`
directory. It makes no network requests or external writes. A cold replay uses
an isolated directory containing only this newly written checker and the
inert frozen source files. The deterministic JSON outputs are compared byte
for byte; timing records are excluded from byte-equality comparisons.
`REPLAY_VERIFICATION.json` supplies the exact receipt. `MANIFEST.json` binds
the final review packet and an external seal binds the ZIP archive.

No service preview/resource limit was encountered. No historical-source
execution or replacement search loop was used. No Sheet or GitHub write was
made by this reviewer. The stopping condition is met once the source-bound
report and cold replay receipt are sealed: the requested N13 numerical and
mathematical claims have been independently accepted within their stated
restrictions.
