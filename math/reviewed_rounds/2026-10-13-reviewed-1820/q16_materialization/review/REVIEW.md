# Independent review: exact centered source materialization

13 October 2026 UTC

## Verdict

**ACCEPT the mathematical representation/applicability lemma and its O_d(N) paid growing-word bound, on the explicitly declared bounded-field and trusted source-level model. No required repair or in-domain counterexample was found.**

This verdict applies to the frozen MATERIALIZATION_LEMMA.md and its relevant interface claims in GAP_LEDGER.md. It does not accept a production constructor, general parser, implicit-source implementation, all-length dispatcher, full Fourier executable, or host interpreter. The ledger correctly leaves those executable obligations open. The recovered theorem's historical mathematical acceptance is inherited with its stated premises, not newly replayed here.

## 1. Frozen evidence and review method

The reviewed archive is Q16_Exact_Input_Interface_Gap_Ledger_2026-10-13.zip, 120,127 bytes, SHA-256:

    1248773169d32ed606b2750843d6cf9992840dde2eb86ca974ed8637003d330e

Its manifest is SHA-256 c695a4202d61ed76ec8f64ab1c486a42292492a89f279e86ef9b5b36b6c9bb4d. Independently checked: archive CRC, unique 25-member inventory, exact manifest inventory, all 24 manifested payload sizes/hashes, and byte equality of the reviewed extracted payloads to the frozen archive. SEAL.json is a local receipt outside this 25-member archive; the authoritative archive hash was independently recomputed.

The two principal reviewed files are:

- MATERIALIZATION_LEMMA.md: 9,379 bytes; SHA-256 e3def2bdb1f175f7927226dfa6be0e617bf276525e1f58c1d6adc974143422ed.
- GAP_LEDGER.md: 12,677 bytes; SHA-256 08ee394c5f2f50776ae16551459a78938fe4c6f9b8f31b9d17174ae8bff8c80c.

All 16 EVIDENCE.json source copies were independently checked against their recorded hashes/sizes and their available original local bytes. The recorded three inherited archive hashes/sizes were also independently checked. Crucially, the recovered theorem, buckets.py, pipeline.py and fair_tape.py copies are byte-equal to their members in the frozen sparse bridge candidate, SHA-256 55c074877d47b7c0f8d0d6f5f1394005b650ff29a428b9180e6de34d488d5f6f. The sparse independent acceptance report is byte-equal to its member in the acceptance archive, SHA-256 4ebd428764c96ec2c233db76604fc47b3705fa3489850ab0b2a468c7a3f17333.

Reviewed evidence was read as inert text. No candidate control program, historical reviewer, scientific source, FFT, sparse pipeline, or production constructor was imported or executed. Only the newly authored independent_checks.py and ordinary file/hash utilities were executed. No scientific source, accepted record, repository, Sheet, publication, or external state was changed.

## 2. Source-bound outer theorem

RECOVERED_EDITION.md is 33,082 bytes, SHA-256 0a7733e2ac1d1c32cf70609ba0db151a13a73765107907aec44045daaf0a58f5. Sections 1–2 explicitly specify:

- Fixed 0 < alpha < beta < 1/2, rational beta, c > 0, integer d >= 1 and integer D > alpha+4.
- All N >= 1, with M=2^ceil(log2(4N)), m=log2 M, and 4N <= M < 8N.
- Common-exponent finite inputs x_j=(a_j+i b_j)/2^e, |a_j|,|b_j| <= 2^(dm), 0 <= e <= dm, represented in declared bounded binary fields.
- The negative-sign unitary DFT, simultaneous weak coordinate error C N^(-alpha)||x||_2 with probability at least 1-N^(-c), and O(N) growing-word work/storage on every valid-domain tape.

Section 2 already supplies max normalization, exact power-of-two scaling and the centered embedding. It explicitly stores only N entries and describes an implicit random-access source. The proposed M-tuple is therefore an equivalent mathematical representation with separately paid O(N) acquisition/storage, not a claim that those literal source-storage instructions were already implemented unchanged.

The edition-QA report, SHA-256 579f7f4515c2e744a12821c217bdb696801b76b5a3eb0ce8db156ba8190de34d, accepts faithful preservation of the historically accepted theorem and its inherited E(beta)/P05 premises. It expressly does not re-audit all those premises or replay missing historical programs. The present review preserves that distinction.

## 3. Exact normalization, zero branch and scale

Let A=max_j(|a_j|,|b_j|). Global validation and the max scan must reach all 2N fields before the zero conclusion or tape acquisition. The lemma says this explicitly, including the last imaginary field. If A=0, writing N zeros is exact and costs O(N); the source recovery theorem with R>1/2 is not invoked.

