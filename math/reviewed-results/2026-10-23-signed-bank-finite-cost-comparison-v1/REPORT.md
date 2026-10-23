# Finite signed-bank cost and exact FFT comparison

23 October 2026. One exact finite fixture, not an asymptotic or physical-network speed claim.

## Bottom line

The N=19, d=4, m=15, B=32 original signed-bank realization is now independently accepted as a correct complete Fourier realization. Correctness does not make its literal application faster.

In this fresh, shared-kernel warm benchmark, the executed-style bank application took a median 11.342992 ms, versus 177.586699 microseconds for exact 64-point Bluestein and 29.982016 microseconds for direct 19-point DFT. The banks took 63.87 times this FFT baseline's time, or 6,287.30% more time. There is no positive bank-over-FFT speedup. Using the explicitly defined metric 100*(T_FFT-T_bank)/T_FFT gives -6,287.30%, not a positive percentage.

These are observations for this implementation, fixture and cloud environment. They are not an optimized-library contest, a universal lower bound, a complex floating-point FFT comparison, or physical finite-network/hardware latency. The first timing run, also retained, gave 69.03 times FFT runtime. Timing variation must not be hidden behind a highly precise percentage. For a short summary, use “about 64 times slower than this exact FFT implementation in the final run,” not a universal claim.

## 1. Same mathematical input and output

All methods compute the negative unnormalized transform y[a]=sum(t=0..18) 5^(-a*t) x[t], with q=5 of exact order 19 in F191. Every input/output is interpreted in the SAME field

L=F191[A,B]/(f11(A), B^2+78B+121),

f11=A^11+158A^10+43A^9+32A^8+42A^7+173A^6+183A^5+33A^4+17A^3+153A^2+48A+175.

Elements use the ordered 22-coordinate basis (1,A,...,A^10,B,AB,...,A^10 B). The separately accepted realization certifies that this is the field F191^22 and that all 15 roots and all 32 effective banks are genuine. This comparison uses those frozen exact coordinates as DATA. It does not execute an author/historical program, reconstruct a precomputed Fourier matrix from the banks, or relabel matrix multiplication as the bank algorithm.

The DFT coefficients lie in F191 even though bank nodes and coefficients can require L. Therefore a direct coefficient product is a cheap base-scalar scaling, not generally a full L multiplication. For general L input, it needs 22 base multiplications in the written scalar kernel. For base-field input, an implementation staying in F191 needs only one base multiplication per coefficient product, 361 total, and 342 base additions. The common L benchmark does not exploit that entire-input descent. Base-field bank input still travels through L-valued intermediates; returning it as F191 requires checking/removing 21 extension coordinates per output if validation of descent is desired.

## 2. Exact literal bank ledger, independently reconciled

For each bank, beta=1 and

(1-q^(eps*delta*j+delta*i)) v[i] - alpha v[i-eps] = x[i].

The zero diagonal is at i0=-eps*j modulo 19. Precompute ratio[s]=(1-q^s)/alpha and normalized weights w[j]/19. One application computes b[i]=-x[i]/alpha once per bank, obtains v[i0-eps]=b[i0], then traverses the other 18 rows by v[i-eps]=ratio[s]*v[i]+b[i]. It weights and accumulates all 19 output entries of all 19 branches of each of all 32 banks. The bank sum is not collapsed into a Fourier matrix.

Multiplications per bank: N input scales + N(N-1) recurrence products + N^2 weighting products = 2N^2. Therefore total multiplications are 2BN^2=23,104.

Optimized additions: BN(N-1) recurrence additions + (BN-1)N global output additions = 2BN^2-BN-N=22,477. This is equivalent to accumulating each bank with (N-1)N additions and then the B banks with (B-1)N additions.

The accepted author's executed style adds 608 input negations, and adds the first 19 terms into zero output slots, giving 22,477+608+19=23,104 add/subtract calls. Our fresh code reproduces both schedules. The optimized schedule caches -alpha^(-1), paying 32 negations in setup, and assigns rather than adds the first 19 output terms. It was actually executed and passed here; that does not retroactively change the author's original executed tally. Zero/unit products and the four zero raw weights are not skipped.

Direct DFT, under the same conservative no-unit-elision convention, has N^2=361 coefficient products and N(N-1)=342 additions. The bank multiplication-call ratio is exactly 64. The optimized addition-call ratio is 22,477/342=65.722222... . These are arithmetic-call ratios, not speed percentages, and most bank products cost much more than direct scalar products.

## 3. Exact FFT baseline and paid normalization

A 64-point radix-2 transform is valid inside the quadratic subfield: 64 divides 191^2-1. Deterministic search through u+B found a primitive 64th root omega=50+42B on candidate 2. Exact checks establish omega^64=1 and omega^32=-1. No root oracle or approximate complex arithmetic is used.

Let e=10, the inverse of 2 modulo 19. Define c[n]=q^(-e*n^2) and h[r]=q^(e*r^2). Then

q^(-k*n)=c[k] c[n] h[k-n].

Embed h for r=-18,...,18 in length 64. Since 64>=2N-1=37, the desired convolution entries do not alias. Cache the forward 64-point transform of h. A warm call performs:

