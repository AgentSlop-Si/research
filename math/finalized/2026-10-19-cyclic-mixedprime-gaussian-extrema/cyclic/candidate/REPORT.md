# Cyclic phase minimax: an exact infinite family

## Result

For every m>=1, the normalized cyclic Fourier matrix of order N=4m satisfies

**delta_(4m,m-1)=sin(pi/(8m)).**

The model permits an unrestricted real scalar core, complex correction of rank at most m-1, arbitrary invertible complex monomial outer gauges, and measures the external operator norm. The least rank allowing zero error is exactly m.

This is an attaining infinite family, including every dyadic N>=4. It specializes to C4 rank zero, C8 rank one, C12 rank two, C16 rank three, and so on.

## Why it works

The C8 commutator obstruction extends uniformly. If the phase objective is too small at correction rank r, a low-rank unitary replacement forces N-4r eigenvalues of the commutator into a short open arc. The commutator is a weighted two-step shift, with gcd(N,2) cycles. For even N the two equally spaced cycles give

delta_(N,r)>=sin(pi(N-4r-2)/(4N))

whenever N-4r-2>0.

At r=N/4-1, explicit parity-dependent phases produce four invariant m-dimensional spaces. On each, the relevant unitary is a scalar phase times a weighted involution. The four involution traces sum to 4. Hence the imaginary part has exactly N/2+2 singular values sin(pi/(2N)) and N/2-2 singular values cos(pi/(2N)). The latter directions fit exactly into complex correction rank N/4-1.

The proof includes deterministic construction of the correction and real core. Arbitrary monomial magnitudes are absorbed before forming the residual; no conditioning assumption is introduced.

## Verification

The fresh exact checker passed N=4,8,12,16,20,24,28,32 using rational arithmetic in cyclotomic quotient fields. It verifies full Fourier/phase Gram identities, the singular-value polynomial, spectral projector rank, exact residual norm identity, all four involution traces, the explicit sparse Fourier block formula, and endpoint multiplicities. Five destructive controls include omission of the odd-m sign, omission of the global phase, transpose/adjoint confusion, and both closed-arc mistakes.

The proof is uniform in m and over the entire phase torus. The finite checks support the algebra; they do not establish the infinite family by sampling.

## Limits

For smaller ranks r<N/4-1, only the displayed lower bound is proved here; a precise matching-attainment question is recorded in Section 9. No full rank/error tradeoff, arbitrary finite-group theorem, jointly real Green construction, FFT operation-count conclusion, minimizer classification, or historical novelty is claimed.

Status: candidate theorem and exact check packet complete; independent review not yet performed on these bytes.
