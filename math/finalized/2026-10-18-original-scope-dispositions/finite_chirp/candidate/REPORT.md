# ALG-FINITE-CHIRP-1001: exact Padé comparison and bounded disposition

18 October 2026 UTC. Read-only comparison at repository commit e3099aa1657e9b9fe8e053282c0cdb658d50e7d3. No repository or spreadsheet change was made.

## Decision

Close the recorded exact-comparison obligation and retain ALG-FINITE-CHIRP-1001 as a completed, scoped finite supporting result under F021. The denominator, formal-moment realization, and forced-diagonal machinery have exact classical identifications. The complete legal-cycle minimum is a qualified nonmatch to those generic theorems because their admissible objects differ.

The previously accepted coverage remains exactly all 500 odd N from 3 through 1001: 250 saved modular squarefreeness certificates for N=5,9,...,1001, combined with the uniform N=3 mod 4 resonance obstruction. This comparison does not rerun those certificates or add a new acceptance of their bytes.

No mathematical proof gate remains for this finite record. Do not extend its endpoint, turn the finite result into an all-composite theorem, close the wider F021 owner, create another owner, or promote historical priority. Retain the existing supporting/refinement attribution and the unverified worldwide-priority qualification.

## 1. Target and accepted evidence

Write N=2m+1 >= 3, h=m+1, K=Q(q), with q a primitive Nth root in characteristic zero. The target is

    f(k)=q^(h k^2),  C=sum_(k=0)^(2m) f(k)P^k,
    C=delta I + sum_(s=1)^Q a_s (I-lambda_s P)^(-1),

where P is one fixed natural N-cycle, a_s != 0, lambda_s != 0, and lambda_s^N != 1. Nodes may lie in an algebraic closure of K. Repeated ordinary nodes combine; confluent/higher-order resolvents are excluded. An arbitrary free diagonal still has to be scalar, since both other terms are circulant. Arbitrary nonconstant diagonal endpoints on individual branches would change the model.

The accepted criterion is Q_min=m precisely when

    T_m(z)=sum_(j=0)^m (-1)^(m-j) [m choose j]_q z^j

is squarefree and has no Nth-root-of-unity zero. Its constant coefficient is already nonzero. Otherwise the accepted guarded pencil gives Q_min=m+1. The shifted Hankel rank proves Q>=m.

The accepted finite classification is

    Q_min=(N-1)/2  if N=1 mod 4,
    Q_min=(N+1)/2  if N=3 mod 4,

only for the stated finite record, although some separate ingredients have wider proven domains.

