# Independent audit: young-feedback batching obstruction

## Verdict

**Accepted in its stated arbitrary-jet, exact-output, bounded-coefficient complex linear scope.** The routed row formula, disjoint output supports, all cross-age orthogonality cases, rectangular-minor argument, explicit constants, marker-regime asymptotics, and matching paid causal upper bound are valid. No substantive correction to equations (1)–(16) is required.

The conclusion is a component lower bound. It is not a lower bound for every implementation of the retained inverse, a fused computation starting from the original source, unrestricted arithmetic, or finite-field arithmetic. The distinction between **Jr independent arbitrary jet entries** and jets generated from **N original inputs** is essential, and the target preserves it correctly.

Audited target:

- `young_feedback_batch_0253/YOUNG_FEEDBACK_BATCH_OBSTRUCTION.md`
- SHA-256: `0c7ac6b5c481ba34d3bf6abb6bc97f6f1bdea49396d81f7414d63fe2b50b3a0e`

Accepted contextual inputs, read without executing their code:

- `marker_cut_audit_0241/INDEPENDENT_MARKER_CUT_AUDIT.md`
- `marker_cut_compression_0229/EXACT_MARKER_CUT_COMPRESSION.md`

All three existing seal manifests passed. All 27 files in those directories were hashed before and after this audit and remained unchanged. No target, predecessor, or supplied program was executed or imported. The verifier in this new directory was authored for this audit and uses only the Python standard library.

## 1. Routed rows: exact coefficient, support, and merge count

Write N=2^n, d=n-b, r=2^d, eta=omega^(2^b), and assume the target's b>=7 and L+b<=d, with L=2^(b-1). The identities themselves need only the corresponding smaller horizon t<=d-b.

For an appended t-bit word k, direct multiplication of Q_r edge weights gives destination

    a = 2^t s + k mod r

and coefficient

    eta^(s rev_t(k) + gamma(k)).

This follows by writing the appended bits c_1,...,c_t in chronological order: the contribution of the original source index is s sum_h c_h 2^(h-1)=s rev_t(k), while the contributions of preceding appended bits sum to gamma(k). Reducing intermediate states modulo r changes no eta power.

Because t<=d, the low t bits of a determine k. C_t multiplies by omega^gamma(k) eta^(-gamma(k)), and routes a to

    2^b(a-k)+k = 2^(b+t)s+k mod r.

Set R_t=2^(d-b-t). This destination depends exactly on q=s mod R_t and is the integer

    i=2^(b+t)q+k,  0<=q<R_t.

It lies below r, so the final displayed representation has no wrap. Its coefficient is exactly

    omega^gamma(k) sum_(s congruent q mod R_t) eta^(s rev_t(k)) u_s.

There are r/R_t=2^(b+t) source summands. Q_r^t has already merged 2^t source paths at each fixed a, and C_t merges 2^b such a coordinates. The formula includes both kinds of merge. None is being counted as a free arithmetic operation.

The valid words begin and end with 1 and avoid 0^b. Their count is 1 at t=1 and a_b(t-2) for t>=2: the two bounding 1s cannot participate in a zero marker, leaving precisely the interior avoiding-word condition. Therefore m_t=R_t|K_t|, not the active trajectory width e_t.

Independent evidence: 205 input vectors, including 168 complete small-case basis vectors, agree among the row formula, Q_r propagation followed by C_t, and full-N weighted propagation with retained states killed after every step. The 37 parameter/field cases use GF(257) and GF(65537), check root order, and vary the primitive-root embedding. These are exact algebraic controls, not complex magnitude arguments.

## 2. Output supports and exact temporal independence

The d-bit representation of i contains b zero bits immediately before its low t-bit suffix k. Since k begins with 1 and contains no 0^b, the rightmost completed marker ends immediately before this suffix. Its age is exactly t. This remains true at q=0 and when the marker uses leading zeros. Longer zero runs before k do not change where the rightmost completed marker ends.

Thus S_t and S_t' are disjoint for t!=t'. At output coordinate i in S_t, the batch sum has exactly one contributing age:

    (g_(j+b+t))_i = (C_t Q_r^t u_j)_i.

