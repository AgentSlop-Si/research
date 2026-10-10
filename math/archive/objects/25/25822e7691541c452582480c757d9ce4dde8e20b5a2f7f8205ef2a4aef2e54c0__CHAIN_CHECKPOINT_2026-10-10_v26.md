# Chain checkpoint — higher-dimensional local-ring Weil exponent gate v26

## Inherited state

- v21: the multi-shift Weyl–Green span contains Fourier but collapses to Bluestein.
- v22: two Weyl lines either fail or expose a Fourier-equivalent factor.
- v23: one-dimensional field-metaplectic words are monomial or full-DFT-equivalent.
- v24: higher-dimensional field-Weil operators are partial tensor DFTs; cyclic prime-power Fourier is excluded.
- v25: one-dimensional local-ring Weil cells are partial cyclic FFTs, but proper cells form a subgroup that cannot reach the full Fourier element.
- Exact arbitrary-input cyclic sub-`N log N` FFT remains open.

## New dense/sparse theorem

For `R=Z/p^s Z`, `V=R^n`, and `S=[[A,B],[C,D]] in Sp(2n,R)`:

- if `B` is noninvertible, Heisenberg covariance forces every row of `rho(S)` to have support at most `|im B|<|V|`;
- if `B` is invertible,

  `S = L(DB^-1) G(-B) W L(B^-1 A)`,

  so `rho(S)` is monomially equivalent to the additive Fourier transform on `R^n`.

Thus a ring-Weil operator is dense exactly when `B` is invertible.

## Mixed-valuation hierarchy

For an upper shear with diagonal valuation profile `(v_1,...,v_n)`:

- number of blocks: `p^(sum v_i)`;
- row/column support: `p^(sum (s-v_i))`;
- each block core: tensor product of cyclic `F_(p^(s-v_i))`;
- maximum cross-ratio order: `p^(max(s-v_i))`.

At `R=Z/9Z`, `n=2`, all six profiles were checked exactly.

## Main cyclic obstruction

The additive Fourier transform on `R^n` has cross ratios of order dividing `p^s`.
The cyclic Fourier matrix of the same dimension `p^(sn)` has a primitive `p^(sn)` cross ratio.
For `n>1` these cannot be monomially equivalent.

Therefore no single higher-dimensional local-ring Weil operator—and no finite word of them—equals the cyclic DFT of dimension `p^(sn)`.

More generally, the character table of a finite abelian p-group can be monomially equivalent to the cyclic character table of the same order only if the group itself is cyclic.

## Rank budget

`r(S)=rank_Fp(B mod p)` satisfies

`r(ST) <= r(S)+r(T)`.

The full additive Fourier Weyl element has rank `n`, so any literal factorization has total rank budget at least `n`. Coordinate swaps attain the budget and reproduce the ordinary tensor/radix-p FFT ledger `Theta_p(Q log_p Q)`.

This is not an unrestricted arithmetic lower bound, and the additive transform is not the cyclic transform anyway.

## Verification

- 10 automated test groups pass.
- 60 exact random symplectic words: 0 failures.
- Exact mixed-valuation kernels at dimension 81.
- Exact dense Bruhat reconstruction at dimensions 9 and 81.
- Cyclic phase-order witnesses at dimensions 9, 25, 81, 625 and 729.
- Independent verifier passes.
- Complete v25 predecessor ZIP embedded and hash-checked.

## Do not repeat

- treating linear digit mixing in `(Z/p^s)^n` as an embedding of the cyclic group `Z/p^(sn)`;
- claiming the tensor/additive Fourier transform has cyclic phase depth;
- another finite higher-dimensional ring-Weil word as though depth leaves the group representation;
- treating the mixed-valuation hierarchy as a new FFT exponent without the cyclic exponent gate.

## Exact next target

Leave direct finite-ring Weil words. Try either:

1. a non-Weil high-treewidth exact stage with a genuine non-Krylov sub-`N log N` solver; or
2. a rigorously charged invariant-subspace embedding into a larger representation that preserves primitive cyclic phase order and does not hide a full FFT in extraction.
