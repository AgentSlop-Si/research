# Independent review: endpoint-anchor Schur pivot obstruction

Date: 2026-10-19. Owner: M-SCAN-DIMENSION. Priority remains 34.

## Verdict

**ACCEPT SCOPED: the exact local Schur/tangent statements and the specified complementary-pivot rank theorem are valid. The requested all-dyadic endpoint-anchor Jacobian lemma remains unresolved.**

The reviewed frozen candidate is `/workspace/shared/scan_endpoint_20261019_0834/candidate/REPORT.md`, SHA-256 `46968f362319f164f5eb01476d46899b34b9c1593f48a9cd412250f649c355ba`. All six candidate manifest entries and four source bindings were independently verified. No correction to the frozen mathematical statements is required.

This is a proof of failure of one specifically identified block-elimination pivot. It is not a rational Jacobian annihilator, a counterexample to the endpoint anchor, an all-size rank proof, or a counterexample to generic dominance. Consequently it does not satisfy the completion gate in the next-three-tasks proposal. M-SCAN-DIMENSION stays TO RESEARCH.

## 1. Original conventions and field distinctions

The underlying source uses zero-based indices, the subdiagonal shift `L e_i=e_(i+1)` with truncation at the last coordinate, and actual reversal of all binary digits, `P e_i=e_rev(i)`. The anchor in this review is exactly

    T_N=3I+L_N+L_N^T+E_00.

It is not silently replaced by the negative-Laplacian matrix `J_N=−2I+L_N+L_N^T+E_00` over the rationals. The candidate's parity block formula, the orientation of both coupling blocks, the bit-reversal block formula and the sparse Jacobian's product order agree with the original certificate and accepted reduction.

The original rational anchor remains positive definite, with nonzero neighboring entries and every leading/trailing principal-minor guard. These are the hypotheses that allow transfer between the original separated-generator tangent and the pentadiagonal tangent. Invertibility modulo five alone would not supply those guards. In fact a trailing four-by-four block of the original anchor has determinant 55, hence is singular modulo five. The candidate correctly uses modular sparse-matrix calculations without claiming original-chart regularity in characteristic five.

## 2. Independent Schur and tangent audit

In even-then-odd order, `T_(2n)` has diagonal blocks `3I+E_00` and `3I`, and cross blocks `B=I+L_n` and `B^T`. Thus the exact rational Schur complement is

    (7I+4E_00−L_n−L_n^T)/3.

Only after reduction modulo five does this become `3T_n`. Separately, `J_n=−(I−L_n)(I−L_n)^T`, so its determinant is `(-1)^n`, and its parity Schur complement is exactly `J_n/2` in characteristic different from two. Both normalizations are correct and distinct.

For an arbitrary, not necessarily symmetric, pentadiagonal variation, the parity diagonal blocks are tridiagonal and the two cross blocks are lower and upper bidiagonal. Differentiating `A−BD^(−1)C` at `D=3I` gives the candidate's formula. The last term `BX_oo B^T/9` has upper second-diagonal entry `X_oo[i,i+1]/9` and lower second-diagonal entry `X_oo[i+1,i]/9`. These input coordinates are independent. After setting them, all remaining target entries can be supplied by the tridiagonal `X_ee`. The image is therefore exactly `B_2(n)` whenever 3 is invertible.

For the relevant `n≥4`, input and output dimensions are `10n−6` and `5n−6`, respectively, and the kernel dimension is exactly `5n`. This proof makes no symmetry restriction and no product-level inference. The same tangent-surjectivity argument applies to the separate J normalization with its corresponding nonzero odd diagonal; it is not needed to replace the original anchor.

## 3. Independent pivot-rank proof audit

Put `N=4h`, `h=2^q`, `q≥1`. The odd-coordinate block `O=(T_N P_N T_N)[odd,odd]` has size `2h`. With `D=I+L_h`, `F=e_0 e_(h−1)^T`, and `P=P_h`, direct multiplication from the original matrices gives

    O = [[D^T P D+3(F+F^T), 3PD],
         [3D^T P,                 9P]].

This retains both adjacency couplings. The endpoint diagonal perturbation does not enter these odd rows/columns of T, so no argument relies on mistakenly treating it as an odd-sector perturbation.

For `C=[[I,B/3],[0,I]]`, the factorization is `T_par=C diag(S,3I) C^T`. The dressed boundary is `C^T P_par C`. Its lower-right block is exactly `O/9`: the odd rows of `T_par` are `3[B^T/3,I]`, and the odd columns are their transposes. The scaling is valid over Q and F5, but not characteristic three.

Eliminating the invertible `9P` block leaves

    R=P[U,L_h]+3(F+F^T),  U=P L_h^T P.

