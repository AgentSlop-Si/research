# Independent proof/model inspection: norm-certified finite-word Fourier tabulation

10 October 2026. Source: `library_delta_extracted/fft_norm_certified_tabulation_2026-10-10/fft_norm_tabulation_2026-10-10/THEORY.md`, all sections 1–10, plus README and source ledger. This pass read the mathematical argument, not just its title. No supplied program was executed, imported, compiled or AST-parsed. No recorded test result is represented as a fresh run.

Exact source SHA-256: `a18a347674000c77f29ad86d5ffad2986b4f1091bcb25a3f9487905216a09f84` (THEORY.md), `8c8c167152c1746082541489f6989eed1f24646222b8634aa50bc93b0ec7af8b` (README.md), and `4a375635e6e072f274f74f3c4ee3879950902f9421c21f85eae185666cdbae36` (SOURCE_LEDGER.md).

## Finding

The fixed-accuracy mathematical construction is supported in its stated word-RAM model. I found no substantive gap in its input normalization, error accumulation, complete table preparation, addressing, or space accounting. It is a real newly surfaced research candidate, not an unbuilt exact-factorization premise.

The result is deterministic, applies to every input in the specified finite binary format, writes every output, and gives relative Euclidean error. This is materially stronger accuracy than the earlier all-bin absolute alpha-below-one-half sketch. It remains a finite-word approximate algorithm, with no exact arbitrary-complex, bit-complexity, practical speed or external-priority conclusion.

One generality clarification is needed: “effectively specified epsilon_N” is insufficient to bound the cost of computing a precision schedule. State that its precision exponent is supplied or efficiently computable, and charge that cost. The fixed dyadic epsilon theorem is unaffected. The displayed n^beta regime can be used with a supplied integer exponent or an explicitly efficiently computable fixed beta/schedule.

## Checked mathematical obligations

1. **Input scale.** For nonzero dyadic input, choosing a power-of-two scale by the largest real/imaginary component gives 1/2 <= ||a||_2 <= sqrt(2N). It avoids computing an exact norm. O(log N)-bit dyadics with polynomial dynamic range can be aligned and rescaled in O(N) word work. A chunked leading-bit table is sublinear preparation. Output mantissa/exponent pairs restore the scale exactly.

2. **Alphabet size and arithmetic.** With n=log2 N and p=ceil(log2(1024(n+1)/epsilon)), the exponent range has O(n+p) entries. For p=o(n), one complex code has O(p+log n) bits. The lattice integer representing a decoded value has O(n+p) bits; multiplying by dyadic coefficients, summing at most polynomially many terms and requantizing needs a fixed number of sufficiently large Theta(n)-bit words. This is an explicit fixed-word model, not free arbitrary precision. Intermediate rational coefficient preparation may use polynomially more work, already covered by the sublinear preparation bound.

3. **Uniform quantization error.** Componentwise truncation gives |q(v)-v| <= u|v|+tau. Taking the vector norm yields u||v||_2+sqrt(2N)tau. The residual additive underflow term is divided by a norm bounded below by 1/2, so the argument also covers sparse inputs with extremely small original norms.

4. **Block preparation.** The largest power-of-two radix satisfies mb<=n/4. Therefore every r<=m table has at most N^(1/4) keys. All padded inputs, including invalid codes, are covered. A direct O(r^2) computation per key and O(log m) tables yield N^(1/4)poly(n,p)=o(N). An r-code output fits in the same word budget. Online gathering, packing, unpacking and scattering cost O(r); no r-output operation is counted as free.

5. **Coefficient and phase errors.** Entrywise error u/(8r) implies spectral error <=u/8 for each normalized r-point block. Quantization then satisfies the claimed conservative 3u bound. A 2^(p+8)-point phase grid avoids an N-step accumulated twiddle recurrence. The closest-grid angular error and certified dyadic coefficient error total less than u/8. Its full 2^p poly(n,p) preparation is sublinear when p=o(n). The Machin/Taylor/integer-square-root construction provides a conventional uniform polynomial-cost route; no exact transcendental oracle is needed.

6. **Factorization and operation count.** The displayed mixed-radix identity is the classical unitary Cooley–Tukey formula, with the correct child indexing, phase and normalization. At a recursion level, local transforms are block diagonal and twiddles are diagonal unitary targets. There are ceil(n/log2 m) levels, each with O(N) work, including all indexing and output movement.

7. **Global error and overflow.** The recurrence e_(j+1)<=(1+3u)e_j+3u||a||_2+sqrt(2N)tau is valid for at most 2n+1 target stages. Its exponential sum gives the stated relative-error bound, with ample constant slack. The first-overflow argument is noncircular: every preceding stage is nonsaturating, its norm is bounded by the recurrence, and the next prequantized coordinate is far below 2^(n+4). Arbitrary unreachable table entries may saturate without affecting the theorem.

8. **Space and parameters.** A depth-first recursion retains arrays of geometrically decreasing sizes, giving O(N) live words; tables are o(N). For fixed epsilon, b=Theta(log n), m=Theta(n/log n) and depth Theta(n/log n). For precision exponent ceil(n^beta), 0<beta<1, b=Theta(n^beta), log m=Theta((1-beta)log n). These give the claimed N log N/log log N word bounds. At polynomially small epsilon, b=Theta(n), the radix ceases to grow and this saving is not established.

## Remaining distinction from software validation

The source explicitly says that its fully eager tables are toy-precision examples. Higher-accuracy tests use on-demand entries and forced small radices. Those may test error mechanisms but do not instantiate or benchmark the asymptotic fully eager executor. This inspection does not change that boundary. A production implementation, peak-memory measurements, cold-run timings and meaningful crossover remain absent.

## Prior-art and ranking judgment

Alman's primary paper proves the analogous logarithmic saving for exact constant-field Kronecker transforms using lookup tables; its Section 5 separately discusses word-RAM implementation and bit-permutation costs. This is a close mechanism/model precedent. It does not itself state this rounded complex Fourier norm theorem. Cooley–Tukey, floating quantization and the Four-Russians principle must be credited. [Primary paper](https://arxiv.org/pdf/2211.04643)

Fürer's log-RAM paper, Section 2 and Theorem 1(a), supplies a relevant word-cost precedent: O(n) integer multiplication for n input bits through about n/log n complex Fourier coefficients. Here N counts coefficients, each potentially requiring Theta(log N) bits; substituting that aggregate input size gives the usual O(N log N) Fourier work in this comparison. The cited O(n) multiplication theorem therefore does not directly supply the claimed fixed-accuracy N log N/log log N transform. This is a checked model distinction, not a proof of novelty. [Primary paper](https://arxiv.org/pdf/1402.1811)

The precise possible increment is the all-input complex finite-word relative-l2 contract with cold tables, normalization, underflow, scale-dependent twiddles and the accuracy/radix boundary all charged. A focused comparison with broader finite-precision circuit tabulation and word-RAM Fourier algorithms is still needed. Negative keyword searches are not a novelty finding.

This belongs in the supported-candidate ranking, with a visibly newer proof-inspection record and an unresolved external comparison. It should rank above the old weak-error approximate-FFT headline for research significance. Whether it should outrank an older exact structural theorem depends on whether one values model-wide algorithmic usefulness or the maturity of its precise prior-art distinction; the final rank should explain that tradeoff.
