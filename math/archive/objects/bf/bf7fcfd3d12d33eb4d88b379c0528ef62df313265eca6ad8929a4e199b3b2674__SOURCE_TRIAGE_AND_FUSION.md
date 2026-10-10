# Six attachments received 9 October 2026, 19:54 UTC

## Result

All six originals are preserved unchanged. Four are byte-identical to sources already preserved and independently reviewed in the research master. Two archives contain new bytes: divisor-spectrum v13 and HERO17 tensor/fiber/graph union. Their mathematical status differs: divisor-spectrum v13 reuses a covariance bound already proved in the master, while HERO17 proposes broader recognized structured-input exact algorithms. Neither supplies the requested exact, all-output, arbitrary-fresh-input, fully charged sub-N-log-N algorithm.

This is source triage and a fusion map. New mathematical/code audits are separate. No uploaded code was imported, compiled, or executed. Source-recorded test counts and benchmarks have not been rerun or promoted to independent evidence.

## Provenance and integrity

- `originals/` preserves all six exact uploaded archive streams, including duplicate uploads under their new Library identities.
- `library_provenance.json` retains each Library ID, underlying file ID, resolved filename, size, version 0 and returned metadata. Signed download URLs are deliberately omitted.
- `content_inventory.json` records every first-level member's SHA-256, size, extracted path, and matching regular/master-archive content paths.
- `COMPARISON_SCOPE.json` records comparison against all regular master files and recursively inspected unique master ZIP containers: 37 containers, 1,090 member occurrences. The master was read-only throughout.
- `STATIC_VALIDATION.json` records six passing ZIP CRC checks, all 114 embedded hash entries passing, 45 Python files parsed as syntax only, and 15 JSON files parsed as data.
- The six archives contain 121 first-level file occurrences, 114 distinct contents, 33 byte-new occurrences and 31 distinct byte-new contents. These are first-level counts; repeated nested predecessor archive bytes remain preserved and were compared recursively.
- Dates containing 2026-10-10 are original source labels. Receipt/materialization is 2026-10-09 UTC; source labels are not dates of independent validation.

### Archive identities

1. `fft_sparse_defect_green_gate_2026-10-10(1).zip`
   - Library ID: `[private-id]`
   - 569,344 bytes; SHA-256 `f0bcde62ec1a8fff9609a463c79025edc6ac150fd910f55ccc2cfd3cc56d885b`
   - 14 members, no new content. Entire archive matches master `additions/1930_static/source_archives/fft_sparse_defect_green_gate_2026-10-10.zip`.
2. `fft_divisor_spectrum_v13(1).zip`
   - Library ID: `[private-id]`
   - 52,521 bytes; SHA-256 `465d0cf5573539887fdb93376e7dc6fba740512a92ac8121952dafc3492b51fd`
   - 21 members, 16 new member occurrences. Five inherited members include the byte-identical HERO0 composite executor, offset-class v12 core, v11 Bessel reference and unit-step core.
3. `fft_green_research_phase26_2026-10-10(1).zip`
   - Library ID: `[private-id]`
   - 808,017 bytes; SHA-256 `b3b03e9c84728cc4c9e9d258967fd8092f637d32f4a0aa6ecf27e1c6ea9c206e`
   - 17 members, no new content. Entire archive matches both `additions/1930_phase26/source_archives/` and `additions/1930_static/source_archives/` copies.
4. `fft_hero17_tensor_fiber_graph_union_2026-10-10.zip`
   - Library ID: `[private-id]`
   - 36,422 bytes; SHA-256 `67e831c40b1f516abb15dd676a1034291b9f9474497717e2a36af0613ba55a26`
   - 18 members, 17 new member occurrences. `phase_union_general.py` is identical to the predecessor HERO17 archive under `additions/1930_static/source_archives/`; it is not the later independently derived polynomial-cost extension.
5. `fft_hero1_mixedradix_v13_20261010.zip`
   - Library ID: `[private-id]`
   - 57,802 bytes; SHA-256 `f9ccd6749ad214bc8038660cdb41bcc9e92cdba1232f75879c1a94064b3b7090`
   - 27 members, no new content. Entire archive matches master `additions/1930_static/source_archives/fft_hero1_mixedradix_v13_20261010.zip`.
6. `fft_hero0_phase2_composite_green_2026-10-09(1).zip`
   - Library ID: `[private-id]`
   - 45,877 bytes; SHA-256 `41d56b89d6020334cbb7504919dcbece69aeb4ce95726e2d6a6ebf0b995a0555`
   - 24 members, no new content. Entire archive matches master `additions/1916/original_source.zip`.

## New-content claims and audit targets

### HERO17: three recognition branches and graph convolution

Primary source: extracted HERO17 `RESEARCH.md`, with `CHAIN_CHECKPOINT.md` and the named source modules.

