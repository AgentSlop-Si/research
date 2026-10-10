# C03 refinement: exact degree and endpoint certificates

10 October 2026. New derivation, separate from accepted C03/R15. Source programs were not executed or imported; all computational controls here were newly authored. No external document was changed.

## Result and significance

C03 admits an exact leading-coefficient formula and a division-free Laurent determinant for its trace polynomial. These sharpen its generic statements to specialization-level certificates:

1. Over a field, full residual degree is equivalent to nonvanishing of an explicit list of leading and trailing principal minors. Four ordinary elimination runs decide this and compute the leading coefficient in O(m³) field operations and O(m²) field storage, without resultant construction, sampling nodes, extensions, or root finding.
2. Two explicit constant matrices give the values V(2) and V(−2). They decide whether the forced collision at w=1 has exactly its universal multiplicity and whether w=−1 is an additional root.
3. Degree loss and all extra endpoint multiplicities obey exact formulas, including the characteristic-2 qualification below.

This is a useful structural supplement and a fully costed degree/nondegeneracy test. It is **not** an end-to-end sparse-recovery algorithm or a demonstrated major novelty result. The initial-form calculation, Kronecker resultant identity, trace substitution, and elimination algorithms are classical mechanisms. Exact-family priority remains unresolved.

## 1. Setup and theorem

Let S be a commutative ring, m≥1, A,B in S^(m×m), and D(w)=diag(1,w,…,w^(m−1)). All indices below run from 0 to m−1. Use the fixed degree-(m,m) homogeneous Sylvester resultant

    R(w)=Res_a(det(A−aDAD), det(B−awDBD)).

Retain C03's notation

    v=m(m−1)(4m+1)/6,  b=m(m−1)(2m−1)/6,
    T=m²(2m−1),        v+b=m²(m−1),
    R(w)=w^(v+b)(w−1)^(m²)V(w+w^(−1)),  deg V≤b.

Define leading and trailing principal determinants

    ell_j(M)=det M[{0,…,j−1},{0,…,j−1}],
    r_j(M)=det M[{m−j,…,m−1},{m−j,…,m−1}],

with ell_0=r_0=1 and ell_m=r_m=det M. Put

    C(A,B)=det A det B ∏_(j=1)^(m−1) ell_j(A)r_j(A)ell_j(B)r_j(B).

The coefficient at the *prescribed* degree b, including when actual degree drops, is

    [x^b]V(x) = (−1)^(m(m−1)/2) C(A,B).                 (1)

For every integer n define the integral Laurent polynomial

    S_n(w)=(w^n−1)/(w−1).

This notation means an exact Laurent-polynomial quotient, not inversion of w−1: S_0=0, S_n=1+⋯+w^(n−1) for n>0, and S_(−q)=−w^(−q)−⋯−w^(−1) for q>0. Let X=A⊗B, with row indices (i,k) and column indices (j,l), and let

    N(w)_((i,k),(j,l))=A_ij B_kl S_(1+k−i+l−j)(w).

Then the following identity holds over S[w,w^(−1)]:

    V(w+w^(−1))=det N(w).                              (2)

In particular, with L=diag(0,…,m−1),

    V(2)=det[A⊗(LB+BL+B)−(LA+AL)⊗B]                  (3)
        =Res_t(det(tA+LA+AL),det(tB+LB+BL+B)),

where the latter resultant again has fixed degree-(m,m). If

    E={(i,k): i+k is even},  O={(i,k): i+k is odd},

then

    V(−2)=det X[E,E] · det X[O,O].                    (4)

The determinant of an empty matrix is 1. All four identities hold integrally and therefore in characteristic 2 and in rings with zero divisors. No invertibility of A, B, or their submatrices is assumed.

### Field consequences

Over any field F, (1) gives the exact equivalence

    deg V=b  ⇔ every ell_j(A),r_j(A),ell_j(B),r_j(B)
                 for 1≤j≤m is nonzero.                (5)

In this display the zero polynomial does not have degree b. The same implication from each factor being nonzero is invalid over rings with zero divisors; there (1), and nonvanishing of its whole product, are the appropriate statements.

Suppose now V≠0, put d=b−deg V, and use orders of nonzero polynomials over F. Then

    ord_(w=0)R=v+d,      deg R=T−v−d,                 (6)
    ord_(w=1)R=m²+2 ord_(x=2)V.                      (7)

If char F≠2, also

    ord_(w=−1)R=2 ord_(x=−2)V.                       (8)

