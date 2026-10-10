# Final-form matrix theorems and two new strengthenings

Date: 2026-10-10. This is a new working manuscript. Frozen research originals were not changed. “Proved here” describes a mathematical deduction, not worldwide priority or external peer review. All matrices and norms in the analytic results are complex. No conclusion below is a general arithmetic lower bound for the FFT.

## 1. Sharp cyclic-dyadic endpoint rank, with a robust extension

For a square matrix A define

q(A) = max over 1 ≤ k < N of rank A[0:k,k:N] and rank A[k:N,0:k].

Let F_N = (exp(2πiab/N)) be the unnormalized cyclic Fourier matrix and U_N = F_N/√N. Row and column permutations may be independent.

### Theorem 1A: exact minimax (C02, re-exposition)

If N = 2^m ≥ 8, then

min over ρ,σ in S_N of q(P_ρ F_N P_σ^T) = N/4 + 1.

Double bit reversal attains the minimum. The exact rank statement also holds over any characteristic-zero field containing a primitive Nth root: ranks are unchanged on extending its cyclotomic subfield to the complex numbers. This does not assert the lower bound over finite fields.

### Theorem 1B: universal singular-value gap (new deduction)

More generally, let G be any finite abelian 2-group of order N = 4L ≥ 8, and let U be its normalized character table. For every set R of 2L−1 characters and every set H of 2L+1 group elements, set V = U[R,H]. Then

σ_(L+1)(V) ≥ δ_N,

δ_N = sqrt(1 − sqrt(B_L/(L+1))),

B_L = L + 3/4 + 1/(4L) + 1/(16L²) < L+1.

In particular rank(V) ≥ L+1. The number δ_N is positive and asymptotic to (2N)^(-1/2). For every independent endpoint ordering and every matrix M whose upper-right block at k=2L−1 has rank at most L,

||P_ρ U P_σ^T − M||_2 ≥ δ_N.

Thus the lower bound and its robustness extend beyond cyclic groups; a matching upper bound for other abelian 2-groups is not claimed here.

### Proof of the lower bound and gap

Let I be the complement of R in the character set, so |I|=|H|=h=2L+1. On C^H put A = U[I,H]^* U[I,H]. Then 0 ≤ A ≤ I_h and V^*V = I_h−A. Write

c_H(s)=|H∩(H−s)|, and f_I(s)=Σ_(χ∈I) χ(s).

Direct expansion gives

tr(A²) = N^(-2) Σ_(s∈G) c_H(s)|f_I(s)|².

Here c_H(0)=h. Each nonidentity translation in a finite 2-group has even-length orbits. An odd-cardinality H cannot be invariant under it, so c_H(s)≤h−1 for s≠0. Character orthogonality gives Σ_s |f_I(s)|²=Nh and f_I(0)=h. Consequently

tr(A²) ≤ ((h−1)Nh+h²)/N² = B_L.

If a_1≥…≥a_h are the eigenvalues of A, then (L+1)a_(L+1)²≤tr(A²)≤B_L. The descending eigenvalues of V^*V are 1−a_h,…,1−a_1; since h=2L+1,

σ_(L+1)(V)² = 1−a_(L+1) ≥ 1−sqrt(B_L/(L+1)) > 0.

This proves the singular-value claim. A rank-at-most-L matrix cannot approximate V in operator norm more closely than σ_(L+1)(V). One elementary proof is to intersect the span of V's top L+1 right singular vectors with the kernel of that approximating matrix. The intersection contains a unit vector on which the error norm is at least σ_(L+1)(V). Coordinate restriction cannot increase operator norm, giving the full-matrix claim. Expanding the displayed expression gives δ_N~(2N)^(-1/2).

For cyclic G, every endpoint-permuted Fourier matrix has such a block at k=2L−1. This proves the lower half of Theorem 1A.

### Proof of the matching cyclic upper bound

Let b_m reverse m binary digits, let Q_N[i,j]=ω_N^(b_m(i)b_m(j)), and let r_N(k)=rank Q_N[0:k,k:N], including r_N(0)=r_N(N)=0. For N=4L and 0≤k≤2L,

r_N(k)=ceil(k/2)+r_L(floor(k/2)).

