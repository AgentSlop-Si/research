# Prior-art boundary — v26

## Classical background

The following are established ingredients and are not claimed as new:

1. **Weil representations over finite rings.**  
   Gerald Cliff, David McNeilly and Fernando Szechtman, *Weil Representations of Symplectic Groups Over Rings*, Journal of the London Mathematical Society 62 (2000), 423–436, DOI `10.1112/S0024610700001381`.

2. **Weil representations for finite abelian groups.**  
   Frieder Ladisch, *The character of the Weil representation of a finite abelian group of odd order*, arXiv:`2303.09676`.

3. **Smith normal form and finite-module decompositions.**  
   Matrix reduction over principal ideal rings and the classification of finite abelian groups are classical.

4. **Fourier transforms on finite abelian groups.**  
   The character table of a direct product is the tensor product of the character tables of its cyclic factors.

5. **Heisenberg covariance and Bruhat factorization.**  
   These are standard structural tools in finite Weil representations.

## Project-specific claims in this checkpoint

The package combines the classical ingredients into the following computational gate:

- support of a ring-Weil kernel is bounded by `|im B|` using all modulation relations from `ker B`;
- invertible `B` gives an explicit additive-Fourier normal form;
- diagonal p-adic valuation profiles give exact tensor products of shorter cyclic Fourier cores;
- cross-ratio order separates the additive transform on `(Z/p^s)^n` from the cyclic transform of the same matrix dimension;
- the obstruction extends to every finite abelian p-group via its exponent;
- exact finite-field implementations and independent certificates are supplied.

A limited literature search did not establish whether this exact combined computational formulation has appeared previously. No priority claim is made.

## Scope

The results do not cover unrestricted arithmetic circuits, nonlinear algorithms, arbitrary invariant-subspace embeddings or non-Weil high-treewidth solvers. They do not establish a practical or bit-complexity FFT improvement.
