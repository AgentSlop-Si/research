# Uniform extensions and a matched Fourier comparator

12 October 2026

This round extends previously accepted results in five specific directions. Acceptance means independent project review, not external peer review or a historical-priority determination. Original evidence archives remain the authoritative records.

## Prefix optimization for every prime above five

For G=D8×C5×Cr, with D8 of order eight and every prime r>5, the maximum sum of (left-stabilizer size−1) over nonempty prefixes of a labeled element ordering is 132r−40. Requiring the proper-prefix stabilizers to generate G gives maximum 122r−40, a sharp deficit of 10r. The full prefix contributes once and is excluded from that generation condition.

All unrestricted maximizers are exactly recursive maximal-subgroup right-coset block orders, with an exact labeled-count recurrence. A uniform affine certificate establishes the unbounded-prime result. Full-escape optimizer classification/count and prime pairs 7≤p<r remain open. [Review](prefix-p5-uniform.md)

## A growing full-target construction and restricted obstructions

For m≥1, q=483^m and N=5q², the entire positive-chirp matrix B=(F⁻¹+A)⁻¹ has an explicit N-term diagonal-ended cycle-resolvent representation in its original coordinates over L=Q(ω), with ω primitive of order N, F[i,j]=ω^(ij), A[j,j]=ω^(hj²), and h=(N+1)/2. Zero edge weights and singular diagonal endpoints are allowed. Preparation and application each cost O(N²) field operations; growing field degree, indexing, storage and bit arithmetic are charged. This is a dense baseline with no FFT advantage.

The block field K=Q(ω^(q⁴)) has degree four. B[0,1] generates L over K, excluding every finite all-K Green representation. Separately, k ordinary forward/reverse cycle branches plus a diagonal and t isolated-entry corrections require k+t≥21^m. One interleaved arbitrary cycle defeats the rank-one premise, so this lower bound does not cover arbitrary-cycle representations or general FFT circuits. The earlier five-dimensional minimum-three result retains its separate scope. Efficient full-target constructions, arbitrary-cycle small-length representations, negative chirps and stability remain open. [Review](q11-growing-baseline.md)

## Rogers–Szegő overlap for b=13

In characteristic zero, for every primitive root of odd order 29≤d≤103 and every integer A≥1, the overlap polynomial J_(A+1)(x;τ)=x He_A(x)−Aτ He_(A−1)(x), with the original b=13 normalization, has nonzero discriminant. Its degree is A+1; He denotes monic probabilists’ Hermite polynomials. Exact residue-field certificates and rigorous conjugate-annulus witnesses cover all 38 orders; uniform arguments cover all A.

Together with the inherited lower strip and tail, this completes overlap for every odd d>13. Together with the other inherited guards, all four guards now hold for b=1,3,5,7,9,11,13. Overlap gaps in odd degree b≥15 remain open. The separate ordinary-residual squarefreeness remainder at b≥27 also remains open, except separately proved instances. Even orders, nonprimitive roots, positive characteristic and quantitative conditioning are outside scope. [Review](rs-b13-overlap.md)

## Certified amplitudes at supplied locations

For the trusted accepted window family n=2^m, B=2^b, 2≤b≤m, q≥10, w=16Bq+1<n, stable bounded rational inputs, odd integer permutation multiplier and integer translation, the new component estimates a finite supplied index list. The full accepted tap/precision contract applies, including p=q+ceil(log2 w)+6 and Q=m+q+p+10≥56. For every k≥1, simultaneous arithmetic error against its companion estimator is at most a≤(63/512)2^−k<2^−k/8, in unnormalized negative-DFT units.

Actual coefficient error remains |Y_i−F_i|≤|C_i|+(5/64)2^−q|F_i|+a. C_i is full interference; its smallness is unproved. The companion denominator equals one, while the true tap response generally differs. More arithmetic precision removes neither interference nor response bias. Trusted tap provenance and stable source access are assumptions. Preparation, source acquisition, rational scratch, outputs and parsing costs remain charged. For J supplied indices, O((B+J)polylog n) applies under logarithmic numeric/index widths and q=O(log n), with source acquisition separate. This does not establish location discovery, ranking, recovery probabilities, certified randomness, outer-loop composition, unitary/S6 integration or a complete sparse engine. [Review](q16-companion-estimation.md)

## A same-accuracy known FFT comparator

A Good–Thomas 4×3×5 implementation evaluates all outputs of the positive normalized F60 for exact 2^−32-grid inputs with Euclidean norm R≤65,536. Its uniform absolute Euclidean error is below (8R+9)2^−32, meeting the common (28R+22)2^−32 target. Input quantization and relative error are not covered. Stored values and coefficients use 32 fractional bits; exact 128-bit accumulators and higher-width cold coefficient certification are explicitly paid. Setup, admission and all outputs are included; Python preparation costs are not a fully expanded portable bit-operation count.

Qualification is restricted to the reviewed GCC 14.2 Linux x86_64 build and its valid, synchronized-buffer caller contract. Noisy one-host measurements establish no practical speed advantage. Production-library, other-platform and physical-resource qualification remain open; the result gives no general-length improvement or impossibility theorem. [Review](q32-matched-comparator.md)

Classical coset constructions, Gauss-sum/cycle-resolvent algebra, Sawa–Uchida identities and Hermite congruences attributed to Carlitz through Grosu–Grosu, HIKP estimation and Good–Thomas factorization retain attribution. The remaining EFK source-body/equality comparison and historical novelty remain unresolved.
