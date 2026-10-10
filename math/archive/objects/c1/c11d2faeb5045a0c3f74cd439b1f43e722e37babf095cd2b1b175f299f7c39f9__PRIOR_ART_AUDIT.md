# Prior-art boundary — v20

This is a limited audit, not a novelty search sufficient for a priority claim.

## Classical ingredients

1. Finite shift and modulation operators, the generalized Pauli group, and Weyl–Heisenberg projective commutation are standard. Relevant background:
   - Erik Hostens, Jeroen Dehaene, Bart De Moor, *Stabilizer states and Clifford operations for systems of arbitrary dimensions, and modular arithmetic*, arXiv:quant-ph/0408190.
2. Krylov subspace methods for sparse linear systems are classical. Relevant background:
   - Yousef Saad, *Iterative Methods for Sparse Linear Systems*, second edition, SIAM, 2003.
3. Roots-of-unity filters and finite geometric resolvent expansions are elementary algebraic tools.

## Project-specific deductions checked here

- the exact operator-index character formula for the Green resolvents `(I-alpha X^h Z^r)^(-1)`;
- the resulting `N-1` / `2N-1` sparse support count;
- the quadratic coordinate `u_h(t)=t(t-h)/(2h)` for the complete weighted orbit;
- the reflected zero-minor obstruction against affine Fourier endpoints;
- the explicit graph-distance lower bound as applied to a dense Fourier-like inverse in an exact Krylov schedule.

The limited search did not identify this exact compound result. No absolute novelty or peer-review status is claimed.
