# Independent-order Schur interface bounds

Date: 10 October 2026. Source checkpoint: v30, “Independent-order Schur-interface gate”.

## Conclusions

The reverse-order rigidity theorem, the necessary LIS correction-rank inequality, the Schur rank factorization, and the stated totally-nonsingular same-branch and invertible-target cross-branch bounds are valid in their direct-coordinate architectures. The strict-upper-triangle minimum completion rank is floor(N/2).

Three qualifications must accompany integration.

1. Total nonsingularity cannot be replaced by “Fourier” without its field and order hypotheses. Composite Fourier is a genuine counterexample to the floor(N/2) bound in arbitrary orders. The source's power-of-two same-branch dimension table is not justified by its theorem.
2. The LIS inequality is necessary, not a complete or sharp characterization for every relative permutation. Shared zero rectangles can force much more rank.
3. Matrix completion and an invertible triangular baseline are distinct assertions. The source conditions its Schur construction on baseline invertibility. An elementary proof below supplies that invertibility for every totally nonsingular target; this is a separately labeled audit addition.

The finite-field examples (N,p)=(9,19),(11,23),(13,53) are not totally nonsingular. Their individual realizations remain valid. The exhaustive full-spark evidence is confined to (5,11) and (7,29).

No exact sub-N-log-N Fourier evaluator, unrestricted arithmetic lower bound, bit-complexity result, or novelty claim follows.

## Provenance and evidence scope

The standalone research text and the archived RESEARCH.md are byte-identical. Their original hashes and the archive hash are in SOURCE_MANIFEST.json. Source programs, bytecode and runners remained inert. The independent mathematical verifiers and certificates distributed here are separate from the source's historical execution claims.

The source-core correction and the all-target completion, singular-pivot extension, composite counterexample and LIS-gap additions have distinct acceptance scopes in PROOF_STATUS.json. The additions are not silently credited to the submitted source.

## Direct coordinate assumptions

A pi-lower matrix means T[i,j]=0 whenever coordinate i precedes j in pi. Both indices refer to the same labeled coordinate set. A DAG denominator is square and invertible, and its inverse is triangular in its topological order.

For a coupled branch system, write

K = [[D,U],[V,H]],     D = diag(A_1,...,A_t),

where the interface comprises q coordinates, H is q by q, and every interbranch matrix entry is zero outside the interface. This is a statement about the complete support of K, including every coupling. It is not justified by inspecting branch graphs alone.

For the two-branch sum the input is duplicated by E=[I;I] and outputs summed by P=[I I]. These specific endpoint maps preserve the baseline A_1^{-1}+A_2^{-1}. Arbitrary dense endpoint maps need not preserve a triangular baseline. For example A=I, E=M, P=I realizes M without any interface, but places the target in E.

A common permutation or gauge of a totally nonsingular target preserves the property. Independent endpoint monomial changes of the target also preserve it, but the actual baseline must still have the specified triangular zero pattern in the coordinates where the proof is applied.

## Reverse order rigidity and its v29 consequence

Suppose every off-diagonal entry of M is nonzero and M=T_pi+T_sigma. If i precedes j in both orders, both summands vanish at (i,j), contradicting density. Every pair must therefore reverse, so sigma is exactly the reverse of pi. This uses density, not total nonsingularity.

When T_pi=A^{-1} and T_sigma=B^{-1}, with A and B invertible triangular denominators, a simultaneous coordinate permutation converts the two orders to a lower/upper pair. The embedded v29 row-gap argument therefore applies when M is totally nonsingular: nnz(A)+nnz(B) >= 2 S_N, with S_N=sum_{i=0}^{N-1} ceil((sqrt(8i+9)-1)/2), hence Omega(N^(3/2)).

This is an explicit denominator-support bound. It becomes a solve-cost exclusion only in a ledger charging literal edge-by-edge substitution. It does not exclude an implicit dense structured solver, arbitrary routing, auxiliary coordinates, a nonsum coupling, or unrestricted circuits. The v30 extension is the reduction from independent direct orders; the v29 support theorem itself should be referenced rather than counted as a new v30 theorem.

## The LIS gate and its limitations

Let rho list sigma-positions in pi-order, and let ell=LIS(rho). If M=T_pi+T_sigma+R is totally nonsingular, choose an increasing chain of ell coordinates. Its earliest m=floor(ell/2) and latest m coordinates form row and column sets I,J. Both triangular summands vanish on I by J, so M[I,J]=R[I,J]. A nonzero m-square determinant implies rank(R)>=m.

Consequently ell<=2 rank(R)+1, the relative permutation has a decreasing subsequence of length at least ceil(N/(2 rank(R)+1)), and it can be partitioned into at most 2 rank(R)+1 decreasing subsequences. These are valid necessary order constraints.

The more general immediate inequality is

rank(R) >= rank(M[I,J])

for every rectangle I by J on which both triangular baselines vanish. For a totally nonsingular target this gives min(|I|,|J|).

