# ALG-007: bounded exact rejection-to-fallback adapter

16 October 2026 UTC. Owner: ALG-007, Raw sparse global-phase support recognition. This is a new, separately authored implementation of the accepted formulas and the missing rejection/fallback control flow. Historical sources are preserved and were read only as data. The historical executable was not imported, patched, compiled, or run.

## Result and review boundary

This is a bounded implementation/completeness repair of already accepted formulas. No novel mathematical theorem or asymptotic improvement is established; technical completion does not imply high mathematical research value.

`alg007_bounded_adapter.py` is an actual callable implementation, not a callback stub or an abstract fallback label. It performs cold validation/setup, adaptive exact recognition, complete Green decoding, and a complete full NTT if recognition exceeds the cap or the fast attempt runs out of its declared budget. Budget exhaustion during decoding also discards the partial output and takes the full fallback. Every route returns all Q coordinates of the same unnormalized negative-exponent Fourier transform. The fallback consumes the original validated snapshot, never a partial reconstruction.

New direct-definition controls passed 2,960 transform calls and 45,784 exact output-coordinate comparisons: 931 Green acceptances, 1,401 cap fallbacks, and 628 budget fallbacks. These are finite checks of this new module, not execution evidence for historical source. The parent independently accepted this bounded adapter after 3,252 additional calls, 108,224 direct-DFT coordinate comparisons, 17 edge controls and 60 exact accounting controls. The completed implementation gate is eligible for owner reconciliation; this artifact makes no novelty, arbitrary-length, floating, optimized-runtime, or unbounded asymptotic improvement claim.

## 1. Source and owner binding

The historical `phase6_exact.py` was read in full from the original archive. Its public `adaptive_green_sparse(x, m, rmax, a=1, beta=0, counter=None)` returns an unnormalized accepted transform or `None` with partial support and a counter; it does not call a fallback. Its `independent_full_dft` uses a full radix-2 NTT, but is not dispatched on rejection. The source fixes p=2013265921 and generator 31; its arithmetic domain is dyadic. Its `sum(terms)` Green seed and root/inverse powers bypass the displayed field-operation proxy.

The governing Phase6 audit and Integrated Results §2 were read in full. Their corrections control over broader original prose. The current owner was read in all three complete rows, including notes: Catalogue A72:AF72, `novelity breakthough` A33:Z33, and Research overview A50:Q50, in spreadsheet `1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU`. The comparison is already complete; the compatible-model implementation/charging gate is the remaining recorded work. Live status was TO RESEARCH, priority 42. Nothing was written to those rows.

`SOURCE_BINDINGS.json` identifies original/archive members and pinned audit/comparison bytes. The complete private readback is retained separately; the portable packet contains only the necessary source bindings and public report. Original source texts, formulas, accepted proof status, and history are unchanged.

This new module is source-bound by explicit input/model/formula/output correspondence. It is not a wrapper that imports `phase6_exact.py`, nor is it evidence that an external dispatcher now calls the old module. Actual old-module integration and replay remain **UNRUN**. The recorded owner gate does not promise a legacy import, patch, or live dispatcher integration, so this evidence limitation is not an additional owned blocker. Such work would require a separately authorized integration task. No dummy callback stands in for the implemented fallback.

## 2. Exact field, length, parameter and root contract

The only supported field is the prime field F_p with p=2013265921=15·2^27+1. All field values use canonical Python built-in integers 0 through p−1; booleans, floats, subclasses, and noncanonical integers are rejected. Input must be an exact built-in list or tuple, with no concurrent mutation during the call. A fresh canonical tuple snapshot is made and fully validated before any recognition. No synthesized support, selected coefficients, input-dependent advice, or cached preprocessing is accepted by the public API.

The length Q must be a power of two with 4≤Q≤2^27. The supplied M must be a power-of-two divisor of Q with M≥2 and K=Q/M≥M. Consequently K is dyadic, Q is even and 2Q is invertible in F_p. The supplied slope a is a canonical odd integer modulo Q, hence a unit; beta is canonical modulo Q. The cap R is an integer in [0,M]. The supplied chirp/factorization is used once; no favorable-parameter search or padding is hidden.

