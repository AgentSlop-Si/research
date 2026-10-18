# Phase18 and inherited Phase17: independent audit

9 October 2026. Source: `fft_green_research_phase18_2026-10-09(1)`, including its recursively nested Phase17 and Phase16 checkpoints. Uploaded programs and tests were read only as data; none was executed or imported. Every fresh computation described below is in `independent_phase18.py`.

## Verdict and genuine changes to the master

The principal Phase18 theorems are correct within their stated models. The substantial nested Phase17 theorem is also correct, with a small but useful sharpening and one overstatement about sharpness corrected below. These additions do **not** establish an exact arbitrary-input sub-N-log-N Fourier algorithm or an unrestricted arithmetic lower bound.

New relative to the supplied master checkpoint:

1. **Independently ordered additive Green terms.** The common-order rank barrier extends to a sum of q independently conjugated banded inverses. A shared separated rectangle yields the necessary all-length condition `m_*² ≤ WN`, where `W=Σw_r` and this audit sharpens the source's group-size guarantee to `m_*=ceil(floor(N/2)/2^(q−1))`. There is also a uniform operator-norm approximation gap.
2. **Independent row/column order extension.** A new separate split lemma also covers independently permuted rows and columns within each Green term. Its guaranteed rectangle has size `floor(N/2^q)`, so the source’s original all-length exact and robust bounds survive in this larger additive model. Products remain outside the proof.
3. **Prime-length synthesis.** Combining that separator with the classical full-spark theorem gives the stronger necessary condition `N ≤ 2^q W+1` for prime N over the complex numbers. In particular, two independently ordered tridiagonal terms cannot equal a prime-length Fourier matrix for **any prime N≥11**, improving the source's sufficient exclusion threshold N≥29. For independently permuted rows and columns, the weaker necessary prime bound is `N≤2^q(W+1)−1`; two tridiagonal terms are excluded for primes N≥13. These are deductions within this audit, not claims of publication novelty.
4. **Harper functional calculus.** For `4|N`, the two zero modes prevent any scalar function of one Harper H from equaling F. Reflection resolves the ambiguity, with exact polynomial degrees `N/2` and `N/2−2`. The direct evaluator is quadratic.
5. **Exact phase-coherence certificates.** The two sparse intertwining equations characterize a two-dimensional span `span{F,FJ}`; one appropriate column selects F. Fixed outer Green factors can be rejected for every middle monomial using permutation-invariant diagonal and directed-cycle products.
6. **Positive and negative controls.** An unrestricted real orthogonal eigenbasis permits a single four-phase mask, but its pair-orthogonal-gate implementation still costs Ω(N log N). Products of two Green sums can regain full selected-block rank; our examples fail Fourier covariance in full rank.

The inherited Phase16 archive is **byte-identical** to the already-audited master source: SHA-256 `7bacbe5379aa168f8e7c8dcb5aeec55960791c391da2eadf6757b6c480384c04`. Its 330 recursive member occurrences agree. Thus its entropy theory is inherited, not a new Phase18 result, and the master’s adaptive-pivot repair must not be overwritten by the older source wording.

## 1. Models and conventions

Use normalized complex Fourier `F[j,k]=ω^(jk)/sqrt(N)`, `ω=exp(−2πi/N)`. Let `Z e_k=e_(k+1 mod N)`, `D e_k=ω^k e_k`, and `J e_k=e_(−k mod N)`. Then

`FZ=DF`, `FD=Z^(−1)F`, `F²=J`.

Exact finite-field checks below use the **unnormalized** W with entries ω^(jk). This avoids arbitrary modular square-root conventions. Consequently `W²=NJ`; polynomial coefficients and eigenvalues in those checks must be divided by sqrt(N) to compare with normalized complex F. Modular controls are not statements about numerical precision, complex matrix entropy, or finite-field full spark.