The permitted input starts exposing every age are j=0,...,n-b-L. Their count is J=n-b-L+1, including the endpoint. The selected output locations are all distinct for every pair (j, packet row): equal locations first force equal age by their spatial coordinate and then equal input time by their temporal coordinate.

Selecting these output entries therefore reveals J copies of B on independent blocks u_j. It is a fixed selection and permutation, with no summation or inversion needed to recover these packet outputs. This is stronger than merely observing that each g_k is a sum.

Independent evidence: exact support cardinality/marker-age checks and 46,064 full temporal output-coordinate comparisons. The streaming implementation and direct packet placement agree; every location is checked for duplicate occupancy and every one of the J full blocks is checked for exposure.

## 3. Complex orthogonality, including the different-age boundary

Each row contains 2^(b+t) unit-modulus coefficients, so its squared norm is 2^(b+t).

For equal ages, distinct q values have disjoint source supports. For equal t,q and distinct k, distinct reversals differ by a nonzero integer of absolute value below 2^t. Summing the row product over s=q+ell R_t gives a complete geometric sum of length 2^(b+t), and the frequency difference cannot be divisible by that length.

For t<t', R_t is a multiple of R_t'. Intersection is possible exactly when q=q' mod R_t'. In that case the entire smaller support s=q+ell R_t is contained in the larger support. The row product, apart from its nonzero unit phase, is

    sum_(ell=0)^(2^(b+t)-1) exp(2 pi i ell (rev_t(k)-rev_t'(k'))/2^(b+t)).

For an arbitrary primitive root, the exponent receives an odd multiplier; divisibility and the zero criterion are unchanged. A nonzero sum would require

    rev_t'(k') = rev_t(k) mod 2^(b+t).

There are three cases:

1. If t'<t+b, both frequencies are below the modulus. The long frequency has its bit t'-1 set because k' ends in 1, so it is at least 2^(t'-1)>=2^t. It cannot equal the short frequency, which is below 2^t.
2. If t'=t+b, the same range argument already excludes equality. Equivalently, the congruence would require the last b bits of k' to be zero, contradicting its final 1.
3. If t'>t+b, reversal of the congruence says the first t bits of k' equal k and the next b bits are all zero. This is an internal forbidden marker.

Consequently every distinct pair of rows is orthogonal and

    BB* = diag(2^(b+t), repeated m_t times).

The target's grouping of cases 2 and 3 is valid. Its endpoint treatment does not omit t'=t+b.

Independent evidence goes beyond finite-field reciprocal-root tests: the new verifier reduces each Gram entry exactly in Z[X]/(X^(N/2)+1), the cyclotomic representation for a primitive power-of-two complex root. All 67,760 tested row pairings vanish or have the exact required norm across 28 cases and 1,098 rows. Nonempty cross-age intersections include 2,964 pairs with t'<t+b, 1,328 with equality, and 2,176 with t'>t+b. No floating-point tolerance is used.

A negative control admits the forbidden word 1001 at b=2. Ages 1 and 4 then collide at output index 9; their phase-free pairing is -8 X^96 in the primitive-256th-root ring, hence is nonzero. Both the language restriction and age-disjointness are genuinely used.

## 4. Rectangular volume and full-dimensional determinant potential

Let m=sum_t m_t and S=sum_t(b+t)m_t. Orthogonality proves rank(B)=m<=r and det(BB*)=2^S. Cauchy–Binet gives

    sum_(I subset [r], |I|=m) |det B_I|^2 = 2^S.

A largest term is at least the average, yielding

    log2 |det B_I| >= S/2 - (1/2)log2 binom(r,m).

This is a rectangular argument; it does not pretend B has r output rows or substitute e_t for m_t. Append the standard coordinate rows e_s for s outside I. Expansion along those rows gives a full r-by-r determinant of modulus |det B_I|. All r original input dimensions are still present. These coordinate rows are available at time zero in the conceptual circuit potential; they are not new free computational outputs.

Do this on each of the J independent input blocks and retain coordinate rows on every other block. The full ambient dimension is D=r(n+1), and the selected determinant has modulus |det B_I|^J. Off-block coefficients vanish, so the block product is exact. This is why factor J is valid only when the component receives independently supplied u_j.

