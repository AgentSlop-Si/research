# HERO #17 — Phase 14 proof certificate

**Date:** 2026-10-10. **Scope:** exact algebraic statements over `C` or a field containing a primitive `N`-th root of unity, with characteristic not dividing `N`, and not 2 where indicated. All arithmetic-algorithm bounds are for explicit prime-field or exact-field operations, not floating-point/bit complexity. **No universal linear-time Fourier transform is established.**

Let `N >= 2`, `ω` be primitive of order `N`, and use the unnormalized DFT `F[i,j]=ω^(ij)`. Set `S e_j=e_(j+1 mod N)`, `T e_j=ω^j e_j`; then `TS=ω ST`. In any expression `S^a T^b`, S is always written to the **left** of T. We use `H_{εδ}(α,β)=(I-αS^ε-βT^δ)^(-1)` for signs `ε,δ ∈ {+1,-1}`.

## 1. Root-of-unity quantum-binomial collapse

**Theorem.** If `Δ=1-α^N-β^N != 0`, the signed magnetic Green operator exists and

`H_{εδ}(α,β)= Δ^(-1) sum_(k=0)^(N-1) (αS^ε+βT^δ)^k`.

**Proof.** Put `A=αS^ε`, `B=βT^δ`. Then `BA=q AB` with `q=ω^(εδ)` primitive of order `N`. The Gaussian/binomial coefficients `[N choose r]_q` vanish for each `0<r<N`: their numerators contain `1-q^N=0`, but each denominator factor `1-q^j`, `1<=j<N`, is nonzero. Thus `(A+B)^N=A^N+B^N=(α^N+β^N)I`. Multiplying the finite geometric sum by `I-A-B` gives `Δ I`, and division by Δ proves the identity.

Moreover, `I-αS^ε-βT^δ` is cyclic bidiagonal. Its determinant equals `prod_(j=0)^(N-1)(1-βω^(δj))-α^N = 1-β^N-α^N=Δ`; only its diagonal and full-cycle permutations contribute. So Δ is also the **necessary** nonsingularity criterion. QED.

The polynomial on the right contains `2^N-1` formal ordered words if expanded without merging, but it can be evaluated by a standard `O(N^2)` dynamic polynomial iteration; our improvement for this operator is to use a charged **O(N) recurrence**. This does not imply exponential-time prior art or a new DFT algorithm.

## 2. Charged all-input O(N) evaluator, including zero pivots

Relabel indices by `i=ε j (mod N)`. With `q=ω^(εδ)`, the inverse equation becomes

`d_j z_j-α z_(j-1 mod N)=u_j`, where `d_j=1-β q^j`.

If `α!=0`, set `r_j=d_j/α`. A backward sweep from `j=N-1` to `1` gives `z_0=A z_(N-1)+B`, with `A=prod_(j=1)^(N-1) r_j` and `B` obtained using one multiply/subtract at each position. At `j=0`, the closure gives

`z_(N-1)=(u_0-d_0 B)/(d_0 A-α)`.

The denominator is nonzero, because `(d_0A-α) α^(N-1)=Δ`. A second backward sweep recovers every `z_j`. This procedure **never divides by an individual `d_j`**, so zero diagonal pivots, including `β^N=1`, are harmless when Δ is nonzero. When `α=0`, the operator is diagonal and its entries can be prepared by one batch inversion and O(N) multiplications.

All required powers and roots are generated iteratively after accepting a supplied primitive root `ω`. The implementation counts every addition, multiplication, and inversion used to prepare its N-entry tables and to evaluate a fresh vector. A complete input is read and every output explicitly written. Preparation and one query both cost O(N) field operations; memory is O(N). This says nothing about general FFT, numerical conditioning, or arbitrary-precision bit costs. QED.

## 3. Exact signed-Weyl support and linear-span classification

For a fixed pair of signs, the identity in Theorem 1 implies a Weyl expansion

`H_{εδ}(α,β) = Δ^(-1) sum_(a,b>=0; a+b<N) [a+b choose a]_(ω^(εδ)) α^a β^b S^(εa) T^(δb)`.

Each Gaussian-binomial coefficient shown is nonzero because its top index is less than N. Thus the support is contained in the **signed triangular set**

