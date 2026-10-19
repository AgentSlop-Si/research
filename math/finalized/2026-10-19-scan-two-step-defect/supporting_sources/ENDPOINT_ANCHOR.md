# M-SCAN-DIMENSION: a uniform sparse-tangent reduction and a precise blocked lift

Date: 18 October 2026. Owner: M-SCAN-DIMENSION. Priority remains 34.

## Verdict

**The all-dyadic threshold is not proved or refuted here.** The terminal result is a precise missing minor lemma for one explicit rational anchor family, together with two proved uniform facts that narrow the route:

1. The original separated-generator Jacobian at inverse-tridiagonal stages is exactly equivalent, by invertible tangent changes, to a product Jacobian with **pentadiagonal variations** at tridiagonal anchors.
2. The tempting identical centrosymmetric tridiagonal anchor cannot work uniformly. At every N=2^m with odd m>=5 it has a nonzero Jacobian annihilator **at every depth**, not just at the threshold. This is a structural failure of that anchor, **not** a counterexample to generic dominance in the original chart.

A one-endpoint perturbation removes that particular symmetry obstruction and gives an explicit, small-height candidate family. Its required all-size minor/size-lift assertion is stated in Section 5 and remains unresolved. No N=64 sample was substituted for that assertion.

## 1. Controlling scope and preserved acceptances

The pinned original certificate is Git blob 9384b6a4936e16772c8a45290b6a22e88882a4c4, preserved in sources/PROOF_CERTIFICATE.md. It uses exactly

S_ij = a_i b_j (i>j), S_ii=d_i, S_ij=c_i e_j (i<j),

with 5N raw scalar coordinates per stage and the actual reversal of all log2(N) binary digits at every boundary. The product is M=S_t P S_(t-1) ... P S_1. The field is characteristic zero, with complex Zariski closure. There is no claim about every exceptional/singular QS1 component or a particular Fourier matrix.

The accepted all-size upper bound is min(N^2,N+t(4N-6)). It excludes dominance below t=N/4+1 for dyadic N>=8. The pinned finite threshold certificates cover N=8,16,32, with all individual stages invertible.

The fresh native read of Catalogue!A115:AF115 is saved in sources/CATALOGUE_ROW_115.json. Its later accepted overlay is preserved: for every dyadic N>=8, depth two with actual bit reversal has dimension 9N-12 and generic raw-chart kernel dimension N+12, exactly the local and interstage gauges. The corresponding all-integer-N>=8 result for its separately specified transposition permutation also remains accepted. We do not replace those accepted depth-two anchors with the special anchors below. In particular, a poor rank at one of our special depth-two anchors would not contradict that theorem.

No historical research program was executed or imported. All computations below use newly written code. No external write is part of this packet.

## 2. Proved inverse-tridiagonal tangent reduction

Let B_2(N) be the vector space of matrices X with X_ij=0 whenever |i-j|>2. Its dimension is 5N-6. Let T be tridiagonal with nonzero neighboring entries, nonzero leading and trailing principal minors, and nonzero determinant. Put S=T^(-1).

### Lemma 2.1: local identification of the original chart

The upper and lower off-diagonal cut blocks of S have rank one. This follows either from the block inverse formula or the tridiagonal inverse recurrence. Moreover the relevant corner and generator entries are nonzero under the assumptions on T.

Near such S, the conditions that every strictly off-diagonal cut block has rank at most one describe exactly the original separated-generator chart. For example, on S_(0,N-1)!=0 the upper entries factor as

S_ij = S_(i,N-1) S_(0,j) / S_(0,N-1), for i<j.

For 0<i<j<N-1 this is one of the cut-block 2x2 minors; the boundary cases hold identically. The lower formula uses S_(N-1,0) in the same way. Thus this is a smooth local chart of dimension N+2(2N-3)=5N-6, not an enlargement to a singular QS variety.

### Lemma 2.2: inversion carries its tangent onto B_2(N)

