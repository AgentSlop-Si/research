# The next pivot: one tree plus a growing-rank, small-support correction

## Result

The next literal parity pivot has a fully explicit decomposition into a weighted two-bit tree and one transfer through the preceding one-bit tree. Its correction rank grows, but its image is supported on an explicit coordinate set of size N/32+1 for N>=32. A guarded support-Schur/Woodbury identity therefore reduces this pivot to that many coordinates while preserving arbitrary right inputs and left markers.

The new reduced operator has an O(N)-work formal jet action on a constant input through degree log2 N. Its inverse on the unknown polynomial input is not supplied, and no closed multistage complexity recurrence is claimed. This is additive to the sealed first-Schur report.

## 1. Exact symbolic decomposition

Retain the preceding notation l=N/4 and set k=N/8, for N>=16. The first Schur even block was

    S=I_l-z H_EE-z^2 H_EO D^(-1)H_OE,
    D=I_l-z B_1,
    B_1 e_j=omega^(4j+3)e_(2j+1 mod l).

Restrict S to its odd row and column coordinates. The resulting k-dimensional next pivot is exactly

    Z(z)=I_k-z^2 T-z^3 U(I_l-z B_1)^(-1)V,             (1)

where

    T e_s=omega^(16s+10)e_(4s+2 mod k),
    V e_s=omega^(8s+5)e_(4s+2 mod l),
    U e_j=omega^(8j+6)e_(2j+1 mod k).                   (2)

These formulas follow by applying the odd-row formula of the regularized Haar operator twice. The rank-one root correction is on row zero, so it disappears at this odd restriction. The verifier checks all entries of (1), including the phases, against the independently assembled first Schur block.

The map of T appends the two-bit word 10. It is a functional tree with unique root s_* solving 3s_*=-2 modulo k. Every vertex reaches that root after at most ceil(log2(k)/2) steps. Therefore the reference

    A(z)=I_k-z^2 T

has an O(k)-work guarded tree inverse, with

    lambda_T=omega^(16s_*+10),
    delta(z)=1-z^2 lambda_T.                            (3)

The earlier tree has root denominator

    q(z)=1-z omega^(-1).                                (4)

The reference A is the canonical no-feedback part of the exact decomposition (1). It has not been optimized over all possible tree references.

## 2. Rank bounds and exact reachable rows

For the transfer R(z)=U(I-zB_1)^(-1)V, its constant coefficient is

    UV e_s=omega^(40s+27)e_(8s+5 mod k).                 (5)

Consequently rank(UV)=max(k/8,1). A minor selecting distinct image positions in (5) has a nonzero constant term. Hence over the rational-function field, and generically after specialization,

    rank R(z)>=max(k/8,1).                              (6)

The same generic rank applies to the correction z^3 R(z). Thus its rank is not bounded independently of N relative to the canonical reference A. This says nothing about the optimum over other reference trees.

For a>=0, every column of the a-th transfer coefficient has the explicit formula

    U B_1^a V e_s
      =omega^((48*2^a-8)s+36*2^a-9-a)
         e_(2^(a+3)s+3*2^(a+1)-1 mod k).               (7)

In particular its image lies in the union S_k of the displayed coordinate sets. For k=2, |S_k|=1. For k=2^r>=4,

    |S_k|=k/4+1.                                       (8)

To count: for a=0,...,r-3 the disjoint residue classes have sizes k/2^(a+3), summing to k/4-1. The two additional positions are k/2-1 and k-1; all subsequent powers stay at k-1. Their low-bit patterns distinguish the classes, so this is an exact union count.

Thus rank R<=k/4+1. Exact controls at z=1,2,3 for N=32,64,128,256 attain ranks 2,3,5,9, respectively. The all-size lower bound (6), rather than those finite values, justifies the growing-rank conclusion. No exact all-size generic-rank formula beyond the stated bounds is claimed.

At N=32 the correction lives on two rows, while the explicit tree T contributes the third nontrivial row. This accounts for the previously recorded column with three off-diagonal entries without turning that entry count into a solve-cost lower bound.

## 3. Coordinate-support Schur reduction

Let E inject into the sorted coordinate set S_k, of size r_s. Define

    W(z)=E^T U(I-zB_1)^(-1)V,
    Z=A-z^3 E W,
    R_small(z)=I_(r_s)-z^3 W A^(-1)E.                  (9)