Thus (3) is nonzero exactly when R has order m² at w=1. If (3) vanishes, either R is identically zero or its order is at least m²+2. Likewise, when char F≠2, (4) vanishes exactly when a nonzero R has a root at −1, and that root has even multiplicity.

In characteristic 2, 1=−1 and 2=−2. Equations (3) and (4) coincide, (7) remains valid, and (8) must not be used as a separate endpoint formula. For w_0≠0 with w_0²≠1 over an algebraic closure, the quotient is unramified and ord_(w=w_0)R=ord_(x=w_0+w_0^(−1))V. These are field statements, not claims about arbitrary-ring valuations.

## 2. Proof

### Kronecker determinant and complete deflation at w=1

The standard determinant-pencil resultant identity, with the present sign convention, is

    Res_a(det(A−aC),det(B−aF))=det(A⊗F−C⊗B).          (9)

To verify both sign and singular specialization, first work over the fraction field of the universal integer coefficient ring. When A and B are invertible, write H=A^(−1)C and K=B^(−1)F. Triangularize H and K over an algebraic closure. If their eigenvalues are h_i and k_j, the two sides of (9) are both

    (det A det B)^m ∏_(i,j)(k_j−h_i).

Both sides are polynomials in all entries, so equality holds in the universal integer ring and specializes without invertibility. The fixed homogeneous convention is essential when degrees drop.

Apply (9) with C=DAD, F=wDBD. Its entry at ((i,k),(j,l)) is

    A_ij B_kl (w^(1+k+l)−w^(i+j))
      =w^i w^j (w−1) N(w)_((i,k),(j,l)).

Extract w^i from each row indexed (i,k), w^j from each column indexed (j,l), and w−1 from each of the m² rows. The total power of w is

    m Σ_i i + m Σ_j j = m²(m−1)=v+b.

This gives

    R(w)=w^(v+b)(w−1)^(m²)det N(w).

Compare with C03 and cancel the monic factor (w−1)^(m²) and the Laurent unit w^(v+b). Multiplication by a monic polynomial is injective even over a ring with zero divisors. This proves (2).

For every integer n, S_n(1)=n. Hence N(1) has entries A_ij B_kl(1+k+l−i−j), exactly the matrix in (3). The second identity in (3) follows from (9), or from its variant Res_t(det(tA+C),det(tB+F))=det(A⊗F−C⊗B).

Also S_n(−1)=1 for odd n and 0 for even n, for negative as well as nonnegative n. Thus N(−1) is X with entries joining opposite pair parities set to zero. Simultaneously reorder rows and columns to E,O; the two permutation signs cancel. The matrix is block diagonal and its determinant is (4). This also proves the characteristic-2 consistency directly.

### Exact leading coefficient

Work generically over Q(A_ij,B_ij), and set

    d_j(M)=ell_j(M)r_(m−j)(M),   0≤j≤m.

The accepted mixed-minor calculation gives

    [a^j]det(M−aw^e DMD)
      =(−1)^j d_j(M) w^(j(j−1)+ej)+higher powers of w.

The generic roots of the e=0 and e=1 pencils therefore begin respectively as

    alpha_i=(d_i(A)/d_(i+1)(A)) w^(−2i)+higher valuation,
    beta_j =(d_j(B)/d_(j+1)(B)) w^(−2j−1)+higher valuation.

There are no equal valuations between the two families. In alpha_i−beta_j the leading term comes from −beta_j if i≤j and from alpha_i if i>j. There are m(m+1)/2 negative signs. The leading coefficients of the two degree-m polynomials contribute (det A det B)^m with positive combined sign. Consequently

    [w^v]R = (−1)^(m(m+1)/2)(det A det B)^m
       × ∏_i (d_i(A)/d_(i+1)(A))^i
       × ∏_j (d_j(B)/d_(j+1)(B))^(j+1).

The two ratio products telescope to

    (∏_(j=1)^(m−1)d_j(A))/(det A)^(m−1),
    (det B ∏_(j=1)^(m−1)d_j(B))/(det B)^m,

respectively. Thus [w^v]R=(−1)^(m(m+1)/2) C(A,B). On the other hand the C03 factorization gives [w^v]R=(−1)^(m²)[x^b]V. The signs differ by (−1)^(m(m−1)/2), proving (1) generically. Both sides are universal integral polynomials, so the identity specializes to every S, including all cases where the ratio derivation itself would be undefined.

### Orders and degree

