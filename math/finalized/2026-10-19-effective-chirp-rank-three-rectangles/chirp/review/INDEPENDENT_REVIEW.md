# Independent review: effective positive-Gauss chirp cutoff

## Verdict

**Accept the explicit cutoff `N0 = 2^(2^534)`, conditional only on the two already accepted restriction and N=5 projective-exclusion inputs.**

For every odd `N=5m` satisfying `gcd(m,5)=1`, `N ≡ 1 (mod 4)`, and `N ≥ N0`, the specified forced chirp feedback `B_N`, for every primitive complex additive character, is outside a sum of two weighted Hamiltonian-cycle Green resolvents with arbitrary diagonal endpoint masks, legal Green denominators, and fixed coordinates.

This upgrades the previously accepted non-effective finite-exception statement to an explicit, exceptionally large cutoff. It does not determine the actual exceptions below the cutoff. “Positive-Gauss” refers to `G_N²=+N`, not a requirement that `G_N` itself be positive. Both real signs are covered. The `G_N²=-N` branch, unmatched endpoint permutations, different feedback targets, further summands, products of Green sums, and general Fourier algorithms remain outside this conclusion.

No proof defect or required mathematical revision was found. The new proof is deliberately conditional on the existing computer-assisted N=5 result; this review does not silently replace that dependency with sampled tests.

## Reviewed inputs and independence

The candidate reviewed is `source/CANDIDATE_EFFECTIVE_CUTOFF.md`, copied from the constructor's `EFFECTIVE_POSITIVE_CHIRP_CUTOFF.md`, SHA-256:

`a3c758d9016ac5bbc7c78d1133e135d7714a81adf14e8dbc541d18ed7aab7b38`.

The frozen constructor manifest was independently checked: all six entries match. Its final proof change explicitly permits the constant-generator shortcut `Delta=p`; this was reviewed and is valid. The constructor manifest is preserved as inert provenance, not as this review's replay manifest.

The accepted inputs were read in full and their bytes independently hashed:

- Restriction, scalar family, Gauss-sign and infinite-family review: `8fcf5b11cd161e33b8fcab05acae7bf1f17d0f6775b9d2cca6c8f3807b1ea82f`.
- All-order N=5 closed projective exclusion: `aa91fdec5f08cc03e33652869d41be9f9a53bf3c37838c2d5f8d58532dd54586`.

They are preserved under `source/`. The candidate and historical programs were not imported or executed. `independent_controls.py` was written independently for this review, uses only the Python standard library, and has no source-code dependency on either constructor. There were no external writes.

## 1. Primary effective theorem and the degree-two issue

I independently consulted the primary paper, J. Kollár, *Sharp Effective Nullstellensatz*, JAMS 1 (1988), 963–975, specifically Theorem 1.5 and Corollary 1.9 on printed page 965: [primary PDF](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Kollar/kollarnullstellen.pdf).

The statement works over any field and assumes each generator degree differs from two. For `n>1`, its degree bound is a product of at most `n` generator degrees, with the specified extreme-degree selection when there are more generators than variables. Thus in ten variables, positive degrees at most 36, individually different from two, imply `deg(q_j p_j) ≤ 36^10`. This controls each product, exactly what the truncated coefficient matrix needs. No coefficient-height estimate is taken from the paper.

The original chart equations can have degree two, so citing only a maximum degree of twelve would be insufficient under this theorem. Cubing every equation genuinely repairs the issue: over the field `K(g)`, every nonconstant nonzero generator then has degree `3d` for `1≤d≤12`. The zero set is unchanged, while the positive degrees are among `3,6,…,36`. Identically zero equations can be omitted. A nonzero polynomial depending only on `g` is a nonzero constant over `K(g)` and yields a unit certificate of variable-degree zero. These cases are explicitly handled in the candidate.

The theorem is therefore applicable to the actual generator list, rather than to an unjustified degree-only surrogate.

## 2. Closed projective necessity and the anchor

Let `K=Q(eta)`, with `eta` primitive of order five, and define `H=F-gC+g³D` as in the candidate. There are five row-direction pairs and five column-direction pairs. The ten formal scale labels in the augmented matrix are coefficient-column labels; they are not extra variables in the variety or the Nullstellensatz application.

For each of the 576 cycle-order pairs, the off-support equations are entries of `UHV`, and the additional equations are all maximal eleven-column minors of the augmented matrix. The target occurs in exactly one column, hence every such minor is linear in the target. Replacing the target by a nonzero scalar multiple preserves the zero set.

