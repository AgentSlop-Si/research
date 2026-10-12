# Reviewed two-call Fourier recovery schedule

12 October 2026 UTC.

[Independent derivation, prior-result comparison and complete cost review](q11-two-call-fourier-recovery.md).

For the original q=483^m, m>=1, N=5q² positive-chirp target B=(F^-1+A)^-1 over the exact ambient field Q(omega), the reviewed identity is

    F=(1+c) B A B+(1−2c) B+c A^-1,
    A_ii=omega^(hi²), h=(N+1)/2, c=N sum_i A_ii.

Two sequential calls to the same prepared exact full-B evaluator, with exactly 4N extra scalar multiplications and 2N additions, recover all Fourier outputs. The oracle must accept every exact input in the full ambient field, including the actual second-call input. Setup, preserved copies, routing, allocations and output are separately paid. Standalone extra power/diagonal preparation costs 2N−1 multiplications plus scalar synthesis, root checks and O(N) word/storage work.

The existing research already had a three-B reverse identity and constant-factor exact-field cost equivalence. This result shortens that schedule to two calls; it does not discover equivalence for the first time. The already known converse evaluates B using two forward-F calls, 3N multiplications and 2N additions under its tighter schedule. A literal F/Fbar alternative costs 4N multiplications instead. Nonuniform oracle advice transfers only as nonuniform advice.

The current shared-bank evaluator plugged into this recovery remains O(N log N). At m=1 its literal counts are 184,298,160 multiplications and 165,635,040 additions, versus 82,817,595 and 74,652,480 for the stated direct-DFT schedule. These are algebraic counts, not timings, and establish no FFT exponent or practical speed improvement.

Independent symbolic checks derive the identity from T³=cI and contract the old three-call expression. Newly written finite-field controls include all 1,166,445 outputs at the smallest true family member, both actual oracle inputs against the defining inverse, exact overhead instrumentation, singular/imprimitive refusals and corrupted controls. The sealed reviewer cold replay passes. The finite test oracle itself is implemented with Fourier transforms; no cheap new B oracle is claimed, and author/historical programs remain inert during review.

The growing field and second-call coefficient heights must be charged in a bit model. The stated elementary relative-error bound can grow as O(N*epsilon); no stability equivalence is established. Products B A B do not preserve the additive Green grammar or branch counts. The existing Model R interval, coloring costs and expanded-output limits remain unchanged. Broader Q11, all-length/negative-family extensions, minimality among arbitrary architectures, bit/physical performance and historical priority remain open.

Earlier: [whole-output and shared-bank reviews](../2026-10-12-whole-output-shared-banks/README.md). Prior scientific reports and repository visibility/licensing remain unchanged.
