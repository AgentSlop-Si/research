# Independent review: Certified growing-fiber Fourier theory

## Decision and exact coverage

**The mathematical algorithm and bounds in Sections 1–13 are accepted in the stated exact-field/word model.** They give a genuine structured-input algorithm with full input certification and all N Fourier outputs. They do not give an unrestricted faster FFT. Section 14's limitations are appropriate.

This direct upload contains only THEORY.md. Its referenced `verify.py`, implementation module, RESULTS.json, source test logs and counted-operation profiles were not supplied with this source. Therefore the source's implementation/test-count assertions and the specific 7,516,160-versus-7,340,032 profile are **not independently verified**. The reviewer instead authored and ran a separate implementation of the mathematical algorithm. This review does not certify unavailable code or claim every referenced artifact was inspected. External publication priority remains unverified.

Source identity: Library [private-id], version 0, 22,661 bytes, SHA-256 a5c0da63f7761f91c26cf7662afb0ba5f7874f330db36791addde9bf6c58f045. It differs substantively from the earlier dyadic/aggregate theorem; it is not a byte-identical resend. Snapshots of the compared earlier theorem and Hero17 report are preserved.

## 1. Recognition and Fourier orientation

For N=QM, Q=2^floor(k/2), M=N/Q, define eta=w^Q and theta=w^M. A fiber expansion y_t[u]=sum_h a[t,h] eta^(−hu) gives exactly

Fx[h+Mv]=M sum_t a[t,h] w^(ht) theta^(vt).

The sign, inverse-root synthesis and factor M are correct. The reviewer reconstructs fibers independently by direct character sums and compares final results to an iterative FFT, itself cross-checked against direct DFTs at small sizes.

For r distinct nonzero nodes with nonzero amplitudes, the r-by-r Hankel matrix V diag(a) V^T is invertible even over the permitted finite fields. This makes the 2r-sample recurrence identification complete, without a generic-position assumption. Berlekamp–Massey on the first 2b samples therefore succeeds under the cap. A prefix fit alone is not accepted: all roots must lie on the Fourier grid, candidate amplitudes must be nonzero with nonzero derivative denominators, and all M original coordinates must match the reconstructed fiber. The zero-degree case requires a full zero check.

The formula a_h=−lambda_h A(z_h)/C'(z_h) follows by multiplying the partial fraction identity by C and evaluating at z_h=lambda_h^−1. Truncated polynomial multiplication and r evaluations cost O(r²). The root-grid scan evaluates the zero-padded recurrence coefficient vector with a pruned M-transform; no uncharged factoring or discrete-log oracle is used.

## 2. Pruning and charged costs

At depth d of the parity tree, at most min(2^d,s) nodes are active, each with length L/2^d. Summing combine work and zero-output allocation gives O(L[1+log(s+1)]). Sparse-list partition work O(s log L) is bounded by the same envelope for 1≤s≤L; the zero vector costs O(L) to write. Depth-first live buffers and lists fit O(L) space. Shared root tables can be built in O(N), with all subsequent twiddle lookups charged.

Three uses matter: recurrence-root evaluation, full fiber verification and global synthesis grouped by equal frequency residue. Since sum_h kappa_h=K, concavity gives Q sum_h log(1+kappa_h)≤N log(1+K/M). Together with quadratic recurrence/amplitude work, this yields

O(N log(b+2)+Q b²)

for every accepted or rejected cap-recognition run. Setup, root tables, mode records, input/index work and explicit output writes are included. O(N) memory suffices. Rejected candidates stop within the cap; no search over unbounded recurrence degrees is permitted.

The profile-sensitive successful bound and the optional O(Qb+bK) successful-prefix refinement are consistent with the same analysis. The simpler headline O(Qb²) is sufficient. For b=polylog(N), Qb²=o(N), yielding O_c(N log log N). For b=N^o(1), Qb²=N^(1/2+o(1))=o(N) and log b=o(log N). These are exact field/word bounds, not bit complexity, finite-precision stability, or practical timing claims.

## 3. Aggregate heavy-fiber bound

Let ell=log2 M, a=max(1,ceil(K0/Q)), B=min(M/2,a ell). A failed complete light recognizer certifies r_t>B. A full ordinary M-transform then discovers that fiber's true modes. On successful runs each heavy fiber spends at least B+1 units of the supplied budget. On rejection, at most one final over-budget heavy fiber is uncharged to the accepted prefix. Consequently the heavy count is at most floor(K0/(B+1))+1 and its transform cost is O(M ell(1+K0/B)).

