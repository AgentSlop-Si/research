# Independent review: fixed phase-one CHIRP sparse path

11 October 2026 UTC. Decision: **ACCEPT at bounded implementation scope**.

This review accepts the fixed phase-zero/phase-one sparse schedule, exact
nonzero-phase output kernel, and residual-budget fallback at final
`chirp_phase_one.py` SHA-256
`0dd2e0f54851bff04c3f6b9f5b9c29caa1ec9d9089e4df8eae7f341facf430e6`.
It does not accept general sparse phase search, min(B,H), production readiness,
an optimized-FFT speed claim, or historical novelty. No mathematical or
executable-code repair is required. Two overbroad source docstrings were
clarified before this final-byte acceptance; executable AST equality and
retesting are recorded separately.

## Exact binding and independence

The author archive is 105,969 bytes, SHA-256
`849aa57cff7a2842c461756992cef951374f821de8e179520510f8bf98d76eec`.
All 41 payload hashes and byte lengths, ZIP CRCs, and manifest coverage were
independently checked. The final report is bound to its archived bytes.
The immutable accepted dispatcher is
`b6ba169043f522f4d419f54b7b3cc24f439e76e9d9b69d76d977da6dfd1c1aad`;
the dense reference is
`7d263f616526bd1123658771afc73bb44fc15282ef8ee0131e48ade0b59d18b7`.

The reviewer read the previously accepted phase-zero and dispatcher contracts,
the complete source diff, final report, test code and benchmark harness. Fresh
reviewer-owned controls calculate direct finite-field support and DFT values;
candidate outputs are not the expected-value oracle. Only fresh candidate code
and the explicitly permitted accepted reference implementations were executed.
Original uploaded research programs remained inert. This is independent project
review, not external peer review or proof-assistant certification.

## Mathematical argument

Let N be a power of two, N>=4, M=N/2, and let omega have exact order N in F_p
with N dividing p-1. The field has odd characteristic. Define
G(s)=sum_j omega^(j^2+s*j). Pairing j with j+M multiplies each summand by
omega^(M^2+s*M)=(-1)^s because N divides M^2. Thus G(s)=0 for odd s.
For s=2t, completion of the square gives G(2t)=omega^(-t^2)G(0).
The expression is invariant under t modulo M, since 2Mt+M^2 is divisible by N.
These identities require no complex square root or numerical Gauss oracle.

For a verified phase-one representation
x_j=omega^(j^2) sum_b gamma_b omega^(b*j), its positive-sign unnormalized DFT
at k is sum_b gamma_b G(k+b). At k=2u+delta, only b=2v+delta contributes.
Putting h=v+delta modulo M yields

    DFT[2u+delta] = G(0) omega^(-u^2)
        sum_h gamma_(2v+delta) omega^(-h^2) (omega^(-2))^(u*h).

For each parity, b maps bijectively to h, and omega^(-2) has order M. Therefore
the two calls to the previously accepted support-pruned FFT compute exactly
the required output. Empty parity supports produce explicit zero arrays. N=4,
negative exponents, modular h wraparound, and both parities are covered. Linearity
in the amplitudes extends the single-mode argument to every recovered support.

The new attempt first dechirps every validated raw entry, applies the accepted
BM/grid-root/partial-fraction recovery, synthesizes every dechirped coordinate,
rechirps it, and compares it with the original raw input. Thus every success has
an independently checkable complete witness. The prefix alone never certifies
membership. The accepted cyclic recovery permits wrapped prefixes with 2r>N.
Any sparse rejection goes to the next scheduled route or the complete accepted
dense reference, never directly to NONMEMBER. The whole recognizer's completeness
is therefore retained even independently of sparse-path efficiency. The returned
phase a=1 is canonical for dyadic N>=4; N=2 skips it.

## Program and resource contract

The original exact built-in container/integer restrictions, primality/root
validation, sign/normalization, dimension/bit/work caps and CLI finite-JSON
restrictions remain in force. Input is resident at API entry. N=1, r>=N and
the order-2N-root curvature model are excluded. Runtime or operating-system
exceptions are outside the decision-status guarantee.

