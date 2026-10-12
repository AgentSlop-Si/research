Publication derivative of an independently reviewed research report. Private tracking and delivery details are omitted; mathematics, source attribution, limitations and review method are retained. Original source-report SHA-256: f6927e2cf61aad79cbaef82181b0cbe67bbb23ea757fe214e8635c6008dbc733.

# Q32 matched p32 Good–Thomas comparator: independent ACCEPT

12 October 2026 UTC. Verdict: **ACCEPT_SCOPED**. No blocking defect was found in the reviewed numerical theorem, source-level range argument, or tested ABI implementation. This completes the bounded all-admitted-input **algorithmic comparator** sub-obligation. Broader native qualification remains open.

## Artifact binding and execution boundary

Reviewed candidate: `Q32_Matched_P32_PFA_Comparator_CANDIDATE_2026-10-12.zip`, SHA256 `40bf6c9c43ffa08faedf8f5b4e2c744d7759be332d9cf3de82894e7aef82f26e`.

Author cold evidence: `Q32_Matched_P32_PFA_Comparator_AUTHOR_COLD_2026-10-12.zip`, SHA256 `c70534a2dd9983439c370375aa635af277c67cfe270143c8ee81ce7360b75484`.

All 57 candidate archive members were safely extracted into a new writable directory; all 56 SHA256SUMS entries passed before execution. Numerical source, preparation/model/test/benchmark scripts and executed reference dependencies were inspected first. Shipped build artifacts were not trusted. Every native profile was rebuilt from the extracted source.

The concrete replay environment was Debian GCC/G++ 14.2.0-19, Linux x86_64 LP64 little endian, Python 3.12 and the available pthread/runtime. The source’s GCC-compatible and architecture guards do not qualify every compiler that happens to pass them.

## Accepted mathematical contract

The input is 120 interleaved exact signed integers divided by Q=2^32, representing 60 complex numbers. The accepted domain is the closed ball sum(a_i^2) <= 2^96, including zero and equality, with component cap 2^48. The component cap is redundant mathematically on this ball but essential for safe native admission. For any R satisfying ||x||_2 <= R <= 65,536, the target is the positive normalized transform exp(+2*pi*i*k*j/60)/sqrt(60).

The comparator returns every component on the same q=2^-32 grid and satisfies

    ||PFA(x) - U60 x||_2 < (8R+9)/2^32 < (28R+22)/2^32.

This is an absolute complex Euclidean bound. It is not a relative-error statement and does not include conversion of arbitrary real or floating inputs to the dyadic domain. At zero the implementation returns exactly zero. Neither bit equality with the accepted Q32 method nor equal rounding locations is required by the matched accuracy contract.

### Ordering and coefficient proof

The input coordinates are j=15a+20b+12c mod 60; output coordinates are k=45A+40B+36C mod 60. Both are bijective. Their product satisfies jk = 15aA+20bB+12cC mod 60, yielding the positive 4x3x5 transform with no inter-factor twiddles. A second reviewer implementation reconstructed input coordinates as (-j mod 4, -j mod 3, 3j mod 5) and output coordinates as (k mod 4, k mod 3, k mod 5); all 3,600 identities passed.

All six coefficient integers were independently recovered from 224-bit outward algebraic intervals, without importing the candidate preparation program:

- sqrt(3)/2: 3719550787
- (sqrt(5)-1)/4: 1327217885
- -(sqrt(5)+1)/4: -3474701533
- sqrt(10+2sqrt(5))/4: 4084756634
- sqrt(10-2sqrt(5))/4: 2524518436
- 1/sqrt(60): 554477894

Each complete interval lies strictly inside its unique nearest-even p32 rounding cell. The candidate’s independent 96-bit preparation also regenerates the exact header, ten bounded integer-square-root searches, 970 search passes and all permutation checks.

### Rounding and uniform error proof

Radix 4 is exact. In radix 3, each of 80 non-DC real components is formed with a complete signed widened dot numerator and rounded once; the half coefficient is exact. In radix 5, each of 96 non-DC real components similarly receives one final rounding after all cosine/sine products and sums. The 120 normalized output components are then rounded once. These operations agree with the stated coefficient-rounded matrices and rounding-error vectors.

