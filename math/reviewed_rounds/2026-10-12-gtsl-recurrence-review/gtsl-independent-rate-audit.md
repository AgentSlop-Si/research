# Independent GTSL recurrence rate audit

Date: 2026-10-12

## Verdict

The fixed-saving recurrence theorem is valid with nonnegative costs and coefficients, a uniform overhead constant, a fixed eventual upper bound on the saving factor, and finite base cases. Its exact-half conclusion is conditional on the proposed compiler supplying that recurrence. The source does not supply the compiler.

The implication “rho(w) tends to 1/2, therefore C(N) is O(N log log N)” is false as a recurrence inference. Section 5 needs correction, and Conjecture 9.1's half-limit form must be distinguished from its stronger eventual-half form. The polynomial-in-w approach in Section 13 is sufficient for the exact-half conclusion when its missing assumption gamma > 0 is added. Neither these proofs nor the exact finite controls establish a faster Fourier algorithm, a DFT lower bound, a realizable saving family, or historical novelty.

## Publication derivative and source binding

This is a publication derivative of the complete independent rate audit. Private source-location metadata has been removed. Sections 1 through 8 retain the audit's mathematics and verifier-scope analysis verbatim. Section 9 records the original control evidence while explaining the code-free reproduction boundary of this collection.

The [original GTSL manuscript](originals/GTSL_Fourier_Theory_2026-10-12.md) is preserved byte for byte. Its SHA-256 is 68b161ca9880853d38bcf060587a2813cf8b702e5a2c1d75f59f7ae599c42ad1. The retained original ZIP has SHA-256 7dc77fac78b9251a97451d317ef395026fa41faf2c6b01c4ab78f73fe8df9433, and the source verifier has SHA-256 21e9f577f27118012ffc52f26cc3fae7ea0ef50cc9d1cd8bbb8270b4fedad292. The ZIP contains only the same Markdown and verifier, each byte-identical to its separately supplied file.

The source verifier was read and parsed statically, never imported or executed. The independent audit used separately authored standard-library exact-rational controls, whose archived output is preserved in ORIGINAL_CONTROL_RESULTS.json. Executable source and archives are omitted from this prose collection. The source audit's SHA-256 and the derivative relation are recorded in FILE_MANIFEST.json.

The audit treats Section 3's fixed-saving result, Section 5's half-limit statement, Section 9's conjecture, Section 13's rate lemma, Section 16's abbreviated thresholds, and the scope of verify_gtsl_core.py. Claims about public research and project phases were not evaluated here.

## 1 Recurrence assumptions

Let w be a positive integer, N = 2^w, f(w) = C(2^w)/2^w, and let kappa be a fixed nonnegative constant. Assume that, for every sufficiently large integer w,

    0 <= f(w) <= rho(w) [f(floor(w/2)) + f(ceil(w/2))] + kappa,
    rho(w) >= 0.

The base region has bounded finite costs. A recurrence beginning above w = 2 is handled by absorbing its finite prefix into base constants. The claimed algorithmic model must supply these hypotheses with one common cost ledger. The equation is a scalar cost inequality; its validity for an explicit uniform Fourier circuit family is a separate obligation.

All lower-growth statements below concern equality solutions of this scalar recurrence or its dyadic restriction. They demonstrate that particular upper-bound inferences do not follow from the stated hypotheses. They are not lower bounds on Fourier complexity.

## 2 Exact product and sum criterion

On the subsequence w = 2^j, set g_j = f(2^j) and q_j = 2 rho(2^j). Then

    g_j <= q_j g_(j-1) + kappa.

For a nonnegative initial value b, the exact maximal equality envelope is

    B_j = b P_j + kappa S_j,
    P_j = product_(k=1..j) q_k,
    S_j = sum_(i=1..j) product_(k=i+1..j) q_k.

An empty product is 1, B_0 = b, and S_0 = 0. Induction proves the formula and the domination g_j <= B_j. It also handles q_k = 0 without division.

For fixed kappa > 0, finite q_1 >= 0, and b >= 0, the sharp necessary-and-sufficient criterion for this envelope to obey B_j = O(j) is

    S_j = O(j).

Indeed, kappa S_j <= B_j. Conversely, P_j = q_1 product_(k=2..j) q_k <= q_1 S_j for j >= 1, so B_j <= (b q_1 + kappa) S_j. This criterion concerns the worst equality envelope; a particular inequality solution can be smaller.

When kappa = 0 and b > 0, the corresponding criterion is only P_j = O(j). When both kappa and b vanish, the nonnegative solution is zero. Consequently, Theta growth assertions from positive-overhead examples must not be transferred to the zero-overhead case.

This dyadic criterion alone does not control arbitrary rho at non-dyadic w. Uniform shell conditions in Section 3 provide an all-integer sufficient condition.

## 3 Rounded children and sufficient rates

Define d(w) = ceil(log_2 w), with d(1) = 0. If w >= 2 and d = d(w), each child floor(w/2), ceil(w/2) has depth at most d - 1.

### Summable positive shell excess

