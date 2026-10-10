# An aligned-cut gate for noncommuting Green resolvents

9 October 2026. This is a specialized corollary of the preceding whole-word quasiseparable inverse and subadditivity audits. It is a restricted representation obstruction, not a universal arithmetic lower bound or novelty claim.

## Why this matters to the fusion

Phase16 recommends exploring sums of noncommuting Green resolvents. Noncommutativity alone does not remove the low-cut-rank obstacle. If all underlying paths retain one common coordinate order, even different path weights, coupling strengths, diagonal masks, and products of sums remain subject to the following budget. Independently reordered paths and shared-state algorithms that are not such operator expressions require separate analysis.

## Inverse cut-rank identity without principal-block assumptions

Let T be any invertible N-by-N matrix over a field. Split coordinates after k, and write X=T^{-1}. Then

rank(X21) = rank(T21),  rank(X12) = rank(T12).

For the first identity, ker X21 consists of vectors u for which X(u,0)=(v,0). Equivalently T21 v=0 and u=T11 v. The map v -> T11 v is a bijection from ker T21 to ker X21: injectivity follows from the invertibility of T, and the displayed equations give surjectivity. Thus the two kernels have the same dimension k, proving equality of ranks. The upper identity follows by the other cut. No invertibility of T11 or T22 is needed.

Consequently, the inverse of an invertible tridiagonal matrix has rank at most one across either side of every aligned contiguous cut. This includes nonsymmetric and noncommuting matrices, singular principal subblocks, and zero couplings. More generally, a bandwidth-b matrix gives cut rank at most b.

## Sums, products, and diagonal masks

For a fixed cut define q_-(A)=rank A21 and q_+(A)=rank A12. The identities

(A+B)21=A21+B21,
(AB)21=A21 B11+A22 B21

imply q_-(A+B), q_-(AB) <= q_-(A)+q_-(B), and likewise above the diagonal. Left/right diagonal multiplication never increases these ranks; diagonal operators have zero off-diagonal cut rank.

Consider an expression made from diagonal operators and resolvents T_j^{-1}, using sums and products. Every T_j is invertible and bandwidth b_j in the same coordinate order. At any cut the expression has off-diagonal rank at most

B = sum of b_j over the resolvent occurrences in the expression tree.

In particular, a sum of r distinct tridiagonal inverses, with independently chosen diagonal masks D_j T_j^{-1} E_j, has cut rank <=r. The matrices need not commute. A product of sums has the sum of their term budgets as a valid bound. For a DAG with repeated subexpressions, this elementary statement counts expanded occurrences; it does not equate that count with an optimal algorithm's running time.

## What exact Fourier requires

For the standard DFT F_N=(omega^{ij}), rows k,...,N-1 and columns 0,...,k-1 form a rectangular Vandermonde matrix on distinct roots. Their rank is min(k,N-k). Thus representing the standard-order DFT by the preceding expression requires

B >= floor(N/2).

This also holds with nonsingular diagonal endpoint scalings. It holds after any common relabeling only when the correspondingly relabeled Fourier cut is known to have this full rank.

With arbitrary endpoint row/column permutations, a uniform weaker conclusion still holds. Any r-by-c submatrix M of the normalized Fourier matrix has ||M||_F^2=rc/N and ||M||_2<=1. Since rank M >= ||M||_F^2/||M||_2^2, its rank is at least ceil(rc/N). Endpoint nonzero diagonal scalings preserve rank. At a balanced cut this yields

B >= ceil(floor(N^2/4)/N).

Therefore a fixed number of common-order noncommuting path resolvents cannot produce an exact Fourier transform up to endpoint monomial factors. Merely exchanging one common-base rational function for a bounded sum of different common-order path inverses is insufficient.

## Scope and next constructive requirement

- The theorem does not exclude independently permuted paths, nonaligned intermediate routing, or arbitrary algorithms that apply the same matrix more efficiently than its displayed expression.
- A term budget is not a runtime lower bound. In particular no Omega(N^2) bound is asserted for a general shared-work implementation.
- An exact candidate must demonstrate how its Fourier cut ranks arise, satisfy the full Fourier coefficient/covariance identities, and give a complete charged evaluator. Passing this rank gate is necessary, never sufficient.
- The proof uses standard block-rank facts. Its use here is a concrete screening criterion for this project's proposed noncommuting-resolvent fusion, with no claim of publication priority.

## Independent finite controls

`check_aligned_resolvents.py` is newly authored. It verifies inverse cut-rank equality, the sum/product budgets for noncommuting tridiagonal matrices, and standard Fourier cut ranks over a field containing exact dyadic roots. It includes the two-by-two swap matrix, whose principal blocks are singular. These finite checks are controls for the proof, not its basis. No uploaded code is executed or imported.
