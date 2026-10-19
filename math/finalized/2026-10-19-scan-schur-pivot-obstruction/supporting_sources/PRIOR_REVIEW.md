# Independent review: sparse tangent reduction and centrosymmetric obstruction

Date: 2026-10-18. Review target: the frozen candidate REPORT.md with SHA-256 `3c2043c73d2c765d88a050e47e9f1487c8b811479c346b8c712d7b8ff0c367ae`.

## Verdict

**ACCEPT SCOPED**, with the original-chart qualification below made explicit. The report supplies two valid uniform results and a precisely stated unresolved endpoint-anchor lemma. It does not prove or refute the original all-dyadic dominance threshold. The allowed terminal outcome is the precise missing minor / dual-uniqueness / size-lifting lemma.

Accepted new claims:

1. At the good inverse-tridiagonal points of Section 2, inversion identifies the tangent of the original separated-generator chart with the full pentadiagonal space. The sparse product Jacobian has exactly the original raw-chart rank, with the stated local redundancies and interstage gauges accounted for.
2. For every dyadic size with odd bit length at least five, the repeated identical centrosymmetric tridiagonal sparse anchor has a nonzero annihilator at every positive depth. In particular, this proves all-depth original-chart deficiency for the concrete anchor `T=3I+L+L^T`, which satisfies every good-anchor hypothesis.
3. The one-endpoint-perturbed family is an explicit regular invertible rational family, breaks the specific centrosymmetric intertwiner, and reduces a possible affirmative solution to the exact unproved endpoint Jacobi–bit-reversal lemma stated in Section 5.

**Qualification to the wording of Theorem 3.2:** the sparse annihilator statement holds for any invertible centrosymmetric tridiagonal `T`. Its final transfer to the *original raw-chart* Jacobian additionally uses the good-anchor hypotheses of Section 2 (nonzero neighbors and nonzero leading/trailing principal minors). Those hypotheses cannot silently be discarded at singular chart representations. The concrete claimed obstruction meets them, so this qualification changes neither that result nor the terminal outcome. This review does not accept an unrestricted transfer at arbitrary degenerate inverse-tridiagonal raw representations.

No corrections to the claimed concrete obstruction, the local tangent theorem, or the precise open endpoint lemma were needed.

## 1. Input integrity and preserved scope

All eleven file sizes and SHA-256 values in candidate MANIFEST.json matched. Its SHA-256 is `ecdd0f915580d7d311f061a426073f668b402f31b5d1853dedb50f29450857c0`. The pinned certificate's Git blob was independently recomputed as `9384b6a4936e16772c8a45290b6a22e88882a4c4`.

The original certificate was read as inert text. The source snapshot of Catalogue!A115:AF115 preserves the later accepted all-size depth-two theorem and its exact scope: dimension `9N−12`, generic raw kernel `N+12`, actual bit reversal at dyadic `N≥8`, and a separately specified transposition at all integer `N≥8`. This review does not rerun those historical or depth-two programs or promote their already accepted scope. The all-size upper bound, original finite certificates and later depth-two acceptance remain intact.

Candidate code was inspected, copied into the review's replay directory, and executed there. No candidate file was modified. No archived or exploratory program was executed or imported. No external write was made.

## 2. Independent mathematical audit

### Original chart and pentadiagonal tangent

On the open set where the upper corner `S[0,N−1]` is nonzero, every upper triangular entry is recovered as

`S[i,j]=S[i,N−1] S[0,j] / S[0,N−1]`, for `i<j`.

For interior indices the relevant 2-by-2 minor belongs to an off-diagonal cut block. Boundary identities are automatic. The lower corner gives the corresponding lower factorization. Thus the cut-rank locus agrees locally with the original separated-generator chart; the upper and lower contributions are independently smooth of dimension `2N−3`, and the diagonal supplies `N` more coordinates.

At a good tridiagonal `T`, the principal-block invertibilities needed for the inverse-block formula hold both at `T` and at `S=T^{-1}`. For the latter they follow from complementary-minor identities. Consequently inversion preserves the upper/lower cut ranks near these points.

At a cut after index `k`, the upper-right block of `T` has its sole nonzero entry in row `k`, column `k+1`. The linearized rank-one equations force precisely those entries with row less than `k` and column greater than `k+1` to vanish. Over all cuts this excludes precisely the entries at distance at least three above the diagonal. The lower equations do the same below it. This gives containment in the pentadiagonal space, and equality follows because both tangent spaces have dimension `5N−6`. This dimension argument is valid at `T` because inversion has transported a smooth local chart; no unproved global smoothness assertion about the full quasiseparable variety is being used.

The six raw redundancies are also valid at the specified nonzero active-generator point: four inactive coordinates and one scaling in each connected lower/upper triangular generator graph. Diagonal interstage gauges stay tridiagonal after inversion, so they remain within the pentadiagonal stage space. Their action is free on invertible tuples. The claimed excess threshold nullity `7N/2−6` over these combined gauges is arithmetically correct.

