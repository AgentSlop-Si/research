Public derivative of an independently reviewed research report. Private tracking and delivery details are omitted; mathematical statements, source attribution, review method and remaining limitations are retained. Original source-report SHA-256: 0d00a4e7d39c74c26ba7511bc2530d6ccdc530c057c07c15b261b07d6fa92bbd.

Review date: 12 October 2026 UTC.

# ALG079 independent source-bound ABI/counter bridge review

12 October 2026 UTC. Verdict: **ACCEPT, bounded exact-byte bridge only**.

## Result

The frozen candidate `ALG079_Legacy_ABI_Counter_Bridge_CANDIDATE_2026-10-12.zip` is 70,898 bytes, SHA256 `fe104b61030fad17b70c0ed5ed1316ea9e02e25b85a1f859ad52364f46e485e5`. All 27 manifest-listed files match; all 13 inert historical snapshots match both the pinned lengths/hashes and original files. Independent AST reconstruction reproduces the complete 13-module local import closure and its directed edges. The executable backend also matches the previously independently accepted original byte-for-byte.

The author harness replays from a fresh archive extraction with byte-identical `RESULTS.json`. The independent harness passes 1,118 invertible/269 singular plans, 4,472 Cost and 4,472 Work RHS comparisons against independent dense elimination, 8,944 literal solve deltas, 297 preview/full/reset/close schedules, 24,865 rejection/nonmutation checks, and 256 cold-preparation cases. Solver coverage includes 121 beta-zero and 493 invertible zero-diagonal/nonzero-beta plans. Graph domains include N=4096 and p=2^31-1. Exact counts and executable controls are included.

No historical module was imported or executed in this review. A meta-path denial guard and end-of-run module check enforce that boundary for independent controls. Historical text was parsed, not compiled or evaluated. No candidate or historical source was modified.

## Accepted source-bound conclusions

1. `deferred_dif.transform_deferred_conjugate(engine,x,s=4)` is a preconstructed-engine API. A body-only change cannot catch an exception raised while its engine argument is constructed before invocation. The pinned `RecurrenceGreen` inherits `AllLengthGreen.__init__`, whose L/P construction calls the old `CyclicSolver`. A separately defined raw-metadata/lazy-plan boundary is necessary to establish an ordinary fallback before that optional construction. This is a control-flow/API observation, not a new cyclic-solver theorem.
2. The original caller literally charges `3*N+1` multiplications and `2*N` additions after `L.solve`. The sealed replacement executes `(3*N,2*N-1)` for nonzero beta and `(N,0)` for beta zero. Retaining that charge overstates the replacement by 2 and 4*N+1 scalar field operations, respectively. This is a migration statement; the unchanged historical recurrence legitimately executes its own reported arithmetic. Inversions, setup, representation/bit work and traffic are separate.
3. Sequential, non-reentrant delta projection maps one successful accepted solve into either the historical ordinary-instance Cost fields or Work fields exactly once. Invalid sink fields and malformed RHS values fail before solve primitives or sink mutation. Unrelated fields and Work inversions are preserved. Projection and backend Field are alternative views and must not be added together.
4. The facade's caller-used names and normalized read aliases work for this specifically pinned caller. Input arrays and returned output containers are detached. It does not expose legacy private `h`/`invdiag`, accept every historical calling convention, or migrate all importers.
5. Full root-table validation, guarded one-preview lifecycle, exact N-q live backups, full completion, abandoned-preview release, idempotent close, reset/reopen and refusal nonmutation pass. Literal completed dyadic arithmetic is `(N log2 N/2 multiplications, N log2 N additions/subtractions)` per epoch, including identity twiddles.
6. Cold preparation creates a validated ordinary session first; static guards skip Green preparation, setup refusal preserves spent setup field charges, and ordinary fallback remains exact. The return reason `prepared-detector-not-run` is accurate. It does not perform historical detection, cyclic certification, denominator checking or compilation itself.

## Required interpretation and compatibility limits

- The concrete bridge scope is dyadic 2<=N<=4096, verified prime 2<=p<=2^31-1, supplied exact-order root. `CyclicSolverABI` itself follows the accepted solver's N>=2 contract and is not limited to dyadic sizes. Unsupported transform metadata is refused; no fallback is promised outside the validated transform domain.
- Read-only property aliases are not an immutable-object or tamper-resistance guarantee. The plan/session and underlying Field are ordinary Python objects. Use an unmodified accepted plan, exclusive ownership of its accounting during operations, and ordinary integer dataclass/namespace records. Concurrent/reentrant use, raw-object mutation, hostile iterators/descriptors, or arbitrary forged subclasses are outside this review.
- Graph arithmetic and selected traffic remain cumulative across successful reset; backup peak and live storage are per current epoch. Consumers must take deltas between epochs when they want per-input costs. The independent tests explicitly verify this distinction.
- `snapshot()['reads']` excludes separately reported `backup_reads`; caller aggregation may sum them once. `backup_writes=0` means an already-counted temporary copy is retained by alias, not that preserving data has zero physical cost.
- `storage_bound()` reports selected components, not a complete memory bound. It omits enabled diagnostic labels (O(N log N)), transient operand slices, host structures and runtime overhead. Repeated `full()` makes a fresh returned list, so its output-copy time/traffic is real although graph and selected counters do not change.
- Cost `output_writes` projects exactly N final-output entries. It is not the historical 2N proxy or a replacement full-RAM ledger. Work projection updates arithmetic only. Every migrated caller must revisit the old read/write estimates separately.
- Root validation/preparation and optional failed preparation are visible in the backend Field. The facade validates and builds its own root plan; later integration must avoid or account for duplicated setup. No free setup or production speed claim follows.
- `prepare_cold_entry` retains inherited Green coefficient defaults, including missing positional coefficients when a shorter tuple is passed. Malformed coefficient types/arity take setup-refused fallback. No claim of strict three-element-only input was made.

## Historical execution and remaining qualification

No historical detector module was imported or executed in this bounded review. Historical end-to-end migration/qualification is a separate task; the bridge controls and static source analysis do not constitute its execution evidence.

The broader lifecycle-integration problem remains open. Every downstream caller, actual detector/compiler resource bounds, complete successful and failed branch accounting, and production RAM/bit/time/cold obligations are not closed by this packet. Prior accepted solver/lifecycle results remain intact. No historical-priority, practical-speed or full-caller qualification conclusion follows.
