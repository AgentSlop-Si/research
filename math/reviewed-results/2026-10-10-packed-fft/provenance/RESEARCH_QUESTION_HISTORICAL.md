# Candidate: keep the quantized radix-2 FFT packed between stages

Status: NEW UNREVIEWED RESEARCH HYPOTHESIS. No accepted improvement or historical novelty claim. Derived by the parent during the review cycle on 10 October 2026. Intended target is the existing deterministic finite-word, all-input relative-l2 model, not exact arbitrary-complex arithmetic.

## Why examine this

The accepted F132 / corrected Q01 backend charges O(r) gathering, packing, unpacking and scattering per tabulated radix-r block. This yields O(N log N / log log N) word work for fixed tolerance. That charge is correct for its unpacked representation. It does not automatically apply to another executor that retains many quantized complex states in each word through every radix-2 stage.

Candidate target: power-of-two N, v=log2 N, precision t=ceil(log2(1/epsilon)). Aim for O(N (t+log v)) cold word-RAM work and O(N) words, at least at fixed epsilon and t=o(v). For fixed epsilon this is O(N log log N). A stable all-length compiler may extend it, but do not assume that until its coefficient-generation and interpolation costs are checked. No practical speedup is claimed.

## State and error contract

Reuse the accepted normalized finite-state floating quantizer: p=ceil(log2(C(v+1)/epsilon)), underflow tau on the order of epsilon/(N(v+1)), exponent range O(v+p), b=O(p+log v) bits per complex state. Invalid codes map to zero; overflow must have a total clipped value, and a first-overflow argument must show reachable states never clip. All ideal radix-2 stages are unitary, so a stagewise bound O(2^-p)||z||+sqrt(N)tau accumulated over v stages should give the same relative-l2 contract as the existing proof.

Choose P as a power of two with 2 b P <= v/8 (a conservative budget). Store P consecutive complex state codes in one word. Initial scan, normalization, bit-reversal placement, quantization and packing cost O(N); final unpacking, scale restoration and explicit output cost O(N). Coefficients and indices have bounded O(v) bits; address-capable word RAM includes integer multiplication/division, shifts and Boolean operations. This must not presume a free arbitrary permutation or SIMD instruction.

## Literal iterative DIT layout

Input is packed in bit-reversed order. At radix-2 stage with butterfly span L=2^ell, pair contiguous halves in each length-L block.

- L <= P: each complete length-L block lies inside one packed word. The same within-word transform pattern occurs in every aligned word. Prepare a table mapping every P-state word to its P-state output for that ell. Online: one word lookup/read/write per word, O(N/P) work.
- L > P: each P consecutive lane positions j0,...,j0+P-1 in the first half pairs with one contiguous packed word in the second half. Read two words, form their 2P-state key, look up the P independent normalized butterflies with the appropriate twiddle pattern, split the packed output and write two words. Online: O(1) word operations per pair, hence O(N/P) per stage, IF twiddle-pattern identification is O(1).

This does not gather P separately stored scalars per stage. Lane codes remain packed; the only materialization of individual scalar outputs is at the beginning/end.

## Twiddle patterns: the central finite catalogue claim

Let Q=2^g, g=p+O(1), and approximate exp(-2pi i j/L) by a certified coefficient for grid index floor(Q j/L). Quantized coefficient error is O(2^-p). Since L, P, Q are powers of two and each j0 is P-aligned:

- For L <= Q, the grid index is an exact arithmetic progression with step Q/L.
- For Q < L < Q P, grid indices repeat in groups B=L/Q < P, with B a power of two. The vector pattern is determined by B and its starting grid index.
- For L >= Q P, B=L/Q >= P and each aligned P-lane block uses a single grid index: every lane has the same approximate twiddle.

Tentative number of distinct patterns across all stages is O(Q poly(v)), and pattern identification uses shifts/masks and stage constants in O(1) work per packed-word pair. A sharper O(Q) count might be possible but is unnecessary. The small-span within-word stage tables add only O(log P) pattern types.

For each pattern, tabulate every 2P-state key (or P-state key for small spans). Table size at most 2^(2bP) Q poly(v,p). With 2bP <= v/8 and t=o(v), this is N^(1/8+o(1)) poly(v), hence o(N); preparation of each response by exact dyadic arithmetic, followed by total quantization, costs only poly(v,p). Outputs contain 2bP bits and fit in one word. Pattern directory and offset/address multiplication must be charged and bounded. No oracle or free root/phase table is allowed.

If t is a fixed fraction of v, choose more conservative cutoffs and a conventional fully charged fallback when the table bound ceases to be sublinear. The claim is not established merely by this sketch.

## Intended resulting cost

v stages times O(N/P) work gives O(N v/P)=O(N b), plus O(N) input/output and charged sublinear preparation. This would avoid the old executor's O(r) materialization per block without changing its normwise approximation contract. Uniform finite-size fallbacks and state-width/address guard conditions still need a complete proof.

## Mandatory audit questions

1. Is the packed DIT layout actually maintained with only constant word operations per word pair, including small stages, twiddle phases, index updates, root-grid pattern IDs and output layout?
2. Does one catalogue handle every stage without hidden O(N) scalar coefficient generation per stage or O(P) unpacking online?
3. Are total invalid/overflow table semantics compatible with the existing first-overflow proof? Are one/two-word intermediate products, packed offsets and payloads genuinely bounded?
4. Is preparation uniformly o(N) in the claimed precision regime, including every pattern, table response, constant/root approximation and all directory entries?
5. Does the all-input normwise guarantee survive every butterfly quantization and coarse-grid phase error with conservative constants?
6. Is this already a classical packed approximate FFT theorem? A model-matching primary-source search is required before any novelty assertion.
7. If all-length composition is attempted, count its interpolation, coefficient grids and precision schedule independently. Do not silently multiply its cost by growing Taylor rank.

Canonical accepted comparison: research_cycle_0958/algorithms/FINAL_THEOREM_AND_PROOF.md (SHA c8a775230a824872c23fc48b351e03d63878154bcfb314a8cca689842e31fc8d). Earlier unpacked backend and word model are fully spelled out there. The new candidate must be audited independently rather than inheriting its asymptotic runtime.
