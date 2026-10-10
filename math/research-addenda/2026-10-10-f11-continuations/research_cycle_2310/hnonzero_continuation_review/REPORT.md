# Independent review of the regular H-nonzero continuation

Date: 2026-10-10 UTC.

## Verdict and exact scope

PASS. The sealed candidate is an exact, exhaustive, disjoint refinement of the accepted fixed-F11 regular H!=0 residual circuit into:

- A(b,e)!=0: two retained inputs (b,e), q=-B/A, followed by the unchanged accepted reconstruction and every original/accepted predicate.
- A(b,e)=B(b,e)=0: three retained inputs (b,q,e), with the unchanged accepted reconstruction and every original/accepted predicate.

The three-input exception is essential to the accepted statement. It has not been excluded. This is not a global two-input theorem, a dimension computation, an existence or infeasibility result, an unrestricted parameterization, a new fusion, a full Fourier factorization, or a novelty claim. The separate H=0 chart is outside the review. No author or historical research program was inspected, imported, or executed.

The reviewed candidate is `research_cycle_2304/regular_hnonzero_analysis/CANDIDATE.json`, SHA-256 `6f10377ef9be102175f559e20e67c928eb88ca1f1868baafe62c4678ce3da8fa`. The author seal is SHA-256 `b7b0b311515d5e35675566fa5ddb6c0af05dca645b9b13e89fed976442d74ca0`.

## Trust boundary

This review takes the already independently accepted six-chart fixed-F11 atlas, as bound by `research_cycle_2016/three_input_atlas_review/RECEIPT.json`, as its baseline theorem. The baseline's historical reductions and inverse-map proof are not re-proved. Its original guarded residual circuit contains 50 retained residual equations and 19 original guards. The accepted continuation dispatch and its referenced receipts are hash-checked; their historical empty-branch arguments are not rerun, and the new refinement does not require a further empty-branch claim.

Every candidate source pin, every atlas source pin, both atlas prerequisite pins, the accepted atlas receipt binding, the continuation receipt pins, and every author-sealed artifact are checked. Referenced original polynomials are rebound to their compact-JSON SHA-256 content keys before mathematical use. Exact original-coordinate order is (0,11,22,25,34,39,41,44,49,52,55,65,83,88,91,92).

## Independent arithmetic

A new checker was written for this review. It reads inert JSON and hashes source bytes; it contains its own sparse polynomial addition, multiplication, denominator clearing, and coefficient decoding. Arithmetic is over Q[zeta]/Phi11 with rational coefficients using Python `fractions.Fraction`. Every distinct coefficient product is checked twice: cyclic convolution modulo zeta^11-1 followed by elimination of zeta^10, and ordinary polynomial convolution followed by long reduction by the monic Phi11. This is an exact characteristic-zero computation, valid in every extension field of the baseline field. No numeric substitution, finite-field inference, Groebner calculation, resultant, or factorization is used.

The checker verifies the accepted identities

- c_num=b*C1+C0 and c_den=b*H;
- D65=zeta^4*b*q*e*D25;
- D88=q*M*d*x0+K0;
- J=A35*N88+B35*K0;
- x0=-J/(B35*q*M*d);
- N88=-zeta^10;
- D88=-A35*N88/B35 after the accepted x0 reconstruction.

The last facts establish r=x88=-B35/A35 on the accepted regular chart. The original numerator and denominator for r are independently rebound to the displayed atlas polynomials after x22=1 and x49=zeta-c. A35 and B35 here are the accepted E35 coefficients and are distinct from the new E41 coefficients A and B.

## The representative shift is safe

The exact identity for the accepted x92 numerator is checked as

    x92_num = x92_num evaluated at x0=0 - x0*d*(q*a),
    x92_den = q*a.

Thus y=x92+x0*d can be evaluated using the x0=0 representative. Independently, the original x25 numerator is verified to depend on x0 and x92 only through y: substituting x92+x0*d into its x0=0 restriction reconstructs every original coefficient. The original E41 has exactly 22 terms with support {x11,x25,x34,x39,x41,x49,x83}; it contains neither x0 nor d nor x92. The representative does not impose x0=0 on the actual solution.

## All cancellations and nonzero conditions

Five coordinate rows are checked in order: d, y, r, x25, x39. The checker starts from each exact original or accepted numerator/denominator and computes an unsimplified rational pair by common-denominator clearing. For every row, the candidate supplies T and the checker proves both identities

    raw numerator = saved numerator * T,
    raw denominator = saved denominator * T.