To establish this, write the first 2L bit-reversed frequency labels as 2q_i, where

q_(2j)=b_(m−2)(j),  q_(2j+1)=L+b_(m−2)(j).

The k selected rows contain p=floor(k/2) complete pairs and, if k is odd, one additional row. All odd natural-time columns remain on the right. Their evaluations span a space of dimension ceil(k/2): paired rows have opposite signs, and after removing their nonzero phases the distinct residues modulo L form complete rows of F_L. A quotient by this span is given by summing each complete row pair. There are p quotient coordinates.

Every remaining even column 2ℓ maps in the quotient to a nonzero common scalar times (ω_L^(qℓ)) over those p pair residues. The selected paired residues are b_(m−2)(0),…,b_(m−2)(p−1). The remaining column residues contain exactly the suffix beginning at b_(m−2)(p). This remains true at an odd cut: the second member of the partly removed even-column pair survives, so its residue must not be dropped. Repeated columns do not change rank. The quotient rank is therefore r_L(p), proving the recurrence.

Because b_m(N−1−i)=N−1−b_m(i), simultaneous reversal of row and column positions changes Q_N only by invertible diagonal scales. Symmetry therefore gives r_N(k)=r_N(N−k). For k=2a≤2L, the recurrence and r_L(a)≤L−a give r_N(k)≤L. For k=2a+1<2L they give r_N(k)≤L+1. At k=2L−1, r_L(L−1)=1, since L≥2 and Fourier entries are nonzero, so r_N(k)=L+1. The base orders 1 and 2 are immediate. Symmetry equates the upper and lower cut ranks. This completes Theorem 1A.

### Corollary 1C: charged common-order products and scaling

For every same-order product A_s⋯A_1, q(A_s⋯A_1)≤Σ_j q(A_j). Indeed at each cut (AB)_12=A_11B_12+A_12B_22, and similarly for the lower block. Thus any exact dyadic Fourier factorization

P_ρ F_N P_σ^T = S_s P_(s−1) S_(s−1)⋯P_1 S_1

must satisfy Σ_j q(S_j)+Σ_j q(P_j)≥L+1 when all ranks are measured in this displayed common coordinate order. If the same sum is at most L, approximation to the normalized target has operator error at least δ_N. Arbitrary interstage permutations cannot be discarded from this budget.

If the target is D(P_ρ U_N P_σ^T)E, with invertible diagonal D,E, then the error threshold becomes d_min e_min δ_N, where d_min=min_i|D_ii| and e_min=min_j|E_jj|. Multiplying an approximant by D^(-1),E^(-1) preserves all cut ranks and multiplies its error by at most 1/(d_min e_min). A condition number alone does not set an absolute scale: scalar rescaling of the entire target must still be specified.

The exact minimax is supported by the inherited complete proof. The universal error-gap corollary and abelian-2-group lower extension are new deductions in this finalization, not certified publication novelties. The bit-reversal low-rank hierarchy itself is established prior art; see PRIOR_ART_AND_NEXTCHECKS.md.

## 2. Stronger independently routed separator obstruction

The following replaces the previous factor 36^r by 9^r and also improves the leading constants. The structural family is unchanged.

A matrix L has permutation-contained support if some permutation p satisfies L[a,p(a)]=ℓ_a and all other entries vanish; ℓ_a may be zero. Right endpoints are defined similarly. Different branches may use entirely different permutations and weights.

For invertible Q∈C^(N×N), its symmetric bipartite support lift is the support graph of

H_Q = [[0,Q],[Q^T,0]].

Say this graph has weighted half-separators of size q if every nonnegative vertex weighting has a set X of at most q vertices such that each component after deletion contains at most half the total vertex weight. It suffices to require this for the two-color markings used in the proof. Treewidth at most q−1 guarantees the stated property.

### Theorem 2A: improved exact bound (new strengthening of F018)

Let r,q≥1 be integers. Suppose U∈C^(N×N) is unitary with every entry of modulus N^(-1/2). For i=1,…,r let Q_i be invertible, each lifted support graph have the stated separator property, and L_i,R_i have permutation-contained support. Put T=Σ_i L_i Q_i^(-1) R_i. Then

