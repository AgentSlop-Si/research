# Independent acceptance: exact NTT output extension at 512 and 1024

Date: 2026-10-13. Decision: **ACCEPT_BOUNDED_512_1024_EXACT_OUTPUT_EXTENSION**.

No blocking repair was found within the declared scope. Accept the source-reviewed bounded fresh radix-2 reference and the complete frozen expected-output artifact for the 32 vectors at n=512 and n=1024. This decision is independent reconstruction and source review, not execution of the candidate's programs.

## 1. Result and exact boundary

All **32 vectors, 24,576 coordinates, and 98,304 serialized bytes** independently agree with the required positive-exponent, unnormalized, natural-order transform over F_998244353. The complete output SHA-256 is:

`7ad3b732c3be717408ca2634a86a1518530225bd6428de043410655bc527863f`.

The accepted candidate archive is exactly:

`Paid_NTT_512_1024_Exact_Output_Extension_Candidate_2026-10-13.zip`

SHA-256 `c36757feea1a39a520ed42a8251bf81618fea08a00a870f77b5c4e44505592fb`.

The earlier accepted 128 vectors and 8,160 coordinates at n=2 through 256 are byte-identical to their sealed prior acceptance. That acceptance is preserved without rerunning its programs. The combined accepted availability is therefore **160/288 vectors and 32,736 complete coordinates**, stored as the unchanged 32,640-byte prior artifact plus this 98,304-byte extension, totaling 130,944 bytes.

The remaining **128 frozen vectors at n=2048,4096,8192,16384,32768,65536,131072,262144 have no accepted expected outputs in this work**. Reading and checking their input bytes is not computing their transforms.

This acceptance does not establish inherited-schedule correctness, adapter correctness, any binary/build acceptance, full-corpus readiness, production readiness, timing, benchmark readiness, speedup, or novelty. It grants no extra execution scope. The original protocol and historical sources are unchanged.

## 2. Identity and preservation audit

The independent checker established all of the following before evaluating the extension:

- The requested candidate ZIP SHA-256 matches; all 61 members are unique, have safe relative paths, and pass ZIP CRC validation.
- The candidate's 60-entry FILES_SHA256 manifest covers every member other than itself exactly. Every recorded length and hash matches.
- All 35 immutable-input bindings, all 16 protocol-manifest bindings, all 11 old-candidate-manifest bindings, and all six preexecution-seal bindings match. These groups total 128 binding checks; this is not a claim of 128 distinct files.
- The declaration binds its input manifest and previous acceptance receipt. The extension manifest binds the precise generator source, declaration and corpus.
- The preserved receipt binds the old candidate manifest, protocol manifest, old oracle and test-source bytes, historical C++, corpus, accepted output bytes, and previous independent review report.
- The design-only v2 acceptance receipt still binds the same contract, protocol and manifest. The current accepted protocol manifest hash remains `def2f742943cc2a50b15c785cf1a14b4605f9a93a6d48e3ed9e029688be676ff`.
- The 33,554,304-byte frozen input corpus hash remains `f07e9e1c550420ae431ee64a60e73449b1dcffce105bf452653972dbb7a7bba7`. All 288 input records have the required increasing lengths, original 16-case order, contiguous extents, full per-vector hashes, complete little-endian decoding and canonical ranges. No input generator was run.
- Every one of the preserved 128 output records has its exact extent, complete hash and canonical range checked. Their output hash remains `1401cb324cf991f4eb69db4e962f78f3d2881b5bb9116d8fd629a08f04134091`.

A separate read-only provenance recheck after the scientific run compared all 61 candidate archive members with the supplied candidate workspace; all 35 input snapshots with their claimed originals; and both historical source snapshots with their original source paths. All matched.

The prior acceptance ZIP independently matches SHA-256 `8fb4dba8f90387ac400bde1c2b108e0dc358c8c9fbe156e202a27a18a2d89bd7`. All its 41 members and its manifest were verified. Of the candidate's 35 input snapshots, 34 rebound byte-for-byte to that sealed prior ZIP. The remaining queue snapshot matched its separate original workspace file. Thus preservation was checked against actual earlier bytes, not merely the candidate's claims about them.

