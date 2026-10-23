# Attribution comparison for binary Fourier masks at odd semiprime order

Date: 2026-10-23 UTC.

## Conclusion and scope

The divisor-only cardinality list is already known for Hadamard submatrices of the Fourier matrix and for spectral subsets of the cyclic group of order pq. The primitive two-prime cancellation input is also classical. The primary passages inspected in this bounded comparison did not provide a theorem, or a proved reduction, establishing the full degree-existence classification for arbitrary binary square masks with prescribed Fourier phases. This is a bounded nonmatch report, not a certification of historical novelty.

The exact comparison target is the following accepted statement. Let p<q be distinct odd primes, N=pq, and zeta any primitive complex Nth root of unity. For an N-by-N binary matrix R, define D[r,c]=R[r,c] zeta^(rc). There exists such an R with DD*=dI exactly when d belongs to {0,1,p,q,pq}. Equivalently, every successful mask has one of these degrees, and a witness exists for every listed degree. An arbitrary mask of a listed degree need not succeed.

The statement allows different supports in different rows and imposes neither Cartesian support nor a block decomposition. Because the matrix is square, either scalar Gram identity supplies the other; at d>0 every row and column has degree d. This is not a theorem about free phases, rectangular one-Gram systems, or the classification of every support pattern. The accepted cycle-propagation addendum, its independent acceptance, and the bound compatibility baseline are identified by hashes in SOURCE_BINDINGS.json. Their proof is not re-reviewed here.

## Known result for Fourier Hadamard submatrices

Bond, Glickfield, and Herr, *On the existence of complex Hadamard submatrices of the Fourier matrices* (2019), Theorem 1, gives a necessary condition for an n-by-n Hadamard submatrix of F_m: whenever ell divides m and ell<n, n must be a nonnegative integer combination of the distinct primes dividing m/ell.

Its semiprime specialization is immediate. Put m=pq. If 1<n<=p, ell=1 forces n=p. If p<n<=q, ell=p forces q|n and hence n=q. If q<n<=pq, the choices ell=p and ell=q force both q|n and p|n, hence n=pq. Along with the standard divisor examples and n=1, this gives exactly {1,p,q,pq} for submatrix sizes.

This is a genuine known branch, not new credit. Applying it to an arbitrary square mask would require an additional theorem producing a suitable d-by-d Hadamard submatrix. No such reduction was established in the passages inspected.

Source: [primary PDF indexed by NSF](https://par.nsf.gov/servlets/purl/10088774), Theorem 1; [publication DOI](https://doi.org/10.1515/dema-2019-0001). Retrieval qualification: the indexed primary theorem text was read; direct PDF retrieval was unavailable. This report does not claim that the complete PDF was read.

## Independent spectral set implication

Malikiosis and Kolountzakis, *Fuglede's conjecture on cyclic groups of order p^n q* (2017), Theorem 1.2, proves that a spectral subset of such a group tiles the group. At exponent n=1, its cardinality must therefore divide pq. A Hadamard submatrix F_pq[J,K] with |J|=|K| is a spectral pair and falls within that implication.

The gap to arbitrary masks is exact: spectral-pair orthogonality uses one fixed support K, whereas masked-row orthogonality uses the pair-dependent set S_r intersect S_s. Replacing these intersections by a single common support is not justified by the definition of a successful mask.

Source: [primary paper](https://arxiv.org/pdf/1612.01328), Theorem 1.2 and the spectral-set setup, pp. 2-4.

## Classical cancellation and elementary positive cases

Lam and Leung, *On vanishing sums of roots of unity*, Theorem 3.3 and Corollary 3.4, supply the two-prime nonnegative prime-cycle decomposition and minimal-sum classification. Their text attributes the two-prime structure to de Bruijn. For a primitive row difference, the overlap coefficients are binary; in the pq CRT grid, cycles of the two orientations intersect. Thus a binary overlap decomposes into complete cycles of one orientation only. This is the inherited cancellation input, not the new residual-window argument. De Bruijn's original paper was not separately retrieved in this pass.

Source: [Lam-Leung primary paper](https://arxiv.org/pdf/math/9511209), pp. 7-8.

Herr and Wiegand, *Identifying complex Hadamard submatrices of the Fourier matrices via primitive sets* (2021), Definition 1.1 and Theorem 2.6, concern Cartesian selections J-by-K and their primitive-set compatibility. They do not replace arbitrary entrywise masks by Cartesian selections. The introduction also explicitly records the elementary divisor construction F_d within F_N when d|N. The accepted packet's positive divisor-block masks should remain elementary/inherited constructions, not be credited as newly discovered here.

Source: [primary paper](https://arxiv.org/pdf/1909.13145), pp. 2-3 and 9.

## Why weighing and sparse unitary results are not interchangeable

Best, Kharaghani, and Ramp, *On unit weighing matrices with small weight*, Definition 1 and Theorem 12/Corollary 13, permit arbitrary unimodular nonzero entries. Their weight-three results provide UW(35,3), for example from one order-three block and eight order-four blocks. But degree 3 is excluded by the literal F_35 mask statement. Therefore the unrestricted unit-weighing degree problem is demonstrably a different one. This example does not claim that its phases are 35th roots.

Source: [primary paper](https://arxiv.org/pdf/1209.4581), Definition 1, Theorem 12, and Corollary 13.

Severini, *On the digraph of a unitary matrix*, Lemma 1, gives strong quadrangularity as a necessary condition on unitary supports; Theorem 1 gives sufficiency with an additional specular-pattern hypothesis. These support results do not prescribe the entries zeta^(rc), so they do not themselves supply the target degree classification.

Source: [primary paper](https://arxiv.org/pdf/math/0205187), Lemma 1 and Theorem 1.

The more recent Egan-O Cathain-Svob preprint on complex generalized weighing matrices, Theorem 3.1, assumes bounded matrix order, primitive automorphism rank, and specified orbital-coefficient conditions. Its census theorem is not a universal classification of arbitrary Fourier masks. Its finite search was not executed in this comparison.

Source: [primary preprint](https://arxiv.org/pdf/2607.16069), Theorem 3.1.

## Short comparison for publication

Divisor-only cardinalities for Hadamard submatrices of F_pq already follow from Bond-Glickfield-Herr, Theorem 1, and independently from Malikiosis-Kolountzakis, Theorem 1.2. Two-prime overlap cancellation is classical de Bruijn-Lam-Leung theory. The present statement instead concerns arbitrary binary square masks retaining the Fourier phase at every selected position. Their pair-dependent intersections need not have a common support, so the submatrix results require an additional reduction before they can apply. The accepted proof supplies global row-column compatibility and excludes the remaining window q<d<=q+p-1. This bounded comparison found no direct full-mask implication in the inspected passages; historical priority remains unclaimed.

## Boundaries of the comparison

Searches covered Fourier entry masks and submatrices, unit and complex generalized weighing matrices, vanishing sums, and sparse-unitary zero patterns. Only the relevant retrieved passages were compared; complete reading of every source and exhaustive citation chasing are not claimed. SOURCE_READ_LEDGER.json records the actual access extent, including limited screens not used as direct theorem evidence. No external files or tables were changed, no historical scientific program was run, and no change to the accepted mathematical theorem or full-owner status is proposed. The report is suitable for a scoped attribution note after a separate hypothesis/domain review.