U=T  ⇒  N≤qr·9^r+q(3^r−1).

For any diagonal D,

U=D+T  ⇒  N≤4qr·9^r+2q(3^r−1)+2.

In particular the simpler bounds N≤4qr·9^r and N≤16qr·9^r hold. For invertible matrices Q_i with at most two nonzeros per column one can take q=2, obtaining

N≤2r·9^r+2(3^r−1),

or, with D, N≤8r·9^r+4(3^r−1)+2.

Fixed q therefore forces r=Ω(log N) for exact representations. The diagonal exceptional case r=0,N=1 is outside the theorem; no assertion with a zero right-hand side is made there.

### Proof: inverse ranks and separators

For an invertible d×d matrix M and index sets A,B,

rank M^(-1)[A,B] = rank M[B^c,A^c]+|A|+|B|−d.

To see this, for y supported on B, the condition (M^(-1)y)|_A=0 is equivalent under z=M^(-1)y to z supported on A^c and (Mz)|_(B^c)=0. Equating the two kernel dimensions and applying rank-nullity proves the identity. Principal blocks need not be invertible.

If a support separator X splits all remaining vertices into component unions A,B, then M[A,B]=0. The complementary matrix M[A∪X,B∪X] has rank at most 2|X|, because entries outside its zero A×B block occupy only |X| extra rows or |X| extra columns. The identity gives rank M^(-1)[A,B]≤|X|. Apply this to H_Q, whose inverse is [[0,Q^(−T)],[Q^(-1),0]]. Taking marked lower rows and upper columns yields the same bound for a Q^(-1) rectangle. Endpoint scales, including zeros, cannot increase it.

### Proof: the improved two-color selection lemma

Start with any m target rows and m target columns of one routed branch, where m≥4q. Mark the associated m lower vertices red and m upper vertices blue. The two color classes are distinct; arbitrary independent routing causes no collision. Mark even zero endpoint positions. A half-separator X leaves each graph component with at most m marks. Delete X and trim each surviving color to exactly t=m−q marks.

Each component now has total retained weight at most m≤4t/3, and all components together have weight 2t. Partition them into sides A,B with each side weight at least 2t/3. If one component has weight at least 2t/3, use it as A; its weight is at most 4t/3. Otherwise accumulate components until their weight first reaches 2t/3; it remains below 4t/3. The complement works in either case.

Let A contain a red and b blue marks, so B contains t−a red and t−b blue marks. At least one of the oriented cross pairs (a,t−b) and (t−a,b) has both entries at least t/3. If neither did, the four ways of combining failures would say either a+b<2t/3, or (t−a)+(t−b)<2t/3, or both a<t/3 and t−a<t/3, or both b<t/3 and t−b<t/3. Each is impossible. Since counts are integers, one can select

m_next=ceil((m−q)/3)

target rows on one side and target columns on the other. The branch rank on their rectangle is at most q.

This is the improvement over the frozen proof, which used side weights t/3 and retained floor(t/6) of each color. The fraction 1/3 is sharp for the abstract component-grouping information alone: with no deleted marks, three components each containing t/3 red and t/3 blue marks permit no larger cross-color minimum. This does not prove optimality of the resulting matrix theorem or its constants.

### Proof: iteration and explicit constants

Apply the lemma successively to the r branches. Previously established rank bounds survive restriction. Thus the final m_r×m_r rectangle has rank at most R=qr for T. With m_0 the starting size, the recurrence implies

m_j≥m_0/3^j−(q/2)(1−3^(−j)).

Write a=3^r, c=q(a−1)/2 and b=qr a².

First suppose there is no D and N>b+2c. Start with m_0=N. For 0≤j≤r−1,

m_j≥N/3^j−q/2>qr3^(r+1)−q/2≥8.5q>4q.

All uses of the selection lemma are therefore valid. Also m_r≥(N−c)/a>0. A square m×m restriction V of a flat unitary has ||V||_F²=m²/N and ||V||_2≤1, hence rank(V)≥m²/N. Exact equality U=T would give

(N−c)²≤Nb.

But (N−c)²−Nb=N[N−(b+2c)]+c²>0, a contradiction. This proves the first bound, including all integer sizes.

