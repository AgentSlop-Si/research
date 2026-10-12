Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: df9ff2dfacecd0d14f0740c472b202e2ae3120847d30f36f1de333da1534390b

---

# Independent review: complete Q30 Karatsuba P/Fourier baseline

11 October 2026. Independent review of the sealed fresh implementation, with no external writes and no original uploaded research-program execution.

## Verdict

ACCEPTED_SCOPED_COMPLETE_SUPERLINEAR_BASELINE, subject to the exact pins in VERDICT.json. The accepted object is the complete canonical b=1 finite-word P application and its composition with the already accepted full-Q inverse. It is not an acceleration result. The linear P and general linear/sub-N-log-N Fourier gates remain OPEN.

For fixed integer d>=1, odd N>=5, n=bit_length(N), Cartesian dyadic input components bounded by 2^(dn), and shared denominator exponent 0<=e<=dn, the full cold Fourier executor returns all N output coordinates. For nonzero input, its full-vector relative 2-norm error is <2^-44; zero input returns exact zero. Standalone P error is <2^-45 and the inherited inverse has relative equation residual <=2^-112. This scope excludes arbitrary target precision, unrestricted descriptions, even lengths, general b, noncanonical embeddings, fixed IEEE hardware, differentiable arithmetic/conditioning upgrades, and historical priority.

The completely charged mathematical resource bound is O_d(N^log2(3)+n^20) word work and O_d(N+n^8) words of storage, on the stated widened O_d(n)-bit word model. Bit work remains O_d(N^log2(3)n^2+n^20), and the available fixed-width output encoding has Theta_d(Nn) bits. This is superlinear, and this literal schedule does not meet the linear acceleration budget.

## Exact review target and source integrity

Accepted author archive: Q30_Complete_Karatsuba_P_Fourier_Baseline_CANDIDATE_v2_2026-10-11.zip (the generic candidate alias has identical bytes), SHA-256 08df04a0e0c85a450ef64b4c6d33196e6931e6e88c0507104818b8cf12e5ab8c.

Accepted executor: cffa7d8aeb0e91b861d6b5f3fefea49f17dc0fa396c62d1aa8dae99b178bc4cb.
Accepted report: a127d5127acb483897c6e2701d10e25630dd92b030f974ee044c93c35e283d4b.

The author superseded archive 60227556e0230009806d7f4b01bfe3f7bdf910e60b81b12080bbe885d77b56a3 solely to enlarge three interval-width constants. The code and both test programs remained byte-identical. The accepted report pays both outward endpoints: theta width <=(4r+6)delta, squared-argument width <=(8r+14)delta, and term width <=(16r+34)delta. The final 64(r+5)^2delta envelope is unchanged. The earlier report hash is not the accepted report.

All 14 source snapshots were independently compared with their stated source files and SHA-256 pins. The frozen accepted source chain includes the paid P packing/error theorem, the actual full-Q residual theorem, direct inverse and outer-chirp reports, and their existing scoped verdicts. Those mathematical premises are not enlarged here. All final manifest entries and archive checksums were verified. No source program under the inert sources directory was loaded or executed. Only the fresh candidate and independently written review code were run.

## Algorithm, signed product, and complete execution

The coefficient orientation agrees with P=FQ and the accepted Q entries. The inverse performs the a-grid prechirp, exact lift to p, reversed alpha solve, ordinary reciprocal-beta solve, -r scaling, and the shifted conjugate ell_(j+1) final down-rounding. In particular, the shifted index and conversion denominator are correct.

P forms its phase/chirp arrays once per target precision and derives B and the shared kernel t by the accepted rounded formulas. The expression 2 Re(phase_j)+2 chat is precisely phase_j+conjugate(phase_j)+2 chat. The four nonnegative kernel arrays are constructed once and reused across the 16 pairings.

The backend recursively multiplies integer coefficient arrays. It never assembles the N-digit operands as giant Python integers. Induction on the Karatsuba identity proves the ordinary polynomial product exactly, including negative intermediate differences. The four sign/type categories reconstruct the complex product with the correct imaginary-times-imaginary sign. All ordinary coefficients beyond 2N-2 are checked zero, then coefficient k+N is explicitly folded into coefficient k. Direct integer controls independently verify this reconstruction and folding, including lengths crossing padding boundaries and signed/zero cases.

Each nonnegative ordinary product coefficient is below N 2^(2h+Dn+5)<2^ell, so there are no carries across digit positions. There is no omitted carry-propagation routine to pay: the original output coefficients already are legal radix digits. Signed reconstruction occurs after those nonnegative products and is exact. Recursion sums and differences are polynomial coefficients, rather than prematurely normalized radix digits, and may be signed.

Summed digits at recursion depth l grow by at most 2^l. A deliberately loose m^3 bound on coefficient magnitudes, where m=2^ceil(log2 N), supplies the reported O_D(n) intermediate bit bound. The final scalar multiplication uses the exact 2h-grid convolution numerator and rounds its 3h-grid product directly to h, with shift 2h. It does not silently discard an intermediate grid.

Depth-first recursion uses O(m) live words: storage at nested active levels is geometric, returned sibling products and slices are explicitly included, and the 16 products run sequentially. Its complete operation recurrence is T(m)=3T(m/2)+O(m). Input parsing, zero scan, conversions, coefficients, shared arrays, signs, folding, address work, allocations/copies, and output coordinates are all included in the resource proof. Optional conversion from per-component dyadics to the shared input grid is a separately paid O_d(N) step.

## Cold seeds, guards, and accuracy

