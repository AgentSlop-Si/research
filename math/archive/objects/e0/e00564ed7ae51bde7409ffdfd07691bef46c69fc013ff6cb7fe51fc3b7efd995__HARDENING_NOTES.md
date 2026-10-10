# Query-engine v2 hardening

This is a separate tested derivative of `fft_relation_query_engine_v2(2).zip`.
The uploaded archive and the extracted original source were not overwritten.

## Changes

1. Reduce Fourier exponents using integer modular arithmetic before converting
   them to floating-point angles. The large-logical-period path uses Python
   integer multiplication to avoid int64 overflow.
2. Validate calibration-sample reuse with a 256-bit BLAKE2 fingerprint. A
   different or mutated first row is transformed afresh. Computing/verifying
   this fingerprint costs O(N), and setup fingerprinting is inside the reported
   calibration time. This is a practical hash guard, not a proof against all
   possible digest collisions.
3. Honor `max_pruned_trials=0` and the low-basis-count no-tuning decision.
4. Shared views inspect only the recent event suffix, then replay that suffix
   in original chronological order. This avoids lifetime-history scans without
   changing floating-point addition order. Temporary replay storage is O(H).
5. Union-fusion planning charges a complete rebuild when a view's history was
   discarded, and excludes already-current bins from the proposed union.
6. The shared store owns a compact basis-projection copy, preventing retention
   of a much larger parent array and accidental caller mutation.
7. `storage_bytes` now includes union-bin and event numeric payload. It remains
   a lower bound, not Python heap or RSS: dict/deque/tuple/object overhead,
   allocator behavior and temporary arrays are excluded.

## Verification

Run from this directory:

    OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v

All 30 supplied tests plus 10 targeted regressions pass (40 total).
The independent audit script also passes 234 arbitrary-bin comparisons and
3,000 mixed multi-consumer comparisons against fresh NumPy FFTs. It covers odd,
prime, composite and power-of-two lengths; duplicate bins; empty bases;
bounded/missing histories; mixed coefficient and point updates; shared queries;
and isolation of returned arrays.

Reproduced original-to-derivative changes:

| Case | Original | Hardened |
|---|---:|---:|
| Events visited with 100,000 old events and H=1 | 100,001 | 2 |
| Backing retained for a visible 64-byte projection | 1,048,576 bytes | 64 bytes |
| Wrong first-row sample max absolute error | 80.485 | 5.96e-14 |
| Requested zero productive trials | 1 trial | 0 trials |
| N=2^20 constant signal, bin N-1 expected zero | 4.29e-5 error | 9.59e-11 error |

The cancellation case diagnoses phase generation; it is not a global forward
or backward numerical-stability guarantee. Ordinary summation and float64
roundoff remain, and near-zero outputs require absolute/scaled error measures.

## Scope and remaining limits

- The original `relation_view.py` and `projected_fourier.py` are carried through
  unchanged. Their previously identified lifetime scans, retained backing and
  log-accounting issues remain. Use the separate coalesced single-view
  experiment in the bundle for that work.
- A default `event_capacity=None` remains unbounded storage. Configure a finite
  capacity or compact deliberately. Reverse-suffix replay fixes scan cost, not
  retention policy.
- A returned q-vector takes Ω(q), even with H=0. With available history and no
  one-off promotion, shared query work is O(q[1+min(H,r+k)]). Missing history
  requires O(q[1+r+k]); a small event cap alone does not preserve the min bound.
- Promotion can copy r*q values. Shared projection registration, phase tables,
  cache construction and returned-vector copies need to be charged.
- `query_many` still builds/compares the frequency union and copies outputs;
  its cost proxy is not a complete timing model. It is not a universal optimum.
- Planner memory limits remain phase-table admission heuristics, not measured
  peak-memory guarantees. Productive trials still pay losing-plan construction
  and can select a noisy winner; no universal timing improvement is claimed.
- Numeric finiteness and integer-index validation remain limited in trusted
  fast-path APIs. This derivative is research code, not a hardened public API.
- The mathematical pruning identity is classical. No new uniform FFT,
  exact-floating FFT, integer-multiplication bound or novelty claim is made.

## Benchmark interpretation

The uploaded arbitrary end-to-end result reports 1.935102 ms projected
steady-state versus 1254.803499 ms dense maintenance + full FFT, a 648.44x ratio.
Its projected registration costs another 112.507438 ms. Charging that cost
reduces this particular comparison to approximately 10.96x before further
matching the baseline to the same q outputs. These are reported source timings,
not timings reproduced on this machine. The useful next experiment measures
total build/update/query work against both full FFT+gather and a fresh pruned
q-output baseline across lifetime, query cadence, overlap, and cancellation.
