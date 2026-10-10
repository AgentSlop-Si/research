# Exact parity-block Fourier ranks and a GF(2)-affine scan-depth obstruction

**Research checkpoint: 2026-10-10.** All proofs refer to exact complex DFTs. They do not claim a general FFT circuit lower bound or a faster DFT algorithm. Terminology and network model are inherited from the previous checkpoint.

## Definitions

Set \(N=2^k\), \(k\ge2\), \(\omega=\exp(2\pi i/N)\), and \(F_N[r,c]=\omega^{rc}\). For nonzero \(k\)-bit masks \(a,b\), let

\[
C_{a,s}=\{c\in[0,N):\operatorname{parity}(a\mathbin{\&}c)=s\},\qquad
R_{b,t}=\{r\in[0,N):\operatorname{parity}(b\mathbin{\&}r)=t\}.
\]

Both sets have size \(N/2\), for either \(s,t\in\{0,1\}\).

## Theorem 1: exact parity-block rank

Let \(u=\lfloor\log_2 a\rfloor\) and \(v=\lfloor\log_2 b\rfloor\). Then, for every choice of the two parity signs,

\[
\operatorname{rank}_{\mathbb C}F_N[R_{b,t},C_{a,s}]=
\begin{cases}N/4,&u+v\le k-2,\\ N/2,&u+v\ge k-1.\end{cases}
\]

**Proof.** Put \(h=2^{u+1}\) and \(d=N/h=2^{k-u-1}\). Since the binary predicate defined by \(a\) only involves the lowest \(u+1\) bits, \(C_{a,s}\) is periodic modulo \(h\). Let \(E=C_{a,s}\cap[0,h)\), so \(|E|=h/2\). Since the highest bit of \(a\) is \(u\), each pair \(j,j+h/2\) with \(0\le j<h/2\) contains exactly one element of \(E\). Thus \(E\) is a complete system of residues modulo \(h/2\) and hence has uniformly balanced residue counts modulo every power of two dividing \(h/2\). By the universal sampling-set criterion for prime-power Fourier matrices, **every** \(h/2\)-by-\(h/2\) row restriction of \(F_h[:,E]\) is nonsingular over \(\mathbb C\). We apply that established theorem, not a new assertion about arbitrary Fourier minors.

Now write \(c=e+hj\) for \(e\in E\), \(0\le j<d\), and write \(r=\rho+d\ell\), \(0\le\rho<d,\ 0\le\ell<h\). Then

\[
\omega^{rc}=\omega^{\rho e}\omega_h^{\ell e}\omega_d^{\rho j}.
\]

An invertible length-\(d\) Fourier change of basis on the column groups separates the matrix into \(d\) independent blocks, indexed by \(\rho\); the \(\rho\)-block has columns \(E\) and rows indexed by those \(\ell\) with \(\rho+d\ell\in R_{b,t}\). The extra factor \(\omega^{\rho e}\) is a nonzero column scaling.

If \(v<\log_2d\), the parity predicate defining \(R_{b,t}\) depends only on \(\rho\). Exactly \(d/2\) blocks contain all \(h\) rows; the others contain none. Each present block has column rank \(h/2\). Total rank \((d/2)(h/2)=N/4\).

If \(v\ge\log_2d\), for each fixed \(\rho\), the condition on \(\ell\) is a nonzero GF(2)-linear parity constraint, so exactly \(h/2\) rows survive. The universal sampling property of \(E\) makes each such square block nonsingular. Total rank \(d(h/2)=N/2\). These cases are exactly \(u+v\le k-2\) and \(u+v\ge k-1\), respectively. This proof is characteristic zero. **QED.**

### Counting deficient pairs

Masks with highest set bit \(u\) number \(2^u\). Thus

\[
\sum_{u+v\le k-2}2^{u+v}
=\sum_{u=0}^{k-2}2^u\left(2^{k-1-u}-1\right)
=\boxed{(k-2)2^{k-1}+1}.
\]

This is out of \((2^k-1)^2\) ordered nonzero mask pairs.

## Lemma 2: low-boundary partitions under GF(2)-affine shuffles

The order of a quasiseparable factor \(S\) is \(r\) if both strictly lower and upper off-diagonal contiguous blocks have ranks at most \(r\). A scalar scan representation realizes the crossing rank inequality

\[
\operatorname{rank}S[A^c,A]\le r\,d(A),\qquad
d(A)=\#\{0\le j<N-1:\mathbf1_A(j)\ne\mathbf1_A(j+1)\}.
\]