With D, start from disjoint target row and column sets of size floor(N/2); the diagonal vanishes and stays zero upon restriction. Put C=2c+1=q(a−1)+1 and b_D=4qr a². If N>b_D+2C, then for j≤r−1,

m_j≥N/(2·3^j)−1/2−q/2>2qr3^(r+1)−(q+1)/2≥17q>4q.

The selection is valid and m_r≥(N−C)/(2a)>0. The rank inequality would require (N−C)²≤Nb_D, contradicted in the same manner. This gives the diagonal bound.

A tree decomposition with bags of size ≤q supplies the separator property: assign each vertex's weight to one containing bag, choose a weighted centroid of the bag tree, and remove its bag. Every remaining graph component lies on one side of that tree centroid and has at most half the weight.

Finally, when Q has at most two nonzeros in each column, make a row-support multigraph with one column-labeled edge per column and loops for singleton columns. Invertibility ensures each connected component has no more edges than vertices. Equality of global totals forces equality in every component, so each is unicyclic. The bipartite lift subdivides two-entry edges and turns singleton-loop columns into leaves. It is a pseudoforest of treewidth at most two. This already gives q=3, but the following direct argument improves it to q=2, regardless of row degrees or component count.

Let W be the total vertex weight of a pseudoforest. If W=0 or every connected component has weight at most W/2, the empty separator works. Otherwise exactly one component is heavy. A heavy tree has a one-vertex weighted centroid. For a heavy unicyclic component, let T_v be the tree attached to cycle vertex v, including v, and let w_v be its weight.

If some w_v>W/2, place all weight W−w_v from outside T_v onto its root v and choose a weighted centroid c of this augmented tree of total weight W. If c≠v, the component of the tree after deletion containing v reconnects exactly to the outside part of the heavy component; its actual weight is at most the augmented component weight, at most W/2. Other attached components have the same weights as in the tree. If c=v, the outside cycle remainder has weight at most W−w_v<W/2, and the detached tree branches satisfy the centroid bound. Other original graph components were already light. Thus one vertex suffices in this case.

Otherwise every w_v≤W/2. Delete any cycle vertex x. Regard the remaining cycle path as a weighted path with vertex weights w_v, and choose its weighted centroid y. Deleting y leaves path segments of aggregate weight at most (W_component−w_x)/2≤W/2. Each branch detached from x or y has weight at most w_x or w_y, hence at most W/2. Other graph components remain light. Therefore {x,y} is a weighted half-separator. The support lift has no genuine loop; a singleton column made the corresponding component a tree. This proves q=2 and completes the theorem. ∎

### Theorem 2B: quantitative approximation and conditioning

Use the same selection construction whenever every step has m_j≥4q. Set m=m_r and R=qr. For any branch sum T,

||U−T||_F² ≥ max(0,m²/N−R).

If m>R, the sharper operator estimate is

||U−T||_2² ≥ max(0,(m²/N−R)/(m−R)).

The diagonal version uses the initial disjoint rectangle. Proof: each singular value of U's restricted block is at most one, so its top R singular values have squared sum at most R. Its tail energy is at least m²/N−R. There are m−R tail singular values. Equivalently, if operator error is ε, then the tail singular values are all at most ε, and m²/N≤R+(m−R)ε².

For fixed r,q as N→∞, m/N→3^(−r) without D and m/N→(2·3^r)^(-1) with D. Thus the asymptotic operator-error lower bounds are 3^(−r/2) and (2·3^r)^(-1/2), respectively. Normalized Frobenius-error lower bounds tend to 3^(−r) and (2·3^r)^(-1). These are approximation obstructions for fixed r; they do not imply r=Ω(log N) at a fixed nonzero error tolerance.

For a target A=D_L U D_R with invertible diagonal factors, transform every branch endpoint by D_L^(-1),D_R^(-1). The separator model is preserved, so exact branch-count obstructions are unchanged. Every displayed absolute error lower bound is multiplied by min|D_L|·min|D_R|. Relative operator-error bounds may be divided by max|D_L|·max|D_R|, giving at least the unscaled lower bound divided by κ_2(D_L)κ_2(D_R). Arbitrary dense preconditioners do not preserve the endpoint grammar and are not covered.

