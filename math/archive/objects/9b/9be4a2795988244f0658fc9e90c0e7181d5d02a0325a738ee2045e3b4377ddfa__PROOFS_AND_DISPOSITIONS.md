# Q18/Q19 independent intake audit

Date: 2026-10-10. Status: mathematical reconstruction complete at the scopes below; independent reviewer acceptance tracked separately. Supplied programs were read as inert text only. None was executed, imported, or AST-parsed. `fresh_checks.py` is independently authored and runs only its own definitions and ordinary installed libraries.

## Executive disposition

- **Q18:** the support/dense-cell/exponent obstruction is correct for the stated odd local ring and a coherent Heisenberg/Weil convention. The supplied upper-shear association has a real sign error: `rho(U(E))=F^-1 C_(-E) F`, not `F^-1 C_E F`, under the other stated conventions. All valuation/support/order conclusions survive this repair. The character-table obstruction is a corollary of established classification, with a direct primary comparator below. Finite source test claims were not rerun.
- **Q19:** the Phase18 energy, phase-gauge distance, forest/rank, and rank-k Frobenius bounds are valid under explicit constituent-inverse, common-gauge, norm, and occurrence-count hypotheses. The inherited spectrum and Phase17 gauge floor are reconstructed here, not merely presumed from a source label. The `O(E)` certificate exists in exact scalar arithmetic; the supplied floating implementation does not establish rigorous finite-precision certification.
- **NF01:** preserve a common rejection interface, not a new composite-architecture theorem. Cross-ratio invariants do not propagate through arbitrary matrix products. Odd-primary Weil and dyadic primitive-holonomy families have different literal dimension domains. Their conjunction does not produce a new FFT lower bound.

## 1. Frozen Q18 field and representation contract

Let `p` be odd prime, `s,n>=1`, `q=p^s`, `V=(Z/qZ)^n`, `Q=q^n`, and `psi(t)=exp(2 pi i t/q)`. On complex functions on V use

- `T_a f(x)=f(x-a)`;
- `M_b f(x)=psi(b^T x)f(x)`;
- `H(a,b)=psi(-a^T b/2) M_b T_a`;
- `F[x,y]=Q^(-1/2)psi(x^T y)`;
- `C_E[x,x]=psi(x^T E x/2)` for symmetric E;
- `P_M f(x)=f(M^-1 x)` for invertible M.

Their direct covariance is `F H(v)F^-1=H(Wv)`, `C_E H(v)C_E^-1=H(L(E)v)`, and `P_M H(v)P_M^-1=H(G(M)v)`, with the source's `W=[[0,-I],[I,0]]`, `L(E)=[[I,0],[E,I]]`, `G(M)=diag(M,M^-T)`. Checking the translation and modulation generators establishes all three identities; the centered half-phase then makes covariance exact. A covariance implementer is unique up to scalar because the H(a,b) span the complete matrix algebra: modulation orthogonality isolates diagonal matrix units and translation supplies every other matrix unit. Standard finite Heisenberg theory provides the implementers for all symplectic S. Ladisch §3, Proposition 3.3 and §4, Theorems 4.1/4.3, supplies this precise projective/linear representation framework.

Projective scalar choices do not affect any invariant here. For exact finite-field controls one may replace C by a field of characteristic different from p containing a primitive qth root, and use unnormalized F with its exact algebraic inverse. Complex absolute-value assertions are not transferred to finite fields.

### 1.1 Support theorem, with a stronger equality

Write `S=[[A,B],[C,D]]`. Covariance for `v in ker B` gives `K M_v=M_(Dv) K`, so nonzero `K[x,y]` implies `v^T y=(Dv)^T x` in Z/qZ for every v in ker B. Thus a row is contained in one coset of `(ker B)^perp`, of size `|im B|`.

There is also equality, not just an upper bound. Inverse covariance for output modulation b uses
`S^-1(0,b)=(-B^T b,A^T b)`.
The corresponding identity moves the input column by `B^T b`, multiplying entries only by nonzero character factors. Hence the support of each row is invariant under `im B^T`. Perfect-pairing duality gives `im B^T=(ker B)^perp`. A row is nonempty since K is invertible, so it is exactly that coset and has exactly `|im B|` entries. In the normalized complex representation their absolute values are all `|im B|^-1/2` by unitarity.

