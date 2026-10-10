# Independent completion of three previously unreviewed matrix families

10 October 2026. Every conclusion below distinguishes a proof from a historical source-program claim. No supplied research program was executed, imported, compiled or AST-parsed. Two small excerpts were inspected as inert text solely to establish saved parameter conventions. Fresh programs in this directory are independently authored.

## A. Permutation-displacement theorem: accepted, even-size proof repaired

Let N≥1, K contain a primitive Nth root ω with char(K)∤N, F[i,j]=ω^(ij), and choose the cyclic output shift Z so ZF=FD, D=diag(ω^j). Replacing ω by ω^−1 changes no zero-sum condition. For any permutation P, let z(P) count its cycles whose index sum is zero modulo N. Then

rank(ZF−FP)=rank(D−P)=N−z(P),
min_P rank(ZF−FP)=floor(N/2),

and negation j↦−j is the unique minimizer.

### Complete proof, including the omitted even-size step

On a permutation cycle, the equation (D−P)x=0 propagates one coordinate by nonzero multipliers. It returns consistently exactly when the product of the diagonal roots on that cycle is one. Each such cycle supplies one kernel dimension and every other cycle supplies none. This proves the formula.

Only {0} is a zero-sum singleton. Every other zero-sum cycle has at least two elements, so z(P)≤ceil(N/2). Negation attains this with {0}, all non-self-inverse pairs {j,−j}, and, for even N, the remaining singleton {N/2}, which is not zero-sum.

For odd N, equality in the count requires {0} and (N−1)/2 zero-sum pairs, uniquely negation.

For even N=2k, the source's statement that equality directly forces all pairs skips a possibility allowed by vertex counts. Here is the repair. If there is no zero-sum singleton and z(P)=k, all N vertices would lie in zero-sum pairs, so the sum of all indices would be zero modulo N. But that sum is N(N−1)/2≡N/2≠0. Thus {0} is a cycle. The remaining k−1 zero-sum cycles consume at least 2k−2 vertices. If they consumed all remaining 2k−1 vertices, every cycle would again be zero-sum, contradicting the same total-index sum. Therefore they are all pairs and exactly one vertex remains. The only remaining vertex not paired with its negative is N/2, which is fixed. This proves uniqueness. N=1 is immediate.

The same proof is valid in every stated field; the zero-sum test is in Z/NZ. A monomial permutation with freely chosen nonzero weights is a different class and need not obey this extremum.

### What it establishes and what it does not

A one-permutation displacement representation needs a forcing/correction space of dimension at least floor(N/2). This is a displacement-rank obstruction, not an unrestricted arithmetic lower bound. A constant input-independent scalar recurrence generating all Fourier output sequences needs order N because its annihilating polynomial must vanish at N distinct roots. A deterministic adaptive linear-measurement algorithm has the usual zero-transcript kernel obstruction if it collects fewer than N scalar measurements on that branch. These supporting mechanisms are classical.

The source's separate-row work inequality is only a charged scheduling model: it assumes RN full-input scan cost and sum K_j log_2 K_j short-transform cost. The convexity minimum N log_2 N+N at integer R=1 or 2 is valid under those charges, not a lower bound against every batched evaluator.

### Fresh controls

`fresh_checks.py` enumerates all permutations at N=1,...,9 (409,113 total), confirms the unique extremizer at each size, and checks 852 actual modular matrix ranks against the cycle formula. This corrects the proof presentation; it does not discover a counterexample to the theorem. Classical displacement rank and cycle monodromy remain the close antecedents; exact worldwide priority is unresolved.

## B. Paired Fourier/Jacobi gates: accepted in the explicit saved affine layout

### Exact architecture and layout scope

N=256, U=F_256/16 over C. Use P_j x=x[p_j], where p_j is the binary-linear permutation obtained by xor-summing the eight columns in `AFFINE_LAYOUT.json`. All four S_j are invertible, two-sided quasiseparable order≤1, with zero generators allowed. Suppose

U=S4 P3 S3 P2 S2 P1 S1.

Set C4=S4^−1, C1=S1^−1 and H=P3^−1 C4 U C1 P1^−1=S3 P2 S2.

The JSON also carries `toffoli_gate_sequence_in_shuffle_2`. It is not applied by the inherited paired verifier or the inherited affine theorem. Our accepted instance is the three explicit binary-linear maps. No result is newly claimed for a Toffoli-composed nonlinear permutation. This semantic boundary must be kept in any portable certificate.

