# Supplemental audit: recovered growing-fiber companion

## Result

The recovered full companion closes the earlier **availability** gap: its THEORY.md is byte-identical to the already accepted direct upload, and its implementation and recorded results can now be inspected. The earlier sealed theorem review remains unchanged.

The reviewer has read all 345 lines of fiber_fft.py and all 252 lines of verify.py as inert text. Their internal algorithms are consistent with the accepted mathematics under the documented input contracts. No uploaded program was executed or imported. This is a static algorithm/contract audit with independent controls, not a claim that every original software execution or invalid-input behavior was tested.

All six recorded arithmetic profiles were independently derived from a fresh operation-count model. In particular the largest case is exactly **7,516,160 versus 7,340,032** counted field operations, a ratio of 1.0239955357142858. It is about 2.4% more arithmetic than the supplied baseline, not a demonstrated finite speed advantage. A separate reviewer implementation also verifies all 262,144 Fourier outputs for this exact structured profile.

## Source identity and coverage

Library [private-id], `fft_certified_growing_fibers_2026-10-10.zip`, 31,401 bytes, SHA-256 4dcf274a1691f6725102c6f186b2bb3a1719ed3bef7dc3ae9c9863afdf02f0e1. CRC and all eight internal manifest entries pass. THEORY.md hash a5c0da63f7761f91c26cf7662afb0ba5f7874f330db36791addde9bf6c58f045 matches the direct source exactly.

Fully read: README.md, SOURCE_LEDGER.md, VERIFICATION.txt, both Python programs, and the previously reviewed THEORY.md. RESULTS.json was fully parsed and its group/cardinality/profile fields inspected. SOURCE_INVENTORY.json was parsed as metadata; its referenced historical files were not individually re-audited here. The source itself explicitly describes that historical inventory as targeted inspection rather than exhaustive proof review, and this supplement preserves that distinction.

The accepted mathematical review dependency is `review_growing_fiber`, manifest 74f5424e70a63be289a1f9263a907c5525576da93779af6a1e750fd0cf9b853f. No theorem change was found in the companion.

## Static implementation audit

- The public entrypoints normalize raw inputs modulo p, enforce dyadic N≥4 and valid budgets, build and validate a complete root table, and pass the correct fiber and bucket strides.
- Primality is supplied, as explicitly stated. The root is supplied; root-table generation and order validation do not construct a suitable field or discover a primitive root.
- The input-pruned transform omits empty children. Even-only combines are copies; odd-only combines use a twiddle multiplication and a negation; two-child combines use one multiplication and two additions. All full outputs, including absent buckets, are explicitly allocated/written.
- Its sparse helper requires distinct support indices and a stride of the intended root order. It does not independently validate every such helper contract; internal callers satisfy them. It should not be advertised as validating arbitrary malformed external sparse lists or strides.
- The Berlekamp–Massey recurrence, grid-root evaluation, derivative/residue amplitude formula and full raw-fiber comparison implement the accepted recognizer. A fitted degree exceeding the cap rejects before grid work. A degree-zero candidate checks the whole fiber. A nominal degree whose leading coefficient vanishes cannot pass the exact root-count requirement because C(0)=1.
- The global residue buckets use the required phases and factor M. The Green residual and undo scan retain the correct positive-Fourier orientation.
- The cyclic solver checks individual diagonal and closure denominators. Invalid finite-field Green choices may raise even when `fallback=True`; the full-input fallback guarantee is under the declared valid-parameter contract. Rejection fallback transforms the original x, not the residual, so no erroneous extra undo is applied.
- The aggregate implementation computes a full fiber transform only after a complete light-recognizer failure, checks the discovered degree is genuinely heavy, and rejects immediately when the cumulative budget is exceeded. Its final-heavy-fiber charge matches the accepted proof. Zero budget is handled by the same path.
- Test-data generation and reference FFTs are outside the raw-input fast path. The operation counters are field primitives plus a separately labeled coarse word proxy, not wall-clock timings or bit-complexity costs.

No substantive correctness discrepancy was found under these declared contracts. This is not exhaustive execution testing of the source implementation.

## Independent arithmetic profile derivation

The reviewer wrote a new count model using a fresh recurrence computation and a support-tree recurrence for pruning cost. For a node of length L, the local arithmetic charge is 0 for an even-only child, L for an odd-only child, and 3L/2 for two nonempty children. Amplitude recovery for r nonzero modes costs 5r²+6r primitives in the stated residue/Horner implementation. Root-table construction, every mode phase and all final scaling operations are added explicitly. Berlekamp–Massey discrepancy/update operations are counted independently from the newly computed prefixes and recurrences.

All six profile totals for N=256,1024,4096,16384,65536,262144 match exactly. The full-dense baseline is N+(3N/2)log2 N, including its root table. The independent model verifies the recovered polynomial roots for every fiber used in the profiles. It also checks the displayed ratios, total K, and two old-ledger comparison terms. This reproduces the **arithmetic model**, not the source's exact instruction trace, word proxy, wall time, or original test execution.

A second independent program reuses only the reviewer's own earlier algorithm, constructs the N262144, Q=M512, b18 profile from raw samples, and checks every output against an independently written dense FFT. It verifies K=9216. It also replays the earlier 1,294 recognition controls. The output digest and exact count breakdowns are included.

## What remains unverified

- The historical claim that running uploaded verify.py produced its log, passed 8/8 groups, or reran byte-identically. We validate the supplied result hash and deterministic loop cardinalities, but do not execute uploaded software.
- Exact random sample sequences and all original per-test counter snapshots. Fresh controls use a separately authored implementation and include the largest deterministic profile.
- Exact coarse word-proxy counts, hardware performance, numerical stability, arbitrary-precision costs, or an FFTW comparison.
- The abandoned N1048576 profile, which the source explicitly does not claim completed.
- Complete historical-corpus reading or proof coverage inferred from SOURCE_INVENTORY.json, and external publication novelty.

The accepted conclusion remains an exact, certified structured-input algorithm. Its all-input fallback retains the ordinary worst-case FFT bound. A dense raw input and dense final spectrum do not remove the intermediate-fiber restriction.

## Reproduction

Only reviewer-authored scripts are executed. The standalone profile model reads source RESULTS.json as data. The large-profile checker imports only the bundled reviewer implementation. Full isolated replay reproduces all three result JSON files byte for byte, with no uploaded code import. See REPRODUCE.md and PORTABILITY.json.