If V has degree b−d and is nonzero over a field, the lowest exponent of w in V(w+w^(−1)) is −(b−d), with nonzero coefficient. Its highest exponent is b−d. This yields both formulas in (6). The exact identities

    w+w^(−1)−2=(w−1)²/w,
    w+w^(−1)+2=(w+1)²/w

give (7) and, away from characteristic 2, (8). If w_0²≠1, the derivative of the quotient map is 1−w_0^(−2)≠0, giving the unramified assertion. ∎

## 3. Fully costed application: decide full residual degree

### Exact field-arithmetic model

Input consists of two explicitly stored m×m matrices over a field with unit-cost exact addition, subtraction, multiplication, division by a nonzero element, and zero test. Reading the input costs O(m²). No arbitrary-precision bit claim is implicit in this model.

Perform no-pivot Gaussian elimination separately on A, B, JAJ, and JBJ, where J reverses the coordinates. The last two runs test the trailing principal chains. At the first zero pivot, stop and report [x^b]V=0, hence failure of full degree. This is valid because all preceding pivots are nonzero and the failed pivot is the next leading principal determinant divided by the preceding one. Do not pivot around that zero and then pretend to have tested the original minor chain.

If all runs finish, the product of the first j pivots supplies each required principal determinant. Compute (1) from the four lists. Each elimination uses at most Σ_(k=1)^(m−1) (m−k)²=O(m³) Schur-complement updates and O(m²) divisions. The cumulative determinants and final product use O(m) further multiplications. Reusing work arrays gives O(m²) peak field storage. A zero pivot can only shorten the computation.

Output is the exact prescribed leading coefficient, and a yes/no answer to full degree b. A yes answer also certifies R≠0. A no answer means either degree below b or zero polynomial; it does not distinguish those alternatives. No resultant evaluations, interpolation, admissible w nodes, field extensions, candidate lifting, root finding, or sparse-recovery validation occur in this algorithm. This closes the specified degree-certification task and no larger recovery task.

### Integer input and bit accounting

For integer entries of absolute value at most 2^h, no-pivot fraction-free Bareiss elimination may replace field elimination, stopping at the same zero principal minor. Let B_0=O(m(h+log(m+1))) bound the bit length of every intermediate minor and let B_1=O(m²(h+log(m+1))) bound the final product in (1), by Hadamard's inequality. With M(L) a cost bound for L-bit multiplication and exact division, a conservative implementation costs

    O(m³ M(B_0) + m M(B_1)) bit operations,

and O(m² B_0+B_1) working bits, including the leading-coefficient output. If only the yes/no degree answer is needed, omit the second product term and its output storage. These bounds are deliberately not asserted to be optimal. Rational input requires separately charging denominator clearing and the resulting integer heights.

Bareiss elimination and efficient computation of principal determinant chains are established algorithms, not part of a novelty claim here.

### Endpoint certificates have a different cost

The explicit matrices in (3) and (4) have dimension up to m². Their entries can be built in O(m⁴) field operations/storage; ordinary dense determinant computation costs O(m⁶) operations and O(m⁴) space. These bounds handle singular A or B, any field characteristic, and a vanishing answer without field extension. They are **not** O(m³) merely because A and B are m×m.

When A and B are invertible, the tangent value (3) can instead be computed from the two degree-m polynomials det(tI+A^(−1)(LA+AL)) and det(tI+B^(−1)(LB+BL+B)), multiplying their resultant by (det A det B)^m. Classical O(m³) field-arithmetic characteristic-polynomial methods and a 2m-square Sylvester determinant give O(m³) operations and O(m²) storage for this nonsingular case. More explicitly, paired row/column operations give a similar upper-Hessenberg matrix in O(m³) operations, dividing only by selected nonzero pivots. Its characteristic polynomials of nested leading submatrices follow the standard recurrence using O(m³) scalar operations and O(m²) coefficient storage. This uses no field extensions or division by the integers 1,…,m; it therefore also works in small characteristic. Lo–Monagan–Wittkopf, §2.1, pp. 2–4, supplies the explicit finite-field implementation and recurrence. This optional specialization is not used in the singular-safe O(m⁶) bound, and no corresponding rational bit-complexity claim is made here.

Neither the LU degree test nor the endpoint formulas claim a numerical conditioning guarantee. Exact zero testing cannot be replaced by an unexplained floating-point threshold.

## 4. Controls and strict negative examples