### Corollary 2C: an actual minimax–separator fusion

When the target is the normalized character table of an abelian 2-group and the final separator rectangle has odd side m, the C02 moment argument yields the stronger necessary inequality

qr ≥ ceil(m²/N + m(N−m)/N²).

Indeed choose H to be its m columns and I the complement of its m rows. The same odd-cardinality translation argument gives tr(A²)≤[(m−1)N(N−m)+(N−m)²]/N², while rank(V)=m−dim eig_1(A)≥m−tr(A²). The branch rank remains at most qr. For example N=64,m=21 gives rank at least 8, whereas the plain flat-unitary stable-rank ceiling gives 7. No claim is made that the selection always yields odd m or that this changes the asymptotic exponent.

There is also an explicit odd-rectangle operator gap. Put B(N,m)=[(m−1)N(N−m)+(N−m)²]/N². If a block approximant has rank ≤R<m−B(N,m), then its operator error is at least sqrt(1−sqrt(B(N,m)/(m−R))). Indeed σ_(R+1)(V)²=1−a_(m−R) for the descending eigenvalues of the complementary contraction, and (m−R)a_(m−R)²≤tr(A²). In the separator model use R=qr. This quantitative form was independently derived during cross-family synthesis.

## 3. Final scoped statements for the other main candidates

### C01: exact three terms in fixed dimension five

Let q be a positive odd integer, gcd(q,5)=1 and q≡1 mod 241. Put N=5q², choose a primitive complex Nth root ω, define

F_N[i,j]=ω^(ij), A_N[j,j]=ω^((N+1)j²/2), B_N=(F_N^(-1)+A_N)^(-1),

S={0,q²,2q²,3q²,4q²}, and C_q=B_N[S,S]. A permitted five-coordinate Green term is D_u(I−W)^(-1)D_v, where W[i,π(i)]=w_i for a Hamiltonian cycle π, all other entries vanish, and 1−∏_i w_i≠0. Endpoint entries and edge weights may be zero.

The minimum number of such terms for C_q, allowing arbitrary complex coefficients and Hamiltonian orders, is exactly three. A three-term representation exists over a genuine quadratic extension of Q(η), η=ω^(q⁴); two terms have nonzero reciprocal holonomy and the third is diagonal. The full growing matrix B_N inherits only a lower bound of three.

This is a final statement supported by the inherited certificate chain, not a newly reproduced complete certificate in this file. The lower proof requires all 576 Hamiltonian order pairs, algebraic-closure special-fiber emptiness of a closed projective necessary system, and proper specialization. The upper proof requires the explicit synthesis quadratic and the uniform local-ring nonvanishing guards. The retained original sources contain them; this pass inspected their mathematical audits, not their programs. A generic multiplicative diagonal–circulant factorization does not establish this additive minimum.

### C04: three-stage discrepancy obstruction

Let M=S_3P_2S_2P_1S_1 with q(S_i)≤r_i. Let the target be a Fourier matrix up to nonzero diagonal scaling and endpoint permutations. Assume at least one endpoint permutation is affine with stride coprime to N; the other may be arbitrary. Over any field containing a primitive Nth root, exact equality entails

2r_1+r_2+r_3 ≥ c log N−2,

r_1+r_2+2r_3 ≥ c log N−2,

for some absolute positive c. For complex prime N, full spark permits both endpoint orders arbitrary. The c is the classical planar-discrepancy constant; no explicit numerical cutoff is claimed here.

Proof outline with all active hypotheses: use an output prefix I of size W and every cyclic input window J_s of size W. Outer-stage errors have rank ≤r_3+2r_1, including wrapping windows. With R=p_2^(-1)(I), C_s=p_1(J_s), and a=|R∩[0,t)|, b_s=|C_s∩[0,t)|, deleting selected rows/columns gives rank S_2[R,C_s]≤r_2+W−|a−b_s|. The affine endpoint makes the target block Vandermonde of rank W (or use prime complex full spark). Thus |a−b_s|≤K=2r_1+r_2+r_3. Each original coordinate belongs to exactly W cyclic windows, so Σ_s b_s=Wt and |a−Wt/N|≤K. The permutation point set has grid discrepancy ≤K; passing to arbitrary anchored rectangles costs at most 2. Schmidt's theorem forces K+2≥c log N. Transpose for the other inequality.

