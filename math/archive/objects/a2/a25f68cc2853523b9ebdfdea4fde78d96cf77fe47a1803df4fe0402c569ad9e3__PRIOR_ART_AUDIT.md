# Prior-art audit — v11 fusion

This checkpoint uses established components and does not claim their invention.

1. **Bessel generating function / Jacobi--Anger expansion.** NIST DLMF §10.12 gives the generating function and associated Jacobi--Anger series.
2. **Bessel addition theorem.** NIST DLMF §10.23 records Neumann's addition theorem. For integer-order `J_n`, the identity used in the code also follows directly by multiplying two Bessel generating functions and comparing Laurent coefficients.
3. **Clenshaw recurrence.** C. W. Clenshaw, “A note on the summation of Chebyshev series,” Mathematics of Computation 9 (1955), 118--120, DOI `10.1090/S0025-5718-1955-0071856-0`.
4. **Low-rank NUFFT correction.** D. Ruiz-Antolín and A. Townsend, “A Nonuniform Fast Fourier Transform Based on Low Rank Approximation,” SIAM J. Sci. Comput. 40(1), 2018, DOI `10.1137/17M1134822`.

The specific project claim being tested is the composition:

- split `pi(bM+t)/Q` by the Bessel addition theorem inside the random chirp block summary;
- keep a constant number of local Bessel channels;
- synthesize the rank channels only after compression;
- decode selected dyadic frequencies and combine them by streamed Clenshaw;
- preserve the v10 deterministic and covariance bounds with an explicit additional tail `kappa_RH`.

A limited search did not locate this exact composition. That is not a proof of novelty.