Consequently B noninvertible gives zeros, whereas B invertible permits full support. This is an all-size proof, not an inference from random words.

### 1.2 Dense cell and explicit normalized kernel

Direct block multiplication gives
`S=L(DB^-1) G(-B) W L(B^-1 A)`.
Symplectic relations imply `DB^-1` and `B^-1 A` symmetric and the remaining block is `C=DB^-1 A-B^-T`. Therefore, for a unit-modulus projective scalar mu,

`K_S(x,y)=mu Q^-1/2 psi( x^T DB^-1 x/2 - x^T B^-T y + y^T B^-1 A y/2 )`.

This is a row chirp, invertible coordinate permutation, additive Fourier, and column chirp. Dense iff B is invertible is proved. Monomial *equivalence* costs O(Q) to apply once the Q phase entries/permutation route are supplied; constructing n-variable quadratic phases and routes, matrix inversions, roots and precision is separately charged. Nothing here proves a sub-Q log Q algorithm.

### 1.3 Actual upper-shear error and exact counterexample

Block multiplication gives `W^-1 L(E) W=U(-E)`. Thus the source's Section 3 and `upper_shear_operator_nd` associate the wrong S to their otherwise well-defined Gauss kernel. Correct formula:

`rho(U(E))=F^-1 C_(-E) F`.

Over F7 at q=3, zeta=2, n=1, E=1, the source formula has diagonal 3 and off-diagonal 6. The correct formula has diagonal 4 and off-diagonal 2. The dense Bruhat formula for U(1) has diagonal 1 and off-diagonal 4. The corrected matrix is four times Bruhat; the source matrix is not projectively equal. These are exact residues, independently regenerated in `fresh_check_results.json`.

This rejects the unchanged association, not the corrected dense/sparse obstruction. A scalar normalization cannot remove the error. Either rename the source Gauss kernel U(-E), or negate E in its chirp.

### 1.4 Completed-square valuation theorem

For a diagonal entry `e=p^v u`, `0<=v<s`, put `g=p^v`, `r=q/g`, and `eta=psi(g)`. The coherent upper-shear kernel is
`q^-1 sum_z psi(-e z^2/2+(y-x)z)`.
Translation by r in the summation shows it vanishes unless `x=y mod g`. On one residue block write `x=a+gX`, `y=a+gY`; it equals

`r^-1 G_r(-u/2) eta^((Y-X)^2/(2u))`,
`G_r(-u/2)=sum_(z mod r) eta^(-u z^2/2)`.

The usual change `(z,t) -> (z-t,z+t)` is invertible for odd r and proves `|G_r(-u/2)|^2=r`: the inner character sum vanishes unless the first coordinate is zero. Thus this is a nonzero scalar times diagonal phases and a permuted `F_r` core. If e=0, the factor is identity. Tensoring coordinates gives `p^(sum v_i)` blocks and support `p^(sum(s-v_i))` per row and column. Cross ratios of each nontrivial tensor core lie in roots of order `p^max(s-v_i)` and an active coordinate attains that order. For the all-zero E identity cell, order 1 is a convention (or obtained by repeated-index ratios); there is no nonzero rectangle with two distinct rows and two distinct columns.

Congruence diagonalization is valid: take an entry with minimum p-adic valuation. If it is off-diagonal and no diagonal has that valuation, the quadratic value on `e_i+e_j` does, since 2 is a unit. This gives a primitive vector with that value. Extend it to a basis and remove other first-row/column entries by multiples of it, which is possible after dividing by the common valuation. Recurse. This proves the stated symmetric-form reduction, including degenerate forms. Ladisch §7, Corollaries 7.3/7.4 and the following Gram-Schmidt observation provide a matching classical antecedent.

### 1.5 Exponent and word closure