For distinct stages, differentiating `K=M^{-1}` gives `δK=−K(δM)K` and `X_k=−T_k(δS_k)T_k`. Both tangent changes are invertible in the required spaces. For identical stages, the column formula `A^k E_ij C^(t−1−k)` and the right-normalized adjoint-sum description follow directly from the product order. The transpose in the dual statement is harmless but necessary; the pentadiagonal index set is symmetric under transposition.

### Uniform distance lemma and all-depth annihilator

Write `f_m(i)=i+rev_m(i)`. An odd target forces the endpoint bits to sum to one, giving the displayed recursion by two bits. The middle target `2^m−1` therefore reduces at odd bit length to the impossible value `f_1=1`.

For any bit length `ell≥2`, the two even targets `2^ell` and `2^ell−2` are impossible: endpoint sum zero leaves a maximum of `2^ell−4`, while endpoint sum two gives a minimum of `2^ell+2`. This excludes offsets one from the middle target directly and offsets two after one recursion. The latter argument requires the inner bit length to be at least two, which holds for odd `m≥5`. The explicitly supplied index `2^(m−1)−2` attains distance three. Thus the distance bound is uniform and exact; it is not an extrapolation from samples.

Bit reversal commutes with full reversal, and centrosymmetry gives `CB=BA` for `B=RP`, `A=TP`, `C=PT`. For every depth `t`, `Z^T=C^{−(t−1)}B` is nonzero, indeed invertible. Cyclicity of trace and the intertwiner reduce every stage pairing to `tr(BX)`, which is zero because the support of `B` misses the entire pentadiagonal band. This proves the sparse rank defect at all depths, not merely the threshold. Section 2 then transfers it to the original chart for good anchors.

Why the qualification matters: at `T=I`, one may represent `S=I` with all active lower `a_i=1` and lower `b_j=0`. A derivative in `b_j` then has nonzero entries arbitrarily far below the diagonal. Its inverted variation is not necessarily pentadiagonal. Thus invertibility and centrosymmetry alone do not license the local chart-tangent identification. This does not affect the concrete irreducible positive-definite anchor in the report.

### Endpoint family and exact open obligation

Strict diagonal dominance with positive diagonal proves positive definiteness of the endpoint anchor and every principal submatrix. The continuant inverse, raw generator formula, inactive-coordinate convention and stated height bounds are consistent. Breaking `[R,T]=0` invalidates the particular displayed intertwiner but supplies no general uniqueness theorem; the report correctly makes no such inference.

The missing assertion is exactly full row rank of the explicitly defined integer `H_N` for every dyadic `N≥8` at `t=N/4+1`. Over the rationals this is equivalent to the displayed zero-band observations forcing `Z=0`, because the trace pairing is nondegenerate and the coefficients are rational. No unspecified generic parameter or maximal block-Krylov assumption remains in this candidate lemma.

The size step `t_(2n)=2t_n−1`, the interleaver decomposition of actual bit reversal, and the even/odd block decomposition of `T_(2n)` are exact. The nonzero off-diagonal blocks explain why a copied smaller minor is insufficient. An all-size complementary Schur-block nonvanishing argument, another certified minor construction, or a proof of the stated dual uniqueness remains absent. A counterexample to the endpoint lemma would only reject that family, not original generic dominance.

## 3. Execution and independent controls

Both author programs replayed successfully in `replay/`. The complete first result agrees with candidate RESULTS.json after removing only elapsed_seconds. The second result agrees byte-for-byte with candidate INDEPENDENT_RESULTS.json. The replay reproduces all six stated selected-minor determinants and the raw/sparse ranks at N=8,16,32, as well as all stated transport and mutation checks. The finite-field integer operations are below signed-int64 overflow bounds at these sizes and primes.

The separately written reviewer_checks.py imports no candidate or archived code. It checks:

- Exact Fraction-arithmetic raw-chart tangent transport at nonsymmetric tridiagonal N=4,5,8 anchors, obtaining ranks 14,19,34 and no support outside the pentadiagonal band.
- Exact output-inversion transport of all 60 original raw product derivative columns for three distinct nonsymmetric N=4 anchors.
- The candidate's selected minors, rebuilt from independent prefix/suffix formulas and evaluated with column elimination at the additional prime 104729. Their determinants are 4335, 63963, 35810 for N=8,16,32. The primality of 104729 was also verified by trial division.
- Exact doubling/interleaver identities at total sizes 8,16,32.
- Distance controls for bit lengths 3,4,5,7,9,11,13,15, including the excluded low-bit controls.
- An exact integer intertwiner for a non-Toeplitz centrosymmetric N=32 anchor and explicit modular annihilator observations at depths 1,2,3,9,17.

These finite checks test transcription and implementation. They are not substitutes for either uniform proof, nor evidence that the endpoint uniform lemma has been resolved. No N=64 threshold rank was computed or used.

## 4. Final disposition

M-SCAN-DIMENSION remains TO RESEARCH, priority 34. Accepted scoped progress is the exact sparse-tangent reduction and the concrete all-depth centrosymmetric-anchor obstruction. The endpoint uniform minor / dual-uniqueness size-lifting lemma is the precise blocker. General repeated-bit-reversal dominance, intermediate-depth generic gauge completeness, Fourier membership or construction, coefficient synthesis, runtime improvements and historical priority remain outside the claimed result.
