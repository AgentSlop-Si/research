# Independent final review: codimension-three Fourier masks and quantitative separation

Date: 2026-10-18. Stable owner: **M-SPARSE-DEFECT**.

## Verdict

**ACCEPT both stated theorems, including the complete weight-three support and phase description. No mathematical correction is required.**

1. For every N≥4, Delta(N,N−3)=sqrt(3/N) if and only if 3 divides N. The divisible case is attained; otherwise the infimum is strictly above the floor.
2. Every weight-three complementary Fourier mask satisfying the equality criterion splits, after independent row and column permutations, into full 3×3 blocks. Each block must and can satisfy precisely the four congruences in the candidate's equation (4.1).
3. For N≥2, 1≤s≤N−1, d=N−s, absence of an equality mask implies

   Delta(N,s)^2 ≥ d/N + s^6 / [2^22 N^10 d^(2 phi(N)−2)].

   This is a bound for the unrestricted simultaneous inverse-row-sparsity problem, proved for every admissible matrix before taking the infimum. It is not an exact nonsharp optimum or an optimal gap rate.

Retain **TO RESEARCH**, priority **42**. Remaining composite budgets and exact nonsharp values remain unresolved. No additional mathematical gate is needed for these scoped results.

## Evidence binding and accepted input

The candidate reviewed is `retained-source-history/sparse_codimension_three_20261018_1331`:

- REPORT.md SHA-256: `4993a893a85f3fd40956f8cdd90476b8fde5a24b07cc488bceaf268196967abc`
- MANIFEST.json SHA-256: `729d1ecec41b762d0e3bc7ee3f796177d4307e803535fb68f0775cb189097927`
- verify_exact.py SHA-256: `17213bca05de0779b6a88874d2cce6a2627552d08fea831b1c64bdab15b7b0f0`

All 12 manifest members matched their declared byte lengths and hashes. The candidate seal matches its report, checker, and manifest. All four bound source copies match their original local files, lengths, and declared hashes. The accepted review `retained-source-history/sparse_mask_final_review_20261018_1248/REVIEW.md` has SHA-256 `ec6631ebb5f36bcf68abfb7c03c464048f922356d97080b8e1b2fd55ca345a35`; its nine-member manifest and relevant seal bindings also verify. The candidate's accepted mask report has SHA-256 `1fcfed20e788dbc9bc1085b8eab8fcd92564888d21f429db8c044ee7569d10ee`.

The candidate manifest is copied into this packet. Before and after checks bind this decision to unchanged candidate bytes. This review does not endorse subsequently edited files without renewed review.

The accepted model is the normalized complex Fourier matrix F[r,c]=N^(-1/2) omega^(rc), omega=exp(−2 pi i/N), the spectral norm, invertible M, and at most s nonzeros in **every row** of M^(-1). The inherited floor is sqrt((N−s)/N). The accepted criterion says the floor is the infimum exactly when a complementary Fourier-entry mask C with d=N−s entries per column has C*C=(d/N)I. Every associated minimizer is M=q(A*)^(-1), where q=s/N and A=F−C. The accepted compactness argument makes equality of the infimum imply attainment. The candidate uses these inputs correctly and does not replace the simultaneous budget by a one-row model.

## 1. Degree-three support classification

The candidate's support lemma is correct for any square matrix with exactly three nonzeros per row and column and mutually orthogonal columns. Only the impossibility of a singleton overlap is needed.

If two columns have the same triple S, those columns consume two incidences at each of the three rows of S. Exactly three incidences with S remain. Every further column meeting S must meet it in at least two rows, because its inner product with either original column cannot consist of a single nonzero term. Three remaining incidences can therefore belong only to one further column, using all three. These rows and columns are saturated, producing an isolated full 3×3 block.

Remove all such blocks. For a remaining column with support {a,b,c}, each other column meeting it uses exactly two of these rows: one is forbidden, and three would create a repeated support. The six remaining row incidences consequently belong to three columns. Writing multiplicities of ab, ac, bc as x,y,z gives x+y=x+z=y+z=2, hence x=y=z=1. The columns have supports {a,b,u}, {a,c,v}, {b,c,w}, with u,v,w outside the first triple. Pairwise exclusion of singleton overlaps forces u=v=w. The four rows and four columns are saturated, and their missing entries form a perfect matching.

