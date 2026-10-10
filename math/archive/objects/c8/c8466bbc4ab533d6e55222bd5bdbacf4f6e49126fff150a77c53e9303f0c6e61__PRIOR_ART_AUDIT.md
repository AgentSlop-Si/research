# Prior-art boundary — v27

Classical background includes:

- finite Heisenberg/Weyl groups;
- the finite Stone-von Neumann uniqueness phenomenon;
- the Schrödinger representation;
- construction of the Weil representation from automorphisms of the Heisenberg group;
- Fourier character tables of finite abelian groups;
- direct-product/tensor factorization of abelian Fourier transforms.

A relevant primary source is Gurevich and Hadani, *Quantization of symplectic vector spaces over finite fields* (arXiv:0705.4556), which develops a canonical finite-field Weil representation and a strengthened Stone-von Neumann property.

The project-specific result is not the existence of the Stone-von Neumann theorem. It is the FFT-facing computational gate:

1. exact finite Weyl pairs have an explicit `N x multiplicity` normal form;
2. every Fourier-swap solution is `F_N tensor U`;
3. covariant injection/extraction collapses to `scalar*F_N`;
4. exact character-table submatrices split into a direct cyclic factor plus mutually orthogonal spectators;
5. the theorem is tied to exact exhaustive certificates and a charged embedding ledger.

This package does not claim literature-wide novelty or priority. A full novelty review would need broader searches in finite Heisenberg representation theory, complex Hadamard submatrices and covariant coding/embedding literature.