Eight reused class/function definitions have identical ASTs: Meter, append,
copy, BM, pruned FFT, Horner, non-dyadic guard and CLI. The phase-zero arithmetic
and metered non-dyadic direct route are unchanged. The generalized sparse
attempt changes stage labels and adds paid rechirping only on the new route.
The output kernel uses actual nonempty-subtree recursion, not a dense transform
after which work is relabeled sparse.

There is one global instrumented budget. Successful payments precede the
represented operations. Both failed sparse attempts and repeated dense setup
are charged; fallback receives exactly the original budget minus the completed
prefix. Aggregate categories are the sum of the two ledgers. LIMIT is indeterminate
and removes both representation and DFT, including a final-write interruption.
Same-cap decisions need not match the previous dispatcher: a new success can
avoid expensive fallback, while a new failed attempt can consume its budget.

For s recovered modes, the non-FFT output categories sum to 9N+5s units:
2N+s each for root reads and index events; N additions; 3N/2+s products;
N/2+s field-entry writes; s parity tests; and 2N output writes. Both full
pruned-FFT ledgers are additional. Dechirping costs 4N units and rechirping adds
3N to the reused synthesis ledger; the schedule test costs one unit. The
successful fixed-two-attempt path uses O(N log(r+2)+r^2) field additions/products
excluding inverse internals, plus O(r) inversions; implemented Fermat inversions
add O(r log p) products. Sparse live field storage is O(N). Fallback retains
the accepted O(N+r^2) field-storage scope plus retained frontend arrays.

These are selected arithmetic/data-event and field-cell contracts, not a
complete Python instruction count, bit-complexity theorem, process-memory cap
or wall-clock guarantee. Integer indexing, dictionaries, object bookkeeping,
JSON, hashing, allocation and control overhead are not all metered. The final
report states these limitations explicitly. No setup or Gauss/root cache is
silently supplied to the new mathematical kernel.

## Independent executable evidence

The final source passed fresh reviewer-owned tests:

- 716 complete mathematical decisions, with 10,431 independently computed
  returned coordinates and 159 new phase-one successes.
- 3,925 every-unit interruptions, preserving output withholding and work caps.
- 402 exact residual-budget fallback replays and 235 unchanged-route ledgers.
- Eight unchanged AST definitions and equality of all executable AST after the
  documentation-only correction.
- A separate import-free Gauss derivation control: all primitive roots in 114
  tested length/prime/root cases, 2,264 Gauss entries and 58,848 single-mode
  output entries.

The entire author suite was replayed against the final bytes: 17,618 differential
decisions, 923 exact output-kernel/ledger cases, 2,768 Gauss coordinates,
3,323 every-unit cutoffs, 892 residual replays, malformed-input/CLI controls,
and the N=512,r=128 last-write boundary all pass. The latter needs 406,494
instrumented units and withholds outputs at 406,493.

All 165 author benchmark records were checked for stable exact ledgers/digests.
A further 33 reviewer-owned fresh processes, one per engine/fixture, reproduce
every saved exact ledger and decision/output digest. These fresh samples are
not a remeasurement of the five-sample medians. The reported host timings are
accepted only as attributed finite diagnostics. The final author report correctly
discloses the N=8 loss against the previous dispatcher, small-case losses against
dense reference, zero/fallback regressions, and absence of an optimized-library
baseline. Fewer instrumented units do not imply a uniform elapsed-time gain.

## Accepted milestone and remaining work

The bounded fixed phase-one sparse/Gauss-output integration is closed at the
exact final source hash. It is an implementation extension of already accepted
mathematical ingredients, not a new unrestricted FFT theorem. General phase
selection, all-phase sparse execution, min(B,H), optimized blocked/Toeplitz
integration, complete production costs, optimized FFT comparisons, finite-bit
or numerical transfer and historical priority remain open.

This review does not modify the live Sheet or earlier artifacts. The separate
table-gap pass is paused after a canceled four-cell batch; readback confirmed
zero newly saved cells. Repository publication can record this review without
claiming those table proposals were applied.
