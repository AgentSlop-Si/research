# Library text-read transcript
Source: [private-id]
File: FFT_THEORETICAL_GATE_2026-10-10.md
This is the full returned text; byte identity with the backing file is not asserted.

# FFT Theoretical Gate — October 10, 2026

**Question.** Can the user's Green/graph-union/phase-bank/scan machinery yield a fully charged exact all-output DFT of every fresh arbitrary input in $O(N)$ or at least $o(N\log N)$ scalar operations?

**Conclusion.** No exact all-input linear-time algorithm is established by the archived identities. Several tempting constant-stage architectures are excluded by elementary all-$N$ theorems. A non-affine, **branched** or **dense-inverse** global-scan architecture survives the listed exclusions, but lacks an all-$N$ exact Fourier construction. The surviving open issue is not the speed of a recurrence: it is whether the recurrence has the *right Fourier coefficients*.

## Precise contract

Let $F_N[k,j]=\omega_N^{kj}$, $\omega_N=e^{-2\pi i/N}$, or the normalized version $U_N=F_N/\sqrt N$. Distinguish exact complex-register arithmetic from finite-precision word-RAM computations; explicitly charge construction of fixed coefficients, all preprocessing, all vector operations, indexing and full $N$-coordinate output. A finite-size factorization or a randomized additive approximation is not a universal exact FFT.

## Gate 1 — pure non-affine Green product **excluded** at constant depth

Let $A_i=I-D_iP_i$ be invertible; each $D_i$ is diagonal and each $P_i$ is *any* permutation matrix, including non-affine Hamiltonian cycles. Put $G_i=A_i^{-1}$. Suppose

$$F_N=L_0 G_1L_1G_2\cdots G_tL_t,$$

where each $L_i$ is an invertible monomial matrix (diagonal times permutation). The inverse is a product of monomial and row-2-sparse matrices. If $B,C$ have row sparsities at most $a,b$, then $BC$ has row sparsity at most $ab$. Thus $F_N^{-1}$ has at most $2^t$ nonzeros per row. Since **all $N$ entries of each row of $F_N^{-1}$ are nonzero**, necessarily

$$\boxed{t\ge\lceil\log_2N\rceil.}$$

No permutation expansion property can defeat this inverse-support certificate. It **does not** apply to sums/branches of Green inverses or globally dense inverse stages. It also does not rule out a fundamentally fused computation rather than separately executed factors. This is the $s=2,r=0$ member of the sparse-defect lineage already present in `fft_sparse_defect_green_gate_2026-10-10.zip`.

## Gate 2 — bounded-affine-run Green sums **excluded** at constant total term count

Green Phase 26 supplies a common balanced character cut for the entire allowed product of sums of weighted Green inverses when the cycle edges lie in boundedly many affine runs, with bounded exceptional bridge count and only affine intermediate permutations. If $Q$ is the **total count of Green summands**, $d$ the maximum number of step magnitudes per term, $s\le dQ$ the count of distinct transformed steps, $B$ the total bridges, and $r=\lfloor(N-1)^{1/s}\rfloor$, then for a particular balanced block $I,J$,

$$\operatorname{rank}M[I,J]\le \frac{2dQN}{r}+B.$$

For the normalized DFT every balanced $N/2\times N/2$ submatrix $H$ obeys $\|H\|_F^2=N/4$ and $\|H\|_2\le1$, and so $\operatorname{rank}H\ge N/4$ regardless of endpoint monomial maps. Therefore, for bounded $d$ and bounded bridges per term, **exact** equality forces

$$\boxed{Q=\Omega(\log N/\log\log N).}$$

This is a lower bound on **terms in this restricted architecture**, not an unrestricted arithmetic lower bound; the $Q\asymp\log N/\log\log N$ regime is not ruled out. To escape with $O(1)$ terms, abandon the bounded-affine-run assumption or adopt a different globally mixing operator.

## Gate 3 — phase-bank reconstruction identity is full-rank but not a speed theorem

Hero #1 v13 constructs $M$ mutually orthogonal rank-$N/M$ projectors $Q_t=P_t/M$ with $\sum_{t=0}^{M-1}Q_t=I_N$. Thus

