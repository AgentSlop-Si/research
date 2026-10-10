# A striped-bank obstruction for natural plus bit-reversed Green cycles

## Theorem

Let N=2^k, m=2^floor(k/2), q=N/m, and let Z be the natural cyclic shift and R the k-bit reversal permutation. Consider a product of L paired-Green layers. Each layer is the sum of two terms with respective cycle orders Z and R Z R, with arbitrary edge weights and nonsingular diagonal endpoint factors. More generally the endpoint monomials may permute within each contiguous m-block, but must preserve those blocks. Every cycle inverse must exist; individual edge weights may be zero.

Allow any additional matrices inserted anywhere in the product that are block diagonal on the same contiguous m-blocks. This includes any active Fourier bank with F_m on selected blocks and identity on the rest. Then an exact Fourier factorization requires

\[
L(q/2+m)\ge N/2,
\qquad\text{equivalently}\qquad
L\ge\left\lceil\frac{N}{q+2m}\right\rceil. \tag{1}
\]

Consequently:

* Three paired layers are impossible for every dyadic N>=128.
* Four paired layers, even with a full active Fourier bank, are impossible for every dyadic N>=256.
* A uniform fixed-depth family with these cycle orders and endpoint restrictions cannot realize the Fourier transform. The necessary number of layers grows as Omega(sqrt N).

This includes arbitrary diagonal masks, weighted wraps, and exponential diagonal gauges. It does not include arbitrary endpoint permutations or arbitrary independent Hamiltonian cycle orders.

## 1. The relevant Fourier block has full rank

Let I be the union of the even-numbered contiguous m-blocks, and let I^c be the odd-numbered blocks. Both have N/2 coordinates. Put t=q/2, so N=2mt and t divides m in the balanced dyadic setting. Write

\[
i=2ma+b\in I,\qquad j=2mc+m+d\in I^c,
\]

where 0<=a,c<t and 0<=b,d<m. Let omega be a primitive Nth root and zeta=omega^(N/t). Since t divides m, the Fourier entry simplifies to

\[
\omega^{ij}=\zeta^{ad+bc}\,\omega^{b(m+d)}. \tag{2}
\]

Apply invertible inverse t-point Fourier transforms to the a row coordinate and the c column coordinate. The transformed entry indexed by (e,b),(f,d) vanishes unless

\[
e\equiv d\pmod t,\qquad f\equiv b\pmod t,
\]

and otherwise equals omega^[b(m+d)]. Reorder the rows and columns by (e,f). Put L0=m/t, b=f+t beta and d=e+t delta. Each resulting L0-by-L0 block is, after nonzero row/column diagonal scalings,

\[
[\eta^{\beta\delta}]_{0\le\beta,\delta<L_0},
\qquad \eta=\omega^{t^2}.
\]

The order of eta is N/t^2=2L0. Thus 1,eta,...,eta^(L0-1) are distinct, and each block is an invertible Vandermonde matrix. Therefore

\[
\operatorname{rank}F_N[I,I^c]=N/2. \tag{3}
\]

For balanced exponents, L0 is2 when q=m, and1 when q=2m. The same proof works whenever N=2mt and t divides m. It is valid over any field with the supplied primitive Nth root and characteristic not dividing N; no complex-only full-spark theorem is used.

## 2. Rank contributed by a weighted Green term

For a nonsingular A=I-D_w P, complementary off-diagonal ranks satisfy

\[
\operatorname{rank}A^{-1}[I,I^c]
=\operatorname{rank}A[I,I^c].
\]

This is the standard inverse complementary-submatrix rank identity and does not require invertible principal subblocks. The sparse block A[I,Ic] has one possible nonzero for each cycle edge entering I from Ic. These locations form a partial matching, so its rank is exactly the number of nonzero crossing weights, and at most the unweighted crossing-edge count. Endpoint monomials preserving I do not change the rank.

For the natural cycle Z, each odd block ends with one edge entering the next even block. There are q/2 such edges.

For RZR, conjugate the tested set I by R. Membership in I tests whether the bit in position log2(m) is zero. Bit reversal changes that to the bit in position k-1-log2(m)=log2(q)-1. Along the natural cycle, this bit has a zero run and a one run of length q/2, repeated N/q=m times. Hence exactly m edges enter the zero-bit set.

The paired sum therefore has cross rank at most q/2+m. This upper bound includes every zero-weight or cancellation branch.

## 3. Products and banks

For any square A,B,

\[
(AB)[I,I^c]=A[I,I]B[I,I^c]+A[I,I^c]B[I^c,I^c],
\]

so its rank is at most the sum of the two factor cross ranks. The same rank subadditivity applies to each paired sum. Every matrix block diagonal on the m-blocks has zero cross rank because I is a union of complete blocks. Thus the full product has cross rank at most L(q/2+m). Combining with (3) proves (1).

## 4. Thresholds

If k is even, q=m and (1) reads L>=ceil(m/3). Three layers therefore fail once the dyadic m is at least16, beginning at N256. If k is odd, q=2m and (1) reads L>=ceil(m/2). Three layers fail once m>=8, beginning at N128. Together, every dyadic N>=128 is excluded for three layers.

For four layers, the even-exponent branch fails at m>=16, N256; the odd branch fails at m>=16, N512. Together, every dyadic N>=256 is excluded. The bound at N128 is exactly64 for four layers, equal to the Fourier rank, and gives no contradiction there.

Selected exact counts:

| N | m | q | rank of target block | cap for three pairs | cap for four pairs |
|---:|---:|---:|---:|---:|---:|
| 64 | 8 | 8 | 32 | 36 | 48 |
| 128 | 8 | 16 | 64 | 48 | 64 |
| 256 | 16 | 16 | 128 | 72 | 96 |
| 512 | 16 | 32 | 256 | 96 | 128 |

## 5. Provenance, checks and research consequence

This is an additional scoped deduction developed while examining the new recursively active-bank target. It is separate from the source's inherited inverse-sparsity theorem and from the earlier three-QS-stage bit-reversal obstruction. No claim of publication priority is made.

`check_two_cycle_cut.py` is independently authored and executes no uploaded source. It checks both crossing counts through N65536, direct Fourier block ranks through N512, entrywise identity (2), and the exact transformed Vandermonde blocks through N64 over F65537. The paired reviewer independently reconstructed the algebra and crossing counts and approved the threshold.

The natural-plus-bitrev construction track confirmed its current three-layer family has precisely these two cycle orders and diagonal masks, so it is covered. A next candidate must change the geometry: a sufficiently different independent cycle order, or endpoint routing that does not preserve these bank blocks. Passing the striped cut would only remove this obstruction; it would still require all coefficient/Weyl equations and an O(N) uniform parameter generator.