Thus no longer connected component is possible. This proof does not assume the entries all have the same magnitude. In the Fourier-mask application, the required row-regularity follows from C*C=(3/N)I and squareness: C is invertible and CC*=(3/N)I, so every row also has three entries.

An ordinary real weight-three conference matrix of order four exists, so the second support type cannot be dismissed by support reasoning alone. The candidate correctly retains it until the Fourier-phase argument.

## 2. Fourier conference exclusion, including even composite N

Relabel the matched zeros as (r_i,c_i), i=0,1,2,3. Two distinct columns i,j overlap exactly in the complementary rows k,l. Their orthogonality requires

   (r_k−r_l)(c_i−c_j) ≡ N/2 (mod N).

For odd N, the two-term cancellation would require −1 to be an N-th root, which is impossible. For even N, write N=2^n m with m odd. Reduction modulo 2^n gives a product congruent to 2^(n−1), so each complementary pair of differences has finite valuations satisfying

   v2(r_k−r_l)+v2(c_i−c_j)=n−1.

All six row edges and all six column edges appear, so the congruences themselves exclude any pairwise coincidence modulo 2^n. This is why the proof applies to mixed even dimensions as well as powers of two.

Let alpha be the smallest row-edge valuation. After translating and dividing by 2^alpha, the four row labels split into two nonempty parity classes. Cross-class row differences have valuation alpha; within-class differences have larger valuation. Put beta=n−1−alpha. Complementary cross-class row edges force column differences of valuation beta; complementary within-class row edges force column differences of valuation strictly less than beta.

- In a 1+3 split, the three cross-class row edges form a star. Complementing them gives a column triangle. Three integer pairwise differences cannot all have the same finite 2-adic valuation beta: subtracting two differences of valuation beta gives valuation at least beta+1.
- In a 2+2 split, the complement of each cross-class edge is again cross-class. All four corresponding column differences have valuation beta. Comparing two column vertices in one class against the same vertex in the other gives a within-class difference of valuation at least beta+1. That edge is complementary to a within-class row edge, which required its valuation to be less than beta.

Both possibilities contradict the six equations. The direction and strictness of the valuation inequalities are correct; no odd factor, residue-coincidence exception, or low-2-adic-order case is omitted.

## 3. Global codimension-three criterion and block phases

Only triple components survive, so their sizes sum to N and 3 divides N. Conversely, for N=3m, the prescribed blocks use rows {3t,3t+1,3t+2} and columns {t,t+m,t+2m}, 0≤t<m. These sets separately partition all row and column coordinates. Their entries satisfy

   omega^((3t+u)(t+ell m)) = omega^((3t+u)t) (omega^m)^(u ell).

Each block is therefore a row-phased sqrt(3/N) multiple of the normalized F_3. Both Gram matrices of the resulting C are (3/N)I. The accepted inverse formula supplies the attained minimizer. Since N≥4, s=N−3 is positive; the inadmissible optimization endpoint N=3,s=0 is not asserted.

For an arbitrary full triple block, row and column dephasing turns its entries into omega^((r−r_0)(c−c_0)) and makes the initial row and column all ones. For unit complex x,y, 1+x+y=0 forces x and y to be the primitive cube roots in either order. The two remaining columns cannot have the same order, because they would coincide. They must have opposite orders. After relabelling this gives exactly

   (r_1−r_0)(c_1−c_0) ≡ N/3,
   (r_1−r_0)(c_2−c_0) ≡ 2N/3,
   (r_2−r_0)(c_1−c_0) ≡ 2N/3,
   (r_2−r_0)(c_2−c_0) ≡ N/3  (mod N).

These four equations are sufficient as well, since the dephased block is an unnormalized F_3. Arbitrary row/column partitions into triples are not sufficient, and the candidate explicitly avoids that mistake. The resulting support-plus-phase classification is exhaustive. Applying the accepted coefficient-rigidity theorem then classifies every floor minimizer, not just the displayed divisor examples.

## 4. Discrete gap for a bad complementary mask

For a mask with exactly d entries per column, the diagonal of C*C is d/N. If C*C differs from (d/N)I, it has a nonzero off-diagonal entry N^(-1)P(omega), where P is an integer sum of at most d monomials. Different overlap indices can give equal exponents; this only introduces nonnegative integer coefficients and does not invalidate the argument.