For A>=1, set k0=(A-1).bit_length(). This is exactly the least nonnegative k with A<=2^k. Consequently:

    0<=k0<=dm,
    1/2 < A/2^k0 <= 1,
    -dm<=lambda_exp=k0-e<=dm.

At A=1, k0=0 and the maximum normalized Cartesian magnitude is 1. At A=2^q, k0=q, again giving maximum 1. The common erroneous choice A.bit_length() would instead give 1/2 at exact powers; it is not the choice in this lemma.

Every normalized field is exactly its original numerator divided by 2^k0. The positive scale lambda=2^(k0-e), kept symbolically by its signed exponent, reconstructs x exactly. Negative lambda exponents cause no integer-allocation or rounding requirement. There is no norm oracle, producer approximation, projected-signal lower bound, requantization, or extra error term.

The norm bounds follow directly from one Cartesian field with magnitude >1/2 and at most 2N Cartesian fields bounded by 1:

    1/2 < ||v||_2 = ||x||_2/lambda <= sqrt(2N).

The guarantee is Cartesian magnitude <=1, not complex magnitude <=1. The corresponding complex bound is sqrt(2), exactly as used by the source and outer proof.

## 4. Centering and literal source compatibility

For a0=floor((N-1)/2), the map j -> (j-a0) mod M is injective because distinct j differ by less than M. Its inverse at residue r is j=(r+a0) mod M; precisely j<N identifies an occupied slot. Thus the construction places each original pair exactly once, inserts zeros elsewhere and preserves the squared Euclidean norm.

The occupied signed lifts obey |j-a0|<=N/2<=M/8, including the right endpoint for even N. This is the centered-support condition in P05 S6 (the pinned P05 source is SHA-256 02ec40df49f0585c57f98d3af7cbb9867216773f98a2998db9d51237fd69b787). The shift direction agrees with the negative-sign outer phase in the recovered interpolation identity.

The actual source contract is literal:

- buckets.py lines 19–29 define the frozen DyadicSource dataclass and cell schema ((real_numerator, real_exponent), (imag_numerator, imag_exponent)).
- buckets.py lines 168–173 require exact DyadicSource identity, exact tuple identity for values, and length M.
- Its lines 181–199 require each reached complex/dyadic cell to be an exact tuple of length two, with exact integer fields, exponent in [0,F] and numerator magnitude <=2^exponent.
- pipeline.py lines 111–116 repeat the exact source/header requirement; lines 188–197 leave unsampled validity and deep immutability to the caller.

The lemma supplies F=k0, all exponents exactly k0 including zero cells, and |numerator|<=2^k0. This establishes a bound on the numeric exponent value, not merely the encoding width of F. Numerator magnitudes need at most k0+1 bits, plus a constant sign allowance. F=0 and zero cells with exponent zero are legal.

New immutable tuples at every container level, containing exact immutable integer fields, isolate the source from later changes to input lists. Sharing immutable integer values would also be harmless; no mutable alias is needed. The wrapper must use the same actual imported pinned class object consumed by the source reader. A lookalike class or callback is insufficient. Reflective mutation, host corruption and concurrent mutation during acquisition are outside the declared fixed-input/trusted-source model, not promised defenses.

## 5. Resource accounting: words versus bits

The declared word width is a sufficiently large fixed parameter-dependent multiple of log2(N+2). Each valid Cartesian field, exponent, pointer/index and relevant metadata item occupies O_d(1) such words. The algorithm can therefore pay a fixed number of bounded-word operations per field for validation, absolute values, maxima and copying.

The single metadata computation of m and k0 costs O_d(m) elementary scan steps, or any fixed conservative polynomial in m using explicit bit routines. For every fixed exponent q, m^q=O_q(N) because m=Theta(log(N+2)); this is a one-time metadata charge, not a poly(m) routine repeated on all coordinates.

For each of M residues, r+a0<2M. The modulo operation needs one comparison and at most one subtraction. A source-cell construction uses only a fixed number of bounded fields and tuple references. The ledger must charge:

1. All raw field reads, range checks, max comparisons and retained copies.
2. M temporary slots and the complete centered/zero-filled source cells.
3. Every inner tuple and the final M-reference outer tuple copy.
4. Return metadata and any coexisting retained input/temporary/output copies.

There are only a fixed number of whole-array passes/copies. Thus both total word work and cumulative finite-copy storage are O_d(N+M)=O_d(N), as 4N<=M<8N. Distinct zero cells can be allocated without affecting the bound; neither interning nor aliasing is required.