`T_{εδ}={ (εa mod N, δb mod N) : a,b>=0, a+b<N }`.

**Exact linear span.** Over `C`, varying `α,β` with `Δ!=0` spans *every* Weyl monomial indexed by `T_{εδ}`. Indeed, if a linear functional annihilated all resolvents near `(α,β)=(0,0)`, multiplying by Δ would yield a polynomial in α and β whose every coefficient must vanish. The nonzero Gaussian binomial factors force the functional to annihilate every monomial in that triangle. Finite-dimensional duality proves the span assertion.

Consequently, for the **sum of all four sign families**:

- If N is odd, the union of four signed triangles covers all `N²` Weyl indices; the span has dimension `N²`.
- If N is even, the union excludes precisely `(N/2,N/2)`; the span has dimension `N²-1` and consists exactly of those operators whose coefficient at that Weyl monomial is zero.

In the odd case, **all four orientations are necessary** to span `F_N`: excluding the `++`, `--`, `+-`, or `-+` family respectively leaves uncovered the Weyl position `(1,1)`, `(N-1,N-1)`, `(1,N-1)`, or `(N-1,1)`. Every Weyl coefficient of the odd-length Fourier matrix is nonzero: its normalized Gauss sum is nonzero by `G(ω)G(ω^(-1))=N`.

**Note:** Spanning is merely an existence result for finite linear combinations of appropriately chosen resolvents. The proof does not give O(N) or sub-NlogN preparation or evaluation for the Fourier transform. QED.

## 4. The even-length central Fourier obstruction

For `N` even, the Weyl coefficient at `(N/2,N/2)` of every signed magnetic Green operator is zero by Theorem 3. Coefficient extraction for the Fourier matrix gives

`c_{a,b}(F_N)=(1/N) sum_(j=0)^(N-1) ω^(j²+(a-b)j)`.

Therefore, `c_{N/2,N/2}(F_N)=G(ω)/N`, where `G(ω)=sum_j ω^(j²)`.

- If `N=4m`, **`G(ω)G(ω^(-1))=2N`**. To see this, substitute `u=x-y`, `v=x+y` in the product. The map has exactly two preimages when u and v have equal parity. Writing both even yields sum N; writing both odd yields zero (the relevant character has nonzero odd exponent). The factor of two gives `2N`. In characteristic not dividing 2N, the coefficient is nonzero. In `C`, its modulus is `sqrt(2/N)`.
- If `N=4m+2`, pairing the terms at j and `j+N/2` shows `G(ω)=0`, since `ω^((N/2)^2)=-1`.

Thus over `C`, the full Fourier matrix belongs to the four-family linear span **if and only if** `4` does not divide `N`. In particular, when `4|N`, **no finite scalar sum of those four un-gauged signed Green families can equal `F_N`**, regardless of branch count. There is an explicit annihilating linear functional measuring this missing coefficient.

This excludes **only** this exact grammar: endpoint Weyl shifts, additional arbitrary Weyl generators, or products can populate the missing coordinate. It is not a universal FFT lower bound. QED.

## 5. Quasiseparable cross-cut rank and multistage branching

Let `m=floor(N/2)`, `L={0,...,m-1}`, `R={N-m,...,N-1}`. Define `ρ(A)=max(rank(A[R,L]),rank(A[L,R]))`.

For one magnetic Green `H`, both separated cross-blocks have rank at most one. One way to see this without division by any possibly zero `d_j` is the cyclic Green-kernel formula. For `ε=+1` and `i>j`,

`H[i,j]= α^(i-j)/Δ * (prod_(k=i+1)^(N-1)d_k) * (prod_(k=0)^(j-1)d_k)`.

The factors in i and j separate (choose a fixed boundary m to split the exponent into nonnegative powers). For `ε=-1` and `i>j`,

`H[i,j]=α^(N-i+j)/Δ * prod_(k=j+1)^(i-1)d_k`,

and the product splits at the same boundary. The top-right formulas are analogous with wrapping direction reversed. Consequently, `ρ(H)<=1` for **all four sign choices and all nonsingular parameters**, even when a diagonal pivot is zero.

For conformable block matrices with this fixed two-part coordinate cut,