The multihomogeneity calculation is correct. If a minor uses eleven equation rows and a given coordinate index occurs `n_i` times as a row index and `m_j` times as a column index, its direction scaling is

`product(lambda_i^(n_i-1)) product(mu_j^(m_j-1))`.

If any exponent would be negative, the corresponding entire scale column is zero and the determinant is identically zero. Every nonzero minor therefore has nonnegative multidegrees, total row degree six and total column degree six. This is the correct closed projective system, including its boundary. It is important that all maximal minors are present in the universal system; the finitely many historical witnesses used to certify its empty anchor are not substituted for that system.

At `g0=1+2(eta²+eta³)`, the accepted identities give `g0²=5` and `H(g0)=(1+5g0)B5`. The multiplier is nonzero. Thus the accepted empty N=5 projective system supplies an empty fiber of this exact family.

Projection from the product of ten projective lines over `A¹_K` is projective. Its closed subfamily is proper, so its image is closed. A nonempty geometric generic fiber would put the generic point into that image and hence force the whole affine line into the image, contradicting the empty anchor. This is valid separately for every order pair. The required properness statement was independently checked in [Stacks, Tag 01WC](https://stacks.math.columbia.edu/tag/01WC).

No claim that a single empty affine specialization implies generic emptiness is being used. That false shortcut would be vulnerable to solutions escaping to infinity. Projectivity is precisely what excludes that problem here.

## 3. All charts and singular limits

Each projective pair has two standard charts; their product gives exactly 1,024 charts in ten affine variables. Setting the chart's selected coordinate to one is valid on that chart and imposes no condition on the other coordinate. Every geometric projective point, including any pattern of zero base coordinates, lies in at least one of these charts.

The accepted necessary-system result includes singular diagonal endpoint masks by a formal-parameter limit: perturb zero endpoints, normalize each direction by its lowest valuation, then specialize the homogeneous equations. The resulting projective directions remain nonzero even when scale parameters have poles. The new effective proof retains the complete closed system and the complete chart cover; it adds no invertibility guard that could discard those limits.

Zero Green edge weights are also retained because the principal-restriction theorem divides by no individual edge. Singular Green denominators are outside the underlying representation grammar and are not added by this argument.

## 4. Polynomial degrees and coefficient heights

All coefficients lie in `Z[eta]`, hence are algebraic integers. Under every embedding of `K`, every root-of-unity coefficient has absolute value one.

Each target entry has at most three `g` monomials, so embeddingwise polynomial coefficient norm is at most three. Each `UHV` entry has at most four products of one target entry and two direction coordinates, giving norm at most twelve. The ten scale-coefficient columns have entries zero or one direction coordinate, with norm at most one.

An eleven-column determinant has at most `11!` signed products, exactly one target-containing factor in each. Thus its embeddingwise coefficient sum is at most `H*=12·11! = 479001600`. Its total direction degree is twelve and its `g` degree at most three. Dehomogenization cannot increase coefficient sum: it only merges monomials, to which the triangle inequality applies. After cubing, the required bounds are

- affine-variable degree at most 36;
- parameter degree at most nine;
- coefficient norm at most `L=(12·11!)³=109903340320478724096000000`.

These estimates are deliberately coarse but valid for all equations, charts, orders and embeddings. They do not depend on coefficient cancellation, numerical rounding or a selected convenient chart.

## 5. The rank-minor identity is valid at exceptional specializations

Put `D=36^10` and `R=binom(D+10,10)`. Use all monomials of total degree at most `D` as coefficient rows, and columns representing each allowed monomial multiple of a cubed generator. The Nullstellensatz certificate ensures that the coefficient vector `e` of one lies in the column span over `K(g)`.

Let `r` be the generic rank, choose `r` independent columns `C`, and choose `r` rows making a square invertible matrix `Q`. Then `Delta=det Q` is a nonzero polynomial in `Z[eta][g]`. The key claim does not require full row rank, does not require a determinant containing the constant row, and does not require that the chosen determinant remain nonzero at the anchor.

Indeed, because the chosen columns are a basis of the full column space, there is a unique field vector `c` with `Cc=e`. Restriction to the selected rows gives `Qc=e_J`, so `c=adj(Q)e_J/Delta`. Multiplying the full identity gives

`C adj(Q)e_J = Delta e`.

Both sides have polynomial entries, so this is a polynomial identity before specialization. Interpreting its columns as generator multiples shows that `Delta` belongs to the chart ideal in `Z[eta][g,z]`. Consequently every specialized chart solution forces `Delta(g)=0`, including values at which the matrix rank changes. No division is performed at that parameter.

Each matrix entry has `g` degree at most nine and embeddingwise coefficient norm at most `L`. Determinant expansion gives

`deg Delta ≤ 9r`, and `||sigma(Delta)||_1 ≤ r! L^r ≤ A := R! L^R`.

This establishes a completely explicit height bound without needing to form the enormous matrix or select its actual nonzero minor computationally.

## 6. Norm, root bound and the absence of missing chart factors

The four conjugates of nonzero `Delta` are nonzero polynomials. Their product `P` is Galois invariant and has algebraic-integer coefficients, hence `P` is a nonzero integer polynomial. Its degree is at most `36r≤36R`, and its coefficient sum is at most `A^4`.

An exceptional point under any primitive fifth-root embedding makes the corresponding factor vanish. A nonconstant integer `P` has leading coefficient of absolute value at least one, so Cauchy's bound gives `|g|≤1+A^4`. If `P` is constant, that chart has no exceptional parameter at all.

There is no missing multiplication by the number of charts or order pairs in the height cutoff. For any hypothetical point, choose its order pair and one chart containing it; every such chart has the same uniform bound. One need not multiply the chart polynomials together. The four-embedding norm does not require that the selected rank minor be the same as a separately chosen minor in each conjugate system: conjugating its polynomial ideal identity already supplies what is needed.

This is an explicit root bound, not an expanded eliminant or a computed exception list. The existential choice of a nonzero rank minor causes no non-effectivity because all possible choices have the displayed uniform arithmetic bounds.

## 7. Parameter-to-modulus conversion and the numerical cutoff

For the stated moduli, `eta=omega^(m²)` has order five: `gcd(5m,m²)=m` under `gcd(m,5)=1`. The accepted restriction formula is

`B_N[S,S] = H(G_N)/(1+G_N³)`.

The Gauss identity on this branch gives `G_N²=N`, so `|G_N|²=N`, including negative real Gauss sums. The scalar denominator is nonzero because `|G_N³|=N^(3/2)>1`. A full allowed representation would restrict to a block representation and hence to a point of the projective necessary system for `H(G_N)`. Thus

`N ≤ (1+A^4)²`.

The explicit estimates were independently checked with exact integers:

`D=3656158440062976`, `D+10<2^52`, `R<2^520`, and `L<2^87`.

Using `R!≤R^R` gives `log2(A)<607·2^520<2^530`. Hence

`log2((1+A^4)²)<2+2^533<2^534`,

so `(1+A^4)² < 2^(2^534)`. This proves the claimed cutoff, with the displayed `N≥N0` safely beyond the obstruction bound. No floating-point approximation is required.

## 8. Fresh exact controls

The standalone checker passes:

- the exact cyclotomic identity `g0²=5` and nonzero anchor scalar;
- four independent finite-field anchor matrix inversions, checking all 100 entries across the primitive embeddings;
- all 576 structural cycle-order pairs, with 14,400 target-entry and 14,400 `UHV`-entry degree/norm bounds;
- one fresh nonzero symbolic eleven-column determinant for each order pair, including all 576 multidegrees and 576 projective gauge identities;
- 2,304 chart dehomogenization degree/norm checks;
- all 1,024 standard-chart choices, explicitly including zero opposite coordinates;
- a fully expanded cubed sample with 512 terms, affine degree 21 and parameter degree nine;
- the exact rectangular Cramer control `(eta*g)f1-f2=eta²g²-1`, where `f1=eta*g+x+2x²` and `f2=1+eta*g*x+2eta*g*x²`;
- the exact four-embedding norm `Norm(eta²g²-1)=1+g²+g^4+g^6+g^8`;
- all displayed integer constants and exponent inequalities.

The sparse polynomial representation uses integer coefficients and an auxiliary fifth-root exponent; reduction modulo the fifth cyclotomic polynomial is done exactly. Its unreduced coefficient sum provides a safe embeddingwise norm upper bound. The observed small sample bounds are not substituted for the general factorial estimate.

These tests validate the new machinery and its implementation-independent algebraic claims. They do not rerun the accepted finite-field projective emptiness certificate, enumerate exceptional moduli, or construct the huge Macaulay matrix. An isolated replay from a copied standalone checker reproduces the exact results file.

## Final scope

The positive-epsilon branch now has a rigorously explicit cutoff within the stated fixed-coordinate two-Green grammar. The previously accepted square-modulus congruence family remains independently valid below and above that cutoff. No conclusion is promoted to the negative-epsilon curve or unmatched endpoint architecture, and no general algorithmic or asymptotic FFT lower bound follows.