For a nonzero eight-bit mask m, let g_m(i) indicate even parity of i&m, C_m={i:g_m(i)=1}, R_m={i:g_m(p2[i])=0}. Both have size128. Let d(g) count natural-order binary transitions and b_m=d(g_m)+d(g_m∘p2).

### Paired rank proof

For any order-q quasiseparable A and a binary set X, rank A[X,X^c]≤q d(1_X). Strip off the first constant run of the indicator. Its crossing rows (or columns) form one restriction of a single upper-right or lower-left cut block and hence have rank≤q; the remaining entries have the same problem on the suffix, with one fewer transition. Induction proves the claim without divisions or nonzero-generator assumptions.

Split S2's intermediate coordinates between C_m and C_m^c. The part entering C_m^c has rank≤d(g_m). The part entering C_m is carried by P2 to R_m^c, so its output restriction contributes at most rank S3[R_m,R_m^c]≤d(g_m∘p2). Therefore

rank H[R_m,C_m]≤b_m.

Complementing g_m interchanges both sets and preserves transition counts, proving rank H[R_m^c,C_m^c]≤b_m as well. In the saved layout exactly32 masks have b_m<128; mask64 has b=16 (3+13). Thus there are64 necessary block-rank conditions.

Invertibility of H additionally forces both opposite cross blocks at mask64 to have rank≥112: each half of its columns has rank128, while its matching diagonal block has rank≤16.

### Paired norms and exact moment

For H0=P3^−1 U P1^−1, its two diagonal128-square blocks A0,D0 have identical singular values. Indeed unitarity gives A0*A0=I−C0*C0 and D0D0*=I−C0C0*, and the two C0 Gram matrices have the same spectrum. This is the classical cosine–sine identity.

Each block has squared Frobenius norm64 and all singular values≤1. Any rank≤16 approximation therefore leaves tail squared energy≥64−16=48. The blocks occupy disjoint entries, so every exact architecture above obeys, for every diagonal unitary D4,D1,

||C4 U C1−D4 U D1||_F²≥96,
||C4 U C1−D4 U D1||_*≥96.

For the trace norm, pinching to the two diagonal blocks is contractive, and the singular-value tail sum is at least its square sum since the baseline singular values lie in [0,1]. This uses the classical singular-value best-rank approximation theorem.

The saved mask64 block K also satisfies the strict spectral statement σ17(K)>3sqrt(2)/5. This pass independently rebuilt the integer modular-difference counts and all128 cyclotomic fourth-moment coefficients. Using Machin's identity with alternating rational arctangent bounds, then a rational cosine Taylor bound, it independently proves

M=tr((K*K)²)>1264/25.

Writing λ_j=σ_j², sum λ_j=64 and 0≤λ_j≤1, one has M≤16+48λ17. Hence λ17>18/25, giving the claimed spectral threshold. The new rational interval is saved in `paired_check_results.json`; displayed decimals are not used in this proof.

If C4 and C1 are both exactly unitary, H is unitary. The kernel of its rank≤16 block has dimension≥112. Intersect it with the span of K's top17 right singular vectors to obtain a unit x with P_R Hx=0 and ||P_R(D4 U D1)x||>3sqrt(2)/5. The minimum distance from a unit vector having projected norm a to any unit vector supported on the complementary output set is sqrt(2−2sqrt(1−a²)). Thus

||C4 U C1−D4 U D1||_2>sqrt(2−2sqrt(7)/5).

The corresponding equal outer-neighborhood radius is half this quantity. Exactly unitary outers are essential to this sharper operator constant. General invertible outers inherit the ordinary >3sqrt(2)/5 rank-approximation restriction instead.

### Denominator-free Jacobi dual and relaxation saturation

For invertible H and equal half-sets R,C, complementary nullity gives

rank H[R,C]=rank H^−1[C^c,R^c].

Since H^−1=P1 S1 U^−1 S4 P3, the paired rank constraints become polynomial minor conditions bilinear in the actual outer matrix entries before taking minors. They are necessary, not sufficient; invertibility remains an open guard. This is a specialization of the classical nullity theorem.

The scalar Frobenius-energy relaxation is exactly saturated at96. Assign energy3/1024 per entry to the two mask64 rectangles and zero elsewhere. Every other relevant rectangle intersects this support in8192 cells, receiving24 units, while its required scalar lower bound is at most17. We independently counted all62 intersections. This is a formal energy witness, not a matrix factorization. Weighted combinations of these scalar inequalities alone cannot improve96.

