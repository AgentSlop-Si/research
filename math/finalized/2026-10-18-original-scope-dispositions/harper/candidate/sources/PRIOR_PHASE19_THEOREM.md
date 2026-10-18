# Phase 19 — Dual Weyl gauges and stable noncommuting Green-product obstructions

**Date:** 9 October 2026  
**Scope:** normalized exact DFT at powers of two, all uniform asymptotic results for arbitrary dimension as stated.  
**Status:** proofs and reproducible finite-field/numerical controls. **NOT an FFT below `N log N`.**

## 0. Research provenance and prior art

Continue exactly from the Phase 18 checkpoint, preserving the earlier research in `previous_full_phase18_checkpoint.zip`. Our purpose is to test the surviving architecture of products of independently permuted, noncommuting Green sums, with exact Fourier covariance.

The inverse-norm estimate for strictly diagonally dominant systems is classical (J. M. Varah, *Linear Algebra Appl.* 11 (1975), 3–5, DOI `10.1016/0024-3795(75)90112-3`). Exponential decay for well-conditioned banded inverses is classical (S. Demko, W. F. Moss and P. W. Smith, *Math. Comp.* 43 (1984), 491–499, DOI `10.1090/S0025-5718-1984-0758197-9`). The Neumann-series constant below is a self-contained, possibly nonsharp project-specific derivation. The permutation/diagonal-similarity invariant machinery is elementary invariant algebra, with no literature-priority claim. Fourier/Harper commutation and zero-mode facts belong to the known Harper literature discussed in Phase 18.

## 1. The normalized Fourier target

Fix `N>=4` a power of two, `ω=exp(-2πi/N)`, `F[j,k]=ω^(jk)/sqrt(N)`, `Z e_k=e_{k+1}` and `D e_k=ω^k e_k`. Set `T=Z+Z^-1` and `V=D+D^-1`. The exact DFT obeys

`F T=V F`, `F V=T F`, and `F²=J`, with `J e_k=e_-k`.

For `N>2`, the solution space of the *two* intertwining identities

`M T=V M`, `M V=T M`

is exactly `{F(a I+b J): a,b complex}`. This fact is from Phase 18. In particular, **two identities are not enough to distinguish F**. The single full probe `M e_1=F e_1` forces `a=1,b=0`, because `e_1` and `e_{N-1}` are distinct. One scalar entry cannot replace this full-column probe in the general two-parameter case.

## 2. Joint middle-monomial Fourier coherence gate

Let `A,B` be fixed *invertible* matrices and set `M=A C B`, where `C=Q P`, `Q` is any invertible diagonal, and `P` is any permutation. Define

`U_T=A^-1 V A`, `U_V=A^-1 T A`, `W_T=B T B^-1`, `W_V=B V B^-1`.

Then **the following are equivalent**:

1. `M T=V M` **and** `M V=T M`.
2. `U_T C=C W_T` **and** `U_V C=C W_V`.

Writing `P[i,p(i)]=1`, the second statement is the elementwise simultaneous condition

`(U_s)[i,j] = (q_i/q_j) (W_s)[p(i),p(j)]`, for `s=T,V`.

Thus all choices of middle phases and permutations are encoded by one common coordinate permutation and one common diagonal gauge, not independently fit choices for the two Weyl identities.

### Exact vertex-signature invariant

The six-dimensional signature at vertex `i` for any matrix pair `(X,Y)` is

`sig(i;X,Y)=(X_ii,Y_ii,(X²)_ii,(XY)_ii,(YX)_ii,(Y²)_ii)`.

Since diagonal similarity cancels along every closed walk, simultaneous monomial conjugacy implies

`sig(i; U_T,U_V)=sig(p(i); W_T,W_V)`.

