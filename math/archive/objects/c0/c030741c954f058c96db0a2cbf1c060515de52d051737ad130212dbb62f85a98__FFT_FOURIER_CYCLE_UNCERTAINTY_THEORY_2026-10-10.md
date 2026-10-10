# Fourier–Cycle Uncertainty Theory (FCUT): a sparse-sandwich obstruction for exact DFT matrices

**Independent research note / candidate new result**  
**Date:** 2026-10-10  
**Status:** Mathematical statement and proof checked against concrete exact algebraic tests; not externally peer-reviewed. The ingredients (Chebotarev's Fourier-minor theorem, cycle recurrences, and sparse linear algebra) are known. Novelty of their particular combination and corollaries has **not** been established by exhaustive literature search. **Not an O(N) FFT.**

## Abstract

We prove that conjugating a prime-order Fourier matrix on the left and right by arbitrary first-order weighted Hamiltonian-cycle *difference operators* cannot create a sparse matrix, even with arbitrary endpoint diagonal gauges and permutations. More precisely, for the complex p×p Fourier matrix F_p, any two p-cycles α,β, any diagonal coefficient matrices D_a,D_b, and any invertible monomial L,R,

    C = (I-D_a P_α) L^{-1} F_p R^{-1} (I-D_b P_β)

satisfies

    nnz(C) >= ceil( p*ceil(p/2)/2 ) >= p^2/4.

This excludes exact identities F_p = L(A^{-1}+B^{-1})R for every prime p≥11 when A and B are invertible weighted cyclic first-order denominators, even for arbitrarily non-affine cycles. The proof combines cycle defect propagation and Chebotarev's *full-spark* property of prime Fourier matrices. An arithmetic-progression extension applies to arbitrary lengths, including powers of two, under a local primitive-stride condition.

The result does **not** exclude three or more Green branches, termwise independent gauges, general dense-inverse scans, structured fast dense centers, or unrestricted O(N) algorithms.

## 1. Setup and conventions

Let N≥3 and let ω_N=exp(-2π i/N). Write F_N[r,c]=ω_N^(rc) for the unnormalized DFT matrix. For a permutation σ of {0,...,N−1}, use the convention (P_σ)_{r,σ(r)}=1. A Hamiltonian cycle means a single permutation cycle of length N, not necessarily an affine permutation or an expander.

For diagonal D_a=diag(a_r) and D_b=diag(b_r), define

    A = I - D_a P_α,
    B = I - D_b P_β.

A monomial matrix is a product of an invertible diagonal matrix and a permutation matrix. We allow arbitrary invertible monomial endpoint matrices L,R.

For a matrix M, supp(M[r,:])={c:M[r,c]≠0} and nnz(M)=∑_r |supp(M[r,:])|.

## 2. Propagation-vs.-spark lemma (general N)

**Lemma (cycle boundary-propagation).** Let β be one N-cycle, B=I-D_b P_β with arbitrary complex b_r, H any N×N matrix, and C=HB. Fix two distinct rows r,s. Suppose H[{r,s},T] has rank 2 for *every* three-element column set T. Then

    |supp(C[r,:]) ∪ supp(C[s,:])| >= ceil(N/2).                 (1)

**Proof.** Set J=supp(C[r,:]) ∪ supp(C[s,:]), m=|J|. For each destination j=β(k) outside J, the equations C[r,j]=C[s,j]=0 imply

    (H[r,j],H[s,j])^T = b_k (H[r,k],H[s,k])^T.                (2)

Remove from the directed β-cycle the incoming edge of each vertex j∈J. If m>0, the remaining graph decomposes into exactly m directed paths whose vertex sets partition all N coordinates. Equation (2) implies that the two-row restriction of H to each path has rank at most 1: its column vectors are scalar multiples of the first column vector (possibly all zero). By the hypothesis, no path can contain three or more columns. Therefore N≤2m and m≥ceil(N/2).

If m=0, (2) holds all around the full cycle, so the entire two-row restriction of H has rank at most 1, again impossible since N≥3 and any three columns have rank 2. ∎

**More general form.** If every q-column restriction H[{r,s},T] has rank 2 for some integer q≥2, then the same proof yields |supp C_r ∪ supp C_s|≥ceil(N/(q−1)). This formulation allows a local *Fourier spark profile* to replace the global prime-length assumption.

## 3. Local Fourier full spark

**Known external ingredient (Chebotarev).** If p is prime, *every square minor* of F_p is nonzero. In particular, for any three distinct frequency labels S and any three distinct column indices T,

    det(F_p[S,T]) != 0.                                     (3)

The equivalent additive uncertainty inequality for a nonzero function f on Z/pZ is |supp f|+|supp Fourier(f)|≥p+1 (Tao, 2005).

**Local consequence.** Let i be any coordinate, k=α(i), ℓ=α(k). Since α is a Hamiltonian cycle of size N≥3, the labels i,k,ℓ are distinct. The two rows (i,k) of A have supports in the three-dimensional coordinate set {i,k,ℓ}, with an explicitly rank-two coefficient matrix:

    A[i,{i,k,ℓ}]  = (1,-a_i, 0),
    A[k,{i,k,ℓ}]  = (0, 1, -a_k).

Multiplication by L^(-1), an invertible monomial matrix, moves the three coordinate labels bijectively and rescales them; it preserves the coefficient rank 2. Then multiplication by F_p R^(-1) restricts to an invertible 3×3 Fourier minor (up to nonzero column scaling and a column permutation) for **any** choice of three columns. Therefore

    rank((A L^(-1) F_p R^(-1))[{i,k},T]) = 2                (4)

for every three distinct columns T.

This conclusion is independent of the values of a_i or a_k; A need not be invertible for the densification theorem.

## 4. Main theorem: quadratic densification

**Theorem 1.** Let p≥3 be prime, α and β arbitrary Hamiltonian p-cycles, D_a,D_b arbitrary complex diagonal matrices, and L,R invertible monomial matrices. Then

    C = (I-D_aP_α) L^(-1) F_p R^(-1) (I-D_bP_β)

obeys for **every** index i,

    |supp C[i,:] ∪ supp C[α(i),:]| >= ceil(p/2).             (5)

Consequently,

    nnz(C) >= ceil( p*ceil(p/2)/2 ) >= p^2/4.             (6)

**Proof.** By §3 the indicated pair of rows of H=A L^(-1) F_p R^(-1) has rank 2 on every three-column restriction. Apply Lemma (1) to H and B to obtain (5). Since |X ∪Y|≤|X|+|Y|,

    |supp C_i| + |supp C_{α(i)}| >= ceil(p/2).

Sum over i=0,...,p−1. Because α is a bijection, each row support occurs twice on the left:

    2 nnz(C) >= p*ceil(p/2).

Integer rounding proves (6). ∎

**Interpretation.** The intermediate matrix in any such two-sided Green-scan sandwich cannot be represented by a sparse O(p)-nonzero matrix. Dense does not automatically mean slow: a dense matrix may have a faster structured multiplication method. Therefore (6) is an entry-sparsity theorem, not a general arithmetic-circuit lower bound.

## 5. New no-go corollary: two resolvents fail at prime p≥11

**Corollary 2.** Let p≥11 be prime, A=I-D_a P_α and B=I-D_b P_β both invertible, with α,β arbitrary Hamiltonian p-cycles. Then for any invertible monomial L,R,

    F_p != L(A^(-1)+B^(-1))R.                              (7)

**Proof.** If equality held, multiplying by A on the left and B on the right gives

    A L^(-1) F_p R^(-1) B = A+B.

For any i, k=α(i), the union of the supports of rows i,k in A+B lies within

    {i, α(i), β(i), α²(i), β(α(i))},

which contains at most five column indices. By (5) its cardinality must be at least ceil(p/2), which is ≥6 for p≥11. Contradiction. ∎

This excludes **all** possible parameter choices, not merely generic or random parameters, and **all** Hamiltonian cycles, not only affine-run cycles. It does not exclude separate left/right diagonal gauges on individual summands, nor Q≥3 sums of Green inverses.

## 6. Composite-length extension, including powers of two

The prime assumption can be replaced by *local* full spark of the relevant three Fourier frequencies.

**Proposition 3.** Let N≥3, α and β N-cycles and L,R invertible monomial. Fix i and put k=α(i), ℓ=α²(i). If the three Fourier row labels appearing in the rows of A L^(-1) at {i,k} form an arithmetic progression

    {r, r+d, r+2d} (mod N), gcd(d,N)=1,

then (5) holds with N in place of p for that pair of rows.

**Proof.** For any three distinct columns j1,j2,j3, the 3×3 Fourier submatrix at frequency rows r,r+d,r+2d has columns proportional to

    (1,t_j,t_j²)^T,   t_j=ω_N^(d*j).

Because gcd(d,N)=1, the three t_j are distinct. The Vandermonde determinant ∏_{a<b}(t_{j_b}−t_{j_a}) is nonzero. Right monomial transformations only permute/rescale columns; the lemma then applies unchanged. ∎

**Corollary 4 (unit-stride cycles at all lengths).** Suppose α(i)=i+d modulo N with gcd(d,N)=1 and L's output permutation is affine with unit slope (the identity, hence any invertible diagonal L, is allowed). Then every adjacent row pair satisfies Proposition 3, and the densification (6) holds for **all N≥3**, including N=2^m. In particular no two-resolvent representation (7) is possible for any N≥11 under this additional α/L hypothesis, with β still arbitrary.

Note: This does **not** cover arbitrary non-affine α and arbitrary L for composite N. For those, verify the *specific three-row full-spark profile*; the entire composite Fourier matrix need not be full spark.

## 7. Concrete exact p=11 certificate

Take the non-affine cycles in array notation

    α = [2,4,9,6,10,1,0,5,3,7,8]
    β = [5,8,4,0,3,6,7,10,2,1,9].

For row i=0, k=α(i)=2, ℓ=α²(i)=9, the candidate A+B support union lies in J={0,2,4,5,9}; deleting incoming β-edges at these five indices creates paths of sizes [1,1,2,4,3]. One path is [5,6,7,10]. Pick three column indices T=[5,6,7] from this path. The Fourier frequencies are S=[0,2,9]. Direct exact integer-polynomial expansion gives

    det( z^(s*t) )[S,T] ≡ -2 z² + z⁴ - z⁷ + 2 z⁹   (mod z¹¹−1).

At a primitive 11th root ζ, the minimal polynomial is Φ_11(z)=1+z+...+z^10. The displayed degree-10 polynomial is not a multiple of Φ_11 because its 11 integer coefficients are not all equal. Therefore the determinant is nonzero over C. The candidate sparse-sandwich equations would force rank≤1 on those columns, while this invertible Fourier minor forces rank2. This is one explicit parameter-free obstruction certificate; the theorem handles every pair of cycles and all permitted gauges.

## 8. Reproducibility and independent testing

Run

    python fft_cycle_uncertainty_verify.py

using Python 3 standard library only. The independent finite checks include:

- Exhaustive exact confirmation that every 3×3 Fourier minor is nonzero at p=7 (1,225 minors), p=11 (27,225 minors), and p=13 (81,796 minors).
- 280 symbolic non-affine cycle-pair certificates for primes 11,13,17,19,23,29,31. Each uses an exact 3×3 cyclotomic minor, with no approximate root evaluation.
- 100 randomly parameterized sparse-sandwich computations for primes 5,7,11,13,17, with arbitrary monomial endpoint permutations and nonzero integer diagonal scalings. Each matrix entry is tested for exact zero in Q(ζ_p): a polynomial of degree <p vanishes at ζ_p iff all its coefficients are equal.
- Composite N=12,16,24,32,64,128 checked for all coprime shifts d in the local Vandermonde condition.

These checks supplement rather than replace the all-N mathematical proof. **Warning:** naïve reduction modulo a finite field can destroy Chebotarev nonvanishing even if the original complex cyclotomic determinant is nonzero; the verifier deliberately avoids that pitfall.

## 9. Novelty and related work: what is known and what is unverified

**Known prior theorems:**

1. Chebotarev's nonvanishing-minors theorem for prime-order Fourier matrices; see T. Tao, *An uncertainty principle for cyclic groups of prime order*, Mathematical Research Letters 12 (2005), 121–127, https://arxiv.org/abs/math/0308286.
2. Partial Fourier full-spark row selection including arithmetic-progressions/coprime shifts, e.g. H. K. Achanta et al., *The spark of Fourier matrices: Connections to vanishing sums and coprimeness*, Digital Signal Processing 61 (2017), 76–85, https://doi.org/10.1016/j.dsp.2016.07.008.
3. Sparse graph signal uncertainty principles, including prime cycle analogues, e.g. *Sparse graph signals – uncertainty principles and recovery* (2025), https://doi.org/10.1002/gamm.70002.
4. Dvir and Liu, *Fourier and Circulant Matrices are Not Rigid*, Theory of Computing (2020), https://theoryofcomputing.org/articles/v016a020/ (different model and conclusion).

**Project-originated deduction:** The propagation-vs.-spark lemma, quantitative quadratic nonzero count for two cyclic difference operators sandwiching F_p with *arbitrary* non-affine permutations/gauges, and the p≥11 two-Green-resolvent impossibility. I found no exact matching statement in a short targeted web search or in the inspected October 10 Green Phase 26 / sparse-defect project notes. That **does not establish publication-level novelty**; a mathematician should perform a wider literature review and independent proof check before claiming an original theorem.

## 10. What this does and does not mean for FFT complexity

**Established:** A broad class of seemingly plausible O(N)-work factorization architectures is mathematically impossible at prime lengths. For one natural composite-length cyclic architecture the obstruction extends to all N≥11. This significantly narrows the Green + Graph + Union research search space.

**Not established:** Any exact arbitrary-input FFT faster than N log N; a lower bound on arbitrary computational circuits; exclusion of sums with >=3 independently gauged Green terms; exclusion of general dense-inverse scans; or any conclusion about numerical stability/bit complexity.

**Next possible genuinely new theorem:** Extend the propagation-spark argument to a *sum of three or more independently gauged Green branches*, or derive a phase-covariance compatibility criterion that characterizes when a branched dense-inverse operator represents F_N. Any resulting claim must specify arithmetic model, charge preprocessing, and work for the entire N-output transform.

## 11. Research provenance

This note directly follows the supplied work on weighted Green operators, Hamiltonian/non-affine cycles, Fourier covariance (Weyl/seed), and sparse-defect certificates, especially the `fft_green_research_phase26_2026-10-10.zip` and `fft_sparse_defect_green_gate_2026-10-10.zip` archives. It is separate from the dynamic cached-FFT and randomized approximate FFT branches, which solve different problems. The previously explored `A U F_N V B=A+B` sandwich identity is used as a starting point, but the **prime full-spark × cycle-propagation bound** and its no-go consequence are derived here.