The extra +1 is necessary, including when K0=0. The full bound in Section 9 includes it. In the eventual unsaturated regime B=a ell, K0≤aQ makes the heavy cost O(N+M ell)=O(N) for the balanced layout. The remaining O(N log(a ell+2)+Q a² ell²) is O_c(N log log N) for K0=O(Q log^c N). Individual fibers may have all M modes. The finite saturated case uses the unsimplified bound and remains correct. An ordinary full-FFT fallback after total-budget rejection gives all-input correctness but restores the usual O(N log N) worst case for the stated schedules.

This extends the earlier aggregate theorem's useful growing-budget regime. The earlier O(N) algorithm at K0=O(Q) can be better and is not superseded at every parameter point. The cap-only and aggregate classes must not be conflated.

## 4. Density, Green preconditioning and coverage limits

For square N=M², the cyclic b-mode support with dominant coefficient 2b has coefficient matrix 2bI plus b−1 permutation matrices. Over C its perturbation norm is at most b−1, proving invertibility. Reverse triangle inequalities give no zero raw entries and no zero Fourier outputs. Balanced reshaping therefore has full rank, despite the sparse intermediate bank. This norm proof is not imported into finite fields. The stated modular N16 control was independently reproduced: dominant coefficient 4 causes an output zero, while 5 avoids it.

For P=7I+S+2D^−1 and L=7I+D+2S, FS=DF and FD^−1=SF imply FP=LF. One sparse residual application and one guarded cyclic solve add O(N). Over C both operators have singular values in [4,10] and condition number at most 2.5, by the norm bound on the perturbation of 7I. This says nothing about numerical stability of exact Prony recognition. Finite-field diagonal and closure guards must be checked, as the source requires. The optional test-input generation P^−1r is separate from the raw-input algorithm.

For each fixed support pattern the accepted set is a K-dimensional linear subspace. A finite collection of fixed invertible frames and fixed d-dimensional correction spaces has dimension at most K0+d per pattern. It cannot cover C^N when K0+d<N. This is a valid finite-union-of-proper-subspaces obstruction, with the stated restriction to fixed linear frames/corrections. It is not a lower bound for all nonlinear parameterizations or arbitrary circuits.

## 5. Independent controls and portability

Fresh reviewer code passes:

- 240 pruned-transform cases against both direct DFT and separately written dense iterative FFT;
- 1,294 exact recognition cases: 575 accepted and 719 rejected;
- 211,856 checked accepted output coordinates;
- 72 late-corruption cases whose short prefixes remain unchanged;
- 530 charged heavy-fiber fallbacks, checking the success/rejection heavy-count inequalities;
- 14,034 pruned calls with conservative operation/allocation/partition envelopes checked;
- four modular dense/full-rank square controls;
- seven Green-preconditioned cases and 1,016 final output coordinates.

Sizes range from N4 to N16,384, with both square and Q<M layouts. Fields are F65537 and F998244353. Atomic raw vectors, zero budget, generic dense inputs, saturated caps and completely heavy fibers are included. These are controls of the reviewer's implementation, not the absent source implementation. Isolated standard-library replay is byte-identical.

## 6. Prior art and source comparison

The [FFTW pruning discussion](https://fftw.org/pruned.html) explicitly describes the O(N log K) arithmetic bound for K nonzero inputs and warns that arithmetic reductions need not improve practical performance. This supports the source's attribution and performance caution. The [Briani–Cuyt–Lee paper](https://arxiv.org/abs/1706.04520) establishes that Fourier/Prony hybrid methods are prior art; its abstract was checked, not its complete proof. The [Bringmann et al. paper](https://arxiv.org/abs/2107.07347) concerns sparse Fourier recovery via tree exploration; its abstract was checked only for the stated broad relationship, not as a proof of this algorithm or a universal lower bound.

The earlier project theorem's O(N+MK0+QK0+K0²) ledger and the older bounded-fiber O(rN+Qr²+rQ²+N) ledger were compared to their actual preserved texts. Replacing mode-by-mode evaluation with three pruned transforms changes these documented upper bounds. No lower bound against every possible implementation of the old ideas or publication novelty is inferred.
