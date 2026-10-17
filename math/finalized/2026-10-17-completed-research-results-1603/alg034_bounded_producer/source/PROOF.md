# ALG-034: executable producer binding and semantic verification

17 October 2026. Final-stage candidate, subject to independent check.

## 1. Exact goal and completed scope

The specific previously open gate was: bind the original finite exact common-grid input to the accepted all-length zero/precision policy, execute the genuine specified serial producer at that selected precision, bind its exact output to a compatible adapter, and reject fabricated payloads even when an adversary recomputes every editable digest.

This packet implements that composition. It does not claim a new precision theorem. The already accepted theorem and policy remain unchanged. `producer.execute` is the new actual entrypoint, and `producer.verify` is a paid semantic replay verifier. Neither accepts an upstream attestation or caller-supplied output as proof that a producer ran. A nonzero successful output has been calculated directly from the checked original arguments. A replay-verified payload is equal, coordinate by coordinate and on the exact grid, to a newly calculated correct output.

The implementation is bounded: N<=64, raw Cartesian numerator width<=1024, selected p<=4096, the inherited strict metadata/JSON caps, at most 4,000,000 metered integer operations and at most 100,000 working-integer bits. These are explicit implementation resource restrictions, not changes to the all-size mathematical theorem. A resource failure is not a proof of impossibility or an accepted result. A successful nondyadic-length result returns the correct producer payload and an explicit legacy-adapter length exclusion.

The pinned bounded adapter is invoked on the actual fresh output for dyadic lengths. A real reviewed BUCKETS component call is also demonstrated at its valid N=64 reduced-component domain. A theorem-scale sparse Q16 integration is not claimed; Section 9 proves why the retained legacy cap rules out every such instance.

## 2. Sources and what is new

Reviewed source dependencies copied unchanged:

- `policy.py`: accepted bounded binding checker aa6863c524d69a1433bb4298cdc63092a4e7dd869f857356689bc2cbc0612d27. Its exact input/state/cyclotomic policy implementation is reused, not re-credited as a new theorem.
- `vendor/paid_source.py`: accepted bounded adapter 5cd35d6b3dc1dd6b077db3f1b957cbf4794479aa1b0e592008edf83fa5216d2b.
- `vendor/buckets.py`: accepted component df3937a632217a8a1342545b803169ff8da062117b3837796386509b64f650d1.
- `vendor/compact_window.py`: accepted component e29741e71c276c156d708f1d9dce6d60ff9d3d2c34a6045b03630c46506dac59.

All dependency text was inspected before execution, including imports, top-level definitions and complete numerical bodies. The adapter loader checks exact file SHA-256 and resolves its two accepted module identities in order. It refuses a conflicting existing module. The tests also check the reviewed import/top-level grammar. This is a trusted source execution model, not a sandbox for hostile Python. No historical test program, historical ALG-034 producer, network client, subprocess or archived executable is run. The reviewed legacy adapter and BUCKETS numerical component themselves are deliberately run; claiming that no historical code ran would be inaccurate.

Fresh work: `producer.py`, intended-root integer interval construction, finite inverse-square-root construction, exact-grid implementation of all accepted serial stages, live input/output composition, replay verification, resource/range guards, and fresh `checks.py` with an independent direct interval-DFT oracle.

Accepted antecedents:

- All-length policy: https://github.com/AgentSlop-Si/research/blob/acd8db5e6ad4660fb63ce1f2c63ee45577d454f0/math/finalized/2026-10-16-research-finalization-1458/all_length_policy/REPORT.md ; SHA-256 7153cde50511545ea2b63b3ab7a67efc0b7222ba0b96c1ef76d1612635564062.
- Serial theorem report: SHA-256 8dcc83d64316a136cb482fd04cff81ebaf7bf2351ab61fec1f02d8eadaf81cf8 in https://github.com/AgentSlop-Si/research/blob/35d9dcdc3f3869de75b33b2b09705222e8d09e8d/math/reviewed_rounds/2026-10-13-reviewed-1354/archives/ALG034_Fixed_Point_Precision_Contract_Independent_Review_2026-10-13.zip . Its independent acceptance is 31820fc28ff120f5982d4be0a03922600f06c3b7fb1a707b2617ae6e65201bf4.
- Adapter archive: https://github.com/AgentSlop-Si/research/blob/35d9dcdc3f3869de75b33b2b09705222e8d09e8d/math/reviewed_rounds/2026-10-13-reviewed-1625/archives/ALG034_Q16_Bounded_Paid_Source_Adapter_Independent_Acceptance_2026-10-13.zip ; SHA-256 1ea2f4ce8db36d0f7e13141e8c1e679cf02e552f2054afe84a0dbda738ea5797.

