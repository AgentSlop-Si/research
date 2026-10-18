# Degree-eleven N13 certificate

Primary result: REPORT.md proves an explicit original-grammar sixteen-bank
witness over F_(53^11), and exact optimality using the accepted field-uniform
lower bound. Final independent reviewer acceptance is pending.

## Primary files

* DEGREE11_LITERAL_CERTIFICATE.json: all nodes, guards, 208 raw weights,
  208 amplitudes, support polynomial, and final 13-by-13 matrix.
* independent_literal_check.py: self-contained standard-library checker
  from inert JSON; establishes the field and checks literal original banks
  using backward recurrence, not the discovery algorithm.
* INDEPENDENT_LITERAL_RESULT.json: its complete arithmetic receipt.
* verify_literal.cpp: actual-root sector solver, raw-weight construction,
  Gauss-Jordan literal inverse checks, certificate generation.
* search_nonstable.cpp: deterministic extension-valued discovery and shared
  C++ arithmetic definitions; its search main is not executed by the literal
  verifier. candidate_data.h is exact inert input for that verifier.
* DEGREE11_LITERAL_RESULT.json: C++ literal verification receipt.
* NONSTABLE_CANDIDATE.json: frozen first splitting candidate, clearly
  distinct from the completed literal certificate.
* OPERATION_LEDGER.md: finite work and paid-interface accounting.
* SOURCE_PINS.json and sources/: exact immutable accepted dependencies.

The word independent in the Python filenames means a separately authored
implementation by this worker. It does not denote an external reviewer.

## Supporting bounded obstruction

PRIME_CROSS_OBSTRUCTION.md is a separate new theorem: when both cross nodes
belong to F53*, the minimum is 18 for gcd(d,210)=1 even with unrestricted
extension-valued same-sign annihilators. explore_cross_gate.py produces all
2,704 exact quadratic obstructions. independent_cross_check.py verifies them
using another Gaussian-coefficient construction and linear-solve procedure.
Their inert outputs are CROSS_GATE_CENSUS.json and
INDEPENDENT_CROSS_ARITHMETIC.json. This obstruction is compatible with the
main d=11 witness because its cross nodes are nonbase.

Run scripts in a disposable directory because they write receipts. See
REPORT.md for reproduction commands. MANIFEST.json binds the final packet;
replay receipts include hashes of frozen certificates. No uploaded,
committed or published state is claimed.