For a nonzero matrix define a four-entry ratio as `M_xy M_x'y'/(M_xy' M_x'y)`. Monomial equivalence preserves the set of all such ratios, rather than the value at an unchanged pair of indices. Additive Fourier on V has ratios `psi((x-x')^T(y-y'))`, all of order dividing q. Cyclic Fourier of dimension Q has a primitive Q ratio. Therefore Q>q excludes equivalence. Sparse cells are excluded by zero support first. Products of genuine Weil operators collapse projectively to a single S, so the same obstruction excludes every such finite word, even with external monomial decoration.

This does **not** allow arbitrary extra monomial matrices between Weil factors: arbitrary coordinate permutations/diagonals need not be Weil operators. Nor does it cover an invariant-subspace embedding or extraction map.

The finite-abelian p-group extension follows from exponent versus order. In fact the same implication holds for any finite abelian group: if its exponent is smaller than its order, its character table lacks the primitive full-order ratio; exponent equals order iff that abelian group is cyclic.

### 1.6 Rank budget

Modulo p, `B(ST)=A(S)B(T)+B(S)D(T)` gives `rank B(ST)<=rank B(S)+rank B(T)`. The additive full Fourier element needs total rank at least n. Coordinate Fourier swaps attain n. A specified radix-p implementation with p q s charged multiply-add terms per q-point transform costs p Q n s over all coordinates. This validates a literal schedule and a structural rank budget, not an arithmetic lower bound for arbitrary implementations of individual stages.

## 2. Frozen Q19 contract and complete dependency check

Let even `s>=4`, `N=s^2`, `h=s/2`, `tau(sx+y)=sx+(y+h mod s)`, Pi its involutive permutation, and `U[k,j]=exp(-2pi i k j/N)/sqrt N`. Every supplied pi_(l,t) must be a genuine permutation commuting with tau. `P[i,pi(i)]=w_i`, `G=(I-P)^-1` exists, `L_l=sum_t alpha_(l,t)G_(l,t)`, `T=L_m...L_1`, `m>=1`. Define `a=max_l sum_t |alpha|`, `A=sum |alpha|`, `g>0` bounding every actual G and, when used, every reference G0. For `A=0`, T=0 and Fourier equality is trivially excluded; energy thresholds with division by A are only stated for A>0. Put `B=(ag)^(m-1)g^2`.

### 2.1 Half-grid spectrum independently reconstructed

Factor U by Fourier-transforming x into b, multiply by `omega_N^(by)`, and Fourier-transform y into a, with output index sa+b. The input half-shift is on y and the output half-shift on b. Thus `V=Pi U^-1 Pi U` is conjugate to the monomial

`W e_(b,y)=omega_N^((b-tau_s(b))y) e_(tau_s(b),tau_s(y))`.

Writing `tau_s(t)-t=h epsilon_t`, applying W twice gives `omega_N^(h^2 epsilon_b epsilon_y)=+i or -i`, half of the N positions each. The map pairs positions into two-cycles, so each sign contributes both square roots equally. Hence the four primitive eighth roots occur N/4 times and `V^4=-I`. It follows that `[U,Pi]` has singular values `sqrt(2+sqrt2)` and `sqrt(2-sqrt2)`, N/2 of each, squared Frobenius norm 2N and full rank.

### 2.2 Phase17 gauge floor reconstructed, with scope kept exact

For monomial Q,R the equality `FQ=RF` entrywise forces both underlying permutations to be affine: evaluating the entry identity at j=0 and k=0 removes the scalar phases, then j=1 and k=1 force `tau(j)=u j+b`, with u a unit. The half-grid tau is not affine for s>=4: tau(0)=h, tau(1)=h+1 would force j+h, contradicted at j=h. This proves exact exclusion for arbitrary invertible external diagonal gauges. For s=2 the affine exception is real.

For the numerical floor require unitary diagonals. Put `rho=2/(s sin(pi/s))`, `H[k,j]=omega_N^(k tau(j)-tau(k)j)`. Partition by epsilon_j in {+1,-1}. Each of the four sign blocks has rank one, since its entries are `alpha^(f k) alpha^(-e j)`, alpha=omega_N^h. Normalized within-sign overlaps have modulus rho from a length-h geometric series, with opposite signs on the two groups. After rephasing, the two 4x4 Gram matrices are