Whenever q, delta, and the needed coupled pivot are nonzero,

    Z^(-1)=A^(-1)+z^3 A^(-1)E R_small^(-1)W A^(-1).   (10)

This is the exact support-Schur/Woodbury identity, not a bounded-rank approximation. The new dimension is r_s=k/4+1=N/32+1 for N>=32. Its determinant satisfies

    det Z=det A * det R_small=delta * det R_small.       (11)

Both q and delta have constant term one. Thus (9)-(11) are valid formally around z=0; pointwise exceptional parameters do not constitute a formal-series obstruction. At a scalar parameter, those chart guards must be respected. For example, the exact N=32, z=2, GF(65537) control has delta=0, so this tree-reference inverse is unavailable there. The report neither divides by it nor declares the formal reduction impossible.

For arbitrary right input b and left marker h, put

    b_small=W A^(-1)b,
    h_small^T=h^T A^(-1)E.

Then

    h^T Z^(-1)b=h^T A^(-1)b
                    +z^3 h_small^T R_small^(-1)b_small. (12)

The markers remain present. Formula (12) holds also when b,h are already formal polynomial vectors; the cost bounds below do not automatically extend to that case.

## 4. Work and representation ledger

Preparing T,U,V and the sorted reachable-row routing costs O(N) arithmetic/addressing from the shared root table. At one scalar z, applying W or R_small to a supplied vector costs O(l+k): the known tree solves in D and A cost O(l) and O(k), and U,V,E are explicit sparse routings with weights. Computing the full dense small matrix by applying all its columns would instead cost O(r_s N), and is not part of the claimed setup.

The representation carries two scalar denominators, q and delta; equivalently, R_small has the shared denominator q*delta of degree three. Root powers, tree orders, and routing are charged. No solve in R_small is treated as one scalar operation.

### A constant-input formal jet

For constant v on S_k, the exact degree-n truncation of the new small operator is

    R_small(z)v = v
       -sum_(a,b>=0, 3+2a+b<=n)
           z^(3+2a+b) E^T U B_1^b V T^a E v.           (13)

The path motifs are a repetitions of 10, then b ones, with the two explicit weighted folds U,V. Generate T^a E v in quotient arrays, then for each a generate the B_1 powers after V. The potential support before B_1 iteration has size at most max(k/(2*4^a),1); after b steps it is at most max(k/(2*4^a*2^b),1). Therefore the aggregate noncollapsed work is bounded by

    sum_(a,b>=0) k/(2*4^a*2^b)=4k/3.

The collapsed root tails and index pairs add O(n^2). Since n^2=O(N), this is O(N) arithmetic and storage for this one constant-input prefix. Each weighted merge is performed explicitly. There is no free polynomial inversion or uncharged evaluation at n different points. Left marked contractions against constant vectors use the same shared program followed by the marker-weighted sum.

The literal ambient workspaces here have dimensions k and l, not merely r_s. A later reduction would need a proof that these carried trees, folds, and coordinate restrictions can be regenerated on proportionally smaller spaces. The current construction does not establish such closure.

### Exact remaining operator state

The new unresolved state is the inverse of

    I-z^3 E^T U(I-zB_1)^(-1)V(I-z^2T)^(-1)E.

Its row selection is the explicit union of dyadic residue classes S_k, rather than the uniform parity interface of the original Haar step. The operator contains two different tree motifs and sparse folds. Its inverse may create arbitrarily repeated packet interactions, and applying it to the carried polynomial inputs is still a separate task. Neither a constant-rank Woodbury argument nor the geometric dimension decrease proves a total-work recurrence by itself.

## 5. Exact independent controls

The authored diagnostic checks 15 cases: N=16,32,64,128,256 and z=1,2,3 over GF(65537). It verifies (1)-(2), the leading transfer formula (5), the reachable-row count and support, and the correction ranks. Fourteen guarded cases check the actual support-reduced solve and the preserved marked bilinear identity; the one delta=0 case is explicitly recorded rather than solved through the forbidden reference inverse.

The constant-input formal prefix is constructed by sparse quotient-state propagation and checked against the corresponding dense tree transitions. All dense inverses and matrix products are small verification oracles only. No uploaded source program was executed.

Files: verify_next_pivot_rank_diagnostic.py, NEXT_PIVOT_RANK_DIAGNOSTIC.json, NEXT_PIVOT_SUPPORT_SHA256SUMS.txt.
