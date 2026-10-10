# Hero #1 — Phase 28: Nested 60-point Winograd tensor inside an all-input FFT

**Date:** 2026-10-10. **Scope:** exact algebraic identities, independently expanded finite-field circuits, fully charged additions and nonidentity scalar multiplications. **Not** an original Winograd factorization, a new `o(N log N)` theorem, or a floating-point/bit-complexity claim.

## 1. Model and exact correctness

Let `H=2^t`, `G=4H`, `N=15G=60H`, and let `F` be a field of characteristic different from 2 with an element `ω` of multiplicative order exactly `N`. Define the unnormalized transform

\[
(F_Nx)_k=\sum_{j=0}^{N-1}\omega^{jk}x_j.
\]

An addition/subtraction costs one field operation. Multiplication by a predetermined scalar different from `1` costs one field operation, even if that scalar is a fourth root of unity. Primitive root generation and coefficient preparation are charged in a separate cold-setup ledger. CRT permutations/index arithmetic, word traffic, allocation, and field bit-complexity are not silently treated as field additions: they are separately scoped and do not support a wall-clock speedup claim.

### Proposition 1: exact short-transform diagonalizations

For each `n=3,4,5` there are explicit integer-coefficient pre/post maps `B_n`, `A_n` and a diagonal matrix `D_n` such that

\[
F_n=A_nD_nB_n.
\]

`symbolic_check.py` verifies these identities **over characteristic-zero cyclotomic quotient rings**, not merely in sample finite fields:

- `F3`: `B3` has 3 additions, `A3` has 3 additions, `D3` has width 3 with 2 paid scalars. Its diagonal is `(1,-3/2,(ζ3-ζ3²)/2)`.
- `F4`: `B4` has 4 additions, `A4` has 4 additions, `D4=(1,1,1,ζ4)` with 1 paid scalar.
- `F5`: `B5` has 8 additions, `A5` has 9 additions, `D5` has width 6 with 5 paid scalars, using the explicitly computed symmetric/antisymmetric cyclotomic coefficients from `wfta15.py`.

The characteristic-zero check uses exact rational polynomial remainders modulo `Φ3`, `Φ4`, and `Φ5`. These are classical Winograd-type preweave/diagonal/postweave identities, **not claimed as new**.

### Proposition 2: the combined 60-point kernel

Because 3, 4, and 5 are pairwise coprime, the Good–Thomas CRT permutations identify `F60` with `F3⊗F4⊗F5`, with the short roots induced from the primitive 60th root. Tensoring Proposition 1 yields

\[
F_{60}=P_{\rm out}\,
(A_3\otimes A_4\otimes A_5)
(D_3\otimes D_4\otimes D_5)
(B_3\otimes B_4\otimes B_5)\,P_{\rm in}.
\]

There are `3×4×6=72` central scalar channels. Exactly 3 of the tensor diagonal coefficients equal `1` in characteristic zero, as **independently proved by 72 exact reductions modulo `Φ60`**; the two tested prime fields have the same unit count. Thus the central product requires **69 nonidentity field multiplications** in our model. In conventional real/imaginary arithmetic, multiplication by `±i` can be a data swap and sign change, so published WFTA real-multiplication tables are **not directly comparable** to these field counts.

The preweaves in the order `F3,F4,F5` cost `60+60+96=216` additions. The postweaves in the reverse order `F5,F4,F3` cost `108+60+60=228` additions. Therefore this **complete, explicitly expanded 60-point kernel** costs

\[
\boxed{444\text{ additions}+69\text{ multiplications}=513\text{ field operations}.}
\]

`kernel60` is directly implemented in `fused60.py`: no high-arity node is counted as one gate. Independent full-basis tests and exact cyclotomic codelet checks pass.

### Proposition 3: optimal pre/post ordering *within these fixed codelets*

Let factor `i` have physical dimension `n_i`, diagonal-intermediate width `r_i≥n_i`, `p_i` input-preweave additions, and `q_i` output-postweave additions. Write `δ_i=r_i−n_i`.

When two independent tensor preweaves `i,j` are swapped, their incremental costs (times identical positive widths of spectator factors) are respectively

\[
 p_i n_j+p_j r_i\quad\text{versus}\quad p_jn_i+p_i r_j.
\]

Therefore `i` before `j` is at least as good precisely when `δ_i/p_i ≤ δ_j/p_j`. Adjacent transpositions prove that sorting **preweaves** by increasing `δ_i/p_i` is optimal among their tensor permutations.

For postweaves the two costs are

\[
q_i r_j+q_j n_i\quad\text{versus}\quad q_jr_i+q_in_j.
\]

Thus sorting **postweaves** by decreasing `δ_i/q_i` minimizes total additions. The result concerns fixed tensor pre/post maps; it asserts neither shortest possible Fourier circuit nor historical priority for weave-order optimization.

In our case `(n_i,r_i,p_i,q_i)` is `(3,3,3,3)`, `(4,4,4,4)`, and `(5,6,8,9)`. The sorting rule puts `F5` last in the preweaves and first in the postweaves. The six-by-six exact enumeration in `weave_optimizer.py` confirms the minimum **444 additions**. Bad orderings can require 456–492 additions. The multiplicative savings would have been lost by an incorrect ordering.

## 2. Fusing the kernel with an arbitrary-dense length-`N` FFT