`A=[[1,rho,0,0],[rho,1,0,0],[0,0,1,-rho],[0,0,-rho,1]]`,
`B=[[1,0,rho,0],[0,1,0,-rho],[rho,0,1,0],[0,-rho,0,1]]`.

Their product has characteristic polynomial `(lambda-(1+rho)^2)(lambda-(1-rho)^2)(lambda-(1-rho^2))^2`. This was also verified by our own exact symbolic calculation. H therefore has norm `N(1+rho)/2` and the source's four nonzero singular values. For unit-modulus a,b,
`||H-ab^T||_F^2 >= N^2(1-rho)`.
For Q=D_in Pi D_in^-1 and R=D_out Pi D_out^-1 this yields `||UQ-RU||_F^2>=N(1-rho)`. Any T0 commuting with Pi gives `T_g=D_out T0 D_in^-1` intertwining Q,R, hence

`||U-T_g||_F/sqrt N >= (1/2)sqrt(1-rho)=g_s`.

The operator norm is at least the relative Frobenius norm. This proves the dependency Phase18 needs. It does not transfer the metric bound to nonunitary gauges.

### 2.3 Raw energy theorem

The commuting permutation support gives
`||[P,Pi]||_F^2=sum_i |w_i-w_tau(i)|^2`.
The exact identity `[G,Pi]=G[P,Pi]G`, the product commutator rule, `||L_l||_2<=ag`, and the triangle inequality imply
`||[T,Pi]||_F <= B sum_(l,t) |alpha| ||[P,Pi]||_F`.
Weighted Cauchy-Schwarz gives `B sqrt(A E_tau)`, where E_tau is exactly the source energy. Since
`sqrt(2N)<=2||U-T||_F+||[T,Pi]||_F`,
all Theorem18.1 displayed floors and exact-equality energy requirements follow. Constants a,A,g,m must stay bounded to infer Omega(N). This has no implication that changing Omega(N) edges costs superlinear work.

### 2.4 Flat reference and norm propagation

Use one common unitary D across all occurrences and `w0_i=c_(l,t)d_i/d_pi(i)`. Then `P0=D(c P_pi)D^-1`; each inverse exists by hypothesis; the full T0 is D times a Pi-commuting network times D^-1. The constituent identity
`G-G0=G(P-P0)G0`
and product telescoping give
`||T-T0||_F<=B sum |alpha| ||P-P0||_F<=B sqrt(A E_flat)`.
Combine with §2.2 and triangle inequality. This proves Theorem18.2 for every admissible reference and therefore for the infimum over any such uniformly norm-bounded reference family. A minimum can be used when attained. Distances are gauge invariant when actual weights and the reference/gauge are transformed together; a supplied reference need not minimize that distance.

A useful instance-specific classical strengthening is obtained by retaining exact prefixes/suffixes: replace B inside each term by `Gamma_(l,t)=||L_m...L_(l+1) G_(l,t)||_2 ||G_(l,t) L_(l-1)...L_1||_2` for the raw commutator. Then `||[T,Pi]||_F<=sum |alpha| Gamma d <=sqrt((sum |alpha|Gamma)(sum |alpha|Gamma d^2))`. For flat telescoping use actual suffixes and reference prefixes, with G and G0 on their matching sides. Norm discovery is charged; this is a standard sharper estimate, not a new uncharged implementation theorem.

### 2.5 Rank-k floors and independent review of sharpened operator bound

If `T=T0+Delta`, `[T0,Pi]=0`, `rank Delta<=k`, then `[T,Pi]` has rank at most 2k. Removing the largest 2k values of the spectrum in §2.1 and dividing the squared remaining sum by 4N gives precisely the two Phase18 piecewise Frobenius formulas. For k>=N/2 the floor is zero. Exact equality requires k>=N/2 without conditioning.

Separately, for **any unitary** input/output phase gauges, set `E=UQ-RU`, so `||E||_F^2>=N(1-rho)` and `||E||_2<=2`. A rank-k correction Delta contributes `J=Delta Q-R Delta`, of rank at most 2k. For integer `0<=k<N/2`, singular-value min-max gives

