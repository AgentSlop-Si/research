# Prior-art / novelty boundary for v33

The following foundations are classical or externally known. Do not claim any of them as this research project's discovery.

- **Jacques Morgenstern (1973)**, *Note on a Lower Bound on the Linear Complexity of the Fast Fourier Transform*, J. ACM 20(2), 305–306, DOI https://doi.org/10.1145/321752.321761. Its bounded-coefficient determinant method gives `Omega(N log N)` for the **unnormalized** DFT with bounded coefficients. The v33 charge-per-edge extension to arbitrary fan-in is an immediate elementary consequence of the same determinant-potential argument; no priority claim.
- **Lindström–Gessel–Viennot** path-minor determinant lemma. Disjoint paths give nonzero path-minor polynomials with algebraically independent edge weights.
- **Radhakrishnan–Ta-Shma** depth-two superconcentrator lower bound; **Alon–Pudlák** depth-three `Theta(N log log N)` bounds; **Pippenger** linear-size growing-depth superconcentrators. v31 cited these accurately.
- **OpenAI Math result #130**, *An explicit power saving for the exact discrete Fourier transform*, September 25, 2026, https://github.com/openai/math/blob/main/lean/docs/130.md , reports a uniform exact-register all-length `O(N(log N)^(1-10^-13))` bound with a supplied specified root; it is not a standard bit-complexity or float result. We have not independently rebuilt the Lean formalization.
- Project v32 positive root-of-unity cyclotomic count was correct in scope, but Morgenstern already excludes sub-`N log N` in a larger bounded-modulus class and removes a misleading apparent positive-root loophole.

## Exactly new *within this saved project*

1. A concrete fixed 11×11×11×11, 99-edge 3-layer support; all **705431** equal-cardinality terminal routing tests exhaustively pass.
2. One explicit GF(1000000123) 99-weight assignment with **every one of 705431 nonempty square minors nonzero**, checked by compiled independent modular Gaussian elimination.
3. The 99-parameter project's projective crossratio map has exactly **56** generic characteristic-zero dimensions (43-dimensional connected vertex-gauge action plus explicit 56×56 Jacobian residue 915710031).
4. The 101 basis functions `{1, all 100 crossratios}` are linearly independent in characteristic zero, witnessed by a 101×101 modular evaluation determinant of 763214669; hence every relation within the 44-dimensional elimination ideal has degree at least 2.
5. The exact phase conditions for this topology are 100 degree-at-most-6 polynomial equations; this chosen assignment satisfies none of them for the Fourier 11th-root target.
6. Nonuniform coefficient-scaling controls and exact radial butterfly controls integrated with a fully charged arithmetic ledger.

**Not established:** existence of Fourier weights on the 99-edge support; impossibility for all weights; an all-length `o(N log N)` algorithm; a new unrestricted lower bound; peer-reviewed originality of the topology/dimension facts; a practical speedup or bit-complexity statement.