The goal remains computation of all coordinates for every fresh arbitrary input. A factorization is not an algorithm with the claimed runtime until coefficients, roots, routing, conversions, workspace, precision when relevant, and output work are accounted for.

## 2. Phase17 additive architecture: complete reconstructed proof

Assume

`A = Σ_(r=1)^q L_r P_r^(−1) B_r^(−1) P_r R_r`,

where each B_r is invertible with upper and lower half-bandwidth at most w_r, each P_r is a permutation, and L_r,R_r are arbitrary diagonal matrices. The same permutation acts on rows and columns within each term; different terms can use different orders. The terms need not be unitary, normal, mutually commuting, or well conditioned. Write `W=Σ_r w_r`.

### 2.1 Inversion preserves off-diagonal block rank

For any invertible B partitioned into a principal cut L|R, let G=B^(−1). A row vector y is a left annihilator of G_LR precisely when `(y,0)G=(z,0)` for some z. Multiplication by B gives `y=zB_LL` and `zB_LR=0`.

The map `z↦zB_LL` is injective on the left kernel of B_LR: if both zB_LL and zB_LR vanish then `(z,0)B=0`, hence z=0. Conversely each such z yields a left annihilator of G_LR. Their left-nullity dimensions agree, so `rank G_LR=rank B_LR`. Reversing the blocks gives the opposite direction. This proof requires no invertibility of the principal diagonal blocks; the checker includes an invertible swap matrix with singular principal blocks.

For a contiguous cut of a bandwidth-w matrix, the crossing block has at most w nonzero boundary rows or columns, hence rank at most w. Subselections and diagonal gauges cannot increase rank.

### 2.2 A common separated rectangle, with the rounding sharpened

In the first of q orders, take the first and last `floor(N/2)` labels as R,C. They have equal size and are separated in that order.

Suppose R,C have size m. In the next order, sort their 2m distinct labels, and split after the first m. If a members of R are in the left half, exactly a members of C are in the right half; the reverse orientation has m−a members of each color. Retain the larger opposite-color pair. Both new groups have size at least `ceil(m/2)`, are separated in the new order, and remain separated in all earlier orders because they are subsets.

Iterating gives

`|R|=|C| ≥ m_* := ceil(floor(N/2)/2^(q−1))`.

The identity `ceil(ceil(a/2)/2)=ceil(a/4)` gives the closed form. This is at least the source's `floor(N/2^q)`. The proof is constructive, requires no randomness, and works for all N≥2 and q≥1.

In each term of A, its R×C block lies within one crossing block in that term’s own order. Therefore

`rank A[R,C] ≤ W`.

### 2.3 All-length exact obstruction and robust gap

For any m×m submatrix X of normalized complex Fourier, flat entry modulus and unitarity give

`||X||_F²=m²/N`, and `||X||₂≤1`.

Thus `rank X ≥ m²/N`. Taking separated groups of exactly m_* coordinates proves

`A=F  ⇒  m_*²≤WN`.

When `2^q|N`, this specializes to `N≤4^qW`. For q fixed-width tridiagonal terms, W=q, so a sublogarithmic term count cannot work at growing N. This is an **additive representation/term-count** restriction. It is not a scalar-operation lower bound for every possible shared computation DAG evaluating such a sum.

For `m=m_*>W` and `m²>WN`, let σ_j be X's decreasing singular values. Since σ_j≤1,

`m²/N ≤ W+(m−W)σ_(W+1)²`.

Any rank-W approximation Y to X has `||X−Y||₂≥σ_(W+1)`. The full error dominates this submatrix error, yielding

`||A−F||₂ ≥ sqrt[(m_*²/N−W)/(m_*−W)]`.

For fixed q and fixed widths, this bound tends to `2^(−q/2)`. At q=2 the limit is 1/2. This complex operator-norm theorem has no conditioning hypothesis on A. The argument also applies to every normalized complex Hadamard matrix. The conditions for a positive bound must be stated; outside them it does not assert positive error.