## 3. Program model, input and provenance

Original input is the separately supplied exact built-in `raw={F,real,imag}` and canonical state `{N,B,a,beta}`. No float, bool-as-integer, custom numeric/container object or callback is accepted. The original arrays are scanned and copied before computation. Their actual W, zero state, value identity and grid identity are recomputed. Canonical state fixes balanced longer-first blocks, gcd, parity and output frequency order.

The trusted program model consists of the running interpreter/standard library, the reviewed code, correct integer arithmetic, unmodified dependencies, no concurrent mutation while validating arguments and no hostile reflection/monkeypatching. The user/caller must supply the original context to be certified. No algorithm can authenticate an unknown external source merely from a self-contained record; a malicious party replacing both original context and claimed answer changes the statement being checked. The API explicitly reports `external_origin_authenticated=false` and never claims historical remote execution attestation.

After validation, Run is frozen and contains immutable input/policy/trace/ledger bytes, an immutable payload tuple, and the legacy adapter's deeply immutable source. Later mutation of the caller's list or a returned decoded policy/packet does not alter Run.

The numerical conclusion is bound to the actual supplied original input. The input hash labels that context, but its cryptographic strength is not needed for semantic payload comparison: replay compares canonical exact full content and recalculates the whole result. Source pins detect file replacement; they are not treated as proof that an earlier execution happened.

## 4. Exact policy and zero distinctions

The unchanged accepted policy computes the full cyclotomic prepass with L=lcm(2N,4), actual odd parity, block polynomials, exact monic remainders, minimal original aggregated nonzero mass A and block-order tie break. It derives D, K=ceil(log2 A), G=W+(D-1)K, H=min(binomial(N+B-1,B),2^(N-B)), C=64 H B 2^B N^2 and c=ceil(log2 C).

For integer t>=0, q>=ceil(log2 N), actual p must satisfy

    p >= max(W,c+t+1,c+q+G+2).

The entrypoint chooses this minimum unless the caller explicitly supplies a higher admitted p. A record cannot secretly select another p. For dyadic N, the default q is 16 log2 N+16; otherwise it is ceil(log2 N).

EXACT_INPUT_ZERO and EXACT_PROJECTED_ZERO stop before producer/normalization and return no adapter payload. The latter is never relabeled as original zero. On NONZERO_PLAN the actual output must be nonzero; a zero result is an invariant failure, not silently accepted. The all-length policy's proof already supplies nonzero separation and one-shot target-budget slack, so no retry policy is introduced.

## 5. Intended roots and inverse square root

### 5.1 Pi interval

At guard grid S=2^K, with K=p+32+2 ceil(log2(p+64)), compute n=p+32 terms of atan(1/q), q=5,239. For each positive magnitude 1/((2j+1)q^(2j+1)), integer floor/ceiling times S enclose the exact term. Alternating summation uses interval endpoints in the correct order. The alternating-series remainder has the next term's sign and magnitude at most that term; the code enlarges only that endpoint by its ceiling. Machin's identity pi=16 atan(1/5)-4 atan(1/239), with interval subtraction reversing endpoints, therefore produces a true intended pi enclosure. The exact guard 3S<lo<=hi<4S is checked.

### 5.2 All 2N intended roots

For every r=0,...,2N-1, divide r times the pi enclosure by N using outward floor/ceiling. Thus the angle interval contains exactly pi*r/N and lies in [0,8). Exact quadrant phases are returned exactly.

For other r, recursively enclose theta^k/k! on the same guard grid: multiply the nonnegative previous interval by the nonnegative angle interval and divide by S*(k+1), rounding outward. This is an inclusion-preserving induction. Sum the terms by k mod 4 into cosine and sine intervals through degree d=p+64. Taylor's theorem bounds each coordinate's omitted remainder by 8^(d+1)/(d+1)!; its guard-grid ceiling is added to both endpoints. No approximate root equation or rounded-power identity is used.

Round the midpoint of each resulting component interval to the p-grid by signed nearest-even. If er and ei are the maximum guard-grid distances from that chosen center to the two endpoints, check

    er^2+ei^2 <= 2^(2(K-p)).

By containment, this proves complex error at most 2^-p from the intended exponential. This exact admission test is sufficient for every successful run independently of how pessimistic the intervals are. If it ever fails, the entrypoint returns no certificate; the bounded implementation does not rely on an unproved assertion that all finite guards always succeed. It runs a finite predetermined number of terms and does not retry. All 2N roots are prepared once per actual run and indexed by exact reduced integer phase exponents.

