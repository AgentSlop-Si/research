# Independent delta review of the Q16 exact centered source constructor v2

13 October 2026 UTC, after the 18:20 publication cutoff. This is a separate later checkpoint.

## Verdict

**ACCEPT v2 as the exact finite-record, centered literal-source constructor in its declared fixed-d growing-word source model. The two required v1 repairs are closed. No additional required repair or counterexample was found.**

This acceptance covers the constructor's specified built-in input validation and rejection boundary, complete scalar acquisition, separate exact-zero branch, max normalization, symbolic scale, centered immutable source, numeric exponent-value bound and paid source-model work/storage. It is conditional on the unchanged trusted pinned dependency and stable-acquisition premises, with sufficiently large finite resources.

The acceptance is source-level. Actual execution with the pinned historical DyadicSource and its consumers remains unperformed. No complete Fourier transform, sparse dispatch, dense fallback, outer interpolation/accumulation or amplification executable is accepted by this delta review. The source constructor is one closed input gate.

The reviewed v2 archive is Q16_Exact_Centered_Source_Constructor_Candidate_v2_2026-10-13.zip, 530,400 bytes, SHA-256 5efa51f2293e57550458c1ededa93e5dd437f676bb3be23941d8b36c0bdcb181. The exact v2 constructor hash is 8334e657dd0048bdb91459e5f6e126080c7513d341ef3d17665b05422a8bbada.

The v1 candidate, hash a837bf0dfc376a6914e6fa3e75d10323766be41202a30e240eb85ccb2e446ae9, remains REPAIR. This acceptance applies only to the newly pinned v2 bytes and does not relabel the v1 record. The complete earlier audit is preserved in v2's evidence/V1_REPAIR_REVIEW.zip, hash 3d21101d48a0a43d9981e64dfab7652cf0346a0e891186f53927417605fbb1a6.

## Exact production delta

Byte comparison establishes that the entire source change consists of these two substitutions, with no added or removed source lines:

- Line 102: type(values) not in (tuple, list) becomes type(values) is not tuple and type(values) is not list.
- Line 138: type(pair) not in (tuple, list) becomes type(pair) is not tuple and type(pair) is not list.

The independently computed replacement of precisely those two old strings reproduces the complete v2 constructor bytes, not merely an AST equivalent. The old source and archive are preserved unchanged. The input contract, resource ledger, original numerical/mutation/metadata/ledger test programs, original numerical result records and all original scientific evidence remain byte-identical. The proof-ledger changes only identify v2 and correctly describe the repaired identity boundary. The complete packet delta is listed in DELTA_INVENTORY.json.

V1 used equality-based membership, allowing a foreign class's metaclass equality to claim equality with tuple. The repaired predicates use only identity. Their boolean operands are the ordinary boolean results of is not; the and operation does not truth-convert the supplied object or a metaclass-generated equality result. Thus no equality, inequality, hash or supplied sequence protocol can run at either predicate.

The outer predicate precedes len(values). The cell predicate precedes len(pair), indexing or scalar processing of that cell. A foreign object or list/tuple subclass must therefore be rejected at its appropriate boundary even if its metaclass returns true, false, raises, or produces an object with hostile truth conversion. The minimal v1 witnesses no longer pass.

## Broader boundary and callback audit

The production source now contains exactly eight type comparisons, all identity-only:

1. The outer type against tuple and list.
2. The cell type against tuple and list.
3. d against int.
4. exponent against int.
5. real against int.
6. imag against int.

The d guard short-circuits before d<1 for any foreign type. The exponent guard precedes its interval comparison. Real and imaginary type guards precede their signed magnitude comparisons, absolute-value arithmetic and maximum updates. Booleans and all integer subclasses therefore remain rejected. A supplied __class__ or instance attribute hook cannot change the result of the built-in one-argument type operation.

