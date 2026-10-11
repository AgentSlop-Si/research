# E25 continuation on the accepted regular H=0 fixed-F11 chart

## Bounded result

**Author-checked candidate; independent review required.** The second retained original residual chosen here is E25, a 55-term source polynomial. Exact guarded reconstruction and reduction modulo H produce a 54-term polynomial S(e,c,q), of degrees (2,4,3). On the unchanged accepted regular H=0 chart, S=0 is equivalent to original E25=0.

Let P(e,c,q) be the previously accepted 33-term E41 remainder, of degrees (2,3,2). The 5-by-5 Sylvester determinant for eliminating q from P and S is **identically zero modulo H**. This calculation therefore supplies no nontrivial q-free necessary condition. The zero determinant is an obstruction to this particular resultant step; it is not an infeasibility certificate, a feasible point, or evidence that every input works.

Division-free pseudo-division does give a nonzero 60-term linear consequence L1(e,c)q+L0(e,c), with 30 terms in each coefficient and degrees in c at most 9. Thus q=-L0/L1 is valid conditionally where L1 is nonzero. The L1=0 case, including L0=0, must remain. No globally valid elimination of q is established.

The certificate preserves the accepted chart verbatim: all 50 original residuals, all 19 original guards, every extra guard and branch predicate, the polynomial b(e) reconstruction, and every other definition. No optional-zero exclusion is added. All algebraic roots of H, over every field extension of K, remain in scope.

## Trust boundary

Work is over K=Q[zeta]/Phi11(zeta). We use the accepted fixed-F11 regular H=0 chart and the identities accepted in:

- `research_cycle_2303/regular_hzero_analysis/CERTIFICATE.json`, SHA-256 `779b560d09cdf9dc6cae1afe5cd568f267bbf1db545c0639dcc937b4b00f4c2b`;
- its independent receipt `research_cycle_2308/hzero_continuation_review/RECEIPT.json`, SHA-256 `8d9767ba65f61fce39676dadd7b187d520ceb3f770b8f8b4401bfaf6c6b34127`;
- the atlas and predecessor source files pinned by that accepted packet.

Historical programs are not imported or executed. The new programs read inert JSON only. This packet does not reprove the accepted atlas, earlier reconstruction theorems, or earlier exceptional-chart exclusions. It verifies the original E25 source hash, the new exact clearing and remainder calculations, and the elimination identities. The H!=0 chart is untouched.

## 1. Original E25 and denominator clearing

Use b=x11, c=x34, q=x41, e=x83. The accepted polynomial b=B(e) equals -C0(e)/C1(e) on H=0, with C1 nonzero there. We use the latter equivalent expression solely for termwise polynomial denominator clearing; the preserved chart still uses B(e).

The selected original E25 source is content-addressed by:

`ce2413e7d1b9e31c5372467e1d12115510d1385a73052fbb0e9c005b1d7ca841`.

It uses only x11,x22,x25,x34,x39,x41,x49,x65,x83,x88. Make the accepted substitutions

    x22=1, x49=zeta-c,
    x25=N25n/N25d,
    x39=N39/D39,
    x65=Nd/Dd,
    x88=-B35/A35.

N25n,N25d are the accepted prior packet's cleared x25 formula; the other named polynomials are exactly those of the accepted atlas. Each of the four nonunit denominators appears to at most the first power in the original E25. Therefore define

    Den = N25d * D39 * Dd * A35,
    Clear25 = Den * E25(reconstructed coordinates).

The expression on the right is evaluated by monomial-wise polynomial clearing, without rational-function simplification. It has 882 terms and degrees (b,c,q,e)=(10,4,8,6).

Exact polynomial division supplies

    F = q^2 * b * e * D25^2 * a^2 * D39,
    Clear25 = F * Reduced25.

Reduced25 has 204 terms and degrees (6,4,3,3). The full coefficient arrays for Clear25, F and Reduced25 are in DERIVATION.json. The original source polynomial is reconstructed afresh by both new programs.

Every cancelled factor is already nonzero on the accepted chart. q and e are original guards; b and a are accepted additional guards; D25 is an original guard; D39 is the unchanged inherited x39 denominator. Den is likewise nonzero by the unchanged accepted reconstruction. No division by c, x0, x49, or a q-leading coefficient occurs.

## 2. Exact remainder modulo H

Termwise define the polynomial

    T25(c,q,e) = C1(e)^6 * Reduced25(-C0(e)/C1(e),c,q,e).

This notation means polynomial denominator clearing, not unrestricted rational substitution. The packet supplies a 339-term polynomial Q25 and the 54-term S satisfying the exact identity

    T25 = H*Q25 + S,
    deg_e S=2, deg_c S=4, deg_q S=3.

In particular, on H=0,

    E25(reconstructed coordinates) = F*S/(Den*C1^6).

