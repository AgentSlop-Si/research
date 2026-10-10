# Classical ingredients and verification scope

The following public primary documentation was checked on 9 October 2026. It supports attribution of the classical ingredients, not novelty of a project-specific composition or verification of an uploaded implementation.

- NIST DLMF, [Neumann's Bessel addition theorem, equation 10.23.2](https://dlmf.nist.gov/10.23.E2). The displayed addition formula applies without the usual argument restriction when the cylinder function is J and its order is an integer. This is the identity used by v11's block/local separation.
- NIST DLMF, [Chebyshev-series summation and Clenshaw's algorithm](https://dlmf.nist.gov/3.11.ii), including equation 3.11.15. This supplies the classical backward recurrence underlying the two-accumulator implementation. The convention for the constant Chebyshev coefficient must be respected when comparing formulas.
- AMD's rocFFT [Bluestein design document](https://rocm.docs.amd.com/projects/rocFFT/en/docs-6.3.0/design/bluestein.html). It presents the quadratic-phase identity reducing the DFT to chirp-weighted convolution. Phase21's Weyl polynomial is an algebraic expression of this classical family, not a newly discovered DFT identity.

No public source listed here is used to infer that a restricted representation bound is an unrestricted arithmetic lower bound, or that a finite modular certificate proves a universal-in-length claim. The independent reports provide the specific derivations and checked scopes.