Outside the monotone binary words `M={x_b=2^b−1:0≤b≤q}`, the first 1 lies before the last 0. Reversed-order decrement and ordinary increment then affect disjoint prefix and suffix regions, preserve each other's stopping bit and avoid truncation. Their commutator vanishes on those basis columns. The endpoint correction has no other columns. Since R is symmetric, its rows are also supported on M.

For completeness, the formula on M can be derived without extrapolating any finite table. If `b<q`, ordinary increment sends `x_b` to `2^b`; reversed decrement sends that to `h−2^(b+1)`, whose reversal is `x_(q−b−1)`. This contribution is absent at `b=q`. If `b≥1`, reversed decrement sends `x_b` to `h−2^(b−1)−1`; ordinary increment and then reversal yield `x_(q−b+1)`. This contribution is absent at `b=0`. Hence

    P[U,L_h] e_(x_b)=e_(x_(q−b−1))−e_(x_(q−b+1)),

with out-of-range terms omitted, including both base-case boundaries.

Reverse the row order in the `(q+1)`-square restriction to M. Its diagonal is 3 at both endpoints and zero inside, with lower neighbors +1 and upper neighbors −1. This is not wholly skew-symmetric, since it includes the two endpoint diagonal entries. Its leading continuants alternate `1,3` until the final step. The full determinant is 6 for even q and 10 for odd q. Therefore

    rank_Q O=h+q+1=N/4+log2(N)−1,
    nullity_Q O=h−q−1.

For `q=1` (`N=8`), this gives full rational rank 4. For `q≥2` (`N≥16`), `h>q+1`, so the nullity is strictly positive. This establishes the claimed boundary of uniform singularity.

Over F5, the rank is `h+q+1` for even q. For odd q the determinant vanishes, but the leading q-square minor is 3, giving rank `h+q` exactly. Thus the rational and mod-five ranks must not be conflated. The stated integer null vectors `(3e_x,−P D^T P e_x)` for `x∉M` form a basis for the rational nullspace, by their independent first blocks and the exact nullity count. They remain independent modulo five; at odd q the modular nullspace has one additional dimension.

The three-entry witness at original indices `5`, `N/2+5`, and `N−7`, with weights `3,−1,−1`, is correct for every dyadic `N≥16`. Its odd output vanishes. Its even output does not vanish, consistently with invertibility of the full product `T_N P_N T_N`.

## 4. Original independent exact controls

The newly written `reviewer_checks.py` imports no candidate or historical research code. The candidate and historical files were read only as inert text. No external writes were made. The script was executed once successfully; `REVIEWER_CHECKS.log` and `REVIEWER_RESULTS.json` contain its complete results.

Checks include:

- Original matrix reconstruction, exact rational Schur formula, mod-five factor 3, and the distinct J factor 1/2, for smaller sizes n=4,8,16.
- Every pentadiagonal input column, all output-basis preimages, exact rational and mod-five differential ranks at n=4,8. At n=4 all 34 input derivatives are also reconstructed independently by scalar Gaussian elimination over dual numbers, rather than using the block derivative formula.
- Direct original `TPT` construction, block identity, dressed-boundary normalization, commutator, support, residual matrix and determinants, direct rational and mod-five elimination, and every stated integer null vector at N=8,16,32,64,128,256. These are auxiliary pivot controls, not threshold-Jacobian scans.
- The resulting rational ranks are 4,7,12,21,38,71; the mod-five ranks are 3,7,11,21,37,71.
- A separate reconstruction of the original 64-by-102 sparse H_8 at depth 3 gives rank 64 modulo 5 and 12289. Meanwhile the dressed odd pivot has rational determinant `−10/81` and rank 3 modulo five. Thus singularity of this auxiliary modular pivot coexists with full rank of the actual H_8, directly guarding the essential scope distinction.

No H_N rank for any N larger than eight was computed in this review. The uniform theorem is proved by the binary and continuant arguments, not inferred from finite checks.

## 5. Disposition and remaining obligation

The exact obstruction applies to the specific procedure that individually decimates the stages and then requires the lower-right block of the dressed boundary to be invertible. That pivot fails. Alternative coordinates, grouped temporal blocks, elimination orders, complementary minors or direct dual-observability arguments are not excluded.

The requested completion remains exactly: prove full row rank of the original H_N at depth `N/4+1` for every dyadic `N≥8`, or produce an actual rational Jacobian annihilator at one such size. Neither is supplied here. Preserve the accepted good-anchor tangent reduction, all-size upper bound and depth-two theorem, finite threshold certificates, owner and priority. No statement on Fourier membership, intermediate-depth gauge completeness, coefficient synthesis or runtime follows.
