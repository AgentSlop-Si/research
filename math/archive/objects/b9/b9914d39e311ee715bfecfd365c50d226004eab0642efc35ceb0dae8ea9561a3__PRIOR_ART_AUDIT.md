# Prior-art and claim audit — v24

## Classical ingredients

1. **Finite Weil representation on `F_p^n`.** The DFT on functions on `F_p^n` is a distinguished operator in the Weil representation of `Sp(2n,F_p)`. See Ronny Hadani's research statement and standard finite-Weil expositions.
2. **Siegel-parabolic double cosets.** The double cosets of the Siegel parabolic are indexed by the rank of an off-diagonal symplectic block. The audit uses the opposite-parabolic version, so the source's `rank(C)` statement becomes `rank(B)` here.
3. **Partial Fourier normal forms.** The Weyl representative of rank `r` swaps `r` Lagrangian coordinates, giving a partial `r`-coordinate tensor Fourier transform.
4. **Monomial-equivalence invariants.** Cross ratios of four entries are invariant under row/column permutations and nonzero diagonal scalings; this is the elementary form of the Haagerup invariant used for complex Hadamard matrices.
5. **Tensor/radix Fourier factorization.** `F_p^{tensor n}` factors into `n` coordinate `p`-point DFT stages.

## Project-specific deductions in this checkpoint

- exact support count `p^rank(B)` for every row and column of a finite-field Weil operator;
- additive rank budget for a product of metaplectic stages;
- exact root-order cross-ratio obstruction separating cyclic `F_(p^n)` from every higher-dimensional field-Weil operator;
- exact reduction of every nondegenerate bilinear/additive extension-field Fourier kernel to tensor Fourier by a linear column relabeling;
- executable finite-field certificates and a fully explicit partial-core operation ledger.

## Sources consulted

- Ronny Hadani, *Research Statement* (2014), section on the Weil representation and DFT on `F_p^n`.
- Nir Elber and Hahn Lheem, *Intertwining operators for Siegel parabolics over finite fields* (notes, 2025), Lemma 2.2.3 on parabolic double cosets indexed by block rank.
- Tim Tzaneteas, *Weil Representations of Finite Fields* (2005 notes).
- Wojciech Tadej and Karol Zyczkowski, *A concise guide to complex Hadamard matrices* (2006), for standard monomial equivalence and related invariants.

## Claim boundary

This bundle does not establish:

- an exact faster cyclic FFT;
- a lower bound for unrestricted arithmetic circuits;
- a fully charged `O(N)` implementation of an arbitrary supplied symplectic operator;
- a fixed-precision theorem;
- literature-wide novelty.

The structural and finite-field certificates are reproducible, but independent mathematical review is still required before any external novelty claim.