### 5.3 Normalization scalar

At K=p+16 compute the integer square root h=floor(sqrt(floor(2^(2K)/N))) using a predetermined greedy bit loop. Hence h/2^K <=1/sqrt(N)<=(h+1)/2^K. If h^2*N=2^(2K), use the exact endpoint instead. Round the midpoint to p-grid and check maximum endpoint distance<=2^(K-p). This proves absolute scalar error<=2^-p. Every shift, product, division and square-root trial is metered.

## 6. Implementation-to-theorem correspondence

Represent every normalized complex grid value as pair of integers times 2^-p. Let e=W-F. Loading multiplies original numerators by 2^(p-W), losslessly because p>=W. The final payload exponent is exactly kappa=e-p, with no physical shift by |F|.

`Fixed.mul` forms both complex Cartesian products using exact integers, and rounds each once to nearest p-grid. Signed ties-to-even is a permitted nearest rule; its coordinate error is at most 2^-p/2 and complex error at most 2^-p. Add/subtract/conjugation and summations are exact. `Fixed.half` performs the single specified half-sum rounding.

The `serial` body follows accepted stages literally:

1. d: round each compression phase times loaded x, then sum exactly per actual block.
2. w: subtract the single rounded preceding endpoint-phase times preceding d, cyclically.
3. Q: factor-by-factor updates, each old coefficient minus one rounded lambda-times-prior coefficient; constant coefficient exactly one.
4. s_0,...,s_(B-1): direct sums of rounded w_b times independent table entries at -2*s_b*k.
5. s_B,...,s_(N-1): negative exact sum of B individually rounded coefficient-times-earlier-source products.
6. f: one rounded rho*s per position.
7. Gauge: independent table entries with exact accepted parity/exponents; rounded conjugate-gauge*f in a-cycle order, exact full sum and prefixes, one half-sum rounding, one final gauge multiplication, frequency-index output permutation.
8. Return exact row integers with symbolic kappa.

No FFT, iterated rounded phase powers, altered product rounding, uncharged output rounding or normalization by block length is substituted. Every stored/partial-sum grid component is checked below 2^(p+I), I=B+2 ceil(log2 N)+10. Both exact multiplication accumulators are checked below 2^(2(p+I)+3), fitting the accepted signed double-width allowance. All these checks operate at actual p.

The accepted theorem therefore applies to every successful nonzero run:

    ||Yhat-U_N P_(a,beta)x||_infinity <= C*2^kappa
                                      <= 2^-t ||x||_2.

Here P is the phase-weighted block map without an extra 1/block_length, and U_N is the negative-sign unitary DFT. The accepted one-shot policy also guarantees the genuine output is nonzero and gives the normalized target-budget allowance at its declared q.

## 7. Actual adapter and semantic soundness

For dyadic N the actual returned immutable payload is passed directly to the reviewed pinned `adapt`; no separately supplied approximation intervenes. Its 17-field certificate is constructed inside the successful execution from actual raw F/W/state, actual selected p, exact C and actual output digest. The literal premise is consequently discharged by Sections 3–6, rather than accepted as a caller claim. The legacy conditional label remains unchanged; the wrapper supplies its antecedent.

The adapter checks its original grammar/caps, actual numerator widths, metadata, exact error inequality, output digest, normalization, requantization and final strict norm. Actual caps are not relaxed. A failed sufficient p+I width bound would not itself establish overwidth. The adapter's actual width scan is authoritative.

`verify(raw,state,t,q,packet,p)` bounds the untrusted packet, recomputes a fresh run without adapter, and compares the entire expected semantic packet to the supplied packet byte for byte in deterministic typed canonical form. Equality of serialized exact integers implies actual same input/state/plan/grid/output. Hence any accepted nonzero packet is numerically correct for the separately supplied original input under the same theorem. Recomputing attacker-editable hashes cannot cause unequal payloads to pass. Extra self-attestation fields are rejected by exact grammar. Replay proves present numerical validity, not historical execution provenance, and is fully paid as another run.

The verified producer and adapter cannot authenticate or infer an external original data source that the caller did not supply. That is a general trust boundary, not the former missing arithmetic/I/O implementation.

## 8. Resource contract and cumulative accounting

No machine-time, host-memory availability, all-size practical runtime or speed improvement is claimed. Resource exceptions produce no partial success certificate. Big integer allocation/runtime failure also is not numerical success.

The reused policy uses the accepted finite exact setup/prepass. `policy_cost_envelope` pays a deliberately oversized schoolbook envelope on every call, including warm-cache calls. With conservative L=4N, T0=L^2+3L+4, S=W+T0+4N+32 and V the metadata-width envelope, it charges 2^20 times

    (L+1)^4(T0+1)^2
      +(N+B(L+1)^2)(S+V+1)^2
      +4 MiB*(8192+V)^2.