The candidate ZIP was hashed again after the independent scientific run. No input, candidate, old accepted artifact, historical source, Sheet or GitHub item was changed.

## 3. Exact arithmetic, domain and roots

The field modulus is p=998244353, and the generator is g=3. Fresh trial division checks every odd possible divisor through a bound exceeding floor(sqrt(p)), with factor 2 separately excluded. Together with

    p - 1 = 2^23 * 7 * 17,

and the three nonunity values

    3^((p-1)/2)  mod p = 998244352,
    3^((p-1)/7)  mod p = 779057549,
    3^((p-1)/17) mod p = 337827833,

this proves the stated primality and primitive-generator order.

For n in {512,1024}, omega_n=3^((p-1)/n) has exact order n. The roots are 166035806 and 258648936, respectively. Both quarter roots are 911660635, whose square is -1 modulo p. The fresh scalar checks match the original protocol certificate.

The exact required map is

    y[k] = sum(x[j] * omega_n^(j*k), j=0,...,n-1) mod p.

The sign is positive; there is no forward scale factor; k is in natural order. Every coefficient is an ordinary integer in [0,p-1], and there are exactly n coefficients. The wire format is exactly four little-endian bytes per canonical value, no header, increasing n then original case order. The finite extension includes only n=512 and 1024. The fresh reference guards all execution above n=1024 even though the inherited mathematical public domain reaches 2^23.

Fresh controls explicitly distinguish the pinned g-derived root from other primitive roots, including the opposite root. Exact order alone would not determine the required sign or frequency labeling.

## 4. Source review of the candidate

All four current Python source files were read as text, and their syntax trees were inspected without compilation, evaluation or import. The full source inventory records every import and called function. No old oracle, historical generator, old reviewer, C++ schedule, benchmark program or binary was executed.

### fresh_forward.py

- Lines 13-20 pin integer p and g, reject booleans and other non-integer lengths, exclude n=1 and nonpowers of two, and impose the execution cap before work allocation.
- Lines 23-30 freshly form the positive root and check exact order and the quarter-root identity.
- Lines 33-39 require exactly n ordinary canonical integers in a literal list/tuple and copy them to an immutable tuple. Malformed values are rejected, not normalized.
- Lines 49-59 allocate a fresh work array and compute every bit-reversed destination through an explicit binary-digit loop. No inherited permutation table is read.
- Lines 60-72 recompute the root for each width and perform the standard two-child polynomial recurrence with exact Python integers. Each written value is reduced modulo p.
- Lines 76-84 implement strict canonical LE32 encode/decode with exact wire extent and immutable bytes input.

For the correctness argument, write A(z)=E(z^2)+z O(z^2). If w has order m and U,V are the natural-order child transforms, then the two parent values are U[k]+w^k V[k] and U[k]-w^k V[k]. The latter follows from w^(m/2)=-1. Repeated even/odd decomposition has bit-reversed leaf order; the initial copy supplies exactly that order. The width loop combines correct child blocks with w=3^((p-1)/m) and factor w^k, so induction from the single-coefficient internal leaves establishes every final natural-order value. The internal leaf does not extend the public API to n=1.

Input immutability follows structurally from the tuple copy and separate work allocation. Guarded canonical residues and Python arbitrary-precision arithmetic remove a fixed-word overflow premise. This reference has O(n log n) fixed-field arithmetic and index-bit work, and O(n) transform storage. This is a reference complexity statement, not an inherited-schedule improvement claim.

### generate_packet.py and verify_packet.py

The producer imports only the new reference and standard-library modules. It checks the frozen input bindings, validates the new reference against the 128 stored accepted small outputs, and generates only corpus records 128 through 159. Its source checks complete small coordinates, full wire bytes and unchanged input values. It does not run old sources.