Track the largest determinant modulus of D coefficient rows among all forms ever available. It starts at 1. A unit-bounded scalar multiplication cannot increase it. A new binary sum or difference changes any candidate determinant by a sum of at most two old determinants, hence can multiply the potential by at most 2. Copies and permutations do nothing. This proves exactly

    A >= J [S/2 - (1/2)log2 binom(r,m)].

Allowing all historical rows only strengthens the computational model, so overwriting does not undermine the lower bound. No assumption about intermediate value magnitudes or numerical precision is needed.

Independent evidence: 628 minors are evaluated exactly in cyclotomic rings for four small rectangular banks. Their squared-modulus sums equal 2^S with (r,m,S)=(4,1,2), (8,3,7), (8,1,3), and (16,3,10). All 628 coordinate-completed matrices are also evaluated in a prime field and match their minor up to sign. These controls corroborate the all-size argument; the argument, not the controls, proves the bound.

## 5. Constants and marker-regime asymptotics

For a uniform (t-2)-bit interior, each possible length-b zero window has probability 2^(-b). There are at most t-2 such windows, including when there are actually none. Thus

    a_b(t-2) >= 2^(t-2) [1-(t-2)/2^b] >= 2^(t-3)

for 2<=t<=L=2^(b-1). Multiplying by R_t gives

    m_t >= r/2^(b+3) = r/(16L).

Ignoring the positive b and age-1 terms is safe. Since

    sum_(t=2)^L t = (L^2+L-2)/2 >= L^2/2  for L>=2,

one obtains S/2>=rL/64. The general binomial estimate binom(r,m)<=2^r then gives

    A >= J(rL/64-r/2).

The next inequality holds exactly when L>=64:

    rL/64-r/2 >= rL/128.

The hypothesis b>=7 supplies precisely that threshold. Since rL=N/2,

    A >= JrL/128 = JN/256.

Every displayed constant in the target is correct, including the boundary b=7,L=64. The proof is deliberately loose but positive; no entropy estimate beyond binom(r,m)<=2^r is needed.

For b=floor(log2(n/(4 ln n))), the floor gives

    n/(8 ln n) < 2^b <= n/(4 ln n),
    n/(16 ln n) < L <= n/(8 ln n).

Therefore b=o(n), L=o(n), and L+2b<=n for sufficiently large n, verifying the target's feasibility condition L+b<=d. Also b>=7 eventually and J/n tends to 1. Hence A>=((1-o(1))/256)Nn.

The independent arbitrary-jet dimension is quantitatively

    Jr = (J/n) N [n/2^b] = Theta(N ln n),

with the multiplicative bracket n/2^b between 4 ln n and 8 ln n. The floor oscillation means this should be understood as order comparability rather than a claimed ratio tending to 1. The target's informal “approximately N ln n” has this valid interpretation.

Independent evidence: a fresh b-state word-count dynamic program checks 16,369 exact rational inequalities through b=14,L=8192, including the union bound, normalized row count, volume bound, and the L>=64 constant. These checks use a different recurrence formulation from the target verifier.

## 6. Matching upper bound and causal composition

The displayed dense-step algorithm is a valid constructive upper bound:

- Build consecutive omega and eta power tables and the gamma/phase tables in O(N+n) operations. Gamma follows the binary-parent recurrence, and negative eta powers can be looked up from the positive root table.
- Read the r(n+1) arbitrary inputs and initialize the output array, paying O(r(n+1)). Copy each new input vector into scratch, also paid.
- At every requested age, carry out the full two-edge Q_r step in O(r) operations, then scan the r entries for C_t. Membership is an O(1) lookup/test after the stated O(r) integer tables; every routed merge is an addition.
- There are at most (n+1)L such age steps, hence O(rnL)=O(Nn) total work. Two scratch vectors require O(r) words. Tables and input/output storage total O(N+r(n+1)) words.

All constants applied to input-dependent data are unit modulus, so this algorithm lies in the lower-bound model. No hidden many-input sum, polynomial multiplication, per-edge exponentiation, or free routing merge is needed.