The published block spectral/Frobenius bounds are conservative but valid. There is no missing multiplicity factor for block copies: the spectral norm of a block diagonal operator is the maximum block norm. The full 120-component round-error bounds are accounted for separately. Grouping the exact unnormalized Fourier product before bounding normalizer error gives the displayed uniform bound. Independently recomputed rational upper constants are 798119/102400 < 8 and 879637/102400 < 9. Strict rational radical inequalities justify the strict final bound, including the norm boundary.

This is an audited mathematical/source argument, not a theorem inferred from 2,507, 4,100 or any other finite number of tests. It is not a machine-checked verification of an arbitrary compiler or processor.

### Native admission, ranges and undefined behavior

Null pointers or sizes other than exactly 960 return status 1 before dereferencing buffers. The source copies the input locally before validation, rejects components outside +/-2^48 before squaring, and accumulates the exact squared norm in unsigned 128 bits. Equality with 2^96 is accepted. Domain failures return status 2. On normal nonzero return no output bytes are changed.

The component-box proof bounds the stored radix-4, radix-3 and radix-5 magnitudes by 4M, 16M and 144M respectively, M=2^48. Thus stored magnitudes are at most 40,532,396,646,334,464 < 2^56. Widened intermediate magnitudes are at most 174,085,318,024,506,601,157,689,344 < 2^88. Validation sums are bounded by 120*2^96 < 2^103. Intermediate pair sums, partial dot sums and products fit their stated types.

Every potentially wide multiplication converts before multiplying. No negative signed left shift is used. The magnitude calculation -(n+1) followed by unsigned +1 is safe, shifts have valid fixed counts, and the rounded result is representable before narrowing or signed negation. All transform coordinates are populated before being read; the checked table permutations stay inside the arrays. No saturation or overflow fallback is needed.

The byte-buffer copy boundary supports unaligned, exact in-place and arbitrary partial overlap under the stated valid-buffer, lifetime and synchronization preconditions. It does not protect invalid addresses, falsely declared extents, races, signal-interrupted copies, process faults or stack exhaustion. Immutable globals and local per-call state support concurrent independent calls; TSan and a general concurrency proof are not claimed.

## Fresh execution evidence

1. Archive-only cold replay passed every documented stage: hash check, coefficient/CRT preparation, proof, five compiler profiles, adversarial controls, benchmark and cost ledger. The original 2,507-vector fixture, rigorous interval record, proof certificate, rounding fixture and adversarial result regenerated byte-for-byte. The accepted reference was freshly compiled and all 2,507 same-fixture outputs passed its existing common error target.
2. A reviewer-authored 224-bit outward algebraic oracle constructed each true 60th root using root60 = i^3 * root3^2 * root5^3, followed by exact normalized dense DFT interval accumulation. This does not reuse the submitted Machin/Taylor oracle or its numerical Python functions.
3. A second reviewer-authored p32 model used generic short dense transforms on modular coordinates, independently of the native conjugate-pair expressions. All 120 output integers agreed on 1,597 reviewer fixture vectors. Every vector also satisfied a rigorous full-output direct interval bound. There are 1,593 inputs absent from the author fixture, or 4,100 combined unique inputs.
4. The reviewer fixture covers 360 randomly signed support-boundary vectors, 240 different tangent vectors, 500 independently seeded ball vectors, 256 tiny vectors, 240 inputs placing the normalizer on halfway residues, and zero. All five rebuilt native profiles passed this full fixture, all 1,919 overlap displacements and their thread/guard controls. An additional 638 admission/status-precedence/unchanged-output controls passed.
5. Reviewer-only scalar executables passed 166,450 separately encoded signed/tie/boundary rounding checks each under O3 and ASan+UBSan. Fresh protected-page controls place both input and output at the beginning or end of a readable page and test bad-size rejection against inaccessible pages. No sanitizer diagnostics occurred.

