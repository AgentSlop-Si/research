# Independent audit: global moment chirp bank

## Verdict

**Accept the stated characteristic-zero construction and its narrow minimality theorem.** No fatal identity, legal-pole, or arithmetic-cost error was found. For every odd N≥3, the report gives an exact full-target construction with N+1 nonzero Green occurrences and one diagonal occurrence. Each individual chirp uses exactly r=(N+1)/2 scalar resolvents when the shift is fixed and no separate diagonal correction is permitted. The certified root-free implementation has O(N³) setup and O(N²) application in operations over K=Q(ω).

This is not a sub-N log N Fourier algorithm or an unrestricted Green-count lower bound. It does not resolve independently varying orders, branch-dependent nonconstant endpoints, or arbitrary fused circuits. Its finite-moment/Prony/formal-orthogonality ingredients are established mathematics; publication-level novelty remains unverified.

Two wording clarifications should remain explicit whenever the result is summarized:

1. Individual branch nodes and weights may belong to an algebraic extension of K. The exact branch count is attained over an algebraic closure (and hence over C). The root-free *sum* is implemented over K. There is no proof here that the same minimum is attained with all individual scalar nodes in K.
2. The uniform full-target result is in characteristic zero. Over finite fields, the chirp-bank theorem can hold while 1+NG=0 and B does not exist. Our independent N=3, F7 control demonstrates this exactly.

Neither clarification contradicts the detailed source report, which already supplies the relevant qualifications. They prevent an abbreviated statement from silently becoming stronger.

A constructive audit addendum below gives an exact decision criterion for the same scalar-bank problem when a separate diagonal correction is allowed. The minimum is then either (N−1)/2 or (N+1)/2. The larger count remains necessary for every N≡3 mod 4. At N=5 the smaller count is attained with a simple explicit polynomial. This is a bounded extension of the audited ansatz, not a claim about the unrestricted full inverse.

## 1. Sources, independence, and reproducibility

Primary source: `joint_chirp_bank_0200/GLOBAL_MOMENT_CHIRP_BANK.md`, SHA256 `a1a1343cfb791786360752cd1e32f4767a469657223c98aa8fd418fb7b811c3e`.

The entire source report and its two checker scripts were read statically. Every entry in its manifest was verified. Its two archived predecessor-hash snapshots are equal, contain 26 files, and match the current predecessor files. The predecessor's `FULL_CRT_LIFT_AND_POLE_OBSTRUCTION.md` was consulted only for definitions, the full-target identity, and the stated scope of the earlier obstruction. Its eight-root exception proof was not independently re-audited.

No constructor, predecessor, or uploaded code was executed or imported. `audit_controls.py` is fresh standard-library auditor code. It independently implements rational cyclotomic fields, finite fields, polynomial arithmetic, Gaussian elimination, and regular-representation quotient algebras. In particular, it computes quotient traces as literal matrix traces and inverses by ordinary linear solving, rather than relying on the constructor's Newton-sum trace and extended-Euclidean quotient-inverse routines.

The protected source package was hashed before and after the controls. Its bytes remained unchanged. See `SOURCE_HASHES_BEFORE.json`, `SOURCE_HASHES_AFTER.json`, and `SOURCE_SEAL_VERIFICATION.json`.

## 2. Full target, normalizations, and cycle orientation

Put h=2⁻¹ modulo N, A_ii=ω^(h i²), D=A⁻¹, and X=FA. Completing the square gives

    FAF=GH.

Direct character orthogonality gives

    HAF=ND,
    X³=NG I=cI.

Consequently

    (I+X)⁻¹=(I−X+X²)/(1+c),
    B=(I+X)⁻¹F=(F−GH+cD)/(1+c).

This independently establishes equation (1), without needing to treat the predecessor's cubic identity as a black box. The Gauss-norm argument is valid for composite as well as prime odd N: the substitution (x−y,x+y) is a bijection modulo N, and the resulting additive-character sum is N. Thus |G|²=N, |c|=N^(3/2)>1, and 1+c≠0 in the specified complex embedding.