This can be strictly stronger than the LIS-chain certificate. With pi=(0,1,2,3), sigma=(1,0,3,2), LIS=2 gives only rank(R)>=1, while rows {0,1} and columns {2,3} force rank(R)>=2. More generally, reverse each of two consecutive half-blocks: LIS remains 2, but a shared half-by-half zero rectangle forces rank(R)>=N/2. Thus “exact interface/order tradeoff” should mean the exact stated necessary inequality, not a sufficient or uniformly tight characterization.

## Schur inverse and interface dimension

If D is invertible, block elimination gives

det(K)=det(D) det(S),     S=H-VD^{-1}U.

Thus invertibility of K is equivalent to invertibility of S. There is no circular step: “K^{-1} exists” and “D^{-1} exists” already imply that the Schur inverse used in the proof exists. Neither H nor the original interface block has to be invertible.

The branch block is

G=D^{-1}+D^{-1}U S^{-1}V D^{-1},

so rank(G-D^{-1})<=q. Multiplication by fixed input/output maps cannot increase this rank. In particular, with duplicated input and summed output, the correction to A_1^{-1}+A_2^{-1} has rank at most q, and q>=floor(LIS(rho)/2).

For a direct same-branch N by N block M, the baseline is triangular. The first floor(N/2) rows and last floor(N/2) columns in its order form a zero rectangle. Total nonsingularity of M therefore gives q>=floor(N/2).

For distinct branches a and b, the inverse block is

G_ab=A_a^{-1}U_a S^{-1}V_b A_b^{-1},

and has rank at most q. A full-rank N by N target forces q>=N, whether or not it is totally nonsingular. This includes composite Fourier transforms whenever their roots and characteristic make the transform invertible. The source's displayed branch-to-interface block -A^{-1}U S^{-1} is N by q; the nontrivial cross-branch interpretation uses two branches as in the formula above.

### Separator formulation without principal invertibility

For an invertible matrix K, partition coordinates U,S,V with K[U,V]=K[V,U]=0. Then rank(K^{-1}[U,V])<=|S|, without assuming K[U,U] or K[V,V] invertible.

For completeness, a nonzero r-square inverse minor with row set I subset U and column set J subset V makes the complementary matrix K[J^c,I^c] nonsingular by Jacobi's identity. Its |U| rows from U have support only in (U minus I) union S, of size |U|-r+|S|. If r>|S| this is impossible. This is the already established separator mechanism, not a new v30 treewidth result.

There is also a one-sided version useful for auditing same-branch pivots. If K=[[A,U],[V,H]] is invertible and A is lower triangular, A itself may be singular. For a nonzero inverse minor using r early branch rows and r late branch columns, the complementary matrix's early branch rows have support only in the remaining early columns and the q interface columns. If r>q, they are dependent. Hence the same-branch zero-rectangle rank bound still holds. This removes the need for an invertible branch pivot in that specific extension, but does not make a nonexistent D^{-1} correction formula valid.

## Sharp completion with a provably invertible baseline