Machin alternating sums use signed first-omitted-term enclosures. Taylor tails are bounded mathematically by factorials rather than by a rounded zero term. The corrected width recurrence in the final report absorbs both outward endpoints and gives the explicit trig-width guarantee. The scale K=4p+80 and r=2K+100 has ample slack. The production setup uses only bounded integer arithmetic, including an explicit integer-square-root search.

The square-root construction uses the correct positive-quadrant square root of c^2-q. Nonnegative radicands can be clipped at zero without excluding the true value. The Hölder square-root width bounds remain safe with the extra r-grid rounding. One can check the denominator bound independently with tighter coarse magnitudes: c,s in [0,1], L<3, U,V<2, hence beta real/imaginary magnitudes are below 3 and 2. Coordinate width <=5 e0^(1/4) therefore gives squared-denominator width below 51 e0^(1/4), inside the report's looser 93 allowance. The reciprocal-width bound 4096 e0^(1/4)=2^-p/256 is consequently safe. Midpoint rounding plus enclosure uncertainty yields complex seed error strictly below one target-grid unit. The executable also checks this with exact squared endpoint distances.

The contracting seed guard and cyclic closure guard follow from the accepted exact root bounds and rounding budget. Their runtime checks are exact integer comparisons. Guard failure is a reported error, with no unpriced or uncertified fallback. A zero kernel coefficient is harmless because the convolution never divides by it. Invalid public length/type/range/exponent inputs are rejected before setup, including zero-valued invalid vectors.

The single shared enclosure construction supplies all required q/c/root precisions within a cold Fourier call. It does not claim equality of differently rounded seed values. Standalone P and inverse calls each pay their own cold setup. There is no free table, supplied spectral data, numerical transcendental, FFT import, or opaque long-integer product.

The actual inverse output meets the enlarged D=2d+42 input description; h>=a makes its P conversion exact. The original P theorem applies to exactly this represented vector and exact cyclic product. Composition gives rho+eta(1+rho)<2^-44 with rho<=2^-112 and eta<2^-45. It is a full-vector 2-norm assertion, with no coordinate-relative promise. A nonzero legal input cannot trigger a zero inverse/P shortcut under the residual theorem. The all-zero input is stated by absolute error only.

## Counter semantics

The independently observed nonzero schedules match:

- P: 7N rounded complex cmul calls.
- Full-Q inverse: 11N-2 rounded complex cmul calls and two rounded complex cdiv calls.
- Full Fourier: 18N-2 rounded complex cmul calls and two rounded complex cdiv calls.
- P and full Fourier backend: 16*3^ceil(log2 N) real integer leaf products.
- Backend recursive calls: 16*(3^(ceil(log2 N)+1)-1)/2.

These are separate counters. scalar_products does not count every real product, seed/setup work, guard arithmetic, division internals, additions, copies, or memory access. For example, the Python cmul instrumentation itself recomputes some component products; that is a constant-factor cost already inside the word-work proof. Instrumented maximum bit lengths are observations at the specified sites, not a census of all temporary integers. The complete theoretical bound, rather than those maxima, covers all omitted work. No runtime benchmark or primitive-operation optimality claim follows from these counters.

## Independent controls

The independent reference uses pi/4=atan(1/2)+atan(1/3), not the candidate Machin identity, with separate outward integer intervals and Taylor tail certification. Direct F matrix summation and original-entry Q references do not reuse candidate chirps, cyclic solves, or convolution. Candidate q/c/alpha/reciprocal seeds are independently enclosed at six parameter pairs.

INDEPENDENT_RESULTS.json records 18 full input cases across (d,N)=(1,5),(1,7),(2,9),(3,11),(1,17),(1,33), each checking P, inverse residual, and Fourier: 54 full nonzero output calls. Cases include minimum nonzero dyadics, maximum alternating values and random mixed signs. Every returned coordinate and exact squared error inequality is checked. There are also 44 independently reconstructed cyclic products, 50 malformed-input/guard controls, and 66 independently instrumented counter cases including 12 zero calls.

INDEPENDENT_EXTRA.json adds four Fourier description/exponent-boundary cases, three deliberate output countercontrols (truncation, corrupted final coordinate, and zero fallback on nonzero input), and 5,130 exact parameter-budget/word-width checks. These controls are corroboration of the uniform proof, not a substitute for it or a runtime scaling experiment.

The sealed candidate's own main and supplement suites were independently rerun from a cold archive extraction. They cover 210 main P/Q/F calls (180 nonzero certificates, 30 zeros), three further complete Fourier outputs at N=65,129,257, 80 product cases, 39 negative controls, 2,570 parameter cases, 7,839 rounding controls, and 726 square-root controls. Final rerun status and code-identity linkage are in COLD_REPRODUCTION.json. The proof-only archive correction is separately identified above.

## Root-writer guidance

Use an append-only dated bounded-baseline update on the existing Q30 rows, and existing NF-10/FUS-01 cross-references. Preserve all prior accepted history and restrictions. Re-read live stable IDs and old values before any authorized change; the row numbers in the candidate are locators, not authority to overwrite.

Suggested wording: "Independent review accepts a complete canonical b=1 finite-word P/Fourier baseline with explicit 16-product Karatsuba convolution, certified shared cold coefficients, and all outputs. It has Fourier relative 2-norm error <2^-44 on the stated fixed-d dyadic input class, with exact zero handling, O_d(N^log2(3)+n^20) cold word work and O_d(N+n^8) storage. This completes the previously unspecified backend only at superlinear cost. The linear P/general Fourier acceleration gate remains OPEN."

Do not create a new discovery row, increment theorem/discovery counts, mark the acceleration gate closed, or promote general-b, embedding, fixed-hardware, asymptotic-speed or priority claims. This review makes no Sheet, Library, GitHub or other external mutation.
