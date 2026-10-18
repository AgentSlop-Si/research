# N13: sixteen original physical banks over F_(53^11)

18 October 2026 UTC. New attainment result for M-MAGNETIC-SPAN / NEW-17 /
Q35 / NEXT-MAGNETIC-SIGNED. **Candidate theorem; final independent review
pending.** Two separate same-author exact implementations have passed.

## Result

For N=13, q=16, characteristic 53 and the original signed-resolvent grammar
with one independently free nonzero effective node in each cross orientation,
let B(K) be the minimum physical-bank count over K, with arbitrary legal
beta and raw weights allowed. Then

    B(F_(53^11)) = 16.

The new witness has allocation (7,1,1,7), beta=1, **both same-sign supports
non-Frobenius-stable**, and both cross nodes genuinely outside F53. It
therefore passes beyond the previously accepted stable-support obstruction.
It is a literal original-bank identity, not only a recurrence or splitting
candidate, and not a trace/quotient-algebra replacement primitive.

By scalar extension, B(F_(53^d))=16 whenever 11 divides d. Combining this
with already accepted cases, at least one divisor in {2,3,5,7,11} suffices.
This is not an if-and-only-if classification. Apart from the solved base
field d=1, the remaining degrees can now be restricted to d>1 coprime to
2310; the smallest is d=13. The broad four parent problems remain open.

A separate new supporting theorem, PRIME_CROSS_OBSTRUCTION.md, proves that
if both cross nodes stay in F53*, the exact minimum is 18 for every degree
coprime to 210, without assuming stability of either support. The d=11
witness here escapes that restriction using nonbase cross nodes. This
supporting result is not needed to prove the upper bound 16.

## 1. Exact field and explicit nodes

Use

    K=F53[u]/(u^11+u+3).

Encode sum_(i=0)^10 a_i u^i by the eleven-entry array [a0,...,a10]. The
independent Python checker proves exact irreducibility before doing any
extension-field inversion:

    X^(53^11) = X mod (X^11+X+3),
    gcd(X^11+X+3, X^53-X) = 1.

Since 11 is prime, every irreducible factor of a polynomial dividing
X^(53^11)-X has degree 1 or 11. The gcd removes degree 1; total degree 11
therefore proves irreducibility. The full sequence of eleven Frobenius
remainders is in INDEPENDENT_LITERAL_RESULT.json.

Take the two cross nodes equal, as allowed by independently free choices:

    y=z=[27,22,25,32,30,33,36,2,45,45,16].

Use these seven nodes in each same-sign orientation:

    [7,17,50,48,24,34,40,48,22,14,48]
    [11,10,27,22,8,21,25,42,20,12,49]
    [11,46,28,17,37,31,40,0,47,5,50]
    [11,47,32,50,7,4,15,42,34,2,6]
    [25,16,14,42,18,27,23,16,14,5,30]
    [26,39,40,52,40,52,34,40,8,5,4]
    [31,15,16,26,14,25,25,11,2,45,8].

Both exact verifiers check distinctness and nonzeroness. They multiply all
seven factors and obtain the same degree-seven monic H stored in the raw
certificate. Its t^6 coefficient is

    [37,22,5,8,11,18,10,13,12,18,17],

which is outside F53. Thus H is genuinely nonbase. The independent checker
also explicitly computes the 53rd powers of all seven roots and verifies
that the resulting set is different. Both supports are nonstable, rather
than merely being presented with a nonbase coordinate system.

Every beta is 1. Every original denominator is

    Delta=1-alpha^13-beta^13=-alpha^13 != 0.

All sixteen guard arrays are in DEGREE11_LITERAL_CERTIFICATE.json and are
recomputed independently. The two cross nodes are nonzero and nonbase.

## 2. Original physical-bank grammar

For indices modulo 13, let S e_t=e_(t+1), T e_t=16^t e_t and
F[k,t]=16^(-kt). Each of the sixteen records in the certificate is exactly

    B_(epsilon,delta)(alpha,1;w)
      = (1/13) sum_(j=0)^12 w_j
          (I-alpha S^epsilon-16^(epsilon delta j) T^delta)^(-1),

with epsilon,delta in {+1,-1}. No new primitive, derivative bank, singular
limit, pre/post map, or uncharged trace is introduced. Both implementations
verify that every physical bank matrix is nonzero.

The certificate contains all sixteen orientation/alpha/beta records,
their guards, all 208 normalized sector amplitudes, all **208 raw branch
weights**, the seven roots and their full annihilator, and the complete
13-by-13 matrix. Every array is an element of the explicitly proved field.

## 3. Complete sector reconstruction and raw weights

The accepted expansion uses the normalized target

    f(a,b)=16^(10(a+b)^2), gamma=7,

