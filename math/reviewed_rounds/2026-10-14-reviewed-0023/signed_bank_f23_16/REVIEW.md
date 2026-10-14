# Independent review: pinned F23 signed-bank lower bound

13 October 2026. **Verdict: ACCEPT.**

The accepted statement is precisely:

> In the original signed-bank grammar at N = 11, q = 13 over F23, with exactly one effective alpha node in each cross-sign orientation and both nodes fixed at 4, every representation of the specified Fourier matrix uses at least 16 actual original banks.

If no representation exists, its bank minimum is infinity and the inequality remains valid. This is a lower bound, not a determination of the minimum.

The reviewed candidate is `Signed_Bank_Pinned_F23_Sixteen_Lower_Bound_Candidate_2026-10-13.zip`, SHA-256 `e58d0405e4d7664b3ed6318181caa4ce79e2af2ef07bc686cd6b0dd8a8274201`. Its report has SHA-256 `92a43bdb04c61937add67ab6c8c8470877c90e382aef5ad70aa69281e54a3e1d`; those bytes agree with the supplied working report. The exact candidate archive is included as `INPUT_CANDIDATE.zip`.

All 19 candidate manifest entries and all five source pins were verified. The candidate and historical Python programs were never executed or imported. Their bytes were only hashed as archive members. This review's newly written standard-library program rebuilds the mathematics from the literal matrices, then compares the candidate's inert arithmetic records with the independently obtained values.

## 1. Exact grammar and meaning of the count

Work entirely over F23. For t in Z/11Z, define

    S e_t = e_(t+1),   T e_t = 13^t e_t,
    F[k,t] = 13^(-kt).

Each counted bank is one original summand

    B_(epsilon,delta)(alpha,beta;w)
      = (1/11) sum_(j=0)^10 w_j
        (I - alpha S^epsilon - beta 13^(epsilon delta j) T^delta)^(-1),

where epsilon and delta are independently +1 or -1; alpha, beta and all eleven raw weights belong to F23; and

    Delta = 1 - alpha^11 - beta^11 != 0.

Within an orientation, summands at equal alpha can have their sector-amplitude vectors added for necessity arguments. An effective alpha node is a group whose combined vector is not identically zero. The model requires exactly one such node in each of (-,+) and (+,-), both at alpha = 4. It does not require each group to consist of exactly one physical bank, nor restrict legal beta values to a nonzero value.

This bookkeeping does not reduce the number of original summands. No derivative or confluent nodes, infinite nodes, extra generators, pre/post transforms, transformed target, trace-bank primitives or singular limits are introduced.

## 2. Independent derivation of original-bank coefficients

The freshly checked element 13 has exact order 11 in F23, and 11 is invertible. Let U = S^epsilon, V = T^delta and omega = 13^(epsilon delta). Then VU = omega UV.

For degree r + ell <= 10, the coefficient of U^r V^ell in (U + V)^(r+ell) is

    D_omega(r,ell) = product_(k=1)^r (1 - omega^(ell+k))/(1 - omega^k).

All denominators are nonzero. This expression also follows inductively from the ordered-monomial recurrence

    D(r,ell) = omega^ell D(r-1,ell) + D(r,ell-1).

The fresh checker evaluates the product expression and independently verifies that recurrence through degree eleven. At degree eleven, each mixed term has numerator factor 1 - omega^11 and a nonzero denominator, so all mixed coefficients vanish. The two pure terms have coefficient one.

For X_j = alpha U + beta omega^j V, U^11 = V^11 = I and (omega^j)^11 = 1 give

    X_j^11 = (alpha^11 + beta^11) I.

Consequently, when Delta != 0,

    (I - X_j)^(-1) = (I + X_j + ... + X_j^10)/Delta.

The monomials S^a T^b for 0 <= a,b < 11 form a basis. For any matrix A, direct character extraction gives its coefficient

    c_A(a,b) = (1/11) sum_(t=0)^10 A[t+a,t] 13^(-bt).

For a bank, set r = [epsilon a]_11 and ell = [delta b]_11. Define G_(epsilon,delta)(a,b) = D_omega(r,ell) for r+ell <= 10, and zero otherwise. Its coefficient is

    alpha^r G_(epsilon,delta)(a,b) H_b,

where

    H_b = beta^ell/(11 Delta) * sum_(j=0)^10 w_j omega^(j ell).

This formula uses the original 1/11 factor and never divides by alpha or beta. It covers beta = 0 and alpha = 0 using the ordinary zeroth-power convention. Equal-alpha groups add their H vectors, even when the physical summands have different legal betas or denominators. Groups whose combined H vector vanishes contribute zero to every coefficient.

