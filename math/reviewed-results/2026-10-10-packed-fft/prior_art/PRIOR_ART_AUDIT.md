# Packed approximate FFT: bounded primary-source prior-art audit

Audit date: 10 October 2026. Candidate: `packed_fft_candidate_1355/RESEARCH_QUESTION.md`, SHA-256 `030030cbfe69f7e53e650c9661ccc74e6a9721bfdb185c23c8f3ea6c16dd63d5`. The candidate remains unproved; this audit does not certify its correctness, complexity, or novelty.

## Result

No exact match of the entire proposed contract was located in the material inspected: deterministic, all-input, explicit complex DFT output with relative Euclidean error, logarithmic machine words, low-precision floating states retained in packed form, and all setup charged, in `O(N(t + log log N))` time. This is a bounded negative finding, not a priority claim.

The main implementation idea has substantial direct precedent. In particular, retaining the FFT working array in packed form between rounds, tabulating batches of operations, and charging sublinear table construction are already explicit in Chan–Jin–Vassilevska Williams–Xu. Consequently, any eventually proved contribution should be positioned as a particular complex-approximation theorem and uniform implementation, not as the invention of packed FFT stages or Fourier lookup tables.

## Primary-source comparisons

### 1. Chan, Jin, Vassilevska Williams and Xu, 2023