Suppose there are nonnegative numbers epsilon_d with finite sum such that, on every sufficiently large shell 2^(d-1) < w <= 2^d,

    2 rho(w) <= 1 + epsilon_d.

Choose a finite base envelope A_0 and define

    A_d = (1 + epsilon_d) A_(d-1) + kappa.

The sequence is nondecreasing. Induction over the shells therefore gives f(w) <= A_(d(w)), including unequal children. Every product of factors 1 + epsilon_d is at most exp(sum epsilon_d) = K < infinity. Expanding the recurrence gives

    A_d <= K (A_0 + kappa d).

Thus f(w) = O(log w), and C(N) = O(N log log N). Finite exceptional shells only modify the constant.

Summability is sufficient, not necessary.

### A useful nonsummable sufficient rate

Suppose, for some fixed 0 <= c < 1, all w >= 2 obey

    0 <= 2 rho(w) <= 1 + c/d(w).

Then the explicit barrier

    f(w) <= M (d(w) + 1)

holds for any M >= max(f(1), kappa/(1-c)). At depth d, both children have f <= M d; hence the right side is at most

    (1 + c/d) M d + kappa = M d + c M + kappa <= M(d+1).

For an eventual bound only, enlarge M to cover all exceptional base depths. This proves the same O(N log log N) conclusion even though the positive excess c/d is not summable. The coefficient restriction c < 1 is substantive.

Equivalently, if rho(w) <= 1/2 + a/log_2 w uniformly for large w, a strict margin a < 1/2 is sufficient: choose c with 2a < c < 1 and use d(w)/log_2 w tending to 1. If natural logarithms are used instead, the analogous threshold in this sufficient condition is a < (ln 2)/2. Logarithm bases cannot be dropped from the coefficient comparison.

## 4 Sharp inverse-depth threshold

Consider the positive-overhead equality recurrence with

    q_j = 1 + c/(j+s),

where c >= 0, s >= 0 are fixed and the initial value is nonnegative. With kappa > 0, its asymptotic regimes are

- 0 <= c < 1: B_j = Theta(j)
- c = 1: B_j = Theta(j log j)
- c > 1: B_j = Theta(j^c)

To prove this, sum log(1 + c/(k+s)). The linear terms give c log j + O(1), and the sum of squared terms converges, so P_j = Theta(j^c). Because the factors are positive, the exact expansion may be written

    B_j = P_j [b + kappa sum_(i=1..j) 1/P_i].

Integral comparison gives the three regimes for the sum of i^(-c). No finite experiment is needed for the asymptotic conclusion. The same proof applies to a perturbation q_j = 1 + c/j + O(j^(-1-delta)) for delta > 0, when the factors are eventually positive.

For c = 1, s = 0, and b = kappa = 1, there is an exact formula:

    B_j = (j+1) H_(j+1),
    H_m = sum_(k=1..m) 1/k.

The base value is B_0 = 1. Substitution proves the formula exactly. Define rho(w) = (d(w)+1)/(2d(w)) for w >= 2 and define f by equality in the rounded recurrence with f(1) = 1. This supplies an all-integer recurrence whose dyadic subsequence is the harmonic example, with rho(w) tending to 1/2. Although rho(2) = 1, rho(w) < 1 eventually, as required by any eventual-saving formulation.

For an example with every q_j < 2, take q_j = 1 + 2/(j+2), b = kappa = 1. Direct substitution gives

    B_j = (j+1)(j+3)/3.

Thus even a convergent half-limit with inverse-depth error may have quadratic normalized depth growth.

## 5 Half-limit can exceed every polynomial in depth

The example q_j = 1 + 1/sqrt(j), b = kappa = 1 has

    log P_j = Theta(sqrt(j)),
    P_j <= B_j <= (j+1) P_j.

For j >= 1, log(1+x) lies between x/2 and x when 0 <= x <= 1. Summing x = 1/sqrt(j) proves the product bounds and hence

    B_j = exp(Theta(sqrt(j))).

The independent controls use the entirely rational variant

    q_j = 1 + 1/(floor(sqrt(j)) + 1).

Its factors are strictly below 2, approach 1, and satisfy the same estimates: 1/(sqrt(j)+1) <= 1/(floor(sqrt(j))+1) <= 1/sqrt(j). Therefore it also gives exp(Theta(sqrt(j))) growth. Defining rho(w) as q_(d(w))/2 extends it to the rounded recurrence. At dyadic depth j = 256, the exact rational equality solution has B_j/j > 2,000,000,000. That finite witness illustrates the failure of a small linear envelope; the analytic proof establishes the asymptotic failure of every fixed polynomial in j.

A half-limit alone does imply the weaker uniform statement

    for every fixed eta > 0, f(w) = O(w^eta),
    hence C(N) = O(N (log N)^eta).

For any eta > 0, convergence eventually gives 2 rho(w) <= 2^eta, and the fixed-factor shell recurrence proves the claim. This is sometimes abbreviated as an upper bound N (log N)^(o(1)); the quantified formulation avoids implying a matching lower bound or a polylogarithmic-in-depth bound.

