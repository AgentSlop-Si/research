# A safe affine-q refinement of the regular H-nonzero fixed-F11 chart

Status: exact author-side candidate, awaiting independent review. Date: 2026-10-10 UTC.

## Result

The original retained residual E41 supplies an affine equation in q after the accepted regular H!=0 reconstructions:

    A(b,e) q + B(b,e) = 0.

The coefficient vectors are in CANDIDATE.json. No factor is deleted from either coefficient. The cleared polynomial has 84 terms: A has 48, B has 36. Their multidegrees in (b,e) are respectively (6,12) and (5,12). Both are formally nonzero polynomials, which does not assert that either branch contains a feasible point.

This yields an exhaustive, disjoint refinement of the accepted H!=0,d*M!=0 chart:

1. A!=0: retain inputs (b,e), reconstruct q=-B/A, then run every accepted branch definition and test every accepted predicate.
2. A=0: retain inputs (b,q,e), additionally require B=0, then run the same accepted branch definitions and predicates.

The second branch is not excluded. This is a two-input generic piece with a three-input exception, not a global two-input theorem or a dimension statement. The separate H=0 regular chart is unchanged and outside this packet's scope. The accepted empty nonregular branches are not reopened or independently re-proved.

Every piece retains all 50 original residual equations, all 19 original guards, and all accepted additional equations, guards and H!=0,d!=0,M!=0 conditions. In particular q!=0 remains compulsory. If A!=0,B=0, the formula produces q=0 and the original guard rejects that assignment; the proof never divides by B. If A=0,B!=0, E41 itself rejects it. A=B=0 is retained without any new division.

## Trust boundary and input bindings

The target is precisely the accepted fixed-F11 guarded residual circuit over K=Q[zeta]/Phi11, or any field extension of K. The notation is

    x=x0, b=x11, c=x34, q=x41, d=x65, e=x83, r=x88.

The accepted atlas is research_cycle_2014/fused_chart_atlas/CERTIFICATE.json, independently accepted by research_cycle_2016/three_input_atlas_review/RECEIPT.json. The accepted exclusions are recorded in research_review_dispatch_2056/ACCEPTED_F11_CONTINUATIONS.json. Input hashes are recorded in CANDIDATE.json and independently checked by this packet's fresh checker. Earlier accepted historical theorems remain the explicit trust boundary.

Original E41 is bound to content reference

    13e9426f231129cf1288accbfb148f08d3f3a903d5eeaafc56bb665fcb74d6a5.

It has 22 source terms and support {b,x25,c,x39,q,x49,e}. No unverified equation substitution replaces it.

The v38 result rules out nonzero transfer-only identities of total degree at most three on the frozen unrestricted transfer map. This packet does not search for such identities. It works directly with original guarded target-specific edge-coordinate equations, which that result does not exclude. No new cross-theory fusion is used.

## Derivation with a small exact circuit

Write A35=F_A and B35=F_B for the accepted E35 coefficients, to distinguish them from the new A,B above. Accepted identities and guards give

    D88 = q*M*d*x + K0,
    J35 = A35*N88 + B35*K0,
    x = -J35/(B35*q*M*d),
    N88 = -zeta^10,
    A35!=0, B35!=0, q!=0, d!=0, M!=0.

Therefore

    D88 = -A35*N88/B35 != 0,
    r = N88/D88 = -B35/A35.

This is the unchanged atlas r value. The calculation introduces no extra r branch or division by x.

Next use the affine shift

    y = x92 + x*d = -(q*b*t*d+C)/(q*a),
    d = N65/D65.

The original x25 numerator depends on x and x92 only through y. The checker verifies the paired coefficients of every x*d*r term and x92*r term, including those multiplied by e. Hence the representative x=0,x92=y produces exactly the actual x25, without assuming the actual x0 is zero. E41 itself depends on neither x0, d nor x92, so this representative is used nowhere that changes E41.

The original x25 and x39 definitions are evaluated, with x49=zeta-c, using those exact d,y,r expressions. Fresh rational arithmetic gives an exact four-variable identity

    E41 = N(b,c,q,e) / D(b,c,q,e),

where N has 54 terms, multidegree (3,3,1,3), and D has four terms, multidegree (1,1,0,2). The full N and D vectors are stored; no factor is discarded. The reconstructed x25 happens to have no q dependence, as verified in the stored rational expression, but the result does not rely on guessing this property.

The accepted H!=0 formula is

    c = cn/cd,
    cn = b*C1+C0,
    cd = b*H != 0.

Both cn and cd depend only on b,e. The fresh checker verifies their source binding and their absence of c and q support. It forms the polynomial

    P(b,q,e) = cd^3 * N(b, cn/cd, q, e)
              = A(b,e)*q + B(b,e).

