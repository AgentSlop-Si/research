# The regular H-nonzero affine exception satisfies a decic in e

Date: 2026-10-10 UTC. Status: author-checked candidate, requiring independent review.

## Result and exact scope

Only the already accepted fixed-F11 regular H != 0 exception A(b,e) = B(b,e) = 0 is analyzed. Here b = x11, q = x41, e = x83, and the accepted E41 identity is A q + B = 0. The field is K = Q[zeta]/Phi11, and the argument remains valid over every field extension of K.

Every solution of this exception satisfies the explicit, monic, degree-10 polynomial condition F10(e) = 0. Its eleven exact K-coefficient vectors are in CANDIDATE.json, under polynomials.F10. This is a necessary condition, not a sufficient condition and not an infeasibility proof.

The candidate gives the following exhaustive refinement of the accepted exception:

- F10(e) != 0: excluded.
- F10(e) = 0: retained, with the original inputs (b,q,e), all original and accepted equations, all guards, the original reconstruction order, and every denominator exclusion unchanged.

The A != 0 piece, H = 0 chart, and all other charts are outside this task. No rank, dimension, existence, novelty, Fourier factorization, or global no-solution assertion is made.

## Accepted inputs and preservation

The accepted coefficient split is research_cycle_2304/regular_hnonzero_analysis/CANDIDATE.json, SHA-256 6f10377ef9be102175f559e20e67c928eb88ca1f1868baafe62c4678ce3da8fa. Its independent receipt is research_cycle_2310/hnonzero_continuation_review/RECEIPT.json, SHA-256 22e0babbd1d637a38a355bed333317fb1f38c98057403715374fcdd066880d9e.

The new certificate copies the accepted E41_A_zero branch verbatim, including its full retained regular H-nonzero branch. Thus all 50 original residual equations, all 19 original guards, the accepted extra equations and guards, and H != 0, d != 0, M != 0 remain mandatory. In particular q != 0 is retained; q is never fixed, solved for, canceled, or replaced by a sample value.

The entire accepted rational-coordinate cancellation ledger, E41 denominator and quotient, c denominator, and c-clearing exponent are copied verbatim. The old conditions protecting b, e, D25, q, a, A35, B35, d, M, the x39 denominator and all earlier canceled factors remain in force. Accepted historical reductions are the trust boundary; they are not re-proved or changed here.

To avoid overloading notation, A35 denotes the accepted E35 coefficient named F_A in the atlas. It is distinct from the affine E41 coefficient A analyzed here.

## 1. Remove only an already forbidden common monomial

Exact coefficient comparison gives

    A = b^3 e alpha,
    B = b^3 e beta.

The b-degrees of alpha and beta are respectively 3 and 2; both have e-degree 11. Their coefficient vectors are stored in the certificate.

Because b != 0 is an accepted additional guard and e != 0 is the original x83 guard, A = B = 0 is equivalent to alpha = beta = 0 on this chart. The b = 0 and e = 0 cases are not silently lost: both were already explicitly excluded by the copied chart. No other common factor is canceled from these equations.

## 2. Division-free elimination in b

Let R(e) = Res_b(alpha,beta). Direct exact evaluation of the 5-by-5 Sylvester determinant yields a nonzero polynomial of degree 53. The checker forms this determinant by addition and multiplication only, without dividing by any leading coefficient.

If alpha(b,e) = beta(b,e) = 0 for a finite b, the Sylvester matrix annihilates the nonzero evaluation vector (b^4,b^3,b^2,b,1), with rows corresponding to b alpha, alpha, b^2 beta, b beta, beta. Therefore R(e) = 0 even at specializations where a leading coefficient vanishes. No degree-stability assumption is used.

The following polynomial identity is checked coefficient by coefficient:

    R = u H^9 D25^4 L0 L1 L2^4 L3^4 L5^2 F10.

Here u is an explicitly stored nonzero constant in K; H and D25 are the accepted univariate guard polynomials; the L factors and F10 are monic. The factor labels are their indices in resultant_factorization.factors, with index 4 reserved for F10. Degrees sum to 27 + 4 + 1 + 1 + 4 + 4 + 2 + 10 = 53. No assertion that F10 is irreducible or square-free is needed or made.

H and D25 cannot vanish on the retained chart. Every other factor-zero case is handled next, rather than discarded by a generic resultant argument.

## 3. All five linear-zero cases

Write Li(e) = e - ri. The exact roots, listed in the basis 1,zeta,...,zeta^9, are:

- r0 = zeta^7.
- r1 = (29691 + 41555 zeta + 23630 zeta^2 + 7468 zeta^3 + 8701 zeta^4 + 32856 zeta^5 + 5312 zeta^6 + 16947 zeta^7 + 21196 zeta^8 + 8258 zeta^9)/72887.
- r2 = zeta^3.
- r3 = (-1 + 9 zeta + 8 zeta^2 + 7 zeta^3 + 6 zeta^4 + 5 zeta^5 + 4 zeta^6 + 3 zeta^7 + 2 zeta^8 + zeta^9)/11.
- r5 = (4 + 8 zeta + zeta^2 + 5 zeta^3 - 2 zeta^4 + 2 zeta^5 + 6 zeta^6 - zeta^7 + 3 zeta^8 + 7 zeta^9)/11.

For each i the certificate stores alpha_i(b) = alpha(b,ri), beta_i(b) = beta(b,ri), and exact univariate U_i,V_i,G_i satisfying

    U_i alpha_i + V_i beta_i = G_i.

It also stores exact divisibility identities alpha_i = G_i a_i and beta_i = G_i b_i. These identities identify the specialized common-root condition without assuming that the pre-specialization degrees persist.

For i = 0,2,3,5, G_i = 1. Consequently these four factor-zero cases cannot satisfy alpha = beta = 0. This includes all their leading-coefficient degeneracies.

For i = 1, G_1 is monic of degree one. This case has a common root in the two affine-coefficient equations and must not be ruled out by claiming their gcd is 1. It is excluded by the original guard as follows.

## 4. The remaining linear case violates A35 != 0 for every q

The accepted c reconstruction is c = cn/cd, with cd = b H != 0. The atlas polynomial A35 = F_A is affine in q and has c-degree one. The certificate stores two polynomials J0(b,e),J1(b,e), obtained by exact homogeneous substitution, such that

    cd A35(b,cn/cd,q,e) = J0(b,e) + q J1(b,e).

At e = r1, both coefficients are exactly divisible by G_1(b):

    J0(b,r1) = G_1(b) T0(b),
    J1(b,r1) = G_1(b) T1(b).

Both quotient vectors are stored and checked. Hence alpha = beta = 0 gives G_1 = 0 by the Bezout identity, and then cd A35 = 0 identically for the retained free q. Since cd != 0, this forces A35 = 0, contradicting the copied F_A != 0 guard.

This is an identity in q, not a claim inferred from testing q = 1. Both q coefficients are separately verified. No new q restriction is introduced.

## 5. Consequence and two-way preservation

On the accepted exception, the determinant forces R = 0. H and D25 are nonzero, and the five linear-zero cases have just been excluded with complete exact witnesses. Since u is a nonzero field constant, the factored identity forces F10(e) = 0.

Forward, any accepted exceptional solution therefore belongs to the F10-zero retained piece; no coordinate changes. Reverse, an assignment in that piece still has to pass every unchanged accepted exceptional definition, residual, guard, condition and denominator check. It is thus exactly an accepted exceptional solution. The identity maps in both directions preserve the full guarded residual circuit.

The F10-nonzero case is explicitly excluded, and the F10-zero case remains explicitly open. Algebraic roots of F10 are not presented as feasible points. The argument does not solve the remaining equations or show that this retained piece has a point.

## Exact verification and bounded work

All input artifacts were read as inert JSON. No inherited research program was inspected, imported, or executed. Fresh author scripts derive the common-monomial split, the resultant and factorizations, specialized gcd/Bezout identities, and the guard obstruction. The fresh checker independently re-parses the pinned inputs and verifies a division-free Sylvester determinant, the entire factor product, every specialization and Bezout/divisibility identity, the two free-q coefficient identities, and exact preservation of the accepted branch and cancellation ledger.

The CHECK_RECEIPT.json records semantic negative controls. They include removal of each original residual and guard, each additional condition and reconstruction definition, removal of either F10 branch, unsupported existence/infeasibility/dimension claims, altered coefficients, missing linear-zero cases, corrupted Bezout data, and omission of one free-q guard coefficient. Candidate hashes are not used to make those mutated copies fail.

Reproduce only this fresh checker from the workspace root:

    python research_cycle_2325/f11_affine_exception/check_fresh.py

Exploration of a direct factorization of the large bivariate coefficients and the full degree-53 resultant was stopped after the exact resultant was available. A guarded factor extraction and smaller degree-16 factorization succeeded. The intermediate cubic C1 was subsequently resolved into its linear factors; the final certificate contains all five distinct linear cases directly. No conclusion depends on an incomplete factorization attempt, a numerical root, or a finite-field sample.

The task stops at this necessary decic condition and its guarded exclusions. Independent review is required before acceptance. No Sheet, GitHub, ranking or accepted-artifact changes were made.