## 6 Repair of the polynomial rate lemma

Make the missing parameters explicit: let 0 <= rho_* < 1, c >= 0, gamma > 0 be fixed, and suppose

    rho(w) <= rho_* + c/w^gamma

uniformly for all sufficiently large w, with the common constant overhead and finite bases.

- If rho_* = 1/2, the shell excess is at most 2c 2^(-gamma(d-1)), a summable geometric sequence. Therefore C(N) = O(N log log N), with no larger power depending on gamma.
- If 1/2 < rho_* < 1, put q_* = 2rho_* > 1. The products of q_* + 2c 2^(-gamma(d-1)) are O(q_*^d), since their ratios to q_* have summable excess. The accumulated constant overhead is also O(q_*^d). Therefore C(N) = O(N (log N)^(log_2(2rho_*))) with the same limiting exponent, not merely some slightly larger fixed exponent.
- If rho_* < 1/2, choose a fixed number q with 2rho_* < q < 1. Eventually 2rho(w) <= q, giving a contracting shell envelope and C(N) = O(N).

Without gamma > 0, these conclusions do not follow. In particular gamma = 0 permits a constant positive error that changes the effective limiting factor. Negative gamma does not even provide convergence to rho_*.

## 7 Pointwise and uniform thresholds differ

Section 16's abbreviated statements are safe only with Section 3's fixed eventual bound understood.

First, pointwise rho(w) < 1 does not imply sub-N log N. For every integer w >= 2, set

    rho(w) = 1 - 1/w, kappa = 1, f(w) = w, f(1) = 1.

Because floor(w/2) + ceil(w/2) = w, the recurrence is exactly

    (1 - 1/w) w + 1 = w.

Thus C(2^w) = 2^w w satisfies the equality despite strict pointwise saving.

Second, pointwise rho(w) < 1/2 does not imply O(N) without a fixed positive gap. Let q_j = j/(j+1), b = kappa = 1. Then

    B_j = (j+2)/2

by direct substitution. Extending rho(w) = d(w)/(2(d(w)+1)) gives strict rho(w) < 1/2 everywhere in the recursion while its dyadic normalized equality costs are unbounded. A fixed bound rho <= 1/2 - epsilon with epsilon > 0 gives O(N); a gap tending to zero need not.

## 8 Scope of the original verifier

Static inspection finds two finite test groups:

1. Cooley-Tukey: one vector x_j = 7 + 11j + 3j^2 modulo 257 for each of N = 16, 32, 64, 128, 256, with splits 4x4, 4x8, 8x8, 8x16, 16x16.
2. Recurrence: fixed rho values 3/4, 1/2, 2/5; base f_0 = 5, kappa = 3; depths 0 through 12; closed-form comparisons and elementary threshold checks.

It does not test varying rho, certify an all-input union DAG, establish a uniform growing compiler, or audit preparation/routing/storage/coefficient ledgers. The Cooley-Tukey identity has a general algebraic proof; a single test vector is not itself an all-input certificate.

There is a simple exact adversarial witness. In the tested field and for every listed size, x_0 = 7 and x_1 = 21. Set

    E = e_0 (21 e_0^T - 7 e_1^T).

Then E is nonzero, E x = 0, and E e_0 = 21 e_0 is nonzero. Hence an erroneous linear map F_N + E would agree with F_N on that one test vector but fail on e_0. The fresh controls verify these facts exactly. This is a witness about test coverage, not evidence that the original Cooley-Tukey implementation is erroneous.

Even a complete basis test over this one finite field would establish that specialization only. An exact complex/cyclotomic claim needs a symbolic identity or an explicit valid lifting argument. A Weyl-relation certificate can be exact when its field, primitive root, shift convention, diagonal convention, normalization, and all relevant identities are defined and verified; the original verifier does not perform that certificate.

## 9 Independent control evidence and reproduction boundary

The archived result ORIGINAL_CONTROL_RESULTS.json records 11 passing groups from the independent exact-rational audit. Its source binding was rechecked against the retained audit packet. The audit's separately authored control script never executed either original file. The original audit packet also supported cold extraction and exact result reproduction. Those historical facts are not represented as a rerun of that script during preparation of this publication collection.

The controls cover source hashes and ZIP equality; a separate suffix-product expansion with zero factors and zero overhead; fixed-factor closed forms and rounded children through w = 4096; subcritical inverse-depth and polynomial-w-rate barriers; exact harmonic and quadratic counterexamples; the rational superpolynomial-in-depth example through j = 256; both pointwise-threshold failures; the original verifier's nullspace blind spot; and rejected overhead/sign mutations.

No executable code or archive is included here, so this collection does not claim turnkey reproduction of the original 11-group run. VERIFICATION.md specifies direct mathematical checks that a reader can reproduce independently. MINIMAL_VERIFICATION.json records the fresh exact-arithmetic checks performed during publication preparation, separately from the historical audit result.

These are finite implementation controls. The asymptotic claims rest on the proofs above. The scope is conditional recurrence mathematics and verifier coverage. Constructing and certifying an actual uniform tensor-union compiler remains open.
