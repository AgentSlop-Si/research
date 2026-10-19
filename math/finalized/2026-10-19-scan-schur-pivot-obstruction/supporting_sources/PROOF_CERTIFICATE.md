# Exact proof certificate: multi-stage rank-one scan algebraic dimension

**Date:** 2026-10-09. Statements are made over the complex field in an input-independent scalar-linear stage model. Every stage has a permitted scalar O(N) executor; no FFT complexity claim is made.

## Model and notation

For `N >= 3`, define `V_N` to be the matrices

\[
S_{ij}=\begin{cases}
 a_i b_j,&i>j,\\
 d_i,&i=j,\\
 c_i e_j,&i<j.
\end{cases}
\]

This is the **separated-generator chart** of two-sided quasiseparable order one, not a statement about every singular/exceptional quasiseparable matrix. Its parameterization uses `5N` scalars (some inactive or redundant). For fixed permutations `P_1,...,P_{t-1}`, let

\[
\mathcal M_{N,t}(P)=\{S_tP_{t-1}S_{t-1}\cdots P_1 S_1:S_i\in V_N\}.
\]

The closure and dimension are in the complex Zariski topology. `P_i` may be independently chosen from any of the finitely many `N!` permutations; a finite union has dimension the maximum of its pieces.

## Theorem A: upper bound for all sizes and permutations

For all `N >= 3` and integer `t >= 1`,

\[
\boxed{\dim\overline{\mathcal M_{N,t}(P)}\le
\min\{N^2,\,N+t(4N-6)\}.}
\]

**Proof.** The strictly lower outer-product triangular chart has active coefficient vectors
`(a_1,...,a_{N-1})` and `(b_0,...,b_{N-2})`. On a dense open set with their entries nonzero, the only redundancy is the simultaneous scaling `(a,b)->(\lambda a,\lambda^{-1}b)`. Thus the image dimension is `2N-3`. The strictly upper chart has the same dimension, and its coefficients are independent from the `N` diagonal entries. Hence

\[
\dim V_N=N+2(2N-3)=5N-6.
\]

Restrict to the dense open set where all `S_i` are invertible. Across each internal permutation `P_j`, insert an arbitrary invertible diagonal matrix `D_j`, moving `D_j` to the left factor and `P_j D_j^{-1}P_j^{-1}` to the right factor. Explicitly, with missing boundary terms omitted,

\[
S_j\mapsto D_j S_j P_{j-1}D_{j-1}^{-1}P_{j-1}^{-1}.
\]

Every stage remains in `V_N` because left/right diagonal scaling preserves the separated outer-product triangular form. The full product remains exactly unchanged: each `D_j` cancels its neighbor. These `t-1` independent diagonal tori have dimension `(t-1)N`, and their action on an invertible stage tuple is free: the first transformed invertible stage forces `D_1=I` if fixed, then recursively each subsequent `D_j=I`. The fiber-dimension inequality therefore gives

\[
\dim \overline{\mathcal M_{N,t}(P)}
\le t(5N-6)-(t-1)N=N+t(4N-6).
\]

The ambient dimension supplies the additional cap `N²`. The upper bound continues to hold on the whole image because the invertible stage tuples form a dense open subset of the irreducible stage parameter space. QED.

**Generic-depth corollary.** If `N+t(4N-6)<N²`, the image of the map is contained in a proper algebraic subset. Even allowing **all** independent intermediate and endpoint permutations makes only a finite union of such proper algebraic subsets, still proper. Thus a Zariski-generic complex matrix requires

\[
\boxed{t\ge\left\lceil\frac{N^2-N}{4N-6}\right\rceil.}
\]

When `4|N` and `N>=4`, this ceiling is exactly `N/4+1`: at `t=N/4` the upper bound is `N²-N/2`, while at `t=N/4+1` it exceeds `N²`.

## Theorem B: exact bit-reversal dimension for N=8,16,32