- 19 input chirp products.
- One radix-2 length-64 forward transform: 192 products, 384 add/subtract operations.
- 64 pointwise products with the cached kernel transform.
- One unnormalized inverse transform using inverse twiddles: 192 products, 384 add/subtract operations.
- 19 output products using cached c[k]/64. Here 64^(-1)=3 in F191; normalization is paid when preparing these coefficients, not omitted.

Total: 486 multiplications and 768 add/subtract operations. Unit/zero twiddle products are included. The forward kernel transform, primitive-root search, twiddle preparation, inverse-length computation and final normalization coefficients are all counted in setup. No additional extension beyond L is needed.

The bank's 1/19 is already incorporated into its cached weights. The target itself is NOT normalized by 1/19. Applying a normalized DFT would require consistently changing every method; it would be wrong to charge a final 1/19 to only one side.

## 4. Expanded arithmetic, not free extension words

The common fresh C++ kernel uses scalar detection on both operands. A base-scalar product performs 22 base multiplications. A generic product uses four degree-10 polynomial convolutions, quadratic reduction, then degree-11 reduction: 746 base multiplications, 746 base additions/subtractions, and 42 modular reductions in the written accounting. An L addition/subtraction uses 22 base additions/subtractions and reductions. These are explicit algorithmic kernel counts, not CPU instructions. Coordinate scanning, indexing, assignment, initialization and equality checks remain additional real work.

| Warm method, archived mixed input | L multiplication calls | Scalar / generic split | L add/sub calls | F191 multiplications | F191 add/sub |
|---|---:|---:|---:|---:|---:|
| Direct 19-point DFT | 361 | 361 / 0 | 342 | 7,942 | 7,524 |
| Original bank executed style | 23,104 | 2,888 / 20,216 | 23,104 | 15,144,672 | 15,589,424 |
| Bank optimized ledger | 23,104 | 2,888 / 20,216 | 22,477 | 15,144,672 | 15,575,630 |
| Exact Bluestein, length 64 | 486 | 241 / 245 | 768 | 188,072 | 199,666 |

These scalar/generic splits are for the archived mixed input, not all possible vectors. The FFT's twiddles and kernel coefficients actually lie in the quadratic subfield. A dedicated quadratic-scalar kernel could multiply a general L element using 66 base multiplications and 33 additions here, rather than the generic 746/746 path. Similarly, subfield-aware bank kernels may improve some of their products. Neither optimization is implemented; the same basic scalar-or-generic kernel is used by every method. Thus this baseline is sound but deliberately simple, not the fastest known exact FFT. No theoretical lower bound or optimality claim follows.

The bank needs about 1,906.91 times direct DFT's base multiplication count in this mixed-input kernel. That is still not a timing ratio. Arithmetic alone must not be converted to an asserted wall-time percentage.

## 5. Cold setup and validation are separate

Common representation and frozen data are supplied. Shared q-power preparation in this exact implementation costs 18 L scalar products; storing these powers directly as F191 values could instead use 18 base products. The comparison does not call either representation/certification free in a general problem: here the supplied accepted finite-field certificate is part of the starting fixture.

Starting from frozen alpha inverses and raw weights, this fresh program's bank cache preparation costs 1,230 L products and 640 L add/subtract calls. This includes 1/19 by exponentiation and a product check, 608 weight normalizations, 608 ratio products, and 32 cached negative inverses. It EXCLUDES upstream root recovery and construction of those raw weights, because those were completed in the accepted fixture, not repeated or assumed to disappear.

FFT-specific preparation costs 342 L products and 384 L add/subtract calls, expanded to 145,808 F191 multiplications and 150,934 additions/subtractions. It includes both tested root candidates, exact root-order checks, all twiddles, the length-64 kernel transform, inverse-length exponentiation/check, and normalized final chirps. Direct DFT uses only the shared q table. Exponentiation costs are included rather than treated as free inversion calls.

The original accepted realization reports its actual upstream costs separately:

- Field/root preparation and controls: 15,634 L multiplications, 662 add/subtract calls, 44 inversions.
- Amplitudes, raw weights, controls and preparation: 291,252 multiplications, 126,195 add/subtract calls, 357 inversions.
- Dense archived inverses, both inverse products and weighted matrix validation: 1,755,904 multiplications and 877,952 add/subtract calls.
- One original warm application: 23,104 multiplications and 23,104 add/subtract calls.

Inversions internally expand into counted multiplication work; the separate inversion count is not a second additive charge for the same exponentiations. The author's final approximately 0.427-second executable run is a combined construction/validation observation, excluding separate factorization and compilation. It is NOT a bank application timing and is not compared with our microsecond transform timings. Separately recorded deterministic factorization took approximately 0.009 seconds; its internal base-field operations are not fully counted. No fabricated end-to-end cold speed ratio is given.

The theorem's structured post-root construction is O(N^3); the author's straightforward per-sector elimination and dense validation have different, higher-order schedules. Warm literal application is O(BN^2), hence cubic for this theorem's B proportional to N. Those three ledgers must not be interchanged.