`||E-J||_2 >= sigma_(2k+1)(E)`,
`(N-2k)sigma_(2k+1)(E)^2 >= sum_(j>2k)sigma_j(E)^2 >= N(1-rho)-8k`.

Since `||E-J||_2<=2||U-T||_2`, the independently proposed improvement is valid:

`||U-T||_2 >= (1/2)sqrt(max(0,(N(1-rho)-8k)/(N-2k)))`.

This independently checks the reviewer's new derivation. Do not assert `rank(E-J)<=N-2k`; that is unnecessary and generally false. The Frobenius denominator remains N, not N-2k. The uniform exact count `k>=ceil(N(1-rho)/8)` follows; the stronger N/2 exact count applies only when a corresponding full-rank defect is certified (including identity gauge), not uniformly to every gauge.

### 2.6 Forest holonomies and occurrence edits

Over a field, require all w_e and c_t nonzero. In each underlying connected component choose a tree and a root potential, then set `d_v=(c_t/w_e)d_u` on a forward tree edge and invert the ratio on a reversed traversal. Every tree edge is flat. For each remaining edge compute `H_e=w_e d_v/(c_t d_u)`. All H_e=1 iff the weighted connection is globally gauge-flat; the number of failures depends on the tree.

Replace exactly the failing occurrence edges by `c_t d_u/d_v`. For each constituent P, its difference from its reference has rank at most the number of changed entries. Provided every actual and reference `I-P` is invertible, the resolvent identity preserves that rank bound; sums and product telescoping give `rank(T-T0)<=k`, counting occurrences separately even for shared parameter names. The full network T0 itself need not be invertible. As it commutes with `Q=D Pi D^-1`, exact Fourier equality forces `rank(FQ-QF)<=2k`. This rank is over the same field with a primitive Nth root and characteristic not dividing N. It is a conditional certificate for the recovered D, not a claim that every gauge defect has full rank.

Tree traversal is O(E+N) field operations plus inversions, assuming adjacency/access preparation is charged. Explicit generic adjacency storage is O(E+N), not O(N) for arbitrarily many terms. The optional dense rank audit is cubic, not linear.

### 2.7 What O(E) certification does and does not mean

For a supplied valid list of permutation arrays/weights, streaming the paired and flat squared distances takes O(E+N) scalar arithmetic, with O(N) auxiliary workspace when occurrences are streamed and the common d is retained. Inputs and coefficients, route validation, and output are charged. If `max |w_i|<=rho0<1` for actual and reference terms, `||P||_2=max |w_i|` and a geometric-series estimate proves `g<=1/(1-rho0)`.

A truly rigorous finite-data variant can use exact rational complex entries, exact common unit phases, rational upper bounds beta>=|alpha| and rho0<1, exact squared-distance sums, and exact comparisons. Replace a,A,E by their beta-weighted upper versions. For a trig-free uniform gauge constant, `s sin(pi/s)>=2sqrt2` for even s>=4 implies rho<=1/sqrt2<3/4, hence `g_s>=1/4`. The resulting exact algebraic floors, or their safely downward-rounded intervals, are valid. Rational/algebraic bit costs are additional and are not constant-cost field operations.

The supplied `linear_time_curvature_certificate` instead uses NumPy floats, `allclose` with tolerances, approximate magnitudes, and ordinary rounded arithmetic. Thus its returned decimal is a numerical diagnostic; no outward rounding or exact phase/flatness certificate is present. It also materializes `all_terms` and does not independently establish all permutation hypotheses. The abstract theorem is accepted; certified finite-precision implementation is not established by those source tests. No supplied implementation was executed.

## 3. Fusion audit and prerequisite boundary

A correct common exact interface is:

1. Freeze one coefficient field, matrix dimension, target, and allowed left/right monomial group.
2. Check zero patterns (and, when legal, inverse zero patterns).
3. For nonzero rectangles compare the **set** of root orders/groups of four-entry ratios.
4. Only when a common primitive Nth root identifies every ratio with a unique exponent in Z/NZ, reduce anchored exponent matrices modulo a chosen prime divisor of N. Fourier's anchored exponent grid has rank at most one. Primitive-holonomy Green's accepted dyadic determinant theorem can then be invoked in its own scope.
5. Passing these rejection checks does not certify Fourier equivalence. A complete anchored grid with compatible row/column residue permutations is needed for acceptance.