Inversion preserves the ranks of off-diagonal cut blocks locally: for a block partition with invertible principal blocks, the block inverse formula multiplies an off-diagonal block by invertible matrices. These principal-block invertibilities hold at T and S and hence in a neighborhood.

At a tridiagonal T the upper-right block at cut k has just one nonzero entry, at (k,k+1). Linearizing its 2x2 rank-one minors forces a tangent entry X_ij to vanish if i<k and j>k+1. Taking all cuts gives exactly the upper entries with j-i>=3. The lower blocks similarly force i-j>=3. The remaining constraints have zero or redundant differentials. Hence the tangent is contained in B_2(N).

The original smooth chart at S has dimension 5N-6, and inversion is a local isomorphism. Since dim B_2(N)=5N-6, that containment is equality. In coordinates, X=-T (delta S) T, or delta S=-S X S.

The original 5N raw stage coordinates still have exactly their six local kernel directions at these points: four inactive coordinates and the two lower/upper scaling directions. No generator coordinate has been removed without accounting for it. Across the t-1 boundaries the original N-dimensional diagonal gauges survive; their stage-inverse variations are tridiagonal and hence belong to B_2(N). Their action remains free on invertible tuples. Thus the reduction removes the 6t local redundancies and preserves the (t-1)N interstage gauge directions. If full row rank holds at threshold, the raw kernel has dimension 5Nt-N^2, exceeding the combined gauge dimension 6t+(t-1)N by 7N/2-6. No all-size assertion of below-threshold gauge completeness is inferred.

### Corollary 2.3: an explicit sparse product Jacobian suffices

For possibly different good T_k, let K=M^(-1)=T_1 P ... P T_t. Inversion of the output has differential delta K=-K(delta M)K, an invertible linear map. Each stage tangent under inversion is exactly B_2(N). Therefore the full original raw-chart Jacobian rank equals the rank of the linear map

(X_1,...,X_t) -> sum_k (T_1 P ... T_(k-1) P) X_k (P T_(k+1) ... P T_t), with X_k in B_2(N).

For identical T, write A=TP, C=PT. The matrix of this map, indexed by output (r,s) and input (k,i,j), is

H_N[(r,s),(k,i,j)] = (A^k)_(r,i) (C^(t-1-k))_(j,s),

where 0<=k<t and |i-j|<=2. Thus H_N has N^2 rows and t(5N-6) columns. Equivalently its right-normalized image is the sum of the spaces Ad_A^k(B_2(N) T^(-1)).

This reduction is an exact all-size fact. It does not say that all original regular points arise from inverse-tridiagonal anchors, and failure of this restricted family would not refute original dominance.

## 3. Proved uniform obstruction to the centrosymmetric identical-anchor route

Let R e_i=e_(N-1-i) be full index reversal, let P be actual bit reversal, and put B=RP=PR. Suppose the same invertible tridiagonal T is used in every stage and RT=TR. The concrete example T=3I+L+L^T, with L the subdiagonal shift, satisfies all the good-anchor assumptions and is positive definite.

### Lemma 3.1: the support of RP misses the pentadiagonal band

For N=2^m with odd m>=5,

min_i |N-1-i-rev_m(i)| = 3.

Proof. Let f_m(i)=i+rev_m(i). To obtain an odd target near 2^m-1, the two endpoint bits must sum to one. Removing those bits gives