The candidate's separate-method checker imports no producer. Its forward is direct descending-coefficient Horner evaluation at each pinned root power, and its inverse is a separately written negative-root matrix summation with n^-1 scaling. The orthogonality identity proves that inverse and the F_+ squared identity. Its coordinate comparator checks canonical type, range, length and every value, not merely hashes or scalar invariants.

The candidate's recorded 34 producer and 59 checker controls were checked for unique names, recorded rejection, and consistency with the inspected validator and call paths. **They were not rerun against candidate code.** The 76 independent controls below test the fresh review machinery; the candidate's guard behavior is assessed by source inspection. Author-level controls and independent review controls are not conflated.

### run_bounded.py and resource boundary

The launcher permits only its two named fresh drivers. Lines 9-12 install both soft and hard RLIMIT_CPU=180 seconds, RLIMIT_AS=268,435,456 bytes, RLIMIT_FSIZE=67,108,864 bytes, and RLIMIT_CORE=0 before runpy loads a scientific driver. The producer/checker themselves assert the CPU and address-space limits. The launcher does not read or execute an old source. The prescribed two serial original invocations have an aggregate declared CPU ceiling of 360 seconds.

The source seals bind the exact reviewed bytes. The declaration and author logs record preexecution sealing and one successful invocation per driver. As a retrospective reviewer, I independently verify their content, source consistency and all results, but **do not claim to have independently witnessed the original chronology or operating-system invocations**. A hash seal alone cannot prove its creation time. This limitation does not affect the fresh reconstruction of the exact stored outputs, and no timing or measured-resource assertion is inferred from the logs.

## 5. Independent reconstruction and controls

The only independently executed scientific program is the newly authored independent_check.py in this acceptance packet, run once. It imports only Python standard-library modules and loads candidate files solely as bytes/JSON/text from the pinned ZIP.

For each transform it constructs a fresh table T[e]=omega^e for e=0,...,n-1 by multiplication, and computes every row directly:

    reference[k] = sum(x[j] * T[(j*k) mod n], j=0,...,n-1) mod p.

The table identity is immediate by induction; reduction of j*k modulo n is valid because omega has order n. The complete sum uses arbitrary-precision integers and one final reduction per coordinate. This method contains no butterflies, bit-reversal transform, descending coefficient-Horner evaluation, inherited table or candidate transform call.

The direct inverse constructs its own table for omega^-1 and scales by n^-1. Root orthogonality proves exact inversion. The positive transform is also applied independently to each stored output and checked against n*x[-j mod n]. These identities supplement complete direct forward equality; they do not replace it.

Observed independent results:

- 32/32 complete vectors, 24,576/24,576 coordinates, and 98,304/98,304 bytes match. Coordinates were compared before confirming the reconstructed serialized artifact and its hash.
- All 32 vectors pass direct inverse, forward-squared, DC, sum and input-immutability checks.
- All 14 applicable complete zero, constant, impulse and alternating closed forms match.
- Three literal small forward-and-inverse anchors pass, including an asymmetric n=4 example.
- All 24,576 independently introduced canonical single-coordinate mutations are rejected, one per stored coordinate.
- At each extension length, a (+1,-1) mutation leaves the DC coordinate and total output sum unchanged but is rejected by complete comparison.
- 76 distinct independent conceptual negative controls reject wrong sign, another primitive root, forward normalization, bit-reversed order, big-endian decoding, malformed output extent/container/type/range, malformed wire extent/type/range, wrong roots, illegal lengths, wrong fixed constants, bad input shape and noncanonical coefficients.
- The program records 1,219 asserted checks and the detailed per-vector and binding results.

The unchanged prior 128-vector acceptance is inherited through its verified receipt and bytes, not newly re-awarded by these tests. These 32 new vectors remain a finite frozen corpus. General algebraic behavior of the inspected guarded reference is supported by its structural proof, not by a claim of exhaustive testing of all possible length-512/1024 inputs.

## 6. Paid work and exact ledger

The candidate's counts were independently recalculated from the declared lengths and source loops:

