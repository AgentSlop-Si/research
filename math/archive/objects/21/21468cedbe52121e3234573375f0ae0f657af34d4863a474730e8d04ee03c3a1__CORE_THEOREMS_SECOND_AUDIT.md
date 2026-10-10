# Core matrix-theory second audit

10 October 2026. This completes the second proof-level review of C01, C02, C04, F018, F014 and FUS-03, with explicit evidence depth. The previous finalization's complete C02/F018/phase-gap proofs are retained at `research_finalization_0923/matrix/FINAL_THEOREMS.md`; this document supplies the missing full C04 argument, verifies sensitive steps in the retained proofs, and links actual strengthenings. Correctness, independent certificate reconstruction and worldwide novelty are separate statuses.

## 1. C02: sharp cyclic-dyadic minimax retained; analytic boundaries checked

For N=2^m≥8, F_N=(ω^(ij)) and q(A)=max over cuts of both off-diagonal block ranks,

min_(independent ρ,σ) q(Pρ F_N Pσ^T)=N/4+1.

The exact statement is over C, and over characteristic-zero fields containing the required root by extension of scalars. Its proof is not asserted over every finite field. The matching upper construction is double bit reversal; it is not claimed new to the literature.

The lower proof uses r=N/2−1 rows and h=N/2+1 columns of a normalized character table, the complementary Gram contraction A, and the fourth-moment bound

tr A²≤B_L=L+3/4+1/(4L)+1/(16L²), N=4L.

Every nonzero translation in an abelian2-group has even orbit size, so an odd column set cannot be invariant. This gives σ_(L+1)≥sqrt(1−sqrt(B_L/(L+1)))>0. The index reversal between A and I−A, positivity for L≥2, and asymptotic δ_N~(2N)^−1/2 all check. The lower extension to abelian2-groups is valid, but a matching minimax upper construction for every such group is not supplied.

The cyclic bit-reversal recurrence r_N(k)=ceil(k/2)+r_(N/4)(floor(k/2)), k≤N/2, is correct only if an odd cut retains the residue from the unremoved member of the split even-column pair. The retained proof does this. Reflection extends the upper bound to the second half, and the critical cut N/2−1 attains N/4+1.

Common-order product subadditivity is valid. Every interstage permutation must be charged by its actual cut rank; independent endpoint minimization does not authorize free changes of coordinates inside a product. A cut-rank budget is not an arithmetic-operation count.

### Novelty comparison still genuinely open

The final Delvaux–Van Barel article is verified at DOI10.1016/j.laa.2008.04.043, LAA429(7),1587–1605,2008. The current publisher full-text attempt again returned403; the author-institution record provides an external DOI link, and targeted legitimate author/institution/exact-title searches located the2006 TW470 version or bibliographic records rather than a verified final full text. No access denial was bypassed.

TW470 was already read in depth by the prior finalization, including Lemma8 and Theorem10. Its rank-one digit-reversal hierarchy is established prior art. Its extremal support/Hamming-number quantifiers differ from C02's all-independent-orders critical-kernel-dimension minimax assertion. This identifies a comparison question, not absence from the2008 final article. The final-paper theorem-by-theorem priority check remains open and must not be marked completed.

Verified source links: https://www.cs.kuleuven.be/publicaties/rapporten/tw/TW470.pdf ; https://www.sciencedirect.com/science/article/pii/S0024379508002164 ; https://lirias.kuleuven.be/1537109 .

## 2. F018: the 9^r and q=2 refinements survive adversarial rechecking

The exact model is a sum T=Σ_(i=1)^r L_iQ_i^−1R_i over C. Each Q_i is invertible; its symmetric bipartite support lift has weighted half-component separators of size≤q for the two-color markings in the proof. Each endpoint has support contained in a permutation graph and can have zero weights. Branch routes are independent. Integers r,q≥1.

For a flat normalized unitary U, exact equality U=T implies

N≤qr9^r+q(3^r−1).

With any diagonal correction D, U=D+T implies

N≤4qr9^r+2q(3^r−1)+2.

The retained proof's sensitive points all check:

- complementary inverse-block rank uses the nullity theorem and does not assume nonsingular principal subblocks;
- red and blue markings are on distinct vertices of the bipartite lift even when branch endpoint routes differ;
- after deletion/trim to t=m−q, m≥4q ensures every component has≤4t/3 total retained marks;
- a component partition with each side between2t/3 and4t/3 exists;
- at least one oriented cross-color pair has both counts≥t/3, giving ceil((m−q)/3);
- prior branch-rank constraints survive restriction;
- the exact thresholds imply every preceding m_j≥4q, avoiding circular iteration;
- initial disjoint half-sets correctly remove a free diagonal and explain the floor correction+2.