Let `N=8,16,32`. For every stage boundary choose the **same** permutation `P`, reversing the `log₂ N` binary digits. For each integer `1<=t<=N/4+1`,

\[
\boxed{\dim\overline{\mathcal M_{N,t}(P)}
=\min\{N^2,N+t(4N-6)\}.}
\]

**Proof by explicit exact certificates.** The stage-product coordinates are integer polynomials in the stage generator parameters. The derivative with respect to each generator parameter is an integer-polynomial vector of length `N²`. At the explicit integer parameter values in `WITNESS_N*_T*.json` for the full-rank cases, or the deterministic parameter-generation recipe in `multistage_jacobian.py` for smaller depths, modular Gaussian elimination gives a Jacobian minor of size equal to the upper bound with nonzero determinant modulo 12,289. The same ranks are reproduced modulo 65,537. A nonzero modular determinant proves the corresponding integer determinant is nonzero, therefore the complex Jacobian rank is at least the stated value. Theorem A gives the reverse inequality.

For complete details at each depth, `BITREV_RESULTS.json` gives **34 exact field ranks**. `independent_verifier.py` reconstructs all derivatives independently using left and right matrix products, and checks the following full-row determinants:

| N | t | determinant mod 12289 | determinant mod 65537 |
|---:|---:|---:|---:|
| 8 | 3 | 5222 | 41948 |
| 16 | 5 | 4288 | 60210 |
| 32 | 9 | 848 | 41818 |

All full-dimensional witnesses have **invertible individual stages**. At the full-rank points the complex holomorphic submersion theorem implies the image contains a nonempty Euclidean open set, and in fact the polynomial map is dominant. Theorem B concerns **these three lengths only**, not arbitrary `N`. QED.

## Theorem C: gauge completeness immediately below saturation

At `(N,t)=(8,2),(16,4),(32,8)` and the saved integer sample points, the exact Jacobian kernel is precisely the span of the following explicit infinitesimal gauge directions:

- `6t` local redundancies: four inactive generator coordinates and two lower/upper pair scalings in each stage;
- `(t-1)N` cross-stage diagonal row/column scalings, matched through the bit-reversal permutations.

The dimensions are respectively `20`, `72`, and `272`. `gauge_audit.py` constructs every tangent vector, verifies `J G=0`, and independently verifies `rank G = nullity J` over both primes. These are finite-point exact tangent statements. **No all-N theorem about generic gauge completeness** is claimed.

At the full-dimensional threshold the Jacobian has additional kernel dimensions caused by exhausting the ambient `N²` coordinates; thus not all null directions are gauges there.

## Theorem D: identity shuffles cannot achieve comparable full dimension

Every separated-generator stage has quasiseparable upper/lower rank at most one. For two matrices in the **same coordinate ordering**,

\[
q(AB)\le q(A)+q(B)
\]

because the upper-right block of `AB` at any cut is `A_LL B_LR + A_LR B_RR` and the analogous lower-left formula holds. Therefore with all `P_j=I`, every `t`-stage output satisfies `q(M) <= t`. A generic `N×N` matrix has `q(M)=floor(N/2)`. If `t<floor(N/2)`, the identity-shuffle product image cannot be dominant, whereas Theorem B verifies that repeated bit reversal can be dominant at the three stated lengths.

## Cost and scope

One rank-one separated-generator scan stage can be evaluated by two running sums with at most `5N` scalar multiplications and `4N` scalar additions under a deliberately unoptimized full-charge reference count. `t=N/4+1` such stages cost `Theta(N²)` arithmetic, plus index and coefficient work. These witnesses are **not Fourier factorizations**. Nothing here proves any bound above `Omega(N)` on *unrestricted* exact Fourier arithmetic circuits, or a new `O(N)`/`o(N log N)` FFT.

The all-length saturation of this bound under repeated bit reversal is a **conjecture supported by N=8,16,32**, not a proved general statement. Different transition generators and zero-corner boundary components of the broader QS order-one class are not claimed to be covered by the separated-generator chart.