## 3. Target coefficients and forced shared moments

The same extraction formula for the literal target is

    c_F(a,b) = (1/11) sum_t 13^(-t^2 - (a+b)t).

Completing the square in Z/11Z, where 1/4 = 3, yields

    c_F(a,b) = C * 13^(3(a+b)^2),
    C = (1/11) sum_t 13^(-t^2) = 18 != 0.

All 121 coefficients were independently extracted and compared with this expression, then recomposed into the literal matrix F. Write f(a,b) = 13^(3(a+b)^2), dividing coefficient equations by C only as algebraic notation.

At a = 11-b for b = 1,2, exactly the (-,+) orientation has a nonzero G. Its sole effective alpha is 4. Its normalized sector amplitude is therefore forced to be

    T_1 = 22,   T_2 = 20.

For b <= a <= 10-b, both negative-delta orientations vanish and G_(+,+)(a,b) is nonzero. Thus the original representation necessarily satisfies

    v_b(a) = ( f(a,b) - T_b 4^(11-a) G_(-,+)(a,b) ) / G_(+,+)(a,b)
           = sum_(x in X) A_(b,x) x^a,

where X is the set of distinct nonzero effective (+,+) alpha nodes. The separate sectors may have different amplitudes, including zero amplitudes, but their nodes lie in the same X.

Reconstruction from the original grammar gives exactly

    b = 1, a = 1,...,9: 19, 4, 20, 14, 20, 3, 14, 16, 8;
    b = 2, a = 2,...,8: 21, 15, 14, 11, 13, 22, 19.

All exponents are strictly positive, so a zero-alpha same-sign group contributes zero to these windows. This does not assume the group vanishes elsewhere. Repeated-alpha banks only change A_(b,x); they do not create a derivative term.

## 4. Why every support of size at most six is covered