The caller may supply a canonical root zeta. It is admitted only after zeta^Q=1 and zeta^(Q/2)≠1, which characterize exact order Q for dyadic Q. If omitted, zeta=31^((p−1)/Q) is constructed by charged repeated squaring. Every call also verifies the fixed complete factorization of p−1 and checks 31^(p−1)=1, with 31^((p−1)/d)≠1 for d=2,3,5. Thus 31 has multiplicative order p−1 modulo p. Since it is a unit, its order is at most phi(p)≤p−1, with equality only when p is prime. This proves the fixed prime/generator certificate without assuming a field for the preceding modular operations. Those operations have their own `setup_modular_mul` category.

A full Q-entry root table is freshly constructed with exactly Q−1 field multiplications, plus its charged storage/reads/writes. M^−1 and 2^−1 are independently computed by charged repeated squaring with exponent p−2. All short and full NTTs use the same table and field; no stage-root oracle or additional FFT backend is assumed.

Invalid parameters or field encodings raise `ContractError` and carry the completed ledger when available. They do not silently select another length, field, chirp, normalization, or padded transform. Ordinary memory exhaustion and implementation faults are not caught and mislabeled as successful fallback. The upper algebraic length bound is not a claim that the Python prototype has sufficient memory or practical speed at that bound.

## 3. Independently specified recognition and output interface

Public call:

    transform(x, m, cap, a=1, beta=0, root=None, attempt_budget=None)

Keyword-only parameters after cap retain the displayed semantics. `attempt_budget` is a nonnegative integer. The default is B=64 Q log2(Q) declared event units. It covers both recognition and Green decoding. Cold setup/input validation, fallback, and final explicit output materialization are separately charged. A supplied B may be smaller or larger; the general bound retains B explicitly.

The return value contains:

- `values`: a canonical tuple of exactly Q values Y[k]=sum_n x[n] zeta^(−nk), k=0,…,Q−1, with no sqrt(Q) or 1/Q normalization.
- `route`: `GREEN_ACCEPT`, `FALLBACK_CAP`, or `FALLBACK_BUDGET`.
- `support`: the exact active support in discovery order only for completed Green acceptance; otherwise `None`. It is never a fake certificate for an interrupted call.
- `progress`: fully completed blocks, completed full short discoveries, and a certified lower bound from completed processing. A budget stop can leave this lower bound smaller than modes found in an unfinished discovery. Rejection does not claim complete recognition.
- `model`: p,Q,M,K,zeta,a,beta, sign and normalization.
- `ledger`: phase counters, their exact componentwise sum, consumed budget, and the rejected next reservation, if any.

There is no caller-supplied executable recognizer or fallback callback. `_recognize` is internal and returns either `ACCEPT` with all exact coefficient columns or `CAP_REJECT` with a lower bound exceeding R. Budget exhaustion raises a private control exception and does not return an accepted certificate. This avoids granting arbitrary untrusted code free work or trusting a fabricated acceptance flag.

For each block b, the module forms

    y_b(t)=zeta^[a t(t−1)/2 +(aMb+beta)t] x[bM+t]
    D[b,j]=sum_t y_b(t) zeta^(Kjt).

It maintains the discovered union S. Every selected coefficient is directly recomputed for the current block, and every one of its M reconstruction coordinates is tested by strict finite-field equality. A failed certificate triggers a complete positive-sign M-NTT. Its nonzero coefficients extend the union; exceeding R rejects before any Green decoding. New columns are initialized with paid K zeros, correctly recording their absence in all previous completed blocks. A passing block needs no full M-transform. The zero input is accepted with S empty after checking every coordinate.

On a completed acceptance with r=|S|, every raw coordinate has been reconstructed exactly and at most r full short discoveries were completed. On cap rejection, at most R+1 complete short discoveries occurred. A mode appearing only in the final block cannot be omitted. No scalar projection can cancel a mode out of the vector-valued union.

For each accepted mode j, set beta_j=beta+jK and compute the negative-sign K-NTT B_j of D[:,j]. The forcing and gauge are exactly the accepted formulas:

    f_j[k]=B_j[k mod K]
       − zeta^[−M(k+beta_j)−aM(M−1)/2] B_j[(k+aM) mod K]
    g_j(h)=zeta^[a h(h−1)/2+beta_j h],  k=ah mod Q.

The module computes every term f_j[ah]/g_j(h), its complete seed sum multiplied by 2^−1, and the prefix reconstruction of each output. Since g_j(Q)=−1, the antiperiodic closure is valid in this model. It accumulates all mode rows and multiplies by M^−1. Exactly rQ seed additions are charged by this implementation, including addition to an initial zero; this exceeds the historical missing lower count r(Q−1). All r K-NTTs, r Q-scans, normalization, accumulation and Q final writes are paid.

