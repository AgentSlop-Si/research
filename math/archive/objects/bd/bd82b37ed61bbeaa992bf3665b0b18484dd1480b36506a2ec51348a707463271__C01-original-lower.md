# Exact N5 exclusion for the forced chirp B, over all two Hamiltonian orders

## Result

Let zeta be any primitive complex fifth root, let F5 be the unnormalized positive-exponent Fourier matrix, and set

    A=diag(zeta^(3j^2)), 0<=j<5,
    B=(F5^(-1)+A)^(-1).

There is no representation

    B=L0(I-W_pi)^(-1)R0 + L1(I-W_tau)^(-1)R1

in which pi,tau are any Hamiltonian permutations of the five fixed coordinates, W_pi,W_tau have arbitrary edge weights on those structural cycles, the two Green denominators are invertible, and all four endpoints L0,R0,L1,R1 are arbitrary diagonal matrices. The endpoints may be singular, and edge weights may be zero.

This is a computer-assisted exact finite-size exclusion, supported by the algebraic proof and replayable certificates below. It covers all 24^2=576 ordered pairs, with no symmetry reduction. It does not cover unmatched endpoint permutations, a different target B, sums with more terms, or products of Green sums. It does not contradict the separate N3 constructive base case or establish an asymptotic Fourier lower bound.

## 1. The regular target reduction

Put h=3,

    G=sum_j zeta^(3j^2), c=5G,
    B_ij=[zeta^(ij)-G zeta^(-3(i+j)^2)
          +c zeta^(-3i^2) delta_ij]/(1+c).                (T)

This is the previously derived odd-chirp inverse formula. Here G=1+2(zeta^2+zeta^3), and the cyclotomic relation gives G^2=5. Hence c^2=125 and 1+c is nonzero in characteristic zero. For exact verification, reduce the cyclotomic coefficient ring at

    p=241, zeta ->91.

Here 91 has exact order 5, G=103, c=33, and 1+c=34 is nonzero. Thus the target has good reduction; no target denominator is discarded. Its reduction is

    [[161, 20,102,102, 20],
     [ 20,182, 62, 26, 92],
     [102, 62,236, 28, 26],
     [102, 26, 28,236, 62],
     [ 20, 92, 26, 62,182]].

The verifier separately checks this against (F5^(-1)+A)^(-1). Dense matrices here define/check the target; they do not supply an application algorithm.

The working extension for finite branch enumeration is

    E=F241[theta]/(theta^2-7).

Since 7^120=-1 modulo241, this is a field. Every quadratic over F241 splits in E. A field element is recorded as [a,b], meaning a+b theta.

## 2. The finite order universe and first gate

Every Hamiltonian permutation has a unique cyclic traversal starting at 0 followed by a permutation of 1,2,3,4. Enumerating those 24 traversals gives every structural cycle exactly once. Taking every ordered pair gives 576 cases. These structural orders remain fixed even on zero-weight edges. Arbitrary edge-weight choices, diagonal gauges and masks are not discretized or fitted.

For each pair, apply all eligible cleared row-pair equations from the projective-consistency gate. The inverse support patterns are (I,P_pi) and (I,P_tau). Results over the algebraic closure of F241 are:

| Result | Ordered pairs |
|---|---:|
| No common projective row directions |384|
| Finite projective row survivors |192|

All selected transition matrices are invertible in this reduction. Each of the 384 exclusions supplies a spanning forest and at most three incompatible homogeneous quadratics:382 use two, and2 use three. These are algebraic-closure rejections, not merely a failure to find F241-rational roots.

Among the 192 survivors:

- 72 have one connected component and exactly two root directions.
- 120 have two components, each with exactly two root directions.

Consequently there are exactly 72*2+120*4=624 row-direction branches. Infinity is included when the homogeneous quadratic has that root. All roots are simple in this reduction. There are no continuous row components and no unrecorded singular transition strata. These conclusions are checked from the exact gcd and leading/infinity data, not inferred from a numerical fit.