The first term dominates at most L^2 monic divisions, each at most L^2 integer multiply/add/control actions, at the accepted T0 temporary width. The second pays all input copies/scans, phase/gcd work, block reductions and bounded planning; the third pays the inherited bounded canonical tree/hash serialization and small metadata arithmetic. The huge constant deliberately absorbs bounded elementary-control actions, exact binomial construction, source movement and bit-length operations; it is not an empirical performance estimate. Full retained polynomial/trace storage is charged conservatively by the accompanying envelope. The local N and metadata caps are essential to this explicit deployment envelope.

Every root/inverse-square-root and fixed-grid arithmetic operation is recorded by Meter with operand/output widths. Integer add/multiply/divide/shift are charged 128*(sum widths+8)^2 schoolbook units. The control/storage envelope 4096*events*(maxwidth+log2(events)+16)^2 pays loop/index/modulo expressions, comparisons, signs, range checks, Python-free logical allocation/copy bookkeeping and fixed formulas. Direct phase/index arithmetic has O(log N) bounded operand widths; it is absorbed conservatively. Stored values, all roots, prefixes, exact partial sums, transient products and cumulative produced integers are included.

The cumulative successful-run receipt adds policy, producer, legacy adapter receipt, dependency-file reads/hash costs and their storage envelopes. No root cache is reused across actual producer calls. `verify` pays its own full recomputation; combine its returned work bound with the original execution if both are performed. The demonstrated BUCKETS fixture explicitly adds its preparation/run ledger to the complete upstream total. Trace/context/policy serialization and a 64 KiB ledger reserve are charged explicitly by emitted-byte/observed-width envelopes; dependency reads, parsing and loading are charged by a separate deliberately oversized quadratic byte envelope. Replay additionally charges two policy envelopes for the untrusted packet validation and expected packet serialization/comparison. Repeated later calls to packet() are additional exports, not free preprocessing; each can conservatively be charged another policy envelope. Trace construction is diagnostic and not an uncharged source for downstream queries. Files/tests and the independent oracle are validation costs, not included in a production runtime claim.

The inherited arithmetic-stage count remains O(NB+B^2+N), plus fully paid exact policy, roots, checking, copying, normalization, output and any downstream preparation/calls. It is not a sub-FFT claim.

## 9. Exact downstream stopping boundary

For the retained legacy adapter N<=4096. A theorem sparse Q16 instance requires beta_Q>0 and

    k=2^ceil(2 beta_Q m), B_Q>=4096k, B_Q<=N.

Since m>=2, beta_Q>0 implies ceil(2 beta_Q m)>=1, so k>=2 and B_Q>=8192>N. No instance can satisfy both interfaces. The stronger compact-window/divisibility and outer guards only reinforce this obstruction. It does not depend on benchmarks, difficulty judgments or novelty uncertainty.

The actual N=64, B_Q=4, r=1, Pq=112 fixture is a valid standalone BUCKETS component input and demonstrates real class/adapter execution, but beta_Q=None explicitly makes it a reduced component fixture, not the E(beta_Q) theorem regime. It cannot stand in for full sparse-recovery integration.

For that wider goal, the precise next dependencies are a widened and separately reviewed producer deployment beyond this entrypoint's N<=64 cap, a separately reviewed cap-compatible source adapter/representation beyond the retained N<=4096 cap, and a valid downstream instance retaining all sparse/window/schedule/tolerance guards. The accepted mathematical producer theorem itself is already all-length; this is an implementation/deployment boundary. Original-input Fourier recovery also cannot be inferred from this composition: the second ideal target remains R P x/alpha, with R[j]=(-j mod N), not U_N x. Sampling/projection error and full recovery are independent owner goals.

## 10. Why this task can stop

After independent acceptance, the requested bounded original-input→policy→genuine serial producer→actual payload→legacy adapter gate can be closed. Fresh implementation, implementation correspondence, exact semantic verifier and independent numerical/direct-target tests supply the previously missing evidence. Re-running consistency audits is no longer useful for this gate.

ALG-034 as an unrestricted/full-recovery owner must remain open only for its separately stated goals: cap-compatible theorem-scale downstream integration, broader deployment/all-size interfaces, any claimed fast backend or full recovery, and their actual resource guarantees. Those are not prerequisites for the proved bounded gate, and this task does not expand indefinitely to solve them. No Sheet/GitHub mutation, owner-priority change or novelty assertion occurs here.
