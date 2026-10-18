# Dependency and execution provenance

All work in this packet was local. No repository, research-register, or external service mutation was attempted.

The new theorem was developed after reading these accepted predecessor scopes:

- nonconstant_buckets_completion_20261017_2130: proof, contract, numerical
  engine and live adapter
- nonconstant_buckets_final_review_20261017_2144: full final review
- sparse_supplier_completion_20261017_2130: proof and complete supplier source
- sparse_supplier_final_review_20261017_2144: full final review
- cycle_subgates_table_20261017_2148: retained scope and next-action plan

Unmodified local dependencies were copied into vendor and pinned before use:

- nonconstant_buckets.py:
  9b6accac4781c07a7e06acfa4239762b0cf21503bf619d7138971ce0c00d9993
- sparse_adapter.py:
  cdbe745859a7f729c26e43f1476bacb5d8ee0f0ee656ab5bf2674e102332efa7
- vendor/sparse_supplier.py:
  5c1454ef006d34c91be02643a57ebf4cd47adaf9aaaf85fb951e98095ca439ed

The accepted engines were executed as dependencies of the new recovery
pipeline. Their earlier check suites were not executed or imported. No
predecessor test result is counted as new recovery evidence. New production
work is recovery.py; new evidence is live_checks.py and replay_checks.py.

The provider receives the original sparse input because that is the explicitly
accepted deployment family. The recovery decoder receives only finite dense
bucket arrays and source-independent K(d) intervals. The test harness's input
comparison and good-isolation check are evaluation controls, not hidden data
available to the decoder. This distinction is a logical API audit under trusted
execution, not an operating-system security boundary against malicious code.

The reproduction uses a fixed explicit sigma=10007, not an attested random
draw. The probability theorem separately assumes 27 unbiased random bits and
an input fixed independently of that draw. Numerical error bounds hold against
all permitted per-call errors on the good isolation event, so no independence
of numerical errors is required.

This packet has author-run controls and full semantic replay. It does not yet
have independent final acceptance. Earlier reviews apply only to the unchanged
dependency scopes, not automatically to the new recovery theorem.
