# ALG-034 executable-binding source audit: independent review

17 October 2026

## Verdict

**ACCEPT the narrow source-audit checkpoint. No required scientific repair.**

The inspected sources do not supply the composition that binds exact original input, the accepted zero/precision policy, genuine specified serial arithmetic, and the exact returned payload. This is a verified evidence gap within the inspected source set. It is neither a theorem of implementation impossibility nor a search claim about every newer source elsewhere.

The audit is complete. The implementation-evidence gate remains **BLOCKED_ON_BOUND_IMPLEMENTATION_EVIDENCE**. ALG-034 remains **TO RESEARCH, priority 48**. The already accepted all-integer-length exact-dyadic policy must not be reopened, recounted as new mathematics, or dispatched for another proof of the same precision formula.

## Objects and method

I independently read the final report and nine-item obligation map, the accepted all-length report and acceptance, the serial-producer report and acceptance, and the bounded adapter's contract and acceptance. I independently checked the supplied archive lengths and content identities, matched relevant program copies to their exact archive members, and parsed all eight archived Python members as syntax trees. Direct source reading establishes the semantic conclusions below; syntax-tree checks corroborate interface and call relationships.

No archived or candidate program was imported or executed. No numerical tests were rerun. The only executed checking logic was freshly authored standard-library byte, identity, archive-member and syntax inspection. No remote file, native owner record, repository or permission was changed. This review does not claim a fresh audit of live native owner state.

## Verified call relationships and trust boundary

### 1. Normalized reference arithmetic

In `checks/fresh_controls.py`, `main` creates fixtures and invokes `fixed_producer` and a separate `oracle`. `fixed_producer(x,n,b,a,beta,p)`, lines 83–116, expressly receives already normalized exact dyadic input.

Its root path is `root_fixed` → `root_box` → `pi_box` → `atan_mid_rad`. Its rounded complex products use `mul` → `rc` → `rnd`. It obtains the longer-blocks-first partition, computes the actual parity-aware compression and boundary phases, constructs recurrence coefficients, forms direct seeds, advances the serial recurrence, applies inverse-square-root scaling, and performs the gauge half-sum/prefix scan in frequency-index order. Its returned object contains the intermediate arrays and normalized output.

There is no raw common exponent argument, raw numerator-width scan, accepted cyclotomic-policy call, original-input receipt, symbolic raw-output rescaling, or downstream-adapter call in this entry point. The reference arithmetic is real source evidence, but these absent composition steps cannot be supplied by its normalized-input docstring or its fixture caller.

### 2. Fixed-reference independent controls

In `checks/independent_controls.py`, `main` invokes `pipeline(n,b,a,beta,W,t,seed)`, lines 80–137. That function constructs its own numerator fixtures at lines 84–87 and derives its precision internally. It receives neither arbitrary original input nor its common exponent.

The integer numerical path uses `approx_root` → `root` and `imul` → `nearest`; an interval path checks the projected transform separately. The reference scale is the module-global `G=224`, and the code explicitly uses shifts by `G-p` in the pipeline and root conversions. Thus this file does not expose an arbitrary-precision producer API as written. This is a static source conclusion; no failing run was performed or claimed. Its return value is a diagnostic summary, not a bound payload and production certificate.

### 3. Bounded adapter

In `paid_source.py`, `adapt(payload,certificate)`, lines 179–278, receives a three-part output payload and a 17-field declaration. The source performs substantive exact checks: built-in grammar and caps, matching length, dyadic state constraints, exact reconstruction of C, precision and symbolic-exponent consistency, a complete dense payload scan, canonical output digest, exact norm, signed requantization and immutable source construction.

Its nonzero return constructs `DyadicSource`; it does not invoke an ALG-034 producer, cyclotomic prepass, `BucketEngine`, window preparation or a downstream recovery pipeline. The imported source-record dependency does not supply those missing calls. The independent adapter tests manufacture explicitly synthetic declarations and then call `adapt`; they therefore cannot witness an authentic upstream producer run.

The original input digest is checked only for its text encoding. The original input itself is absent. `ProducerContract` explicitly records that it does not authenticate its assertions, and every result carries conditional upstream soundness. The input contract expressly requires a genuine accepted producer contract applying to this exact payload. A matching output digest checks serialization consistency; it does not prove the missing input-to-output relationship.

## Obligation-map assessment

The nine items correctly retain the missing raw-input, state, zero-policy, precision-plan, producer-correspondence, payload-binding, bounded-adapter, downstream and alternate-backend evidence. They are an intake checklist, not an implemented semantic verifier.

For a future implementation, the acceptance chain must establish all of the following:

1. Scan exact original integer components and signed common exponent, derive actual W and original-zero state, validate canonical state and preserve the same input throughout the run.
2. Bind the actual exact prepass to that input/state, keeping original-input zero, projected zero and zero approximation distinct. The previously accepted smaller-field dyadic specialization remains available where applicable.
3. Bind the nonzero plan, including integer nonnegative t, integer q at least ceil(log2 N), and actual integer p satisfying the accepted inequalities, to the actual selected precision and same input/state.
4. Establish implementation-to-theorem correspondence for intended roots, inverse-square-root enclosure, lossless loading, exact indices and sums, rounding, all stages, range, symbolic rescaling and the exact returned grid payload. Alternatively, provide a separately proved and paid semantic trace/certificate verifier. A receipt's shape is insufficient.
5. Preserve the existing adapter's actual dyadic length, numerator-width, grammar and metadata restrictions, then separately establish real downstream eligibility, allowance and cumulative costs.

The report correctly preserves these consequential limits:

- The adapter has no exact-projected-zero status. A nonzero original input with zero projected signal cannot use its exact-original-zero branch.
- Failure of the sufficient bound `p+I<=65536` does not prove actual numerator overwidth. The actual payload and metadata remain subject to the unchanged caps.
- The fixed producer's p is fractional grid precision, not ordinary floating-point significand width.
- A different or fast backend still needs its own seed, coefficient and recurrence-defect bounds, including `H(Delta_Q+r1)<1` or another valid stability argument. The existing conditional inequality is not evidence that a chosen backend satisfies it.
- Root work, policy construction, production, validation, copying, normalization, downstream work and outputs remain cumulative. No machine-word speedup follows.
- The second ideal target remains `R P x/alpha`. No original-input Fourier recovery or theorem-scale sparse Q16 instance is established by the capped adapter.

## Precise closure recommendation

Record this current child audit as **COMPLETE_SCOPED_PRODUCER_BINDING_SOURCE_AUDIT** and archive only duplicate dispatches of this same source-gap review. Retain the separate unresolved condition **BLOCKED_ON_BOUND_IMPLEMENTATION_EVIDENCE** and retain ALG-034 **TO RESEARCH / 48**.

Suggested concise checkpoint text:

> Independent data-only source audit complete. The accepted all-length exact-dyadic zero/precision policy is retained. The inspected reference producer, fixed-scale independent controls and conditional bounded adapter do not establish an original-input-to-actual-payload composition. Resume this gate only with a named bound implementation or separately verified semantic evidence; preserve all existing adapter, downstream, target and cost restrictions. ALG-034 remains TO RESEARCH, priority 48.

This closes the audit question, not the missing implementation, downstream integration, full owner, novelty review or resource claims. Any native synchronization or publication is a separate parent action.
