# Phase 37 — projective phase curvature and complex two-mask Green pencils

**Date:** 2026-10-10. **Status:** Exact all-length curvature theorem for a *single cyclic Green*, and finite-length, all-complex-parameter exclusion certificates for a specified **six-resolvent, two-internal-mask** circuit. No new worst-case sub-`N log N` Fourier algorithm.

## Mathematical conventions

For `N = 2^m >= 4`, let `omega = exp(-2*pi*i/N)`. A Fourier matrix, normalized or not, has entries proportional to `omega^(jk)`. We allow **arbitrary nonzero** outer row/column scalings and permutations (a larger equivalence class than unitary monomial equivalence).

For an entrywise-nonzero matrix `M` define its anchored cross ratios

`R_(i,j)^(a,b) = M[i,j] M[a,b] / (M[i,b] M[a,j])` for `i != a, j != b`.

These are invariant under arbitrary outer diagonal scalings; arbitrary outer permutations only relabel the indices and anchors. If all anchored ratios are `N`th roots of unity, define the **exponent-curvature matrix** `E^(a,b)` over `Z/NZ` by `R = omega^E`. This is an exponent *of a ratio*, not the argument of an individual matrix entry.

## Theorem 37A — exact curvature rank difference

Let `W` be any `N`-cycle with positions `p_i`, let `alpha != 0`, `alpha^N != 1`, and `G=(I-alpha W)^(-1)`. Assume `alpha^N=omega^c` with `gcd(c,N)=1`.

**For every choice of row anchor `a`, column anchor `b`, and independent input/output permutations, the anchored exponent-curvature matrix of `G` has determinant a unit in `Z/NZ`.** Its reduction mod 2 has rank exactly `N-1`.

By contrast, for any matrix monomially equivalent to the Fourier matrix, its exponent curvature is an outer product and has rank one after reduction mod 2. Hence `G` is not Fourier-equivalent for `N>=4`.

### Proof, including arbitrary anchors

The Green kernel is

`G[i,j]=alpha^((p_i-p_j) mod N)/(1-alpha^N)`.

Writing `s(u,v)=1` when `u<v` and `0` otherwise, we have

`(u-v) mod N = u-v+N*s(u,v)`.

Consequently the anchored Green ratio is

`R_(i,j)^(a,b) = omega^{c (s(p_i,p_j)-s(p_i,p_b)-s(p_a,p_j)+s(p_a,p_b))}`.

In cycle coordinates take anchors `a=b=0`. For `i,j=1,...,N-1` the exponent matrix is

`E[i,j] = -c*1_(i>=j)`.

This matrix is lower triangular, with diagonal `-c`, and determinant `(-c)^(N-1)`, a unit modulo `N` when `gcd(c,N)=1`.

For general anchors let `T[i,j]=s(i,j)`, and let `u_i=e_i-e_a`, `v_j=e_j-e_b`. Then the anchored exponent is the bilinear pairing `u_i^T T v_j`. The vectors `{u_i: i != a}` and `{v_j: j != b}` are each an integer basis of the lattice of zero-sum integer vectors. Changing anchors therefore acts by **unimodular integer** basis changes, preserving the determinant up to sign. Independent row/column permutations also induce unimodular reordering. The factor `c` preserves invertibility modulo `N`.

For the Fourier matrix with row labels `r_i` and column labels `c_j`, including permutations,

`R_(i,j)^(a,b) = omega^{(r_i-r_a)(c_j-c_b)}`.

Thus `E_(i,j)=(r_i-r_a)(c_j-c_b)` is an outer product. Since `N` is even and both label permutations include both parities, its mod-2 rank is **exactly one**. The Green reduction has mod-2 rank `N-1`.

### Exact characteristic-two shortcut

Over any odd finite field containing the `N`th roots, the parity of `E` is obtained without a discrete logarithm:

`R^(N/2) = (-1)^E`.

This yields an exact GF(2) rank gate that is invariant under arbitrary external monomial gauges and permutations. The theorem is restricted to primitive `N`th-root Green holonomy: nonprimitive holonomies may have smaller parity rank. That does not weaken the claim for the primitive family.

The underlying cross-ratio invariance is classical in complex Hadamard theory (Haagerup-type invariants). The anchored integer-lattice determinant is the specific graph-resolvent deduction used in this project, not a claim of independently established novelty.

## Theorem 37B — two plaquettes exclude an entire complex coupling family

Consider a **fixed-mask, two-mask, three-stage Green circuit**

`M_N(lambda)=A_N D1_N (G2_N+lambda G3_N) D2_N C_N`,

with `A_N=G0_N+w_A G1_N` and `C_N=G4_N+w_C G5_N`. Its six cycle orders are explicitly generated in `phase37_curvature.py:seeded_cycles(N,37037)` and serialized verbatim in the certificate files.

Each `G_s=(I-alpha_s W_s)^(-1)` uses an independently ordered Hamiltonian cycle and has coefficients in `Q(i)`. The exact constants are

