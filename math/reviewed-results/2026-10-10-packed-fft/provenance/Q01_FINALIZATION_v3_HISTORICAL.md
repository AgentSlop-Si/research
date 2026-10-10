# All length normwise Fourier computation

## Canonical theorem and two proof routes

10 October 2026

The canonical result is the corrected interpolation construction [A]. The independently audited Taylor construction [B, C] is an alternative proof for two accuracy regimes and supplies a useful exact correction-rank diagnostic. Both use a deterministic pointwise error contract for a finite-word dyadic backend. This consolidation adds no asymptotic improvement or historical-priority claim. The exact Necklace–Green factorization remains a separate open problem.

## 1 Canonical theorem and computational contract

Fix an input-format constant \(c\). Let \(N\ge2\), \(n=\lceil\log_2(N+1)\rceil\), and let the integer precision exponent \(t\) be supplied with \(2\le t\le n\). Set \(\varepsilon=2^{-t}\). Every real and imaginary input component is a dyadic with \(O(cn)\) description bits and polynomial dynamic range. For example,

\[
x_j=(a_j+i b_j)2^{-B},\qquad
|a_j|,|b_j|\le N^c,\quad |B|\le cn.
\]

Separate coordinate exponents with absolute value at most \(cn\) are allowed. The machine is an address-capable word RAM with \(w=C(c)n\) bits for a sufficiently large fixed constant, supporting integer addition, subtraction, multiplication, division, comparisons, shifts, Boolean operations and indexed access. Online operands occupy a fixed number of words. Larger rational computations used in coefficient certification incur their full multiword cost.

There is one uniform deterministic algorithm that writes all \(N\) finite dyadic mantissa/exponent outputs and satisfies, for every represented input,

\[
\|y-U_Nx\|_2\le 2^{-t}\|x\|_2,\qquad
(U_N)_{k,j}=N^{-1/2}e^{-2\pi i kj/N}.
\tag{1}
\]

Its storage is \(O(N)\) words throughout this precision domain. Every table entry, coefficient certificate, memory operation, normalization, gather/scatter, address calculation and output write is charged. Zero input returns zero; \(N=1\) is an exact copy. The guarantee is relative Euclidean error, not per-coordinate relative error, correct rounding or exact norm preservation.

For every supplied schedule \(t=o(n)\), the eventual cold running time is

\[
O\!\left(\frac{Nn}{\log_2(n/(t+\log_2 n))}\right)=o(N\log N).
\tag{2}
\]

The denominator is used only in its eventual positive growing range. Consequently:

- Fixed accuracy and \(\varepsilon=(\log N)^{-a}\), for fixed \(a>0\) and an efficiently supplied dyadic target within a constant factor, give \(O(N\log N/\log\log N)\).
- Supplied \(t=\lceil n^\beta\rceil\), for fixed \(0<\beta<1\), gives the same order, with a constant depending on \(\beta\).

Reading the accuracy specification and generating \(t\) are separately charged. A non-power-of-two dyadic target is rounded down to the next power of two. Computability alone is not an efficient precision schedule.

The fast branch runs only when its radix exists, its interpolation stencil has distinct indices and its certified preparation work/space bound is at most \(N\). Otherwise the certified direct fallback takes \(N^2\operatorname{poly}(n+t)\) work with \(O(N)\) words for \(2\le t\le n\). Arbitrary supplied precision outside that domain has a separate fallback using \(w=C(c)(n+t+1)\) and \(O(N)+\operatorname{poly}(n+t)\) words; those larger costs are not hidden in (2). Polynomial accuracy does not inherit a sub-\(N\log N\) saving. See [A, Theorem 1 and §§5, 9–10](sources/INTERPOLATION_PROOF.md).

This is the accepted mathematical construction. It is not a certified production implementation, fixed-binary64 runtime statement, bit-complexity breakthrough or exact-complex arithmetic algorithm.

## 2 Pointwise backend composition

All norms below are Euclidean vector norms or their induced operator norms. This elementary lemma packages the common stability argument without assuming a rounded backend is linear.

**Lemma.** Let \(U\) be the target linear map and suppose

\[
T=\sum_{r=1}^R C_r V_r B_r,\qquad \|U-T\|\le\tau,
\]

where the linear maps have compatible finite dimensions. For each represented input \(x\), let the actual supplied backend input \(v_r(x)\) satisfy