f_m(i) = 1+2^(m-1)+2 f_(m-2)(i').

The equation f_m=2^m-1 therefore recurses to f_1=1, impossible because f_1 is 0 or 2. For length ell>=2, neither 2^ell nor 2^ell-2 can equal f_ell: these are even, so endpoint bits sum to zero or two; zero makes the inner target larger than its maximum, and two makes it negative. Consequently f_m=2^m-1 +/- 2 would recurse to one of those two impossible inner targets. The targets 2^m-1 +/-1 are impossible by the same even-target argument directly. Thus distances 0,1,2 are excluded. Taking i=2^(m-1)-2, whose m-bit word is 0 followed by m-2 ones and then 0, gives f_m=2^m-4 and distance 3. QED.

In particular tr(BX)=0 for every X in B_2(N).

### Theorem 3.2: rank deficiency at every depth

With A=TP and C=PT, centrosymmetry gives

C B = P T R P = R P T P = B A.

At any integer depth t>=1 define the nonzero functional matrix Z by

Z^T = C^(-(t-1)) B.

It is invertible, so in particular nonzero. For every k and every pentadiagonal X,

tr(Z^T A^k X C^(t-1-k))
= tr(C^(t-1-k) Z^T A^k X)
= tr(C^(-k) B A^k X)
= tr(BX)
= 0.

Thus Z annihilates the entire sparse Jacobian, and therefore also, through the invertible output change, the original raw-chart Jacobian. Its rank is at most N^2-1 for every depth.

This theorem holds for infinitely many dyadic sizes and is not inferred from modular failure. It rules out a simple identical centrosymmetric anchor induction. It says nothing negative about other points of the original image. The accepted N=32 generic full-row minor is fully compatible with it.

## 4. Explicit symmetry-breaking anchors and exact parameter ledger

Define T_N=3I+L+L^T+E_00. It has diagonal (4,3,...,3) and both adjacent diagonals 1. Every principal submatrix is strictly diagonally dominant with positive diagonal, so T_N is positive definite and all needed principal minors and neighboring entries are nonzero.

Define integer continuants

eta_0=1, eta_1=3, eta_k=3 eta_(k-1)-eta_(k-2),
theta_0=1, theta_1=4, theta_k=3 theta_(k-1)-theta_(k-2).

The inverse has, for i<=j,

(S_N)_ij = (-1)^(i+j) theta_i eta_(N-1-j) / theta_N,

and is symmetric. This formula follows by multiplying by T_N and applying the two continuant recurrences, including the first-row boundary condition 4.

One explicit original raw-chart point is

a_i=(-1)^i eta_(N-1-i), b_j=(-1)^j theta_j/theta_N,
c_i=(-1)^i theta_i/theta_N, e_j=(-1)^j eta_(N-1-j),
d_i=theta_i eta_(N-1-i)/theta_N.

Use these formulas only for active coordinates; set a_0=b_(N-1)=c_(N-1)=e_0=0. All active coordinates are nonzero. At every stage use these same 5N parameters. Stage invertibility and exact membership are proved without a modular test.

This perturbation does break the particular obstruction in Section 3: [R,T_N]=[R,E_00] is nonzero, hence C B-B A is nonzero. Breaking one annihilator is not a proof that no other annihilator exists.

Costs and heights:

- theta_k and eta_k are positive, less than 4^(k+1), and have O(N) bits for k<=N. The stated rational generators and diagonals have O(N)-bit numerators and denominators; reduction to lowest terms is optional.
- The recurrences use O(N) constant-coefficient integer operations with total O(N^2) bit work under a direct addition/constant-multiplication implementation. Preparing all diagonal numerator products costs O(N M(N)) additional bit work, where M(N) is an N-bit multiplication bound.
- One shared anchor stores O(N^2) coefficient bits. Copying the full coefficients independently into all t=Theta(N) stages costs O(N^3) bits; sharing identical stages avoids that duplication. Actual permutation preparation costs O(N log N) elementary bit/index work and O(N log N) bits of index storage.
- The ordinary reference execution of t scan stages still costs Theta(N^2) scalar arithmetic, plus coefficient and index work. This is not a Fourier construction or speedup.
- Entries of A^k and C^k have magnitude at most 6^k; entries of H_N have O(t)=O(N) bits. Materializing its O(N^4) entries uses O(N^5) bits. Sparse multiplication can prepare powers in O(t N^2) scalar operations; outer-product column assembly uses O(N^4). A dense finite-field rank check uses O(N^6) field operations and O(N^4) field storage. These are certification costs, not an efficient uniform proof.

## 5. The precise missing minor/induction lemma

**Endpoint Jacobi–bit-reversal lemma (UNPROVED).** For every N=2^m>=8, let t=N/4+1, T_N be exactly the integer matrix in Section 4, and H_N be exactly the integer matrix in Corollary 2.3. Then H_N has row rank N^2 over Q.

There are no unspecified generator choices or generic specializations in this lemma. Its entries are the explicit integer products of powers specified above. An equivalent dual statement is:

If a rational N-by-N matrix Z satisfies that every matrix

(PT_N)^(t-1-k) Z^T (T_N P)^k, for 0<=k<t,

has zero entries in the entire band |i-j|<=2, then Z=0.

Proving the lemma would, by Section 2 and the rational points in Section 4, settle the original all-dyadic threshold affirmatively with invertible original stages. A counterexample to this lemma alone would only reject this anchor family; it would not refute original generic dominance.

For a recursive proof the exact required size step is from n to 2n, with t_(2n)=2 t_n-1. It must produce a nonzero 4n^2-row minor, or prove the displayed dual uniqueness at size 2n, from a proved induction hypothesis; copying a finite minor does not do that. The actual bit reversal obeys

P_(2n)=Q_n diag(P_n,P_n), where Q_n e_(bn+j)=e_(2j+b).

The adjacent coupling in T_(2n) is not block diagonal. In the even/odd coordinate split,

Q_n^T T_(2n) Q_n = [[3I+E_00, I+L_n], [I+L_n^T,3I]].

These are exact identities. The interleaver Q_n and the two off-diagonal blocks prevent simply placing copies of the old minor on a block diagonal. We have no invertible changes producing a certified nonzero complementary Schur block, nor a proof of the dual uniqueness step. **That symmetry-breaking size-lifting/minor step is the precise blocker.** No premise that generic parameters automatically give maximal block-Krylov rank is used.

## 6. Fresh controls and their limited role

Run: OPENBLAS_NUM_THREADS=1 python controls.py. Full output is CONTROLS.log; RESULTS.json records the exact anchor, prime fields, selected columns, determinants, raw-chart ranks, transport checks and mutations. No archived code was executed.

The controls reconstruct both the sparse Jacobian and the full original 5Nt-coordinate Jacobian independently from their respective formulas, verify exact stage membership and every pentadiagonal-to-raw tangent column, and check the same selected minor in two prime fields. They only check the previously certified lengths 8,16,32. They support transcription of the new reduction and candidate; they do not establish the missing all-size lemma.

The selected sparse-minor determinants modulo 12289 and 65537 are respectively (10450,17832) at N=8, (1980,45606) at N=16, and (10459,16976) at N=32. Both sparse and full original raw Jacobian ranks are 64,256,1024. These certify only these fixed finite anchors.

A second implementation, independent_verify.py, imports no candidate code and uses only built-ins and exact Fraction arithmetic. It proves by exact multiplication that the continuant formula is T_N inverse at N=8,16, and independently reconstructs every one of the 120 original raw derivative columns at N=8 by finite differences of the full product. Its separate column-basis algorithm finds rank 64 over both primes. These are independent implementations, not a claim of external mathematical review.

Negative controls replace every boundary by identity, which is rank-deficient at the threshold, and verify the uniform obstruction's intertwining identity exactly over the integers. The endpoint perturbation is also checked to destroy that particular intertwiner. Integer distance controls include odd bit lengths 5,7,9, but the all-size distance claim is proved in Lemma 3.1 rather than inferred from those controls.

## 7. Stop condition and index implications

This packet stops at the allowed terminal **precise missing induction/minor lemma**. The original saturation question remains open; it is neither closed by the controls nor refuted by the special-anchor obstruction. M-SCAN-DIMENSION remains TO RESEARCH, priority 34.

Retain the accepted upper bound, original finite certificates, and later all-size depth-two result. Intermediate-depth generic gauge completeness, fixed Fourier membership, coefficient synthesis, execution savings and historical priority are separate. No automatic progression to another finite length is part of this result.