Both endpoint factorizations are exact:

    A_ii ω^(−h(i−j)²) A_jj = ω^(ij),
    D_ii² ω^(h(i−j)²) D_jj² = ω^(−h(i+j)²).

They are identities on every pair of coordinates, so no CRT-fiber coupling has been dropped.

For P[i,i+1]=1, (P^k)[i,j] is supported on k=j−i modulo N. The chirp is even modulo N, so its coefficient sequence gives the stated circulant. The resolvent geometric series has denominator 1−λ^N with the displayed sign. This is consistent with the backwards application recurrence y_i=x_i+z y_(i+1).

The stated three-B Fourier recovery is also valid. Writing Z=BA=X/(1+X), the cubic implies

    (1+c)Z³−3cZ²+3cZ−cI=0,

and hence

    F=(1+c)B+(1−2c)BAB+(1+c)BABAB.

Our controls verify this identity as well as both inverse products.

## 3. Hankel lower bound and its scope

For f(k)=ω^(σh k²), let q=ω^σ. The factorization

    f(i+j)=f(i)f(j)q^(ij)

is correct. Since q is primitive of order N, the first j nodes 1,q,...,q^(j−1) are distinct for j≤N. Every corresponding leading Hankel determinant is therefore nonzero. In particular M_r uses precisely moments f(0),...,f(N−1), since 2r−2=N−1.

A Q-branch scalar representation supplies those same moments as a sum of Q exponentials. Its Hankel matrix is a sum of Q rank-one matrices, so Q≥r. Repeated nodes combine and cannot evade this bound; zero coefficients can be deleted. Distinct closing weights are not being counted: different nodes may have the same Nth power.

This proof is sharp only in the specified scalar, common-P, no-extra-diagonal model. It does not survive arbitrary branch-dependent diagonal endpoints as written. It does not prove that the displayed N+1 nonzero branches are minimal for B. A diagonal term changes the moment data at k=0, as the addendum concretely demonstrates.

The source's common-order cut-rank discussion is also valid. For a consecutive half-cycle cut, each diagonal-ended cycle Green has off-diagonal rank at most one. The inverse-complementary-cut rank identity removes A. The Fourier Frobenius/operator-norm bound gives |I||Iᶜ|/N, whose integer ceiling is ceil(N/4) for odd N. In natural coordinate order, a Vandermonde minor gives the stronger (N−1)/2 lower bound. These are existing common-order restrictions, not exclusions of arbitrary independently changing orders.

## 4. Orthogonal polynomials, parameter search, and residues

The explicit polynomial formula is correct: multiplying its lth coefficient by L(z^(k+l)) cancels f(l) and leaves f(k)f(j)V_j(q^k). The defining moment systems are nonsingular. P_r uses one extra moment f(N)=1, but its subsequent pencil needs only orthogonality through degree r−2, exactly the constraints imposed by the N target moments.

The algebraic three-term recurrence requires neither positivity nor a real measure. Its norms ν_j=Δ_(j+1)/Δ_j are nonzero for j<r. The coefficient of P_(j−1) is ν_j/ν_(j−1), so a common root of consecutive polynomials propagates to P_0=1. Hence P_r and P_(r−1) are coprime.

Let P=P_r and R=P_(r−1). A repeated root of P+τR cannot be a root of R, and it must be a root of

    W=P′R−PR′.

The leading coefficient of W is r−(r−1)=1 and its degree is 2r−2. Thus there are at most 2r−2 bad finite parameters for repeated roots. Each of the N roots of z^N−1 excludes at most one further parameter; zero excludes at most one. There are at most 2N forbidden values in total. The 2N+1 trial integers are distinct in characteristic zero, and also in characteristic p>2N. The search proof is therefore valid. It should not be transferred unchanged to a small finite characteristic where those trial integers collide.