\[
\|v_r(x)\|\le b_r\|x\|,\qquad
\|v_r(x)-B_rx\|\le\beta_r\|x\|.
\]

Assume every such input lies in the represented domain of a possibly nonlinear backend \(A_r\) with

\[
\|A_r(v)-V_rv\|\le\delta_r\|v\|.
\]

Let the implemented linear output map \(\widehat C_r\) obey
\(\|\widehat C_r\|\le c_r\) and
\(\|\widehat C_r-C_r\|\le\gamma_r\).
If the actual reported value has the form

\[
y=\sum_r\widehat C_r A_r(v_r(x))+e(x),
\qquad \|e(x)\|\le\eta\|x\|,
\]

then

\[
\|y-Ux\|\le
\left[\tau+\eta+
\sum_r\left(c_r\delta_r b_r+
\gamma_r\|V_r\|b_r+
\|C_r\|\|V_r\|\beta_r\right)\right]\|x\|.
\tag{3}
\]

**Proof.** For each channel, insert and subtract the exact intermediate values to obtain

\[
\begin{aligned}
\widehat C_r A_r(v_r)-C_rV_rB_rx
={}&\widehat C_r\bigl(A_r(v_r)-V_rv_r\bigr)\\
&+(\widehat C_r-C_r)V_rv_r
+C_rV_r(v_r-B_rx).
\end{aligned}
\]

The three terms have norm at most, respectively,
\(c_r\delta_r b_r\|x\|\),
\(\gamma_r\|V_r\|b_r\|x\|\) and
\(\|C_r\|\|V_r\|\beta_r\|x\|\).
Sum the channel bounds and add
\(\|(T-U)x\|\le\tau\|x\|\) and \(\|e(x)\|\le\eta\|x\|\).
This proves (3), including \(x=0\). Neither \(A_r\) nor the input preprocessing \(v_r(x)\) was assumed linear. ∎

Every certificate concerns the actual supplied input. Equation (3) gives no free preparation, representation conversion or data movement. Distinct required tables must be constructed; legitimate shared preparation may be paid once within a cold call. Wrapper arithmetic, all backend calls, accumulation and output remain charged.

## 3 Applying the common contract

### Interpolation is the canonical route

For \(M=2^{\lceil\log_2(4N)\rceil}\), [A, §§2–3](sources/INTERPOLATION_PROOF.md) gives centered padding \(Z\), unitary \(U_M\), a phase diagonal \(D\), and an interpolation map \(B\) with

\[
U_N=DBU_MZ,\qquad \|B\|<3.
\]

For \(\rho=\varepsilon/1024\), the certified implementation uses
\(\widehat C=E\widetilde B\), with
\(\|\widetilde B-B\|\le2\rho\),
\(\|\widetilde B\|<3\),
\(\|E\|<2\) and \(\|E-D\|\le3\rho\).
Hence \(\|\widehat C\|<6\) and
\(\|\widehat C-DB\|\le4\rho+9\rho=13\rho\).

Apply the lemma to the normalized input \(a=x/R\), with one channel, \(b_1=1\), \(\beta_1=\tau=0\), \(\delta_1=\rho\) and \(\|V_1\|=1\). The prequantization error is at most \(19\rho\|a\|\), so the prequantized output has norm at most \((1+19\rho)\|a\|<2\|a\|\). Final rounding adds at most \(3\rho\|a\|\). Exact restoration of the scale \(R\) therefore gives
\((6+13+3)\rho\|x\|=22\rho\|x\|<\varepsilon\|x\|\). This recovers [A, §4](sources/INTERPOLATION_PROOF.md). The all-entry tables, total quantizer, initial rounding, coefficient certificates and fallback in [A, §§1, 3, 5, 9–10](sources/INTERPOLATION_PROOF.md) provide the computational obligations behind (1)–(2).

### Taylor is an alternative for two regimes

Let \(L\) be the least power of two at least \(2N\). The centered Taylor lift [B, §§2–4](sources/TAYLOR_PROOF.md) is a sum of \(R\) diagonally scaled copies of \(U_L\), with contraction input masks and an analytic remainder at most \(4/R!\). Its ideal output-map norm sum is less than 6. Thus a backend pointwise error is controlled without asserting that the executed map is one fixed matrix.

