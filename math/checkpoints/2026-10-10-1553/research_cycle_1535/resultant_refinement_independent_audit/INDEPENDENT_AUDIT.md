# Independent audit of C03 quotient-determinant refinements

10 October 2026. New, source-preserving work. No supplied/author program was executed or imported. The controls in this folder were written from scratch and use an explicit fixed-degree Sylvester matrix, a separate integer Bareiss determinant, and a separate rational Gaussian determinant. Source hashes were checked before and after the run.

## Verdict

**PASS at the stated algebraic scope.** The proposed Laurent divided-difference determinant has exactly the claimed quotient normalization. Its tangent endpoint, parity endpoint, signed leading coefficient, and field-arithmetic cubic full-degree test are valid. The characteristic-2 endpoint merger and the distinction between full residual degree and exact collision multiplicity must remain explicit. These are refinements of the already accepted C03 family, not a novelty clearance or an end-to-end fast resultant/recovery algorithm.

A complete independent proof and 1,038 recorded exact controls support this verdict. The numerical controls corroborate the proof; they do not substitute for it.

## 1. Definitions and exact normalization

Let S be any commutative ring, m≥1, A,B in S^(m×m), and D=diag(1,w,...,w^(m−1)). Use zero-based indices and the standard fixed homogeneous degree-(m,m) resultant convention

    Res(f,g) = lc(f)^m ∏_{f(α)=0} g(α)

on full-degree specializations, extended by the degree-(m,m) Sylvester determinant on every specialization. Set

    n=m², b=m(m−1)(2m−1)/6,
    v=m(m−1)(4m+1)/6, L=m²(m−1)=v+b.

The accepted base theorem defines V uniquely by

    R(w)=Res_a(det(A−aDAD),det(B−awDBD))
        =w^L(w−1)^n V(w+w^(−1)),  deg V≤b.

For every integer t define a Laurent polynomial, with no actual division operation,

    S_t(w)=Σ_{r=0}^{t−1} w^r                 if t>0,
    S_0(w)=0,
    S_t(w)=−Σ_{r=t}^{−1} w^r               if t<0.

Thus (w−1)S_t=w^t−1 in S[w,w^(−1)]. Define the m²×m² matrix N by

    N_(i,k),(j,l) = A_ij B_kl S_(1+k−i+l−j)(w).

Then, exactly and without an extra sign or monomial,

    det N(w)=V(w+w^(−1)).

### Proof

For arbitrary m×m matrices A,C,B,E over a commutative ring, the universal determinant-resultant identity is

    Res_a(det(A−aC),det(B−aE))=det(A⊗E−C⊗B).

To check its convention, work first over the characteristic-zero universal fraction field, where A and B are invertible. If λ_i and μ_j are the eigenvalues of A^(−1)C and B^(−1)E, respectively, the resultant is

    det(A)^m det(B)^m ∏_(i,j)(μ_j−λ_i).

The right-hand determinant has exactly this value. The equality is a polynomial identity with integer coefficients in all matrix entries, so specialization proves it over arbitrary commutative rings, including singular inputs and degree drops. In particular, m=1 gives AE−CB, fixing the sign.

Apply it with C=DAD, E=wDBD. Each Kronecker entry is

    A_ij B_kl (w^(1+k+l)−w^(i+j))
      =w^i (w−1) N_(i,k),(j,l) w^j.

The total row-and-column w-power is

    2m Σ_(i=0)^(m−1)i =m²(m−1)=L.

Therefore R=w^L(w−1)^n det N. Comparing with the base theorem proves the claim universally. No inverse of A or B, of 2, or of w−1 is used in the specialized result. The notation S_t=(w^t−1)/(w−1) is safe only as shorthand for the Laurent polynomial above.

## 2. The endpoints

Put H=diag(0,1,...,m−1), and K=A⊗B.

### At x=2

Because S_t(1)=t for every integer t,

    V(2)=det[A⊗(B+HB+BH)−(HA+AH)⊗B].

Equivalently, its (i,k),(j,l) entry is (1+k−i+l−j)A_ij B_kl. This tangent Kronecker formula is valid over every S, with integers mapped to S.

### At x=−2

Let E={ (i,k):i+k is even } and O={ (i,k):i+k is odd }. These are index sets, not spectral assumptions. Since S_t(−1) is 1 for odd t and 0 for even t, N(−1) is K with its opposite-parity off-diagonal blocks zeroed. Consequently

    V(−2)=det K[E,E] · det K[O,O].

There is no sign: the same index permutation groups both rows and columns. Empty determinants equal 1, covering m=1. The block sizes are ceil(m²/2) and floor(m²/2).

In characteristic 2, −1=1 and −2=2=0. The two endpoint expressions agree; they are not separate certificates. The integer identities themselves remain valid.

## 3. Leading coefficient, including its exact sign

For an m×m matrix M, write

    L_t(M)=det M[{0,...,t−1},{0,...,t−1}],
    T_t(M)=det M[{m−t,...,m−1},{m−t,...,m−1}].