1. Balanced coprime CRT tensor rank. For N=AB, gcd(A,B)=1 and A²+B²=O(N), discover a bounded-rank factorization of the raw CRT input matrix, perform direct short transforms, and emit all outputs in O(rN+r(A²+B²)). The source includes arbitrary factor vectors and polynomial phases that separate across CRT. Audit exact indexing, rank discovery, degenerate inputs, balance checks, setup, and rank-dependent inversion costs.
2. Sparse Fourier fibers. For N=QM with Q²=O(N), independently recognize at most r characters in each length-M strided fiber. The claimed charged work is O(rN+Qr²+rQ²+N), with all outputs explicit. This allows maximal ordinary matrix rank while retaining small per-fiber spectral support. Audit bounded BM completeness, the transposed Vandermonde recovery, full verification, small-M handling and field/root contract.
3. Polynomial-phase coverage. At N=Q², the identity P(t+Qu)=P(t)+QuP'(t) mod N gives one mode per fiber for every integer polynomial P. Fixed odd prime powers with odd exponent give at most p modes per fiber; powers of two give one by the parity identity. These are promised input families, not a coverage theorem for arbitrary samples.
4. Support-coset branch. A charged gcd scan finds the maximal support coset; the inherited common-chirp recognizer works on its pullback and an exact modulation/aliasing identity expands every output. Preserve all assumptions and limitations of the old recognizer.
5. Graph convolution. Equal character labels create edges contributing M c1 c2 eta^(-h carry) to output partial-Fourier states. The claimed work is O((r1+r2)N+(r1²+r2²)Q+E+N+MS), with E≤r1r2Q². Exact O(N) reconstruction needs an explicitly checked S≤CQ. Audit carry sign, cancellations, repeated active-state bookkeeping, field compatibility and rejection before expensive reconstruction. The adversarial S=Q^(3/2) family is a rejection example for this method, not a universal convolution lower bound.

The arithmetic theorem assumes a supplied certified prime field and primitive Nth root; polynomially bounded field size and modular-operation assumptions matter for word-RAM interpretation. Complex identities do not supply stable floating recognition. Root-finding, primality, precision and output-bit costs cannot silently be removed. The fused entry point returns None for unsupported data.

### Divisor-spectrum v13: useful packaging, inherited covariance

Primary source: extracted divisor `RESEARCH.md`, especially sections 3–6, and `prototype.py`.

The displayed bound is V(N,M)=2 sum_(d=1)^(M-1) 1/phi(N/gcd(N,d)), for N=KM, 2≤M≤K. This is already proved explicitly in master `additions/1916/COMPOSITE_GREEN_AUDIT.md`, section 3, before its coarser simplification. New file bytes therefore do not establish a new mathematical bound.

The previously accepted shell-count bound C(N,M)=sum_g max_u c_g(u)/phi(N/g) is no larger. For M equal to the least prime p, every nonzero permitted displacement has gcd one and c_1(u)=p−1, so C=(p−1)/phi(N)=V/2. The balanced-composite shrinking-error regime follows at least as strongly from that existing bound plus the earlier fixed-row median tail.

Two concrete review points:

- The formula V(pq,p)=2/(q−1) stated for p≤q needs distinct primes p<q. For p=q, V(p²,p)=2/p. The exponent-level square-prime regime survives.
- The planner scans every eligible divisor and calculates many exact rational bounds using repeated gcd and totient/factorization calls, while its displayed work proxy charges only a single sqrt(N) setup term. Audit the complete dispatcher ledger, including rational representation, unit sampling, all candidate planning and median storage. A complexity theorem for a chosen route does not automatically certify the uploaded planner.

Approximation remains fixed-input randomized additive energy-relative error. Exact expectation, a variance certificate and recorded numerical agreement do not imply exact transform values. The original source states its Python prototype was slower than NumPy FFT in every saved benchmark; those timings remain source records.

## How to fuse all six without losing earlier corrections

- HERO0 supplies the already-audited composite projected-transform executor. Divisor v13 reuses that exact core and repackages covariance/length selection; retain the stronger accepted covariance and sampling qualifications.
- Mixed-radix v13 already connects exact beta-bank completion to ordinary Cooley–Tukey. Completing all missing channels recovers exactness but restores the charged transform bank. Its independently established shared-randomness and completed-bank conditioning refinements remain intact, as does the source test-sign correction.
- HERO17 adds restricted raw-input recognition. Sparse fibers allow pruning the dense polyphase bank; generic full spectral fibers return to M unrelated length-Q transforms. The resulting dense-channel evaluator is an open constructive target, not a supplied algorithm.
- Sparse-defect and Phase26 restrict particular uniform operator architectures. Their rank and crossing obstructions do not directly prohibit nonlinear input-dependent recognition on a proper input family. Conversely, maximal ordinary rank of a structured input matrix does not refute those operator obstructions.
- The sparse-defect audit's arbitrary-row-sparse repair, charged Woodbury setup and pivot qualifications remain authoritative. The Phase26 factor-two crossing improvement and exact strict-witness repair remain authoritative. Reuploading identical sources does not reset them.
- Balanced distinct-prime products illustrate complementary contracts: exact CRT transforms on bounded tensor rank, versus randomized approximation on arbitrary input. Square/power-of-two lengths illustrate exact polynomial-phase fiber families and dyadic architecture gates. Neither comparison expands an input promise into arbitrary-input coverage.

Next integration should add the three new independent audits and this provenance record, reference the four completed duplicate-source audits, retain original archive bytes, and clearly distinguish source claims, proved inheritance, corrections, finite controls and unresolved targets. No publication-priority verdict follows from this triage.