The full-rank hypothesis is essential: for composite N, arbitrary selected Fourier minors may be singular. The theorem does not cover arbitrary depth, two arbitrary composite endpoints, or an approximate target without a quantitative singular-value replacement.

## 4. What was actually checked this pass

The proof of Theorem 2A's improved component lemma, ceiling recurrence, and thresholds was independently challenged by another researcher in this task and accepted within the stated scope. Fresh standard-library checks enumerate 641,425 color-count cases and 2,560 threshold/recurrence cases. Fresh numerical controls checked 3,736 complex Fourier submatrices for the moment identity and Theorem 1B gap; these are floating-point regression tests only. No supplied research program was executed, imported, compiled, or AST-parsed. See fresh_checks.py and fresh_check_results.json.

## 5. Additional current-intake sharpening: fixed-stage quadratic gap

This section concerns the newly retrieved Quadratic Fourier–Green Phase Rigidity checkpoint, not C02's cut-rank invariant. Its finite coefficient certificates were read as static evidence and not replayed.

### Theorem 5A: improved all-gauge operator bound

Let N≥3, F∈C^(N×N) be fixed, A,C∈GL_N(C), and B∈C^(N×N) have no zero entries. For j=0,1,2 define

P_j=diag((B[:,j])^(-1)) A^(-1) diag((FC^(-1))[:,j]).

For c∈C^N let Z_J(c)=[P_0c,P_1c,P_2c]. Let Q_J be the coefficient matrix of all its 2×2 minors in the unscaled degree-two monomials v(c)=(c_ac_b)_(a≤b). Assume Q_J has full column rank. Write

s=σ_min(Q_J)>0, M_P=(Σ_(j=0)^2 ||P_j||_2²)^(1/2), b_*=min_(u,j)|B_uj|>0,

β_N=sqrt((N+1)/(2N)).

Then every invertible diagonal L,D,E satisfies

||LADBEC−F||_2 ≥ β_N s b_* / (M_P ||A^(-1)||_2 ||C^(-1)||_2).

This improves the checkpoint's displayed constant by the factor sqrt(N+1). It requires the same fixed-stage hypotheses; it is not uniform over the stages, over N, or over all Green wirings.

### Proof

The unscaled monomial vector obeys

||v(c)||_2² = (||c||_2⁴+Σ_a|c_a|⁴)/2 ≥ (N+1)/(2N) · ||c||_2⁴.

Consequently the vector of all minors of Z_J(c) has norm at least β_N s ||c||_2². If its singular values are σ_1≥σ_2≥σ_3≥0, Cauchy–Binet identifies the squared minor norm with Σ_(i<j)σ_i²σ_j². This is at most (Σ_i σ_i²)(σ_2²+σ_3²). Since ||Z_J(c)||_F≤M_P||c||_2,

dist_F(Z_J(c),rank≤1) ≥ β_N s ||c||_2/M_P.

For M=LADBEC set c_i=L_ii^(-1). Multiplying L by a common nonzero scalar and dividing D by it leaves M unchanged, so assume ||c||_2=1. The entrywise quotient Z_M(c)=(A^(-1)diag(c)MC^(-1))⊘B equals de^T and has rank one. Therefore

β_N s/M_P ≤ ||(A^(-1)diag(c)(F−M)C^(-1))⊘B||_F

≤ ||A^(-1)||_2 ||C^(-1)||_2 ||diag(c)(F−M)||_F / b_*.

For every matrix Y,

||diag(c)Y||_F² = Σ_i |c_i|² ||Y[i,:]||_2² ≤ ||c||_2² ||Y||_2².

This removes the unnecessary unweighted Frobenius-to-operator factor sqrt(N). Substitution proves the theorem. ∎

The full-column-rank lift is only a sufficient rejection test. Rank deficiency can leave a kernel containing no decomposable v(c), and even a decomposable vector must meet every untested column and nonzero-coordinate guard. The source's N=3,4 modular examples and Hensel exceptional-locus examples are separate certificate-backed applications, not universal failures of four-Green networks.