- 160 successful producer forward calls: 128 prior-output validation calls plus 32 new output calls.
- 28,688 butterflies for prior small validation; 118,784 for the extension; total 147,472.
- 294,944 explicit bit-reversal bit iterations across those successful calls.
- 20,971,520 coefficient steps each for new candidate Horner forwards and forward-squared checks; 20,971,520 candidate inverse summands.
- 24,576 complete new coordinate comparisons, 98,304 serialized bytes, and 24,576 coordinate mutation tests.

These counts are exact loop-work identities for the newly authored references. They are not retired-instruction counts or measurements of inherited schedules. Root exponentiation, guards, validation scans, comparisons, codecs, copying, all allocations, hashes, corpus loading, report generation, archive preparation and review are separately paid work in the ledger. No oracle, setup, input fixture, validation or output materialization is treated as free.

The independent reviewer likewise performed 20,971,520 dense matrix summands for each of the extension forward, inverse and squared checks, plus its literal anchors, power-table setup, full binding/input audit and all controls. One fresh reviewer process installs the same 180-second CPU, 256-MiB address-space, 64-MiB single-file and zero-core hard caps before evidence loading or scientific evaluation. It completed successfully without a retry or cap expansion. The post-run provenance recheck and artifact sealing are additional paid artifact work, not hidden transform work.

No wall-time, CPU-consumption, throughput, latency or peak-RSS samples were collected by the scientific checker. The caps are safety bounds, not performance results. Corpus and serialized byte sizes are storage floors, not measured RSS; interpreter, objects, metadata, temporary buffers and allocator overhead remain paid.

## 7. Gates that remain open

This review closes only the separate independent acceptance gate for the 32 selected outputs. Preserve the outstanding requirements from the accepted v2 protocol and previous review:

1. Independent complete expected outputs for the remaining 128 frozen larger vectors, under their own bounded authorized work.
2. Explicitly authorized source-bound adapter work and a reviewed source-to-adapter diff; guarded requests, arithmetic, sizes and allocations; schedule-owned paid plans; private paid fixtures and lifetimes; and a full-output sink.
3. Direct enclosing intervals, exact diagnostic/release source and binary identities, correct integer type widths, environment/resource/sanitizer evidence, every schedule's complete all-output preflight, and session pre/postflight checks.
4. Resolution of the missing later historical review-body provenance. Its missing hash remains `32b9e8e7c33b69633e1616188b59e0f9ad643677680bbb5b6175ee5900ddf4d8`; matching C++/CSV bytes does not reconstruct that body.
5. No timing until the separately authorized correctness, resource, source, build and protocol gates are satisfied. Historical CSV entries are not current performance evidence.

No claim is added for cyclic-versus-linear convolution, integer reconstruction, CRT, Bluestein, arbitrary-length support, other fields, asymptotic improvement or historical butterfly defects.

## 8. Reproduction and package contents

Run the fresh scientific reviewer only:

    python -I -B paid_ntt_extension_independent_review_2023/independent_check.py

It reads the bundled inputs/candidate.zip and rewrites only this review's deterministic result JSON files and independently reconstructed output bytes. It never imports or executes code inside that ZIP. Reproduction is new paid work and does not change the one-run statement above. The full candidate archive is bundled to keep this scientific reconstruction self-contained.

check_preservation.py is a separate read-only check against the original task workspace and earlier ZIP. Its recorded receipt is included; rerunning that provenance-only helper requires those original paths to exist. They are not required for the self-contained mathematical reconstruction.

INDEPENDENT_RESULTS.json, PER_VECTOR_RESULTS.json, INDEPENDENT_NEGATIVE_CONTROLS.json, BINDING_CHECKS.json, CORPUS_INPUT_AUDIT.json, SOURCE_INVENTORY.json and WORKSPACE_PRESERVATION_RECHECK.json contain the complete detailed evidence. PREEXECUTION_SEAL.json identifies the fresh checker bytes before invocation. ACCEPTANCE_RECEIPT.json binds this decision, candidate, prior acceptance, independent source, results, report and reconstructed output. FILES_SHA256.json binds the complete acceptance package, and the adjacent ZIP seal identifies the final archive.