The 1/3 retention bound is sharp for the component-count information alone. This does not prove9^r or the matrix thresholds optimal.

If Q has at most two nonzeros per column, invertibility forces each component of its row-support multigraph to be unicyclic: each component has no more column-edges than row-vertices, and global equality forces equality componentwise. The bipartite support lift is a pseudoforest. A weighted tree centroid, or two deleted cycle vertices after aggregating attached trees, gives q=2. The attached-heavy-tree case is handled by moving external weight to the attachment root before choosing the centroid. Zero weights, disconnected supports and singleton columns cause no gap. A forest lift permits q=1.

For the selected m-square block and R=qr, operator error² is at least max(0,(m²/N−R)/(m−R)) when m>R; Frobenius error² is at least max(0,m²/N−R). Singular values are≤1, so subtracting at mostR from the total squared energy proves both. At fixed r,q the operator lower bound tends to3^(−r/2), or(2·3^r)^−1/2 with a diagonal. These fixed-r floors do not imply r=Ω(log N) at fixed positive error tolerance.

Inverse rank closure, separators, treewidth and singular-value tail inequalities are classical. The new-to-project result is the sharpened selection/cutoff within this specific routed-sum model. Final TQS binary-tree and ordering discussions were already inspected in the prior pass; no published-open-question-solved claim is justified.

## 3. C04: full reconstruction of the previously carried discrepancy theorem

Let q(S_i)≤r_i in one fixed coordinate order and

M=S3 P2 S2 P1 S1.

Let M equal a Fourier matrix with nonzero diagonal endpoint scaling and row/column permutations, at least one of which is affine with invertible stride modulo N. For complex prime N, both endpoint permutations may instead be arbitrary by the classical full-spark Fourier theorem. Then an absolute c>0 gives

2r1+r2+r3≥c log N−2,
r1+r2+2r3≥c log N−2.                                      (5)

The algebraic argument with one affine endpoint holds over any field containing a primitive Nth root (hence N is invertible). The two-arbitrary-endpoint full-spark extension here is specifically complex prime length, not an arbitrary finite-field claim.

### Proof

Use the convention P e_j=e_(p(j)). Fix output prefix I=[0,W) and each cyclic input window J_s={s,...,s+W−1} modN, 1≤W<N. The exterior S3[I,I^c] has rank≤r3. The exterior S1[J_s^c,J_s] has rank≤2r1: for a nonwrapping interval it is a vertical combination of two cut restrictions; for a wrapping window its complement is an interior interval and the two exterior column groups give the analogous horizontal combination.

Let E_X be the coordinate projector on X. Split

E_I S3 = E_I S3 E_I + E_I S3 E_(I^c),
S1 E_J = E_J S1 E_J + E_(J^c) S1 E_J.

Expanding the product groups every term containing the first exterior piece into one error of rank≤r3, and the remaining terms containing the second into one error of rank≤2r1. The main piece factors through S2[R,C_s], where R=p2^−1(I), C_s=p1(J_s). Hence

rank M[I,J_s]≤r3+2r1+rank S2[R,C_s].

For a middle threshold t, let a=|R∩[0,t)| and b_s=|C_s∩[0,t)|. Removing W−a rows and b_s columns leaves an upper-right cut restriction, proving rank≤r2+W−a+b_s. The other orientation removes a rows and W−b_s columns, giving rank≤r2+W+a−b_s. Taking the smaller yields

rank S2[R,C_s]≤r2+W−|a−b_s|.

Every target block M[I,J_s] has rank W. If the output endpoint is affine, its W selected frequencies are consecutive affine residues and the arbitrary distinct input labels produce a Vandermonde matrix. If the input endpoint is affine, the cyclic window provides consecutive affine time labels, and transposed Vandermonde gives the same conclusion even with arbitrary selected output labels. Nonzero endpoint scales preserve rank. In the prime complex two-arbitrary-endpoint case full spark supplies rankW instead.

Thus |a−b_s|≤K=2r1+r2+r3. Each original coordinate belongs to exactly W cyclic windows, so Σ_s b_s=Wt and |a−Wt/N|≤K. This holds for every W,t. It says the permutation point set {(i/N,p2^−1(i)/N)} has unnormalized grid discrepancy≤K. Extending to all anchored rectangles changes N times area by at most2, so its star discrepancy is≤K+2. Schmidt's classical planar lower bound is≥c log N, proving the first inequality in(5). Transpose the entire factorization to obtain the second; the one-affine-endpoint property is preserved.

Wrapping windows, the exact averaging, singular stage generators and independent internal permutations are all covered. This does not prove arbitrary-depth bounds, composite two-arbitrary-endpoint bounds, or approximation bounds. The latter require quantitative smallest singular values for all selected windows; C02's one critical-rectangle gap cannot silently supply them.