### 2.4 Prime-length strengthening

For prime N over characteristic zero, every square Fourier minor is nonsingular. This is the classical Chebotarev result; a primary proof is [Tao, Lemma 1.3, *An uncertainty principle for cyclic groups of prime order*](https://arxiv.org/html/math/0308286v3).

Consequently the separated m_*×m_* Fourier block has rank **m_***, not merely at least m_*²/N. Exact equality requires

`ceil(floor(N/2)/2^(q−1))≤W`.

For integer W this is equivalent to

`floor(N/2)≤2^(q−1)W`, hence `N≤2^qW+1`.

For tridiagonal terms, W=q. Two terms require prime `N≤9`; therefore all primes N≥11 are excluded. Three terms require prime `N≤25`; all primes N≥29 are excluded. Four terms require prime `N≤65`; all primes N≥67 are excluded. At prime lengths and fixed bandwidth, this yields `q≥(1−o(1))log₂N` as a term-count bound.

The source instead combines a much smaller common monotone chain with full spark, giving `N≤(2W+1)^(2^(q−1))`. That statement is valid but needlessly weaker: its own balanced-separator lemma can be substituted directly. **The improved full-spark statement is over C/characteristic zero; it is not an assertion that arbitrary finite-field Fourier matrices are full spark.** The checker's nonzero modular minors are individual one-way certificates at explicitly selected good primes, not a substitute for the all-prime complex proof.

### 2.5 Correcting the advertised bisection sharpness

The source's adversarial interleaving example demonstrates that **its greedy procedure** can return `N/2^q`. It does not establish that no larger groups are separated in all orders, nor that the universal best separator constant is optimal.

A direct counterexample to that inference is N=8, with orders

`0,1,2,3,4,5,6,7` and `0,4,1,5,2,6,3,7`.

The prescribed greedy procedure returns size 2. But `R={0,1,4}` and `C={5,6,7}` are separated in both orders and have size 3. Thus “sharpness of the bisection constant” must be phrased as sharpness of the displayed **greedy recurrence on those instances**, not extremality over all choices of separated groups. The main existence theorem is unaffected.

### 2.6 Remaining Phase17 special cases and escape controls

- **Common path order:** all crossing ranks add to at most W at a fixed half-cut. A consecutive half-size Fourier block is Vandermonde and has full rank. Thus W≥floor(N/2). For tridiagonal terms this is the existing common-order q≥floor(N/2) obstruction, already represented in the master.
- **Bluestein/shift-resolvent subfamily:** for even N, let ξ=exp(−πi/N) and `c_t=ξ^(−t²)`. Then c is N-periodic and `ω^(jk)=ξ^(j²)c_(j−k)ξ^(k²)`. Its size m=N/2 Hankel block factors into invertible diagonal factors and a Vandermonde matrix on distinct nodes ω^(−a), so has rank m. A kernel of `(I−αZ)^(−1)` with α^N≠1 is proportional to α^t; over indices a+b≤N−2 its Hankel block has rank at most one. A sum of q such resolvents therefore needs q≥N/2. This is a special commuting shift-resolvent family, not all graph Green operators.
- **Products are a genuine escape from the additive proof:** our freshly generated two-sum products have selected cut ranks 4,8,17 at N=16,32,64, versus additive rank 2. Their Fourier covariance defects have full ranks 16,32,64. These are new controls, not reproductions of the source's random sample values. Four banded solves suffice to apply such a product at bounded width, but these matrices are not Fourier.
- **Architecture scope matters:** the uploaded proof excludes independent row/column permutations within one summand, but the new argument immediately below closes that particular escape. Arbitrary non-diagonal outer mixing matrices, products of sums, and more general shared-state DAGs remain outside these additive proofs.

### 2.7 New extension: independent row and column permutations

The same **original floor-sized** all-length obstruction extends to

`A=Σ_r L_r P_r^(−1) B_r^(−1) Q_r R_r`,

where P_r and Q_r may now be independent. The sharper ceiling bound in §2.2 is not asserted for this larger model.

Maintain a set I of original row labels and a set J of original column labels, initially both all N labels. Their overlap is permitted: Fourier minors require distinct labels within each side, not disjoint row and column sets. In one term’s inverse-coordinate system, sort their positions as

`r_1<…<r_m` and `c_1<…<c_m`.

For m≥2, put `k=floor(m/2)`. At least one of these two strict inequalities holds:

`r_k<c_(m−k+1)` or `c_k<r_(m−k+1)`.

If both failed, strict ordering within the two lists would imply

`r_k≥c_(m−k+1)>c_k≥r_(m−k+1)>r_k`,

a contradiction. In the first case retain the first k rows and last k columns; in the second retain the last k rows and first k columns. The retained inverse-coordinate positions are strictly separated by a principal cut. All earlier separations persist because only subsets were retained. After q stages, `|I|=|J|=m_0=floor(N/2^q)`. If an intermediate m<2, the guaranteed final size is zero and the resulting assertion is vacuous.

Each term’s selected inverse block has rank at most its bandwidth, even though the original labels I,J may overlap. Thus `rank A[I,J]≤W`. Applying exactly the Fourier block arguments above yields

`A=F ⇒ floor(N/2^q)^2≤WN`,

and, when `m_0>W` and `m_0²>WN`,

`||A−F||₂≥sqrt[(m_0²/N−W)/(m_0−W)]`.

For prime N over C, full spark strengthens this to `m_0≤W`, equivalently

`N≤2^q(W+1)−1`.

For q tridiagonal terms, the first excluded primes from this independent-row/column theorem are 13 for q=2, 37 for q=3, and 83 for q=4. The stronger conjugate-order thresholds 11,29,67 belong to §2.4; they must not be substituted here. No universal optimality of either separator size is claimed.

The additional checker exhausts the local inequality over all equal-sized position subsets of a six-position universe, tests 384 random full independent-order systems, and verifies exact individual and sum cut ranks on independently row/column-permuted Green examples at N=13,37,83,64. Individual prime-case Fourier minors are certified nonzero at the displayed good moduli. This closes only the independent-row/column additive escape; it does not cover products or unrestricted shared-state computation.

## 3. Phase18 Harper/parity theorem

Let `T=Z+Z^(−1)`, `V=D+D^(−1)`, `H=T+V`. Fourier exchanges T,V, hence commutes with H and anticommutes with T−V. H is real symmetric and cyclic tridiagonal, with O(N) application work.

For N=4m, the reflection-even and reflection-odd orthonormal bases give real Jacobi blocks of dimensions `N/2+1` and `N/2−1`. Their potentials are `v_j=2cos(2πj/N)`. The even block has endpoint off-diagonal weights sqrt(2) and interior weights 1; the odd block has all weights 1. Nonzero off-diagonals ensure simple real spectra: an eigenvector is fixed by its first component and the three-term recurrence, and cannot have zero first component.

Signed reversal conjugates each block to its negative: its diagonal potential changes sign on reversal, while alternating signs negate the symmetric off-diagonal weights. Both dimensions are odd, so each block has a zero eigenvalue; simplicity makes each zero line one-dimensional. Therefore H has exactly two zero modes, one in each parity sector.

F preserves each zero line. Because F²=J, its even zero-line eigenvalue is ±1 and its odd zero-line eigenvalue is ±i. A scalar spectral function of H must act equally on both zero lines; F does not. No scalar f(H) exists, including rational p(H)/q(H) with q(H) invertible. Adding unrelated noncommuting operators is outside that restriction.

Within each parity sector, simple spectrum and commutation imply unique interpolating polynomials of degrees below the corresponding sector dimensions:

`F=p_+(H)(I+J)/2+p_−(H)(I−J)/2`.

These degree upper bounds are attained:

- Coordinates 0 and N/2 are graph distance N/2 in the cycle. Lower powers of H have zero in this entry, while F has entry 1/sqrt(N). Reflection fixes both endpoints, so the odd projector contributes zero. At degree N/2 there are exactly two shortest paths, each of weight one. Thus `deg p_+=N/2` and its leading coefficient is `1/(2sqrt(N))`.
- In the odd Jacobi basis, the first and last coordinates are distance N/2−2, with all path-edge weights one. The Fourier entry is `(ω^(N/2−1)−ω^(−(N/2−1)))/sqrt(N)=−2i sin(2π/N)/sqrt(N)`, nonzero. Thus `deg p_−=N/2−2`, with that leading coefficient. This includes N=4, where the odd polynomial has degree zero.

Direct sparse Horner evaluation takes Θ(N²) arithmetic. Polynomial degree is not a lower bound for all arithmetic circuits: alternate algebraic evaluators, rational functions in larger algebras, and noncommuting shared constructions require separate analysis. Linear-time application of a single shifted cyclic-tridiagonal resolvent also does not turn this entire degree-N/2 polynomial into a linear-time Fourier algorithm. Any claimed solver runtime must handle its actual pivoting/regularity conditions.

The basic commuting Harper operator, parity decomposition, and Fourier eigenbasis are established earlier work. The author-hosted [Barker–Candan–Hakioğlu–Kutay–Ozaktas paper (2000)](https://users.metu.edu.tr/ccandan/pub_dir/frft_withbarker00.pdf), particularly Section 2, documents these structures. It also discusses the known double-zero phenomenon. This audit proves the project’s exact degree statements directly and makes no novelty claim.

## 4. Sparse intertwiners and calibration

For every even N≥4, the joint complex commutant of T,V is `span{I,J}`.

In the parity basis, V is diagonal with strictly distinct values in each block, since cosine is strictly decreasing between 0 and π. A commuting X therefore has diagonal same-parity blocks. Commutation with the irreducible Jacobi T blocks forces these diagonals to be constant. A cross-parity block can only connect matching interior potential values. The first even endpoint is absent from the odd block; its commutator equation forces the first possible cross coefficient to zero. Successive neighboring equations force all the rest to zero. Hence X is scalar on each parity sector, equivalently aI+bJ.

For any M, including singular or nonunitary M, suppose

`MT=VM` and `MV=TM`.

Then `X=F^(−1)M` commutes with T,V. Indeed Fourier exchanges those two operators, so multiplying either intertwiner on the left by F^(−1) gives the corresponding commutator. Thus `M=F(aI+bJ)`.

If additionally `M e_1=F e_1`, then `(a−1)e_1+b e_(N−1)=0`. Those coordinates are distinct for N≥4, so a=1,b=0 and M=F. Calibration at e_0 **does not suffice**, since Je_0=e_0. The checker confirms ranks 2 and 1 respectively for these two column choices.

This is a useful **symbolic proof target**. Verifying the two full matrix equations from black-box application alone can still require many probes. It is not a deterministic sublinear black-box equality test. The usual stronger Weyl relation `MZ=DM` plus a correct first column is another sufficient certificate.

## 5. Fixed-factor middle-monomial veto

Let A,B be fixed and invertible and seek `F=A Q P B`, where Q is diagonal and P is a permutation. Since F,A,B are invertible, any successful Q is automatically invertible. Fourier covariance requires

`U(QP)=(QP)V`, where `U=A^(−1)DA` and `V=BZB^(−1)`.

Therefore U,V must be monomially similar. Similarity by a diagonal preserves every directed cycle product; conjugation by a permutation only relabels its vertices. In particular both of these multisets must agree:

`{U_ii}_i = {V_ii}_i`,

`{U_ij U_ji}_{i<j} = {V_ij V_ji}_{i<j}`.

Any mismatch rejects **every middle diagonal and every middle permutation for those fixed A,B**. Equality is only necessary. It does not certify the full covariance, and even covariance still needs calibration to select Fourier.

With a prescribed permutation (including P=I), diagonal similarity is exactly a graph-potential problem. Supports must match and every nonzero position requires `q_i/q_j=U_ij/V_ij`. Propagate a nonzero potential on each connected component; reject inconsistent cycles, including self-loops. This returns all solutions up to one nonzero component scaling. Graph inspection is O(N²) for dense U,V after they are formed; computing U,V can already require expensive dense work.

The independent checker reconstructs the source’s four fixed cyclotomic stage specifications from their published seed/coefficient protocol, using newly written pivoted linear algebra. N=8,16,32,64 each fails both multiset tests. All A,B modular inverses are explicitly multiplied back to identity. The raw A B products violate Weyl covariance at all N² entries. Compact second-moment witnesses already suffice:

- N=8: Σ U_ii² = 72702970, Σ V_ii² = 313892487
- N=16: 617093740 versus 173844115
- N=32: 342874219 versus 730189029
- N=64: 130546465 versus 269819468

All displayed values are modulo 998244353. These are permutation-invariant sums of **squares of diagonal entries**, not traces of U² and V². The latter would agree because U,V are both similar to the respective Weyl generators.

A modular mismatch lifts to a characteristic-zero contradiction when the cyclotomic root reduction is valid and all denominators in A,B,U,V remain nonzero at that reduction. Here the exact-order root and verified inverses provide those checks. If a characteristic-zero equality of invariant multisets existed, its elementary symmetric polynomials would reduce equally; the modular mismatch contradicts that. No such one-way lift is valid at a singular/bad reduction, and modular agreement never proves a characteristic-zero identity.

These are **four fixed-instance exclusions**, not an all-parameter impossibility theorem for Green sums. Dense inversions in the audit are offline verification, not a fast transform executor. Positive diagonal and permuted controls prevent a vacuous rejection rule; a transpose example also demonstrates that the short invariants do not suffice for a fixed-permutation diagonal similarity.

## 6. Four-phase spectral control and inherited entropy

Real and imaginary parts of complex symmetric unitary F are commuting real symmetric matrices. A real orthogonal O simultaneously diagonalizes them. Because F⁴=I,

`F=O diag(±1,±i) O^T`.

The parity Harper eigenbasis supplies such an O explicitly. This is algebraically compatible with one quaternary central mask, but no fast evaluator for its generally dense O has been supplied. Restricting central phases does not restrict the algebraic coefficients of the outer basis to the old small coefficient fields.

If O uses g two-coordinate orthogonal gates, then O, its inverse, and the free central phase mask implement F with at most 2g two-coordinate complex-unitary gates. Matrix entropy starts at zero and ends at N log₂N; one pair-unitary gate changes it by at most two bits because it preserves each column’s pair mass, and the total mass in the two rows is two. Therefore

`g≥N log₂N/4`.

This is an inherited application of [Ailon's unitary-gate entropy model](https://arxiv.org/abs/1305.4745), **not** an unrestricted arithmetic lower bound on applying O.

The identical nested Phase16 source does not undo prior audit corrections or extensions:

- Phase15 normalized factor entropies remain `N log₂B`, `N−B`, and `B+N(log₂L−1)`. Their particular gate-by-gate Fourier construction is entropy-optimal in the pair-unitary model.
- A path Cayley has rank≤1 across each lower contiguous cut. A zero-safe descending sweep selects any nonzero prefix column, not a fixed column; it needs at most N−2 pair rotations to become Hessenberg, followed by N−1 to become diagonal. Thus its existence bound is 2N−3 gates.
- The source's fixed nearest-column rule fails for the 4×4 permutation swapping coordinates 0 and 3 and fixing 1 and 2: the chosen column is zero although a preceding prefix column is nonzero. The master’s adaptive-prefix repair remains necessary for the generic lemma.
- A Haar sandwich needs `3N/2−2` pair gates; with two path Cayleys a stage uses at most `11N/2−8`. Therefore an exact Fourier product needs `t≥ceil[N log₂N/(11N−16)]`. No linear-time coefficient-preparation theorem follows from gate existence.
- Zero-initialized unitary ancillas still obey the two-bit bound via the effective input-to-register isometry. Nonunitary copying or sharing is a different model.
- The master’s entropy-continuity extension survives: for exactly unitary outputs within fixed operator-norm error ε<1, or relative Frobenius error ε, the stage count remains Ω(log N). With `τ=min(ε,1−1/N)`, the stated lower numerator is `N[log₂N−h₂(τ)−τ log₂(N−1)]` over denominator `11N−16`.

The old uploaded regressions were not rerun. Source equality and the previous independent master audit preserve the already-established provenance; the new checker separately validates the Phase18 spectral identities numerically.

## 7. Independent tests, portability, and limits

Run from any directory:

`OPENBLAS_NUM_THREADS=1 python independent_phase18.py`

Optional source verification:

`OPENBLAS_NUM_THREADS=1 python independent_phase18.py --source-root PATH_TO_PHASE18_DIRECTORY_OR_OUTER_ZIP`

Python 3, NumPy, and SymPy are required; the audit used NumPy 2.3.5 and SymPy 1.14.0. The mathematical checker has no dependency on the original workspace or source modules. It writes results next to itself unless `--output` is supplied. The source option reads and hashes archive bytes; it never imports them, extracts executable modules, or runs source tests.

Fresh verified coverage:

- All-entry exact Harper polynomial reconstruction at N=4,8,12,16,20,28,32,36,60,64,128; sector nullities, leading coefficients, and inequivalent zero-line Fourier eigenvalues.
- Exact joint-commutant dimensions at N=4,6,8,10,12,16,20,32,64, with calibration controls.
- Four independently reconstructed source middle-monomial veto instances, and synthetic valid-diagonal/permutation controls.
- 5,424 separator checks, including every second ordering at N=7; the greedy-sharpness counterexample; individual nonzero prime Fourier minors at N=11,13,17,29,67.
- Independent row/column split and rank checks described in §2.7, with overlapping original row/column label sets explicitly allowed.
- Three new Green-product rank-escape controls; exact chirp identities and Hankel ranks at N=8,16,32,64,128.
- Numerical real-orthogonal four-phase reconstructions at nine lengths through 128, including non-dyadic lengths. Maximum observed entry error was about 2.86e−15. Numerical singular-value checks support three robust-gap cases; these floating-point checks are not exact certificates or finite-precision implementation guarantees.
- Recursive source-content inventory preserves all 382 non-directory member occurrences of the outer Phase18 ZIP, including the embedded Phase17 ZIP itself and nested repeated history. The initial 381 count omitted that embedded ZIP member while counting its contents; the inventory and results are corrected. The branch checker validates 238 entries in its recognized `SHA256SUMS.txt`/`MANIFEST.sha256` files. That is a branch-checker subset, not the central three-archive total of 714 successfully checked manifest entries. The authoritative complete cross-archive inventory is the supplement’s `SOURCE_MEMBER_INVENTORY.json` and `recursive_summary.json`; these are not recounts of unique Library items.

## 8. Bounded next step and stopping condition

This audit stops after reconstructing the stated proofs, correcting scope/rounding, adding the prime-length consequence, and executing the finite independent controls. No unbounded search was started.

The remaining constructive target is precise: an explicitly parameterized nonunitary product or shared-state construction outside the additive and pair-unitary models, with symbolic sparse intertwining or full Weyl covariance, correct calibration, and a complete charged evaluator. A candidate that merely has high cut rank, commutes with H, passes short monomial invariants, or fits a few numerical inputs has not met that target. The exact arbitrary-input sub-N-log-N question remains unresolved.