For the selected monic p, the stated q(z) is precisely the polynomial part of p times the Laurent moment series. Partial fractions give residues q(λ)/p′(λ). The first r moments agree by construction, and the recurrence supplies the remaining r−1 moments through k=N−1. If any residue vanished, the full-rank M_r would be generated by fewer than r exponentials, an impossibility. Nonresonance makes every a=(1−λ^N)b nonzero.

No root extraction cost is hidden in the root-free algorithm. Conversely, the individual node list is not promised as an explicit list of K-coordinates. Already for N=3, one selected polynomial is z²+ωz+1 over Q(ω). Its discriminant has norm 21 to Q, so it is not a square in Q(ω); these particular roots lie outside K.

## 5. Root-free algebra and costs

The selected quotient E=K[z]/(p) is finite étale: p is monic and squarefree. After passing to a splitting field, its trace is the sum of evaluations at the distinct roots. Therefore

    Tr_(E/K)[a(I−zP)⁻¹]

is exactly the scalar branch sum. The guards make p′ and 1−z^N units in E. This is an r-dimensional K-algebra, not a unit-cost scalar field or a scalar-width-one representation.

The source's elementary setup accounting is consistent:

- chirp moments and scalar guards: O(N);
- explicit degree-r coefficient construction: O(r²);
- at most 2N+1 classical polynomial-gcd candidate tests: O(N³);
- q, quotient inverses, z^N, and the trace functional: O(r²+Nr).

The retained coefficients fit in O(N) base-field storage. No Hankel solve is needed by the advertised setup algorithm; the cubic solves in the checkers are only controls.

For application, Horner evaluation takes N multiplications by z, each O(r). One ordinary quotient multiplication by the precomputed closure inverse costs O(r²). The backwards solve and one length-r functional evaluation per output cost O(Nr). Total O(Nr+r²)=O(N²), with O(N+r) working storage. Two banks and chirp scalings leave the same order. There is no missing O(r)-fold branch summation or closure operation.

These are exact field-operation counts with a supplied primitive ω. They are not rational-coordinate bit-complexity, conditioning, numerical root-finding, or finite-precision stability bounds. The construction can of course be replaced by ordinary chirp convolution; doing that does not establish a new FFT speedup.

## 6. Fresh exact controls

The nine full controls are:

- N=3 over F7;
- N=5 over F11;
- N=7 over F29;
- N=9 over F19;
- N=11 over F23;
- N=15 over F31;
- N=21 over F43;
- N=3 over Q(ζ3);
- N=5 over Q(ζ5).

For both signs, each control reconstructs the moment polynomials by linear solving, checks the explicit product formula, checks every leading Hankel determinant through r, performs the guarded search, verifies the recurrence, constructs the quotient algebra independently, and applies the complete scan to every input basis vector. Across all nine cases this is 1,970 bank-output entry comparisons. It is an all-input identity for each finite test size, not merely a few sampled input vectors.

For the eight nonsingular full targets, there are 976 all-entry B comparisons, 1,952 inverse-product comparisons, and 976 three-B Fourier-recovery comparisons. The cubic chirp identity is also checked.

The N=3, F7 exception is intentional: ω=2, G=2, c=6=−1, so the full denominator vanishes. Both chirp banks are still constructed and checked. This is a negative control for the field qualification, not a failure of the characteristic-zero theorem.

The addendum's shifted-polynomial criterion is checked in all nine cases, and separately in Q(ζ9). At N=9 over Q(ζ9), both shifted polynomials pass the guards, giving four nonzero branches plus a diagonal term per chirp. These finite checks do not establish legality for every N≡1 mod 4.

## 7. Constructive addendum: exact criterion with a free diagonal

Consider the relaxed but still narrow model

    C_σ = δI + Σ_(s=1)^Q a_s(I−λ_sP)⁻¹,
    λ_s≠0,  λ_s^N≠1.