Then

    [x^b]V(x)
      =(−1)^(m(m−1)/2) det(A)det(B)
         ·∏_(t=1)^(m−1) L_t(A)T_t(A)L_t(B)T_t(B).       (★)

The product is empty for m=1. This is an arbitrary-ring coefficient identity, whether or not V actually has degree b.

### Proof and sign audit

Work generically over Q(A_ij,B_ij). Put

    c_j(M)=L_j(M)T_(m−j)(M),  0≤j≤m,

with L_0=T_0=1, so c_0=c_m=det M. The coefficient of a^j in det(M−aw^eDMD) has unique lowest w-term

    (−1)^j c_j(M) w^(j(j−1)+ej).

The Newton polygon has root leading terms

    α_i=(c_i(A)/c_(i+1)(A)) w^(−2i),
    β_j=(c_j(B)/c_(j+1)(B)) w^(−2j−1).

All these ratios are nonzero generically. In α_i−β_j the α term wins exactly when i>j; the β term wins when i≤j. Therefore the sign of the product of differences is (−1)^(m(m+1)/2). The leading coefficient of R at w^v is

    (−1)^(m(m+1)/2) det(A)^m det(B)^m
      ·∏_(i=0)^(m−1)(c_i(A)/c_(i+1)(A))^i
      ·∏_(j=0)^(m−1)(c_j(B)/c_(j+1)(B))^(j+1)
      =(−1)^(m(m+1)/2) det(A)det(B)
         ·∏_(t=1)^(m−1)c_t(A)c_t(B).

The w^v coefficient in w^L(w−1)^n V(w+w^(−1)) is (−1)^n[x^b]V. The resulting sign is (−1)^(m(m−1)/2), since the exponent difference is even. Reindexing the trailing minors gives (★). It is a universal integer-coefficient identity and specializes to every S.

Simple sign controls: A=B=I gives V=1 for m=1, V=−x−1 for m=2, and V=−x^5−4x^4−5x^3−x²+2x+1 for m=3. The leading signs are +,−,− as (★) requires.

## 4. Full-degree decision in O(m³) field operations

Over a field F, V has degree exactly b if and only if every determinant factor in (★) is nonzero. This does not require constructing either V or R.

Run ordinary elimination without row swaps on A and B, and on their simultaneous row/column reversals JAJ and JBJ. At any zero pivot, return “not full degree.” Provided previous pivots are nonzero, a zero pivot is exactly a zero next leading principal minor, so stopping is sound. If all four passes succeed, every leading and trailing principal minor, including det A and det B, is nonzero, and the answer is “full degree.”

Four classical elimination passes take O(m³) field operations and O(m²) storage. Running products of pivots can also obtain all required minors and (★) at the same asymptotic cost. Row pivoting must not be used to hide an encountered zero pivot: nonsingularity alone is insufficient.

This is a field-arithmetic count with equality tests and inversions. It is not a bit-complexity bound, does not give a cubic algorithm for all coefficients of V, and does not automatically extend to arbitrary rings where a nonzero element need not be invertible or where a product of nonzero factors may vanish.

## 5. Exact valuations and caveats

Suppose F is a field and V≠0, with d=deg V. Then

    ord_(w=0) R=v+b−d,
    deg_w R=v+b+n+d.

Thus full degree is equivalent to attaining the universal lower w-order v. A zero resultant corresponds to V=0; use infinite order / undefined degree conventions separately, rather than substituting it into the finite formulas.

Let mult_c V be root multiplicity at x=c. The exact identity

    w+w^(−1)−2=(w−1)²/w

gives, in every field characteristic,

    ord_(w=1) R=n+2 mult_2 V.

If char F≠2, the distinct endpoint identity

    w+w^(−1)+2=(w+1)²/w

gives

    ord_(w=−1) R=2 mult_(−2) V.

If char F=2, the two points merge and the correct order is

    ord_(w=−1) R=ord_(w=1) R=n+2 mult_0 V.

In particular V(2)≠0 certifies exact collision order n. For char F≠2, V(−2)≠0 certifies absence of a root at w=−1. The full-degree test and endpoint certificates answer different questions. Example: for A=B=I and m=2, V=−x−1 still has full degree over F_3, but V(2)=0 and ord_(w=1)R=6 rather than n=4.

The quotient determinant can be evaluated at nonzero w, including ±1 through S_t. The formula does not authorize division by w−1 in a ring or field at w=1, and a vanishing homogeneous resultant still does not certify a legal recovery.

## 6. Fresh exact controls

`fresh_controls.py` is the sole newly written executable in this audit. `EXACT_CONTROL_RESULTS.json` contains the full result and source-preservation hashes. `control_run.log` records the successful run. The final run records:

- 21 full exact polynomial reconstructions from explicit homogeneous Sylvester matrices, with m=1,2,3,4; identity, dense full-degree, random, zero, singular, and nonzero degree-drop cases.
- Each polynomial case checks the exact leading-coefficient formula, four direct quotient-determinant values at rational nodes, both endpoint formulas, and (for nonzero R) zero/infinity degrees and rational endpoint multiplicities.
- 60 larger exact specializations through m=5, comparing separately implemented resultant and quotient determinants.
- 92 unit-w specializations in Z/qZ for q=2,3,4,5,8,9,12, including rings with zero divisors.
- 56 ring endpoint controls, including the characteristic-2 merger.
- 700 finite-field comparisons between direct principal-minor products and the four-pass O(m³) full-degree test, for m=1,...,7 and p=2,3,5,7,101.
- 74 finite-field endpoint multiplicity controls, including characteristic 2 and the extra collision order in characteristic 3.
- 21 direct tangent fixed-degree resultant controls and 14 normalized characteristic-polynomial resultant controls for nonsingular inputs.

All 1,038 records pass. The additional per-record assertions are not counted as separate records. Source files remained byte-for-byte unchanged. A first completed assertion run hit only a JSON serialization issue for SymPy integer objects; the serializer was corrected and the complete suite rerun. No failed mathematical assertion occurred.

## 7. Novelty and use boundary

The normalizing Kronecker resultant, Laurent divided differences, generic lowest-weight telescoping, and principal-minor elimination are classical mechanisms. This audit establishes exact specialized formulas and an inexpensive degeneracy/full-degree certificate for C03. It does not establish that the particular printed family has appeared before, nor that it is novel. The existing `RESULTANT_NOVELTY_VERDICT.md` therefore remains applicable: formula/application priority unresolved; no major breakthrough or general fast recovery claim follows.

The determinant N has dimension m². Merely replacing a resultant by that determinant is not an arithmetic speedup. The useful cheap result proved here is the O(m³) field-arithmetic full-degree decision, and the endpoint formulas provide exact specialization/collision certificates.

## Sources preserved

- `research_cycle_0958/algebra/final_v1/PROOF_CLOSURE.md`: accepted C03 base theorem.
- `research_cycle_1453/novelty_resultant/RESULTANT_NOVELTY_VERDICT.md`: existing scoped prior-art assessment.

Their SHA-256 values are recorded in `EXACT_CONTROL_RESULTS.json`; the audit report supplements rather than edits either source.


## 8. Review of the completed refinement draft and its further cost claims

Reviewed artifact: `research_cycle_1535/resultant_structure/RESULTANT_STRUCTURAL_REFINEMENT.md`, SHA-256 `2da369c92f44648dcf1c68c94fae623610efedf37ab11e91a1df328ebb858a14`.

The draft's additional fixed-degree identity

    V(2)=Res_t(det(tA+HA+AH),det(tB+HB+BH+B))

has the correct sign and normalization. It follows from the same universal Kronecker resultant identity and is independently checked in all 21 polynomial cases, including singular inputs.

When A and B are invertible, normalizing the two tangent pencils multiplies their resultant by (det A det B)^m. The resulting two monic characteristic polynomials and a 2m-square Sylvester determinant can indeed be computed in O(m³) field operations and O(m²) field storage. This is a distinct nonsingular tangent-value algorithm, rather than a bound for all coefficients of V. Fourteen fresh normalized-resultant controls pass.

The final draft explicitly chooses a characteristic-safe characteristic-polynomial method: upper-Hessenberg reduction by paired row/column similarities, followed by a polynomial coefficient recurrence. It does not use division by the integers 1,...,m. To see the arithmetic count directly, for upper-Hessenberg Q let p_j(t)=det(tI_j−Q_j), where Q_j is its leading j-square submatrix. Then p_0=1 and, with one-based indices,

    p_j=(t−Q_jj)p_(j−1)
        −Σ_(i=1)^(j−1) Q_ij (∏_(k=i)^(j−1)Q_(k+1),k) p_(i−1).

The product chain takes O(j) scalar work for each j and the coefficient sums take O(j²), totaling O(m³), with O(m²) coefficients stored. The upper-Hessenberg reduction itself uses O(m³) operations, dividing only by selected nonzero field pivots. Thus the claim includes small characteristic without an unspoken field extension.

The separate singular-safe endpoint bound O(m⁶) field operations and O(m⁴) space is sound for ordinary dense determinants of matrices of dimension at most m². It should not be mislabeled cubic.

For integer entries bounded by 2^h, the draft's conservative fraction-free bit bounds are also sound as stated. Bareiss intermediates are minors with bit size B_0=O(m(h+log(m+1))); transient products differ only by a constant factor in bit length. The product in (★) has size B_1=O(m²(h+log(m+1))). Under the draft's explicit convention that M(L) bounds both multiplication and exact division, O(m³ M(B_0)+m M(B_1)) bit operations and O(m² B_0+B_1) working bits are valid upper bounds. Denominator clearing for rational input is correctly left separately charged. This does not assert an optimal bit bound or numerical conditioning guarantee.

**Final draft verdict: PASS on correctness and stated computational scope.** No remaining mathematical correction was identified. Exact-family novelty remains unresolved, as the draft itself says. The prior-art quotations/locators are not independently literature-audited by this report; its independent scope is the stated formulas, algebraic proofs, and cost claims.