If the two multisets differ, **no middle `Q,P` exists**. If all signatures are pairwise distinct, they determine the *only possible* permutation in `O(N²)` arithmetic once the matrices are known. For a fixed permutation, solve the nonzero-entry ratios `q_i/q_j` over the union of directed nonzero graphs. This is a graph cocycle: BFS propagation and exact edge consistency either recover the gauge (up to components' scalar factors) or prove impossibility. The program `joint_gate.py` does this without heuristic fitting. If the signatures are duplicated, it exhausts the admissible group permutations only up to an explicit cap and reports **inconclusive**, not impossible, when the cap is exceeded.

Dense offline inversions in these verification scripts have `O(N³)` cost; the gate is **not** claimed to be an FFT executor or a subquadratic prover for arbitrary factor data.

### Adversarial control showing why both identities matter

Take `A=F`, `B=I+2T`, and `C=I`, for sizes where `B` is invertible. Then `M=F(I+2T)` satisfies `M T=V M` *exactly* because `B` commutes with `T`, but generally fails `M V=T M`. Phase 19's joint signature gate rules out *every* middle monomial for these **fixed** `A,B` at checked `N=8,16,32`. This is stronger than judging a candidate solely by the first intertwiner.

The positive control builds random invertible `A`, hides a random `Q P` in `B=(Q P)^-1 A^-1 F`, recovers the *exact permutation* and a gauge up to global scalar, and verifies **every entry** of the recovered Fourier matrix after calibration at `N=8,16,32`. The positive outer factors are arbitrary invertible matrices, **not fast Green factors**.

### Actual Green-sum product controls

`green_product_audit.py` forms fixed stages `A,B`, each the sum of two independently permuted and cyclotomic-phase-gauged tridiagonal inverses. All twelve tested combinations `(N,seed)` with `N=8,16,32,64` and seeds `0,1,2` have *unequal joint signatures*, exactly proving that **no** choice of middle diagonal/permutation can produce Fourier duality for those fixed stages. **No universal all-parameter impossibility theorem follows.**

## 3. Uniform `l1` obstruction for Green sums, with spectral error

Consider a general circuit

`M=S_t ... S_1`,

with `S_j=sum_(r=1)^(q_j) L_jr P_jr (B_jr)^-1 P_jr^-1 R_jr`. All permutations may differ and all `B_jr` may be complex, nonnormal and noncommuting. Suppose `L,R` are diagonal with maximum modulus <=1, and denote `gamma_jr=||(B_jr)^-1||_1`. Inserting any additional unit-modulus monomial layers between the `S_j` changes no bound. By the induced norm triangle/submultiplicativity inequalities,

`||M||_1 <= product_j Gamma_j`, where `Gamma_j=sum_r gamma_jr`.

Every column of normalized `F` has `l1` norm `sqrt(N)`, so `||F||_1=sqrt(N)`. Exact Fourier equality requires

**`product_j Gamma_j >= sqrt(N)`.**

For approximation `E=F-M`, the basic inequalities `||E||_1>=||F||_1-||M||_1` and `||E||_1<=sqrt(N)||E||_2` imply

**`||M-F||_2 >= max(0, 1-(product_j Gamma_j)/sqrt(N))`.**

This is an *actual operator-norm approximation floor*, not just an entrywise error heuristic. If `Gamma_j<=Gamma` uniformly and `t=o(log N)`, then the floor converges to 1. If `Gamma>1`, exact `F` needs `t>=log(sqrt(N))/log(Gamma)`.

### 3a. Strict column diagonal dominance: an easy sufficient condition

If every `B_jr` satisfies `|B_kk|-sum_(i != k)|B_ik|>=delta>0`, the classical inverse bound, applied to the transpose, gives `||B_jr^-1||_1<=1/delta`. If every `q_j<=q`, then `Gamma_j<=q/delta` and the advertised bound follows. For `q/delta<=1`, equality with `F` is impossible for every `N>1` under the stated restrictions. Otherwise `t>=ln N/[2 ln(q/delta)]`.

## 4. Stronger theorem: singular-value bounds *without diagonal dominance*

Let `B` be any invertible complex matrix of half-bandwidth `w>=1` (so `B_ij=0` if `|i-j|>w`). Suppose its singular values all lie in `[a,b]` with `0<a<=b`. Then

**`||B^-1||_1 <= C(a,b,w) = (b/a²)(1+2w (b/a)²)`.**

This constant is **independent of N**, and the bound does not assume `B` Hermitian, normal, diagonally dominant, real, or positive.

### Self-contained proof and explicit coefficient estimate

Set `A=B* B`, where `*` means conjugate transpose, `c=2/(a²+b²)`, and `E=I-c A`. Then `A` has half-bandwidth `2w`, `E` likewise, and its spectral contraction satisfies

`||E||_2 <= rho=(b²-a²)/(b²+a²)<1`.

The Neumann series gives

`B^-1=A^-1 B* = c sum_(k>=0) E^k B*`.

`E^k B*` has half-bandwidth at most `(2k+1)w` and spectral norm at most `b rho^k`. Therefore, for `d=|i-j|`, its `(i,j)` entry vanishes unless `k>=K(d):=max(0,ceil((d-w)/(2w)))`. Hence

`|(B^-1)_ij| <= c b rho^K(d)/(1-rho) = (b/a²) rho^K(d)`.

In each column, at most `2w+1` entries have `K=0`, and at most `4w` entries have `K=k` for each integer `k>=1`. Summing the geometric series yields

`||B^-1||_1 <= (b/a²)[(2w+1)+4w rho/(1-rho)]`
` = (b/a²)[1+2w(b/a)²]`.

The bound for `w=0` is immediate since `B` is diagonal.

A second explicit numerical control uses `B=I+i*0.75*T_path+0.2*U_path`, where `U_path` is the strictly upper-shift matrix. This B is **nonnormal and non-diagonally dominant**, yet its singular values remain in `[0.8,sqrt(3.25)+0.2]` by singular-value perturbation bounds. Independent dense verification through `N=256` confirms the uniform inverse `1`-norm estimate.

### Consequence for all stable Green products

If `B_jr` all have half-bandwidth <=w and spectra of singular values in the fixed common interval `[a,b]`, we may set `Gamma_j<=q_j C(a,b,w)`, recovering the exact and approximate FFT obstructions in §3 for all stages, any path-order permutations, any unit-modulus gauges, and any noncommuting products.

For fixed `q,w,a,b`, the number of stages is therefore `Omega(log N)`; the **number of Green summand calls** is also `Omega(log N)`, even allowing variable `q_j`, under bounded-magnitude coefficients. This is *not by itself* an arithmetic `Omega(N log N)` lower bound for a shared-DAG implementation; we have not shown that separate calls' internal work cannot be reused.

### Conditioning tax for trying to escape

Normalize each `B` so that `sigma_max(B)=1`, and let `K` be the largest spectral condition number of any Green denominator in the circuit. Then its inverse `1`-norm is <=`K²(1+2wK²) <= (1+2w)K^4` since `K>=1`. If every stage contains at most `q` terms and we have `t` stages, exact Fourier equality forces

**`K >= N^(1/(8t)) / [q(1+2w)]^(1/4)`**, provided all stage gauges/coefficient amplitudes remain <=1.

This is a necessary condition, not a sufficient construction. Large diagonal amplitude gains, shrinking denominator scale without normalization, growing bandwidth, or stages outside the products-of-Green-sums model evade its premises.

### Non-diagonally-dominant numerical control

`B=I+i*0.75*T_path` fails diagonal dominance at every interior row, but `1<=sigma(B)<=sqrt(3.25)` for every `N`. Exact inequalities and independent NumPy dense inverse controls through `N=256` show `||B^-1||_1~1.832`, below the N-independent proved constant ~13.521. This illustrates the extension beyond Varah's condition. It is not an FFT factor.

### Norm-growth counterexample that still fails the Fourier phase equation

Let `B_N=I-0.5(1-1/N)*T_path`. Its smallest eigenvalue vanishes asymptotically, and `||B_N^-1||_1` grows on the order of `N`, permitting it to clear the `sqrt(N)` column-norm threshold with one solve. However, the numerical `FZ=DF` covariance defect remains large (relative Frobenius defect roughly 1.5 in tested cases through `N=256`). In particular, satisfying a norm budget does **not** imply Fourier coherence. The spectral condition number in the control grows roughly linearly with `N`.

## 5. Another exact obstruction: one Harper monomial sandwich

Let `H=Z+Z^-1+D+D^-1`, with `N` divisible by four and `N>=4`. Define a monomial matrix as `Q P`, with `Q` any invertible complex diagonal (not necessarily unit-modulus) and `P` any coordinate permutation.

**Monomial centralizer theorem:** If `C H=H C`, then `C=c I` or `C=c J`, with a nonzero scalar `c` and reflection `J e_j=e_-j`.

**Proof:** Similarity by a monomial permutes diagonal entries. The diagonal entries of `H` are `2cos(2πj/N)`; the unique maximum `2` occurs at coordinate 0. Thus `P` must fix coordinate 0. Because the off-diagonal support of `H` is the cycle graph and diagonal scalings do not change zero patterns, `P` must be an automorphism of the cycle that fixes 0. The only two are identity and reflection `J`. For either permutation, the nonzero unit edge coefficients force neighboring entries of `Q` to agree. Connectivity gives `Q=c I`.

**Harper sandwich no-go:** For arbitrary invertible scalar rational functions `A=f(H)` and `B=g(H)` (well-defined at H), there is no monomial `C` such that `F=A C B`. Indeed, because `F,A,B` all commute with H, this would imply `C=A^-1 F B^-1` commutes with H, so `C=c I` or `c J`. Then `F=c h(H) J^e` for `e=0` or 1. Phase 18 proved that for `4|N`, H has two distinct zero modes of J parity ± on which F acts with eigenvalues from `{±1}` and `{±i}` respectively. But `h(H) J^e` acts on these with the same scalar up to a sign. Those eigenvalue ratios cannot agree. Contradiction.

This strictly strengthens the Phase 18 `F!=f(H)` result by permitting *one arbitrary intermediate coordinate permutation and diagonal scaling*. It does not rule out multiple monomial layers or noncommuting Green operators.

`harper_monomial.py` exhaustively checks the graph automorphism conclusion at `N=4,8`; its exact modular witness with `A=(H-7I)^-1`, `B=(H-11I)^-1` has a candidate middle matrix with N nonzeros **per row**, so it is not monomial at `N=8,16,32`.

## 6. What the results do and do not say

**Supported**: joint two-operator middle-monomial gate with exact positive/negative finite-field controls; uniformly conditioned banded inverse `l1` bound; exact and approximate norm-budget obstruction to shallow noncommuting Green products; a conditioning growth necessity under fixed scale/gauge normalization; all-size Harper one-middle-mask rational no-go; finite fixed Green-sum rejections; explicit near-resonant norm-growth example still missing phases.

**NOT supported**: an exact `o(N log N)` FFT; a new integer-multiplication upper bound; an unconditional arithmetic lower bound for general FFTs; a universal no-go for all noncommuting Green-product parameter families; a universal `Omega(N log N)` arithmetic bound after allowing arbitrary graph reuse; a claim that classical inverse-decay or Harper ideas were first discovered here.

## 7. Next gate (Phase 20)

The surviving branch must abandon at least one of: (i) uniformly bounded singular-value scales of each banded denominator; (ii) bounded coefficient gain; (iii) fixed bandwidth/one-dimensional path geography; (iv) the literal product-of-sums architecture. It must *also* satisfy **both** Weyl intertwiners, with one full-vector calibration, and include precision/data movement in its cost.

The strongest testable next proposal is to allow controlled near-resonance **while enforcing the dual intertwiners symbolically** through a shared-state recurrence across multiple Green resolvents. The first task is a necessary precision and transfer-operator budget for such a recurrence; the current near-resonant control proves that simply making inverse norms large is not enough.
