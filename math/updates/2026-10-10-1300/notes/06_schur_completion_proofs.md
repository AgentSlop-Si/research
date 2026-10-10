# Independent verification of Schur completion refinements

Date: 10 October 2026.

## Verdict and scope

The four bounded propositions reviewed here are accepted:

1. Every totally nonsingular square target has a completion of its strict upper triangle of minimum rank floor(N/2), with an invertible lower-triangular residual.
2. A shared zero rectangle of two triangular baselines gives a correction-rank obstruction that can be arbitrarily stronger than the stated longest-increasing-subsequence bound.
3. A reordered complex four-point Fourier matrix admits a rank-one correction to an invertible triangular baseline. Consequently a universal floor(N/2) lower bound for arbitrarily reordered composite Fourier matrices is false.
4. The forward-rectangle inverse-rank bound for a triangular branch remains valid when the branch pivot is singular, provided the complete bordered system is invertible. Its proof uses complementary minors rather than an undefined branch inverse.

These conclusions concern exact algebra and the specified direct-coordinate branch/interface architecture. They establish no faster Fourier evaluator, unrestricted arithmetic lower bound, implementation cost bound, numerical-stability claim, or research-priority claim.

The frozen reviewed proof is `PROOF_AUDIT.md`, SHA256 `36c5fc24d92be77d34ae63267cd11a4efb94d6575da588241625e2226e551447`. Its row-tail construction is valid as written. This note also supplies a different block construction, so acceptance does not depend solely on agreement between implementations.

## Definitions and endpoint conditions

All matrices are over a field. A square matrix is totally nonsingular if every square submatrix has nonzero determinant. In particular, all its entries and its determinant are nonzero. A pi-lower-triangular matrix vanishes at (i,j) whenever i precedes j in pi. Both indices refer to the same labeled coordinate set.

Row permutations, column permutations, and nonzero diagonal left/right gauges preserve total nonsingularity: each new square determinant is an old square determinant multiplied by a nonzero product and a permutation sign. However, independent row and column permutations need not preserve a lower-triangular baseline in one common order. Any zero-pattern argument must be applied in coordinates where the actual baseline or branch denominator has that pattern. The independent endpoint controls below transform the target, then construct a new valid triangular baseline in the chosen coordinates; they do not assume arbitrary endpoint maps preserve triangularity.

Arbitrary dense input or output maps fall outside the direct-coordinate hypothesis. Such a map can itself contain the target and erase the intended restriction.

## Minimal completion with invertible residual

Let M be an N by N totally nonsingular matrix, and let h=floor(N/2). For N=1 take R=0 and T=M. Assume N>=2 below. Write I for the first h coordinates, J for the last h coordinates, and B=M[I,J]. Since B is a square minor, it is invertible. Let up(W) denote the strict upper-triangular part of W, with its diagonal and all lower entries set to zero.

### Even size

When N=2h, write X=up(M[I,I]) and Z=up(M[J,J]), and define

R = [[X, B],
     [Z B^{-1} X, Z]].

Equivalently,

R = [B; Z] B^{-1} [X, B].

This is a rank-at-most-h factorization. The I by J block of R is B, so rank(R)=h. Every strict upper-triangular entry of R agrees with M: the two diagonal blocks have the correct strict upper parts, and the entire top-right block is B.

Thus T=M-R is lower triangular. The diagonal of R is zero, so T[i,i]=M[i,i] is nonzero for every i. Consequently T is invertible.

### Odd size

When N=2h+1, let c be the central coordinate, b=M[I,c], e=M[c,J], X=up(M[I,I]), and Z=up(M[J,J]). In block order I,c,J define

R = [B; e; Z] B^{-1} [X, b, B].

Again its rank is h, because its I by J block is B. Its strict upper entries agree with M: the I,I and J,J blocks have the prescribed strict upper parts, while I,c, I,J, and c,J agree exactly.

The residual T=M-R is lower triangular. All diagonal entries except the central one are M[i,i], hence nonzero. The central entry is

T[c,c] = M[c,c] - e B^{-1} b.

For the square minor with ordered rows (I,c) and ordered columns (J,c), block elimination gives

det([[B,b],[e,M[c,c]]]) = det(B) T[c,c].