The order inventory and all 576 outcomes appear in ORDER_PAIR_SUMMARY.csv. Full first-stage certificates are in ORDER_SCREEN_RESULTS.json and SURVIVOR_DOMAINS.json.

## 3. Joint column directions and the scale obstruction

For each of the 624 row branches, build the sparse row-direction matrix U. For column j, impose every joint off-support equation on its two possible coefficient positions j,tau^(-1)(j). The resulting two-column constraint matrix has rank exactly one in every column of every branch. Therefore each row branch has exactly one compatible projective column-direction tuple V. No rank-zero column family is omitted.

Let K=UBV. The fixed-direction scale identity is

    K_ij=V_ij x_i+U_ij y_j.

Build the 25-by 11 augmented matrix M(U,V;B) with row indexed by (i,j):

    first 5 columns: V_ij in column x_i, zero elsewhere;
    next 5 columns: U_ij in column y_j, zero elsewhere;
    last column: K_ij.

A genuine invertible-branch sum necessarily has rank M<=10. Every one of the 624 candidates instead has coefficient rank10 and augmented rank 11. For each candidate the certificate records11 equation positions and their nonzero11-by 11 determinant in E.

Crucially, the classification does not reject candidates merely because a base coordinate vanishes. In fact240 branches have a zero row base,240 have a zero column base, and144 have neither. All624 are rejected by the same closed augmented-minor condition. No modular base-coordinate or denominator guard is promoted into a characteristic-zero exclusion.

One certificate example, for order indices0 and7 and their first recorded branch, uses equation positions

    [(0,0),(1,4),(2,1),(3,0),(4,3),(4,0),
     (1,1),(1,2),(2,3),(3,4),(0,2)]

and has determinant 221+173 theta, which is nonzero in E. Its row multidegrees are (1,2,1,1,1), and its column multidegrees are (2,1,1,1,1). The other 623 certificates are supplied in the same explicit format, with both row and column directions.

## 4. Why the augmented minors define a closed projective condition

This is the step that makes the lift safe. A general modular failure of an affine scale solve or an inverse guard would not suffice.

Scale row direction u_i by lambda_i and column direction v_j by mu_j. Then

    U' = D_lambda U, V'=V D_mu, K'=D_lambda K D_mu,

and the augmented matrix transforms as

    M'=D_(lambda_i mu_j) M
       diag(lambda_0^(-1),...,lambda_4^(-1),
            mu_0^(-1),...,mu_4^(-1),1).                    (H)

Take a minor containing all 11 columns and any 11 equation rows R. Write n_i for the number of selected equations whose first index is i, and m_j for the number whose second index is j. Its determinant transforms by

    product_i lambda_i^(n_i-1) product_j mu_j^(m_j-1).

If any n_i or m_j is zero, the corresponding scale column is identically zero, so the determinant is the zero polynomial. Otherwise every displayed exponent is nonnegative, proving that this determinant is multihomogeneous in the ten projective direction pairs. Its total degree in row directions is6 and in column directions is6. The verifier checks these multidegrees and an exact nonzero projective gauge test for every displayed minor.

Thus, for a fixed order pair and target B, the following equations define a closed subset S_B of (P1)^10:

1. all joint off-support equations u_i^T M_ij v_j=0;
2. all 11-by 11 minors of the augmented matrix M(U,V;B).

Only selected nonzero minors need be evaluated to reject the finite candidate list; the necessary system itself is the vanishing of all such minors. It is a necessary condition, not a claimed sufficient description of Green sums.

Sections2 and3 prove that this entire closed projective system has no point over the algebraic closure of F241, for every one of the576 order pairs.

## 5. Singular endpoint masks are retained

The inverse derivation initially assumes invertible endpoint diagonals. To handle masks, suppose a forward Green representation with singular endpoints existed. Replace its zero endpoint scales by a formal epsilon, leaving all cycle weights and valid Green denominators unchanged. The two perturbed branches are invertible over C(epsilon), and their sum B(epsilon) specializes to B.