All factors outside S are nonzero or invertible on the accepted chart, so E25=0 if and only if S=0 there. E25 remains an original retained residual regardless of this equivalence. The preceding equalities also apply at every algebraic root of H; no root is assumed to belong to K itself.

## 3. Division-free resultant and zero-resultant caveat

Write

    P=p2*q^2+p1*q+p0,
    S=s3*q^3+s2*q^2+s1*q+s0.

Every pi and si belongs to K[e,c], represented with e-degree below 3. No pi or si is inverted. Form the matrix whose columns are the coefficients of

    q^2*P, q*P, P, q*S, S

in descending rows q^4,q^3,q^2,q,1. This is the transpose of the usual fixed-degree Sylvester matrix for P and S. Its determinant is computed in the quotient ring K[e,c]/(H) by multiplication, addition and reduction modulo H only. This procedure does not assume that H is irreducible or that this quotient is a field.

The determinant is exactly zero. Its evaluation is independently recomputed within this author packet by a subset-DP determinant, using a different expansion order from the derivation's permutation sum. The packet also stores nonzero cofactors giving explicit U,V,QB such that

    U*P + V*S = H*QB.

U has 120 terms and q-degree at most 2; V has 75 terms and q-degree at most 1. This syzygy is checked as a polynomial identity before taking the quotient.

A zero resultant is only a necessary elimination relation, which here reduces to 0=0. It does not assert any solution to all original residuals and guards. Even for an isolated polynomial pair, a fixed-degree determinant can vanish after both leading coefficients drop while the actual lower-degree polynomials have no common affine root. The checker records the simple exact warning example of q+1 and q+2 padded as quadratics: their fixed 4-by-4 determinant is zero, although their gcd is 1. This example illustrates the general caveat, not a purported point of the F11 chart.

## 4. Linear pseudo-remainder and complete conditional cover

With ell=p2, two division-free pseudo-division steps yield coefficient-ring representatives M,Qp,L and an explicit H-multiple:

    M = remainder_H(ell^2),
    M*S - Qp*P - L = H*QH,
    L = L1(e,c)*q + L0(e,c).

L has 60 terms, degree e at most 2, degree c at most 9, and degree q 1. All arrays, including QH, are in ELIMINATION.json. The leading q coefficient ell is never inverted. Before reduction, the usual coefficient formulas are

    L1 = ell^2*s1 - ell*s3*p0 - ell*s2*p1 + s3*p1^2,
    L0 = ell^2*s0 - ell*s2*p0 + s3*p1*p0,

interpreted modulo H. The explicit identity is valid when ell=0 as well.

Every full accepted-chart solution has P=S=0 and therefore L=0. This gives the following exhaustive conditional cover over fields:

1. If L1!=0, reconstruct q=-L0/L1. Every original residual, guard, and reconstruction predicate must still be tested after substitution. This conditional change of coordinates is sound because any full solution satisfies this formula, and any reconstruction satisfying all original predicates is still a full solution by the accepted chart theorem.
2. If L1=0, retain q as an input and require L0=0 together with the entire original chart. No q reconstruction is supplied on this case. No part of it is discarded, and no assertion is made about whether it contains solutions.

The preserved_chart in the machine-readable packet is unchanged; this conditional cover is a proved possible refinement, not a replacement that silently imposes L1!=0. Neither ell=0, s3=0, L1=0, nor any originally allowed optional-coordinate zero is excluded. A nonzero formal polynomial L1 need not be nonzero at a particular solution.

## 5. Checks, files, and limits

- DERIVATION.json: original residual binding, source pins, exact clear/cancel/remainder identities and the verbatim accepted chart.
- ELIMINATION.json: q-coefficient arrays, zero Sylvester determinant, nonzero syzygy, exact pseudo-division identity and claim limits.
- check_certificate.py: fresh author-side verifier, with no historical-code imports.
- CHECKS.json and NEGATIVE_CONTROLS.json: exact-check results and rejected mutations, including every original residual/guard deletion and unproved nonzero restrictions.
- CERTIFICATE.json and AUTHOR_RECEIPT.json: final bounded scope, artifact hashes and status.

Reproduction from the workspace root:

    python research_cycle_2325/f11_zero_resultant/derive.py
    python research_cycle_2325/f11_zero_resultant/eliminate.py
    python research_cycle_2325/f11_zero_resultant/check_certificate.py

Only these newly written programs are run. Polynomial division by H uses its nonzero constant-in-parameters leading coefficient in K. It never inverts a polynomial in e or c. All computations are exact, with no finite-field or numerical feasibility inference.

This packet establishes a second exact residual, a zero-resultant obstruction to this bounded elimination attempt, and a guarded conditional linear consequence. It makes no feasibility, dimension, unrestricted-parameter, novelty, general Fourier-sufficiency, new-fusion, or FFT-improvement claim. Independent review remains necessary.
