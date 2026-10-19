# Independent review: ALG-019 evaluator retirement

19 October 2026 UTC. Verdict: **APPROVE retirement of the current complete decimation evaluator as asymptotically dominated in its declared exact-field arithmetic model.** Preserve the accepted sparse grading, orbit transport, finite-corner identities, recursion and falsification controls as supporting mathematics. This is not a claim that each identity appeared verbatim in earlier literature or that a future improved sharing rule is impossible.

## Exact comparator and model

The source evaluator handles arbitrary supplied polynomials p of degree below N, where N=2^L>=2, q is a supplied primitive Nth root, and the field has odd characteristic (or characteristic zero). Its claimed online arithmetic is Theta(N^(1+(log_2 3)/2)), with O(N log N) coefficient preparation and O(N) live storage. The comparison below handles exactly the same arbitrary p, C and input/output interface. It does not rely on H_q-specific polynomial coefficients.

Let A be the lower nilpotent shift, f_j=product_(a=1..j)(1−q^a), T=H_q(A), and let B be the upper weighted shift with B[i,i+1]=q−q^(−i). The retained [finite-boundary source](https://github.com/AgentSlop-Si/research/blob/29c18ecae33c2d0a39c338b886f49e2802ff7e88/math/archive/objects/e7/e7c06a4bc237a97c74aefc854ad6b7d22d44f7c7f858ec82789780935e857c35__e7c06a4bc237a97c__README.md) states the exact similarity

C=TBT^−1=B+diag(q^−i)−(q/N)e_(N−1)e_0^T.

It retains the real finite corner. T is lower triangular and B is upper triangular; their conjugation is not asserted to preserve upper triangularity.

Set w_0=1, w_j=product_(h=0..j−1)(q−q^−h), and D=diag(w_j). For j<N,

w_j=(−1)^j q^(−j(j−1)/2) f_j != 0.

The nonzero statement follows because q has exact order N. Comparing the single superdiagonal gives B=D^−1 A^T D. Therefore, for every p,

p(C)=T D^−1 p(A^T) D T^−1.

T and T^−1 are lower triangular Toeplitz; p(A^T) is upper triangular Toeplitz. Thus the complete application requires three triangular Toeplitz products, two diagonal passes and, if desired, reversal passes to handle the upper product. All are paid.

## Inverse and field validity

[Kuznetsov, Theorem 2(i), printed p.2](https://arxiv.org/pdf/1507.02959v2#page=2), gives an explicit diagonal/Toeplitz expression for T^−1. Equivalently its jth lower-diagonal coefficient is (−1)^j q^(j(j−1)/2)/f_j. The theorem is printed over the complex numbers. The coefficients in this finite identity are rational functions with integer coefficients and denominators consisting of powers of q and factors 1−q^j for j<N. Clearing those denominators yields a polynomial identity over the integers, so the identity specializes to any admitted exact field where they are nonzero. This extension is an explicit algebraic inference, not a claim that the paper states all finite-field cases.

Because N is a power of two and the characteristic is odd, N and 2 are invertible. No uncharged field extension, new root or floating-point approximation is introduced.

## No missing 2N-th root

A triangular Toeplitz product is multiplication of two degree-below-N polynomials modulo z^N, possibly after reversal. A conventional zero-padding argument must not silently assume a primitive 2N-th root. Instead put m=N/2, a=a_0+z^m a_1 and b=b_0+z^m b_1. Then

ab mod z^N = a_0b_0 + z^m(a_0b_1+a_1b_0) mod z^N.

Each half-product has degree at most N−2, so it is recovered exactly by length-N cyclic convolution using the already supplied root q. A constant number of radix-two forward/inverse transforms computes each product. Inverse transforms use the charged 1/N scaling. This works also at N=2, with constant-size cases; N=1 is outside the source's stated contract.

## Complete cost and disposition

Prepare root powers, factorials, reciprocal factorials, w_j and w_j^−1 in O(N) field work and O(N) storage, using charged inversions or one product inversion and backward products. Read the N supplied p coefficients and input coordinates. All transform twiddles, coefficient transforms, diagonal/reversal passes, copies, N outputs and word-index operations cost at most O(N log N) overall. Scratch can be reused sequentially, giving O(N) live field elements. The full cold one-shot cost, including preparation, is O(N log N). No bit-complexity, numerical-stability or hardware claim follows from this exact-field ledger.

This is a derived classical comparator assembled from the retained exact similarity, the explicit triangular inverse and radix-two convolution. Its O(N log N) bound is asymptotically better than the [recorded complete evaluator](https://github.com/AgentSlop-Si/research/blob/29c18ecae33c2d0a39c338b886f49e2802ff7e88/math/archive/objects/e8/e84fd241ddf5f362c09cb41cec13483b6f67c40703acfe6bec5f13e5e1ce6d46__e84fd241ddf5f362c09cb41cec13483b6f67c40703acfe6bec5f13e5e1ce6d46__README.md) for the same arbitrary-p problem. It is not a previously published verbatim theorem about this exact C. The source's absence of an FFT call is an implementation property, not a restriction in its declared scalar-arithmetic comparison model.

The sparse orbit relation HR=DH can be retained after a faster first H action and still gives its original paid O(N) related-input updates. Thus it is not a lost application that requires the slower decimator to remain active. Retire the current evaluator research track, preserve F096 as its source-family identifier, and do not count that identifier separately. A concrete stronger algorithm or a newly restricted cost model would require a new comparison; an unspecified wish to find sharing is not an accepted result.

No external record changed and no historical scientific program was rerun during this review.