The cyclotomic norm of P(omega) is a nonzero integer. Irreducibility of Phi_N means a nonzero value at one primitive N-th root cannot have a zero conjugate. Each of the other phi(N)−1 factors has modulus at most d by the triangle inequality. Consequently

   |P(omega)| ≥ d^(−(phi(N)−1)),
   ||C*C−(d/N)I|| ≥ gamma = 1/[N d^(phi(N)−1)].

The operator norm dominates each matrix entry, so the last implication is valid. This step does not need row-regularity, invertibility of the masked matrix, or an assumption that the column difference is coprime to N. At d=1 or phi(N)=1 the formula remains meaningful. If there is no such no-mask case at some parameter value, the conditional theorem is simply vacuous there.

## 5. Direct all-matrices quantitative argument

Fix any admissible M. Write B=M^(-1), E=M−F, rho=||E||, q=s/N, a²=1−q, and D=rho²−a²≥0. Put rho_0=(1+a)/2, L=(1−a)/2, U=(3+a)/2. The elementary inequalities

   L≥q/4, U≤2, rho_0²−a²=(1−a)(1+3a)/4≥q/8

hold over the full parameter range. In particular, the last follows after cancelling 1−a>0 and using 2(1+3a)≥1+a.

If rho≥rho_0, D≥q/8. If D≥1/N, there is a second easy branch. Otherwise rho<rho_0<1 and D<1/N. The inherited one-row bound applied to every actual support size t_i forces t_i=s: a row with t_i≤s−1 would imply D≥1/N.

For the resulting supports, let A[r,i]=F[r,i] on S_i and zero elsewhere, and B_0=q^(-1)A*. The exact support-restricted identity is

   q||b_i−b_0i||² = 1+q||b_i||²−2 Re((b_iF)_i)
                    = ||b_iE||²−a²||b_i||² ≤ D||b_i||².

The unitary F, b_iM=e_i, and ||b_0i||²=1/q justify all normalizations. This identity permits arbitrary complex coefficients in B. Since ||M||≤U and ||B||≤1/L, summing over the complete inverse-row family gives

   T=||B−B_0|| ≤ sqrt(ND/q)/L.

Now H=rho²I−EE* is positive semidefinite, and

   0≤b_iHb_i*≤D||b_i||²,
   tr(BHB*)≤ND/L².

Because H=M(BHB*)M*, positivity gives tr(H)≤U² tr(BHB*), so ||H||≤NU²D/L². To make the candidate's next norm step explicit, EE*−a²I=DI−H has eigenvalues D−lambda_j(H). Thus its norm is at most max(D,||H||), and NU²/L²≥1. Therefore

   ||EE*−a²I||≤NU²D/L².

This is valid; it does not require an extra additive D or an extra factor two. The use of all inverse rows, and the invertibility of B, is essential in the trace transfer.

Define G(X)=I−XF−F*X*+qXX*. The following identities have the correct order of factors:

   G(B)=B(EE*−a²I)B*,
   qG(B_0)=C*C−a²I, where C=F−A.

Hence ||G(B)||≤NU²D/L^4. Moreover,

   ||G(B_0)−G(B)||≤T(2+q||B||+q||B_0||)
                   ≤T(2+q/L+sqrt(Nq)),

using ||B_0||≤||B_0||_F=sqrt(N/q). It follows that

   ||C*C−a²I|| ≤ (qNU²/L^4)D
                  +[sqrt(Nq)/L](2+q/L+sqrt(Nq))sqrt(D).

Here D<1/N<1. Using D≤sqrt(D), L≥q/4, U≤2, and q≤1 bounds the coefficient of sqrt(D) by

   1024N/q³ + 24sqrt(N/q) + 4N ≤ 1052N/q³ ≤ 2048N/q³.

The intermediate comparison sqrt(N/q)≤N/q³ follows from q^5≤N. If no equality mask exists, this extracted C is necessarily a bad mask, even if its row degrees are irregular. Applying the discrete gap gives

   D ≥ [gamma q³/(2048N)]²
     = s^6/[2^22 N^10 d^(2phi(N)−2)].

The exponent 2^22 is 2048². The N^10 comes from N² in gamma², N^6 in q^6, and the remaining N² denominator. Writing the final expression as g=q^6/[2^22 N^4 d^(2phi(N)−2)] also shows

   g≤q/[2^22 N^4]<q/8, and g<1/N.