$$F_N=\sum_t F_N Q_t$$

is exact. However $r<M$ of these sketches, followed by *arbitrary output-side linear decoding*, have combined rank at most $rN/M<N$. For the **unitary** Fourier operator $U_N$, any such rank-deficient approximation $A$ has $\|U_N-A\|_2\ge1$. Taking all $M$ simply recovers the original problem $F_Nx$. In Hero #1's exact arithmetic accounting the unshared scans cost at least $\Omega(MN)$ for the target $M\asymp\log N$.

To claim savings, produce an **explicit joint executor** with all input compressions, cross-bank recurrence steps, root generation, output restoration and word operations charged. A rank identity is not an executor.

## Gate 4 — a single low-rank global quasiseparable scan is not the DFT

Any single rank-$r$ separated-generator quasiseparable scan (up to outer monomial permutations) has a balanced cross block of rank at most $r$. Since every balanced Fourier block has rank $\ge N/4$, a single such stage requires $r\ge N/4$. At $O(Nr)$ per scan this is not a linear-time single-stage FFT. Products with genuinely independent non-affine internal shuffles are **not** excluded by this one-stage argument; a graph min-cut obstruction may disappear even while a higher-degree polynomial coefficient-compatibility obstruction remains.

The separate N=8 two-rank-one-stage checkpoint reports all tested min-cut inequalities vacuous but generator-map dimension 60 rather than 64. Generic dimension $<64$ proves the family is not all matrices; it **does not** prove the specific Fourier matrix is excluded. An exact Fourier-specific polynomial certificate is still required.

## Gate 5 — exact Weyl/seed identity is a necessary and sufficient test

Put $S e_j=e_{j+1\pmod N}$, $D=\operatorname{diag}(1,\omega_N,\ldots,\omega_N^{N-1})$ and $v=(1,\ldots,1)^T$. Then

$$\boxed{T=F_N\quad\Longleftrightarrow\quad TS=DT\quad\text{and}\quad Te_0=v.}$$

**Proof:** $e_j=S^je_0$, so $Te_j=TS^je_0=D^jTe_0=D^jv=F_Ne_j$. The forward direction follows by inspecting Fourier columns. For $U_N$, replace $v$ by $v/\sqrt N$. For the opposite Fourier phase convention, invert $D$ accordingly.

The two Weyl intertwinings alone determine $T$ **only up to an overall scalar**; the seed fixes it. Establish these equations as *symbolic operator identities*, not merely on finitely many random vectors. Testing all $N^2$ entries by brute force verifies only an instance, not an asymptotic algorithm.

## Gate 6 — a new elementary obstruction, then a gauged two-sum target

### Ungauged sum: excluded by its diagonal

A weighted Hamiltonian cycle $T=D_aP_a$ has $T^N=pI$, where $p=\prod_j a_j$. If $I-T$ is invertible, $p\ne1$ and

$$G=(I-T)^{-1}=\frac{I+T+\cdots+T^{N-1}}{1-p}.$$

No $T^k$ with $1\le k<N$ has any nonzero diagonal entry because the underlying single cycle has not returned to its starting vertex. Thus

$$\boxed{G_{jj}=\frac1{1-p}\quad\text{for all }j.}$$

**Every finite sum of these unmodified Green inverses in one common coordinate basis has a constant diagonal**, regardless of whether its cycles are affine, random, expander-like or weighted. Independent left/right gauges or row/column permutations on the summands destroy this particular invariant. But $F_N[j,j]=\omega_N^{j^2}$ has diagonal entries $1$ at $j=0$ and $\omega_N\ne1$ at $j=1$ when $N\ge2$. Consequently an **ungauged sum cannot equal $F_N$ for any $N\ge2$**. This necessary condition is stronger than a random numerical Weyl failure for this exact restricted representation. It is not a no-go for diagonal-gauged sums.

### Common outer diagonal gauges: exact sparse-sandwich feasibility gate

The first elementary two-summand variant that escapes this *diagonal* argument is