## 6. Outputs, storage and traffic

All 19 outputs are computed and consumed in every measured transform. A complete L vector holds 19*22=418 base coordinates. The C++ element uses 22 ordinary 32-bit ints, 88 bytes. Nothing stores a complete L element in a magic machine word.

Minimal prepared bank data for this schedule is 608 ratios + 608 normalized weights + 32 (signed) alpha inverses, or 1,248 L elements / 27,456 base coordinates, apart from q values and signs. The code retains both signed and unsigned inverses to compare the two schedules, adding 32 elements. Runtime input-scaled and branch buffers each hold N elements, plus output. The 608 archived inverse matrices contain 4,828,736 base coordinates. The actual RESOLVENT_INVERSES.u8 archive stores each coordinate in one unsigned byte (values 0 through 190), so the verified archive file size is 4,828,736 bytes. Holding all those same coordinates as 32-bit C++ ints would instead require 19,314,944 bytes before container overhead. These archive matrices are NOT loaded, used or needed by the warm bank evaluator.

Direct DFT can use just 19 base q powers and input/output vectors; a full 361-entry coefficient matrix is not required. This implementation stores q as scalar L values. Bluestein stores 64 forward twiddles, 64 inverse twiddles, a 64-entry transformed kernel and 38 chirp coefficients, 230 L elements / 5,060 coordinates as implemented, plus its length-64 workspace. Many coefficients are in smaller subfields and could be compressed, but such compression is not silently assumed in timing or storage.

Indexing, copies, zero-fill, array traffic and output checksum are included in elapsed application measurements. File loading, coefficient setup, correctness comparisons, compilation and output-file writes are not in those warm timings. For a base-field-only output representation, descent removes/checks extension coordinates; no free identification is claimed.

## 7. Execution and evidence

Fresh benchmark.cpp was written from the actual recurrence and transform formulas. It consumes only frozen data in frozen_data.txt. It agrees with the accepted archived mixed input/output and checks all 19 outputs for eight deterministic inputs: that mixed input, six full 22-coordinate vectors, and one base-field vector. The optimized-ledger application also runs, rather than being merely asserted. This is a runtime comparison/control, not a substitute for the independent full 361-entry matrix acceptance already obtained.

A separate -O1 build with undefined-behavior sanitizer and standard-library assertions agrees on every operation count and equality test. An independent read-only algebra audit, using only calculator snippets rather than executing this source, confirmed the root checks, chirps, normalization, FFT counts, bank recurrence and addition reconciliation.

Environment: Linux x86_64, reported CPU model AMD EPYC 9V74 80-Core Processor, GCC 14.2.0. The environment is shared and CPU affinity/frequency isolation was not controlled. Seven sequential batches per method were timed, using the same eight cached inputs and a full-coordinate output checksum. Batches are 4,000 direct calls, 16 bank calls, and 256 FFT calls. Before timing, each of the eight inputs is run through each of the four methods in an untimed equality-validation pass; these eight calls per method are also the only explicit warmup. No timing batch is discarded. Counters are compiled out of the timed instantiations. The timed inner loop uses input (call_index+trial_index) modulo 8 and sums every output coordinate into a checksum written to a volatile sink, preventing dead-code removal of unused results. Methods run in fixed order, not randomized; results are descriptive, with no confidence interval or performance guarantee.

Final-run median (minimum..maximum batch-average):

- Direct DFT: 29.982 microseconds (28.136..32.699).
- Original bank executed style: 11342.992 microseconds (11178.845..11600.249).
- Bank optimized ledger: 12733.137 microseconds (11427.104..14991.907).
- Exact Bluestein: 177.587 microseconds (169.483..207.246).

Fewer counted additions did not produce a reliable timing win for the optimized bank schedule in these runs; branching/compiler effects and shared-machine noise matter. We report both instead of selecting the faster result after the fact.

## 8. Reproduction and boundary

Compile and run only this new source:

    g++ -O2 -std=c++17 -Wall -Wextra -pedantic benchmark.cpp -o benchmark
    ./benchmark frozen_data.txt RESULT_REPRODUCED.json

Exact sanitizer check without rerunning the timing loop:

    g++ -O1 -g -std=c++17 -D_GLIBCXX_ASSERTIONS -fsanitize=undefined -fno-sanitize-recover=all benchmark.cpp -o benchmark_sanitized
    ./benchmark_sanitized frozen_data.txt RESULT_SANITIZED_REPRODUCED.json --verify-only

RESULT.json is the final run; RESULT_INITIAL_TIMING.json preserves the first timing run; RESULT_SANITIZED.json stores the exact sanitizer replay. COMPARISON.csv is a machine-readable summary. SOURCE_BINDINGS.json freezes all read source data/text. No source program from the author or historical research was executed. No external writes were performed.

Established: this one correct original-bank fixture, this same-field literal application ledger, one valid and fully charged exact Bluestein baseline, and reproducible illustrative warm measurements. Not established: a bank speed advantage, optimal bank/FFT kernels, a universal FFT disadvantage, a hardware/parallel-network advantage, an asymptotic improvement, or historical novelty.
