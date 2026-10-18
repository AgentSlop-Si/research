# Prior-art and claim boundary — v25

## Established background

The existence and representation theory of Weil representations for symplectic groups over finite local rings, including `R=Z/p^k Z` for odd `p`, is established work. A principal source is:

- G. Cliff, D. McNeilly, F. Szechtman, **Weil representations of symplectic groups over rings**, *Journal of the London Mathematical Society* 62 (2000), 423–436, DOI `10.1112/S0024610700001381`.

Quadratic Gauss sums over finite commutative rings and their degeneracies are also classical; see work of F. Szechtman in *Journal of Number Theory* 95 (2002).

The cyclic prime-power DFT and radix-`p` Cooley--Tukey factorization are classical.

## Scoped project result

v25 does not claim construction of the local-ring Weil representation. It derives and verifies the following computational consequences in the one-dimensional position model:

1. if `v=v_p(b)`, the upper-shear kernel has support exactly on pairs congruent modulo `p^v`;
2. each nonzero residue block is monomially equivalent to cyclic `F_(p^(k-v))`;
3. the block cross-ratio has exact root order `p^(k-v)`;
4. all nonunit-upper-right cells form a subgroup and cannot multiply to the full Fourier Weyl element;
5. the valuation computational class can be coarser than the true parabolic double-coset decomposition.

## Claims explicitly not made

- no exact sub-`N log N` FFT;
- no unrestricted arithmetic-circuit lower bound;
- no complete classification of every parabolic double coset over the local ring;
- no bit-complexity or fixed-precision theorem;
- no practical speed comparison against FFTW, pocketfft, MKL, cuFFT, or NTT libraries;
- no literature-wide novelty or priority claim.
