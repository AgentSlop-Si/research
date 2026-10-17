# Independent final review: ALG-034 restricted exact theorem-scale producer

17 October 2026 UTC. Decision: **ACCEPT the restricted exact ideal-target producer and caller-relative semantic replay verifier** at source SHA-256 `9bbd77a44f8a265f170b1993b63cae71d8f5a8da9f108a85d68b2a7719fca717`.

This decision is confined to the newly implemented, explicitly restricted backend `ALG034-EXACT-AXIS-SUPPORT-v1`. It accepts canonical four-axis sparse exact dyadic inputs, singleton blocks, and N=2^m with even 2<=m<=64. It produces an exact symbolic representation of the ideal negative-sign normalized DFT target, with zero error. It does **not** establish execution of the accepted rounded serial recurrence, equality with that recurrence's rounded output, arbitrary-input deployment, full sparse recovery, practical large-N explicit output, or novelty. The companion adapter and its downstream numerical theorem require their own independent review.

## 1. What was independently checked

The complete candidate source, check source, proof, contract, README, example and existing results were read. The candidate source imports only dataclasses, hashlib and json. Production arithmetic and all serialization/control paths were inspected before execution. The supplied checks were then rerun in a separate snapshot. A fresh reviewer-written script, `independent_controls.py`, independently checked 6,880 exact transform cases, the policy specialization, exact symbolic grid alignment, endpoint resources, actual theorem-scale production and replay, and malformed or forged packets. All 69 named controls passed.

Historical Python was neither imported nor executed. The exact accepted all-length policy report was read as inert text from a locally available body and independently SHA-256 matched to `7153cde50511545ea2b63b3ab7a67efc0b7222ba0b96c1ef76d1612635564062`. Its stated original target, phases, block map, policy equations and scale conventions agree with the specialization below. The earlier bounded policy Python was also inspected as inert source for correspondence only. This review does not claim a new remote source fetch or historical execution attestation.

The candidate's nine listed payload files match its supplied manifest byte-for-byte; see `CANDIDATE_MANIFEST_VERIFICATION.json`. The manifest is an integrity list, not an authentication signature. Fresh candidate test results are preserved separately from the original candidate snapshot.

## 2. Original input and target proof

The admitted original input is exactly the schema-defined sparse object: entries [j,u,v] mean x_j=(u+i v)2^-F, and every omitted coordinate is zero. The code checks exact built-in types, sorted unique indices, nonzero listed coordinates, support contained in {0,N/4,N/2,3N/4}, bounded integer widths, and the canonical common-grid condition that at least one numerator is odd. Empty support requires F=0. Thus no hidden dense vector, unevaluated callback, omitted-coordinate uncertainty, or duplicate-summation convention is being treated as free data. This is a different restricted input representation, not a claim to have scanned an arbitrary dense N-vector.

The accepted phase definition is r_(b,t)=a t(t-1)+2(a s_b+beta)t+h t modulo 2N, with block summary d_b=sum S_(b,t)x_(s_b+t) and expansion (Px)_(s_b+t)=conjugate(S_(b,t))d_b. For B=N every block has length one and t=0, so its phase is one. Consequently P is exactly the identity, independent of the admitted a and beta. No additional block normalization is introduced.

Let c_l be the Gaussian integer numerator at lN/4, with c_l=0 for missing support. Then

    (U_N P x)_j = 2^(-F-m/2) sum_(l=0)^3 c_l (-i)^(j l).

The code's four pairs are precisely the four Gaussian-integer sums in this formula. The roots and Cartesian multiplication signs were checked directly. Even m makes N^(-1/2)=2^(-m/2) exactly dyadic. Therefore the returned period, indexed by j mod 4, and value_exponent=-F-m/2 denote all N ideal target coordinates exactly, with error zero.

The four-point Fourier matrix is invertible. Nonzero admitted input cannot give an all-zero period, and the code checks this invariant. Since P is identity throughout this family, original zero and projected zero coincide; a distinct nonzero projected-zero branch does not exist here. The zero branch returns `EXACT_INPUT_ZERO`, no numerical payload and no declared precision. Its replay result correctly does not claim a nonzero target certificate.

An exhaustive 6,560-case control covered every nonzero four-coordinate Gaussian sign pattern with components in {-1,0,1} at N=4. Another 320 independent random canonical cases covered every even m=2,...,64. The oracle used separately expanded real 4x4 character formulas, not the producer's root table or helper functions. Exact Parseval identity sum |period_l|^2=4 sum |c_l|^2 was also checked. Candidate controls separately enumerated full small-N Fourier sums. These finite checks corroborate the universal algebraic argument; they do not replace it.

## 3. Precision and formal fixed-point grid

For admitted N, L=lcm(2N,4)=2N and Phi_(2N)=X^N+1, so D=N. Each nonzero singleton block polynomial is u+vX^(N/2), already reduced. Its original aggregated l1 mass is |u|+|v|. Selecting minimum mass A with index tie-breaking over the explicit support therefore exactly matches the accepted policy's selection over all N singleton blocks. Missing blocks are identically zero.

The exact specialization is

    K=ceil(log2 A)=bit_length(A-1),
    G=W+(N-1)K,
    H=min(binomial(2N-1,N),2^0)=1,
    C=64*N*2^N*N^2=2^(N+3m+6),
    c=N+3m+6,
    p_min=max(W,c+t+1,c+q+G+2),
    I=N+2m+10.

All these formulas agree with the inspected original report. The symbolic pair C_factor=(1,c) is an exact representation of C; no giant power or binomial is evaluated. The code accepts the minimum p or an explicitly supplied larger admissible p, and rejects insufficient precision. It checks t>=0 and q>=m. Caller p and selected p must fit the stated 128-bit magnitude cap.