After the outer/cell guards, length and indexing operate only on genuine exact built-in containers. All numerical comparisons and arithmetic then use exact built-in integers. The API takes values, exponent and d only; its private practical flag is a literal boolean supplied by each fixed wrapper. The source has no input factory, callback, arbitrary iterator, structural isinstance/issubclass check, conversion through int/float/bool, dynamic eval/import, diagnostic repr/str, or supplied-object attribute lookup. The fixed error codes and prefix/index/component diagnostics contain no user-supplied object requiring representation.

The remaining method calls concern the known internal meter, fixed standard-library operations, or bit_length on established exact integers. There is no equality-based type membership remaining. No second callback bypass was found. As before, overriding globals/built-ins, replacing import resolution, reflective mutation of returned records, concurrent input mutation, memory corruption and resource exhaustion are outside the declared trusted-program model; they are not assumed away to excuse an ordinary hostile input object.

## Validation, zero and numerical claims retained

On valid records, the two predicates produce the same branch decisions as intended in v1. All downstream numerical statements are byte-identical to the source already reviewed. The prior proof and resource audit therefore transfer without an unreviewed numerical change.

The full N-cell scan validates both exact integer fields and inclusive bounds before zero classification or source creation. A late imaginary rejection reports validated_fields=2j+1; a foreign cell after j complete cells reports 2j. No early successful return or break occurs in the scan. An all-zero valid input returns N exact complex dyadic zeros before importing buckets. It receives no false nonzero normalization promise.

For nonzero A=max_j(|a_j|,|b_j|), the exact formula k0=(A-1).bit_length() remains the least k with A<=2^k. It handles A=1 and all exact powers without weakening the strict lower bound. Every normalized Cartesian magnitude is <=1, at least one exceeds 1/2, and therefore 1/2<||v||_2<=sqrt(2N). Complex amplitude may be sqrt(2); no stronger complex bound is assumed.

Every dyadic exponent, including padding zeros, equals F=k0<=dm. This is a numeric exponent-value bound. The signed scale exponent k0-exponent reconstructs the raw input exactly without rounding. The centered residue is (j-floor((N-1)/2)) mod M; the inverse gather, injectivity, one-wrap bound and even/odd support endpoints are unchanged. The represented support has |signed lift|<=N/2<=M/8. Fresh tuples at all numerical container levels preserve deep immutability under the stated ordinary model, with no mutable input alias retained.

## Paid cost and all-size versus practical scope

The repaired predicates add only constant elementary comparison work already covered by the conservative macro budget. Event counts, temporary/final copy counts, retained storage and receipt formulas are unchanged. For center=floor((N-1)/2) and H=(dm+m+16)^2:

    U_nonzero = 15N + 18M + center + 589 + H
    U_zero = 29N + 584 + H
    U <= [750 + 8(d+9)^2] N
    word_operations_upper = 1024 U

The bound uses 4N<=M<8N, m^2<=8N and H<=8(d+9)^2N. Complete scalar acquisition, maximum scanning, retained pairs, M temporary slots, every dyadic/complex tuple and the final M-reference freeze are paid. Source storage is not reassigned to the sparse routine's sublinear auxiliary budget.

For fixed d, the constructor has O_d(N) growing-word work and cumulative storage. The stated conservative local random-access bit simulation remains O_d(Nm^2), and cumulative represented storage remains O_d(Nm) bits. The meter is an elementary source-model envelope, not Python instruction, allocator or wall-clock certification.

The unrestricted all-size theorem concerns every finite valid N for fixed d with adequate finite resources. The separate deployment entry caps N at 65,536 and d at 8, giving m<=18, M<=262,144 and dm<=144. These finite deployment limits are not practical speed or memory guarantees and do not constitute proof of the all-size theorem. This reviewer did not execute the candidate at the maximum practical case.

## Production class binding and execution evidence

