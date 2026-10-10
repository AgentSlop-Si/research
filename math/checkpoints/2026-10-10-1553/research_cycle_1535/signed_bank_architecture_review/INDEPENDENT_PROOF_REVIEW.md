# Independent proof review: sharp universal signed-bank architecture

10 October 2026. Verdict: **accepted by independent mathematical proof review**. No author or predecessor program was read, imported, executed, compiled, or parsed. This receipt makes no claim of a new computational control run. Author controls, if supplied separately, are supplementary evidence rather than the basis of this all-order proof acceptance.

## Accepted statement and source

For every odd N>=3, every field k with characteristic not dividing N, and every q in k of exact multiplicative order N, let U_k(N;q) be the least number of fixed legal signed-bank parameter/sign slots whose independently variable phase weights span Mat_N(k). Then

U_k(N;q)=2N-2.

An attaining architecture has orientation multiplicities (N-2,1,1,N-2), same-sign nodes q^2,...,q^(N-1), cross-sign singleton nodes 1, and beta=1 in every slot. Its parameters and every target-dependent phase weight lie in k. Every branch guard is -1.

Source: sources/UNIVERSAL_FIXED_BANK_THEOREM.md, SHA-256

c2c30eac3bfcdbd0f7cc2a0c973c56f1821d4326300a1dc1baa2e5f937b273c1

The source is an inert copy of the author theorem. It was read in full. The review is against these bytes only.

## 1. Lower bound is universal and covers all legal strata

For a fixed slot, all dependence of the physical b=1 row on its weights is through one transformed sector amplitude. If delta=-1, that sector has ell=N-1 and vanishes at every nonaxis a because r>=1. If delta=+1, the nonaxis row belongs to a fixed one-dimensional subspace, or to zero in a degenerate case. Universality requires spanning all N-1 independent coordinates, so there must be at least N-1 positive-delta slots.

The physical b=N-1 row gives the disjoint requirement of at least N-1 negative-delta slots. This proves the sum 2N-2. It does not use beta=1, nonzero alpha, distinct nodes, or any special root set. Beta=0, alpha=0, repeated parameters, and possible amplitude cancellations can only preserve or decrease a slot's projected dimension. The projection onto these Weyl coordinates is onto for arbitrary matrices because the Weyl matrices are a basis.

There is no inference about the target-adaptive minimum of one particular Fourier matrix. The required distinction between fixed universality and target-dependent nonlinear node selection is stated correctly.

## 2. Gaussian units at composite order and in positive characteristic

Every nonzero Gaussian coefficient actually divided by has total degree at most N-1. All numerator and denominator factors have the form 1-q^(plus or minus d), with 1<=d<=N-1. Exact order N, rather than primality of N, makes each nonzero. Since k is a field, they are units.

The usual degree-N q-binomial collapse remains valid: mixed coefficients have the zero factor 1-q^N and nonzero lower denominators. Hence X_j^N=(alpha^N+beta^N)I. For the chosen parameters alpha^N=beta^N=1, the inverse guard is 1-1-1=-1. It is nonzero in every field, including characteristic two. The proof never excludes alpha^N=1 or -1 by mistake.

Primitive q implies the listed nodes q^2,...,q^(N-1) are distinct and nonzero. All required Vandermonde determinants are nonzero. No extension field, generic-node existence argument, root extraction, or choice outside k is used.

## 3. The b=0 axis row is complete

The ++ slots supply the distinct coefficient sequences q^(ja) for j=2,...,N-1. The selected -- node q^(N-1) supplies

(q^(N-1))^[−a]_N=q^a

for every a, including a=0. The cross-sign singleton supplies the constant sequence. Thus the assignment covers every character j=0,...,N-1 exactly once for this solve. The finite Fourier inversion has its stated factor 1/N, which exists because char(k) does not divide N. Other sector-zero amplitudes can be zero without affecting any other physical row.

## 4. The b=1 edge row is complete, including N=3

The endpoint a=N-1 receives only the -+ singleton among nonzero assigned groups. Its Gaussian factor has local total 2, which is at most N-1 for every N>=3. The chosen y matches the endpoint.