Woerdeman's Theorem 2.2 gives the triangular partial-matrix rank formula over a field and explicitly permits zero-size block dimensions. Its strict-triangular specialization agrees with the source's floor(N/2) evaluation. [Primary paper](https://arxiv.org/pdf/math/0608130).

Here is an independent constructive proof that additionally verifies every baseline pivot. This audit addition applies over any field whenever M is totally nonsingular. All indices below are zero-based; N>=2 and h=floor(N/2).

For k=0,...,h-1 define a row b_k by

b_k[j]=M[k,j] for j>k, and b_k[j]=0 for j<=k.

Set the first h rows of R equal to these b_k. For each i>=h, let d=N-i-1. If d=0, set row i of R to zero. Otherwise define

B=M[0:d, i+1:N],
c=M[i, i+1:N] B^{-1},

where Python-style half-open interval notation is used. B is a d-square minor, so it is invertible. Set row i of R to sum_{k=0}^{d-1} c_k b_k. Since d<=h and k<i, the prescribed tails of the b_k equal the rows of B. This row therefore agrees with M in every column j>i.

All rows of R lie in the span of h rows, so rank(R)<=h. Conversely R[0:h,N-h:N] equals the corresponding totally nonsingular square submatrix of M; therefore rank(R)=h.

T=M-R is lower triangular. Its first h diagonal entries equal M[i,i], which are nonzero. For i>=h and d>0,

T[i,i]=M[i,i]-M[i,i+1:N] B^{-1} M[0:d,i].

The (d+1)-square submatrix with rows (0,...,d-1,i) and columns (i+1,...,N-1,i) has determinant det(B) T[i,i]. Total nonsingularity makes both determinants nonzero, so T[i,i] is nonzero. When d=0 the diagonal is M[i,i]. Thus T is invertible for every such M. For N=1 use R=0 and T=M.

Factoring R=XY with X of size N by h and Y of size h by N, define

A=T^{-1}, U=AX, V=YA, H=I_h+YAX.

Then H-VA^{-1}U=I_h, the whole matrix is invertible, and its top-left inverse block is T+XY=M. This proves universal sharpness within the totally-nonsingular same-branch architecture, not merely existence of some finite examples. Routing and the branch denominator can be dense; no efficient arithmetic evaluator is supplied.

## Fourier and field boundary corrections

For complex prime-order Fourier matrices all square minors are nonzero by Chebotarev's theorem. This implication concerns characteristic zero roots; it cannot be transferred automatically to every finite-field prime-length Fourier matrix. [Frenkel's proof](https://arxiv.org/abs/math/0312398).

Fresh exhaustive checks certify all square minors for N=5 over F_11 and N=7 over F_29, with 251 and 3,431 minors respectively.

Fresh counterexamples show that the remaining source test pairs are not totally nonsingular:

- N=9, p=19, root 4: rows (0,3), columns (0,3) give [[1,1],[1,1]].
- N=11, p=23, root 2: rows (0,1,3), columns (0,2,6) give [[1,1,1],[1,4,18],[1,18,13]], determinant zero modulo 23.
- N=13, p=53, root 10: rows (0,1,3), columns (0,1,5) give [[1,1,1],[1,10,42],[1,46,47]], determinant zero modulo 53.

These roots need not match the source's chosen primitive root: replacing a primitive Nth root by another permutes Fourier columns, preserving whether the matrix is totally nonsingular. The explicit fresh roots are recorded to make each certificate reproducible.

All five individual natural-order sharp constructions were independently reproduced. Those at non-full-spark pairs verify only the particular construction and the minors actually used. They are not general totally-nonsingular controls, nor do they validate arbitrary endpoint changes at those pairs.

### An explicit composite Fourier counterexample

Over the complex numbers take the four-point Fourier matrix with primitive root i, and reorder both coordinates by (0,2,1,3). The result is

M = [[1,1,1,1],
     [1,1,-1,-1],
     [1,-1,i,-i],
     [1,-1,-i,i]].

Let X=(1,-1,-i,0)^T and Y=(0,1,1,1). Then R=XY has rank one, all strict upper entries agree with M, and T=M-R is lower triangular with diagonal (1,2,2i,i). Thus T is invertible. The Schur construction above realizes M with q=1<floor(4/2)=2.

The same certificate reduces modulo 5 with i=2; the fresh control saves the complete 5 by 5 system and verifies its inverse block. The unqualified floor(N/2) statement for arbitrary Fourier orders is therefore false.

The source's results.json and experiment.py list same_branch_min_interface=N/2 for N=16,32,...,65536. These power-of-two Fourier entries are unsupported by the stated total-nonsingular theorem and should be removed, relabeled as hypothetical totally-nonsingular target sizes, or reproved under additional order assumptions. This correction does not assert that every listed numerical value is false in every chosen order.

## Relationship to the accepted v28 audit

The accepted earlier audit establishes complete-extension treewidth at least ceil(N/4)-1 for a totally nonsingular target F=P A^{-1}E, together with the appropriate quadratic-size fixed-minor-free consequence. It also gives an explicit planar complete extension for every target with M=3N^2+2N internal coordinates, maximum degree four, and O(N^2) arithmetic.

Those accepted results remain unchanged. The current audit concerns an additional specified branch/interface decomposition and triangular direct baselines. Its q bounds do not replace the complete-extension graph condition, invalidate the planar construction, or yield a stronger unrestricted arithmetic lower bound. Count the reverse-order reduction, necessary LIS gate, and this precisely scoped interface audit as v30's distinct contribution; cross-reference the already accepted separator and planar results without duplicating their claim identities.

## Independent exact controls and scope

The new controls pass:

- all second orders through N=8, one reverse-order survivor each;
- 3,682 exhaustive finite-field full-spark minors;
- 5,160 full-spark Fourier order/LIS controls;
- five natural-order Fourier rank-completion/Schur realizations;
- Cauchy targets at every N=2,...,40 with rank-minimal completion and invertible baseline;
- 80 independent endpoint-permutation/scaling realizations;
- nine two-branch Schur correction, cross-block, and summed-transfer rank checks;
- exact singular-minor and composite q=1 counterexamples;
- general separator tests, including singular principal branches;
- one-sided triangular same-branch tests, including singular A;
- a shared-zero-rectangle example stronger than the LIS bound.

Additional bit-reversal rank-formula evaluations are retained as exploratory exact data; they are not promoted to invertible-baseline realizations or characteristic-zero theorems.

The source's mathematical claims are accepted with the explicit scope corrections above. The elementary all-target invertible-baseline proof and one-sided pivot-free extension are separately identified additions; their accepted proof scope is recorded in PROOF_STATUS.json. Implementation, unrestricted arithmetic complexity, finite precision, and historical novelty remain unestablished.