The exponent three is the exact c-degree of N. Since c substitution introduces no q, q-affinity survives. The checker verifies every coefficient of this identity by addition and multiplication, without evaluation at sample points. Thus on the accepted chart,

    E41 = P / (cd^3 * D(b,cn/cd,q,e)).

All denominator factors are nonzero as described next. Original E41=0 is consequently equivalent to P=0 within this chart.

## Every rational cancellation remains protected

For each intermediate rational coordinate and E41, the packet stores a polynomial quotient T with both exact identities

    raw_numerator = reduced_numerator * T,
    raw_denominator = reduced_denominator * T.

The fresh checker constructs the raw pair directly from the original source polynomial and the preceding rational expressions, then verifies both identities. It does not infer safety from an unsigned resultant or assume a canceled factor nonzero.

Raw denominators are protected inductively:

- d uses the accepted nonzero D65=zeta^4*b*q*e*D25.
- y uses q*a, with q originally guarded and a accepted globally nonzero, plus denominators already protected for d.
- r uses A35, accepted globally nonzero; its equality with the original r definition is verified above.
- x25 uses the original D25 and protected denominators for y and r.
- x39 uses the accepted original D39 denominator, protected by the original x91 guard and the accepted nonzero field factor.
- E41 is polynomial in these reconstructed coordinates; its raw denominator is a product of their protected denominators.
- c substitution uses b*H, protected by accepted b!=0 and the explicit H!=0 condition.
- The new generic q solve uses A only on the explicit A!=0 piece.

Since each raw denominator is nonzero and equals reduced_denominator*T in a field, neither factor can vanish. The quotient identities therefore preserve every canceled-denominator exclusion. All original guard tests remain present even when a displayed identity makes a guard redundant.

## Forward and reverse maps

Forward, project an accepted regular H!=0 solution onto (b,e) when A!=0, or onto (b,q,e) when A=0. The E41 identity forces q=-B/A in the first case and B=0 in the second. Every denominator is protected by the preceding ledger. The accepted reconstruction then recovers the complete original assignment, including its actual x0 and x92.

Reverse, in the A!=0 piece compute q=-B/A before running the unchanged accepted branch definition order. In the A=0 piece retain q and require B=0. In both cases, test every original and accepted predicate after reconstruction. Such an assignment is therefore an accepted solution of the original H!=0 regular chart. Projection returns precisely the input pair or triple. No new existence or sufficiency claim beyond this residual-circuit equivalence is made.

The copies of retained_branch in CANDIDATE.json are pinned baseline records: their original three-input list documents the source chart. The active refined inputs, q-first execution order, and reverse projection are recorded separately and explicitly in each new branch.

## Verification and bounded attempt

The fresh author checker uses only Python standard-library Fraction arithmetic, sparse polynomial addition and multiplication, and exact reduction modulo Phi11. It imports or executes no historical research script. It verifies the original input hashes, accepted atlas receipt binding, source equations, regular r identity, affine y shift, N25 shift invariance, all rational cancellation quotients, c support, the cleared affine-q identity, the two branches, and exact preservation of every predicate.

All 11 deliberate semantic corruptions are rejected without a candidate-hash gate. They remove the exceptional branch or its compatibility condition, remove an original guard or equation, change the q sign, make an unsupported feasibility claim, corrupt A, corrupt a cancellation quotient, corrupt the E41 numerator or denominator, or change the c-clearing exponent.

Reproduce from the workspace root:

    python research_cycle_2304/regular_hnonzero_analysis/check_fresh.py

Optional fresh derivation from inert source certificates:

    python research_cycle_2304/regular_hnonzero_analysis/explore_e41.py
    python research_cycle_2304/regular_hnonzero_analysis/build_candidate.py
    python research_cycle_2304/regular_hnonzero_analysis/check_fresh.py

The exploration has a 120-second bound, the build a 180-second bound, and the final checker a 240-second bound. The successful final checker ran in roughly two seconds. No Groebner computation, resultant computation, finite-field feasibility inference, numerical root substitution or external write was used.

A first direct three-input rational expansion was stopped because repeatedly simplifying x0 before using the x92+x0*d shift was unnecessarily costly. A tentative numerator-factorization call was also stopped and removed from the successful derivation. No mathematical conclusion depends on either stopped computation. The successful bounded continuation ends at the coefficient split above; no attempt is made here to decide A=B=0 or the remaining residuals.

## Remaining question

Independent review is required before accepting this refinement. After acceptance, the substantive open local question would be whether the explicitly retained A=B=0 exception is empty under the remaining guards and residuals. This packet neither answers that question nor decides the feasibility of the generic two-input piece. It supplies no exact Fourier weights, full-support factorization, generic FFT algorithm, lower bound, asymptotic speed result or novelty claim.
