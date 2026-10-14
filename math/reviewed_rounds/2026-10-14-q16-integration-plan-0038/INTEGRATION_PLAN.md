# Q16 production outer integration: bounded source inspection and plan

**Finding: the production outer coefficient wrapper and provenance adapter are
missing from the inspected accepted source chain.** The existing endpoint is
run_pipeline(...) -> PipelineRun(output=MedianResult(...), ...). The fresh
Reference class is a standalone regression implementation, not an existing
production adapter. No historical code was executed for this inspection.

## Bounded inspected source chain

The canonical files are the six exact modules in
observer_v2_candidate/source_bytes/. Their hashes match both its frozen
CONTRACT.json and the accepted run's source inventory. SOURCE_INTERFACE_AUDIT.json
contains full paths, hashes, definitions, fields and fixture guard calculations.

- exact_source.py: 8334e657dd0048bdb91459e5f6e126080c7513d341ef3d17665b05422a8bbada
- compact_window.py: e29741e71c276c156d708f1d9dce6d60ff9d3d2c34a6045b03630c46506dac59
- buckets.py: df3937a632217a8a1342545b803169ff8da062117b3837796386509b64f650d1
- location_decode.py: e3b592c40906d860d58c12cf7e21f17c6560cb8c95e7bcde4c161b0d52881c3a
- phase_medians.py: 45c0c6a59cac18912278dcda183fe8e5bea2a19398cb61fc1bf8ec97cac5a788
- pipeline.py: c3a2da5a11ceba2cfa0df7bbb346525013e740e7bc170b3d27dfadc3f2be4d3b

The original and recovered outer-contract directories contain specification,
proof and control-checker files, but no production evaluator/adapter. This is
bounded local absence evidence, not a claim to have searched every file or
remote repository. The accepted observer review explicitly excludes outer
coefficient generation/scatter (FINAL_REVIEW.md:116) and recommends the static
outer contract as its next gate (lines 120-126).

## Concrete existing interfaces

1. exact_source.materialize_exact(values, exponent, d) or materialize_practical
   returns SourceResult for nonzero input; fields include source, N, m, M, d,
   input_exponent, center, k0, lambda_exp, receipt (exact_source.py:42-52,
   224-254). ZeroResult is a separate branch. SourceResult supplies the original
   N and centering/scale metadata absent from PipelineRun.
2. pipeline.run_pipeline(spec, source, q, location_schedule, estimation_schedule)
   validates the exact WindowSpec and the exact shared DyadicSource class, then
   owns bucket/estimate production internally (pipeline.py:103-119,188-245).
3. PipelineRun has output, candidates, location_trace, estimation_trace, ledger,
   and bucket_error. It has no N, M, source identity, spec identity, outer D,
   run_binding or exported production capability (pipeline.py:40-47).
4. MedianResult has only pairs and bits. pairs is the sorted tuple
   (k,(real_numerator,imag_numerator)); bits is the front-end estimate precision
   P. Zero estimates are retained (phase_medians.py:18-20,203-208,235-255).
5. The internal _Context, _BoundBuckets and _BoundEstimates use object identity
   and a private capability to reject cross-run/same-valued substitutions.
   Those guards operate during run_pipeline. The final PipelineRun does not
   carry that context/capability (pipeline.py:50-78,133-185,245-246).

## Exact mismatches and missing obligations

- A public PipelineRun/MedianResult dataclass, its dict serialization or a
  matching hash is not proof that a particular execution produced it. Checking
  its class and values alone cannot reconstruct the dropped private capability.
- The outer contract needs N,M,D, a validated sorted support tuple and a
  32-byte association label bound to one actual accepted output. PipelineRun
  alone lacks the header/provenance connection needed to supply those fields.
- The new Reference constructor receives independent N,M,D,support,binding
  arguments. Its public coefficient(ell,k) does not validate that the pair was
  issued by its enumerator or belongs to that support. Its mutable attributes
  and arbitrary fixture label are unsuitable as a production provenance gate.
  This does not invalidate the frozen three valid test records already checked.
- Front-end q is the selected-bucket count; outer q is floor(M/(8s)). Front-end
  P differs from outer p=(D+3)m+3. Input d differs from outer D. A production
  interface must keep these distinct rather than forwarding same-named fields.
- The accepted compact-window even_power rejects odd exponents. It cannot be
  used unchanged for outer s=Dm. Scalar may be reused only with its exact pinned
  source/API and a reviewed wrapper; acceptance of the old component does not
  authenticate new calls or bookkeeping.

## Why the existing accepted fixtures cannot close this integration

At D=5, t=160m+4. The accepted N=1,M=4 fixture has t=324; N=9 or 16,M=64
has t=964; N=17,M=128 has t=1124. Every one fails t<M, including the nonzero
consumer cases. A correct outer adapter returns OUTER_DENSE_REQUIRED before
scalar preparation for these metadata. Replaying them cannot exercise sparse
outer coefficients or the m=57 odd/minimum-residue path.

The materialized constructor and existing DyadicSource require an M-entry
represented source. It would be inappropriate to run the m=57 regression by
materializing 2^57 cells or fabricating a PipelineRun and calling it accepted
front-end output. The large fixture must remain a bounded coefficient-kernel
test; live provenance integration is a separate finite control.

## Implementation-ready plan (proposed files do not yet exist)