Suppose |X| <= 6. There are 22 nonzero elements of F23, so choose a six-element set X' containing X, with six distinct nonzero elements. Define

    h(t) = product_(x in X') (t-x) = sum_(k=0)^6 h_k t^k.

It is monic, squarefree and split with six nonzero roots. For every available length-seven window starting at a,

    sum_(k=0)^6 h_k v_b(a+k)
      = sum_(x in X) A_(b,x) x^a h(x) = 0.

There are three such windows in sector b = 1 and one in b = 2. Therefore H h = 0, with ascending coefficients and

    H = [19  4 20 14 20  3 14]
        [ 4 20 14 20  3 14 16]
        [20 14 20  3 14 16  8]
        [21 15 14 11 13 22 19].

This argument covers empty supports, fewer than six nodes, cancellation at repeated nodes, ineffective groups and zero nodes. Padding assigns no nonzero amplitude to new nodes and adds no physical bank. It is only a necessary annihilator construction.

In particular, a sextic with five distinct roots and a repeated root does not rescue a five-node representation: that representation would also admit a six-distinct-root padded annihilator, which is excluded below.

## 5. Complete independent finite arithmetic certificate

The determinant of the first four columns of H is 4 modulo 23; this was evaluated with a separate 24-term Leibniz calculation. Row reduction gives

    [1 0 0 0  7  7  6]
    [0 1 0 0 10  8 12]
    [0 0 1 0 16 15 21]
    [0 0 0 1  4 13 12].

Setting h_6 = 1 and writing h_4 = u, h_5 = v therefore yields all monic sextics satisfying Hh = 0:

    h_(u,v)(t) = t^6 + v t^5 + u t^4
      + (11 - 4u - 13v)t^3 + (2 - 16u - 15v)t^2
      + (11 - 10u - 8v)t + (17 - 7u - 7v),

for all 23^2 = 529 parameter pairs. The homogeneous RREF's last column and the affine system's right-hand side have opposite signs; both candidate records are correct.

The new checker derives this affine system rather than entering the displayed family as an input. It evaluates every member at all 22 nonzero field elements. The number of polynomials with respectively 0,1,2,3,4,5,6 distinct nonzero roots is

    190, 214, 92, 26, 5, 2, 0.

Thus no family member is the required six-distinct-root annihilator. Every one of the 529 recomputed records agrees with the candidate's inert JSON record.

For a second finite certificate, the checker independently enumerates every six-element subset of F23*. It computes each polynomial through elementary symmetric sums, rather than the candidate's successive multiplication of linear factors, and tests the four residuals. All 74,613 CSV rows, including each support, coefficient and residual, agree exactly with the candidate. Successive survivor counts are

    74,613 -> 3,233 -> 121 -> 3 -> 0.

The three supports surviving the sector-b=1 tests are

    {2,3,5,12,20,22}, with final residual 17;
    {2,7,9,10,12,13}, with final residual 15;
    {3,4,8,17,19,20}, with final residual 20.

A separate direct Vandermonde solve fits the first six b=1 moments for each survivor and confirms all nine b=1 values. Fitting the first six b=2 moments predicts the last value as respectively 2, 4, 22. The required last value is 19, so each fails, with exactly the three displayed residuals. These are direct moment-fit checks in addition to the polynomial obstruction.

No full-sector support-pair solve is needed: there are zero eligible (+,+) supports and hence zero pairs. The candidate's empty pair file is correct. No sufficiency assertion is inferred from a recurrence-only positive result.

## 6. Reflection and actual-bank counting

The contradiction in section 5 proves that any representation in this model has at least seven distinct nonzero effective (+,+) nodes. The argument uses the pinned (-,+) singleton and permits arbitrary numbers of banks in the negative-delta orientations.

Let J e_t = e_(-t). Directly,

    JSJ = S^(-1),   JTJ = T^(-1),   JFJ = F.

Conjugation maps a legal bank of orientation (epsilon,delta) to the same original-grammar bank of orientation (-epsilon,-delta), with the same alpha, beta and raw weights. The phase product epsilon*delta and Delta remain unchanged. The sector index is permuted, so effective groups and their nonvanishing are preserved. In particular both fixed cross-sign singleton nodes remain 4.

Apply the (+,+) lower bound to the conjugated representation. Its (+,+) nodes are the original (-,-) nodes. The original representation therefore has at least seven distinct nonzero effective (-,-) nodes too.

Each distinct effective node in an orientation requires at least one actual bank of that orientation. Each cross-sign orientation has a required nonzero effective group and consequently at least one actual bank. Thus

    actual banks >= 7 + 1 + 1 + 7 = 16.

This counting is valid even if one cross-sign group uses several physical banks, some same-sign nodes are zero, or repeated physical banks cancel in some sectors. It rules out every allocation with at most fifteen actual banks under the stated pins. Conjugation is used to prove a symmetry of representations, not added as a legal computational primitive.

## 7. Controls and reproducibility

Beyond the two exhaustive censuses, the independent checker verifies:

- all 121 target coefficients and exact target recomposition;
- 152 closed-product/ordered-recurrence quantum-binomial checks, including degree-eleven mixed-term vanishing;
- all 484 Gaussian reflection identities and 121 normalized target reflection identities, plus the literal J identities;
- six synthetic recurrence controls: six nodes, three nodes, repeated/canceling nodes, a zero node with nonzero nodes, empty support, and zero-only support;
- legal (alpha,beta) controls (0,7), (7,0), (2,2), (4,6), (22,22), for all four orientations and all eleven phases;
- 220 literal branch inversions by fresh modular Gauss-Jordan elimination and 440 two-sided inverse products;
- 2,420 literal weighted-bank Weyl coefficients against the derived formula, with arbitrary deterministic raw weights and the original 1/11 normalization;
- reflection of every literal branch control.

The controls support the algebra but are not substitutes for it. In particular, legality for all allowed beta values follows from the symbolic coefficient derivation; the numerical controls are not presented as exhaustive over all parameters.

`independent_check.py` is the complete fresh standard-library checker. `outputs/SEXTIC_FAMILY.json`, `outputs/SUPPORT_CENSUS.csv` and `outputs/RESULTS.json` retain its full scientific output. A cold replay of this checker reproduces all three output files byte-for-byte; `REPLAY_VERIFICATION.json` records the sizes and hashes. The package manifest and external seal bind the final deliverable.

## 8. Acceptance boundary and stop

No mathematical repair is required for the candidate's base-field sixteen-bank lower bound. The result is independent of the earlier quintic irreducibility and extension-witness claims: this review proves the base-field lower bound directly from the original grammar and the two new exhaustive finite censuses.

The separately reported equality over F23^5 is not independently re-reviewed here. This acceptance does not establish sixteen-bank attainment, an exact base-field minimum, any unpinned singleton bound, a sixteen-bank lower bound over other extensions, an unrestricted Fourier optimum, characteristic-zero transfer, historical novelty or arithmetic/FFT speed improvement.

The finite review is complete. No seven-node or attainment search was started, no research scope was expanded, no external service was written, and no nested agent was used. Publication significance remains separate from this mathematical acceptance. No live research-table score was changed.
