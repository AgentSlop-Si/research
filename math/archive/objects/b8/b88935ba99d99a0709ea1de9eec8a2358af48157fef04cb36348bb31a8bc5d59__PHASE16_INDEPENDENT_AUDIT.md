# Phase 16 independent audit: entropy-optimal factors and the Haar–Green stage barrier

9 October 2026. Supplied material was inspected as data only. No supplied executable, module, test, packaging script, or validation script was run or imported. All new numerical checks are in the self-contained `independent_phase16.py`, with machine-readable results in `independent_phase16_results.json`.

## Verdict

**The principal restricted-model theorems are correct.** The normalized Phase15 factors attain their exact two-coordinate-unitary entropy lower bounds. A complete Phase13 Haar–Green stage has a representation with at most `11N/2−8` pair-unitary gates, and consequently an exact product representation of the normalized Fourier matrix requires

`t ≥ ceil[N log₂N/(11N−16)]`.

This holds uniformly for finite real couplings, including couplings that depend on N. It is a stage-count obstruction and a pair-unitary-gate lower bound, not a general scalar-arithmetic FFT lower bound. It does not establish a new sub-N-log-N Fourier algorithm.

One implementation/proof-presentation correction is needed: the nearest-shared-column pivot in the supplied generic semiseparable compiler can fail on degenerate unitary inputs. The all-size path-Cayley result survives; an adaptive nonzero-prefix pivot repairs the general lemma without changing its count. A direct cut-rank proof below also handles zero edges and Hermitian tridiagonal extensions without a limiting argument.

Two useful extensions follow from explicit proofs:

1. The same stage obstruction survives fixed-error approximation measured in operator norm, or relative Frobenius norm, while the represented operator remains unitary.
2. Extra zero-initialized registers alone do not escape the two-coordinate-unitary gate bound. Ordinary nonunitary copying, rescaling, or general shared-state algorithms are a different model.

The Phase15 entropy identity and total gate optimality already appear in the previous independent Phase15 audit. Phase16 corroborates them and adds the Haar–Green structural compiler argument. None of this report certifies publication novelty.

## 1. Exact model, normalization, and entropy

Let `F̂_N[k,j]=exp(2πikj/N)/√N`. Computation begins from the identity on N complex coordinates. A charged gate is an arbitrary 2×2 unitary acting on two coordinates; permutations and unit-modulus coordinate phases may be free. Coefficients and wiring may depend arbitrarily on N but are fixed independently of the input vector.

For a unitary U define

`Φ(U)=−Σ_ij |U_ij|² log₂|U_ij|²`.

A gate changes only two rows. In column j it preserves their combined squared mass r_j, and the column-pair contribution is `−r_j log₂r_j+r_j h₂(p_j)`. Since binary entropy lies in [0,1], the absolute change is at most r_j. The two rows have combined mass 2, so `|ΔΦ|≤2`. As `Φ(I)=0` and `Φ(F̂_N)=N log₂N`, at least `N log₂N/2` charged gates are necessary. Free monomial unitaries preserve Φ.