[Author preprint, version 2](https://arxiv.org/html/2310.13174v2), Lemma 2.2; Appendix B, Lemmas B.6–B.7 and their DFT-implementation paragraphs.

Lemma 2.2 gives deterministic length-n convolution over F_p in O(n log p) time for polynomially bounded prime p. B.6–B.7 use packed input/output, a persistently compact FFT array, batched twiddle tables, and explicitly charged n^(0.2+o(1)) preprocessing. Their bit-transposition costs are paid. The proof repairs a missing finite-field multiplication assumption in Indyk's earlier argument. The arithmetic is exact and modular; no complex-error or dynamic-range contract is asserted. No direct black-box conversion to the candidate is established here.

### 2. Fredriksson and Grabowski, 2009; journal version 2013

[Author-uploaded conference full text](https://www.researchgate.net/publication/220266604_Fast_Convolutions_and_Their_Applications_in_Approximate_String_Matching), §2, Algorithm 1, Observation 1, and Theorem 1. [Journal publisher record](https://doi.org/10.1016/j.ejc.2012.07.013).

The method combines independent integer convolutions in carry-free fields, with b=floor(w/u) and u large enough for an exact output coefficient. Algorithm 1 explicitly unpacks the result in O(n). Theorem 1 gives O(n+sigma n log²m/w), subject to the stated pattern-length restriction. It assumes constant-time word multiplication and uses shifts/masks. Its NTT discussion does not independently charge uniform root/modulus construction. This is integer instance packing, not a finite-state complex-error theorem. The full journal article was not accessible; conclusions here use the conference full text.

### 3. Meng Zhang, 2017

[Author-uploaded full text](https://www.researchgate.net/publication/312218301_Fast_Convolutions_of_Packed_Strings_and_Pattern_Matching_with_Wildcards), §§2.2, 3.4.1–3.4.3, especially Theorem 1. [Publisher DOI](https://doi.org/10.1142/S0129054117500186).

The interface explicitly assumes packed integer-alphabet input and returns packed convolution output. Carry-free spacing requires u at least log m+2 log sigma and (2c−1)u≤w. Theorem 1 includes both FFT work and representation-expansion costs; other sections give a different in-place construction. The algorithm uses word multiplication, shifts and Boolean operations, and discusses integer multiplication as another backend. With m≈n and w=Theta(log n), even constant alphabet gives u=Theta(log n), so this packing does not provide growingly many lanes. Its output is exact integer convolution, not approximate complex Fourier coordinates. No candidate-equivalent normwise or cold finite-state table theorem is stated.

### 4. Fürer, 2014

[Author preprint](https://arxiv.org/pdf/1402.1811), §2 Definitions 1–2; §4.1 Theorem 1(a), printed pp. 3–6.

The log-RAM explicitly supports Boolean operations, addition/subtraction, multiplication, integer division, cyclic shifts, branching and direct/indirect addressing on O(log n)-bit registers at unit cost. Theorem 1(a) computes the product of two n-bit integers in O(n) time using the complex Schönhage–Strassen approach. Its FFT has O(n/log n) coefficients of Theta(log n) bits and O(log n)-bit accuracy, recovering an exact integer product. Thus n counts bits, not arbitrary complex output coordinates. This is a uniform arithmetic algorithm rather than a theorem granting free tables. The model is a close instruction-level comparator, while the input size and precision contracts differ.

### 5. Alman, 2022

[Author preprint](https://arxiv.org/html/2211.04643v1), Theorems 1.1 and 3.2; §5.

Theorem 1.1 concerns the exact Walsh–Hadamard transform over constant-sized finite fields and counts bit operations. Its proof explicitly constructs the small transform table. Section 5 analyzes word-level permutation costs and explains why its tabulation does not improve the standard word-RAM implementation. The transform is a fixed Kronecker-power operator rather than the complex cyclic DFT with growing phase catalogue. There is no floating exponent range or approximation tolerance. This source supports the importance of specifying the cost model and of paying data rearrangement, not an identification of the proposed complex theorem.

### 6. Lyubashevsky, Micciancio, Peikert and Rosen, SWIFFT, 2008

[Author-hosted paper](https://people.csail.mit.edu/cpeikert/pubs/fft_impl.pdf), §3, printed pp. 5–7.

The concrete implementation transforms binary length-64 vectors over Z_257. It tabulates an initial eight-input transform in 256 entries and continues with eight-lane, signed-16-bit SIMD operations, including componentwise addition/multiplication and modular reductions. The tables and multipliers are fixed precomputed implementation data. Its stated hardware primitives include SSE2/AltiVec vector operations, stronger than assuming only scalar word instructions without simulation. This is direct precedent for FFT lookup/SIMD techniques but a fixed-size exact finite-field hashing implementation, not the candidate's uniform asymptotic complex approximation guarantee or charged growing tables.

### 7. Reif, 1999

[Publisher statement](https://epubs.siam.org/doi/10.1137/S0097539797324291). The [author's full PDF](https://users.cs.duke.edu/~reif/paper/Eval.pdf) was located but direct retrieval returned 403; the full article and theorem numbering were not independently read. The publisher abstract and indexed author abstract were reviewed.

The stated model uses exact arithmetic and coordinatewise absolute error eta, with k=log(||a||_1/eta). The general fixed-point result has amortized O(log²k) work when m≥n log n/log²k. Its O(n log k) Fourier-related claims concern a restricted root-order regime or descending-magnitude input coefficients. No bounded word instruction set, packed output encoding, or charged low-bit butterfly catalogue is specified in that statement. These restrictions prevent using the abstract alone as a matching all-input single-DFT theorem; full-text verification remains open.

### 8. Cherniavskii, Gribanov, Malyshev and Pardalos, 2025 version

[Author preprint, version 4](https://arxiv.org/html/2405.17001v4), §8, especially Lemmas 17–18 and Remark 5.

This recent source independently analyzes approximate cyclic/generalized DFTs in a Word-RAM setting. Lemma 18 uses O(n log n) operations on rationals with O(log n+log(1/epsilon)+gamma) encoding length, where gamma controls the encoded input approximation. It gives an infinity-norm error estimate, and Remark 5 explicitly discusses root-approximation setup across repeated transforms. It does not state a packed O(n log log n) relative-Euclidean FFT theorem. It is a useful precision/setup comparator, not a subsuming asymptotic result.

## Comparison deductions, not claims made by the cited authors

1. **Norm conversion is not itself a separation proof.** For an unnormalized Fourier matrix F, ||Fa||_2=sqrt(N)||a||_2. Coordinatewise absolute error at most epsilon||a||_2 suffices for relative Euclidean error epsilon. Thus an absolute-error theorem can sometimes imply the desired normwise guarantee. In Reif's stated parameters, this choice yields k≤t+(1/2)log N up to constants. At fixed epsilon, the general-point threshold m≥N log N/log²k still exceeds N asymptotically. The sampling-count/input restrictions matter in addition to the norm terminology.

2. **Integer packing does not eliminate carry bits for free.** Straight Kronecker substitution of length-N, B-bit nonnegative integer coefficients needs fields of order 2B+log N bits so products and summation do not overlap. Combined with linear-in-bit-length integer multiplication on a log-RAM, the resulting bound is O(N(B+log N)), not automatically O(N(B+log log N)). Modular convolution over a small prime avoids large integer outputs, but preserving arbitrary complex amplitudes and relative error requires an additional reduction, not a change of notation.

3. **Explicit output does not invalidate an O(N log log N) bound.** An O(N) final unpack/scale/output pass fits. However, packed-input/output results with sublinear runtime cannot be quoted without adding that pass. The candidate correctly intends to pay initial and final materialization; the proof must make the finite-word complex output representation explicit.

4. **The candidate's distinctive unresolved interface is precision plus phases.** Its promise is that all reachable complex states can be represented using b=O(t+log log N) bits while preserving a global relative norm bound despite very small entries and cancellation. It then needs a compact, uniformly generated set of packed twiddle patterns and constant-time pattern identification throughout the full-length FFT. Neither property follows merely from the existence of a finite-field packed transform.

5. **Instruction-level comparison must be literal.** A proof using table lookup, scalar integer arithmetic, shifts, masks and bounded addressing is compatible in spirit with the reviewed logarithmic-word algorithms. It must still show bounded products, keys, outputs and addresses. Hardware lane multiplication or arbitrary permutations cannot be silently counted as one allowed scalar word instruction. Generic algebraic-operation counts and BIT-operation counts must not be used as the same baseline.

6. **Cold uniformity matters separately from online work.** A correct theorem must include all table enumeration, coefficient certification, directory construction, finite-size cutoffs and fallback execution. A hardware benchmark with a fixed precomputed table does not establish this. Conversely, sublinear charged universal tables already occur in prior work, so that device alone is not a novelty differentiator.

## Search coverage and remaining gaps

- Examined the exact candidate sketch; revisited the existing prior-source crosswalk; followed primary sources for recent packed convolution, finite-field transform tabulation, integer multiplication, older integer convolution packing and FFT-specific SIMD lookup.
- Searched terminology spanning word-RAM/log-RAM, bit-packed FFT, lookup butterflies, quantized states, low precision, relative error, and O(N log log N). This is not an exhaustive citation search or a priority certification. No absence-of-keyword argument is used.
- Fredriksson–Grabowski 2009 and Zhang 2017 author-uploaded full texts were inspected, including algorithm/theorem locations. Fredriksson–Grabowski 2013 publisher access did not yield full text.
- Reif's full author PDF and the parent-supplied Michigan dissertation URL returned 403. The latter is therefore not used for a substantive conclusion. SIMD evidence above instead comes from the accessible primary SWIFFT paper.
- The entire numerical-FFT and historical Four-Russians literature, all unpublished folklore, and every citation descendant of the matching methods have not been exhausted. An expert priority inquiry and fuller Reif/journal access would materially strengthen any publication novelty discussion.

## Recommended research-record wording

“An unproved candidate adaptation of established packed/table-based transform techniques to a deterministic finite-word, all-input relative-Euclidean complex DFT contract. The claimed O(N(t+log log N)) cold bound requires independent proof. The reviewed prior results overlap substantially in mechanism but did not establish an exact match of the complete contract; external priority remains unresolved.”

No remote state was changed. No publisher PDFs or full-text copies were placed in a public repository.
