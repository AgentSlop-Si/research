# Primary-source comparison for the routed inverse-branch audit

Checked 2026-10-10. This is a focused structural comparison, not a systematic
novelty search. No verbatim passages are reproduced. All substantive source
claims below come from research papers or their author-hosted versions.

## 0. Direct structural antecedent: biased-graph contraction

Thomas Zaslavsky, *Biased Graphs. IV. Geometrical Realizations*, Journal of
Combinatorial Theory, Series B (2003), Section 2.1, especially the paragraph
immediately before Theorem 2.1 and the theorem's contraction assertion.
[author-hosted PDF](https://people.math.binghamton.edu/zaslav/Tpapers/bg4.pdf).
The inspected author version is dated August 18, 2002, revised December 16,
2005; relevant PDF pages are 8–9 (printed pages 8–9).

The contraction map sends coordinate basis vectors, after switching, to the
coordinate of their balanced component or to zero for unbalanced components.
This is a direct structural antecedent of the audited projective-column
lemma. To see the connection, A=Q^{-1}[S,:] has kernel equal to the span of
Q[:,S^c], so its columns are images of the original coordinate vectors in
the corresponding quotient. The independent-column case gives the tree
components and surviving full-rank unicyclic components used in our proof.
The disjoint-component projective-direction mechanism should be credited as
classical, not described as a newly discovered lemma. The independently
routed sum count against Fourier full-spark rows is a further application;
its priority is not settled by this audit.

## 1. Inverse sparsity and complementary nullity

Raf Vandebril and Marc Van Barel, *A note on the nullity theorem*, Journal of
Computational and Applied Mathematics 189 (2006), 179–190, DOI
[10.1016/j.cam.2005.02.007](https://doi.org/10.1016/j.cam.2005.02.007).
Read the accessible author/institution report, *A short note on the nullity
theorem*, TW397 (July 2004):
[institutional PDF](https://www.cs.kuleuven.be/publicaties/rapporten/tw/TW397.pdf).

Relevant result: complementary submatrices of an invertible matrix and its
inverse have matching nullities, and this controls structured inverse ranks.
The paper derives consequences for banded, semiseparable and related matrices.
It identifies the earlier work of Gustafson and Fiedler–Markham. Their original
publisher pages were not accessible during this audit, so those originals
were not independently read here.

Comparison: the audited proof uses the same general inverse-sparsity-to-rank
principle, but makes a particularly simple direct kernel decomposition after
deleting selected constraint columns from a permutation-cycle superpattern.
The common-refinement count across independently routed summands is an
additional step, not a consequence stated in this source.

## 2. Green matrices and quasiseparable generators

Paola Boito and Yuli Eidelman, *Computation of quasiseparable representations of
Green matrices*, arXiv:2308.02701; published in Linear Algebra and its
Applications 721 (2025), 47–80.
[paper PDF](https://arxiv.org/pdf/2308.02701),
[publisher record](https://www.sciencedirect.com/science/article/pii/S0024379524001976).

Read Section 2, especially Theorem 2.1 (the Asplund theorem), equations
(2.1)–(2.3), and the introduction. It connects a one-sided bandwidth condition
with inverse submatrix-rank bounds and quasiseparable representations.

Comparison: this confirms that rank-structured inverses and small generators
are classical ingredients. The audit's useful invariant is instead a bound
on the number of one-dimensional column classes for an arbitrary selected
row set. Applying that invariant to sums with unrelated endpoint permutations
needs the explicit path-kernel and common-refinement argument given here.
No Fourier branch-count claim was located in the inspected sections.

## 3. Explicit bidiagonal inverse formulas

Nicholas J. Higham, *The Power of Bidiagonal Matrices*, arXiv:2311.06609 (2023).
[paper](https://arxiv.org/abs/2311.06609),
[PDF](https://arxiv.org/pdf/2311.06609).

Read Section 2, Lemma 2.1 and the surrounding formula discussion. The inverse
entries of a nonsingular upper bidiagonal matrix are products of edge factors
and reciprocal diagonal entries. Later results concern products of
bidiagonal factors, perturbation bounds and stable computation.

Comparison: a cut permutation cycle is the graph analogue of a bidiagonal
path. This source explains the nondegenerate product formula background.
The present audit avoids dividing by potentially zero coefficients by using
column independence and path nullity. It handles cyclic closure and independent
endpoint routings without requiring the bidiagonal diagonal to be nonzero.

An additional directly read author-hosted section on inverse-bidiagonal
semiseparability is
[Vandebril, theoretical proof of the structure](https://people.cs.kuleuven.be/~raf.vandebril/homepage/publications/papers_html/trideig/node3.html).
Its proof explicitly uses the lower-triangular semiseparable structure of the
inverse of a lower bidiagonal matrix; it does not discuss the branch-count
obstruction.

## 4. The Fourier full-spark ingredient

Boris Alexeev, Jameson Cahill and Dustin G. Mixon, *Full spark frames*, Journal
of Fourier Analysis and Applications 18 (2012), 1167–1194; arXiv:1110.3548.
[author paper PDF](https://borisalexeev.com/pdf/spark.pdf),
[author publication record](https://borisalexeev.com/papers/spark.html).

The paper explicitly observes that the first M rows of an N-point Fourier
matrix form a Vandermonde matrix with distinct bases and are full spark. It
also warns that general row selections need not have this property, including
a four-point example.

Comparison: this is precisely the complex-field Fourier ingredient in the
audit. The field-general version here follows directly from the same
Vandermonde determinant and the exact-order root assumption. Nothing about
prime N or arbitrary Fourier minors is needed. The paper does not provide
the inverse-branch partition mechanism in the inspected material.

## 5. Fourier bidiagonal products are a different model

Paul D. Gader, *Bidiagonal factorization of Fourier matrices and systolic
algorithms for computing discrete Fourier transforms*, IEEE Transactions on
Acoustics, Speech, and Signal Processing 37(8) (August 1989), 1280 onward.
[author-hosted PDF](https://faculty.eng.ufl.edu/computing-for-life/wp-content/uploads/sites/68/2020/07/Bidiagonal-Factorization-of-Fourier-Matrices-and-Systolic-Algorithms-for-Computing-Discrete-Fourier-Transforms-.pdf).

Read the abstract, introduction, equation (1), and the algorithm discussion.
It gives factorizations using a product of 2N-2 bidiagonal factors and studies
systolic computation. The paper itself distinguishes the resulting arithmetic
count from its regularity and hardware-organization advantages.

Comparison: a **product** of many bidiagonal factors is neither a counterexample
to nor evidence for a fixed-size **sum** of routed inverse-cycle branches.
It also reinforces the need to distinguish a matrix representation parameter
from a universal Fourier arithmetic lower bound.

## Search scope and conclusion

Queries included combinations of inverse cyclic bidiagonal matrices, graph
cycles and inverse nullity, projective column classes, Fourier sums of inverse
bidiagonal matrices, quasiseparable generators and full-spark Fourier rows,
followed by frame-matrix and gain-graph contraction sources. This located a
direct classical antecedent for the componentwise projective-column mechanism,
but no exact match for the independently
routed branch-sum bound N<=r(r+1)^r. Search-engine non-detection cannot establish
novelty. Describe the proof as an elementary restricted-model obstruction
built from classical gain-graph contraction, inverse-rank and Vandermonde
mechanisms unless a broader
literature review establishes more.