For a=1,...,N-2, the ++ Gaussian factor is nonzero. After subtracting the singleton's contribution, the required N-2 moments have exponents 1,...,N-2. Their square determinant is the ordinary Vandermonde determinant times the product of the nonzero nodes, hence invertible in k.

The opposite-delta +− singleton's sector ell=N-1 affects only a=0. It corrects the residual there without disturbing the matched nonaxis coefficients. The -- amplitudes for this row are zero. At N=3 the moment system is 1-by-1, and this argument still applies; there are no middle rows to check.

## 5. Every middle row has a noninterfering support partition

For 2<=b<=(N-1)/2, the coordinate a*=N-b belongs only to the -+ orientation: its local total is 2b<=N-1; the same-sign totals are N, and the +− total is 2(N-b)>N-1. Its nonzero Gaussian factor determines the singleton y.

The ++ group covers a=0,...,N-b-1. Its N-b prescribed moments, starting at zero, fit into N-2 available nodes because b>=2. The -- group covers the other nonaxis coordinates a=N-b+1,...,N-1. Their local exponents are r=1,...,b-1; including Q_0=0 makes b consecutive moments, again no more than N-2. Both systems are legal Vandermonde solves.

Away from the axis, the two same-sign supports are disjoint and omit only a*. The singleton contribution is subtracted in each residual. At a=0 all Gaussian factors equal 1; Q_0=0 suppresses the -- contribution, the +− singleton is zero, and the ++ zero moment accounts for the remaining residual. This verifies every coordinate of every middle row, not just the interior.

## 6. Reflection is valid for arbitrary targets

The map (a,b,epsilon,delta) to (-a,-b,-epsilon,-delta) preserves the local r,ell and the Gaussian parameter q^(epsilon delta). The paired same-sign node sets agree, and the cross-sign nodes are both 1. Thus applying a lower-half recipe to the explicitly reflected target row and swapping orientations produces the desired upper-half row.

No symmetry of A is assumed. Reflection is used only to describe coefficients for the actual allowed banks. It is not a free pre/post transformation or an additional synthesis operation.

## 7. Global sector compatibility and literal bank reconstruction

For any one slot, b maps bijectively to ell=[delta b]_N. Therefore all N physical rows assign different amplitudes in that slot, and no later row overwrites an earlier condition. The proof has specified all N(2N-2) sector amplitudes in k.

The raw-weight formula is

w_(i,j)=-sum_ell eta_(i,ell) q^(-epsilon_i delta_i j ell).

Taking its phase Fourier coefficient gives -eta_(i,ell). Dividing by Delta=-1 recovers eta_(i,ell), so the bank's 1/N appears exactly once. The legal finite inverse identity then converts the verified coefficient equations into the original resolvents. As the Weyl matrices are a basis, equality of all N^2 coefficients proves equality of all original matrix entries.

## 8. Consequences and publication meaning

The theorem improves the universal upper bound from 4N to 2N-2 for all odd orders and is sharp for fixed universal architectures. In particular M_k(N;q)<=2N-2. Over C the accepted Fourier lower bound can now be paired with this improved upper bound. This says nothing about exact Fourier minima at N>=9. At N=11 it gives twenty banks; the already accepted Fourier-specific fourteen-bank construction remains stronger.

The full linear weight map has N(2N-2) inputs and rank N^2, hence kernel dimension N^2-2N. That identity is a correct algebraic resource statement. It neither compresses an arbitrary N-by-N matrix's information content nor bounds runtime.

This materially strengthens the publication framing: one can ask a natural target-independent universality question, answer it exactly for all odd orders over all eligible fields, and then investigate how a canonical Fourier target admits fewer banks when parameters adapt to it. It supplies a general-order theorem and a meaningful distinction between a fixed architecture and special-target rank. Its proof is elementary support/Vandermonde algebra; publication significance and historical originality still require independent literature judgment. No inspected scroll secant theorem automatically supplies this fixed-architecture optimum.

## Excluded claims

- M_k(N;q)=2N-2 for the Fourier target.
- A lower bound of 2N-2 for a target-adaptive decomposition.
- An arithmetic, stability, conditioning, bit-complexity, or FFT-speedup result.
- A claim that the supplied mathematical programs were executed in this review.
- Historical novelty, public priority, or acceptance of future edited bytes.

No mathematical blocker was found within the stated scope.