Causality adds no obstacle: once u_j is finalized, processing its entire trajectory writes only to slots j+b+t>j. It may be completed before finalizing the next coefficient. These are exactly the terms needed by the accepted residual recurrence. Direct retained edges, other feedback, fresh-source work, and final recovery remain separate costs; the target does not declare the young component to be a complete solve.

The lower bound also applies to any causal implementation that must expose the same arbitrary-jet g outputs, since granting offline knowledge of all inputs can only help. It does not force a general fused solver to expose them.

## 7. Source-jet scope: the required separation

Three objects must remain separate:

1. Arbitrary component inputs (u_0,...,u_n), of dimension r(n+1), with Jr independent dimensions used by this lower bound.
2. Arbitrary retained right sides f, for which the causal retained equation can generate arbitrary retained solution sequences, but an implementation need not expose this particular packet bank separately.
3. The actual source-generated solve from one original x in C^N. Its source f and retained solution jets u_j=(Q^j x)_R are linear functions of at most N independent scalars.

The predecessor's rank-N fresh-source result does not grant Jr independent solution-jet entries. Nor does rank N alone prove the required packet-output volume after restriction. Composing B with a source-dependent map can change its rank, determinant, and output materialization requirements. Therefore this component proof cannot be substituted into the source-generated computation without a new argument.

The independent verifier computes selected source-generated solution-jet ranks as a concrete check. For n=6,b=1,J=5, the arbitrary input array has Jr=160 entries, but the map from N=64 original inputs to those entries has rank 62 over GF(65537). Other controls give ranks 14 of 24 entries from 16 inputs, 30 of 64 from 32, 32 of 48 from 64, and 76 of 128 from 128. These are illustrative finite controls, not asserted formulas for all parameters or the large-marker regime. The all-size dimension ceiling is simply N.

The target correctly leaves open a constrained and fused source/solve construction. A full exact unnormalized complex transform in the same bounded-coefficient linear model still has the separate full-transform determinant obstruction, but that is a different theorem with N independent inputs. Nothing here produces an unrestricted FFT lower bound or transfers a complex modulus argument to finite fields.

## 8. Model precision and remaining constructive interfaces

No substantive correction is needed, but two reading conventions should remain explicit:

- The target's fixed-K statement “per gate factor at most max(2,K)” refers to its primitive model of separate scalar multiplication and addition gates. If instead one counts alpha*x+beta*y, with |alpha|,|beta|<=K, as a single generalized gate, the determinant factor is at most 2K. Either convention gives the same Omega(Nn) total-gate order for fixed K, but its constant should use the chosen primitive.
- “Approximately N ln n” for Jr means Theta(N ln n); the marker floor does not fix a limiting leading constant.

For separate scalar multiplications with |c|>1, the potential gives the necessary budget A+sum log2|c| at least the target's right-hand side of (12). Making such constants during setup does not pay for applying them to input-dependent forms. This is a necessary condition, not a construction.

A finite-field proposal still needs an actual field family, supplied or constructed primitive roots, representation, setup, operation accounting, arbitrary-input circuit, causal composition, and full recovery. Exact cyclotomic complex volume supplies no finite-field magnitude lower bound. The target's finite-field discussion respects that boundary.

## 9. Reproducible audit evidence and stopping boundary

New audit artifacts:

- `independent_young_audit.py`: independently authored standard-library controls.
- `INDEPENDENT_CONTROLS.json`: per-case exact results and scope labels.
- `CLAIM_EVIDENCE.md`: claim-by-claim evidence index.
- `INDEPENDENT_RUN.log` and `INDEPENDENT_REPLAY.log`: identical deterministic runs.
- `REPLAY_CHECK.log`: byte-for-byte replay check.
- `INPUT_FILES_BEFORE.sha256`, `INPUT_FILES_AFTER.sha256`, and `INPUT_FILES_UNCHANGED.log`: preservation of all 27 input files, including the manifests.
- The three `*_SEAL_BEFORE.log` and three `*_SEAL_AFTER.log` files: existing seals verified before and after.
- `AUDIT_SHA256SUMS.txt`: seal for this new audit package.

All controls passed. The result is an accepted scoped obstruction with a matching causal upper bound, not a faster transform or a closure of the constrained-source/finite-field constructive questions.