Primary support: the unnormalized all-point-set discrepancy formulation is explicitly recorded in Bilyk–Lacey–Parissis–Vagharshakyan, pp.1–2, equation(1.2), https://arxiv.org/pdf/0810.5544 . The original Schmidt1972 DOI is https://doi.org/10.4064/aa-21-1-45-50 . Full spark for complex prime Fourier is in Tao, https://arxiv.org/abs/math/0308286 . The application's rank/discrepancy bridge is proved above; the classical discrepancy theorem is not claimed new.

## 4. C01: exact three retained, with certificate-dependency status intact

For q positive odd, gcd(q,5)=1, q≡1 mod241, let N=5q², ω primitive complex Nth root, A_N=diag(ω^((N+1)j²/2)), B_N=(F_N^−1+A_N)^−1 and S={0,q²,2q²,3q²,4q²}. The fixed5-square block C_q=B_N[S,S] has exact additive length3 in the grammar D_u(I−W)^−1D_v, where W has one weighted Hamiltonian structural cycle and1−product(weights)≠0. Zero edge weights and singular endpoint masks are included in the lower bound. Independent unmatched left/right permutations are not.

The two-summand exclusion is over arbitrary complex coefficients; the three-term construction is defined over a genuine quadratic extension of Q(η), η=ω^(q⁴). It uses two reciprocal nonzero holonomies plus a diagonal zero-weight term. The full growing B_N inherits only length≥3.

This pass reread the complete independent lower and upper audit texts. The critical lower chain is: all24² order pairs; nonsingular projective transition forms; algebraic-closure row enumeration including infinity;384 empty row domains and624 remaining branches; nonzero augmented minors at each branch; a closed projective necessary scheme including endpoint limits; and proper specialization from a local cyclotomic ring at(241,η−91). An absence of F241-rational points alone would be insufficient, but the audited computation explicitly uses the quadratic extension and all projective roots.

The upper chain has target denominator norm1−125q^6≠0, the synthesis quadratic and residual identity, a monic reduction d²+30d+124 with nonsquare discriminant163 modulo241, and successive unit/norm guards. Since q≡1 mod241, all rational reconstruction denominators remain units by induction in the local ring. This justifies both roots and every complex embedding. The variable q controls parameters of a fixed5-dimensional matrix; it is not the matrix dimension in the upper theorem.

The existing independently audited portable certificate is substantial evidence. This second pass did not recompute its entire576-pair/624-branch dataset or upper quadratic formulas. Its correct status is “accepted certificate chain, reread in full; not freshly reconstructed here,” rather than a new independent certificate replay. Base-field-only length, a growing-dimensional upper family and precise additive-variety/secant prior art remain open. Generic circulant–diagonal product factorization does not settle this additive minimum.

## 5. Actual new strengthenings and other closed gaps

- `NEW_COMPOSITE_WEYL_THEOREM.md`: F014 is fully rederived and extended. Every fixed generating pair at odd prime-power N needs at least(N+1)/2 two-resolvent branches; general odd N has the explicit gcd bound and ceil(sqrt N). The separate canonical-with-Weyl-endpoints theorem still needsN. An independent reviewer accepted the complete artifact.
- `FOURIER_DEFICIT_SEPARATOR_FUSION.md`: FUS-03 extends to autocorrelation-deficit bounds for rectangular minors of every finite abelian character table and cardinality-only p-group versions. Safe trimming supplies a legal coprime-size subrectangle; no unsupported odd-output assumption remains.
- `OMITTED_MATRIX_THEOREMS_AUDIT.md`: complete displacement extremizer proof with an even-N repair; paired-Jacobi analytic proof and decisive exact certificate reconstruction; Hadamard–Segre gates with all8 saved modular witnesses rebuilt, a sqrt N gap improvement, and a classical sparse-middle characterization.
- The retained quadratic-minor all-gauge bound β_N s b*/(M_P||A^−1||||C^−1||), β_N=sqrt((N+1)/(2N)), survives this second proof audit. Its monomial norm and weighted-row estimate are correct. Current source-specific finite quadratic certificates remain separate from this analytic implication.

## 6. Remaining obligations are not hidden completion claims

1. Obtain an authorized final2008 Delvaux–Van Barel text and compare its rank/nullity statements theorem by theorem.
2. Independently reconstruct the full C01 certificate packet in this cycle if a new third audit is required; the existing sealed independent audit remains the support actually used.
3. Search specialist additive cyclic-resolvent, fixed-Weyl-grammar and independently routed low-width inverse-sum literature before claiming publication priority.
4. No accepted theorem supplies an unrestricted FFT arithmetic lower bound or an all-length exact linear-time evaluator.
5. No proof here makes the stage-dependent analytic constants uniform without additional conditioning certificates.