This is not O(N) bit work. The represented numerical data and addresses may have Theta_d(N log(N+2)) total bits. A conventional bit simulation of the per-field bounded-word scan/copy pays those widths; whatever fixed polynomial bit overhead is chosen for the one-time metadata is separate. No unbounded-precision arithmetic, transcendental call or arbitrary-length textual parse is charged as one word operation. The argument does not certify Python allocation limits or timing.

The current sparse theorem starts with the represented source already supplied. Its source storage/construction is excluded from its sublinear auxiliary bound. Adding this paid O(N) constructor at the outer level is valid; charging it to O(M^(1/2+beta)poly(m)) would not be valid. GAP_LEDGER.md and the lemma state this boundary correctly.

## 6. E(beta) and precision compatibility

The pinned independent sparse acceptance, SHA-256 2baf544af1fe8670728ea0ed300b7dcea6069ca5fc3c26823df3262f26b24e97, requires a fixed globally valid deeply immutable normalized source, R>1/2, numeric F=O_d(m), fixed rational beta, the exact source sparse route, and an independent uniform tape. The construction establishes the source-side premises for every nonzero outer-domain x. It does not establish entropy, and it does not bypass branch guards.

The required sparse guards remain B|M, B>=4, T=M/B>=4, B>=4096k and W<M, with the pinned exact parameter definitions. The extra outer guards beta*m>=2 and t<M are still needed for transfer. Small legal raw inputs need not be sparse eligible. In particular, source construction is not a dispatcher or a dense fallback.

Under these premises, the accepted output has:

    Pr[||zhat-U_M v||_infinity <= 4 M^(-beta) R] >= 1-M^(-3),
    grid exponent P=16m+16,
    support <=2qT,
    every-tape Cartesian magnitude <3M^2.

The probability is stronger than the outer interface's sufficient 1-1/M, and the target, sign, unitary normalization, grid and every-tape magnitude/support caps are the same ones used by recovered Sections 4–6. In particular |numerator|<2^(P+2m+2) feeds its explicit accumulator width. There is no missing input-precision premise created by full materialization: the source has exact values with F<=dm, not an approximation on the output P grid.

These statements supply the named mathematical frontend interface on the normalized domain. They do not directly produce U_N x. P05 interpolation, active coefficient preparation/scatter, finite sums, final rounding, scale-back, exact all-length fallback and J independent complete-call medians remain separate obligations for an integrated executable. This review does not newly certify their implementations.

## 7. Fresh exact controls

New reviewer code: independent_checks.py, SHA-256 11ee9d3240b4efcd688c437e2a02c16a8ff8b9d54556d8ba3c5fed2a2e67b3aa. CONTROL_RESULTS.json and CONTROL_LOG.txt record PASS.

There were 36,408 exact finite input-vector/exponent cases, including exhaustive fields from {-2,-1,0,1,2} for N=1,2,3 at both endpoint exponents, plus 3,858 boundary cases at lengths through 1025. Six all-zero cases were exercised. Nonzero cases compare an independent forward scatter using repeated-doubling normalization against the stated inverse-gather and bit-length formulas. Controls check every represented cell, strict squared-norm inequalities, support endpoints, mutation isolation, both signs, last-imaginary-only nonzero inputs, exact power boundaries and rational scale reconstruction.

Metadata-only controls cover m up to 4096 and d in {1,3,7}, without attempting enormous vectors. Exact rational symbolic guards at beta=1/4 check the m=45 failure / m=46 eligibility boundary and larger values. They do not execute sparse recovery. All 11,660,192 recorded assertions passed, including byte checks. The assertion count is bookkeeping, not a probability experiment or a substitute for the universal proof above.

The reviewer model does not implement a production parser or instantiate the actual DyadicSource class. Those claims were intentionally not tested or accepted.

## 8. Required scope of the next gate

No repair is required to the present mathematical lemma. For an executable acceptance, the next artifact must still pin its exact input grammar or built-in finite-record domain, handle all validation and zero cases, use the exact consumed DyadicSource class, freeze/copy every relevant container, disclose its all-size finite-word simulation, and include its complete scan/copy/output ledger. Tests of invalid bounded fields, exact type rejection, late invalid fields and post-return input mutation belong to that future source-level review.

Acceptance of that constructor would close only the exact input representation gate. It would not close the remaining integrated all-length executable work or convert the weak-coordinate theorem into exact Fourier evaluation, relative-l2 recovery, O(N)-bit complexity or a practical performance claim.