## 4. Fallback and interruption contract

The fallback is a fresh decimation-in-frequency radix-2 NTT followed by an explicit bit-reversal permutation into natural output order. It uses the negative exponent and the same zeta table as the accepted route. It is implemented in this packet; it is not a reference to a merely assumed compatible backend.

A cap rejection retains every recognition/setup charge and invokes one full Q-NTT. An insufficient reservation in recognition or decoding does likewise. No partial coefficients or output are interpreted as a valid transform. The full NTT reads the original validated tuple snapshot. The same meter remains alive throughout; no reset or counter replacement hides earlier work. Final output materialization is charged after either route.

Reservations occur before operations. Grouped allocation/read/write and root-lookup reservations are atomic: if the remaining budget cannot fund the group, none of that group's operations occurs. Scalar field operations are individually charged. A budget denial may occur between two operations of a larger kernel; all already executed operations remain charged and the unfinished kernel's output is discarded. Diagnostic completion events such as `ntt_finished` and `green_row_finished` count only when reached.

Budget B=0 is legitimate: cold validation/setup is still paid, then the first recognition allocation fails its budget reservation and a complete full NTT runs. A budget exhausted after complete recognition but during the final decoder likewise performs the full fallback. It is deliberately incorrect to report only the fallback's cost in either case.

## 5. Cumulative work and memory ledger

The ledger is a declared exact-field / word-RAM event model, not a claim to meter every Python instruction, allocation header, cache miss, branch, or bit operation. `field_mul` and `field_add` count actual modular arithmetic calls; subtraction counts as one addition-category operation. `field_equal`, setup modular multiplications, root lookups, selected reads/writes, allocation words, index/control steps, certificate coordinates, and completion/dispatch markers are separate charged categories. Their sum is the budget unit used by the adapter. Tags such as `green_seed_addition` intentionally add a diagnostic/control unit as well as the associated field-add unit; they are not extra mathematical additions.

Each loop iteration and variable-length allocation has a charged unit or charged length. Unlisted scalar bookkeeping and integer index arithmetic cost O(1) word operations per charged event in the declared model; indices/exponents require O(log Q)-bit words with a constant-factor expansion. Coefficient columns are indexed arrays, not data-dependent hash maps. Remaining dictionaries have a fixed finite vocabulary of counter/metadata keys, so their bookkeeping has an input-size-independent bound. Growing Python big-integer, OS/runtime and wall-clock costs are not asserted to equal the event sum. The fixed p and finite Q domain do not establish an unbounded family theorem.

Let L=log2(Q) and E(e)=popcount(e)+2 bitlength(e)−1 for positive e. This is the exact event total of `_pow_mod`: popcount(e)+bitlength(e)−1 modular multiplications plus bitlength(e) loop/index events. For a valid default-root call define

    H(Q)=E(p−1)+E((p−1)/2)+E((p−1)/3)+E((p−1)/5)
         +E((p−1)/Q)+E(Q)+E(Q/2)+2E(p−2).

For a supplied valid root, omit E((p−1)/Q). Cold input and setup cost exactly

    C_cold(Q)=15Q+11+H(Q)

in this event model. It includes both snapshot copies, every canonical input check, the prime/generator certificate, root construction/order tests, both inverses, and the entire table. The NTT kernel on n=2^ell words costs exactly

    T(n)=(13/2)n ell +9n+ell+1,

using the already paid Q table. In particular it executes n ell/2 butterflies, n ell/2 field multiplications and n ell field additions; the other terms pay copy/permutation/index/control/storage events. Fallback dispatch adds one unit. Final result materialization costs 4Q units, plus 3r support-metadata units for Green acceptance.

With A_rec and A_dec the actual attempted recognition/decoder event sums, A_rec+A_dec≤B. The total on either kind of fallback is exactly

    C_cold(Q)+A_rec+A_dec+1+T(Q)+4Q,

where A_dec=0 for a cap rejection. Thus

    W_fallback ≤ B +(13/2)Q L +28Q+L+13+H(Q).

At the default B=64QL this is at most (141/2)QL+28Q+L+13+H(Q) declared units. This finite implementation envelope does not assert a smaller asymptotic FFT bound or measured practical speed.