### Fresh certification depth

`paired_checks.py` reconstructs all32/64 gate counts, the mask64 cap16, all62 overlap counts, all128 exact moment coefficients, a fresh rational strict moment bound, and all eight17-square primal/dual determinant residues at primes12289 and65537. Those residues match the source. It does not re-execute the historical all128-square rank checks or random quasiseparable controls. The analytic proof above and newly reconstructed decisive certificate suffice for the stated paired theorem; no global four-stage infeasibility is claimed.

## C. Hadamard–Segre fixed-stage gate: accepted, eight witnesses reconstructed

Work over a field K. Fix invertible N-square A,B,C and invertible target F, with every entry of B nonzero. In the intended application F is a Fourier matrix with a supplied primitive root; the algebra below itself does not need that specialization. Let

Z(c)=(A^−1 diag(c) F C^−1) ⊘ B.

There exist invertible diagonal L,D,E with F=LADBEC if and only if an all-nonzero c has Z(c) rank one and every entry of Z(c) nonzero. The forward direction sets c=diag(L)^−1 and obtains Z(c)=de^T. The reverse direction factors the all-nonzero rank-one matrix as de^T with all coordinates nonzero, then reverses the multiplication. Zero-coordinate guards cannot be dropped.

Let h_j=(FC^−1)[:,j], b_j=B[:,j] and P_j=diag(b_j^−1)A^−1diag(h_j). If P0 is invertible, set T_j=P0^−1P_j. The factorization is equivalent to a common eigenvector c of all T_j satisfying c_i≠0, (P0c)_i≠0, and all eigenvalues nonzero. Consequently an invertible [T1,T2] excludes every L,D,E for N≥3. A singular commutator is not a converse.

For C=I and positive-exponent Fourier, T_j=A diag(b0/bj) A^−1 Δ^j, Δ=diag(ω^i). This equality follows directly from P0=diag(b0^−1)A^−1 and h0=1. It genuinely permits a free right gauge.

### Sharpened complex gap: remove the unnecessary sqrt N

Under the hypotheses above over C, assume K0=[T1,T2] invertible. Put

s=σmin(K0), μ=σmin(P0), a=||T1||2, b=||T2||2, Mj=||Pj||2,
δ=min{μ/2, sμ/[4sqrt(a²+b²)sqrt((1+M1/μ)²+(1+M2/μ)²)]}.

Then every invertible diagonal L,D,E obeys

||LADBEC−F||2 ≥ δ min|B_uv| / [||A^−1||2 ||C^−1||2].       (4)

This improves the source's positive constant by sqrt N, using the same weighted-row estimate that sharpened the quadratic-minor gap.

Proof of δ: normalize ||c||2=1. For λj=c*T_jc and ej=T_jc−λjc, the commutator expansion gives s≤2sqrt(a²+b²)sqrt(||e1||²+||e2||²). If a rank-one R lies ε<μ/2 from Z(c) in Frobenius norm, its first column has norm≥μ/2. Write R[:,j]=αjR[:,0]; then |αj|≤1+2Mj/μ and dist(T_jc,span(c))≤(2ε/μ)(1+Mj/μ). Substitution gives ε≥δ. If ε≥μ/2 the conclusion is immediate; rank-zero R also has error≥μ. Thus every Z(c) has rank-one distance≥δ.

For M=LADBEC, the scalar gauge L↦tL,D↦D/t permits ||c||2=1. The exact rank-one comparator yields

δ≤||[(A^−1 diag(c)(F−M)C^−1)⊘B]||F
 ≤(||A^−1||2||C^−1||2/min|B|) ||diag(c)(F−M)||F.

Finally ||diag(c)Y||F²=sum_i|c_i|²||row_i(Y)||²≤||c||2²||Y||2². This proves(4). The constants depend on fixed stages and may vanish along a varying family. No all-size or all-wiring bound follows.

### Sparse-middle extension: complete characterization, classical attribution

The source leaves sparse B as an unsettled masked rank-one problem. Its exact algebraic characterization is available by classical diagonal equivalence. Let E be the bipartite support of B and Y(c)=A^−1diag(c)FC^−1. Then F=LADBEC with invertible diagonals if and only if an all-nonzero c satisfies:

1. Y(c)_uv=0 exactly where B_uv=0;
2. z_uv=Y(c)_uv/B_uv is nonzero on E;
3. on every bipartite cycle, the alternating products of the z edge labels agree.