The output uses formal integer numerators

    period[j mod 4] * 2^(p-W-m/2)

on the grid with kappa=W-F-p. The common shift is nonnegative. Adding its exponent to kappa gives -F-m/2 exactly, so this formal p-grid representation equals the ideal output. A Cartesian period numerator has bit length at most W+2, hence the formal numerator width is at most p+2-m/2<=p+1<=p+I. This is a compressed representation of the exact integer, not a claim that its expanded bits have been allocated.

Exact expansions were used only in bounded small-domain reviewer controls. At N=2^64 the reviewer also tested maximal 1024-bit original numerators, F=±(2^128-1), and caller p=2^128-1. The recorded data width remained at most 1026 bits. Large exponents stayed symbolic.

The accepted serial radius C*2^kappa is retained as an additional correctly derived permissible bound. The new direct producer's actual error is independently zero. Its correctness is not inferred from having run the serial algorithm, and the output field explicitly denies bit equivalence with that algorithm.

## 4. Actual theorem-scale result

The reviewer executed the pinned source at N=B=2^28=268435456, a=1, beta=0, canonical delta_0 input with F=0, t=16 and q=464, and independently replayed the result against that original context. The actual result is

    period=((1,0),(1,0),(1,0),(1,0)),
    value_exponent=-14,
    p=268436013,
    c=268435546,
    kappa=-268436012,
    common_left_shift=268435998,
    formal_numerator_bits_max=268435999,
    accepted_serial_radius=2^-466,
    actual target error=0.

Thus y_j=2^-14 for every coordinate, ||y||_2^2=2^28*2^-28=1, and U_N y=delta_0. This is an actually computed symbolic producer instance, not an explicit 268-million-entry allocation. The producer receipt reports 155 metered integer operations and maximum metered integer width 30 bits. The independent traced execute-plus-replay operation peaked at 23,172 Python-traced bytes; the entire reviewer process peaked at 14,848 KiB RSS on this host. Those are observations only, not formal memory or runtime guarantees.

For the companion adapter's identity-period interface, a period identically (1,0) forces c_0=1 and the other three c_l=0 by inversion of the four-point transform. For arbitrary admitted F, alpha=2^-F is therefore exact, positive and equal to the target norm. Dividing gives the same constant 2^-14 source, and the displayed serial radius divided by alpha is 2^-466 in the default fixture. This producer-side implication was communicated to the adapter worker. It establishes no downstream window, bucket or recovery conclusion by itself.

## 5. Binding and rejected forgeries

Replay takes the separately retained raw input, state, t, q and optional caller p. It canonicalizes the bounded supplied packet, freshly executes the entire producer on that retained context, exports the expected packet and compares the complete canonical bytes. Equal canonical objects give equal exact output and policy for that retained context. The raw hash is only a label; collision resistance is not the semantic argument.

Independent controls rejected output-period, value-exponent and common-grid changes, a wholly recomputed alternative-input packet, and even a different valid phase state yielding the same ideal target. That last test confirms that original context itself remains bound. A larger explicitly supplied p replays only when the caller separately supplies that same expected p. Boolean/integer substitution cannot exploit Python's True==1 equality because typed canonical serialization distinguishes them. Extra attestation fields and oversized/cyclic packet structures are rejected.

The frozen run contains immutable tuples and bytes. Mutating original lists after execution or decoded context/packet copies cannot modify it. This assumes a correct unmodified Python interpreter, standard library and pinned source, and no concurrent input mutation during validation or hostile reflection/monkeypatching. It is not a sandbox or code-authentication protocol.

The bound context is whatever original context the caller independently supplies. An adversary replacing both the original context and answer changes the statement checked. The verifier correctly reports `external_origin_authenticated=false` and `historical_execution_attested=false`. No stronger provenance claim is accepted.

## 6. Resource and failure assessment

Production loops inspect at most four input entries and four output residues. Serialization is bounded by exact types, tree size/depth, container sizes, integer widths and a conservative byte budget. There is no loop sized by N, p, D or a support radius, and no production shift by p, C's exponent or |F|. The only length construction in the fixture is 1<<28. Giant symbolic p-grid or C values never become physical integers.

The receipt's schoolbook arithmetic envelope, additional bounded control/serialization envelope and cumulative logical storage charge are conservative for successful admitted executions under the declared binary model. They are not CPU-time, Python heap, peak RSS or availability guarantees. Input ingestion outside the API, source loading, repeated packet exports, consumer decompression and downstream operations remain separately chargeable. In particular, the public packet export's separate 2^70 bit-work and 2^42 storage envelope must be added when used; replay includes its own export and full execution. A composition wrapper must also pay source-load/pin checks and all consumer work. The adapter worker has stated that it does so; this review accepts only the producer-side accounting.

Grammar, domain, resource, precision and invariant failures raise exceptions rather than returning a numerical certificate. Host allocation failure likewise cannot become successful execution. Rejected malformed caller objects do not receive a successful-run resource receipt. The reviewer checked odd m, out-of-range m, nondyadic N, invalid support or state, noncanonical dyadic inputs, width overflows, insufficient/invalid p/q/t, serialization limits, and zero-with-precision rejection.

## 7. Final scope and handoff

No blocking producer defect was found. The accepted artifact is the restricted exact ideal-target producer and caller-relative semantic verifier at the pinned source. The successful N=2^28 result and its zero error can be used as a producer premise for a separately reviewed compatible adapter.

This is not acceptance of the rounded serial backend at theorem scale, a change to the old bounded backend's caps, an arbitrary-input or all-size implementation, an explicit N-row/p-bit expansion, a downstream BUCKETS theorem, full sparse recovery, original-input Fourier recovery, historical provenance or novelty. No external writes were made during this review.