There is no valid rule that cross-ratio orders/ranks of factors are preserved under ordinary matrix multiplication or summation. Therefore this interface cannot exclude an alternating unrestricted Green/Weil architecture. Moreover Q18 assumes p odd, whereas the accepted primitive-holonomy determinant family is dyadic. A new fusion theorem needs a genuinely common family and new implication beyond dispatching the existing tests.

The inverse-support check already in the matrix programme also excludes a single weighted-cycle Green resolvent at N>=3 under arbitrary external monomials: if G were monomially equivalent to Fourier, G^-1 would be equivalent to inverse Fourier and hence dense; but `G^-1=I-P` has at most two entries per row. This does not invalidate the stronger *explicit curvature determinant* result, but its basic single-resolvent no-go conclusion must not be sold as a new consequence of this fusion.

## 4. Primary-source comparison and honest priority state

- **Ladisch**, *The character of the Weil representation of a finite abelian group of odd order*, https://arxiv.org/pdf/2303.09676. Directly inspected §3 Proposition3.3 and §4 Theorems4.1/4.3, including surrounding proofs, for matrix algebra/covariance/projective closure; §7 Corollaries7.3/7.4 and following Gram-Schmidt observation for odd-PIR symmetric form reduction. This establishes matching classical machinery, not an assertion that every source kernel formula was copied from that paper.
- **Tadej**, *Permutation Equivalence Classes of Kronecker Products of Unitary Fourier Matrices*, https://arxiv.org/pdf/math/0501233. Directly inspected Definition4.1, Theorem3.12 and Theorem4.5 with its dephasing proof. These classify prime-power Fourier tensor factors and show permutation-phasing equivalence adds no new equivalences. Equal-modulus Fourier tables under arbitrary nonzero diagonal scaling reduce to unitary phasing: `|a_i b_j|=1` forces constant row modulus and reciprocal column modulus. Hence the v26 additive-vs-cyclic table obstruction is a classical corollary, not an independently new theorem.
- **Cliff–McNeilly–Szechtman**, *Weil Representations of Symplectic Groups Over Rings*, https://doi.org/10.1112/S0024610700001381. Publisher metadata/abstract verified; full article unavailable through that route. No full-theorem comparison is claimed from this citation.
- **Lange–Liu–Peyerimhoff–Post**, *Frustration index and Cheeger inequalities for discrete and continuous magnetic Laplacians*, https://link.springer.com/article/10.1007/s00526-015-0935-x. Directly read §2 Definition2.3 and equations2.10–2.11, including tree switching observation: classical gauge/switching background. Actual publication is 2015, whereas the Phase18 source calls it 2016. No conclusion that its Cheeger theorems subsume this specific Fourier energy floor.
- **Chandrasekaran–Govindarajan–Rajagopal**, https://arxiv.org/abs/1807.03437: identity and abstract verified only. It is background, not a full theorem-level priority comparison here.

Search/read boundary: 2026-10-10. Priority for the exact support/energy synthesis remains bounded-review unresolved; the explicitly identified Fourier-table theorem is subsumed. No absence-of-search-hit worldwide novelty inference is made.

## 5. Fresh evidence and unverified source evidence

Our exact controls independently checked 16 coherent symplectic words over q=3 and9, n=2; all row support sizes equal |im B|, covariance holds, and every dense cell agrees projectively with Bruhat. All six canonical q=9,n=2 profiles match the corrected completed-square formula entrywise. The sign counterexample is exact. An independent symbolic 4x4 Gram characteristic polynomial check passed. Complex direct checks at s=2,4,6,8,10 support the two spectral formulas; these floating checks are not proofs and all-size proofs are above.

The source's 60-word runs, ten test groups, other coefficient-field witnesses, source benchmark timing, and claims of independent source-verifier execution remain source-reported. This audit neither reran them nor certifies the supplied programs as production-correct. The fixed own controls close only their explicitly recorded cases.