$$F_N\stackrel{?}=L(A^{-1}+B^{-1})R,\qquad A=I-D_aP_a,\ B=I-D_bP_b,$$

where $L,R$ are **invertible diagonal gauges** and $P_a,P_b$ are arbitrary non-affine Hamiltonian cycles. Set $U=L^{-1},V=R^{-1}$. For invertible $A,B$ this is exactly equivalent to the **gauged sparse-sandwich identity**

$$\boxed{A\,U F_N V\,B=A+B.}$$

For **fixed** permutations, the $N^2$ entry equations are polynomials of total degree at most four in the $4N$ unknown diagonal parameters of $A,B,U,V$, subject to nonzero/invertibility constraints. The right-hand side has at most **three entries per row**, unlike a generic dense left-hand side. Solving or disproving this exact Fourier-specific coefficient system is a concrete research gate, *not* a claim that a solution exists. **Term-wise independent diagonal gauges** create an even larger family to investigate; they do not satisfy the displayed sparse-sandwich equation in general.

A numerical optimizer failure or failure to find points in one finite field is **not** proof of impossibility over the complex numbers. A credible negative certificate needs a rigorous characteristic-zero polynomial identity/ideal infeasibility certificate (including singular/exceptional cases) or another all-$N$ theorem. A positive construction must work for an unbounded family of $N$ and charge all coefficients and applications.

## Gate 7 — sparse surrogate word-RAM approximation has a sharply different accuracy contract

The signed-atom scheme draws $k=O(\epsilon^{-2}\log(N/\delta))$ samples and targets

$$\|U_Ny-U_Nx\|_\infty\le \epsilon\,L_\Box(x)/\sqrt N,$$

not exact Fourier output or high-fidelity relative $\ell_2$ error. For a flat real vector $x_j\in\{-1,1\}$, let $J_1,\ldots,J_k$ be iid uniform indices and $y=(N/k)\sum_\ell x_{J_\ell}e_{J_\ell}$. Then

$$\begin{aligned}
\mathbb E\|U_Ny-U_Nx\|_2^2
&=\mathbb E\|y-x\|_2^2\\
&=\frac{N^2-N}{k},\\
\frac{\mathbb E\|U_Ny-U_Nx\|_2^2}{\|x\|_2^2}
&=\boxed{\frac{N-1}{k}}.
\end{aligned}$$

This is an **exact** full-vector mean-square identity for this importance-sampling surrogate. With $k=\Theta(\log N)$ the relative $\ell_2$ error is large; obtaining expected relative squared error $\le\epsilon^2$ requires $k\ge (N-1)/\epsilon^2$ for this scheme. This does not refute the source's weaker all-output $\ell_\infty$ tolerance. Its proposed packed-table $O(N)$ complexity additionally needs a rigorous word-RAM input/precision contract and packed-lane proof.

## Gate 8 — legitimate scoped positives are not exact arbitrary-input FFTs

- Hero #17 `fft_hero17_tensor_fiber_graph_union_2026-10-10.zip`: exact $O_r(N)$ on *recognized bounded-character-per-fiber* and other restricted families (including some dense, full-rank reshaped matrices). Generic random vectors fail the recognizable family.
- Hero #0 `fft_divisor_spectrum_v13.zip`: randomized $O(N)$ one-row work for balanced composite length families, with provable additive pointwise covariance and an all-bin median bound using a fixed number of rows. Not an exact transform or coefficientwise relative-accuracy FFT.
- Hero #1 v13: $O(N)$ one-row randomized sketches at favorable lengths, but $\mathbb E\|\widehat U_Nx-U_Nx\|_2^2=(M-1)\|x\|_2^2$ for a single state. Not a high-accuracy full-vector FFT.
- Quantum Fourier circuits transform quantum amplitudes, not a freely readable list of $N$ exact arbitrary classical complex outputs. Input loading and readout must be charged.

## Corrected ranking