Both excluded easy branches therefore satisfy the same lower bound. This proves the claimed estimate for every admissible M, so taking the infimum is legitimate without any new attainment or compactness assumption. No condition-number bound on the original admissible class has been introduced: the temporary inverse bound follows automatically only in the near-floor branch.

## 6. Fresh independent exact controls

The new `fresh_controls.py` neither imports nor executes the candidate checker or either historical checker. It uses integer/rational arithmetic and its own rational-coordinate arithmetic in Q[x]/Phi_N for matrix multiplication, adjoints, and Gaussian elimination. SymPy supplies cyclotomic polynomials, exact polynomial inverses, and exact resultants. No floating-point norm threshold enters these tests.

The successful results are recorded in `FRESH_RESULTS.json`, `FRESH_RUN.log`, and empty `FRESH_RUN.stderr`:

- **29,625 labelled support masks:** Every column-labelled degree-three support avoiding singleton overlaps for N=3,...,7 was enumerated without component-based pruning. Counts were 1,24,0,200,29,400. Every support decomposed into the two claimed component types. Fourier-passing counts were 1,0,0,14,0.
- **Independent Fourier-only exhaustive search for N=3,...,9:** This second search imposed column weight three and exact column orthogonality, with no row-degree pruning. Its passing counts were 1,0,0,14,0,0,432. Row-regularity and all-triple decomposition were verified afterward for every passer. The N=3 result is a support-theorem control, not an s=0 optimization claim.
- **10,354,734 conference configurations:** Every normalized row triple and ordered column triple for each even N=2,...,20 was tested directly against the six congruences. No valuation or partial-phase pruning was used. None passed. Translation sets r_0=c_0=0, and simultaneous permutation of the remaining matched indices permits sorting the row triple without losing configurations.
- **4,203,692 triple-block tests:** For every row/column triple pair at N=4,...,20, exact Fourier orthogonality agreed with the four-congruence test. Arbitrary triple partitions were not assumed to work.
- **28 arbitrary sparse-inverse tests:** Every nontrivial budget at N=2,...,8 was tested using an explicitly invertible diagonally dominant inverse with the required support and arbitrary rational coefficients. Both inverse products and the exact row-rigidity, G(B), and mask-transfer identities passed. These are nonequality tests, independent of the divisor witnesses.
- **23 exact divisor witnesses:** Every proper divisor budget for N=2,...,12 passed both inverse products, both error Grams, both omitted-mask Grams, and all inverse support counts. The d=3 witnesses include N=6,9,12. Deliberately doubling the inverse failed the exact floor Gram in every case.
- **1,787 cyclotomic norm controls:** All root multisets of sizes 1 through min(3,N−1), at N=2,...,12, including repeated exponents, had zero norm exactly when the root sum vanished. Every nonzero norm was an integer of absolute value at least one.
- **44,850 budget pairs:** All N=2,...,300, 1≤s<N, passed rational checks of the final gap formula, exponent normalization, easy-branch domination, and the squared coefficient comparison. Additional rational a probes verified the displayed scalar inequalities without rounded square roots.
- **Negative controls:** A real order-four conference matrix passes ordinary orthogonality while its Fourier-filled support fails; an arbitrary dimension-six triple partition fails; a row-irregular bad mask has a nonzero cyclotomic Gram entry; and the wrong inverse gain fails floor equality.

These finite controls check formulas, support logic, normalizations, and proof mechanisms. The infinite results rest on the proofs above, not on extrapolation of the finite searches.

## 7. Scope and approved record delta

The candidate's proposed record update is accurate: codimension-three floor sharpness is completely classified, every weight-three equality mask has its full block support and phase test, and certified no-mask cases now have the displayed positive numerical squared-gap lower bound. The bound also applies to the already accepted odd codimension-two and prime-dimensional no-mask slices. It does not itself decide unclassified composite budgets.

No exact nonsharp optimizer, optimal gap size, condition-number-one theorem, cheap application algorithm, FFT improvement, free preparation/output claim, finite-word stability guarantee, arithmetic lower bound, or historical-priority claim follows from this review. The reconstruction M=q(A*)^(-1) can be dense and requires an inverse or equivalent solve. The parent's unresolved sparse-column and shared-frame limitations remain intact.

The independent review is complete. The candidate was not edited, and no GitHub, repository index, spreadsheet, or other external state was changed by this review.