Normalize each inverse row pair and each inverse column pair independently by its lowest epsilon valuation. Their limits are nonzero projective directions. The joint off-support equations are multihomogeneous, and Section4 proves the same for every relevant augmented minor. Each polynomial vanishes before specialization, so it vanishes at epsilon=0 as well.

Therefore every singular-endpoint representation also supplies a point of S_B. This argument does not require the scale variables to remain finite, a base coordinate to remain nonzero, or any transition determinant to survive specialization. Those are exactly the degenerations that an ordinary affine scale-rejection argument could miss. Zero edges require no division and are retained throughout.

Only genuinely singular Green denominators remain outside the definition of the inverse grammar.

## 6. Projective good reduction gives the complex exclusion

Let R be the localization of Z[zeta5] at the prime (zeta5-91,241), with the target denominator 1+c inverted; it is already a unit there. Equations(T) and the homogeneous equations of S_B are defined over R. The product(P1_R)^10 is projective, and S_B is a closed subscheme of it. Hence its map to Spec(R) is proper. Projective morphisms are proper, and the valuative criterion formalizes their specialization property; see the primary references [Stacks, Tag 01WC](https://stacks.math.columbia.edu/tag/01WC) and [Stacks, Tag 0BX5](https://stacks.math.columbia.edu/tag/0BX5).

If the characteristic-zero fiber had a complex point, it would be nonempty over the fraction field after field extension. The image of a proper morphism is closed. Since that image would contain the generic point of the integral local base, it would also contain its closed point. The special fiber would then have a point over an algebraic closure of F241, contrary to the exhaustive certificates.

Equivalently, over a valuation extension one can normalize every projective coordinate pair and reduce a characteristic-zero solution; the multihomogeneous equations survive. The properness argument also covers solutions whose scale variables or chosen affine coordinates have poles.

Thus S_B has no complex point. Section5 shows that any permitted two-Green representation, including endpoint masks, would create such a point. The conclusion is independent of the complex embedding of Q(zeta5), so it covers every primitive complex fifth root.

This is a lift of emptiness of a closed projective necessary system. It is not a lift of a finite-field positive completion, an open invertibility condition, or a rank-drop-sensitive affine contradiction.

## 7. Controls, replay and limits

The newly authored exact replay uses:

- all 24 Hamiltonian cycles and all 576 ordered pairs;
- algebraic-closure quadratic gcd tests for the 384 first-stage rejections;
- all 624 finite row branches over E, with all 3120 column-nullspace ranks checked;
- 624 explicitly nonzero augmented minors and624 exact gauge-homogeneity checks.

Positive controls verify that the augmented condition is genuinely necessary:

- Eight constructed N5 two-Green sums, including six singular-endpoint controls and four zero-edge controls, all have augmented rank at most 10 using exact normalized limit directions.
- The actual supplied N3 chirp-B two-Green construction has augmented rank 6; all 36 possible7-by7 augmented minors vanish.

These controls do not serve as evidence for an asymptotic algorithm. They test the algebra and boundary handling used in the finite exclusion.

The self-contained Python replay files were authored for these controls. They import local copies of our own earlier verified helpers; no uploaded program was executed. Their hashes and every certificate file are listed in MANIFEST.sha256. Run, in order:

    python screen_orders.py
    python inspect_domains.py
    python screen_completions.py
    python check_minor_positive_controls.py
    python summarize_classification.py

There is no floating-point fitting or unbounded permutation search. No symmetry identification reduces the stated universe. Arbitrary unmatched input/output permutation gauges are not covered by this diagonal-endpoint classification.

Original motivation: ACFF Library package [private-id], ZIP SHA-256 490d919ee261f13bdb22dd5136f065b9ca8d099833ce32bb787bfa1650dbfcf9. The chirp target, projective gate and fixed-direction scale identity come from the prior constructive reports; the exhaustive classification and closed-minor lift are this bounded extension. Independent review remains a separate check of the certificate and proof.