This follows by cutting the forward/backward order-\(r\) scan channels at every boundary of \(A\). It includes arbitrary diagonal entries, zero coefficients, and singular factors.

Transport an input subset through the interstage index permutations. By the standard telescoping product-rank inequality, for a \(t\)-factor network with stage orders \(r_1,\dots,r_t\),

\[
\operatorname{rank}M[A_t^c,A_1]\le\sum_{j=1}^t r_jd(A_j).
\]

When the index permutations are affine invertible bit maps \(x\mapsto Lx\oplus c\), a parity set is transported to another parity set, whose mask transforms linearly as \(a\mapsto L^Ta\) (possibly with its parity sign flipped). This transformation is invertible on nonzero masks. If the lowest \(q\) bits of a transported mask are zero, membership is constant on each block of \(2^q\) consecutive integers, so

\[
d(A)\le N/2^q-1.
\]

The orientations of permutation matrices are immaterial provided the corresponding inverse/transpose map is consistently used. Code records these orientations explicitly.

## Theorem 3: heterogeneous binary-affine depth/width obstruction

Suppose \(F_N\) factors into \(t\) two-sided quasiseparable stages of orders \(r_1,\ldots,r_t\ge1\), with arbitrary GF(2)-affine permutations between stages and natural Fourier endpoints (or additional GF(2)-affine endpoint coordinate changes). Let \(q_1,\ldots,q_t\ge1\) be integers with

\[
\sum_{j=1}^t r_j2^{-q_j}\le1/4.
\]

A **necessary condition** for exact factorization is

\[
\boxed{\sum_{j=1}^t q_j\ge k=\log_2N.}
\]

**Proof.** Suppose instead \(\sum_jq_j<k\). Starting with a free \(k\)-bit mask, requiring its transported mask to have its bottom \(q_j\) bits zero at stage \(j\) gives at most \(\sum_jq_j<k\) homogeneous GF(2) linear equations in \(k\) unknown bits. They have a nonzero solution \(a\). Every transported mask stays nonzero because the coordinate maps are invertible. Its stage boundary count is at most \(N2^{-q_j}-1\), giving

\[
\operatorname{rank}M[R,C]\le\sum_j r_j(N2^{-q_j}-1)
\le N/4-\sum_jr_j <N/4.
\]

But \(C\) and \(R\) are nonempty parity halfsets, and Theorem 1 gives \(\operatorname{rank}F_N[R,C]\ge N/4\), a contradiction. No stage coefficients, invertibility, or numerical approximation enter the argument. **QED.**

For uniform order \(r\), choose \(q_j=q=\lceil\log_2(4rt)\rceil\). Therefore

\[
\boxed{k\le t\lceil\log_2(4rt)\rceil.}
\]

For fixed \(r\), \(t=\Omega(k/\log k)=\Omega(\log N/\log\log N)\) within this architecture. This is a stage-depth restriction; an arithmetic-operation lower bound requires an additional explicit per-stage charging model.

### Fixed rank-one thresholds

- \(t=2,q=3\): if \(k\ge7\) then impossible for every binary-affine shuffle.
- \(t=3,q=4\): if \(k\ge13\) then impossible.
- \(t=4,q=4\): if \(k\ge17\) then impossible.
- \(t=5,q=5\): if \(k\ge26\) then impossible.

The theorem does **not** cover non-affine index permutations, arbitrary rank-growing global stages, or general FFT circuits. The numerical thresholds are sufficient, not proved sharp. This is a project-specific deduction based on universal Fourier sampling and the previous moving-partition rank lemma, without claiming priority over the literature.

## References for imported facts

1. B. Osgood, A. Siripuram, W. Wu, *Discrete Sampling and Interpolation: Universal Sampling Sets for Discrete Bandlimited Spaces*, IEEE Transactions on Information Theory 58(7), 4176–4200 (2012). arXiv: https://arxiv.org/abs/1204.0992. The balanced-residue characterization of universal sampling sets is used in Theorem 1.
2. S. Delvaux, M. Van Barel, *Rank-deficient submatrices of Fourier matrices*, Linear Algebra and its Applications 429 (2008), 1587–1605. DOI: https://doi.org/10.1016/j.laa.2008.04.043. Background on ranks of Fourier submatrices for prime-power lengths.
3. Prior self-contained archive in `prior_checkpoint_full.zip`: moving-partition rank inequality, scan-network verifier, and exact rank/cut certificates.