It separately proves the same two identities for the original E41, using the already verified reconstructed coordinates. No canceled factor is simply dropped.

These equalities have the following nonvanishing induction on the accepted chart:

1. D65 is nonzero because zeta, b, q, e and the original D25 are nonzero.
2. The y formula uses q*a and already protected d denominators. Both q and a are nonzero by retained/accepted guards.
3. The r formula uses A35, nonzero by the accepted guard. Its equality with the original r formula was checked independently above.
4. The x25 formula uses the original guarded D25 and earlier protected denominators.
5. The original x39 denominator is nonzero by the accepted baseline denominator proof, whose x91 guard and complete reconstruction are retained unchanged.
6. E41 is polynomial in the reconstructed coordinates, so its raw denominator is a product of protected coordinate denominators.
7. In a field, nonzero raw denominator = saved denominator*T implies both saved denominator and T are nonzero. This protects every cancellation, including factors that can otherwise vanish.
8. The later c substitution divides only by b*H, with accepted b!=0 and explicit H!=0. The generic q solve divides only by the explicitly nonzero new A.

This review does not separately re-prove the accepted historical x39 denominator theorem. It does independently prove that the candidate uses the exact original numerator/denominator and preserves every baseline condition required by that theorem.

## Affine-q identity and the zero case

The saved E41 numerator N has 54 terms and multidegree (3,3,1,3) in (b,c,q,e). Its denominator D has four terms and multidegree (1,1,0,2). These claims and the matching diagnostic JSON are verified exactly.

Both c_num and c_den have support only in b,e. Clearing the c substitution by precisely c_den^3 gives

    P = c_den^3 * N(b,c_num/c_den,q,e) = A(b,e)*q+B(b,e).

All coefficients are checked. P has 84 terms, A has 48, and B has 36. Their multidegrees in (b,e) are (6,12) and (5,12). Both coefficient polynomials are formally nonzero; this says nothing about feasible points.

On the guarded chart E41=0 is equivalent to P=0 because all denominators are protected. If A!=0, q=-B/A is forced; direct exact substitution also gives P=0. The proof never divides by the new B. Original q!=0 remains the original hash-bound x41 guard in both branches. In particular A!=0,B=0 produces q=0 and is rejected. If A=0, P=B, so B=0 is mandatory and q remains a retained input. The case A=0,B!=0 is excluded by E41 itself; A=B=0 remains represented.

## Both reconstruction/projection compositions

The active wrapper records generic inputs (x11,x83), q-first evaluation, and the projection back to those same two coordinates. The exception records (x11,x41,x83), no q division, and projection to that same triple. Both wrappers retain exact copies of the accepted branch: all definitions, 50 residual references, 19 guard references, additional equations/guards, and the H!=0,d!=0,M!=0 conditions. The baseline's 13 definitions reconstruct all other coordinates without overwriting any of its three inputs.

For an accepted regular H!=0 solution, the verified E41 identity determines its unique coefficient case. On A!=0, the computed q equals the original q; on A=B=0, it is retained unchanged. The accepted reconstruction/projection theorem then returns the entire original assignment, including actual x0 and x92.

Conversely, a wrapper input must reconstruct with all denominators nonzero and pass every unchanged baseline predicate. Therefore it produces an accepted regular H!=0 solution. Projection returns its original input pair or triple, and the affine identity ensures the generic q solve agrees on the reverse composition. No remaining predicate is assumed to vanish merely because the new affine relation vanishes.

The baseline copy still documents its three-input source chart. It is not confused with the active wrapper's refined input list or projection.

## Negative controls, bounds, and delivery

The fresh checker rejects 117 deliberate semantic corruptions without relying on a candidate-hash gate. They remove the exception, B=0, q!=0 or E41; change q's sign, active inputs, projection or evaluation order; assert unsupported feasibility; corrupt each kind of saved coordinate numerator/denominator/cancellation quotient; corrupt E41, c, P, A or B; change the c-clearing exponent; and perturb each of the 84 A/B terms individually.

Exact counts, timings, source pins, and coefficient cross-check counts are in `ARITHMETIC_RECEIPT.json`. `RECEIPT.json` binds the final checker, arithmetic receipt, log, report, all reviewed author bytes, and source pins. `SEAL.json` freezes the independent review packet. The review is local-only and makes no external writes.

Reproduce from the workspace root:

    python research_cycle_2310/hnonzero_continuation_review/check_independent.py

The stopping point is this bounded coefficient split and its independently checked guarded equivalence. Determining the feasibility of either piece, or excluding the exceptional A=B=0 piece, remains open.