```
alpha = [(1+i)/4, (2+i)/7, (1+2i)/8, (1-i)/5, (2+i)/9, (1+i)/6]
w_A = (1+i)/3        w_C = (1-i)/4
D1[j] = i^((3*j+1) mod 4)
D2[j] = i^((j*j+j+1) mod 4)
```

All denominators are nonsingular over `Q(i)` since `|alpha_s|<1`.

### Two necessary Fourier equations

Let `m_ij(lambda)` be an entry of `M_N(lambda)`. Because the **only** remaining variable is the scalar `lambda`, each `m_ij` has polynomial degree at most one. Define

`f_j(lambda) = [m_00(lambda)*m_1j(lambda)]^N - [m_0j(lambda)*m_10(lambda)]^N`, for `j=1,2`.

Both have degree at most `2N`. If `M_N(lambda)` were monomially equivalent to a Fourier matrix, every `2 x 2` cross ratio would be an `N`th root of unity **regardless of the unknown external permutations and nonzero diagonal scalings**. Hence both `f_1(lambda)=0` and `f_2(lambda)=0` are necessary, even when we allow arbitrary complex external gauges.

### Exact finite-field Bézout/resultant certificates

For `N=4,8,16,32,64,128`, the code generates both polynomials by executing the six Green recurrences on basis columns—not by multiplying dense `N x N` matrices. Their coefficients are rational Gaussian integers and reduce in the two independent splitting primes

- `p1=998244353`, with primitive generator `3`;
- `p2=2013265921`, with primitive generator `31`.

In **both** fields, at each listed size, the two reductions have full degree `2N`, nonzero leading coefficients, and polynomial gcd `1`. Each saved certificate contains polynomials `f_1, f_2` and Bézout coefficients `u, v` satisfying the exact finite-field identity

`u(lambda)*f_1(lambda)+v(lambda)*f_2(lambda)=1 (mod p)`.

The nonvanishing leading coefficients prove that reducing the characteristic-zero polynomials does **not** reduce their degree. If `f_1,f_2` had a common complex root, the Sylvester resultant over `Q(i)` would vanish. Since the coefficients lie in `Q(i)`, the resultant is in that field, and the compatible finite-field reduction has a nonzero resultant (gcd `1` and degrees preserved), a contradiction. Therefore the polynomials have no common root over `C`.

**Conclusion at precisely the certified sizes:** no complex `lambda` can make this **specified fixed-mask, fixed-outer-parameters** circuit equal to a Fourier transform up to arbitrary external permutations and invertible row/column scalings. This is a finite-length family exclusion, NOT an all-`N` theorem and NOT an exclusion of freely tunable internal masks or Green generator parameters.

An independent direct symbolic computation over `Q(i)` verifies the whole gcd argument for `N=4` (`charzero_control.py`). Full direct symbolic expansion at `N=8` was not completed because of excessive symbolic cost; it is **not** claimed as validation. The exact modular Bézout and characteristic-zero resultant reasoning are sufficient for the stated certified sizes.

### Application cost

Every `(I-alpha W)^(-1)` can be applied by one cyclic linear recurrence in `O(N)` arithmetic. The circuit has six Green solves, two diagonal masks, and two sum operations, hence `O(N)` field arithmetic *per application*, once its cycle lists and constants are available. Computing `f_1,f_2` requires a constant number of basis-vector circuit applications, plus polynomial arithmetic to build and certify the resultant. The polynomial arithmetic is a **research preprocessing/certification cost**, not a hidden step in a successful FFT algorithm; this candidate is excluded from computing the DFT.

## Controls and reproducibility

- Primitive-holonomy Green: every anchored ratio is an `N`th root, but projective parity-curvature rank is `N-1`, for every tested randomized external gauge/permutation and anchors.
- Hidden permuted-and-scaled Fourier: projective parity-curvature rank exactly `1`.
- Deliberately planted Fourier member `F+(lambda-lambda_*)B`: both necessary polynomial constraints share `(lambda-lambda_*)`; the verifier does not falsely exclude it.
- Exact Green recurrence agrees with independently constructed dense kernels. The two-mask circuit is linear on arbitrary input vectors.
- Two independently implemented finite-field settings agree through `N=128`. Explicit Bézout polynomials are saved for both fields.
- The 19 inherited Phase 36 regressions pass. The new Phase 37 regressions are in `tests_phase37.py`.

## What remains open for Phase 38

**Do not confuse phase complexity with entrywise phase-matrix rank.** The former must reproduce the whole projective exponent structure and the Weyl equations, not merely many distinct phases. We need to design **jointly tunable internal complex phase masks and noncommuting Green weights** that force low-rank bilinear Fourier curvature without losing an `O(N)` reusable execution graph. Any exceptional construction must be verified on *all* inputs, and its parameter generation, precision, and total arithmetic cost counted. The present research has NOT beaten worst-case `N log N`.

**Boundary qualification:** The `N=4` test is a small-size algebraic control, where two of the six cycle successors happen to be affine. At every certified `N>=8`, all six seeded cycle successors are distinct and non-affine; the exact test suite checks this explicitly.