The direct production dependency remains from buckets import DyadicSource followed by DyadicSource(frozen, k0). The pinned buckets class is the previously inspected frozen two-field dataclass, hash df3937a632217a8a1342545b803169ff8da062117b3837796386509b64f650d1. The pinned consumer and pipeline require exact class identity. Under the fixed trusted dependency premise, the constructor binds the same class, and its data meet the literal schema and exponent/amplitude checks.

This is not runtime authentication of an arbitrary installed buckets package. Nor does a structurally identical fixture establish actual consumer identity. The author's main dynamic controls use a freshly authored fixture substituted for buckets, exactly as disclosed. Its new hostile-boundary suite runs only the new constructor on rejection and zero paths, requiring no historical scientific dependency. Its recorded results are 296 hostile rejections, 24 genuine built-in combinations, 675 assertions and zero observed callbacks. The source of that suite was independently inspected, including expected diagnostic checks and hooks for metaclass equality, truth conversion, sequence operations, arithmetic, representation and conversion.

Those producer results were not independently rerun here. The independent review executed neither candidate programs nor producer tests, historical scientific programs, prior reviewer programs or extracted candidate code. It used source/AST data, file/hash utilities and one newly authored checker. No candidate AST interpreter was used.

## Fresh independent checks and provenance

The new checker reports 3,746 passed assertions. Its independent grammar/language model covers 372 rejection cases and 672 genuine built-in acceptance cases with zero supplied callbacks, plus 1,548 metadata-only formula cases through m=8192. This is explicitly a fresh review model, not an execution of the constructor under review.

The hostile classes cover four metaclass equality outcomes: true, false, raising and a hostile truth-conversion object. They derive from object, list, tuple and int and provide traps including __getattribute__, sequence methods, arithmetic, conversions and representation. They appear at outer, cell, d, exponent and both Cartesian positions. Cell and scalar cases include genuine zero prefixes and exact prefix/component expectations. Separate controls cover boolean/noninteger fields and practical-cap rejection. All genuine list/tuple combinations, both exponent endpoints, zero/small/inclusive-maximum numerators and both d endpoints are included in the model.

A separate positive adversary control verifies that the old membership predicate actually invokes metaclass equality and admits its witness, while the new identity predicate rejects the same witness with no hook call. This prevents an inactive test adversary from producing a vacuous pass. Full source inspection connects the independently checked language behavior to the two exact production predicates and guards their placement before user-controlled protocols.

Archive checks establish the exact v2 hash, CRC, 43 unique members, all 42 manifested payloads and all 11 provenance records. The nested v1 archive and independent REPAIR archive match their separately known pins. The copied earlier review matches its sealed report. The complete original scientific evidence remains byte-identical, preserving the sparse-success and materialization prerequisites reviewed previously. No acceptance is inferred solely from a filename or author-provided status label.

## Remaining gates and publication handling

The exact-source constructor gate is closed at the declared source-model level for v2. Its unchanged applicable source promises are global validity, immutable normalized centered representation, R>1/2, Cartesian magnitudes <=1 and numeric F=O_d(m).

The accepted sparse success theorem additionally requires fixed rational beta in (0,1/2), exact sparse route guards B|M, B>=4, T>=4, B>=4096k and W<M, the pinned finite-arithmetic contracts, and an independent uniform tape. The outer theorem still uses strict 0<alpha<beta<1/2 and its separate transfer conditions. lambda remains a normalization scale. No alpha endpoint, exact DFT, relative-l2 or practical FFT performance claim changes.

Still open for a complete executable claim: actual source-pinned integrated conformance; exact all-length dispatch and certified dense fallback; active interpolation coefficient generation/scatter; finite accumulators, final rounding and scale-back; fresh J-call amplification; and complete end-to-end input/output accounting. Physical entropy, general text parsing, host certification and practical performance remain separate claims.

This acceptance was produced after the 18:20 checkpoint cutoff. It belongs in a later independent checkpoint and must not be retroactively represented as accepted by that earlier cutoff. The v1 REPAIR record is retained. No candidate source, accepted dependency, Sheet, repository, publication or external state was modified by this review.