Sources:
- [Accepted classification](https://github.com/AgentSlop-Si/research/blob/e3099aa1657e9b9fe8e053282c0cdb658d50e7d3/math/archive/objects/c6/c64b813620686131f520339c14a0e5efc1c859999c228c823faf68e943d5a0b1__CLASSIFICATION.md), sections 1, 4-6.
- [Independent audit](https://github.com/AgentSlop-Si/research/blob/e3099aa1657e9b9fe8e053282c0cdb658d50e7d3/math/archive/objects/af/af52543f5eddb8bbcdc1c96bc3fde65db64b58090eb0ed36d93eb0cc1d141333__INDEPENDENT_AUDIT.md), exact model, residues, finite certificates, and limitations.
- The live bounded Catalogue row 94 read in this pass agrees with those scope and remaining-comparison statements.

## 2. Primary-source theorem locators

LS87 is D. S. Lubinsky and E. B. Saff, Convergence of Padé Approximants of Partial Theta Functions and the Rogers-Szegö Polynomials, Constructive Approximation 3 (1987), 331-361, [DOI record](https://doi.org/10.1007/BF01890574). The retained authorized scan was read as page images.

Printed p.340, Theorem 3.2(ii)/(3.12), identifies the normalized denominator for the partial theta series through the Rogers-Szegö polynomial. The displayed degree condition is M>=n-1>0; the needed non-root conditions hold when q has order N>m. Printed p.343, Lemma 4.1/(4.5), gives reciprocity, and (4.6)-(4.7) supplies the finite q-binomial product. LS87's auxiliary H in (4.6) is weighted and is not its G or this record's unweighted H.

PP20 is S. Pozza and M. Pranić, The Gauss quadrature for general linear functionals, Lanczos algorithm, and minimal partial realization, [arXiv:1903.11395v3](https://arxiv.org/html/1903.11395v3). Theorem 3.3, Definition 4.1, Theorem 4.2, Lemma 4.5, Theorem 4.6, and section 6 give the complex-moment framework: regular formal orthogonality yields unique Gaussian quadrature, with multiplicities counted and derivative evaluations permitted, and the corresponding minimal matrix realization. These are inspected theorem statements and proofs, not a claim that this survey originated the framework.

The following substitutions and conclusions are this comparison's algebraic deductions, rather than verbatim source claims.

## 3. Exact Lubinsky-Saff substitution

Use different symbols for the source Padé indices: [M/n]. Define

    alpha=q^h, beta=q alpha=q^(h+1),
    h_q(u)=sum_(k>=0) q^[k(k-1)/2] u^k,
    F(t)=sum_(k>=0) f(k)t^k,
    U(t)=sum_(k>=0) f(k+1)t^k.

Since k(k-1) is even and 2h=N+1,

    f(k)=alpha^k q^[k(k-1)/2],
    F(t)=h_q(alpha t),
    U(t)=alpha h_q(beta t),
    F(t)=1+tU(t).

These are formal series identities. No analytic continuation or convergence limit is needed.

Writing G_n(w;q)=sum_j [n choose j]_q w^j, LS87 (3.12) is

    Q_(M,n)(-w q^(-M))=G_n(w;q),
    equivalently Q_(M,n)(u)=G_n(-q^M u;q).

At (M,n)=(m-1,m) for U and (M,n)=(m,m) for F,

    Q_(m-1,m)(beta t)=G_m(-q^(m-1+h+1)t;q)=G_m(-t;q),
    Q_(m,m)(alpha t)=G_m(-q^(m+h)t;q)=G_m(-t;q),

because m+h=2m+1=N. The scalar alpha in U changes its numerator, not its normalized denominator. Thus the exact common denominator is

    D(t)=G_m(-t;q),  D(0)=1,
    T_m(z)=z^m D(1/z)=(-1)^m G_m(-z;q).

The last equality follows from reciprocity. This proves the requested formula-level equivalence, including the shift, scaling, reciprocal variable, and sign.

For m>=2, both source index hypotheses hold, and q^j!=1 for 1<=j<=m because m<N. The source's strict n-1>0 excludes m=1. At N=3, direct series matching supplies the omitted boundary: D(t)=1-t and T_1(z)=z-1. No invocation of Theorem 3.2 outside its printed range is needed.

## 4. Numerators, residues, and the forced diagonal

Let A(t)/D(t) be the shifted [m-1/m] approximant. Then

    U(t)-A(t)/D(t)=O(t^(2m)),
    B(t)=D(t)+t A(t),
    F(t)-B(t)/D(t)=O(t^(2m+1)),

with deg A<=m-1 and deg B<=m. Therefore B/D is the full [m/m] approximant with the same D.

The accepted Laurent numerator R is exactly related by

    A(t)=t^(m-1)R(1/t),
    R(z)/T_m(z)=z^(-1) A(1/z)/D(1/z).

If T has simple roots lambda_s, partial fractions give

    c_s=R(lambda_s)/T'(lambda_s),
    U_*(t)=A(t)/D(t)=sum_s c_s/(1-lambda_s t).

The bank-moment coefficients and physical resolvent coefficients differ:

    b_s=c_s/lambda_s,
    a_s=(1-lambda_s^N)b_s.

This is the essential conversion. The PP weights match c_s, not a_s. Roots of D are t_s=1/lambda_s, so cycle resonance is equivalently t_s^N=1.

The constant polynomial part of B/D at infinity is forced:

    delta=B_m/D_m=1+A_(m-1)/D_m
          =1+R(0)/T(0).

Here D_m=T(0)=(-1)^m. Subtracting this delta leaves a proper rational function of denominator degree m. Hence it has exactly the right form sum b_s/(1-lambda_s t) when the roots are simple and nonzero.

The product formula is also an exact classical-product consequence. Since B agrees through degree m with D F,

    B_m=sum_(j=0)^m (-1)^j [m choose j]_q f(m-j)
       =f(m) sum_(j=0)^m (-1)^j [m choose j]_q q^[j(j+1)/2]
       =f(m) product_(j=1)^m(1-q^j).

The second equality uses alpha q^(-m)=q, and the third is LS87's finite product at argument -1. Also

    h m^2 + m(m+1)/2 = N m(m+1)/2,

so f(m)=q^[-m(m+1)/2]. Dividing by D_m yields

    delta=(-1)^m q^[-m(m+1)/2] product_(j=1)^m(1-q^j).

All its factors are nonzero. This agrees with the accepted determinant ratio and residue formula. It remains the forced candidate in an illegal smaller-bank case; it does not cure a repeated or resonant node.

Attribution consequence: the explicit denominator and diagonal product should be described as this exact Padé/q-binomial specialization and elementary rational-part extraction. They are not evidence for a new general moment method or a new Rogers-Szegö identity.

## 5. Exact quadrature mapping and the qualified nonmatch

Define the finite linear functional

    L(x^j)=mu_j=f(j+1),  0<=j<=2m-1.

Its m by m Hankel matrix is [f(i+j+1)]. The accepted Vandermonde factorization proves its determinant nonzero. Consequently its degree-m regular formal orthogonal polynomial is uniquely T_m. This is exactly PP20's setup, with source n=m, source moments mu_j, and source Delta_(m-1) equal to this shifted Hankel determinant.

After extending the functional arbitrarily beyond the supplied moments if needed, the theorem only uses the displayed finite range. Its quadrature agrees through degree 2m-1. The corresponding transfer function at infinity is R(z)/T_m(z). A state dimension below m is impossible: for any d-dimensional realization mu_j=w* S^j v, its m by m Hankel matrix factors through dimension d. Hence the generic minimal realization dimension is m.

This is a full match of the finite moment machinery. It is not a full match of the legal resolvent theorem:

1. A generic matrix realization allows Jordan blocks. Generalized quadrature allows derivative weights at repeated roots. A sum of ordinary scalar resolvents has neither freedom.
2. Generic quadrature imposes no exclusion of zero or Nth-root-of-unity nodes. Here zero is harmlessly excluded by T(0)!=0, but the cycle roots are essential forbidden points.
3. A nonzero c_s implies a nonzero a_s only after both lambda_s!=0 and lambda_s^N!=1 are checked.
4. Generic state dimension m is not a theorem that m legal branches exist. The precise guard is squarefreeness and coprimality with z^N-1.

A concrete separation occurs already at N=3. Let q be primitive cubic. Then

    mu_0=mu_1=q^2,  T_1(z)=z-1,
    U_*(t)=q^2/(1-t),
    F_*(t)=1+q^2 t/(1-t),
    delta=1-q^2.

This is a legitimate one-state realization and simple-node quadrature with lambda=1. But I-P is singular, so it cannot be a legal one-resolvent bank. The accepted minimum is two. The generic-realization conclusion and the legal-cycle conclusion therefore cannot be identified without the extra guard.

Conversely, when T is simple and avoids the forbidden set, ordinary quadrature yields the legal bank by the displayed conversion. Rank m prevents a vanishing residue, since otherwise fewer than m exponential terms would generate the shifted moments. The accepted fallback gives the upper value m+1 when a guard fails. The finite certificates and uniform resonance theorem remain the specific inputs that select the two cases in this record.

## 6. Additional LS87 scope check

The retained scan's printed pp.333-338 were inspected beyond the denominator formula. The rational-q portion of Theorem 2.1 concerns asymptotic sup-norm growth; the principal convergence and zero-distribution statements impose irrational angle hypotheses or concern asymptotic distributions. Theorem 2.6 gives zero-free regions and an annular enclosure, without a legal-cycle branch-count theorem.

Printed p.346, Lemma 4.5, gives G_(kN+l)(z;q)=(1+z^N)^k G_l(z;q). At the present degree m<N, its substitution has k=0 and l=m; it reduces to the identity G_m=G_m. It cannot by that substitution alone supply the ordinary squarefreeness guard or the cycle-resonance gcd for T_m.

This is a qualified nonmatch to the inspected statements. It is not a claim that all possible implications of LS87 or its citation chain have been exhausted.

## 7. Cost-model comparison

The correspondence concerns exact algebraic objects. It does not transfer a fast application bound merely from the word Padé or from a state-dimension theorem.

The accepted smaller-bank implementation retains the m-dimensional K-algebra E=K[z]/(T), and uses its trace to sum branches without explicitly extracting roots. Ordinary polynomial arithmetic charges O(N^2) K operations for setup and O(N^2) per application, with O(N) retained coefficients. Multiplication by z and applying the retained trace functional each cost O(m); a general quotient multiplication costs O(m^2). The state is not a unit-cost scalar.

The fallback has accepted O(N^3) setup and O(N^2) application. The inspected primary theorem statements supply no same-model operation-count improvement. None supplies bit-complexity, numerical-conditioning, floating-point-stability, explicit-root-in-K, subquadratic-FFT, unrestricted-endpoint, or unrestricted Green-count conclusions.

## 8. Verification and evidence limits

Fresh checks in checks/check_mapping.py use exact polynomial remainders in QQ[q]/Phi_N(q) for N=3,5,7,9,11,13. All six cases passed the two LS substitutions, shifted/full Padé coefficient equations, numerator conversion, reciprocal residue numerator, and both forced-diagonal formulas. These are bounded normalization controls supporting the displayed general derivation. They do not replay any of the 250 saved certificates, re-establish the finite census, or extend the endpoint.

The accepted classification and audit were read as inert text at the pinned repository commit. Their connector snapshots and the bounded live catalogue row are included in sources/. No historical program was executed or imported.

The authorized LS87 scan has SHA-256 034c2af8f6b6696d90d2f744e2932740f9fe1696b3a937b984fd7faca4f39b56. The previously retained page inventory records printed p.360 absent. This pass did not restore it or claim a complete article/citation-chain review. The core mathematical pages required here, pp.332, 340 and 343, were freshly read as images, together with pp.333-338 and 346 for the neighboring statements. The missing bibliography image is not a blocker to the exact theorem substitution just proved.

The source PDF and reading images are not licensed publication assets and are excluded from the proposed public report set. The public derivation cites the DOI and precise page/equation locators.

## 9. Bounded owner disposition

Recommended disposition: COMPLETE_SCOPED_FINITE_SUPPORT, with the recorded exact-comparison obligation satisfied.

- Retain the finite result as supporting data/appendix under F021.
- Attribute the annihilator and forced diagonal as exact classical Padé/q-binomial consequences.
- Retain the legal-cycle restriction, finite accepted certification, and m versus m+1 classification exactly as scoped.
- Keep historical originality and worldwide priority unverified. An exact mapping of ingredients does not show that the complete constrained specialization was published before; a nonmatch to the inspected statements does not show it was not.
- Do not reopen or rerun the accepted finite mathematical gate simply because the general composite question is separate.
- Do not change a priority ranking, owner count, native table, or repository as part of this read-only comparison.

Possible wider historical work would inspect the original sources behind LS87's Padé attribution (Balk, Gragg, Wynn) and the partial-realization antecedents behind PP20 (including Gragg-Lindquist and Draux), plus relevant root-of-unity literature. These were not all independently inspected here. Such a wider priority project requires its own bounded assignment; it is not an unsatisfied obligation of the present finite-support record.

No source-access blocker prevents the requested exact/qualified comparison or this original-scope closure recommendation.

