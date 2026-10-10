# Independent review of the packed all-length Fourier theorem

10 October 2026. Decision: accepted at the mathematical proof level for the exact source hashes below. No blocking mathematical or computational-model gap was found in the all-length composition or its newly supplied scalar fallback.

## Frozen sources and scope

The reviewed all-length source is `../all_length_extension/CONDITIONAL_ALL_LENGTH_THEOREM.md`, SHA-256 `71d85d704058bd245d14ce5aad65f747cb1a5b038e69510b21b41d3c8a217927`.

The paired dyadic source is `../executor_derivation/DYADIC_PACKED_THEOREM.md`, SHA-256 `bb40decffd28b87a88065880363ff099b0d22071ef976bc67a8195c9b9db6d6f`. Its independent acceptance is `../independent_audit/FROZEN_PROOF_REVIEW.md`, SHA-256 `c8ccac0e576240c4b95dc9f9a58829b0fd33c17062526c5e19324a1a6156fb28`. This review directly checked the dyadic interface needed by the composition; the complete packed-layout acceptance is the separate dyadic review.

The canonical interpolation source was read directly and its SHA-256 verified as `c8a775230a824872c23fc48b351e03d63878154bcfb314a8cca689842e31fc8d`. The earlier Q01 acceptance receipt was read and verified as `f842356d4b49ce036024991ab4d5cb2f718b888821df1d9f104cf437d61de396`. This review does not replace or change that accepted theorem, its precision boundary, or its previous correctness fallback.

The all-length manuscript is written as a conditional theorem with interface H. The cited accepted dyadic construction supplies that interface. Consequently the paired sources establish the stated finite-word all-integer-length theorem at the proof level. Neither source is a production implementation certificate or an external novelty determination.

## Accepted theorem

For fixed input-format constant c, N>=2, n=ceil(log2(N+1)), and a supplied integer 2<=t<=n, represented dyadic inputs with O(cn)-bit descriptions and polynomial dynamic range admit deterministic explicit dyadic outputs satisfying

    ||y-U_N x||_2 <= 2^-t ||x||_2.

On the specified address-capable integer RAM with sufficiently large fixed word width C(c)n, the cold work bound is O_c(N(t+log2(n+1))) and storage is O_c(N) words. N=1 is an exact copy. Input scans, normalization, all coefficient construction, tables, memory access, indexing, conversion, rounding, and output are charged.

The result is finite-word approximate Fourier computation with an all-input relative-l2 guarantee. It is not an exact arbitrary-complex arithmetic FFT result, per-coordinate relative-error result, fixed-hardware claim, or bit-complexity theorem.

## Interpolation and representation checks

1. The padding length M is between 4N and 8N. For v=log2 M, v is either n+1 or n+2. Centered padding is an exact isometry. After the wrapper's single normalization, the backend receives maximum real/imaginary component magnitude in [1/2,1), so scale 1 is legal.
2. The compiler uses exactly one dyadic transform with T=t+10 and rho=2^-(t+10). The branch explicitly checks T<=v+1; a statement at precision t alone would be insufficient.
3. The accepted full interpolation operator has norm less than 3 on arbitrary errors. Its truncated, coefficient-quantized version and phase/scale map satisfy the quoted spectral bounds. No linearity of the rounded backend is assumed.
4. The three error terms are 6rho, 4rho, and 9rho times the normalized input norm. Final quantization adds at most 3rho. The total 22rho is strictly below 2^-t. The prequantization norm bound also excludes the final upper-clipping threshold.
5. The actual backend supplies lattice 2^(-v-2p)Z[i], with p=T+10+ceil(log2(v+1)), O(v+p)-bit lattice numerators, and constant-word decoding. Exact O(t)-term interpolation sums, coefficient multiplication, phase multiplication, and carries use O_c(n+t+log(n+1)) bits. There is no hidden O(t) multiplicative expansion of operand width.
6. Kernel-table cardinality is O(2^t(t+1)^2), final phase-grid cardinality is 2^(t+15), and each coefficient certificate has charged polynomial work. Online phase addresses, retained-sample addresses, wrap, gathers, and output cost O(N(t+1)). No N separately expensive transcendental evaluations are inserted.

## Uniform preparation and fallback checks

The wrapper attempts interpolation only for t<=n/4 and the stated backend/stencil guards. Its actual preparation is limited to N elementary RAM instructions and N preparation words, with allocation checked before use. Either a completed table is used or the incomplete attempt is discarded. Counter overhead and cleanup are O(N). The leading-bit table is built within that budget before the successful branch's O(N) normalization scan, so the fast case does not hide an earlier O(Nn) input pass.