Let `G=4H`. Since `gcd(15,G)=1`, an outer Good–Thomas permutation removes all twiddles between the 15-point and `G`-point coordinates. However, inside `F_G` the `(4,H)` factors are **not coprime** for even `H`, so we retain and pay the Cooley–Tukey twiddle diagonal; we do not pretend to remove it.

The fully expanded algorithm is:

1. Permute the length-`N` inputs into a `15×4×H` array (CRT on `15,G`, ordinary `G=4H` split).
2. Compute 60 ordinary length-`H` dyadic FFTs, each costing `H log₂ H` additions and `(H/2)log₂H−H+1` scalar multiplications for `H≥1` (the expression also gives zero for `H=1`).
3. Pay all `15·3(H−1)=45(H−1)` nonidentity twiddle multiplications of the `(4,H)` stage.
4. For each of the `H` intermediate frequencies, apply one *full* 60-point fused tensor kernel from Proposition 2.
5. Scatter the final result to natural DFT order using the exact CRT output mapping.

The complete arithmetic ledger is

\[
\boxed{A_{28}(N)=60H\log_2H+444H},
\]
\[
\boxed{M_{28}(N)=30H\log_2H+54H+15},
\]
\[
\boxed{C_{28}(N)=90H\log_2H+498H+15.}
\]

The preceding Phase 27 implementation, using exactly the same outer CRT and dyadic root model, costs

\[
C_{27}(N)=90H\log_2H+544H+15.
\]

Hence **for every input** in the specified model,

\[
\boxed{C_{27}(N)-C_{28}(N)=46H=\frac{23}{30}N.}
\]

An intermediate Phase 28 approach using only the nested 15-point codelet costs

\[
C_{15\mathrm{nested}}(N)=90H\log_2H+512H+15.
\]

The additional 60-point fusion therefore saves `14H` operations over that already optimized circuit. All saved operations are scalar *multiplications*, not additions.

## 3. Cold setup, precision, and asymptotic ceiling

`make_plan` from Phase 27 produces the length-`G` root table and original 3-/5-point constants (with field arithmetic charged). The new 15-point diagonal requires **12 extra preparation operations** (10 multiplications and two additions), while the 60-point diagonal requires **17 further field multiplications**; the fourth-root coefficient is reused from the dyadic root table. The new execution therefore has a **29-operation cold-setup surcharge**, exactly as counted by the implementation.

Consequently, comparing the two particular one-shot plans with identical root-order assumptions:

\[
\boxed{C^{\rm cold}_{27}-C^{\rm cold}_{28}=46H-29>0.}
\]

Root-order verification, modular index inverses, memory traffic, workspace, floating-point rounding, and bit complexity are **not** included in this scalar-arithmetic equality. The execution has `O(N)` field-element storage plus fixed-size intermediate buffers; gathering/scattering incurs `O(N)` extra movement with non-negligible practical constants.

Since the leading term is still `90H log₂ H`, the new algorithm remains **`Θ(N log N)`**. The relative advantage decreases with growing `N`. This does not prove a new unrestricted faster-than-FFT exponent or exact `O(N)` complexity.

## 4. Noncoprime coupling persists

For even `H`, `F_{4H}` cannot become `F4⊗FH` using only row/column permutations and nonzero row/column scalings. Indeed, a cross-ratio invariant of `F_{4H}` contains an element of order `4H`, whereas any cross-ratio of the tensor has order dividing `lcm(4,H)<4H`. The `45(H−1)` internal twiddles in our chosen `(4,H)` realization are therefore honestly charged.

This is an obstruction to a **monomial-equivalence trick**, not to more general multiwire circuits. The architecture is a constant/lower-order saving, not a solution of this noncoprime coupling problem.

## 5. Evidence and prior art

- `test_phase28.py`: 10 new exact unit/regression tests pass; Phase 27's 7 tests also pass unchanged.
- `audit_phase28.py`: **2,455,200 distinct Fourier matrix entries** across two fields and lengths 60,120,240,480,960; for every entry, three distinct circuits are checked against the independent closed-form root power, totaling **7,365,600 exact equality comparisons**.
- `symbolic_check.py`: exact characteristic-zero proof of all short basis coefficients and exactly 3 identity diagonal coefficients among 72 central positions.
- `benchmark_phase28.py`: counted complete circuits through `N=61,440`, verifies the closed-form operation identities, independent direct-DFT checkpoints, and cold preparation counts.
- Perturbed diagonal-coefficient negative control is rejected by an independent reference.

The nested WFTA and CRT are established work: Winograd's 1976/1978 DFT papers; Burrus et al. treatments of Winograd Fourier transforms and prime-factor FFTs; and later split-nesting improvements. Published arithmetic tables for a length-60 WFTA exist. **This work does not claim to have invented its underlying factorization, nor that 513 is the global minimum count.** Our verified contribution is the precise model-aligned **scalar circuit fusion with Phase 27** and an explicit exchange-rule cost certificate.

References:
- https://pmc.ncbi.nlm.nih.gov/articles/PMC430186/
- https://eng.libretexts.org/Bookshelves/Electrical_Engineering/Signal_Processing_and_Modeling/Fast_Fourier_Transforms_%28Burrus%29/09%3A_The_Prime_Factor_and_Winograd_Fourier_Transform_Algorithms/9.03%3A_The_Winograd_Fourier_Transform_Algorithm
- https://opg.optica.org/ao/abstract.cfm?uri=ao-21-18-3273 (historical WFTA operation table; real-arithmetic counting differs)
