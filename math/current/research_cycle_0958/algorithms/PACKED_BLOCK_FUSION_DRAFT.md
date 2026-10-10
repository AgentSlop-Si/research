# Locally normalized Fourier blocks through packed integer multiplication

10 October 2026. New project derivation, pending independent acceptance. The mechanism is classical Kronecker substitution and word-level parallelism. External novelty is unresolved. This is a replacement local backend for the proved finite-word approximate theorem, not an exact complex circuit.

## Statement

In the dyadic primitive let H=2^v, u=2^{-p}, and use its existing global floating state alphabet and norm/underflow budget. Choose a power of two m such that, with

  P=p+ceil(log2 m)+12,
  D=2P+ceil(log2 m)+4,
  2m^2 D <= v/4,

and prepare each required normalized r-point Fourier matrix, r a power of two with r<=m, by componentwise truncation to the dyadic lattice 2^{-P} Z[i]. Every small block can then be applied, followed by the original global quantizer, in O(r) word operations. All coefficient preparation costs poly(v,p), apart from an optional separately charged leading-bit table. No input-state response table is used.

For p=o(v), the largest such m satisfies

  m=Theta(sqrt(v/(p+log v))),
  log m=Theta(log(v/(p+log v))).

Consequently replacing the response-table backend preserves all stated fixed-accuracy and subpolynomial-accuracy time savings. Together with the guarded full-circle phase lemma, the dyadic cold cost becomes

  O(H+Hv/log m+poly(v,p)+H^{1/4}poly(v)),

with O(H) words in those regimes. The last term is the optional leading-bit table; it is not a response table. All-length interpolation still carries its own offset-coefficient preparation and O(Nt) evaluation costs. No polynomial-accuracy saving follows.

## 1. Local input conversion

For a nonzero r-vector z of represented floating states, scan its real and imaginary components and choose a power of two R with

  1/2 <= max_j max(|Re(z_j/R)|,|Im(z_j/R)|) < 1.

Then R<=2||z||_2. For a zero block, return zeros. Truncate each real/imaginary component of z/R to P fractional bits. Call the resulting vector v_tilde and put z_tilde=R v_tilde. Then

  ||z_tilde-z||_2 <= R sqrt(2r)2^{-P}
                   <=2 sqrt(2r)2^{-P}||z||_2
                   <=u/1000 ||z||_2.

The final numerical constant follows from 2^P>=4096m/u and r<=m. This conversion cannot increase component magnitudes. Global state exponents span O(v+p), so exact comparisons, shifts and truncations use O(v+p+P) bits, a fixed number of sufficiently wide words. The scan and conversion cost O(r).

## 2. Coefficient matrix and error

Let A_r be the componentwise-truncated dyadic matrix. Since each complex entry changes by at most sqrt(2)2^{-P},

  ||A_r-U_r||_2 <= r sqrt(2)2^{-P} <=u/1000.

(The conservative 1/1000 is larger than sqrt(2)/4096.) Hence

  ||A_r z_tilde-U_r z||_2
    <= (1+u/1000)(u/1000)||z||_2+(u/1000)||z||_2
    <u/100 ||z||_2.

After the original global quantizer, a nonoverflowing stage satisfies its original conservative bound

  ||q(A_r z_tilde)-U_r z||_2 <=3u||z||_2+sqrt(2H)tau

when independent blocks act on the full H-vector. The local conversion errors combine in squared norm across disjoint blocks; R need not be shared between them. The original cumulative error and first-overflow argument therefore apply unchanged.

## 3. Exact unsigned row packing

Write B=2^D. For a nonnegative integer matrix C=(c_ij) and vector a=(a_j), with each entry at most 2^P, define

  C_pack=sum_{i=0}^{r-1} sum_{j=0}^{r-1}
                c_ij B^{(2r-1)i+j},
  a_pack=sum_{j=0}^{r-1} a_j B^{r-1-j}.

In their integer product, the coefficient at digit (2r-1)i+r-1 is precisely sum_j c_ij a_j. Each row's complete polynomial product occupies digit indices (2r-1)i,...,(2r-1)i+2r-2. These row intervals are disjoint. Every intermediate convolution coefficient is at most r 2^{2P}<B, so there are no carries between digits. Thus every desired row sum is obtained by a shift and a B-1 mask.

The largest occupied product digit is 2r^2-r-1; the product occupies at most (2r^2-r)D<=2m^2D<=v/4 bits. The packed matrix and vector occupy no more. All shifts and integer products therefore have the charged O(1)-word size. Constructing a_pack and extracting all r sums cost O(r). Each packed coefficient matrix is prepared once and reused at every block of that size.

## 4. Signed complex arithmetic

Split every signed integer matrix or input vector into its nonnegative positive and negative parts. A signed matrix-vector product is

  (C_plus a_plus+C_minus a_minus)
   -(C_plus a_minus+C_minus a_plus).

Each of these four products uses the preceding unsigned packing. Real and imaginary parts of a complex matrix-vector product reduce to a constant number of such signed products (at most sixteen unsigned packed integer multiplications). After extracting digits, form the signed exact integer row sums by ordinary additions/subtractions.

Input components and matrix components both have denominator 2^P. Multiplying the exact extracted numerators by R 2^{-2P} therefore gives exactly A_r z_tilde. No approximation enters the packed computation. There are O(r) output extraction, exact rescaling and global requantization operations. All exact numerators have O(P+log r) bits; after restoring R's exponent their alignment with the global state lattice still has O(v+p+P) bits.

## 5. Preparation, depth and precision

There are O(log m) matrices. Preparing all entries costs at most m^2 poly(v,p)=poly(v,p), including certified roots and normalization. Packing their positive/negative real/imaginary parts is also polynomial. Stored packed matrices occupy O(log m) fixed words. A completely charged leading-bit table of at most H^{1/4}poly(v) entries may be reused for normalization; constant-many chunks suffice for every O(v+p) operand when p=o(v).

The choice of m can be found by testing powers of two using integer arithmetic. Since D=Theta(p+log m+1), the largest admissible m is Theta(sqrt(v/(p+log v))) whenever p=o(v). In particular the normalized Cooley-Tukey recursion has Theta(v/log m) macrolevels, each costing O(H), with every gather, packing loop, coefficient product, extraction, rounding and scatter included.

## Acceptance tests

1. Prove the row intervals are disjoint and every convolution coefficient is below B, including all-maximum matrices/vectors.
2. Exhaustively compare packed products with direct integer row sums for small signed matrices and vectors.
3. Check complex signs, zero blocks, mixed exponents, underflow and upper clipping explicitly.
4. Verify both local norm bounds with exact dyadic arithmetic and high-precision reference Fourier coefficients; verify the global stage recurrence analytically.
5. Confirm the true packed product bit length, rather than only the input key width, fits the word contract.
6. Compare with primary Kronecker-substitution and word-RAM literature. A valid proof is not novelty clearance.

This note does not claim that a matrix with real arbitrary coefficients fits a word, or that an r-output operation costs O(1). Coefficients are certified finite dyadics, all movement is charged, and the O(r) block cost is essential.