The fresh program constructs each pencil and a **padded** 2m-square Sylvester determinant, divides only the accepted universal factors, and extracts V coefficientwise. It independently checks (1), both forms of (3), (4), and (2) at three rational non-endpoint w-values. Reduction to characteristics 2, 3, 5, and 7 checks all applicable nonzero-polynomial order formulas. The resulting JSON, rather than this prose, gives the completed case count and exact instances.

Useful exact m=2 examples, with the current normalization:

- A=B=I gives V(x)=−x−1.
- A=B=[[0,1],[1,0]] gives V(x)=1. Full degree fails but R is nonzero.
- A=[[1,1],[1,1]], B=I also gives V(x)=1. A singular input does not force a zero homogeneous resultant.
- A=[[4,3],[1,1]], B=I gives V(x)=−4(x−2), hence ord_1 R=6 instead of m²=4 in characteristic zero.
- A=B=[[1,1],[1,−1]] gives V(x)=−4(x+2), hence ord_(−1) R=2 in characteristic zero.
- A=0 gives R=V=0, for which finite multiplicity and degree-loss formulas are not asserted.

The controls are corroboration and regression tests, not a proof or priority determination. Independent review is tracked separately; the original R15 acceptance is unchanged.

## 5. Prior-art boundary and remaining obstruction

The coefficient formula explicitly evaluates a resultant initial form. Sturmfels, *On the Newton Polytope of the Resultant* (1994), Theorems 2.1 and 4.1, supplies the established general framework. Our telescoping calculation is a particular specialization of that mechanism; a negative search does not establish priority for its precise principal-minor product.

The passage from two linear matrix polynomials to A⊗F−C⊗B is classical operator-determinant/resultant algebra. Muhič–Plestenjak, *On the singular two-parameter eigenvalue problem*, §1–2, explicitly studies 2×2 operator determinants using Kronecker products. Graf–Townsend, *A Hidden Variable Resultant Method for the Polynomial Multiparameter Eigenvalue Problem* (2025), §2.4, equation (10), reviews established matrix-polynomial Bézoutian constructions with A(s)⊗B(t)−A(t)⊗B(s). Their general framework must not be attributed to C03; our proof of the exact scalar determinant equality and sign is supplied above.

Baker, *Reciprocity via Reciprocants*, Proposition B.1 and Remark B.2, already provides the trace substitution and integral recurrence. Proposition 2.3 also explains why square phenomena at reciprocal specializations are not inherently new. The parity-block endpoint formula here is an explicit specialization, not a new invariant theory.

Bareiss's 1968 original article explicitly includes determinant and leading-minor computation. The O(m³) arithmetic certificate uses this standard linear algebra after the explicit product has been identified.

What is now stronger than the accepted statement is the exact specialized coefficient, explicit residual determinant, endpoint values, and inexpensive complete decision procedure for **full degree**. What remains unproved is a consequential new sparse-recovery result, a faster general construction of all coefficients or roots, a numerical stability advantage, or worldwide priority. The original b+1 versus T+1 interpolation comparison remains Θ(m³) versus Θ(m³) and cannot supply such an asymptotic claim.

### Primary sources inspected in this pass

- Sturmfels, Theorems 2.1 and 4.1: https://www.maths.tcd.ie/EMIS/journals/JACO/Volume3_2/m4496732732u7744.fulltext.pdf
- Muhič–Plestenjak, operator determinants and singular cases: https://users.fmf.uni-lj.si/plestenjak/Papers/SingularMEPDeltaSubm.pdf
- Graf–Townsend, §2.4, equation (10), and established matrix-polynomial resultant constructions: https://arxiv.org/html/2503.22887v1
- Baker, Proposition B.1, Remark B.2, and Proposition 2.3: https://arxiv.org/html/2309.02512v2
- Bareiss, original article, abstract and opening identity/leading-minor discussion available through primary search extraction; full-open requests returned an internal tool error and HTTP 403 on the alternate AMS path, so no complete page-level reading is claimed: https://www.ams.org/mcom/1968-22-103/S0025-5718-1968-0226829-0/S0025-5718-1968-0226829-0.pdf
- Lo–Monagan–Wittkopf, *A Modular Algorithm for Computing the Characteristic Polynomial of an Integer Matrix in Maple*, §2.1, pp. 2–4, primary full-text pseudocode and recurrence read: https://www.cecm.sfu.ca/CAG/papers/CPpaperOld.pdf

The first four sources and Lo–Monagan–Wittkopf were opened as primary full texts. No exact printed match for the complete specialization-level theorem above was established. None of these comparisons changes C03's accepted correctness.
