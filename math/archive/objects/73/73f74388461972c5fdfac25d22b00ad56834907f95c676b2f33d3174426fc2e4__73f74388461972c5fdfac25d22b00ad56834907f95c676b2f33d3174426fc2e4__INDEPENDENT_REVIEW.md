# Independent exact review: finite F8 factorization exists

9 October 2026 UTC. The complete constructor certificate and a separately authored verifier prove a finite positive result:

F8/sqrt(8)=S3 P S2 P S1,

where P=[0,4,2,6,1,5,3,7] is bit reversal and each stage has independent lower separated generators, upper separated generators and a diagonal. The Fourier sign is positive. The factors exist with the specified 56 frozen Gaussian-rational parameters and the remaining 64 complex parameters in the certified rational ball.

This is genuine exact local existence for the particular Fourier target, stronger than a floating fit or generic dimension-count statement. It does not establish an all-length family, a closed-form coefficient list, uniform parameter synthesis, a new asymptotic evaluator or numerical stability of a growing family.

## What was independently checked

The inert data file gives 120 Gaussian-rational center parameters with denominator 2^60, the 64 selected parameter indices, and a Gaussian-rational 64-by-64 approximate inverse with denominator 2^44. The reviewer reconstructs the three dense eight-by-eight stage matrices and their repeated-bit-reversal product independently.

Instead of reusing the constructor's analytic Jacobian formula, the reviewer obtains each derivative column from an exact unit finite difference: evaluate at the center and with that one selected complex parameter increased by one. Each path monomial uses any parameter at most once, because the three stages have disjoint parameter lists and each stage entry is either one diagonal parameter or a product of two distinct generator parameters. Thus the unit difference equals the exact partial derivative, not an approximation. This independently verifies parameter indexing, permutation orientation, output flattening and all selected columns.

The target is evaluated with an integer square-root enclosure for sqrt(2) of width 2^-120. Entries of normalized F8 are signed 1/4 or signed sqrt(2)/4 in their real and imaginary components. All asserted inequalities use integers and rational numbers. Floating numbers in the saved JSON are display-only conversions after the exact checks pass.

## Norm and polynomial bounds

Use the real Banach-space norm on C^64 given by the maximum over coordinates of |Re z|+|Im z|. Although this is not the rotationally invariant complex absolute value, it is a valid real norm and complex multiplication is submultiplicative for it. Gaussian-rational row sums therefore give valid operator bounds. The fixed-point proof is on the complete real normed space underlying C^64.

Each product entry is the sum of 8² path monomials, each of degree at most six. On the radius-at-most-one neighborhood used here, every parameter, including frozen parameters, has scalar norm at most M=4. Summing ordered second derivatives bounds the vector infinity-operator Hessian norm by

30*8²*M⁴=491,520.

Restricting to the selected variables cannot increase this bound. Lower-degree monomials also obey it because M>=1.

The independent rational calculations give the following conservative displayed bounds:

- residual norm at the center: 1.029524e−15
- approximate-inverse norm: 60.848987
- eta=||I−B J(center)||: 5.772635e−12
- beta=||B|| times residual bound: 6.264549e−14
- derivative Lipschitz bound L: 29,908,493.804
- ball radius r=2^−30: 9.313225746e−10
- contraction bound eta+Lr: 0.027854456<1
- self-map bound beta+eta*r+(L/2)r²: 1.303339e−11<r

The exact rational numerators and denominators are retained in INDEPENDENT_CERTIFICATE_RESULTS.json; the proof does not rely on these rounded displays.

## Why these inequalities prove exact equality

Let f be the 64 complex Fourier-entry residuals with 56 parameters frozen, and define G(z)=z−B f(z). The self-map inequality puts G's entire closed radius-r ball inside itself. The derivative bound makes G a contraction there. Banach's theorem gives a unique fixed point in this ball.

Because eta<1, B J(center) is invertible by the Neumann argument. Both are square, so B is invertible. Consequently a fixed point of G has f(z)=0. This proves exact equality to normalized F8. The equality to an invertible Fourier matrix automatically forces every square stage factor to be invertible; no unproved principal-pivot assumption is used.

## Coefficient and computational scope

The certificate specifies coefficients as the unique local root of an explicit polynomial system with algebraic Fourier target coefficients. It does not identify closed-form coefficients or a uniform family over N. Applying stages with their exact coefficients supplied is separate from preparing or representing those coefficients. A finite N=8 existence result cannot defeat the verified asymptotic three-stage obstruction, and it is compatible with the explicit larger-size bit-reversal exclusions.

The constructor's proof/data/checker are preserved under constructor/. The independent checker consumes the separately retained byte-identical data copy and imports no constructor or uploaded program. Mutable numerical search/build diagnostics are not required for the proof payload and are excluded. Relocated independent execution reproduces its result JSON exactly.