Let N=2m+1 and q=ω^σ. Only moments f(1),...,f(2m) must now be matched by the exponential sum. Define shifted moments g(k)=f(k+1). Their m×m Hankel matrix remains nonsingular, because

    g(i+j)=f(1)[f(i)q^i][f(j)q^j]q^(ij).

Thus Q≥m. Let T_m be the unique monic polynomial of degree m satisfying

    Σ_(j=0)^m t_j f(k+j+1)=0,  0≤k<m.

The shifted Hankel system uniquely determines it. If an m-node legal representation exists, its annihilating polynomial must be T_m. Conversely, if T_m has simple nonzero nonresonant roots, standard moment matching supplies m nonzero residues for g, division by the nonzero nodes supplies the residues for f(1),...,f(2m), and δ restores f(0). The original r=m+1 construction is always available.

Consequently the exact relaxed minimum is

    Q_min = m     if T_m has simple, nonzero, nonresonant roots;
            m+1   otherwise.

This is a finite exact classification criterion, not yet a closed-form classification in N.

### Explicit shifted polynomial and the N≡3 mod 4 obstruction

The shifted analogue of the audited coefficient formula is

    T_m(z) = Σ_(l=0)^m (−1)^(m−l) [m choose l]_q z^l,

where the Gaussian binomial coefficient is the ordinary polynomial/rational-product expression at q. Its denominators are nonzero because 1≤j≤m<N. To verify the formula directly, expand ∏_(k=0)^(m−1)(y−q^k) and multiply coefficient l by f(m)q^m/[f(l)q^l]. The extra phase is q^(h(m−l)N)=1, leaving the displayed coefficients.

Gaussian binomial symmetry yields

    z^m T_m(1/z) = (−1)^m T_m(z),
    T_m(0) = (−1)^m.

If m is odd, T_m(1)=0. This root is cycle-resonant. Hence, for every odd N≡3 mod 4, even a free diagonal correction does not reduce the nonzero scalar-resolvent count below (N+1)/2.

If m is even, the reciprocity identity does not force a resonant node. Determining whether its remaining guards always hold for primitive q of odd order N≡1 mod 4 is a concrete next problem. The audit does not claim the answer.

### Complete N=5 formula

Here m=2 and

    T_2(z)=z²−(1+q)z+1.

Its roots λ1,λ2 are nonzero. Its discriminant is (q−1)(q+3)≠0. A unit-circle root would satisfy λ+λ⁻¹=1+q with a real left-hand side, impossible because primitive fifth roots q are nonreal. Thus the roots are nonresonant.

Put

    s0=q³+q⁴−q²,
    δ=1−s0,
    b1=(q³−s0 λ2)/(λ1−λ2),
    b2=(s0 λ1−q³)/(λ1−λ2),
    a_s=(1−λ_s^5)b_s.

Then

    C_σ=δI+a1(I−λ1P)⁻¹+a2(I−λ2P)⁻¹.

The shifted Hankel determinant is 1−q⁴≠0, so neither residue vanishes and two branches are minimal in this relaxed model. The defining identities and both guards were checked exactly in Q(ζ5).

This addendum identifies a productive, closely related next step while showing why the source's original no-diagonal minimum must not be generalized casually. It does not claim a new minimality result for arbitrary Green endpoint/order grammars.

## 8. Novelty and stopping boundary

The cited primary source is correctly described: Stefano Pozza and Miroslav S. Pranić, *The Gauss quadrature for general linear functionals, Lanczos algorithm, and minimal partial realization*, https://arxiv.org/abs/1903.11395. Its abstract explicitly treats complex moments, formal orthogonal polynomials, and minimal partial realization. This independently verified connection supports the report's modest attribution; it is not an exhaustive priority search.

The added shifted-Prony criterion and Gaussian-binomial specialization likewise use established tools. Their project-specific usefulness does not establish publication novelty.

The audit is complete within its assigned scope. The next worthwhile bounded research target is the squarefreeness/nonresonance classification of T_m for N≡1 mod 4, or a genuinely wider endpoint/order ansatz. Repeating finite bank identities alone would not advance either question.