The completed structured route retains the accepted work accounting, now including all seed and setup costs:

    O(Q + rQ + rK log K +(r+1)M log M + H(Q)),

and rejection before decoding retains

    O(Q + RQ +(R+1)M log M + H(Q)).

These are structural operation bounds for eligible parameters; the budget may truncate either route sooner. There is no claim that every sparse input fits the default constant 64, and no free arbitrary-length M=Theta(log Q) factorization. An explicitly larger B retains that larger B in the wrapped worst-case bound.

Peak working field-word storage is O(Q), including during interrupted work. The snapshot and root table take 2Q; all accepted columns together take Kr≤Q; column slots/support flags take O(M). Recognition has O(M)-size block/selected/discovery/NTT temporaries. Decoding has one Q accumulator, one Q term array, and O(K) transform work. On an interrupted decoder the accepted columns may remain referenced until function return, but still occupy ≤Q; discarded temporary frames do not form a growing history. The fallback's input copy/permutation arrays and final tuple add only a constant number of Q arrays. Sum-of-allocation events may be superlinear across many iterations; that is distinct from simultaneous live storage. Ordinary Python allocator overhead and garbage collection are outside the field-word bound.

## 6. Tests, replay and limits

Run from the portable packet directory:

    python test_alg007_bounded_adapter.py

Only Python's standard library is used. This imports the new adapter only. The independent oracle evaluates every output from the direct Fourier definition with modular powers; it does not call the production NTT or historical helpers. The independent support oracle directly evaluates all block coefficients. Test generation is separate from, and never substitutes for, paid raw recognition.

The suite covers:

- All 81 Q=4 raw vectors over the explicit alphabet {0,1,p−1}, both unit slopes, all shifts, and all three caps. This is not exhaustive over F_p^4.
- Q=8,16,32,64,128,256, several eligible M, unit slopes and shifts; zero, shared one-mode, disjoint per-block, final-block-only, late new mode, dense full support, and deterministic arbitrary raw inputs.
- Every budget 0 through 613 for a Q=8 case needing 612 attempt units. Boundary checks also interrupt recognition, the first decode allocation, and a nearly finished Q=64 decoder.
- Multiple supplied primitive root orientations; invalid root orders and malformed/noncanonical parameters/values, without silently invoking fallback.
- Repeated cold calls produce identical full ledgers, demonstrating no reusable hidden table/certificate cache in this API.
- Exact phase-sum conservation, spent-budget limit, Q final coordinate writes, complete fallback butterfly/add/multiply counts, accepted support equality, full-coordinate certification and rQ seed-addition tags.

`CHECK_RESULTS.json` binds the final source/test hashes and reports all counts. `CONTROL_RUN.log` records the author-side run. The independent reviewer should verify source bytes before executing this new module and keep any additional reviewer files separate from the immutable source. Finite direct controls support the implementation; the formulas and control-flow/ledger arguments supply the general contract within the bounded admissible model. No historical timings or historical source test claims are promoted to fresh evidence.

## 7. Owner scope adjudication

The recorded obligation is to implement and charge a compatible-field/length rejection/fallback wrapper, with source binding, exact backend/domain, all prior failed-attempt charges, roots/inverses/all outputs and independent verification. It does not require importing or patching the historical executable, nor does it name an existing external dispatcher that must be modified.

That obligation is now complete at the bounded domain in this report. `transform` is a real wrapper around independently implemented, source-bound recognition and Green stages and an actual compatible full NTT. The original source's exact model, raw grammar, signs, formulas, rejection behavior and counter omissions have been explicitly read, pinned and mapped. The independent review accepts the new realization, cumulative contract and executable controls. Requiring literal historical replay as an additional closure condition would add work absent from the recorded owner promise.

The earlier primary comparison is already complete. On the complete owner rows read for this task, no other currently owned open clause remains after this bounded implementation gate. The parent may therefore close the current recorded stage after its own owner reconciliation; no native row has been changed by this worker. Preserve the accepted scoped theorem, historical priority/rank text and all broader model, novelty, floating, bit-complexity and practical-speed limitations. Closing the recorded work is not promotion to an unrestricted FFT result.

Historical `phase6_exact.py` execution, patching and live dispatcher integration are still unrun. This is a strict provenance/evidence boundary, not a claim that the old module now falls back or has complete counters. If a future task explicitly asks for those actions, obtain the required execution/integration permission and verify that separate work. Do not silently turn that possible future task into an unresolved obligation here.