Its row and column sets have h+1 distinct elements. Total nonsingularity makes the left side and det(B) nonzero. Therefore T[c,c] is nonzero, and T is invertible.

### Minimality

Every completion of the prescribed strict upper triangle has the fixed h by h submatrix M[I,J]. That submatrix is invertible, so every such completion has rank at least h. The constructions above attain h and simultaneously make the residual invertible. The minimum rank is therefore exactly floor(N/2).

The existence of a minimum-rank triangular completion is consistent with the classical partial-matrix formula in [Woerdeman, Theorem 2.2](https://arxiv.org/pdf/math/0608130). The direct proof here separately establishes the residual pivots needed for the Schur realization.

### Verification of the reviewed row-tail construction

The frozen proof uses the first h rows b_k, each equal to the strict upper part of row k of M. For row i>=h put d=N-i-1. When d>0, the d by d matrix B_i=M[0:d,i+1:N] is invertible. The coefficient row M[i,i+1:N] B_i^{-1} makes the completed row match its entire prescribed tail. Since d<=h, all rows remain in the span of the first h rows. The first-h/last-h minor then proves rank exactly h.

Its residual pivot equals

M[i,i] - M[i,i+1:N] B_i^{-1} M[0:d,i].

Multiplying this scalar by det(B_i) gives the determinant with ordered rows (0,...,d-1,i) and columns (i+1,...,N-1,i). These are distinct row and column indices, including at the odd-size central case d=h. Total nonsingularity proves that pivot nonzero. The first h pivots and the final pivot are original nonzero diagonal entries. The N=1 case is handled separately. No diagonal or endpoint gap remains in this proof.

## Schur realization and inverse domain

Suppose R=XY has rank h and T=M-R is the invertible lower-triangular residual just constructed. Set

A=T^{-1}, U=AX, V=YA, H=I_h+YAX,

and K=[[A,U],[V,H]]. Every inverse in this definition exists. Its Schur complement with respect to A is

H - V A^{-1} U = I_h.

Thus K is invertible even if H alone is singular. In fact the full inverse is

K^{-1} = [[T+XY, -X],
          [-Y, I_h]].

Direct multiplication on either side gives the identity. Its top-left block is M. This realizes the sharp interface dimension h. The construction permits dense denominators and dense routing; it supplies no arithmetic efficiency claim.

For N=1, h=0 means the empty interface and K=T^{-1}, with the usual empty-block convention.

## Shared zero rectangles versus the LIS gate

Suppose M=T_pi+T_sigma+R. If every element of a row set I precedes every element of a column set J in both orders, both baselines vanish on I by J. Hence

rank(R) >= rank(R[I,J]) = rank(M[I,J]).

For totally nonsingular M, the last quantity is min(|I|,|J|). This holds for every such rectangle. Choosing the first and last halves of a common increasing chain recovers the lower bound floor(LIS/2), but other rectangles can be stronger.

For N=2m, take pi in natural order and sigma formed by reversing each consecutive half:

sigma=(m-1,...,0,2m-1,...,m).

Its relative-position permutation consists of two decreasing blocks. An increasing subsequence has at most one element per block, and one element from each block is possible, so LIS=2. The first half precedes the last half in both orders. Their shared m by m zero rectangle forces rank(R)>=m, whereas the LIS inequality gives only rank(R)>=1.

For m>=2 this is a strict improvement, and its factor grows without bound. This proves that the LIS inequality is a necessary constraint rather than a complete or uniformly sharp characterization of a relative order. It does not assert that the largest shared-rectangle bound is always the exact minimum completion rank.

## One-sided inverse bound with a singular branch

Let K=[[A,U],[V,H]] be invertible, with A an N by N lower-triangular matrix and H a q by q interface block. A is allowed to be singular. Fix a cut s and let E be the first s branch coordinates and L the remaining branch coordinates. Then

rank(K^{-1}[E,L]) <= q.

To prove it, assume a nonzero r by r inverse minor has rows I contained in E and columns J contained in L. Jacobi's complementary-minor identity implies that K[J^c,I^c] is nonsingular. All s early branch rows remain in this complementary matrix, because J is late. Lower triangularity says these rows can be supported only on the s-r remaining early branch columns and the q interface columns. If r>q, their support has fewer than s columns, forcing dependence. This contradicts nonsingularity of the complementary matrix. Every nonzero minor therefore has order at most q.

If the direct same-branch inverse block M is totally nonsingular, choose s=floor(N/2) and a square subblock of the forward rectangle of that order. It is nonsingular, so q>=floor(N/2), including when A is singular.

Only K^{-1} is used here. The identity with an A^{-1} low-rank correction remains unavailable if A is singular. Likewise, independent endpoint changes require checking the actual triangular zero pattern before applying this extension.

## Exact composite Fourier counterexample

Let i be the complex square root of -1. Start with F[r,c]=i^(rc), and reorder both coordinates by (0,2,1,3). The result is

M = [[1, 1, 1, 1],
     [1, 1, -1, -1],
     [1, -1, i, -i],
     [1, -1, -i, i]].

Take X=(1,-1,-i,0)^T and Y=(0,1,1,1). Then R=XY has rank one and agrees with M at every strict upper entry. The residual is

T = [[1, 0, 0, 0],
     [1, 2, 0, 0],
     [1, -1+i, 2i, 0],
     [1, -1, -i, i]].

Its diagonal is (1,2,2i,i), so det(T)=-4. Applying the explicit Schur construction yields an invertible five by five system with a one-dimensional interface and top-left inverse block M. The complete matrices and exact two-sided inverse certificate are saved in the accompanying JSON.

Thus q=1 is strictly less than floor(4/2)=2. The example disproves the unqualified arbitrary-order composite-Fourier extrapolation. It does not determine the optimal interface dimension at every composite size or in every prescribed order.

## Prime complex Fourier and finite fields

For prime N over the complex numbers, all square Fourier minors are nonzero by [Chebotarev's theorem, as proved by Frenkel](https://arxiv.org/abs/math/0312398). This is the hypothesis needed to apply the totally-nonsingular statements.

Prime transform length alone does not imply total nonsingularity after reduction to an arbitrary finite field. Fresh exhaustive modular controls verify the property for N=5 over F_11 and N=7 over F_29, with 251 and 3,431 nonzero square minors respectively. The certificates use primitive roots 3 and 16, respectively.

Fresh exact zero-minor certificates also verify the following failures:

- N=9 over F_19, root 4: rows (0,3), columns (0,3), determinant 0.
- N=11 over F_23, root 2: rows (0,1,3), columns (0,2,6), determinant 0.
- N=13 over F_53, root 10: rows (0,1,3), columns (0,1,5), determinant 0.

The accompanying verifier checks that each stated root has exact transform order. A successful individual finite-field completion can remain correct at these pairs, but such a success does not establish full-spark hypotheses or arbitrary endpoint universality there.

## Independent control record

No submitted program, bytecode, runner, or first-audit control program was executed or imported. The verifier accompanying this note was newly written from the mathematical formulas. It uses exact rational/Gaussian-rational arithmetic and fresh modular Gaussian elimination. All groups pass:

- Both the block and row-tail completion constructions at rational Cauchy sizes N=1 through 16.
- Thirty independent row/column permutation and nonzero diagonal-gauge targets at sizes N=1 through 10, with both completion constructions.
- Full Schur complements and two-sided inverse identities for the ten ungauged sizes N=1 through 10 and all thirty gauged targets.
- Sixteen reversed-half-block examples at sizes N=2,4,...,32.
- Sixty invertible bordered systems with singular triangular A, checking every forward inverse cut; applicable complementary minors are also checked directly.
- The exact complex N=4 rank-one realization and its full inverse.
- All 3,682 square minors at the two finite-field full-spark pairs, plus three exact zero-minor controls.

The Cauchy entries are M[i,j]=1/(i+N+j+1) over the rationals. Their total nonsingularity follows from the Cauchy determinant formula with distinct row parameters, distinct column parameters, and nonzero pairwise sums; it is not inferred from a sample of minors. Gauges and permutations preserve this property as proved above.

The control results are finite corroborating certificates. The universal conclusions are justified by the proofs in this note. 

## Reproduction

See REPRODUCE.md for the independent verifier under programs/schur_refinement and complete exact certificates under certificates/schur_refinement. The verifier requires Python and SymPy 1.14.0 or a compatible exact-arithmetic version. No submitted program is a dependency. Source and export hashes are recorded separately in SOURCE_MANIFEST.json.