The unbudgeted wrapper preparation is bounded by a fixed polynomial times N^(1/4)+2^t(t+1)^2+1. Uniformly for t<=n/4 this is o(N), and every guard eventually holds. For every supplied t=o(n), the wrapper preparation is o(N). The paired concrete dyadic construction separately proves eventual packed selection and sublinear cold table preparation in that regime.

For t>n/4, the new scalar fallback's O(Nn) cost is O(Nt). If a low-precision guard or preparation budget fails, n is below one fixed finite threshold, and the same fallback is absorbed into the claimed bound with a uniform constant. The old N^2 poly(n+t) correctness fallback is not used to justify the improved uniform runtime.

## Scalar Bluestein fallback checks

The fallback is separately justified and does not assume H.

- A fixed-lattice scalar normalized radix-2 transform, including initial input rounding, satisfies error at most 16k u (||z||+sqrt(H)), where H is its dyadic length, k=log2 H+1, and u=2^-q. The coefficient-perturbation Frobenius bound below 4u and the accumulated rounding recurrence are valid under the stated smallness condition.
- Two full guarded circles of orders H and 2N are generated in O(N) word operations after polynomial-cost seeds. The guard K=q+ceil(log2 L)+10 gives phase error below u/128. Modular j^2 addresses correctly supply both signs of the chirps; products and indices have O(n+t) bits.
- The normalized Bluestein identity has alpha=sqrt(H/N) and lambda=alpha U_H b. Its crude multiplier norm bound sqrt(2H) suffices. The proof does not assume an O(1)-sup-norm chirp-spectrum construction or suppress the known black-box error amplification.
- The manuscript's vector bounds follow successively: transform errors at most 100k sqrt(H)u and 50k sqrt(H)u; multiplier error at most 160k sqrt(H)u; product error at most 500kHu; inverse error at most 600kHu; final error at most 2048kHu.
- Choosing q=t+log2 H+ceil(log2 k)+13 gives total absolute error at most epsilon/4. Since the normalized input norm is at least 1/2, this is safely within the relative target. Exact restoration of the original power-of-two scale preserves that guarantee.
- Three scalar FFTs, two generated circles, and O(N) remaining operations give O(Nn+poly(n+t)) work and O(N)+poly(n+t) words. In the finite theorem domain t<=n these are uniformly O(Nn) and O(N), including all small sizes. Polynomial scratch and seed costs are not treated as free.

The optional arbitrary-t fallback proposition also remains separate from the fast theorem. Its larger word width and polynomial certificate cost are explicit; fixed-lattice output can be written directly without a t-dependent floating leading-bit scan. It does not enlarge the packed backend's accepted precision domain.

## Fresh independent falsification controls

The accompanying `check_all_length_controls.py` was newly authored for this review and run directly. It imports only the Python standard library; no uploaded, predecessor, or constructor program was run, imported, compiled, or parsed for execution. `CONTROL_RESULTS.json` records all completed cases.

- 8 normalized Bluestein identities at lengths 2 through 31, using 100-digit Decimal reference arithmetic. Largest discrepancy was below 9.2e-89.
- 48 three-transform fallback executions at selected lengths 2 through 65 and both low and upper-domain supplied precision. The FFT arithmetic, lattice truncations, guarded recurrence updates, and products were exact integer operations. Every result met the target and conservative budget; the largest observed fraction of the absolute error budget was below 0.000310.
- 45,149 exact Fraction/integer checks of the precision choice, smallness conditions, and conservative aggregate error inequalities.
- 4 independent interpolation identity and periodic-tail Schur controls, including N=137 with the actual t=2 stencil s=18. Largest relative identity discrepancy was below 3.6e-14 in ordinary complex floating arithmetic. Every tail bound passed.

Decimal trigonometry and floating controls are falsification evidence, not certified coefficient-generator execution. The controls are not benchmarks, exhaustive validation of all lengths, or a replacement for the analytic proof. No remote state was changed.

## Remaining boundaries

External priority is unresolved; packed/tabulated FFT computation has prior literature. The accepted contribution here is the checked combined theorem and exact model scope, not a claim that packing itself is new. An implemented eager-table executor with certified coefficients, realistic crossover study, external theorem/model comparison, and the separate exact-complex objective remain outside this acceptance.