The author’s 10,354 rounding cases per O3/UBSan profile and four mutation controls also reproduced. Leak detection alone was disabled as documented; there is no successful LeakSanitizer or ThreadSanitizer qualification. The independent O3 export inspection confirms the sole numerical API symbol pfa_f60_eval_v1.

## Required cost and precision clarifications

**“p32 internally” means p32 coefficients and stored transform values, with explicitly widened exact product/dot numerators.** The fused radix dots retain their exact numerator until one rounding. There are no higher-precision stored roots or transform arrays and no floating-point arithmetic, but it would be misleading to say every intermediate bit pattern has only 32 fractional bits or that each scalar product is individually rounded. The accepted reference also uses exact 128-bit product/combination numerators, with its own different rounding schedule. The disclosed source costs charge these wider operations.

The independently re-counted PFA transform uses 352 nontrivial product expressions, 104 exact power-of-two scaling product expressions, 504 int64 additions/subtractions, 360 int128 additions/subtractions and 296 roundings. Admission adds 120 widened squares and 120 unsigned-128 additions: **576 total widened product expressions**. These are source-expression counts, not generated machine instructions.

The pinned Q32 reference has 396 transform product expressions and 120 admission squares: **516 total widened product expressions**, plus 1,026 transform real additions/subtractions and 258 component roundings. Its transform count includes zero and power-of-two factors. Therefore the isolated comparison “352 versus 396 products” is not an apples-to-apples total-cost claim. PFA has fewer source additions but more total product expressions and more component rounding calls. No time ordering follows from these mixed ledgers.

PFA reads/copies all 960 input bytes, writes/copies all 960 output bytes and constructs its 168-byte plan on every admitted call. The Q32 reference’s per-call plan is 4,720 bytes. PFA’s stated array/plan object payload is 4,168 bytes versus the reference’s 16,768 bytes. These exclude scalar temporaries and ABI/runtime overhead and are not hard stack or process-memory bounds.

The fixed native helper code is explicit and bounded. Preparation pays all ten bounded integer-square-root searches and interval/permutation work in fresh runs. However, the preparation ledger does not enumerate every primitive operation inside Python Fraction normalization, division, allocation or serialization; those remain explicit source/runtime work included in observed elapsed setup. “Fully charged” should mean none of the setup, admission, plans or outputs is silently omitted, not a fully expanded portable exact bit-operation or physical-resource count.

Fresh timing observations, in milliseconds:

- 41 process-only samples: PFA median 0.747, reference 0.768; ranges overlap.
- 11 preparation-plus-process samples: PFA median 30.892, reference 58.738.
- Three source-cold samples including fresh compilation: PFA 239–298, reference 195–223.

All 960 output bytes are captured and checked. Process creation, loader/runtime, serialization and IPC are inside these timing boundaries. They are process-cold measurements with warm/uncontrolled filesystem and CPU cache state. The source-cold ranking differs from the preparation-only ranking. There is no benchmark-supported practical speedup claim.

## Attribution and remaining scope

The primary research source describes Good–Thomas as a coprime-factor decomposition that removes inter-factor twiddles and discusses PFA selection in its code generator. This candidate is a fresh bounded implementation of that known algorithm, not a new algorithm or a reproduction of that generator’s performance. [Kurzak et al., Sections 3.1–3.2](https://pmc.ncbi.nlm.nih.gov/articles/PMC2744990/).

FFTW’s official accuracy methodology uses random test inputs and high-precision comparisons; its comments discuss implementation/compiler-dependent accuracy. Those sources provide useful context, not an all-admitted-input certificate for an installed FFTW binary. No FFTW production qualification is obtained here. [Methodology](https://www.fftw.org/accuracy/method.html), [accuracy comments](https://www.fftw.org/accuracy/comments.html).

Still open: other compilers and hardware, production callers, exact-build black-box/production-library qualification where required, deployment and physical-resource guarantees. There is no novelty, priority, best-possible-FFT, general-N asymptotic, broad resource or practical-speed claim.