and the ordered Gaussian factor G_(epsilon,delta)(a,b) defined in the
source reports. A bank contributes G_(epsilon,delta)(a,b)
alpha^[epsilon a]_13 A_b. For each b, the C++ reconstruction solves the
full thirteen-row, sixteen-column actual-root system, not a quotient
system with unverified splitting. All 169 original sector equalities pass.

The thirteen ranks, in b=0,...,12 order, are

    13,9,11,12,13,13,13,13,13,13,12,11,9.

For a bank with first sign epsilon, the raw weights are constructed by

    w_j=Delta*7*sum_(b=0)^12 A_b 16^(-epsilon*b*j).

Both verifiers invert this character transform and recover all 208
amplitudes. More importantly, the entire raw operator identity is verified
directly below; the validity of the final witness does not rest on a
necessary recurrence gate or an untested expansion convention.

## 4. Two exact literal original-matrix checks

For every bank and every j, the literal branch matrix is built as

    M[t,t]=1-16^(epsilon*delta*j+delta*t),
    M[t+epsilon,t]=-alpha.

The C++ verifier performs Gauss-Jordan elimination for all 208 inverses,
checks both M M^(-1)=I and M^(-1) M=I, and applies the original raw weight
and original factor 1/13. All 169 entries of the sum equal 16^(-kt).

The separate Python checker imports no discovery/C++ or historical program.
It consumes only the inert JSON certificate. Its field arithmetic is
independently implemented by general polynomial reduction. Its inversion
algorithm is different: each beta=1 matrix has exactly one zero diagonal
entry at r0=-epsilon*j. That row fixes x_(r0-epsilon)=-delta_(r0,c)/alpha
for each inverse column c. The remaining coordinates follow by backward
recurrence

    x_(r-epsilon)=(d_r*x_r-delta_(r,c))/alpha.

The checker then verifies literal sparse left and right products for every
entry, rather than relying on the recurrence alone. It independently sums
all raw weighted inverses and agrees with the target in all 169 entries.

Both runs certify:

* 16 original physical banks and 16 nonzero guards;
* 7 distinct nonzero roots on each same-sign side;
* 208 branch inverses and 416 two-sided inverse identities;
* 70,304 scalar inverse-entry equalities per two-sided pass;
* 208 raw-weight/amplitude equalities and 169 target entries;
* zero target mismatches.

Falsification controls independently give 169 mismatches if 1/13 is omitted,
144 for the opposite Fourier sign, and 91 after changing the last raw
branch weight of the final bank by 1. These controls supplement the exact
positive identities. Same-author independent implementation is not external
reviewer acceptance; final independent review is still pending.

## 5. Lower bound and scalar extension

The immutable accepted predecessor review gives the field-uniform bound
B(K)>=16 in this same free-cross-singleton grammar, for arbitrary legal
beta, repeated physical banks and cancellation. Its large lower-minor
calculation is inherited, not repeated or newly credited here.

The complete explicit upper witness above gives B(F_(53^11))<=16, hence
equality. Whenever 11 divides d, the finite field F_(53^11) embeds in
F_(53^d). The embedding preserves all raw weights, nodes, nonzero guards,
inverses and every matrix identity. Thus it gives the same upper bound,
and the same accepted universal lower bound proves equality there as well.

## 6. Discovery, reproducibility, and exact stopping point

Discovery uses a declared symmetric extension-valued subfamily: y=z in
K*, the same seven-node annihilator on each side, beta=1, and the complete
rank-six affine recurrence family. The b=3 compatibility polynomial is
solved exactly for its extension-valued affine parameter. Search never
assumes that this necessary equation proves the full bank identity.

The deterministic xorshift seed is 202610181044. The first split candidate
appeared at zero-based cross-node index 29,464, after 29,261 nonzero-
constant-term recurrence candidates. The attained pair and H are frozen
in NONSTABLE_CANDIDATE.json. Search bounds and negative prefixes make no
general nonexistence claim. Once a candidate passed H | X^(53^11)-X,
factorization, all full sector systems and both literal checks were still
required and completed.

Run in a disposable copy, because checkers write receipts:

    python independent_literal_check.py
    g++ -O3 -std=c++17 verify_literal.cpp -o verify_literal
    ./verify_literal
    python independent_literal_check.py

The first command independently validates the supplied frozen certificate
and establishes the field before the C++ reconstruction. To reproduce
discovery additionally compile search_nonstable.cpp and run it with 30000
as its trial cap; it deterministically returns the frozen candidate. The
mathematical proof does not require rerunning the search.

OPERATION_LEDGER.md charges the representation and verification interfaces.
This fixed-instance result does not imply a fast FFT or a better bit-
complexity algorithm. The parent field classification remains open, as do
other cross allocations, lengths/parameters, historical priority and any
joint-evaluation optimization. No external write, commit or register change
was performed by this worker.

See SOURCE_PINS.json for exact immutable predecessor sources, README.md for
file roles, and MANIFEST.json for the frozen delivery-byte bindings.