Necessity is cancellation in z_uv=d_u e_v. For sufficiency choose a spanning forest of the support graph, assign a nonzero value at one vertex per component, and propagate d_u,e_v via each tree-edge equation. All propagated values are nonzero. A non-tree edge is correct exactly when its fundamental-cycle product is one; thus all edges agree. Invertible B has no isolated rows or columns; an isolated vertex in a more general rectangular problem can simply receive any nonzero scale. This yields the required diagonal factors.

This is an application of Engel–Schneider's 1982 diagonal-equivalence/spanning-forest theory, not a newly invented sparse gauge algorithm. It closes the exact characterization interface but does not solve the polynomial search over c or make it linear-time.

### Fresh witness audit and correct modular lifting

All eight saved certificates at N=3,4,6,8, with four-Green and six-Green architectures, were reconstructed from the signed integer cycle weights, endpoint diagonals and independently specified row/column permutations. Forty individual Green branches were rebuilt by fresh modular inversion. The reconstructed A,B,C,P0,T1,T2 and commutators match all saved matrices. Determinants modulo97 are 8,3,71,90 (four-Green) and38,34,55,70 (six-Green).

These nonzero values certify nonzero cyclotomic determinants over C for the fixed integer/rational parameter choices, since every denominator is invertible in the modular specialization. This is legitimate nonvanishing lifting. It is not a finite-field emptiness argument and does not show every choice of parameters fails. The other56 reported random witnesses were not stored in this certificate and are not claimed independently reconstructed.

### Primary comparison, directly inspected

- Engel–Schneider, *Algorithms for Testing the Diagonal Similarity of Matrices and Related Problems*, final1982 paper, author archive https://people.math.wisc.edu/hans/paper_archive/scanned_papers/hs066.pdf. Theorem3.8, Corollaries3.9–3.11 and §4.4 explicitly give spanning-forest/Hadamard-quotient tests and the bipartite embedding for diagonal equivalence. The sparse characterization above is classical.
- Shemesh, *Common eigenvectors of two matrices*, final1984 paper, author-uploaded full text https://www.researchgate.net/publication/242984666_Common_eigenvectors_of_two_matrices. Theorem3.1 and its proof use the intersection of kernels of all commutators [A^k,B^ℓ], a stronger classical criterion than a single commutator determinant. Its primary text was inspected directly, not inferred from a later abstract.
- Vandebril–Van Barel, nullity theorem, https://www.cs.kuleuven.be/publicaties/rapporten/tw/TW397.pdf: complementary inverse-block ranks are classical.

No priority claim is assigned to these mechanisms. The supported project contribution is their fully specified fixed-stage Fourier/Green application, guarded field specialization, and the displayed improved norm constant.

## D. Outer-stability extension: explicit proof and freshly certified constant

Use exactly the N256 affine layout and mask64 from §B. Let α=3sqrt(2)/5, now independently certified by the rational moment calculation. For an exact factorization, H's selected block has rank≤16, whereas the block of P3^−1D4 U D1P1^−1 has seventeenth singular value>m4 m1 α, where D4,D1 are any invertible diagonal reference matrices and m4,m1 are the minimum absolute diagonal entries on the selected Fourier row/column sets. Coordinate restriction and singular-value best-rank approximation imply

||C4 U C1−D4 U D1||2>m4 m1 α.

The exact decomposition

C4 U C1−D4 U D1=(C4−D4)U C1+D4 U(C1−D1)

gives

||C4−D4||2||C1||2+||D4||2||C1−D1||2>m4 m1 α.       (5)

For unitary diagonal references and both distances≤ε, ||C1||≤1+ε, so ε(2+ε)>α, equivalently ε>sqrt(1+α)−1. This general-invertible-outer statement is distinct from the stronger exactly-unitary-outer radius in §B.

For an approximate architecture M=S4P3S3P2S2P1S1, let e=||U−M||2. If e<1 then M is invertible by the Neumann lemma and so are all square S_j. Its middle restriction still has rank≤16. Adding the transformed error C4(U−M)C1 to the preceding comparison gives

e||C4||2||C1||2+||C4−D4||2||C1||2+||D4||2||C1−D1||2>m4m1α.

For unitary diagonal references with both distances≤ε, this yields the convenient non-strict corollary

e≥max(0,α−ε(2+ε))/(1+ε)².

If e≥1 the displayed bound is automatically true since α<1. This completes the expanded outer-stability implication. It does not exclude outers far from diagonal references, and it does not solve simultaneous complex infeasibility for the four-stage architecture.
