# Chain checkpoint — tensor Weil rank hierarchy v24

## Inherited state

- v21: the complete multi-shift Weyl–Green span contains Fourier but collapses to Bluestein.
- v22: two Weyl lines either fail or expose a Fourier-equivalent factor.
- v23: every finite one-dimensional metaplectic word is monomial or one full DFT core.
- Exact arbitrary-input cyclic sub-`N log N` FFT remains open.

## New higher-dimensional theorem

For `S=[[A,B],[C,D]] in Sp(2n,F_p)`, let `r=rank(B)`.

Siegel-parabolic double-coset normal form gives

`S = P1 * w_r * P2`,

where the `P_i` are lower-parabolic and `w_r` swaps exactly `r` position/momentum coordinates.

In the Weil representation:

`rho(S) = monomial * (F_p^{tensor r} tensor I) * monomial`.

Therefore every row and column has exactly `p^r` nonzeros.

## Rank budget

For products,

`rank B(ST) <= rank B(S)+rank B(T)`.

Reaching the full tensor Fourier element requires total stage rank at least `n`. The coordinate-rank-one factorization attains equality and is exactly the ordinary radix-`p` tensor FFT. This is a structural budget, not an unrestricted circuit lower bound.

## Cyclic prime-power obstruction

A dense tensor-Weil operator has only `p`th-root cross ratios. The cyclic Fourier matrix of length `p^n` has the witness cross ratio `zeta_(p^n)` of order `p^n`.

Hence for `n>1`:

`cyclic F_(p^n)` is not monomially equivalent to any `Sp(2n,F_p)` Weil operator.

Rank-deficient Weil operators already have zeros, so no other rank can work.

## Extension-field trap

The additive DFT on `F_(p^n)` uses `psi(Tr(xy))`. In coordinates it is `omega_p^(x^T M y)` for invertible `M`, hence a column permutation of `F_p^{tensor n}`. It is not the cyclic length-`p^n` DFT.

## Verification

- 10 automated test groups pass.
- Exhaustive `Sp(4,3)` generation: 51,840 elements.
- Rank-B distribution: 1,296 / 15,552 / 34,992 for ranks 0 / 1 / 2.
- Exact random-word support law at dimensions 9, 27 and 25.
- Cyclic cross-ratio witnesses have orders 9, 27 and 25; tensor/Weil ratios are p-torsion.
- Independent verifier reproduces the group distribution and root-order gate.

## Do not repeat

- treating the additive DFT on `F_(p^n)` as the cyclic DFT on `Z/(p^n)`;
- claiming a higher-dimensional field Weil operator embeds cyclic prime-power Fourier;
- treating partial-rank stages as a new exponent without charging the rank budget and stage preparation;
- claiming the standard tensor factorization is beyond Cooley--Tukey/radix-p.

## Exact next target

Move to the Weil representation over the finite local ring `Z/(p^k)`, where `p^k`th phases are native. Classify cells by p-adic off-diagonal valuation and determine whether their partial cyclic transforms can be jointly evaluated below the ordinary radix-p ledger.