`ρ(A+B)<=ρ(A)+ρ(B)`, and `ρ(AB)<=ρ(A)+ρ(B)`,

because the bottom-left block of the product equals `A[R,L]B[L,L]+A[R,R]B[R,L]`; the other cross-block is symmetric. Any diagonal matrix has `ρ=0`.

Consider a **sum of B products** in the fixed physical coordinate order, with path b containing `L_b` signed nearest-neighbor magnetic Green stages and arbitrarily many diagonal scalings between them. Then

`ρ(operator)<=sum_(b=1)^B L_b`.

But `F_N[R,L]` is a Vandermonde matrix on distinct nodes `ω^i` with consecutive exponents `j=0,...,m-1`, and has rank m; similarly for `F_N[L,R]` after a column scaling. Thus an exact Fourier representation in this grammar requires

`sum_b L_b >= floor(N/2)`.

This is a **restricted path/depth budget**, not a sequential computation lower bound for a shared DAG. Different paths can sometimes be evaluated jointly, and inserting arbitrary long-range permutations destroys the hypothesis that every gate has cross rank <=1. QED.

## 6. Positive fusion of N noncommuting Weyl-conjugate branches

For the `++` Green operator `H=(I-αS-βT)^(-1)`, define two twirls:

`E_T(H)=(1/N)sum_(k=0)^(N-1) T^k H T^(-k)`,

`E_S(H)=(1/N)sum_(k=0)^(N-1) S^k H S^(-k)`.

Conjugation by T annihilates every Weyl monomial with a nonzero S exponent; conjugation by S annihilates every monomial with a nonzero T exponent. The finite q-binomial expansion therefore gives

`E_T(H)=Δ^(-1) sum_(b=0)^(N-1) β^b T^b`,

`E_S(H)=Δ^(-1) sum_(a=0)^(N-1) α^a S^a`.

If `β^N !=1`, the first is `[(1-β^N)/Δ] (I-βT)^(-1)`; if `α^N !=1`, the second is `[(1-α^N)/Δ](I-αS)^(-1)`. When either scalar denominator vanishes, the **polynomial** formulas above remain exact and become a coordinate selector or rank-one cyclic projector respectively. Therefore **both averages of N branches are executable in O(N) field work on arbitrary fresh inputs**, including their preparation and N explicit output writes.

This is a real multibranch fusion for operators other than the DFT. It also illustrates why a lower bound on literal branch count alone is not a bound on optimized shared execution. QED.

## 7. Long-range shift explicitly escapes the nearest-neighbor cut gate

For even `N=2M`, let `G=(I-αS^M)^(-1)`, with `α² !=1`. Because `(S^M)²=I`,

`G=(I+αS^M)/(1-α²)`.

Its separated bottom-left `M×M` block is `α/(1-α²) I_M`, and hence has rank M for nonzero α. Nevertheless it applies in O(N) work to every input. More generally, `S^s` decomposes into `gcd(N,s)` disjoint cycles. Each can be solved by the recurrence of Theorem 2, with the total sum of cycle lengths equal to N; a batched closing-denominator inversion keeps full preparation in O(N).

Thus Theorem 5 cannot be generalized to all O(N) Green-like operators. In particular, **allowing long-range strides invalidates the cross-cut rank-one premise**. The direct target for Phase 15 is a multiscale long-stride network, tested on the complete DFT including its input and output maps. QED.

## Prior art / caution

Root-of-unity quantum-binomial identities, cyclic bidiagonal Green inverses, quasiseparable ranks, Weyl displacement bases, Gaussian sums and Vandermonde Fourier minors are established mathematics. Useful starting points:

- Root-of-unity quantum-plane identities: https://www.mdpi.com/2227-7390/8/3/352
- Quantum binomial context: https://golem.ph.utexas.edu/category/2007/11/geometric_representation_theor_9.html
- Fourier submatrix conditioning: https://arxiv.org/abs/2004.09643
- Benchmark for *arbitrary fresh exact full DFT*, not achieved here: https://github.com/openai/math/blob/main/lean/docs/130.md

The combination of scoped facts in this report is an independently reproducible project research checkpoint; **historical novelty, optimality outside each grammar, numerical stability and integer-multiplication implications are unverified**.