### A. Define the controlled handoff without changing accepted module bytes

Propose a new driver-owned adapter, for example pipeline_outer_adapter.py.
The name is a proposed destination, not a discovered file. It should retain the
actual SourceResult, WindowSpec, exact module identities and the actual return
of a run_pipeline call made by that driver. The trusted driver then issues a
private immutable outer context tied by identity to that returned object,
its source/spec/header and an unforgeable in-process capability. Merely accepting
an arbitrary caller-supplied PipelineRun must not issue provenance.

Validate N,M,m, center=floor((N-1)/2), D, spec.M, actual output.bits==spec.P,
and pair-index order/range. Derive support by an O(S) copy of output.pairs or
validate equality to run.candidates in O(S); retain zero estimates. Do not
scan source.values, hash an M-vector or re-sort an already canonical support.
Bind any 32-byte association label to that context; it remains a label, not
authentication on its own. The separate zero-input branch bypasses this stage.

Keep this trusted-driver boundary explicit: an in-process capability protects
against accidental/structural cross-run substitution under the declared trusted
program model; it is not a hostile-process security or cryptographic claim.

### B. Factor and review a production coefficient candidate

Propose outer_coefficients.py with immutable validated parameters, exact support
enumeration, private issuance of incidence records and an evaluator that accepts
only records bound to the same context. Keep a bounded mathematical-fixture
entrypoint separately labeled for the m57 test; it must never assert real
front-end provenance. A record should bind label/context, k, ell, J,K,p and the
output Cartesian enclosures/certificate. Validate exact built-in types and
support/incidence membership before numerical work. Do not reuse the mutable
Reference object verbatim as an accepted production interface.

Implement signed odd/even endpoint powers and preserve the reviewed precision
recurrence. Guard t<M before numerical setup; initialize pi/sqrt only on the
first actual emission. Stream emitted records and reject mixed contexts,
modified headers, substituted indices and malformed numeric fields.

### C. Use two finite integration controls with distinct claim boundaries

1. Provenance/API control: after source review and any required historical-code
   execution permission, a small actual constructor/pipeline run can be handed
   to the adapter by the trusted driver. Existing accepted fixtures check the
   dense-required boundary only. A separately approved reduced fixture such as
   N=257,M=2048,D=5 (m=11,s=55,t=1764<M) could exercise a nonempty sparse-outer
   interface. Its B,r,P,q_select and schedules must be explicitly declared and
   validated as reduced component parameters. Derive actual support from the
   actual run; do not assume its output or promote it to theorem-valid sampling.
   Enumerate bounded support, then select only a declared small number of
   actual retained records for coefficient evaluation. Charge the whole
   constructor/front-end separately; no theorem-sized execution is needed.
2. Large-denominator kernel control: route the three preserved m57/s285 records
   through the newly reviewed production coefficient implementation at
   J=587,K=623,p=459. Retain the four-support 9,123-incidence enumeration,
   n_u=1, zero limit, negative ratio and signed-power sentinel. Mark its origin
   as an authorized mathematical fixture, not an accepted PipelineRun. This
   tests the production kernel but cannot by itself close live provenance.

Reject a structural foreign output, same-valued substituted output/source/spec,
cross-run record, altered support order/index, wrong front-end P, wrong outer
p/K, stale binding, wrong N/M and out-of-domain ell/k. Include empty support,
zero estimates and t>=M with zero scalar preparation. Freeze the exact rejection
codes/prefix charges before execution. A certificate failure is a defect, not a
permitted random recovery event.

### D. Preserve oracle separation and paid accounting

The frozen regression source SHA-256 is
e2226910c0abdc5a3fd0da5bdc6c0262db6c83248d26fa12340582a191c681be.
Its oracle uses pi=4 atan(1/2)+4 atan(1/3), interval-Horner sine, restoring sqrt
and repeated odd powers. Keep those formulas and its B=900 precision separate
from production Machin/point-Taylor/square-and-multiply calls. Do not replace
the oracle with production output or share a production Scalar cache. Sharing
simple arithmetic helpers is already disclosed and requires independent review.
Have a separate reviewer inspect the new production and oracle sources; the
current experiment is same-agent implementation diversity only.

Charge upstream constructor/front-end work separately and cumulatively. For
outer work charge header/support validation, support copying, context/label
issuance, all endpoint/reduction operations, pi/sqrt setup, scalar/factorial
loops, powers/shifts, divisions, rounding, certificates, emitted records and
control/address work. Preserve the bound

    O_D((S+1)m^2 + 1_{E>0}m^5 + E*m^5)

for this component only. Do not reset ledgers on retries or revalidation; pay
retained record storage and any sorting/cache/serialization separately. No
N-row phase preparation is allowed. N accumulators, estimate multiplication,
scale-back and N output work belong to the still-separate outer composition.

Freeze every source hash, test scope and launcher cap; compare pre/post hashes
and retain normal process-exit receipts. This plan grants no execution of the
historical modules. The present inspection only parses their source as data.

## Stopping condition

The bounded identification task is complete: the actual accepted endpoint and
the missing adapter/evaluator are identified, with exact input/output mismatches
and an implementable split-gate plan. No production file has been invented,
created or accepted. Full-stream scatter, accumulation, scale-back, dense
fallback/all-length dispatch and independent amplification remain later gates.
