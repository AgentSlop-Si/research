# Chain checkpoint — local-ring Weil valuation hierarchy v25, sign-corrected derivative

Correction dated 16 October 2026. Original archive and historical outputs remain preserved separately. The verification list below is an original-source report, not fresh execution acceptance.

## Inherited state

- v21: multi-shift Weyl–Green span contains Fourier but collapses to Bluestein.
- v22: two Weyl lines either fail or expose a Fourier-equivalent factor.
- v23: one-dimensional field metaplectic words are monomial or full-DFT-equivalent.
- v24: higher-dimensional field Weil operators are partial tensor DFTs; cyclic `F_(p^k)` is excluded.
- Exact arbitrary-input cyclic sub-`N log N` FFT remains open.

## New local-ring hierarchy

Let `R=Z/p^k Z`, `p` odd, and let `v=v_p(b)` for the upper-right entry of a symplectic matrix.

For the upper shear `U(b)`, the kernel

`F^(-1) C_(-b) F`

vanishes unless row and column indices agree modulo `p^v`. On each residue class it is diagonally/permutationally equivalent to the cyclic Fourier matrix of length `p^(k-v)`.

Therefore a valuation-`v` ring-Weil operator is computationally equivalent to

`p^v copies of F_(p^(k-v))`.

Every row/column has exactly `p^(k-v)` nonzeros, and a nonzero block has a cross ratio of exact order `p^(k-v)`.

## General element

- `v=0`: the upper-right entry is a unit, and ordinary ring Bruhat factorization makes the stage full `F_(p^k)`-equivalent.
- `1<=v<k`: the stage is monomial times the partial cyclic core above.
- `v=k`: monomial only.

The true lower-parabolic double-coset space may refine the valuation. At `Z/9Z`, valuation one splits into two double cosets, but both have the same three-copy `F_3` computational core.

## All-depth gate

For each `t>=1`, matrices whose upper-right entry is divisible by `p^t` form a subgroup:

`b(ST)=a(S)b(T)+b(S)d(T)`.

The Fourier Weyl element has unit upper-right entry. Hence any ring-metaplectic word equal to it must contain a valuation-zero factor, which is already full-DFT-equivalent.

Proper partial cells cannot assemble the full cyclic Fourier transform inside this one-dimensional representation.

## Cost

A valuation-`v` core costs

`Theta_p(p^k (k-v))`

under the standard radix-`p` implementation, with explicit dense-butterfly term count

`(k-v) p^(k+1)`.

The `v=k-1` cell is one radix-`p`-looking layer, but ring-Weil monomial factors preserve p-adic congruence classes; standard digit-transpose permutations leave this stage class.

## Historical verification report (not rerun)

- 10 automated test groups pass.
- 13 exact support/root-order certificates at dimensions 9, 25, 27, 49.
- Exhaustive `SL2(Z/9Z)` and `SL2(Z/25Z)` counts.
- Exhaustive subgroup closure over `Z/9Z`.
- Independent verifier passes.
- Clean v24 ZIP predecessor hash is checked.

## Do not repeat

- claiming valuation alone indexes every group double coset;
- treating the partial cyclic hierarchy as a new FFT exponent without the subgroup gate;
- claiming standard radix-p stages form a word in the one-dimensional ring-Weil group;
- another finite word of local-ring metaplectic factors as though depth removes the full Fourier-hard cell.

## Exact next target

Either:

1. higher-dimensional symplectic geometry over `Z/p^k Z` that genuinely exchanges p-adic digit layers and does not collapse to Cooley--Tukey; or
2. a non-Weil high-treewidth exact stage with a genuine non-Krylov sub-`N log N` solver.