This is the established entropy argument in [Ailon, Theorem 2.1 (2013)](https://arxiv.org/html/1305.4745). The cited paper establishes this same restricted gate model and lower bound; the method is not new to this project.

Normalization is essential: an unnormalized Fourier matrix is not unitary. Arbitrary diagonal scalings, unnormalized residuals, and nonunitary intermediate computations cannot be inserted into this proof as if they were free unitary phases. Working over a finite field does not supply the real probability distribution or logarithmic entropy used here.

### Phase15 factor identities

For powers of two `N=BL`, with `8≤B<N≤B²`, the Galois orbit histogram is B fixed points and B/2 orbits of each size `2,4,…,L`. Normalized factors have entropies

- Base bank: `N log₂B`
- Folding factor `R_u=diag(√(d/L))R`: `N−B`
- Orbit Fourier bank: `B+N(log₂L−1)`

A direct independent construction of a row of R_u is particularly useful. For orbit length d, let `g=L/d`, representative `k₀=gu`, choose `a∈[0,d)` with `ua≡e mod d`, and let `c=(ua−e)/d`. For each `r=0,…,g−1`, put the coefficient

`exp(2πi(c+ur)/B)/√g`

at base-bank register `(a+dr, ug mod B)`. These are g distinct registers. Thus each normalized row has g equal nonzero probabilities 1/g and entropy log₂g. Summing over the histogram gives N−B. This construction does not use the supplied folding executor.

The three implemented gate counts are respectively half of those three entropies and sum to `N log₂N/2`. Since the complete exact circuit reaches F̂_N with precisely this many gates, every gate must achieve +2 bits. Equality implies the two incoming rows have disjoint supports and balanced mixing splits each active column equally. The independent recursive-wiring checker confirms both properties gate by gate.

These entropy values happen to add to the target entropy for this factorization. Entropy is **not generally additive under matrix multiplication**. In particular, a small value of Φ(S) for one stage does not justify dividing Fourier entropy by Φ(S) to obtain a stage bound. The compiler proof below supplies the valid universal bound on each stage's entropy change.

## 2. Path Cayleys: a zero-safe proof of the compiler bound

Let A be Hermitian tridiagonal, with possibly zero or complex-conjugate off-diagonal entries and real diagonal entries, and let α be finite and real. The source's weighted real path adjacency is a special case. Define

`T=I−iαA`,  `C=(I+iαA)(I−iαA)⁻¹=2T⁻¹−I`.

A has real eigenvalues, so every eigenvalue `1−iαλ` of T is nonzero, and each eigenvalue `(1+iαλ)/(1−iαλ)` of C has modulus 1. The same argument applies to every principal block of T. Thus C is unitary and all those principal blocks are invertible.

Across any contiguous cut k, the off-diagonal block of tridiagonal T has rank at most one. A block inverse formula expresses the lower-left block of T⁻¹ as the product of an invertible block, that rank-one coupling block, and an inverse Schur complement. Therefore

`rank(C[k:N, 0:k])≤1` for every `1≤k<N`.

This cut-rank property is all the compiler needs. It avoids dividing by edge weights and covers disconnected paths directly. For an irreducible path, the familiar tridiagonal Green formula additionally gives global strict-lower generators `C_ij=u_i v_j` for i>j.

### General lemma, with degeneracies handled

Any N×N unitary U with `rank(U[k:N,0:k])≤1` at every cut, for N≥2, admits at most `2N−3` adjacent two-coordinate unitary gates and a diagonal unitary.

1. Sweep k from N−1 down to 2. At this moment, rows k−1 and k restricted to columns `0,…,k−2` have rank at most one. Row k is a combination of original rows k,…,N−1, whereas row k−1 is untouched; the original cut-rank property ensures the claim.
2. If this two-row prefix is zero, skip the gate. Otherwise choose **any nonzero column of that prefix**. A unitary rotation that annihilates its lower entry simultaneously annihilates the whole lower prefix, because all its columns are proportional. Previously processed lower rows are untouched. At most N−2 rotations produce an upper-Hessenberg unitary.
3. An ordinary adjacent-row QR sweep takes at most N−1 further rotations to make it upper triangular. An upper-triangular unitary is diagonal. Reversing the rotations reconstructs U with `2N−3` gates and those unit phases.

The result applies to C and its inverse. Relabeling the path merely conjugates the circuit by a free permutation. This proof establishes existence and gate count; it does not certify that numerical coefficients can be generated at uniform precision or fully charged O(N) bit cost.

### Concrete defect in the supplied generic compiler

The source always chooses column k−2, the nearest shared column. This is valid for the connected nonzero-edge Cayleys under discussion, but not for every unitary with global strict-lower rank-one generators.

Consider the 4×4 permutation swapping coordinates 0 and 3 and fixing 1 and 2:

`U = [[0,0,0,1], [0,1,0,0], [0,0,1,0], [1,0,0,0]]`.

Its only strictly lower nonzero is U₃₀=1, so it has the advertised global generator form. At k=3, column 1 is zero in both selected rows, although column 0 is not. The source's rule uses identity and leaves U₃₀ untouched. Later it rejects the matrix as non-semiseparable. The independently written reconstruction of this pivot rule has Hessenberg error 1; the adaptive prefix rule has exactly zero error on the same input.

Consequently, the source's phrase “zeros permit gates to be skipped or limits applied” is not a sufficient implementation rule. Replace the generic pivot selection with the nonzero-prefix choice above. This is a minor generic-compiler correction, not a counterexample to the path stage-count theorem.

## 3. Haar compilation and the complete stage

Let `m=N/2`, with m a power of two, and H_m the normalized Haar synthesis matrix in the specified scaling-plus-heap-order wavelet basis. Its binary tree has m−1 internal nodes. Each node uses one balanced pair gate, and a final permutation orders the leaves. Hence H_m and H_m* each need m−1 gates.

Set `W=diag(H_m,I_m)` and `J=[[0,I_m],[I_m,0]]`. Then

`R_H=WJW*`,

`V_H=(I+iεR_H)/√(1+ε²)=W[(I+iεJ)/√(1+ε²)]W*`.

For finite real ε the middle matrix consists of m independent 2×2 unitary blocks. Thus V_H uses `2(m−1)+m=3m−2` gates. The two path Cayleys use at most `2(2N−3)`, giving

`G_N=11N/2−8`.

A product of t such stages or their inverses, with arbitrary intervening monomial unitaries, therefore has a pair-gate circuit of at most tG_N gates. Combining this **upper** compilation bound with the Fourier **lower** gate bound gives the claimed lower stage count. The directions of the inequalities are correct. Every stage may have its own path order, weights, α, and ε; finite real N-dependent parameters cause no exception.

The numerical source stage tests fix the original α=1/32 and ε=1/512. They do not numerically cover arbitrary strengths, although the algebraic theorem does. Our independent stage tests additionally cover zero, negative, large, and N-dependent strengths, and independently permuted weighted paths.

### Haar entropy formula

The scaling column of H_m contributes log₂m; at wavelet level ℓ, 2^ℓ columns have support m/2^ℓ. Therefore

`Φ(H_m)=log₂m+Σ_(ℓ=0)^(log₂m−1) 2^ℓ log₂(m/2^ℓ)=2(m−1)`.

For `p=ε²/(1+ε²)`, the own-half and opposite-half supports of each row of V_H are disjoint, yielding

`Φ(V_H)=N h₂(p)+2pΦ(H_m)=N h₂(p)+2p(N−2)`.

This is O(N) uniformly in real ε, even if ε depends on N. It supports the diagnostic interpretation of global support and cut rank, but the actual product obstruction comes from gate compilation, not from an unjustified entropy subadditivity assumption.

## 4. Determinants and phase conventions

For a zero-diagonal Hermitian path adjacency, the spectrum is symmetric under λ↦−λ. The Cayley eigenvalues therefore pair to product 1, so det C=1. Also R_H has m eigenvalues +1 and m eigenvalues −1, giving det V_H=1 and det S_H=1. The Hermitian-tridiagonal extension with nonzero diagonal retains unitarity and the gate bound but need not have determinant 1.

The positive-exponent normalized DFT has

`det(F̂_N)=exp[πi(N−1)(3N−2)/4]`.

This follows directly from the phase of its Vandermonde product. It is −i at N=4 and i for dyadic N≥8. Thus products of the original determinant-one stages and permutations **without arbitrary complex diagonal phases** cannot equal this exact DFT at those sizes, regardless of depth. With the source's permitted unit-modulus diagonal phases, the determinant mismatch is removable and does not invalidate the entropy argument. A normalized unitary matrix has determinant of modulus one, not necessarily determinant equal to one.

## 5. Justified extension: approximation still needs logarithmically many stages

This section is an independently derived consequence, not a claim of new literature priority.

Let U be the exactly unitary operator represented by the stage product. Suppose either

- `||U−F̂_N||₂≤ε` in operator norm, or
- `||U−F̂_N||_F≤ε√N` in Frobenius norm.

The second is the weaker relative-Frobenius guarantee, because `||F̂_N||_F=√N`. Define `τ=min{ε,1−1/N}` and `b_N(τ)=h₂(τ)+τ log₂(N−1)`.

For a normalized row u and the matching Fourier row f, their squared-modulus distributions have total variation distance

`δ=½Σ_j ||u_j|²−|f_j|²| ≤ ||u−f||₂`.

This follows from Cauchy–Schwarz and `|| |u|+|f| ||₂≤2`. A maximal coupling of the two distributions has disagreement probability δ. Conditional entropy then gives

`log₂N−H(|u|²)≤h₂(δ)+δ log₂(N−1)`.

For the Frobenius hypothesis, average row distance is at most ε by Cauchy–Schwarz. The function b_N is concave and increasing on `[0,1−1/N]`; Jensen's inequality and the fact that a distribution's distance from uniform is at most `1−1/N` give

`Φ(U)≥N[log₂N−b_N(τ)]`.

The operator-norm hypothesis implies the same estimate row by row. Therefore

`t ≥ ceil{ N[log₂N−h₂(τ)−τ log₂(N−1)]/(11N−16) }`.

For any fixed ε<1, this remains Ω(log N), with leading lower-bound coefficient `(1−ε)/11`. It does not cover a nonlinear algorithm, an operator that ceases to be unitary internally, or an unspecified “small residual” lacking one of these error guarantees. Entrywise error alone must be converted with its dimension-dependent norm factors before using this statement.

## 6. Justified extension: zero workspace is not itself an escape

Suppose there are M≥N registers, initialized to `(x,0)`, and all operations are still pairwise unitaries and free monomial unitaries. Let A be the effective M×N input-to-current-state matrix. Initially `A=[I;0]`; throughout `A*A=I`. Hence each row has squared norm at most one, and any two selected rows have total squared mass at most two.

The same entrywise entropy potential and column-pair calculation still give `|ΔΦ(A)|≤2` per gate. If designated output registers equal F̂_N x exactly, those N output rows already contribute `N log₂N` entropy. In fact, their complete unitary output consumes the entire input norm, so all other effective rows must be zero. Therefore the same `N log₂N/2` pair-gate bound holds with arbitrary zero-initialized workspace.

This strengthens the supplied conservative “in-place only” statement. It does **not** extend the theorem to ordinary copying of inputs, arbitrary nonunitary intermediates, data-dependent branching, free preprocessing of input data, or different access-cost models. Those are genuine model changes, not counterexamples to this entropy argument.

## 7. Independent evidence and reproducibility

Run from any directory with Python 3 and NumPy available:

`OPENBLAS_NUM_THREADS=1 python3 independent_phase16.py`

The script resolves its output beside itself and has no dependency on an original shared directory or uploaded source module.

Verified cases:

- Seven direct normalized factorizations and seven gate-by-gate circuits at `(N,B)=(16,8),(32,8),(64,8),(128,16),(256,16),(256,128),(512,32)`.
- Separate flat-support, Gram, and entropy identities for all three factors.
- Exactly 2-bit entropy gain at every gate; the maximum observed deviation was `1.60×10⁻¹⁴` bits. Maximum full Fourier matrix error was `1.83×10⁻¹⁶` using modularly reduced root exponents.
- 192 complete path-Cayley matrix reconstructions: N=2,3,4,8,16,32,64,128; signed real paths, zero-edge splits, and complex Hermitian paths with diagonal potentials; α=0,−2,1/32,1/2,2,N,N²,10⁻⁹. Maximum reconstruction error: `2.56×10⁻¹⁵`.
- 36 entire Haar–Green stage matrices at N=4,8,16,32,64,128, with ε=0,1/512,−1/2,1,N,N² and path strengths −N and N². Both paths have independently permuted random signed weights. Maximum stage and adjoint-inverse reconstruction error: `2.23×10⁻¹⁵`.
- Haar entropy and V_H entropy formulas, stage determinants, DFT determinant phases, and the concrete generic-pivot counterexample.
- 600 random square-unitary gate updates; 1,680 rectangular-isometry gate updates with three times as many registers as inputs; and 12 numerical sanity checks of the approximation entropy estimate.

These floating-point checks are consistency tests, not exact-arithmetic certificates or substitutes for the proofs. The supplied 55 inherited/new regression results remain source-reported; their uploaded executables were not rerun in this audit.

## 8. Historical attribution and research consequence

[Ailon (2013)](https://arxiv.org/abs/1305.4745) supplies the entropy lower-bound method and exact pair-gate constant. The structured-unitary/Givens literature substantially predates Phase16: [Delvaux and Van Barel, *Unitary rank structured matrices*, JCAM 215(1), 49–78 (2008)](https://doi.org/10.1016/j.cam.2007.03.020) explicitly studies efficient representations by elementary unitary/Givens transformations. The bibliographic identity is also confirmed by the [authors' institutional publication record](https://www.cs.kuleuven.be/publicaties/lirias/TEST2/numapub.php?year=2008). No systematic novelty search for the exact `2N−3` specialization was completed.

The correct project consequence is to stop expecting asymptotic savings from merely rewiring these unitary pair-gate factors or retuning the same finite-strength stage family. Parameter growth, zero unitary ancillas, and fixed-error unitary approximation do not provide that escape. A proposed nonunitary shared-state or sum-of-resolvents construction still needs its own exact Fourier identity and fully charged executor; neither a dense output nor a large cut rank demonstrates a faster FFT.