With \(R!\ge16/\varepsilon\), \(\delta=\varepsilon/128\) and
\(q=\lceil\log_2(512R^2/\varepsilon)\rceil\), the accepted outer estimates give

\[
\|y-U_Nx\|_2\le
\left(4/R!+12\delta+64R^2 2^{-q}\right)\|x\|_2
<\varepsilon\|x\|_2.
\]

The certified mask, coefficient, endpoint and exact-dyadic accumulation estimates instantiate (3); their constants remain those in [B, §4](sources/TAYLOR_PROOF.md) and [C, Outer finite precision](sources/TAYLOR_ACCEPTANCE.md). Taylor gives the same fixed-accuracy order as (2), but its inverse-polylogarithmic bound is only \(O_a(N\log N/\log\log\log N)\), weaker than interpolation. Both use \(O(N)\) words in these regimes. The Taylor audit does not extend this composite construction to all supplied \(t=o(n)\) schedules. It does not replace the canonical precision domain or fallback.

Taylor's exact correction matrix has rank \(N/\gcd(N,L)\), so an exact separated correction needs that many terms, including \(N\) at odd lengths [B, §7](sources/TAYLOR_PROOF.md). This is a representation-specific statement, not a lower bound for arbitrary Fourier algorithms. The source's on-demand reference executor establishes no eager-table runtime claim [C, Computational contract and Catalogue disposition](sources/TAYLOR_ACCEPTANCE.md).

## 4 Separate exact transport gate

The Necklace–Green source concerns exact scalar arithmetic over \(\mathbb C\), or a field containing a supplied primitive \(N\)-th root \(\omega\), and the unnormalized matrix \((F_N)_{i,j}=\omega^{ij}\), initially for \(N=2^n\). In either setting the primitive root is supplied. It computes an auxiliary operator \(T_N=P_N^T H_NP_N\); it does not supply a growing uniform low-work choice with \(T_N=F_N\). See [D, §§1, 4, 7](sources/NECKLACE_THEORY.md).

For \(S e_j=e_{j+1\bmod N}\) and \(D_\omega=\operatorname{diag}(1,\omega,\ldots,\omega^{N-1})\), the exact gate is

\[
T_Ne_0=\mathbf1,\qquad T_NS=D_\omega T_N.
\]

These identities are necessary and sufficient: induction gives \(T_Ne_j=D_\omega^j\mathbf1\), precisely every Fourier column. A valid construction must also charge parameter generation, root supply, nonzero-denominator checks, addressing, transport application and transpose, and output. Ordinary transpose here is not conjugate transpose.

For the canonical carrier \(\Psi=\operatorname{tr}(B^k)\), characteristic dividing \(k\) is excluded: cyclicity gives \(d\operatorname{tr}(B^k)=k\operatorname{tr}(B^{k-1}dB)=0\), hence its formal Hessian vanishes. The sparse-Gram division formula additionally requires nonzero baselines; the polynomial circuit remains the zero-baseline route [D, §5](sources/NECKLACE_THEORY.md).

The composition lemma proves none of the missing exact identities. This gate remains open; no new exact Fourier speedup or historical novelty follows from the consolidation.

## Source versions

The linked text files are unchanged source snapshots. SHA-256 identifies the precise versions.

- **A.** [Corrected interpolation proof](sources/INTERPOLATION_PROOF.md), Theorem 1; §§1–5, 9–10. SHA-256: `c8a775230a824872c23fc48b351e03d63878154bcfb314a8cca689842e31fc8d`.
- **B.** [Taylor lift proof](sources/TAYLOR_PROOF.md), §§2–7. SHA-256: `1716f38b2be430287973ea76856c3173770e873d102e4bf339d0084d4c994b77`.
- **C.** [Independent Taylor acceptance and scope](sources/TAYLOR_ACCEPTANCE.md), Computational contract, Outer finite precision, and Catalogue disposition. SHA-256: `d1b12a9a7e3e00695e9f73e0addc8b21c6316bfe2f22ea47afc62659df161f00`.
- **D.** [Necklace–Green theory](sources/NECKLACE_THEORY.md), §§1, 4–7. SHA-256: `8f9e1d4a0de9826fba802e885f7cff244119dffcb543153d6a25173c804eaaea`.

Prior mathematical acceptance is reused at its stated scope. No historical test is presented as rerun here. Production implementation, practical crossover and external priority remain unverified.