| Priority | Surviving theoretical target | Known blocker | Decisive next certificate |
|---|---|---|---|
| 1 | Two or more **diagonal-gauged non-affine Green summands** | Ungauged sums have constant diagonal; pure products have sparse inverses | Solve/test $A U F_N V B=A+B$ with invertible diagonal $U,V$, then lift to all $N$ |
| 2 | Products of genuinely global **dense-inverse separated-generator scans** with non-affine mixing | One scan has small Fourier cross-block rank; N8 graph cuts can be vacuous while polynomial identities remain | Fourier-specific algebraic compatibility plus scalable operator recurrence |
| 3 | Pre-materialization cross-bank/chirp joint evaluation | Orthogonal bank rank and Chebyshev-Vandermonde channel-state barriers | Explicit fused straight-line program with $o(N\log N)$ fully charged work |
| 4 | Non-affine/high-state graph union, tensor-fiber fusion | Generic input destroys bounded fiber spectral support | Prove a nontrivial shared-state compression on every input, not an adapted recognizer |
| Separate | Randomized approximate all-output transforms | Different error metric; finite precision | Fully charged proof in its stated approximation model, no exact-FFT claim |

## Independent finite-field sanity checks

Run `python fft_theoretical_gate_2026-10-10.py` (included separately). It uses the prime field $\mathbb F_{97}$, $N=16$ and a primitive 16th root. Outputs:

```
green_product_inv_row_support after stage 1 max 2 bound 2
green_product_inv_row_support after stage 2 max 4 bound 4
green_product_inv_row_support after stage 3 max 8 bound 8
random_two_Green_sum_Weyl_discrepant_entries 255 of 256
ungauged_two_Green_sum_diagonal_distinct_values 1
Fourier_diagonal_distinct_values 4
phase_banks 1 combined_rank 4 upper_bound 4
phase_banks 2 combined_rank 8 upper_bound 8
phase_banks 3 combined_rank 12 upper_bound 12
phase_banks 4 combined_rank 16 upper_bound 16
single_dense_scan_balanced_cut_rank 1
Fourier_same_cut_rank 8
```

These tests corroborate the proofs, but finite checks do not establish all-$N$ impossibility or feasibility. In particular the **random** two-Green sum is only a negative *example*, not a no-go theorem for all tuned sums.

## Final mathematical status

**No proof of $O(N)$ for exact arbitrary-input DFT.** The simple product-of-Green-inverses idea is rigorously blocked at constant depth, every ungauged cyclic Green sum is excluded by its constant diagonal, affine-run bounded-term sums are rigorously blocked, direct incomplete phase-bank fusion is rigorously rank-deficient, and sparse-surrogate high-fidelity full-vector recovery needs $\Omega(N)$ samples within that specific unbiased sampling architecture. The strongest unexcluded direction is an **explicit all-$N$ non-affine branched/dense-inverse operator factorization certified by Fourier covariance**. This is a concrete open search, not a discovered breakthrough.

### Research sources inspected

- `fft_green_research_phase26_2026-10-10.zip`, `THEOREM.md` and `CHECKPOINT.md`
- `fft_sparse_defect_green_gate_2026-10-10.zip`, `RESEARCH.md`
- `fft_hero1_mixedradix_v13_20261010.zip`, `THEOREM.md` and `NEXT_GATE.md`
- `fft_hero17_tensor_fiber_graph_union_2026-10-10.zip`, `RESEARCH.md`
- `fft_divisor_spectrum_v13.zip`, `RESEARCH.md`
- `SPARSE_SURROGATE_WORDRAM_CHECKPOINT_2026-10-09_v2.md`
- `FFT_NONLINEAR_SESSION_HANDOFF_2026-10-09.md`
- `FFT_RESEARCH_CANONICAL_CHECKPOINT_2026-10-09.md`

### Model/prior art comparisons

- OpenAI Math #130, `https://github.com/openai/math/blob/main/lean/docs/130.md`: an all-length $O(N(\log N)^{1-10^{-13}})$ **exact** result is reported in a permissive complex-register model; this does not settle linear time, bit complexity or numerical stability.
- Morgenstern (1973), DOI `10.1145/321752.321761`: bounded-coefficient linear-circuit lower bounds do not automatically apply to unrestricted-coefficient arithmetic.
