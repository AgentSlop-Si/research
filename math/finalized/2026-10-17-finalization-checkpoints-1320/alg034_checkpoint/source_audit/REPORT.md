# ALG-034: exact remaining producer-binding gate

17 October 2026. Read-only source audit; no mathematical promotion.

## Result

The all-integer-length exact-dyadic projected-zero, separation and one-shot precision policy is already independently accepted. It must not be redispatched as an unresolved numerical lemma. The existing ALG-034 parent remains TO RESEARCH, priority 48.

The next unresolved contract is an actual raw-input-to-payload implementation binding the accepted policy to the accepted serial producer. The verified sources include reference producer code and a bounded downstream adapter, but their interfaces do not establish this composition. This audit records the precise missing evidence; it does not claim that no newer implementation exists elsewhere.

## Accepted source identities

- S1: all-length policy report, SHA-256 7153cde50511545ea2b63b3ab7a67efc0b7222ba0b96c1ef76d1612635564062. [Immutable report](https://github.com/AgentSlop-Si/research/blob/acd8db5e6ad4660fb63ce1f2c63ee45577d454f0/math/finalized/2026-10-16-research-finalization-1458/all_length_policy/REPORT.md).
- S2: its [independent acceptance](https://github.com/AgentSlop-Si/research/blob/acd8db5e6ad4660fb63ce1f2c63ee45577d454f0/math/finalized/2026-10-16-research-finalization-1458/independent_review/ALG034_REVIEW.md).
- S3: serial precision archive, SHA-256 6381acc0cf5bf6aff7af69b645f77462026fa92949d7d685abaf0c5f523fc4b2; 59,410 bytes. REPORT.txt has SHA-256 8dcc83d64316a136cb482fd04cff81ebaf7bf2351ab61fec1f02d8eadaf81cf8; INDEPENDENT_REVIEW.txt has SHA-256 31820fc28ff120f5982d4be0a03922600f06c3b7fb1a707b2617ae6e65201bf4. [Immutable archive](https://github.com/AgentSlop-Si/research/blob/35d9dcdc3f3869de75b33b2b09705222e8d09e8d/math/reviewed_rounds/2026-10-13-reviewed-1354/archives/ALG034_Fixed_Point_Precision_Contract_Independent_Review_2026-10-13.zip).
- S4: bounded adapter archive, SHA-256 1ea2f4ce8db36d0f7e13141e8c1e679cf02e552f2054afe84a0dbda738ea5797; 155,889 bytes. [Immutable archive](https://github.com/AgentSlop-Si/research/blob/35d9dcdc3f3869de75b33b2b09705222e8d09e8d/math/reviewed_rounds/2026-10-13-reviewed-1625/archives/ALG034_Q16_Bounded_Paid_Source_Adapter_Independent_Acceptance_2026-10-13.zip).

Both archives were fetched as inert bytes and their lengths and SHA-256 identities rechecked in this audit. The proof reports and relevant implementation bodies were read as text. No archive program was imported or executed. A fresh standard-library audit parsed source syntax and checked identities only.

## Exact interface gap

1. In S3, checks/fresh_controls.py, lines 83–116, fixed_producer(x,n,b,a,beta,p) expressly assumes x is already normalized exact dyadic data. It returns d,w,q,s,f,out. It has no raw common-grid exponent F input, no derivation of actual raw numerator width W, no policy decision object, no raw-input/payload receipt, and no adapter call. This is useful reference arithmetic, not the missing end-to-end raw-input entry point. SHA-256: 3e5941756a99f51f628c3d3972967374cd4e425eb9d1164dd8172305af52d5b8.

2. In S3, checks/independent_controls.py, pipeline(n,b,a,beta,W,t,seed), lines 80–137, generates its own numerical fixtures (lines 84–87). Its root enclosure uses global G=224 and shifts by G-p (lines 70–73 and 81). Its returned object is a diagnostic summary, not a raw-input payload/certificate. This source is not an arbitrary-p producer API and must not be presented as one. SHA-256: 2f7fb49c261bf8ac0beccdb6f9a8cedcc00dc068e7ca8b1e291bca5842df96a8. No failing run was performed or asserted.

3. In S4, paid_source_adapter_independent_1618/inspected_source/paid_source.py, adapt(payload,certificate), lines 179–278, receives only a proposed output and a 17-field declaration. Its actual checks reconstruct C, validate p,t,kappa and state, scan the complete output, and check its digest (lines 209–238). It has no original input or producer trace to verify. INPUT_CONTRACT.txt explicitly makes target soundness conditional on the genuine producer applying to this exact payload. SHA-256: 5cd35d6b3dc1dd6b077db3f1b957cbf4794479aa1b0e592008edf83fa5216d2b.

The missing implication is therefore:

    exact original input + canonical state + accepted policy
       -> genuine specified arithmetic at the actual selected p
       -> this exact returned grid payload and symbolic kappa
       -> valid bounded adapter input, or an explicit out-of-domain result.

A declaration string or matching output hash establishes no such implication. Merely adding more metadata fields cannot repair it.

## Data-only evidence obligations for the next implementation

OBLIGATIONS.json specifies the evidence map. It is an intake checklist, not a new acceptance theorem or implemented verifier.

- Raw input: ordinary finite exact integer arrays and common exponent; full scan establishes actual W and exact original-zero state. Bind the unchanged data to the run.
- State: validate N,B,a,beta, gcd, longer-blocks-first partition, parity term and frequency output order using exact arithmetic.
- Policy: for nonzero raw input, bind the actual cyclotomic prepass and its zero/nonzero decision to that input/state. Nonzero plans retain L,D,A,K,G,c,q,t,p and the exact accepted inequalities.
- Producer: pin exact implementation and root routine; show intended-root enclosures, lossless loading, rounding schedule, exact products/partial sums, all stages and exact symbolic output rescaling. At the actual p, charge all reached work and widths.
- Payload: derive kappa=W-F-p and the declared radius from the actual run. Establish exact payload equality. A cryptographic digest can detect mismatches but cannot substitute for this premise.
- Adapter: verify actual dyadic length, width and metadata caps before invoking the existing adapter. Its accepted scope stays 4<=N<=4096 and Cartesian numerator width <=65536, with the original metadata caps.
- Integration: prove the actual downstream instance meets its own eligibility, source-class, window, schedule, tolerance and cost requirements. The present capped wrapper covers no theorem-scale sparse Q16 instance.

A data-only checker can validate a plan and serialization, but cannot certify that a producer ran merely by checking the shape of a receipt. Full numerical acceptance requires either a separately reviewed implementation-to-theorem correspondence with actual I/O binding, or a separately proved and paid semantic trace/certificate verifier. Neither is supplied by this audit.

## Stop/pass boundaries

EXACT_INPUT_ZERO, EXACT_PROJECTED_ZERO and ZERO_APPROXIMATION stay distinct. The accepted adapter has no exact-projected-zero status: do not forge its exact-original-zero flag to transport that case. A projected-zero branch must stop before normalization or use a separately specified result interface.

Do not relax the existing wrapper caps. Failure of p+I<=65536 is failure of a sufficient width certificate, not proof of actual numerator overwidth. Evaluate actual payload widths and metadata; p is fractional precision, not ordinary floating-point significand width.

If selecting a different or fast backend, S3 section 8 leaves a genuine numerical obligation: prove backend-specific seed error, coefficient error Delta_Q, and recurrence defect r0+r1 max|shat|, including roots, padding, overlap, normalization, rounding and range, and establish H(Delta_Q+r1)<1 (or supply another valid stability proof). The conditional inequality itself is already given; no backend bounds have been newly established here.

Keep cumulative costs for zero prepass, precision planning, roots, serial production, independent checking, copying, normalization, downstream work and final output. The accepted O(NB+B^2+N) arithmetic ledger is not a machine-word runtime claim. The second ideal target remains R P x/alpha, not U_N x.

## Disposition

BLOCKED_ON_BOUND_IMPLEMENTATION_EVIDENCE, within this inspected source set. No new numerical lemma, producer execution, downstream execution, all-size adapter, speed claim or novelty claim. No parent closure, priority change, external write or active-release change.

To resume this gate, supply or create the named raw-input entry point together with its implementation-to-theorem and exact I/O binding evidence. Do not spend another cycle reproving the already accepted precision formula.

